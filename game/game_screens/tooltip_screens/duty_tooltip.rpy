screen duty_tooltip(the_duty):
    frame:
        background None
        vbox:
            spacing 20
            text the_duty.duty_name style "menu_text_style" size 24 xanchor 0.5 xalign 0.5
            text the_duty.duty_description style "menu_text_style" text_align 0.0

            transclude
