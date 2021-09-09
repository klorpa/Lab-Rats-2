screen review_designs_screen(show_designs = True, show_traits = True, allow_exit = True, select_instead_of_delete = False, hide_partially_researched = False):
    add "Science_Menu_Background.png"
    default selected_research = None

    frame:
        xalign 0.1
        yalign 0.1
        background "#888888"
        hbox:
            if show_designs:
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

                            if serum_design == selected_research:
                                textbutton serum_name:
                                    action SetScreenVariable("selected_research", None)
                                    sensitive serum_design.researched or not hide_partially_researched
                                    style "textbutton_style" text_style "textbutton_text_style" background "#666666"

                            else:
                                textbutton serum_name:
                                    action SetScreenVariable("selected_research", serum_design)
                                    sensitive serum_design.researched or not hide_partially_researched
                                    style "textbutton_style" text_style "textbutton_text_style"

            if show_traits:
                viewport:
                    xsize 540
                    ymaximum 800
                    scrollbars "vertical"
                    mousewheel True
                    vbox:
                        text "Designed Traits:" style "menu_text_style" size 30
                        for trait_design in mc.business.blueprinted_traits:
                            $ trait_name = trait_design.name
                            if trait_design.researched:
                                $ trait_name += " - Research Finished"
                            else:
                                $ trait_name += " - " + str(trait_design.current_research) + "/" + str(trait_design.research_needed) + " Research Required"

                            if trait_design == selected_research:
                                textbutton trait_name:
                                    action SetScreenVariable("selected_research", None)
                                    sensitive trait_design.researched or not hide_partially_researched
                                    style "textbutton_style" text_style "textbutton_text_style" background "#666666"

                            else:
                                textbutton trait_name:
                                    action SetScreenVariable("selected_research", trait_design)
                                    sensitive trait_design.researched or not hide_partially_researched
                                    style "textbutton_style" text_style "textbutton_text_style"



    if selected_research:
        $ research_verb = "Scrap"
        if select_instead_of_delete:
            $ research_verb = "Select"
        if isinstance(selected_research, SerumDesign):
            use serum_tooltip(selected_research, given_anchor = (1.0,0.0), given_align = (0.9,0.1)):
                textbutton research_verb + " Design":
                    if select_instead_of_delete:
                        action Return(selected_research)
                    else:
                        action [Function(mc.business.remove_serum_design,selected_research), SetScreenVariable("selected_research", None)]
                    style "textbutton_style" text_style "textbutton_text_style" xanchor 0.5 xalign 0.5
        if isinstance(selected_research, SerumTrait):
            use trait_tooltip(selected_research, given_anchor = (1.0,0.0), given_align = (0.9,0.1)):
                textbutton research_verb + " Trait":
                    if select_instead_of_delete:
                        action Return(selected_research)
                    else:
                        action [Function(mc.business.remove_trait,selected_research), SetScreenVariable("selected_research", None)]
                    style "textbutton_style" text_style "textbutton_text_style" xanchor 0.5 xalign 0.5

    if allow_exit:
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
