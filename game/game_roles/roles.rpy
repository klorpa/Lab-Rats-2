# This file holds the initialization information and general storyline info for all of the roles in the game. Individual roles and individual files.
init -1 python:
    def prostitute_requirement(the_person):
        if mc.business.funds < 200:
            "Not enough cash"
        elif the_person.sexed_count >= 1:
            "She's worn out. Maybe later."
        else:
            return True

    def always_true(the_person):
        return True

label instantiate_roles(): #This section instantiates all of the key roles in the game. It is placed here to ensure it is properly created, saved, ect. by Renpy.
    #All of the role labels and requirements are defined in their own file, but their Action representitions are stored here for saving purposes.
    python:
        #EMPLOYEE ACTIONS#
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
        nora_role = Role("Nora", [], hidden = True)

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

        sister_role = Role("Sister", [sister_reintro_action, sister_serum_test_action, sister_strip_reintro_action, sister_strip_action])


        #MOTHER ACTIONS#
        mother_offer_make_dinner = Action("Offer to make dinner. {image=gui/heart/Time_Advance.png}", mom_offer_make_dinner_requirement, "mom_offer_make_dinner_label",
            menu_tooltip = "Earn some good will by making dinner for your mother and sister.", priority = 5)

        mom_work_promotion_two_prep_action = Action("Prepare for her interview.", mom_work_promotion_two_prep_requirement, "mom_work_promotion_two_prep",
            menu_tooltip = "Help your mom prepare for her one-on-one interview.", priority = 10)

        mom_work_bigger_tits_reintro = Action("Talk to her about getting bigger tits.", mom_work_secretary_replacement_bigger_tits_reintro_requirement, "mom_work_secretary_replacement_bigger_tits_reintro",
            menu_tooltip = "Talk to her about improving her natural assets, either with implants or by using some of your serum.", priority = 10)

        mom_debug_test = Action("DEBUG", always_true, "text_message_style_test")

        mother_role = Role("Mother", [mother_offer_make_dinner, mom_work_promotion_two_prep_action, mom_work_bigger_tits_reintro])


        #AUNT ACTIONS#
        aunt_help_move = Action("Help her move into her apartment. {image=gui/heart/Time_Advance.png}", aunt_intro_moving_apartment_requirement, "aunt_intro_moving_apartment_label",
            menu_tooltip = "Help your aunt and your cousin move their stuff from your house to their new apartment. They're sure to be grateful, and it would give you a chance to snoop around.", priority = 5)

        aunt_share_drinks_action = Action("Share a glass of wine. {image=gui/heart/Time_Advance.png}", aunt_share_drinks_requirement, "aunt_share_drinks_label",
            menu_tooltip = "Sit down with your aunt and share a glass or two of wine. Maybe a little bit of alcohol will loosen her up a bit.", priority = 10)

        aunt_role = Role("Aunt", [aunt_help_move,aunt_share_drinks_action])


        #COUSIN ACTIONS#
        cousin_blackmail_action = Action("Blackmail her.", cousin_blackmail_requirement, "cousin_blackmail_label",
            menu_tooltip = "Threaten to tell her mother about what she's been doing and see what you can get out of her.", priority = 10)

        cousin_role = Role("Cousin", [cousin_blackmail_action])

        #COUSIN After start actions# - Actions that are meant to be added to her action list after the game has begun.
        cousin_talk_boobjob_again_action = Action("Talk to her about getting a boobjob. -$5000", cousin_talk_boobjob_again_requirement, "cousin_talk_boobjob_again_label")
        #cousin_role.actions.append(cousin_talk_boobjob_again_action)

        #STUDENT ACTIONS#
        #student_study_meetup_action = Action("Tutor her. {image=gui/heart/Time_Advance.png}", student_study_meetup_requirement, "student_study_meetup")

        student_reintro_action = Action("Ask about tutoring her.", student_reintro_requirement, "student_reintro")

        student_study_propose_action = Action("Tutor her. {image=gui/heart/Time_Advance.png}", student_study_propose_requirement, "student_study_propose")

        student_role = Role("Student", [student_reintro_action, student_study_propose_action])

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

        ask_break_up_action = Action("Break up with her.", ask_break_up_requirement, "ask_break_up_label", menu_tooltip = "Breaking up may break her heart, but it'll be easier on her than catching you with another woman.")

        ask_get_boobjob_action = Action("Ask her to get a boob job. -$7000", ask_get_boobjob_requirement, "ask_get_boobjob_label", menu_tooltip = "A little silicone goes a long way. Ask her to get breast enhancement surgery for you.")

        girlfriend_ask_trim_pubes_action = Action("Ask her to trim her pubes.", girlfriend_ask_trim_pubes_requirement, "girlfriend_ask_trim_pubes_label", menu_tooltip = "Ask her to do a little personal landscaping. Tell her to wax it off, grow it out, or shape it into anything in between.")

        girlfriend_role = Role("Girlfriend", [ask_break_up_action, ask_get_boobjob_action, girlfriend_ask_trim_pubes_action]) #Your girlfriend, and she's not in a relationship with anyone else
        #Getting married is some kind of victory for the game?


        #affair ACTIONS
        # Sneaky versions of all of the normal girlfriend stuff
        # Have her get money from her (b/f/h) and give it to you.
        # Convince her to leave her (boyfriend/fiance/husband) for you. Changes to her being your girlfriend.
        # Start to blackmail her for money or sex.

        plan_fuck_date_action = Action("Plan a fuck date at her place.", fuck_date_requirement, "plan_fuck_date_label", menu_tooltip = "Pick a night to go over there and spend nothing but \"quality time\" with each other.")
        ask_leave_SO_action = Action("Ask her to leave her significant other for you.", ask_leave_SO_requirement, "ask_leave_SO_label", menu_tooltip = "This affair has been secret long enough! Ask her to leave her significant other and make your relationship official.")
        affair_role = Role("Paramour", [plan_fuck_date_action, ask_get_boobjob_action, girlfriend_ask_trim_pubes_action, ask_leave_SO_action]) #A woman who is in a relationship but also wants to fuck you because of love (rather than pure sluttiness, where she thinks that's normal)


        ###################
        ### OTHER ROLES ###
        ###################

        prostitute_action = Action("Pay her for sex. -$200", prostitute_requirement, "prostitute_label",
            menu_tooltip = "You know she's a prostitute, pay her to have sex with you.")

        prostitute_role = Role("Prostitute", [prostitute_action])



        pregnant_role = Role("Pregnant", [], hidden = True)
    return




label pay_strip_scene(the_person):
    # TODO: Figure out where this scene should go, since this file should be a pure role-define section.
    #A loop where someone strips if you pay them. Not nessicarily limited to the Lily-MC relationship.
    #Concept: tell the girl what position to stand in and ask her to take things off for you. If her outfit is conservative she'll strip for free, when it starts to get slutty she'll want extra cash.
    #High obedience will sub in for sluttiness; an obedient girl will strip just because you ask.
    #Compliment, insult, etc. to change some of her stats.

    #Requirements: Person can be told to stand in a few different positions. Some are unlocked at higher sluttiness.
    #Requirements: Person can be asked to take off clothing.
    #Requirements: Some they will strip off on their own.
    #Requirements: Person will demand some amount of $$$ while stripping if they feel it's slutty.
    #Requirements: Person will have different descriptions of stripping/dancing depending on sluttiness.
    #Optional: Some way to ask the person to change into a different outfit.
    #Optional: Way to progress from strip tease to sex and/or mastribation.

    $ pose_list = [["Turn around","walking_away"],["Turn around and look back","back_peek"],["Be flirty","stand2"],["Be casual","stand3"],["Strike a pose","stand4"],["Move your hands out of the way","stand5"],["Hands down, ass up.","standing_doggy"]]
    $ pose_dances = {} #Dict that maps poses to animations that look good for them.


    $ picked_pose = the_person.idle_pose #She starts in her idle pose (which is a string)
    $ rand_strip_desc = renpy.random.randint(0,3) #Produce 4 different descriptions at each level to help keep this interesting.

    # strip_willingness is a measure of how into the whole strip process the girl is. The less dressed she get the more embarrassed she'll get,
    # the more slutty the more she'll tease you, take clothing off willingly, etc.
    $ strip_willingness = the_person.effective_sluttiness("underwear_nudity") + (5*the_person.get_opinion_score("not wearing anything")) - the_person.outfit.slut_requirement
    #If there are other things that influence how willing a person is to strip they go here!

    $ keep_stripping = True #When set to false the loop ends and the strip show stops.

    while keep_stripping:
        $ the_person.draw_person(position = picked_pose)
        if strip_willingness < 0:
            if rand_strip_desc == 0:
                "[the_person.title] blushes intensely while you watch her."
            elif rand_strip_desc == 1:
                if the_person.has_large_tits():
                    "[the_person.title] instinctively tries to cover herself with her hands, but her large tits make it a difficult task."
                else:
                    "[the_person.title] instinctively tries to cover herself with her hands."
            elif rand_strip_desc == 2:
                the_person "Oh my god..."
                "[the_person.title] covers her eyes for a moment and looks away."
            else:
                "[the_person.title] shakes her head and mutters to herself."
                the_person "I can't believe I'm doing this..."

        elif strip_willingness < 10:
            if rand_strip_desc == 0:
                "[the_person.title] stands awkwardly in front of you and avoids making eye contact."
            elif rand_strip_desc == 1:
                if the_person.has_large_tits():
                    "[the_person.title] shifts her weight from side to side while you watch her. The small movements still make her big tits jiggle around."
                else:
                    "[the_person.title] shifts her weight from side to side while you watch her."
            elif rand_strip_desc == 2:
                "You get a good look at [the_person.title] while she stands in front of you."
            else:
                "[the_person.title] blushes and looks around the room to avoid making eye contact."

        elif strip_willingness < 30:
            $tease_clothing = the_person.outfit.remove_random_any(top_layer_first = True, exclude_feet = True, do_not_remove = True) #She's slutty enough that she wants to tease you a little more
            if rand_strip_desc == 0:
                if tease_clothing is not None:
                    "[the_person.title] pulls at her [tease_clothing.name] seductively."
                    the_person "Mmm, I bet you want me to take this off, right?"
                else:
                    "[the_person.title] runs her hands down her body seductively."
                    the_person "Mmm, I bet you want to get your hands on me now, right?"

            elif rand_strip_desc == 1:
                if the_person.has_large_tits():
                    "[the_person.title] moves her body side to side for you, letting her large tits bounce and jiggle while you watch."
                else:
                    "[the_person.title] moves her body side to side for you while you watch."

            elif rand_strip_desc == 2:
                if tease_clothing is not None:
                    "[the_person.title] slips a hand under her [tease_clothing.name] and starts to pull it off."
                    the_person "Maybe I should just... slip this off. What do you think?"
                else:
                    if the_person.has_large_tits():
                        "[the_person.title]'s hands slide up and down her body. She cups one of her sizeable breast and squeezes it, pinching her own nipple while she does."
                    else:
                        "[the_person.title]'s hands slide up and down her body. She rubs her small breasts, paying special attention to their firm nipples."
            else:
                the_person "I hope you're enjoying the show [the_person.mc_title]."
                "She wiggles her hips for you and winks."

        else: #strip_willingness >= 30
            $tease_clothing = the_person.outfit.remove_random_any(top_layer_first = True, exclude_feet = True, do_not_remove = True) #She's slutty enough that she wants to tease you a little more
            if rand_strip_desc == 0:
                if tease_clothing is not None:
                    "[the_person.title] pulls at her [tease_clothing.name]."
                    the_person "I'm going to have to get this out of the way before we can have any fun."
                else:
                    "[the_person.title] runs her hands over her own body."
                    the_person "Oh [the_person.mc_title], I think I'm going to need more than your eyes on me soon..."

            elif rand_strip_desc == 1:
                "[the_person.title] puts her hands up in the air and spins around. You get a great look at her body as she enjoys herself."

            elif rand_strip_desc == 2:
                if tease_clothing is not None:
                    the_person "Don't you just think all of this clothing is just useless? How about I take it all off for you... would you like that?"
                else:
                    "[the_person.title] takes a wider stances and slides her hands down her own thighs, all while maintaining eye contact with you."
                    the_person "You're looking so good today [the_person.mc_title], did you know that?"

            else:
                "[the_person.title] wiggles her hips side to side and bites her bottom lip, as if imagining some greater pleasure yet to come."

        $pay_strip_list = ["Strip"] #Tuple of menu things.
        # High obedience characters are more willing to be told to strip down (althoug they still expect to be paid for it)
        # Low obedience characters will strip off less when told but can be left to run the show on their own and will remove some.
        python:
            for item in the_person.outfit.get_unanchored():
                if not item.is_extension:
                    test_outfit = the_person.outfit.get_copy()
                    test_outfit.remove_clothing(item)
                    new_willingness = the_person.effective_sluttiness("underwear_nudity") + (5*the_person.get_opinion_score("not wearing anything")) - test_outfit.slut_requirement

                    taboo_break = False
                    if test_outfit.vagina_visible() and the_person.has_taboo("bare_pussy"):
                        taboo_break = "bare_pussy"
                    elif test_outfit.tits_visible() and the_person.has_taboo("bare_tits"):
                        taboo_break = "bare_tits"
                    elif test_outfit.underwear_visible() and the_person.has_taboo("underwear_nudity"):
                        taboo_break = "underwear_nudity"

                    if new_willingness + (the_person.obedience-100) >= -20:
                        #They're willing to strip it off.
                        price = 0 # Default value
                        price_display = "Free"
                        if taboo_break == "bare_pussy" or taboo_break == "bare_tits":
                            price = (strip_willingness - new_willingness) * 10

                        elif taboo_break == "underwear_nudity":
                            price = (strip_willingness - new_willingness) * 5

                        elif new_willingness >= 40:
                            price = 0 #They'll do it for free!

                        elif new_willingness >= 20:
                            price = (strip_willingness - new_willingness) * 1 #They feel pretty good about how they'll be dressed after, so the price is decent.

                        else:
                            price = (strip_willingness - new_willingness) * 3 #THey will feel pretty uncomfortable, so they expect to be paid well.

                        if price < 0:
                            price = 0

                        price = math.ceil((price/5.0))*5 #Round up to the next $5 increment
                        if price > 0:
                            price_display = "$" + str(price)

                        display_string = item.display_name
                        if taboo_break:
                            display_string = "{image=gui/extra_images/taboo_break_token.png} " + display_string + " {image=gui/extra_images/taboo_break_token.png}"

                        display_string += "\n{size=22}" + price_display + "{/size}"
                        if price > mc.business.funds:
                            display_string += " (disabled)"

                        pay_strip_list.append([display_string, [item,price]])

                    else:
                        display_string = item.display_name
                        if taboo_break:
                            display_string = "{image=gui/extra_images/taboo_break_token.png} " + display_string + " {image=gui/extra_images/taboo_break_token.png}"
                        pay_strip_list.append([display_string + "\n{size=22}Too Slutty{/size} (disabled)", [item,-1]])

            other_options_list = ["Other Options"]
            other_options_list.append(["Just watch.","Watch"])
            other_options_list.append(["Tell her to pose.","Pose"])
            #TODO: This is where the "jerk off" option should be.
            #TODO: If Jerking off there should be some way to transition into having sex.
            other_options_list.append(["Finish the show.","Finish"])
        call screen main_choice_display([pay_strip_list, other_options_list])
        $ strip_choice = _return
        if strip_choice == "Watch":
            if renpy.random.randint(0,1) == 0:
                $ tease_item = the_person.outfit.remove_random_any(top_layer_first = True, exclude_feet = True, do_not_remove = True) #The clothing item she's considering taking off
                $ free_spirit_threshold = 40 + (100 - the_person.obedience)
                if renpy.random.randint(0,100) < free_spirit_threshold: #She's independant enough to strip, change pose, etc. on her own.
                    if tease_item is not None and new_willingness >= (the_person.obedience-100): #A more obedient person is less willing to strip without being told to. A less obedient person will strip further on their own.
                        $ test_outfit = the_person.outfit.get_copy()
                        $ test_outfit.remove_clothing(tease_item)
                        $ new_willingness = the_person.sluttiness + (5*the_person.get_opinion_score("not wearing anything")) - test_outfit.slut_requirement
                        $ price = 0
                        $ taboo_break = False

                        if test_outfit.vagina_visible() and the_person.has_taboo("bare_pussy"):
                            $ price = (strip_willingness - new_willingness) * 10
                            $ taboo_break = "bare_pussy"
                        elif test_outfit.tits_visible() and the_person.has_taboo("bare_tits"):
                            $ price = (strip_willingness - new_willingness) * 10
                            $ taboo_break = "bare_tits"
                        elif test_outfit.underwear_visible() and the_person.has_taboo("underwear_nudity"):
                            $ price = (strip_willingness - new_willingness) * 5
                            $ taboo_break = "underwear_nudity"
                        elif new_willingness >= 30: #She's slutty enough to do it for free!
                            $ price = 0
                        elif new_willingness >= 10:
                            $ price = (strip_willingness - new_willingness) * 1
                        else:
                            $ price = (strip_willingness - new_willingness) * 3

                        $ price = math.ceil((price/5.0))*5 #Round up to the next $5 increment
                        if price > 0:
                            "[the_person.title] steps a little closer to you and plays with the edge of her [tease_item.display_name]."
                            if taboo_break: #TODO: If this style of stripping becomes more important this dialogue should be personality based (mainly for family related dialogue)
                                if taboo_break == "bare_pussy":
                                    the_person "Would you like a look at my pussy? How about... $[price] and I'll take off my [tease_item.display_name]."
                                elif taboo_break == "bare_tits":
                                    the_person "So, would you like to see my tits? Just, oh... $[price] and I'll take off my [tease_item.display_name]."
                                else: #Underwear_nudity
                                    the_person "Want to see what I'm wearing underneath this [tease_item.display_name]? Just $[price] and I'll show you."
                            else:
                                the_person "$[price] and I'll take this off for you..."

                            menu:
                                "Pay her $[price]." if price <= mc.business.funds:
                                    "You pull the cash out of your wallet and hand it over."
                                    $ mc.business.funds += -price
                                    $ the_person.change_obedience(-1)
                                    $ the_person.change_slut_temp(1)
                                    $ the_person.draw_animated_removal(tease_item, position = picked_pose)
                                    "[the_person.title] takes it, puts it to the side, and starts to slide her [tease_item.name] off."
                                    if the_person.update_outfit_taboos():
                                        "She seems momentarily uneasy about undressing, but shakes the feeling quickly and returns her attention to you."

                                "Pay her $[price]. (disabled)" if price > mc.business.funds:
                                    pass

                                "Don't pay her.":
                                    mc.name "I think you look good with it on."
                                    "[the_person.title] seems disappointed but shrugs and keeps going."

                        else:
                            $ the_person.draw_animated_removal(tease_item, position = picked_pose)
                            "You watch as [the_person.title] grabs their [tease_item.name] and pulls it off."
                    else:
                        #She has nothing to strip off or she's as slutty as she's willing to get
                        "[the_person.title] seems comfortable just the way she is."

                else: #She doesn't quite know what to do without you telling her.
                    "Without any direction [the_person.title] just keeps doing what she was doing."

            else:
                #She decides to change pose half the time.
                $ new_pose = get_random_from_list(pose_list)
                if not new_pose[1] == picked_pose:
                    $ picked_pose = new_pose[1]
                    "While you're watching [the_person.title] changes pose so you can see her from a different angle."
                else:
                    "[the_person.title] seems comfortable just the way she is."


        elif strip_choice == "Pose":
            #You ask her to change into a different pose
            mc.name "I want to see you from a different angle."
            $pose_menu_tuple = []
            python:
                for pose_tuple in pose_list:
                    if not pose_tuple[1] == picked_pose:
                        pose_menu_tuple.append(pose_tuple)
                pose_menu_tuple.append(["Nevermind.",None])

            $ pose_choice = renpy.display_menu(pose_menu_tuple,True,"Choice")
            if pose_choice is not None:
                $ picked_pose = pose_choice
                "[the_person.title] nods and moves for you."

            else:
                mc.name "Nevermind, you look perfect like this."

        elif strip_choice == "Finish":
            $ keep_stripping = False
            mc.name "That was fun [the_person.title], I think that's enough."
            if strip_willingness < 0:
                "[the_person.title] sighs happily."
                the_person "Oh my god, I thought I was going to die of embarrassment!"
            elif strip_willingness < 20:
                the_person "Oh, okay. That... wasn't as bad as I thought it was going to be, at least."
            else:
                the_person "Oh, is that all you wanted to see? I feel like we were just getting started!"

        else: #The only other result is an actual strip. Pay the cash, remove the piece and loop or end.
            $ mc.business.funds += -strip_choice[1]
            $ test_outfit = the_person.outfit.get_copy() #We use a temp copy so that we can get her reaction first.
            $ test_outfit.remove_clothing(strip_choice[0])
            $ the_clothing = strip_choice[0]

            $ taboo_break = False
            if test_outfit.vagina_visible() and the_person.has_taboo("bare_pussy"):
                $ taboo_break = "bare_pussy"
            elif test_outfit.tits_visible() and the_person.has_taboo("bare_tits"):
                $ taboo_break = "bare_tits"
            elif test_outfit.underwear_visible() and the_person.has_taboo("underwear_nudity"):
                $ taboo_break = "underwear_nudity"

            $ strip_willingness = the_person.effective_sluttiness("underwear_nudity") + (5*the_person.get_opinion_score("not wearing anything")) - test_outfit.slut_requirement
            mc.name "Take off your [the_clothing.display_name] for me."
            if taboo_break: #Always use special dialogue for the taboo breaks
                $ the_person.call_dialogue(taboo_break + "_taboo_break", the_clothing = the_clothing)
                $ the_person.break_taboo(taboo_break)

            if strip_choice[1] > 0:
                if strip_willingness < 0:
                    "You pull some cash from your wallet and offer it to [the_person.title]. She takes it and looks at it for a long second."
                    the_person "Oh my god... I shouldn't be doing this..."
                    $ the_person.change_obedience(2)
                    $ the_person.change_slut_temp(1)
                    $ the_person.draw_animated_removal(strip_choice[0], position = picked_pose)
                    "Nevertheless, she keeps the money and pulls off her [the_clothing.display_name]."
                elif strip_willingness < 20:
                    "You pull some cash out from your wallet and hand it over to [the_person.title]. She puts it to the side and grabs her [the_clothing.display_name]."
                    the_person "Ready?"
                    $ the_person.change_obedience(1)
                    $ the_person.change_slut_temp(1)
                    $ the_person.draw_animated_removal(strip_choice[0], position = picked_pose)
                    "You nod and [the_person.title] pulls off the piece of clothing, throwing it to the side."
                else:
                    "You're still pulling out cash as [the_person.title] strips off her [the_clothing.display_name] and chucks it to the side."
                    $ the_person.draw_animated_removal(strip_choice[0], position = picked_pose)
                    the_person "Thank you!"
                    "She plucks the cash from your hand and quickly puts it away."

            else: #She'll only do it for free if she's becoming less slutty (ie taking off lingerie, bondage gear, etc.) or if she's very slutty anyways.
                the_person "Is that all? Well, I think that's easy."
                $ the_person.draw_animated_removal(strip_choice[0], position = picked_pose)
                "[the_person.title] strips off her [the_clothing.display_name] for free, leaving it on the ground at her feet."
    return


label prostitute_label(the_person):
    mc.name "[the_person.title], I'm looking for a friend to spend some time with. Are you available?"
    the_person "If you're paying I am."
    $ mc.business.funds += -200
    $ the_person.change_obedience(1)

    $ the_person.add_situational_obedience("prostitute", 40, "I'm being paid for this, I should do whatever he wants me to do.")
    call fuck_person(the_person, private = True, ignore_taboo = True) from _call_fuck_person_23 #She's a prostitute, she doesn't care about normal taboos
    $ the_report = _return

    $ the_person.clear_situational_obedience("prostitute")
    if the_report.get("girl orgasms", 0) > 0:
        "It takes [the_person.title] a few moments to catch her breath."
        the_person "Maybe I should be paying you... Whew!"
    $ the_person.review_outfit()

    the_person "That was fun, I hope you had a good time [the_person.mc_title]."
    "She gives you a quick peck on the cheek."
    $ clear_scene()
    return
