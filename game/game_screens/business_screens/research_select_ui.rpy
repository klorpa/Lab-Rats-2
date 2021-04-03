screen research_select_ui: #How you select serum and trait research
    default selected_research = None #If not None a screen is shown, including a "begin research" button or an "unlock and research" button.
    add "Science_Menu_Background.png"
    modal True
    vbox:
        xalign 0.1
        yalign 0.4
        frame:
            background "#888888"
            xsize 1000
            ymaximum 55
            if not mc.business.active_research_design == None:
                text "Current Research: [mc.business.active_research_design.name] " + str(int(mc.business.active_research_design.current_research)) + "/[mc.business.active_research_design.research_needed]":
                    style "menu_text_style" size 25
                    xanchor 0.0 xalign 0.0
                    yalign 0.0
            else:
                text "Current Research: None!":
                    style "menu_text_style" size 25
                    xanchor 0.0 xalign 0.0
                    yalign 0.0

            text "Available Clarity: [mc.free_clarity]":
                style "menu_text_style" size 25
                xanchor 1.0 xalign 1.0

        null height 20

        frame:
            background "#888888"
            ysize 900
            xsize 1000
            hbox:
                viewport: #Research new traits
                    xsize 320
                    ysize 800
                    scrollbars "vertical"
                    mousewheel True
                    vbox:
                        xsize 320
                        spacing 0
                        text "Research New Traits" style "menu_text_style" size 20 xanchor 0.5 xalign 0.5
                        for trait in sorted(sorted(list_of_traits, key = lambda trait: trait.exclude_tags, reverse = True), key=lambda trait: trait.tier, reverse = True):
                            if not trait.researched and trait.has_required():
                                $ trait_tags = ""
                                if trait.exclude_tags:
                                    $ trait_tags = "\nExcludes Other: "
                                    for a_tag in trait.exclude_tags:
                                        $ trait_tags += "[[" + a_tag + "]"

                                if trait.research_needed > 10000: #Assume very high values are impossible #TODO: Just make this a boolean we can toggle on each trait.
                                    $ research_needed_string = "Research Impossible"
                                else:
                                    $ research_needed_string = "(" +str(trait.current_research)+"/"+ str(trait.research_needed) + ")"
                                $ trait_title = trait.name + " " + research_needed_string  + trait_tags
                                textbutton trait_title:
                                    text_xalign 0.5
                                    text_text_align 0.5
                                    text_size 14
                                    action SetScreenVariable("selected_research", trait)
                                    style "textbutton_style"
                                    text_style "textbutton_text_style"
                                    if selected_research == trait:
                                        background "#59853f"
                                        hover_background "#a9d59f"
                                    else:
                                        background "#000080"
                                        hover_background "#1a45a1"
                                    xsize 300

                viewport: #Master Existing traits
                    xsize 320
                    ysize 800
                    scrollbars "vertical"
                    mousewheel True
                    vbox:
                        xsize 320
                        text "Master Existing Traits:" style "menu_text_style" size 20 xanchor 0.5 xalign 0.5

                        for trait in sorted(sorted(list_of_traits, key = lambda trait: trait.exclude_tags, reverse = True), key=lambda trait: trait.tier, reverse = True):
                            if trait.researched:
                                $ trait_tags = ""
                                if trait.exclude_tags:
                                    $ trait_tags = "\nExcludes Other: "
                                    for a_tag in trait.exclude_tags:
                                        $ trait_tags += "[[" + a_tag + "]"

                                if trait.research_needed > 10000: #Assume very high values are impossible #TODO: Just make this a boolean we can toggle on each trait.
                                    $ research_needed_string = "Research Impossible"
                                else:
                                    $ research_needed_string = "(" +str(trait.current_research)+"/"+ str(trait.research_needed) + ")"

                                $ side_effect_chance = trait.get_effective_side_effect_chance()
                                if side_effect_chance >= 10000: #If it's a massively high side effect chance assume it's a special trait and it's just guarnateed.
                                    $ side_effect_chance_string = "Always Guaranteed"
                                else:
                                    $ side_effect_chance_string = str(side_effect_chance) + "%"
                                $ trait_title = trait.name + " " + research_needed_string + trait_tags + "\nMastery Level: " + str(trait.mastery_level) + "\nSide Effect Chance: " + side_effect_chance_string
                                textbutton trait_title:
                                    text_xalign 0.5
                                    text_text_align 0.5
                                    text_size 14
                                    action SetScreenVariable("selected_research", trait)
                                    style "textbutton_style"
                                    text_style "textbutton_text_style"
                                    if selected_research == trait:
                                        background "#59853f"
                                        hover_background "#a9d59f"
                                    else:
                                        background "#000080"
                                        hover_background "#1a45a1"
                                    xsize 300

                viewport: #Research new designs
                    xsize 320
                    ysize 800
                    scrollbars "vertical"
                    mousewheel True
                    vbox:
                        xsize 320
                        text "Research New Designs:" style "menu_text_style" size 20 xanchor 0.5 xalign 0.5
                        for serum in mc.business.serum_designs:
                            if not serum.researched:
                                textbutton "[serum.name] ([serum.current_research]/[serum.research_needed])":
                                    text_xalign 0.5
                                    text_text_align 0.5
                                    text_size 14
                                    action SetScreenVariable("selected_research", serum)
                                    text_style "textbutton_text_style"
                                    style "textbutton_style"
                                    if selected_research == trait:
                                        background "#59853f"
                                        hover_background "#a9d59f"
                                    else:
                                        background "#000080"
                                        hover_background "#1a45a1"
                                    xsize 300

            textbutton "Return" action Return("None") style "textbutton_style" text_style "textbutton_text_style" yalign 0.995 xanchor 0.5 xalign 0.5

    if selected_research is not None:
        frame: #Frame that displays the info on the currently selected screen.
            xsize 600
            ysize 900
            background "#888888"
            xanchor 1.0
            xalign 0.9
            yanchor 1.0
            yalign 0.9
            $ button_name = ""
            $ button_actions = []
            $ button_sensitive = True

            if isinstance(selected_research, SerumTrait):
                use trait_tooltip(selected_research, given_align = (0.5,0.0), given_anchor = (0.5,0.0))
            elif isinstance(selected_research, SerumDesign):
                use serum_tooltip(selected_research, given_align = (0.5,0.0), given_anchor = (0.5,0.0))

            if selected_research == mc.business.active_research_design:
                $ button_name = "Halt Research"
                $ button_actions.append(Function(mc.business.set_serum_research,None))

            elif isinstance(selected_research, SerumTrait): #
                if not selected_research.unlocked:
                    $ button_name = "Unlock and Begin Research"
                    $ button_name += "\nCosts: " + str(selected_research.clarity_cost) + " Clarity"
                    if selected_research.clarity_cost > mc.free_clarity:
                        $ button_sensitive = False
                    else:
                        $ button_actions.append(Function(selected_research.unlock_trait))
                        $ button_actions.append(Function(mc.business.set_serum_research,selected_research))

                elif not selected_research.researched:
                    $ button_name = "Continue Unlock Research"
                    $ button_actions.append(Function(mc.business.set_serum_research,selected_research))

                else:
                    $ button_name = "Continue Mastery Research"
                    $ button_actions.append(Function(mc.business.set_serum_research,selected_research))

            elif isinstance(selected_research, SerumDesign):
                use serum_tooltip(selected_research, given_align = (0.5,0.0), given_anchor = (0.5,0.0))
                if not selected_research.unlocked:
                    $ button_name = "Unlock and Begin Research"
                    $ button_name += "\nCosts: " + str(selected_research.clarity_needed)
                    if selected_research.clarity_needed > mc.free_clarity:
                        $ button_sensitive = False
                    else:
                        $ button_actions.append(Function(selected_research.unlock_design))
                        $ button_actions.append(Function(mc.business.set_serum_research,selected_research))
                elif not selected_research.researched:
                    $ button_name = "Continue Unlock Research"
                    $ button_actions.append(Function(mc.business.set_serum_research,selected_research))
                else:
                    pass #Serum designs that are unlocked and researched shouldn't get here anyways.

            textbutton button_name:
                text_xalign 0.5
                text_text_align 0.5
                #text_size 14
                text_style "textbutton_text_style"
                style "textbutton_style"
                action button_actions
                sensitive button_sensitive
                xsize 300
                anchor (0.5,1.0)
                align (0.5,1.0)


    imagebutton:
        auto "/tutorial_images/restart_tutorial_%s.png"
        xsize 54
        ysize 54
        yanchor 1.0
        xalign 0.0
        yalign 1.0
        action Function(mc.business.reset_tutorial,"research_tutorial")

    $ research_tutorial_length = 5 #The number of  tutorial screens we have.
    if mc.business.event_triggers_dict["research_tutorial"] > 0 and mc.business.event_triggers_dict["research_tutorial"] <= research_tutorial_length: #We use negative numbers to symbolize the tutorial not being enabled
        imagebutton:
            auto
            sensitive True
            xsize 1920
            ysize 1080
            idle "/tutorial_images/research_tutorial_"+__builtin__.str(mc.business.event_triggers_dict["research_tutorial"])+".png"
            hover "/tutorial_images/research_tutorial_"+__builtin__.str(mc.business.event_triggers_dict["research_tutorial"])+".png"
            action Function(mc.business.advance_tutorial,"research_tutorial")
