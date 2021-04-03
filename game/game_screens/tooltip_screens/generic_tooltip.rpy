screen tooltip_screen(): #TODO: Convert this to use Use instead of being explicitly shown/hidden.
    zorder 110
    default hovered_enough_time = False
    $ tooltip = GetTooltip()
    if tooltip and len(tooltip) > 0:
        timer 0.5 action SetScreenVariable("hovered_enough_time",True)
        if hovered_enough_time:
            $ mouse_xy = renpy.get_mouse_pos()
            $ proper_x_anchor = 0.0
            $ proper_y_anchor = 0.0
            $ x_offset = 0
            $ y_offset = 0
            if mouse_xy[0] > 1920/2:
                $ proper_x_anchor = 1.0 #If we're on the right side of the screen anchor the tooltip right
                $ x_offset = -x_offset

            if mouse_xy[1] > 1080/2:
                $ proper_y_anchor = 1.0
                $ y_offset = -y_offset

            frame:
                background "#888888DD" xsize 450 xpos mouse_xy[0] + x_offset ypos mouse_xy[1] + y_offset anchor(proper_x_anchor, proper_y_anchor)
                text "[tooltip]" style "menu_text_style"
            #timer 0.03 action SetScreenVariable("mouse_xy", renpy.get_mouse_pos()) repeat True

    else:
        $ hovered_enough_time = False
