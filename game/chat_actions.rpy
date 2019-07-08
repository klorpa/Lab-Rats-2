init -2 python:
    def change_titles_requirement(the_person):
        if the_person.obedience < 110:
            return "Requires: 110 Obedience"
        else:
            return True

    def small_talk_requirement(the_person):
        if time_of_day >= 4:
            return "Too late to chat."
        else:
            return True

    def compliment_requirement(the_person):
        if time_of_day >= 4:
            return "Too late to chat."
        elif the_person.love < 10:
            return "Requires: 10 Love"
        else:
            return True

    def flirt_requirement(the_person):
        if time_of_day >= 4:
            return "Too late to chat."
        elif the_person.love < 10:
            return "Requires: 10 Love"
        else:
            return True

    def date_requirement(the_person):
        love_requirement = 20
        if the_person.relationship == "Girlfriend":
            love_requirement += 20
        elif the_person.relationship == "Fiancée":
            love_requirement += 30
        elif the_person.relationship == "Married":
            love_requirement += 40

        love_requirement += -10*the_person.get_opinion_score("cheating on men")
        if love_requirement < 20:
            love_requirement = 20

        if the_person.love < love_requirement:
            return "Requires: " + str(love_requirement) + " Love"
        elif mc.business.event_triggers_dict.get("date_scheduled", False):
            return "You already have a date planned!"
        else:
            return True

    def dinner_date_requirement(day_of_week): #Used for a mandatory crisis that triggers on the next Friday in time chunk 3.
        if time_of_day == 3 and day%7 == day_of_week: #Day of week is a nubmer from 0 to 6, where 0 is Monday.
            return True
        return False

label person_introduction(the_person):

    $ the_person.call_dialogue("introduction")

    #
    # mc.name "Excuse me, could I bother you for a moment?"
    # "She turns around and looks at you quizzically."
    # #TODO: Have this differ based on personality
    # $ the_person.set_title("???")
    # the_person.char "Sure, I guess. How can I help you?"
    # mc.name "I'm so sorry, I know this is silly but I just couldn't let you walk by without knowing your name."
    # "She laughs and rolls her eyes."
    #
    #
    #
    # $ title_choice = get_random_title(the_person)
    # $ formatted_title = the_person.create_formatted_title(title_choice)
    # the_person.char "Well then, I suppose I shouldn't disappoint you. You can call me [formatted_title]."
    # $ the_person.set_title(title_choice)
    # $ the_person.set_possessive_title(get_random_possessive_title(the_person))
    # "[the_person.possessive_title] holds her hand out to shake yours."
    # the_person.char "What about you, what's your name?"
    #

    #She's given us her name, now she asks for yours.
    $ title_tuple = []
    $ title_choice = None
    python:
        for title in get_player_titles(the_person):
            title_tuple.append([title,title])

    $ title_choice = renpy.display_menu(title_tuple,True,"Choice")
    mc.name "[title_choice], it's a pleasure to meet you."
    $ the_person.set_mc_title(title_choice)
    return

label change_titles_person(the_person):
    menu:
        "Change what you call her. (tooltip)Change the title you have for her. This may just be her name, an honourific such as \"Miss.\", or a complete nickname such as \"Cocksleeve\". Different combinations of stats, roles, and personalities unlock different titles.":
            call new_title_menu(the_person) from _call_new_title_menu
            $ title_choice = _return
            if not (title_choice == "Back" or the_person.title == the_person.create_formatted_title(title_choice)):
                "You tell [the_person.name] [the_person.last_name] that you are going to call her [title_choice] instead of [the_person.title]."
                $ the_person.set_title(title_choice)

        "Change what she calls you. (tooltip)Change the title she has for you. This may just be your name, an honourific such as \"Mr.\", or a complete nickname such as \"Master\". Different combinations of stats, roles, and personalities unlock different titles.":
            call new_mc_title_menu(the_person) from _call_new_mc_title_menu
            $ title_choice = _return
            if not (title_choice == "Back" or the_person.mc_title == title_choice):
                "You tell [the_person.title] to stop calling you [the_person.mc_title] and to refer to you as [title_choice] instead."
                $ the_person.set_mc_title(title_choice)

        "Change how you refer to her. (tooltip)Change your possessive title for this girl. A possessive title takes the form \"your employee\", \"your sister\", etc. It can also just be their name repeated. Different combinations of stats, roles, and personalities unlock different titles.":
            call new_possessive_title_menu(the_person) from _call_new_possessive_title_menu
            $ title_choice = _return
            if not (title_choice == "Back" or the_person.possessive_title ==  the_person.create_formatted_title(title_choice)):
                "You decide to start refering [the_person.name] [the_person.last_name] as [title_choice] instead of [the_person.possessive_title] when you're talking about her."
                $ the_person.set_possessive_title(title_choice)
    return

label new_title_menu(the_person):
    $ title_tuple = []
    $ title_choice = None
    python:
        for title in get_titles(the_person):
            title_tuple.append([title,title])
        
        tuple_list.append(["Do not change her title.","Back"])
        title_choice = renpy.display_menu(title_tuple,True,"Choice")
    return title_choice

label new_mc_title_menu(the_person):
    $ title_tuple = []
    $ title_choice = None
    python:
        for title in get_player_titles(the_person):
            title_tuple.append([title,title])
        
        tuple_list.append(["Do not change your title.","Back"])
        title_choice = renpy.display_menu(title_tuple,True,"Choice")
    return title_choice

label new_possessive_title_menu(the_person):
    $ title_tuple = []
    $ title_choice = None
    python:
        for title in get_possessive_titles(the_person):
            title_tuple.append([title,title])
        
        tuple_list.append(["Do not change your title.","Back"])
        title_choice = renpy.display_menu(title_tuple,True,"Choice")
    return title_choice

label person_new_title(the_person): #She wants a new title or to give you a new title.
    if __builtin__.len(get_titles(the_person)) <= 1: #There's only the one title available to them. Don't bother asking to change
        return
    $ randomised_obedience = the_person.obedience + renpy.random.randint(-30,30) #Randomize their effective obedience a little so they sometimes ask, sometimes demand

    if randomised_obedience > 120: #She just asks you for something "fresh". Her obedience is high enough that we already have control over this.
        the_person.char "[the_person.mc_title], do you think [the_person.title] is getting a little old? I think something new might be fun!"
        menu:
            "Change what you call her":
                #TODO: present the player with a list. TODO: Refactor the event above to be a generic way of presenting a list, w/ the dialogue separated.
                call new_title_menu(the_person) from _call_new_title_menu_1
                $ title_choice = _return
                if not (title_choice == "Back" or the_person.title == the_person.create_formatted_title(title_choice)):
                    mc.name "I think [title_choice] would really suit you."
                    $ the_person.set_title(title_choice)
                    "[the_person.title] seems happy with her new title."
                else:
                    mc.name "On second thought, I think [the_person.title] suits you just fine."
                    the_person.char "If you think so [the_person.mc_title]."

            "Don't change her title.":
                mc.name "I think [the_person.title] suits you just fine."
                the_person.char "If you think so [the_person.mc_title]."

    elif randomised_obedience > 95: #She picks a couple of choices and asks you to decide.

        $ title_one = get_random_from_list(get_titles(the_person))
        $ title_two = get_random_from_list(get_titles(the_person))
        python: #Quick hack to make sure they're always different.
            while title_one == title_two:
                title_two = get_random_from_list(get_titles(the_person))
        if the_person.title == the_person.create_formatted_title(title_one) or the_person.title == the_person.create_formatted_title(title_two):  #If we picked the one we're currently using we have a slightly different dialogue setup.
            if the_person.title == the_person.create_formatted_title(title_two):
                $ placeholder = title_two #Swap them around so title_one is always the current title she has
                $ title_two = title_one
                $ title_one = placeholder
            $ formatted_title_one = the_person.title
            $ formatted_title_two = the_person.create_formatted_title(title_two)
            the_person.char "Hey [the_person.mc_title], do you like calling me [formatted_title_one] or do you think [formatted_title_two] sounds better?"
            menu:
                "Keep calling her [formatted_title_one].":
                    mc.name "I think [the_person.title] suits you perfectly, you should keep using it."
                    "She nods in agreement."
                    the_person.char "Yeah, I think you're right."
                "Change her title to [formatted_title_two].":
                    mc.name "[formatted_title_two] does have a nice ring to it. You should start using that."
                    $ the_person.set_title(title_two)
                    the_person.char "I think you're right. Thanks for the input!"

        else: #Both are new!
            $ formatted_title_one = the_person.create_formatted_title(title_one)
            $ formatted_title_two = the_person.create_formatted_title(title_two)
            the_person.char "So [the_person.mc_title], I'm thinking of changing things up a bit. Do you think [formatted_title_one] or [formatted_title_two] sounds best?"
            menu:
                "Change her title to [formatted_title_one].":
                    mc.name "I think [formatted_title_one] is the best of the two."
                    $ the_person.set_title(title_one)
                    the_person.char "Yeah, I think you're right. I'm going to have people call me that from now on."

                "Change her title to [formatted_title_two].":
                    mc.name "I think [formatted_title_two] is the best of the two."
                    $ the_person.set_title(title_two)
                    the_person.char "Yeah, I think you're right. I'm going to have people call me that from now on."

                "Refuse to change her title.\n-5 Happiness.":
                    mc.name "I don't think either of those sound better than [the_person.title]. You should really just stick with that."
                    "[the_person.title] rolls her eyes."
                    $ the_person.change_happiness(-5)
                    the_person.char "Well that isn't very helpful [the_person.mc_title]. Fine, I guess [the_person.title] will do."

    else: #She doesn't listen to you, so she just picks one and demands that you use it, or becomes unhappy.
        $ new_title = get_random_from_list(get_titles(the_person))
        python:
            while the_person.create_formatted_title(new_title) == the_person.title:
                new_title = get_random_from_list(get_titles(the_person))

        $ formatted_new_title = the_person.create_formatted_title(new_title)
        the_person.char "By the way [the_person.mc_title], I want you to start refering to me as [formatted_new_title] from now on. I think it suits me better."
        menu:
            "Change her title to [formatted_new_title].":
                mc.name "I think you're right, [formatted_new_title] sounds good."
                $ the_person.set_title(new_title)

            "Refuse to change her title.\n-10 Happiness.":
                mc.name "I think that sounds silly, I'm just going to keep calling you [the_person.title]."
                "[the_person.title] scoffs and rolls her eyes."
                $ the_person.change_happiness(-10)
                the_person.char "Whatever. It's not like I can force you to do anything."
    return

label person_new_mc_title(the_person):
    if __builtin__.len(get_player_titles(the_person)) <= 1: #There's only the one title available to them. Don't bother asking to change
        return
    $ randomised_obedience = the_person.obedience + renpy.random.randint(-30, 30) #Randomize their effective obedience a little so they sometimes ask, sometimes demand
    if randomised_obedience > 120: #She just asks you for something "fresh". Her obedience is high enough that we already have control over this.
        the_person.char "I was just thinking that I've called you [the_person.mc_title] for a pretty long time. If you're getting tired of it I could call you something else."
        menu:
            "Change what she calls you.":
                #TODO: present the player with a list. TODO: Refactor the event above to be a generic way of presenting a list, w/ the dialogue separated.
                call new_mc_title_menu(the_person) from _call_new_mc_title_menu_1
                $ title_choice = _return
                if not (title_choice == "Back" or title_choice == the_person.mc_title):
                    mc.name "I think you should call me [title_choice] from now on."
                    $ the_person.set_mc_title(title_choice)
                    "[the_person.title] seems happy with your new title."
                else:
                    mc.name "On second thought, I think [the_person.mc_title] is fine for now."
                    the_person.char "If you think so [the_person.mc_title]."

            "Don't change her title for you.":
                mc.name "I think [the_person.mc_title] is fine for now."
                the_person.char "Okay, if you say so!"

    elif randomised_obedience > 95: #She picks a couple of choices and asks you to decide.
        $ title_one = get_random_from_list(get_player_titles(the_person))
        $ title_two = get_random_from_list(get_player_titles(the_person))
        python: #Quick hack to make sure they're always different.
            while title_one == title_two:
                title_two = get_random_from_list(get_player_titles(the_person))
        if the_person.mc_title == title_one or the_person.mc_title == title_two:  #If we picked the one we're currently using we have a slightly different dialogue setup.
            if the_person.mc_title == title_two:
                $ placeholder = title_two #Swap them around so title_one is always the current title she has
                $ title_two = title_one
                $ title_one = placeholder

            the_person.char "Hey [the_person.mc_title], would you rather I called you [title_two]?"
            menu:
                "Have her keep calling you [title_one].":
                    mc.name "I think I like [title_one], but thanks for asking."
                    "She shrugs."
                    the_person.char "Sure, whatever you like [the_person.mc_title]."
                "Have her call you [title_two] instead.":
                    mc.name "[title_two] does have a nice ring to it. You should start using that."
                    $ the_person.set_mc_title(title_two)
                    the_person.char "Alright, you got it [the_person.mc_title]!"

        else: #Both are new!
            the_person.char "You know, I really think [title_one] or [title_two] would fit you a lot better than [the_person.mc_title]. Which one do you think is better?"
            menu:
                "Have her call you [title_one].":
                    mc.name "I think [title_one] is the best of the two."
                    $ the_person.set_mc_title(title_one)
                    the_person.char "Yeah, you're right. I think I'll start calling you that from now on."

                "Have her call you [title_two].":
                    mc.name "I think [title_two] is the best of the two."
                    $ the_person.set_mc_title(title_two)
                    the_person.char "Yeah, you're right. I think I'll start calling you that from now on."

                "Refuse to change your title.\n-5 Happiness.":
                    mc.name "I don't think either of those sound better than [the_person.mc_title]. Let's stick with that for now."
                    "[the_person.title] rolls her eyes."
                    $ the_person.change_happiness(-5)
                    the_person.char "Fine, if you don't like chnage I can't make you."

    else: #She doesn't listen to you, so she just picks one and demands that you use it, or becomes unhappy.
        $ new_title = get_random_from_list(get_player_titles(the_person))
        python:
            while new_title == the_person.title:
                new_title = get_random_from_list(get_player_titles(the_person))

        the_person.char "You know, I think [new_title] fits you better than [the_person.mc_title]. I'm going to start using that."
        menu:
            "Let her call you [new_title].":
                mc.name "Alright, if you think that's better."
                $ the_person.set_mc_title(new_title)

            "Demand she keeps calling you [the_person.mc_title].\n-10 Happiness.":
                mc.name "I think that sounds silly, I want you to keep calling me [the_person.mc_title]."
                "[the_person.title] scoffs and rolls her eyes."
                $ the_person.change_happiness(-10)
                the_person.char "Whatever. If it's so important to you then I guess I'll just do it."

    return

label small_talk_person(the_person): #Tier 0. Useful for discovering a character's opinions and the first step to building up love.
    $ smalltalk_opinion = the_person.get_opinion_score("small talk")
    mc.name "So [the_person.title], what's been on your mind recently?"
    $ the_person.discover_opinion("small talk")
    $ successful_smalltalk = 60 + (smalltalk_opinion * 20) + (mc.charisma * 5)
    $ smalltalk_chance = renpy.random.randint(0,100)

    if smalltalk_chance < successful_smalltalk:
        if smalltalk_opinion >= 0:
            $ the_person.draw_person(emotion = "happy")
            "She seems glad to have a chance to take a break and make small talk with you."

        else:
            "She seems uncomfortable with making small talk, but after a little work you manage to get her talking."

        $ casual_sex_talk = the_person.sluttiness > 50
        $ opinion_learned = the_person.get_random_opinion(include_known = True, include_sexy = casual_sex_talk)

        if not opinion_learned is None:
            $ opinion_state = the_person.get_opinion_topic(opinion_learned)
            $ opinion_string = opinion_score_to_string(opinion_state[0])

            "The two of you chat pleasantly for half an hour before [the_person.possessive_title] has a question for you."
            the_person.char "So [the_person.mc_title], I'm curious what you think about about [opinion_learned]. Do you have any opinions on it?"
            $ love_gain = 4
            $ prediction = 0
            menu:
                "I hate [opinion_learned].":
                    $ prediction = -2
                    mc.name "I'll be honest, I absolutely hate [opinion_learned]. I just can't stand it."

                "I don't like [opinion_learned].":
                    $ prediction = -1
                    mc.name "I'm not a fan, that's for sure."

                "I don't have any opinion about [opinion_learned].":
                    $ prediction = 0
                    mc.name "I don't really have any thoughts on it, I guess I just don't think it's a big deal."

                "I like [opinion_learned].":
                    $ prediction = 1
                    mc.name "I really like [opinion_learned]."

                "I love [opinion_learned].":
                    $ prediction = 2
                    mc.name "Me? I love [opinion_learned]. Absolutely love it."

            $ prediction_difference = math.fabs(prediction - opinion_state[0])
            if prediction_difference == 4: #as wrong as possible
                the_person.char "Really? Wow, we really don't agree about [opinion_learned], that's for sure."
            elif prediction_difference == 3:
                the_person.char "You really think so? Huh, I guess we'll just have to agree to disagree."
            elif prediction_difference == 2:
                the_person.char "I guess I could understand that."
            elif prediction_difference == 1:
                the_person.char "Yeah, I'm glad you get it. I feel like we're both on the same wavelength."
            else: #prediction_difference == 0
                the_person.char "Exactly! It's so rare that someone feels exactly the same way about [opinion_learned] as me!"


            if opinion_state[1]:
                "You listen while [the_person.possessive_title] talks about how she [opinion_string] [opinion_learned]."
            else:
                $ the_person.discover_opinion(opinion_learned)
                "You listen while [the_person.possessive_title] talks and discover that she [opinion_string] [opinion_learned]."

            $ the_person.change_love(love_gain - prediction_difference)

        else:
            "You and [the_person.possessive_title] chat for a while. You don't feel like you've learned much about her, but you both enjoyed talking."

        $ smalltalk_bonus = smalltalk_opinion + 1
        $ the_person.change_happiness(smalltalk_bonus)
        if smalltalk_opinion >= 0:
            the_person.char "It was nice chatting [the_person.mc_title], we should do it more often!"
        else:
            the_person.char "So uh... I guess that's all I have to say about that..."
            "[the_person.char] trails off awkwardly."
    else:
        if smalltalk_opinion < 0:
            the_person.char "Oh, not much."
            $ the_person.change_happiness(smalltalk_opinion)
            "You try and keep the conversation going, but making small talk with [the_person.title] is like talking to a wall."
        else:
            the_person.char "Oh, not much honestly. How about you?"
            $ the_person.change_happiness(smalltalk_opinion)
            "[the_person.possessive_title] seems happy to chitchat, and you spend a couple of hours just hanging out. You don't feel like you've learned much about her, but least she seems to have enjoyed talking."

    $ the_person.apply_serum_study()
    return

label compliment_person(the_person): #Tier 1. Raises the character's love. #TODO: just have it raise love and not sluttiness.
    mc.name "Hey [the_person.title]. How are you doing today? You're looking good, that's for sure."
    the_person.char "Aww, thank you. You're too kind. I'm doing well."
    "You chat with [the_person.possessive_title] for a while and slip in a compliment when you can. She seems flattered by all the attention."
    $ the_person.change_love(5)
    $ the_person.change_happiness(2)
    the_person.char "It's been fun talking [the_person.mc_title], we should do this again some time!"
    $ the_person.apply_serum_study()
    return


#    mc.name "Hey [the_person.name], I just wanted to say that you look great today. That style really suits you." #TODO: Add more context aware dialogue.
#    $ slut_difference = int(the_person.sluttiness - the_person.outfit.slut_requirement) #Negative if their outfit is sluttier than what they would normally wear.
#    # Note: The largest effect should occure when the outfit is just barely in line with her sluttiness. Too high or too low and it will have no effect.

#    $ sweet_spot_range = 10
#    if slut_difference < -sweet_spot_range : #Outfit is too slutty, she will never get use to wearing it.
#        the_person.char "Really? It's just so revealing, what do people think of me when they see me? I don't think I'll ever get use to wearing this."
#        $ the_person.draw_person(emotion = "default")

#    elif slut_difference > sweet_spot_range:  #Outfit is conservative, no increase.
#        $ the_person.draw_person(emotion = "default")
#        the_person.char "Really? I think it looks too bland, showing a little more skin would be nice."

#    else: #We are within the sweet_spot_range with the outfit.
#        $ slut_difference = math.fabs(slut_difference)
#        if slut_difference > sweet_spot_range:
#            $ slut_difference = sweet_spot_range
#        $ slut_difference = sweet_spot_range - slut_difference #invert the value so we now have 10 - 10 at both extreme ends, 10 - 0 at the middle where it will have the most effect.
#        $ change_amount = int((mc.charisma + 1 + slut_difference)/2)
#        if change_amount + the_person.sluttiness > 40:
#            $ change_amount = 40 - the_person.sluttiness
#        $ slut_report = the_person.change_slut_temp(change_amount)
#        the_person.char "Glad you think so, I was on the fence, but it's nice to know that somebody likes it!"
#    return

label flirt_person(the_person): #Tier 1. Raises a character's sluttiness up to a low cap while also raising their love by less than a compliment.
    #TODO: change this to be more appropriate for a love changing action (and maybe move the current stuff somewhere else?)
    #TODO: Vary the flirting intro and response based on sluttiness.
    mc.name "Hey [the_person.title], you're looking particularly good today. I wish I got to see a little bit more of that fabulous body."
    $ mc.listener_system.fire_event("player_flirt", the_person = the_person)
    $ change_amount = mc.charisma + 1 + the_person.get_opinion_score("flirting") #We still cap out at 20, but we get there a little faster or slower depending on if they like flirting
    if change_amount + the_person.sluttiness > 20:
        $ change_amount = 20 - the_person.sluttiness
        if change_amount < 0:
            $ change_amount = 0

    $ the_person.change_happiness(the_person.get_opinion_score("flirting"))
    $ the_person.change_slut_temp(change_amount)
    $ the_person.change_love(3)
    $ the_person.discover_opinion("flirting")
    $ the_person.call_dialogue("flirt_response")
    $ the_person.apply_serum_study()
    return

label lunch_person(the_person): #You take them out to lunch. A sort of mini-date where you get to know them.
    # How do we want this to play out?
    # Should this just be a simple kind of "gathering information" scene?
    # Oportunity to slip serum into their food/drink (remove ability to do it normally?)?
    # Becomes available around 20 or so Love. It's the early "seduce" of raising Love.
    # Ability to impress based on multiple things? Maybe just a money sink to give the rest of the economy more meaning.

    return

label date_person(the_person): #You invite them out on a proper date
    #TODO: have different date options

    if sister_role in the_person.special_role:
        mc.name "[the_person.title], I was wondering if you'd like to go out and get dinner together. Some brother sister bonding time."
        the_person.char "That sounds great [the_person.mc_title]. Would Friday be good?"

    elif mother_role in the_person.special_role:
        mc.name "Mom, I was wondering if I could take you out to dinner, just the two of us. I'd enjoy some mother son bonding time."
        the_person.char "Aww, that's so sweet. How about Friday, after we're both finished with work."

    elif not the_person.relationship == "Single":
        mc.name "[the_person.title], I'd love to spend some time together, just the two of us. Would you let me take you out for dinner?"
        $ SO_title = SO_relationship_to_title(the_person.relationship)
        the_person.char "[the_person.mc_title], you know I've got a [SO_title], right? Well..."
        if the_person.get_opinion_score("cheating on men") > 0:
            "She doesn't take very long to make up her mind."
            the_person.char "He won't know about it, right? What he doesn't know can't hurt him. Are you free Friday?"
        else:
            "She thinks about it for a long moment."
            the_person.char "Just this once, and we have to make sure my [SO_title] never finds out. Are you free Friday?"



    else:
        mc.name "[the_person.title], I'd love to get to know you better. Would you let me take you out for dinner?"
        the_person.char "That sounds delightful [the_person.mc_title]. I'm free Friday night, if you would be available."
    menu:
        "Plan a date for Friday night.":
            mc.name "It's a date. I'm already looking forward to it."
            the_person.char "Me too!"
            $ dinner_action = Action("Dinner date", dinner_date_requirement, "dinner_date", args=the_person, requirement_args=4) #it happens on a friday, so day%7 == 4
            $ mc.business.mandatory_crises_list.append(dinner_action)
            $ mc.business.event_triggers_dict["date_scheduled"] = True

        "Maybe some other time.":
            mc.name "I'm busy on Friday unfortunately."
            the_person.char "Well maybe next week then. Let me know, okay?"
            "She gives you a warm smile."


    # Different date activities that different girls will like differently (based on opinions?)
    # Fancy dinner
    # Movie date
    # Go shopping together
    # After, depending on how the date went, she may invite you back to her place (discover where she lives).
    # Automatic seduce w/ bonus because you romanced her first.
    return

label dinner_date(the_person):
    $ mc.business.event_triggers_dict["date_scheduled"] = False #Deflag this event so you can schedule a date with another person for next week.
    "You have a dinner date planned with [the_person.title]."
    menu:
        "Get ready for the date." if mc.business.funds >= 30:
            pass

        "Get ready for the date.\nRequires: $30 (disabled)" if mc.business.funds < 30:
            pass

        "Cancel the date. (tooltip)She won't be happy with you canceling last minute.":
            "You get your phone out and text [the_person.title]."
            mc.name "I'm sorry, but something important came up at the last minute. We'll have to reschedule."
            $ the_person.change_love(-5)
            $ the_person.change_happiness(-5)
            the_person.char "I hope everything is okay. Maybe we can do this some other time then."
            return

    $ mc.change_location(downtown)
    $ renpy.show(downtown.name,what=downtown.background_image)
    "You get yourself looking as presentable as possible and head downtown."
    $ the_person.draw_person(emotion = "happy")
    "You meet up with [the_person.title] on time."
    the_person.char "So, where are we going tonight [the_person.mc_title]?"
    menu:
        "A cheap restaurant. -$40":
            $ mc.business.funds += -40
            the_person.char "It sounds cozy. Let's go, I'm starving!"

        "A moderately priced restaurant. -$80" if mc.business.funds >= 80:
            $ mc.business.funds += -80
            $ the_person.change_love(5)
            $ the_person.change_happiness(5)
            the_person.char "It sounds nice. Come on, I'm starving and could use a drink."

        "An expensive restaurant. -$200" if mc.business.funds >= 200:
            $ mc.business.funds += -200
            $ the_person.change_love(10)
            $ the_person.change_happiness(5)
            the_person.char "Oh, it sounds fancy! Well, I'm flattered [the_person.mc_title]."

        "A moderately priced restaurant. -$80 (disabled)" if mc.business.funds <= 80:
            pass

        "An expensive restaurant. -$200 (disabled)" if mc.business.funds < 200:
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
                    $ renpy.show(mc.location.name,what=mc.location.background_image)
                    "[the_person.possessive_title] leads you into her room and closes the door behind you."
                    $ the_person.add_situational_slut("Romanced",25,"What a wonderful date!")
                    call fuck_person(the_person, private = True) from _call_fuck_person_16
                    $ the_person.reset_arousal()
                    $ the_person.clear_situational_slut("Romanced")

                    #TODO: add support for spending the night somewhere other than home.
                    "When you and [the_person.possessive_title] are finished you slip back to your own bedroom just down the hall."

                "Call it a night.":
                    mc.name "I think we should just call it a night now. I've got to get up early tomorrow."
                    "She lets go of your hand and looks away."
                    the_person.char "Right, of course. I wasn't saying we should... I was just... Goodnight [the_person.mc_title]."
                    "She hurries off to her room."
        else:
            the_person.char "I had a great night [the_person.mc_title]. We should get out of the house and spend time together more often."
            mc.name "I think so too. Goodnight [the_person.title]."

    else:
        "At the end of the night you pay the bill and leave with [the_person.title]. You wait with her while she calls for a taxi."
        if renpy.random.randint(0,100) < the_person.sluttiness + the_person.love + (mc.charisma * 10): #She invites you back to her place.
            $ the_person.call_dialogue("date_seduction") #She invites you back to her place to "spend some more time together". She's been seduced.
            menu:
                "Go to [the_person.title]'s place.":
                    mc.name "That sounds like a great idea."
                    $ mc.change_location(the_person.home)
                    $ renpy.show(mc.location.name,what=mc.location.background_image)
                    if not the_person.home in mc.known_home_locations:
                        $ mc.known_home_locations.append(the_person.home) #You know where she lives and can visit her.
                    "You join [the_person.possessive_title] when her taxi arrives. It's not a far ride to her house, and she invites you in."
                    "She pours you a drink and gives you a tour. When the tour ends in her bedroom you aren't surprised."

                    $ the_person.add_situational_slut("Romanced",25,"What a wonderful date!")
                    call fuck_person(the_person, private = True) from _call_fuck_person_17
                    $ the_person.reset_arousal()
                    $ the_person.clear_situational_slut("Romanced")

                    #TODO: add support for spending the night somewhere other than home.
                    "When you and [the_person.title] are finished you get dressed and say goodnight."

                "Call it a night.":
                    mc.name "I'd like to call it an early night today, but maybe I'll take you up on the offer some other time."
                    "Her taxi arrives. You give her a goodbye kiss and head home yourself."

        else: #She says goodnight to you here.
            the_person.char "I had a great night [the_person.mc_title], you're a lot of fun to be around. We should do this again."
            mc.name "It would be my pleasure."
            "[the_person.title]'s taxi arrives and she gives you a kiss goodbye. You watch her drive away, then head home yourself."

    $ renpy.scene("Active")

    return
