# Everything associated with having a DikDok account

init -2 python:
    def dikdok_on_turn(the_person):
        if renpy.random.randint(0,100) < 20 + 5*the_person.get_opinion_score("skimpy outfits") + 5*the_person.get_opinion_score("showing her tits") + 5*the_person.get_opinion_score("showing her ass"):
            the_person.event_triggers_dict["dikdok_generate_vid"] = True

        return

    def dikdok_on_day(the_person):

        return




#TODO: Profile viewing code (Similar to Insta's)
#TODO: Girls generate videos (Similar to Insta's, but animations are added and sluttier options are included.
#TODO: Girls pimp their Onlyfans if it exists.
#NOTE: No comments, no direct messages.


label check_dikdok():
    # TODO: Check if anyone you know has posted pictures on InstaPic
    $ dikdok_list = ["Accounts You Know"]
    python:
        for a_person in mc.phone.get_person_list():
            if a_person.has_role(dikdok_role) and a_person.event_triggers_dict.get("dikdok_known", False): #We may add a flag to have some girls (ie. Lily) hide their profile under a different name.
                dikdok_list.append(a_person)

    $ other_options_list = ["Other Options", "Back"]
    call screen main_choice_display([dikdok_list, other_options_list], draw_hearts_for_people = False)
    $ picked_option = _return
    if isinstance(picked_option, Person):
        call view_dikdok(picked_option) from _call_view_dikdok
    elif picked_option == "Back":
        return
    return

label view_dikdok(the_person):
    if the_person.event_triggers_dict.get("dikdok_generate_vid", False):
        "It looks like [the_person.title] has posted a new video."
        $ rand_num = renpy.random.randint(0,3)
        if the_person.effective_sluttiness() < 10: # Barely does anything of note with her account
            if rand_num == 0:
                "[the_person.possessive_title] just filmed her food. She isn't even in the shot."
            elif rand_num == 1:
                "It's just the view of the sunrise from her front door. Pretty."
            elif rand_num == 2:
                "It's a video of a dog she met today. Cute."
            else:
                "She's a video of a street performer she saw today. Interesting, but [the_person.possessive_title]'s not even in the shot."


        elif the_person.effective_sluttiness() < 20: # Does a few videos with herself in it, generally not looking to be slutty, just "cute"
            if rand_num == 0:
                $ the_person.apply_outfit()
                $ the_person.draw_person()
                the_person "Going out for my morning run, keep that body strong everyone!"
                "The camera swivels around, and the video continues for a few more seconds as she starts to jog."
                $ clear_scene()

            elif rand_num == 1:
                $ the_person.apply_outfit()
                $ the_person.draw_person()
                the_person "This is one of my favourite outfits, maybe this style will work for you too!"
                "She smiles for the camera, and then the video ends."
                $ clear_scene()
            elif rand_num == 2:
                $ the_person.apply_outfit()
                $ the_person.draw_person(position = "sitting")
                "[the_person.possessive_title] is curled up on the couch with a steaming drink and a book on her lap."
                "She blows a kiss to the camera, then the video ends."
                $ clear_scene()
            else:
                $ the_person.apply_outfit()
                $ the_person.draw_person()
                "[the_person.possessive_title] is leaning towards to her bathroom mirror, giving a closeup of her lips."
                the_person "Here are my 3 quick tricks to blowout lips!"
                "She proceeds to detail parts of her morning makeup routine."
                $ clear_scene()
                pass

        elif the_person.effective_sluttiness() < 40: # Starts to get sluttier, starts wearing specific outfits to show off.
            if rand_num == 0:
                $ the_person.apply_outfit()
                $ the_person.outfit.strip_to_underwear(avoid_nudity = True)
                $ the_person.draw_person()
                "[the_person.possessive_title] is standing in front of her bedroom mirror, and showing off her body."
                the_person "Here's a look at a new set I found recently!"
                "She turns around to show off her butt."
                $ the_person.draw_person(position = "back_peek")
                the_person "It's cute, right? Hope you liked it!"
                $ the_person.apply_outfit()
                $ clear_scene()
            elif rand_num == 1:
                $ the_person.apply_outfit(insta_wardrobe.pick_random_outfit()) #TODO: We might want a dedicated athletics wardrobe at some point.
                $ the_person.draw_person(the_animation = tit_bob, animation_effect_strength = 0.5)
                "[the_person.possessive_title] is holding her phone out and filming herself as she jogs down a residental street."
                the_person "Hey crew, I'm keeping fit and focusing on my health. Come on a run with me!"
                if the_person.has_large_tits():
                    "She keeps the camera focused on herself as she runs, her big tits bouncing in and out of frame as she goes."
                else:
                    "She keeps the camera focused on herself as she runs."
                $ the_person.apply_outfit()
                $ clear_scene()
            elif rand_num == 2:
                $ the_person.apply_outfit()
                $ the_person.outfit.strip_to_underwear(avoid_nudity = True)
                $ the_person.draw_person(position = "kneeling1")
                "[the_person.possessive_title] is on her knees, and still propping up her phone when the video starts."
                "Music kicks in, and she spins around to point her ass at you."
                $ the_person.draw_person(position = "doggy", the_animation = ass_bob, animation_effect_strength = 0.4)
                "[the_person.title] starts to twerk to the beat, bouncing her hips to jiggle her ass."
                "As the music picks up she starts to move her hips faster and faster."
                $ the_person.draw_person(position = "doggy", the_animation = ass_bob, animation_effect_strength = 0.6)
                "She keep shaking her butt for her digital audience until the song and the video end."
                $ the_person.apply_outfit()
                $ the_person.clear_scene()
            else:
                $ the_person.apply_outfit(lingerie_wardrobe.pick_random_outfit())
                $ the_person.draw_person(position = "kneeling1")
                the_person "Hey crew, it's me again. Today I'm showing off some lingerie I just bought..."
                if the_person.has_large_tits():
                    $ the_person.draw_person(position = "kneeling1", the_animation = tit_bob, animation_effect_strength = 0.5)
                    "She pinches her arms together and jiggles her tits for the camera."
                    the_person "Well, what do you think? Hmm?"
                    "[the_person.possessive_title] looks down at her own cleavage and smiles."
                else:
                    $ the_person.draw_person(position = "kneeling1", the_animation = tit_bob, animation_effect_strength = 0.5)
                    "She wiggles her shoulders, jiggling her tits around for the camera."
                    the_person "Pretty cute, right?"
                "She shakes her tits for a few more seconds, then reaches towards her phone and the video ends."
                $ the_person.apply_outfit()
                $ clear_scene()

        else: #Very slutty, videos of her pretending to ride someone, suck cock, ect.
            if rand_num == 0: # Short JOI in some lingerie.
                $ the_person.apply_outfit(lingerie_wardrobe.pick_random_outfit())
                $ the_person.draw_person(position = "kneeling1", the_animation = tit_bob, animation_effect_strength = 0.3)
                "[the_person.title] is kneeling in front of her phone, looking directly intothe camera."
                the_person "We all know why you're here, so let's get down to it."
                "She bites her lip sensually and leans forward a little, accentuating her breasts."
                the_person "I want you to take your cock out and stroke it for me. Jerk off that nice big cock for me."
                "She mimes a handjob motion slowly with one hand."
                the_person "It's such a nice dick, I want to feel it in my mouth. Does that sound nice? Keep jerking off."
                "[the_person.possessive_title] licks her lips slowly and pulls teasingly at her underwear."
                the_person "Oh, looks like we're out of time for today. We'll have to finish this up next time. See you around."
                "She bites her lip again as she reaches forward and ends the video."
                $ the_person.apply_outfit()
                $ clear_scene()

            elif rand_num == 1: # Underwear show w/ some nudity ("Ooops!)
                $ the_person.apply_outfit()
                $ the_person.outfit.strip_to_underwear(avoid_nudity = True)
                $ the_person.draw_person()
                the_person "Hey everyone! Here to show off a new set of underwear for all of you today."
                the_person "DikDok is super strict with their censoring, so I need to be really careful not to do this..."
                $ strip_list = the_person.outfit.get_tit_strip_list()
                if the_person.outfit.can_half_off_to_tits():
                    $ strip_list = the_person.outfit.get_half_off_to_tits_list
                    $ generalised_strip_description(the_person, strip_list, half_off_instead = True)
                else:
                    $ generalised_strip_description(the_person, strip_list)
                the_person "Ooops! I guess you'll just have to report me for being so naughty!"
                "She bites her lip and winks at the camera."
                the_person "See you all next time!"
                $ the_person.apply_outfit()
                $ clear_scene()
            elif rand_num == 2: # Blowjob practice
                $ the_person.apply_outfit(lingerie_wardrobe.pick_random_outfit())
                $ the_person.draw_person(position = "kneeling1", the_animation = tit_bob, animation_effect_strength = 0.3)
                "[the_person.title] is on her knees, smiling at the camera as music plays in the background."
                "She reaches off screen and comes back holding a dildo. She looks into the camera again and pouts innocently."
                "After a moment of fake hesitation she opens her mouth and starts to suck on the tip."
                $ the_person.draw_person(position = "kneeling1", the_animation = blowjob_bob, animation_effect_strength = 0.4)
                "[the_person.possessive_title] sucks on the fake dick, working it furthur and furthur into her mouth in time with the music."
                "Soon she's taken it as deep as she can manage. She flutters her eyes and pulls the toy out, letting the wet toy trail spit down between her cleavage."
                "She waves goodbye with a free hand, then reaches towards her phone and ends the video."
                $ the_person.apply_outfit()
                $ clear_scene()
            else: # ON/OFF video
                $ the_person.apply_outfit()
                $ the_person.draw_person()
                "[the_person.title] is dancing for the camera to some upbeat music."
                "After a few seconds of dancing she hops into the air and..."
                $ the_person.outfit.strip_to_underwear()
                if the_person.outfit.tits_visible() or the_person.outfit.vagina_visible():
                    "... is suddenly naked! She pretends to be embarrassed for a second, then shrugs and goes back to dancing for the camera."
                else:
                    "... is suddenly in her underwear! She shrugs her shoulders and keeps dancing for the camera."
                "[the_person.possessive_title]'s dance goes on for a little longer, then she reaches for her phone and the video ends."
                $ the_person.apply_outfit()
                $ clear_scene()

    else:
        "Nothing new."
    return
