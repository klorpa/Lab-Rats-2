init -2 python:
    def alpha_sort(a_trait):
        return a_trait.name

    def men_sort(a_trait):
        return -a_trait.mental_aspect

    def phys_sort(a_trait):
        return -a_trait.physical_aspect

    def sex_sort(a_trait):
        return -a_trait.sexual_aspect

    def med_sort(a_trait):
        return -a_trait.medical_aspect

    def flaw_sort(a_trait):
        return a_trait.flaws_aspect

    def attn_sort(a_trait):
        return a_trait.attention

screen serum_design_ui(starting_serum,current_traits):
    add "Science_Menu_Background.png"
    python:
        effective_traits = 0
        for trait_count in starting_serum.traits:
            if not "Production" in trait_count.exclude_tags:
                effective_traits += 1

    $ tooltip_anchor = (0.5,0.57)
    $ tooltip_align = (0.5,0.0)

    $ all_tiers = [0,1,2,3]
    $ tier_zero = [0]
    $ tier_one = [1]
    $ tier_two = [2]
    $ tier_three = [3]

    default sort_method = alpha_sort
    default sort_reversed = False


    default allowed_tiers = all_tiers
    hbox:
        yalign 0.15
        xanchor 0.5
        xalign 0.5
        xsize 1080
        spacing 40
        frame:
            background "#888888"
            ysize 900
            vbox:
                xsize 550
                if not starting_serum.has_production_trait():
                    text "Pick Production Method" style "menu_text_style" size 25 xanchor 0.5 xalign 0.5 xsize 530
                else:
                    text "Add Serum Traits" style "menu_text_style" size 25 xanchor 0.5 xalign 0.5 xsize 530
                hbox:
                    xanchor 0.5 xalign 0.5
                    $ tier_sort_dict = OrderedDict([("All", all_tiers), ("T0", tier_zero), ("T1", tier_one), ("T2", tier_two), ("T3", tier_three)])
                    for tier_name in tier_sort_dict:
                        if allowed_tiers == tier_sort_dict[tier_name]:
                            $ button_sensitive = False
                        else:
                            $ button_sensitive = True
                        textbutton tier_name action SetScreenVariable("allowed_tiers", tier_sort_dict[tier_name]) sensitive button_sensitive xsize 90 ysize 50 style "textbutton_style" text_style "textbutton_text_style" text_align (0.5,0.5) text_anchor (0.5,0.5)
                viewport:
                    xsize 550
                    ysize 760
                    scrollbars "vertical"
                    mousewheel True
                    frame:
                        xsize 550
                        background None
                        vbox:
                            xsize 530
                            $ sorted_traits_list = list_of_traits+mc.business.blueprinted_traits
                            if not sort_method == alpha_sort:
                                $ sorted_traits_list = sorted(sorted_traits_list, key = alpha_sort) # If we're sorting by something other than alphabetical also sort by alphabetical after.
                            $ sorted_traits_list = sorted(sorted_traits_list, key=sort_method, reverse = sort_reversed)

                            #TODO: Sort the trait list here. Sort by: Alpha, men, phy, sex, med, flaw, attention, going high or low (cycle through high low when clicked)
                            if not starting_serum.has_production_trait():
                                for trait in sorted_traits_list:
                                    if trait.researched and trait not in starting_serum.traits and "Production" in trait.exclude_tags and trait.tier in allowed_tiers:
                                        $ trait_allowed = starting_serum.trait_add_allowed(trait)
                                        use trait_select_button(trait, is_enabled = trait_allowed, the_action = Function(starting_serum.add_trait, trait), tooltip_anchor = (0.5, 0.57), tooltip_align = (0.5, 0.0))
                            else:
                                for trait in sorted_traits_list:
                                    if trait.researched and trait not in starting_serum.traits and "Production" not in trait.exclude_tags and trait.tier in allowed_tiers:
                                        $ trait_allowed = starting_serum.trait_add_allowed(trait)
                                        use trait_select_button(trait, is_enabled = trait_allowed, the_action = Function(starting_serum.add_trait, trait), tooltip_anchor = (0.5, 0.57), tooltip_align = (0.5, 0.0))

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
                            xsize 70 ysize 50 style "textbutton_style" text_style "textbutton_text_style" text_align (0.5,0.5) text_anchor (0.5,0.5) text_size 14

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
                                use trait_select_button(trait, is_enabled = True, the_action = [Hide("trait_tooltip"), Function(starting_serum.remove_trait,trait)], tooltip_anchor = (0.5, 0.57), tooltip_align = (0.5, 0.0))

        frame:
            background "#888888"
            ysize 900
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

                use aspect_grid(starting_serum)

                grid 2 3 xanchor 0.5 xalign 0.5:
                    spacing 10
                    text "Research Required: [starting_serum.research_needed]" style "menu_text_style"
                    text "Production Cost: [starting_serum.production_cost]" style "menu_text_style"
                    if starting_serum.tier <= mc.business.max_serum_tier:
                        text "Serum Tier: " + str(starting_serum.tier) style "menu_text_style"
                    else:
                        text "Serum Tier: {color=#fb6868}" + str(starting_serum.tier) + "{/color}" style "menu_text_style"
                    $ calculated_profit = round(mc.business.get_serum_base_value(starting_serum)-(starting_serum.production_cost/mc.business.batch_size))
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
                            spacing 5
                            for trait in starting_serum.traits:
                                use trait_details(trait)




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

            textbutton "View Contracts":
                style "textbutton_style"
                text_style "textbutton_text_style"
                xsize 230
                action Show("contract_select")

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
