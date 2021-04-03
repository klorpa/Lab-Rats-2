screen outfit_select_manager(slut_limit = 999, show_outfits = True, show_overwear = True, show_underwear = True, main_selectable = True, show_make_new = True, show_export = True, show_modify = True, show_duplicate = True, show_delete = True):
    #If sluttiness_limit is passed, you cannot exit the creator until the proposed outfit has a sluttiness below it (or you create nothing).
    add "Paper_Background.png"
    modal True
    zorder 100
    default preview_outfit = None

    $ outfit_info_array = []
    ## ["Catagory name", is_catagory_enabled, "return value when new is made", slut score calculation field/function, "export field type", add_outfit_to_wardrobe_function] ##
    $ outfit_info_array.append([show_outfits, "Full Outfit", "new_full", Outfit.get_slut_requirement , "FullSets", Wardrobe.add_outfit, Wardrobe.get_outfit_list])
    $ outfit_info_array.append([show_overwear, "Overwear Set", "new_over", Outfit.get_overwear_slut_score, "OverwearSets",  Wardrobe.add_overwear_set, Wardrobe.get_overwear_sets_list])
    $ outfit_info_array.append([show_underwear, "Underwear Set", "new_under", Outfit.get_underwear_slut_score, "UnderwearSets", Wardrobe.add_underwear_set, Wardrobe.get_underwear_sets_list])

    hbox:
        spacing 20
        xalign 0.1
        yalign 0.1
        for catagory_info in outfit_info_array:
            if catagory_info[0]:
                frame:
                    background "#888888"
                    xsize 450
                    ysize 850
                    viewport:
                        scrollbars "vertical"
                        xsize 450
                        ysize 850
                        mousewheel True
                        vbox:
                            spacing -10
                            text catagory_info[1] + "s" style "menu_text_style" size 30 #Add an s to make it plural so we can reuse the field in the new button. Yep, I'm that clever-lazy.
                            null height 10
                            if show_make_new:
                                textbutton "Create New " + catagory_info[1]:
                                    action Return(catagory_info[2])
                                    sensitive True
                                    style "textbutton_style"
                                    text_style "outfit_description_style"
                                    xsize 450

                                null height 35

                            for outfit in catagory_info[6](mc.designed_wardrobe):
                                textbutton outfit.name + " (Sluttiness " +str(catagory_info[3](outfit)) +")":
                                    action Return(["select",outfit.get_copy()])
                                    sensitive (catagory_info[3](outfit) <= slut_limit) and main_selectable
                                    hovered SetScreenVariable("preview_outfit", outfit.get_copy())
                                    unhovered SetScreenVariable("preview_outfit", None)
                                    style "textbutton_style"
                                    text_style "outfit_description_style"
                                    tooltip "Pick this outfit."
                                    xsize 450

                                if show_export or show_modify or show_duplicate or show_delete:
                                    hbox:
                                        spacing 0
                                        xsize 450
                                        if show_export:
                                            default exported = []
                                            textbutton "Export":
                                                action [Function(exported.append,outfit), Function(log_outfit, outfit, outfit_class = catagory_info[4], wardrobe_name = "Exported_Wardrobe"), Function(renpy.notify, "Outfit exported to Exported_Wardrobe.xml")]
                                                sensitive outfit not in exported
                                                hovered SetScreenVariable("preview_outfit", outfit.get_copy())
                                                unhovered SetScreenVariable("preview_outfit", None)
                                                style "textbutton_style"
                                                text_style "outfit_description_style"
                                                tooltip "Export this outfit. The export will be added as an xml section in game/wardrobes/Exported_Wardrobe.xml."
                                                xsize 100

                                        if show_modify:
                                            textbutton "Modify":
                                                action Return(["modify",outfit]) #If we are modifying an outfit just return it. outfit management loop will find which catagory it is in.
                                                sensitive (catagory_info[3](outfit) <= slut_limit)
                                                hovered SetScreenVariable("preview_outfit", outfit.get_copy())
                                                unhovered SetScreenVariable("preview_outfit", None)
                                                style "textbutton_style"
                                                text_style "outfit_description_style"
                                                tooltip "Modify this outfit."
                                                xsize 100

                                        if show_duplicate:
                                            $ the_copied_outfit = outfit.get_copy() #We make a copy to add to the wardrobe if this is selected. Otherwise continues same as "Modify"
                                            textbutton "Duplicate":
                                                action [Function(catagory_info[5], mc.designed_wardrobe, the_copied_outfit), Return(["duplicate",the_copied_outfit])]
                                                #sensitive (catagory_info[3](outfit) <= slut_limit)
                                                hovered SetScreenVariable("preview_outfit", outfit.get_copy())
                                                unhovered SetScreenVariable("preview_outfit", None)
                                                style "textbutton_style"
                                                text_style "outfit_description_style"
                                                tooltip "Duplicate this outfit and edit the copy, leaving the original as it is."
                                                xsize 100

                                        if show_delete:
                                            textbutton "Delete":
                                                action Function(mc.designed_wardrobe.remove_outfit, outfit)
                                                #sensitive (catagory_info[3](outfit) <= slut_limit)
                                                hovered SetScreenVariable("preview_outfit", outfit.get_copy())
                                                unhovered SetScreenVariable("preview_outfit", None)
                                                style "textbutton_style"
                                                text_style "outfit_description_style"
                                                tooltip "Remove this outfit from your wardrobe. This cannot be undone!"
                                                xsize 100

                                    null height 20

                                null height 25

        if slut_limit != 999:
            frame:
                background "#888888"
                text "Slut Limit: " + str(slut_limit) + "{image=gui/heart/red_heart.png}" style "textbutton_text_style" text_align 0.0
    frame:
        background None
        anchor [0.5,0.5]
        align [0.39,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action Return("No Return")
        textbutton "Return" align [0.5,0.5] text_style "return_button_style"

    fixed:
        pos (1450,0)
        add mannequin_average
        if preview_outfit:
            for cloth in preview_outfit.generate_draw_list(None,"stand3"):
                add cloth
