screen review_designs_screen():
    add "Science_Menu_Background.png"
    default selected_serum = None

    frame:
        xalign 0.1
        yalign 0.1
        background "#888888"
        viewport:
            xsize 540
            ymaximum 800
            scrollbars "vertical"
            mousewheel True
            vbox:
                text "Serum Designs:" style "menu_text_style" size 30
                for serum_design in mc.business.serum_designs:
                    $ serum_name = serum_design.name
                    if serum_design.researched:
                        $ serum_name += " - Research Finished"
                    else:
                        $ serum_name += " - " + str(serum_design.current_research) + "/" + str(serum_design.research_needed) + " Research Required"

                    if serum_design == selected_serum:
                        textbutton serum_name:
                            action SetScreenVariable("selected_serum", None) style "textbutton_style" text_style "textbutton_text_style" background "#666666"

                    else:
                        textbutton serum_name:
                            action SetScreenVariable("selected_serum",serum_design) style "textbutton_style" text_style "textbutton_text_style"



    if selected_serum:
        use serum_tooltip(selected_serum, given_anchor = (1.0,0.0), given_align = (0.9,0.1)):
            textbutton "Scrap Design":
                action [Function(mc.business.remove_serum_design,selected_serum), SetScreenVariable("selected_serum", None)]
                style "textbutton_style" text_style "textbutton_text_style" xanchor 0.5 xalign 0.5

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
        textbutton "Return" align [0.5,0.5] style "return_button_style" text_style "return_button_style"
