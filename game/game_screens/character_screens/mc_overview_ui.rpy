screen mc_character_sheet():
    add "Paper_Background.png"
    modal True
    zorder 100
    vbox:
        xanchor 0.5
        xalign 0.5
        yalign 0.2
        frame:
            background "#1a45a1aa"
            vbox:
                xsize 1620
                text mc.name + " " + mc.last_name style "menu_text_style" size 40 xanchor 0.5 xalign 0.5
                text "Owner of: " + mc.business.name style "menu_text_style" size 30 xanchor 0.5 xalign 0.5
        null height 60
        hbox:
            xanchor 0.5
            xalign 0.5
            yalign 0.4
            spacing 40
            frame:
                background "#1a45a1aa"
                xalign 0.5
                xanchor 0.5
                vbox:
                    xsize 500
                    text "Main Stats" style "menu_text_style" size 32 xalign 0.5
                    text "Unspent Points: " + str(mc.free_stat_points) style "menu_text_style" xalign 0.5
                    hbox:
                        xalign 0.5
                        text "Charisma: " + str(mc.charisma) + "/" + str(mc.max_stats) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_stat, "cha") sensitive mc.free_stat_points > 0 and mc.charisma<mc.max_stats yanchor 0.5 yalign 0.5

                    hbox:
                        xalign 0.5
                        text "Intelligence: " + str(mc.int) + "/" + str(mc.max_stats) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_stat, "int") sensitive mc.free_stat_points > 0 and mc.int<mc.max_stats yanchor 0.5 yalign 0.5

                    hbox:
                        xalign 0.5
                        text "Focus: " + str(mc.focus) + "/" + str(mc.max_stats) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_stat, "foc") sensitive mc.free_stat_points > 0 and mc.focus<mc.max_stats yanchor 0.5 yalign 0.5


                    null height 40
                    frame:
                        background "#888888"
                        xsize 500
                        vbox:
                            xalign 0.5
                            if mc.stat_goal:
                                text "Goal: " + mc.stat_goal.name style "menu_text_style" xalign 0.5 size 24
                                text "    " + mc.stat_goal.description style "menu_text_style" xalign 0.5
                                frame:
                                    ysize 60
                                    background None
                                    bar value mc.stat_goal.get_progress_fraction() range 1 xalign 0.5
                                    text mc.stat_goal.get_reported_progress() style "menu_text_style" xalign 0.5 yanchor 0.5 yalign 0.5
                                if mc.stat_goal.completed:
                                    textbutton "Collect Reward" xalign 0.5 action Function(mc.complete_goal,mc.stat_goal) style "textbutton_style" text_style "textbutton_text_style"
                                else:
                                    textbutton "Replace Goal (1/day)" xalign 0.5 action Function(mc.scrap_goal,mc.stat_goal) style "textbutton_style" text_style "textbutton_text_style" sensitive mc.scrap_goal_available and not mc.stat_goal.mandatory
                            else:
                                text "Goal: No goals available!" style "menu_text_style" xalign 0.5

            frame:
                background "#1a45a1aa"
                xalign 0.5
                xanchor 0.5
                vbox:
                    xsize 500
                    text "Work Skills" style "menu_text_style" size 32 xalign 0.5
                    text "Unspent Points: " + str(mc.free_work_points) style "menu_text_style" xalign 0.5
                    hbox:
                        xalign 0.5
                        text "Human Resources: " + str(mc.hr_skill) + "/" + str(mc.max_work_skills) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_work_skill, "hr") sensitive mc.free_work_points > 0 and mc.hr_skill < mc.max_work_skills yanchor 0.5 yalign 0.5
                    hbox:
                        xalign 0.5
                        text "Marketing: " + str(mc.market_skill) + "/" + str(mc.max_work_skills) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_work_skill, "market") sensitive mc.free_work_points > 0 and mc.market_skill < mc.max_work_skills yanchor 0.5 yalign 0.5
                    hbox:
                        xalign 0.5
                        text "Research and Development: " + str(mc.research_skill) + "/" + str(mc.max_work_skills) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_work_skill, "research") sensitive mc.free_work_points > 0 and mc.research_skill < mc.max_work_skills yanchor 0.5 yalign 0.5
                    hbox:
                        xalign 0.5
                        text "Production: " + str(mc.production_skill) + "/" + str(mc.max_work_skills) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_work_skill, "production") sensitive mc.free_work_points > 0 and mc.production_skill < mc.max_work_skills yanchor 0.5 yalign 0.5
                    hbox:
                        xalign 0.5
                        text "Supply Procurement: " + str(mc.supply_skill) + "/" + str(mc.max_work_skills) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_work_skill, "supply") sensitive mc.free_work_points > 0 and mc.supply_skill < mc.max_work_skills yanchor 0.5 yalign 0.5

                    null height 40
                    frame:
                        background "#888888"
                        xsize 500
                        vbox:
                            xalign 0.5
                            if mc.work_goal:
                                text "Goal: " + mc.work_goal.name style "menu_text_style" xalign 0.5 size 24
                                text "    " + mc.work_goal.description style "menu_text_style" xalign 0.5
                                frame:
                                    ysize 60
                                    background None
                                    bar value mc.work_goal.get_progress_fraction() range 1 xalign 0.5
                                    text mc.work_goal.get_reported_progress() style "menu_text_style" xalign 0.5 yanchor 0.5 yalign 0.5
                                if mc.work_goal.completed:
                                    textbutton "Collect Reward" xalign 0.5 action Function(mc.complete_goal,mc.work_goal) style "textbutton_style" text_style "textbutton_text_style"
                                else:
                                    textbutton "Replace Goal (1/day)" xalign 0.5 action Function(mc.scrap_goal,mc.work_goal) style "textbutton_style" text_style "textbutton_text_style" sensitive mc.scrap_goal_available and not mc.work_goal.mandatory
                            else:
                                text "Goal: No goals available!" style "menu_text_style" xalign 0.5

            frame:
                background "#1a45a1aa"
                xalign 0.5
                xanchor 0.5
                vbox:
                    xsize 500
                    text "Sex Skills" style "menu_text_style" size 32 xalign 0.5
                    text "Unspent Points: " + str(mc.free_sex_points) style "menu_text_style" xalign 0.5
                    hbox:
                        xalign 0.5
                        text "Stamina: " + str(mc.max_energy) + "/" +str(mc.max_energy_cap) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_sex_skill, "stam") sensitive mc.free_sex_points > 0 and mc.max_energy<mc.max_energy_cap yanchor 0.5 yalign 0.5
                    hbox:
                        xalign 0.5
                        text "Foreplay: " + str(mc.sex_skills["Foreplay"]) + "/" + str(mc.max_sex_skills) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_sex_skill, "Foreplay") sensitive mc.free_sex_points > 0 and mc.sex_skills["Foreplay"]<mc.max_sex_skills yanchor 0.5 yalign 0.5
                    hbox:
                        xalign 0.5
                        text "Oral: " + str(mc.sex_skills["Oral"]) + "/" + str(mc.max_sex_skills) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_sex_skill, "Oral") sensitive mc.free_sex_points > 0 and mc.sex_skills["Oral"]<mc.max_sex_skills yanchor 0.5 yalign 0.5
                    hbox:
                        xalign 0.5
                        text "Vaginal: " + str(mc.sex_skills["Vaginal"]) + "/" + str(mc.max_sex_skills) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_sex_skill, "Vaginal") sensitive mc.free_sex_points > 0 and mc.sex_skills["Vaginal"]<mc.max_sex_skills yanchor 0.5 yalign 0.5
                    hbox:
                        xalign 0.5
                        text "Anal: " + str(mc.sex_skills["Anal"]) + "/" + str(mc.max_sex_skills) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_sex_skill, "Anal") sensitive mc.free_sex_points > 0 and mc.sex_skills["Anal"]<mc.max_sex_skills yanchor 0.5 yalign 0.5

                    null height 40
                    frame:
                        background "#888888"
                        xsize 500
                        vbox:
                            xalign 0.5
                            if mc.sex_goal:
                                text "Goal: " + mc.sex_goal.name style "menu_text_style" xalign 0.5 size 24
                                text "    " + mc.sex_goal.description style "menu_text_style" xalign 0.5
                                frame:
                                    ysize 60
                                    background None
                                    bar value mc.sex_goal.get_progress_fraction() range 1 xalign 0.5
                                    text mc.sex_goal.get_reported_progress() style "menu_text_style" xalign 0.5 yanchor 0.5 yalign 0.5
                                if mc.sex_goal.completed:
                                    textbutton "Collect Reward" xalign 0.5 action Function(mc.complete_goal,mc.sex_goal) style "textbutton_style" text_style "textbutton_text_style"
                                else:
                                    textbutton "Replace Goal (1/day)" xalign 0.5 action Function(mc.scrap_goal,mc.sex_goal) style "textbutton_style" text_style "textbutton_text_style" sensitive mc.scrap_goal_available and not mc.sex_goal.mandatory
                            else:
                                text "Goal: No goals available!" style "menu_text_style" xalign 0.5

    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action Hide("mc_character_sheet")
        textbutton "Return" align [0.5,0.5] text_style "return_button_style"
