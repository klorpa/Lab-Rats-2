# Contains all of the events for the egirl role. Most of these are events triggered from the PC's room and take place entirely online

init -2 python:
    def check_insta_requirement():
        return True

    def check_insta_requirement():
        return True

    def check_dikdok_requirement():
        return True

    def check_onlyfans_requirement():
        return True

    def ask_location_requirement(the_person):
        return True

    def text_chat_requirement(the_person):
        if mc.energy < 15:
            return "Not enough energy"
        return True

    def text_flirt_requirement(the_person):
        if mc.energy < 15:
            return "Not enough energy"
        return True

init -1 python:
    texting_actions = [] #List of actions that are displayed when you select a person to text
    ask_location_action = Action("Ask where she is.", ask_location_requirement, "ask_location_label")
    text_chat_action = Action("Chat with her. -15{image=gui/extra_images/energy_token.png}", text_chat_requirement, "text_chat_label")
    text_flirt_action = Action("Flirt with her. -15{image=gui/extra_images/energy_token.png}", text_flirt_requirement, "text_flirt_label")

    texting_actions.append(ask_location_action)
    texting_actions.append(text_chat_action)
    texting_actions.append(text_flirt_action)


# Use this screen any time you want to display a phone based text log. the "newest" parameters can be used to force something to the bottom with the History log might not have been updated (Used in the say statement).
label browse_internet(is_phone = True): #TODO: Maybe make this a generic function you can use at any time to call people, make it a "use phone" type of thing.
    # The phone thing should be a location based default option, kind of like "Go somewhere else". It makes it easier to gate events (ie. no triggering events inside of events) and tell where the player is.
    # We may want some static options that can be brought up at any time.
    # TODO: We absolutely want the player to be able to save pictures to their phone and set them as a background. That sounds great.
    #TODO: Provide a bunch of internet browsing options. Later on this leads to "OnlyFanatics" and "InstaPic", but it might start out with just some porn (or a comment about how "normal porn just seems boring now")
    $ text_actions = ["Text Someone"]
    $ internet_actions = ["Check the Internet"]
    $ other_actions = ["Other Actions"]

    python:
        for a_person in mc.phone.get_person_list():
            text_actions.append(a_person)

        check_insta_action = Action("Check InstaPic", check_insta_requirement, "check_insta")
        check_dikdok_action = Action("Check Dikdok", check_dikdok_requirement, "check_dikdok")
        check_onlyfans_action = Action("Check OnlyFanatics", check_onlyfans_requirement, "check_onlyfans")

        internet_actions.append(check_insta_action)
        internet_actions.append(check_dikdok_action)
        internet_actions.append(check_onlyfans_action)


    $ other_actions.append("Back")
    call screen main_choice_display([text_actions, internet_actions, other_actions], draw_hearts_for_people = False, draw_person_previews = False)
    $ clear_scene()

    if _return == "Back":
        return
    elif isinstance(_return, Action):
        $ the_action = _return
        $ the_action.call_action()
        if _return == "Skip Phone":
            return
        else:
            call browse_internet() from _call_browse_internet_1

    elif isinstance(_return, Person):
        $ the_person = _return
        $ return_to_phone = True
        $ mc.start_text_convo(the_person)

        $ text_actions_display_list = []
        python:
            for act in texting_actions:
                text_actions_display_list.append([act, the_person])

            for role in the_person.special_role:
                for act in role.internet_actions:
                    text_actions_display_list.append([act, the_person])

            for act in the_person.get_duty_internet_actions():
                if keep_talking or act.is_fast:
                    text_actions_display_list.append([act, the_person])


        $ text_actions_display_list.sort(key = sort_display_list, reverse = True)
        $ text_actions_display_list.insert(0,"Text [the_person.title]")

        $ other_actions_list = ["Other Actions"]
        $ other_actions_list.append("Back")

        call screen main_choice_display([text_actions_display_list, other_actions])
        if _return == "Back":
            pass

        elif isinstance(_return, Action):
            $ the_action = _return
            $ the_action.call_action(the_person)
            $ return_to_phone = _return

        if return_to_phone:
            $ mc.end_text_convo()
            call browse_internet() from _call_browse_internet_2
    else:
        pass #It was an action, we've taken care of it already.
    return

label ask_location_label(the_person):
    $ return_to_phone = True
    mc.name "Hey, where are you right now?"
    if the_person.love < 0:
        the_person "Why would I tell you that?"

    if mc.location.has_person(the_person): #She's in the same location as you.
        $ mc.end_text_convo()
        $ the_person.draw_person()
        "[the_person.possessive_title] glances at her phone when it buzzes. She looks up at you and shakes her head."
        the_person "I'm right here, silly. What's up?"
        $ return_to_phone = False
        call talk_person(the_person) from _call_talk_person_26

    else:
        $ the_person_location = None
        python:
            for place in list_of_places:
                if place.has_person(the_person):
                    the_person_location = place
                    break
        if the_person_location is None:
            the_person "I'm... not sure. I think Vren forgot to put me somewhere."
            the_person "I'm going to get this sorted out. We'll have to talk later."
        elif the_person_location == the_person.home:
            the_person "I'm at home right now."
        else:
            the_person "You can find me at [the_person_location.name] right now."
    return return_to_phone

label text_chat_label(the_person):
    $ return_to_phone = True
    if mc.location.has_person(the_person): #She's in the same location as you.
        mc.name "Hey, how's it going [the_person.title]?"
        $ mc.end_text_convo()
        $ the_person.draw_person()
        "[the_person.possessive_title] glances at her phone when it buzzes. She looks up at you and shakes her head."
        the_person "I'm right here [the_person.mc_title]. We can just chat if you'd like."
        call small_talk_person(the_person) from _call_small_talk_person_1
        $ return_to_phone = False
    else:
        call small_talk_person(the_person, is_phone = True) from _call_small_talk_person_2
    return return_to_phone

label text_flirt_label(the_person, apply_energy_cost = True, skip_intro = True):
    $ return_to_phone = True
    if mc.location.has_person(the_person) and not skip_intro: #She's in the same location as you.
        mc.name "Hey, [the_person.title]. What are you up to right now?"
        $ mc.end_text_convo()
        $ the_person.draw_person()
        "[the_person.possessive_title] glances at her phone when it buzzes. She looks up at you and shakes her head."
        the_person "I'm right here [the_person.mc_title], let's just talk."
        call flirt_person(the_person) from _call_flirt_person
        $ return_to_phone = False
    else:
        if (apply_energy_cost):
            $ mc.change_energy(-15)
        $ the_person.call_dialogue("flirt_response_text")
        menu:
            "Be romantic.":
                "You text back and forth with [the_person.title], being kind and romantic."
                the_person "I've got to run, but this was nice [the_person.mc_title]. Talk to you later!"
                $ the_person.change_happiness(2)
                $ the_person.change_love(1, max_modified_to = 25)
                #$ the_person.call_dialogue("text_flirt_romantic") #TODO: Write personality specific dialogue for this

            "Be dirty.":
                "You text back and forth with [the_person.title], being as flirty as you think you can get away with."
                if the_person.effective_sluttiness() < 20:
                    "She doesn't seem very interested, unfortunately."
                    the_person "I've got to go, sorry. Talk some other time, okay?"
                else:
                    $ the_person.change_slut(1, 30)
                    the_person "Hahah, you're so funny [the_person.mc_title]."
                    the_person "I've got to run. Talk to you later, okay?"
                mc.name "Alright, talk to you later."
                #$ the_person.call_dialogue("text_flirt_dirty") #TODO: Write personality specific stuff

            "Ask for nudes.":
                mc.name "Hey, I'm feeling bored and lonely. Send me something to cheer me up."
                if the_person.has_role(affair_role):
                    "There's a pause, then she texts you back."
                    the_person "For you, anything."
                    python:
                        the_person.outfit.strip_to_underwear()
                        the_person.outfit.strip_to_tits()
                        the_person.draw_person(position = "kneeling1", emotion = "happy", the_animation = None)
                    $ mc.change_locked_clarity(15)
                    "Another pause, then she sends you a picture."
                    the_person "Wish you were here so we could really have some fun."
                    mc.name "We'll have some fun soon, I promise."

                    $ the_person.draw_person(position = "back_peek", the_animation = None)
                    "She sends you another pic."
                    $ the_person.change_slut(1, 60)
                    the_person "Don't make me wait too long!"

                elif the_person.has_role(girlfriend_role):
                    if the_person.effective_sluttiness() >= 30:
                        the_person "You're so bad for me! One second..."
                        python:
                            the_person.outfit.strip_to_underwear()
                            the_person.outfit.strip_to_tits()
                            the_person.draw_person(position = "kneeling1", emotion = "happy", the_animation = None)
                        $ mc.change_locked_clarity(15)
                        "Another pause, then she sends you a picture."
                        the_person "Come and see me so we can have some real fun!"
                        $ the_person.change_slut(1, 60)
                        mc.name "I'll see you soon, I promise."

                    else:
                        the_person "Feeling a little frisky? Well, let's see what I can do..."
                        "There's a pause, then she sends you a picture."
                        python:
                            the_person.outfit.strip_to_underwear()
                            the_person.draw_person(emotion = "happy", the_animation = None)
                        $ mc.change_locked_clarity(10)
                        $ the_person.change_slut(1, 40)
                        the_person "You'll have to convince me in person to show you any more. Hope that cures your \"boredom\"."
                elif the_person.is_family():
                    if the_person.effective_sluttiness() >= 60:
                        the_person "I really shouldn't do this, but..."
                        "There's a pause, then she sends you a picture."
                        python:
                            the_person.outfit.strip_to_underwear()
                            the_person.outfit.strip_to_tits()
                            the_person.draw_person(position = "kneeling1", emotion = "happy", the_animation = None)
                        $ mc.change_locked_clarity(15)
                        the_person "How's that?"
                        $ the_person.change_slut(1, 65)
                        mc.name "You're looking great [the_person.title], that's just what I wanted."

                    elif the_person.effective_sluttiness() >= 40:
                        the_person "I really shouldn't do this, but I know you'll like it..."
                        "There's a pause, then she sends you a picture."
                        python:
                            the_person.outfit.strip_to_underwear()
                            the_person.draw_person(emotion = "happy", the_animation = None)

                        $ mc.change_locked_clarity(10)
                        $ the_person.change_slut(1, 55)
                        the_person "There, I hope that helps. Don't show it to anyone else!"

                    else:
                        the_person "What do you want me to send?"
                        mc.name "You know, a picture of yourself. Show me something fun."
                        "There's a long pause."
                        the_person "Come on [the_person.mc_title], don't be silly. Talk to you later!"
                else:
                    if the_person.effective_sluttiness() >= 50:
                        the_person "I really shouldn't do this, but..."
                        python:
                            the_person.outfit.strip_to_underwear()
                            the_person.outfit.strip_to_tits()
                            the_person.draw_person(position = "kneeling1", emotion = "happy", the_animation = None)
                        $ mc.change_locked_clarity(15)
                        "There's a pause, then she sends you a picture."
                        $ the_person.change_slut(1, 55)
                        the_person "It's kind of fun doing this! Enjoy ;)"

                    elif the_person.effective_sluttiness() >= 30:
                        the_person "I shouldn't, but I guess a little fun wouldn't hurt."
                        the_person "One sec, I need to find some good light."
                        python:
                            the_person.outfit.strip_to_underwear()
                            the_person.draw_person(emotion = "happy", the_animation = None)
                        $ mc.change_locked_clarity(10)
                        "There's a pause, then she sends you a picture."
                        $ the_person.change_slut(1, 35)
                        the_person "I'm so embarrassed! I hope you like it!"

                    else:
                        "There's a long pause before [the_person.possessive_title] responds."
                        the_person "I'm not sure what you mean [the_person.mc_title]. I need to go, we can talk later okay?"
                # $ the_person.call_dialogue("text_flirt_nudes") #TODO: Personality specific responses
                $ clear_scene()

            # "Send a dick pic.": #TODO: Implement this, girls might respond by sending you nudes.
            #     if mc.location.get_person_count() > 0:
            #         "You find a quiet spot where nobody will spot you taking a picture of your dick."
            #     "You rub your cock until it begins to swell and harden. When you're standing hard and impressive you snap a picture with your phone."
            #     mc.name "Take a look at this. Like what you see?"
            #     "You text her the picture."
            #     $ the_person.call_dialogue("text_flirt_dick_pic")

    return return_to_phone

label view_twatch(the_person): #TODO: Implement this as a role at some point
    # TODO: Watch a girl stream, different outcomes based on different games.
    # TODO: Much more likely to spawn on introverts, basically inverted from Insta or DikDok.
    # TODO In all cases if she's slutty she's doing things like teasing the camera.
    # TODO: She'll pimp her justfanatics if she has one
    # TODO: Otherwise you'll just end up throwing a bunch of money at her without any results.
    return
