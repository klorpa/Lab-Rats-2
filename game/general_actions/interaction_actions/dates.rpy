# Contains all of the descriptions for different date results, and shared things such as a girl taking you home after a successful date.

#Note: This only contains generic dates, if a date is specific to a role (ie. the special fuck date available to paramours) it's in their role file.
#Note: These are only the dates themselves. How they are added (ie. what specific thing triggered them) is in whatever file is appropriate (usually chat_action.rpy, since you ask her out)
init -2 python:
    def shopping_date_requirement(the_person):
        if time_of_day == 0:
            return "Too early to go shopping."
        elif time_of_day >= 4:
            return "Too late to go shopping."
        return True


label date_conversation(the_person):
    $ opinion_question_list = []
    python: #Generates a list with a few (usually 4, unless there's some opinion collision, but it's not important enough to fliter things out more intelligently) opinions, one of which she likes
        for x in __builtin__.range(3):
            possible_opinions = get_random_opinion()
            if possible_opinions not in opinion_question_list:
                opinion_question_list.append(possible_opinions)

        key_opinion = the_person.get_random_opinion(only_positive = True)

        if key_opinion is not None and key_opinion not in opinion_question_list:
            opinion_question_list.append(key_opinion)

        renpy.random.shuffle(opinion_question_list)

    $ formatted_opinion_list = []
    python:
        for item in opinion_question_list:
            formatted_opinion_list.append(["Chat about " + item, item])


    $ conversation_choice = renpy.display_menu(formatted_opinion_list,True,"Choice")
    $ the_person.discover_opinion(conversation_choice)
    $ score = the_person.get_opinion_score(conversation_choice)
    $ kiss_after = False
    if score > 0:
        "You steer the conversation towards [conversation_choice] and [the_person.title] seems more interested and engaged."
        $ kiss_after = True
        $ the_person.change_love(10, max_modified_to = 50)
        $ the_person.change_happiness(5)
    elif score == 0:
        "You steer the conversation towards [conversation_choice]. [the_person.title] chats pleasantly with you, but she doesn't seem terribly interested in the topic."
        $ the_person.change_love(5, max_modified_to = 50)
    else: #Negative score
        "You steer the conversation towards [conversation_choice]. It becomes quickly apparent that [the_person.title] is not interested in talking about that at all."
        $ the_person.change_love(1, max_modified_to = 35)
    return kiss_after


label lunch_date_label(the_person): #Could technically be included in the planning phase, but broken out to fit the structure of the other events.
    the_person "So, where do you want to go?"
    $ food_types = ["chinese food","thai food","italian food","sushi","korean barbeque","pizza","sandwiches"]
    $ the_type = get_random_from_list(food_types)
    mc.name "I know a nice place nearby. How do you like [the_type]?"
    the_person "No complaints, as long as it's good!"
    mc.name "Alright, let's go then!"
    "You and [the_person.title] walk together to a little lunch place nearby. You chat comfortably with each other as you walk."
    $ renpy.show("restaurant", what = restaraunt_background)
    "A bell on the door jingles as you walk in."
    mc.name "You grab a seat and I'll order for us."
    $ clear_scene()
    "You order food for yourself and [the_person.possessive_title] and wait until it's ready."
    $ mc.business.funds += -30
    $ the_person.draw_person(position = "sitting")
    "When it's ready you bring it over to [the_person.title] and sit down at the table across from her."
    if renpy.random.randint(0,100) < 40:
        the_person "Mmm, it looks delicious. I'm just going to wash my hands, I'll be back in a moment."
        $ clear_scene()
        "[the_person.possessive_title] stands up heads for the washroom."
        menu:
            "Add some serum to her food." if mc.inventory.get_any_serum_count() > 0:
                call give_serum(the_person) from _call_give_serum_20
                if _return:
                    "Once you're sure nobody else is watching you add a dose of serum to [the_person.title]'s food."
                    "With that done you lean back and relax, waiting until she returns to start eating your own food."
                else:
                    "You think about adding a dose of serum to [the_person.title]'s food, but decide against it."
                    "Instead you lean back and relax, waiting until she returns to start eating your own food."

            "Add some serum to her food.\nRequires: Serum (disabled)" if mc.inventory.get_any_serum_count() == 0:
                pass

            "Leave her food alone.":
                "You lean back and relax, waiting until [the_person.title] returns to start eating."

        $ the_person.draw_person(position = "sitting")
        the_person "Thanks for waiting, now let's eat!"
    else:
        the_person "Mmm, it looks delicious. Or maybe I'm just really hungry. Either way, let's eat!"
    "You dig into your food, chatting between bites about this and that. What do you talk about?"

    call date_conversation(the_person) from _call_date_conversation_1
    $ kiss_after = _return
    "Before you know it you've both finished your lunch and it's time to leave. You walk [the_person.title] outside and get ready to say goodbye."
    the_person "This was fun [the_person.mc_title], we should do it again."
    if the_person.love > 30 and not mc.phone.has_number(the_person):
        the_person "Can I give you my number, so you can call me some time?"
        mc.name "Of course you can."
        "You hand her your phone. She types in her contact information, then hands it back with a smile."
        $ mc.phone.register_number(the_person)

    if not the_person.has_family_taboo() and (the_person.relationship == "Single" or the_person.get_opinion_score("cheating on men") > 0) and kiss_after:
        "She steps in close and kisses you. Her lips are soft and warm against yours."
        "After a brief second she steps back and smiles."
        mc.name "Yeah, we should. I'll see you around."

    else:
        "She steps close and gives you a quick hug, then steps back."
        mc.name "Yeah, we should. I'll see you around."

    $ clear_scene()
    call advance_time() from _call_advance_time_29
    return


label movie_date_label(the_person):
    #The actual event produced when it's time to go on your date.
    $ mc.business.event_triggers_dict["date_scheduled"] = False #Deflag this event so you can schedule a date with another person for next week.
    "You have a movie date planned with [the_person.title] right now."

    menu:
        "Get ready for the date. {image=gui/heart/Time_Advance.png}" if mc.business.funds >= 50:
            pass

        "Get ready for the date.\nRequires: $50 (disabled)" if mc.business.funds < 50:
            pass

        "Cancel the date. (tooltip)She won't be happy with you canceling last minute.":
            "You get your phone out and text [the_person.title]."
            $ mc.start_text_convo(the_person)
            mc.name "I'm sorry, but something important came up at the last minute. We'll have to reschedule."
            $ the_person.change_love(-5)
            $ the_person.change_happiness(-5)
            the_person "I hope everything is okay. Maybe we can do this some other time then."
            $ mc.end_text_convo()
            return

    if mom_date_intercept_requirement(mom, the_person) and renpy.random.randint(0,100) < (25 + mom.love):
        call mom_date_intercept(mom, the_person) from _call_mom_date_intercept
        if _return:
            $ clear_scene()
            return "Advance Time"

    "You get ready and text [the_person.title] confirming the time and place. A little while later you meet her outside the theater."
    $ mc.phone.add_non_convo_message(the_person, "On my way to the theater. See you soon?")
    $ mc.phone.add_non_convo_message(the_person, "Almost there, I'll meet you outside.", as_mc = True)
    $ the_person.draw_person()
    the_person "Hey, good to see you!"
    the_person "I'm ready to go in, what do you want to see?"
    $ renpy.show("Theater", what = theater_background)
    $ movie_type = None
    $ likes_movie = False
    menu:
        "Watch an action movie.":
            $ action_movie_list = ["The Revengers", "Raiders of the Found Ark", "Die Difficult", "Mission: Improbable", "Wonderful Woman", "John Wicked: Part 3", "The Destructonator", "Waterman"]
            $ the_choice = get_random_from_list(action_movie_list)
            $ movie_type = "action"
            if the_person.personality.personality_type_prefix == wild_personality.personality_type_prefix or the_person.personality.default_prefix == wild_personality.personality_type_prefix: #If it's a wild or wild derived personality type
                $ likes_movie = True
            mc.name "Yeah, I've wanted to see [the_choice] for a while. I'll go get us tickets."

        "Watch a comedic movie.":
            $ comedy_movie_list = ["Spooky Movie", "Aaron Powers", "Dumber and Dumberest-er", "Ghostblasters", "Shaun of the Undead"]
            $ the_choice = get_random_from_list(comedy_movie_list)
            $ movie_type = "comedy"
            if the_person.personality.personality_type_prefix == relaxed_personality.personality_type_prefix or the_person.personality.default_prefix == relaxed_personality.personality_type_prefix:
                $ likes_movie = True
            mc.name "I thought we'd both enjoy [the_choice]. I'll go get us tickets."

        "Watch a romantic movie.":
            $ romance_movie_list = ["Olympic", "Britannic","The Workbook", "East Side Tale", "Pottery Poltergeist"]
            $ the_choice = get_random_from_list(romance_movie_list)
            $ movie_type = "romantic"
            if the_person.personality.personality_type_prefix == reserved_personality.personality_type_prefix or the_person.personality.default_prefix == reserved_personality.personality_type_prefix:
                $ likes_movie = True
            mc.name "I thought [the_choice] would be a good fit for us. You just wait here, I'll go get us tickets."

        "Watch a foreign film.":
            $ foreign_movie_list = ["that one in French", "that one in Italian", "that one in Russian", "that one in Japanese", "that one in Mandarin", "that one that's silent"]
            $ the_choice = get_random_from_list(foreign_movie_list)
            $ movie_type = "foreign"
            if the_person.personality.personality_type_prefix == introvert_personality.personality_type_prefix or the_person.personality.default_prefix == introvert_personality.personality_type_prefix:
                $ likes_movie = True
            mc.name "I haven't heard much about it, but I think we should watch [the_choice]. It should be a really unique one."
            mc.name "I'll go get us tickets; be back in a moment."

    if the_person.personality is bimbo_personality and movie_type != "foreign":
        $ likes_movie = True # Bimbos like anything other than weird art pieces.

    #TODO: Generate a girl and assign them a uniform.
    "You walk up to the ticket booth and get tickets for yourself and [the_person.possessive_title]."
    $ mc.business.funds += -50

    "Tickets in hand, you rejoin [the_person.title] and set off to find your theater."
    the_person "Did you want to get us some popcorn or anything like that?"
    menu:
        "Stop at the concession stand. -$20" if mc.business.funds >= 20:
            mc.name "Sure, you run ahead and I'll go get us some snacks."
            $ clear_scene()
            $ mc.business.funds += -20
            "You give [the_person.possessive_title] her ticket and split up. At the concession stand you get a pair of drinks and some popcorn to share."
            menu:
                "Put a dose of serum in her drink." if mc.inventory.get_any_serum_count() > 0:
                    call give_serum(the_person) from _call_give_serum_14

                "Put a dose of serum in her drink.\nRequires: Serum (disabled)" if mc.inventory.get_any_serum_count() == 0:
                    pass

                "Leave her drink alone.":
                    pass

            "Snacks in hand you return to [the_person.title]. She takes a sip from her drink as you settle into your seat beside her."


        "Stop at the concession stand. -$20 (disabled)" if mc.business.funds < 20:
            pass

        "Just go to the movie.":
            mc.name "That stuff is always so overpriced, I hate giving them the satisfaction."
            $ the_person.change_happiness(-2)
            the_person "Right. Sure."
            "You find your theater, pick your seats, and settle down next to each other for the movie."


    $ the_person.draw_person(position = "sitting", lighting = [0.5,0.5,0.5])
    "You chat for a few minutes until the theater lights dim and the movie begins."

    if likes_movie: #She's enjoying the movie. Good for love gain, and you may be able to feel her up while she's enjoying the movie.
        "Halfway through the movie it's clear that [the_person.title] is having a great time. She's leaning forward in her seat, eyes fixed firmly on the screen."
        $ mc.change_locked_clarity(10)
        "As the movie approaches its climax she reaches her hand down and finds yours to hold."
        "When it's finished you leave the theater together, still holding hands."
        $ the_person.draw_person()
        mc.name "So, did you like the movie?"
        the_person "It was amazing! Let's watch something like that next time."
        $ the_person.change_love(10, max_modified_to = 80)

    else: #She's bored. Bad for love gain, but good for getting her to fool around. She may start to feel you up to disctract herself.
        "Halfway through the movie it's becoming clear that [the_person.title] isn't enthralled by it."
        if (the_person.sluttiness + the_person.get_opinion_score("public sex") * 5) > 50 and (the_person.relationship == "Single" or the_person.get_opinion_score("cheating on men") > 0) and not the_person.has_family_taboo():
            $ mc.change_locked_clarity(10)
            "While you're watching you feel her rest her hand on your thigh. She squeezes it gently and slides her hand up higher and higher while whispering into your ear."
            the_person "I'm bored. You don't mind if I make this a little more interesting, do you?"
            "You take a quick look around. The theater you're in is mostly empty, and nobody is in the same row as you."
            menu:
                "Go ahead.":
                    mc.name "I'm certainly not going to stop you."
                    $ mc.change_locked_clarity(10)
                    "Her hand slides up to your waist and undoes the button to your pants. You get a jolt of pleasure as her fingers slide onto your hardening cock."
                    "[the_person.title] stays sitting in her seat, eyes fixed on the movie screen as she begins to fondle your dick."
                    "As you get hard she starts to stroke you off. Her hand is warm and soft, and the risk of being caught only enhances the experience."
                    $ mc.change_locked_clarity(10)
                    "After a few minutes [the_person.possessive_title] brings her hand to her mouth, licks it, and then goes back go jerking you off with her slick hand."

                    if (the_person.sluttiness + the_person.get_opinion_score("public sex") * 5) > 65 and (the_person.relationship == "Single" or the_person.get_opinion_score("cheating on men") > 0) and not the_person.has_family_taboo():
                        "You're enjoying the feeling of her wet hand sliding up and down your cock when she stops. You're about to say something when she slides off of her movie seat and kneels down in the isle."
                        $ the_person.draw_person(position = "blowjob", special_modifier = "blowjob", lighting = [0.5, 0.5, 0.5])
                        $ mc.change_locked_clarity(20)
                        "Without a word she slides your hard dick into her mouth and starts to suck on it. You struggle to hold back your moans as she blows you."
                        "You rest a hand on the top of her head and keep a lookout in the theater, but nobody seems to have noticed."
                        "She comes up for air slides up your body, whispering into your ear."
                        the_person "Do you want to go to the bathroom and fuck me, or do you want to finish in my mouth right here?"
                        menu:
                            "Fuck her.":
                                "You zip up your pants and stand up. [the_person.title] takes your hand and you rush out of the theater."
                                $ movie_bathroom = Room("threater bathroom", "Theather Bathroom", [], bathroom_background, [], [], [], False, [0,0], visible = False) #TODO: Decide if we need any objects in the bathroom
                                $ movie_bathroom.show_background()
                                $ movie_bathroom.add_object(make_wall())
                                $ movie_bathroom.add_object(make_floor())
                                $ mc.change_location(movie_bathroom)
                                $ the_person.change_arousal(20 + (the_person.get_opinion_score("public sex") * 10))
                                $ mc.change_arousal(40)
                                "You hurry into the womens bathroom and lock yourselves in an empty stall."
                                call fuck_person(the_person, private = True) from _call_fuck_person_28
                                $ the_report = _return
                                $ the_person.call_dialogue("sex_review", the_report = the_report)
                                $ the_person.review_outfit()
                                $ renpy.show("Theater", what = theater_background)
                                "You slip out of the bathroom as quickly as possible and return to your seats with some time pleasantly passed."

                            "Cum right here.":
                                mc.name "I want you to finish me here."
                                $ mc.change_locked_clarity(20)
                                "She purrs in your ear and slides back down to her knees again. Her warm mouth wraps itself around your shaft and she starts to blow you again."
                                "It doesn't take long for her to bring you to the edge of your orgasm."
                                $ climax_controller = ClimaxController(["Cum in her mouth.","mouth"],["Cum down her throat.","throat"])
                                $ the_choice = climax_controller.show_climax_menu()
                                if the_choice == "Cum in her mouth.":
                                    $ climax_controller.do_clarity_release()
                                    "You clutch at the movie seat arm rests and suppress a grunt as you climax, blowing your hot load into [the_person.title]'s mouth."
                                    $ the_person.cum_in_mouth()
                                    $ the_person.draw_person(position = "sitting")
                                    "She waits until you're finished, then pulls off your cock, wipes her lips on the back of her hand, and sits down next to you."
                                    $ the_person.change_slut(1 + the_person.get_opinion_score("drinking cum"), 60)
                                    $ the_person.discover_opinion("drinking cum")
                                    the_person "Mmm, thank you. That was fun."
                                    "She takes your hand and holds it. You lean back, thoroughly spent, and zone out for the rest of the movie."
                                elif the_choice == "Cum down her throat.":
                                    "You grab onto [the_person.title]'s head and pull her as deep as you can get her onto your cock."
                                    if the_person.get_opinion_score("being submissive") > 0 or the_person.get_opinion_score("drinking cum") > 0:
                                        "She gags and twitches, but shifts to let you bury yourself entirely in her throat."
                                        $ climax_controller.do_clarity_release()
                                        "You cum, pumping your load out in big, hot pulses right into her stomach. In the dim theater light you can see her flutter with each new deposit."
                                        $ the_person.cum_in_mouth()
                                        "When you're entirely spent you let go of [the_person.possessive_title]'s head and sit back with a sigh."
                                        $ the_person.change_slut(2 + the_person.get_opinion_score("being submissive") + the_person.get_opinion_score("drinking cum"), 80)
                                        $ the_person.discover_opinion("being submissive")
                                        $ the_person.discover_opinion("drinking cum")
                                        "[the_person.title] doesn't move for another few long seconds. You feel her throat constrict a few times as she swallows the last of your cum first."
                                        $ the_person.draw_person(position = "sitting")
                                        "She finally slides off of your dick and sits back down in her seat. She takes your hand and holds it tight in hers."
                                        the_person "Thank you [the_person.mc_title]. That was fun."

                                    else:
                                        "She gags and tries to pull back, but you hold your dick deep down her throat as you cum."
                                        $ climax_controller.do_clarity_release()
                                        "You pump your load out in big hot pulses. She twitches with each new deposit of semen, barely keeping herself in control."
                                        $ the_person.cum_in_mouth()
                                        $ the_person.draw_person(position = "kneeling1", emotion = "angry")
                                        "When you're entirely spent you let go of [the_person.possessive_title]'s head and sit back with a sigh."
                                        $ the_person.change_love(-2)
                                        $ the_person.change_slut(1, 80)
                                        $ the_person.change_obedience(1)
                                        "She pulls off your dick and gasps for breath. When she's recovered she glares up at you."
                                        mc.name "Sorry, I got carried away."
                                        $ the_person.draw_person(position = "sitting")
                                        "[the_person.title] slides back into her chair beside you."
                                        the_person "Yeah. A little. At least it wasn't boring..."
                                        "You lean back and zone out for the rest of the movie, feeling thoroughly spent."


                "Tell her to knock it off.":
                    mc.name "I just want to watch a movie together. Can you at least try and pay attention?"
                    $ the_person.change_obedience(2)
                    $ the_person.change_happiness(-5)
                    $ the_person.change_love(-1)
                    "She pulls her hand back and sighs."
                    the_person "Aw, you're no fun."

        else:
            # She just annoys you by asking random questions
            the_person "Who is that again?"
            mc.name "He's working for the bad guy."
            the_person "Wait, I thought he was just with the good guys though."
            mc.name "He was lying. It's hard to explain."
            "Eventually the movie is over and you leave the theater together."

        $ the_person.draw_person()
        mc.name "So, did you like the movie?"
        the_person "It was okay. Let's try something else next time though."
        $ the_person.change_love(5, max_modified_to = 80)

    the_person "There will be a next time, right?"
    mc.name "I'd love for there to be."
    $ the_person.change_happiness(10)

    if the_person.has_role(sister_role) or the_person.has_role(mother_role): #You live at home with those two, so it would be weird to kiss them goodnight.
        $ mc.change_locked_clarity(5)
        "She leans towards you and gives you a quick kiss."
        the_person "Let's head home then."


    else:
        if renpy.random.randint(0,100) < the_person.sluttiness + the_person.love + (mc.charisma * 10): #She invites you home with her. TODO: This, and other date things, should depend on if she's in a relationship. Break it out into a function
            $ mc.change_locked_clarity(5)
            "She leans towards you and gives you a quick kiss."
            $ the_person.call_dialogue("date_seduction")
            menu:
                "Go to [the_person.title]'s place.":
                    mc.name "That sounds like a great idea. Let's get a cab."
                    if not the_person.has_role(aunt_role) and not the_person.has_role(cousin_role):
                        if not the_person.home in mc.known_home_locations:
                            $ mc.known_home_locations.append(the_person.home) #You know where she lives and can visit her.
                    "You flag a taxi and get in with [the_person.possessive_title]."
                    "After a short ride you pull up in front her house. She leads you to the front door and invites you inside."
                    $ the_person.add_situational_slut("Romanced",15,"What a wonderful date!")
                    call date_take_home_her_place(the_person, date_type = "movie") from _call_date_take_home_her_place
                    $ the_person.clear_situational_slut("Romanced")

                "Call it a night.":
                    mc.name "I'd like to call it an early night today, but maybe I'll take you up on the offer some other time."
                    "Her taxi arrives. You give her a goodbye kiss and head home yourself."
        else:
            "She leans towards you and gives you a quick kiss on the cheek before saying goodbye."

    $ clear_scene()
    $ mc.change_location(hall) #Put them back at home after the event, so if they were in the bathroom they aren't any more.
    $ mc.location.show_background()
    return "Advance Time"


label dinner_date_label(the_person):
    $ mc.business.event_triggers_dict["date_scheduled"] = False #Deflag this event so you can schedule a date with another person for next week.
    "You have a dinner date planned with [the_person.title]."
    menu:
        "Get ready for the date. {image=gui/heart/Time_Advance.png}" if mc.business.funds >= 50:
            pass

        "Get ready for the date.\nRequires: $30 (disabled)" if mc.business.funds < 50:
            pass

        "Cancel the date. (tooltip)She won't be happy with you canceling last minute.":
            "You get your phone out and text [the_person.title]."
            mc.name "I'm sorry, but something important came up at the last minute. We'll have to reschedule."
            $ the_person.change_love(-5)
            $ the_person.change_happiness(-5)
            the_person "I hope everything is okay. Maybe we can do this some other time then."
            return


    if mom_date_intercept_requirement(mom, the_person) and renpy.random.randint(0,100) < (25 + mom.love):
        call mom_date_intercept(mom, the_person) from _call_mom_date_intercept_1
        if _return:
            $ clear_scene()
            return "Advance Time"

    $ mc.change_location(downtown)
    $ downtown.show_background()

    "You get yourself looking as presentable as possible and head downtown."
    $ the_person.draw_person(emotion = "happy")
    "You meet up with [the_person.title] on time."
    the_person "So, where are we going tonight [the_person.mc_title]?"
    menu:
        "A cheap restaurant. -$50":
            $ mc.business.funds += -50
            the_person "It sounds cozy. Let's go, I'm starving!"

        "A moderately priced restaurant. -$100" if mc.business.funds >= 100:
            $ mc.business.funds += -100
            $ the_person.change_love(5)
            $ the_person.change_happiness(5)
            the_person "It sounds nice. Come on, I'm starving and could use a drink."

        "An expensive restaurant. -$300" if mc.business.funds >= 300:
            $ mc.business.funds += -300
            $ the_person.change_love(10)
            $ the_person.change_happiness(5)
            the_person "Oh, it sounds fancy! Well, I'm flattered [the_person.mc_title]."

        "A moderately priced restaurant. -$100 (disabled)" if mc.business.funds <= 100:
            pass

        "An expensive restaurant. -$300 (disabled)" if mc.business.funds < 300:
            pass

    $ the_person.draw_person(emotion = "happy", position = "sitting")
    if the_person.has_role(sister_role) or the_person.has_role(mother_role):
        if the_person.sluttiness >= 20:
            "You and [the_person.possessive_title] get to the restaurant and order your meals. She chats and flirts with you freely, as if forgetting you were related."
        else:
            "You and [the_person.possessive_title] get to the restaurant and order your meals."
            "She chats and laughs with you the whole night, but never seems to consider this more than a friendly family dinner."

    else:
        "You and [the_person.possessive_title] get to the restaurant and order your meals. You chat, flirt, and have a wonderful evening."

    if renpy.random.randint(0,100) < 40: #Chance to give her some serum.
        "After dinner you decide to order desert. [the_person.title] asks for a piece of cheese cake, then stands up from the table."
        the_person "I'm going to go find the little girls room. I'll be back in a moment."
        $ clear_scene()
        "She heads off, leaving you alone at the table with her half finished glass of wine."
        menu:
            "Add a dose of serum to her drink." if mc.inventory.get_any_serum_count()>0:
                call give_serum(the_person) from _call_give_serum_21
                if _return:
                    "You pour a dose of serum into her wine and give it a quick swirl, then sit back and relax."
                    "[the_person.possessive_title] returns just as your desert arrives."
                else:
                    "You sit back and relax, content to just enjoy the evening. [the_person.possessive_title] returns just as your desert arrives."

            "Add a dose of serum to her drink.\nRequires: Serum (disabled)" if mc.inventory.get_any_serum_count() == 0:
                pass

            "Leave her drink alone.":
                "You sit back and relax, content to just enjoy the evening. [the_person.possessive_title] returns just as your desert arrives."

        $ the_person.draw_person(position = "sitting")
        the_person "Ah, perfect timing!"
        "She sips her wine, then takes an eager bite of her cheesecake. She closes her eyes and moans dramatically."
        the_person "Mmm, so good!"
    $ the_person.change_love(mc.charisma)
    $ the_person.change_happiness(mc.charisma)
    if the_person.has_role(sister_role) or the_person.has_role(mother_role):
        "At the end of the night you pay the bill and leave with [the_person.title]. The two of you travel home together."
        if renpy.random.randint(0,100) < the_person.sluttiness + the_person.love + (mc.charisma * 10): #She invites you back to her place.
            $ the_person.call_dialogue("date_seduction")
            menu:
                "Go to [the_person.title]'s room.":
                    mc.name "I think I would. Lead the way."
                    $ mc.change_location(the_person.home)
                    $ mc.location.show_background()
                    "[the_person.possessive_title] leads you into her room and closes the door behind you."
                    #TODO: Mirror the real date stuff: ie she might get dressed up or start stripping down right away.
                    $ the_person.add_situational_slut("Romanced",25,"What a wonderful date!")
                    call fuck_person(the_person, private = True) from _call_fuck_person_16
                    $ the_report = _return
                    $ the_person.call_dialogue("sex_review", the_report = the_report)
                    $ the_person.clear_situational_slut("Romanced")
                    #TODO: add support for spending the night somewhere other than home.
                    "When you and [the_person.possessive_title] are finished you slip back to your own bedroom just down the hall."

                "Call it a night.":
                    mc.name "I think we should just call it a night now. I've got to get up early tomorrow."
                    "She lets go of your hand and looks away."
                    the_person "Right, of course. I wasn't saying we should... I was just... Goodnight [the_person.mc_title]."
                    "She hurries off to her room."
        else:
            the_person "I had a great night [the_person.mc_title]. We should get out of the house and spend time together more often."
            mc.name "I think so too. Goodnight [the_person.title]."

    else:
        "At the end of the night you pay the bill and leave with [the_person.title]. You wait with her while she calls for a taxi."
        if renpy.random.randint(0,100) < the_person.sluttiness + the_person.love + (mc.charisma * 10): #She invites you back to her place.
            $ the_person.call_dialogue("date_seduction") #She invites you back to her place to "spend some more time together". She's been seduced.
            menu:
                "Go to [the_person.title]'s place.":
                    mc.name "That sounds like a great idea."
                    if not the_person.has_role(aunt_role) and not the_person.has_role(cousin_role):
                        if not the_person.home in mc.known_home_locations:
                            $ mc.known_home_locations.append(the_person.home) #You know where she lives and can visit her.
                    "You join [the_person.possessive_title] when her taxi arrives."
                    "After a short ride you pull up in front her house. She leads you to the front door and invites you inside."
                    $ the_person.add_situational_slut("Romanced",25,"What a wonderful date!")
                    call date_take_home_her_place(the_person, date_type = "dinner") from _call_date_take_home_her_place_1
                    $ the_person.clear_situational_slut("Romanced")

                "Call it a night.":
                    mc.name "I'd like to call it an early night today, but maybe I'll take you up on the offer some other time."
                    "Her taxi arrives. You give her a goodbye kiss and head home yourself."

        else: #She says goodnight to you here.
            the_person "I had a great night [the_person.mc_title], you're a lot of fun to be around. We should do this again."
            mc.name "It would be my pleasure."
            "[the_person.title]'s taxi arrives and she gives you a kiss goodbye. You watch her drive away, then head home yourself."

    $ clear_scene()
    return "Advance Time"

#TODO: Add a "date_take_home_your_place" where you take her to your house.

#TODO: Add a "date_take_home_family", where you take her back to your house, because she's your Mom or sister.

label date_take_home_her_place(the_person, date_type = None): #Your date went well and you go back to her place. This event starts off when you enter the door.
    #date_type can be passed through to identify what type of date it was to trigger different dialogue
    $ mc.change_location(the_person.home)
    $ mc.location.show_background()
    $ relationship_slut_modifier = 0
    if the_person.relationship != "Single":
        $ relationship_slut_modifier = 10*the_person.get_opinion_score("cheating on men")

    if the_person.has_role(affair_role):
        call fuck_date_event(the_person) from _call_fuck_date_event_1 #You're having an affair, leads to all of the normal affair stuff like being caught.

    elif the_person.effective_sluttiness(["vaginal_sex", "sucking_cock"]) + relationship_slut_modifier >= 70:
        "You're barely in the door before [the_person.title] has her hands all over you."
        $ her_hallway = Room(the_person.name +"'s front hall", the_person.name +"'s front hall", [], standard_house_backgrounds[:],[],[],[],False,[3,3], visible = False, lighting_conditions = standard_indoor_lighting)
        $ her_hallway.add_object(Object("Front Door", ["Lean"], sluttiness_modifier = 10, obedience_modifier = 5))
        $ her_hallway.add_object(Object("Front Hall Carpet", ["Kneel", "Lay"], sluttiness_modifier = 5, obedience_modifier = 10))
        $ her_hallway.add_object(Object("Stairs", ["Sit", "Low"], sluttiness_modifier = 5, obedience_modifier = 10))
        $ mc.change_location(her_hallway)
        $ mc.location.show_background()
        the_person "Fuck, I can't wait any longer [the_person.mc_title]! I've been thinking about this all night long!"
        $ mc.change_locked_clarity(20)
        "She puts her arms around you and kisses your neck, grinding her body against you."
        mc.name "Don't you want to go to your bedroom first?"
        the_person "I can't wait! I want you right here, right now!"
        menu:
            "Fuck her in the front hall.":
                "You return the kiss. A moment later [the_person.possessive_title] has her hand down your pants, fondling your cock."
                the_person "It's already hard! Oh my god... Come on, how do you want me?"
                call fuck_person(the_person, private = True) from _call_fuck_person_103
                $ the_report = _return
                $ the_person.call_dialogue("sex_review", the_report = the_report)

            "Turn her down.":
                "You push her back firmly. She seems confused and tries to kiss you again, but you don't let her."
                mc.name "Slow down, this is going way too fast for me. You need to get yourself under control."
                the_person "What? But don't you want this too? Don't you want me?"
                mc.name "I was thinking about it, but you're acting like the only thing you care about is getting at my cock!"
                mc.name "Now I just want to head home. Maybe you can try this again some other night."
                $ the_person.change_happiness(-20)
                $ the_person.change_love(-(2 + the_person.get_opinion_score("being in control")))
                if the_person.get_opinion_score("being in control") > 0:
                    the_person "If you felt like that why did you come home with me at all?"
                    the_person "Wasn't it obvious what was going to happen? Did I have to write it out for you?"
                    "She scoffs and backs away from you."
                    the_person "Whatever, if that's how you feel then there's no reason for you to stay here."
                    mc.name "Right. Have a good night [the_person.title]."
                    "She sighs unhappily and watches you leave."
                else:
                    "[the_person.possessive_title] deflates like a balloon. She steps back."
                    the_person "I... I'm sorry [the_person.mc_title], I didn't know you felt like that."
                    "An awkward silence hangs for a few moments before you speak again."
                    mc.name "I'm going to get going. Have a good night."
                    "[the_person.title] watches you leave, then sulks back inside of her house."

    elif (the_person.effective_sluttiness(["underwear_nudity", "bare_tits", "bare_pussy"]) + (5 * the_person.get_opinion_score("not wearing anything")) + (5 * the_person.get_opinion_score("lingerie")) > 45) or the_person.has_role(girlfriend_role):
        the_person "Let me get you a drink and show you around."
        "She pours you a drink and leads you around her place. The tour ends in the living room."
        the_person "Have a seat and enjoy your drink, I'll be back in a moment."
        $ clear_scene()
        if the_person.get_opinion_score("not wearing anything") > the_person.get_opinion_score("lingerie"):
            $ the_person.apply_outfit(Outfit("Nude"), update_taboo = True) #She's wearing nothing at all. nothing at all. nothing at all...

        elif the_person.get_opinion_score("lingerie") >= 0:
            $ the_person.apply_outfit(lingerie_wardrobe.get_random_appropriate_outfit(the_person.sluttiness + 20, 0 + (the_person.sluttiness/2), guarantee_output = True), update_taboo = True) #She's just wearing lingerie for the evening.

        else: #She doesn't like being nude or wearing lingerie, so just strip her to her underwear
            $ the_person.outfit.strip_to_underwear()
        "You sit down on the couch and relax while you wait for [the_person.possessive_title]. A few minutes later she calls out for you."
        the_person "[the_person.mc_title], could you come here?"
        "You down the rest of your drink and leave the empty glass behind, following the sound of her voice."
        mc.name "On my way. Is everything okay?"
        the_person "Everything's fine, just get in here!"
        "Her voice is coming from the other side of a partially opened door. You nudge it open and step inside."
        $ the_person.draw_person(position = "sitting")
        $ mc.change_locked_clarity(15)
        "It's the master bedroom, and [the_person.possessive_title] is sitting at the foot of the bed."
        the_person "I thought we might be more comfortable in here. I got changed for you, too."
        $ the_person.draw_person()
        "She stands up and steps closer to you, leaning in for a kiss."
        menu:
            "Kiss her.":
                "You put your arm around her waist and pull her against your body. She kisses you passionately, and you return the gesture in full."
                call fuck_person(the_person, private = True, start_position = kissing) from _call_fuck_person_17
                $ the_report = _return
                $ the_person.call_dialogue("sex_review", the_report = the_report)
                "When you and [the_person.title] are finished you get dressed and say goodnight."

            "Turn her down.":
                mc.name "[the_person.title], we shouldn't do this..."
                the_person "What? You're not interested in me?"
                $ the_person.change_happiness(-20)
                $ the_person.change_love(-2)
                "She steps back, hurt by your rejection."
                mc.name "No, I am, it's just that tonight isn't the right night for this. I'm sorry."
                the_person "Oh, I... I'm sorry, I shouldn't have been so eager."
                "An awkward silence fills the room."
                mc.name "I should, um... I should probably get going."
                the_person "Right, that's a good idea... Maybe some other time we can do this again?"
                mc.name "Yeah, I think I'd like that."
                "You say goodnight and leave, heading back to your place."

    else:
        #Normal date-turned-fuck session.
        the_person "Let me get you a drink and show you around."
        "She pours you a drink and leads you around her place. The tour ends with the two of you sitting on the couch in the living room."
        $ the_person.draw_person(position = "sitting")
        the_person "Well, what would you like to do now?"
        $ mc.change_locked_clarity(10)
        "[the_person.possessive_title] leans closer to you and puts her hand on your thigh. It's obvious what she wants, but she's waiting for you to make the first move."
        menu:
            "Kiss her.":
                "You put your drink aside, then put one hand on the back of [the_person.possessive_title]'s neck and pull her into a kiss."
                if the_person.relationship == "Single" or the_person.get_opinion_score("cheating on men") > 0:
                    "She returns the kiss eagerly."
                else:
                    $ so_title = SO_relationship_to_title(the_person.relationship)
                    "She returns the kiss for a moment, then breaks away. Her lips hover, barely separated from yours."
                    the_person "I shouldn't... My [so_title]..."
                    "You kiss her again, and this time all resistance falls away."
                "After a long moment spent making out [the_person.title] pulls away."
                the_person "I think we'd be more comfortable in the bedroom, don't you think?"
                call fuck_person(the_person, private = True, start_position = kissing) from _call_fuck_person_104
                $ the_report = _return
                $ the_person.call_dialogue("sex_review", the_report = the_report)
                #TODO: add support for spending the night somewhere other than home.
                "When you and [the_person.title] are finished you get dressed and say goodnight."

            "Go home.":
                mc.name "It's been a fun evening, but I need to be going soon. I hope we can do this again some time though."
                $ the_person.change_happiness(-5)
                "[the_person.possessive_title] seems a little disappointed, but she smiles politely."
                if the_person.relationship == "Single" or the_person.get_opinion_score("cheating on men") > 0:
                    the_person "Of course. It's getting late, I should probably be going to bed as well."
                else:
                    $ so_title = SO_relationship_to_title(the_person.relationship)
                    the_person "Of course, that's fine. My [so_title] probably wouldn't like it that I have other men visiting anyways."

                the_person "I had a fun time, we should do this again."
                mc.name "I think I'd like that."
                "You finish your drink and say goodnight to [the_person.title]."

    return

label shopping_date_intro(the_person, skip_intro = False, skip_outro = False):
    if not skip_intro: #Skip the intro if another event (like Lily's LTE) already provides the context. Assumes you're talking to your girlfriend/paramour
        mc.name "Want to hang out for a while? I was going to head the mall and wander around for a while."
        if the_person.has_role(employee_role) and mc.business.is_open_for_business():
            the_person "Right now? I had some work to get done, but I could take a break if you want me to."
            menu:
                "Take some time off.":
                    #TODO: Make sure her production isn't added for the turn
                    mc.name "You've been doing a great job, you deserve some time off."
                    $ the_person.change_obedience(-2)
                    the_person "Alright, you're the boss. Some time at the mall sounds fun!"

                "Stay at work.":
                    mc.name "You're right, you've got more important things to do at the lab."
                    the_person "Come see me after work, I should be free then."
                    return
        else: #She's not your employee, or it's outside of work hours.
            the_person "A shopping trip sounds like fun, and I've always got time for you [the_person.mc_title]."
            the_person "Come on, let's go!"

        "You and [the_person.possessive_title] head to the mall together."


    $ mc.change_location(mall)
    $ mc.location.show_background()
    call shopping_date_loop(the_person)
    $ previous_choice = _return
    $ should_advance_time = True
    if previous_choice == "leave_early":
        $ should_advance_time = False
    else:
        call shopping_date_loop(the_person, previous_choice)

    if not skip_outro:
        "You walk with [the_person.possessive_title] to the mall entrance."
        the_person "This was fun [the_person.mc_title], maybe we can do it again some time."
        mc.name "Yeah, I hope so too."
        $ clear_scene()
        "She waves goodbye and you part ways outside of the mall."


    if should_advance_time:
        call advance_time()
    return

label shopping_date_loop(the_person, previous_choice = None):
    if previous_choice is not None:
        the_person "So, what do you want to do now?"
    else:
        the_person "What should we do first?"

    menu:
        "Get some food." if previous_choice != "Food":
            call shopping_date_food(the_person)
            return "Food"

        "Go clothes shopping." if previous_choice != "Overwear":
            call shopping_date_overwear(the_person)
            return "Overwear"

        "Go lingerie shopping." if previous_choice != "Underwear":
            call shopping_date_underwear(the_person)
            return "Underwear"
        #
        # "Look at electronics." if previous_choice != "Electronics": #TODO: Write these other options when we have time
        #     call shopping_date_electronics(the_person)
        #     return "Electronics"
        #
        # "Visit the sex store." if previous_choice != "Sex_Store":
        #     call shoppint_date_sex_store(the_person)
        #     return "Sex_Store"

        "Head home.":
            if previous_choice is None:
                mc.name "I just remembered, I have an important appointment today!"
                the_person "You do? But we just got here!"
                mc.name "I'm really sorry, I'll make it up to you some other time."
                $ the_person.change_love(-1)
                $ the_person.change_obedience(-2)
                "[the_person.possessive_title] seems disappointed, but nods her understanding."
            else:
                mc.name "That was fun [the_person.title], but I'm going to have to cut this trip a little short."
                mc.name "I've got some work to get back to."
                "She smiles and nods."
                the_person "Okay. Maybe we can do this again some time."
            return "leave_early"

    # TODO: Asks the player what they want to do at the mall, if they are in control. "previous_choice" cannot be picked."
    # TODO: Give the girl the chance to take control. Girls with Low obedience demand to do things, moderate obedience ask to do something specifically, and high obedience always give you complete control.
    # TODO: If she has control for one round it's less likely for her to have control for the next, and if you take control for the first she'll be more likely to take control and want to do something specifically.
    return

label shopping_date_food(the_person):
    mc.name "Let's head over to the food court, I could use a bite."
    the_person "Sounds like a plan."
    "You lead [the_person.possessive_title] to the crowded food court. She looks around and hums as she decides what to eat."
    #TODO: Have a list of random food places to arbirarily chose from
    menu:
        "Pay for her lunch. -$40" if mc.business.funds >= 40:
            mc.name "Lunch is on me, what do you want me to get you?"
            $ the_person.change_love(1)
            $ the_person.change_happiness(10)
            the_person "Aw, thanks [the_person.mc_title]..."
            "She thinks for a while, then points to a fast food place."
            the_person "Get me something that looks good from there."
            mc.name "Okay, you go find us a place to sit and I'll be over soon."
            "[the_person.title] nods and heads off into the crowd to find a free table."
            $ clear_scene()
            "You get in line and order food for yourself and [the_person.possessive_title]. It takes a few minutes until order number is called."
            $ mc.business.funds += -40
            "You collect your order and move over to the condiment station."
            menu:
                "Add serum to her drink." if mc.inventory.get_any_serum_count() > 0:
                    call give_serum(the_person)
                    if _return is None:
                        "You reconsider, and bring [the_person.title]'s food back to her without any additions."
                    else:
                        "You pour a dose of serum into [the_person.title]'s drink and swirl it in."


                "Leave her food alone.":
                    pass
            "You wander around the food court, until you spot [the_person.possessive_title]."
            $ the_person.draw_person(position = "sitting")
            "She waves you over to the table she's saved."
            the_person "Thank you [the_person.mc_title], this looks great!"
            $ the_person.change_love(1)
            "You eat lunch together, chatting idly about nothing important."

        "Pay for her lunch. -$40 (disabled)" if mc.business.funds < 40:
            pass

        "Just buy your own lunch. -$20" if mc.business.funds >= 20:
            mc.name "See anything you like?"
            the_person "Not right away... I'm going to wander around a bit, you go ahead and order something."
            $ clear_scene()
            "[the_person.possessive_title] moves off into the crowd. You pick a fast food place for yourself and order some food."
            $ mc.business.funds += -20
            "When you get your order you find a table, and a couple of minutes later [the_person.title] shows up with her own lunch."
            $ the_person.draw_person(position = "sitting", emotion = "happy")
            the_person "Hope you weren't waiting long, it just all looked so good!"
            $ the_person.change_love(1)
            "You eat lunch together, chatting idly about nothing important."

        "Just buy your own lunch. -$20 (disabled)" if mc.business.funds < 20:
            pass

        "Don't buy anything.":
            mc.name "Actually, I'm not as hungry as I thought I was."
            the_person "Oh, alright. Let's get shopping then!"

    return

label shopping_date_overwear(the_person, skip_intro = False):
    if not skip_intro:
        mc.name "Let's do some window shopping. If you see any cute outfits you could try them on."
        the_person "That sounds fun, and I think I know the first place we should check out. Follow me!"
        $ the_person.draw_person(position = "back_peek")
        "[the_person.title] takes your hand and leads you through the mall."
        #TODO: List of random store names (and maybe have each place have a specific set of clothing they can sell in the future)
    the_person "Here, doesn't it have the cutest stuff? Let's go look around!"
    "[the_person.possessive_title] brings you into one of the dozens of clothing stores in the mall."
    the_person "Oh, look at this! I should try this on... and this... Check if they have this one in my size!"
    $ the_person.change_happiness(10)
    menu:
        "Pick out an outfit for her." if the_person.obedience >= 110:
            call outfit_master_manager(show_outfits = False, show_underwear = False)
            if _return:
                $ new_overwear = _return
                "You move between the racks and pick out a few pieces for [the_person.title]."
                $ the_person.draw_person()
                the_person "What have you got there?"
                mc.name "Something for you. I think it'll look good on you."
                "She takes the clothes from you and smiles."
                the_person "Well let's go see!"
                "She leads you to the changing rooms at the back of the store."

            else:
                "You can't find anything you like for [the_person.title], but she comes to you with plenty of clothing for her to hold."
                $ the_person.draw_person()
                "When she feels like she had collected enough she leads you to the changing rooms at the back of the store."
                $ new_overwear = default_wardrobe.pick_random_overwear()

        "Pick out an outfit for her.\nRequires: 110 Obedience (disabled)" if the_person.obedience < 110:
            pass

        "Let her pick out an outfit.":
            "She moves between the racks of clothes, picking out her favourites and handing them over to you to hold."
            $ the_person.draw_person()
            "When she feels like she had collected enough she leads you to the changing rooms at the back of the store."
            $ new_overwear = default_wardrobe.pick_random_overwear()
    call shopping_date_changing_room(the_person, new_overwear, "overwear")
    if _return:
        "You and [the_person.possessive_title] move to the cashier at the front of the store."
        $ cost = (10 * len(new_overwear.generate_clothing_list())) + (5 * new_overwear.get_overwear_slut_score())
        menu:
            "Pay for the outfit. -$[cost]" if mc.business.funds >= cost:
                mc.name "Let me get this for you [the_person.title]."
                "She smiles at you as you pull out your wallet."
                $ the_person.change_obedience(1)
                $ the_person.change_love(2)
                $ mc.business.funds += -cost
                the_person "That's so sweet of you [the_person.mc_title]. Thank you!"

            "Pay for the outfit. -$[cost] (disabled)" if mc.business.funds < cost:
                pass

            "Let [the_person.title] pay.":
                "She waits for the outfit to be rung up by the cashier, then hands over a credit card and pays."

        $ the_person.wardrobe.add_overwear_set(new_overwear)
        "Purchase in hand, the two of you leave the store and head back into the mall."

    else:
        "[the_person.possessive_title] drops the outfit into a return bin nearby, and the two of you leave the store."

    $ the_person.change_love(1)
    "[the_person.title] seems to have enjoyed your shopping trip together."
    return

label shopping_date_underwear(the_person):
    mc.name "There was a store I saw that might have something you'd like. Let's do a little shopping."
    the_person "That sounds fun! Which store did you want to visit?"
    "You take her hand and lead her through the mall to a small lingerie store."
    mc.name "Here it is. You can buy yourself something pretty to wear."
    if the_person.effective_sluttiness("underwear_nudity") < 15:
        "[the_person.possessive_title] seems unsure for a moment, then shakes her head."
        the_person "I don't want to shop for that kind of... stuff with you [the_person.mc_title]!"
        the_person "Come on, let's just go look for some normal clothes. There's a place right over there."
        "It doesn't seem like you can change her mind, so you follow her to the opposite side of the hall into a normal clothing store."
        call shopping_date_overwear(the_person, skip_intro = True)
        return
    elif the_person.has_taboo("underwear_nudity") and the_person.is_family():
        "[the_person.possessive_title] seems unsure for a moment."
        the_person "Are you sure you want to go into a place like that with me?"
        the_person "Wouldn't it be embarrassing for you?"
        mc.name "Not at all. It's just clothing, right?"
        the_person "Yes.. Just clothing... Okay, let's go in."
        "[the_person.title] seems unconvinced, but she finds her courage and leads the way."
    else:
        the_person "That's a good idea, let's go!"
        "She leads the way and hurries in."

    menu:
        "Pick out some lingerie for her." if the_person.obedience >= 120:
            "You move between the racks of bras and display boxes of panties, picking out a cute little outfit for [the_person.possessive_title]."
            call outfit_master_manager(show_outfits = False, show_overwear = False, show_underwear = True)
            if _return:
                $ new_underwear = _return
                mc.name "Here you go [the_person.title]. You should try this on."
                "You hand the collection of underwear to [the_person.possessive_title]. She takes it and looks it over."
                if new_underwear.get_underwear_slut_score() > the_person.effective_sluttiness(): #TODO: Check to make sure it actually covers her
                    "She glances at it and scoffs."
                    the_person "I couldn't wear this, it's..."
                    mc.name "Just try it on. Maybe you'll like it more when you're wearing it."
                    "She sighs and shrugs."
                    the_person "Okay, I'll try it. No promises though..."
                else:
                    "She takes it and looks it over."
                    the_person "Hmm, this could be nice..."
                the_person "The changing rooms are at the back."

            else:
                if the_person.effective_sluttiness() > 50 or the_person.get_opinion_score("lingerie") > 0:
                    $ new_underwear = lingerie_wardrobe.get_random_appropriate_underwear(the_person.sluttiness, 6, guarantee_output = True)
                else:
                    $ new_underwear = default_wardrobe.get_random_appropriate_underwear(the_person.sluttiness, 0, guarantee_output = True)
                "[the_person.title] moves between the racks of bras and display boxes of panties, picking out a few choice pieces."
                the_person "I want to go try some of this on. The changing rooms are at the back."


        "Pick out some lingerie for her.\nRequires: 120 Obedience (disabled)" if the_person.obedience < 120:
            pass

        "Let her do her own shopping.":
            if the_person.effective_sluttiness() > 50 or the_person.get_opinion_score("lingerie") > 0:
                $ new_underwear = lingerie_wardrobe.get_random_appropriate_underwear(the_person.sluttiness, 6, guarantee_output = True)
            else:
                $ new_underwear = default_wardrobe.get_random_appropriate_underwear(the_person.sluttiness, 0, guarantee_output = True)
            "[the_person.title] moves between the racks of bras and display boxes of panties, picking out a few choice pieces."
            the_person "I want to go try some of this on. The changing rooms are at the back."


    call shopping_date_changing_room(the_person, new_underwear, "underwear")
    if _return:
        "You and [the_person.possessive_title] move to the cashier at the front of the store."
        $ cost = (5 * len(new_underwear.generate_clothing_list())) + (15 * new_underwear.get_overwear_slut_score())
        menu:
            "Pay for the lingerie. -$[cost]" if mc.business.funds >= cost:
                mc.name "Let me get this for you [the_person.title]."
                "She smiles at you as you pull out your wallet."
                $ the_person.change_obedience(1)
                $ the_person.change_love(2)
                $ mc.business.funds += -cost
                the_person "That's so sweet of you [the_person.mc_title]. Thank you!"

            "Pay for the lingerie. -$[cost] (disabled)" if mc.business.funds < cost:
                pass

            "Let [the_person.title] pay.":
                "She waits for the lingerie to be rung up by the cashier, then hands over a credit card and pays."

        "Lingerie in hand, [the_person.possessive_title] leads you out of the store and back into the busy mall."
        $ the_person.wardrobe.add_underwear_set(new_underwear)

    else:
        "[the_person.possessive_title] drops the underwear into a return bin nearby, and the two of you leave the store."

    $ the_person.change_happiness(10 + the_person.get_opinion_score("lingerie"))
    $ the_person.change_love(1)
    "[the_person.title] seems to have enjoyed shopping for lingerie with you."
    return

label shopping_date_changing_room(the_person, new_outfit, changing_type):
    $ waiting_outside = True
    $ wants_outfit = False
    if the_person.effective_sluttiness("underwear_nudity") > 40:
        "[the_person.possessive_title] steps into one of the changing rooms, then pauses and looks back at you."
        the_person "Come on in, I want your opinion. Quick, before someone else shows up."
        menu:
            "Join her in the changing room.":
                $ waiting_outside = False
                "You glance over your shoulder to make sure you're actually alone, then follow [the_person.title] into the changing room."
                "She pulls the curtain closed behind you."

            "Wait outside.":
                mc.name "I don't want us to get kicked out. I'm sure you'll manage without me."
                $ clear_scene()
                "[the_person.title] shrugs and pulls the curtain closed."
                the_person "Your loss!"
    else:
        the_person "Wait here, I'm going to try some of this on."
        $ clear_scene()
        "[the_person.possessive_title] slips into one of the changing rooms and pulls the curtain closed behind her."
        "You can see her feet move as she maneuvers around the small room."
        menu:
            "Step into the changing room.": #Effectively this is the peek, and sometimes you get thrown out.
                if the_person.effective_sluttiness() > 20: #Great for taboo breaking.
                    $ waiting_outside = False
                    $ the_person.outfit.strip_to_underwear()
                    $ the_person.draw_person(position = "back_peek", emotion = "angry")
                    if changing_type == "overwear":
                        if the_person.has_taboo("underwear_nudity"):
                            the_person "Occupied! [the_person.mc_title]?!"
                            "She turns her back to you, trying to shield her body from your view."
                            mc.name "I thought this would be a little faster way for me to give some advice."
                            mc.name "We should be quiet though, or someone else might hear us."
                            "[the_person.possessive_title] is still for a moment, then sighs, lowers her hands, and turns around to face you."
                            $ the_person.draw_person()
                            the_person "Well, I guess it's fine as long as I keep my underwear on."
                            the_person "Just... look away, okay? You shouldn't be seeing me undressed like this..."
                            $ the_person.update_outfit_taboos()
                        else:
                            the_person "Occupied! I.."
                            "[the_person.possessive_title] sighs and lowers her hands to her side."
                            $ the_person.draw_person()
                            the_person "Oh, it's just you."
                            mc.name "I thought this would be a little faster way for me to give some advice."
                            the_person "Okay, but you need to be quiet. Have a seat over there."
                            the_person "And try not to stare, okay? You shouldn't be seeing me undressed like this..."

                    else:
                        if the_person.has_taboo(["bare_tits", "bare_pussy"]):
                            the_person "Occupied! [the_person.mc_title]?!"
                            "She turns her back to you, trying to shield her body from your view."
                            the_person "I'm getting changed [the_person.mc_title], can you wait outside?"
                            mc.name "I can't give you my opinion if I'm out there. We need to be quiet though, or someone will catch us."
                            "[the_person.possessive_title] is still for a moment, then sighs, lowers her hands, and turns around to face you."
                            $ the_person.draw_person()
                            the_person "Okay, you can stay. Just... try and look away while I get changed."
                            $ the_person.update_outfit_taboos() #NOTE: We also do proper nudity breaks as she strips.

                        else:
                            the_person "Occupied! I.."
                            "[the_person.possessive_title] sighs and lowers her hands to her side."
                            $ the_person.draw_person()
                            the_person "Oh, it's just you."
                            mc.name "I thought you might want my opinion. We'll need to be quiet though, or someone will catch us."
                            "[the_person.title] nods and motions to a narrow knee high shelf."
                            the_person "Sit down, I'll be changed in a second. Just... try not to stare too much, okay?"
                            the_person "You really aren't suppose to be seeing me naked."

                else:
                    the_person "Occupied! [the_person.mc_title]?!"
                    "She turns her back to you, trying to shield her body from your view."
                    mc.name "I thought this would be a little..."
                    $ the_person.draw_person(emotion = "angry")
                    $ the_person.change_love(-2)
                    "[the_person.title] glares at you and grabs the changing room curtain."
                    the_person "You're going to get us kicked out of the store! Go wait until I'm finished!"
                    "She hurries you out of the changing room and yanks the curtain closed again."
                    $ clear_scene()


            "Wait for her to get changed.":
                pass

    if waiting_outside:
        "You find a seat and wait while [the_person.title] changes."
        if changing_type == "overwear":
            $ merged_outfit = new_outfit.get_copy() #By merging into the new outfit first it's shoes are taken with preference.
            $ merged_outfit.merge_outfit(the_person.outfit)
            $ the_person.apply_outfit(merged_outfit)
            "Soon enough the changing room curtain is pulled open and [the_person.possessive_title] steps out."
            $ the_person.draw_person()
            the_person "Thanks for waiting. Well, what do you think?"
            "She waits for a moment, then turns around to let you see her outfit from behind."
            $ mc.change_locked_clarity(5)
            $ the_person.draw_person(position = "back_peek")
            if new_outfit.get_overwear_slut_score() > the_person.sluttiness + 5*(the_person.get_opinion_score("skimpy outfits")):
                the_person "I think it may be too revealing..."
            else:
                pass

            menu:
                "Get it.":
                    mc.name "Buy it, it looks fantastic on you [the_person.title]."
                    $ wants_outfit = True


                "Leave it.":
                    mc.name "Leave it, it's not your style."

            "[the_person.possessive_title] thinks for a moment, then nods in agreement."
            the_person "You're right, as always."
            $ clear_scene()
            $ the_person.apply_outfit()
            the_person "I just need to change back, I'll be out in a moment!"
            "She steps back into the changing room and closes the curtain behind her."
            $ the_person.draw_person()
            "A short wait later and she steps back out, ready to leave the store."

        else:
            "After waiting for a little while [the_person.title] calls out from behind the curtain."
            if the_person.effective_sluttiness("underwear_nudity") < 20 or the_person.has_taboo("underwear_nudity"):
                if new_outfit.get_underwear_slut_score() < the_person.sluttiness + 5*the_person.get_opinion_score("lingerie"):
                    the_person "I think it's really cute [the_person.mc_title]!"
                    the_person "I'm going to buy it! I'll be out in a second!"
                    $ wants_outfit = True
                else:
                    the_person "Oh my... It doesn't leave much to the imagination!"
                    the_person "I don't think I'm going to be buying this. Wow, do women actually wear stuff like this?"
                    the_person "I'll be out in a second, thanks for waiting!"
                $ the_person.apply_outfit() #Gets changed back into her normal outfit before coming out.
                $ the_person.draw_person()
                "A little more waiting, then the curtain slides open again."

            elif the_person.effective_sluttiness() > 60 - 10*(the_person.get_opinion_score("skimpy outfits") + the_person.get_opinion_score("public sex")) and not new_outfit.tits_visible() and not new_outfit.vagina_visible():
                if new_outfit.get_underwear_slut_score() <= 5:
                    if the_person.has_role(sister_role):
                        the_person "This is disappointing. It looks like something our grandmother would wear!"
                    else:
                        the_person "This is disappointing. It looks like something my grandmother would wear!"
                    the_person "I might as well put on a chastity belt and call it a day!"
                    the_person "I'll be out in a moment, just need to get dressed again."
                    $ the_person.apply_outfit()
                    $ the_person.draw_person()
                    "Another short wait, then the changing room curtain slides open and [the_person.title] steps out."
                else:
                    $ the_person.apply_outfit(new_outfit)
                    the_person "Hmm, this is pretty cute. I think I need your opinion on it [the_person.mc_title]."
                    $ mc.change_locked_clarity(10)
                    $ the_person.draw_person()
                    "You're about to get up when [the_person.title] throws the changing room curtain open and strides out into the store."
                    the_person "What do you think? It's nice, right?"
                    $ the_person.draw_person(position = "back_peek")
                    $ mc.change_locked_clarity(10)
                    "She gives you a look from the front, then turns around to let you gawk at her ass."
                    $ the_employee = create_random_person() #TODO: Decide if we want to specify other things about this person.
                    $ the_employee.set_title("Store Employee")
                    $ the_employee.set_possessive_title("The Store Employee")
                    $ the_employee.set_mc_title("Sir")

                    mc.name "You look good in it [the_person.title], I..."
                    the_employee "Excuse me, Ma'am?"
                    $ the_group = GroupDisplayManager([the_person, the_employee], the_employee)
                    $ the_group.draw_person(the_employee)
                    "You're interrupted by a store employee, who hurries up to [the_person.possessive_title]."
                    the_employee "I'm sorry, but you need to stay inside of your changing room while you're trying outfits on."
                    $ the_group.draw_person(the_person)
                    the_person "I have everything covered, don't I? It's no worse than me wearing a bathing suit."
                    $ the_group.draw_person(the_employee)
                    the_employee "It's just store policy, now if you could just step back into the changing room..."
                    $ the_group.draw_person(the_person)
                    the_person "Okay, I understand. Just quickly... [the_person.mc_title], what do you think? Should I buy it?"
                    menu:
                        "Get it.":
                            mc.name "Buy it, it looks fantastic on you [the_person.title]."
                            $ wants_outfit = True

                        "Leave it.":
                            mc.name "Leave it, it's not your style."

                    the_person "There, I told you I would just need a moment."
                    "[the_person.possessive_title] smiles smugly at the store employee and steps back into the changing room."
                    "The employee sighs with relief and wanders back to the front of the store."
                    $ clear_scene()
                    $ the_group = None
                    $ the_employee = None #Clear them to avoid keeping memory locked up
                    $ the_person.apply_outfit()
                    "After another short wait [the_person.title] steps out, dressed appropriately once again."

            else:
                the_person "It's cute, but... I think I'm going to need your opinion on it [the_person.mc_title]."
                "The curtain to the changing room shifts, and [the_person.title] sticks her head out to check if anyone else is around."
                the_person "Come in. Quick, before anyone notices."
                "You hurry up from your seat and slide into the small changing room with [the_person.possessive_title]."
                $ the_person.apply_outfit(new_outfit)
                $ the_person.draw_person()
                the_person "What do you think? Does it look good on me?"
                "She poses for you briefly, then turns around so you can see it from behind."
                $ the_person.draw_person(position = "back_peek")
                call shopping_date_inside_changing_room(the_person, new_outfit, changing_type, skip_get_changed = True)
                $ wants_outfit = _return
    else:
        call shopping_date_inside_changing_room(the_person, new_outfit, changing_type)
        $ wants_outfit = _return

    return wants_outfit

label shopping_date_inside_changing_room(the_person, new_outfit, changing_type, skip_get_changed = False): #NOTE: skip_get_changed used when an event has already set her outfit properly.
    if not skip_get_changed:
        if changing_type == "overwear":
            $ strip_list = the_person.outfit.get_underwear_strip_list(visible_enough = False, strip_shoes = True)

        else: #Changing into underwear.
            $ strip_list = the_person.outfit.get_full_strip_list()
            if the_person.has_taboo(["bare_tits", "bare_pussy"]):
                the_person "I'm going to need to... get naked. You don't mind, do you?"
                "[the_person.possessive_title] thumbs nervously at her underwear."
                the_person "You could wait outside if you want..."
                mc.name "It's fine [the_person.title], I really don't mind. It's actually nice to watch you like this."
                if the_person.is_family():
                    the_person "You shouldn't be saying that about me [the_person.mc_title]. It's not right..."
                    "She takes a deep breath and nods."
                    the_person "Okay, here we go..."
                else:
                    the_person "You're cute, did you know that? Alright, here we go..."

        if len(strip_list) > 0:
            "[the_person.possessive_title] starts to strip down."
            $ generalised_strip_description(the_person, strip_list)
            $ the_person.update_outfit_taboos()
            $ mc.change_locked_clarity(15)

        the_person "Okay, let's see what this looks like..."
        $ her_opinion = "likes"
        if changing_type == "overwear":
            $ merged_outfit = new_outfit.get_copy() #By merging into the new outfit first it's shoes are taken with preference.
            $ merged_outfit.merge_outfit(the_person.outfit)
            $ the_person.apply_outfit(merged_outfit)
            "She picks up the outfit and slides it one piece at a time."
            if new_outfit.get_overwear_slut_score() > the_person.sluttiness + 5*(the_person.get_opinion_score("skimpy outfits")):
                $ her_opinion = "slutty"

        else:
            $ the_person.apply_outfit(new_outfit)
            "She picks up the underwear and slips it on."
            if new_outfit.get_underwear_slut_score() > the_person.sluttiness + 5*(the_person.get_opinion_score("lingerie")):
                $ her_opinion = "slutty"
            elif new_outfit.get_underwear_slut_score() <= 5:
                $ her_opinion = "conservative"

        $ the_person.draw_person()
        "She turns to you when it's on, posing for you to get a good view."
        if her_opinion == "likes":
            the_person "What do you think? I think it's a cute look. I could definitely imagine myself wearing this."
        elif her_opinion == "slutty":
            the_person "What do you think? Is it too much? I think it's too much."
        elif her_opinion == "conservative":
            the_person "What do you think? I don't think it suits me very well."
            the_person "It covers up a little too much."

    $ mc.change_locked_clarity(10)
    $ the_person.draw_person(position = "back_peek")
    "[the_person.possessive_title] turns around to give you a look at her ass."

    $ wants_outfit = False
    menu:
        "Get it.":
            mc.name "Buy it, it looks fantastic on you [the_person.title]."
            $ wants_outfit = True
            "She considers for a moment, then nods in agreement."
            the_person "You're right, of course! Alright, I'm getting it!"

        "Leave it.":
            mc.name "Leave it, it's not your style."
            "She considers it for a moment, then nods in agreement."
            the_person "You're right. It looked a lot cuter on the rack."
            the_person "Oh well..."


    $ wall = Object("Changing Room Wall", "Lean")
    $ floor = Object("Floor", ["Lay", "Kneel"])
    $ chair = Object("Changing Room Chair", ["Sit", "Low"])
    $ changing_room = Room("Changing Room", objects = [wall, floor, chair])
    $ old_location = mc.location
    $ mc.change_location(changing_room)
    $ sluttiness_token = get_red_heart(20)
    menu:
        "Grope her butt.":
            $ mc.change_locked_clarity(10)
            "You lean forward from your seat and plant a hand on [the_person.possessive_title]'s ass."
            if the_person.has_taboo("touching_body"):
                "She gasps and tries to take a step away from you, but there isn't enough room in the small changing room for her to escape."
                the_person "[the_person.mc_title]! What are you doing?"
                "She glances nervously at the curtain-door, worried her outburst had been too loud."
                $ mc.change_locked_clarity(10)
                if the_person.outfit.vagina_available() or (the_person.outfit.wearing_panties() and not the_person.outfit.panties_covered()):
                    "You continue to run your hand over her smooth butt as you respond."
                else:
                    "You continue to run your hand over her ass as you respond."
                mc.name "You were shoving it in my face, I thought this is what you wanted."
                the_person "I... Of course not!"
                mc.name "Quiet, [the_person.title], or someone's going to hear us. Imagine if they found us like this..."
                $ the_person.break_taboo("touching_body")
                "[the_person.possessive_title] shuffles uncomfortably, but seems more comfortable under your touch."
                "She plants her hands on the far side of the changing room and arches her back a little bit."

            else:
                "She gasps and shuffles away from you in surprise, but there isn't enough room in the small changing room to get away from your touch."
                the_person "[the_person.mc_title], stop it! You're going to get us in trouble!"
                "She glances nervously at the curtain-door, worried someone might have heard her yelp."
                $ mc.change_locked_clarity(10)
                if the_person.outfit.vagina_available() or (the_person.outfit.wearing_panties() and not the_person.outfit.panties_covered()):
                    "You continue to run your hand over her smooth butt as you respond."
                else:
                    "You continue to run your hand over her ass as you respond."
                mc.name "You were shoving this in my face, isn't this what you want?"
                the_person "Not here, obviously! I..."
                mc.name "Quiet, [the_person.title], or someone's going to hear us."
                "[the_person.title] sighs and relents, planting her hands hands on the far side of the changing room and arching her back a little."

            $ the_person.draw_person(position = "standing_doggy")
            if the_person.effective_sluttiness() + 10*the_person.get_opinion_score("public sex") >= 40:
                $ mc.change_locked_clarity(10)
                "She lets you caress her body from your seat, leaning herself against your hands happily."
                "You stand up and wrap your arms around her, kissing her neck sensually."
                the_person "As long as we're quiet..."
                call fuck_person(the_person, private = True, start_position = standing_grope, skip_intro = True)
                $ the_report = _return
                $ the_person.call_dialogue("sex_review", the_report = the_report)
            else:
                $ mc.change_locked_clarity(10)
                "She lets you caress her for a few moments, then stands up and starts to collect her clothing."
                $ the_person.draw_person()
                the_person "That was nice, but we can't be in here too long. You'll have to wait until later."



        "Pull out your cock." if the_person.effective_sluttiness() >= 30:
            "You slide your pants down and pull out your hard cock while [the_person.possessive_title] is checking herself out in the mirror."
            $ sex_valid = False
            if the_person.effective_sluttiness() + 10*the_person.get_opinion_score("public sex") > 60:
                "When she glances back she smiles and nods."
                the_person "Right here [the_person.mc_title]? It's a little risky..."
                $ mc.change_locked_clarity(15)
                "You grab onto your hard cock and and stroke it slowly while talking."
                mc.name "Watching you get dressed up for me got me excited. I need to take care of this before I go back out."
                if the_person.outfit.vagina_available() and not the_person.has_taboo("vaginal_sex"): # She bends over and asks if you want to fuck her
                    $ sex_valid = True
                    $ the_person.draw_person()
                    "[the_person.title] turns around and plants her back against the changing room wall."
                    $ mc.change_locked_clarity(20)
                    "She reaches betwen her legs and pets her pussy."
                    the_person "I think I have just what you need."
                elif the_person.outfit.can_half_off_to_vagina() and not the_person.has_taboo("vaginal_sex"):
                    $ sex_valid = True #She pulls her clothing to the side and asks if you want to fuck her
                    $ the_person.draw_person()
                    "[the_person.title] turns around and plants her back against the changing room wall."
                    $ strip_list = the_person.outfit.get_half_off_to_vagina_list()
                    $ generalised_strip_description (the_person, strip_list, half_off_instead = True)
                    $ mc.change_locked_clarity(20)
                    "[the_person.title] reaches between her legs and pets her pussy as you watch."
                    the_person "I think I have just what you need."
                else:
                    the_person "You do, huh? Well then, what can I do to help?"
            else:
                "When she glances back and sees she gasps quietly."
                the_person "[the_person.mc_title]! What are you doing?"
                mc.name "Watching you get dressed up for me got me hard, I can't go outside like this."
                $ mc.change_locked_clarity(10)
                "You grab onto your hard cock with one hand and stroke it slowly while talking."
                mc.name "I won't be long, I just need to take care of this."


            $ blowjob_slut_requirement = 40 - 5* (the_person.get_opinion_score("public sex") + the_person.get_opinion_score("giving blowjobs"))
            $ blowjob_slut_token = get_red_heart(blowjob_slut_requirement)

            $ sex_slut_requirement = 60 - 5* (the_person.get_opinion_score("public sex") + the_person.get_opinion_score("vaginal sex"))
            $ sex_slut_token = get_red_heart(sex_slut_requirement)

            menu:
                "Jerk yourself off.":
                    "You stroke your cock while looking at [the_person.title]."
                    "You know you might not have long before you are interrupted, so you focus on making yourself cum as quickly as possible."
                    if the_person.outfit.tits_available():
                        $ mc.change_locked_clarity(15)
                        "[the_person.title]'s tits give you something nice to focus on as you draw closer and closer to climax."
                    else:
                        $ mc.change_locked_clarity(5)
                        "[the_person.title]'s nice body gives you something to focus on as you draw closer and closer to climax."
                    the_person "[the_person.mc_title], are you almost done? We've been in here a really long time."
                    if the_person.outfit.can_half_off_to_tits():
                        the_person "Here..."
                        $ strip_list = the_person.outfit.get_half_off_to_tits_list()
                        $ generalised_strip_description(the_person, strip_list, half_off_instead = True)
                        "She jiggles her tits for you, giving you something to focus on."
                    $ climax_controller = ClimaxController(["Cum on the floor.","air"])
                    $ climax_controller.show_climax_menu()
                    "You push yourself past the point of no return and lean back, grunting softly as you cum."
                    $ climax_controller.do_clarity_release(the_person)
                    "You pulse your load in an arc onto the floor, getting some of it on [the_person.title]'s feet."
                    the_person "... Better?"
                    "You pant and nod, stuffing your cock back in your pants."
                    mc.name "Much bettter."

                "Ask for a handjob.":
                    "You stroke your cock in front of [the_person.possessive_title] for a little bit."
                    mc.name "This would go faster if you would take care of it... Just come over here and put your hand on it."
                    if the_person.has_taboo("touching_penis"):
                        $ the_person.call_dialogue("touching_penis_taboo_break")
                        $ the_person.break_taboo("touching_penis")
                    $ mc.change_locked_clarity(10)
                    "[the_person.title] wraps her hand around your shaft and starts to stroke it for you."
                    call fuck_person(the_person, private = True, start_position = handjob, skip_intro = True, girl_in_charge = True, position_locked = True)
                    $ the_report = _return
                    $ the_person.call_dialogue("sex_review", the_report = the_report)

                "Ask for a blowjob." if the_person.effective_sluttiness() >= blowjob_slut_requirement:
                    "You stroke your cock in front of [the_person.possessive_title] for a little bit."
                    mc.name "This would go faster if you would take care of it."
                    mc.name "Get on your knees and suck me off, before anyone notices what's going on in here."
                    if the_person.has_taboo("sucking_cock"):
                        $ the_person.call_dialogue("sucking_cock_taboo_break")
                        $ the_person.break_taboo("sucking_cock")
                    $ the_person.draw_person(position = "blowjob")
                    $ mc.change_locked_clarity(15)
                    "[the_person.title] kneels down in front of you. You let go of your shaft and let it flop onto her face."
                    the_person "Ah..."
                    "She leans back and brings the tip of your dick to her lips. After giving it a quick kiss she bobs forward, sliding you into her mouth."
                    "You have to stifle a moan as her slippery tongue begins to work it's magic up and down your shaft."
                    call fuck_person(the_person, private = True, start_position = blowjob, skip_intro = True, girl_in_charge = True, position_locked = True)
                    $ the_report = _return
                    $ the_person.call_dialogue("sex_review", the_report = the_report)

                "Ask for a blowjob.\nRequires: [blowjob_slut_token] (disabled)" if the_person.effective_sluttiness() < blowjob_slut_requirement:

                    pass

                "Fuck her." if sex_valid and the_person.effective_sluttiness >= sex_slut_requirement:
                    mc.name "Yeah, that's exactly what I need right now."
                    call condom_ask(the_person)
                    if _return:
                        call fuck_person(the_person, private = True, start_position = against_wall)
                        $ the_report = _return
                        $ the_person.call_dialogue("sex_review", the_report = the_report)
                    else:
                        call fuck_person(the_person, private = True) #ie. enter the normal sex system, so you can still get a blowjob or something.
                        $ the_report = _return
                        $ the_person.call_dialogue("sex_review", the_report = the_report)

                "Fuck her.\nRequires: [sex_slut_token] (disabled)" if the_person.effective_sluttiness() < sex_slut_requirement:
                    pass

        "Pull out your cock.\nRequires: [sluttiness_token] (disabled)" if the_person.effective_sluttiness() < 20:
            pass

        "Let her get dressed.":
            pass


    $ mc.change_location(old_location)
    $ the_person.apply_outfit()
    $ the_person.draw_person()
    "[the_person.title] changes back into her original outfit and slides the curtain to the changing room open."
    the_person "Come on, let's get going."
    return wants_outfit

#TODO: Write all of the date options, which should include.
# A) Get some food (chat + serum chance)
# B) Go overwear shopping. (Tries on some different overwear sets for you, gives you the option to buy it for her)
# C) Go underwear shopping. (Suggest some underwear sets to her. At moderate slut you can sneak in and view it on her.)
# |-> Both of these should include options to peek in on her as she changes (and maybe get caught), or have her invite you in.
# |-> At high Sluttiness you can try and fuck her in the changing booth.
# E) Go electronics shopping. (Chance to spend major cash for Love boost)
# F) Go sex toy shopping. (Chance to increase Sluttiness, but needs high Sluttiness to begin with).
# Z) Go home/Go home early.
