#All of the info and stuff for the Onlyfans role

init -2 python:
    def onlyfans_on_turn(the_person):
        return

    def onlyfans_on_day(the_person):
        underwear_weight = 25 + 10*the_person.get_opinion_score("lingerie")
        nudes_weight = 25 + 10*(the_person.get_opinion_score("showing her tits") + the_person.get_opinion_score("showing her ass"))
        dildo_weight = 25 + 10*(the_person.get_opinion_score("public sex") + the_person.get_opinion_score("masturbating"))

        content_types = [["underwear", underwear_weight], ["nudes", nudes_weight], ["dildo", dildo_weight]] #Decide on what new content she has on her site for the day.
        if the_person.event_triggers_dict.get("onlyfans_new_boobs_brag", False):
            the_person.event_triggers_dict["onlyfans_content_type"] = "new_boobs"
            the_person.event_triggers_dict["onlyfans_new_boobs_brag"] = False
        else:
            the_person.event_triggers_dict["onlyfans_content_type"] = get_random_from_weighted_list(content_types)
        the_person.event_triggers_dict["onlyfans_visited_today"] = False

        return



label check_onlyfans():
    $ onlyfans_list = ["Accounts You Know"]
    python:
        for a_person in mc.phone.get_person_list():
            if a_person.has_role(onlyfans_role) and a_person.event_triggers_dict.get("onlyfans_known", False): #We may add a flag to have some girls (ie. Lily) hide their profile under a different name.
                onlyfans_list.append(a_person) #TODO: Have a flag that notes girls who have a new picture. (Flag is set at the beginning of each day in the on_day action)

    $ other_options_list = ["Other Options", "Back"]
    call screen main_choice_display([onlyfans_list, other_options_list], draw_hearts_for_people = False, draw_person_previews = False)
    $ picked_option = _return
    if isinstance(picked_option, Person):
        call view_onlyfans(picked_option) from _call_view_onlyfans
    elif picked_option == "Back":
        return

    return

label view_onlyfans(the_person):
    if the_person.event_triggers_dict.get("onlyfans_subscription_valid_until", 0) < day: # If you haven't recently subscribed
        $ the_person.apply_outfit(lingerie_wardrobe.pick_random_outfit())
        $ the_person.draw_person(emotion = "happy")
        "A short video plays when you bring up [the_person.possessive_title]'s profile."
        the_person "Welcome to my OnlyFanatics page! For just $5 you can have access all day to my dirtiest videos."
        the_person "Or start a weekly subscription and help support me as I make more tasty content just for you!"
        the_person "There's new content every day, so you'll always have something to enjoy."
        "She blows a kiss to the camera, then a subscription information box pops up."
        menu:
            "Subscribe for the day. -$5" if mc.business.has_funds(5):
                $ the_person.event_triggers_dict["onlyfans_subscription_valid_until"] = day
                $ mc.business.change_funds(-5)

            "Subscribe for the day. -$5 (disabled)" if not mc.business.has_funds(5):
                pass

            "Subscribe for the week. -$20" if mc.business.has_funds(20):
                $ the_person.event_triggers_dict["onlyfans_subscription_valid_until"] = day + 7
                $ mc.business.change_funds(-20)

            "Subscribe for the week. -$20 (disabled)" if not mc.business.has_funds(20):
                pass

            "Back":
                pass


    if the_person.event_triggers_dict.get("onlyfans_subscription_valid_until", 0) >= day:
        #NOTE: These should all be deterministic events (ie. no random chance) because the MC can return here whenever they want and should be given the same content.
        $ give_clarity = True # Only get Clarity from one post a day.
        if the_person.event_triggers_dict.get("onlyfans_visited_today",False):
            $ give_clarity = False
        $ the_person.event_triggers_dict["onlyfans_visited_today"] = True
        if the_person.event_triggers_dict.get("onlyfans_content_type", "underwear") == "new_boobs":
            $ the_person.apply_outfit(lingerie_wardrobe.pick_random_outfit())
            $ the_person.draw_person()
            $ mc.change_locked_clarity(15)
            "[the_person.title] is standing in front of her bed in her underwear."
            the_person "Hello everyone, glad to have you stop by. You might notice something different today..."
            $ the_person.draw_person(position = "sitting")
            "[the_person.possessive_title] sits down on the edge of her bed and crosses her legs."
            the_person "That's because I got something special, just for you. Have you noticed what it is yet?"
            "She leans towards the camera, emphasising her tits."
            the_person "How about now? See anything different? Maybe a little... bigger?"
            "She uncrosses her legs and plants her hands between her thighs. Her arms pinch her breasts together, squeezing them and making them look even bigger."
            the_person "That's right, I decided to go and get some bigger tits just for you. Do you like them?"
            "She wiggles her shoulders and jiggles her boobs."
            the_person "I knew you would. I knew you'd like me getting big, fake tits just for you to look at."
            if the_person.outfit.tits_visible():
                $ the_person.draw_person()
                $ mc.change_locked_clarity(10)
                "She stands up and walks towards the camera, swaying her shoulders to bounce her breasts even more than normal."
            else:
                the_person "But you want a closer look, right? Want a better look at my fake bimbo tits? Here..."
                $ the_person.draw_person()
                $ top_item = the_person.outfit.get_upper_top_layer()
                "She stands up and walks towards the camera, sliding her [top_item.display_name] around playfully."
                if the_person.outfit.can_half_off_to_tits():
                    $ strip_list = the_person.outfit.get_half_off_to_tits_list()
                    $ generalised_strip_description(the_person, strip_list)
                else:
                    $ strip_list = the_person.outfit.get_tit_strip_list()
                    $ generalised_strip_description(the_person, strip_list)
                $ mc.change_locked_clarity(20)
                the_person "Isn't that better? Take a close look at them"
            the_person "Don't these make me look like a complete slut?"
            "She cups them in her hands and pushes them together. She closes her eyes and moans dramatically."
            the_person "Mmm, I think I like that. I like looking like a brain dead bimbo for you."
            "[the_person.title] fingers her nipples gently, making sure to get a closeup for the camera."
            the_person "Make sure to come back tomorrow, and every day after that, for more videos of me having fun."
            $ clear_scene()
            "She kisses her hand, then slides it towards the camera until everything goes black."

        elif the_person.event_triggers_dict.get("onlyfans_content_type", "underwear") == "underwear": # Tries on different underwear types
            $ the_person.apply_outfit(lingerie_wardrobe.pick_random_outfit())
            $ the_person.draw_person()
            "[the_person.title] is standing in front of her bed, which has a few shopping bags spread out on it."
            "She waves at the camera and smiles."
            the_person "I went shopping today, and I have a big haul of new lingerie I want to try on for you..."
            $ the_person.draw_person(position = "walking_away")
            if give_clarity:
                $ mc.change_locked_clarity(10)
            "She turns around and leans over onto her bed, intentionally showing her ass off to the camera."
            the_person "Let's see what else I have..."
            $ strip_list = the_person.outfit.get_full_strip_list()
            $ generalised_strip_description(the_person, strip_list)
            if give_clarity:
                $ mc.change_locked_clarity(10)
            $ the_person.apply_outfit(lingerie_wardrobe.pick_random_outfit())
            the_person "Hmm, how about this..."
            $ the_person.draw_person()
            "She slips on her new set of underwear, then turns back to the camera."
            the_person "Cute, right?"
            "She bounces her shoulders, jiggling her tits."
            the_person "Let's try something else though. Hmmm..."
            $ strip_list = the_person.outfit.get_full_strip_list()
            $ generalised_strip_description(the_person, strip_list)
            if give_clarity:
                $ mc.change_locked_clarity(10)
            the_person "Ooh, this is so pretty!"
            $ the_person.draw_person()
            the_person "Doesn't this look good? I look so hot in this!"
            $ the_person.draw_person(position = "back_peek")
            "[the_person.possessive_title] holds up her arms and spins around, giving the camera a full view of her body."
            if give_clarity:
                $ mc.change_locked_clarity(10)
            "She puts two fingers under her butt and jiggles it, then winks at the camera and turns back to face it."
            $ the_person.draw_person()
            the_person "Plenty more for me to try on, but that's going to have to wait for another day. See you then sweethearts!"
            "She waves goodbye and reaches towards the camera, ending the video."
            $ the_person.apply_outfit()
            $ clear_scene()

        elif the_person.event_triggers_dict.get("onlyfans_content_type", "underwear") == "nudes":
            $ strip_list = the_person.outfit.get_full_strip_list()
            $ the_person.outfit.remove_clothing_list(strip_list)
            $ the_person.draw_person()
            "[the_person.title] smiles at the camera as the video starts. She's standing in her bedroom beside her bed."
            "She doesn't waste any time turning on some music and starting to dance slowly for you."
            $ the_person.draw_person(position = "back_peek", the_animation = ass_bob, animation_effect_strength = 0.5)
            if give_clarity:
                $ mc.change_locked_clarity(30)
            "She turns around and jiggles her butt arms held high above her head."
            "After showing of ass she turns around and runs her hands over her naked body."
            $ the_person.draw_person(the_animation = tit_bob, animation_effect_strength = 0.5)
            if the_person.has_large_tits():
                if give_clarity:
                    $ mc.change_locked_clarity(20)
                "She holds her tits and lifts them up, then lets them drop and jiggle."
                "She could be exaggerating for the camera, but she seems to be having a good time."
            else:
                if give_clarity:
                    $ mc.change_locked_clarity(10)
                "She pinches her nipples and moans happily. Maybe she's exaggerating for the camera, but she looks like she's having a good time."
            if give_clarity:
                $ mc.change_locked_clarity(20)
            "[the_person.possessive_title] dances for another couple of minutes, alternating between playing with her tits and jiggling her ass."
            "When the song ends she smiles at her digital audience and waves goodbye, then the video ends."

            $ the_person.apply_outfit()
            $ clear_scene()

        elif the_person.event_triggers_dict.get("onlyfans_content_type", "underwear") == "dildo":
            # Sucks on a dildo
            $ strip_list = the_person.outfit.get_full_strip_list()
            $ generalised_strip_description(the_person, strip_list)
            $ the_person.draw_person(position = "kneeling1")
            "[the_person.title] smiles at the camera as the video begins. Then she reaches off screen and comes back holding a thick dildo."
            if give_clarity:
                $ mc.change_locked_clarity(20)
            "She doesn't waste any time, licking at the tip of the plastic tip enthusiastically."
            "After wetting the tip she slips it into her mouth and start to work it deeper into her throat."
            $ the_person.draw_person(position = "kneeling1", the_animation = blowjob_bob, animation_effect_strength = 0.5)
            "[the_person.title] looks directly into the camera as she gives a blowjob to her toy."
            if give_clarity:
                $ mc.change_locked_clarity(20)
            "For the next couple of minutes she works over the toy, speeding up and pushing it a little deeper."
            "As a finale she jams the dildo down her throat until she gags, then holds it in place."
            if give_clarity:
                $ mc.change_locked_clarity(30)
            "She maintains eye contact with her digital audience until her eyes are watering and her cheeks are flush, then she pulls it out and pants for breath."
            "The toy trails spit down her chin and chest as she breathes heavily."
            "[the_person.possessive_title] waves goodbye and ends the video with her face and chest still a sloppy mess."

            $ the_person.apply_outfit()
            $ clear_scene()

    return
