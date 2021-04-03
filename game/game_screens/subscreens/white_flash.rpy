screen flash_screen(strength = 1.0): #Flashes white over the screen. #TODO: Change strength to 1.0 by default
    zorder 300 #Flash on top of everything
    frame at flash_effect(strength):
        background "#FFFFFF"
        #alpha strength
        xsize 1920
        ysize 1080

    timer 0.1 action Hide("flash_screen")

screen border_pulse(strength = 1.0):
    zorder 300
    frame at zoom_effect(strength):
        background "images/BorderPulse.png"

        xsize 2304
        ysize 1296

        xanchor 0.5
        yanchor 0.5
        xalign 0.5
        yalign 0.5

    timer 0.1 action Hide("border_pulse")

screen cum_screen():
    zorder 300
    frame at cum_effect():
        background "images/BorderPulse.png"

        xsize 2304
        ysize 1296

        xanchor 0.5
        yanchor 0.5
        xalign 0.5
        yalign 0.5

    timer 0.6 action Show("flash_screen", None, 0.65)
    timer 0.7 action Hide("cum_screen")

transform flash_effect(strength = 1.0):
    on show:
        alpha 0.0
        linear 0.1 alpha strength*0.7

    on hide:
        linear 0.6 alpha 0

transform zoom_effect(strength = 1.0):
    on show:
        zoom 1.0
        linear 0.1 zoom 1.0-(0.1*strength)

    on hide:
        linear 2.0 zoom 1.0

transform cum_effect():
    on show:
        zoom 1.0
        linear 0.1 zoom 0.97
        linear 0.2 zoom 0.995
        linear 0.1 zoom 0.94
        linear 0.2 zoom 0.98
        linear 0.1 zoom 0.9

    on hide:
        linear 2.0 zoom 1.0
