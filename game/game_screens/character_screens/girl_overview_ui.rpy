screen person_info_detailed(the_person):
    add "Paper_Background.png"
    modal True
    zorder 100
    default hr_base = the_person.charisma*3 + the_person.hr_skill*2 + the_person.int + 10
    default market_base = the_person.charisma*3 + the_person.market_skill*2 + the_person.focus + 10
    default research_base = the_person.int*3 + the_person.research_skill*2 + the_person.focus + 10
    default prod_base = the_person.focus*3 + the_person.production_skill*2 + the_person.int + 10
    default supply_base = the_person.focus*3 + the_person.supply_skill*2 + the_person.charisma + 10
    use tooltip_screen()

    vbox:
        spacing 25
        xalign 0.5
        xanchor 0.5
        yalign 0.2
        frame:
            xsize 1750
            ysize 120
            xalign 0.5
            background "#1a45a1aa"
            vbox:
                xalign 0.5 xanchor 0.5
                text "[the_person.name] [the_person.last_name]" style "menu_text_style" size 30 xalign 0.5 yalign 0.5 yanchor 0.5 color the_person.char.who_args["color"] font the_person.char.what_args["font"]
                if not mc.business.get_employee_title(the_person) == "None":
                    text "Position: " + mc.business.get_employee_title(the_person) + " ($[the_person.salary]/day)" style "menu_text_style" xalign 0.5 yalign 0.5 yanchor 0.5

                $ visible_roles = []
                $ role_string = "Special Roles: "
                python:
                    for role in the_person.special_role:
                        if not role.hidden:
                            visible_roles.append(role.role_name)

                    if visible_roles:
                        role_string += visible_roles[0]
                        for role in visible_roles[1::]: #Slicing off the first manually let's us use commas correctly.
                            role_string += ", " + role
                if visible_roles:
                    text role_string style "menu_text_style" xalign 0.5 yalign 0.5 yanchor 0.5

        hbox:
            xsize 1750
            xalign 0.5
            xanchor 0.5
            spacing 30
            frame:
                background "#1a45a1aa"
                xsize 325
                ysize 450
                vbox:
                    text "Status and Info" style "menu_text_style" size 22
                    text "Happiness: [the_person.happiness]" style "menu_text_style"
                    text "Suggestibility: [the_person.suggestibility]" style "menu_text_style"
                    text "Sluttiness: [the_person.sluttiness]" style "menu_text_style"
                    text "Love: [the_person.love]" style "menu_text_style"
                    text "Obedience: [the_person.obedience] - " + get_obedience_plaintext(the_person.obedience) style "menu_text_style"

                    text "Age: [the_person.age]" style "menu_text_style"
                    text "Cup Size: [the_person.tits]" style "menu_text_style"
                    if girlfriend_role in the_person.special_role:
                        text "Relationship: Girlfriend" style "menu_text_style"
                    else:
                        text "Relationship: [the_person.relationship]" style "menu_text_style"

                    if the_person.relationship != "Single":
                        text "Significant Other: [the_person.SO_name]" style "menu_text_style"
                    elif girlfriend_role in the_person.special_role:
                        text "Significant Other: [mc.name]" style "menu_text_style"

                    text "Kids: [the_person.kids]" style "menu_text_style"
                    #TODO: Decide how much of this information we want to give to the player directly and how much we want to have delivered in game.
                    if persistent.pregnancy_pref > 0:
                        if persistent.pregnancy_pref == 1:
                            text "Fertility: " + str(round(the_person.fertility_percent)) + "%" style "menu_text_style"
                        if persistent.pregnancy_pref == 2:
                            $ modified_fertility = the_person.calculate_realistic_fertility()
                            text "Fertility: " + str(round(modified_fertility)) + "%" style "menu_text_style"
                            text "Monthly Peak Day: " + str(the_person.ideal_fertile_day ) style "menu_text_style"
                            #TODO: replace this with less specific info. Replace fertility peak with the_person.fertility_cycle_string()

                        if the_person.event_triggers_dict.get("birth_control_status", None) is None:
                            text "Birth Control: Unknown" style "menu_text_style" size 16
                        else:
                            if the_person.event_triggers_dict.get("birth_control_status"):
                                #text "Taking Birth Control: Yes" style "menu_text_style"
                                text "Birth Control: Yes {size=12}(Known " + str(day - the_person.event_triggers_dict.get("birth_control_known_day")) + " days ago){/size}" style "menu_text_style" size 16
                            else:
                                text "Birth Control: No {size=12}(Known " + str(day - the_person.event_triggers_dict.get("birth_control_known_day")) + " days ago){/size}" style "menu_text_style" size 16
                        #text "Birth Control: " + str(the_person.on_birth_control) style "menu_text_style" #TODO less specific info

            frame:
                background "#1a45a1aa"
                xsize 325
                ysize 450
                vbox:
                    text "Characteristics" style "menu_text_style" size 22
                    text "Charisma: [the_person.charisma]" style "menu_text_style"
                    text "Intelligence: [the_person.int]" style "menu_text_style"
                    text "Focus: [the_person.focus]" style "menu_text_style"

                    $ list_of_relationships = town_relationships.get_relationship_type_list(the_person, visible = True)
                    if list_of_relationships:
                        text "Other relationships:"  style "menu_text_style"
                        viewport:
                            xsize 325
                            yfill True
                            scrollbars "vertical"
                            mousewheel True
                            vbox:
                                for relationship in list_of_relationships:
                                    #TODO: Once we have more relationship stuff going on make this only show when the relationship is known.
                                    text "    " + relationship[0].name + " " + relationship[0].last_name + " - " + relationship[1] style "menu_text_style" size 14
            frame:
                background "#1a45a1aa"
                xsize 325
                ysize 450
                vbox:
                    text "Work Skills" style "menu_text_style" size 22
                    text "HR Skill: [the_person.hr_skill]" style "menu_text_style"
                    text "Marketing Skill: [the_person.market_skill]" style "menu_text_style"
                    text "Researching Skill: [the_person.research_skill]" style "menu_text_style"
                    text "Production Skill: [the_person.production_skill]" style "menu_text_style"
                    text "Supply Skill: [the_person.supply_skill]" style "menu_text_style"

            frame:
                background "#1a45a1aa"
                xsize 325
                ysize 450
                vbox:
                    text "Sex Skills" style "menu_text_style" size 22
                    text "Foreplay Skill: " + str(the_person.sex_skills["Foreplay"]) style "menu_text_style"
                    text "Oral Skill: " + str(the_person.sex_skills["Oral"]) style "menu_text_style"
                    text "Vaginal Skill: " + str(the_person.sex_skills["Vaginal"]) style "menu_text_style"
                    text "Anal: " + str(the_person.sex_skills["Anal"]) style "menu_text_style"
                    text "Novelty: " + str(the_person.novelty) + "%" style "menu_text_style"
                    text "Sex Record:"  style "menu_text_style" size 22
                    viewport:
                        xsize 325
                        yfill True
                        scrollbars "vertical"
                        mousewheel True
                        vbox:
                            for the_record in the_person.sex_record:
                                text the_record + ": " + str(the_person.sex_record.get(the_record, 0)) style "menu_text_style" size 14
                            # for relationship in list_of_relationships:
                            #     #TODO: Once we have more relationship stuff going on make this only show when the relationship is known.
                            #     text "    " + relationship[0].name + " " + relationship[0].last_name + " - " + relationship[1] style "menu_text_style" size 14

            frame:
                background "#1a45a1aa"
                xsize 325
                ysize 450
                vbox:
                    use serum_tolerance_indicator(the_person)

                    text "Currently Affected By:" style "menu_text_style" size 22
                    if the_person.serum_effects:
                        default selected_serum = None
                        for serum in the_person.serum_effects:
                            if serum == selected_serum:
                                textbutton serum.name + " : " + str(serum.duration - serum.duration_counter) + " Turns Left":
                                    action [SetScreenVariable("selected_serum", None), Hide("serum_tooltip")]
                                    style "textbutton_style"
                                    text_style "textbutton_text_style"
                                    text_size 12
                                    background "#888888"
                            else:
                                textbutton serum.name + " : " + str(serum.duration - serum.duration_counter) + " Turns Left":
                                    action SetScreenVariable("selected_serum", serum)
                                    hovered [SetScreenVariable("selected_serum", None), Show("serum_tooltip", None, serum, given_align = (0.4,0.1), given_anchor = (0.0,0.0))]
                                    unhovered Hide("serum_tooltip")
                                    style "textbutton_style"
                                    text_style "textbutton_text_style"
                                    text_size 12

                    else:
                        text "No active serums." style "menu_text_style"

                    null height 20


        hbox:
            xsize 1750
            spacing 30
            $ master_opinion_dict = dict(the_person.opinions, **the_person.sexy_opinions)
            frame:
                background "#1a45a1aa"
                xsize 415
                ysize 200
                vbox:
                    text "Loves" style "menu_text_style" size 22
                    for opinion in master_opinion_dict:
                        if master_opinion_dict[opinion][0] == 2:
                            if master_opinion_dict[opinion][1]:
                                text "   " + opinion style "menu_text_style"
                            else:
                                text "   ????" style "menu_text_style"

            frame:
                background "#1a45a1aa"
                xsize 415
                ysize 200
                vbox:
                    text "Likes" style "menu_text_style" size 22
                    for opinion in master_opinion_dict:
                        if master_opinion_dict[opinion][0] == 1:
                            if master_opinion_dict[opinion][1]:
                                text "   " + opinion style "menu_text_style"
                            else:
                                text "   ????" style "menu_text_style"

            frame:
                background "#1a45a1aa"
                xsize 415
                ysize 200
                vbox:
                    text "Dislikes" style "menu_text_style" size 22
                    for opinion in master_opinion_dict:
                        if master_opinion_dict[opinion][0] == -1:
                            if master_opinion_dict[opinion][1]:
                                text "   " + opinion style "menu_text_style"
                            else:
                                text "   ????" style "menu_text_style"

            frame:
                background "#1a45a1aa"
                xsize 415
                ysize 200
                vbox:
                    text "Hates" style "menu_text_style" size 22
                    for opinion in master_opinion_dict:
                        if master_opinion_dict[opinion][0] == -2:
                            if master_opinion_dict[opinion][1]:
                                text "   " + opinion style "menu_text_style"
                            else:
                                text "   ????" style "menu_text_style"

    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action [Hide("serum_tooltip"), Hide("person_info_detailed")]
        textbutton "Return" align [0.5,0.5] text_style "return_button_style"
