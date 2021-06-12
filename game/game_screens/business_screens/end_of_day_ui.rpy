screen end_of_day_update():
    add "Paper_Background.png"
    zorder 100
    text mc.business.name:
        style "textbutton_text_style"
        xanchor 0.5
        xalign 0.5
        yalign 0.07
        size 40

    frame:
        background "#1a45a1aa"
        xalign 0.1
        yalign 0.22
        xanchor 0.0
        vbox:
            xsize 1500
            ysize 200
            text "Daily Statistics:" style "textbutton_text_style" size 20
            text "     " + "Current Efficiency Modifier: " + str(mc.business.team_effectiveness) + "%" style "textbutton_text_style"
            text "     " + "Production Potential: " + str(mc.business.production_potential) style "textbutton_text_style"
            text "     " + "Supplies Procured: " + str(mc.business.supplies_purchased) + " Units" style "textbutton_text_style"
            text "     " + "Production Used: " + str(mc.business.production_used) style "textbutton_text_style"
            text "     " + "Research Produced: " + str(mc.business.research_produced) style "textbutton_text_style"
            text "     " + "Sales Made: $" + str(mc.business.sales_made) style "textbutton_text_style"
            text "     " + "Daily Salary Paid: $" + str(mc.business.calculate_salary_cost()) style "textbutton_text_style"
            text "     " + "Serums Sold Today: " + str(mc.business.serums_sold) style "textbutton_text_style"
            text "     " + "Serums Ready for Sale: " + str(mc.business.sale_inventory.get_any_serum_count()) style "textbutton_text_style"

    frame:
        background "#1a45a1aa"
        xalign 0.1
        yalign 0.48
        xanchor 0.0
        yanchor 0.0

        viewport:
            mousewheel True
            scrollbars "vertical"
            xsize 1500
            ysize 350
            vbox:
                text "Highlights:" style "textbutton_text_style" size 20
                for item in mc.business.message_list:
                    text "     " + item style "textbutton_text_style" text_align 0.0

                for item in mc.business.counted_message_list:
                    text "     " + item + " x " + str(int(mc.business.counted_message_list[item])) style "textbutton_text_style" text_align 0.0

    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.9]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action Return()
        textbutton "End Day" align [0.5,0.5] style "button_text" text_style "textbutton_text_style"
