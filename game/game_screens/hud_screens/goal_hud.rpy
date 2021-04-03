screen goal_hud_ui():
    frame:
        background "Goal_Frame_1.png"
        yalign 0.5
        xsize 260
        ysize 250
        vbox:
            textbutton "Goal Information" action Show("mc_character_sheet") style "textbutton_style" text_style "textbutton_text_style" xsize 245 text_align 0.5 tooltip "Complete goals to earn experience, and spend experience to improve your stats and skills."
            for goal in [mc.stat_goal,mc.work_goal,mc.sex_goal]:
                if goal:
                    frame:
                        ysize 60
                        background None
                        bar value goal.get_progress_fraction() range 1 xalign 0.5
                        textbutton goal.name + "\n" + goal.get_reported_progress() text_style "menu_text_style" xalign 0.5 yanchor 0.5 yalign 0.5 text_size 12 text_text_align 0.5 action NullAction() sensitive True tooltip goal.description
