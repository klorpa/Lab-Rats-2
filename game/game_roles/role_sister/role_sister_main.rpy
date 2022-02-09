##########################################
# This file holds all of the role requirements and labels for the main unskippable sister storyline.
##########################################

#TODO: Purposeful teasing events

init -2 python:
    #Sister on day events to set up taboo breaks
    def sister_on_day(the_person):
        # Set up taboo break revisits if taboos have been broken.
        if the_person.has_broken_taboo(["touching_body","kissing","bare_pussy","bare_tits","touching_vagina"]) and not the_person.event_triggers_dict.get("kissing_revisit_complete", False): #Checks if they have all of these taboos or not.
            if the_person.has_role(sister_girlfriend_role):
                the_person.event_triggers_dict["kissing_revisit_complete"] = True
            else:
                broken_taboos = the_person.event_triggers_dict.get("kissing_revisit_restore_taboos",[]) #Note: this will result in duplicates sometimes.
                if the_person.has_broken_taboo("bare_tits"):
                    broken_taboos.append("bare_tits")
                if the_person.has_broken_taboo("bare_pussy"):
                    broken_taboos.append("bare_pussy")
                if the_person.has_broken_taboo("kissing"):
                    broken_taboos.append("kissing")
                if the_person.has_broken_taboo("touching_body"):
                    broken_taboos.append("touching_body")
                if the_person.has_broken_taboo("touching_vagina"):
                    broken_taboos.append("touching_vagina")

                taboo_revisit_event = Action("sis kissing taboo revisit", sister_kissing_taboo_revisit_requirement, "sister_kissing_taboo_break_revisit")
                if not the_person.has_queued_event(taboo_revisit_event):
                    the_person.event_triggers_dict["kissing_revisit_count"] = the_person.event_triggers_dict.get("kissing_revisit_count",0) + 1
                    the_person.on_room_enter_event_list.append(taboo_revisit_event)
                    for a_taboo in broken_taboos:
                        the_person.restore_taboo(a_taboo, add_to_log = False)
                the_person.event_triggers_dict["kissing_revisit_restore_taboos"] = broken_taboos

        if the_person.has_broken_taboo(["sucking_cock", "licking_pussy"]) and not the_person.event_triggers_dict.get("oral_revisit_complete", False):
            if the_person.has_role(sister_girlfriend_role):
                the_person.event_triggers_dict["oral_revisit_complete"] = True
            else:
                broken_taboos = the_person.event_triggers_dict.get("oral_revisit_restore_taboos",[])
                if the_person.has_broken_taboo("sucking_cock"):
                    broken_taboos.append("sucking_cock")
                if the_person.has_broken_taboo("licking_pussy"):
                    broken_taboos.append("licking_pussy")
                taboo_revisit_event = Action("sis oral taboo revisit", sister_oral_taboo_revisit_requirement, "sister_oral_taboo_break_revisit")
                if not the_person.has_queued_event(taboo_revisit_event):
                    for a_taboo in broken_taboos:
                        the_person.restore_taboo(a_taboo, add_to_log = False)
                    the_person.event_triggers_dict["oral_revisit_count"] = the_person.event_triggers_dict.get("oral_revisit_count", 0) + 1
                    the_person.on_room_enter_event_list.append(taboo_revisit_event)
                the_person.event_triggers_dict["oral_revisit_restore_taboos"] = broken_taboos

        if the_person.has_broken_taboo("anal_sex") and not the_person.event_triggers_dict.get("anal_revisit_complete", False):
            if the_person.has_role(sister_girlfriend_role):
                the_person.event_triggers_dict["anal_revisit_complete"] = True
            else:
                taboo_revisit_event = Action("sis anal taboo revisit", sister_anal_taboo_revisit_requirement, "sister_anal_taboo_break_revisit")
                if not the_person.has_queued_event(taboo_revisit_event):
                    the_person.restore_taboo("anal_sex", add_to_log = False)
                    the_person.event_triggers_dict["anal_revisit_count"] = the_person.event_triggers_dict.get("anal_revisit_count", 0) + 1
                    the_person.on_room_enter_event_list.append(taboo_revisit_event)

        if the_person.has_broken_taboo("vaginal_sex") and not the_person.event_triggers_dict.get("vaginal_revisit_complete", False):
            if the_person.has_role(sister_girlfriend_role):
                the_person.event_triggers_dict["vaginal_revisit_complete"] = True
            else:
                taboo_revisit_event = Action("sis vaginal taboo revisit", sister_vaginal_taboo_revisit_requirement, "sister_vaginal_taboo_break_revisit")
                if not the_person.has_queued_event(taboo_revisit_event):
                    the_person.restore_taboo("vaginal_sex", add_to_log = False)
                    the_person.event_triggers_dict["vaginal_revisit_count"] = the_person.event_triggers_dict.get("vaginal_revisit_count", 0) + 1
                    the_person.on_room_enter_event_list.append(taboo_revisit_event)


        return

init -2 python:
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
        elif not mc.business.has_funds(50):
            return "Requires: $50"
        else:
            return True

    def sister_strip_intro_requirement(the_person): #Note that this only ever triggers once, so we don't need to worry if it will retrigger at any point.
        if time_of_day == 4 and mc.location == bedroom:
            if the_person.sluttiness >= 30 and mc.business.event_triggers_dict.get("sister_serum_test_count",0) >= 4:
                return True
        return False

    def sister_strip_reintro_requirement(the_person):
        if not mc.business.event_triggers_dict.get("sister_strip_reintro",False):
            return False
        elif mc.location != lily_bedroom:
            return False
        elif len(lily_bedroom.people) > 1:
            return False
        elif the_person.sluttiness < 30:
            return "Requires: " + get_red_heart(30)
        else:
            return True

    def sister_strip_requirement(the_person): #She'll only strip if you're in her bedroom and alone.
        if not mc.business.event_triggers_dict.get("sister_strip",False):
            return False
        elif mc.location != lily_bedroom:
            return False
        elif len(lily_bedroom.people) > 1:
            return False
        elif the_person.sluttiness < 30 or not mc.business.has_funds(100):
            return "Requires: $100, " + get_red_heart(30)
        else:
            return True

    def sister_offer_to_hire_requirement(the_person): #NOTE: This is attached to the sister student role.
        if the_person.event_triggers_dict.get("dropout_convince_progress", 0) > 2:
            return False
        elif the_person.love < 10:
            return False
        elif the_person.love < 20:
            return "Requires: 20 Love"
        elif mc.business.get_employee_count() >= mc.business.max_employee_count:
            return "At employee limit"
        else:
            return True

    def mother_sister_dropout_convince_requirement(the_person):
        if lily.event_triggers_dict.get("dropout_convince_progress", 0) != 1:
            return False
        else:
            return True


#SISTER ACTION LABELS#

label sister_intro_crisis_label(the_person):
    #This is a mantatory crisis, so we assume that our requirements are tight enough to always trigger correctly. If you want to do crisis requirement checks here you need to re-add the crisis to the mandatory list!
    $ bedroom.show_background()
    "There's a knock at your bedroom door."
    mc.name "Come in."
    $ the_person.draw_person()
    the_person "Hey [the_person.mc_title], do you have a moment?"
    mc.name "Sure, what's up?"
    "[the_person.possessive_title] steps into your room and closes the door behind her."
    the_person "I wanted to say I'm really impressed with how your business is going. It must be really exciting to be your own boss now."
    mc.name "It's certainly been challanging, that's for sure."
    the_person "And... Well, I've been so busy with school that I haven't had a chance to get a job like Mom's been wanting..."
    mc.name "Oh no, I can see where this is going."
    the_person "If you could just give me a {i}tiny{/i} bit of cash I could show Mom I can take care of myself."
    mc.name "But you can't, apparantly."
    the_person "Please? Please please please, [the_person.mc_title]? Maybe there's some extra work I could do? I could..."
    "She gives up and shrugs."
    the_person "Help you science all that science stuff?"
    mc.name "I don't think that's really where I need help. But..."
    menu:
        "Ask [the_person.title] to test serum for you.":
            the_person "But...? Come on [the_person.mc_title], I really need your help."
            mc.name "Well, at the lab we've been running some experiements, but we need some test subjects."
            mc.name "I can bring home some of the stuff we're working on and if you let me test it on you I can pay you for it."
            the_person "It's not going to turn me into a lizard or something, right?"
            mc.name "Obviously not. It's just a liquid that you'd need to drink, then I'll watch to see how it affects you over the next few hours."
            the_person "What is it going to do?"
            mc.name "That's what we're trying to find out."
            $ the_person.draw_person(emotion = "happy")
            "[the_person.possessive_title] thinks about it for a moment, then nods."
            the_person "Okay, but I want $50 each time."
            mc.name "You drive a hard bargain sis. You've got a deal."
            "You shake on it."
            $ the_person.change_obedience(5)
            the_person "Thank you so much [the_person.mc_title]. Uh, if Mom asks just say I got a part time job."
            mc.name "Sure thing. I'll come see you when I have something for you to test."
            "[the_person.title] gives you one last smile then leaves your room, shutting the door behind her."
            $ mc.business.event_triggers_dict["sister_serum_test"] = True

        "Ask [the_person.title] to leave you alone.":
            the_person "But...?"
            mc.name "But I was just about to head to bed, so if you could let me get some sleep that would be a huge help."
            $ the_person.draw_person(emotion = "sad")
            $ the_person.change_happiness(-5)
            "[the_person.title] pouts and crosses her arms. She leaves your room in a huff."
            $ mc.business.event_triggers_dict["sister_needs_reintro"] = True

    $ clear_scene()
    return

label sister_reintro_label(the_person):
    #If you turn your sister away the first time you can approach her and ask to have her test serums anyways.
    mc.name "So [the_person.title], are you still looking for some work to do?"
    $ the_person.draw_person(emotion = "happy")
    the_person "Oh my god yes! Do you have something for me to do?"
    mc.name "Well, at the lab we've been running some experiements, but we need some test subjects."
    mc.name "I can bring home some of the stuff we're working on and if you let me test it on you I can pay you for it."
    the_person "It's not going to turn me into a lizard or something, right?"
    mc.name "Obviously not. It's just a liquid that you'd need to drink, then I'll watch to see how it affects you over the next few hours."
    the_person "What is it going to do?"
    mc.name "That's what we're trying to find out."
    $ the_person.draw_person(emotion = "happy")
    "[the_person.possessive_title] thinks about it for a moment, then nods."
    the_person "Okay, but I want $50 each time."
    mc.name "You drive a hard bargain sis. You've got a deal."
    "You shake on it."
    $ the_person.change_obedience(5)
    the_person "Thank you so much [the_person.mc_title]. Uh, if Mom asks just say I got a part time job."
    mc.name "Sure thing. I'll let you know when I have something for you to test."
    $ mc.business.event_triggers_dict["sister_needs_reintro"] = False
    $ mc.business.event_triggers_dict["sister_serum_test"] = True
    return

label sister_serum_test_label(the_person):
    #Give your sister some serum to test for cash.
    mc.name "Hey [the_person.title], I have something for you to test out for me."
    the_person "Alright, $50 and I'll try it."
    call give_serum(the_person) from _call_give_serum_7
    if _return:
        $ mc.business.change_funds(-50)
        "You give [the_person.possessive_title] the cash and the serum. She puts the money away then drinks the serum, handing back the empty vial."
        $ the_person.change_obedience(1)
        the_person "Easiest fifty bucks I've ever earned. I guess you can hang around and keep an eye on me if it's important for your research."
        if mc.business.event_triggers_dict.get("sister_serum_test_count", False):
            $ mc.business.event_triggers_dict["sister_serum_test_count"] += 1
        else:
            $ mc.business.event_triggers_dict["sister_serum_test_count"] = 1


    else:
        mc.name "Sorry [the_person.title], I guess I don't actually have anything for you to test."
        the_person "Ugh, come on [the_person.mc_title], you know I need the money!"
        mc.name "I'll find something for you to test, promise."
    return

label sister_strip_intro_label(the_person):
    #Give your sister some cash in exchange for her stripping. Higher sluttiness means she'll strip more (for less).
    $ bedroom.show_background()
    "There's a knock at your bedroom door."
    mc.name "Come in."
    $ the_person.draw_person()
    the_person "Hey [the_person.mc_title], can I talk to you about something?"
    "[the_person.possessive_title] comes into your room and shuts the door behind her. She seems nervous, avoiding eye contact as she comes closer."
    mc.name "Any time, what's up?"
    the_person "You know how I've been testing some of that lab stuff you make? For money?"
    mc.name "Yeah."
    the_person "Well I've been out shopping, and Mom would {i}kill{/i} me if she knew how much I was spending, so I was hoping you could pay me some more."
    mc.name "Sorry [the_person.title], I don't have anything for you to test right now."
    $ the_person.draw_person(emotion = "sad")
    the_person "Oh come on [the_person.mc_title], don't you have anything I could do? I really need the money now."
    "[the_person.possessive_title] puts her arms behind her back and pouts at you."
    menu:
        "Pay her to strip for you.":
            call sister_strip_explanation(the_person)


        "Tell her to leave.":
            mc.name "I just don't have anything to give you [the_person.title]. I promise if I think of anything I'll come to you right away."
            the_person "Ugh... fine."
            "She turns and leaves your room, disappointed."
            $ the_person.change_happiness(-5)
            $ mc.business.event_triggers_dict["sister_strip_reintro"] = True

    $ clear_scene()
    return

label sister_strip_reintro_label(the_person):
    mc.name "I've been thinking about some stuff you could do for me [the_person.title]. Are you still interested in earning some more money?"
    $ the_person.draw_person(emotion = "happy")
    the_person "Yes! What do you want me to do?"

    call sister_strip_explanation(the_person)

    $ mc.business.event_triggers_dict["sister_strip_reintro"] = False
    return

label sister_strip_explanation(the_person):
    #Pulls out the explanation part of the strip intro so it's not duplicated
    mc.name "I've been busy getting my business running and earning all of this money I'm going to be paying you, so I haven't had a chance to meet many people."
    mc.name "It's been a while since I was able to just appreciate the looks of a hot woman."
    the_person "What are... what are you suggesting?"
    mc.name "I'll pay you if you just stand around and let me look at you. Maybe take some of your clothing off, if you're comfortable with it."
    the_person "So you want me to give you a strip show?"
    "You nod."
    "[the_person.possessive_title] seems surprised, but not particularly offended by the idea. She takes a long moment to consider it."
    $ mc.change_locked_clarity(20)
    the_person "Okay, I'll do it. I want $100 up front, plus a little extra if you want me to take anything off."
    mc.name "I think that's reasonable."
    $ the_person.change_obedience(5)
    $ mc.business.event_triggers_dict["sister_strip"] = True
    the_person "And obviously you can't touch me. Or yourself. And you can {i}never{/i} tell Mom about it."
    mc.name "Don't worry [the_person.title], I promise I won't make it weird."
    "[the_person.title] nods. There's a long silence before she speaks again."
    the_person "So... do you want me to do it for you now?"
    menu:
        "Ask her to strip for you." if mc.business.has_funds(100):
            mc.name "I don't see why not."
            $ mc.business.change_funds(-100)
            "You pull a hundred dollars out of your wallet and hand it over to [the_person.possessive_title]. She tucks it away and gets ready."
            call strip_tease(the_person, for_pay = True)

        "Ask her to strip for you.\n{size=22}Requires: $100{/size} (disabled)" if not mc.business.has_funds(100):
            pass

        "Not right now.":
            mc.name "Not right now. I'll come find you if I'm interested, okay?"
            the_person "Okay. Thanks for helping me out [the_person.mc_title], you're a life saver."
            "[the_person.title] leaves your room and closes the door behind her."
    return

label sister_strip_label(the_person):
    #A short intro so that we can reuse the pay_strip_scene with other characters if we want.
    mc.name "So [the_person.title], are you interested in earning a hundred dollars?"
    if the_person.effective_sluttiness("underwear_nudity") < 50:
        the_person "Oh, do you want me to... show off for you?"
    else:
        the_person "You want me to strip down for you?"
    $ mc.business.change_funds(-100)
    $ the_person.change_obedience(1)
    "You nod and sit down on [the_person.possessive_title]'s bed. She holds her hand out and you hand over her money."
    "She tucks the money away and gets ready in front of you."
    call strip_tease(the_person, for_pay = True)
    return

label sister_offer_to_hire(the_person):
    #TODO: If you've talked to Mom about this already a different event is added.
    if the_person.event_triggers_dict.get("dropout_convince_progress", 0) == 2:
        call sister_offer_to_hire_2(the_person)
    else:
        mc.name "So, have you ever thought of getting a job?"
        the_person "I don't have the time for one! Between school and posting to InstaPic I'm way too busy!"
        mc.name "Alright, I've got an idea for you then."
        "She raises a curious eyebrow and waits for you to continue."
        mc.name "Drop out of school and come work for me."
        the_person "What? God, I couldn't do that!"
        mc.name "Why not? Do you really think your English degree is going to get you a better job?"
        "[the_person.possessive_title] pouts."
        the_person "Shut up. Mom would never let me drop out."
        mc.name "Is that the only thing stopping you? If I convince [mom.title] you'll drop out and come work for me?"
        "She rolls her eyes dramatically, but takes a few moments to think."
        the_person "I don't know... Maybe. It doesn't matter, you'll never convince [mom.title]."
        mc.name "You leave that to me. I can be very convincing."
        if the_person.event_triggers_dict.get("dropout_convince_progress", 0) == 0:
            python:
                dropout_convince_action = Action("Let " + the_person.title + " drop out.", mother_sister_dropout_convince_requirement, "mother_sister_dropout_convince_label",
                    menu_tooltip = "Convince " + mom.title + " to let her daughter drop out of school and come work for you.")
                mom.get_role_reference(mother_role).actions.append(dropout_convince_action)
                the_person.event_triggers_dict["dropout_convince_progress"] = 1
    return

label sister_offer_to_hire_2(the_person):
    # Called after you've convinced Mom to let her drop out of school.
    mc.name "So, given any more thought about coming to work for me?"
    the_person "What's there to think about? Unless Mom is going to let me drop out of school I don't have the time."
    mc.name "Well I have some good news..."
    "Her jaw drops in surprise."
    the_person "No... She didn't really say I could drop out, did she? How did you do it?"
    mc.name "Don't worry about that, the important point thing is that she said yes."
    mc.name "So, interested in a job?"
    "[the_person.possessive_title] thinks for a long moment, clearly unsure."
    the_person "I don't know..."
    menu:
        "You hate school." if the_person.get_known_opinion_score("research work") <= -2:
            mc.name "Why do you want to stay there? You hate it at school."
            mc.name "You complain about it every time you come home."
            the_person "Yeah... It does suck pretty hard."
            "That seems to help her make up her mind."
            the_person "Screw it, I'll do it!"
            mc.name "That's the brave little sister I know! Now, let's see where you might fit in..."
            call stranger_hire_result(the_person)
            if _return:
                mc.name "There we go. All settled."
                the_person "Wow, I'm actually really excited!"
                mc.name "Good to hear, I want to see all that enthusiasm in the office."
                $ the_person.event_triggers_dict["dropout_convince_progress"] = 3
            else:
                mc.name "I'm going to need to get things ready before we can take on anyone else, actually."
                mc.name "So uh... don't drop out just yet, alright?"
                "She pouts but nods."
                the_person "Fiiiiine."


        "You hate school.\nRequires: Hates research work (disabled)" if the_person.get_known_opinion_score("research work") -2:
            pass

        "We'll get to work together!" if the_person.has_role(girlfriend_role):
            mc.name "Think about how much more time we'll have to spend together."
            mc.name "Wouldn't that be nice?"
            "She smiles and nods meekly."
            the_person "I guess that would be pretty fun. You really think I can do this?"
            mc.name "You'll be perfect for the job [the_person.title]. I know it."
            "Her resolve hardens and she nods her head with determination."
            the_person "Okay, I'll do it!"
            mc.name "That's the brave little sister I know! Now, let's see where you might fit in..."
            call stranger_hire_result(the_person)
            if _return:
                mc.name "There we go. All settled."
                the_person "Wow, I'm actually really excited!"
                mc.name "Good to hear, I want to see all that enthusiasm in the office."
                $ the_person.event_triggers_dict["dropout_convince_progress"] = 3
            else:
                mc.name "I'm going to need to get things ready before we can take on anyone else, actually."
                mc.name "So uh... don't drop out just yet, alright?"
                "She pouts but nods."
                the_person "Fiiiiine."

        "We'll get to work together!\nRequires: Make her your girlfriend (disabled)" if not the_person.has_role(girlfriend_role):
            pass

        "I'll double your normal pay.":
            mc.name "I'll pay you double what I would normaly pay someone with your experience. How about that?"
            the_person "It's not about the money... How much money would that be?"
            $ the_person.salary_modifier = 2.0
            $ predicted_amount = the_person.calculate_base_salary()
            mc.name "$[predicted_amount]. Per day."
            "That gets her full attention. She pretends to think for a moment before making her decision."
            the_person "Okay, I'll do it!"
            mc.name "That's the brave little sister I know! Now, let's see where you might fit in..."
            call stranger_hire_result(the_person)
            if _return:
                mc.name "There we go. All settled."
                the_person "Wow, I'm actually really excited!"
                mc.name "Good to hear, I want to see all that enthusiasm in the office."
                $ the_person.event_triggers_dict["dropout_convince_progress"] = 3
            else:
                mc.name "I'm going to need to get things ready before we can take on anyone else, actually."
                mc.name "So uh... don't drop out just yet, alright?"
                "She pouts but nods."
                the_person "Fiiiiine."

        "Nevermind.":
            mc.name "If you don't want to, don't worry about it."
            mc.name "The offer is open if you change your mind."
            the_person "Thanks [the_person.mc_title]. I'll think about it."

    return

label mother_sister_dropout_convince_label(the_person):
    mc.name "I need to talk to you about [lily.title]."
    "She frowns, looking converned."
    the_person "What do you mean? Is everything okay?"
    mc.name "It's fine, but [lily.title] wants to drop out of school."
    the_person "She... WHAT?"
    "[the_person.possessive_title] shakes her head in immediate refusal."
    the_person "Nonsense! Her education is so important, she can't abandon that just because it's difficult!"
    mc.name "She wants to drop out so she can come work for me. I've got a job lined up for her already."
    the_person "Well you're going to have to change your plans. She can't drop out of school. That's final!"
    menu:
        "We need the money!" if mom.has_job(unemployed_job):
            mc.name "We need the money [the_person.title], I can't be the only person with a job here!"
            "She pouts and wants to argue, but the truth of the statement sinks in."
            the_person "She shouldn't have to give up her education just for us..."
            mc.name "She can go back to school in a few years. I need the help, and I know I can trust her."
            "[the_person.possessive_title] looks conflicted, but finally she nods."
            the_person "Okay, okay. Only if this is what she really wants to do though!"
            mc.name "Thank you for understanding [the_person.title], I'll let her know."
            $ lily.event_triggers_dict["dropout_convince_progress"] = 2


        "We need the money!\nRequires: [the_person.title] is Unemployed (disabled)" if not mom.has_job(unemployed_job):
            pass

        "We'll all be working together." if the_person.has_role(employee_role):
            mc.name "We'll all be working together if [lily.title] comes to work for me."
            mc.name "Wouldn't that be great? The whole family, working as a team?"
            the_person "It would be nice to see both of you all day..."
            mc.name "she can go back to school in a few years. I just really need the help right now."
            "[the_person.possessive_title] looks conflicted, but finally she nods."
            the_person "Okay, okay. Only if this is what she really wants to do though!"
            mc.name "Thank you for understanding [the_person.title], I'll let her know."
            $ lily.event_triggers_dict["dropout_convince_progress"] = 2

        "We'll all be working together.\nRequires: Hire [the_person.title] (disabled)" if not the_person.has_role(employee_role):
            pass

        "She's never going to graduate..." if lily.int <= 1:
            mc.name "She's never going to graduate [the_person.title]. Her grades are terrible!"
            the_person "Well... She's trying her hardest. That's what really matters."
            mc.name "No, having a career actually matters. I can give her real world experience."
            "[the_person.possessive_title]'s resolve seems to be wavering. You press your point."
            mc.name "The university just wants to milk her for tuition money. They'll string her along for years before they kick her out."
            mc.name "We've got to make sure to take care of her, right?"
            "[the_person.possessive_title] looks conflicted, but finally she nods."
            the_person "Never tell her I said this, but... you're right. Okay, you can hire her."
            the_person "But only if that's what she wants to do!"
            mc.name "Thank you for understanding [the_person.title], I'll let her know."
            $ lily.event_triggers_dict["dropout_convince_progress"] = 2

        "She's never going to graduate...\nRequires: [lily.title] Int 1 (disabled)" if lily.int > 1:
            pass

        "You need to let this happen." if the_person.obedience >= 150:
            mc.name "I'm sorry, but what you care doesn't really matter here [the_person.title]."
            mc.name "I need [lily.title] to work for me, which means I need you to get out of the way and let it happen."
            the_person "But what about her education... Her future?"
            mc.name "She can go back to school in a few years. The experience will look great on her resume."
            mc.name "Now I'm going to go tell her you're okay with this, and you aren't going to argue. Understood?"
            "[the_person.possessive_title] nods meekly."
            mc.name "Good."
            $ lily.event_triggers_dict["dropout_convince_progress"] = 2

        "You need to let this happen.\nRequires: 150 Obedience (disabled)" if the_person.obedience < 150:
            pass

        "Nevermind.":
            mc.name "You know, I think you're right... Her education is an important part of her life."
            the_person "Good. I'm glad you understand."

    return


label sister_cam_girl_intro_label(the_person):
    # Your sister comes to you asking for _more_ money, this time to buy a better computer.
    # "I have an idea to make money, right here at home. I just need to buy some equipment."
    # "I need a new computer. And a microphone. And a webcam."
    # "It's none of your business!"
    # Threaten to tell your Mom, she tells you that she's going to make some videos for her "premium instapic followers".
    # Offer to buy her the equipment in exchange for a cut.
    return

label sister_cam_girl_online_view_label(the_person):
    # Tune into one of your sisters shows. Give her cash to do things as an anonymous doner.
    return

label sister_cam_girl_in_person_view_label(the_person):
    # Crash your sister's room and watch/join in on the show. At very high sluttiness she has you pose as her "boyfriend" for various things.
    return

label sister_pregnant_report(the_person):
    #TODO: Special event called when your sister realises she's pregnant.
    return
