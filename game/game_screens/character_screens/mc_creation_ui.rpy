init 0:
    default name = "Input Your First Name"
    default l_name = "Input Your Last Name"
    default b_name = "Input Your Business Name"

    python:
        def name_func(new_name):
            store.name = new_name

        def b_name_func(new_name):
            store.b_name = new_name

        def l_name_func(new_name):
            store.l_name = new_name

screen character_create_screen():

    default cha = 0
    default int = 0
    default foc = 0

    default h_skill = 0
    default m_skill = 0
    default r_skill = 0
    default p_skill = 0
    default s_skill = 0

    default F_skill = 0
    default O_skill = 0
    default V_skill = 0
    default A_skill = 0


    default name_select = 0

    default character_points = 20
    default stat_max = 4
    default work_skill_max = 4
    default sex_skill_max = 4

    imagebutton auto "/gui/Text_Entry_Bar_%s.png" action [SetScreenVariable("name_select",1), SetVariable("name","")] pos (320,800) xanchor 0.5 yanchor 0.5 alternate SetScreenVariable("name_select",0)
    imagebutton auto "/gui/Text_Entry_Bar_%s.png" action [SetScreenVariable("name_select",3), SetVariable("l_name","")] pos (320,880) xanchor 0.5 yanchor 0.5 alternate SetScreenVariable("name_select",0)
    imagebutton auto "/gui/Text_Entry_Bar_%s.png" action [SetScreenVariable("name_select",2), SetVariable("b_name","")] pos (320,960) xanchor 0.5 yanchor 0.5 alternate SetScreenVariable("name_select",0)
    imagebutton auto "/gui/button/choice_%s_background.png" action Return([[cha,int,foc],[h_skill,m_skill,r_skill,p_skill,s_skill],[F_skill,O_skill,V_skill,A_skill]]) pos (1560,900) xanchor 0.5 yanchor 0.5 sensitive character_points == 0


    if name_select == 1: #Name
        input default name pos(320,800) changed name_func xanchor 0.5 yanchor 0.5 style "menu_text_style" length 25
    else:
        text name pos(320,800) xanchor 0.5 yanchor 0.5 style "menu_text_style"

    if name_select == 3: #Last Name
        input default l_name pos(320,880) changed l_name_func xanchor 0.5 yanchor 0.5 style "menu_text_style" length 25
    else:
        text l_name pos(320,880) xanchor 0.5 yanchor 0.5 style "menu_text_style"

    if name_select == 2: #Business Name
        input default b_name pos(320,960) changed b_name_func xanchor 0.5 yanchor 0.5 style "menu_text_style" length 25
    else:
        text b_name pos(320,960) xanchor 0.5 yanchor 0.5 style "menu_text_style"


    if character_points > 0:
        text "Spend All Character Points to Proceed" style "menu_text_style" anchor(0.5,0.5) pos(1560,900)
    else:
        text "Finish Character Creation" style "menu_text_style" anchor(0.5,0.5) pos(1560,900)

    text "Character Points Remaining: [character_points]" style "menu_text_style" xalign 0.5 yalign 0.1 size 30
    hbox: #Main Stats Section
        yalign 0.7
        xalign 0.5
        xanchor 0.5
        frame:
            background "#1a45a1aa"
            vbox:
                xsize 550
                text "Main Stats (3 points/level)" style "menu_text_style" size 25
                null height 40
                hbox:
                    text "Charisma: " style "menu_text_style"
                    textbutton "<" action [SetScreenVariable("cha",cha-1), SetScreenVariable("character_points", character_points+3)] sensitive cha>0 style "textbutton_style" text_style "textbutton_text_style"
                    text str(cha) + "/[stat_max]" style "textbutton_text_style"
                    textbutton ">" action [SetScreenVariable("cha",cha+1), SetScreenVariable("character_points", character_points-3)] sensitive character_points>2 and cha<stat_max style "textbutton_style" text_style "textbutton_text_style"
                text "     Your visual appearance and force of personality. Charisma is the key attribute for selling serums and managing your business." style "menu_text_style"
                null height 30
                hbox:
                    text "Intelligence: " style "menu_text_style"
                    textbutton "<" action [SetScreenVariable("int",int-1), SetScreenVariable("character_points", character_points+3)] sensitive int>0 style "textbutton_style" text_style "textbutton_text_style"
                    text str(int) + "/[stat_max]" style "textbutton_text_style"
                    textbutton ">" action [SetScreenVariable("int",int+1), SetScreenVariable("character_points", character_points-3)] sensitive character_points>2 and int<stat_max style "textbutton_style" text_style "textbutton_text_style"
                text "     Your raw knowledge and ability to think quickly. Intelligence is the key attribute for research and development of serums." style "menu_text_style"
                null height 30
                hbox:
                    text "Focus: " style "menu_text_style"
                    textbutton "<" action [SetScreenVariable("foc",foc-1), SetScreenVariable("character_points", character_points+3)] sensitive foc>0 style "textbutton_style" text_style "textbutton_text_style"
                    text str(foc) + "/[stat_max]" style "textbutton_text_style"
                    textbutton ">" action [SetScreenVariable("foc",foc+1), SetScreenVariable("character_points", character_points-3)] sensitive character_points>2 and foc<stat_max style "textbutton_style" text_style "textbutton_text_style"
                text "     Your mental endurance and precision. Focus is the key attribute for production and supply procurement." style "menu_text_style"

        null width 40
        frame:
            background "#1a45a1aa"
            vbox:
                xsize 550
                text "Work Skills (1 point/level)" style "menu_text_style" size 25
                null height 40
                hbox:
                    text "Human Resources: " style "menu_text_style"
                    textbutton "<" action [SetScreenVariable("h_skill",h_skill-1), SetScreenVariable("character_points", character_points+1)] sensitive h_skill>0 style "textbutton_style" text_style "textbutton_text_style"
                    text str(h_skill)+"/[work_skill_max]" style "textbutton_text_style"
                    textbutton ">" action [SetScreenVariable("h_skill",h_skill+1), SetScreenVariable("character_points", character_points-1)] sensitive character_points>0 and h_skill<work_skill_max style "textbutton_style" text_style "textbutton_text_style"
                text "     Your skill at human resources. Crutial for maintaining an efficient business." style "menu_text_style"
                null height 30
                hbox:
                    text "Marketing: " style "menu_text_style"
                    textbutton "<" action [SetScreenVariable("m_skill",m_skill-1), SetScreenVariable("character_points", character_points+1)] sensitive m_skill>0 style "textbutton_style" text_style "textbutton_text_style"
                    text str(m_skill)+"/[work_skill_max]" style "textbutton_text_style"
                    textbutton ">" action [SetScreenVariable("m_skill",m_skill+1), SetScreenVariable("character_points", character_points-1)] sensitive character_points>0 and m_skill<work_skill_max style "textbutton_style" text_style "textbutton_text_style"
                text "     Your skill at marketing. Higher skill will allow you to ship more doses of serum per day." style "menu_text_style"
                null height 30
                hbox:
                    text "Research and Development: " style "menu_text_style"
                    textbutton "<" action [SetScreenVariable("r_skill",r_skill-1), SetScreenVariable("character_points", character_points+1)] sensitive r_skill>0 style "textbutton_style" text_style "textbutton_text_style"
                    text str(r_skill)+"/[work_skill_max]" style "textbutton_text_style"
                    textbutton ">" action [SetScreenVariable("r_skill",r_skill+1), SetScreenVariable("character_points", character_points-1)] sensitive character_points>0 and r_skill<work_skill_max style "textbutton_style" text_style "textbutton_text_style"
                text "     Your skill at researching new serum traits and designs. Critical for improving your serum inventory." style "menu_text_style"
                null height 30
                hbox:
                    text "Production: " style "menu_text_style"
                    textbutton "<" action [SetScreenVariable("p_skill",p_skill-1), SetScreenVariable("character_points", character_points+1)] sensitive p_skill>0 style "textbutton_style" text_style "textbutton_text_style"
                    text str(p_skill)+"/[work_skill_max]" style "textbutton_text_style"
                    textbutton ">" action [SetScreenVariable("p_skill",p_skill+1), SetScreenVariable("character_points", character_points-1)] sensitive character_points>0 and p_skill<work_skill_max style "textbutton_style" text_style "textbutton_text_style"
                text "     Your skill at producing serum in the production lab. Produced serums can then be sold for profit or kept for personal use." style "menu_text_style"
                null height 30
                hbox:
                    text "Supply Procurement: " style "menu_text_style"
                    textbutton "<" action [SetScreenVariable("s_skill",s_skill-1), SetScreenVariable("character_points", character_points+1)] sensitive s_skill>0 style "textbutton_style" text_style "textbutton_text_style"
                    text str(s_skill)+"/[work_skill_max]" style "textbutton_text_style"
                    textbutton ">" action [SetScreenVariable("s_skill",s_skill+1), SetScreenVariable("character_points", character_points-1)] sensitive character_points>0 and s_skill<work_skill_max style "textbutton_style" text_style "textbutton_text_style"
                text "     Your skill at obtaining raw supplies for your production division. Without supply, nothing can be created in the lab." style "menu_text_style"
                null height 30
        null width 40
        frame:
            background "#1a45a1aa"
            vbox:
                xsize 550
                text "Sex Skills (1 point/level)" style "menu_text_style" size 25
                null height 40
                hbox:
                    text "Foreplay: " style "menu_text_style"
                    textbutton "<" action [SetScreenVariable("F_skill",F_skill-1), SetScreenVariable("character_points", character_points+1)] sensitive F_skill>0 style "textbutton_style" text_style "textbutton_text_style"
                    text str(F_skill)+"/[sex_skill_max]" style "textbutton_text_style"
                    textbutton ">" action [SetScreenVariable("F_skill",F_skill+1), SetScreenVariable("character_points", character_points-1)] sensitive character_points>0 and F_skill<sex_skill_max style "textbutton_style" text_style "textbutton_text_style"
                text "     Your skill at foreplay, including fingering, kissing, and groping." style "menu_text_style"
                null height 30
                hbox:
                    text "Oral: " style "menu_text_style"
                    textbutton "<" action [SetScreenVariable("O_skill",O_skill-1), SetScreenVariable("character_points", character_points+1)] sensitive O_skill>0 style "textbutton_style" text_style "textbutton_text_style"
                    text str(O_skill)+"/[sex_skill_max]" style "textbutton_text_style"
                    textbutton ">" action [SetScreenVariable("O_skill",O_skill+1), SetScreenVariable("character_points", character_points-1)] sensitive character_points>0 and O_skill<sex_skill_max style "textbutton_style" text_style "textbutton_text_style"
                text "     Your skill at giving oral to women, as well as being a pleasant recipient." style "menu_text_style"
                null height 30
                hbox:
                    text "Vaginal: " style "menu_text_style"
                    textbutton "<" action [SetScreenVariable("V_skill",V_skill-1), SetScreenVariable("character_points", character_points+1)] sensitive V_skill>0 style "textbutton_style" text_style "textbutton_text_style"
                    text str(V_skill)+"/[sex_skill_max]" style "textbutton_text_style"
                    textbutton ">" action [SetScreenVariable("V_skill",V_skill+1), SetScreenVariable("character_points", character_points-1)] sensitive character_points>0 and V_skill<sex_skill_max style "textbutton_style" text_style "textbutton_text_style"
                text "     Your skill at vaginal sex in any position." style "menu_text_style"
                null height 30
                hbox:
                    text "Anal: " style "menu_text_style"
                    textbutton "<" action [SetScreenVariable("A_skill",A_skill-1), SetScreenVariable("character_points", character_points+1)] sensitive A_skill>0 style "textbutton_style" text_style "textbutton_text_style"
                    text str(A_skill)+"/[sex_skill_max]" style "textbutton_text_style"
                    textbutton ">" action [SetScreenVariable("A_skill",A_skill+1), SetScreenVariable("character_points", character_points-1)] sensitive character_points>0 and A_skill<sex_skill_max style "textbutton_style" text_style "textbutton_text_style"
                text "     Your skill at anal sex in any position." style "menu_text_style"
                null height 30
