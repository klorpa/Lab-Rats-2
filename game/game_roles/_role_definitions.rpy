# This file holds the initialization information and general storyline info for all of the roles in the game. Individual roles and individual files.
init -1 python:
    def always_true(the_person):
        return True

label instantiate_roles(): #This section instantiates all of the key roles in the game. It is placed here to ensure it is properly created, saved, ect. by Renpy.
    #If this is in an init block each Role is reinstantiated on startup, meaning role references become confused.
    #All of the role labels and requirements are defined in their own file, but their Action representitions are stored here for saving purposes.
    #EMPLOYEE ACTIONS#
    python:
        move_employee_action = Action("Move her to a new division", move_employee_requirement, "move_employee_label",
            menu_tooltip = "Move her to a new division, where her skills might be put to better use.")
        employee_complement_action = Action("Compliment her work.", employee_complement_requirement, "employee_complement_work",
            menu_tooltip = "Offer a few kind words about her performance at work. Increases happiness and love, dependent on your charisma.")
        employee_insult_action = Action("Insult her work.", employee_insult_requirement, "insult_recent_work",
            menu_tooltip = "Offer a few choice words about her performance at work. Lowers love and happiness, but is good for instilling obedience.")
        employee_pay_cash_action = Action("Pay her a cash bonus.", employee_pay_cash_requirement, "employee_pay_cash_bonus",
            menu_tooltip = "A bonus in cold hard cash is good for obedience and happiness. The larger the reward the greater the effect.")
        employee_performance_review = Action("Start a performance review. {image=gui/heart/Time_Advance.png}", employee_performance_review_requirement , "employee_performance_review",
            menu_tooltip = "Bring her to your office for a performance review. Get her opinion about her job, reward, punish, or fire her as you see fit. Can only be done once every seven days.")
        employee_paid_serum_test = Action("Test serum (paid) -$100.", employee_paid_serum_test_requirement, "employee_paid_serum_test_label",
            menu_tooltip = "Pay her to willingly take a dose of serum, per company policy.")
        employee_unpaid_serum_test = Action("Test serum (unpaid).", employee_unpaid_serum_test_requirement, "employee_unpaid_serum_test_label",
            menu_tooltip = "Give her a dose of serum to test on herself, per company policy.")
        employee_punishment = Action("Punish her.", employee_punishment_hub_requirement, "employee_punishment_hub",
            menu_tooltip = "Punish her for any violations of company policy.", priority = 5)
        employee_generate_infraction = Action("Invent an infraction.", employee_generate_infraction_requirement, "employee_generate_infraction_label",
            menu_tooltip = "Company policy here is so complicated it's nearly impossible to go a day without violating some minor rule. If you were paranoid, you might think it was written that way on purpose...")

        employee_role = Role("Employee", [employee_paid_serum_test, employee_unpaid_serum_test, employee_complement_action, employee_insult_action, employee_pay_cash_action, employee_performance_review, move_employee_action, employee_punishment, employee_generate_infraction],
            on_turn = employee_on_turn, on_day = employee_on_day)

        #EMPLOYEE BUSYWORK ACTIONS#
        employee_busywork_role = Role("Office Busywork", [], hidden = True) #TODO: Add some other actions to this role
        employee_role.link_role(employee_busywork_role) #Link this role to the employee_role, so they are removed at the same time.

        #EMPLOYEE HUMILIATING WORK ACTIONS#
        employee_humiliating_work_role = Role("Humiliating Office Work", [], hidden = True) #TODO: Add some other actions to this role.
        employee_role.link_role(employee_humiliating_work_role)

        #EMPLOYEE FREEUSE ACTIONS#
        freeuse_fuck = Action("Fuck her", freeuse_fuck_requirement, "employee_freeuse_fuck",
            menu_tooltip = "Grab your free use slut and have some fun with her.")

        employee_freeuse_role = Role("Freeuse Slut", [freeuse_fuck], hidden = True)
        employee_role.link_role(employee_freeuse_role)

        #HEAD RESEARCHER ACTIONS#
        improved_serum_unlock = Action("Ask about advancing your research.", improved_serum_unlock_requirement, "improved_serum_unlock_label",
            menu_tooltip = "Your basic initial research can only take you so far. You will need a breakthrough to discover new serum traits.", priority = 10)

        visit_nora_intro = Action("Visit Nora to try and advance your research.", visit_nora_intro_requirement, "nora_intro_label",
            menu_tooltip = "Have your head researcher reach out to your old mentor to see if she can help advance your research.", priority = 10)

        advanced_serum_unlock_stage_1 = Action("Ask about advancing your research.", advanced_serum_stage_1_requirement, "advanced_serum_stage_1_label",
            menu_tooltip = "Another breakthrough will unlock new serum traits.", priority = 10)

        advanced_serum_unlock_stage_3 = Action("Present with recording of prototype serum test.", advanced_serum_stage_3_requirement, "advanced_serum_stage_3_label",
            menu_tooltip = "Your new head researcher will have to take over now, and this recording should help them.", priority = 10)

        futuristic_serum_unlock_stage_1 = Action("Ask about advancing your research.", futuristic_serum_stage_1_requirement, "futuristic_serum_stage_1_label",
            menu_tooltip = "You will need another breakthrough to unlock new serum traits.", priority = 10) #First time you ask about it

        futuristic_serum_unlock_stage_2 = Action("Talk about the test subjects.", futuristic_serum_stage_2_requirement, "futuristic_serum_stage_2_label",
            menu_tooltip = "Your head researcher needs willing, dedicated test subjects to advance your research any further.", priority = 10) #Talk to her to either select test subjects or get a refresher on what you need.


        fire_head_researcher_action = Action("Remove her as head researcher.", fire_head_researcher_requirement, "fire_head_researcher",
            menu_tooltip = "Remove her as your head researcher so you can select another. Without a head researcher your R&D department will be less efficent.")

        head_researcher = Role("Head Researcher", [fire_head_researcher_action,improved_serum_unlock,advanced_serum_unlock_stage_1, visit_nora_intro, advanced_serum_unlock_stage_3,futuristic_serum_unlock_stage_1, futuristic_serum_unlock_stage_2])


        #MODEL ACTIONS#

        model_ad_photo_list = Action("Shoot pictures for an advertisement. {image=gui/heart/Time_Advance.png}", model_photography_list_requirement, "model_photography_list_label", priority = 5)

        fire_model_action = Action("Remove her as your company model.", fire_model_requirment, "fire_model_label",
            menu_tooltip = "Remove her as your company model so you can give the position to someone else. Effects from existing ad campaigns will continue until they expire.")

        company_model_role = Role("Model", [model_ad_photo_list, fire_model_action])


        #STEPH ACTIONS#

        steph_role = Role("Stephanie", [], hidden = True) #Used to hold any Stephanie specific actions not tied to another role, and to guarantee this is Steph even if she undergoes a personality change.

        #NORA ROLE#
        # Note: Nora's role actions are assigned through Stephanie's events.

        nora_student_exam_rewrite_request_action = Action("Ask her about the exam rewrite.", nora_student_exam_rewrite_request_requirement, "nora_student_exam_rewrite_request",
            menu_tooltip = "Ask if she can set up a new exam for your student.") # This crisis triggers if your RL ever gets to 2 or higher without her introing herself. Provides an alternative way to the university.

        nora_role = Role("Nora", [nora_student_exam_rewrite_request_action], hidden = True)

        #ALEXIA ACTIONS#
        alexia_ad_reintro = Action("Have her order photography equipment. -$500", alexia_ad_suggest_reintro_requirement, "alexia_ad_suggest_reintro_label")

        alexia_ad_photo_intro = Action("Shoot pictures for your business cards. {image=gui/heart/Time_Advance.png}", alexia_photography_intro_requirement, "alexia_photography_intro_label") #This vent leads to Alexia being given the model role.

        alexia_role = Role("Alexia", [alexia_ad_reintro, alexia_ad_photo_intro], hidden = True) #Hide her role because we don't want to display it.

        #SISTER ACTIONS#
        sister_reintro_action = Action("Ask if she needs extra work.", sister_reintro_action_requirement, "sister_reintro_label",
            menu_tooltip = "She was eager to make some money before, maybe she still is.")

        sister_serum_test_action = Action("Ask her to test serum.", sister_serum_test_requirement, "sister_serum_test_label",
            menu_tooltip = "Have your sister test serum for you. Over time she will become more comfortable following your orders and making deals with you.")


        sister_strip_reintro_action = Action("Ask if she would strip for pay.", sister_strip_reintro_requirement, "sister_strip_reintro_label",
            menu_tooltip = "She was eager to make some money, maybe she will be willing to strip for you if you pay her.")

        sister_strip_action = Action("Ask her to strip for you.", sister_strip_requirement, "sister_strip_label",
            menu_tooltip = "Have your sister strip for you, in exchange for some money.", priority = 5)

        sister_boobjob_give_serum_action = Action("Give her some breast enhancement serum.", sister_boobjob_give_serum_requirement, "sister_give_boobjob_serum_label",
            menu_tooltip = "Give your sister some serum, which she thinks will grow her boobs.", priority = 10)

        sister_boobjob_ask_action = Action("Talk to her about getting implants.", sister_get_boobjob_talk_requirment, "sister_get_boobjob",
            menu_tooltip = "Talk to your sister about the implants she wants to get.", priority = 10)

        sister_mom_girlfriend_blessing_action = Action("Talk to her about Mom.", mom_girlfriend_ask_blessing_requirement, "mom_girlfriend_sister_blessing",
            menu_tooltip = "Try and convince her to give you and Mom her blessing.", priority = 100)

        sister_girlfriend_return_action = Action("Give her the news.", sister_girlfriend_return_requirement, "sister_girlfriend_return",
            menu_tooltip = "Tell her how your conversation with Mom went.", priority = 100)

        sister_role = Role("Sister", [sister_reintro_action, sister_serum_test_action, sister_strip_reintro_action, sister_strip_action, sister_boobjob_give_serum_action, sister_boobjob_ask_action, sister_mom_girlfriend_blessing_action, sister_girlfriend_return_action],
            on_day = sister_on_day)

        sister_hire_offer_action = Action("Offer to hire her.", sister_offer_to_hire_requirement, "sister_offer_to_hire",
            menu_tooltip = "Offer her a job at your company. You'll have to convince her to drop out of school first...")

        sister_student_role = Role("Student", [sister_hire_offer_action], hidden = True)


        #MOTHER ACTIONS#
        mother_offer_make_dinner = Action("Offer to make dinner. {image=gui/heart/Time_Advance.png}", mom_offer_make_dinner_requirement, "mom_offer_make_dinner_label",
            menu_tooltip = "Earn some good will by making dinner for your mother and sister.", priority = 5)

        mom_work_promotion_two_prep_action = Action("Prepare for her interview.", mom_work_promotion_two_prep_requirement, "mom_work_promotion_two_prep",
            menu_tooltip = "Help your mom prepare for her one-on-one interview.", priority = 10)

        mom_work_bigger_tits_reintro = Action("Talk to her about getting bigger tits.", mom_work_secretary_replacement_bigger_tits_reintro_requirement, "mom_work_secretary_replacement_bigger_tits_reintro",
            menu_tooltip = "Talk to her about improving her natural assets, either with implants or by using some of your serum.", priority = 10)

        mom_sister_girlfriend_blessing_action = Action("Talk to her about Lily.", sister_girlfriend_ask_blessing_requirement, "sister_girlfriend_mom_blessing",
            menu_tooltip = "Try and convince her to give you and Lily her blessing.", priority = 100)

        mom_girlfriend_return_action = Action("Give her the news.", mom_girlfriend_return_requirement, "mom_girlfriend_return",
            menu_tooltip = "Tell her how your conversation with Lily went.", priority = 100)

        mother_role = Role("Mother", [mother_offer_make_dinner, mom_work_promotion_two_prep_action, mom_work_bigger_tits_reintro, mom_sister_girlfriend_blessing_action, mom_girlfriend_return_action],
            on_day = mom_on_day)

        mom_convince_quit_action = Action("Convince her to quit her job.", mom_convince_quit_requirement, "mom_convince_quit_label", priority = -5)

        mom_associate_role = Role("Business Associate", [mom_convince_quit_action], hidden = True) #Used for the different jobs she holds in various events
        mom_secretary_role = Role("Personal Associate", [mom_convince_quit_action], hidden = True) #TODO: Have the ability to link random events to roles.


        #AUNT ACTIONS#
        aunt_help_move = Action("Help her move into her apartment. {image=gui/heart/Time_Advance.png}", aunt_intro_moving_apartment_requirement, "aunt_intro_moving_apartment_label",
            menu_tooltip = "Help your aunt and your cousin move their stuff from your house to their new apartment. They're sure to be grateful, and it would give you a chance to snoop around.", priority = 5)

        aunt_share_drinks_action = Action("Share a glass of wine. {image=gui/heart/Time_Advance.png}", aunt_share_drinks_requirement, "aunt_share_drinks_label",
            menu_tooltip = "Sit down with your aunt and share a glass or two of wine. Maybe a little bit of alcohol will loosen her up a bit.", priority = 10)

        aunt_offer_hire_action = Action("Offer to hire her.", aunt_offer_hire_requirement, "aunt_offer_hire", priority = -5)

        aunt_role = Role("Aunt", [aunt_help_move, aunt_share_drinks_action, aunt_offer_hire_action])


        #COUSIN ACTIONS#
        cousin_blackmail_action = Action("Blackmail her.", cousin_blackmail_requirement, "cousin_blackmail_label",
            menu_tooltip = "Threaten to tell her mother about what she's been doing and see what you can get out of her.", priority = 10)

        cousin_role = Role("Cousin", [cousin_blackmail_action])

        #COUSIN After start actions# - Actions that are meant to be added to her action list after the game has begun.
        cousin_talk_boobjob_again_action = Action("Talk to her about getting a boobjob. -$5000", cousin_talk_boobjob_again_requirement, "cousin_talk_boobjob_again_label")
        #cousin_role.actions.append(cousin_talk_boobjob_again_action)

        #GENERIC STUDENT ACTIONS
        generic_student_role = Role("Student", [], hidden = True)

        #STUDENT ACTIONS#
        #student_study_meetup_action = Action("Tutor her. {image=gui/heart/Time_Advance.png}", student_study_meetup_requirement, "student_study_meetup")

        student_reintro_action = Action("Ask about tutoring her.", student_reintro_requirement, "student_reintro")

        student_study_propose_action = Action("Tutor her. {image=gui/heart/Time_Advance.png}", student_study_propose_requirement, "student_study_propose")

        student_test_intro_action = Action("Tell her she can rewrite her exam.", student_test_intro_requirement, "student_test_intro")

        student_test_action = Action("Time to rewrite her exam. {image=gui/heart/Time_Advance.png}", student_test_requirement, "student_test")

        student_offer_job_reintro_action = Action("Offer her a job.", student_offer_job_requirement, "student_offer_job_reintro")

        student_role = Role("Student", [student_reintro_action, student_study_propose_action, student_test_intro_action, student_test_action, student_offer_job_reintro_action], hidden = True) #This can now be hidden, becuase "student" is shown as her job.

        ################
        #INTERNET ROLES#
        ################
        #These roles are given to any girl who has an account on the particular site, even if you don't know about it.


        instapic_role = Role("On InstaPic", [], hidden = True, on_turn = insta_on_turn, on_day = insta_on_day)


        dikdok_role = Role("On Dikdok", [], hidden = True, on_turn = dikdok_on_turn, on_day = dikdok_on_day)


        onlyfans_role = Role("On OnlyFanatics", [], hidden = True, on_turn = onlyfans_on_turn, on_day = onlyfans_on_day)


        ####################
        #RELATIONSHIP ROLES#
        ####################

        #GIRLFRIEND ACTIONS#
        # Give her gifts (bonus happiness + Love)
        # She tests serum for you for free.
        # Go on dates (Remove this option from the normal chat menu?)
        # If she has (of age) kids, meet them (and, amazingly, they're hot young women!)

        #Other things to add#
        # Enables new girlfriend specific crises.
        # Adds more love to seduction attempts (reduce love from other sources)
        # Fallout if your girlfriend catches you with someone else.

        plan_fuck_date_action = Action("Plan a fuck date at her place.", fuck_date_requirement, "plan_fuck_date_label", menu_tooltip = "Pick a night to go over there and spend nothing but \"quality time\" with each other.")

        girlfriend_shopping_date = Action("Go shopping together. {image=gui/heart/Time_Advance.png}", shopping_date_requirement, "shopping_date_intro", menu_tooltip = "Take her to the mall and do some shopping together.")

        ask_break_up_action = Action("Break up with her.", ask_break_up_requirement, "ask_break_up_label", menu_tooltip = "Breaking up may break her heart, but it'll be easier on her than catching you with another woman.")
        ask_get_boobjob_action = Action("Ask her to get a boob job. -$7000", ask_get_boobjob_requirement, "ask_get_boobjob_label", menu_tooltip = "A little silicone goes a long way. Ask her to get breast enhancement surgery for you.")
        girlfriend_ask_trim_pubes_action = Action("Ask her to trim her pubes.", girlfriend_ask_trim_pubes_requirement, "girlfriend_ask_trim_pubes_label", menu_tooltip = "Ask her to do a little personal landscaping. Tell her to wax it off, grow it out, or shape it into anything in between.")

        girlfriend_role = Role("Girlfriend", [ask_break_up_action, ask_get_boobjob_action, girlfriend_ask_trim_pubes_action], role_dates = [plan_fuck_date_action, girlfriend_shopping_date]) #Your girlfriend, and she's not in a relationship with anyone else
        #Getting married is some kind of victory for the game?


        sister_girlfriend_role = Role("Girlfriend", [ask_break_up_action, ask_get_boobjob_action, girlfriend_ask_trim_pubes_action],
            role_dates = [girlfriend_shopping_date, plan_fuck_date_action],
            looks_like = girlfriend_role) #Sister specific girlfriend role.

        mom_girlfriend_role = Role("Girlfriend", [ask_break_up_action, ask_get_boobjob_action, girlfriend_ask_trim_pubes_action],
            role_dates = [girlfriend_shopping_date, plan_fuck_date_action],
            looks_like = girlfriend_role) #Sister specific girlfriend role.

        #affair ACTIONS
        # Sneaky versions of all of the normal girlfriend stuff
        # Have her get money from her (b/f/h) and give it to you.
        # Convince her to leave her (boyfriend/fiance/husband) for you. Changes to her being your girlfriend.
        # Start to blackmail her for money or sex.

        ask_leave_SO_action = Action("Ask her to leave her significant other for you.", ask_leave_SO_requirement, "ask_leave_SO_label", menu_tooltip = "This affair has been secret long enough! Ask her to leave her significant other and make your relationship official.")
        affair_role = Role("Paramour", [ask_get_boobjob_action, girlfriend_ask_trim_pubes_action, ask_leave_SO_action], role_dates = plan_fuck_date_action) #A woman who is in a relationship but also wants to fuck you because of love (rather than pure sluttiness, where she thinks that's normal)


        ###################
        ### TRANCE ROLE ###
        ###################

        trance_training_action = Action("Take advantage of her trance.", trance_train_requirement, "trance_train_label", menu_tooltip = "Take advantage of her orgasm-induced trance and make some changes while she is highly suggestible.")


        trance_role = Role("In a Trance", actions = [trance_training_action], on_turn = trance_on_turn, on_day = trance_on_day)
        heavy_trance_role = Role("In a Deep Trance", actions = [trance_training_action], on_turn = trance_on_turn, on_day = trance_on_day, looks_like = trance_role)
        very_heavy_trance_role = Role("In a Very Deep Trance", actions = [trance_training_action], on_turn = trance_on_turn, on_day = trance_on_day, looks_like = heavy_trance_role)

        #######################
        ### TRAINABLE ROLES ###
        #######################
        breeder_fuck_action = Action("Offer to knock her up.", breeder_fuck_requirement, "breeder_fuck", menu_tooltip = "She wants to get pregnant. You could help with that." )

        breeder_role = Role("Eager Breeder", actions = [breeder_fuck_action]) #TODO: Add an on-day (or on-turn?) LTE when her fertility is really high and she begs you to fuck her.


        hypno_trigger_orgasm_action = Action("Trigger an orgasm.", hypno_trigger_orgasm_requirement, "hypno_trigger_orgasm", menu_tooltip = "You've implanted a trigger word. You can make her cum whenever you want.")
        hypno_trigger_online_action = Action("Trigger an orgasm.", hypno_trigger_orgasm_requirement, "hypno_trigger_online", menu_tooltip = "You've implanted a trigger word, it should work over a text message.")

        hypno_orgasm_role = Role("Hypno Orgasm", actions = [hypno_trigger_orgasm_action], hidden = True, on_turn = hypno_orgasm_on_turn, internet_actions = [hypno_trigger_online_action])

        ###################
        ### OTHER ROLES ###
        ###################

        unemployed_hire_action = Action("Offer to hire her.", offer_to_hire_requirement, "unemployed_offer_hire")
        unemployed_role = Role("Unemployed", [unemployed_hire_action], hidden = True)

        critical_job_role = Role("Critcal Job", [], hidden = True) # Used for role where it is impossible to get the character to quit their job, but they don't have anything else going on.

        unimportant_hire_action = Action("Offer to hire her.", offer_to_hire_requirement, "unimportant_job_offer_hire")
        unimportant_job_role = Role("Unimportant Job", [unimportant_hire_action], hidden = True) # Used for roles where it is relatively simple to get the character to quit their job.

        stripper_dance_action = Action("Ask for a private dance. -$100", stripper_private_dance_requirement, "stripper_private_dance_label",
            menu_tooltip = "Ask her to a back room for a private dance.")
        stripper_hire_action = Action("Offer to hire her.", offer_to_hire_requirement, "stripper_offer_hire")
        stripper_role = Role("Stripper", [stripper_dance_action, stripper_hire_action], hidden = True)

        prostitute_action = Action("Pay her for sex. -$200", prostitute_requirement, "prostitute_label",
            menu_tooltip = "You know she's a prostitute. Pay her to have sex with you.")
        prostitute_hire_action = Action("Offer to hire her.", offer_to_hire_requirement, "prostitute_hire_offer")
        prostitute_role = Role("Prostitute", [prostitute_action], hidden = True) #Now a hidden role, because "prostitute" is listed as her job.

        pregnant_role = Role("Pregnant", [], hidden = True)

        milk_for_serum_action = Action("Milk her for serum. -15{image=gui/extra_images/energy_token.png}", milk_for_serum_requirement, "milk_for_serum_label", menu_tooltip = "Those tits contain company property!")
        lactating_serum_role = Role("Lactating Serum", [milk_for_serum_action], hidden = True, on_turn = lactating_serum_on_turn, on_day = lactating_serum_on_day)


        # crity rep role trainables
        city_rep_dressup_training = Trainable("City_Rep_Dressup", "city_rep_dressup_training", "Slutty Work Uniform.", unlocked_function = city_rep_dressup_training_requirement, doubling_amount = 4)
        city_rep_penalty_reduction_training = Trainable("City_Rep_Pen_Reduct", "city_rep_penalty_reduction_training", "Reduce Penalty Severity", 200, city_rep_penalty_reduction_training_requirement)
        city_rep_internal_sabotage_training = Trainable("City_Rep_Satbo", "city_rep_internal_sabotage_training", "Sabotage Investigations", 400, city_rep_internal_sabotage_training_requirement)

        city_rep_hire = Action("Offer to hire her.", offer_to_hire_requirement, "city_rep_offer_hire")

        city_rep_role = Role("City Representative", [city_rep_hire], role_trainables = [city_rep_dressup_training, city_rep_penalty_reduction_training, city_rep_internal_sabotage_training])

return
