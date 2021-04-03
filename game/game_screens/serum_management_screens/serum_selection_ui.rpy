screen serum_inventory_select_ui(the_inventory, the_person = None): #Used to let the player select a serum from an inventory. if the_person is handed over we display their serum Tolerance as well
    add "Science_Menu_Background.png"
    modal True
    frame:
        background "#888888"
        xsize 400
        ysize 1000
        xalign 0.05
        yalign 0.05
        anchor (0.0,0.0)
        vbox:
            spacing 10
            default selected_serum = None
            text "Serum Available" size 22 style "menu_text_style"
            for serum in the_inventory.serums_held:
                button:
                    background "#1a45a1aa"
                    xsize 380
                    ysize 80
                    action [Hide("serum_tooltip"),Return(serum[0])]
                    hovered Show("serum_tooltip",None,serum[0], given_align = (0.9,0.1), given_anchor = (1.0,0.0))
                    #unhovered Hide("serum_tooltip")
                    text serum[0].name + " - " + str(serum[1]) + " Doses" style "menu_text_style" size 18 xalign 0.5 xanchor 0.5 yalign 0.5 yanchor 0.5

    if the_person:
        frame:
            background None
            anchor [1.0, 1.0]
            align [0.9,0.9]
            use serum_tolerance_indicator(the_person)

    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action [Hide("serum_tooltip"), Return("None")]
        textbutton "Return" align [0.5,0.5] text_style "return_button_style"
