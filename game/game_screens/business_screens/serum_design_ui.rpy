screen serum_design_ui(starting_serum,current_traits):
    add "Science_Menu_Background.png"
    python:
        effective_traits = 0
        for trait_count in starting_serum.traits:
            if not "Production" in trait_count.exclude_tags:
                effective_traits += 1

    $ tooltip_anchor = (0.5,0.57)
    $ tooltip_align = (0.5,0.0)
    hbox:
        yalign 0.15
        xanchor 0.5
        xalign 0.5
        xsize 1080
        spacing 40
        frame:
            background "#888888"
            ysize 800
            vbox:
                xsize 550
                #text "Add a trait" style "menu_text_style" size 25 xanchor 0.5 xalign 0.5
                viewport:
                    xsize 550
                    ysize 480
                    scrollbars "vertical"
                    mousewheel True
                    frame:
                        xsize 550
                        background None
                        vbox:
                            xsize 530
                            text "Pick Production Type" style "menu_text_style" size 25 xanchor 0.5 xalign 0.5 xsize 530
                            for trait in sorted(sorted(list_of_traits, key = lambda trait: trait.exclude_tags, reverse = True), key=lambda trait: trait.tier, reverse = True): # Sort traits by exclude tags (So all production traits are grouped, for example), then by tier (so the highest tier production tag ends up at the top
                                if trait not in starting_serum.traits and trait.researched and "Production" in trait.exclude_tags:
                                    $ trait_tags = ""
                                    if trait.exclude_tags:
                                        $ trait_tags = " - "
                                        for a_tag in trait.exclude_tags:
                                            $ trait_tags += "[[" + a_tag + "]"
                                    $ trait_allowed = True
                                    python: # Check to see if the trait is excluded by any of the traits currently in the serum. A long looped segment only to deal with lists of tags, which are unlikely.
                                        for checking_trait in starting_serum.traits:
                                            for tag in trait.exclude_tags:
                                                for checking_tag in checking_trait.exclude_tags:
                                                    if tag == checking_tag:
                                                        trait_allowed = False
                                    $ side_effect_chance = trait.get_effective_side_effect_chance()
                                    if side_effect_chance >= 10000: #If it's a massively high side effect chance assume it's a special trait and it's just guarnateed.
                                        $ side_effect_chance_string = "Always Guaranteed"
                                    else:
                                        $ side_effect_chance_string = str(side_effect_chance) + "%"
                                    $ trait_side_effects = "\nMastery Level: " + str(trait.mastery_level) + " | Side Effect Chance: " + side_effect_chance_string
                                    textbutton trait.name + trait_tags + trait_side_effects:
                                        action [Hide("trait_tooltip"),Function(starting_serum.add_trait,trait)]
                                        sensitive trait_allowed
                                        style "textbutton_style"
                                        text_style "textbutton_text_style"
                                        hovered Show("trait_tooltip",None,trait, tooltip_anchor, tooltip_align)
                                        unhovered Hide("trait_tooltip")
                                        xsize 530

                            null height 30
                            text "Add Serum Traits" style "menu_text_style" size 25 xanchor 0.5 xalign 0.5 xsize 530
                            for trait in sorted(sorted(list_of_traits, key = lambda trait: trait.exclude_tags, reverse = True), key=lambda trait: trait.tier, reverse = True): # Sort traits by exclude tags (So all production traits are grouped, for example), then by tier (so the highest tier production tag ends up at the top
                                if trait not in starting_serum.traits and trait.researched and "Production" not in trait.exclude_tags:
                                    $ trait_tags = ""
                                    if trait.exclude_tags:
                                        $ trait_tags = " - "
                                        for a_tag in trait.exclude_tags:
                                            $ trait_tags += "[[" + a_tag + "]"
                                    $ trait_allowed = True
                                    python: # Check to see if the trait is excluded by any of the traits currently in the serum. A long looped segment only to deal with lists of tags, which are unlikely.
                                        for checking_trait in starting_serum.traits:
                                            for tag in trait.exclude_tags:
                                                for checking_tag in checking_trait.exclude_tags:
                                                    if tag == checking_tag:
                                                        trait_allowed = False
                                    $ side_effect_chance = trait.get_effective_side_effect_chance()
                                    if side_effect_chance >= 10000: #If it's a massively high side effect chance assume it's a special trait and it's just guarnateed.
                                        $ side_effect_chance_string = "Always Guaranteed"
                                    else:
                                        $ side_effect_chance_string = str(side_effect_chance) + "%"
                                    $ trait_side_effects = "\nMastery Level: " + str(trait.mastery_level) + " | Side Effect Chance: " + side_effect_chance_string
                                    textbutton trait.name + trait_tags + trait_side_effects:
                                        action [Hide("trait_tooltip"),Function(starting_serum.add_trait,trait)]
                                        sensitive trait_allowed
                                        style "textbutton_style"
                                        text_style "textbutton_text_style"
                                        hovered Show("trait_tooltip", None, trait, tooltip_anchor, tooltip_align)
                                        unhovered Hide("trait_tooltip")
                                        xsize 530 # Trait tooltip use to have an argument of ,0.315,0.57, corrisponding to x and yoffset, I think.

        frame:
            background "#888888"
            ysize 800
            vbox:
                xsize 550
                text "Remove a trait" style "menu_text_style" size 25 xanchor 0.5 xalign 0.5
                viewport:
                    xsize 550
                    ysize 480
                    scrollbars "vertical"
                    mousewheel True
                    frame:
                        xsize 550
                        background None
                        vbox:
                            for trait in starting_serum.traits:
                                $ trait_tags = ""
                                if trait.exclude_tags:
                                    $ trait_tags = " - "
                                    for a_tag in trait.exclude_tags:
                                        $ trait_tags += "[[" + a_tag + "]"
                                $ side_effect_chance = trait.get_effective_side_effect_chance()
                                if side_effect_chance >= 10000: #If it's a massively high side effect chance assume it's a special trait and it's just guarnateed.
                                    $ side_effect_chance_string = "Always Guaranteed"
                                else:
                                    $ side_effect_chance_string =  str(side_effect_chance) + "%"
                                $ trait_side_effects = "\nMastery Level: " + str(trait.mastery_level) + " | Side Effect Chance: " + side_effect_chance_string
                                textbutton trait.name + trait_tags + trait_side_effects:
                                    action[Hide("trait_tooltip"), Function(starting_serum.remove_trait,trait)]
                                    style "textbutton_style"
                                    text_style "textbutton_text_style"
                                    hovered Show("trait_tooltip",None,trait, tooltip_anchor, tooltip_align)
                                    unhovered Hide("trait_tooltip")
                                    xsize 550 #trait_tooltip use to have a value of ,0.635,0.57

        frame:
            background "#888888"
            ysize 800
            vbox:
                xsize 550
                text "Current Serum Statistics:" style "menu_text_style" size 25 xanchor 0.5 xalign 0.5
                if effective_traits > starting_serum.slots:
                    text "Trait Slots: " + str(effective_traits) +"/[starting_serum.slots]" style "menu_text_style" color "#DD0000" xanchor 0.5 xalign 0.5
                else:
                    text "Trait Slots: " + str(effective_traits) +"/[starting_serum.slots]" style "menu_text_style" xanchor 0.5 xalign 0.5
                hbox:
                    xanchor 0.5
                    xalign 0.5
                    spacing 10
                    xsize 550
                    for num in __builtin__.range(__builtin__.max(starting_serum.slots,effective_traits)):
                        if num < effective_traits and num < starting_serum.slots:
                            add "Serum_Slot_Full.png" xanchor 0.5 xalign 0.5
                        elif num < effective_traits and num >= starting_serum.slots:
                            add "Serum_Slot_Incorrect.png" xanchor 0.5 xalign 0.5
                        else:
                            add "Serum_Slot_Empty.png" xanchor 0.5 xalign 0.5
                grid 2 3 xanchor 0.5 xalign 0.5:
                    spacing 10
                    text "Research Required: [starting_serum.research_needed]" style "menu_text_style"
                    text "Production Cost: [starting_serum.production_cost]" style "menu_text_style"
                    text "Value: $[starting_serum.value]" style "menu_text_style"
                    $ calculated_profit = (starting_serum.value*mc.business.batch_size)-starting_serum.production_cost
                    if calculated_profit > 0:
                        text "Expected Profit:{color=#98fb98} $[calculated_profit]{/color}/dose" style "menu_text_style"
                    else:
                        $ calculated_profit = 0 - calculated_profit
                        text "Expected Profit:{color=#ff0000} -$[calculated_profit]{/color}/dose" style "menu_text_style"
                    text "Duration: [starting_serum.duration] Turns" style "menu_text_style"
                    text "Unlock Cost: [starting_serum.clarity_needed] Clarity" style "menu_text_style"

                text "Serum Effects:" style "menu_text_style" size 25 xanchor 0.5 xalign 0.5

                viewport:
                    xsize 550
                    scrollbars "vertical"
                    mousewheel True
                    frame:
                        xsize 550
                        background None
                        vbox:
                            for trait in starting_serum.traits:
                                text trait.name style "menu_text_style"
                                text "    "  + trait.positive_slug style "menu_text_style" color "#98fb98"
                                text "    "  + trait.build_negative_slug() style "menu_text_style" color "#ff0000"

    frame:
        background "#888888"
        xsize 250
        xanchor 0.5
        xalign 0.5
        yalign 0.9
        vbox:
            xanchor 0.5
            xalign 0.5
            textbutton "Create Design":
                action Return(starting_serum) sensitive (starting_serum.slots >= effective_traits and len(starting_serum.traits) and starting_serum.has_tag("Production")) > 0
                style "textbutton_style"
                text_style "textbutton_text_style"
                xanchor 0.5
                xalign 0.5
                xsize 230

            textbutton "Reject Design" action Return("None") style "textbutton_style" text_style "textbutton_text_style" xanchor 0.5 xalign 0.5 xsize 230

    imagebutton:
        auto "/tutorial_images/restart_tutorial_%s.png"
        xsize 54
        ysize 54
        yanchor 1.0
        xalign 0.0
        yalign 1.0
        action Function(mc.business.reset_tutorial,"design_tutorial")

    $ design_tutorial_length = 5 #The number of  tutorial screens we have.
    if mc.business.event_triggers_dict["design_tutorial"] > 0 and mc.business.event_triggers_dict["design_tutorial"] <= design_tutorial_length: #We use negative numbers to symbolize the tutorial not being enabled
        imagebutton:
            auto
            sensitive True
            xsize 1920
            ysize 1080
            idle "/tutorial_images/design_tutorial_"+__builtin__.str(mc.business.event_triggers_dict["design_tutorial"])+".png"
            hover "/tutorial_images/design_tutorial_"+__builtin__.str(mc.business.event_triggers_dict["design_tutorial"])+".png"
            action Function(mc.business.advance_tutorial,"design_tutorial")
