# All info related to the "Student" role

#Plan:
# 1) On your second(ish) visit to Nora you run into one of her students talking to Nora. Nora hurries her out.
# 1a) Add a way to connect with Nora even if you don't accept her help on serum. (ie. without Steph either)
# 2) Student needs help with class. Next time you visit she talks to you instead, asking "I know you've worked with Professor blah. Maybe you could help me."
# 3) Help the student study for Nora's classes, raising Love each time. Convince her to take serum to make her smarter.
# 4) Nora notices her student is doing better and mentions she's having trouble with her lectures. She "Can't keep the attention of the class."
# 5) Convince Nora she needs to "put on more of a show", starting with sexier outfits. Eventually have Nora letting students fuck her as a reward for doing well.
# 6) Convince student to try more and more slutty things as either a reward or punishment for her performance.

init -2 python:
    def student_intro_two_requirement(the_person):
        if not the_person in university.people:
            return False
        return True

    def student_reintro_requirement(the_person):
        if not the_person.event_triggers_dict.get("student_reintro_required", False):
            return False

        return True

    def student_study_propose_requirement(the_person):
        if not the_person.event_triggers_dict.get("tutor_enabled", False):
            return False
        elif not ((the_person in university.people and the_person.event_triggers_dict.get("tutor_enabled", False)) or (the_person.event_triggers_dict.get("home_tutor_enabled", False) and the_person in the_person.home.people)):
            return False
        elif ((the_person in university.people and the_person.event_triggers_dict.get("tutor_enabled, False")) or (the_person.event_triggers_dict.get("home_tutor_enabled", False) and the_person in the_person.home.people)) and the_person.event_triggers_dict.get("last_tutor", -5) >= day:
            return "Already studied today."
        return True

    def student_mom_intro_requirement(the_person):
        if not the_person in the_person.home.people:
            return False
        elif not emily.event_triggers_dict.get("home_tutor_enabled", False):
            return False
        return True



label student_intro_one(the_nora, the_student): #the_nora just because we don't want to conflict with the global Nora name.
    "You knock on the door to the lab. After a moment [the_nora.title] answers and steps out into the hallway."
    $ the_nora.draw_person()
    the_nora.char "Hello, I'm glad you were able to make it. Come on, let's..."
    the_student.char "Professor [the_nora.last_name]!"
    "Your conversation is interrupted by a girl hurrying down the hallway towards you. [the_nora.title] sighs."
    the_nora.char "Sorry, this will just take a moment."
    $ the_student.draw_person()
    the_student.char "Professor, I'm glad I was able to catch you, I..."
    $ the_nora.draw_person()
    $ the_student.set_title(the_student.name)
    $ the_student.set_possessive_title(the_student.name)
    the_nora.char "[the_student.title], you know I'm not allowed to have students in my lab."
    $ the_student.draw_person()
    the_student.char "I know, which is why I was hoping I could talk to you here. There are a few questions I'm really struggling with on..."
    $ the_nora.draw_person()
    the_nora.char "Okay, but I'm with a colleague of mine right now. I will be back in a few minutes."
    $ the_student.draw_person()
    the_student.char "Thank you Professor."
    "She turns to you and smiles."
    the_student.char "Sorry for the interruption."
    mc.name "No problem at all."
    $ the_nora.draw_person()
    $ university.show_background()
    "[the_nora.title] leads you upstairs to make sure none of her co-workers are around."
    the_nora.char "Sorry about that. The university requires me to teach at least one class in order to recieve grant money."
    the_nora.char "Now I've got undergrads hounding me every hour of the day asking for help on this or an extension on that."
    the_nora.char "All they have to do is show up and pay attention, but somehow half of them can't even manage that."
    "She gives an exhausted sigh."
    the_nora.char "But never mind that, we have more important things to discuss."

    python: #Sets up all the variables needed for this story line.
        student_intro_two_action = Action("Student_intro_two", student_intro_two_requirement, "student_intro_two")
        the_student.on_room_enter_event_list.append(student_intro_two_action)
        the_student.special_role.append(student_role)
        the_student.event_triggers_dict["current_marks"] = 25 # Should be a value between 0 and 100%
    return


label student_intro_two(the_person):
    the_person.char "Um, excuse me. I don't mean to interrupt you, but do you have a moment?"
    $ the_person.draw_person()
    "You hear a voice behind you as you're walking across campus. When you turn around you recognise the same student [nora.title] was talking to on your last visit."
    mc.name "Sure, how can I help you?"
    the_person.char "You work with Professor [nora.last_name], right? I'm [the_person.title], I'm taking her class right now."
    call person_introduction(the_person, girl_introduction = False) from _call_person_introduction_2
    mc.name "I've worked with [nora.title] before."
    the_person.char "So nice to meet you! I'm taking her class on molecular biology, and I'm kind of having a hard time with it."
    the_person.char "My parents want me to find a tutor, and since you've worked with her I thought I would ask you."
    mc.name "Well, I'm not on campus very often. I have my own business that I need to run."
    the_person.char "That's okay, I'm very flexible. I mean, my schedule is very flexible."
    the_person.char "If it's money you're worried about my parents will pay anything. They said to find the best tutor I could."
    "[the_person.possessive_title] waits nervously for your response."
    menu:
        "Tutor [the_person.title].":
            mc.name "Okay, I think we'll be able to work out some sort of price."
            $ the_person.draw_person(emotion = "happy")
            "She smiles and claps her hands."
            the_person.char "Thank you so much! Here, let me give you my phone number and you can call me when you're on campus and available."
            "You hand [the_person.title] your phone and let her put in her phone number."
            the_person.char "Thank you! My parents said they pay $200 a session, but I'm sure they'll pay more if my grades are improving. I hope that's enough."
            mc.name "That will be fine to start."
            the_person.char "Yay! Okay, I've got to run to class. I'm so lucky I ran into you [the_person.mc_title]!"
            $ the_person.draw_person(position = "walking_away")
            "She waves goodbye and hurries off."
            $ the_person.event_triggers_dict["tutor_enabled"] = True


        "Refuse.":
            mc.name "I'm sorry, but I don't want to disappoint you if I don't have the time. I'm going to have to say no."
            $ the_person.draw_person(emotion = "sad")
            "She visibly deflates."
            the_person.char "Right, sorry I bothered you. Thanks for the time anyways."
            the_person.char "I should get to class. Bye."
            $ the_person.draw_person(position = "walking_away")
            "She gives you a sad wave goodbye and hurries off."
            $ the_person.event_triggers_dict["student_reintro_required"] = True

    $ renpy.scene("Active")
    return

label student_reintro(the_person): #Called when you turned down the student in the first interaction but now want to restart this story line.
    mc.name "Are you still having trouble with [nora.title]'s class?"
    the_person.char "You mean Professor [nora.last_name]? Yeah, I am. I've tried another tutor but it just isn't sticking."
    menu:
        "Offer to tutor her.":
            mc.name "Well I think I'm going to be on campus more often now, if you're still interested in..."
            $ the_person.draw_person(emotion = "happy")
            the_person.char "Yes! My parents are paying the current guy $200 a session, I'm sure they would pay you even more if my grades start to improve."
            the_person.char "Here, I'll put my phone number into your phone. If you're on campus let me know and I'll drop everything."
            "You hand her your phone and wait for her to put in her number."
            the_person.char "There. Thank you so much [the_person.mc_title]!"
            mc.name "My pleasure, I just want to see you do well in your class."
            $ the_person.event_triggers_dict["student_reintro_required"] = False
            $ the_person.event_triggers_dict["tutor_enabled"] = True

        "Do nothing.":
            mc.name "I'm sorry to hear that. I'm sure you'll get the hang of it soon."
            "She sighs and shrugs."
            the_person.char "Yeah, me too. Thanks for asking, at least."
    return

# No longer needed, all of the girls actions are specific to her (ie. role actions) instead of being available from the location.
# label student_study_meetup(the_person): #The university action, in case she's not around but should be.
#     "You text [the_person.title] and let her know you're on campus and have some spare time."
#     the_person.char "I'll go get a study room right now. See you in the library!"
#     "You make your way to the library and find [the_person.possessive_title] in a private study room. She already has her textbooks out and ready to go."
#     the_person.draw_person(position = "sitting")
#     the_person.char "Hey!"
#     "You take a seat on the same side of the table as her."
#     call student_study_university(the_person)
#     return

label student_study_propose(the_person):
    if the_person in the_person.home.people: #ie. she's at home and the event has triggered.
        mc.name "I've got time, if you're ready to do some studying."
        the_person.char "Oh yeah, that's probably a good idea. I've been having a really hard time with my assignment."
        "[the_person.title] leads you up to her room."
        call student_study_home(the_person) from _call_student_study_home
    else:
        mc.name "I've got some spare time, if you want to get some studying in."
        the_person.char "Oh, that's a good idea. Let's head over to the library and get a study room."
        "You and [the_person.title] head to the university. She talks to the librarian at the front and books one of the private study rooms for the two of you."
        the_person.char "Good thing there was one left!"
        $ the_person.draw_person(position = "sitting")
        "You find the study room and sit down next to [the_person.possessive_title] as she opens up her backpack and pulls out her textbook."
        call student_study_university(the_person) from _call_student_study_university

    $ the_person.event_triggers_dict["last_tutor"] = day
    return

label student_study_university(the_person):
    # TODO: Add an "inside library" location that we can change the background to.
    $ starting_focus = the_person.focus #Record her starting focus so we can compare it at the end (ie. after being given serum)
    $ starting_int = the_person.int

    $ took_serum = False #Set to true if you give her serum to study with. If the study session goes well (either from raised focus, int, or she orgasms) she'll want more in the future.
    $ current_marks = the_person.event_triggers_dict["current_marks"]

    if the_person.event_triggers_dict.get("times_studied_university", 0) == 0:
        the_person.char "Okay, so where should we start?"
        mc.name "Well let's start by talking about your marks, so we know how much work we need to do."
        "[the_person.title] drums her fingers nervously on the desk."
        the_person.char "Right. Well, they aren't great. Right now I'm failing, but Professor [nora.last_name] said she would transfer all of the class weight to my exam if I could get up to an 80%%!"
        mc.name "That's good, then we just have to focus on that. How bad are your marks right now? 45%%? 40%%?"
        the_person.char "Well... My average right now is 25%%."
        mc.name "That's a lot of ground to make up."
        the_person.char "I know, I just find it so hard to focus and memorize all of this stuff."
        mc.name "Well let's get started and give it a try."
        $ the_person.event_triggers_dict["times_studied_university"] = the_person.event_triggers_dict.get("times_studied_university", 0) + 1

    else:
        the_person.char "Okay, so what are we working on today?"
        mc.name "Let's start with your grades. Any changes?"
        the_person.char "Well, I got a [current_marks]%% on my last assignment."
        if current_marks > 80:
                mc.name "Fantastic! A little more work and you'll be the best in your class!"
                the_person.char "Thanks, you've really helped everything come together!"
                "Vren" "This section of the game is under construction. In v0.30.1 you will have the ability to hire [the_person.title] once her marks are high enough."
        elif current_marks > 50:
            mc.name "That sounds like a pass to me!"
            the_person.char "Yeah! I need to convince Professor [nora.last_name] to shift more weight to my exam, but I might be able to do this!"
            mc.name "And we still have more time to improve."
        else:
            mc.name "So there's some room for improvement. That's fine, we still have time."

    if the_person.event_triggers_dict.get("student_wants_serum", False): #TODO: Double check this gives more total buffs than her not wanting it
        the_person.char "Hey, so before we get started do you have any more of that stuff you gave me last time?"
        the_person.char "I feel like it really helped me focus."
        menu:
            "Give her a dose of serum." if mc.inventory.get_any_serum_count() > 0:
                mc.name "Of course, I'm glad to hear it helped."
                call give_serum(the_person) from _call_give_serum_22
                if _return:
                    $ took_serum = True
                    $ the_person.change_love(1)
                    $ the_person.change_obedience(1)
                    $ the_person.event_triggers_dict["student_given_serum"] = the_person.event_triggers_dict.get("student_given_serum", 0) + 1
                    "You hand over the dose of serum. [the_person.possessive_title] drinks it down happily."


                else:
                    mc.name "I'm sorry, I think I left it at home by mistake. Maybe next time."
                    the_person.char "Oh, okay."



            "Give her a dose of serum.\nRequires: Serum (disabled)" if mc.inventory.get_any_serum_count() == 0:
                pass


            "No serum this time.":
                mc.name "We're going to try this session without any serum."
                the_person.char "Oh, okay."

    elif the_person.event_triggers_dict.get("times_studied_university",0) or mc.inventory.get_any_serum_count() == 0:
        pass #Don't talk about serum the first time or if we don't have any on us.
    else:
        menu:
            "Start studying.":
                pass

            "Give her a dose of serum." if the_person.obedience >= 110 and mc.inventory.get_any_serum_count() > 0:
                if the_person.event_triggers_dict.get("student_given_serum", 0) == 0:
                    mc.name "Before we get started I'd like to try something today."
                    the_person.char "Okay, what's that?"
                    mc.name "My pharmaceutical produces a number of products. Some of them help aid focus, and I think that could also help you."
                    mc.name "I want you to try some."
                    "[the_person.title] thinks for a moment, then shrugs and nods."
                    the_person.char "Yeah, sure. It's not illegal or anything like that, right?"
                    mc.name "No, it's perfectly safe and legal."
                    call give_serum(the_person) from _call_give_serum_23
                    if _return:
                        $ took_serum = True
                        $ the_person.change_obedience(2)
                        $ the_person.event_triggers_dict["student_given_serum"] = the_person.event_triggers_dict.get("student_given_serum", 0) + 1
                        "You produces a vial of serum and hand it over to [the_person.title]. She drinks it down without hesitation."
                        the_person.char "That wasn't so bad. How fast should this work?"
                        mc.name "It will take a few minutes. Let's focus on your studying."
                    else:
                        mc.name "Hmm, it looks like I forgot it at home."
                        the_person.char "That's fine, we can try it next time then."
                        mc.name "I guess we'll have to. Let's focus on your studying then."

                else:
                    mc.name "Before we start I'd like you to take some serum, to help with your focus."
                    call give_serum(the_person) from _call_give_serum_24
                    if _return:
                        $ took_serum = True
                        the_person.char "Do you think it really helps? I didn't notice anything last time."
                        mc.name "Trust me, it does."
                        $ the_person.change_love(-1)
                        $ the_person.change_obedience(1)
                        $ the_person.event_triggers_dict["student_given_serum"] = the_person.event_triggers_dict.get("student_given_serum", 0) + 1
                        "[the_person.title] seems unconvinced, but she drinks down the serum anyways."
                    else:
                        mc.name "On second thought, I think we'll see how you do without serum this session. Let's focus on your studying."



            "Give her a dose of serum.\nRequires: 110 Obedience (disabled)" if the_person.obedience < 110 and mc.inventory.get_any_serum_count() > 0:
                pass


    call study_normally(the_person, public = True) from _call_study_normally

    if the_person.int > starting_int and took_serum: #If she has either her int or focus boosted by serum she's much happier to take it in the future.
        the_person.char "Wow, I actually found that really easy! I think this serum stuff you gave me actually helped."
        the_person.char "Could you bring some more for next time? If I keep this up I'm going to smash this course!"
        $ the_person.event_triggers_dict["student_wants_serum"] = True
        mc.name "Good to hear it helped. I'll see what I can do."
    elif the_person.focus > starting_focus and took_serum:
        the_person.char "Really? Oh man, I was in the zone for that last section. I think this serum stuff you gave me really helps my focus."
        the_person.char "Could you bring some more for me next time? If I can study like this all the time I'm going to smash this course!"
        $ the_person.event_triggers_dict["student_wants_serum"] = True
        mc.name "Good to hear it helped. I'll see what I can do."
    else:
        if took_serum:
            $ the_person.event_triggers_dict["student_wants_serum"] = False
        the_person.char "Finally! I can't believe Professor [nora.last_name] expects us to figure all that stuff out on our own!"
        mc.name "Well you made it through, so good job."

    if the_person.focus > starting_focus or the_person.int > starting_int:
        $ total_improvement = (the_person.focus - starting_focus) + (the_person.int - starting_int)
        $ the_person.event_triggers_dict["current_marks"] += total_improvement
        $ mc.log_event(the_person.title + " stayed focused while studying and learned more than usual.", "float_text_grey")

    "[the_person.possessive_title] packs up her books and hands over your pay for the study session."
    $ mc.business.funds += 200

    if not the_person.event_triggers_dict.get("home_tutor_enabled", False):
        menu:
            "Say goodbye.":
                mc.name "You did a good job today [the_person.title]. Hopefully we can keep that up next time."
                the_person.char "Thanks [the_person.mc_title], I feel like I'm actually learning something for once!"

            "Offer to tutor her at home." if the_person.love >= 15:
                mc.name "You did a good job today [the_person.title], but I think you would be able to focus even better in a less formal location."
                mc.name "How would you feel about having these study sessions at your home?"
                the_person.char "Oh, I guess that would be pretty convenient, but would it really help me focus?"
                mc.name "At home you'll be able to relax and not worry about your surroundings. I think it's a good idea."
                "[the_person.possessive_title] nods and smiles."
                the_person.char "Okay then, I'll text you my address and let my mom know you might be coming by."
                the_person.char "I really need to do well in this course, so you're welcome any time."
                $ mc.known_home_locations.append(the_person.home)
                $ the_person.event_triggers_dict["home_tutor_enabled"] = True

                $ student_mom_intro_action = Action("Student_Mom_Intro", student_mom_intro_requirement, "student_mom_intro")
                $ christina.on_room_enter_event_list.append(student_mom_intro_action)

            "Offer to tutor her at home.\nRequires: 15 Love (disabled)" if the_person.love < 15:
                pass

    $ the_person.event_triggers_dict["times_studied_university"] = the_person.event_triggers_dict.get("times_studied_university", 0) + 1
    if the_person.event_triggers_dict.get("current_marks",0) > 100:
        $ the_person.event_triggers_dict["current_marks"] = 100
    $ renpy.scene("Active")
    call advance_time() from _call_advance_time_21
    return


label student_study_home(the_person):
    $ starting_focus = the_person.focus #Record her starting focus so we can compare it at the end (ie. after being given serum)
    $ starting_int = the_person.int

    $ took_serum = False #Set to true if you give her serum to study with. If the study session goes well (either from raised focus, int, or she orgasms) she'll want more in the future.
    $ current_marks = the_person.event_triggers_dict["current_marks"]

    if the_person.event_triggers_dict.get("times_studied_home", 0) == 0:
        the_person.char "So, how do you want to do this?"
        mc.name "Just treat it like our study sessions on campus."

    else:
        the_person.char "One second, I just need to get my books out. Have a seat!"

    $ the_person.draw_person(position = "sitting")
    "[the_person.title] gathers up her books and spreads them out on her desk, then pulls up an extra chair and sits down beside you."

    mc.name "Let's talk about your grades. How have you been doing recently?"
    the_person.char "Well, I got a [current_marks]%% on my last assignment."
    if current_marks > 80:
            mc.name "Fantastic! A little more work and you'll be the best in your class!"
            the_person.char "Thanks, you've really helped everything come together!"
            "Vren" "This section of the game is under construction. In v0.30.1 you will have the ability to hire [the_person.title] once her marks are high enough."
    elif current_marks > 50:
        mc.name "That sounds like a pass to me!"
        the_person.char "Yeah! I need to convince Professor [nora.last_name] to shift more weight to my exam, but I might be able to do this!"
        mc.name "And we still have more time to improve."
    else:
        mc.name "So there's some room for improvement. That's fine, we still have time."

    if the_person.event_triggers_dict.get("student_wants_serum", False): #TODO: Hook up this trigger. Basically if she's had serum before and it made her smarter.
        the_person.char "I was wondering... Do you have any more of that stuff you gave me last time?"
        the_person.char "I feel like it really helped me focus."
        menu:
            "Give her a dose of serum." if mc.inventory.get_any_serum_count() > 0:
                mc.name "Of course, I'm glad to hear it helped."
                call give_serum(the_person) from _call_give_serum_25
                if _return:
                    $ took_serum = True
                    $ the_person.change_love(1)
                    $ the_person.change_obedience(1)
                    $ the_person.event_triggers_dict["student_given_serum"] = the_person.event_triggers_dict.get("student_given_serum", 0) + 1
                    "You hand over the dose of serum. [the_person.possessive_title] drinks it down happily."


                else:
                    mc.name "I'm sorry, I think I left it at home by mistake. Maybe next time."
                    the_person.char "Oh, okay."


            "No serum this time.":
                mc.name "We're going to try this session without any serum."
                the_person.char "Oh, okay."

    else:
        menu:
            "Start studying.":
                pass

            "Give her a dose of serum." if the_person.obedience >= 110 and mc.inventory.get_any_serum_count() > 0:
                if the_person.event_triggers_dict.get("student_given_serum") == 0:
                    mc.name "Before we get started I'd like to try something today."
                    the_person.char "Okay, what's that?"
                    mc.name "My pharmaceutical produces a number of products. Some of them help aid focus, and I think that could also help you."
                    mc.name "I want you to try some."
                    "[the_person.title] thinks for a moment, then shrugs and nods."
                    the_person.char "Yeah, sure. It's not illegal or anything like that, right?"
                    mc.name "No, it's perfectly safe and legal."
                    call give_serum(the_person) from _call_give_serum_26
                    if _return:
                        $ took_serum = True
                        $ the_person.change_obedience(2)
                        $ the_person.event_triggers_dict["student_given_serum"] = the_person.event_triggers_dict.get("student_given_serum", 0) + 1
                        "You produces a vial of serum and hand it over to [the_person.title]. She drinks it down without hesitation."
                        the_person.char "That wasn't so bad. How fast should this work?"
                        mc.name "It will take a few minutes. Let's focus on your studying."
                    else:
                        mc.name "Hmm, it looks like I forgot it at home."
                        the_person.char "That's fine, we can try it next time then."
                        mc.name "I guess we'll have to. Let's focus on your studying then."

                else:
                    mc.name "Before we start I'd like you to take some serum, to help with your focus."
                    call give_serum(the_person) from _call_give_serum_27
                    if _return:
                        $ took_serum = True
                        the_person.char "Do you think it really helps? I didn't notice anything last time."
                        mc.name "Trust me, it does."
                        $ the_person.change_love(-1)
                        $ the_person.change_obedience(1)
                        $ the_person.event_triggers_dict["student_given_serum"] = the_person.event_triggers_dict.get("student_given_serum", 0) + 1
                        "[the_person.title] seems unconvinced, but she drinks down the serum anyways."
                    else:
                        mc.name "On second thought, I think we'll see how you do without serum this session. Let's focus on your studying."

            "Give her a dose of serum.\nRequires: 110 Obedience (disabled)" if the_person.obedience < 110 and mc.inventory.get_any_serum_count() > 0:
                pass


    menu:
        "Study normally.":
            call study_normally(the_person, public = False) from _call_study_normally_1

        "Try something different...": #TODO: These should probably all be events so their requirements can be made dynamic and depend on options ect.
            mc.name "I want to try something different today [the_person.title]. I think it will help your focus."
            the_person.char "Okay, what did you have in mind?"


            # python:
            #     # The "Get her off" chain of events
            #     private_masturbate_action = Action("Masturbate first.", private_masturbate_requirement, "private_masturbate_label", args = the_person, requirement_args = the_person)
            #     view_masturbate_action = Action("Masturbate first.", view_masturbate_requirement, "view_masturbate_label", args = the_person, requirement_args = the_person)
            #     mutual_masturbate_action = Action("Masturbate together first.", finger_masturbate_requirement, "masturbate_together_label", args = the_person, requirement_args = the_person)




                # The "Punisher her" chain
                #study_punish_hub_action = Action("Punish her for wrong answers.", study_punish_hub_requirements, "study_punish_requirements", args = the_person, requirement_args = the_person)
                # Strip for each wrong answer
                # Spank her for each wrong answer
                # Suck me off for each wrong answer
                # Fuck her for each wrong asnwer
                # Cream pie her for each wrong answer
                # Anal her for each wrong answer

            menu:
                "Masturbate first" if the_person.effective_sluttiness() >= 15:
                    call student_masturbate_label(the_person) from _call_student_masturbate_label

                "Masturbate first\nRequires: 15 Sluttiness (disabled)" if the_person.effective_sluttiness() < 15:
                    pass

                "Punish her for wrong answers." if the_person.obedience >= 100:
                    call student_punish_hub_label(the_person) from _call_student_punish_hub_label

                "Punish her for wrong answers.\nRequires: 100 Obedience (disabled)" if the_person.obedience < 100:
                    pass

            # menu:
            #     "Masturbate first.(Under Construction)" if the_person.effective_sluttiness() >= 25:
            #         "Vren" "This content is under construction. The mechanical effects are in place, but the dialogue is not. It will be ready for v0.30.1!"
            #         $ the_person.event_triggers_dict["student_masturbate"] = the_person.event_triggers_dict.get("student_masturbate",0) + 1
            #         $ the_person.change_slut_temp(3,40)
            #         $ the_person.change_obedience(2)
            #         if the_person.effective_sluttiness() > 50 or the_person.get_opinion_score("masturbating") > 0:
            #             $ the_person.discover_opinion("masturbating")
            #             $ the_person.event_triggers_dict["current_marks"] += 3
            #             $ mc.log_event(the_person.title + " learns much better after she gets off.", "float_text_grey")
            #
            #         else:
            #             $ the_person.change_love(-2)
            #             $ the_person.event_triggers_dict["current_marks"] += 1
            #             $ mc.log_event(the_person.title + " has trouble focusing. She doesn't learn very much.", "float_text_grey")
            #
            #
            #     "Masturbate first.(Under Construction)\nRequires: 25 Sluttiness (disabled)" if the_person.effective_sluttiness() < 25:
            #         pass
            #
            #     "Play strip study.(Under Construction)" if the_person.effective_sluttiness() >= 35:
            #         "Vren" "This content is under construction. The mechanical effects are in place, but the dialogue is not. It will be ready for v0.30.1!"
            #         $ the_person.event_triggers_dict["student_strip_study"] = the_person.event_triggers_dict.get("student_strip_study",0) + 1
            #         $ the_person.change_slut_temp(3,40)
            #         $ the_person.change_obedience(2)
            #         if the_person.effective_sluttiness() > 60 or the_person.get_opinion_score("not wearing anything") > 0: #TODO: This should probably be "showing tits" and "showing ass". Fix in v0.30.1
            #             $ the_person.discover_opinion("not wearing anything")
            #             $ the_person.event_triggers_dict["current_marks"] += 1
            #             $ mc.log_event(the_person.title + " has too much fun stripping for you to concentrate on studying.", "float_text_grey")
            #         else:
            #             $ the_person.change_love(-1)
            #             $ the_person.event_triggers_dict["current_marks"] += 3
            #             $ mc.log_event(the_person.title + " studies harder to avoid stripping, and learns a lot.", "float_text_grey")
            #
            #     "Play strip study.(Under Construction)\nRequires: 35 Sluttiness (disabled)" if the_person.effective_sluttiness() < 35:
            #         pass
            #
            #     "Study naked.(Under Construction)" if the_person.effective_sluttiness() >= 50:
            #         "Vren" "This content is under construction. The mechanical effects are in place, but the dialogue is not. It will be ready for v0.30.1!"
            #         $ the_person.event_triggers_dict["student_study_naked"] = the_person.event_triggers_dict.get("student_study_naked",0) + 1
            #         $ the_person.change_slut_temp(3,40)
            #         $ the_person.change_obedience(2)
            #         if the_person.effective_sluttiness() > 65 or the_person.get_opinion_score("not wearing anything") > 0: #TODO: This should probably be "showing tits" and "showing ass". Fix in v0.30.1
            #             $ the_person.discover_opinion("not wearing anything")
            #             $ the_person.event_triggers_dict["current_marks"] += 1
            #             $ mc.log_event(the_person.title + " has too much fun being naked to concentrate on studying.", "float_text_grey")
            #         else:
            #             $ the_person.change_love(-1)
            #             $ the_person.event_triggers_dict["current_marks"] += 4
            #             $ mc.log_event(the_person.title + " studies harder so she can get dressed again. You teach her a lot.", "float_text_grey")
            #
            #     "Study naked.(Under Construction)\nRequires: 50 Sluttiness (disabled)" if the_person.effective_sluttiness() < 50:
            #         pass
            #
            #     # "Punish her for wrong answers.": #TODO: Implement these for v0.30.1
            #     #     "Vren" "This content is under construction. The mechanical effects are in place, but the dialogue is not. It will be ready for v0.30.1!"
            #     #     $ the_person.event_triggers_dict["student_study_punish"] = the_person.event_triggers_dict.get("student_study_punish",0) + 1
            #     #
            #     # "Pay her for correct answers.":
            #     #     "Vren" "This content is under construction. The mechanical effects are in place, but the dialogue is not. It will be ready for v0.30.1!" # TODO: THis event. Pay her for each answer she gets correct, raising happiness and her grades. If slutty this becomes "lick me"
            #     #     $ the_person.event_triggers_dict["student_study_reward"] = the_person.event_triggers_dict.get("student_study_reward",0) + 1
            #
            #     "Never mind.":
            #         call study_normally(the_person, public = False) from _call_study_normally_2

    if the_person.int > starting_int and took_serum: #If she has either her int or focus boosted by serum she's much happier to take it in the future.
        the_person.char "Wow, I actually found that really easy! I think this serum stuff you gave me actually helped."
        the_person.char "Could you bring some more for next time? If I keep this up I'm going to smash this course!"
        $ the_person.event_triggers_dict["student_wants_serum"] = True
        mc.name "Good to hear it helped. I'll see what I can do."
    elif the_person.focus > starting_focus and took_serum:
        the_person.char "Really? Oh man, I was in the zone for that last section. I think this serum stuff you gave me really helps my focus."
        the_person.char "Could you bring some more for me next time? If I can study like this all the time I'm going to smash this course!"
        $ the_person.event_triggers_dict["student_wants_serum"] = True
        mc.name "Good to hear it helped. I'll see what I can do."
    else:
        if took_serum:
            $ the_person.event_triggers_dict["student_wants_serum"] = False

        the_person.char "Finally! I can't believe Professor [nora.last_name] expects us to figure all that stuff out on our own!"
        mc.name "Well you made it through, so good job."

    if the_person.focus > starting_focus or the_person.int > starting_int:
        $ total_improvement = (the_person.focus - starting_focus) + (the_person.int - starting_int)
        $ the_person.event_triggers_dict["current_marks"] += total_improvement
        $ mc.log_event(the_person.title + " stayed focused while studying and learned more than usual.", "float_text_grey")

    #Ideas for actions:
        # Just study
        # Give her serum (Then select a different option)
        # Try masturbating before studying.
        # Strip study (She looses clothing each time she gets a question wrong.)
        # Punish her for wrong answers
        # Reward her for right answers
        # Study nude.
        # If she's slutty enough she may try and bribe you to have Nora pass her (or at least boost her test mark)

    # Random chance that on some events her Mom will walk in on you?

    # TODO: Help the student study at home. Opens up more options for rewards/punishments
    # TODO: If you make her orgasm, and as her marks improve, she'll "talk to her mom" and improves your pay.

    $ mc.business.funds += 200
    $ the_person.event_triggers_dict["times_studied_home"] = the_person.event_triggers_dict.get("times_studied_home", 0) + 1
    if the_person.event_triggers_dict.get("current_marks",0) > 100:
        $ the_person.event_triggers_dict["current_marks"] = 100
    $ renpy.scene("Active")
    call advance_time() from _call_advance_time_22
    return

label study_normally(the_person, public = True):
    "You start working with [the_person.title], making your way through a molecular biology assignment."
    "After an hour of work she sits back in her chair and sighs."
    the_person.char "Ugh, this is so hard! Can we take a break?"
    menu:
        "Take a break.":
            mc.name "Alright, you've been working well so far, so we can take a short break."
            the_person.char "Phew, thank you."
            menu:
                "Chat.":
                    mc.name "While you're letting your brain rest we can chat a bit. What do you want to talk about?"
                    call small_talk_person(the_person) from _call_small_talk_person
                    $ the_person.change_obedience(-1)
                    mc.name "Well, it's time to get back to work."
                    "[the_person.possessive_title] sighs and reluctantly pulls her chair towards the desk."

                "Stretch.":
                    if the_person.event_triggers_dict.get("student_stretched", 0) == 0: #Doesn't include other ways you might "stretch her".
                        mc.name "We've both been sitting for a while, we should get on our feet and do some stretching."
                        the_person.char "Do we have to?"
                        "You stand up and put your arms above your head to stretch them out."
                        mc.name "You'll feel better after it. Come on, get up."
                        $ the_person.draw_person()
                        "[the_person.possessive_title] sighs and stands up, stepping back from the study room table to give herself some extra room."


                    else:
                        mc.name "We've been sitting for a while, let's do some stretches again."
                        the_person.char "I guess that's a good idea."
                        $ the_person.draw_person()
                        "[the_person.possessive_title] stands up and steps back from the table, giving herself some extra room."


                    mc.name "Alright, let's start with your arms."
                    "You cross one arm over your body and pull it towards you, then switch and do the same to the other. [the_person.title] follows your lead."
                    mc.name "Good. Now legs."
                    "You step into a deep lunge, then stand up and do the same with your other leg. [the_person.title] mirrors you again."
                    mc.name "Does that feel better?"
                    the_person.char "Yeah, I guess."
                    mc.name "Now let's stretch out your core. Put your hands on the table, set your legs appart, and bend forward."
                    $ the_person.draw_person(position = "walking_away") #TODO: Replace this with "standing doggy" once the images for that aren't broken.
                    the_person.char "Uh, like this?"
                    menu:
                        "Hold that pose.":
                            mc.name "Perfect. Now just hold that for a few seconds."
                            if the_person.effective_sluttiness() < 15:
                                the_person.char "I feel silly stikcing my butt in the air like this."
                                mc.name "Don't worry about that, it's just the two of us here. Nobody out in the library is looking."
                            else:
                                the_person.char "Hey, you aren't doing this just to stare at my butt, are you?"
                                mc.name "Me? Of course not! It is a perk though."
                                "[the_person.possessive_title] laughs and wiggles her hips."

                            $ the_person.draw_person()
                            "Stretch complete, [the_person.title] stands back up and takes a deep breath."
                            the_person.char "You know what, that actually felt good."
                            $ the_person.change_slut_temp(2, 15)
                            mc.name "Good to hear, now let's get back to it."

                        "\"Help\" her push a little furthur.":
                            mc.name "You can push your hips out a little furthur. Here."
                            "You step close behind her and place your hands on her hips. You pull back gently helping her stretch while also pushing her butt against your crotch."
                            the_person.char "Ooh, I can really feel that..."
                            $ the_person.change_slut_temp(3, 25)
                            $ the_person.change_love(-1)
                            "You enjoy the feeling her ass grinding up against you as long as you think you can get away with, then you ease up on the pressure."
                            $ the_person.draw_person()
                            "[the_person.title] stands up again and takes a deep breath."
                            the_person.char "Uh... Well, thanks for the help."

                    $ the_person.event_triggers_dict["student_stretched"] = the_person.event_triggers_dict.get("student_stretched", 0) + 1
                    $ the_person.draw_person(position = "sitting")
                    "You both sit down and get back to work."

                "Massage." if the_person.effective_sluttiness() >= 10:
                    if the_person.event_triggers_dict.get("student_massaged", 0):
                        "You slide your chair back and stand up."
                        mc.name "You've been doing a really good job so far [the_person.title]. Let me massage your shoulders, it should help you relax."
                        "You step behind her and place your hands on her shoulders."
                        the_person.char "Oh, you don't need to do that [the_person.mc_title]."
                        mc.name "Studying like this can be suprisingly stressful. I promise this will help improve your marks in the long run."
                        "You rub her shoulders gently. She sighs and lets them fall slack."
                        the_person.char "That does feel really good... Okay, just a little massage."

                    else:
                        "You slide your chair back and stand up."
                        mc.name "You've been doing a really good job so far [the_person.title]. Here, let me give you another massage and help you relax."
                        the_person.char "Oh, that does sound nice."
                        "You step behind her, put your hands on her shoulders, and rub them gently."


                    "You spend some time massaging [the_person.possessive_title]'s shoulders. She relaxes and leans back in her chair, eyes closed."

                    $ the_person.change_slut_temp(1,15)

                    menu:
                        "Finish the massage.":
                            mc.name "There you go. Feeling more relaxed now?"
                            "She sighs and nods."
                            $ the_person.change_love(1)
                            the_person.char "Yeah, that actually helped a ton. I guess we have to get back to it then."


                        "Massage her tits." if the_person.effective_sluttiness() >= 15:
                            "You work your massage down [the_person.title]'s arms, then to the front of her chest."
                            if the_person.has_taboo("touching_body"):
                                the_person.char "Hey, you're... getting a little low there."
                                "You slide your hands onto her breasts and rub them slowly."
                                mc.name "I'm just trying to make sure you're nice and relaxed. Doesn't it feel good?"
                                the_person.char "Yeah, but... I... Ah..."
                                "She leans back in her chair and sighs."
                                the_person.char "I guess it's fine, if it's just for a moment... Ah..."
                                "[the_person.possessive_title] relaxes her body and turns herself over to you completely."
                                $ the_person.break_taboo("touching_body")
                            else:
                                "[the_person.title] sighs happily when you slide your hands onto her tits. You feel her body relax under your touch."

                            $ the_person.change_slut_temp(2)
                            if the_person.outfit.tits_available():
                                "You enjoy the feeling of her bare breasts as you play with them. When her nipples harden you give them, a light pinch."
                            else:
                                "You enjoy the feeling of her breasts underneath her clothing. You can feel her nipples harden underneath the fabric."

                            "After a couple of quiet minutes [the_person.title] sits back up in her chair."
                            the_person.char "We should get back to work, right? I don't want us to get too distracted."
                            mc.name "That's a good idea. Are you feeling more relaxed?"
                            the_person.char "Way more relaxed. That was nice."


                        "Massage her tits.\nRequires: 15 Sluttiness (disabled)" if the_person.effective_sluttiness() < 15:
                            pass

                    $ the_person.event_triggers_dict["student_massaged"] = the_person.event_triggers_dict.get("student_massaged", 0) + 1
                    "You sit down and get back to studying with [the_person.title]."

                "Massage.\nRequires: 10 Sluttiness (disabled)" if the_person.effective_sluttiness() < 10:
                    pass


            $ the_person.event_triggers_dict["current_marks"] += 2
            $ mc.log_event(the_person.title + " learns a little bit from your tutoring.", "float_text_grey")


        "Keep working.":
            mc.name "You can't take a break now, you've barely started!"
            the_person.char "But it's so boring! Come on, just a few minutes?"
            mc.name "Do you know what has the largest impact on your grades? It's not how smart you are, it's how determined you are."
            mc.name "You need to learn how to focus, and that's something we're going to work on right now."
            $ the_person.change_love(-1)
            $ the_person.change_obedience(3)
            "She sighs and nods."
            the_person.char "Fine, I'll try and focus a little longer."
            mc.name "Good. Let's keep at it and we'll be finished with this assignment before you know it."
            "You get back to work, stopping any time [the_person.possessive_title]'s attention begins to wander and getting her back on task."
            $ the_person.event_triggers_dict["current_marks"] += 3
            $ mc.log_event(the_person.title + " isn't happy, but she learns more without a break.", "float_text_grey")

    mc.name "...And that's the last question. We're done."
    return

label student_masturbate_label(the_person):
    if the_person.event_triggers_dict.get("student_masturbate", 0) == 0:
        mc.name "I've found, when I'm having trouble focusing, that jerking off can help."
        "[the_person.title] seems a little shocked, and takes a second before she responds."
        the_person.char "Wait, you mean you want me to... masturbate?"
        mc.name "Yeah, exactly. I'm assuming you know how to."
        the_person.char "Oh my god, of course I know {i}how{/i} to. It's just a weird thing to hear someone tell you to do."
        mc.name "I know, but I suspect it will really help your grades."

    else:
        the_person.char "Again?"
        mc.name "I thought it worked well last time. Any problems?"
        the_person.char "No, I guess not. It's still a little strange though..."

    if the_person.effective_sluttiness() < 20:
        # She asks you to leave
        "[the_person.possessive_title] hums awkwardly for a moment, glancing around the room."
        the_person.char "Uh... Could I have some privacy?"
        mc.name "I really don't mind if..."
        the_person.char "No, it's just I can't... It's hard with someone watching, you know? Even when it's for a good reason."
        mc.name "Okay, I'll just be waiting outside then."
        $ the_person.change_slut_temp(2)
        the_person.char "Thanks! I'll let you know when I'm... finished."
        $ renpy.scene("Active")
        "You stand up and leave [the_person.possessive_title]'s room. You close her door and lean on the frame."
        #TODO: Chance her mom walks by and asks what's going on.
        "You listen at the door, and hear [the_person.title]'s chair creaking as she moves. After a few minutes you hear a faint gasp."
        $ the_person.draw_person()
        "The bedroom door opens. Her face is beet red."
        mc.name "Did you have a good time?"
        the_person.char "Oh my god, this is so embarassing. Come on, let's get to work..."
        $ the_person.arousal = 25 # Her arousal goes up because she was touching herself.
        $ the_person.event_triggers_dict["current_marks"] += 1 + the_person.get_opinion_score("masturbating")
        $ the_person.discover_opinion("masturbating")
        $ mc.log_event(the_person.title + " seems much more focused.", "float_text_grey")
        $ the_person.draw_person(position = "sitting")

    else:
        # She just starts going at it.
        the_person.char "I guess I'll just... get to it then."
        $ the_item = the_person.outfit.remove_random_lower(top_layer_first = True, do_not_remove = True)
        while the_item is not None and not the_person.outfit.vagina_available():
            $ the_person.draw_animated_removal(the_item)
            "[the_person.title] strips off her [the_item.name] and throws it on her bed."
            $ the_item = the_person.outfit.remove_random_lower(top_layer_first = True, do_not_remove = True)

        $ the_item = the_person.outfit.remove_random_any(top_layer_first = True, exclude_feet = True, do_not_remove = True) #Just in case she's got a dress or something.
        while the_item is not None and not the_person.outfit.vagina_available():
            $ the_person.draw_animated_removal(the_item)
            "[the_person.title] strips off her [the_item.name] and throws it on her bed."
            $ the_item = the_person.outfit.remove_random_any(top_layer_first = True, exclude_feet = True, do_not_remove = True)

        $ the_person.update_outfit_taboos()
        $ the_person.draw_person(position = "sitting")
        "[the_person.possessive_title] leans back in her chair and spreads her legs. She blushes and looks away as she slides her hand down to her pussy."
        the_person.char "It's a little strange doing this with someone watching..."
        menu:
            "Watch her masturbate.":
                mc.name "Just relax and enjoy yourself. Once you finish we can get to studying."
                the_person.char "Right. I'll just be a moment."
                "She closes her eyes and start to run her index finger up and down her slit."
                the_person.char "Mmm..."
                #TODO: Add the ability to tkae pictures in a future update.
                "After teasing herself [the_person.title] slowly slips two fingers into her pussy. She moans softly, her chair creaking as she leans even furthur back."
                the_person.char "Oh yeah... That's it..."
                "She rubs her clit with her thumb while fingering herself."
                the_person.char "I think... I think I'm going to get there soon..."
                "She grips at the side of her chair and takes a deep breath. She starts to hammer her fingers in and out of herself."
                the_person.char "Oh fuck, there it is! Oh... Oh!"
                $ the_person.change_slut_temp(3)
                $ the_person.change_obedience(1)
                "[the_person.title] keeps her fingers moving for a few more seconds, then slows down and stops. She takes a deep sigh and slides them out of her wet cunt."
                the_person.char "You know, I {i}do{/i} feel very relaxed now."
                "She opens her eyes, then blushes and looks away, as if suddenly shy."
                if the_person.judge_outfit(the_person.outfit):
                    the_person.char "We should probably get to work, right?"
                    mc.name "Exactly right."

                else:
                    the_person.char "Just... One second, let me get dressed again."
                    $ the_person.apply_outfit()
                    $ the_person.draw_person(position = "sitting")
                    "[the_person.possessive_title] hurries back into her clothing, then sits down."

                $ the_person.draw_person(position = "sitting")
                $ the_person.event_triggers_dict["current_marks"] += 1 + the_person.get_opinion_score("masturbating") + the_person.get_opinion_score("public sex")
                $ the_person.discover_opinion("masturbating")
                $ the_person.discover_opinion("public sex")
                $ mc.log_event(the_person.title + " seems much more focused.", "float_text_grey")

            "Masturbate with her." if the_person.effective_sluttiness() >= 30: #TODO: Add a mutual masturbation position? At the very least this deserves a more accurate position
                mc.name "Let me help out with that."
                "You unzip your pants and pull out your hard cock. You give it a few gentle strokes as [the_person.possessive_title] watches."
                the_person.char "What... Do you want to do?"
                "You slide one hand onto [the_person.title]'s thigh and caress it, while jerking yourself off with the other."
                mc.name "I thought I would join in, that way you don't have to feel self concious. If we're both trying to get off we could always..."
                "You move your hand and rub her inner thigh, dangerously close to her pussy."
                mc.name "... help each other finish."
                "[the_person.title] bites her lip and hesitates, then nods nervously."
                the_person.char "Okay, I guess that would be fun."
                $ the_person.break_taboo("touching_vagina") #TODO: Some taboo break dialogue.
                "You seal the deal by sliding your hand onto her cunt, brushing her clit with your thumb. She gasps and leans back in her chair."
                $ the_person.change_arousal(10)
                mc.name "Does that feel good?"
                "[the_person.possessive_title] moans and nods."
                the_person.char "Mmhm."
                mc.name "Good. Now stand up for me."
                $ the_person.draw_person()
                "[the_person.title] stands up, and you do the same. You keep one hand between her legs, rubbing her pussy while you talk to her."
                mc.name "I'm going to make sure you get off, and then we'll get some studying done. Does that sound nice?"
                "Your hand on her wet pussy tells you the answer, but she murmers out a response anyways."
                the_person.char "Yes, it does... Mmm."
                $ the_person.draw_person(position = "walking_away")
                "You step behind [the_person.possessive_title] and wrap your other arm around her torso to hold her close, your hard cock rubbing against her thigh."
                "She gasps and leans against you when you slide a couple of fingers into her cunt."
                call fuck_person(the_person, private = True, start_position = standing_finger, skip_intro = True) from _call_fuck_person_86
                $ the_report = _return
                if the_report.get("girl orgasms", 0) > 0:
                    "[the_person.title] collapses into her chair and sighs happily."
                    the_person.char "I think... I'm ready to do some studying."
                    $ the_person.change_slut_temp(2)
                    $ the_person.change_obedience(2)
                    $ the_person.change_love(2)
                    $ the_person.event_triggers_dict["current_marks"] += 4
                    $ mc.log_event(the_person.title + " is much more focused after getting off.", "float_text_grey")

                else:
                    "[the_person.title] collapses into her chair and groans."
                    the_person.char "Fuck, how am I suppose to focus now? All I want to do is dig out my vibrator and spend the night getting off..."
                    mc.name "I'm sure you can hold it together for an hour or two."
                    $ the_person.change_obedience(-2)
                    $ the_person.event_triggers_dict["current_marks"] += -2
                    $ mc.log_event(the_person.title + " is completely distracted while studying.", "float_text_grey")

                if the_person.judge_outfit(the_person.outfit):
                    pass #She's fine with what she's now "wearing"

                else:
                    the_person.char "Just... One second, let me get dressed again."
                    $ the_person.apply_outfit()
                    $ the_person.draw_person(position = "sitting")
                    "[the_person.possessive_title] hurries back into her clothing, then sits down."


            "Masturbate with her.\nRequires: 50 Sluttiness (disabled)" if the_person.effective_sluttiness() < 30:
                pass

    # TODO: If you enter the sex system add a "Get each other off" option in addition to the masturbate option
    call study_normally(the_person, public = False) from _call_study_normally_2
    return

label student_pick_reward(the_person, punishment):
    #TODO: FIrst time dialogue variation
    if (the_person.effective_sluttiness() > 50 or the_person.get_opinion_score("not wearing anything") > 0) and punishment != "student_punish_strip":
        the_person.char "If I get any questions right I want to take something off. That way I can be more relaxed."
        mc.name "Alright, if that's what you want."
        return "student_punish_strip"
    else:
        the_person.char "I want a cut of your pay. Let's say $50 each time I get one right."
        mc.name "Alright, but don't expect me to go easy on you."
        return "student_punish_pay_her"
    return "student_punish_pay_her"

label student_pick_punishment(the_person):
    # TODO: Have some first time dialogue variation here.
    menu:
        "Pay me":
            mc.name "You're going to pay me an extra $50 for every wrong answer."
            the_person.char "Is that all? My mother will..."
            mc.name "Oh no, this needs to come from {i}you{/i}, not mommy."
            the_person.char "Fine. It's not going to matter, I'm going to crush this."
            return "student_punish_pay_you"

        "Strip" if the_person.effective_sluttiness() >= 30:
            mc.name "For each question you get wrong you're going to take off a piece of clothing for me."
            the_person.char "Like, anything I want?"
            mc.name "Something major. I'm not going to let you get away with pulling off a sock."
            the_person.char "Fine. It's not going to matter, I'm going to crush this."
            return "student_punish_strip"

        "Spank her\nUnder Construction (disabled)":
            pass

        "Suck me off\nUnder Construction (disabled)":
            pass

    return "student_punish_pay_you"

label student_punish_hub_label(the_person):
    #First, you tell her you're going to punish her for each wrong answer.
    # If she's only moderately obedient she asks for a reward for all of her _correct_ answers as well
    if the_person.event_triggers_dict.get("student_punish_any") == 0:
        mc.name "We're going to have a quiz about what you've learned so far. For each wrong answer you give me there's going to be a punishment."
        the_person.char "So like a game? Alright, that sounds like fun!"
    else:
        mc.name "We're going to have another quiz about what I've taught you so far. There will be a punishment for each wrong answer."
        the_person.char "Alright. I'm going to ace this!"

    the_person.char "So, what's my punishment going to be?"


    $ reward_label = None
    $ total_successes = 0
    $ total_failures = 0
    $ wants_to_fail = False
    call student_pick_punishment(the_person) from _call_student_pick_punishment
    $ punishment_label = _return

    if punishment_label == "student_punish_strip" and (the_person.effective_sluttiness() > 65 or the_person.get_opinion_score("not wearing anything") > 0): #TODO: FIgure out how to generalise this a little more. Role it into the punishment pick?
        $ wants_to_fail = True # Screws up questions on purpose.

    if the_person.obedience <= 110:
        the_person.char "If there's a punishment for each wrong answer, I think there should be a reward for each right one."
        mc.name "Okay, what do you think your reward should be?"
        call student_pick_reward(the_person, punishment_label) from _call_student_pick_reward
        $ reward_label = _return
    else:
        pass #TODO: You can pick a victory reward for her, same as a "punishment"



    $ question_count = 0
    while question_count < 4:
        if question_count == 0:
            mc.name "Let's start with the first question..."
        elif question_count == 1:
            mc.name "Alright, next question then..."
        elif question_count == 2:
            mc.name "Onto the next question..."
        else:
            mc.name "And now onto the last question..."
        $ question_count += 1
        call student_punish_question(the_person, wants_to_fail) from _call_student_punish_question
        if _return:
            if reward_label:
                $ total_successes += 1
                $ renpy.call(reward_label, the_person, False, wants_to_fail, total_successes, total_failures)
            else:
                pass
        else:
            $ total_failures += 1
            $ renpy.call(punishment_label, the_person, True, wants_to_fail, total_successes, total_failures)



    if total_successes == 4:
        mc.name "I think it's clear that you've been taking your studies very seriously. Well done [the_person.title]."
        $ the_person.change_love(2)
        the_person.char "Thank you [the_person.mc_title]! It feels so good to be doing well at this for once!"
        $ mc.log_event(the_person.title + " feels encouraged by her success, and learned a lot!", "float_text_grey")
        # Great success

    elif total_failures == 4:
        # Great failure
        mc.name "I think it's clear that you have been seriously neglecting your studies [the_person.title]. You're going to need to try much harder."
        if wants_to_fail:
            the_person.char "Yeah, that's why I got all of those wrong... You'll have to punish me even more next time."
            $ the_person.change_obedience(-2)
        else:
            the_person.char "I'm sorry, I promise I'm going to spend all night studying so I can impress you next time."
            $ the_person.change_obedience(2)

        $ mc.log_event(the_person.title + " didn't learn very much at all.", "float_text_grey")

    else:
        # Normal
        mc.name "I think it's clear there is room for improvement, but you're making progress. Good job [the_person.title]."
        the_person.char "Thanks [the_person.mc_title]. I'm trying my best!"
        $ mc.log_event(the_person.title + " feels encouraged by her success, but there's still more she needs to learn.", "float_text_grey")

    $ the_person.event_triggers_dict["current_marks"] += total_successes

    #TODO: Based on how many questions she succeeds or fails her grades change. More failed questions results in learning less.

    return

label student_punish_question(the_person, wants_to_fail = False):
    "You take a moment to decide on what question to give [the_person.possessive_title]."
    $ question_is_hard = False
    menu:
        "Give her a hard question (tooltip)She is more likely to get a hard question wrong, but it's less likely to teach her something useful.":
            "You pick a hard question from [the_person.title]'s assignment."
            $ question_is_hard = True


        "Give her an easy question (tooltip)She is less likely to get an easy question wrong, but she's more likely to learn something from it.":
            "You pick an easy question from [the_person.title]'s assignment."

    mc.name "Here, solve this one."
    if wants_to_fail:
        the_person.char "Alright, I've totally got this!"
    else:
        the_person.char "I hope I can figure this out..."

    "[the_person.possessive_title] gets to work. You sit in silence for a few moments until she passes her notebook over to you to inspect."

    $ success_chance = 60 + (5 * the_person.int)
    if question_is_hard:
        $ success_chance += -50

    if renpy.random.randint(0,100) < success_chance and not wants_to_fail: #Success
        "You look through her answer and everything seems to be correct."
        mc.name "Well done, you got it right."
        if question_is_hard:
            the_person.char "Really? Oh wow, that one was really tricky! I can't believe I got it right!"
            $ the_person.change_happiness(5)
        else:
            the_person.char "Whew, I thought I had it but I'm never completely sure."

        return True

    else: #Failure
        if wants_to_fail:
            "You look through her answer, and spot several obvious mistakes."
            mc.name "Not quite right [the_person.title]. You've got some problems we'll need to correct."
            the_person.char "Oh no, did I? That's a shame, I guess I'm going to be punished now..."
        else:
            "You look through her answer, and spot a critical error."
            mc.name "Not quite right [the_person.title]. You've got a mistake here that's thrown your answer off."
            if question_is_hard:
                the_person.char "Ugh, that question was so hard! How am I ever suppose to remember all of this?"

            else:
                the_person.char "Really? Aww, I thought I had that one right."
                $ the_person.change_happiness(-5)

        return False

    return False # Shouldn't ever reach this return, but just in case we'll assume she gets it wrong

label student_punish_pay_her(the_person, was_failure, wants_to_fail, successes = 0, failures = 0):
    # You pay your student a cash reward for her answer
    the_person.char "So, what about my reward?"
    $ mc.business.funds += -50
    "You put $50 onto the table. [the_person.possessive_title] grabs it and holds it up triumphantly."
    $ the_person.change_happiness(5)
    if successes + failures < 4:
        the_person.char "Haha! Alright, give me another!"
    else:
        pass
    return

label student_punish_pay_you(the_person, was_failure, wants_to_fail, successes = 0, failures = 0):
    mc.name "Alright, hand over the cash."
    "[the_person.possessive_title] pouts and finds her purse. She hands over $50."
    $ mc.business.funds += 50
    if successes + failures < 4:
        the_person.char "Whatever, just give me another one."
    else:
        the_person.char "At least that's over..."
    # Your student pays you in cash for her answer.
    return


label student_punish_strip(the_person, was_failure, wants_to_fail, successes = 0, failures = 0):
    # TODO: The girl strips off a piece of clothing, if she has any left (What happens if she doesn't?)
    $ the_item = the_person.outfit.remove_random_any(top_layer_first = True, exclude_feet = True, do_not_remove = True)
    if the_item:
        if was_failure:
            mc.name "Well, you know what you need to do."
            $ the_person.draw_animated_removal(the_item)
            "[the_person.possessive_title] nods and stands up. She grabs her the [the_item.display_name] and pulls it off."


        else:
            the_person.char "Let me just take this off..."
            "She strips off her [the_item.display_name] and throws it onto her bed before sitting back down."

        #TODO: Have some tits-now-free style checks.

        $ the_person.draw_person(position = "sitting")
        $ the_person.update_outfit_taboos()


    else:
        the_person.char "So... I don't really have anything else to take off..."
        mc.name "Maybe next time you should wear more when we're going to study."
        "She laughs and shrugs."
        the_person.char "Do you really want that? You don't seem to mind."
        mc.name "I'll just have to think up a more interesting punishment I suppose. Come on, back to work."

    return

label student_punish_spank(the_person, was_failure, wants_to_fail, successes = 0, failures = 0):
    # TODO: This section
    # TODO: bend her over her desk and spank her
    return

label student_punish_suck(the_person, was_failure, wants_to_fail, successes = 0, failures = 0):
    #TODO: THis section
    # TODO: She has to suck you off for each wrong question (to completion? 3 rounsd to finish?)
    return


label student_mom_intro(the_person):
    # An on_room event called when you enter Emily's home for the first time while her Mom is there and meet Christina.
    "You ring the doorbell to [emily.title]'s house and wait. A moment later you hear footsteps and the door opens."
    $ the_person.draw_person()
    $ the_person.set_title("???")
    the_person.char "Hello. Can I help you?"
    mc.name "I'm here to turor [emily.title]. Is she in?"
    if emily in emily.home.people:
        the_person.char "Yes, I believe she is in her room. You must be the tutor she has been going on about."
        "She steps to the side, letting you move into the front room of the luxurious house."
        $ the_person.set_title("Mrs."+the_person.last_name)
        $ the_person.set_possessive_title("Mrs."+the_person.last_name)
        the_person.char "I am [the_person.title], [emily.title]'s mother. I'm happy to finally have a chance to introduce myself."
        "You step inside and introduce yourself."
        call person_introduction(the_person, girl_introduction = False) from _call_person_introduction_3
        the_person.char "My daughter has been very happy with your work so far, and I'm glad to see her marks improving."
        $ emily.draw_person()
        emily.char "[emily.mc_title], you're here!"
        "[emily.title] hurries down a flight of stairs to the front door."
        $ the_person.draw_person()
        the_person.char "I'll leave you to your work. Don't hesitate to ask if you need anything [the_person.mc_title]."
        $ emily.draw_person()
        emily.char "Thanks Mom. Come on, let's go to my room and get started."


    else:
        the_person.char "I'm sorry, she must have given you the wrong time. She's not at home right now."
        $ the_person.set_title("Mrs."+the_person.last_name)
        $ the_person.set_possessive_title("Mrs."+the_person.last_name)
        the_person.char "I would still like to introduce myself. I am [the_person.title], [emily.title]'s mother."
        the_person.char "And you must be the tutor she has been going on about. I'm sorry, I don't remember your name."
        call person_introduction(the_person, girl_introduction = False) from _call_person_introduction_4
        the_person.char "[emily.title] is very happy with your work so far, and I'm glad to see her marks improving."
        the_person.char "You're welcome to come in and wait for [emily.title] to get back."
        "She steps to the side, letting you move into the front room of the luxurious house."

    $ renpy.scene("Active")
    return
