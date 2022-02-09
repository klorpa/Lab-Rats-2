# Holds all of the event stuff related to Jennifer's special taboo break quests.
# TODO: Add an on_day check to her role, if she has a broken sex taboo but you haven't completed the quest for it yet start this.
init -1 python:
    def mom_kissing_taboo_revisit_requirement(the_person):
        return True

    def mom_oral_taboo_revisit_requirement(the_person):
        return True

    def mom_anal_taboo_revisit_requirement(the_person):
        return True

    def mom_vaginal_taboo_revisit_requirement(the_person):
        return True

    def mom_kissing_quest_1_requirement(the_person):
        if not the_person.event_triggers_dict.get("mom_kissing_quest_active", False):
            return False
        elif the_person.event_triggers_dict.get("mom_kissing_quest_1_complete", False):
            return False
        elif time_of_day >= 4:
            return "Not enough time."
        elif mc.energy < 20:
            return "Not enough energy."
        else:
            return True

    def mom_kissing_quest_2_requirement(the_person):
        if not the_person.event_triggers_dict.get("mom_kissing_quest_active", False):
            return False
        elif the_person.event_triggers_dict.get("mom_kissing_quest_2_complete", False):
            return False
        elif time_of_day >= 4:
            return "Not enough time."
        elif mc.energy < 20:
            return "Not enough energy."
        else:
            return True

    def mom_kissing_quest_3_requirement(the_person):
        if not the_person.event_triggers_dict.get("mom_kissing_quest_active", False):
            return False
        elif the_person.event_triggers_dict.get("mom_kissing_quest_3_complete", False):
            return False
        elif time_of_day >= 4:
            return "Not enough time."
        elif mc.energy < 20:
            return "Not enough energy."
        else:
            return True

    def mom_kissing_quest_4_requirement(the_person):
        if not the_person.event_triggers_dict.get("mom_kissing_quest_active", False):
            return False
        elif the_person.event_triggers_dict.get("mom_kissing_quest_4_complete", False):
            return False
        elif time_of_day >= 4:
            return "Not enough time."
        elif mc.energy < 20:
            return "Not enough energy."
        else:
            return True

    def mom_kissing_taboo_break_revisit_complete_requirement(the_person):
        if not the_person.event_triggers_dict.get("mom_kissing_quest_active", False):
            return False
        elif the_person.event_triggers_dict.get("kissing_taboo_revisit_quest_progress", 0) >= 4:
            return True
        elif the_person.event_triggers_dict.get("kissing_taboo_revisit_quest_progress", 0) < 4:
            return str(the_person.event_triggers_dict.get("kissing_taboo_revisit_quest_progress", 0)) + "/4 chores complete."
        return False

    def mom_oral_quest_complete_requirement(the_person):
        if not the_person.event_triggers_dict.get("mom_oral_quest_active", False):
            return False
        elif aunt.love < 40:
            return "Requires: " + aunt.title + " has 40 Love"
        else:
            return True

    def mom_anal_quest_complete_requirement(the_person):
        if not the_person.event_triggers_dict.get("mom_anal_quest_active", False):
            return False
        elif not mc.business.has_funds(5000):
            return ""
        else:
            return True

    def mom_vaginal_quest_2_requirement(the_person):
        if not the_person.event_triggers_dict.get("mom_vaginal_quest_active", False):
            return False
        elif not the_person.event_triggers_dict.get("mom_vaginal_quest_progress", 0) == 1:
            return False
        elif time_of_day == 4:
            return "Not enough time."
        else:
            return True

    def mom_vaginal_quest_3_requirement(the_person, trigger_day):
        if day < trigger_day:
            return False
        elif time_of_day == 4: #Prevents the event from triggering in the morning instead of the evening.
            return False
        elif mom.get_next_destination() == mom_bedroom: #Check that she will be moving into the bedroom on her _next_ Move phase (ie after this crisis check is made).
            return False
        else:
            return True

    def mom_vaginal_quest_complete_requirement(the_person):
        if mom_bedroom.has_person(the_person):
            return True
        else:
            return False


label mom_kissing_taboo_break_revisit(the_person):
    #TODO Maybe have a version where you've also broken a _higher_ taboo already.
    $ first_time = the_person.event_triggers_dict.get("kissing_revisit_count", 0) <= 1
    $ noteable_taboo = "nudity"
    if "touching_body" in the_person.event_triggers_dict.get("kissing_revisit_restore_taboos", []):
        $ noteable_taboo = "touching"
    elif "touching_vagina" in the_person.event_triggers_dict.get("kissing_revisit_restore_taboos", []):
        $ noteable_taboo = "touching"
    elif "kissing" in the_person.event_triggers_dict.get("kissing_revisit_restore_taboos", []):
        $ noteable_taboo = "kissing"
    $ the_person.draw_person()
    "[the_person.possessive_title] smiles awkwardly at you when she sees you."
    the_person "[the_person.mc_title], I need to talk to you."
    mc.name "Okay, is everything alright?"
    if first_time:
        the_person "Everything is fine, it's just about... well..."
        if noteable_taboo == "touching":
            the_person "It's about you touching me." #TODO: Have a non-con varient where you ordered her.
            mc.name "[the_person.title], you said it was fine. You seemed like you liked it."
            the_person "I know, I know. I should have stopped you right away, but I wanted to be a cool mom and not make a big deal about it!"
            the_person "But it's not right for you to have your hands on your mother like that."


        elif noteable_taboo == "kissing":
            the_person "It's about us kissing."
            mc.name "[the_person.title], you said it was fine. You seemed like you liked it."
            the_person "I know, I know. I should have stopped you right away, but I wanted to be a cool mom and not make a big deal about it!"
            the_person "But it's not something we can do again. I want to be close, but that was taking it a step too far."

        else: #noteable_taboo == "nudity"
            the_person "It's about you seeing me naked."
            mc.name "It's no big deal, right [the_person.title]? It's nothing to be embarrassed about."
            the_person "I know, but it sets a bad example. I don't want you to think that it is normal, or that we could go any further."

    else:
        the_person "Everything is fine, it's just that we took things a little too far again."
        mc.name "You seemed fine with it..."
        the_person "I know, and that's my fault. I should have put an end to things earlier."

    the_person "You didn't do anything wrong, but we can't do it again. Understood?"

    $ kissing_count_threshold = 3 - the_person.get_opinion_score("kissing")


    menu:
        "Didn't you like it?" if the_person.get_known_opinion_score("incest") > 0:
            mc.name "Why not [the_person.title]? I know you liked it just as much as I did."
            the_person "That's not... I don't..."
            mc.name "It's fine, we don't need to make a big deal about it. It's just the way we are."
            "[the_person.possessive_title] seems torn."
            the_person "You're really sure?"
            mc.name "Of course [the_person.title]. Why wouldn't I want to be closer to you?"
            "She takes a deep breath and nods her approval."
            the_person "You're right. Thank you, this was really weighing on me."
            $ the_person.event_triggers_dict["kissing_revisit_complete"] = True
            python:
                for a_taboo in the_person.event_triggers_dict.get("kissing_revisit_restore_taboos", []):
                    the_person.break_taboo(a_taboo, add_to_log = False, fire_event = False)

        "Didn't you like it?\nRequires: Likes Incest (disabled)" if the_person.get_known_opinion_score("incest") <= 0:
            pass

        "But it keeps happening..." if the_person.event_triggers_dict.get("kissing_revisit_count", 0) >= kissing_count_threshold:
            mc.name "If it needs to stop why does it keep happening [the_person.title]?"
            mc.name "Let's stop pretending. This is normal now, you don't need to beat yourself up about it."
            "[the_person.possessive_title] seems like she wants to argue, but even she can understand you're right."
            the_person "I suppose I can put up with this, but we can't take it any further."
            $ the_person.event_triggers_dict["kissing_revisit_complete"] = True
            python:
                for a_taboo in the_person.event_triggers_dict.get("kissing_revisit_restore_taboos", []):
                    the_person.break_taboo(a_taboo, add_to_log = False, fire_event = False)

        "But it keeps happening...\nRequires: Break taboo [kissing_count_threshold] times (disabled)" if the_person.event_triggers_dict.get("kissing_revisit_count", 0) < kissing_count_threshold:
            pass

        "What can I do to convince you?" if not the_person.event_triggers_dict.get("mom_kissing_quest_active", False):
            mc.name "It's not a big deal [the_person.title], it's just part of how we love each other."
            mc.name "What can I do to convince you? There must be something."
            "[the_person.possessive_title] thinks for a moment, tapping her finger on her chin until an idea comes to her."
            the_person "Well..."
            the_person "If you want me to be okay with this you need to show me that you're mature enough."
            mc.name "Of course [the_person.title]. What can I do?"
            the_person "I have chores that need to be done around the house. Work has been so busy, I haven't been keeping up with them."
            the_person "If you take care of them I'll know I can trust you to be mature about all of this."
            "She grabs a piece of paper, a pen, and writes out the chores. She hands the note over to you."
            "1. Do your laundry."
            "2. Clean the bathroom."
            "3. Vaccum the living room."
            "4. Clean the fridge."
            "You read it over and nod."
            mc.name "Alright [the_person.title], I can do this. And when I do you won't mind if we..."
            the_person "We can talk about that later, alright? Just start by getting your chores done."
            "You pocket the list and give her a quick hug."

            $ the_person.event_triggers_dict["mom_kissing_quest_active"] = True

            $ bedroom.actions.append(Action("Clean your room. -20 {image=gui/extra_images/energy_token.png},{image=gui/heart/Time_Advance.png}", mom_kissing_quest_1_requirement, "mom_kissing_taboo_break_revisit_quest_1", args = the_person, requirement_args = the_person))
            $ hall.actions.append(Action("Clean the bathroom. -20 {image=gui/extra_images/energy_token.png},{image=gui/heart/Time_Advance.png}", mom_kissing_quest_2_requirement, "mom_kissing_taboo_break_revisit_quest_2", args = the_person, requirement_args = the_person))
            $ hall.actions.append(Action("Clean the living room. -20 {image=gui/extra_images/energy_token.png},{image=gui/heart/Time_Advance.png}", mom_kissing_quest_3_requirement, "mom_kissing_taboo_break_revisit_quest_3", args = the_person, requirement_args = the_person))
            $ kitchen.actions.append(Action("Clean the fridge. -20 {image=gui/extra_images/energy_token.png},{image=gui/heart/Time_Advance.png}", mom_kissing_quest_4_requirement, "mom_kissing_taboo_break_revisit_quest_4", args = the_person, requirement_args = the_person))

            $ the_person.get_role_reference(mother_role).actions.append(Action("Check back in...", mom_kissing_taboo_break_revisit_complete_requirement , "mom_kissing_taboo_break_revisit_complete"))

            $ the_person.change_slut(-10)
            $ mc.log_event(the_person.title + "'s taboos restored!", "float_text_red")

        "Understood.":
            mc.name "I understand."
            "She smiles happily and motions for you to hug her."
            the_person "Come here... I know you love me, you just need to show it in ways that are a little more appropriate."
            $ the_person.change_slut(-10)
            $ mc.log_event(the_person.title + "'s taboos restored!", "float_text_red")

    $ clear_scene()
    return

label mom_kissing_taboo_break_revisit_quest_1(the_person):
    "You look around your room, in particular the dirty clothes you've left strewn around."
    "You get down to work, collecting everything into a basket until it's full and then bring it to the laundry room."
    "You take your best guess at the settings and head back to clean up the rest of your room."
    "It takes some time and hard work, but soon enough you have a tidy room and a basket of clean clothes to show for your effort."
    $ mc.change_energy(-20)
    $ the_person.event_triggers_dict["kissing_taboo_revisit_quest_progress"] = the_person.event_triggers_dict.get("kissing_taboo_revisit_quest_progress", 0) + 1
    $ the_person.event_triggers_dict["mom_kissing_quest_1_complete"] = True
    if the_person.event_triggers_dict.get("kissing_taboo_revisit_quest_progress", 0) == 4:
        "That's the last chore. Time to talk to [the_person.possessive_title]."
    call advance_time()
    return

label mom_kissing_taboo_break_revisit_quest_2(the_person):
    "You collect some cleaning supplies and get to work."
    "After a little bit of scrubbing washing you have the bathroom tidied up to the point that [the_person.possessive_title] should be satisfied."
    $ mc.change_energy(-20)
    $ the_person.event_triggers_dict["kissing_taboo_revisit_quest_progress"] = the_person.event_triggers_dict.get("kissing_taboo_revisit_quest_progress", 0) + 1
    $ the_person.event_triggers_dict["mom_kissing_quest_2_complete"] = True
    if the_person.event_triggers_dict.get("kissing_taboo_revisit_quest_progress", 0) == 4:
        "That's the last chore. Time to talk to [the_person.possessive_title]."
    call advance_time()
    return

label mom_kissing_taboo_break_revisit_quest_3(the_person):
    "You grab the vacuum from the laundry room and plug it in."
    "You run it around the living room, making sure to get under the coffee table and couch."
    "When you figure you've done enough to make [the_person.possessive_title] happy you finish up."
    $ mc.change_energy(-20)
    $ the_person.event_triggers_dict["kissing_taboo_revisit_quest_progress"] = the_person.event_triggers_dict.get("kissing_taboo_revisit_quest_progress", 0) + 1
    $ the_person.event_triggers_dict["mom_kissing_quest_3_complete"] = True
    if the_person.event_triggers_dict.get("kissing_taboo_revisit_quest_progress", 0) == 4:
        "That's the last chore. Time to talk to [the_person.possessive_title]."
    call advance_time()
    return

label mom_kissing_taboo_break_revisit_quest_4(the_person):
    "You open the fridge and size up your task."
    "You start out by moving all of the food and leftovers onto the counter, then wipe down all of the platforms in the fridge."
    "Then you organise things as you put them back in, taking time to throw out anything too old."
    "You smile as you close the door again. [the_person.possessive_title] will have to be happy about the job you've done."
    $ mc.change_energy(-20)
    $ the_person.event_triggers_dict["kissing_taboo_revisit_quest_progress"] = the_person.event_triggers_dict.get("kissing_taboo_revisit_quest_progress", 0) + 1
    $ the_person.event_triggers_dict["mom_kissing_quest_4_complete"] = True
    if the_person.event_triggers_dict.get("kissing_taboo_revisit_quest_progress", 0) == 4:
        "That's the last chore. Time to talk to [the_person.possessive_title]."
    call advance_time()
    return

label mom_kissing_taboo_break_revisit_complete(the_person):
    mc.name "[the_person.title], I've finished my chores."
    the_person "You have, hmm? Well, let's go have a look."
    "[the_person.possessive_title] tours around the house. She smiles and nods as she sees each task has been finished."
    the_person "Well, I suppose you have. Thank you [the_person.mc_title]."
    mc.name "So does this mean we can..."
    "She cuts you off with a wave of her hand and a laugh."
    the_person "As long as you're mature about it and understand we can't take it any further."
    $ the_person.event_triggers_dict["mom_kissing_quest_active"] = False
    $ the_person.event_triggers_dict["kissing_revisit_complete"] = True
    $ the_person.change_slut(10, 40)
    python:
        for a_taboo in the_person.event_triggers_dict.get("kissing_revisit_restore_taboos", []):
            the_person.break_taboo(a_taboo)
    mc.name "Of course [the_person.title], I promise."
    return

label mom_oral_taboo_break_revisit(the_person):
    $ the_person.draw_person()
    the_person "[the_person.mc_title], can we talk?"
    "[the_person.title] hurries over to you, looking a little uncomfortable."
    mc.name "Sure, what's up?"
    $ first_time = the_person.event_triggers_dict.get("oral_revisit_count", 0) <= 1
    $ noteable_taboo = "cunn"
    if the_person.has_broken_taboo("sucking_cock"):
        $ noteable_taboo == "blowjob"
    if first_time:
        if noteable_taboo == "blowjob":
            the_person "It's the, uh... fun we had together."
            mc.name "You mean the blowjob you gave me?"

        else: #noteable_taboo == "cunn"
            the_person "It's the, uh... fun we had together."
            mc.name "You mean me licking your pussy?"

        "She blushes and looks away for a moment."
        the_person "Yes, that. I've been thinking, and that's just not something a mother and her son should do."
        mc.name "Why not? You were fine with it yesterday, and we both enjoyed it."
        the_person "That's just not the point! I'm still fine if we're a little more physical with our love than most."
        the_person "But I just can't cross that line with you again."
    else:
        the_person "It's about our... encounter yesterday. It was a moment of weakness from me, it's not something we can do again."

    the_person "I hope you can understand."

    $ oral_count_threshold = 4 - the_person.get_opinion_score(["giving blowjobs", "getting head"])
    menu:
        "It turned you on, didn't it?" if the_person.get_known_opinion_score("incest") > 0:
            mc.name "I know it turned you on too [the_person.title], why bother pretending?"
            the_person "I... it didnt... I didn't..."
            "She blushes and stammers, obviously unwilling to admit it."
            mc.name "Don't worry, it will be our little secret. Other people might not understand, but I do."
            the_person "You do? I know it's wrong, but somehow that just gets me more excited."
            the_person "Oh, I'm such a terrible mother. I shouldn't feel like this!"
            mc.name "You're a wonderful mom, and you've been one long enough that you deserve a little break."
            mc.name "So go ahead, be a little kinky [the_person.title]. You won't hear me complaining."
            the_person "No, I'm sure you won't be!"
            the_person "And this needs to be as far is this goes, understood? No further."
            mc.name "Of course [the_person.title], I understand."
            "She gives you a smile and a nod of approval."
            the_person "Good. I'm glad we were able to have this talk."
            $ the_person.event_triggers_dict["oral_revisit_complete"] = True
            python:
                for a_taboo in the_person.event_triggers_dict.get("oral_revisit_restore_taboos", []):
                    the_person.break_taboo(a_taboo, add_to_log = False, fire_event = False)

        "It turned you on, didn't it?\nRequires: Likes Incest (disabled)" if the_person.get_known_opinion_score("incest") <= 0:
            pass


        "But it keeps happening..." if the_person.event_triggers_dict.get("oral_revisit_count", 0) >= oral_count_threshold:
                mc.name "If it needs to stop why does it keep happening [the_person.title]?"
                the_person "That's because... I just..."
                "She stumbles over her words, unable to defend her actions."
                mc.name "We should just accept that it's normal. No point in fighting it."
                python:
                    for a_taboo in the_person.event_triggers_dict.get("oral_revisit_restore_taboos", []):
                        the_person.break_taboo(a_taboo, add_to_log = False, fire_event = False)
                $ the_person.event_triggers_dict["oral_revisit_complete"] = True

        "But it keeps happening...\nRequires: Break taboo [oral_count_threshold] times (disabled)" if the_person.event_triggers_dict.get("oral_revisit_count", 0) < oral_count_threshold:
            pass

        "What can I do to convince you?" if not the_person.event_triggers_dict.get("mom_oral_quest_active", False):
            mc.name "Please [the_person.title], I want to be close to you, and I think you want the same thing."
            mc.name "There must be something I can do to get you to change your mind."
            "She looks like she's about to say no, but pauses to think for a moment first."
            the_person "Well..."
            mc.name "Come on, just tell me what I need to do and I'll do it. For you."
            the_person "Okay, okay. If I'm going to allow this sillyness with you I need you to prove you can be more than just a horny boy."
            the_person "My sister just went through a divorce. She's lost the house, she's moved to a new city, and she has to take care of your cousin all by herself."
            the_person "I want you to spend time with her, make sure she's alright, and be a positive male influence on her life."
            the_person "If I hear good things back from her then... Well, then I'll consider giving you a {i}reward{/i} for it."

            $ the_person.event_triggers_dict["mom_oral_quest_active"] = True

            #We get the role reference here in case save/loading breaks that link (but it shouldn't, I think).
            $ the_person.get_role_reference(mother_role).actions.append(Action("Check back in...", mom_oral_quest_complete_requirement, "mom_oral_taboo_break_revisit_complete"))
            $ the_person.change_slut(-10)
            $ mc.log_event(the_person.title + "'s taboos restored!", "float_text_red")

        "Understood.":
            mc.name "I understand."
            the_person "Thank you [the_person.mc_title]. I've heard it's natural for boys to feel this way about their mothers..."
            "She opens her arms up and hugs you."
            the_person "We just need to find healthier outlets for your feelings."
            $ the_person.change_slut(-10)
            $ mc.log_event(the_person.title + "'s taboos restored!", "float_text_red")

    $ clear_scene()
    return

label mom_oral_taboo_break_revisit_complete(the_person):
    mc.name "So, I've been spending some time with [aunt.title] lately."
    the_person "I've heard! Every time I call her she's telling me that you came to visit and that you've been spending time with her!"
    the_person "It really makes me happy to hear that you're going out of your way to take look after the family."
    mc.name "It was no problem, really. I was happy to help her out."
    the_person "Mmhm? Are you sure you weren't doing it for some other reason?"
    "She gives you a knowing look and a mischievous smile."
    mc.name "Well, maybe a little..."
    "[the_person.possessive_title] rolls her eyes and laughs."
    python:
        for a_taboo in the_person.event_triggers_dict.get("oral_revisit_restore_taboos", []):
            the_person.break_taboo(a_taboo)

    $ the_person.event_triggers_dict["mom_oral_quest_active"] = False
    $ the_person.event_triggers_dict["oral_revisit_complete"] = True
    $ the_person.change_slut(10, 50)

    the_person "It means a lot to me either way."
    menu:
        "What about my reward?":
            mc.name "You said you'd give me a reward if I cheered your sister up."
            the_person "Oh yes, that..."
            "She laughs nervously and waves the idea away."
            the_person "Let's not push your luck, alright? But I won't make a big deal if something does happen. Deal?"
            menu:
                "Deal.":
                    mc.name "Alright, you've got a deal."
                    "She sighs with relief and smiles."
                    the_person "Thank you for understanding [the_person.mc_title]."

                "No, you promised!":
                    mc.name "You promised [the_person.title], that's why I did this! You didn't lie to me, did you?"
                    "[the_person.possessive_title] frowns at you."
                    the_person "[the_person.mc_title], you're being silly. Obviously I didn't lie to you, I..."
                    mc.name "Then I want my reward, and we both know what you were suggesting it was going to be."
                    "You catch her eyes flick down to your crotch, where your cock is already bulging against your pants."
                    the_person "I... Well... I suppose I might have suggested that, in passing..."
                    "She looks around nervously and sighs."
                    $ the_person.change_obedience(3)
                    $ the_person.change_love(-3)
                    the_person "Okay, fine. But don't expect this to go any further, alright?"
                    mc.name "Of course [the_person.title]."
                    the_person "Come on, let's go to your room."
                    $ mc.change_location(bedroom)
                    $ bedroom.show_background()
                    "She takes your hand and leads you to your own bedroom. She pats the side of your bed and waits for you to sit."
                    $ the_person.draw_person(position = "blowjob")
                    "When you've sat she gets onto her knees in front of you and sweeps her hair back behind her shoulders."
                    the_person "Okay, take it out for me."
                    "You comply, unzipping your pants and pulling them down to reveal your hard dick."
                    "[the_person.possessive_title] pauses when it springs free in front of her, momentarily stunned by the task in front of her."
                    mc.name "[the_person.title]?"
                    the_person "Right, uh... Enjoy yourself [the_person.mc_title], you've earned it."
                    "She squares her shoulders and leans forward, hesitating before her lips touch the tip of your cock."
                    "You can feel her warm breath, and for an agonizing moment you think she might stop there."
                    $ the_person.break_taboo("sucking_cock") #In case you got here by eating her out, so that taboo wasn't already broken.
                    "Then she kisses it, and that brief moment of contact is enough to break down any limits she might have had."
                    $ the_person.draw_person(position = "blowjob", special_modifier = "blowjob")
                    "She kisses it a few more times, each more passionate than the last, then slips the very top of it inside of her lips."
                    "After a moment of adjustment she has it inside of her mouth, tongue licking at the shaft as she sucks you off."
                    call fuck_person(the_person, private = True, start_position = blowjob, start_object = mc.location.get_object_with_trait("kneel"), skip_intro = True, girl_in_charge = True)
                    $ the_report = _return #TODO double check if we want something special here.
                    $ the_person.call_dialogue("sex_review", the_report = the_report)



        "Anything to make you happy.":
            mc.name "Anything to make you happy [the_person.title]."
            the_person "You're sweet. And I suppose you've shown me that you can be a mature, caring young man."
            the_person "So I'll try not to make a big deal out of it if you need some physical... relief, in the future."
            mc.name "What about right now?"
            "She laughs innocently and shakes her head."
            the_person "Don't push your luck. And don't expect this to go any further. I'm being very understanding as it is."


    return

label mom_vaginal_interupt(the_person):
    #TODO: Triggers before you can have vaginal sex in any way with her.
    #TODO: She tells you that you absolutely, positively cannot do this!
    #TODO: But... you can fuck her ass. Nothing wrong with that. Nope!
    #TODO: She offers you other things she'll do for you ("I'll use my mouth. You can fuck my mouth! Anything but my pussy!)
    if first_time: #TODO: Hook this up
        pass
    else:
        pass #TODO: Same as above, but greatly abreviated ("We can't do that! How about... You can use another hole)
    return

label mom_anal_taboo_break_revisit(the_person):
    $ the_person.draw_person()
    the_person "[the_person.mc_title], we need to talk..."
    "[the_person.possessive_title] hurries over to you. She seems to be some mix of nervous and embarrassed."
    mc.name "[the_person.title]? What's wrong."

    $ first_time = the_person.event_triggers_dict.get("anal_revisit_count", 0) <= 1

    if first_time:
        the_person "Yesterday we... we took things too far. Absolutely too far!"
        mc.name "What do you mean? I had a great time. I hope I wasn't too hard on you."
        "She frowns and shakes her head."
        the_person "No, that's not it at all! I mean we almost lost control!"
        the_person "What if I hadn't stopped you? We could have ended up having sex!"


    else:
        the_person "Yesterday we almost lost control again! If I didn't let you fuck my..."
        "She clears her throat."
        the_person "Well, you know. We could have ended up having real sex!"

    mc.name "Would that really be so bad? It probably would have felt a lot better for both of us."
    "Her glare tells you she doesn't agree."
    the_person "We can't go that far ever again. We can't even get close to it."
    the_person "I'm putting my foot down. No anal, ever again. Understood?"

    $ anal_count_threshold = 5 - the_person.get_opinion_score("anal sex")
    menu:
        "But you want more. I know you do." if the_person.get_known_opinion_score("incest") > 1:
            mc.name "But you loved it, right? I mean, you wanted to go all the way."
            "[the_person.possessive_title] gasps and shakes her head."
            the_person "No, of course not! I'm your mother, and it's not right!"
            mc.name "Right or wrong, it gets you wet. How often do you think about it? Do you touch yourself thinking about it?"
            "She shakes her head, but you think her breathing is getting just a little heavier, just a little faster."
            the_person "No, I... I've never... It's just a fantasy, and that's all it can ever be!"
            mc.name "But it doesn't have to be. I'm right here, and I want the same as you."
            the_person "You shouldn't... we shouldn't..."
            "Her works are softer. Her defenses are breaking down."
            mc.name "You can keep your pussy off limits, but there are other ways for us to have fun."
            "She looks into your eyes, cheeks flush with arousal."
            the_person "You mean more anal? It isn't really like we're having sex..."
            mc.name "But you still get to feel my cock inside of you. Filling you up."
            "[the_person.title] takes a moment to consider it, chest heaving with heavy breaths."
            the_person "And that's as far as it goes, right? Do you think you could be satisfied just fucking my... my..."
            mc.name "Go ahead, you can say it."
            the_person "Fucking my ass? Oh... I think I would like that, but I need you to promise me that's as far as it goes!"
            "She puts her hands on your arms and gazes deep into your eyes."
            mc.name "Of course [the_person.title], I promise."
            "She nods uncertainly."
            the_person "Okay... Okay then. We have a deal. Just a little bit of anal, and that will help us manage our urges."
            "She's muttering, talking mostly to herself as she tries to justify her feelings."
            $ the_person.break_taboo("anal_sex", add_to_log = False, fire_event = False)
            $ the_person.event_triggers_dict["anal_revisit_complete"] = True


        "But you want more. I know you do.\nRequires: Loves Incest (disabled)" if the_person.get_known_opinion_score("incest") <= 1:
            pass


        "But it keeps happening..." if the_person.event_triggers_dict.get("anal_revisit_count",0) >= anal_count_threshold:
                mc.name "Why bother fighting it if it just keeps happening [the_person.title]?"
                mc.name "Stop pretending you aren't part of the problem here."
                "She opens her mouth to argue, but she knows you're right."
                the_person "I... I don't know what else to do."
                mc.name "Just accept it. It's normal for us, even if it isn't normal for other people."
                "She frowns, but that seems to be good enough for her at this point."
                the_person "Maybe you're right..."
                $ the_person.break_taboo("anal_sex", add_to_log = False, fire_event = False)
                $ the_person.event_triggers_dict["anal_revisit_complete"] = True

        "But it keeps happening...\nRequires: Break taboo [anal_count_threshold] times (disabled)" if the_person.event_triggers_dict.get("anal_revisit_count",0) < anal_count_threshold:
            pass

        "What can I do to convince you?" if not the_person.event_triggers_dict.get("mom_anal_quest_active", False):
            mc.name "There must be some way I can change your mind [the_person.title]."
            the_person "Of course not, we can never have sex!"
            mc.name "Sure, but anal isn't really sex. It could be a safe way for us to manage these urges we have."
            the_person "That {i}you{/i} have."
            "She corrects you, obviously delusional."
            mc.name "Alright, my urges then. We've already done it once, why not make the best of it?"
            the_person "I... Well, I don't know if I can trust you."
            the_person "You're young, your desires can be so powerful. If you lose control you might slip up and... slip in."
            mc.name "Then let me prove myself to you. Come on, I'm an adult, let me prove it to you."
            "[the_person.possessive_title] seems unconvinced, but she does pause and think for a bit."
            the_person "Fine, you want to be an adult now? I want you to show me you can handle the cost of being one."
            the_person "I don't like to talk about it, but I've had to pay for a lot of things on credit since we remorgaged the house."
            the_person "It's five thousand dollars. If you can pay me back and be truely independant, well... Maybe then I can trust you."
            mc.name "Okay, I can do that [the_person.title]. For you, it's all worth it."
            "She smirks and shakes her head."
            the_person "It really seems like that dick of yours will motivate you to do anything."
            "She shrugs and smiles weakly."
            the_person "Well I'm glad we could reach some sort of agreement. I'll be very impressed if you manage this."
            $ the_person.change_slut(-10)
            $ mc.log_event(the_person.title + "'s taboos restored!", "float_text_red")
            $ the_person.event_triggers_dict["mom_anal_quest_active"] = True
            $ the_person.get_role_reference(mother_role).actions.append(Action("Pay off her debt. -$5000", mom_anal_quest_complete_requirement, "mom_anal_taboo_break_revisit_complete"))

        "Understood.":
            mc.name "I understand."
            "She nods sternly."
            the_person "Good. And this time I won't be so easily convinced! No matter how good it..."
            "[the_person.possessive_title] shakes the idea from her head."
            the_person "It won't happen! That's all!"
            $ the_person.change_slut(-10)
            $ mc.log_event(the_person.title + "'s taboos restored!", "float_text_red")

    $ clear_scene()
    return

label mom_anal_taboo_break_revisit_complete(the_person):

    $ the_person.event_triggers_dict["mom_anal_quest_active"] = False
    $ the_person.event_triggers_dict["anal_revisit_complete"] = True

    mc.name "[the_person.title], I have some money for you."
    the_person "Hmm? Money for what?"
    mc.name "Remember that talk we had. About paying off some of our debt?"
    the_person "Oh right, that. Well, let's see how much progress you've made, and..."
    mc.name "All of it. I have all of the money you need to pay it off."
    "[the_person.possessive_title] stares at you for a moment, not quite understanding."
    mc.name "The business has been doing well lately. Really well."
    "You show her your bank account balance on your phone."
    the_person "Oh my god, you really do..."
    menu:
        "Send her the money.":
            "With a few button presses all of the cash has been moved over."
            mc.name "There, that should let you pay off everything you owe."
            "[the_person.title] doesn't say anything for a long moment. Her mouth is slack."
            the_person "[the_person.mc_title]... I... I don't know what to say."
            mc.name "Thank you, maybe?"
            $ the_person.draw_person(emotion = "happy")
            $ the_person.change_happiness(30)
            $ the_person.change_love(10)
            "She nods happily and pulls you into a tight hug."
            the_person "Thank you! Thank you! Thank-you-thank-you-thank-you!"
            "You let her spin you around in a circle as she celebrates."
            "At length she lets you go and steps back with a sigh, grinning ear to ear."
            the_person "This is such a weight off of my shoulders [the_person.mc_title]! We can finally get ahead, save up some money!"
            the_person "Here..."
            $ mc.change_locked_clarity(10)
            "She leans forward and gives you a long, passionate kiss on the lips."
            the_person "Ah... and don't think I've forgotten what else I promised..."
            $ mc.change_locked_clarity(15)
            "You feel her hand reach down between your legs and cup your crotch. Your cock twitches in reaction, which makes her gasp."
            $ the_person.change_slut(10, 65)
            $ the_person.break_taboo("anal_sex")
            the_person "Oh yes, I'll have to take care of this later. No sex though, remember? You can only fuck my ass."
            "She nibbles fondles your cock for a moment longer, then steps back with a relieved laugh."


        "Claim your reward first.":
            mc.name "Now I can send this over, just as soon as we sort something else out..."
            "[the_person.possessive_title] cocks her head to the side, confused for a moment."
            the_person "I'm not sure what you mean [the_person.mc_title]..."
            mc.name "You said that if I got this sorted out I could fuck your ass. Right?"
            "She stammers over her words."
            the_person "I... You... I mean, I said that I'd think about it, that was all."
            mc.name "Take as long as you need to think about it. It {i}is{/i} a lot of money."
            the_person "[the_person.mc_title], I can't believe you're trying to extort me, your own mother!"
            mc.name "I'm not extorting you, I'm just want you to prove that you meant what you said."
            "She scowls, but you hold all the cards right now."
            "After a long, silent moment she rolls her eyes and sighs."
            $ the_person.change_obedience(5)
            $ the_person.change_love(-5)
            the_person "So if we... fool around a litle bit, you'll give me the money?"
            mc.name "Yep, that's the deal."
            the_person "Okay, fine. I suppose you have earned it..."
            the_person "You know, most women like a little foreplay before you try and put your cock inside of them."
            mc.name "That's why I love you [the_person.title], you aren't like most women."
            "She doesn't seem happy about that right now."
            $ the_person.change_slut(10, 65)
            $ the_person.break_taboo("anal_sex")

            $ mc.change_location(mom_bedroom)
            $ mc.location.show_background()
            the_person "Come on, if we're doing this I want to be in my own bed."
            "She leads you to her bedroom. She pats the bed and has you sit down while she gets ready."
            $ strip_list = the_person.outfit.get_full_strip_list()
            $ generalised_strip_description(the_person, strip_list)
            mc.name "Looking good [the_person.title]. Now get on your knees and shake that ass for me."
            "You unzip your pants and pull your hard cock out."
            "She still seems annoyed with you, but putting her eyes on your dick seems to soften her mood immediately."
            $ doggy_anal.redraw_scene(the_person)
            "[the_person.possessive_title] climbs onto the bed and rests her head on her pillow, shoulders on the matress and ass in the air."
            the_person "I'm all ready for you [the_person.mc_title], come fuck me."
            "You ditch your pants entirely and position yourself behind [the_person.title]. You tap your cock on her big ass cheeks, enjoying the way they jiggle."
            "You briefly consider fucking her pussy anyways, but decide that's a bridge too far right now."
            "Instead you spit on your cock to lube it up, then press the tip against [the_person.possessive_title]'s tight butthole."
            "She takes a deep breath as you start to stretch her open."
            "You take her slowly, inch by inch. [the_person.title] gasps and moans with every little movement you make."
            the_person "Oh, it feels so big like this! Ah..."
            "You start to pump, fucking her with the first half of your cock and getting deeper with every thrust."
            the_person "Ah... Oh... Fuck..."
            "With a little patience on your end, and a little grit on hers you eventually have your entire cock at work fucking her ass."
            call fuck_person(the_person, private = True, start_position = doggy_anal, start_object = mc.location.get_object_with_name("bed"), skip_intro = True)
            $ the_report = _return
            $ the_person.call_dialogue("sex_review", the_report = the_report)
    return

label mom_vaginal_taboo_break_revisit(the_person):
    $ the_person.draw_person()
    the_person "[the_person.mc_title], we need to talk."
    "[the_person.possessive_title] hurries up to you, wringing her hands together in front of her."
    if first_time:
        the_person "Listen... I know we both had a good time together, and I'm happy for that."
        the_person "But it was a mistake. My mistake. I just haven't felt like that in so, so long."
        the_person "We can still fool around, to help keep our urges under control, but we can't go that far again."

    else:
        the_person "It's about us having sex again... I know it was fun, and it really was fun, but we shouldn't be doing that."
        the_person "When I get excited I just lose control of myself, but... but I'm putting my foot down, we can't do that again!"

    $ vaginal_count_threshold = 8 - the_person.get_opinion_score("vaginal sex")

    menu:
        "Let me change your mind." if the_person.get_known_opinion_score("incest") > 0 and not the_person.event_triggers_dict.get("mom_vaginal_quest_active", False): #TDOO only if not on a quest
            mc.name "You don't really mean that [the_person.title]. You want me just as badly as I want you."
            mc.name "You have needs, and I know there's nobody else who can satisfy them like I can."
            $ the_person.change_slut(-10)
            $ mc.log_event(the_person.title + "'s taboos restored!", "float_text_red")
            "She shakes her head in denial, but you can tell that on some level she agrees."
            the_person "I wish I could talk to someone about this, someone who wouldn't judge me."
            mc.name "You can talk to me."
            the_person "I think we both know you're a little biased..."
            "[the_person.possessive_title] thinks about this for a moment."
            the_person "You know what, I'm going to ask online. I'm sure some other mother has gone through this before."
            "She nods, confident in her decision."
            the_person "I'll do it anonymously, of course! Yes, that sounds like a good idea."
            mc.name "I hope you can find the advice you need [the_person.title]."
            the_person "I'll let you know what they suggest, alright?"
            "You nod, and [the_person.title] seems happier now."
            "It's probably a good idea to make sure [the_person.possessive_title] only sees the advice you want her to see."


            $ the_person.event_triggers_dict["mom_vaginal_quest_active"] = True
            $ the_person.event_triggers_dict["mom_vaginal_quest_progress"] = 0

        "Let me change your mind.\nRequires: Likes Incest (disabled)" if the_person.get_known_opinion_score("incest") <= 0 and not the_person.event_triggers_dict.get("mom_vaginal_quest_active", False):
            pass

        "But we've fucked so many times already..." if the_person.event_triggers_dict.get("vaginal_revisit_count", 0) >= vaginal_count_threshold:
            mc.name "This is getting silly [the_person.title]. We've been fucking all this time..."
            the_person "We shouldn't!"
            mc.name "But we always do anyways!"
            mc.name "Why are you beating yourself up over this when you're just going to end up with my cock in you again anyways?"
            the_person "I... You shouldn't..."
            if the_person.sex_record.get("Vaginal Creampies",0) > 0:
                mc.name "I shouldn't have dumped my load inside you either, but we've already crossed that bridge."
                mc.name "You weren't complaining even when I could have knocked you up!"

            elif the_person.has_broken_taboo("condomless_sex"):
                mc.name "I've even fucked you bareback [the_person.title]. Short of knocking you up what can I do?"

            else:
                mc.name "You've told me that dozens of times, but I still love fucking you [the_person.title]. If it's wrong, I don't want to be right."
            "She tries to summon up some sort of response, but they all sound hollow when faced with the facts."
            $ the_person.break_taboo("vaginal_sex", add_to_log = False, fire_event = False)
            $ the_person.event_triggers_dict["vaginal_revisit_complete"] = True
            the_person "Maybe you're right..."
            mc.name "Of course I'm right, and you know you'll enjoy it a lot more if you just accept that you like it too."
            "She seems unconvinced, but manges a faint smile."


        "But we've fucked so many times already...\nRequires: Break taboo [vaginal_count_threshold] times (disabled)" if the_person.event_triggers_dict.get("vaginal_revisit_count", 0) < vaginal_count_threshold:
            pass


        "I understand.":
            mc.name "I understand."
            "She nods sternly."
            the_person "Good. And this time I won't be so easily convinced! No matter how good it..."
            "[the_person.possessive_title] shakes the idea from her head."
            $ the_person.change_slut(-10)
            $ mc.log_event(the_person.title + "'s taboos restored!", "float_text_red")
            the_person "It won't happen! That's all!"

    $ clear_scene()
    return

label mom_vaginal_taboo_break_revisit_quest_1(the_person):
    "You open the web browser and check the history."
    "You're tempted to see what [the_person.possessive_title] has been looking at on \"MILFSDaily.xxx\", but that's not what you're here for."
    "Below the obvious porn links you see a couple of recent visits to \"A_Mothers_Advice.net\"."
    "You restore the most recent page. It's a post by \"UncertainMommy\", asking for advice. You take a moment to read through it."
    "{b}(Advice Needed) Sex with my Son???{/b}" (what_style = "text_message_style")
    "VeryNaughtyMommy" "I have a very strange situation, and I need help from all of you girls!" (what_style = "text_message_style")
    "VeryNaughtyMommy" "Me and my son have always been very physical when we show our love (please don't judge)." (what_style = "text_message_style")
    "VeryNaughtyMommy" "It was strange at first, but we both enjoy it and I feel closer than ever." (what_style = "text_message_style")
    $ mc.change_locked_clarity(10)
    "VeryNaughtyMommy" "We've had sex (Please please don't judge, it had been so long!), and now he wants to make it a normal thing." (what_style = "text_message_style")
    "VeryNaughtyMommy" "So what do you girls think? I want to have more sex with my son, but I don't know if I should!" (what_style = "text_message_style")
    "You write down the site name along with [the_person.title]'s username so you can follow this up on your own computer."
    menu:
        "Read the responses.":
            "The post already has a few responses, so you scroll down and take a look at them."
            "SphinxyBaby" "This post went from 0 to 100 real quick!" (what_style = "text_message_style")
            "MTeresa" "What the heck is this post? Reported to moderator." (what_style = "text_message_style")
            "Jocasta1" "I wish my kids wanted me like this! Go get 'em VeryNaughtyMommy!" (what_style = "text_message_style")
            "SphinxyBaby" "@VeryNaughtyMommy, you mean stepson, right? You must, otherwise this story is crazy!" (what_style = "text_message_style")
            "It doesn't seem like public opinion is swinging your way."
            "Hopefully [the_person.possessive_title] doesn't check back until you've fixed that." (what_style = "text_message_style")

        "Finish up.":
            pass

    $ the_person.event_triggers_dict["mom_vaginal_quest_progress"] = 1
    $ bedroom.actions.append(Action("Check " + the_person.title + "'s advice post.", mom_vaginal_quest_2_requirement, "mom_vaginal_taboo_break_revisit_quest_2", args = the_person, requirement_args = the_person))

    return

label mom_vaginal_taboo_break_revisit_quest_2(the_person):
    "You go to \"A_Mothers_Advice.net\". [the_person.possessive_title]'s post is still up, and still gathering feedback."
    menu:
        "Message her directly first.":
            "A direct message is the best way to talk to her directly, and is a lot less likely to get you banned off of the site."
            call mom_advice_dm(the_person)
            "You still need to make sure her public post doesn't give her any silly ideas."
            call mom_advice_astroturf(the_person)

        "Astroturf her advice post first.":
            "The most important thing to do is make it look like most people on the site want her to fuck you."
            call mom_advice_astroturf(the_person)
            "Now you should write to her directly. She's more likely to listen to a private message, and it's less likely to get you banned off the site."
            call mom_advice_dm(the_person)

    "You sit back, feeling satisfied with your deception. There's nothing to do now but wait for [the_person.title] to make up her mind."
    $ the_person.event_triggers_dict["mom_vaginal_quest_progress"] = 2

    call advance_time()

    $ decision_event = Action("make a decision", mom_vaginal_quest_3_requirement, "mom_vaginal_quest_3", args = the_person, requirement_args = [the_person, day + renpy.random.randint(1,3)])
    $ mc.business.mandatory_crises_list.append(decision_event)
    return

label mom_advice_dm(the_person):
    "The first step is to set up a fake account so you can message [the_person.title]'s account in private."
    $ fake_name = renpy.input("Pick your username.", default = "AnonymousMommy")
    "Welcome [fake_name]! Say hi to your fellow moms and get that advice you've always wanted!" (what_style = "text_message_style")
    "You pull up [the_person.possessive_title]'s account and start to write her a private message."
    menu:
        "Start polite.":
            fake_name "Hi VeryNaughtyMommy, I saw your post and immediately felt a connection." (what_style = "text_message_style")
            fake_name "It's a difficult situation to be in, but I've been there too." (what_style = "text_message_style")
            $ the_person.change_happiness(5)

        "Get to the point.":
            fake_name "I saw your post and knew I needed to message you right away." (what_style = "text_message_style")
            fake_name "I've been in the same situation, and I can tell you what to do." (what_style = "text_message_style")
            $ the_person.change_happiness(5*the_person.get_opinion_score("being submissive"))

    menu:
        "I'm a psychologist...":
            fake_name "I'm a psychologist, and I've met tons of women with stories just like you." (what_style = "text_message_style")
            fake_name "You are at a critically important part of your relationship with your son, and my advice is simple." (what_style = "text_message_style")
            fake_name "You need to start having sex with him. If you do not, expect him to move on with his life!" (what_style = "text_message_style")
            $ the_person.change_slut(the_person.get_opinion_score("being submissive") * 2)

        "I'm fucking my son too...":
            fake_name "I'm a mother just like you. My son started fucking me years ago, and things have been so much better since!" (what_style = "text_message_style")
            fake_name "We're both happier and so much closer together. My advice is to start fucking him right away!" (what_style = "text_message_style")
            $ the_person.change_slut(the_person.get_opinion_score("incest") * 2)

    "You pause and consider what final justification you could give to her."
    menu:
        "You're an incest slut...":
            fake_name "You must realise by now that you're a total slut for him." (what_style = "text_message_style")
            fake_name "Don't feel bad about it - your brain is wired to want him. There's nothing you can do to fight it." (what_style = "text_message_style")
            fake_name "When you start having sex he'll be able to make you cum like you never have before." (what_style = "text_message_style")
            fake_name "So stop wasting time and go do it!" (what_style = "text_message_style")
            $ the_person.change_slut(3 + the_person.get_opinion_score("incest"), add_to_log = False)

        "You're a loving mother...":
            fake_name "I can already tell you're a loving mother, so I know why you might feel strange about this." (what_style = "text_message_style")
            fake_name "Trust me when I say that this will bring both of you closer together." (what_style = "text_message_style")
            fake_name "Having sex is the purest expression of love we can give to another person." (what_style = "text_message_style")
            fake_name "Don't be afraid of showing that love to your son." (what_style = "text_message_style")
            $ the_person.change_love(3 + the_person.get_opinion_score("incest"))

        "You're an obedient woman...":
            fake_name "It's natural for a boy to come to a point where he takes control of his own life." (what_style = "text_message_style")
            fake_name "When he was younger you needed to protect him, but that's changed now. He needs to learn how to lead." (what_style = "text_message_style")
            fake_name "Stop worrying and listen to your son, he knows what is best for both of you." (what_style = "text_message_style")
            $ the_person.change_obedience(3 + the_person.get_opinion_score("incest"))

    "You proofread the message twice, then send it off to [the_person.possessive_title]'s account."
    return

label mom_advice_astroturf(the_person):
    "The site gives you the option to post annonymously. It's not hard to change your IP so you can post under multiple annonymous accounts."
    "You crack your knuckles and start to write fake comments."
    #TODO: Decide if any of these should have an impact.
    menu:
        "Call her brave.":
            "Anon4682" "You're so brave @VeryNaughtyMommy, I wish more people would talk about this sort of thing!" (what_style = "text_message_style")

        "Call her a slut.":
            "Anon4682" "This sounds so sexy @VeryNaughtyMommy, I wish more moms would think about fucking their son!" (what_style = "text_message_style")

    "A good start, but you're going to need to drown out any other opinions."
    menu:
        "Ask for details.":
            "Anon5535" "We want details @VeryNaughtyMommy, tell us what sort of things you've done with your son!" (what_style = "text_message_style")

        "Argue with other posters.":
            "Anon5535" "These people complaining probably don't have sons. They don't know what it's like to feel this close to them!" (what_style = "text_message_style")

    "Now to make sure she thinks this is a well rounded discussion."
    menu:
        "Link to random \"experts\".":
            "Anon7731" "So many doctors say it's good to have sex with your son, it's crazy people don't agree! Look at all of this research!" (what_style = "text_message_style")

        "Make a post too long to read.":
            "Anon7731" "I have a lot to say about this. First, I'm gald you came to talk to us @VeryNaughtyMommy. We all support you here, whatever decision you make." (what_style = "text_message_style")
            "Anon7731" "There are so many factors to consider, but I think they all point to the same thing..." (what_style = "text_message_style")
            "..."
            "Anon7731" "Which, if you remember, points to incest as a key factor in winning the civil war! You want to be a patriot, don't you? Additionally..." (what_style = "text_message_style")

    "You're almost satisfied, but there's still more you can do."
    menu:
        "Link the discussion on an incest website.":
            "You make a post on a popular incest forum, linking to the discussion. You make sure to drop a comment as well." (what_style = "text_message_style")
            "Anon" "Hey guys, check this out! A real mom wants to fuck her son, and she needs a little encouragement." (what_style = "text_message_style")
            "Anon" "Let's help the kid out and give her all the positive support she needs! Remember, you need to pretend to be a MILF to post there." (what_style = "text_message_style")

        "Spam report all of the dissenters.":
            "You make use of all the annonymous accounts you've made and spam report anyone who doesn't agree with you."
            "You're happy to find out the site automatically hides any comments that have enough reports."
            "Soon enough half of the comments are marked \"Comment flagged for moderator review\", and the other half all agree with you."

    "That should be enough to convince [the_person.title] that public opinion, amonst mothers at least, is overwhelming."
    return

label mom_vaginal_quest_3(the_person):
    "Your phone beeps: a text from [the_person.possessive_title]."
    $ mc.start_text_convo(the_person)
    the_person "I need to talk to you [the_person.mc_title]. Come to my bedroom, right away."
    menu:
        "Ask her why.":
            mc.name "What do you need me for?"
            the_person "I need to tell you in person."
            the_person "It's good news. I promise you won't regret it."
            the_person "Don't make me wait too long, I might have second thoughts..."

        "Don't reply.":
            "You shrug and put your phone back in your pocket."

    $ mc.end_text_convo()
    $ seduce_action = Action("Seduce my son.", mom_vaginal_quest_complete_requirement, "mom_vaginal_taboo_break_revisit_complete")
    $ the_person.on_room_enter_event_list.append(seduce_action)
    return

label mom_vaginal_taboo_break_revisit_complete(the_person):
    $ the_person.apply_outfit(lingerie_wardrobe.get_random_appropriate_outfit(the_person.sluttiness + 20))

    $ the_person.change_arousal(40, add_to_log = False)
    $ the_person.draw_person(position = "sitting", emotion = "happy")
    $ mc.change_locked_clarity(20)
    "[the_person.possessive_title] is sitting on the edge of her bed, barely dressed. She smiles and beckons you in."
    the_person "Hi [the_person.mc_title], thank you for coming. Close to door."
    "You follow her instructions, distracted by what she's wearing for a moment."
    mc.name "Uh, hey [the_person.title]..."
    the_person "So do you remember that discussion we had? About us being physical with each other?"
    the_person "I got some advice online about that. I was very surprised at how much people had to say about it."
    the_person "There were some people who were confused, but almost all of the advice I got was very supportive."
    the_person "I think this sort of relationship, between a mother and her son, is more common than most people realise."
    mc.name "So what does that mean?"

    $ the_person.break_taboo("vaginal_sex")
    $ the_person.event_triggers_dict["mom_vaginal_quest_active"] = False
    $ the_person.event_triggers_dict["vaginal_revisit_complete"] = True
    $ the_person.change_slut(10, 85)

    "She laughs playfully and draws a hand over her inner thigh and up her body to her sizeable chest."
    the_person "It means I want us to have sex, [the_person.mc_title]. I want to be close to you in a way only a mother can."
    if the_person.outfit.can_half_off_to_vagina(visible_enough = False):
        $ strip_list = the_person.outfit.get_half_off_to_vagina_list(visible_enough = False)
        $ generalised_strip_description(the_person, strip_list, position = "sitting", half_off_instead = True)
    else:
        $ strip_list = the_person.outfit.get_vagina_strip_list(visible_enough = False)
        $ generalised_strip_description(the_person, strip_list, position = "sitting", half_off_instead = True)
    $ the_person.draw_person(position = "missionary", emotion = "happy")
    "[the_person.possessive_title] lies back onto the bed and motions with a finger for you to join her."
    $ mc.change_locked_clarity(20)
    the_person "Come here and fuck me [the_person.mc_title]."
    menu:
        "Fuck her.":
            mc.name "You don't have to tell me twice."
            "You start to struggle out of your pants as fast as you can manage."
            the_person "What if I do it anyways? Come fuck me [the_person.mc_title]!"
            "She rubs her legs together in her excitement."
            the_person "Come fuck me! Come fuck your dirty slut mommy! I want you to come and fuck me!"
            "[the_person.possessive_title] gasps softly when your cock springs free."
            the_person "Hurry, hurry! Put that big cock inside your mother. Give her slutty pussy what it's been begging for!"
            "You climb on top of [the_person.title], who spreads her legs and lets you settle down between them."
            "She reaches down and holds onto your cock, rubbing the tip against her pussy lips for a moment."
            call condom_ask(the_person)
            if _return:
                "You're caught off guard when she wraps her legs around your hips and pulls you, gently, inside of her."
                "Her pussy is wet already, she was clearly playing with herself before you arrived."
                "You slide in, all the way to the base, as [the_person.possessive_title] moans in your ear."
                the_person "Yes, that's it... Fuck me... Mmmm... Fuck me..."
                call fuck_person(the_person, private = True, start_position = missionary, start_object = mc.location.get_object_with_name("bed"), skip_intro = True)
                $ the_report = _return
                $ the_person.call_dialogue("sex_review", the_report = the_report)
            else:
                the_person "[the_person.mc_title], we can't fuck without a condom..."
                mc.name "Fine, let's do something else then."
                "She shakes her head and frowns."
                $ the_person.change_happiness(-10)
                $ the_person.change_love(-1)
                the_person "I think I need some time to think actually. Maybe some other time."
                "You climb off of her and leave her room to give her some time to think."
                $ mc.change_location(hall)
                $ hall.show_background()

        "Some other time.":
            mc.name "I'm actually pretty busy right now, [the_person.mc_title]."
            "She lifts herself up on one elbow."
            the_person "Too busy to take care of your mommy? I hope you aren't having cold feet after all of this."
            mc.name "No, I just really don't have the time right now."
            $ the_person.change_happiness(-10)
            $ the_person.change_love(-1)
            "She frowns, but nods her understanding."
            the_person "Okay, but you better come spend some time with me soon, alright?"
            mc.name "I promise I will [the_person.title]."
    return
