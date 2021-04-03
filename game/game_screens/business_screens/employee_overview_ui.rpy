screen employee_overview(white_list = None, black_list = None, person_select = False): #If select is True it returns the person's name who you click on. If it is false it is a normal overview menu that lets you bring up their detailed info.
    modal True
    zorder 100
    add "Paper_Background.png"
    default division_select = "none"
    default division_name = "All"
    python:
        if not white_list: #If a white list is passed we will only display people that are on the list
            white_list = []
        if not black_list:
            black_list = [] #IF a black list is passed we will not include anyone on the blacklist. Blacklist takes priority

    $ showing_team = []
    $ display_list = []
    $ valid_person_count = 0

    python:
        if division_select == "none":
            showing_team = [] + mc.business.research_team + mc.business.production_team + mc.business.supply_team + mc.business.market_team + mc.business.hr_team
            division_name = "Everyone"
        elif division_select == "r":
            showing_team = mc.business.research_team #ie. take a shallow copy, so we can modify the team without everything exploding.
            division_name = "Research"
        elif division_select == "p":
            showing_team = mc.business.production_team
            division_name = "Production"
        elif division_select == "s":
            showing_team = mc.business.supply_team
            division_name = "Supply Procurement"
        elif division_select == "m":
            showing_team = mc.business.market_team
            division_name = "Marketing"
        elif division_select == "h":
            showing_team = mc.business.hr_team
            division_name = "Human Resources"

        display_list = [person for person in showing_team if (not white_list or person in white_list) and (not black_list or person not in black_list)] #Create our actual display list using people who are either on the white list or not on the black list


    vbox:
        xalign 0.5
        xanchor 0.5
        yalign 0.05
        yanchor 0.0
        spacing 20
        frame:
            background "#1a45a1aa"
            xsize 1800
            ysize 100
            if person_select:
                text "Staff Selection" xalign 0.5 xanchor 0.5 yalign 0.5 yanchor 0.5 size 36 style "menu_text_style"
            else:
                text "Staff Review" xalign 0.5 xanchor 0.5 yalign 0.5 yanchor 0.5 size 36 style "menu_text_style"
        frame:
            background "#1a45a1aa" xsize 1800
            hbox:
                xalign 0.5
                xanchor 0.5
                spacing 40
                $ button_mappings = [["All","none"],["Research","r"],["Production","p"],["Supply","s"],["Marketing","m"],["Human Resources","h"]]
                for button_map in button_mappings:
                    frame:
                        ysize 80
                        if division_select == button_map[1]:
                            background "#4f7ad6"
                        else:
                            background "#1a45a1"
                        button:
                            action SetScreenVariable("division_select", button_map[1])
                            xsize 200
                            ysize 60
                            text button_map[0] xalign 0.5 xanchor 0.5 yalign 0.5 yanchor 0.5 style "textbutton_text_style"




        # text "Position: " + division_name style "menu_text_style" size 24 yalign 0.18 xalign 0.02 xanchor 0.0
        frame:
            yanchor 0.0
            background "#1a45a1aa"
            xsize 1800
            $ grid_count = 15
            # if person_select:
            #     $ grid_count += 1
            viewport:
                xsize 1800
                ysize  585
                scrollbars "vertical"
                mousewheel True

                grid grid_count len(display_list)+1:
                    text "Name" style "menu_text_style" xsize 120 size 14
                    # if person_select:
                    #     text "" style "menu_text_style" xsize 120 size 14
                    text "Salary" style "menu_text_style" xsize 120 size 14
                    text "Happiness" style "menu_text_style" xsize 120 size 14
                    text "Obedience" style "menu_text_style" xsize 120 size 14
                    text "Love" style "menu_text_style" xsize 120 size 14
                    text "Sluttiness" style "menu_text_style" xsize 120 size 14
                    text "Suggest" style "menu_text_style" xsize 120 size 14
                    text "Charisma" style "menu_text_style" xsize 120 size 14
                    text "Int" style "menu_text_style" xsize 120 size 14
                    text "Focus" style "menu_text_style" xsize 120 size 14
                    text "Research" style "menu_text_style" xsize 120 size 14
                    text "Production " style "menu_text_style" xsize 120 size 14
                    text "Supply" style "menu_text_style" xsize 120 size 14
                    text "Marketing " style "menu_text_style" xsize 120 size 14
                    text "HR" style "menu_text_style" xsize 120 size 14


                    for person in display_list:
                        vbox:
                            textbutton person.name + "\n" + person.last_name style "textbutton_style" text_style "menu_text_style" action Show("person_info_detailed",None,person) xmaximum 120 xfill True text_size 12
                            if person_select:
                                textbutton "Select" style "textbutton_style" text_style "menu_text_style" action Return(person) xsize 120 yalign 0.5 text_size 12
                        text "$" + str(person.salary) + "/day" style "menu_text_style" xsize 120 yalign 0.5 size 12
                        text str(int(person.happiness)) style "menu_text_style" xsize 120 yalign 0.5 size 12
                        text str(int(person.obedience)) style "menu_text_style" xsize 120 yalign 0.5 size 12
                        text str(int(person.love)) style "menu_text_style" xsize 120 yalign 0.5 size 12
                        text str(int(person.sluttiness)) style "menu_text_style" xsize 120 yalign 0.5 size 12
                        text str(int(person.suggestibility)) style "menu_text_style" xsize 120 yalign 0.5 size 12
                        text str(int(person.charisma)) style "menu_text_style" xsize 120 yalign 0.5 size 12
                        text str(int(person.int)) style "menu_text_style" xsize 120 yalign 0.5 size 12
                        text str(int(person.focus)) style "menu_text_style" xsize 120 yalign 0.5 size 12
                        text str(int(person.research_skill)) style "menu_text_style" xsize 120 yalign 0.5 size 12
                        text str(int(person.production_skill)) style "menu_text_style" xsize 120 yalign 0.5 size 12
                        text str(int(person.supply_skill)) style "menu_text_style" xsize 120 yalign 0.5 size 12
                        text str(int(person.market_skill)) style "menu_text_style" xsize 120 yalign 0.5 size 12
                        text str(int(person.hr_skill)) style "menu_text_style" xsize 120 yalign 0.5 size 12


    if not person_select:
        frame:
            background None
            anchor [0.5,0.5]
            align [0.5,0.88]
            xysize [500,125]
            imagebutton:
                align [0.5,0.5]
                auto "gui/button/choice_%s_background.png"
                focus_mask "gui/button/choice_idle_background.png"
                action Hide("employee_overview")
            textbutton "Return" align [0.5,0.5] style "return_button_style" text_style "return_button_style"
