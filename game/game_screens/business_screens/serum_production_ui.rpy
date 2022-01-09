screen serum_production_select_ui():
    add "Science_Menu_Background.png"
    modal True
    default line_selected = None
    default production_remaining = 100 #TODO: We can set this higher than 100 if we want now.
    python:
        production_remaining = 100 - mc.business.get_used_line_weight()

    vbox:
        xalign 0.04
        yalign 0.04
        xsize 600
        yanchor 0.0
        frame:
            background "#888888"
            xsize 510
            text "Production Lines" style "menu_text_style" size 30 xalign 0.5

        frame:
            background "#888888"
            xsize 510
            vbox:
                text "Capacity Remaining: [production_remaining]%" style "menu_text_style"
                textbutton "Max Serum Tier: " + str(mc.business.max_serum_tier) action VrenNullAction style "textbutton_style" text_style "menu_text_style" tooltip "The highest tier of serum you can produce is limited by your production facilities. Upgrade them to produce higher tier designs."

        spacing 20
        $ line_number = 0
        for line in mc.business.production_lines: #For the non-programmers we index our lines to 1 through production_lines.
            $ line_number += 1
            frame:
                background "#888888"
                vbox:
                    $ name_string = ""
                    if line.selected_design:
                        $ name_string = "Production Line " + str(line_number) + "\nCurrently Producing: " + line.selected_design.name
                    else:
                        $ name_string = "Production Line " + str(line_number) + "\nCurrently Producing: Nothing"

                    $ button_background = "#000080"
                    if line_selected == line:
                        $ button_background = "#666666"

                    if line.selected_design:
                        textbutton name_string action [SetScreenVariable("line_selected", line),Hide("serum_tooltip")] style "textbutton_style" text_style "textbutton_text_style" hovered Show("serum_tooltip",None, line.selected_design, given_anchor = (1.0,0.0), given_align = (0.97,0.04)) unhovered Hide("serum_tooltip") background button_background xsize 500
                    else:
                        textbutton name_string action SetScreenVariable("line_selected", line) style "textbutton_style" text_style "textbutton_text_style" background button_background xsize 500

                    null height 20
                    hbox:
                        ysize 40
                        xsize 500
                        text "Production Weight: " style "menu_text_style" xalign 0.0
                        if line.selected_design:
                            textbutton "-10%" action Function(line.change_line_weight, -10) style "textbutton_style" text_style "textbutton_text_style" sensitive line.production_weight >= 10 yanchor 0.25 tooltip "Work done by production employees will be split between active lines based on production weight."
                            text str(line.production_weight) + "%" style "menu_text_style"
                            textbutton "+10%" action Function(line.change_line_weight, 10) style "textbutton_style" text_style "textbutton_text_style" sensitive production_remaining >= 10 yanchor 0.25 tooltip "Work done by production employees will be split between active lines based on production weight."
                        else:
                            textbutton "-10%" action NullAction style "textbutton_style" text_style "textbutton_text_style" sensitive False yanchor 0.25 tooltip "Work done by production employees will be split between active lines based on production weight."
                            text "0%" style "menu_text_style"
                            textbutton "+10%" action NullAction style "textbutton_style" text_style "textbutton_text_style" sensitive False yanchor 0.25 tooltip "Work done by production employees will be split between active lines based on production weight."

                    hbox:
                        ysize 40
                        text "Auto-sell: " style "menu_text_style" yalign 0.5 yanchor 0.5
                        if line.autosell:
                            button action Function(line.toggle_line_autosell) background "#44aa44" xsize 35 ysize 35 yalign 0.5 yanchor 0.5 xalign 0.0 xanchor 0.0 tooltip "Doses of serum above the auto-sell threshold will automatically be flagged for sale and moved to the marketing department."
                        else:
                            button action Function(line.toggle_line_autosell) background "#444444" xsize 35 ysize 35 yalign 0.5 yanchor 0.5 xalign 0.0 xanchor 0.0 tooltip "Doses of serum above the auto-sell threshold will automatically be flagged for sale and moved to the marketing department."

                        if line.selected_design:
                            if line.autosell:
                                textbutton "-1" action Function(line.change_line_autosell, -1) style "textbutton_style" yalign 0.5 yanchor 0.5  text_style "textbutton_text_style" tooltip "Doses of serum above the auto-sell threshold will automatically be flagged for sale and moved to the marketing department."
                                text "When > " + str(line.autosell_amount) + " doses" style "menu_text_style" ysize 30 yalign 0.5 yanchor 0.5
                                textbutton "+1" action Function(line.change_line_autosell, 1) style "textbutton_style" yalign 0.5 yanchor 0.5 text_style "textbutton_text_style" tooltip "Doses of serum above the auto-sell threshold will automatically be flagged for sale and moved to the marketing department."


    if line_selected:
        frame:
            yanchor 0.0
            background "#888888"
            xalign 0.5
            yalign 0.04
            xsize 600
            vbox:
                text "Choose Production" style "menu_text_style" size 30
                if len(mc.business.serum_designs) == 0:
                    frame:
                        xfill True
                        background "#000080"
                        text "No designs researched! Create and research a design in the R&D department first!" style "textbutton_text_style"
                else:
                    for a_serum in mc.business.serum_designs:
                        if a_serum.researched:
                            textbutton a_serum.name:
                                action [Hide("serum_tooltip"), Function(line_selected.set_product, a_serum, production_remaining), SetScreenVariable("line_selected", None)]
                                hovered Show("serum_tooltip", None, a_serum, given_anchor = (1.0,0.0), given_align = (0.97,0.04))
                                unhovered Hide("serum_tooltip")
                                sensitive a_serum.tier <= mc.business.max_serum_tier
                                style "textbutton_style" text_style "textbutton_text_style"

    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action Return()
        textbutton "Return" align [0.5,0.5] text_style "return_button_style"

    imagebutton:
        auto "/tutorial_images/restart_tutorial_%s.png"
        xsize 54
        ysize 54
        yanchor 1.0
        xalign 0.0
        yalign 1.0
        action Function(mc.business.reset_tutorial,"production_tutorial")


    $ production_tutorial_length = 5 #The number of tutorial screens we have.
    if mc.business.event_triggers_dict["production_tutorial"] > 0 and mc.business.event_triggers_dict["production_tutorial"] <= production_tutorial_length: #We use negative numbers to symbolize the tutorial not being enabled
        imagebutton:
            auto
            sensitive True
            xsize 1920
            ysize 1080
            idle "/tutorial_images/production_tutorial_"+__builtin__.str(mc.business.event_triggers_dict["production_tutorial"])+".png"
            hover "/tutorial_images/production_tutorial_"+__builtin__.str(mc.business.event_triggers_dict["production_tutorial"])+".png"
            action Function(mc.business.advance_tutorial,"production_tutorial")
