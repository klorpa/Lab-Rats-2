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

label ask_break_up_label(the_person):
    # Stop being in a relationship.
    mc.name "[the_person.title], can we talk?"
    if the_person.happiness > 100:
        the_person.char "Sure, what's up?"
    else:
        the_person.char "Oh no, that's never good."

    mc.name "There's no easy way to say this, so I'll just say it: I think we should break up."
    $ the_person.draw_person(emotion = "sad")
    #TODO: Add a varient whre you've passed below the girlfriend threshold and she feels the same way.

    $ the_person.change_happiness(-(the_person.love - 40)) #TODO: Double check this vs. the girlfriend love threshold.
    "She seems to be in shock for a long moment, before slowly nodding her head."
    the_person.char "Okay... I don't know what to say."
    $ the_person.change_love(-10)
    mc.name "I'm sorry, but it's just the way things are."
    $ the_person.special_role.remove(girlfriend_role)
    return

label ask_be_girlfriend_label(the_person):
    #Requires high love, if successful she becomes your girlfriend (which unlocks many other options). Requires high lvoe and her not being in a relationship.
    #Hide this event at low love, show it when it at it's lowest love possibility and let it fail out for specific reasons (thus informing the player WHY it failed out).

    mc.name "[the_person.title], can I talk to you about something important?"
    the_person.char "Of course. What's on your mind."
    mc.name "I've been thinking about this for a while. I really like you and I hope you feel the same way about me."
    mc.name "I'd like to make our relationship official. What do you say?"

    if the_person.relationship != "Single":
        $ so_title = SO_relationship_to_title(the_person.relationship)

        if the_person.get_opinion_score("cheating on men") > 0:
            # She likes cheating on men and offers to have an affair with you instead. Adds the affair role.
            "She takes a moment before responding."
            the_person.char "I mean, I already have a [so_title] and I can't just leave him like this."
            the_person.char "But... Maybe he doesn't need to know about any of this. Do you think you could be discreet."
            $ the_person.discover_opinion("cheating on men")
            menu:
                "Have an affair with [the_person.title].":
                    mc.name "I can be if that's what you need."
                    $ the_person.draw_person(emotion = "happy")
                    $ the_person.special_role.append(affair_role)
                    $ the_person.change_slut_temp(2)
                    "She leans forward and kisses you, putting an arm around your waist and pulling you close. When she breaks the kiss she looks deep into your eyes."
                    the_person.char "Well then, you know where to find me."

                "Refuse.":
                    mc.name "I can't do that. I need a relationship I can count on."
                    $ the_person.change_love(-3)
                    the_person.char "Right... Well, if you change your mind I'll be here."

        else:
            # She's just not into it, no matter how slutty she is. You'll have to seduce her to convince her first to have an affair.
            $ the_person.draw_person(emotion = "sad")
            "She takes a long moment before responding."
            the_person.char "Oh [the_person.mc_title], I'm so flattered, but you know that I have a [so_title]."
            if the_person.kids > 0:
                if the_person.kids > 1:
                    the_person.char "I would never dream of leaving him, and it would devastate our children."
                else:
                    the_person.char "I would never dream of leaving him, and it would devastate our child."
            else:
                the_person.char "I would never dream of leaving him."


            if the_person.sex_record.get("Vaginal Sex", 0) > 0:
                mc.name "You didn't care about him when we were fucking."
                if the_person.sluttiness > 50:
                    the_person.char "That didn't mean anything, we were just having fun. This is so much more serious than that."
                else:
                    the_person.char "I don't know what I was thinking, that was a mistake."

            the_person.char "I care about you a lot, but it's just not something I could do."
            mc.name "I'm sorry to hear that. I hope we can still be friends."
            $ the_person.draw_person()
            the_person.char "As long as you understand where we stand, I think we can be."


    elif any(relationship in [sister_role,mother_role,aunt_role,cousin_role] for relationship in the_person.special_role):
        # She's related to you, so she won't do it. Note that we aren't using has_family_taboo(), which would allow for a postiive incest opinion to allow this.
        # Future events will let you make this happen somehow (and in that case an incest opinion will make those events easier/trigger earlier, so training a girl makes sense).
        if sister_role in the_person.special_role:
            the_person.char "I love you like a brother... but just as a brother, you know?"
            the_person.char "Could you imagine what people would say about us? It would be crazy!"
            the_person.char "So... I guess no? Sorry."

        elif mother_role in the_person.special_role:
            the_person.char "Oh sweety, I love you more than anyone in the world, but we could never do that."
            the_person.char "It's just not something people do."
            the_person.char "Let's just talk about something else, okay?"

        elif aunt_role in the_person.special_role:
            the_person.char "I... I don't know what to say [the_person.mc_title]. I love you like you were my own, but we could never have a real relationship together."
            the_person.char "Could you imagine what your mother would say about that, dating her sister? She would go crazy!"
            the_person.char "Come on, let's talk about something else."

        elif cousin_role in the_person.special_role:
            the_person.char "You and me being, like, boyfriend and girlfriend? Ha, you must be crazy. Have you been inhaling fumes at work?"
            the_person.char "I mean sure, I've come around on you and think you're not a total loser now, but we're cousins. Our parents would kill us."
            the_person.char "So yeah, that's going to be a no from me."

    else:
        # She agrees, you're now in a relationship! Congradulations!
        $ the_person.draw_person(emotion = "happy")
        $ the_person.change_happiness(15)
        $ the_person.change_love(5)
        if the_person.age > 40:
            the_person.char "Oh I'm so happy to hear you say that! I was worried about our age difference, but I don't want that to stop us!"
            "She puts her arms around you and pulls you close."

        else:
            the_person.char "Oh my god, I'm so happy! Yes, I want you to be your girlfriend!"
            "She puts her arms around you and pulls you close."
        "She kisses you, and you kiss her back."
        $ the_person.special_role.append(girlfriend_role)

    return

label caught_cheating_label(the_other_girl, the_girlfriend): #Note: the_other_girl is stored as an argument in the event, while the_girlfriend is passed as an extra argument, so they are listed backwards.
    # This is an event added to the on_enter_room list for the girlfriend after she catches you cheating.

    if girlfriend_role not in the_girlfriend.special_role:
        return #She's lost the role somehow between now and when she caught you, so clear this out and move on.

    $ the_girlfriend.draw_person(emotion = "angry")
    "[the_girlfriend.title] storms up to you as soon as she sees you."
    the_girlfriend.char "What the fuck [the_girlfriend.mc_title]! How could you do that to me?"
    mc.name "Calm down, everything's okay."
    #TODO: Add some dialogue in case she's a particularly important person (ie. friend, mother)
    the_girlfriend.char "Really? Everything's okay while you're with another woman?"
    # Note: This only happens if she saw something happening that was too slutty for her, slutty girls think it's totally fine and normal.
    mc.name "Just let me explain..."
    $ the_girlfriend.change_love(-25)
    $ the_girlfriend.change_happiness(-20)
    if the_girlfriend.love < 60:
        the_girlfriend.char "I don't want to hear it. You're a lying scumbag who broke my heart..."
        $ the_girlfriend.special_role.remove(girlfriend_role)
        the_girlfriend.char "We're done! Through! Finished!"
        "She turns around and storms off."
        $ renpy.scene("Active")
    else:
        the_girlfriend.char "How could you possibly explain that?"
        mc.name "We were just fooling around, it didn't mean anything. Come on, you know I love you, right?"
        "She glares at you, but bit by bit her expression softens."
        "You sit down with her and calm her down, until finally she breaks and hugs you."
        the_girlfriend.char "Just never do that to me again, okay?"
        $ the_girlfriend.change_slut_temp(4)
        $ the_girlfriend.change_obedience(4)
        mc.name "Of course not, you'll never catch me doing that again."
        the_girlfriend.char "And I never want to see that bitch anywhere around you, okay?"
        mc.name "Of course."

    $ town_relationships.worsen_relationship(the_girlfriend, the_other_girl)
    $ town_relationships.worsen_relationship(the_girlfriend, the_other_girl)
    return

label ask_change_hair_style(the_person):
    #Requires moderate obedience. Ask her to cut her hair a different way.

    return

label ask_dye_hair(the_person):
    #Requires moderate obedience. Ask her to dye her hair a different colour.

    return

label ask_get_boobjob(the_person):
    #Requires high obedience. Ask her to get a boob job (you foot the bill, obviously).

    return

label plan_date_night(the_person):
    #Special date for girlfriends only, you invite her over (or go over to her place?) and spend time watching a movie or something.

    return
