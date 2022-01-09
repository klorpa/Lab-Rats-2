screen contract_select():
    add "Science_Menu_Background.png"

    modal True
    hbox:
        spacing 40
        xanchor 0.5
        xalign 0.5
        yalign 0.1
        frame:
            xalign 0.05
            yalign 0.05
            xsize 780
            ysize 800
            background "#888888"
            vbox:
                spacing 20
                text "Available Contracts:" style "menu_text_style"
                viewport:
                    mousewheel True
                    scrollbars "vertical"
                    vbox:
                        spacing 20
                        for new_contract in mc.business.offered_contracts:
                            use contract_select_button(new_contract):
                                textbutton "Accept Contract":
                                    xanchor 1.0
                                    xalign 0.90
                                    style "textbutton_style"
                                    text_style "menu_text_style"
                                    action Function(mc.business.accept_contract, new_contract)
                                    sensitive len(mc.business.active_contracts) < mc.business.max_active_contracts

        frame:
            xalign 0.05
            yalign 0.05
            xsize 780
            ysize 800
            background "#888888"
            vbox:
                spacing 20
                text "Current Contracts (" + str(len(mc.business.active_contracts)) + "/" + str(mc.business.max_active_contracts) + " Max)" style "menu_text_style"
                viewport:
                    mousewheel True
                    scrollbars "vertical"
                    vbox:
                        spacing 20
                        for contract in mc.business.active_contracts:
                            use contract_select_button(contract):
                                textbutton "Abandon": #TODO: This should probably require a double click or something.
                                    xanchor 1.0
                                    xalign 0.90
                                    style "textbutton_style"
                                    text_style "textbutton_text_style"
                                    action Function(mc.business.abandon_contract, contract)


    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action Hide("contract_select")
        textbutton "Return" align [0.5,0.5] style "return_button_style" text_style "return_button_style"
