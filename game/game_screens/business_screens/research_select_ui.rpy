screen research_select_ui: #How you select serum and trait research
    default selected_research = None #If not None a screen is shown, including a "begin research" button or an "unlock and research" button.
    add "Science_Menu_Background.png"
    modal True

    $ all_tiers = [0,1,2,3]
    $ tier_zero = [0]
    $ tier_one = [1]
    $ tier_two = [2]
    $ tier_three = [3]

    default sort_method = alpha_sort
    default sort_reversed = False

    default allowed_tiers = all_tiers

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
                vbox:
                    text "Research New Traits" style "menu_text_style" size 20 xanchor 0.5 xalign 0.5
                    hbox:
                        xsize 300
                        spacing 0
                        $ tier_sort_dict = OrderedDict([("All", all_tiers), ("T0", tier_zero), ("T1", tier_one), ("T2", tier_two), ("T3", tier_three)])
                        $ tier_number = 0
                        for tier_name in tier_sort_dict:
                            if allowed_tiers == tier_sort_dict[tier_name] and tier_number <= mc.business.research_tier:
                                $ button_sensitive = False
                            else:
                                $ button_sensitive = True

                            $ tier_number += 1
                            textbutton tier_name action SetScreenVariable("allowed_tiers", tier_sort_dict[tier_name]) sensitive button_sensitive xsize 55 ysize 40 style "textbutton_style" text_style "textbutton_text_style" text_align (0.5,0.5) text_anchor (0.5,0.5) text_size 16

                    viewport: #Research new traits
                        xsize 320
                        ysize 785
                        scrollbars "vertical"
                        mousewheel True
                        vbox:
                            xsize 320
                            spacing 0
                            $ sorted_traits_list = list_of_traits+mc.business.blueprinted_traits
                            if not sort_method == alpha_sort:
                                $ sorted_traits_list = sorted(sorted_traits_list, key = alpha_sort) # If we're sorting by something other than alphabetical also sort by alphabetical after.
                            $ sorted_traits_list = sorted(sorted_traits_list, key=sort_method, reverse = sort_reversed)

                            for trait in sorted_traits_list:
                                if not trait.researched and trait.has_required() and trait.tier in allowed_tiers:
                                    if trait.research_needed > 10000: #Assume very high values are impossible #TODO: Just make this a boolean we can toggle on each trait.
                                        $ research_needed_string = "\nResearch Impossible"
                                    else:
                                        $ research_needed_string = "(" +str(trait.current_research)+"/"+ str(trait.research_needed) + ")"
                                    $ trait_title = trait.name + " " + research_needed_string
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

                    hbox:
                        yalign 1.0
                        yanchor 1.0
                        xanchor 0.5
                        xalign 0.5
                        $ serum_sort_buttons = OrderedDict([("ABC", alpha_sort), \
                            ("{color=#0049d8}Men{/color}", men_sort), ("{color=#00AA00}Phy{/color}", phys_sort), \
                            ("{color=#FFC0CB}Sex{/color}", sex_sort), ("{color=#FFFFFF}Med{/color}", med_sort), \
                            ("{color=#BBBBBB}Flaw{/color}", flaw_sort), ("{color=#FF6249}Attn{/color}", attn_sort)])
                        for sort_button in serum_sort_buttons:
                            $ sort_name = sort_button
                            $ background_colour = "#000080"
                            if serum_sort_buttons[sort_button] == sort_method:
                                $ background_colour = "#4040c0"
                                $ button_action = ToggleScreenVariable("sort_reversed")
                                if sort_reversed:
                                    $ sort_name += " ^" #TODO: Get the proper unicode here.
                                else:
                                    $ sort_name += " v" #TODO: and here
                            else:
                                $ button_action = [SetScreenVariable("sort_method", serum_sort_buttons[sort_button]), SetScreenVariable("sort_reversed", False)]

                            textbutton sort_name:
                                action button_action sensitive button_sensitive
                                background background_colour insensitive_background "#222222" hover_background "#aaaaaa"
                                xsize 50 ysize 40 style "textbutton_style" text_style "textbutton_text_style" text_align (0.5,0.5) text_anchor (0.5,0.5) text_size 12



                vbox:
                    xsize 320
                    text "Master Existing Traits:" style "menu_text_style" size 20 xanchor 0.5 xalign 0.5
                    viewport: #Master Existing traits
                        xsize 320
                        ysize 800
                        scrollbars "vertical"
                        mousewheel True
                        vbox:
                            xsize 320


                            for trait in sorted(sorted(list_of_traits, key = lambda trait: trait.exclude_tags, reverse = True), key=lambda trait: trait.tier, reverse = True):
                                if trait.researched:
                                    if trait.research_needed > 10000: #Assume very high values are impossible #TODO: Just make this a boolean we can toggle on each trait.
                                        $ research_needed_string = "Research Impossible"
                                    else:
                                        $ research_needed_string = "(" +str(trait.current_research)+"/"+ str(trait.research_needed) + ")"

                                    $ side_effect_chance = trait.get_effective_side_effect_chance()
                                    if side_effect_chance >= 10000: #If it's a massively high side effect chance assume it's a special trait and it's just guarnateed.
                                        $ side_effect_chance_string = "Always Guaranteed"
                                    else:
                                        $ side_effect_chance_string = str(side_effect_chance) + "%"
                                    $ trait_title = trait.name + " " + research_needed_string + "\nMastery Level: " + str(trait.mastery_level) + "\nSide Effect Chance: " + side_effect_chance_string
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

                vbox:
                    xsize 320
                    text "Research New Designs:" style "menu_text_style" size 20 xanchor 0.5 xalign 0.5
                    viewport: #Research new designs
                        xsize 320
                        ysize 800
                        scrollbars "vertical"
                        mousewheel True
                        vbox:
                            xsize 320

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

            elif isinstance(selected_research, SerumTrait):
                if not selected_research.unlocked:
                    if isinstance(selected_research, SerumTraitBlueprint):
                        $ button_name = "Design and Unlock Trait"
                    else:
                        $ button_name = "Unlock and Begin Research"
                    $ button_name += "\nCosts: " + str(selected_research.clarity_cost) + " Clarity"
                    if selected_research.clarity_cost > mc.free_clarity:
                        $ button_sensitive = False
                    else:
                        $ button_actions.append(Function(mc.business.set_serum_research, selected_research.unlock_trait))
                        $ button_actions.append(SetScreenVariable("selected_research", None)) #Unlocking SerumTraitBlueprints might have changed what was selected.

                elif not selected_research.researched:
                    $ button_name = "Continue Unlocked Research"
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
