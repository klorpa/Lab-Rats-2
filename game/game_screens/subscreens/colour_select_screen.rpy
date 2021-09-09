# init -2 python: #TODO: Once verified this works replace move these functions here instead of in outfit_creator_ui
#     def colour_changed_r(new_value):
#         if not new_value:
#             new_value = 0
#
#         try:
#             new_value = float(new_value)
#         except ValueError:
#             new_value = 0
#
#         if float(new_value) < 0:
#             new_value = 0
#         elif float(new_value) > 1:
#             new_value = 1.0
#         cs = renpy.current_screen()
#
#         cs.scope["current_r"] = __builtin__.round(float(new_value),2)
#         renpy.restart_interaction()
#
#     def colour_changed_g(new_value):
#         if not new_value:
#             new_value = 0
#
#         try:
#             new_value = float(new_value)
#         except ValueError:
#             new_value = 0
#
#         if float(new_value) < 0:
#             new_value = 0
#         elif float(new_value) > 1:
#             new_value = 1.0
#         cs = renpy.current_screen()
#
#         cs.scope["current_g"] = __builtin__.round(float(new_value),2)
#         renpy.restart_interaction()
#
#     def colour_changed_b(new_value):
#         if not new_value:
#             new_value = 0
#
#         try:
#             new_value = float(new_value)
#         except ValueError:
#             new_value = 0
#
#         if float(new_value) < 0:
#             new_value = 0
#         elif float(new_value) > 1:
#             new_value = 1.0
#
#         cs = renpy.current_screen()
#
#         cs.scope["current_b"] = __builtin__.round(float(new_value),2)
#         renpy.restart_interaction()
#
#     def update_colour_palette(palette_index, new_r,new_g,new_b,new_a):
#         persistent.colour_palette[palette_index] = [new_r,new_g,new_b,new_a]
#         renpy.save_persistent()

screen colour_selector(allow_none = False, title = None):
    add "Paper_Background.png"
    modal True
    zorder 100

    default current_r = 1.0
    default current_g = 1.0
    default current_b = 1.0
    default current_a = 1.0
    frame:
        xanchor 0.5
        xalign 0.5
        yanchor 0.5
        yalign 0.5
        background"#888888"
        vbox:
            if title:
                text title style "menu_text_style" size 20
            use colour_square([current_r, current_g, current_b, current_a], square_size_x = 600, square_size_y = 100)
            # frame:
            #     ysize 100
            #     xsize 602
            #     xalign 0.5
            #     xanchor 0.5
            #     background Color((current_r*255, current_g*255, current_b*255, current_a*255))
            use colour_ui(current_r,current_g,current_b,current_a)
            hbox:
                xanchor 0.5
                xalign 0.5
                textbutton "Confirm Color":
                    action Return(Color((current_r*255, current_g*255, current_b*255, current_a*255)))
                    style "textbutton_style"
                    text_style "textbutton_text_style" text_text_align 0.5 text_xalign 0.5 text_yanchor 0.5 text_yalign 0.5 xysize (155,60) yanchor 0.5 yalign 0.5

                if allow_none:
                    textbutton "Back":
                        action Return(None)
                        style "textbutton_style"
                        text_style "textbutton_text_style" text_text_align 0.5 text_xalign 0.5 text_yanchor 0.5 text_yalign 0.5 xysize (155,60) yanchor 0.5 yalign 0.5

screen colour_ui(current_r, current_g, current_b, current_a, background_colour = None): # Provides a reusable UI for selecting colours. Stores RGBA values in variables that can be used by other screens for something.
    default bar_select = 0
    frame:
        background background_colour
        vbox:
            hbox:
                spacing 10
                vbox:
                    text "Red" style "textbutton_text_style"
                    hbox:
                        if bar_select == 1:
                            frame:
                                input default current_r length 4 changed colour_changed_r allow ".0123456789" style "menu_text_style"
                                xsize 70
                                ysize 50
                        else:
                            button:
                                background "#888888"
                                action SetScreenVariable("bar_select",1)
                                text "%.2f" % current_r style "menu_text_style"
                                xsize 70
                                ysize 50

                        bar value ScreenVariableValue("current_r", 1.0) xsize 120 ysize 45 style style.slider unhovered SetScreenVariable("current_r",__builtin__.round(current_r,2))
                vbox:
                    text "Green" style "textbutton_text_style"
                    hbox:
                        if bar_select == 2:
                            frame:
                                input default current_g length 4 changed colour_changed_g allow ".0123456789" style "menu_text_style"
                                xsize 70
                                ysize 50
                        else:
                            button:
                                background "#888888"
                                action SetScreenVariable("bar_select",2)
                                text "%.2f" % current_g style "menu_text_style"
                                xsize 70
                                ysize 50

                        bar value ScreenVariableValue("current_g", 1.0) xsize 120 ysize 45 style style.slider unhovered SetScreenVariable("current_g",__builtin__.round(current_g,2))
                vbox:
                    text "Blue" style "textbutton_text_style"
                    hbox:
                        if bar_select == 3:
                            frame:
                                input default current_b length 4 changed colour_changed_b allow ".0123456789" style "menu_text_style"
                                xsize 70
                                ysize 50
                        else:
                            button:
                                background "#888888"
                                action SetScreenVariable("bar_select",3)
                                text "%.2f" % current_b style "menu_text_style"
                                xsize 70
                                ysize 50

                        bar value ScreenVariableValue("current_b", 1.0) xsize 120 ysize 45 style style.slider unhovered SetScreenVariable("current_b",__builtin__.round(current_b,2))

            text "Transparency: " style "menu_text_style"
            hbox:
                spacing 5
                for trans in ['1.0', '0.95', '0.9', '0.8', '0.75', '0.66', '0.5', '0.33', '0.25']:
                    $ trans_name = str(int(float(trans)*100)) + "%"
                    button:
                        if current_a == float(trans):
                            background "#4f7ad6"
                        else:
                            background "#1a45a1"
                        text trans_name style "menu_text_style" xalign 0.5 xanchor 0.5 yalign 0.5 yanchor 0.5
                        xysize (60, 40)
                        action SetScreenVariable("current_a", float(trans))

            grid 10 2:
                spacing 5
                xalign 0.5
                xanchor 0.5
                for count, a_colour in __builtin__.enumerate(persistent.colour_palette[0:20]):
                    use pallet_square(current_r, current_g, current_b, current_a, a_colour, count)
                    # frame:
                    #     background "#aaaaaa"
                    #     button:
                    #         background Color(rgb=(a_colour[0], a_colour[1], a_colour[2]), alpha = a_colour[3])
                    #         xysize (40,40)
                    #         sensitive True
                    #         action [SetScreenVariable("current_r", a_colour[0]), SetScreenVariable("current_g", a_colour[1]), SetScreenVariable("current_b", a_colour[2]), SetScreenVariable("current_a", a_colour[3])]
                    #         alternate Function(update_colour_palette, count, current_r, current_g, current_b, current_a)
