# This file holds information about all of the special roles in the game. Charcters with special roles have extra dialogue options shown when you talk to them, and may be critical for special events.

init -2 python: #This section holds all of the requirements added for the roles that are introduced below.
    #EMPLOYEE ACTION REQUIREMENTS#
    def employee_complement_requirement(the_person):
        if not mc.business.is_open_for_business():
            return False
        elif day - the_person.event_triggers_dict.get("day_last_employee_interaction",-2) <= 0:
            return "Already talked about work today."
        else:
            return True

    def employee_insult_requirement(the_person):
        if not mc.business.is_open_for_business():
            return False
        elif day - the_person.event_triggers_dict.get("day_last_employee_interaction",-2) <= 0:
            return "Already talked about work today."
        else:
            return True

    def employee_pay_cash_requirement(the_person):
        if not mc.business.is_open_for_business():
            return False
        elif day - the_person.event_triggers_dict.get("day_last_employee_interaction",-2) <= 0:
            return "Already talked about work today."
        else:
            return True

    def employee_performance_review_requirement(the_person):
        if not mc.business.is_open_for_business():
            return False
        elif day - the_person.event_triggers_dict.get("day_last_performance_review", the_person.event_triggers_dict.get("employed_since",-7)) < 7:
            return "Had a recent performance review."
        else:
            return True

    def move_employee_requirement(the_person):
        return True

    #HEAD RESEARCHER ACTION REQUIREMENTS#
    def improved_serum_unlock_requirement(the_person): #If the person is with their R&D head in the research division during work hours and they meet the sluttiness requirements you can
        if mc.location != mc.business.r_div:
            return False
        elif not mc.business.is_open_for_business():
            return False
        elif mc.business.research_tier != 0:
            return False
        elif the_person.obedience < 110 or the_person.int < 3:
            return "Requires: 110 Obedience, 3 Intelligence"
        else:
            return True

    def advanced_serum_stage_1_requirement(the_person):
        if mc.business.event_triggers_dict.get("advanced_serum_stage_1",False):
            return False
        elif mc.location != mc.business.r_div:
            return False
        elif not mc.business.is_open_for_business():
            return False
        elif mc.business.research_tier != 1:
            return False
        elif the_person.obedience < 120 or the_person.core_sluttiness < 25 or the_person.int < 4:
            return "Requires: 120 Obedience, 4 Intelligence, " + get_gold_heart(25)
        else:
            return True

    def advanced_serum_stage_2_requirement(the_person,earliest_trigger_day):
        if mc.business.is_open_for_business():
            if day >= earliest_trigger_day:
                return True
        return False

    def advanced_serum_stage_3_requirement(the_person):
        if not mc.business.event_triggers_dict.get("advanced_serum_stage_3",False):
            return False
        elif mc.location != mc.business.r_div:
            return False
        elif not mc.business.is_open_for_business():
            return False
        elif mc.business.research_tier != 1:
            return False
        elif the_person.obedience < 120 or the_person.int < 4:
            return "Requires: 120 Obedience, 4 Intelligence"
        else:
            return True

    def futuristic_serum_stage_1_requirement(the_person):
        if mc.business.event_triggers_dict.get("futuristic_serum_stage_1",False):
            return False
        elif mc.location != mc.business.r_div:
            return False
        elif not mc.business.is_open_for_business():
            return False
        elif mc.business.research_tier != 2:
            return False
        elif the_person.obedience < 140 or the_person.core_sluttiness < 50 or the_person.int < 5:
            return "Requires: 140 obedience, 5 Intelligence, " + get_gold_heart(50)
        else:
            return True

    def futuristic_serum_stage_2_requirement(the_person):
        if not mc.business.event_triggers_dict.get("futuristic_serum_stage_1",False):
            return False
        elif mc.location != mc.business.r_div:
            return False
        elif not mc.business.is_open_for_business():
            return False
        elif mc.business.research_tier != 2:
            return False
        elif the_person.obedience < 140 or the_person.core_sluttiness < 50 or the_person.int < 5:
            return "Requires: 140 obedience, 5 Intelligence, " + get_gold_heart(50)
        else:
            return True

    def fire_head_researcher_requirement(the_person): #Remove the person as your head researcher.
        return True


    #SISTER ACTION REQUIREMENTS#
    def sister_intro_crisis_requirements(the_person, day_trigger):
        if time_of_day == 4 and mc.location == bedroom and day >= day_trigger: #We use time == 4 because we want it to trigger during our night/day transition (ie. when you're guaranteed to be at home)
            return True
        return False

    def sister_reintro_action_requirement(the_person):
        if mc.business.event_triggers_dict.get("sister_needs_reintro"):
            return True
        return False

    def sister_serum_test_requirement(the_person):
        if not mc.business.event_triggers_dict.get("sister_serum_test", False):
            return False
        elif mc.business.funds < 50:
            return "Requires: $50"
        else:
            return True

    def sister_strip_intro_requirement(the_person): #Note that this only ever triggers once, so we don't need to worry if it will retrigger at any point.
        if time_of_day == 4 and mc.location == bedroom:
            if the_person.sluttiness > 20 and mc.business.event_triggers_dict.get("sister_serum_test_count") and mc.business.event_triggers_dict.get("sister_serum_test_count") >= 4:
                return True
        return False

    def sister_strip_reintro_requirement(the_person):
        if not mc.business.event_triggers_dict.get("sister_strip_reintro",False):
            return False
        elif mc.location != lily_bedroom:
            return False
        elif len(lily_bedroom.people) > 1:
            return False
        elif the_person.sluttiness < 20:
            return "Requires: " + get_red_heart(20)
        else:
            return True

    def sister_strip_requirement(the_person): #She'll only strip if you're in her bedroom and alone.
        if not mc.business.event_triggers_dict.get("sister_strip",False):
            return False
        elif mc.location != lily_bedroom:
            return False
        elif len(lily_bedroom.people) > 1:
            return False
        elif the_person.sluttiness < 20 or mc.business.funds < 100:
            return "Requires: $100, " + get_red_heart(20)
        else:
            return True

    #MOM ACTION REQUIREMENTS
    def mom_weekly_pay_requirement(the_person):
        if time_of_day == 4 and day%7 == 4: #It is the end of the day on friday
            return True
        return False

    def mom_offer_make_dinner_requirement(the_person):
        if time_of_day == 3:
            return True
        return False


label instantiate_roles(): #This section instantiates all of the key roles in the game. It is placed here to ensure it is properly created, saved, ect. by Renpy.
    python:
        #EMPLOYEE ACTIONS#
        move_employee_action = Action("Move her to a new division", move_employee_requirement, "move_employee_label",
            menu_tooltip = "Move her to a new division, where her skills might be put to better use.")
        employee_complement_action = Action("Compliment her work.", employee_complement_requirement, "employee_complement_work",
            menu_tooltip = "Offer a few kind words about her performance at work. Increases appiness and love, dependent on your charisma.")
        employee_insult_action = Action("Insult her work.", employee_insult_requirement, "insult_recent_work",
            menu_tooltip = "Offer a few choice words about her performance at work. Lowers love and happiness, but is good for instilling obedience.")
        employee_pay_cash_action = Action("Pay her a cash bonus.", employee_pay_cash_requirement, "employee_pay_cash_bonus",
            menu_tooltip = "A bonus in cold hard cash is good for obedience and happiness. The larger the reward the greater the effect.")
        employee_performance_review = Action("Start a performance review.", employee_performance_review_requirement , "employee_performance_review",
            menu_tooltip = "Bring her to your office for a performance review. Get her opinion about her job, reward, punish, or fire her as you see fit. Can only be performed once every seven days.")

        employee_role = Role("Employee", [employee_complement_action, employee_insult_action, employee_pay_cash_action, employee_performance_review, move_employee_action])

        #HEAD RESEARCHER ACTIONS#
        improved_serum_unlock = Action("Ask about advancing your research.", improved_serum_unlock_requirement, "improved_serum_unlock_label",
            menu_tooltip = "Your basic initial research can only take you so far. You will need a breakthrough to discover new serum traits.")

        advanced_serum_unlock_stage_1 = Action("Ask about advancing your research.", advanced_serum_stage_1_requirement, "advanced_serum_stage_1_label",
            menu_tooltip = "Another breakthrough will unlock new serum traits.")

        advanced_serum_unlock_stage_3 = Action("Present with recording of prototype serum test.", advanced_serum_stage_3_requirement, "advanced_serum_stage_3_label",
            menu_tooltip = "Your new head researcher will have to take over now, and this recording should help them.")

        futuristic_serum_unlock_stage_1 = Action("Ask about advancing your research.", futuristic_serum_stage_1_requirement, "futuristic_serum_stage_1_label",
            menu_tooltip = "You will need another breakthrough to unlock new serum traits.") #First time you ask about it

        futuristic_serum_unlock_stage_2 = Action("Talk about the test subjects.", futuristic_serum_stage_2_requirement, "futuristic_serum_stage_2_label",
            menu_tooltip = "Your head researcher needs willing, dedicated test subjects to advance your research any further.") #Talk to her to either select test subjects or get a refresher on what you need.


        fire_head_researcher_action = Action("Remove her as head reseracher.", fire_head_researcher_requirement, "fire_head_researcher",
            menu_tooltip = "Remove her as your head researcher so you can select another. Without a head researcher your R&D department will be less efficent.")

        head_researcher = Role("Head Researcher", [fire_head_researcher_action,improved_serum_unlock,advanced_serum_unlock_stage_1,advanced_serum_unlock_stage_3,futuristic_serum_unlock_stage_1, futuristic_serum_unlock_stage_2])



        #SISTER ACTIONS#
        sister_reintro_action = Action("Ask if she needs extra work.", sister_reintro_action_requirement, "sister_reintro_label",
            menu_tooltip = "She was eager to make some money before, maybe she still is.")

        sister_serum_test_action = Action("Ask her to test serum.", sister_serum_test_requirement, "sister_serum_test_label",
            menu_tooltip = "Have your sister test serum for you. Over time she will become more comfortable following your orders and making deals with you.")


        sister_strip_reintro_action = Action("Ask if she would strip for pay.", sister_strip_reintro_requirement, "sister_strip_reintro_label",
            menu_tooltip = "She was eager to make some money, maybe she will be willing to strip for you if you pay her.")

        sister_strip_action = Action("Ask her to strip for you.", sister_strip_requirement, "sister_strip_label",
            menu_tooltip = "Have your sister strip for you, in exchange for some money.")

        sister_role = Role("Sister", [sister_reintro_action, sister_serum_test_action, sister_strip_reintro_action, sister_strip_action])


        #MOTHER ACTIONS#
        mother_offer_make_dinner = Action("Offer to make dinner. {image=gui/heart/Time_Advance.png}", mom_offer_make_dinner_requirement, "mom_offer_make_dinner_label",
            menu_tooltip = "Earn some good will by making dinner for your mother and sister.")

        mother_role = Role("Mother", [mother_offer_make_dinner])
    return

#### EMPLOYEE EVENTS ####
label employee_complement_work(the_person):
    $ the_person.event_triggers_dict["day_last_employee_interaction"] = day
    if mc.business.get_employee_count == 1:
        mc.name "[the_person.title], I wanted to tell you that you've been doing a great job lately. Me and you make a great team, and I couldn't do all of this without you."
    else:
        mc.name "[the_person.title], I wanted to tell you that you've been doing a great job lately. Keep it up, you're one of the most important players in this whole operation."

    $ the_person.change_love(1)
    $ the_person.change_happiness(mc.charisma)
    the_person.char "Thanks [the_person.mc_title], it means a lot to hear that from you!"
    return

label insult_recent_work(the_person):
    $ the_person.event_triggers_dict["day_last_employee_interaction"] = day
    if mc.business.get_employee_count == 1:
        mc.name "I'm not sure what's going on with you lately, but I'm going to need you to try a little harder. It's only me and you here and you're really letting me down."
    else:
        mc.name "Honestly [the_person.title], I've been disappointed with your work lately and I really need you to try a little harder. You're letting the whole team down."
    $ the_person.change_obedience(mc.charisma)
    $ the_person.change_happiness(-5)
    $ the_person.change_love(-2)
    return

label employee_pay_cash_bonus(the_person):
    $ the_person.event_triggers_dict["day_last_employee_interaction"] = day
    mc.name "[the_person.title], I noticed you've been putting in a lot of good work at the lab lately. I wanted to give you a little extra to make sure you know you're appreciated."
    "You pull out your wallet and start to pull out a few bills."
    $weeks_wages = the_person.salary*5
    $months_wages = the_person.salary*20
    $raise_amount = int(the_person.salary*0.1)
    menu:
        "Give her a pat on the back.":
            mc.name "And I'll absolutely do that once the next batch of sales go through."
            $ the_person.draw_person(emotion = "sad")
            $ change_amount = 5-mc.charisma
            if change_amount < 0:
                $ change_amount = 0
            $ the_person.change_happiness(change_amount)
            "[the_person.title] looks visibly disapointed."
            the_person.char "Right, of course."

        "Give her a days wages. -$[the_person.salary]" if mc.business.funds >= the_person.salary:
            mc.name "Here you go, treat yourself to something nice tonight."
            $ the_person.draw_person(emotion = "happy")
            $ change_amount = 1+mc.charisma
            $ mc.business.funds -= the_person.salary
            $ the_person.change_happiness(change_amount)
            "[the_person.title] takes the bills from you and smiles."
            the_person.char "Thank you sir."


        "Give her a weeks wages. -$[weeks_wages]" if mc.business.funds >= weeks_wages:
            mc.name "Here you go, don't spend it all in once place."
            $ the_person.draw_person(emotion = "happy")
            $ change_amount = 1+mc.charisma
            $ change_amount_happiness = 5+mc.charisma
            $ the_person.change_happiness(change_amount_happiness)
            $ the_person.change_obedience(change_amount)
            $ mc.business.funds -= weeks_wages
            "[the_person.title] takes the bills, then smiles broadly at you."
            the_person.char "That's very generous of you sir, thank you."

        "Give her a months wages. -$[months_wages]" if mc.business.funds >= months_wages:
            mc.name "Here, you're a key part of the team and you deserved to be rewarded as such."
            $ the_person.draw_person(emotion = "happy")
            $ change_amount = 5+mc.charisma
            $ change_amount_happiness = 10+mc.charisma
            $ the_person.change_happiness(change_amount_happiness)
            $ the_person.change_obedience(change_amount)
            $ mc.business.funds -= months_wages
            "[the_person.title] takes the bills, momentarily stunned by the amount."
            if the_person.sluttiness > 40 and the_person.happiness > 100 and mc.current_stamina > 0:
                the_person.char "Wow... this is amazing sir. I'm sure there's something I can do to pay you back, right?"
                "She steps close to you and runs a finger down your chest."
                $ mc.current_stamina += -1
                call fuck_person(the_person) from _call_fuck_person_3  #TODO: add a temporary obedience and sluttiness modifier to the function to allow for modifiers during situations like this (and firing her)
                #Now that you've had sex, we calculate the change to her stats and move on.
                $ the_person.reset_arousal()
                $ the_person.review_outfit()
            else:
                the_person.char "Wow... this is amazing [the_person.mc_title]. I'll do everything I can for you and the company!"

    return

label employee_performance_review(the_person):
    $ the_person.event_triggers_dict["day_last_performance_review"] = day
    #Bring them into the office. (Set the background appropriately)
    mc.name "[the_person.title], I'd like to have a talk with you about your recent performance here at [mc.business.name]. Can you step inside my office for a moment?"
    if the_person.obedience > 100:
        the_person.char "Oh, of course [the_person.mc_title]."
    else:
        the_person.char "Uh, I guess. so."

    $ renpy.show(office.name,what=office.background_image)
    $ mc.location.move_person(the_person, office)

    "You lead [the_person.title] into your office and close the door behing her. You take your seat at your desk and motion to a chair opposite you."
    $ the_person.draw_person(position = "sitting")
    mc.name "So [the_person.title], tell me what you think about your job."

    if the_person.get_job_happiness_score() > 0:
        #She's happy enough with the job to stay here
        if the_person.salary > the_person.calculate_base_salary() + 15: #She's very overpaid
            the_person.char "It's a fantastic position and I'm lucky to have it! There aren't very many places that would be able to pay me as well as I am here."
        elif the_person.salary > the_person.calculate_base_salary() + 3: #She's reasonably over paid.
            the_person.char "It's a great job. The pay is great and the work is interesting."
        elif the_person.salary > the_person.calculate_base_salary() - 3: #She's reasonably paid.
            the_person.char "I really like my job. I feel like I can come in every day and do an honest day's work."
        else:
            the_person.char "The pay isn't the greatest, but the work environment really makes up for it. It's a joy to be working here."

    else: #She's thinking about quitting.
        if the_person.salary > the_person.calculate_base_salary() + 15: #She's very overpaid
            the_person.char "The pay is amazing, but the work environment here is just terrible. I honestly don't know how much longer I can take it."
        elif the_person.salary > the_person.calculate_base_salary() + 3: #She's reasonably over paid.
            the_person.char "I know you're paying me very well, but the work here is terrible. I hope you have some plans to make things better."
        elif the_person.salary > the_person.calculate_base_salary() - 3: #She's reasonably paid.
            the_person.char "Things could be better. I'd like it if the conditions here at work were improved a little bit, or I could be paid a little bit more."
        else:
            the_person.char "I don't really have anything positive to say. The pay isn't great and it isn't exactly the most pleasant work environment."

    "You nod and take some notes while you think of how you want to respond."
    #TODO: Here is where characters, especially those with moderate sluttiness and who are over paid, might try and win your favour. Is this the right place for it?
    menu:
        "Reward her for work well done.":
            $ raise_amount = __builtin__.round(the_person.salary * 0.1)
            menu:
                "Offer her kind words.": #Raise happiness and obedience a little.
                    call employee_complement_work(the_person) from _call_employee_complement_work

                "Give her a raise. (+$[raise_amount]/day)": #Pay her more money. Large happiness and obedience raise.
                    mc.name "I've been very impressed by your work lately, and I'd like to make sure you stay happy with your decision to work here."
                    mc.name "I'm going to put you down for a 10%% raise. How does that sound?"
                    $ the_person.change_salary(raise_amount)
                    $ the_person.change_happiness(10+mc.charisma)
                    $ the_person.change_obedience(3+mc.charisma)
                    $ the_person.draw_person(position = "sitting", emotion = "happy")
                    the_person.char "That sounds amazing! Thank you sir, I promise I won't let you down!"
                    mc.name "Good to hear it."

                "Reward her sexually." if the_person.sluttiness >= 40: #At high sluttiness you can make her cum to make her even happier with her job.
                    mc.name "You do a lot of work for the company, and I know how stressful your job can be at times."
                    "You get up from your desk and move around to the other side. You step behind [the_person.title] and place your hands on her shoulders, rubbing them gently."
                    mc.name "I'd like to do something for you to help you relax. How does that sound for a bonus?"
                    $ the_person.add_situational_slut("seduction_approach", 15, "It's all about me!")
                    $ the_person.add_situational_obedience("seduction_approach", -20, "It's all about me!")
                    the_person.char "Oh [the_person.mc_title], that sounds like a great idea..."
                    call fuck_person(the_person,private = True) from _call_fuck_person_11
                    $ the_person.clear_situational_slut("seduction_approach")
                    $ the_person.clear_situational_obedience("seduction_approach")
                    if the_person.arousal >= 100: #We made her cum! Congradulations!
                        $ the_person.change_happiness(20)
                        $ the_person.change_slut_temp(5)
                        $ the_person.change_love(2)
                        the_person.char "Oh [the_person.mc_title], that was wonderful! I couldn't have asked for a better performance bonus!"
                    elif the_person.arousal >= 80:
                        $ the_person.change_happiness(5)
                        $ the_person.change_slut_temp(2)
                        the_person.char "Well, that was a good time [the_person.mc_title]. It's a lot more fun than a normal performance bonus, that's for sure!"
                    else:
                        $ the_person.change_happiness(-5)
                        $ the_person.change_obedience(-2)
                        the_person.char "It's not much of a bonus if you're the only one who gets to cum. Maybe next time a cash bonus would be better, okay?"
                    $ the_person.reset_arousal()
                    $ the_person.review_outfit()

        "Punish her for poor performance.":
            $ cut_amount = __builtin__.round(the_person.salary * 0.1)
            menu:
                "Chastise her.": #Lower happiness and love a little, large obedience boost.
                    call insult_recent_work(the_person) from _call_insult_recent_work

                "Cut her pay. (-$[cut_amount]/day)": #Pay her less. Large happiness and obedience drop.
                    mc.name "I'm really sorry to do this [the_person.title], but your performance lately just doesn't justify what I'm paying you."
                    mc.name "I'm going to have to cut your pay by 10%%."
                    $ the_person.change_salary(-cut_amount)
                    $ the_person.change_happiness(-15-mc.charisma)
                    $ the_person.change_obedience(-8-mc.charisma)
                    if the_person.get_job_happiness_score() > 0:
                        $ the_person.draw_person(position = "sitting", emotion = "sad")
                        the_person.char "I... I understand."
                    elif the_person.get_job_happiness_score() > -25:
                        $ the_person.draw_person(position = "sitting", emotion = "angry")
                        the_person.char "What? I... I don't know what to say!"
                        mc.name "Like I said, I'm sorry but it has to be done."
                    else: #She's so unhappy with her job she quits.
                        $ the_person.draw_person(position = "sitting", emotion = "angry")
                        the_person.char "What? I... I can't believe that [the_person.mc_title], why would you ever think I would stay here for less money?"
                        mc.name "Like I said, I'm sorry but it has to be done."
                        the_person.char "Well you know what, I think I'm just going to find somewhere else to work. I quit."
                        $ renpy.scene("Active")
                        "[the_person.title] stands up and storms out."
                        $ mc.business.remove_employee(the_person)
                        call advance_time from _call_advance_time_12
                        return #Don't use the normal "show her out" ending stuff. The scene ends here.

                "Threaten to fire her.": #She may ask to stay in exchange for some sort of favour, or get fired on the spot.
                    mc.name "I'll be honest with you [the_person.title], your performance here at [mc.business.name] leaves a lot to be desired."
                    mc.name "I've been running the numbers and I think we'd be better off without you. Unless you can convince me otherwise I'm going to have to let you go."
                    if the_person.get_job_happiness_score() > -10:
                        if the_person.sluttiness < 20:
                            the_person.char "No sir, I really need this job. What if I took a pay cut? Would that be enough?"
                            menu:
                                "Cut her pay. (-$[cut_amount]/day)":
                                    mc.name "If you're willing to take a pay cut I think I can keep you around and see if your performance improves."
                                    $ the_person.change_salary(-cut_amount)
                                    $ the_person.change_happiness(10)
                                    $ the_person.change_obedience(5)
                                    the_person.char "Thank you sir! Thank you so much!"

                                "Fire her.":
                                    mc.name "I'm sorry, but that wouldn't be enough."
                                    the_person.char "I understand. I'll clear out my desk."
                                    $ the_person.change_happiness(-10)
                                    $ the_person.change_obedience(-5)
                                    $ mc.business.remove_employee(the_person)
                        else:
                            the_person.char "What if... I let you use me. Just so you'll keep me around."
                            menu:
                                "Fuck her." if mc.current_stamina > 0:
                                    $ the_person.add_situational_slut("seduction_approach", -5, "I'm just a toy to him.")
                                    $ the_person.add_situational_obedience("seduction_approach", 25, "I do what I need to keep my job!")
                                    mc.name "Alright, you've got me interested. Let's see what you can do."
                                    call fuck_person(the_person,private = True) from _call_fuck_person_12
                                    $ the_person.clear_situational_slut("seduction_approach")
                                    $ the_person.clear_situational_obedience("seduction_approach")
                                    $ the_person.reset_arousal()
                                    $ the_person.review_outfit()

                                    $ the_person.change_obedience(10)
                                    $ the_person.change_slut_temp(4)
                                    $ the_person.change_happiness(-5)
                                    mc.name "Okay [the_person.title], I'll keep you around for a little while longer, but you're going to need to shape up unless you want this to be a regular occurrence."
                                    if the_person.sluttiness < 50:
                                        the_person.char "I'll do my best sir, I promise."
                                    else:
                                        the_person.char "Would that really be such a bad thing?"

                                "Fuck her later." if mc.current_stamina == 0:
                                    mc.name "I'm already spent for today, but I'll make sure to collect on this later."
                                    "[the_person.title] nods."
                                    $ the_person.change_obedience(10)
                                    $ the_person.change_happiness(-5)
                                    the_person.char "Understood sir. Thank you for giving me a second chance."


                                "Fire her.":
                                    mc.name "I'm sorry, but that wouldn't be enough."
                                    the_person.char "I understand. I'll clear out my desk."
                                    $ the_person.change_happiness(-10)
                                    $ the_person.change_obedience(-5)
                                    $ mc.business.remove_employee(the_person)

                    else:
                        $ the_person.draw_person(position = "sitting", emotion = "angry")
                        the_person.char "What? You want me to beg to stay at this shitty job? If you don't want me here I think it's best I just move on. I quit!"
                        $ renpy.scene("Active")
                        "[the_person.title] stands up and storms out."
                        $ mc.business.remove_employee(the_person)
                        call advance_time from _call_advance_time_13
                        return #Don't use the normal "show her out" ending stuff. The scene ends here.


                "Punish her sexually." if the_person.sluttiness >= 40 and the_person.obedience >= 120: #Orgasm denial and/or make her service you.
                    "You sigh dramatically and stand up from your desk. You walk over to the other side and sit on the corner nearest [the_person.title]."
                    mc.name "Your performance has really let me down, but I think what you need a little motivation."
                    mc.name "I want to have some fun with you, but you're not allowed to climax, is that understood?"
                    $ opinion_modifier = the_person.get_opinion_score("being submissive")*5
                    $ the_person.add_situational_slut("seduction_approach", -5+opinion_modifier, "I'm just being used...")
                    $ the_person.add_situational_obedience("seduction_approach", 15+opinion_modifier, "I'm being punished")
                    the_person.char "I... if you think this is what I need, sir."
                    call fuck_person(the_person,private = True) from _call_fuck_person_13
                    $ the_person.clear_situational_slut("seduction_approach")
                    $ the_person.clear_situational_obedience("seduction_approach")
                    if the_person.arousal >= 100: #We made her cum! Congradulations!
                        $ the_person.change_happiness(5)
                        $ the_person.change_obedience(-10)
                        the_person.char "You just can't resist pleasing me, can you [the_person.mc_title]? I thought I wasn't suppose to cum?"
                        "[the_person.title] seems smug about her orgasmic victory."

                    elif the_person.arousal >= 80:
                        $ the_person.change_happiness(5)
                        $ the_person.change_slut_temp(5)
                        $ the_person.change_obedience(5)
                        the_person.char "Oh my god [the_person.mc_title], you got me so close... Can't you just finish me off, real quick?"
                        mc.name "Do a better job and I'll let you cum next time. Understood?"
                        "[the_person.title] nods meekly."
                    else:
                        $ the_person.change_happiness(-5)
                        $ the_person.change_obedience(10)
                        mc.name "That felt great [the_person.title], I suppose if your performance doesn't improve you'll still be useful as a toy."
                        the_person.char "I... Yes sir, I suppose I would be."
                    $ the_person.reset_arousal()
                    $ the_person.review_outfit()


        "Finish the performance review.":
            mc.name "Well, I think you're doing a perfectly adequate job around here [the_person.title]. If you keep up the good work I don't think we will have any issues."
            $ the_person.change_obedience(1)
            $ the_person.change_happiness(2)
            the_person.char "Thank you, I'll do my best."

    "You stand up and open the door for [the_person.title] at the end of her performance review."
    $ renpy.scene("Active")
    call advance_time from _call_advance_time_14
    return

label move_employee_label(the_person):
    if the_person == mc.business.head_researcher:
        "Moving [the_person.title] will remove her from her role as head researcher. Are you sure you want to move [the_person.title]?"
        menu:
            "Yes, move [the_person.title]":
                pass
            "No, leave [the_person.title]":
                hide screen person_info_ui
                $renpy.scene("Active")
                return

    the_person.char "Where would you like me then?"
    $ mc.business.remove_employee(the_person)
    $ the_person.special_role.append(employee_role) #Remove_employee strips them of their workplace roles. We want to make sure we add it back.
    #TODO: All of the moving employees around should probably be its own function, which would let us set up an employee schedule where they work in different sections if we wanted.

    if rd_division.has_person(the_person):
        $ rd_division.remove_person(the_person)
    elif p_division.has_person(the_person):
        $ p_division.remove_person(the_person)
    elif office.has_person(the_person):
        $ office.remove_person(the_person)
    elif m_division.has_person(the_person):
        $ m_division.remove_person(the_person)

    menu:
        "Research and Development.":
            $ mc.business.add_employee_research(the_person)
            $ mc.business.r_div.add_person(the_person)
            $ the_person.set_work([1,2,3],mc.business.r_div) #TODO: This should reference the business r_div, p_div, etc. not the actual rooms.

        "Production.":
            $ mc.business.add_employee_production(the_person)
            $ mc.business.p_div.add_person(the_person)
            $ the_person.set_work([1,2,3],mc.business.p_div)

        "Supply Procurement.":
            $ mc.business.add_employee_supply(the_person)
            $ mc.business.s_div.add_person(the_person)
            $ the_person.set_work([1,2,3],mc.business.s_div)

        "Marketing.":
            $ mc.business.add_employee_marketing(the_person)
            $ mc.business.m_div.add_person(the_person)
            $ the_person.set_work([1,2,3], mc.business.m_div)

        "Human Resources.":
            $ mc.business.add_employee_hr(the_person)
            $ mc.business.h_div.add_person(the_person)
            $ the_person.set_work([1,2,3],mc.business.h_div)

    the_person.char "I'll move over there right away!"
    return
#####HEAD RESEARCHER EVENTS#####

label fire_head_researcher(the_person):
    mc.name "[the_person.title], I need to talk to you about your role as my head researcher."
    the_person.char "Yes?"
    mc.name "I've decided that the role would be better filled by someone else. I hope you understand."
    if the_person.int > 2:
        $ the_person.change_happiness(-5)
        $ the_person.change_obedience(-1)
        $ the_person.draw_person(emotion="sad")
        the_person.char "I... I'm sorry I couldn't do a better job. Good luck filling the position, sir."
    else:
        $ the_person.draw_person(emotion="happy")
        the_person.char "Whew, I found all that science stuff super confusing to be honest. I hope whoever replaces me can do a better job at it!"
    $ the_person.special_role.remove(head_researcher)
    $ mc.business.head_researcher = None
    return

label improved_serum_unlock_label(the_person):
    $ the_person.call_dialogue("improved_serum_unlock") #In which the player introduces the idea of advancing the lab's research and the head researcher offers to test serum on themselves.
    menu:
        "Assist [the_person.title]":
            mc.name "I think you're right, this is the only way forward. What do you need me to do?"
            "[the_person.title] opens the door to one of the small offices attached to the reserach lab. The two of you step inside and she closes the door."
            the_person.char "First, we're going to need a test dose of serum."
            call give_serum(the_person) from _call_give_serum_6
            if not _return:
                mc.name "I don't have any with me right now. I'll stop by the production division and pick some up."
                the_person.char "Come see me when you do. I'll be waiting."
            else:
                "You pull out the vial of serum and present it to [the_person.title]. She takes the vial and holds it up to the light, then opens it up and drinks the content."
                the_person.char "No going back now. I'm going to need you to take notes for me - about me I suppose."
                "There's a pad of paper and a pen on the desk already. You pick it up, click the pen, and turn to a fresh page."
                mc.name "Let's start with the basics. How did it taste?"
                the_person.char "Hmm, a little sweet, then bitter towards the end."
                mc.name "Was it an overpowering taste?"
                the_person.char "Not particularly, no."
                "You scribble down [the_person.possessive_title]'s name at the top of your notes page then add some bullet points listing her responses."
                mc.name "My old research suggested that these serums could make people more suggestable. Do you feel like you are more suggestable than normal?"
                "[the_person.title] thinks for a moment before responding."
                the_person.char "Maybe? No? God, that's hard question to answer objectively, isn't it?"
                if mc.charisma > 4:
                    "You take a keen look at [the_person.title]. She might not be able to tell but you certainly can. You mark her down as \"Highly Suggestive\"."
                else:
                    "You can't tell any better than [the_person.title]. You put down \"Suggestability Uncertain\" on your notepad."
                mc.name "That's fine, you're doing great."
                mc.name "Next question: Early research has suggested that our serums might deliver performance enhancing effects. What do you think about this?"
                the_person.char "Well, I think I need to know more about it. I suppose that's why I'm doing this - to learn more."
                mc.name "I think we should take advantage of these effects. You agree with me, correct?"
                the_person.char "I... Yes, I agree with you sir."
                "[the_person.title]'s eyes are fixed firmly on yours. This seems like a good chance to impress upon her your goals for the company."
                menu:
                    "Stress the importance of obedience.":
                        mc.name "A highly organised workplace is important, especially in a lab setting. I need employees who are able to listen to my instructions and follow them."
                        "[the_person.possessive_title] nods in agreement."
                        mc.name "As the leader of the research team I need you to be especially loyal. Do you understand?"
                        $ the_person.change_obedience(10)
                        the_person.char "Yes, absolutely. I'll do everything I can to make sure this business is successful."

                    "Stress the importance of appearance.":
                        mc.name "Impressions are key in this line of business, and I need my employees dressed to impress."
                        "[the_person.possessive_title] nods in agreement."
                        mc.name "As the leader of the research team I need you to be especially aware of your appearance. You represent everything our technology can achieve. Do you understand?"
                        $ the_person.change_slut_temp(5)
                        $ the_person.change_slut_core(5)
                        the_person.char "Yes, absolutely. I'll make sure I always leave a positive impression."

                    "Stress the importance of satisfaction.":
                        mc.name "It can be easy to burn yourself out in this line of business. Pay might not always be great and the hours might be long, but a good attitude is key."
                        "[the_person.possessive_title] nods in agreement."
                        mc.name "Your attitude is going to affect the rest of the research team. I need you to be as positive as possible, do you understand?"
                        $ the_person.change_happiness(10)
                        the_person.char "Yes sir, I understand completely. I'll try and be as chipper as possible."

                mc.name "Good to hear it."
                "You ask [the_person.title] a few more questions, recording her observations and noting down a few of your own. Half an hour passes before you're finished."
                the_person.char "Thank you for your help [the_person.mc_title], that was an... interesting experience. It might take some work, but I think I know where we should focus our research efforts."
                $ mc.business.research_tier = 1
                $ mc.log_event("Tier 1 Research Unlocked", "float_text_grey")
                "[the_person.title] takes your notes and returns to the R&D department."
                call advance_time from _call_advance_time_8

        "Do not allow the test.":
            mc.name "I'll think about it, but I would like to avoid self experimentation if possible."
            the_person.char "If you change your mind let me know. Until then I will do my best with what little knowledge we have available."

    return

label advanced_serum_stage_1_label(the_person):
    $ the_person.draw_person()
    mc.name "[the_person.title], the research department has been doing an incredible job lately. I wanted to say thank you."
    $ the_person.draw_person(emotion = "happy")
    the_person.char "Thank you sir, it's been my pleasure. It's my job after all."
    mc.name "On the topic of research: I was wondering if there was anything you needed here to push your discoveries even furthur."
    "[the_person.possessive_title] thinks for a moment."
    the_person.char "We have everything we need for our basic research, but our theoretical work has hit a wall."
    mc.name "Tell me what you need and I'll do what I can."
    the_person.char "Well, I've seen a few papers floating around that make it seem like other groups are working with the same basic techniques as us."
    the_person.char "I'd like to reach out to them and see about securing a prototype of some sort, to see if we can learn anything from its effects."
    the_person.char "These academic types can get very defensive about their research, so I don't think we'll get anything for free."
    menu:
        "Try and secure a prototype serum.\n{size=22}Costs $2000{/size}" if mc.business.funds >= 2000:
            $ mc.business.funds += -2000
            mc.name "That sounds like a good lead. I'll make sure the funds are allocated, let me know when you have something to show me."
            the_person.char "Absolutely sir, you'll know as soon as I know something."
            $ random_day = day + renpy.random.randint(2,4)
            $ mc.business.event_triggers_dict["advanced_serum_stage_1"] = True
            $ advanced_serum_unlock_stage_2 = Action("Advanced serum unlock stage 2",advanced_serum_stage_2_requirement,"advanced_serum_stage_2_label", args = the_person, requirement_args = [the_person, random_day])
            $ mc.business.mandatory_crises_list.append(advanced_serum_unlock_stage_2) #Append it to the mandatory crisis list so that it will be run eventually. We will list the person and the random day that the event will finish.

        "Try and secure a prototype serum.\n{size=22}Costs $2000{/size} (disabled)" if mc.business.funds < 2000:
            pass

        "Wait until later.":
            mc.name "Funds are tight right now. I'll try and secure them for you, but until do what you can with the resources you have."
            the_person.char "Understood. Come by and visit any time."

    return

label advanced_serum_stage_2_label(the_person):
    #TODO: Add a special section where the head researcher aknowledges the work of her predecesor if the person who is handed over here is not the head researcher any more.
    if mc.location != mc.business.r_div:
        "Your phone buzzes, alerting you to a work email."
        the_person.char "I have news about the prototype serum you asked me to retrieve. Meet me in the R&D department when you have a moment."
        "You finish up what you were working on and head over to meet [the_person.title]."
        $ mc.change_location(mc.business.r_div)
        $ renpy.show(mc.business.r_div.name,what=mc.business.r_div.background_image)
        $ the_person.draw_person()
        show screen person_info_ui(the_person)
        mc.name "What's the news [the_person.title]?"

    else:
        $ renpy.show(mc.business.r_div.name,what=mc.business.r_div.background_image)
        the_person.char "Excuse me, [the_person.mc_title]?"
        $ the_person.draw_person()
        show screen person_info_ui(the_person)
        the_person.char "I have some news about that prototype serum you asked me to retrieve. Can I have a moment?"
        mc.name "Of course."
    "[the_person.title] nods towards one of the small offices attached to the lab. You follow her inside and shut the door after yourself."
    the_person.char "I was able to get in touch with a small research team that was doing some work paralleling our own, and after some sweet talking I got my hands on this..."
    if the_person.outfit.get_lower_ordered(): #Use this as a proxy to see if she is wearing something on her lower body.
        "She reaches into a pocket and pulls out small brown tinted vial, corked with a rubber stopper."
    else:
        "She grabs a small brown tinted vial off of the table and shows it to you. It's corked with a rubber stopper."
    mc.name "Excellent work [the_person.title]. Reverse engineering it is our next step then, correct?"
    the_person.char "I've set aside enough for a thorough chemical analysis, but I doubt that will give us a complete picture."
    mc.name "What do you suggest we do then?"
    the_person.char "With your permission I'd like to test it on myself. We can record the results, and I'll look over them after. With some luck I should learn enough to push our research forward."
    #TODO: Give you the option to test on someone else in your R&D division.
    mc.name "I agree, this seems like our most likely way forward."
    the_person.char "I'm glad you agree. Okay, I don't know what effect this will have on me so I want to record it."
    "[the_person.title] leaves the room for a moment, then returns with a small tripod. She mounts her phone on it and sets it up on the table facing both of you."
    "When she turns back she hands a second vial of liquid over to you. This one is in the familiar labware you use every day."
    the_person.char "I prepared this just in case, it counteracts any effects of the prototype serum. Use it if something is going wrong, but remember this might be the only chance we get to try this."
    "You take the second vial of serum and tuck it in your back pocket."
    mc.name "Are you ready?"
    "[the_person.possessive_title] nods. She starts her phone recording and looks into the lens."
    the_person.char "I'm [the_person.title], head researcher at [mc.business.name]. The following are the effects of the prototype serum we have secured."
    "She takes the rubber stopper off of the vial and swirls the content. After a steadying breath and glance at you she drinks it all down."
    the_person.char "Bleh... The taste isn't anything to write home about."
    "[the_person.title] puts the container on the table and waits for a few seconds while the serum takes full effect. You watch carefully, studying her reaction."
    $ old_int = the_person.int
    "As you watch her pupils dilate, her breathing slows and becomes more regular, and her gaze settles dead ahead."
    mc.name "How are you feeling [the_person.title]?"
    the_person.char "Fine. A little warm maybe."
    $ the_person.draw_person(emotion="happy")
    "She looks at you and smiles, then laughs self consciously."
    $ the_person.change_happiness(15)
    the_person.char "I don't know why I was so worried about this, I feel silly getting you so involved. This feels fine."
    $ the_person.change_slut_core(5)
    $ slut_report = the_person.change_slut_temp(10)
    the_person.char "I mean, not that I mind the help of such a good looking man."
    "She giggles and looks you up and down."
    mc.name "Try and focus [the_person.title], do you notice any unusual with yourself right now?"
    the_person.char "With me? Why would... Oh right, because of the test! Sorry, you're just so... distracting."
    $ the_person.change_int(-1)
    $ the_person.change_slut_core(10)
    $ slut_report = the_person.change_slut_temp(20)
    "She bites her lip and takes a step closer. You notice her cheeks are flush and her breathing is getting a little heavier."
    the_person.char "Ugh, [the_person.mc_title] do we really have to do this right now? Couldn't we be doing something more fun? I can think of a ton of fun things we could do together."
    $ the_person.change_int(-1)
    $ the_person.change_slut_core(10)
    $ slut_report = the_person.change_slut_temp(20)
    $ old_personality = the_person.personality
    $ the_person.personality = bimbo_personality
    $ mc.log_event("[the_person.title]: Personality changed. Now: Bimbo", "float_text_pink")
    "[the_person.title] reaches her hand down to your waist and runs her fingers along your cock through your pants."
    menu:
        "Have sex with [the_person.title].":
            "You smile back at [the_person.title]. She lets out a happy giggle when you wrap your arms around her waist."
            $ the_person.change_int(-1)
            call fuck_person(the_person) from _call_fuck_person_8
            if the_person.arousal > 100:
                $ the_person.change_obedience(10)
                the_person.char "Oh... my... god... [the_person.mc_title] that felt so good! If you could make me feel like that all the time I swear I would do anything for you. Anything at all."
            else:
                "[the_person.possessive_title] giggles softly."
                the_person.char "Ahh, that was a lot of fun [the_person.mc_title]. I really want to give that another try, maybe once you've had a chance to recharge."

            "It's been a few minutes since [the_person.title] took the dose of prototype serum. Besides the obvious spike in arousal she seems more carefree and eager to please you."
            "Even her tone of voice has changed; She's practically bubbling over with excitement right now. She certainly doesn't seem like the intelligent research head you've come to rely on though."

            menu:
                "Give [the_person.title] the reversal serum.":
                    $ had_sex = True
                    $ the_person.reset_arousal()
                    pass #This falls through to the previous section.

                "Leave [the_person.title] the way she is.":
                    "You think about giving [the_person.title] the reversal serum but decide against it. You aren't sure if the serum effects will wear off, but she seems happy enough as she is."
                    "[the_person.title] certainly doesn't seem like she's in any state to run your research department. It would be a good idea to pick a successor to continue [the_person.title]'s work."
                    $ the_person.reset_arousal()
                    mc.name "Okay [the_person.title], we're all done here."
                    "Her eyebrows knit together, like a child's attempt to concentrate."
                    the_person.char "I... wasn't there something I was suppose to do first? Or have done? Uh... I'm sorry [the_person.mc_title], I'm having a real hard time thinking right."
                    "She sticks out her tounge, then giggles and shrugs."
                    the_person.char "Oh well, how important can it be, right? Glad I could help you with your science. And all that fun other stuff."
                    mc.name "And thank you for all that help."
                    "[the_person.possessive_title] gives you a wink and leaves the room. "
                    $renpy.scene("Active")
                    "You take [the_person.title]'s phone off of it's tripod and make a copy of the footage it took. Maybe your next head researcher can make use of this to figure out how to press forward."
                    $ mc.business.event_triggers_dict["advanced_serum_stage_3"] = True #Flag the next event to be enabled.
                    $ mc.business.event_triggers_dict["research_bimbo"] = the_person
                    return

        "Give [the_person.title] the reversal serum.":
            $ had_sex = False
            pass

    #Undo the effects of the serum, we will use a special exit if we leave her as she is.
    mc.name "Okay [the_person.title], I think we should wrap this little experiment up. I need you to drink this for me."
    "You grab the reversal serum from your back pocket and hand it over. [the_person.title] pouts and looks at you."
    $ the_person.draw_person(emotion="sad")
    the_person.char "Aww, do I have to? I really like the way I feel right now."
    mc.name "Drink up."
    "She frowns but does as she's told. She drinks the content of the vial."
    $ int_to_add = old_int - the_person.int #Calculate what we need to add back, almost certainly 3 but wierd things might happen.
    $ the_person.change_int(int_to_add)
    $ the_person.change_slut_core(-25)
    $ the_person.change_slut_temp(-50)
    $ the_person.change_happiness(-15)
    # $ the_person.remove_status_effects([bliss,ditzy])
    $ the_person.personality = old_personality
    $ mc.log_event("[the_person.title]: Suggestability removed.", "float_text_blue")
    $ mc.log_event("[the_person.title]: - Ditzy", "float_text_blue")
    $ mc.log_event("[the_person.title]: - Blissful", "float_text_blue")
    $ mc.log_event("[the_person.title]: Personality Restored", "float_text_blue")
    "After another moment [the_person.title] shakes her head and looks at you. She seems suddenly more alert, more aware."
    the_person.char "Ugh, that's given me a serious headache. I'm not sure if I should blame their stuff or mine."
    mc.name "Glad to have you back. Are you feeling like yourself again?"
    the_person.char "Yeah, I think so. I mean, it's a little hard to say I guess."
    "[the_person.title] grabs her phone and unclips it from the short tripod it was on."
    if had_sex:
        the_person.char "Well I guess we have plenty of evidence that the prototype affects inhibition and arousal."
        mc.name "Sorry about that, I just..."
        $ slut_report = the_person.change_slut_temp(5)
        the_person.char "No, I was literally throwing myself at you, I understand. It was fun, honestly."
        "She looks at her phone for a moment, then back up at you."
        the_person.char "And you managed to keep it all in frame. That should help me break down the effects piece by piece."

    else:
        the_person.char "About what I said before, while I was... you know. Thank you for not taking advantage of it."
        $ the_person.change_obedience(5)
        $ the_person.change_happiness(5)
        $ the_person.change_love(5)
        mc.name "Of course, I understand that you weren't yourself. I'm glad to have you're back to normal."
        "She looks at her phone for a moment, then back up at you."
        the_person.char "I'll have to go over the footage in more detail, but I think I'll be able to break the effects down piece by piece from this."
    the_person.char "Obviously I can't make any promises, but between this and the chemical analysis I think we have a good shot at recreating the basic creation techniques used."
    the_person.char "I'm going to go take a break, but stop by later if you want me to change our research focus and look into this more."
    $ mc.log_event("Tier 2 Research Unlocked","float_text_grey")
    $ mc.business.research_tier = 2
    return

label advanced_serum_stage_3_label(the_person):
    #This event can only come up when the player has chosen to keep their head researcher a bimbo. It makes sure they can still reach the second tier of research.
    mc.name "[the_person.title], I have some experimental footage I need you to look at."
    the_person.char "Hmm? What is it about?"
    $ old_researcher = mc.business.event_triggers_dict["research_bimbo"] #Get the old researcher so we can call her name.
    if mc.business.get_employee_workstation(old_researcher):
        mc.name "I'm sure you've seen [old_researcher.name] around the office? She use to be my head of research and insisted she try a prototype serum she had located."
        the_person.char "She use to lead the R&D team?"
        mc.name "Just look at this, it will all make sense."
    else:
        mc.name "A previous head of research insisted she try a prototype serum she had located. These were the test results."
    "You hand [the_person.title] a thumb drive containing the footage of your test session with [old_researcher.name]. She plugs the drive into her computer and opens up the footage."
    $ slut_report = the_person.change_slut_temp(5)
    the_person.char "Oh my god... it's like something flipped a switch inside of her."
    "[the_person.title] watches as [old_researcher.name] steps close to you and reaches down to grab your crotch."
    mc.name "As far as I can tell the effects are permanent. It's unfortunate, but I know she wouldn't want us to let all of her research go to waste."
    the_person.char "I... I understand sir. I'll pull apart what I can and list out some preliminary theories."
    $ mc.business.research_tier = 2
    $ mc.log_event("Tier 2 Research Unlocked", "float_text_grey")

    return

label futuristic_serum_stage_1_label(the_person):
    mc.name "[the_person.title], what do you think about the current state of our R&D? Is there anything we could be doing better?"
    the_person.char "We seem to be pressed right up against the boundry of knowledge for medical science. Before we can come up with anything new we need data, and there just isn't any."
    the_person.char "What I need right now are test subjects. Girls who have taken a few doses of serum and been affected by it. If we can do that I can build up some data and maybe discover something new."
    mc.name "It's probably best these girls come from inside the company. How many test subjects do you need?"
    the_person.char "Not including me: three. I'll need them to be obedient and open to... intimate testing procedures."
    "[the_person.title] requires three employees who satisfy the following requirements: Core Sluttiness 50+ and Obedience 130+."
    mc.name "Alright [the_person.title], I'll do what I can. I'll come back when I've got some girls who fit your requirements."
    $ mc.business.event_triggers_dict["futuristic_serum_stage_1"] = True
    return

label futuristic_serum_stage_2_label(the_person):
    if __builtin__.len(mc.business.get_requirement_employee_list(core_slut_required = 50, obedience_required = 130)) <= 3: # If you don't have enough people who meet the requirements just get an update.
        mc.name "I'm still working on getting your test subjects ready. Could you remind me what you need?"
        the_person.char "To learn anything useful I need at least three girls who have been seriously affected by our serums. I need them to be obedient and open to some intimate testing procedures."
        "[the_person.title] requires three employees who satisfy the following requirements: Core Sluttiness 50+ and Obedience 130+"
        $ satisfying_list = mc.business.get_requirement_employee_list(core_slut_required = 50, obedience_required = 130, exclude_list = [the_person])
        $ my_string = "The following people currently satisfy the requirements: "
        python:
            if satisfying_list:
                for person in satisfying_list:
                    my_string += person.name + " " + person.last_name + ", "
            else:
                my_string = "There is currently nobody in your company who meets these requirements."
        "[my_string]"
        the_person.char "Noted. I'll get back to you when I have your test subjects ready."
        return

    mc.name "[the_person.title], I have your group of test subjects ready."
    the_person.char "Excellent, let me know who to call down and I'll begin as soon as possible."
    $ possible_picks = mc.business.get_requirement_employee_list(core_slut_required = 50, obedience_required = 130, exclude_list = [the_person])
    call screen employee_overview(white_list = possible_picks, person_select = True)
    $ pick_1 = _return
    call screen employee_overview(white_list = possible_picks, black_list = [pick_1], person_select = True)
    $ pick_2 = _return
    call screen employee_overview(white_list = possible_picks, black_list = [pick_1,pick_2], person_select = True)
    $ pick_3 = _return
    "[the_person.title] looks over the files of the employees you suggested and nods approvingly."
    the_person.char "I think they will do. You're sure you want me to bring in [pick_1.name], [pick_2.name], and [pick_3.name] for testing?"
    menu:
        "Begin the testing.":
            pass

        "Reconsider.":
            mc.name "On second thought, I don't think I want them involved. I'll think about it and come back."
            the_person.char "I'll be here."
            return

    mc.name "Yes, you may begin."
    $ the_person.draw_person(emotion = "happy")
    the_person.char "Excellent!"
    "[the_person.title] gets her phone out and calls all three girls down to the lab. It doesn't take long for them all to assemble."
    the_person.char "The testing might take some time sir, I'll get started right now and have all my findings recorded. Come by later and we can review any discoveries."
    "[the_person.title] turns to the other girls."
    the_person.char "Well then, we have some special testing to get through today! Who would like to go first?"
    $ go_first = pick_1
    if pick_2.obedience > go_first:
        $ go_first = pick_2
    if pick_3.obedience > go_first:
        $ go_first = pick_3
    "[go_first.name] raises her hand and [the_person.title] smiles and grabs her clipboard."
    the_person.char "Very good. Come with me, you two can wait here until we're done."
    "[the_person.title] leads [go_first.title] into a side office, and you decide to leave her to her work."
    #TODO: Expand this event for more sexy stuff.
    $ mc.business.research_tier = 3
    $ mc.log_event("Max Research Tier Unlocked", "float_text_grey")
    call advance_time from _call_advance_time_9
    return

#SISTER EVENTS#

label sister_intro_crisis_label(the_person):
    #This is a mantatory crisis, so we assume that our requirements are tight enough to always trigger correctly. If you want to do crisis requirement checks here you need to re-add the crisis to the mandatory list!
    $ renpy.show(bedroom.name,what=bedroom.background_image)
    "There's a knock at your bedroom door."
    mc.name "Come in."
    $ the_person.draw_person()
    show screen person_info_ui(the_person)
    the_person.char "Hey [the_person.mc_title], do you have a moment?"
    mc.name "Sure, what's up?"
    "[the_person.possessive_title] steps into your room and closes the door behind her."
    the_person.char "I wanted to say I'm really impressed with how your business is going. It must be really exciting to be your own boss now."
    mc.name "It's certainly been challanging, that's for sure."
    the_person.char "And... Well, I've been so busy with school that I haven't had a chance to get a job like Mom's been wanting..."
    mc.name "Oh no, I can see where this is going."
    the_person.char "If you could just give me a {i}tiny{/i} bit of cash I could show Mom I can take care of myself."
    mc.name "But you can't, apparantly."
    the_person.char "Please? Please please please, [the_person.mc_title]? Maybe there's some extra work I could do? I could..."
    "She gives up and shrugs."
    the_person.char "Help you science all that science stuff?"
    mc.name "I don't think that's really where I need help. But..."
    menu:
        "Ask [the_person.title] to test serum for you.":
            the_person.char "But...? Come on [the_person.mc_title], I really need your help."
            mc.name "Well, at the lab we've been running some experiements, but we need some test subjects."
            mc.name "I can bring home some of the stuff we're working on and if you let me test it on you I can pay you for it."
            the_person.char "It's not going to turn me into a lizard or something, right?"
            mc.name "Obviously not. It's just a liquid that you'd need to drink, then I'll watch to see how it affects you over the next few hours."
            the_person.char "What is it going to do?"
            mc.name "That's what we're trying to find out."
            $ the_person.draw_person(emotion = "happy")
            "[the_person.possessive_title] thinks about it for a moment, then nods."
            the_person.char "Okay, but I want $50 each time."
            mc.name "You drive a hard bargin sis. You've got a deal."
            "You shake on it."
            $ the_person.change_obedience(5)
            the_person.char "Thank you so much [the_person.mc_title]. Uh, if Mom asks just say I got a part time job."
            mc.name "Sure thing. I'll come see you when I have something for you to test."
            "[the_person.title] gives you one last smile then leaves your room, shutting the door behind her."
            $ mc.business.event_triggers_dict["sister_serum_test"] = True

        "Ask [the_person.title] to leave you alone.":
            the_person.char "But...?"
            mc.name "But I was just about to head to bed, so if you could let me get some sleep that would be a huge help."
            $ the_person.draw_person(emotion = "sad")
            $ the_person.change_happiness(-5)
            "[the_person.title] pouts and crosses her arms. She leaves your room in a huff."
            $ mc.business.event_triggers_dict["sister_needs_reintro"] = True

    $ renpy.scene("Active")
    hide screen person_info_ui
    return

label sister_reintro_label(the_person):
    #If you turn your sister away the first time you can approach her and ask to have her test serums anyways.
    mc.name "So [the_person.title], are you still looking for some work to do?"
    $ the_person.draw_person(emotion = "happy")
    the_person.char "Oh my god yes! Do you have something for me to do?"
    mc.name "Well, at the lab we've been running some experiements, but we need some test subjects."
    mc.name "I can bring home some of the stuff we're working on and if you let me test it on you I can pay you for it."
    the_person.char "It's not going to turn me into a lizard or something, right?"
    mc.name "Obviously not. It's just a liquid that you'd need to drink, then I'll watch to see how it affects you over the next few hours."
    the_person.char "What is it going to do?"
    mc.name "That's what we're trying to find out."
    $ the_person.draw_person(emotion = "happy")
    "[the_person.possessive_title] thinks about it for a moment, then nods."
    the_person.char "Okay, but I want $50 each time."
    mc.name "You drive a hard bargin sis. You've got a deal."
    "You shake on it."
    $ the_person.change_obedience(5)
    the_person.char "Thank you so much [the_person.mc_title]. Uh, if Mom asks just say I got a part time job."
    mc.name "Sure thing. I'll let you know when I have something for you to test."
    $ mc.business.event_triggers_dict["sister_needs_reintro"] = False
    $ mc.business.event_triggers_dict["sister_serum_test"] = True
    return

label sister_serum_test_label(the_person):
    #Give your sister some serum to test for cash.
    mc.name "Hey [the_person.title], I have something for you to test out for me."
    the_person.char "Alright, $50 and I'll try it."
    call give_serum(the_person) from _call_give_serum_7
    if _return:
        $ mc.business.funds += -50
        "You give [the_person.possessive_title] the cash and the serum. She puts the money away then drinks the serum, handing back the empty vial."
        $ the_person.change_obedience(1)
        the_person.char "Easiest fifty bucks I've ever earned. I guess you can hang around and keep an eye on me if it's important for your research."
        if mc.business.event_triggers_dict.get("sister_serum_test_count"):
            $ mc.business.event_triggers_dict["sister_serum_test_count"] += 1
        else:
            $ mc.business.event_triggers_dict["sister_serum_test_count"] = 1

    else:
        mc.name "Sorry [the_person.title], I guess I don't actually have anything for you to test."
        the_person.char "Ugh, come on [the_person.mc_title], you know I need the money!"
        mc.name "I'll find something for you to test, promise."
    return

label sister_strip_intro_label(the_person):
    #Give your sister some cash in exchange for her stripping. Higher sluttiness means she'll strip more (for less).
    $ renpy.show(bedroom.name,what=bedroom.background_image)
    "There's a knock at your bedroom door."
    mc.name "Come in."
    $ the_person.draw_person()
    show screen person_info_ui(the_person)
    the_person.char "Hey [the_person.mc_title], can I talk to you about something?"
    "[the_person.possessive_title] comes into your room and shuts the door behind her. She seems nervous, avoiding eye contact as she comes closer."
    mc.name "Any time, what's up?"
    the_person.char "You know how I've been testing some of that lab stuff you make? For money?"
    mc.name "Yeah."
    the_person.char "Well I've been out shopping, and Mom would {i}kill{/i} me if she knew how much I was spending, so I was hoping you could pay me some more."
    mc.name "Sorry [the_person.title], I don't have anything for you to test right now."
    $ the_person.draw_person(emotion = "sad")
    the_person.char "Oh come on [the_person.mc_title], don't you have anything I could do? I really need the money now."
    "[the_person.possessive_title] puts her arms behind her back and pouts at you."
    menu:
        "Pay her to strip for you.":
            call strip_explanation(the_person) from _call_strip_explanation


        "Tell her to leave.":
            mc.name "I just don't have anything to give you [the_person.title]. I promise if I think of anything I'll come to you right away."
            the_person.char "Ugh... fine."
            "She turns and leaves your room, disappointed."
            $ the_person.change_happiness(-5)
            $ mc.business.event_triggers_dict["sister_strip_reintro"] = True

    $ renpy.scene("Active")
    hide screen person_info_ui
    return

label sister_strip_reintro_label(the_person):
    mc.name "I've been thinking about some stuff you could do for me [the_person.title]. Are you still interested in earning some more money?"
    $ the_person.draw_person(emotion = "happy")
    the_person.char "Yes! What do you want me to do?"

    call strip_explanation(the_person) from _call_strip_explanation_1

    $ mc.business.event_triggers_dict["sister_strip_reintro"] = False
    return

label strip_explanation(the_person):
    #Pulls out the explanation part of the strip intro so it's not duplicated
    mc.name "I've been busy getting my business running and earning all of this money I'm going to be paying you, so I haven't had a chance to meet many people."
    mc.name "It's been a while since I was able to just appreciate the looks of a hot woman."
    the_person.char "What are... what are you suggesting?"
    mc.name "I'll pay you if you just stand around and let me look at you. Maybe take some of your clothing off, if you're comfortable with it."
    the_person.char "So you want me to give you a strip show?"
    "You nod."
    "[the_person.possessive_title] seems surprised, but not particularly offended by the idea. She takes a long moment to consider it."
    the_person.char "Okay, I'll do it. I want $100 up front, plus a little extra if you want me to take anything off."
    mc.name "I think that's reasonable."
    $ the_person.change_obedience(5)
    $ mc.business.event_triggers_dict["sister_strip"] = True
    the_person.char "And obviously you can't touch me. Or yourself. And you can {i}never{/i} tell Mom about it."
    mc.name "Don't worry [the_person.title], I promise I won't make it weird."
    "[the_person.title] nods. There's a long silence before she speaks again."
    the_person.char "So... do you want me to do it for you now?"
    menu:
        "Ask her to strip for you." if mc.business.funds >= 100:
            mc.name "I don't see why not."
            $ mc.business.funds += -100
            "You pull a hundred dollars out of your wallet and hand it over to [the_person.possessive_title]. She tucks it away and gets ready."
            call pay_strip_scene(the_person) from _call_pay_strip_scene

        "Ask her to strip for you.\n{size=22}Requires: $100{/size} (disabled)" if mc.business.funds < 100:
            pass

        "Not right now.":
            mc.name "Not right now. I'll come find you if I'm interested, okay?"
            the_person.char "Okay. Thanks for helping me out [the_person.mc_title], you're a life saver."
            "[the_person.title] leaves your room and closes the door behind her."
    return


label sister_strip_label(the_person):
    #A short intro so that we can reuse the pay_strip_scene with other characters if we want.
    mc.name "So [the_person.title], are you interested in earning a hundred dollars?"
    if the_person.sluttiness < 50:
        the_person.char "Oh, do you want me to... show off for you?"
    else:
        the_person.char "You want me to strip down for you?"
    $ mc.business.funds += -100
    "You nod and sit down on [the_person.possessive_title]'s bed. She holds her hand out and you hand over her money."
    "She tucks the money away and gets ready in front of you."
    call pay_strip_scene(the_person) from _call_pay_strip_scene_1
    return

label pay_strip_scene(the_person):
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

    $ pose_list = [["Turn around","walking_away"],["Turn around and look back","back_peek"],["Hands down, ass up.","standing_doggy"],["Be flirty","stand2"],["Be casual","stand3"],["Strike a pose","stand4"],["Move your hands out of the way","stand5"]]

    $ picked_pose = the_person.idle_pose #She starts in her idle pose (which is a string)
    $ rand_strip_desc = renpy.random.randint(0,3) #Produce 4 different descriptions at each level to help keep this interesting.

    # strip_willingness is a measure of how into the whole strip process the girl is. The less dressed she get the more embarassed she'll get,
    # the more slutty the more she'll tease you, take clothing off willingly, etc.
    $ strip_willingness = the_person.sluttiness + (5*the_person.get_opinion_score("not wearing anything")) - the_person.outfit.slut_requirement
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
                the_person.char "Oh my god..."
                "[the_person.title] covers her eyes for a moment and looks away."
            else:
                "[the_person.title] shakes her head and mutters to herself."
                the_person.char "I can't believe I'm doing this..."

        elif strip_willingness < 20:
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

        elif strip_willingness < 60:
            $tease_clothing = the_person.outfit.remove_random_any(top_layer_first = True, exclude_feet = True, do_not_remove = True) #She's slutty enough that she wants to tease you a little more
            if rand_strip_desc == 0:
                if tease_clothing is not None:
                    "[the_person.title] pulls at her [tease_clothing.name] seductively."
                    the_person.char "Mmm, I bet you want me to take this off, right?"
                else:
                    "[the_person.title] runs her hands down her body seductively."
                    the_person.char "Mmm, I bet you want to get your hands on me now, right?"

            elif rand_strip_desc == 1:
                if the_person.has_large_tits():
                    "[the_person.title] moves her body side to side for you, letting her large tits bounce and jiggle while you watch."
                else:
                    "[the_person.title] moves her body side to side for you while you watch."

            elif rand_strip_desc == 2:
                if tease_clothing is not None:
                    "[the_person.title] slips a hand under her [tease_clothing.name] and starts to pull it off."
                    the_person.char "Maybe I should just... slip this off. What do you think?"
                else:
                    if the_person.has_large_tits():
                        "[the_person.title]'s hands slide up and down her body. She cups one of her sizeable breast and squeezes it, pinching her own nipple while she does."
                    else:
                        "[the_person.title]'s hands slide up and down her body. She rubs her small breasts, paying special attention to their firm nipples."
            else:
                the_person.char "I hope you're enjoying the show [the_person.mc_title]."
                "She wiggles her hips for you and winks."

        else: #strip_willingness >= 60
            $tease_clothing = the_person.outfit.remove_random_any(top_layer_first = True, exclude_feet = True, do_not_remove = True) #She's slutty enough that she wants to tease you a little more
            if rand_strip_desc == 0:
                if tease_clothing is not None:
                    "[the_person.title] pulls at her [tease_clothing.name]."
                    the_person.char "I'm going to have to get this out of the way before we can have any fun."
                else:
                    "[the_person.title] runs her hands over her own body."
                    the_person.char "Oh [the_person.mc_title], I think I'm going to need more than your eyes on me soon..."

            elif rand_strip_desc == 1:
                "[the_person.title] puts her hands up in the air and spins around. You get a great look at her body as she enjoys herself."

            elif rand_strip_desc == 2:
                if tease_clothing is not None:
                    the_person.char "Don't you just think all of this clothing is just useless? How about I take it all off for you... would you like that?"
                else:
                    "[the_person.title] takes a wider stances and slides her hands down her own thighs, all while maintaining eye contact with you."
                    the_person.char "You're looking so good today [the_person.mc_title], did you know that?"

            else:
                "[the_person.title] wiggles her hips side to side and bites her bottom lip, as if imagining some greater pleasure yet to come."

        $menu_list = [] #Tuple of menu things.
        # High obedience characters are more willing to be told to strip down (althoug they still expect to be paid for it)
        # Low obedience characters will strip off less when told but can be left to run the show on their own and will remove some.
        python:
            for item in the_person.outfit.get_unanchored():
                test_outfit = the_person.outfit.get_copy()
                test_outfit.remove_clothing(item)
                new_willingness = the_person.sluttiness + (5*the_person.get_opinion_score("not wearing anything")) - test_outfit.slut_requirement
                if new_willingness + (the_person.obedience-100) >= 0:
                    #They're willing to strip it off.
                    price = 0 # Default value
                    if new_willingness >= 40:
                        price = 0 #They'll do it for free!

                    elif new_willingness >= 20:
                        price = (strip_willingness - new_willingness) * 3 #They feel pretty good about how they'll be dressed after, so the price is decent.

                    else:
                        price = (strip_willingness - new_willingness) * 10 #THey will feel pretty uncomfortable, so they expect to be paid well.

                    price = math.ceil((price/5.0))*5 #Round up to the next $5 increment

                    display_string = "Strip " + item.name + "\n{size=22}$" + str(price) + "{/size}"
                    if price > mc.business.funds:
                        display_string += " (disabled)"

                    menu_list.append([display_string, [item,price]])

                else:
                    menu_list.append(["Strip " + item.name + "\n{size=22}Too Slutty{/size} (disabled)", [item,-1]])

            menu_list.append(["Just watch.","Watch"])
            menu_list.append(["Tell her to pose.","Pose"])
            menu_list.append(["Finish the show.","Finish"])

        $ strip_choice = renpy.display_menu(menu_list,True,"Choice")
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
                        if new_willingness >= 40: #She's slutty enough to do it for free!
                            $ price = 0
                        elif new_willingness >= 20:
                            $ price = (strip_willingness - new_willingness) * 3
                        else:
                            $ price = (strip_willingness - new_willingness) * 10

                        $ price = math.ceil((price/5.0))*5 #Round up to the next $5 increment
                        if price > 0:
                            "[the_person.title] steps a little closer to you and plays with the edge of her [tease_item.name]."
                            the_person.char "$[price] and I'll take this off for you..."
                            menu:
                                "Pay her $[price]." if price <= mc.business.funds:
                                    "You pull the cash out of your wallet and hand it over."
                                    $ mc.business.funds += -price
                                    $ the_person.change_obedience(-1)
                                    $ the_person.change_slut_temp(1)
                                    $ the_person.draw_animated_removal(tease_item, position = picked_pose)
                                    "[the_person.title] takes it, puts it to the side, and starts to slide her [tease_item.name] off."


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
                the_person.char "Oh my god, I thought I was going to die of embarrassment!"
            elif strip_willingness < 20:
                the_person.char "Oh, okay. That... wasn't as bad as I thought it was going to be, at least."
            else:
                the_person.char "Oh, is that all you wanted to see? I feel like we were just getting started!"

        else: #The only other result is an actual strip. Pay the cash, remove the piece and loop or end.
            $ mc.business.funds += -strip_choice[1]
            $ test_outfit = the_person.outfit.get_copy() #We use a temp copy so that we can get her reaction first.
            $ test_outfit.remove_clothing(strip_choice[0])
            $ the_clothing = strip_choice[0]
            # $ the_person.draw_animated_removal(strip_choice[0], position = picked_pose)
            $ strip_willingness = the_person.sluttiness + (5*the_person.get_opinion_score("not wearing anything")) - test_outfit.slut_requirement
            if strip_choice[1] > 0:
                if strip_willingness < 0:
                    "You pull some cash from your wallet and offer it to [the_person.title]. She takes it and looks at it for a long second."
                    the_person.char "Oh my god... I shouldn't be doing this..."
                    $ the_person.change_obedience(2)
                    $ the_person.change_slut_temp(1)
                    "Nevertheless, she keeps the money and pulls off her [the_clothing.name]."
                    $ the_person.draw_animated_removal(strip_choice[0], position = picked_pose)
                elif strip_willingness < 20:
                    "You pull some cash out from your wallet and hand it over to [the_person.title]. She puts it to the side and grabs her [the_clothing.name]."
                    the_person.char "Ready?"
                    $ the_person.change_obedience(1)
                    $ the_person.change_slut_temp(1)
                    $ the_person.draw_animated_removal(strip_choice[0], position = picked_pose)
                    "You nod and [the_person.title] pulls off the piece of clothing, throwing it to the side."
                else:
                    "You're still pulling out cash as [the_person.title] strips off her [the_clothing.name] and chucks it to the side."
                    $ the_person.draw_animated_removal(strip_choice[0], position = picked_pose)
                    the_person.char "Thank you!"
                    "She plucks the cash from your hand and quickly puts it away."

            else: #She'll only do it for free if she's becoming less slutty (ie taking off lingerie, bondage gear, etc.) or if she's very slutty anyways.
                the_person.char "Is that all? Well, I think that's easy."
                $ the_person.draw_animated_removal(strip_choice[0], position = picked_pose)
                "[the_person.title] strips off her [the_clothing.name] for free, leaving it on the ground at her feet."

    return

label mom_weekly_pay_label(the_person):
    $ renpy.show(bedroom.name,what=bedroom.background_image)
    "You're getting ready for bed when [the_person.possessive_title] calls from downstairs."
    the_person.char "[the_person.mc_title], could we talk for a moment?"
    mc.name "Sure, down in a second."
    show screen person_info_ui(the_person)
    $ renpy.show(kitchen.name,what=kitchen.background_image)
    $ the_person.draw_person(position = "sitting")
    "[the_person.title] is sitting at the kitchen table, a collection of bills laid out in front of her."

    if the_person.sluttiness < 20:
        the_person.char "This new morgage on the house is really stressing our finances. It would really help if you could chip in."
        menu:
            "Give her nothing.":
                mc.name "Sorry Mom, I'm just not turning a profit right now. Hopefully we will be soon though. I'll help out as sooon as I can."
                $ the_person.change_happiness(-5)
                $ the_person.change_love(-1)
                $ the_person.draw_person(position = "sitting", emotion = "sad")
                the_person.char "Okay swetheart, I understand. I'll talk with Lily and let her know that we have to cut back on non essentials."

            "Help out.\n{size=22}-$100{/size}" if mc.business.funds >= 100:
                "You pull out your wallet and count out some cash."
                $ mc.business.funds += -100
                mc.name "Here you go Mom, I hope this helps."
                $ the_person.change_happiness(5)
                $ the_person.change_love(3)
                $ the_person.draw_person(position = "sitting", emotion = "happy")
                the_person.char "Every little bit does sweetheart. Thank you so much."
                "She gives you a hug and turns her attention back to the bills."

            "Help out.\n{size=22}-$100{/size} (disabled)" if mc.business.funds < 100:
                pass

    else: #TODO: have an even higher level
    #elif the_person.sluttiness < 60:
        if mc.business.event_triggers_dict.get("Mom_Payment_Level",0) >= 1: #We've been through this song and dance already.
            the_person.char "The budget is still really tight [the_person.mc_title], so I was wondering if you wanted to buy any sort of favour from me?"

        else:
            the_person.char "Our budget is really stretched thin right now, and it would be a huge relief if you could help out."
            the_person.char "I wouldn't feel right about just taking your hard earned money though, so I was hoping we could make a deal..."
            mc.name "What sort of deal Mom?"
            the_person.char "Remember last summer, and you paid me for some... personal favours?"
            "She blushes and looks away for a second before regaining her composure."
            the_person.char "Maybe we could start doing that again... I know I shouldn't even bring it up."
            mc.name "No Mom, you're doing it for the good of the family, right? I think it's a great idea."
            $ the_person.change_slut_temp(2)
            $ the_person.change_happiness(5)
            $ the_person.change_love(2)
            the_person.char "Of course, it's the best thing for all of us. What would you like to do?"
            $ mc.business.event_triggers_dict["Mom_Payment_Level"] = 1


        menu:
            "Have strip for you. -$100" if mc.business.funds >= 100:
                if mc.business.event_triggers_dict.get("Mom_Strip",0) >= 1:
                    mc.name "I want you to show off yourself off to me, how does that sound?"
                    the_person.char "Fair is fair, but I'll need a little extra if you want to see anything... inappropriate."
                    $ mc.business.funds += -100
                    "You hand over the cash and sit back while [the_person.possessive_title] entertains you."
                else:
                    $ mc.business.event_triggers_dict["Mom_Strip"] = 1
                    mc.name "I'd like to see a little more of you Mom, how about I pay you to give me a little strip tease."
                    the_person.char "Oh my god, I've raised such a dirty boy. How about I pose for you a bit, and if you want to see more you can contribute a little extra."
                    mc.name "Sounds like a good deal Mom."
                    $ mc.business.funds += -100
                    "You hand over the cash and sit back while [the_person.possessive_title] entertains you."

                call pay_strip_scene(the_person) from _call_pay_strip_scene_2

            "Have strip for you. -$100 (disabled)" if mc.business.funds <100:
                pass

            "Have her test some serum. -$100" if mc.business.funds >= 100:
                if mc.business.event_triggers_dict.get("Mom_Serum_Test",0) >= 1:
                    mc.name "I've got some more serum I'd like you to test Mom."
                    call give_serum(the_person) from _call_give_serum_10
                    if _return:
                        $ mc.business.funds += -100
                        "You hand the serum to [the_person.possessive_title], followed by the cash."
                        the_person.char "Okay, so that's all for now?"
                        mc.name "That's all. I'll just be keeping an eye on you in the future, but you don't need to worry about that."
                        the_person.char "Well thank you sweetheart, this money will really make a difference. I'm so proud of you!"
                    else:
                        mc.name "Actually, I don't have anything right now. Maybe next wek though, okay?"
                        the_person.char "Okay sweetheart, thanks for at least thinking about it."
                else:
                    $ mc.business.event_triggers_dict["Mom_Serum_Test"] = 1
                    mc.name "I have something you could help me with Mom."
                    the_person.char "What is it sweetheart? I'll do whatever I can for you."
                    mc.name "We have a little bit of a research bottleneck at work. I have something I'd like you to test for me."
                    the_person.char "Oh, okay. If it helps I can be your for hire test subject!"
                    mc.name "Excellent, let me just see if I have anything with me right now..."
                    call give_serum(the_person) from _call_give_serum_11
                    if _return:
                        $ mc.business.funds += -100
                        "You hand the serum to [the_person.possessive_title], followed by the cash."
                        the_person.char "Okay, so that's all for now?"
                        mc.name "That's all. I'll just be keeping an eye on you in the future, but you don't need to worry about that."
                        the_person.char "Well thank you sweetheart, this money will really make a difference. I'm so proud of you!"
                    else:
                        mc.name "Actually, I don't have anything right now. Maybe next wek though, okay?"
                        the_person.char "Okay sweetheart, thanks for at least thinking about it."


            "Nothing this week.":
                mc.name "Sorry Mom, but I'm tight on cash right now as well. Maybe next week, okay?"
                "[the_person.possessive_title] nods and turns back to her bills."
                the_person.char "I understand sweetheart. Now don't let me keep you, I'm sure you were up to something important."
                pass

            #TODO: pay her to fuck you.
            #TODO: pay her to change her wardrobe
            #TODO: pay her to do somehting with Lily.
            #TODO: have Lily start a cam show to make cash, then bring your Mom into it.


    $ mom_weekly_pay_action = Action("mom weekly pay", mom_weekly_pay_requirement, "mom_weekly_pay_label", args=mom, requirement_args =[mom])
    $ mc.business.mandatory_crises_list.append(mom_weekly_pay_action)
    return

label mom_offer_make_dinner_label(the_person):
    #TODO you offer to make dinner. It takes up time, but you can slip serum to your mom and sister.
    mc.name "You've been working youself so hard lately Mom, how about you let me make dinner tonight?"
    the_person.char "Oh [the_person.mc_title], that's such a sweet thing for you to offer!"
    $ the_person.change_happiness(5)
    $ the_person.change_obedience(-1)
    $ the_person.change_love(2)
    "[the_person.possessive_title] gives you a hug."
    the_person.char "Do you know where everything is?"
    mc.name "Yeah, I think I can take care of it."
    the_person.char "Well thank you, you're always such a help around here!"
    $ renpy.scene("Active")
    hide screen person_info_ui
    $ renpy.show(kitchen.name,what=kitchen.background_image)
    "You head to the kitchen and get to work. The cooking isn't hard, but it takes up most of your evening."
    "As you're plating out dinner you have a perfect opportunity to give your mother or sister some serum in secret."
    menu:
        "Add serum to Mom's food.":
            call give_serum(mom) from _call_give_serum_8

        "Leave Mom's food alone.":
            pass

    menu:
        "Add serum to [lily.name]'s food.":
            call give_serum(lily) from _call_give_serum_9

        "Leave [lily.name]'s food alone.":
            pass

    "You bring the food out and have a nice family dinner together."
    call advance_time from _call_advance_time_10
    return
