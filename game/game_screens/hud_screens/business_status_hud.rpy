label check_business_inventory_loop:
    call screen show_serum_inventory(mc.business.inventory,[mc.business.sale_inventory],["Production Inventory","Waiting to Ship"])
    return

screen business_ui(): #Shows some information about your business.
    frame:
        background im.Flip("Info_Frame_1.png",vertical=True)
        xsize 600
        ysize 400
        yalign 1.0
        vbox:
            yanchor 1.0
            yalign 1.0
            spacing 5
            text "[mc.business.name]" style "menu_text_style" size 18 xalign 0.2
            textbutton "Employee Count: " + str(mc.business.get_employee_count()) + "/" + str(mc.business.max_employee_count):
                ysize 28
                text_style "menu_text_style"
                tooltip "Your current and maximum number of employees. Purchase new business policies from your main office to increase the number of employees you can have."
                action NullAction()
                sensitive True

            if mc.business.funds < 0:
                textbutton "Company Funds: $[mc.business.funds]":
                    ysize 28
                    text_style "menu_text_style"
                    text_color "#DD0000"
                    tooltip "The amount of money in your business account. If you are in the negatives for more than three days your loan defaults and the game is over!"
                    action NullAction()
                    sensitive True
            else:
                textbutton "Company Funds: $[mc.business.funds]":
                    ysize 28
                    text_style "menu_text_style"
                    tooltip "The amount of money in your business account. If you are in the negatives for more than three days your loan defaults and the game is over!"
                    action NullAction()
                    sensitive True

            textbutton "Daily Salary Cost: $"+ str(mc.business.calculate_salary_cost()):
                ysize 28
                text_style "menu_text_style"
                tooltip "The amount of money spent daily to pay your employees. Employees are not paid on the weekend."
                action NullAction()
                sensitive True

            textbutton "Company Efficency: [mc.business.team_effectiveness]%":
                ysize 28
                text_style "menu_text_style"
                tooltip "The more employees you have the faster your company will become inefficent. Perform HR work at your office or hire someone to do it for you to raise your company efficency. All productivity is modified by company efficency."
                action NullAction()
                sensitive True

            textbutton "Current Raw Supplys: " + str(int(mc.business.supply_count)) +"/[mc.business.supply_goal]":
                ysize 28
                text_style "menu_text_style"
                tooltip "Your current and goal amounts of serum supply. Manufacturing serum requires supplies, spend time ordering supplies from your office or hire someone to do it for you. Raise your supply goal from your office if you want to keep more supply stockpiled."
                action NullAction()
                sensitive True

            if not mc.business.active_research_design == None:
                text "  Current Research: " style "menu_text_style"
                textbutton "    [mc.business.active_research_design.name] (" + str(int(mc.business.active_research_design.current_research))+"/[mc.business.active_research_design.research_needed])":
                    ysize 28
                    text_style "menu_text_style"
                    tooltip "The current research task of your R&D division. Visit them to set a new goal or to assemble a new serum design."
                    action NullAction()
                    sensitive True

            else:
                textbutton "Current Research: None!":
                    ysize 28
                    text_style "menu_text_style"
                    text_color "#DD0000"
                    tooltip "The current research task of your R&D division. Visit them to set a new goal or to assemble a new serum design."
                    action NullAction()
                    sensitive True

            textbutton "Review Staff" action Show("employee_overview") style "textbutton_style" text_style "textbutton_text_style" xsize 220 tooltip "Review all of your current employees."
            textbutton "Check Stock" action ui.callsinnewcontext("check_business_inventory_loop") style "textbutton_style" text_style "textbutton_text_style" xsize 220 tooltip "Check the doses of serum currently waiting to be sold or sitting in your production area."
