screen girl_outfit_select_manager(the_wardrobe, show_sets = False): ##Brings up a list of outfits currently in a girls wardrobe.
    add "Paper_Background.png"
    modal True
    zorder 100
    default preview_outfit = None

    hbox:
        xalign 0.1
        yalign 0.1
        spacing 20
        frame:
            background "#888888"
            xsize 450
            ysize 750
            viewport:
                scrollbars "vertical"
                xsize 450
                ysize 750
                mousewheel True
                vbox:
                    text "Full Outfits" style "menu_text_style" size 30
                    for outfit in the_wardrobe.get_outfit_list():
                        textbutton "Select "+outfit.name+ "\n(Sluttiness " +str(outfit.slut_requirement) +")" action Return(outfit) hovered SetScreenVariable("preview_outfit", outfit.get_copy()) unhovered SetScreenVariable("preview_outfit", None) style "textbutton_style" text_style "outfit_description_style" xsize 210

        if show_sets:
            frame:
                background "#888888"
                xsize 450
                ysize 750
                viewport:
                    scrollbars "vertical"
                    xsize 450
                    ysize 750
                    mousewheel True
                    vbox:
                        text "Overwear Sets" style "menu_text_style" size 30
                        for outfit in the_wardrobe.get_overwear_sets_list():
                            textbutton "Select "+outfit.name+ "\n(Sluttiness " +str(outfit.get_overwear_slut_score()) +")" action Return(outfit) hovered SetScreenVariable("preview_outfit", outfit.get_copy()) unhovered SetScreenVariable("preview_outfit", None) style "textbutton_style" text_style "outfit_description_style" xsize 210

            frame:
                background "#888888"
                xsize 450
                ysize 750
                viewport:
                    scrollbars "vertical"
                    xsize 450
                    ysize 750
                    mousewheel True
                    vbox:
                        text "Underwear Sets" style "menu_text_style" size 30
                        for outfit in the_wardrobe.get_underwear_sets_list():
                            textbutton "Select "+outfit.name+ "\n(Sluttiness " +str(outfit.get_underwear_slut_score()) +")" action Return(outfit) hovered SetScreenVariable("preview_outfit", outfit.get_copy()) unhovered SetScreenVariable("preview_outfit", None) style "textbutton_style" text_style "outfit_description_style" xsize 210

    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action Return("None")
        textbutton "Return" align [0.5,0.5] text_style "return_button_style"

    fixed:
        pos (1450,0)
        add mannequin_average
        if preview_outfit:
            for cloth in preview_outfit.generate_draw_list(None,"stand3"):
                add cloth
