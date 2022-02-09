### All the information and events related to the girlfriend role.

init -1 python:
    def ask_girlfriend_requirement(the_person):
        if the_person.has_role(girlfriend_role) or the_person.has_role(affair_role):
            return False
        elif the_person.has_role(sister_role) and the_person.event_triggers_dict.get("sister_girlfriend_waiting_for_blessing", False):
            return False
        elif the_person.has_role(mother_role) and the_person.event_triggers_dict.get("mom_girlfriend_waiting_for_blessing", False):
            return False
        elif the_person.love < 30:
            return False
        elif the_person.love < 60:
            return "Requires: 60 Love"
        else:
            return True #But note that there are still failure conditions in the actual event, but those lead to hints about what do to to stop it.

    def ask_break_up_requirement(the_person):
        return True

    def caught_cheating_requirement(the_person):
        return True

    def ask_get_boobjob_requirement(the_person):
        obedience_required = 130 - (the_person.get_opinion_score("showing her tits") * 5)
        if the_person.sluttiness < (40 - the_person.get_opinion_score("showing her tits") * 5):
            return False
        elif the_person.obedience < obedience_required:
            return "Requires: " + str(obedience_required) + " Obedience"
        elif the_person.event_triggers_dict.get("getting boobjob", False):
            return "Boobjob already scheduled."
        elif the_person.tits == "FF":
            return "Boobs are as large as they can become."
        else:
            return True

    def girlfriend_got_boobjob_requirement(start_day):
        if day < start_day:
            return False
        else:
            return True

    def girlfriend_ask_trim_pubes_requirement(the_person):
        obedience_required = 125 - (5*the_person.get_opinion_score("being submissive"))
        if the_person.sluttiness < 30:
            return False
        elif the_person.obedience < 110:
            return False
        elif the_person.obedience < obedience_required:
            return "Requires: " + str(obedience_required) + " Obedience"
        else:
            return True

    def girlfriend_do_trim_pubes_requirement(start_day):
        if day < start_day:
            return False
        else:
            return True

    def girlfriend_boob_brag_requirement(start_day):
        return True

label ask_break_up_label(the_person):
    # Stop being in a relationship.
    mc.name "[the_person.title], can we talk?"
    if the_person.happiness > 100:
        the_person "Sure, what's up?"
    else:
        the_person "Oh no, that's never good."

    mc.name "There's no easy way to say this, so I'll just say it: I think we should break up."
    $ the_person.draw_person(emotion = "sad")
    #TODO: Add a varient whre you've passed below the girlfriend threshold and she feels the same way.

    $ the_person.change_happiness(-(the_person.love - 40)) #TODO: Double check this vs. the girlfriend love threshold.
    "She seems to be in shock for a long moment, before slowly nodding her head."
    the_person "Okay... I don't know what to say."
    $ the_person.change_love(-10)
    mc.name "I'm sorry, but it's just the way things are."
    $ the_person.remove_role(girlfriend_role)
    return

label ask_be_girlfriend_label(the_person):
    #Requires high love, if successful she becomes your girlfriend (which unlocks many other options). Requires high lvoe and her not being in a relationship.
    #Hide this event at low love, show it when it at it's lowest love possibility and let it fail out for specific reasons (thus informing the player WHY it failed out).

    if the_person.has_role(sister_role): #She has specific dialogue
        call sister_girlfriend_intro(the_person)

    elif the_person.has_role(mother_role):
        call mom_girlfriend_intro(the_person)

    else: #General dialogue used for everyone.
        mc.name "[the_person.title], can I talk to you about something important?"
        the_person "Of course. What's on your mind."
        mc.name "I've been thinking about this for a while. I really like you and I hope you feel the same way about me."
        mc.name "I'd like to make our relationship official. What do you say?"


        if the_person.has_role(aunt_role):
            the_person "I... I don't know what to say [the_person.mc_title]. I love you like you were my own, but we could never have a real relationship together."
            the_person "Could you imagine what your mother would say about that, dating her sister? She would go crazy!"
            the_person "Come on, let's talk about something else."

        elif the_person.has_role(cousin_role):
            the_person "You and me being, like, boyfriend and girlfriend? Ha, you must be crazy! Have you been huffing fumes at work?"
            the_person "I mean sure, I've come around on you and think you're not a total loser now, but we're cousins. Our parents would kill us."
            the_person "So yeah, that's going to be a no from me."

        elif the_person.relationship != "Single":
            $ so_title = SO_relationship_to_title(the_person.relationship)

            if the_person.get_opinion_score("cheating on men") > 0:
                # She likes cheating on men and offers to have an affair with you instead. Adds the affair role.
                "She takes a moment before responding."
                the_person "I mean, I already have a [so_title] and I can't just leave him like this."
                the_person "But... Maybe he doesn't need to know about any of this. Do you think you could be discreet."
                $ the_person.discover_opinion("cheating on men")
                menu:
                    "Have an affair with [the_person.title].":
                        mc.name "I can be if that's what you need."
                        $ the_person.draw_person(emotion = "happy")
                        $ the_person.add_role(affair_role)
                        $ the_person.change_slut(2, 60)
                        $ mc.change_locked_clarity(10)
                        "She leans forward and kisses you, putting an arm around your waist and pulling you close. When she breaks the kiss she looks deep into your eyes."
                        the_person "Well then, you know where to find me."

                    "Refuse.":
                        mc.name "I can't do that. I need a relationship I can count on."
                        $ the_person.change_love(-3)
                        the_person "Right... Well, if you change your mind I'll be here."

            else:
                # She's just not into it, no matter how slutty she is. You'll have to seduce her to convince her first to have an affair.
                $ the_person.draw_person(emotion = "sad")
                "She takes a long moment before responding."
                the_person "Oh [the_person.mc_title], I'm so flattered, but you know that I have a [so_title]."
                if the_person.kids > 0:
                    if the_person.kids > 1:
                        the_person "I would never dream of leaving him, and it would devastate our children."
                    else:
                        the_person "I would never dream of leaving him, and it would devastate our child."
                else:
                    the_person "I would never dream of leaving him."


                if not the_person.has_taboo("vaginal_sex"):
                    mc.name "You didn't care about him when we were fucking."
                    if the_person.effective_sluttiness() > 50:
                        the_person "That didn't mean anything, we were just having fun. This is so much more serious than that."
                    else:
                        the_person "I don't know what I was thinking, that was a mistake."

                the_person "I care about you a lot, but it's just not something I could do."
                mc.name "I'm sorry to hear that. I hope we can still be friends."
                $ the_person.draw_person()
                the_person "As long as you understand where we stand, I think we can be."

        else:
            # She agrees, you're now in a relationship! Congratulations!
            $ the_person.draw_person(emotion = "happy")
            $ the_person.change_happiness(15)
            $ the_person.change_love(5)
            if the_person.age > 40:
                the_person "Oh I'm so happy to hear you say that! I was worried about our age difference, but I don't want that to stop us!"

            else:
                the_person "Oh my god, I'm so happy! Yes, I want you to be your girlfriend!"
            "She puts her arms around you and pulls you close."
            $ mc.change_locked_clarity(10)
            "She kisses you, and you kiss her back just as happily."
            $ the_person.add_role(girlfriend_role)

    return

label caught_cheating_label(the_other_girl, the_girlfriend): #Note: the_other_girl is stored as an argument in the event, while the_girlfriend is passed as an extra argument, so they are listed backwards.
    # This is an event added to the on_enter_room list for the girlfriend after she catches you cheating.

    if girlfriend_role not in the_girlfriend.special_role:
        return #She's lost the role somehow between now and when she caught you, so clear this out and move on.

    $ the_girlfriend.draw_person(emotion = "angry")
    "[the_girlfriend.title] storms up to you as soon as she sees you."
    the_girlfriend "What the fuck [the_girlfriend.mc_title]! How could you do that to me?"
    mc.name "Calm down, everything's okay."
    #TODO: Add some dialogue in case she's a particularly important person (ie. friend, mother)
    the_girlfriend "Really? Everything's okay while you're with another woman?"
    # Note: This only happens if she saw something happening that was too slutty for her, slutty girls think it's totally fine and normal.
    mc.name "Just let me explain..."
    $ the_girlfriend.change_love(-25)
    $ the_girlfriend.change_happiness(-20)
    if the_girlfriend.love < 60:
        the_girlfriend "I don't want to hear it. You're a lying scumbag who broke my heart..."
        $ the_girlfriend.remove_role(girlfriend_role)
        the_girlfriend "We're done! Through! Finished!"
        "She turns around and storms off."
        $ clear_scene()
    else:
        the_girlfriend "How could you possibly explain that?"
        mc.name "We were just fooling around, it didn't mean anything. Come on, you know I love you, right?"
        "She glares at you, but bit by bit her expression softens."
        "You sit down with her and calm her down, until finally she breaks and hugs you."
        the_girlfriend "Just never do that to me again, okay?"
        $ the_girlfriend.change_slut(2, 60)
        $ the_girlfriend.change_obedience(4)
        mc.name "Of course not, you'll never catch me doing that again."
        the_girlfriend "And I never want to see that bitch anywhere around you, okay?"
        mc.name "Of course."

    $ town_relationships.worsen_relationship(the_girlfriend, the_other_girl)
    $ town_relationships.worsen_relationship(the_girlfriend, the_other_girl)
    return

label ask_get_boobjob_label(the_person):
    mc.name "I've been thinking about something lately."
    the_person "Mhmm? What about?"
    if the_person.has_large_tits():
        mc.name "Your breasts are great, but I think you could get some work done on them to make them even better."
        "She looks down at her tits and frowns."
        the_person "Do you think? Well, I suppose I could see someone about them."
    else:
        mc.name "Your breasts are nice, but I think they could stand to be a little bigger."
        "She looks down at her tits and frowns."
        the_person "Hmm, I guess you're right. If you want I could see someone about them."


    $ so_title = ""
    $ so_obedience_requirement = 150 - (5*the_person.get_opinion_score("cheating on men"))

    $ self_pay_requirement = 150 - (the_person.get_opinion_score("showing her tits") * 5)
    if the_person.relationship != "Single":
        $ so_title = SO_relationship_to_title(the_person.relationship)
    menu:
        "Pay for her boobjob.\n-$7000" if mc.business.has_funds(7000):
            mc.name "If you arrange for it I don't mind paying for it."
            $ mc.business.change_funds(-7000)

        "Pay for her boobjob.\nRequires: $7000 (disabled)" if not mc.business.has_funds(7000):
            pass

        "Have her pay for it." if the_person.obedience >= self_pay_requirement and the_person.has_role(girlfriend_role):
            mc.name "Yeah, go see someone for me and get some implants. I want some nice big tits to play with"
            if the_person.get_opinion_score("being submissive") > 0:
                $ mc.change_locked_clarity(10)
                "She nods happily."
            else:
                "She hesitates, as if waiting for you to offer to pay, then nods dutifully."
                $ the_person.change_happiness(-5)

        "Have her pay for it.\nRequires: [self_pay_requirement] Obedience (disabled)" if the_person.obedience >= self_pay_requirement and the_person.has_role(girlfriend_role):
            pass

        "Have her [so_title] pay for it." if the_person.obedience >= so_obedience_requirement and the_person.has_role(affair_role):
            mc.name "Yeah, go see someone and get some implants put in. You can get your [so_title] to pay for them, right?"
            the_person "I don't know, what do I tell him?"
            $ mc.change_locked_clarity(10)
            mc.name "What every man wants to hear: \"Honey, I want to get some bigger tits!\"."
            mc.name "He'll be jumping at the opportunity to pay. Trust me."

        "Have her [so_title] pay for it.\nRequires: [so_obedience_requirement] (disabled)"if the_person.obedience < so_obedience_requirement and the_person.has_role(affair_role):
            pass

        "Never mind.":
            mc.name "On second thought, I don't think it's worth it. You look perfect just the way you are."
            the_person "Aww, thank you [the_person.mc_title]!"
            return

    $ the_person.discover_opinion("showing her tits")
    if the_person.get_opinion_score("showing her tits") > 0:
        $ the_person.change_happiness(10)
        $ the_person.change_obedience(1)
        $ mc.change_locked_clarity(10)
        the_person "Alright, I'll do it! Thank you [the_person.mc_title], I've always thought girls with bigger boobs looked hotter."


    elif the_person.get_opinion_score("showing her tits") < 0:
        $ the_person.change_happiness(-10)
        $ the_person.change_obedience(3)
        the_person "Fine, if that's what you'd like. I don't think I'll like all the attention being on my tits, but I want you to be happy."

    else:
        $ the_person.change_obedience(2)
        $ mc.change_locked_clarity(5)
        the_person "Okay [the_person.mc_title], if you want it I'll do it for you."

    the_person "I'll get it scheduled, if we're lucky I'll be able to have it done in a few days."
    if the_person.has_role(affair_role):
        the_person "I don't know if my [so_title] would want to kill you or thank you for this."

    $ the_person.event_triggers_dict["getting boobjob"] = True #Reset the flag so you can ask her to get _another_ boobjob.

    $ got_boobjob_action = Action("Girlfriend Got Boobjob", girlfriend_got_boobjob_requirement, "girlfriend_got_boobjob_label", args = the_person, requirement_args = day + renpy.random.randint(3,6))
    $ mc.business.mandatory_crises_list.append(got_boobjob_action)
    return

label girlfriend_got_boobjob_label(the_person):
    call got_boobjob(the_person)
    $ girlfriend_boob_brag_action = Action("Girlfriend Boobjob Brag", girlfriend_boob_brag_requirement, "girlfriend_boob_brag_label")
    $ the_person.on_talk_event_list.append(girlfriend_boob_brag_action)
    return

label girlfriend_boob_brag_label(the_person): #TODO: Decide if we need a little alt-dialogue for the affair side of things.
    the_person "Hey [the_person.mc_title], what do you think?"
    if the_person.get_opinion_score("showing her tits") < 0:
        $ mc.change_locked_clarity(20)
        "She puts her arms behind her, revealing her newly enlarged chest."
        the_person "These feel so... excessive. It feels like everyone is staring at them all the time now."
        $ the_person.change_slut(-1 + the_person.get_opinion_score("showing her tits"))
    else:
        $ mc.change_locked_clarity(20)
        "She pushes her chest out towards you, shaking her tits just a little."
        the_person "I hope you like them, maybe we can have some fun with them later."
        $ the_person.change_slut(2, 60)

    call talk_person(the_person)
    return

label plan_date_night(the_person):
    #Special date for girlfriends only, you invite her over (or go over to her place?) and spend time watching a movie or something.

    return

label got_boobjob(the_person):
    # Event called a few days after someone has been asked to get a boob job. Results in larger brests. Duh.
    if rank_tits(the_person.tits) <= 2: #Ie. B cup or smaller.
        $ the_person.tits = "D" #Small tits all get upgraded to "large" D cup tits as a minimum, so they can be titfucked after.
        if the_person.personal_region_modifiers.get("breasts", 1) < 0.6:
            $ the_person.personal_region_modifiers["breasts"] = 0.3 #This is "normal" for C cups, so a little firmer than natural breasts but not by much.
    else: #Otherwise they get bigger by two steps.
        $ the_person.tits = get_larger_tits(the_person.tits) #Upgrade them twice, because we want boob jobs to be immediately noticeable.
        $ the_person.tits = get_larger_tits(the_person.tits)
        #Note that we DON'T change their breast region weight, to simulate natural vs. fake tits.

    if the_person.has_role(instapic_role):
        $ the_person.event_triggers_dict["insta_new_boobs_brag"] = True
        $ the_person.event_triggers_dict["insta_generate_pic"] = True #She'll make a post right away on Instapic about her new boobs.
    if the_person.has_role(dikdok_role):
        $ the_person.event_triggers_dict["dikdok_new_boobs_brag"] = True
        $ the_person.event_triggers_dict["dikdok_generate_video"] = True
    if the_person.has_role(onlyfans_role):
        $ the_person.event_triggers_dict["onlyfans_new_boobs_brag"] = True

    $ the_person.event_triggers_dict["getting boobjob"] = False #Reset the flag so you can ask her to get _another_ boobjob.
    if the_person.event_triggers_dict.get("boobjob_count",0) == 0:
        $ the_person.event_triggers_dict["boobjob_count"] = 1
    else:
        $ the_person.event_triggers_dict["boobjob_count"] += 1
    return

label girlfriend_ask_trim_pubes_label(the_person):
    mc.name "I want you to keep your pubes trimmed differently for me."
    "[the_person.possessive_title] nods obediently."
    the_person "How do you want me to trim them?"
    if the_person.event_triggers_dict.get("trimming_pubes", None) is not None:
        # She was already planning on a different style, so we can have some change your mind dialogue here
        $ mc.business.mandatory_crises_list.remove(the_person.event_triggers_dict.get("trimming_pubes",None)) #If she already had an event for this make sure to remove it.
        $ the_person.event_triggers_dict["trimming_pubes"] = None

    python:
        valid_pube_options = []
        for a_style in pube_styles:
            if a_style.name != the_person.pubes_style.name:
                valid_pube_options.append([a_style.name, a_style])
        valid_pube_options.append(["Never mind.","Never mind."])

    $ pube_choice = renpy.display_menu(valid_pube_options,True,"Choice")

    if pube_choice == "Never mind.":
        mc.name "On second thought, I think they're fine the way they are."
    else:
        "You describe the style you want to her as she listens intently.."
        if pube_choice.ordering_variable > the_person.pubes_style.ordering_variable:
            the_person "Okay, I'll have to let it grow out a bit but as soon as I can I'll trim them just the way you want [the_person.mc_title]."
            $ time_needed = renpy.random.randint(3,8) #It will take some time for them to grow out.

        else:
            the_person "Okay, I'll trim them for you as soon as I can [the_person.mc_title]."
            $ time_needed = 1 # She can do it right away (After a turn passes).


        # Create the action where you do it.
        $ trim_pubes_action = Action("Girlfriend trim pubes", girlfriend_do_trim_pubes_requirement, "girlfriend_do_trim_pubes_label", args = [the_person, pube_choice], requirement_args = [day + time_needed])
        $ mc.business.mandatory_crises_list.append(trim_pubes_action)
        $ the_person.event_triggers_dict["trimming_pubes"] = trim_pubes_action
    return

label girlfriend_do_trim_pubes_label(the_person, the_style):
    #TODO: decide if we want to have a pubes comment where she tells you she's done it.
    python:
        new_pubes = the_style.get_copy() #Copy the base style passed to us
        new_pubes.colour = the_person.pubes_style.colour #Modify the copy to match this person's details
        new_pubes.pattern = the_person.pubes_style.pattern #TODO: Make sure this makes sense for any future patterns we use.
        new_pubes.colour_pattern = the_person.pubes_style.colour_pattern
        the_person.pubes_style = new_pubes #And assign it to them.
        the_person.event_triggers_dict["trimming_pubes"] = None
    return

label girlfriend_pubes_comment(the_person):
    #Next time you talk to her she comments that she trimmed her pubes
    return

label girlfriend_fuck_date_event(the_person):
    #Figure out her outfit for this

    if the_person.get_opinion_score("not wearing anything") > the_person.get_opinion_score("lingerie"):
        $ the_person.apply_outfit(Outfit("Nude"), update_taboo = True) #She's wearing nothing at all. nothing at all. nothing at all...

    elif the_person.get_opinion_score("lingerie") >= 0:
        $ the_person.apply_outfit(lingerie_wardrobe.get_random_appropriate_outfit(the_person.sluttiness + 20, 0 + (the_person.sluttiness/2), guarantee_output = True), update_taboo = True) #She's just wearing lingerie for the evening.

    else:
        $ the_person.apply_outfit(the_person.wardrobe.decide_on_outfit(the_person.sluttiness, 0), update_taboo = True) #She picks a slutty outfit, but nothing truely "special".

    if the_person.obedience > 130 or the_person.get_opinion_score("being submissive") > 0 or the_person.get_opinion_score("giving blowjobs") > 0:
        #She's on her knees and ready to suck you off as soon as you come in.
        $ the_person.draw_person(position = "kneeling1")
        $ mc.change_locked_clarity(20)
        the_person "Hello, I'm ready for you [the_person.mc_title]..."
        "She licks her lips and watches you from her knees."
        the_person "Don't waste any time, I want you in my mouth."
        call fuck_person(the_person, private = True, start_position = blowjob)

    else:
        #She's standing and ready to make out as soon as you come in."
        $ the_person.draw_person()
        $ mc.change_locked_clarity(10)
        the_person "Hello [the_person.mc_title]... I've been thinking about this all day."
        "You step inside. She reaches past you and closes the bedroom door." #Note that you never end up with submissive people down this branch
        "She wastes no time wrapping her arms around you and kissing you."
        call fuck_person(the_person, private = True, start_position = kissing)

    $ the_report = _return

    $ done = False
    $ had_to_run = False
    $ girl_came = False
    $ so_called = False
    $ energy_gain_amount = 50 #Drops each round, representing your flagging endurance.
    while not done:
        if the_report.get("girl orgasms", 0) > 0: #TODO: Have some variation to this based on how many times we've looped around.
            $ the_person.change_love(2 + the_person.get_opinion_score("cheating on men"))
            $ the_person.change_slut(1, 80)
            the_person "Oh god... That was amazing!"
            "[the_person.title] lies down on her bed and catches her breath."
            the_person "Ready to get back to it?"
            $ girl_came = True

        else:
            the_person "Whew, good job. Get some water and let's go for another!"
            "You take some time to catch your breath, drink some water, and wait for your refractory period to pass."
            "You hold [the_person.title] in bed while she caresses you and touches herself, keeping herself ready for you."



        if mc.energy < 40 and energy_gain_amount <= 20: #Forced to end the fuck date, so we set done to True.
            "The spirit is willing, but the flesh is spent. Try as she might [the_person.title] can't coax your erection back to life."
            if girl_came:
                the_person "Well, I guess that's all I'm going to be drawing out of you for tonight. That was fun."
                "She kisses you and runs her hand over your back."
                the_person "Now you should get going. Unless you're planning to stay the night?"
            else:

                $ the_person.change_love(-1)
                $ the_person.change_slut(-1)
                the_person "Well I guess we're done then... Maybe next time you can get me off as well."

            $ done = True
            "You get dressed, triple check you haven't forgotten anything, and leave. [the_person.title] kisses you goodbye at the door."
        else:
            "After a short rest you've recovered some of your energy and [the_person.possessive_title]'s eager to get back to work."
            $ mc.change_energy(energy_gain_amount)
            $ the_person.change_energy(energy_gain_amount) #She gains some back too
            if energy_gain_amount >= 10:
                $ energy_gain_amount += -10 #Gain less and less energy back each time until eventually you're exhausted and gain nothing back.
            menu:
                "Fuck her again.":
                    "Soon you're ready to go again and you wrap your arms around [the_person.title]."
                    mc.name "Come here you little slut."
                    # $ random_num = renpy.random.randint(0,100)
                    #TODO: Chance her adult daughter comes home and finds out what you're doing. (ie. same as the affair fuck date).
                    call fuck_person(the_person)
                    $ the_report = _return

                "Call it a night.":
                    mc.name "I have to get going. This was fun."
                    "You kiss [the_person.title], then get up and start collecting your clothes."
                    if girl_came:
                        the_person "Okay then. We need to do this again, you rocked my world [the_person.mc_title]."
                        "She sighs happily and lies down on her bed."

                    else:
                        the_person "Really? I didn't even get to cum yet..."
                        $ the_person.change_love(-1)
                        $ the_person.change_slut(-1)
                    $ done = True
                    "You shrug and pull up your pants."



    #As soon as done is True we finish looping. This means each path should narrate it's own end of encounter stuff.
    #Generic stuff to make sure we don't keep showing anyone.
    if not had_to_run:
        call check_date_trance(the_person)

    $ the_person.clear_situational_slut("Date")
    $ clear_scene()
    return "Advance Time"
