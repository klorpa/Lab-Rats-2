screen serum_production_select_ui():
    add "Science_Menu_Background.png"
    default line_selected = None
    default production_remaining = 100
    python:
        production_remaining = 100
        for key in mc.business.serum_production_array:
            production_remaining -= mc.business.serum_production_array[key][1] # How much of the 100% capability are we using?

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
            text "Capacity Remaining: [production_remaining]%" style "menu_text_style"
        spacing 20
        for count in range(1,mc.business.production_lines+1): #For the non-programmers we index our lines to 1 through production_lines.
            frame:
                background "#888888"
                vbox:
                    $ name_string = ""
                    if count in mc.business.serum_production_array:
                        $ name_string = "Production Line " + str(count) + "\nCurrently Producing: " + mc.business.serum_production_array[count][0].name
                    else:
                        $ name_string = "Production Line " + str(count) + "\nCurrently Producing: Nothing"

                    $ button_background = "#000080"
                    if line_selected == count:
                        $ button_background = "#666666"

                    if count in mc.business.serum_production_array:
                        $ the_serum = mc.business.serum_production_array[count][0]
                        textbutton name_string action [SetScreenVariable("line_selected",count),Hide("serum_tooltip")] style "textbutton_style" text_style "textbutton_text_style" hovered Show("serum_tooltip",None,the_serum, given_anchor = (1.0,0.0), given_align = (0.97,0.04)) unhovered Hide("serum_tooltip") background button_background xsize 500
                    else:
                        textbutton name_string action SetScreenVariable("line_selected",count) style "textbutton_style" text_style "textbutton_text_style" background button_background xsize 500

                    null height 20
                    hbox:
                        ysize 40
                        xsize 500
                        text "Production Weight: " style "menu_text_style" xalign 0.0
                        if count in mc.business.serum_production_array:
                            textbutton "-10%" action Function(mc.business.change_line_weight,count,-10) style "textbutton_style" text_style "textbutton_text_style" yanchor 0.25 tooltip "Work done by production employees will be split between active lines based on production weight."
                            text str(mc.business.serum_production_array[count][1]) + "%" style "menu_text_style"
                            textbutton "+10%" action Function(mc.business.change_line_weight,count,10) style "textbutton_style" text_style "textbutton_text_style" yanchor 0.25 tooltip "Work done by production employees will be split between active lines based on production weight."
                        else:
                            textbutton "-10%" action NullAction style "textbutton_style" text_style "textbutton_text_style" sensitive False yanchor 0.25 tooltip "Work done by production employees will be split between active lines based on production weight."
                            text "0%" style "menu_text_style"
                            textbutton "+10%" action NullAction style "textbutton_style" text_style "textbutton_text_style" sensitive False yanchor 0.25 tooltip "Work done by production employees will be split between active lines based on production weight."

                    hbox:
                        ysize 40
                        xsize 500
                        text "Auto-sell Threshold: " style "menu_text_style"
                        if count in mc.business.serum_production_array:
                            textbutton "-1" action Function(mc.business.change_line_autosell,count,-1) style "textbutton_style" text_style "textbutton_text_style" yanchor 0.25 tooltip "Doses of serum above the auto-sell threshold will automatically be flagged for sale and moved to the marketing department."
                            if mc.business.serum_production_array[count][3] < 0:
                                text "None" style "menu_text_style"
                            else:
                                text str(mc.business.serum_production_array[count][3]) style "menu_text_style"
                            textbutton "+1" action Function(mc.business.change_line_autosell,count,1) style "textbutton_style" text_style "textbutton_text_style"  yanchor 0.25 tooltip "Doses of serum above the auto-sell threshold will automatically be flagged for sale and moved to the marketing department."
                        else:
                            textbutton "-1" action NullAction style "textbutton_style" text_style "textbutton_text_style" sensitive False yanchor 0.25 tooltip "Doses of serum above the auto-sell threshold will automatically be flagged for sale and moved to the marketing department."
                            text "None" style "menu_text_style"
                            textbutton "+1" action NullAction style "textbutton_style" text_style "textbutton_text_style" sensitive False yanchor 0.25 tooltip "Doses of serum above the auto-sell threshold will automatically be flagged for sale and moved to the marketing department."

    if line_selected:
        frame:
            yanchor 0.0
            background "#888888"
            xalign 0.5
            yalign 0.04
            xsize 600
            vbox:
                text "Choose Production for Line [line_selected]" style "menu_text_style" size 30
                if len(mc.business.serum_designs) == 0:
                    frame:
                        xfill True
                        background "#000080"
                        text "No designs researched! Create and research a design in the R&D department first!" style "textbutton_text_style"
                else:
                    for a_serum in mc.business.serum_designs:
                        if a_serum.researched:
                            textbutton a_serum.name:
                                action [Hide("serum_tooltip"), Function(mc.business.change_production,a_serum,line_selected), SetScreenVariable("line_selected",None)]
                                hovered Show("serum_tooltip",None, a_serum, given_anchor = (1.0,0.0), given_align = (0.97,0.04))
                                unhovered Hide("serum_tooltip")
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


    $ production_tutorial_length = 5 #The number of  tutorial screens we have.
    if mc.business.event_triggers_dict["production_tutorial"] > 0 and mc.business.event_triggers_dict["production_tutorial"] <= production_tutorial_length: #We use negative numbers to symbolize the tutorial not being enabled
        imagebutton:
            auto
            sensitive True
            xsize 1920
            ysize 1080
            idle "/tutorial_images/production_tutorial_"+__builtin__.str(mc.business.event_triggers_dict["production_tutorial"])+".png"
            hover "/tutorial_images/production_tutorial_"+__builtin__.str(mc.business.event_triggers_dict["production_tutorial"])+".png"
            action Function(mc.business.advance_tutorial,"production_tutorial")
