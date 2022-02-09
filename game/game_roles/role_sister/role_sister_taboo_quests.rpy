## Contains all of the events related to Lily and her taboo break quests
init -1 python:
    def sister_kissing_taboo_revisit_requirement(the_person):
        return True

    def sister_oral_taboo_revisit_requirement(the_person):
        return True

    def sister_anal_taboo_revisit_requirement(the_person):
        return True

    def sister_vaginal_taboo_revisit_requirement(the_person):
        return True

    def sister_kissing_quest_complete_requirement(the_person):
        if not the_person.event_triggers_dict.get("sister_kissing_quest_active", False):
            return False
        elif the_person.event_triggers_dict.get("sister_kissing_quest_progress", 0) < 3:
            return str(the_person.event_triggers_dict.get("sister_kissing_quest_progress", 0)) + "/3 InstaPic Sessions."
        else:
            return True

    def sister_oral_quest_1_requirement(the_person):
        if not the_person.event_triggers_dict.get("sister_oral_quest_active", False):
            return False
        elif not the_person.event_triggers_dict.get("sister_oral_quest_progress", 0) == 0:
            return False
        else:
            return True

    def sister_oral_quest_2_requirement(the_person):
        if not the_person.event_triggers_dict.get("sister_oral_quest_active", False):
            return False
        elif not the_person.event_triggers_dict.get("sister_oral_quest_progress", 0) == 1:
            return False
        elif not mc.business.has_funds(1200):
            return ""
        else:
            return True

    def sister_oral_revisit_quest_complete_requirement(the_person):
        if not the_person.event_triggers_dict.get("sister_oral_quest_active", False):
            return False
        elif not the_person.event_triggers_dict.get("sister_oral_quest_progress", 0) == 2:
            return "Buy her a pi-phone."
        else:
            return True

    def sister_anal_revisit_quest_complete_requirement(the_person):
        if not the_person.event_triggers_dict.get("sister_anal_quest_active", False):
            return False
        elif the_person.event_triggers_dict.get("sister_instathot_mom_shirtless_covered_count", 0) == 0:
            return "Convince [mom.title] to take shirtless InstaPic shots."
        else:
            return True

    def sister_vaginal_quest_revisit_requirement(the_person):
        if not the_person.event_triggers_dict.get("sister_vaginal_quest_active", False):
            return False
        elif mc.inventory.get_max_serum_count() < 10:
            return "Requires: 10 identical serum doses."
        elif mc.location.get_person_count() > 1:
            return "Not while other people are around."
        else:
            return True

label sister_kissing_taboo_break_revisit(the_person):
    $ the_person.draw_person()
    the_person "[the_person.mc_title], can we talk for a bit?"
    mc.name "Sure, what's up [the_person.title]?"
    $ first_time = the_person.event_triggers_dict.get("kissing_revisit_count",0) == 0
    $ noteable_taboo = "nudity"
    if "touching_body" in the_person.event_triggers_dict.get("kissing_revisit_restore_taboos", []):
        $ noteable_taboo = "touching"
    elif "touching_vagina" in the_person.event_triggers_dict.get("kissing_revisit_restore_taboos", []):
        $ noteable_taboo = "touching"
    elif "kissing" in the_person.event_triggers_dict.get("kissing_revisit_restore_taboos", []):
        $ noteable_taboo = "kissing"

    if first_time:
        "She shuffles around nervously for a moment before speaking again."
        if noteable_taboo == "touching":
            the_person "Well you know how we were touching each other? I don't know if it was right... " #TODO: Have a non-con varient where you ordered her.
            mc.name "Why not? We both liked it, right?"
            "She shrugs noncommittally."
            the_person "Sure, but you're my brother. It's a little weird."
            the_person "It's not a big thing, I just don't think we should do that again."

        elif noteable_taboo == "kissing":
            the_person "Well, you know how we kissed? I don't know if that was a good idea..."
            mc.name "Why not? We both liked it, right?"
            "She shrugs noncommittally."
            the_person "Sure, but you're my brother. It's a little weird."
            the_person "It's not a big thing, I just don't think we should do that again."

        elif noteable_taboo == "nudity":
            the_person "You know how you were looking at me naked? I was just thinking about it and..."
            "She shrugs uncertainly."
            the_person "I don't know, I think that might have been going too far. I don't think [mom.title] would have liked it."
            the_person "It's not a big thing, I just don't think I should be getting naked in front of you again, alright?"

    else:
        the_person "We went too far again, I think we need to take things a little slower."
        the_person "I mean what would our friends think if they find out? They would think we're crazy!"

    $ kissing_count_threshold = 3 - the_person.get_opinion_score("kissing")

    menu:
        "But you liked it, right?" if the_person.get_known_opinion_score("incest") > 0:
            mc.name "But you liked it, right?"
            "She laughs and shrugs."
            the_person "It wasn't a big deal, alright? Just... don't be weird about it!"
            mc.name "You're the one being weird, I just think we don't need to pretend we weren't a little into it."
            "She sighs dramatically."
            the_person "Fine, whatever. But if you tell anyone I'll deny it!"
            python:
                for a_taboo in the_person.event_triggers_dict.get("kissing_revisit_restore_taboos", []):
                    the_person.break_taboo(a_taboo, add_to_log = False, fire_event = False)

            $ the_person.event_triggers_dict["kissing_revisit_complete"] = True

        "But you liked it, right?\nRequires: Likes Incest (disabled)" if the_person.get_known_opinion_score("incest") <= 0:
            pass

        "But it keeps happening..." if the_person.event_triggers_dict.get("kissing_revisit_count", 0) >= kissing_count_threshold:
            mc.name "If you don't want it to happen, why do you keep letting it happen?"
            the_person "I'm not! It just sort of... does."
            "There's a pause while [the_person.possessive_title] reflects on this for a moment."
            the_person "Maybe you're right. It does seem to happen a lot, and it's not really all that bad."
            mc.name "Exactly. So we stop making a big deal out of it then, right?"
            "She sighs and shrugs."
            the_person "Yeah, I guess."
            $ the_person.event_triggers_dict["kissing_revisit_complete"] = True
            python:
                for a_taboo in the_person.event_triggers_dict.get("kissing_revisit_restore_taboos", []):
                    the_person.break_taboo(a_taboo, add_to_log = False, fire_event = False)

        "But it keeps happening...\nRequires: Break taboo [kissing_count_threshold] times (disabled)" if the_person.event_triggers_dict.get("kissing_revisit_count", 0) < kissing_count_threshold:
            pass

        "Come on, how can I change your mind?" if not the_person.event_triggers_dict.get("sister_kissing_quest_active", False):
            mc.name "It was fun though, so why stop? Come on, what can I do to change your mind?"
            the_person "Ew, you're so weird! But..."
            "She rolls her eyes and thinks for a moment."
            if the_person.event_triggers_dict.get("insta_intro_finished", False):
                the_person "Fine, if you're going to be perving on me I want to get something out of it."
                the_person "I need more help taking shots for InstaPic. Help me out for a while and I'll..."

            else:
                the_person "Fine, have you ever heard of InstaPic?"
                mc.name "InstaPic?"
                the_person "Oh my god, how old are you again? It's a social media thing, people post pictures and follow other people."
                the_person "If you're popular some companies will even pay for you to wear their clothes or show off their stuff."
                mc.name "So how popular are you?"
                the_person "Well... Not very, yet, but I just started posting! I'm still figuring out what people want to see."
                the_person "There are some shots that are really hard to get by myself, so I need your help."
                the_person "Help me out for a while and..."
                call setup_sister_insta(the_person)

            "[the_person.possessive_title] laughs nervously and shrugs."
            the_person "You know... see me naked and stuff. God you're so weird!"
            mc.name "{i}We're{/i} weird, [the_person.title]."
            "She sighs, realising how right you are."

            $ the_person.event_triggers_dict["sister_kissing_quest_active"] = True
            $ the_person.change_slut(-10)
            $ mc.log_event(the_person.title + "'s taboos restored!", "float_text_red")

            $ the_person.get_role_reference(sister_role).actions.append(Action("Check back in...", sister_kissing_quest_complete_requirement, "sister_kissing_taboo_break_revisit_complete"))

        "I understand.":
            "You want to complain or argue, but you know that will only make things worse."
            mc.name "You're right, I get it."
            "She lets out a relieved sigh and smiles."
            the_person "Whew, I was worried you were going to be all weird about this."
            $ the_person.change_slut(-10)
            $ mc.log_event(the_person.title + "'s taboos restored!", "float_text_red")

    $ clear_scene()
    return

label sister_kissing_taboo_break_revisit_complete(the_person):
    $ the_person.event_triggers_dict["sister_kissing_quest_active"] = False
    $ the_person.event_triggers_dict["kissing_revisit_complete"] = True
    mc.name "Are you happy with all the help I've given you with InstaPic?"
    the_person "Yeah, I guess you have helped me out a bunch lately."
    mc.name "So does that mean we can..."
    "She laughs and rolls her eyes."
    the_person "Oh my god, you only ever think about one thing! Yeah, yeah, just don't make a big deal about it."

    $ the_person.change_slut(10, 40)
    python:
        for a_taboo in the_person.event_triggers_dict.get("kissing_revisit_restore_taboos", []):
            the_person.break_taboo(a_taboo)
    return

label sister_oral_taboo_break_revisit(the_person):
    $ the_person.draw_person()
    the_person "[the_person.mc_title], do you have a sec?"
    mc.name "Yeah, what's up?"

    $ first_time = the_person.event_triggers_dict.get("oral_revisit_count", 0) <= 1
    $ noteable_taboo = "cunn"
    if "sucking_cock" in the_person.event_triggers_dict.get("oral_revisit_restore_taboos", []):
        $ noteable_taboo == "blowjob"

    if first_time:
        if noteable_taboo == "blowjob":
            the_person "So... you know how I, uh..."
            "She glances around nervously, then brings one hand up to her mouth and mimes a blowjob."
        else: # noteable_taboo == "cunn"
            the_person "So you know how you, uh... ate me out?"

        mc.name "Of course, it was awesome."
        the_person "Yeah, so I've been thinking about that and... I don't think we should do that again."
        the_person "It was kind of fun, but it would be super weird if it became a normal thing."
    else:
        the_person "So, I know we both had a good time, but we went a little too far again."
        the_person "Just... wanted to let you know, I don't think we should make that a normal thing."

    $ oral_count_threshold = 4 - the_person.get_opinion_score(["giving blowjobs", "getting head"])

    menu:
        "I know it turned you on." if the_person.get_known_opinion_score("incest") > 0:
            mc.name "I know you better than that [the_person.title], you're just scared because it turned you on."
            mc.name "Worried you like your brother's cock just a little bit too much?"
            "[the_person.possessive_title] scoffs and shakes her head."
            the_person "Oh shut up, that's not... I mean, it was {i}fun{/i}, but it's a little fucked up, right?"
            mc.name "So what? It's not the weirdist fetish I've heard of."
            mc.name "It's just a little fun, and we can trust each other. Right?"
            "She takes a long time to think it over. At last she sighs and shrugs."
            the_person "Listen, I'm not going to say we {i}should{/i} do it..."
            mc.name "But you aren't going to say we shouldn't either, right?"
            "She smiles mischeviously and winks."
            the_person "Just don't let [mom.title] know."
            mc.name "Same goes for you."
            python:
                for a_taboo in the_person.event_triggers_dict.get("oral_revisit_restore_taboos", []):
                    the_person.break_taboo(a_taboo, add_to_log = False, fire_event = False)

            $ the_person.event_triggers_dict["oral_revisit_complete"] = True

        "I know it turned you on.\nRequires: Likes Incest (disabled)" if the_person.get_known_opinion_score("incest") <= 0:
            pass

        "But it keeps happening..." if the_person.event_triggers_dict.get("oral_revisit_count", 0) >= oral_count_threshold:
                mc.name "I feel like it's already a normal thing. How many times has it happened now?"
                the_person "That's not the point, it's just..."
                "She pauses to actually think about your question."
                the_person "Oh man, it has been a lot, hasn't it."
                mc.name "Exactly. So why are we still making a big deal out of it every single time."
                mc.name "Just embrace it and have fun."
                "She rolls her eyes and sighs."
                the_person "I guess there's no point fighting it. We've seen how that goes already."
                mc.name "You're making a good call here [the_person.title]."
                the_person "I hope so."
                python:
                    for a_taboo in the_person.event_triggers_dict.get("oral_revisit_restore_taboos", []):
                        the_person.break_taboo(a_taboo, add_to_log = False, fire_event = False)
                $ the_person.event_triggers_dict["oral_revisit_complete"] = True

        "But it keeps happening...\nRequires: Break taboo [oral_count_threshold] times (disabled)" if the_person.event_triggers_dict.get("oral_revisit_count", 0) < oral_count_threshold:
            pass

        "Let's make a deal." if not the_person.event_triggers_dict.get("sister_oral_quest_active", False):
            mc.name "Come on, how about we make a deal? You don't make a big deal of this, and I'll do something for you."
            the_person "No, I don't think so... I mean, what could you do for me?"
            mc.name "You tell me."
            "She seems about to refuse, but pauses to think."
            the_person "Well... There is a new πphone out, and the camera is {i}amazing{/i} on it. Everyone on InstaPic wants one."
            the_person "Too bad it's really expensive..."
            mc.name "If I get you the new πphone, we're good?"
            the_person "That's really all it's going to take? Yeah, get me the phone and I'll think about... you know."
            "She mimes a blowjob, poking out her tongue with her cheek. She giggles and winks."
            the_person "Good luck though, I've heard the lines are massive. You'll probably be waiting there all day!"
            mc.name "I'm sure I can manage it."

            $ the_person.event_triggers_dict["sister_oral_quest_active"] = True
            $ the_person.change_slut(-10)
            $ mc.log_event(the_person.title + "'s taboos restored!", "float_text_red")

            $ electronics_store.on_room_enter_event_list.append(Action("pi phone discover", sister_oral_quest_1_requirement, "sister_oral_taboo_break_revisit_quest_1", args = the_person, requirement_args = the_person))

            $ electronics_store.actions.append(Action("Buy a pi-phone. -$1200", sister_oral_quest_2_requirement, "sister_oral_taboo_break_revisit_quest_2", args = the_person, requirement_args = the_person))

            $ the_person.get_role_reference(sister_role).actions.append(Action("Check back in...", sister_oral_revisit_quest_complete_requirement, "sister_oral_taboo_break_revisit_complete"))



        "I understand.":
            mc.name "I understand [the_person.title]."
            "She smiles happily and gives a relieved sigh."
            the_person "Okay, good! I was worried you were going to take that badly!"
            $ the_person.change_slut(-10)
            $ mc.log_event(the_person.title + "'s taboos restored!", "float_text_red")
    $ clear_scene()
    return

label sister_oral_taboo_break_revisit_quest_1(the_person):
    "As you get close to the electronics store you see a long line snaking out the front and down one arm of the mall."
    "The front of the store is covered in posters, all advertising \"The New pi-phone. Only $1200!\"."
    $ the_person.event_triggers_dict["sister_oral_quest_progress"] = 1
    return

label sister_oral_taboo_break_revisit_quest_2(the_person):
    "You follow the line of waiting fans until you reach the end and get in line."
    "The line is moving at a crawl, it's clear that this is going to take some time."
    menu:
        "Keep waiting. {image=gui/heart/Time_Advance.png}" if time_of_day < 4:
            $ lead_girl = iris
            $ iris.add_role(dikdok_role)
            $ iris.add_role(instapic_role) #Make sure she has both an instapic and dikdok account.
            $ iris.add_job(influencer_job)
            $ electronics_store.add_person(iris) #Now that she's added to the world her turns proccess as normal too.
            # Let her wander the city for now, she doesn't "exist" until this point so we don't need to worry about her.
            "You sigh and resign yourself to the long wait."
            $ other_girl_1 = create_random_person()
            $ other_girl_2 = create_random_person()
            "Shortly after you arrive a pack of girls swing into line behind you."

            $ the_group = GroupDisplayManager([other_girl_1, lead_girl, other_girl_2], primary_speaker = lead_girl)
            $ the_group.draw_group()
            "They all have their phones out, taking pictures and themselves as they laugh and chat."
            "With some time - and you have nothing but time - you realise that they're all orbiting around one of the girls."
            lead_girl "It's going to be, like, amazing. I'm already planning a trip, my followers are going to love it."
            $ the_group.set_primary(other_girl_1)
            $ the_group.draw_group()
            other_girl_1 "Wow, that's going to be amazing! I'm so jealous, I wish I could be doing that!"
            $ the_group.set_primary(lead_girl)
            $ the_group.draw_group()
            lead_girl "Well stick close and pay attention, maybe you'll learn something and really grow your presence."
            menu:
                "Ignore them.":
                    "This wait is going to be tedious enough without making small talk with a gaggle of girls."
                    $ clear_scene()
                    "You pass the time on your phone and shuffle forward as the line creeps towards your destination."

                "Talk to them.":
                    "You don't have anything better to do with your time, so you turn around and try and strike up a conversation."
                    mc.name "Hey, you three here for the pi-phone release too?"
                    $ the_group.set_primary(other_girl_2)
                    $ the_group.draw_group()
                    other_girl_2 "Uh, duh. Why else would we be here?"
                    $ the_group.set_primary(other_girl_1)
                    $ the_group.draw_group()
                    other_girl_1 "You're such a bitch [other_girl_2.name]. The guy's just being nice."
                    $ other_girl_2.set_title(other_girl_2.name)
                    $ other_girl_2.set_possessive_title(other_girl_2.name)
                    $ the_group.set_primary(lead_girl)
                    $ the_group.draw_group()
                    "The two girls turn to their leader. She looks you up and down, as if passing judgement."
                    lead_girl "Yeah, I am. What about you?"
                    mc.name "Your friend is right, I'm picking one up..."
                    "She laughs and shakes her head."
                    lead_girl "Oh, they're not my friends. They're just following me around so she can be in the back of my Insta-posts."
                    "The two girls scowl, but their leader doesn't seem to care."
                    mc.name "Right... Well I'm just picking one up for my sister. She's really into InstaPic."
                    $ the_group.set_primary(other_girl_1)
                    $ the_group.draw_group()
                    other_girl_1 "So you're just buying her a phone? Oh my god, I wish my brother was like you..."
                    $ the_group.set_primary(lead_girl)
                    $ the_group.draw_group()
                    lead_girl "She's on InstaPic, huh?"
                    "She looks you over again, and this time she seems to come to a decision."
                    lead_girl "Hey, how about I give you my number. Maybe you can set up a collab with your sister..."
                    "Her two followers glance at each other, but their leader keeps ignoring them."
                    mc.name "Sure, no promises though. She can be pretty busy."
                    "You hand her your phone, and she starts to put her number in."
                    $ lead_girl.set_title(lead_girl.name)
                    $ lead_girl.set_possessive_title(lead_girl.name)
                    lead_girl "My name's [lead_girl.title]."
                    call person_introduction(lead_girl, girl_introduction = False)
                    $ mc.phone.register_number(lead_girl)
                    $ lead_girl.event_triggers_dict["insta_known"] = True
                    lead_girl "Oh, and I added my InstaPic name too. Look me up some time."
                    "She hands your phone back to you with a wink."
                    "You chat a little bit more, then turn back to follow the line as it creeps towards your destination."
                    $ clear_scene()

            "The line finally pulls up to the front of the store."
            "Without much fanfare you're ushered in. The staff look stressed, hurrying to serve the swarms of people."
            "You get your phone, pay for it, and are directed towards the exit without any issues."
            $ mc.business.change_funds(-1200)
            $ the_person.event_triggers_dict["sister_oral_quest_progress"] = 2
            call advance_time()

        "Keep waiting. {image=gui/heart/Time_Advance.png}\nNot enough time (disabled)" if time_of_day == 4:
            pass

        "Buy one from a scalper. -$2400" if mc.business.has_funds(2400):
            "You don't feel like waiting in line for hours just to get this phone, so you start looking for someone who has one to sell you theirs."
            "You wait at the exit from the store, asking people as they go past."
            mc.name "Hey man, want to make some quick money? I'll pay double."
            "No luck at first, but soon enough you get someone to stop and consider your offer."
            "Stranger" "Seriously? Uh..."
            mc.name "Come on, you can take the cash and get back into line right away."
            "Stranger" "Aaaah, fuck it. Fine, do you have actual cash?"
            "You have to find an ATM to get the man his cash, but after a few minutes you have a new pi-phone in your hands."
            "A hell of a lot better than waiting in line for hours, you think to yourself."
            $ mc.business.change_funds(-2400)
            $ the_person.event_triggers_dict["sister_oral_quest_progress"] = 2

        "Buy one from a scalper. -$2400 (disabled)" if not mc.business.has_funds(2400):
            pass

        "Give up for now.":
            "You don't feel like waiting in line for hours. Maybe the line will be shorter some other time."
    return

label sister_oral_taboo_break_revisit_complete(the_person):

    $ the_person.event_triggers_dict["sister_oral_quest_active"] = False
    $ the_person.event_triggers_dict["oral_revisit_complete"] = True

    mc.name "Hey, you were looking for this, right?"
    "You pull out [the_person.title]'s new pi-phone and wave it in front of her."
    $ the_person.draw_person(emotion = "happy")
    the_person "Oh my god, you actually got one? Aaaah!"
    $ the_person.change_happiness(20)
    "She snatches at the phone excitely."
    menu:
        "Ask for a reward.":
            "You yank the box back as she grabs at it. She pouts at you."
            the_person "[the_person.mc_title], give me my phone!"
            mc.name "It's not your phone quite yet. You still need to hold up your end of the deal."
            "She sighs and rolls her eyes."
            the_person "Fine, yeah, whatever. I won't make a big deal out of it if we... you know, do that again."
            "She grabs for the phone again, and again you pull it out of reach."
            mc.name "I want you to prove it to me."
            the_person "What? Oh... Very funny [the_person.mc_title]. Come on, just give me the phone."
            the_person "It's not like I'm going to give you a blowjob just for a phone."
            mc.name "Aren't you? All of the girls at the store were talking about their InstaPic accounts."
            mc.name "Imagine how you'll look, if you're the only who doesn't have a pi-phone..."
            "You leave the question hanging. [the_person.possessive_title] pouts again, but sighs when it's clear that won't break you."
            the_person "You're the worst, you know that? Fiiiine."
            if mc.location.get_person_count() > 1:
                the_person "But not here. Let's find somewhere private."
                "You follow her until she finds a place that satisfies her requirement for privacy."
            "She rolls her eyes and sways her hips, as if unsure what to do now."
            the_person "So..."
            mc.name "You should probably start by getting on your knees."
            $ the_person.draw_person(position = "blowjob")
            "She follows your instructions, getting onto the floor and positioning herself in front of your crotch."
            "You unzip your pants and present her with your cock - already hardening with anticipation."
            "[the_person.possessive_title] reaches up and lightly grasps your shaft. You twitch in response to her gentle touch."
            the_person "That made you move? You're so sensitive..."
            "She explores your cock for a moment, running her thumb along the bottom of your shaft."
            mc.name "Come on, stop stalling."
            the_person "I'm not stalling! I'm just... curious. Ugh, I can't believe I said that!"
            "You tap her on the head with the phone box."
            mc.name "In your mouth now."
            $ the_person.change_slut(10, 40)
            python:
                for a_taboo in the_person.event_triggers_dict.get("kissing_revisit_restore_taboos", []):
                    the_person.break_taboo(a_taboo)
                the_person.break_taboo("sucking_cock")
            "She rolls her eyes, but leans forward and presses your tip against her lips."
            "[the_person.title] holds you there for a second, then swirls her tongue around her lips to get everything wet, and finally slides you inside."
            $ the_person.draw_person(position = "blowjob", special_modifier = "blowjob")
            "She starts to blow you, timidly at first, but after a short adjustment period she's going down on you with adequate enthusiasm."
            call fuck_person(the_person, private = True, start_position = blowjob, start_object = mc.location.get_object_with_name("floor"), girl_in_charge = True, position_locked = True)
            $ the_report = _return
            $ the_person.call_dialogue("sex_review", the_report = the_report)
            "Satisfied with her work, you chuck [the_person.title]'s new phone onto her bed. She watches it sail over her head and land on her pillow."
            the_person "Hey! I... Thank you [the_person.mc_title]."
            mc.name "Anything for my little sis."
            "You tussle her hair before zipping up your pants."

        "Give it to her.":
            "You let her grab the box out of your hands. She starts tearing it open almost immediately."
            the_person "I'm going to take such amazing pictures with this! This is amazing!"
            mc.name "So, remember what we talked about?"
            "She gives you a confused look, as if surprised you could be interested in anything but a new smartphone."
            $ the_person.change_slut(10, 40)
            python:
                for a_taboo in the_person.event_triggers_dict.get("kissing_revisit_restore_taboos", []):
                    the_person.break_taboo(a_taboo)
            the_person "Huh? Oh, that. Yeah, I won't make a big deal out of whatever... we do together."
            "[the_person.possessive_title] frees the phone from it's cardboard prison and holds it to her chest."
            the_person "Oh my god, this is the best day ever!"
    return

label sister_vaginal_interupt(the_person): #TODO: Figure out a way to hook this up.
    #TODO: She says you should fuck her ass instead, because that's not "real sex"
    return

label sister_anal_taboo_break_revisit(the_person):
    $ the_person.draw_person()
    the_person "Hey [the_person.mc_title], got a moment?"
    "[the_person.possessive_title] swings her arms at her side nervously."
    mc.name "Yeah, what's up?"

    $ first_time = the_person.event_triggers_dict.get("anal_revisit_count", 0) <= 1

    if first_time:
        the_person "Well, uh... You know how you kind of... fucked my butt?"
        mc.name "It's a little hard to forget."
        the_person "I just can't stop thinking about that, and how close we were to actually having sex."
    else:
        the_person "Well, it was fun and everything, but... we really shouldn't go that far."

    the_person "You're my brother, you know? It's getting pretty freaking weird!"

    $ anal_count_threshold = 5 - the_person.get_opinion_score("anal sex")

    menu:
        "I know you want more though." if the_person.get_known_opinion_score("incest") > 1:
            mc.name "I know you better than that [the_person.title]. You want it again, right?"
            the_person "[the_person.mc_title], we can't..."
            mc.name "Not just again, no, you want to take it even further."
            "She scoffs and rolls her eyes, but it's a weak denial."
            mc.name "You probably think about us fucking all the time, right?"
            the_person "I... No..."
            "She withers under your knowing stare. Finally she breaks eye contact mutters, embarrassed."
            the_person "Once or twice, maybe. That's so messed up, right?"
            mc.name "I've thought about it too, it's no big deal."
            "[the_person.possessive_title] stays silent, so you continue."
            mc.name "If you're really worried about it we should just keep doing anal."
            the_person "That's not much better."
            mc.name "It's not real sex, I can't get you pregnant..."
            the_person "Oh god, could you imagine?"
            mc.name "And maybe it will be close enough for you to keep your urges under control."
            "She laughs and shakes her head."
            the_person "My urges? What about you? I swear you'd bang anything with a pulse."
            mc.name "And a pair of tits. I have standards."
            "[the_person.title] laughs again, and this time it sounds a little less stressed."
            the_person "Fuck, I can't believe I'm going to say this."
            the_person "We can keep... doing anal, but we can't take it any further than that!"
            mc.name "Deal. Glad we talked about this [the_person.title]."
            the_person "Same here, I guess."
            $ the_person.break_taboo("anal_sex", add_to_log = False, fire_event = False)
            $ the_person.event_triggers_dict["anal_revisit_complete"] = True

        "I know you want more though.\nRequires: Likes Incest (disabled)" if the_person.get_known_opinion_score("incest") <= 1:
            pass

        "But it keeps happening..." if the_person.event_triggers_dict.get("anal_revisit_count", 0) >= anal_count_threshold:
            mc.name "It's just going to keep happening [the_person.title], we know that by now."
            the_person "It doesn't have to..."
            mc.name "I think it does. We can't control ourselves, our bodies want to fuck."
            "She frowns and shakes her head, but she can't really deny the facts."
            the_person "So what do we do?"
            mc.name "Just stop fighting it. It's fun, so let's just enjoy it for what it is."
            the_person "I guess that makes sense..."
            "[the_person.possessive_title] takes a long time to think about that before nodding."
            the_person "Fine, we'll do it your way for a while."
            mc.name "You're making a good call [the_person.title]."
            $ the_person.break_taboo("anal_sex", add_to_log = False, fire_event = False)
            $ the_person.event_triggers_dict["anal_revisit_complete"] = True

        "But it keeps happening...\nRequires: Break taboo [anal_count_threshold] times (disabled)" if the_person.event_triggers_dict.get("anal_revisit_count", 0) < anal_count_threshold:
            pass

        "Let me change your mind." if not the_person.event_triggers_dict.get("sister_anal_quest_active", False):
            mc.name "We're all weird, so what? Come on, let me change your mind."
            the_person "What could you possibly do to change my mind? Like, if [mom.title] found out about this, she would kill us!"
            if the_person.event_triggers_dict.get("sister_instathot_mom_shirtless_covered_count", 0) > 0:
                mc.name "You mean the same woman who's taking topless pictures with her daughter for the internet?"
                mc.name "This whole family is fucked up [the_person.title], at least fucking feels pretty good."
                "She thinks about this for a long, silent moment."
                the_person "Ugh... I hate it when you're right. Fine, but this is as far as it goes."
                mc.name "I think you said that last time."
                the_person "Well this time I mean it!"
                $ the_person.break_taboo("anal_sex", add_to_log = False, fire_event = False)
                $ the_person.event_triggers_dict["anal_revisit_complete"] = True

            else:
                "It seems like she's about to dismiss the entire idea, but pauses for a second."
                the_person "Speaking of [mom.title]... Alright, maybe there is one way you could convince me."
                the_person "My InstaPic followers have been going absolutely crazy over [mom.title]."
                the_person "I think everyone would go absolutely crazy if we got some boudoir pictures with both of us."
                mc.name "You mean in your underwear."
                the_person "Yeah and... maybe topless. But there's no way she would I could get her to agree to any of that."
                the_person "If you can convince her, maybe I'll think about it."
                mc.name "Alright, I'm sure I can figure out some way to convince her."

                $ the_person.change_slut(-10)
                $ mc.log_event(the_person.title + "'s taboos restored!", "float_text_red")
                $ the_person.event_triggers_dict["sister_anal_quest_active"] = True
                $ the_person.get_role_reference(sister_role).actions.append(Action("Check back in...", sister_anal_revisit_quest_complete_requirement, "sister_anal_taboo_break_revisit_complete"))


        "I understand.":
            mc.name "Hey, I get it [the_person.title]."
            "She sighs and smile happily."
            the_person "You do? Whew, that was easy!"
            the_person "And, uh... We can still do other stuff, like with my mouth or something..."
            $ the_person.change_slut(-10)
            $ mc.log_event(the_person.title + "'s taboos restored!", "float_text_red")

    $ clear_scene()
    return

label sister_anal_taboo_break_revisit_complete(the_person):
    $ the_person.event_triggers_dict["sister_anal_quest_active"] = False
    $ the_person.event_triggers_dict["anal_revisit_complete"] = True
    mc.name "So, I got you those pictures with [mom.title]."
    the_person "I know, I can't believe she actually did that!"
    the_person "My fans {i}love{/i} them! They're such perverts!"
    "She laughs, missing the irony."
    $ the_person.change_slut(10, 65)
    $ the_person.break_taboo("anal_sex")
    the_person "I guess you've proved yourself. I won't make a big deal out of... whatever it is we do."
    return

label sister_vaginal_taboo_break_revisit(the_person):
    $ the_person.draw_person()
    the_person "So [the_person.mc_title]... about yesterday..."
    "She calls out to you and hurries over."
    the_person "So that happened, huh? I think we both know it was kind of a mistake."
    if first_time:
        the_person "Right? It was just a one time thing, right?"
    else:
        the_person "Right? That's got to be the last time, right?"
    mc.name "We both had a good time, right?"
    "She nods, slightly embarrassed by it."
    the_person "Yeah, but we can't do it again. I know there are other ways for us to get off though."
    the_person "Those can still be fun."

    $ vaginal_count_threshold = 8 - the_person.get_opinion_score("vaginal sex")

    menu:
        "Let me change your mind." if the_person.get_known_opinion_score("incest") > 0:
            mc.name "Come on [the_person.title], you don't really believe that, do you?"
            mc.name "I know you've been thinking about that moment over and over again, when I slid inside your pussy."
            "She blushes and turns away, but doesn't argue the fact."
            mc.name "What do I have to do to change your mind."
            the_person "But we shouldn't..."
            mc.name "We're so far past that. There must be something you want..."
            the_person "I... Ugh, you're the worst!"
            "She slaps your chest playfully."
            the_person "Okay, if you want to keep on fucking me I nwant something special from you."
            mc.name "And that is?"
            the_person "You make drugs at your lab, right?"
            mc.name "Complex biologically active pharmaceuticals, actually."
            the_person "Sure, but can they, like, get you high?"
            mc.name "Uh... They can do a lot of things, if we tune them right. Why do you care?"
            the_person "Well some of my friends are into that sort of thing, and if I could bring them something cool they would think {i}I'm{/i} cool."
            the_person "So that's what I want: make me some fun drugs and I'll fulfil your weird little fantasies and let you fuck me."
            mc.name "I'll give it some thought, alright?"
            "She nods her approval. You should bring her some serums that raise Happiness, although other effects may be satisfactory..."
            $ the_person.change_slut(-10)
            $ mc.log_event(the_person.title + "'s taboos restored!", "float_text_red")
            $ the_person.event_triggers_dict["sister_vaginal_quest_active"] = True


            $ the_person.get_role_reference(sister_role).actions.append(Action("Hand over the serum.", sister_vaginal_quest_revisit_requirement, "sister_vaginal_taboo_break_revisit_quest_1"))

        "Let me change your mind.\nRequires: Likes Incest (disabled)" if the_person.get_known_opinion_score("incest") <= 0:
            pass

        "But we've fucked so many times already..." if the_person.event_triggers_dict.get("vaginal_revisit_count", 0) >= vaginal_count_threshold:
            mc.name "This is ridiculous [the_person.title]. Have you been keeping track of how mny times we've fucked?"
            the_person "That doesn't mean we should do it more!"
            mc.name "Every time you say that you still end up with my cock inside you. Let's face the facts."
            if the_person.sex_record.get("Vaginal Creampies",0) > 0:
                mc.name "When you get turned on you let me pump you full of cum. How much further could we go?"
                mc.name "You never have argue when I'm risking knocking you up, but the day after all you do is complain!"

            elif the_person.has_broken_taboo("condomless_sex"):
                mc.name "You're already fucking my cock without protection."
                mc.name "The only way we could go further is if I just go ahead and knock you up."

            else:
                mc.name "If you didn't like it you wouldn't have fucked me so many times."

            "She tries to summon up some sort of response, but they all sound hollow when faced with the facts."
            $ the_person.break_taboo("vaginal_sex", add_to_log = False, fire_event = False)
            $ the_person.event_triggers_dict["vaginal_revisit_complete"] = True
            the_person "Ugh, I hate it when you're right!"
            "She throws her arms up and sighs dramatically."
            the_person "Fine, I guess I'll just have to accept that I'm... fucking my brother."
            mc.name "Come on, it's not so bad, is it?"
            if the_person.get_opinion_score("incest") > 0:
                "She gives you a weak smile."
                the_person "It could be worse, I guess."
            else:
                the_person "Don't push your luck."

        "But we've fucked so many times already...\nRequires: Break taboo [vaginal_count_threshold] times (disabled)" if the_person.event_triggers_dict.get("vaginal_revisit_count", 0) < vaginal_count_threshold:
            pass

        "I understand.":
            mc.name "Yeah, I guess that'll have to be enough."
            "[the_person.possessive_title] smiles and breathes a sigh of relief."
            the_person "I was worried you were going to make a big deal out of it."
            the_person "Thanks for being a cool brother [the_person.mc_title]."
            $ the_person.change_slut(-10)
            $ mc.log_event(the_person.title + "'s taboos restored!", "float_text_red")
    $ clear_scene()
    return

label sister_vaginal_taboo_break_revisit_quest_1(the_person):
    mc.name "I've got some serum for you and your friends."
    call screen serum_inventory_select_ui(mc.inventory, the_person, batch_size = 10)
    $ the_serum = _return
    if _return == None:
        mc.name "Actually, I forgot to grab them from the office. I'll be back another time."
        "[the_person.possessive_title] pouts, but nods her understanding."
        return

    $ mc.inventory.change_serum(the_serum, -10)

    "You pull out a cardboard box filled with serum vials."
    the_person "And these are going to get us high, right?"
    mc.name "That's what you asked for."
    "She takes the box and pulls one out, swirling it against the light."
    mc.name "So, does that mean we can..."
    the_person "Hang on, how do I even know if these work? I don't want to look like an idiot in front of my friends."
    the_person "I'm going to test one."

    $ the_person.give_serum(copy.copy(the_serum))

    "She pops the cork off of the vial and downs the content."

    # Use a test person so we can advance time to predict future results (ie. effect over time traits work for this too)
    $ slutty_serum = False #Set true if it raises Sluttiness OR Arousal.
    $ happy_serum = False #Set true if it raises Happiness
    $ test_person = create_random_person()
    $ start_happinesss = test_person.happiness
    $ start_sluttiness = test_person.effective_sluttiness()
    $ start_max_arousal = test_person.max_arousal
    $ start_arousal = test_person.arousal
    $ test_person.give_serum(the_serum, add_to_log = False)

    if test_person.happiness > start_happinesss:
        $ happy_serum = True
    if test_person.effective_sluttiness() > start_sluttiness:
        $ slutty_serum = True
    if test_person.max_arousal < start_max_arousal or test_person.arousal > start_arousal + 20: #Make it 20 so random opinion effects won't swing it, and minor side effects won't affect it.
        $ slutty_serum = True

    $ test_person.run_turn()
    if test_person.happiness > start_happinesss:
        $ happy_serum = True
    if test_person.effective_sluttiness() > start_sluttiness:
        $ slutty_serum = True
    if test_person.max_arousal < start_max_arousal or test_person.arousal > start_arousal + 20:
        $ slutty_serum = True


    the_person "How long does this stuff take to kick in?"
    mc.name "It shouldn't be too long."
    if happy_serum and slutty_serum:
        $ the_person.event_triggers_dict["sister_vaginal_quest_active"] = False
        $ the_person.event_triggers_dict["vaginal_revisit_complete"] = True
        the_person "I don't know, I'm not... Oh wait a second."
        "[the_person.title] takes a deep breath and sighs."
        the_person "Now I'm feeling it. Wow, that's a nice feeling."
        $ the_person.draw_person(position = "sitting")
        "She sits down on the side of her bed and fans at her face with her hand."
        if not the_person.outfit.tits_available():
            the_person "Is it hot in here?"
            $ the_item = the_person.outfit.get_upper_top_layer()
            "She pulls at her [the_item.display_name], then starts to pull it off entirely."
            the_person "I just... need to cool down."
            $ the_person.draw_animated_removal(the_item)
            $ mc.change_locked_clarity(10)
            "[the_person.possessive_title] chucks her [the_item.display_name] to the side and pants softly, her face flush."
        else:
            "[the_person.possessive_title]'s face is flush with sudden desire. She grabs one of her tits and squeezes it absentmindedly."
        the_person "So... hahah, it looks like your drug stuff works! This stuff feels great!"
        $ mc.change_locked_clarity(20)
        $ the_person.change_slut(10, 85)
        $ the_person.break_taboo("vaginal_sex")

        "She looks at you, eyes filled with lust, and spreads her legs open. She runs her hands down her inner thighs."
        the_person "I said you could fuck me if you did this, right? Yeah, I'm pretty sure that's what I said."
        the_person "Come on, what do you say? Wanna do it?"

        menu:
            "Fuck her.":
                mc.name "All worked up already? Alright, let's go."
                $ strip_list = the_person.outfit.get_vagina_strip_list(visible_enough = False)
                if strip_list:
                    "She jumps up and starts to strip for you."
                    $ generalised_strip_description(the_person, strip_list)
                    $ the_person.draw_person(position = "doggy")
                    "[the_person.title] gets onto her bed on all fours, sticking her ass and pussy out towards you."

                else:
                    $ the_person.draw_person(position = "doggy")
                    "[the_person.title] squeeles happily and rolls over, getting onto all fours on top of her bed."
                    "She wiggles her hips, taunting you with her cute butt and tight pussy."

                call condom_ask(the_person)
                if _return:
                    call fuck_person(the_person, start_position = doggy, start_object = mc.location.get_object_with_name("bed"), skip_intro = True)
                    $ the_report = _return
                    $ the_person.call_dialogue("sex_review", the_report = the_report)

                else:
                    "[the_person.possessive_title] seems disappointed with you, but there's nothing you can do about that now."



            "Maybe later.":
                mc.name "I don't have the time right now, but maybe later."
                "She pets her crotch and pouts at you."
                the_person "Aww... Alright."

        the_person "Just leave that box with me, my friends should {i}love{/i} this!"
    elif happy_serum:

        $ the_person.event_triggers_dict["sister_vaginal_quest_active"] = False
        $ the_person.event_triggers_dict["vaginal_revisit_complete"] = True

        the_person "Oh wait, I think... Oooh..."
        $ the_person.draw_person(position = "sitting")
        "A smile spreads across her face and she sits down on the side of her bed."
        mc.name "Feeling it now?"
        "She nods and sighs happily."
        the_person "It's like a warm hug, all over me."
        the_person "Yeah, I think the girls will like this... Thanks [the_person.mc_title]."
        the_person "Just leave the box with me."
        mc.name "And what about your half of the deal?"
        $ the_person.change_slut(10, 85)
        $ the_person.break_taboo("vaginal_sex")
        the_person "Oh, right. We can have sex sometimes I guess."
        the_person "We already did it once, so what's the big deal about doing it again?"
        the_person "But not right now, I just want to enjoy this feeling."

    elif slutty_serum:
        the_person "I don't know if it's working [the_person.mc_title], I... Hmm..."
        "She shuffles her thighs together, unconciously rubbing her thighs together."
        the_person "...I don't know how I'm feeling."
        "Her breathing is getting a little faster, and it's clear the serum is having an effect."
        the_person "This doesn't seem like the kind of drug the girls were looking for."
        "[the_person.possessive_title] grinds her thighs together, harder this time."
        the_person "But it does feel kind of nice..."
        menu:
            "Convince her to take them.":
                mc.name "You just need to be in the right mindset. I'll show you how good they can make you feel."
                the_person "Oh..."
                call fuck_person(the_person)
                $ the_report = _return
                if the_report.get("girl orgasms") > 0:
                    "[the_person.title] seems satisfied with the demonstration you've given her."
                    the_person "I get it now. Alright, I'll bring these to the girls."
                    the_person "It should be a fun night, one way or another!"
                    mc.name "And about our deal..."
                    "She rolls her eyes and shrugs."
                    $ the_person.change_slut(10, 65)
                    $ the_person.break_taboo("vaginal_sex")
                    the_person "Yeah, yeah, we can fuck every once in a while. We've already done it once, so I guess it's not a big deal."
                    $ the_person.event_triggers_dict["sister_vaginal_quest_active"] = False
                    $ the_person.event_triggers_dict["vaginal_revisit_complete"] = True

                else:
                    the_person "That was fun [the_person.mc_title], but I still don't think your drugs are very good."
                    the_person "Bring me something else, something that's fun!"
                    mc.name "Alright, I'll be back with a different design."
                    $ mc.inventory.change_serum(the_serum, 9)

            "Bring her something else.":
                mc.name "Alright, give those back. I'll make you something else you might like."
                "She nods and hands back the rest of the serum doses."
                $ mc.inventory.change_serum(the_serum, 9)
    else:
        the_person "I don't know if it's working [the_person.mc_title]..."
        "She waits a few moments longer, then shakes her head."
        $ the_person.change_obedience(-1)
        the_person "No, this isn't doing it for me. The girls want something fun, something that makes us feel good."
        the_person "Make us something like that, okay?"
        $ mc.inventory.change_serum(the_serum, -9)
    return
