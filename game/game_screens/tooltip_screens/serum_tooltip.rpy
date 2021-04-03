screen serum_tooltip(the_serum, given_anchor = (0.0,0.0), given_align = (0.0,0.0)): # set_x_align = 0.9, set_y_align = 0.1
    zorder 105 #Serum tooltips are a high order so they may be properly layered onto others when needed to show extra info.
    frame:
        background "#888888"

        anchor given_anchor
        align given_align
        viewport:
            xsize 540
            ymaximum 800
            scrollbars "vertical"
            mousewheel True
            vbox:
                text "[the_serum.name]" style "menu_text_style" xanchor 0.5 xalign 0.5 size 26
                grid 2 3 xanchor 0.5 xalign 0.5:
                    spacing 10
                    text "Research Required: [the_serum.research_needed]" style "menu_text_style"
                    text "Production Cost: [the_serum.production_cost]" style "menu_text_style"
                    text "Value: $[the_serum.value]" style "menu_text_style"
                    $ calculated_profit = (the_serum.value*mc.business.batch_size)-the_serum.production_cost
                    if calculated_profit > 0:
                        text "Expected Profit:{color=#98fb98} $[calculated_profit]{/color}" style "menu_text_style"
                    else:
                        $ calculated_profit = 0 - calculated_profit
                        text "Expected Profit:{color=#ff0000} -$[calculated_profit]{/color}" style "menu_text_style"

                    text "Duration: [the_serum.duration] Turns" style "menu_text_style"
                    if the_serum.unlocked:
                        null
                    else:
                        text "Clarity Cost: [the_serum.clarity_needed]" style "menu_text_style"

                for trait in the_serum.traits: #Note: We might want to Use the trait_tooltip for this to keep our display parameters consistent.
                    text trait.name style "menu_text_style"
                    text "    "  + trait.positive_slug style "menu_text_style" color "#98fb98"
                    text "    "  + trait.negative_slug style "menu_text_style" color "#ff0000"

                if the_serum.side_effects:
                    for side_effect in the_serum.side_effects:
                        text side_effect.name style "menu_text_style"
                        text "    "  + side_effect.negative_slug style "menu_text_style" color "#ff0000"

                transclude #If you hand the serum tooltip a child it's added to the vBox
