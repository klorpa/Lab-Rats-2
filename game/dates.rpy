# Contains all of the descriptions for different date results, and shared things such as a girl taking you home after a successful date.

#Note: This only contains generic dates, if a date is specific to a role (ie. the special fuck date available to paramours) it's in their role file.
#Note: These are only the dates themselves. How they are added (ie. what specific thing triggered them) is in whatever file is appropriate (usually chat_action.rpy, since you ask her out)

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
    #TODO: Add a bit of dialogue to their text history for this.
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
            if the_person.personality is wild_personality or the_person.personality.default_prefix == wild_personality.personality_type_prefix: #If it's a wild or wild derived personality type
                $ likes_movie = True
            mc.name "Yeah, I've wanted to see [the_choice] for a while. I'll go get us tickets."

        "Watch a comedic movie.":
            $ comedy_movie_list = ["Spooky Movie", "Aaron Powers", "Dumber and Dumberest-er", "Ghostblasters", "Shaun of the Undead"]
            $ the_choice = get_random_from_list(comedy_movie_list)
            $ movie_type = "comedy"
            if the_person.personality is relaxed_personality or the_person.personality.default_prefix == relaxed_personality.personality_type_prefix:
                $ likes_movie = True
            mc.name "I thought we'd both enjoy [the_choice]. I'll go get us tickets."

        "Watch a romantic movie.":
            $ romance_movie_list = ["Olympic", "Britannic","The Workbook", "East Side Tale", "Pottery Poltergeist"]
            $ the_choice = get_random_from_list(romance_movie_list)
            $ movie_type = "romantic"
            if the_person.personality is reserved_personality or the_person.personality.default_prefix == reserved_personality.personality_type_prefix:
                $ likes_movie = True
            mc.name "I thought [the_choice] would be a good fit for us. You just wait here, I'll go get us tickets."

        "Watch a foreign film.":
            $ foreign_movie_list = ["that one in French", "that one in Italian", "that one in Russian", "that one in Japanese", "that one in Mandarin", "that one that's silent"]
            $ the_choice = get_random_from_list(foreign_movie_list)
            $ movie_type = "foreign"
            if the_person.personality is introvert_personality or the_person.personality.default_prefix == introvert_personality.personality_type_prefix:
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
        "As the movie approaches it's climax she reaches her hand down and finds yours to hold."
        "When it's finished you leave the theater together, still holding hands."
        $ the_person.draw_person()
        mc.name "So, did you like the movie?"
        the_person "It was amazing! Let's watch something like that next time."
        $ the_person.change_love(10, max_modified_to = 80)

    else: #She's bored. Bad for love gain, but good for getting her to fool around. She may start to feel you up to disctract herself.
        "Halfway through the movie it's beocming clear that [the_person.title] isn't enthralled by it."
        if (the_person.sluttiness - the_person.get_opinion_score("public sex") * 5) > 50 and (the_person.relationship == "Single" or the_person.get_opinion_score("cheating on men") > 0) and not the_person.has_family_taboo():
            "While you're watching you feel her rest her hand on your thigh. She squeezes it gently and slides her hand up higher and higher while whispering into your ear."
            the_person "I'm bored. You don't mind if I make this a little more intresting, do you?"
            "You take a quick look around. The theater you're in is mostly empty, and nobody is in the same row as you."
            menu:
                "Go ahead.":
                    mc.name "I'm certainly not going to stop you."
                    "Her hand slides up to your waist and undoes the button to your pants. You get a jolt of pleasure as her fingers slide onto your hardening cock."
                    "[the_person.title] stays sitting in her seat, eyes fixed on the movie screen as she begins to fondle your dick."
                    "As you get hard she starts to stroke you off. Her hand is warm and soft, and the risk of being caught only enhances the experience."
                    "After a few minutes [the_person.possessive_title] brings her hand to her mouth, licks it, and then goes back go jerking you off with her slick hand."

                    if (the_person.sluttiness - the_person.get_opinion_score("public sex") * 5) > 65 and (the_person.relationship == "Single" or the_person.get_opinion_score("cheating on men") > 0) and not the_person.has_family_taboo():
                        "You're enjoying the feeling of her wet hand sliding up and down your cock when she stops. You're about to say something when she slides off of her movie seat and kneels down in the isle."
                        $ the_person.draw_person(position = "blowjob", special_modifier = "blowjob", lighting = [0.5, 0.5, 0.5])
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
                                "She purrs in your ear and slides back down to her knees again. Her warm mouth wraps itself around your shaft and she starts to blow you again."
                                "It doesn't take long for her to bring you to the edge of your orgasm."
                                "You clutch at the movie seat arm rests and supress a grunt as you climax, blowing your hot load into [the_person.title]'s mouth and down her throat."
                                $ the_person.cum_in_mouth()
                                "She waits until you're finished, then pulls off your cock, wipes her lips on the back of her hand, and sits down next to you."
                                $ the_person.change_slut_temp(3)
                                the_person "Thank you, that was fun."
                                "She takes your hand and holds it. You lean back, thoroughly spent, and zone out for the rest of the movie."

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
        "She leans towards you and gives you a quick kiss."
        the_person "Let's head home then."


    else:
        if renpy.random.randint(0,100) < the_person.sluttiness + the_person.love + (mc.charisma * 10): #She invites you home with her. TODO: This, and other date things, should depend on if she's in a relationship. Break it out into a function
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
    if sister_role in the_person.special_role or mother_role in the_person.special_role:
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
    if sister_role in the_person.special_role or mother_role in the_person.special_role:
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
                    if not aunt_role in the_person.special_role and not cousin_role in the_person.special_role:
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
    #TODO: See about combinding this with the fuck_date from the paramour. That's basically a "date" where you just show up and fuck her. At the very least this should trigger some of the same thigns if they're in a relationship.
    #date_type can be passed through to identify what type of date it was to trigger different dialogue
    $ mc.change_location(the_person.home)
    $ mc.location.show_background()

    if the_person.has_role(affair_role):
        call fuck_date_event(the_person) from _call_fuck_date_event_1 #You're having an affair, leads to all of the normal affair stuff like being caught. #TODO: Make sure the date seduction dialogue leads into this properly.

        #TODO: Refactor this huge conditional. It's hard to read
    elif (the_person.effective_sluttiness(["vaginal_sex", "sucking_cock"]) >= 70 and the_person.relationship == "Single") or (the_person.effective_sluttiness(["vaginal_sex", "sucking_cock"]) >= 70-(10*the_person.get_opinion_score("cheating on men")) and the_person.relationship != "Single"): #TODO: Figure out what triggers we want for this
        "You're barely in the door before [the_person.title] has her hands all over you."
        $ her_hallway = Room(the_person.name +"'s front hall", the_person.name +"'s front hall", [], standard_house_backgrounds[:],[],[],[],False,[3,3], visible = False, lighting_conditions = standard_indoor_lighting)
        $ her_hallway.add_object(Object("Front Door", ["Lean"], sluttiness_modifier = 10, obedience_modifier = 5))
        $ her_hallway.add_object(Object("Front Hall Carpet", ["Kneel", "Lay"], sluttiness_modifier = 5, obedience_modifier = 10))
        $ her_hallway.add_object(Object("Stairs", ["Sit", "Low"], sluttiness_modifier = 5, obedience_modifier = 10))
        $ mc.change_location(her_hallway)
        $ mc.location.show_background()
        the_person "Fuck, I can't wait any longer [the_person.mc_title]! I've been thinking about this all night long!"
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
        "It's a bedroom, and [the_person.possessive_title] is sitting at the foot of the bed."
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
