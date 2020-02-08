init -2 python:
    def change_titles_requirement(the_person):
        if the_person.obedience < 110:
            return "Requires: 110 Obedience"
        else:
            return True

    def small_talk_requirement(the_person):
        if mc.energy < 15:
            return "Requires: 15 Energy"
        else:
            return True

    def compliment_requirement(the_person):
        if the_person.love < 10:
            return "Requires: 10 Love"
        elif mc.energy < 15:
            return "Requires: 15 Energy"
        else:
            return True

    def flirt_requirement(the_person):
        if the_person.love < 10:
            return "Requires: 10 Love"
        elif mc.energy < 15:
            return "Requires: 15 Energy"
        else:
            return True

    def date_option_requirement(the_person): #TODO Decide if there's any reason this option shouldn't always be enabled.
        return True

    def lunch_date_requirement(the_person):
        love_requirement = 20

        if time_of_day < 2:
            return "Too early to go for lunch."
        elif time_of_day > 2:
            return "Too late to go for lunch."
        elif the_person.love < love_requirement:
            return "Requires: " + str(love_requirement) + " Love"
        else:
            return True

    def movie_date_requirement(the_person):
        love_requirement = 30
        if the_person.relationship == "Girlfriend":
            love_requirement += 10
        elif the_person.relationship == "Fiancée":
            love_requirement += 15
        elif the_person.relationship == "Married":
            love_requirement += 20
        love_requirement += -10*the_person.get_opinion_score("cheating on men")
        if love_requirement < 30:
            love_requirement = 30

        if the_person.love < love_requirement:
            return "Requires: " + str(love_requirement) + " Love"
        elif mc.business.event_triggers_dict.get("date_scheduled", False):
            return "You already have a date planned!"
        else:
            return True


    def dinner_date_requirement(the_person):
        love_requirement = 40
        if the_person.relationship == "Girlfriend":
            love_requirement += 20
        elif the_person.relationship == "Fiancée":
            love_requirement += 30
        elif the_person.relationship == "Married":
            love_requirement += 40
        love_requirement += -10*the_person.get_opinion_score("cheating on men")
        if love_requirement < 40:
            love_requirement = 40

        if the_person.love < love_requirement:
            return "Requires: " + str(love_requirement) + " Love"
        elif mc.business.event_triggers_dict.get("date_scheduled", False):
            return "You already have a date planned!"
        else:
            return True


    def evening_date_trigger(day_of_week): #Used for a mandatory crisis that triggers on the next Friday in time chunk 3.
        if time_of_day == 3 and day%7 == day_of_week: #Day of week is a nubmer from 0 to 6, where 0 is Monday.
            return True
        return False

    def wardrobe_change_requirment(the_person):
        if the_person.obedience < 120:
            return "Requires: Obedience 120"
        else:
            return True

    def serum_give_requirement(the_person):
        #the_person parameter passed to match other actions and for future proofing.
        if mc.inventory.get_any_serum_count() <= 0:
            return "Requires: Serum in inventory"
        else:
            return True

    def seduce_requirement(the_person):
        if the_person.sluttiness < 15:
            return "Requires: {image=gui/heart/three_quarter_red_quarter_empty_heart.png}"
        else:
            return True


label person_introduction(the_person, girl_introduction = True):
    if girl_introduction:
        $ the_person.call_dialogue("introduction")

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
            if not (title_choice == "Back" or the_person.possessive_title ==  the_person.create_formatted_title(the_person.possessive_title)):
                "You decide to start refering [the_person.name] [the_person.last_name] as [title_choice] instead of [the_person.possessive_title] when you're talking about her."
                $ the_person.set_possessive_title(title_choice)
    return

label new_title_menu(the_person):
    $ title_tuple = []
    $ title_choice = None
    python:
        for title in get_titles(the_person):
            title_tuple.append([title,title])
        title_tuple.append(["Do not change her title.","Back"])
        title_choice = renpy.display_menu(title_tuple,True,"Choice")
    return title_choice

label new_mc_title_menu(the_person):
    $ title_tuple = []
    $ title_choice = None
    python:
        for title in get_player_titles(the_person):
            title_tuple.append([title,title])
        title_tuple.append(["Do not change your title.","Back"])
        title_choice = renpy.display_menu(title_tuple,True,"Choice")
    return title_choice

label new_possessive_title_menu(the_person):
    $ title_tuple = []
    $ title_choice = None
    python:
        for title in get_possessive_titles(the_person):
            title_tuple.append([title,title])
        title_tuple.append(["Do not change your title.","Back"])
        title_choice = renpy.display_menu(title_tuple,True,"Choice")
    return title_choice

label person_new_title(the_person): #She wants a new title or to give you a new title.
    if __builtin__.len(get_titles(the_person)) <= 1: #There's only the one title available to them. Don't bother asking to change
        return
    $ randomised_obedience = the_person.obedience + renpy.random.randint(0,30) - 15 #Randomize their effective obedience a little so they sometimes ask, sometimes demand

    if randomised_obedience > 120: #She just asks you for something "fresh". Her obedience is high enough that we already have control over this.
        the_person.char "[the_person.mc_title], do you think [the_person.title] is getting a little old? I think something new might be fun!"
        menu:
            "Change what you call her":
                #TODO: present the player with a list. TODO: Refactor the event above to be a generic way of presenting a list, w/ the dialogue separated.
                call new_title_menu(the_person) from _call_new_title_menu_1
                $ title_choice = _return
                if not (title_choice == "Back" or title_choice == title_choice):
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
                    $ the_person.set_title(title_one)
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
    $ randomised_obedience = the_person.obedience + renpy.random.randint(0,30) - 15 #Randomize their effective obedience a little so they sometimes ask, sometimes demand
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
                    $ the_person.set_mc_title(title_one)
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
    $ mc.change_energy(-15)
    $ smalltalk_opinion = the_person.get_opinion_score("small talk")
    mc.name "So [the_person.title], what's been on your mind recently?"
    $ the_person.discover_opinion("small talk")
    $ successful_smalltalk = 60 + (smalltalk_opinion * 20) + (mc.charisma * 5)
    $ smalltalk_chance = renpy.random.randint(0,100)
    # TODO: Add a chance that she wants to talk about someone she knows.
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

            "The two of you chat pleasantly for half an hour."
            the_person.char "So [the_person.mc_title], I'm curious what you think about about [opinion_learned]. Do you have any opinions on it?"
            $ love_gain = 4
            $ prediction = 0
            menu:
                "I love [opinion_learned].":
                    $ prediction = 2
                    mc.name "Me? I love [opinion_learned]. Absolutely love it."

                "I like [opinion_learned].":
                    $ prediction = 1
                    mc.name "I really like [opinion_learned]."

                "I don't have any opinion about [opinion_learned].":
                    $ prediction = 0
                    mc.name "I don't really have any thoughts on it, I guess I just don't think it's a big deal."

                "I don't like [opinion_learned].":
                    $ prediction = -1
                    mc.name "I'm not a fan, that's for sure."

                "I hate [opinion_learned].":
                    $ prediction = -2
                    mc.name "I'll be honest, I absolutely hate [opinion_learned]. I just can't stand it."

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
            "[the_person.possessive_title] seems happy to chitchat, and you spend a couple of hours just hanging out."
            "You don't feel like you've learned much about her, but least she seems to have enjoyed talking."

    $ the_person.apply_serum_study()
    return

label compliment_person(the_person): #Tier 1. Raises the character's love. #TODO: just have it raise love and not sluttiness.
    $ mc.change_energy(-15)
    mc.name "Hey [the_person.title]. How are you doing today? You're looking good, that's for sure."
    the_person.char "Aww, thank you. You're too kind. I'm doing well."
    "You chat with [the_person.possessive_title] for a while and slip in a compliment when you can. She seems flattered by all the attention."
    $ the_person.change_love(5, max_modified_to = 20)
    $ the_person.change_happiness(2)
    the_person.char "It's been fun talking [the_person.mc_title], we should do this again sometime!"
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
    $ mc.change_energy(-15)
    mc.name "Hey [the_person.title], you're looking particularly good today. I wish I got to see a little bit more of that fabulous body."
    $ mc.listener_system.fire_event("player_flirt", the_person = the_person)
    $ change_amount = mc.charisma + 1 + the_person.get_opinion_score("flirting") #We still cap out at 20, but we get there a little faster or slower depending on if they like flirting
    if change_amount + the_person.sluttiness > 20:
        $ change_amount = 20 - the_person.sluttiness
        if change_amount < 0:
            $ change_amount = 0

    $ the_person.change_happiness(the_person.get_opinion_score("flirting"))
    $ the_person.change_slut_temp(change_amount)
    $ the_person.change_love(3, max_modified_to = 25)
    $ the_person.discover_opinion("flirting")
    $ the_person.call_dialogue("flirt_response")
    $ the_person.apply_serum_study()
    return



label date_person(the_person): #You invite them out on a proper date
    $ lunch_date_action = Action("Ask her out to lunch. {image=gui/heart/Time_Advance.png}", lunch_date_requirement, "lunch_date_plan_label", args=the_person, requirement_args=the_person,
        menu_tooltip = "Take her out on casual date out to lunch. Gives you the opportunity to impress her and further improve your relationship.")
    $ movie_date_action = Action("Ask her out to the movies.", movie_date_requirement, "movie_date_plan_label", args=the_person, requirement_args=the_person,
        menu_tooltip = "Plan a more serious date to the movies. Another step to improving your relationship, and who knows what you might get up to in the dark!")
    $ dinner_date_action = Action("Ask her out to a romantic dinner.", dinner_date_requirement, "dinner_date_plan_label", args=the_person, requirement_args=the_person,
        menu_tooltip = "Plan a romantic, expensive dinner with her. Impress her and you might find yourself in a more intimate setting.")

    $ date_list = [lunch_date_action, movie_date_action, dinner_date_action, "Never mind."]
    $ return_value = call_formated_action_choice(date_list)
    if return_value == "Never mind.":
        return
    else: #It's an action, so it's one of the date actions (and must have been enabled).
        $ the_date = return_value
        $ the_date.call_action() #This is where you're asked to plan out the date, or whatever.

    return

label lunch_date_plan_label(the_person):
    # Take her out to lunch, raises love to a max of 50 if you pick the correct chat options
    if sister_role in the_person.special_role:
        mc.name "I was thinking about getting some lunch, do you want to come with me and hang out?"
        the_person.char "Hey, that sounds nice! You're always out of the house, I wish we got to spend more time to gether like we did when we were younger."

    elif mother_role in the_person.special_role:
        mc.name "I'm going to go out for lunch. You've been busy lately, would you like to take a break and join me?"
        the_person.char "Aww, it's so sweet that you still want to spend time with your mother. I'd love to!"

    elif aunt_role in the_person.special_role:
        mc.name "Would you like to come and have lunch with me? I haven't seen you much since I was a kid, I'm sure we have a lot to catch up on."
        the_person.char "It has been a long time, hasn't it. Lunch sounds wonderful!"

    elif cousin_role in the_person.special_role:
        mc.name "I'm going to get some lunch, would you like to come along with me?"
        the_person.char "You want me to be seen in public with you? You're really pushing it [the_person.mc_title], but sure."

    elif not (the_person.relationship == "Single" or the_person.get_opinion_score("cheating on men") > 0): #IF she likes cheating she doesn't even mention she's in a relationship
        mc.name "[the_person.title], I was going to get some lunch, would you like to join me? Maybe just grab a coffee and hang out for a while?"
        $ so_title = SO_relationship_to_title(the_person.relationship)
        the_person.char "That sounds nice, [the_person.title]."
        "She pauses and seems to consider something for a moment."
        the_person.char "Just so we're on the same page, this is just as friends, right? I have a [so_title], I don't want to get anything confused here."
        mc.name "Of course! I just want to hang out and talk, that's all."
        the_person.char "Okay, let's go then!"

    else:
        mc.name "Would you like to go get a coffee, maybe a little lunch, and just chat for a while? I fel like I want to get to know you better."
        the_person.char "That sounds nice, I think I'd like to get to know you better too."
        the_person.char "If you're ready to go right now I suppose I am too. Let's go!"

    call lunch_date_label(the_person) from _call_lunch_date_label #There's no need to schedule anything because this happens right awya.
    return

label lunch_date_label(the_person): #Could technically be included in the planning phase, but broken out to fit the structure of the other events.
    the_person.char "So, where do you want to go?"
    $ food_types = ["chinese food","thai food","italian food","sushi","korean barbeque","pizza","sandwiches"]
    $ the_type = get_random_from_list(food_types)
    mc.name "I know a nice place nearby. How do you like [the_type]?"
    the_person.char "No complaints, as long as it's good!"
    mc.name "Alright, let's go then!"
    "You and [the_person.title] walk together to a little lunch place nearby. You chat comfortably with each other as you walk."
    $ renpy.show("restaurant", what = restaraunt_background)
    "A bell on the door jingles as you walk in."
    mc.name "You grab a seat and I'll order for us."
    $ renpy.scene("Active")
    "You order food for yourself and [the_person.possessive_title] and wait until it's ready."
    $ mc.business.funds += -30
    $ the_person.draw_person(position = "sitting")
    "When it's ready you bring it over to [the_person.title] and sit down at the table across from her."
    the_person.char "Mmm, it looks delicious. Or maybe I'm just really hungry. Either way, let's eat!"
    "You dig into your lunch, chatting between bites about this and that. What do you talk about?"
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

    "Before you know it you've both finished your lunch and it's time to leave. You walk [the_person.title] outside and get ready to say goodbye."
    the_person.char "This was fun [the_person.mc_title], we should do it again."
    if not the_person.has_family_taboo() and (the_person.relationship == "Single" or the_person.get_opinion_score("cheating on men") > 0) and kiss_after:
        "She steps in close and kisses you. Her lips are soft and warm against yours."
        "After a brief second she steps back and smiles."
        mc.name "Yeah, we should. I'll see you around."

    else:
        "She steps close and gives you a quick hug, then steps back."
        mc.name "Yeah, we should. I'll see you around."

    $ renpy.scene("Active")
    call advance_time() from _call_advance_time_29
    return

label movie_date_plan_label(the_person):
    # She starts to wonder if she should be telling her boyfriend, etc. about this.
    if day%7 == 1 and time_of_day < 3:
        $ is_tuesday = True #It's already Tuesday and early enough that the date would be right about now.
    else:
        $ is_tuesday = False


    if sister_role in the_person.special_role:
        mc.name "Hey, I was wondering if you'd like to see a movie with me some time? You know, spend a little more time together as brother-sister."
        the_person.char "It's been like, a year since I went to the movies with you. I think it was when my date ghosted me and you swept in and saved the night by coming with me."
        the_person.char "I can't quite remember what we saw though..."
        "She seems puzzled for a moment, then shrugs and smiles at you."
        the_person.char "Oh well, it's probably not important. Sure thing [the_person.mc_title], a movie sounds fun!"
        if is_tuesday:
            the_person.char "How about tonight? I think tickets are half price."
        else:
            the_person.char "How about Tuesday night? I tickets are half price."

    elif mother_role in the_person.special_role:
        mc.name "Hey [the_person.title], would you like to come to the movies with me? I want to spend some more time together, mother and son."
        the_person.char "Aww, you're precious sweetheart. I would love to go to the movies with you."
        the_person.char "Remember how me and you use to watch movies together every weekend? I felt like our relationship was so close because of that."
        "She seems distracted by the memory for a moment, then snaps back to the conversation."
        if is_tuesday:
            the_person.char "Would you be free tonight?"
        else:
            the_person.char "Would you be free Tuesday night?"

    elif aunt_role in the_person.special_role:
        mc.name "[the_person.title], would you like to come see a movie with me? I think it would just be nice to spend some more time together."
        the_person.char "You know, I haven't been out much since I left my ex, so a movie sounds like a real good time."
        if is_tuesday:
            the_person.char "How about later tonight? I don't have anything going on."
        else:
            the_person.char "How about Tuesday night? I don't have anything going on then."

    elif cousin_role in the_person.special_role:
        mc.name "Hey, do you want to come see a movie with me and spend some time together?"
        the_person.char "Fine, but no telling people we're related, okay? I don't want anyone to think I might be a dweeb like you."
        "She gives you a wink."
        if is_tuesday:
            the_person.char "How about tonight? I didn't have anything going on."
        else:
            the_person.char "How about Tuesday? I don't have anything going on then."

    elif not the_person.relationship == "Single":
        mc.name "So [the_person.title], I was going to see a movie some time this week and wanted to know if you'd like to come with me."
        mc.name "It would give us a chance to spend time together."
        $ so_title = SO_relationship_to_title(the_person.relationship)
        if the_person.get_opinion_score("cheating on men") > 0:
            the_person.char "Oh, a movie sounds fun!"
            "She gives you a playful smile."
            the_person.char "Just don't tell my [so_title], okay? He might not like me hanging around with a hot guy like you."
            mc.name "My lips are sealed."
            if the_person.sluttiness > 60:
                if is_tuesday:
                    the_person.char "Treat me right and mine might not be. He's normally out late with work tonight, how does that sound?"
                else:
                    the_person.char "Treat me right and mine might not be. He's normally out late with work on Tuesdays, how does that sound?"
            else:
                if is_tuesday:
                    the_person.char "He's normally out late with work on Tuesdays, so how about would tonight sound for you?"
                else:
                    the_person.char "He's normally out late with work on Tuesdays, how does that sound for you?"

        else:
            the_person.char "Oh, a movie sounds fun! But..."
            mc.name "Is there something wrong?"
            the_person.char "No, I just don't know what my [so_title] would think. He might be a little jealous of you, you know?"
            mc.name "You don't have to tell him that I'll be there, if you don't want to. There's no reason you couldn't go out by yourself if you wanted to."
            "She thinks about it for a moment, then nods and smiles."
            if is_tuesday:
                the_person.char "You're right, of course. He's normally busy with work tonight, so how does that sound for you?"
            else:
                the_person.char "You're right, of course. He's normally busy with work on Tuesdays, how does that sound for you?"

    else:
        mc.name "So [the_person.title], I was wondering if you'd like to come see a movie with me some time this week."
        mc.name "It would give us a chance to spend some time together and get to know each other better."
        if is_tuesday:
            the_person.char "Oh, a movie sounds fun! I don't have anything going on tnight, would that work for you?"
        else:
            the_person.char "Oh, a movie sounds fun! I don't have anything going on Tuesday night, would that work for you?"

    menu:
        "Plan a date for Tuesday night.":
            mc.name "Tuesday would be perfect, I'm already looking forward to it."
            the_person.char "Me too!"

            $ movie_action = Action("Movie date", evening_date_trigger, "movie_date_label", args=the_person, requirement_args=1) #it happens on a tuesday.
            $ mc.business.mandatory_crises_list.append(movie_action)
            $ mc.business.event_triggers_dict["date_scheduled"] = True

        "Maybe some other time.":
            mc.name "I'm busy on Friday unfortunately."
            the_person.char "Well maybe next week then. Let me know, okay?"
            "She gives you a warm smile."

    return "Advance time"

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
            mc.name "I'm sorry, but something important came up at the last minute. We'll have to reschedule."
            $ the_person.change_love(-5)
            $ the_person.change_happiness(-5)
            the_person.char "I hope everything is okay. Maybe we can do this some other time then."
            return

    #TODO: if she has a boyfriend have him sometime show up. Depending on Love and stuff you can sometimes get them to break up (and instantly be in a realationship), or ruin her love and happiness.

    "You get ready and text [the_person.title] confirming the time and place. A little while later you meet her outside the theater."
    $ the_person.draw_person()
    the_person.char "Hey, good to see you!"
    the_person.char "I'm ready to go in, what do you want to see?"
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
    the_person.char "Did you want to get us some popcorn or anything like that?"
    menu:
        "Stop at the concession stand. -$20" if mc.business.funds >= 20:
            mc.name "Sure, you run ahead and I'll go get us some snacks."
            $ renpy.scene("Active")
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
            the_person.char "Right. Sure."
            "You find your theater, pick your seats, and settle down next to each other for the movie."


    $ the_person.draw_person(position = "sitting", lighting = [0.5,0.5,0.5])
    "You chat for a few minutes until the theater lights dim and the movie begins."

    if likes_movie: #She's enjoying the movie. Good for love gain, and you may be able to feel her up while she's enjoying the movie.
        "Halfway through the movie it's clear that [the_person.title] is having a great time. She's leaning forward in her seat, eyes fixed firmly on the screen."
        "As the movie approaches it's climax she reaches her hand down and finds yours to hold."
        "When it's finished you leave the theater together, still holding hands."
        $ the_person.draw_person()
        mc.name "So, did you like the movie?"
        the_person.char "It was amazing! Let's watch something like that next time."
        $ the_person.change_love(10, max_modified_to = 80)

    else: #She's bored. Bad for love gain, but good for getting her to fool around. She may start to feel you up to disctract herself.
        "Halfway through the movie it's beocming clear that [the_person.title] isn't enthralled by it."
        if (the_person.sluttiness - the_person.get_opinion_score("public sex") * 5) > 50 and (the_person.relationship == "Single" or the_person.get_opinion_score("cheating on men") > 0) and not the_person.has_family_taboo():
            "While you're watching you feel her rest her hand on your thigh. She squeezes it gently and slides her hand up higher and higher while whispering into your ear."
            the_person.char "I'm bored. You don't mind if I make this a little more intresting, do you?"
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
                        the_person.char "Do you want to go to the bathroom and fuck me, or do you want to finish in my mouth right here?"
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
                                $ the_person.review_outfit()
                                $ renpy.show("Theater", what = theater_background)
                                "You slip out of the bathroom as quickly as possible and return to your seats with some time pleasantly passed."

                            "Cum right here.":
                                mc.name "I want you to finish me here."
                                "She purrs in your ear and slides back down to her knees again. Her warm mouth wraps itself around your shaft and she starts to blow you again."
                                "It doesn't take long for her to bring you to the edge of your orgasm."
                                "You clutch at the movie seat arm rests and supress a grunt as you climax, blowing your hot load into [the_person.title]'s mouth and down her throat."
                                $ the_person.cum_mouth()
                                "She waits until you're finished, then pulls off your cock, wipes her lips on the back of her hand, and sits down next to you."
                                $ the_person.change_slut(3)
                                the_person.char "Thank you, that was fun."
                                "She takes your hand and holds it. You lean back, thoroughly spent, and zone out for the rest of the movie."

                "Tell her to knock it off.":
                    mc.name "I just want to watch a movie together. Can you at least try and pay attention?"
                    $ the_person.change_obedience(2)
                    $ the_person.change_happiness(-5)
                    $ the_person.change_love(-1)
                    "She pulls her hand back and sighs."
                    the_person.char "Aw, you're no fun."

        else:
            # SHe just annoys you by asking random questions
            the_person.char "Who is that again?"
            mc.name "He's working for the bad guy."
            the_person.char "Wait, I thought he was just with the good guys though."
            mc.name "He was lying. It's hard to explain."
            "Eventually the movie is over and you leave the theater together."

        $ the_person.draw_person()
        mc.name "So, did you like the movie?"
        the_person.char "It was okay. Let's try something else next time though."
        $ the_person.change_love(5, max_modified_to = 80)

    the_person.char "There will be a next time, right?"
    mc.name "I'd love for there to be."
    $ the_person.change_happiness(10)

    if sister_role not in the_person.special_role and mother_role not in the_person.special_role: #You live at home with those two, so it would be weird to kiss them goodnight.
        "She leans towards you and you give her a long kiss before saying goodnight."

    else:
        "She leans towards you and gives you a quick kiss."
        the_person.char "Let's head home then."

    $ renpy.scene("Active")
    $ mc.change_location(hall) #Put them back at home after the event, so if they were in the bathroom they aren't any more.
    $ mc.location.show_background()
    return "Advance Time"


label dinner_date_plan_label(the_person):
    if sister_role in the_person.special_role:
        mc.name "[the_person.title], I was wondering if you'd like to go out for a dinner date together. Some brother sister bonding time."
        the_person.char "That sounds great [the_person.mc_title]. Would Friday be good?"

    elif mother_role in the_person.special_role:
        mc.name "Mom, I was wondering if I could take you out to dinner, just the two of us. I'd enjoy some mother son bonding time."
        the_person.char "Aww, that's so sweet. How about Friday, after we're both finished with work."

    elif aunt_role in the_person.special_role:
        mc.name "[the_person.title], would you like to go out on a dinner date with me? I think it would be a nice treat for you."
        the_person.char "That sounds like it would be amazing. It's been tough, just me and [cousin.title]. I don't get out much any more."
        "She smiles and gives you a quick hug."
        the_person.char "How about Friday night?"

    elif cousin_role in the_person.special_role:
        mc.name "Hey, I want to take you out to dinner."
        the_person.char "Jesus, at least buy me dinner first. Wait a moment..."
        "She laughs at her own joke."
        the_person.char "Fine, how about Friday?"

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
            $ dinner_action = Action("Dinner date", evening_date_trigger, "dinner_date_label", args=the_person, requirement_args=4) #it happens on a friday, so day%7 == 4
            $ mc.business.mandatory_crises_list.append(dinner_action)
            $ mc.business.event_triggers_dict["date_scheduled"] = True

        "Maybe some other time.":
            mc.name "I'm busy on Friday unfortunately."
            the_person.char "Well maybe next week then. Let me know, okay?"
            "She gives you a warm smile."
    return

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
            the_person.char "I hope everything is okay. Maybe we can do this some other time then."
            return

    $ mc.change_location(downtown)
    $ downtown.show_background()
    "You get yourself looking as presentable as possible and head downtown."
    $ the_person.draw_person(emotion = "happy")
    "You meet up with [the_person.title] on time."
    the_person.char "So, where are we going tonight [the_person.mc_title]?"
    menu:
        "A cheap restaurant. -$50":
            $ mc.business.funds += -50
            the_person.char "It sounds cozy. Let's go, I'm starving!"

        "A moderately priced restaurant. -$100" if mc.business.funds >= 100:
            $ mc.business.funds += -100
            $ the_person.change_love(5)
            $ the_person.change_happiness(5)
            the_person.char "It sounds nice. Come on, I'm starving and could use a drink."

        "An expensive restaurant. -$300" if mc.business.funds >= 300:
            $ mc.business.funds += -300
            $ the_person.change_love(10)
            $ the_person.change_happiness(5)
            the_person.char "Oh, it sounds fancy! Well, I'm flattered [the_person.mc_title]."

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
                    $ the_person.add_situational_slut("Romanced",25,"What a wonderful date!")
                    call fuck_person(the_person, private = True) from _call_fuck_person_16
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
                    $ mc.location.show_background()
                    if not the_person.home in mc.known_home_locations:
                        $ mc.known_home_locations.append(the_person.home) #You know where she lives and can visit her.
                    "You join [the_person.possessive_title] when her taxi arrives. It's not a far ride to her house, and she invites you in."
                    "She pours you a drink and gives you a tour. When the tour ends in her bedroom you aren't surprised."

                    $ the_person.add_situational_slut("Romanced",25,"What a wonderful date!")
                    call fuck_person(the_person, private = True) from _call_fuck_person_17
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
    return "Advance Time"


label wardrobe_change_label(the_person):
    menu:
        "Add an outfit.":
            mc.name "[the_person.title], I've got something I'd like you to wear for me."
            $ renpy.scene("Active")
            call screen outfit_select_manager()
            $ the_person.draw_person()
            if not _return == "No Return":
                $ new_outfit = _return
                menu:
                    "Save as a full outfit.":
                        $ outfit_type = "full"

                    "Save as an underwear set." if new_outfit.is_suitable_underwear_set():
                        $ outfit_type = "under"

                    "Save as an underwear set. (disabled)" if not new_outfit.is_suitable_underwear_set():
                        pass

                    "Save as an overwear set." if new_outfit.is_suitable_overwear_set():
                        $ outfit_type = "over"

                    "Save as an overwear set. (disabled)" if not new_outfit.is_suitable_overwear_set():
                        pass


                $ slut_require = new_outfit.slut_requirement
                if outfit_type == "under":
                    $ slut_require = new_outfit.get_underwear_slut_score()
                elif outfit_type == "over":
                    $ slut_require = new_outfit.get_overwear_slut_score()

                if slut_require > the_person.sluttiness:
                    $ the_person.call_dialogue("clothing_reject")
                else:
                    $ the_person.add_outfit(new_outfit,outfit_type)
                    $ the_person.call_dialogue("clothing_accept")

            else:
                mc.name "On second thought, nevermind."

        "Delete an outfit.":
            mc.name "[the_person.title], lets have a talk about what you've been wearing."
            $ renpy.scene("Active")
            call screen outfit_delete_manager(the_person.wardrobe)
            $ the_person.draw_person()
            #TODO: Figure out what happens when someone doesn't have anything in their wardrobe.

        "Wear an outfit right now.":
            mc.name "[the_person.title], I want you to get changed for me."
            $ renpy.scene("Active")
            call screen girl_outfit_select_manager(the_person.wardrobe)
            if _return != "None":
                $ the_person.set_outfit(_return)

            $ the_person.draw_person()
            the_person.char "Is this better?"
    return

label serum_give_label(the_person):
    $ sneak_serum_chance = 70 + (mc.int*5) - (the_person.focus*5)  #% chance that you will successfully give serum to someone sneaklily. Less focused people are easier to fool.
    $ ask_serum_chance = 10*mc.charisma + 5*the_person.int #The more charismatic you are and the more intellectually curious they are the better the chance of success
    $ demand_serum_chance = mc.charisma * (the_person.obedience - 90) #The more charismatic you are and the more obedient they are the more likely this is to succeed.

    if sneak_serum_chance < 0:
        $ sneak_serum_chance = 0
    elif sneak_serum_chance > 100:
        $ sneak_serum_chance = 100

    if ask_serum_chance < 0:
        $ ask_serum_chance = 0
    elif ask_serum_chance > 100:
        $ ask_serum_chance = 100

    if mc.business.get_employee_title(the_person) == "None":
        $demand_serum_chance += -35 #if she doesn't work for you there is a much lower chance she will listen to your demand (unless you are very charismatic or she is highly obedient.)
    if demand_serum_chance < 0:
        $ demand_serum_chance = 0
    elif demand_serum_chance > 100:
        $ demand_serum_chance = 100

    $ pay_serum_cost = the_person.salary * 5
    $ rand_chance = renpy.random.randint(0,100)

    menu:
        "Give it to her stealthily.\n{size=22}Success Chance: [sneak_serum_chance]%%{/size}": #TODO: Have this modified by something so there are interesting gameplay decisions
            "You chat with [the_person.title] for a couple of minutes. Waiting to find a chance to deliver a dose of serum."
            if rand_chance < sneak_serum_chance:
                #Success
                "You're able to distract [the_person.title] and have a chance to give her a dose of serum."
                call give_serum(the_person) from _call_give_serum

            else:
                #Caught!
                "You finally distract [the_person.title] and have a chance to give her a dose of serum."
                the_person.char "Hey, what's that?"
                "You nearly jump as [the_person.title] points down at the small vial of serum you have clutched in your hand."
                $ avoid_chance = renpy.random.randint(0,10)
                if avoid_chance < mc.charisma:
                    if mc.business.get_employee_title(the_person) == "None":
                        mc.name "This? Oh, it's just something we're working on at the lab that I thought you might be interested in."
                        "You dive into a technical description of your work, hoping to distract [the_person.title] from your real intentions."

                    else:
                        mc.name "This? Oh, it's just one of the serums I grabbed from production for quality control. I was just fidgeting with it I guess."
                        "You make small talk with [the_person.title], hoping to distract her from your real intentions."
                    "After a few minutes you've managed to avoid her suspicion, but haven't been able to deliver the dose of serum."

                else:
                    mc.name "This? Uh..."
                    $ the_person.draw_person(emotion="angry")
                    $ the_person.change_obedience(-10)
                    $ the_person.change_happiness(-10)
                    $ the_person.change_love(-5)
                    the_person.char "Were you about to put that in my drink? Oh my god [the_person.mc_title]!"
                    mc.name "Me? Never!"
                    "[the_person.title] shakes her head and storms off. You can only hope this doesn't turn into soemthing more serious."
                    $renpy.scene("Active")
                    return

        "Ask her to take it.\n{size=22}Success Chance: [ask_serum_chance]%%{/size}" if not mandatory_unpaid_serum_testing_policy.is_owned() or mc.business.get_employee_title(the_person) == "None":
            if mc.business.get_employee_title(the_person) == "None":
                mc.name "[the_person.title], I've got a project going on at work that could really use a test subject. Would you be interested in helping me out?"

            else:
                mc.name "[the_person.title], there's a serum design that is in need of a test subject. Would you be interested in helping out with a quick field study?"

            if rand_chance < ask_serum_chance:
                #Success
                if mc.business.get_employee_title(the_person) == "None":
                    if the_person.personality is nora_personality:
                        the_person.char "I'd be happy to help. I've seen your work, I have complete confidence you've tested this design thoroughly."
                    else:
                        the_person.char "I'd be happy to help, as long as you promise it's not dangerous of course. I've always wanted to be a proper scientist!"
                else:
                    the_person.char "I'll admit I'm curious what it would do to me. Okay, as long as it's already passed the safety test requirements, of course."
                mc.name "It's completely safe, we just need to test what the results from it will be. Thank you."
                call give_serum(the_person) from _call_give_serum_2

            else:
                #Denies
                $ the_person.change_obedience(-2)
                the_person.char "I'm... I don't think I would be comfortable with that. Is that okay?"
                mc.name "Of course it is, that's why I'm asking in the first place."

        "Ask her to take it.\n{size=22}Success Chance: Required by Policy{/size}" if mandatory_unpaid_serum_testing_policy.is_owned() and not mc.business.get_employee_title(the_person) == "None":
            #Auto success
            mc.name "[the_person.title], we're running field trials and you're one of the test subjects. I'm going to need you to take this."
            call give_serum(the_person) from _call_give_serum_3

        "Demand she takes it.\n{size=22}Success Chance: [demand_serum_chance]%%{/size}": #They must work for you to demand it.
            mc.name "[the_person.title], you're going to drink this for me."
            "You pull out a vial of serum and present it to [the_person.title]."
            the_person.char "What is it for, is it important?"
            mc.name "Of course it is, I wouldn't ask you to if it wasn't."
            if rand_chance < demand_serum_chance:
                #Success
                the_person.char "Okay, if that's what you need me to do..."
                call give_serum(the_person) from _call_give_serum_4
            else:
                #Refues
                $ the_person.draw_person(emotion = "angry")
                $ the_person.change_obedience(-2)
                $ the_person.change_happiness(-2)
                $ the_person.change_love(-2)
                the_person.char "You expect me to just drink random shit you hand to me? I'm sorry, but that's just ridiculous."

        "Pay her to take it.\n{size=22}Costs: $[pay_serum_cost]{/size}" if mandatory_paid_serum_testing_policy.is_owned() and not mandatory_unpaid_serum_testing_policy.is_owned() and not mc.business.get_employee_title(the_person) == "None": #This becomes redundent when they take it for free.
            #Pay cost and proceed
            $ mc.business.funds += -pay_serum_cost
            mc.name "[the_person.title], we're running field trials and you're one of the test subjects. I'm going to need you to take this, a bonus will be added onto your paycheck."
            call give_serum(the_person) from _call_give_serum_5


        "Pay her to take it.\n{size=22}Requires: Mandatory Paid Serum Testing{/size} (disabled)" if not mandatory_unpaid_serum_testing_policy.is_owned() and not mandatory_paid_serum_testing_policy.is_owned() and not mc.business.get_employee_title(the_person) == "None":
            pass

        "Do nothing.":
            pass
    return

label seduce_label(the_person):
    mc.name "[the_person.title], I've been thinking about you all day. I just can't get you out of my head."

    if prostitute_role in the_person.special_role and the_person.love < 20:
        the_person.char "I've been thinking about you too, but I've got bills to pay and I can't do this for free."
        return
    elif prostitute_role in the_person.special_role and the_person.love >= 20:
        the_person.char "I should really make you pay for this... but you're one of my favourites and I'm curious what you had in mind."
    else:
        $ the_person.call_dialogue("seduction_response")

    $ random_chance = renpy.random.randint(0,100)
    $ chance_service_her = the_person.sluttiness - 20 - (the_person.obedience - 100) + (mc.charisma * 4) + (the_person.get_opinion_score("taking control") * 4)
    $ chance_both_good = the_person.sluttiness - 10 + mc.charisma * 4
    $ chance_service_him = the_person.sluttiness - 20 + (the_person.obedience - 100) + (mc.charisma * 4) + (the_person.get_opinion_score("being submissive") * 4)

    if chance_service_her > 100:
        $ chance_service_her = 100
    elif chance_service_her < 0:
        $ chance_service_her = 0

    if chance_both_good > 100:
        $ chance_both_good = 100
    elif chance_both_good < 0:
        $ chance_both_good = 0

    if chance_service_him > 100:
        $ chance_service_him = 100
    elif chance_service_him < 0:
        $ chance_service_him = 0

    $ seduced = False #Flip to true if the approach works
    menu:
        "I want to make you feel good.\n{size=22}Success Chance: [chance_service_her]%%\nModifiers: +10 Sluttiness, -5 Obedience{/size} (tooltip)Suggest you will focus on her. She will be sluttier for the encounter, but more likely to make demands and take control. More likely to succeed with less obedient girls.": #Bonus to her sluttiness, penalty to obedience
            "You lean in close whisper what you want to do to her."
            if random_chance < chance_service_her: #Success
                $ seduced = True
                $ the_person.add_situational_slut("seduction_approach",10, "You promised to focus on me.")
                $ the_person.add_situational_obedience("seduction_approach",-5, "You promised to focus on me.")
                $ the_person.change_arousal(-5*the_person.get_opinion_score("taking control"))
                $ the_person.discover_opinion("taking control")
            else: #Failure
                pass

        "Let's have a good time.\n{size=22}Success Chance: [chance_both_good]%%\nModifiers: None{/size} (tooltip)Suggest you'll both end up satisfied. Has no extra effect on her sluttiness or obedience, but is not affected by her obedience in return.": #Standard
            "You lean in close and whisper what you want to do together."
            if random_chance < chance_both_good:
                $ seduced = True
            else:
                pass

        "I need you to get me off.\n{size=22}Success Chance: [chance_service_him]%%\nModifiers: +10 Obedience, -5 Sluttiness{/size} (tooltip)Demand that she focuses on making you cum. She will be more obedient but less slutty for the encounter. More likely to succeed with highly obedient girls.": #Bonus to obedience, penalty to sluttiness
            "You lean in close and whisper what you want her to do to you."
            if random_chance < chance_service_him:
                $ seduced = True
                $ the_person.add_situational_slut("seduction_approach",-5, "You want me to serve you.")
                $ the_person.add_situational_obedience("seduction_approach",10, "You want me to serve you.")
                $ the_person.change_arousal(5*the_person.get_opinion_score("being submissive"))
                $ the_person.discover_opinion("being submissive")
            else:
                pass



    if seduced and the_person.sexed_count < 1:

        $ extra_people_count = mc.location.get_person_count() - 1
        $ in_private = True
        if extra_people_count > 0: #We have more than one person here
            $ the_person.call_dialogue("seduction_accept_crowded")
            menu:
                "Find somewhere quiet.\n{size=22}No interuptions{/size}":
                    "You take [the_person.title] by the hand and find a quiet spot where you're unlikely to be interupted."

                "Stay right here.\n{size=22}[extra_people_count] watching{/size}":
                    if the_person.sluttiness < 50:
                        mc.name "I think we'll be fine right here."
                        the_person.char "I... Okay, if you say so."

                    $ in_private = False
        else:
            $ the_person.call_dialogue("seduction_accept_alone")

        call fuck_person(the_person,private = in_private) from _call_fuck_person

        #TODO: This is where we put stuff for her being in a relationship but wants to start an affair with you.

        $ the_person.review_outfit()

        #Tidy up our situational modifiers, if any.
        $ the_person.clear_situational_slut("public_sex")
        $ the_person.clear_situational_slut("seduction_approach")
        $ the_person.clear_situational_obedience("seduction_approach")
    else:
        $ the_person.call_dialogue("seduction_refuse")
        $ the_person.clear_situational_slut("seduction_approach")
        $ the_person.clear_situational_obedience("seduction_approach")

    $ the_person.sexed_count += 1
    return
