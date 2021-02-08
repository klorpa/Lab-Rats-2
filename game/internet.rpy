# Contains all of the events for the egirl role. Most of these are events triggered from the PC's room and take place entirely online

init -2 python:
    def check_insta_requirement():
        return True

    def check_insta_requirement():
        return True

    def check_dikdok_requirement():
        return True

    def check_justfan_requirement():
        return True

label browse_internet(is_phone = True): #TODO: Maybe make this a generic function you can use at any time to call people, make it a "use phone" type of thing.
    # The phone thing should be a location based default option, kind of like "Go somewhere else". It makes it easier to gate events (ie. no triggering events inside of events) and tell where the player is.
    # We may want some static options that can be brought up at any time.
    # TODO: We absolutely want the player to be able to save pictures to their phone and set them as a background. That sounds great.
    #TODO: Provide a bunch of internet browsing options. Later on this leads to "JustFanatics" and "Instapic", but it might start out with just some porn (or a comment about how "normal porn just seems boring now")
    $ text_actions = ["Text Messages"]
    $ internet_actions = ["Internet"]
    $ other_actions = ["Other Actions"]

    python:
        for a_person in mc.phone.get_person_list():
            text_actions.append(a_person)

        check_insta_action = Action("Check InstaPic", check_insta_requirement, "check_insta")
        check_dikdok_action = Action("Check Dikdok", check_dikdok_requirement, "check_dikdok")
        check_justfan_action = Action("Check JustFanatics", check_justfan_requirement, "check_justfan")

        internet_actions.append(check_insta_action)
        internet_actions.append(check_dikdok_action)
        internet_actions.append(check_justfan_action)


    $ other_actions.append("Back")
    call screen main_choice_display([text_actions, internet_actions, other_actions], draw_hearts_for_people = False)
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

    elif isinstance(_return, Person): #TODO: Eventually this will have a custom UI that will show a persons chat log.
        $ the_person = _return
        $ return_to_phone = True
        # if _return == "Skip Phone": #Allows events to skip going to your phone. Usually triggers when an event has you travel somewhere, pass time, ect.
        #     return
        # else:
        "(Under Construction. More Texting options will be added in v0.38)"
        menu:
            "Ask where she is.":
                $ mc.having_text_conversation = the_person
                mc.name "Hey, where are you right now?"
                if the_person.love < 0:
                    the_person "Why would I tell you that?"

                if mc.location.has_person(the_person): #She's in the same location as you.
                    $ mc.having_text_conversation = None
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
                $ mc.having_text_conversation = False

        if return_to_phone:
            call browse_internet() from _call_browse_internet_2
    else:
        pass #It was an action, we've taken care of it already.
    return

label check_insta():
    # TODO: Check if anyone you know has posted pictures on Instapic
    # TODO: Ability to find new Insta girls who are posting revealing pics.
    "404 - Page not found. (Under Construction)" (what_style = "text_message_style")
    return

label check_dikdok():
    # TODO: Checks if anyone you know is streamin on twatch.
    # Listed something like "Lily\n-Playing: Just Talking"
    "404 - Page not found. (Under Construction)" (what_style = "text_message_style")
    return

label check_justfan():
    # TODO: Check if anyone you know is on Just fanatics. Some girls may be live, others may have old posts you can comment on.
    "404 - Page not found. (Under Construction)" (what_style = "text_message_style")
    return

label view_insta(the_person):
    # TODO: Check the recent posts by the_person on insta,
    # Lets you just view, leave a comment, or PM them for something more extreme.
    # One of the PM's might be "Where can I see more of you?"
    # -> Leads to her twatch or justfans
    return

label view_twatch(the_person):
    # TODO: Watch a girl stream, different outcomes based on different games.
    # TODO In all cases if she's slutty she's doing things like teasing the camera.
    # TODO: She'll pimp her justfanatics if she has one
    # TODO: Otherwise you'll just end up throwing a bunch of money at her without any results.
    return

label view_justfan(the_person):
    #TODO: Check out a girls nude pics/videos
    #TODO: Sometimes she's streaming live.
    #TODO: Pay extra to get something "special"
    # -> Stuff like themed texts throughout the day, specific positions, ect.

    return
