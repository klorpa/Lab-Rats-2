transform phone_slide(start_yalign, goal_yalign, duration = 0.4):
    yalign start_yalign
    linear duration yalign goal_yalign

transform background_fade(max_time, time_used):
    alpha (max_time-time_used)/max_time
    linear max_time - time_used alpha 0

screen phone_hud_ui():
    default phone_up = False
    default start_phone_pos = 1.4
    default end_phone_pos = 1.4
    default start = True
    frame:
        background "#1a45a1aa"
        xsize 340
        ysize 400
        xanchor 1.0
        xalign 0.99
        at phone_slide(start_phone_pos, end_phone_pos)
        vbox:
            spacing 0
            if phone_up:
                textbutton "" style "textbutton_style":
                    text_style "textbutton_text_style" xsize 320 ysize 20 action [SetScreenVariable("phone_up",False), SetScreenVariable("end_phone_pos",1.4), SetScreenVariable("start_phone_pos",1.0)]
            else:
                textbutton "" style "textbutton_style":
                    text_style "textbutton_text_style" xsize 320 ysize 20 action [SetScreenVariable("phone_up",True), SetScreenVariable("end_phone_pos",1.0), SetScreenVariable("start_phone_pos",1.4)]

            null height 5

            for log_item in mc.log_items:
                if log_item is not None and log_item[0] is not None and log_item[1] is not None: #Minor hack to try and prevent any crashes. In theory log items should always exist.
                    $ fade_time = 5
                    $ time_diff = time.time() - log_item[2]
                    if time_diff > fade_time:
                        $ time_diff = fade_time

                    frame:
                        background "#33333388"
                        xsize 320
                        padding (0,0)
                        text log_item[0] style log_item[1] size 18 xsize 320 first_indent 20
                    frame:
                        background "#ff0000aa"
                        xsize 320
                        ysize 8
                        yanchor 1.0
                        yalign 0.95
                        xpadding 0
                        ypadding 0
                        at background_fade(5, time_diff)
                    null height 4
