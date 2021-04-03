init -2 python:
    def colour_changed_r(new_value):
        if not new_value:
            new_value = 0

        try:
            new_value = float(new_value)
        except ValueError:
            new_value = 0

        if float(new_value) < 0:
            new_value = 0
        elif float(new_value) > 1:
            new_value = 1.0
        cs = renpy.current_screen()

        cs.scope["current_r"] = __builtin__.round(float(new_value),2)
        renpy.restart_interaction()

    def colour_changed_g(new_value):
        if not new_value:
            new_value = 0

        try:
            new_value = float(new_value)
        except ValueError:
            new_value = 0

        if float(new_value) < 0:
            new_value = 0
        elif float(new_value) > 1:
            new_value = 1.0
        cs = renpy.current_screen()

        cs.scope["current_g"] = __builtin__.round(float(new_value),2)
        renpy.restart_interaction()

    def colour_changed_b(new_value):
        if not new_value:
            new_value = 0

        try:
            new_value = float(new_value)
        except ValueError:
            new_value = 0

        if float(new_value) < 0:
            new_value = 0
        elif float(new_value) > 1:
            new_value = 1.0

        cs = renpy.current_screen()

        cs.scope["current_b"] = __builtin__.round(float(new_value),2)
        renpy.restart_interaction()

    def update_colour_palette(palette_index, new_r,new_g,new_b,new_a):
        persistent.colour_palette[palette_index] = [new_r,new_g,new_b,new_a]
        renpy.save_persistent()


screen outfit_creator(starting_outfit, outfit_type = "full", slut_limit = None): ##Pass a completely blank outfit instance for a new outfit, or an already existing instance to load an old one.\
    add "Paper_Background.png"
    modal True
    zorder 100
    default catagory_selected = "Panties"

    default demo_outfit = starting_outfit.get_copy()

    if outfit_type == "under":
        $ valid_layers = [0,1]
    elif outfit_type == "over":
        $ valid_layers = [2,3]
    else:
        $ valid_layers = [0,1,2,3]

    $ valid_catagories = ["Panties", "Bras", "Pants", "Skirts", "Dresses", "Shirts", "Socks", "Shoes", "Facial", "Rings", "Bracelets", "Neckwear"] #Holds the valid list of catagories strings to be shown at the top.

    $ catagories_mapping = {
        "Panties": [panties_list, Outfit.can_add_lower, Outfit.add_lower],  #Maps each catagory to the function it should use to determine if it is valid and how it should be added to the outfit.
        "Bras": [bra_list, Outfit.can_add_upper, Outfit.add_upper],
        "Pants": [pants_list, Outfit.can_add_lower, Outfit.add_lower],
        "Skirts": [skirts_list, Outfit.can_add_lower, Outfit.add_lower],
        "Dresses": [dress_list, Outfit.can_add_dress, Outfit.add_dress],
        "Shirts": [shirts_list, Outfit.can_add_upper, Outfit.add_upper],
        "Socks": [socks_list, Outfit.can_add_feet, Outfit.add_feet],
        "Shoes": [shoes_list, Outfit.can_add_feet, Outfit.add_feet],
        "Facial": [earings_list, Outfit.can_add_accessory, Outfit.add_accessory],
        "Rings": [rings_list, Outfit.can_add_accessory, Outfit.add_accessory],
        "Bracelets": [bracelet_list, Outfit.can_add_accessory, Outfit.add_accessory],
        "Neckwear": [neckwear_list, Outfit.can_add_accessory, Outfit.add_accessory]}

    default bar_select = 0 # 0 is nothing selected, 1 is red, 2 is green, 3 is blue, and 4 is alpha

    default selected_colour = "colour" #If secondary we are alterning the patern colour. When changed it updates the colour of the clothing item. Current values are "colour" and "colour_pattern"
    default current_r = 1.0
    default current_g = 1.0
    default current_b = 1.0
    default current_a = 1.0

    default hide_underwear = False
    default hide_base = False
    default hide_overwear = False

    default selected_clothing = None
    # $ current_colour = [1.0,1.0,1.0,1.0] #This is the colour we will apply to all of the clothing

    #Each catagory below has a click to enable button. If it's false, we don't show anything for it.
    #TODO: refactor this outfit creator to remove as much duplication as possible.

    hbox: #The main divider between the new item adder and the current outfit view.
        xpos 15
        yalign 0.5
        yanchor 0.5
        spacing 15
        frame:
            background "#aaaaaa"
            padding (20,20)
            xysize (880, 1015)
            hbox:
                spacing 15
                vbox: #Catagories select on far left
                    spacing 15
                    for catagory in valid_catagories:
                        textbutton catagory:
                            style "textbutton_style"
                            text_style "textbutton_text_style"
                            if catagory == catagory_selected:
                                background "#4f7ad6"
                                hover_background "#4f7ad6"
                            else:
                                background "#1a45a1"
                                hover_background "#3a65c1"
                            text_align(0.5,0.5)
                            text_anchor(0.5,0.5)
                            xysize (220, 60)
                            action [SetScreenVariable("catagory_selected",catagory), SetScreenVariable("selected_clothing", None), SetScreenVariable("selected_colour", "colour")] #Set the clothing to None when you change catagories to avoid breaking the clothing add function assignments
                vbox:
                    spacing 15
                    viewport:
                        ysize 480
                        xminimum 605
                        scrollbars "vertical"
                        mousewheel True
                        frame:
                            xsize 620
                            yminimum 480
                            background "#888888"
                            vbox:
                                #THIS IS WHERE ITEM CHOICES ARE SHOWN
                                if catagory_selected in catagories_mapping:
                                    $ valid_check = catagories_mapping[catagory_selected][1]
                                    $ apply_method = catagories_mapping[catagory_selected][2]
                                    $ cloth_list_length = len(catagories_mapping[catagory_selected][0])
                                    $ sorted_list = sorted(catagories_mapping[catagory_selected][0], key = lambda x: x.layer)
                                    $ sorted_list.sort(key = lambda x: x.slut_value)
                                    for cloth in sorted_list:
                                        $ is_sensitive = valid_check(starting_outfit, cloth) and cloth.layer in valid_layers
                                        if cloth.has_extension and cloth.has_extension.layer not in valid_layers:
                                            $ is_sensitive = False
                                        $ cloth_name = cloth.name.title()
                                        $ cloth_info = cloth.generate_stat_slug()

                                        frame:
                                            xsize 580
                                            ysize 50
                                            background "#00000000"
                                            textbutton cloth.name.title():
                                                xalign 0.0
                                                ysize 50
                                                style "textbutton_style"
                                                text_style "textbutton_text_style"
                                                if valid_check(starting_outfit, cloth):
                                                    background "#1a45a1"
                                                    hover_background "#3a65c1"
                                                else:
                                                    background "#444444"
                                                    hover_background "#444444"
                                                insensitive_background "#444444"
                                                xfill True
                                                sensitive is_sensitive
                                                action [SetScreenVariable("selected_clothing", cloth), SetScreenVariable("selected_colour", "colour")]
                                                hovered Function(apply_method, demo_outfit, cloth)
                                                unhovered Function(demo_outfit.remove_clothing, cloth)
                                            text cloth_info:
                                                style "textbutton_text_style"
                                                xalign 0.95
                                                yalign 1.0
                                                text_align 1.0

                    frame:
                        #THIS IS WHERE SELECTED ITEM OPTIONS ARE SHOWN
                        xysize (605, 480)
                        background "#888888"
                        vbox:
                            spacing 10
                            if selected_clothing is not None:
                                text selected_clothing.name + ", " + selected_clothing.generate_stat_slug() style "textbutton_text_style"
                                if __builtin__.type(selected_clothing) is Clothing: #Only clothing items have patterns, facial accessories do not (currently).
                                    hbox:
                                        spacing 5
                                        for pattern in selected_clothing.supported_patterns:
                                            textbutton pattern:
                                                style "textbutton_style"
                                                text_style "textbutton_text_style"
                                                if selected_clothing.pattern == selected_clothing.supported_patterns[pattern]:
                                                    background "#4f7ad6"
                                                    hover_background "#4f7ad6"
                                                else:
                                                    background "#1a45a1"
                                                    hover_background "#3a65c1"
                                                xfill False
                                                xsize 120
                                                text_xalign 0.5
                                                text_xanchor 0.5
                                                text_size 12
                                                sensitive True
                                                action SetField(selected_clothing,"pattern",selected_clothing.supported_patterns[pattern])

                                hbox:
                                    spacing -5 #We will manually handle spacing so we can have our colour predictor frames
                                    textbutton "Primary Colour":
                                        style "textbutton_style"
                                        text_style "textbutton_text_style"
                                        text_size 12
                                        xsize 120
                                        if selected_colour == "colour":
                                            background "#4f7ad6"
                                            hover_background "#4f7ad6"
                                        else:
                                            background "#1a45a1"
                                            hover_background "#3a65c1"
                                        sensitive True
                                        if selected_colour == "colour_pattern":
                                            action [SetField(selected_clothing,"colour_pattern",[current_r,current_g,current_b,current_a]), SetScreenVariable("selected_colour","colour"), SetScreenVariable("current_r",selected_clothing.colour[0]), SetScreenVariable("current_g",selected_clothing.colour[1]), SetScreenVariable("current_b",selected_clothing.colour[2]), SetScreenVariable("current_a",selected_clothing.colour[3])]
                                        else:
                                            action NullAction()

                                    frame:
                                        if selected_colour == "colour":
                                            background Color(rgb=(current_r,current_g,current_b,current_a))
                                        else:
                                            background Color(rgb=(selected_clothing.colour[0], selected_clothing.colour[1], selected_clothing.colour[2]))
                                        xysize (45,45)
                                        yanchor 0.5
                                        yalign 0.5

                                    if __builtin__.type(selected_clothing) is Clothing and selected_clothing.pattern is not None:
                                        null width 15
                                        textbutton "Pattern Colour":
                                            style "textbutton_style"
                                            text_style "textbutton_text_style"
                                            text_size 12
                                            xsize 120
                                            if selected_colour == "colour_pattern":
                                                background "#4f7ad6"
                                                hover_background "#4f7ad6"
                                            else:
                                                background "#1a45a1"
                                                hover_background "#3a65c1"
                                            sensitive True
                                            if selected_colour == "colour":
                                                action [SetField(selected_clothing,"colour",[current_r,current_g,current_b,current_a]), SetScreenVariable("selected_colour","colour_pattern"), SetScreenVariable("current_r",selected_clothing.colour_pattern[0]), SetScreenVariable("current_g",selected_clothing.colour_pattern[1]), SetScreenVariable("current_b",selected_clothing.colour_pattern[2]), SetScreenVariable("current_a",selected_clothing.colour_pattern[3])]
                                            else:
                                                action NullAction()
                                        frame:
                                            if selected_colour == "colour_pattern":
                                                background Color(rgb=(current_r,current_g,current_b,current_a))
                                            else:
                                                background Color(rgb=(selected_clothing.colour_pattern[0], selected_clothing.colour_pattern[1], selected_clothing.colour_pattern[2]))
                                            xysize (45,45)
                                            yanchor 0.5
                                            yalign 0.5

                                hbox:
                                    spacing 10
                                    vbox:
                                        text "Red" style "textbutton_text_style"
                                        hbox:
                                            if bar_select == 1:
                                                frame:
                                                    input default current_r length 4 changed colour_changed_r allow ".0123456789" style "menu_text_style"
                                                    xsize 70
                                                    ysize 50
                                            else:
                                                button:
                                                    background "#888888"
                                                    action SetScreenVariable("bar_select",1)
                                                    text "%.2f" % current_r style "menu_text_style"
                                                    xsize 70
                                                    ysize 50

                                            bar value ScreenVariableValue("current_r", 1.0) xsize 120 ysize 45 style style.slider unhovered SetScreenVariable("current_r",__builtin__.round(current_r,2))
                                    vbox:
                                        text "Green" style "textbutton_text_style"
                                        hbox:
                                            if bar_select == 2:
                                                frame:
                                                    input default current_g length 4 changed colour_changed_g allow ".0123456789" style "menu_text_style"
                                                    xsize 70
                                                    ysize 50
                                            else:
                                                button:
                                                    background "#888888"
                                                    action SetScreenVariable("bar_select",2)
                                                    text "%.2f" % current_g style "menu_text_style"
                                                    xsize 70
                                                    ysize 50

                                            bar value ScreenVariableValue("current_g", 1.0) xsize 120 ysize 45 style style.slider unhovered SetScreenVariable("current_g",__builtin__.round(current_g,2))
                                    vbox:
                                        text "Blue" style "textbutton_text_style"
                                        hbox:
                                            if bar_select == 3:
                                                frame:
                                                    input default current_b length 4 changed colour_changed_b allow ".0123456789" style "menu_text_style"
                                                    xsize 70
                                                    ysize 50
                                            else:
                                                button:
                                                    background "#888888"
                                                    action SetScreenVariable("bar_select",3)
                                                    text "%.2f" % current_b style "menu_text_style"
                                                    xsize 70
                                                    ysize 50

                                            bar value ScreenVariableValue("current_b", 1.0) xsize 120 ysize 45 style style.slider unhovered SetScreenVariable("current_b",__builtin__.round(current_b,2))

                                text "Transparency: " style "menu_text_style"
                                hbox:
                                    spacing 5
                                    for trans in ['1.0', '0.95', '0.9', '0.8', '0.75', '0.66', '0.5', '0.33', '0.25']:
                                        $ trans_name = str(int(float(trans)*100)) + "%"
                                        button:
                                            if current_a == float(trans):
                                                background "#4f7ad6"
                                            else:
                                                background "#1a45a1"
                                            text trans_name style "menu_text_style" xalign 0.5 xanchor 0.5 yalign 0.5 yanchor 0.5
                                            xysize (60, 40)
                                            action SetScreenVariable("current_a", float(trans))

                                hbox:
                                    spacing 5
                                    xalign 0.5
                                    xanchor 0.5
                                    for count, a_colour in __builtin__.enumerate(persistent.colour_palette):
                                        frame:
                                            background "#aaaaaa"
                                            button:
                                                background Color(rgb=(a_colour[0], a_colour[1], a_colour[2]))
                                                xysize (40,40)
                                                sensitive True
                                                action [SetScreenVariable("current_r", a_colour[0]), SetScreenVariable("current_g", a_colour[1]), SetScreenVariable("current_b", a_colour[2]), SetScreenVariable("current_a", a_colour[3])]
                                                alternate Function(update_colour_palette, count, current_r, current_g, current_b, current_a)



                        #TODO: Change this "Add" butotn to "Remove" when you're selecting something that is arleady part of the outfit.
                        if selected_clothing:
                            textbutton "Add to Outfit":
                                style "textbutton_style"
                                text_style "textbutton_text_style"
                                background "#1a45a1"
                                hover_background "#3a65c1"
                                xalign 0.5
                                yalign 1.0
                                xanchor 0.5
                                yanchor 1.0
                                sensitive valid_check(starting_outfit, selected_clothing)
                                action [SetField(selected_clothing, selected_colour,[current_r,current_g,current_b,current_a]), Function(apply_method, starting_outfit, selected_clothing)]
                                hovered [SetField(selected_clothing, selected_colour,[current_r,current_g,current_b,current_a]), Function(apply_method, demo_outfit, selected_clothing)]
                                unhovered Function(demo_outfit.remove_clothing, selected_clothing)




            # vbox: #Items selector
            #     #W/ item customixing window at bottom
            #
        vbox:
            spacing 15
            frame:
                xysize (440, 500)
                background "#aaaaaa"
                padding (20,20)
                vbox:
                    spacing 15
                    text "Current Items" style "textbutton_text_style"
                    frame:
                        xfill True
                        yfill True
                        background "#888888"
                        viewport:
                            ysize 500
                            xminimum 440
                            scrollbars "vertical"
                            mousewheel True
                            vbox:
                                spacing 5
                                for cloth in starting_outfit.upper_body + starting_outfit.lower_body + starting_outfit.feet + starting_outfit.accessories:
                                    if not cloth.is_extension: #Don't list extensions for removal.
                                        button:
                                            background Color(rgb = (cloth.colour[0], cloth.colour[1], cloth.colour[2]))
                                            xysize (380, 40)
                                            action [Function(starting_outfit.remove_clothing, cloth),Function(demo_outfit.remove_clothing, cloth)]
                                            xalign 0.5
                                            yalign 0.0
                                            text cloth.name xalign 0.5 xanchor 0.5 yalign 0.5 yanchor 0.5 style "outfit_style"

            frame:
                background "#aaaaaa"
                xysize (440, 500)
                padding (20,20)
                vbox:
                    yalign 0.0
                    text "Outfit Stats" style "menu_text_style" size 20

                    if outfit_type == "full":
                        text "Sluttiness (Full Outfit) : " + str(demo_outfit.slut_requirement) + "{image=gui/heart/red_heart.png}"style "menu_text_style"

                    if outfit_type == "under":
                        if demo_outfit.is_suitable_underwear_set():
                            text "Sluttiness (As Underwear): " + str(demo_outfit.get_underwear_slut_score()) + "{image=gui/heart/red_heart.png}" style "menu_text_style"
                        else:
                            text "Sluttiness (As Underwear): Invalid" style "menu_text_style"

                    elif outfit_type == "over":
                        if demo_outfit.is_suitable_overwear_set():
                            text "Sluttiness (As Overwear): " + str(demo_outfit.get_overwear_slut_score()) + "{image=gui/heart/red_heart.png}" style "menu_text_style"
                        else:
                            text "Sluttiness (As Overwear): Invalid" style "menu_text_style"
                    text "Tits Visible: " + str(demo_outfit.tits_visible()) style "menu_text_style" #TODO: Show what effects these are having on the outfit.
                    text "Tits Usable: " + str(demo_outfit.tits_available()) style "menu_text_style"
                    text "Wearing a Bra: " + str(demo_outfit.wearing_bra()) style "menu_text_style"
                    text "Bra Covered: " + str(demo_outfit.bra_covered()) style "menu_text_style"
                    text "Pussy Visible: " + str(demo_outfit.vagina_visible()) style "menu_text_style"
                    text "Pussy Usable: " + str(demo_outfit.vagina_available()) style "menu_text_style"
                    text "Wearing Panties: " + str(demo_outfit.wearing_panties()) style "menu_text_style"
                    text "Panties Covered: " + str(demo_outfit.panties_covered()) style "menu_text_style"

                    hbox:
                        yalign 1.0
                        xalign 0.5
                        xanchor 0.5
                        spacing 50
                        $ save_button_name = "Save Outfit"
                        if slut_limit is not None:
                            $ save_button_name += "\nLimit: " + str(slut_limit) + "{image=gui/heart/red_heart.png}"
                        $ slut_to_use = starting_outfit.slut_requirement
                        if outfit_type == "under":
                            $ slut_to_use = starting_outfit.get_underwear_slut_score()
                        elif outfit_type == "over":
                            $ slut_to_use = starting_outfit.get_overwear_slut_score()

                        textbutton save_button_name:
                            action Return(starting_outfit.get_copy())
                            style "textbutton_style"
                            text_style "textbutton_text_style" text_text_align 0.5 text_xalign 0.5 xysize (155,80)
                            sensitive slut_limit is None or slut_to_use <= slut_limit
                        textbutton "Abandon Design" action Return("Not_New") style "textbutton_style" text_style "textbutton_text_style" text_text_align 0.5 text_xalign 0.5 xysize (185,80)

        frame:
            background "#aaaaaa"
            xsize 180
            vbox:
                style_prefix "check"
                label "Show Layers" text_style "menu_text_style" text_size 22
                textbutton "Underwear" action ToggleScreenVariable("hide_underwear", False, True) text_size 20
                textbutton "Clothing" action ToggleScreenVariable("hide_base", False, True) text_size 20
                textbutton "Overwear" action ToggleScreenVariable("hide_overwear", False, True) text_size 20

    fixed: #TODO: Move this to it's own screen so it can be shown anywhere
        pos (1450,0)
        add mannequin_average
        # TODO: Add radio buttons to show or hide layers
        $ hide_list = []
        if hide_underwear:
            $ hide_list.append(1)
        if hide_base:
            $ hide_list.append(2)
        if hide_overwear:
            $ hide_list.append(3)
        for cloth in demo_outfit.generate_draw_list(None,"stand3", hide_layers = hide_list):
            add cloth

    imagebutton:
        auto "/tutorial_images/restart_tutorial_%s.png"
        xsize 54
        ysize 54
        yanchor 1.0
        xanchor 1.0
        xalign 1.0
        yalign 1.0
        action Function(mc.business.reset_tutorial,"outfit_tutorial")


    $ outfit_tutorial_length = 8 #The number of  tutorial screens we have.
    if mc.business.event_triggers_dict["outfit_tutorial"] > 0 and mc.business.event_triggers_dict["outfit_tutorial"] <= outfit_tutorial_length: #We use negative numbers to symbolize the tutorial not being enabled
        imagebutton:
            auto
            sensitive True
            xsize 1920
            ysize 1080
            idle "/tutorial_images/outfit_tutorial_"+__builtin__.str(mc.business.event_triggers_dict["outfit_tutorial"])+".png"
            hover "/tutorial_images/outfit_tutorial_"+__builtin__.str(mc.business.event_triggers_dict["outfit_tutorial"])+".png"
            action Function(mc.business.advance_tutorial,"outfit_tutorial")
