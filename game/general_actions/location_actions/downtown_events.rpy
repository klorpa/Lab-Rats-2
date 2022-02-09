init -1 python:
    def downtown_search_requirement():
        if time_of_day >= 4:
            return "Too late to explore."
        else:
            return True

    def find_nothing_requirement():
        return True

    def lady_of_the_night_requirement():
        if time_of_day == 3:
            return True

    def meet_person_requirement():
        return True


label downtown_search_label(advance_time = True):
    "You devote some time to wandering the city streets with no particular destination in mind."
    call downtown_time_description from _call_downtown_time_description
    #If there are events we want to trigger as soon as the first conditions are met they can go here.
    if time_of_day == 3 and not strip_club.visible:
        call discover_stripclub_label from _call_discover_stripclub_label #Discover the strip club location

    #Otherwise we add some random events and draw from the list.

    else:
        python:
            list_of_downtown_events = []
            find_nothing_action = Action("Find nothing", find_nothing_requirement, "find_nothing_label")
            lady_of_the_night_action = Action("Lady of the night", lady_of_the_night_requirement, "lady_of_the_night_label")
            meet_person_action = Action("Meet person", meet_person_requirement, "meet_person_label")

            list_of_downtown_events.append([find_nothing_action,10])
            list_of_downtown_events.append([lady_of_the_night_action,3])
            list_of_downtown_events.append([meet_person_action,6]) #Now is combined with the find cash event.

            possible_downtown_events = []
            for possible_event in list_of_downtown_events: #Make a list of the valid events.
                if possible_event[0].is_action_enabled():
                    possible_downtown_events.append(possible_event)

            the_event = get_random_from_weighted_list(possible_downtown_events)
            the_event.call_action()

    if advance_time:
        call advance_time from _call_advance_time_26
    return

label downtown_time_description():
    if time_of_day == 0:
        "The city is quiet this early in the morning. In a couple of hours the streets will be packed with people, but right now you're free to wander almost alone."

    elif time_of_day == 1:
        "The city streets are filled with people, all of them hurrying one way or another. You shuffle through the crowds, comfortable in your anonymity."

    elif time_of_day == 2:
        "The streets are filled with business people out for lunch. You shuffle through the crowds, turning down unexplored side streets."

    elif time_of_day == 3:
        "As the sun sets the downtown crowds begin to thin and change. The office workers are gone, replaced by those looking for entertainment and excitement."
    return

label discover_stripclub_label():
    "After some time you find yourself standing in front of a bright neon sign sitting above an otherwise nondescript door."
    $ club_name = strip_club.formal_name
    "{color=#29e729}GIRLS GIRLS GIRLS{/color}\n{color=#e72929}[club_name]{/color}"
    $ strip_club.visible = True
    menu:
        "Go inside.":
            "You open the door and are immediately assaulted by pulsing, base heavy music."

            $ mc.change_location(strip_club)



        "Keep exploring.":
            "You make a mental note of this location in case you want to come back later, but decide against visiting it."
            call downtown_search_label(advance_time = False) from _call_downtown_search_label
    return

label find_nothing_label():
    if time_of_day == 0:
        "Time passes uneventfully and the city begins to come to life around you."

    elif time_of_day == 1:
        "The morning passes uneventfully and soon lunch is approaching."

    elif time_of_day == 2:
        "Soon the sun is getting low in the sky, but you have found nothing of interest."

    elif time_of_day == 3:
        "You explore side streets and dark alleys, but you find nothing that holds your interest."

    else:
        #Catchall, but it shouldn't ever come up.
        "After a couple of wandering you haven't turned up anything interesting."
    return

label lady_of_the_night_label():
    # You run into a lady who propositions you for money.
    $ the_person = create_random_person(start_sluttiness = renpy.random.randint(25, 40))
    $ the_person.set_mc_title("Sir")
    $ the_person.add_job(prostitute_job)
    #$ the_person.add_role(prostitute_role)
    "You're lost in thought when a female voice calls out to you."
    the_person "Excuse me, [the_person.mc_title]."
    $ the_person.draw_person()
    mc.name "Yes?"
    the_person "You're looking a little lonely all by yourself. Are you looking for a friend to keep you warm?"
    "Her tone suggests that her \"friendship\" won't come free."
    menu:
        "Pay her. -$200":
            $ the_person.generate_home()
            $ downtown.add_person(the_person) #If you pay her add her to the location so that she is kept track of in the future.
            mc.name "That sounds nice. It's nice to meet you..."
            $ the_person.set_title(get_random_title(the_person))
            $ the_person.set_possessive_title(get_random_possessive_title(the_person))
            the_person "You can call me [the_person.title]. For two hundred dollars I'll be your best friend for the next hour."
            $ mc.business.change_funds(-200)
            $ the_person.change_obedience(1)
            "The streets are quiet this time of night. You pull your wallet out and hand over the cash."
            "She takes it with a smile and tucks it away, then wraps herself around your arm."

            $ the_person.add_situational_slut("prostitute", 40, "No point being shy about it, this is my job!")
            $ the_person.add_situational_obedience("prostitute", 20, "I'm being paid for this, I should do whatever he wants me to do.")
            call fuck_person(the_person, private = True, ignore_taboo = True) from _call_fuck_person_26
            $ the_report = _return
            $ the_person.clear_situational_slut("prostitute")
            $ the_person.clear_situational_obedience("prostitute")

            if the_report.get("girl orgasms",0) > 0:
                "It takes [the_person.title] a few moments to catch her breath."
                the_person "Maybe I should be paying you... Whew!"

            $ the_person.review_outfit()

            the_person "It's been fun, if you ever see me around maybe we can do this again."
            "She gives you a peck on the cheek, then turns and struts off into the night."
            $ clear_scene()

        "Say no.":
            mc.name "Thanks for the offer, but no thanks."
            "She shrugs."
            the_person "Suit yourself."

    return

label meet_person_label():
    # You see a women drop some cash out of her purse. YOu can either return it for an introduction+bonus love OR
    # Keep it because it's money and you like money.
    $ the_person = create_random_person()
    $ the_person.draw_person(position = "walking_away")
    "While you're wandering a woman hurries past you on the sidewalk, jogging for a bus waiting up the street."
    "A few steps ahead of you she stumbles and trips."
    $ the_person.call_dialogue("surprised_exclaim")
    "She rushes to get back to her feet, unaware that her wallet has slipped out and is sitting on the sidewalk."
    "You crouch down to pick it up. A discreet check reveals there is a sizeable amount of cash inside."
    menu:
        "Return everything.":
            $ downtown.add_person(the_person)
            $ the_person.generate_home()
            "You speed up to a jog to catch the woman."
            mc.name "Excuse me! You dropped your wallet!"
            $ the_person.draw_person()
            "She pauses and turns around."
            the_person "What? Oh! Oh my god!"
            "You hold out her wallet for her and she takes it back."
            the_person "Thank you so much, I really need to..."
            "She glances over her shoulder, and the two of you watch as her bus pulls away. She sighs."
            the_person "Well never mind, I guess I have some time. Thank you."
            mc.name "No problem, I'd do it for anyone."

            "She holds out her hand to shake yours."
            $ title_choice = get_random_title(the_person)
            $ the_person.set_title(title_choice)
            $ the_person.set_possessive_title(get_random_possessive_title(the_person))
            the_person "Thank you so much. I'm [the_person.title]."
            call person_introduction(the_person, girl_introduction = False) from _call_person_introduction_1
            $ mc.change_locked_clarity(5)
            "You shake her hand. You and [the_person.title] chat while she waits for the next bus to come by."
            $ the_person.change_happiness(10)
            $ the_person.change_love(8)

            menu:
                "Ask for her number.":
                    mc.name "I hope this isn't too forward, but could I have your number?"
                    if the_person.relationship == "Single" or the_person.get_opinion_score("cheating on men") > 0:
                        "She smiles and nods, holding her hand out for your phone."
                        the_person "Maybe we can go out for drinks. I owe you something for saving my butt today."
                        "[the_person.title] types in her number and hands back the device."
                        $ mc.phone.register_number(the_person)
                        mc.name "I'm going to hold you to that."
                        "A moment later her bus pulls up and she steps on."
                        the_person "Don't be a stranger."
                        "She waves from her seat as the bus pulls away."
                        $ clear_scene()
                    else:
                        $ so_title = SO_relationship_to_title(the_person.relationship)
                        the_person "I don't know... I've got a [so_title], I don't want him getting the wrong idea."
                        menu:
                            "Convince her." if mc.charisma >= 3:
                                "You smile and pour on the charm."
                                mc.name "You're allowed to have men as friends, right? He can't seriously be that jelous."
                                the_person "Well... You're right. Here..."
                                $ mc.phone.register_number(the_person)
                                "She reaches out for your phone. You hand it over and wait for her to type in her number."
                                the_person "There. Now don't be a stranger, I owe you a drink after everything you've done for me."
                                mc.name "I'm going to hold you to that."
                                "A moment later her bus pulls up and she steps on."
                                the_person "Don't be a stranger."
                                "She waves from her seat as the bus pulls away."
                                $ clear_scene()

                            "Convince her.\nRequires: 3 Charisma (disabled)" if mc.charisma < 3:
                                pass


                            "Let it go.":
                                mc.name "Ah, I understand."
                                the_person "Yeah, you know how it is..."
                                "A minute later the bus arrives. She steps onboard and waves goodbye from the window as she pulls away."
                                $ clear_scene()



                "Say goodbye.":
                    mc.name "I should really get going. Glad I could help you out."
                    the_person "Thank you again, you've saved my whole day. Maybe we'll see each other again."
                    "She waves goodbye as you walk away, leaving her waiting at the bus stop alone."
                    $ clear_scene()



        "Keep the cash.\n{color=#0F0}+$200{/color}":
            $ mc.business.change_funds(200)
            "You slip the cash out of the womans wallet and watch as she rushes to catch her bus."
            $ clear_scene()
            "She gets on and the bus pulls away. When you pass a mailbox you slide the wallet inside - at least she'll get it back."


    return
