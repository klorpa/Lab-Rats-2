### All the information and events related to the girlfriend role.

init -1 python:
    def ask_girlfriend_requirement(the_person):
        if girlfriend_role in the_person.special_role or affair_role in the_person.special_role:
            return False #If we're already in some sort of relationship don't ask about it.
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
            return "Requires: " + str(obedience_required)
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
            return "Requires: " + str(obedience_required)
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

    mc.name "[the_person.title], can I talk to you about something important?"
    the_person "Of course. What's on your mind."
    mc.name "I've been thinking about this for a while. I really like you and I hope you feel the same way about me."
    mc.name "I'd like to make our relationship official. What do you say?"

    if the_person.relationship != "Single":
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
                    $ the_person.change_slut_temp(2)
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


    elif any(relationship in [sister_role,mother_role,aunt_role,cousin_role] for relationship in the_person.special_role):
        # She's related to you, so she won't do it. Note that we aren't using has_family_taboo(), which would allow for a postiive incest opinion to allow this.
        # Future events will let you make this happen somehow (and in that case an incest opinion will make those events easier/trigger earlier, so training a girl makes sense).
        if sister_role in the_person.special_role:
            the_person "I love you like a brother... but just as a brother, you know?"
            the_person "Could you imagine what people would say about us? It would be crazy!"
            the_person "So... I guess no? Sorry."

        elif mother_role in the_person.special_role:
            the_person "Oh sweety, I love you more than anyone in the world, but we could never do that."
            the_person "It's just not something people do."
            the_person "Let's just talk about something else, okay?"

        elif aunt_role in the_person.special_role:
            the_person "I... I don't know what to say [the_person.mc_title]. I love you like you were my own, but we could never have a real relationship together."
            the_person "Could you imagine what your mother would say about that, dating her sister? She would go crazy!"
            the_person "Come on, let's talk about something else."

        elif cousin_role in the_person.special_role:
            the_person "You and me being, like, boyfriend and girlfriend? Ha, you must be crazy. Have you been inhaling fumes at work?"
            the_person "I mean sure, I've come around on you and think you're not a total loser now, but we're cousins. Our parents would kill us."
            the_person "So yeah, that's going to be a no from me."

    else:
        # She agrees, you're now in a relationship! Congratulations!
        $ the_person.draw_person(emotion = "happy")
        $ the_person.change_happiness(15)
        $ the_person.change_love(5)
        if the_person.age > 40:
            the_person "Oh I'm so happy to hear you say that! I was worried about our age difference, but I don't want that to stop us!"
            "She puts her arms around you and pulls you close."

        else:
            the_person "Oh my god, I'm so happy! Yes, I want you to be your girlfriend!"
            "She puts her arms around you and pulls you close."
        "She kisses you, and you kiss her back."
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
        $ the_girlfriend.change_slut_temp(4)
        $ the_girlfriend.change_obedience(4)
        mc.name "Of course not, you'll never catch me doing that again."
        the_girlfriend "And I never want to see that bitch anywhere around you, okay?"
        mc.name "Of course."

    $ town_relationships.worsen_relationship(the_girlfriend, the_other_girl)
    $ town_relationships.worsen_relationship(the_girlfriend, the_other_girl)
    return

label ask_change_hair_style(the_person):
    #Requires moderate obedience. Ask her to cut her hair a different way.
    #TODO: Implement ordered_variable for hair so we know what hairs take more time to grow into what other hairs.
    return

label ask_dye_hair(the_person):
    #Requires moderate obedience. Ask her to dye her hair a different colour.

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
        "Pay for her boobjob.\n-$7000" if mc.business.funds >= 7000:
            mc.name "If you arrange for it I don't mind paying for it."
            $ mc.business.funds += -7000

        "Pay for her boobjob.\nRequires: $7000 (disabled)" if mc.business.funds < 7000:
            pass

        "Have her pay for it." if the_person.obedience >= self_pay_requirement and girlfriend_role in the_person.special_role:
            mc.name "Yeah, go see someone for me and get some implants. I want some nice big tits to play with"
            if the_person.get_opinion_score("being submissive") > 0:
                "She nods happily."
            else:
                "She hesitates, as if waiting for you to offer to pay, then nods dutifully."
                $ the_person.change_happiness(-5)

        "Have her pay for it.\nRequires: [self_pay_requirement] Obedience (disabled)" if the_person.obedience >= self_pay_requirement and girlfriend_role in the_person.special_role:
            pass

        "Have her [so_title] pay for it." if the_person.obedience >= so_obedience_requirement and affair_role in the_person.special_role:
            mc.name "Yeah, go see someone and get some implants put in. You can get your [so_title] to pay for them, right?"
            the_person "I don't know, what do I tell him?"
            mc.name "What every man wants to hear: \"Honey, I want to get some bigger tits!\"."
            mc.name "He'll be jumping at the opportunity to pay. Trust me."

        "Have her [so_title] pay for it.\nRequires: [so_obedience_requirement] (disabled)"if the_person.obedience < so_obedience_requirement and affair_role in the_person.special_role:
            pass

        "Never mind.":
            mc.name "On second thought, I don't think it's worth it. You look perfect just the way you are."
            the_person "Aww, thank you [the_person.mc_title]!"
            return

    $ the_person.discover_opinion("showing her tits")
    if the_person.get_opinion_score("showing her tits") > 0:
        $ the_person.change_happiness(10)
        $ the_person.change_obedience(1)
        the_person "Alright, I'll do it! Thank you [the_person.mc_title], I've always thought girls with bigger boobs looked hotter."


    elif the_person.get_opinion_score("showing her tits") < 0:
        $ the_person.change_happiness(-10)
        $ the_person.change_obedience(3)
        the_person "Fine, if that's what you'd like. I don't think I'll like all the attention being on my tits, but I want you to be happy."

    else:
        $ the_person.change_obedience(2)
        the_person "Okay [the_person.mc_title], if you want it I'll do it for you."

    the_person "I'll get it scheduled, if we're lucky I'll be able to have it done in a few days."
    if affair_role in the_person.special_role:
        the_person "I don't know if my [so_title] would want to kill you or thank you for this."

    $ the_person.event_triggers_dict["getting boobjob"] = True #Reset the flag so you can ask her to get _another_ boobjob.

    $ got_boobjob_action = Action("Girlfriend Got Boobjob", girlfriend_got_boobjob_requirement, "girlfriend_got_boobjob_label", args = the_person, requirement_args = day + renpy.random.randint(3,6))
    $ mc.business.mandatory_crises_list.append(got_boobjob_action)
    return

label girlfriend_got_boobjob_label(the_person):
    call got_boobjob(the_person) from _call_got_boobjob_1
    $ girlfriend_boob_brag_action = Action("Girlfriend Boobjob Brag", girlfriend_boob_brag_requirement, "girlfriend_boob_brag_label")
    $ the_person.on_talk_event_list.append(girlfriend_boob_brag_action)
    return

label girlfriend_boob_brag_label(the_person): #TODO: Decide if we need a little alt-dialogue for the affair side of things.
    the_person "Hey [the_person.mc_title], what do you think?"
    if the_person.get_opinion_score("showing her tits") < 0:
        "She puts her arms behind her, revealing her newly enlarged chest."
        the_person "These feel so... excessive. It feels like everyone is staring at them all the time now."
        $ the_person.change_slut_temp(-1 + the_person.get_opinion_score("showing her tits"))
    else:
        "She pushes her chest out towards you, shaking her tits just a little."
        the_person "I hope you like them, maybe we can have some fun with them later."
        $ the_person.change_slut_temp(2)

    call talk_person(the_person) from _call_talk_person_9
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

    $ the_person.event_triggers_dict["getting boobjob"] = False #Reset the flag so you can ask her to get _another_ boobjob.
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
