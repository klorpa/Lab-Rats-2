##########################################
# This file holds all of the role requirements and labels for the employee role.
##########################################

init -2 python:
    def employee_on_turn(the_person):
        #Each turn check to see if the person wants to quit.
        if mc.business.is_work_day():
            happy_points = the_person.get_job_happiness_score()
            if happy_points < 0: #We have a chance of quitting.
                chance_to_quit = happy_points * -2 #there is a %2*unhappiness chance that the girl will quit.
                if renpy.random.randint(0,100) < chance_to_quit: #She is quitting
                    potential_quit_action = Action(the_person.name + " is quitting.", quiting_crisis_requirement, "quitting_crisis_label", the_person)
                    if potential_quit_action not in mc.business.mandatory_crises_list:
                        mc.business.mandatory_crises_list.append(potential_quit_action)

                else: #She's not quitting, but we'll let the player know she's unhappy TODO: Only present this message with a certain research/policy.
                    warning_message = the_person.title + " (" +mc.business.get_employee_title(the_person) + ") " + " is unhappy with her job and is considering quitting."
                    if warning_message not in mc.business.message_list:
                        mc.business.add_normal_message(warning_message)
        return

    def employee_on_move(the_person):

        return

    def employee_on_day(the_person):
        if the_person.event_triggers_dict.get("forced_uniform", False) and day%7 == 6: #Reset uniforms over the weekend.
            the_person.event_triggers_dict["forced_uniform"] = None #TODO: Add a way to have special uniforms hang around for a specific amount of time.
        return



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
        elif day - the_person.event_triggers_dict.get("employed_since",-7) < 7:
            return "Too recently hired."
        elif day - the_person.event_triggers_dict.get("day_last_performance_review", -7) < 7:
            return "Just had a recent performance review."
        else:
            return True

    def move_employee_requirement(the_person):
        return True

    def employee_paid_serum_test_requirement(the_person):
        if mandatory_unpaid_serum_testing_policy.is_active():
            return False #Don't show anything if we have a higher level to show.
        elif not mandatory_paid_serum_testing_policy.is_active():
            return False #"Requires Policy: Mandatory Paid Serum Testing"
        elif mc.business.funds < 100:
            return "Requires: $100"
        else:
            return True

    def employee_unpaid_serum_test_requirement(the_person):
        if not mandatory_paid_serum_testing_policy.is_owned():
            return False #Don't show anything until the lower level is purchased.
        elif mandatory_paid_serum_testing_policy.is_owned() and not mandatory_unpaid_serum_testing_policy.is_active():
            return False #"Requires Policy: Mandatory Unpaid Serum Testing"
        else:
            return True

    def employee_punishment_hub_requirement(the_person):
        if not office_punishment.is_active():
            return False
        elif not mc.is_at_work():
            return False
        elif not mc.business.is_open_for_business():
            return False
        elif len(the_person.infractions) <= 0:
            return "Requires: Rules Infraction"
        elif the_person.event_triggers_dict.get("last_punished",-1) >= day:
            return "Already punished today"
        else:
            return True

    def employee_generate_infraction_requirement(the_person):
        if not bureaucratic_nightmare.is_active():
            return False
        elif not mc.is_at_work():
            return False
        elif not mc.business.is_open_for_business():
            return False
        else:
            return True


#### EMPLOYEE ACTION LABELS ####

label employee_complement_work(the_person):
    $ the_person.event_triggers_dict["day_last_employee_interaction"] = day
    if mc.business.get_employee_count == 1:
        mc.name "[the_person.title], I wanted to tell you that you've been doing a great job lately. Me and you make a great team, and I couldn't do all of this without you."
    else:
        mc.name "[the_person.title], I wanted to tell you that you've been doing a great job lately. Keep it up, you're one of the most important players in this whole operation."

    $ the_person.change_love(1)
    $ the_person.change_happiness(mc.charisma)
    the_person "Thanks [the_person.mc_title], it means a lot to hear that from you!"
    return

label insult_recent_work(the_person):
    $ the_person.event_triggers_dict["day_last_employee_interaction"] = day
    if mc.business.get_employee_count == 1:
        mc.name "I'm not sure what's going on with you lately, but I'm going to need you to try a little harder. It's only me and you here and you're really letting me down."
    else:
        mc.name "Honestly [the_person.title], I've been disappointed with your work lately and I really need you to try a little harder. You're letting the whole team down."
    if the_person.obedience >= 120:
        "She seems shocked for a second, then nods."
        the_person "I'm sorry. I'll try harder."
    else:
        the_person "What? I... I've been doing my best."
        mc.name "Well I'll need your best to be a little better if you want to justify what I'm paying you."
        $ the_person.draw_person(position = "sitting", emotion = "sad")
        "She scowls, but nods and doesn't object any more."
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
            the_person "Right, of course."

        "Give her a days wages. -$[the_person.salary]" if mc.business.funds >= the_person.salary:
            mc.name "Here you go, treat yourself to something nice tonight."
            $ the_person.draw_person(emotion = "happy")
            $ change_amount = 1+mc.charisma
            $ mc.business.funds -= the_person.salary
            $ the_person.change_happiness(change_amount)
            "[the_person.title] takes the bills from you and smiles."
            the_person "Thank you sir."


        "Give her a weeks wages. -$[weeks_wages]" if mc.business.funds >= weeks_wages:
            mc.name "Here you go, don't spend it all in once place."
            $ the_person.draw_person(emotion = "happy")
            $ change_amount = 1+mc.charisma
            $ change_amount_happiness = 5+mc.charisma
            $ the_person.change_happiness(change_amount_happiness)
            $ the_person.change_obedience(change_amount)
            $ mc.business.funds -= weeks_wages
            "[the_person.title] takes the bills, then smiles broadly at you."
            the_person "That's very generous of you sir, thank you."

        "Give her a months wages. -$[months_wages]" if mc.business.funds >= months_wages:
            mc.name "Here, you're a key part of the team and you deserved to be rewarded as such."
            $ the_person.draw_person(emotion = "happy")
            $ change_amount = 5+mc.charisma
            $ change_amount_happiness = 10+mc.charisma
            $ the_person.change_happiness(change_amount_happiness)
            $ the_person.change_obedience(change_amount)
            $ mc.business.funds -= months_wages
            "[the_person.title] takes the bills, momentarily stunned by the amount."
            if the_person.effective_sluttiness() > 40 and the_person.happiness > 100:
                the_person "Wow... this is amazing sir. I'm sure there's something I can do to pay you back, right?"
                "She steps close to you and runs a finger down your chest."
                $ the_person.add_situational_slut("situation", 10, "He's given me such a generous bonus, I should repay the favour!")
                call fuck_person(the_person) from _call_fuck_person_3
                #Now that you've had sex, we calculate the change to her stats and move on.
                $ the_person.clear_situational_slut("situation")
                $ the_person.review_outfit()
            else:
                the_person "Wow... this is amazing sir. I'll do everything I can for you and the company!"

    return

label employee_performance_review(the_person):
    $ the_person.event_triggers_dict["day_last_performance_review"] = day
    #Bring them into the office. (Set the background appropriately)
    mc.name "[the_person.title], I'd like to have a talk with you about your recent performance here at [mc.business.name]. Can you step inside my office for a moment?"
    if the_person.obedience > 100:
        the_person "Oh, of course sir."
    else:
        the_person "Uh, I guess. so."

    $ office.show_background()
    $ mc.location.move_person(the_person, office)

    "You lead [the_person.title] into your office and close the door behing her. You take your seat at your desk and motion to a chair opposite you."
    $ the_person.draw_person(position = "sitting")
    mc.name "So [the_person.title], tell me what you think about your job."

    if the_person.get_job_happiness_score() > 0:
        #She's happy enough with the job to stay here
        if the_person.salary > the_person.calculate_base_salary() + 15: #She's very overpaid
            the_person "It's a fantastic position and I'm lucky to have it! There aren't very many places that would be able to pay me as well as I am here."
        elif the_person.salary > the_person.calculate_base_salary() + 3: #She's reasonably over paid.
            the_person "It's a great job. The pay is great and the work is interesting."
        elif the_person.salary > the_person.calculate_base_salary() - 3: #She's reasonably paid.
            the_person "I really like my job. I feel like I can come in every day and do an honest day's work."
        else:
            the_person "The pay isn't the greatest, but the work environment really makes up for it. It's a joy to be working here."

    else: #She's thinking about quitting.
        if the_person.salary > the_person.calculate_base_salary() + 15: #She's very overpaid
            the_person "The pay is amazing, but the work environment here is just terrible. I honestly don't know how much longer I can take it."
        elif the_person.salary > the_person.calculate_base_salary() + 3: #She's reasonably over paid.
            the_person "I know you're paying me very well, but the work here is terrible. I hope you have some plans to make things better."
        elif the_person.salary > the_person.calculate_base_salary() - 3: #She's reasonably paid.
            the_person "Things could be better. I'd like it if the conditions here at work were improved a little bit, or I could be paid a little bit more."
        else:
            the_person "I don't really have anything positive to say. The pay isn't great and it isn't exactly the most pleasant work environment."

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
                    the_person "That sounds amazing! Thank you sir, I promise I won't let you down!"
                    mc.name "Good to hear it."

                "Reward her sexually." if the_person.effective_sluttiness() >= 40: #At high sluttiness you can make her cum to make her even happier with her job.
                    mc.name "You do a lot of work for the company, and I know how stressful your job can be at times."
                    "You get up from your desk and move around to the other side. You step behind [the_person.title] and place your hands on her shoulders, rubbing them gently."
                    mc.name "I'd like to do something for you to help you relax. How does that sound for a bonus?"
                    $ the_person.add_situational_slut("seduction_approach", 15, "It's all about me!")
                    $ the_person.add_situational_obedience("seduction_approach", -20, "It's all about me!")
                    the_person "Oh [the_person.mc_title], that sounds like a great idea..."
                    call fuck_person(the_person,private = True) from _call_fuck_person_11
                    $ the_report = _return
                    $ the_person.clear_situational_slut("seduction_approach")
                    $ the_person.clear_situational_obedience("seduction_approach")
                    if the_report.get("girl orgasms", 0) > 0: #We made her cum! Congradulations!
                        $ the_person.change_happiness(20)
                        $ the_person.change_slut_temp(5)
                        $ the_person.change_love(2)
                        the_person "Oh [the_person.mc_title], that was wonderful! I couldn't have asked for a better performance bonus!"
                    elif the_report.get("guy orgasms", 0) > 0: # You "rewarded" her by cumming and leaving her unsatisfied. Not particularly impressive.
                        $ the_person.change_happiness(-5)
                        $ the_person.change_obedience(-2)
                        the_person "It's not much of a bonus if you're the only one who gets to cum. Maybe next time a cash bonus would be better, okay?"
                    else: #She didn't cum, but neither did you so maybe you were just both tired
                        $ the_person.change_happiness(5)
                        $ the_person.change_slut_temp(2)
                        the_person "Well, that was a good time [the_person.mc_title]. It's a lot more fun than a normal performance bonus, that's for sure!"

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
                    $ the_person.change_happiness(-(15-mc.charisma))
                    $ the_person.change_obedience(-(8-mc.charisma))
                    if the_person.get_job_happiness_score() > 0:
                        $ the_person.draw_person(position = "sitting", emotion = "sad")
                        the_person "I... I understand."
                    elif the_person.get_job_happiness_score() > -25:
                        $ the_person.draw_person(position = "sitting", emotion = "angry")
                        the_person "What? I... I don't know what to say!"
                        mc.name "Like I said, I'm sorry but it has to be done."
                    else: #She's so unhappy with her job she quits.
                        $ the_person.draw_person(position = "sitting", emotion = "angry")
                        the_person "What? I... I can't believe that [the_person.mc_title], why would you ever think I would stay here for less money?"
                        mc.name "Like I said, I'm sorry but it has to be done."
                        the_person "Well you know what, I think I'm just going to find somewhere else to work. I quit."
                        $ clear_scene()
                        "[the_person.title] stands up and storms out."
                        $ mc.business.remove_employee(the_person)
                        call advance_time from _call_advance_time_12
                        return #Don't use the normal "show her out" ending stuff. The scene ends here.

                "Threaten to fire her.": #She may ask to stay in exchange for some sort of favour, or get fired on the spot.
                    mc.name "I'll be honest with you [the_person.title], your performance here at [mc.business.name] leaves a lot to be desired."
                    mc.name "I've been running the numbers and I think we'd be better off without you. Unless you can convince me otherwise I'm going to have to let you go."
                    if the_person.get_job_happiness_score() > -10:
                        if the_person.effective_sluttiness() < 20:
                            the_person "No sir, I really need this job. What if I took a pay cut? Would that be enough?"
                            menu:
                                "Cut her pay. (-$[cut_amount]/day)":
                                    mc.name "If you're willing to take a pay cut I think I can keep you around and see if your performance improves."
                                    $ the_person.change_salary(-cut_amount)
                                    $ the_person.change_happiness(10)
                                    $ the_person.change_obedience(5)
                                    the_person "Thank you sir! Thank you so much!"

                                "Fire her.":
                                    mc.name "I'm sorry, but that wouldn't be enough."
                                    the_person "I understand. I'll clear out my desk."
                                    $ the_person.change_happiness(-10)
                                    $ the_person.change_obedience(-5)
                                    $ mc.business.remove_employee(the_person)
                        else:
                            if the_person.effective_sluttiness() < 30: #Willing to show her tits.
                                the_person "Wait, I really need this job! There must be something about me that's worth keeping around."
                                the_person "Just tell me what it is and I'll show it to you..."
                            elif the_person.effective_sluttiness() < 45: #Willing to suck you off, jerk you off.
                                the_person "I can be very convincing [the_person.mc_title]."
                                the_person "Just tell me what I need to do and I'll do it."
                            elif the_person.effective_sluttiness() < 60: #Willing to fuck you
                                the_person "I don't think my value here is really captured by performance quotas... Let me remind you why you really keep me around."
                            else:
                                the_person "I'm not just here for the job though, I'm here for you [the_person.mc_title]."
                                the_person "What do I need to do to convince you to keep me around? I'll do anything at all for you."

                            $ jerk_token = get_red_heart(30)
                            $ blowjob_token = get_red_heart(45)
                            $ fuck_token = get_red_heart(60)
                            menu:
                                "Make her strip.":
                                    mc.name "Fine, I'll reconsider. In exchange, I want you to strip for me."
                                    if the_person.has_taboo("underwear_nudity"):
                                        the_person "[the_person.mc_title], is that really what it's going to take?"
                                        mc.name "It's the only chance you've got right now. Hurry up, I don't have all day and I'm running out of patience."
                                        $ the_person.change_love(-1)
                                        $ the_person.change_obedience(2+the_person.get_opinion_score("being submissive"))
                                        "She takes a deep breath, then begins to undress."
                                    else:
                                        the_person "Well, if that's what it's goign to take I guess I have no choice..."
                                        $ the_person.change_obedience(1)

                                    $ strip_list = the_person.outfit.get_underwear_strip_list()
                                    $ generalised_strip_description(the_person, strip_list)
                                    if the_person.has_taboo("underwear_nudity") or (the_person.has_taboo("bare_pussy") and the_person.outfit.vagina_visible()) or (the_person.has_taboo("bare_tits") and the_person.outfit.tits_visible()):
                                        the_person "Is this what you wanted to see? Are we done?"
                                        "[the_person.title] tries to cover herself up with her hands, shuffling nervously in front of your desk."
                                    else: #No taboo broken, no big deal
                                        the_person "Is this what you wanted to see [the_person.mc_title]? I hope it's worth keeping me around..."

                                    if not (the_person.outfit.vagina_visible() and the_person.outfit.tits_visible()):
                                        menu:
                                            "Make her strip naked." if the_person.obedience > 110:
                                                mc.name "You aren't finished yet. Keep stripping, I want to see you naked."
                                                $ remove_shoes = False
                                                $ feet_ordered = the_person.outfit.get_feet_ordered()
                                                if feet_ordered:
                                                    $ top_feet = feet_ordered[-1]
                                                    the_person "Do you want me to keep my [top_feet.display_name] on?"
                                                    menu:
                                                        "Strip it all off.":
                                                            mc.name "Take it all off, I don't want you to be wearing anything."
                                                            $ remove_shoes = True

                                                        "Leave them on.":
                                                            mc.name "You can leave them on."

                                                if the_person.has_taboo(["bare_pussy", "bare_tits"]):
                                                    the_person "I... I'm not sure [the_person.mc_title]."
                                                    mc.name "I'm not going to bother asking twice."
                                                    the_person "Fine! I'll do it..."
                                                else:
                                                    "She nods obediently."
                                                    the_person "Yes [the_person.mc_title], whatever you want."

                                                $ strip_list = the_person.outfit.get_full_strip_list(strip_feet = remove_shoes)
                                                $ generalised_strip_description(the_person, strip_list)

                                            "Make her strip naked.\n{size=16}{color=#FF0000}Requires: 110 Obedience{/size}{/color} (disabled)" if the_person.obedience < 110:
                                                pass

                                            "Move on.":
                                                pass

                                    if the_person.update_outfit_taboos():
                                        the_person "Are... Are we done now? Can I get dressed?"
                                        mc.name "Not yet. Turn around, I want to get a look at your ass."
                                        mc.name "And stop trying to cover yourself up. The point is for me to look at you, right?"
                                        $ the_person.draw_person(position = "back_peek")
                                        "[the_person.possessive_title] reluctantly follows your instructions, letting her hands drop to her sides and turning around."
                                        "She stands rigidly at first, but as the seconds tick by silently seems to grow more comfortable."
                                    else:
                                        the_person "Well, now what?"
                                        the_person "Turn around, let me take a look at your ass."
                                        $ the_person.draw_person(position = "back_peek", the_animation = ass_bob, animation_effect_strength = 0.4)
                                        "[the_person.possessive_title] obediently follows your instructions. She bounces her hips, jiggling her butt as you oggle her."

                                    mc.name "Okay, that's enough."
                                    $ the_person.draw_person()
                                    the_person "So... I'm not being fired?"
                                    "You shake your head."
                                    mc.name "Not today, at least. I expect to see improvements, or we'll be back here and I won't be so understanding."
                                    $ the_person.change_happiness(-5 + (the_person.get_opinion_score("showing her tits") + the_person.get_opinion_score("showing her ass")))
                                    $ the_person.change_obedience(3 + 3*the_person.get_opinion_score("being submissive"))
                                    $ the_person.change_slut_temp(1)
                                    the_person "Understood. I'll be doing next time, I promise!"
                                    "[the_person.possessive_title] collects her clothing and gets dressed."
                                    $ the_person.apply_outfit()
                                    $ the_person.draw_person()

                                "Make her jerk you off." if the_person.effective_sluttiness() >= 30:
                                    "You nod thoughtfully, then roll your office chair back away from your desk."
                                    mc.name "Alright then, I'll make you a deal."
                                    the_person "Thank you [the_person.mc_title]! What do I need to do?"
                                    "You unzip your pants and pull out your half-hard cock."
                                    mc.name "I want you to jerk me off. I should be getting something for my money, right?"
                                    if the_person.has_taboo("touching_penis"):
                                        the_person "You want me to give you a... handjob?"
                                        "[the_person.possessive_title] seems unsure, but she takes a few shakey steps towards you."
                                        the_person "And if I do this you won't fire me?"
                                        mc.name "That's the deal. Come on, it doesn't bite."
                                    else:
                                        the_person "I give you a handjob and you won't fire me?"
                                        "She walks to your side of the desk, eyes fixed on your cock."
                                        mc.name "That's the deal. It doesn't seem too hard, does it?"
                                        the_person "Oh, that looks plenty hard... Fine, I'll do it."

                                    #TODO: We really need a sitting and kneeling handjob pose.
                                    "[the_person.possessive_title] kneels down in front of you and reaches out, gently wrapping her fingers around your shaft."
                                    if the_person.break_taboo("touching_penis"):
                                        "She gasps when your cock twitches in response."
                                        mc.name "Relax, just do what comes naturally. A woman like you should know what to do with a cock in her hand."

                                    else:
                                        "She laughs when your cock twitches in response."
                                        the_person "Oh my god, happy to see me little guy?"
                                        mc.name "Hey, it's not that little."
                                        the_person "It's certainly not..."

                                    "[the_person.title] starts to stroke it, rhythmically running her hand up and down your length."
                                    call fuck_person(the_person, private = True, start_position = handjob, girl_in_charge = True, skip_intro = True, position_locked = True) from _call_fuck_person_12
                                    $ the_report = _return
                                    "[the_person.possessive_title] sits back and rubs her arm."
                                    if the_report.get("guy orgasms", 0) > 0:
                                        the_person "Whew, that's an arm workout!"
                                        the_person "So... We have an understanding?"
                                        mc.name "For now. If your performance doesn't improve you're going to have to work even harder to convince me."
                                        the_person "It won't happen again, I promise!"

                                    else:
                                        the_person "I can't do it [the_person.mc_title]... I tried, I swear I tried!"
                                        if office_punishment.is_active():
                                            mc.name "You did try. I'll be lenient and just write this up as a rules infraction."
                                            $ the_person.add_infraction(Infraction.underperformance_factory())
                                            the_person "Thank you [the_person.mc_name]. I'll do better next time."

                                        else:
                                            mc.name "You did, that's true. I'll be generous this time, but you better be prepared to finish me next time."
                                            the_person "Next time? I mean, of course [the_person.mc_title]."
                                    $ the_person.change_happiness(-5 + (2*the_person.get_opinion_score("giving handjobs")))
                                    $ the_person.change_obedience(3 + the_person.get_opinion_score("being submissive"))
                                    $ the_person.change_slut_temp(2 + the_person.get_opinion_score("giving handjobs"))
                                    $ the_person.draw_person()
                                    $ the_person.review_outfit()

                                "Make her jerk you off.\nRequires: [jerk_token] (disabled)" if the_person.effective_sluttiness() < 30:
                                    pass

                                "Make her blow you." if the_person.effective_sluttiness() >= 45:
                                    "You nod thoughtfully, then roll your office chair back away from your desk."
                                    mc.name "Alright then, I'll make you a deal."
                                    the_person "Thank you [the_person.mc_title]! What do I need to do?"
                                    "You unzip your pants and pull out your hardening cock."
                                    mc.name "I want you to suck me off. Do a good job and I'll let you keep your job."
                                    if the_person.has_taboo("sucking_cock"):
                                        the_person "You want a blowjob?"
                                        mc.name "Yeah, I do. You know how to give one, right?"
                                        the_person "Of course! I just wasn't expecting... Well, I don't know what I was expecting."
                                        "You motion her closer, and she takes a few unsteady steps."
                                        mc.name "Get on your knees. Don't worry, it doesn't bite."
                                        "[the_person.possessive_title] nods and drops down in front of you."
                                        $ the_person.break_taboo("sucking_cock")
                                    else:
                                        the_person "A blowjob? Well, I guess that's not so bad..."
                                        "She takes a few steps closer."
                                        mc.name "Get on your knees, I'm getting a little impatient."
                                        $ the_person.draw_person(position = "kneeling1")
                                        "[the_person.possessive_title] nods and drops down in front of you."

                                    the_person "Just... a blowjob, right?"
                                    mc.name "To start with, at least."

                                    "You present your cock, and she leans forward to take it in her mouth."
                                    "She sucks on the tip for a few moments, then slides you deeper into her mouth."

                                    if the_person.get_opinion_score("being submissive") > 0:
                                        $ the_person.add_situational_slut("seduction_approach", 5*the_person.get_opinion_score("being submissive"), "He's using me just like a toy!")
                                    else:
                                        $ the_person.add_situational_slut("seduction_approach", -5 + (-5*the_person.get_opinion_score("being submissive")), "I'm just a toy to him.")
                                    $ the_person.add_situational_obedience("seduction_approach", 10, "I'll do what I need to keep my job!")
                                    call fuck_person(the_person,private = True, start_position = blowjob) from _call_fuck_person_105
                                    $ the_person.clear_situational_slut("seduction_approach")
                                    $ the_person.clear_situational_obedience("seduction_approach")
                                    $ the_person.review_outfit()

                                    $ the_person.change_obedience(5)
                                    $ the_person.change_slut_temp(3)
                                    $ the_person.change_happiness(-5)
                                    mc.name "Okay [the_person.title], I'll keep you around for a little while longer, but you're going to need to shape up unless you want this to be a regular occurrence."
                                    if the_person.effective_sluttiness() < 50:
                                        the_person "I'll do my best sir, I promise."
                                    else:
                                        the_person "Would that really be such a bad thing?"


                                "Make her blow you.\nRequires: [blowjob_token] (disabled)" if the_person.effective_sluttiness() < 45:
                                    pass

                                "Fuck her."  if the_person.effective_sluttiness() >= 60:
                                    mc.name "Is that so? Alright, first things first then. Get naked."
                                    "[the_person.possessive_title] doesn't seem to have any problem with the command."
                                    $ remove_shoes = False
                                    $ feet_ordered = the_person.outfit.get_feet_ordered()
                                    if feet_ordered:
                                        $ top_feet = feet_ordered[-1]
                                        the_person "Do you want me to keep my [top_feet.display_name] on?"
                                        menu:
                                            "Strip it all off.":
                                                mc.name "Take it all off, I don't want you to be wearing anything."
                                                $ remove_shoes = True

                                            "Leave them on.":
                                                mc.name "You can leave them on."

                                    "She nods obediently."
                                    the_person "Yes [the_person.mc_title], whatever you want."

                                    $ strip_list = the_person.outfit.get_full_strip_list(strip_feet = remove_shoes)
                                    $ generalised_strip_description(the_person, strip_list)
                                    the_person "Now what?"
                                    "You slide your chair back from your desk and stand up."
                                    mc.name "Now let's see just how committed you are to this job."
                                    "You walk around to her side of the desk and pat the edge."
                                    mc.name "Put your hands here. Keep your legs straight."
                                    $ the_person.draw_person("standing_doggy")
                                    "She follows your instructions obediently, bending over to plant her palms on your desk."
                                    the_person "What are you going to do?"
                                    "You walk behind [the_person.title] and unzip your pants. When you pull them down your hard cock springs out and bounces against an ass cheek."
                                    mc.name "I'm going to fuck you. That's not a problem, is it?"
                                    "You hold your shaft and rub the tip of your cock between her legs."
                                    if the_person.wants_condom():
                                        the_person "Wait, wait! If you're going to fuck me... you need to wear a condom!"
                                        menu:
                                            "Put on a condom.":
                                                mc.name "Fine, but I'm going to have to really lay into you so I can feel anything."
                                                the_person "Thank you [the_person.mc_title]."
                                                "You drag your tip teasingly across the slit of her pussy, then step back and pull a condom out of your wallet."
                                                $ mc.condom = True
                                                "You spread it over your dick, then step into position and line yourself up."

                                            "Fuck her raw anyways." if the_person.obedience >= 130:
                                                mc.name "That's where you draw the line? You'll fuck your boss to keep your job, but you need a tiny bit of latex?"
                                                mc.name "No, I'm going to feel that hot pussy wrapped around my cock raw."
                                                if not the_person.on_birth_control:
                                                    the_person "I'm not on the pill [the_person.mc_title]..."
                                                    $ the_person.update_birth_control_knowledge()
                                                    mc.name "Well then, you've got a choice."
                                                    mc.name "You can walk out of this room unemployeed, or you can walk out of this room pregnant."
                                                    "You drag the tip teasingly across the lips of her pussy while she thinks."

                                                else:
                                                    the_person "[the_person.mc_title], I really shouldn't..."
                                                    mc.name "You've got two choices [the_person.title]."
                                                    mc.name "You can walk out of this room unemployeed, or you can walk out with a pussy full of my cum."
                                                    "You tap the tip of your cock on her clit, teasing her while she thinks."
                                                the_person "... Fine... Just this once."
                                                $ the_person.change_obedience(1 + the_person.get_opinion_score("being submissive"))
                                                mc.name "Good girl, that's what I like to hear."
                                                "You hold your shaft steady with one hand and line yourself up with her."

                                            "Fuck her raw anyways.\nRequires: 130 Obedience (disabled)" if the_person.obedience < 130:
                                                pass

                                    else: #She doesn't want one, but we'll give you the option in case you're trying not to get girls pregnant.
                                        the_person "No [the_person.mc_title], no problem..."
                                        menu:
                                            "Put on a condom.":
                                                mc.name "Of course, I need to put a condom on first."
                                                mc.name "I wouldn't want any accidents showing up nine months from now."
                                                "You step back and pull a condom out of your wallet. After a moment of fumbling you have it spread over your dick."
                                                "You hold your shaft with one hand and step close to [the_person.possessive_title] again, teasing the lips of her pussy with your tip."
                                                $ mc.condom = True

                                            "Fuck her raw.":
                                                pass

                                    "You push forward, plunging your hard dick into [the_person.title]'s tight cunt. She gasps softly under her breath."
                                    "You hold yourself deep inside of her and enjoy the sudden warmth around your shaft."
                                    "When you think she's ready you pull your hips back and start to pump in and out of her."

                                    if the_person.get_opinion_score("being submissive") > 0:
                                        $ the_person.add_situational_slut("seduction_approach", 5*the_person.get_opinion_score("being submissive"), "He's using me just like a toy!")
                                    else:
                                        $ the_person.add_situational_slut("seduction_approach", -5 + (-5*the_person.get_opinion_score("being submissive")), "I'm just a toy to him.")
                                    $ the_person.add_situational_obedience("seduction_approach", 25, "I'll do what I need to keep my job!")
                                    call fuck_person(the_person,private = True, start_position = doggy, skip_condom = True) from _call_fuck_person_106
                                    $ the_person.clear_situational_slut("seduction_approach")
                                    $ the_person.clear_situational_obedience("seduction_approach")
                                    $ the_person.review_outfit()

                                    $ the_person.change_obedience(10)
                                    $ the_person.change_slut_temp(4)
                                    $ the_person.change_happiness(-5)
                                    mc.name "Okay [the_person.title], I'll keep you around for a little while longer, but you're going to need to shape up unless you want this to be a regular occurrence."
                                    if the_person.effective_sluttiness() < 50:
                                        the_person "I'll do my best sir, I promise."
                                    else:
                                        the_person "Would that really be such a bad thing?"


                                "Fuck her.\nRequires: [fuck_token] (disabled)" if the_person.effective_sluttiness() < 60:
                                    pass

                                "Fire her.":
                                    mc.name "I'm sorry, but I don't think there's anything you can do to convince me."
                                    mc.name "Collect your things and get out."
                                    "[the_person.possessive_title] seems slightly stunned, but nods and leaves without any more complaints."
                                    $ the_person.change_happiness(-10)
                                    $ the_person.change_obedience(-5)
                                    $ mc.business.remove_employee(the_person)


                    else:
                        $ the_person.draw_person(position = "sitting", emotion = "angry")
                        the_person "What? You want me to beg to stay at this shitty job? If you don't want me here I think it's best I just move on. I quit!"
                        $ clear_scene()
                        "[the_person.title] stands up and storms out."
                        $ mc.business.remove_employee(the_person)
                        call advance_time from _call_advance_time_13
                        return


                "Punish her sexually." if the_person.effective_sluttiness() >= 40 and the_person.obedience >= 120: #Orgasm denial and/or make her service you.
                    "You sigh dramatically and stand up from your desk. You walk over to the other side and sit on the corner nearest [the_person.title]."
                    mc.name "Your performance has really let me down, but I think what you need a little motivation."
                    mc.name "I want to have some fun with you, but you're not allowed to climax, is that understood?"
                    $ opinion_modifier = the_person.get_opinion_score("being submissive")*5
                    $ the_person.add_situational_slut("seduction_approach", -5+opinion_modifier, "I'm just being used...")
                    $ the_person.add_situational_obedience("seduction_approach", 15+opinion_modifier, "I'm being punished")
                    the_person "I... if you think this is what I need, sir."
                    call fuck_person(the_person,private = True) from _call_fuck_person_13
                    $ the_report = _return
                    $ the_person.clear_situational_slut("seduction_approach")
                    $ the_person.clear_situational_obedience("seduction_approach")
                    if the_report.get("girl orgasms", 0) > 0: #We made her cum! Congradulations!
                        $ the_person.change_happiness(5)
                        $ the_person.change_obedience(-10)
                        the_person "You just can't resist pleasing me, can you [the_person.mc_title]? I thought I wasn't suppose to cum?"
                        "[the_person.title] seems smug about her orgasmic victory."

                    elif the_report.get("end arousal", 0) >= 80:
                        $ the_person.change_happiness(5)
                        $ the_person.change_slut_temp(5)
                        $ the_person.change_obedience(5)
                        the_person "Oh my god [the_person.mc_title], you got me so close... Can't you just finish me off, real quick?"
                        mc.name "Do a better job and I'll let you cum next time. Understood?"
                        "[the_person.title] nods meekly."
                    else:
                        $ the_person.change_happiness(-5)
                        $ the_person.change_obedience(10)
                        mc.name "That felt great [the_person.title], I suppose if your performance doesn't improve you'll still be useful as a toy."
                        the_person "I... Yes sir, I suppose I would be."

                    $ the_person.review_outfit()

                "Record an infraction." if office_punishment.is_active():
                    mc.name "Your performance lately has been less than stellar. I hope the problem is simply a matter of discipline, which we can correct."
                    mc.name "I'm going to take some time to think about what punishment would be suitable."
                    $ the_person.add_infraction(Infraction.underperformance_factory())
                    if the_person.get_job_happiness_score() > 0:
                        the_person "I can improve [the_person.mc_title], I promise."

                    else:
                        the_person "I... Fine, I understand."
                    mc.name "Good to hear it."


        "Finish the performance review.":
            mc.name "Well, I think you're doing a perfectly adequate job around here [the_person.title]. If you keep up the good work I don't think we will have any issues."
            $ the_person.change_obedience(1)
            $ the_person.change_happiness(2)
            the_person "Thank you, I'll do my best."

    "You stand up and open the door for [the_person.title] at the end of her performance review."
    $ clear_scene()
    call advance_time from _call_advance_time_14
    return

label move_employee_label(the_person):
    if the_person == mc.business.head_researcher:
        "Moving [the_person.title] will remove her from her role as head researcher. Are you sure you want to move [the_person.title]?"
        menu:
            "Yes, move [the_person.title]":
                pass
            "No, leave [the_person.title]":
                $ clear_scene()
                return

    the_person "Where would you like me then?"
    $ mc.business.remove_employee(the_person, remove_linked = False)
    $ the_person.add_role(employee_role) #Remove_employee strips them of their workplace roles. We want to make sure we add it back.
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
            $ the_person.set_work(mc.business.r_div) #TODO: This should reference the business r_div, p_div, etc. not the actual rooms.

        "Production.":
            $ mc.business.add_employee_production(the_person)
            $ mc.business.p_div.add_person(the_person)
            $ the_person.set_work(mc.business.p_div)

        "Supply Procurement.":
            $ mc.business.add_employee_supply(the_person)
            $ mc.business.s_div.add_person(the_person)
            $ the_person.set_work(mc.business.s_div)

        "Marketing.":
            $ mc.business.add_employee_marketing(the_person)
            $ mc.business.m_div.add_person(the_person)
            $ the_person.set_work(mc.business.m_div)

        "Human Resources.":
            $ mc.business.add_employee_hr(the_person)
            $ mc.business.h_div.add_person(the_person)
            $ the_person.set_work(mc.business.h_div)

    the_person "I'll move over there right away!"
    return

label employee_paid_serum_test_label(the_person):
    $ pay_serum_cost = 100
    mc.name "[the_person.title], we're running field trials and you're one of the test subjects. I'm going to need you to take this, a bonus will be added onto your paycheck."
    call give_serum(the_person) from _call_give_serum_18
    if _return:
        $ mc.business.funds += -pay_serum_cost
    return

label employee_unpaid_serum_test_label(the_person):
    mc.name "[the_person.title], we're running field trials and you're one of the test subjects. I'm going to need you to take this."
    call give_serum(the_person) from _call_give_serum_19
    return

label employee_punishment_hub(the_person):
    python:
        infraction_list = []
        for infraction in the_person.infractions:
            infraction_list.append([infraction.name + "\n{size=16}Severity " + str(infraction.severity) + ", Valid for " + str(infraction.days_valid - infraction.days_existed) + " days{/size} (tooltip)" + infraction.desc, infraction])

        infraction_list.append(["Return", "Return"])

    $ selected_infraction = renpy.display_menu(infraction_list,True,"Choice")
    if selected_infraction == "Return":
        return

    $ valid_punishments = ["Available Punishments"]
    $ invalid_punishments = ["Locked Punishments"]
    $ other_actions = ["Other Actions","Back"]

    python:
        for punishment in list_of_punishments:
            if punishment.is_action_enabled([the_person, selected_infraction]):
                valid_punishments.append([punishment,[the_person, selected_infraction]]) # This list is broken down by the menu function, the nested list are extra arguments so it can check which buttons are enabled.
            else:
                invalid_punishments.append([punishment,[the_person, selected_infraction]])

    call screen main_choice_display([valid_punishments, invalid_punishments, other_actions])
    $ selected_option = _return
    $ valid_punishments = None
    $ invalid_punishments = None
    $ other_actions = None
    if selected_option == "Back":
        call employee_punishment_hub(the_person) from _call_employee_punishment_hub
    else:
        $ selected_option.call_action([the_person, selected_infraction])
        $ the_person.remove_infraction(selected_infraction)
        $ happiness_drop = -2*(selected_infraction.severity - the_person.get_opinion_score("being submissive"))
        if happiness_drop < 0:
            $ happiness_drop = 0
        $ the_person.change_happiness(happiness_drop)
        $ the_person.event_triggers_dict["last_punished"] = day
    return

label employee_generate_infraction_label(the_person):
    mc.name "[the_person.title], I was reviewing your work and I've found some discrepancies."
    the_person "Oh, I'm sorry [the_person.mc_title], I..."
    mc.name "Unfortunately company policy requires I write you up for it. Don't worry, everyone makes mistakes."
    $ the_person.change_happiness(-5)
    "She frowns, but nods obediently."
    $ the_person.add_infraction(Infraction.bureaucratic_mistake_factory())
    return
