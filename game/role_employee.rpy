##########################################
# This file holds all of the role requirements and labels for the employee role.
##########################################

init -2 python:
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

#### EMPLOYEE ACTION LABELS ####

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
                the_person.char "Wow... this is amazing sir. I'll do everything I can for you and the company!"

    return

label employee_performance_review(the_person):
    $ the_person.event_triggers_dict["day_last_performance_review"] = day
    #Bring them into the office. (Set the background appropriately)
    mc.name "[the_person.title], I'd like to have a talk with you about your recent performance here at [mc.business.name]. Can you step inside my office for a moment?"
    if the_person.obedience > 100:
        the_person.char "Oh, of course sir."
    else:
        the_person.char "Uh, I guess. so."

    $ office.show_background()
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
                            the_person.char "Wait, I really need this job... What if I... let you use me. Just so you'll keep me around."
                            menu:
                                "Fuck her." if mc.current_stamina > 0:
                                    $ the_person.add_situational_slut("seduction_approach", -5, "I'm just a toy to him.")
                                    $ the_person.add_situational_obedience("seduction_approach", 25, "I'll do what I need to keep my job!")
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
