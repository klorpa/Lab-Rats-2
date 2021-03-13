# holds all of the crises involving your family.

init 1 python:
    def mom_outfit_help_requirement():
        if mc_at_home() and time_of_day==4 and (day%7==6 or day%7==0 or day%7==1 or day%7==2 or day%7==3): #It has to be a day before a weekday, so she has work in the morning.
            return True
        return False

    mom_outfit_help_crisis = Action("Mom Outfit Help Crisis ",mom_outfit_help_requirement,"mom_outfit_help_crisis_label")
    crisis_list.append([mom_outfit_help_crisis,5])

label mom_outfit_help_crisis_label():
    $ the_person = mom
    # Your mom asks for help planning an outfit for the next day. As a bonus you get to watch her strip down between outfits (peek/don't peek decision given, she doesn't care at high sluttiness)
    if not mc.location.has_person(mom):
        #She's in a different room, shh calls you in.
        the_person "[the_person.mc_title], can you help me with something for a moment?"
        "You hear [the_person.possessive_title] call for you from her bedroom."
        menu:
            "Help [the_person.possessive_title].":
                mc.name "Sure thing, I'll be right there."
                $ mom_bedroom.show_background()
                $ the_person.draw_person()
                "You step into [the_person.possessive_title]. She's standing at the foot of her bed and laying out a few sets of clothing."
                mc.name "Hey Mom, what's up?"

            "Say you're busy.":
                mc.name "Sorry [the_person.title], I'm a little busy at the moment."
                the_person "Okay, I'll ask your sister."
                $ clear_scene()
                return
    else:
        #She's in the room with you right now (how? no clue, but maybe it'll happen one day!)
        $ the_person.draw_person()
        the_person "[the_person.mc_title], could you help me with something for a moment?"
        menu:
            "Help [the_person.possessive_title].":
                mc.name "Sure thing, what's up?"
                "[the_person.possessive_title] goes over to her closet and pulls out a few sets of clothing. She starts to lay them out."

            "Say you're busy.":
                mc.name "Sorry Mom, I should really be getting to bed."
                the_person "That's okay [the_person.mc_title], I'll ask your sister then."
                $ clear_scene()
                return

    the_person "I've got a meeting with an important client tomorrow and I don't know what I should wear."
    the_person "Could you give me your opinion?"
    mc.name "Of course, lets take a look!"
    $ first_outfit = the_person.wardrobe.decide_on_outfit(the_person.sluttiness) # A normal outfit for her, made from her wardrobe.
    $ second_outfit = None # Changes her goals based on how you respond to the first one (ie. she tones it down, makes it sluttier, or keeps it the way it is)
    $ third_outfit = None # She asks you to put something together from her wardrobe. If it's reasonable for her she'll add it to her wardrobe.
    $ caught = False #Did you get cuaght watching her strip

    if the_person.effective_sluttiness(["underwear_nudity","bare_pussy","bare_tits"]) + the_person.love < 30: #She really doesn't want you to see anything
        the_person "Okay, I'll need a moment to get changed."
        mc.name "I can just turn around, if that would be faster."
        the_person "I'll just be a second. Go on, out."
        $ clear_scene()
        "[the_person.possessive_title] shoos you out of her bedroom. You lean against her door and wait."
        the_person "Okay, all done. Come on in!"

    elif the_person.effective_sluttiness(["underwear_nudity","bare_pussy","bare_tits"]) + the_person.love < 50: #She just asks you to turn your back, so you can peek if you want.
        the_person "Okay, I'll need a moment to get changed. Could you just turn around for a second?"
        $ clear_scene()
        "You nod and turn your back to [the_person.possessive_title]. You hear her moving behind you as she starts to get undressed."
        menu:
            "Try and peek.":
                # Chance to get spotted. Otherwise you get to watch as she strips clothing off one item at a time until she is naked.
                $ the_person.draw_person()
                "You shuffle to the side and manage to get a view of [the_person.possessive_title] using a mirror in the room."

                $ strip_choice = the_person.outfit.remove_random_any(top_layer_first = True, do_not_remove = True)
                while strip_choice is not None and not caught:
                    $ the_person.draw_animated_removal(strip_choice)
                    "You watch as [the_person.possessive_title] take off her [strip_choice.display_name]."
                    if renpy.random.randint(0,100) < 10: #you got caught
                        the_person "I'll be done in just a second [the_person.mc_title]..."
                        "Her eyes glance at the mirror you're using to watch her. You try to look away, but your eyes meet."
                        $ the_person.draw_person(emotion = "angry")
                        $ the_person.change_happiness(-5)
                        $ the_person.change_slut_temp(1+the_person.get_opinion_score("not wearing anything"))
                        the_person "[the_person.mc_title], are you watching me change!"
                        mc.name "No, I... The mirror was just sort of there."
                        "She covers herself with her hands and motions for the door."
                        the_person "Could you wait outside, please?"
                        $ clear_scene()
                        "You hurry outside and close the door to [the_person.possessive_title]'s bedroom behind you."
                        the_person "Okay, you can come back in."
                        $ caught = True
                    else:
                        menu:
                            "Keep watching.":
                                $ strip_choice = the_person.outfit.remove_random_any(top_layer_first = True, do_not_remove = True)

                            "Stop peeking.":
                                "You pull your eyes away from the mirror and do your best not to peek."
                                $ clear_scene()
                                $ strip_choice = None

                if not caught:
                    "[the_person.possessive_title] finishes stripping down and starts to get dressed in her new outfit. After a few moments she's all put together again."
                    the_person "Okay [the_person.mc_title], you can turn around now."

            "Wait until she's done.":
                "You twiddle your thumbs until [the_person.possessive_title] is finished changing."
                the_person "Okay, all done. You can turn around now."

    else: #She's slutty enough that she doesn't care if you watch or not.
        the_person "Just give me one second to get dressed [the_person.mc_title]."
        "[the_person.possessive_title] starts to strip down in front of you."
        $ strip_list = the_person.outfit.get_full_strip_list()
        $ generalised_strip_description(the_person, strip_list)

        "Once she's stripped naked she grabs her new outfit and starts to put it on."
        if the_person.update_outfit_taboos(): #Some taboo was broken.
            the_person "I should probably have told you to look away, but you don't mind, right?"
            the_person "It's nothing you haven't seen when you were younger."
            mc.name "I don't mind at all [the_person.title]."
            "She smiles at you and finishes getting dressed again."


    #$ the_person.outfit = first_outfit changed v0.24.1
    $ the_person.apply_outfit(first_outfit, update_taboo = True)
    $ the_person.draw_person()
    the_person "Well, what do you think?"
    "You take a moment to think before responding."
    menu:
        "Say it's too revealing.":
            mc.name "I don't think it's very appropriate for work Mom. Maybe you should try something a little less... revealing."
            $ the_person.change_slut_temp(-2)
            the_person "Maybe you're right. Okay, I'll try something a little more conservative for this next outfit."
            $ second_outfit = the_person.wardrobe.decide_on_outfit(the_person.sluttiness-10, 0) #Note that if we have impossible values for this function it'll keep exanding the threshold until it's possible

        "Say she looks beautiful in it.":
            mc.name "You look beautiful Mom, I think it would be perfect."
            $ the_person.change_happiness(5)
            $ the_person.change_love(1)
            "She smiles and blushes."
            the_person "You aren't just saying that, are you? I want your real opinion"
            mc.name "It's a great look for you."
            the_person "Great! I want to try another outfit before I settle on this one though, if you don't mind."
            $ second_outfit = the_person.wardrobe.decide_on_outfit(the_person.sluttiness, 0)

        "Say it's not revealing enough.":
            mc.name "I don't know Mom, it's a little stuffy, isn't it? Maybe you should pick something that's a little more modern and fun."
            $ the_person.change_slut_temp(1+the_person.get_opinion_score("skimpy uniforms"))
            $ the_person.discover_opinion("skimpy uniforms")
            if the_person.get_opinion_score("skimpy uniforms") >= 0:
                the_person "Do you think so? Maybe it is a little too conservative."
                "She nods and turns towards her closet."
                the_person "Okay, I'll give something else a try then."
            else:
                the_person "Oh no, I hate having to dress in those skimpy little outfits everyone wants their secretary in these days."
                "She sighs and shrugs."
                the_person "Well, if that's what you think I'll give something else a try."
            $ second_outfit = the_person.wardrobe.decide_on_outfit(the_person.sluttiness+10, 10)


    #Strip choices for the second peek section
    if the_person.effective_sluttiness(["underwear_nudity","bare_pussy","bare_tits"]) + the_person.love < 30 or caught: #She really doesn't want you to see anything
        the_person "Okay, I just need to get changed again."
        $ clear_scene()
        "[the_person.possessive_title] shoos you out of the room while she changes into her new outfit."
        the_person "Okay, come in!"

    elif the_person.effective_sluttiness(["underwear_nudity","bare_pussy","bare_tits"]) + the_person.love < 50: #She just asks you to turn your back, so you can peek if you want.
        the_person "I'm going to need to get changed again."
        $ clear_scene()
        "You turn around to give her some privacy."
        menu:
            "Try and peek.":
                # Chance to get spotted. Otherwise you get to watch as she strips clothing off one item at a time until she is naked.
                $ the_person.draw_person()
                "You shuffle to the side and manage to get a view of [the_person.possessive_title] using a mirror in the room."
                $ caught = False
                $ strip_choice = the_person.outfit.remove_random_any(top_layer_first = True, do_not_remove = True)
                while strip_choice is not None and not caught:
                    $ the_person.draw_animated_removal(strip_choice)
                    "You watch as [the_person.possessive_title] take off her [strip_choice.display_name]."
                    if renpy.random.randint(0,100) < 10: #you got caught
                        the_person "I'll be done in just a second [the_person.mc_title]..."
                        "Her eyes glance at the mirror you're using to watch her. You try to look away, but your eyes meet."
                        $ the_person.draw_person(emotion = "angry")
                        $ the_person.change_happiness(-5)
                        $ the_person.change_slut_temp(1+the_person.get_opinion_score("not wearing anything"))
                        the_person "[the_person.mc_title], are you watching me change!"
                        mc.name "No, I... The mirror was just sort of there."
                        "She covers herself with her hands and motions for the door."
                        the_person "Could you wait outside, please?"
                        $ clear_scene()
                        "You hurry outside and close the door to [the_person.possessive_title]'s bedroom behind you."
                        the_person "Okay, you can come back in."
                        $ caught = True
                    else:
                        menu:
                            "Keep watching.":
                                $ strip_choice = the_person.outfit.remove_random_any(top_layer_first = True, do_not_remove = True)

                            "Stop peeking.":
                                "You pull your eyes away from the mirror and do your best not to peek."
                                $ clear_scene()
                                $ strip_choice = None

                if not caught:
                    "[the_person.possessive_title] finishes stripping down and starts to get dressed in her new outfit. After a few moments she's all put together again."
                    the_person "Okay [the_person.mc_title], you can turn around now."

            "Wait until she's done.":
                "You twiddle your thumbs until [the_person.possessive_title] is finished changing."
                the_person "Okay, all done. You can turn around now."

    else: #She's slutty enough that she doesn't care if you watch or not.
        the_person "It'll just take me a second to get changed."
        "[the_person.possessive_title] starts to strip down in front of you."
        $ strip_list = the_person.outfit.get_full_strip_list()
        $ generalised_strip_description(the_person, strip_list)
        "Once she's stripped naked she grabs another outfit and starts to put it on."

    $ the_person.apply_outfit(second_outfit, update_taboo = True)
    $ the_person.draw_person()

    the_person "Alright, there we go! Now, do you think this is better or worse than what I was just wearing?"
    $ the_person.draw_person(position = "back_peek")
    "She gives you a few turns, letting you get a look at the full outfit."
    $ the_person.draw_person()
    menu:
        "Suggest the first outfit.":
            mc.name "I think you looked best in the first outfit, you should wear that."
            "She smiles and nods."
            $ the_person.change_happiness(5)
            the_person "I think you're right, I'll put it away for tomorrow."

        "Suggest the second outfit.":
            mc.name "I think this one suits you better, you should wear it tomorrow."
            "She smiles and nods."
            $ the_person.change_happiness(5)
            the_person "I think you're right, it does look good on me."

        "Suggest your own outfit.":
            mc.name "They both look good, but I think I have another idea for something you could wear..."
            "You go to [the_person.possessive_title]'s closet and start to put together an outfit of your own for her."
            $ clear_scene()
            call outfit_master_manager(slut_limit = the_person.sluttiness + 10, show_underwear = False) from _call_outfit_master_manager_2
            $ third_outfit = _return
            $ the_person.draw_person()

            if third_outfit is None:
                "You try a few different combinations, but you can't come up with anything you think Mom will like."
                mc.name "Sorry Mom, I thought I had an idea but I guess I was wrong."
                the_person "That's fine [the_person.mc_title]. I think I'm going to go with the first one anyway."
                $ the_person.change_happiness(5)

            else:
                "You lay the outfit out for [the_person.possessive_title]. She looks it over and nods."
                the_person "I'll try it on, but I think I like it!"
                if the_person.effective_sluttiness() + the_person.love < 30 or caught: #She really doesn't want you to see anything
                    $ clear_scene()
                    "[the_person.possessive_title] shoos you out of the room while she changes into her new outfit."
                    the_person "Okay, come back!"

                elif the_person.effective_sluttiness(["underwear_nudity","bare_pussy","bare_tits"]) + the_person.love < 50: #She just asks you to turn your back, so you can peek if you want.
                    the_person "I'm just going to get changed one last time, if you could turn around for a second."
                    $ clear_scene()
                    "You turn around to give her some privacy."
                    menu:
                        "Try and peek.":
                            # Chance to get spotted. Otherwise you get to watch as she strips clothing off one item at a time until she is naked.
                            $ the_person.draw_person()
                            "You shuffle to the side and manage to get a view of [the_person.possessive_title] using a mirror in the room."
                            $ caught = False
                            $ strip_choice = the_person.outfit.remove_random_any(top_layer_first = True, do_not_remove = True)
                            while strip_choice is not None and not caught:
                                $ the_person.draw_animated_removal(strip_choice)
                                "You watch as [the_person.possessive_title] take off her [strip_choice.display_name]."
                                if renpy.random.randint(0,100) < 10: #you got caught
                                    the_person "I'll be done in just a second [the_person.mc_title]..."
                                    "Her eyes glance at the mirror you're using to watch her. You try to look away, but your eyes meet."
                                    $ the_person.draw_person(emotion = "angry")
                                    $ the_person.change_happiness(-5)
                                    $ the_person.change_slut_temp(1+the_person.get_opinion_score("not wearing anything"))
                                    the_person "[the_person.mc_title], are you watching me change!"
                                    mc.name "No, I... The mirror was just sort of there."
                                    "She covers herself with her hands and motions for the door."
                                    the_person "Could you wait outside, please?"
                                    $ clear_scene()
                                    "You hurry outside and close the door to [the_person.possessive_title]'s bedroom behind you."
                                    the_person "Okay, you can come back in."
                                    $ caught = True
                                else:
                                    menu:
                                        "Keep watching.":
                                            $ strip_choice = the_person.outfit.remove_random_any(top_layer_first = True, do_not_remove = True)

                                        "Stop peeking.":
                                            "You pull your eyes away from the mirror and do your best not to peek."
                                            $ clear_scene()
                                            $ strip_choice = None

                            if not caught:
                                "[the_person.possessive_title] finishes stripping down and starts to get dressed in her new outfit. After a few moments she's all put together again."
                                the_person "Okay [the_person.mc_title], you can look."

                        "Wait until she's done.":
                            "You twiddle your thumbs until [the_person.possessive_title] is finished changing."
                            the_person "Okay, all done. You can look."

                else: #She's slutty enough that she doesn't care if you watch or not.
                    the_person "It'll just take a moment for me to slip into this."
                    "[the_person.possessive_title] starts to strip down in front of you."
                    $ strip_list = the_person.outfit.get_full_strip_list()
                    $ generalised_strip_description(the_person, strip_list)
                    "Once she's stripped naked she grabs another outfit and starts to put it on."

                $ the_person.apply_outfit(third_outfit, update_taboo = True)
                #$ the_person.outfit = third_outfit changed v0.24.1
                $ the_person.draw_person()
                $ the_person.change_happiness(5)
                $ the_person.change_obedience(5)
                $ the_person.change_love(1)
                the_person "I think you have great fashion sense [the_person.mc_title]! It's settled, I'll wear this tomorrow!"
                $ the_person.add_outfit(third_outfit,"full")

    the_person "Thank you so much for the help [the_person.mc_title]. I don't know why but I've been feeling much more unsure about the way I dress lately."
    mc.name "Any time, I'm just glad to help."
    "You leave [the_person.possessive_title] in her room as she starts to pack her clothes away."

    $ clear_scene()
    return

init 1 python:
    def mom_lingerie_surprise_requirement():
        if mc_at_home() and time_of_day==4 and not mc.location.has_person(mom): #Make sure we aren't already in the same room because we were sleeping together.
            if mom.effective_sluttiness("underwear_nudity") > 40 and mom.love > 40:
                return True
        return False

    mom_lingerie_surprise_crisis = Action("Mom Lingerie Surprise Crisis", mom_lingerie_surprise_requirement, "mom_lingerie_surprise_label")
    crisis_list.append([mom_lingerie_surprise_crisis,3])

label mom_lingerie_surprise_label():
    #In which your Mom comes to your room at night in some sexy lingerie and fools around with you. Triggers at high sluttiness and love.
    $ the_person = mom
    "You are woken up in the middle of the night by the sound of your bedroom door closing."
    "You sit up and turn on the lamp beside your bed."
    $ the_person.apply_outfit(lingerie_wardrobe.pick_random_outfit(), update_taboo = True)
    $ the_person.draw_person(position = "stand4")
    the_person "I'm sorry to wake you up [the_person.mc_title], but I wanted to ask you something."
    "[the_person.possessive_title] is standing by the door, wearing some very revealing lingerie. She walks over to your bed and sits down beside you."
    $ the_person.draw_person(position = "sitting")
    mc.name "What did you want to ask?"
    the_person "I know you've been busy with work, and I'm very pround, but sometimes I worry you're not having your needs met."
    "She places a hand on your arm and slides it up to your chest, caressing you with her soft fingers."
    the_person "Your physical needs, I mean. I know I'm your mother, but I thought I could dress up and you could pretend I was someone else. Someone not related to you."
    menu:
        "Ask for her help. (tooltip)Ask your mother to help satisfy your phsyical desires.":
            mc.name "That would be amazing Mom, I could really use your help."
            $ the_person.change_slut_temp(2)
            "[the_person.possessive_title] smiles and bounces slightly on your bed."
            if the_person.effective_sluttiness() < 50:
                the_person "Excellent! Now you just pretend that I'm... your highschool sweetheart, and that we aren't related. Okay?"

            elif the_person.effective_sluttiness() < 80:
                the_person "Excellent! Don't think of me as your mother, just think of me as a sexy mom from down the street. I'm a real milf, okay?"

            else:
                the_person "Excellent! Now don't think of me as your mom, just think of me as your private, slutty milf. I'll do wahtever your cock wants me to do, okay?"
            "You nod and she slides closer to you on the bed."

            $ the_person.add_situational_obedience("crisis_stuff", 25, "I'm doing it for my family.")
            call fuck_person(the_person) from _call_fuck_person_14
            $ the_report = _return
            if the_report.get("girl orgasms", 0):
                "[the_person.possessive_title] needs a few minutes to lie down when you're finished. Bit by bit her breathing slows down."
                $ the_person.change_love(5)
                the_person "Oh [the_person.mc_title], that was magical. I've never felt so close to you before..."

            else:
                "When you're finished [the_person.possessive_title] gives you a kiss on your forehead and stands up to leave."
                $ the_person.change_love(3)
                $ the_person.draw_person(position = "back_peek")
                the_person "Sweet dreams."

            $ the_person.clear_situational_obedience("crisis_stuff")

        "Not tonight.":
            mc.name "That's very sweet of you Mom, and you look very nice, but I really just need a good nights sleep."
            "You see a split second of disappointment on [the_person.possessive_title]'s face, then it's gone and she blushes and turns away."
            the_person "Of course, I'm so sorry to have bothered you. I mean, it would be strange if we did anything like that, right?"
            $ the_person.draw_person(position = "walking_away")
            "She stands up and leaves your room. You're asleep within minutes."

    $ clear_scene()
    return

init 1 python:
    def mom_selfie_requirement():
        if not mc_at_home() and not (time_of_day == 0 or time_of_day == 4): #She always sents you text while you're not at home for the middle part of the day
            if not mc.location.has_person(mom): #Obviously don't do it if she's right there with you.
                if mom.love >= 15:
                    return True
        return False

    mom_selfie_crisis = Action("Mom Selfie Crisis", mom_selfie_requirement, "mom_selfie_label")
    crisis_list.append([mom_selfie_crisis,7])

label mom_selfie_label():
    #TODO: have a way of saving and reviewing selfies in the future.
    #TODO: Have a proper weekday/weekend schedule for people and use that to determine when Mom is at home, at work, or out on the town.
    $ the_person = mom
    $ mc.start_text_convo(the_person)
    $ lowest_stat = mom.sluttiness
    if the_person.love < lowest_stat:
        $ lowest_stat = mom.love

    "While you're going about your day you get a text from your mother."
    if lowest_stat >= 100:
        #Both love and sluttiness are very high, she sends you super slutty selfies and says she can't wait till you come home, fuck her, and make her your woman.
        $ ran_num = renpy.random.randint(0,2) #Used to determine which varient we use to avoid spamming the player with the exact same texts.
        if ran_num == 0:
            if mc.business.is_weekend():
                $ the_person.apply_outfit(lingerie_wardrobe.pick_random_outfit(), update_taboo = True)
                $ the_person.draw_person(position = "missionary", emotion = "happy")
                "Her first message is a selfie of herself lying down on your bed in lingerie."
                the_person "I can't wait until you come home and make love to me. I wish I could spend every minute of every day worshiping your cock like a good mother should."
            else:
                the_person "It's so hard not to talk about you at work. The other women are gossiping and I just want to tell them how good it feels when you try and breed me..."
                the_person "My pussy full of your warm cum, knowing that I can take care of you the way only a mother could."
                the_person "I think I'm going to go touch myself in the bathroom. I hope you are having a great day too [the_person.mc_title]!"

        elif ran_num == 1:
            python:
                for i in range(3):
                    the_person.outfit.remove_random_upper(top_layer_first = True)
                    the_person.outfit.remove_random_lower(top_layer_first = True)
            the_person "Hi [the_person.mc_title], I hope I'm not interrupting your busy work day. This is just a quick reminder..."
            $ the_person.draw_person(emotion = "happy")
            $ the_person.update_outfit_taboos()
            "You get a selfie from [the_person.possessive_title] naked in front of her bedroom mirror."
            the_person "...that your Mom wants to feel you inside her tonight. Don't stay out too late!"

        elif ran_num == 2:
            #Blowjob pose, she tells you to face fuck her, as is her duty
            $ the_person.draw_person(position = "blowjob", emotion = "happy", special_modifier = "blowjob")
            "You get a selfie from [the_person.possessive_title]. She's on her knees, mouth open wide."
            the_person "My mouth is yours to use however you want [the_person.mc_title]."
            the_person "It's my duty to take care of you, so grab and use it whenever you want."

    elif lowest_stat >= 80:
        #Both are high. Sends you slutty selfies and talks about how she wants to fuck you. Sends them from work, etc.
        $ ran_num = renpy.random.randint(0,1) #Used to determine which varient we use to avoid spamming the player with the exact same texts.
        if ran_num == 0:
            if mc.business.is_weekend():
                the_person "I'm here at home and wishing it was you could help me take these pictures..."
                python:
                    for i in range(3):
                        the_person.outfit.remove_random_upper(top_layer_first = True)
                        the_person.outfit.remove_random_lower(top_layer_first = True)
                $ the_person.draw_person(position = "standing_doggy")
                "[the_person.possessive_title] sends you a selfie her bedroom naked and bent over her bed."
            else:
                the_person "I'm stuck here at work and all I can think about is you. Wish you were here..."
                python:
                    for i in range(3):
                        the_person.outfit.remove_random_upper(top_layer_first = True)
                        the_person.outfit.remove_random_lower(top_layer_first = True)
                $ the_person.draw_person(position = "standing_doggy")
                "[the_person.possessive_title] sends you a selfie of herself in the office bathroom, naked and bending over the sink."
            $ the_person.update_outfit_taboos()

        elif ran_num == 1:
            if mc.business.is_weekend():
                the_person "I know it shouldn't, but thinking about you gets me so wet. You've made me a new woman [the_person.mc_title]."
            else:
                the_person "I'm at work and stuck at my desk but I can't get you out of my head. I'm so wet, I wonder if anyone would notice if I touched myself..."

    elif lowest_stat >= 60:
        #Sends you nudes and talks about how she'll help you blow off steam later.
        $ ran_num = renpy.random.randint(0,3) #Used to determine which varient we use to avoid spamming the player with the exact same texts.
        if ran_num == 0:
            if mc.business.is_weekend():
                the_person "I was just about to get in the shower and I thought you might like a peek. Love you [the_person.mc_title]!"
                python:
                    for i in range(3):
                        the_person.outfit.remove_random_upper(top_layer_first = True)
                        if the_person.outfit.panties_covered(): #If we get down to her panties keep them on, because that's sexier.
                            the_person.outfit.remove_random_lower(top_layer_first = True)
                $ the_person.draw_person(emotion = "happy")
                "[the_person.possessive_title] sends you a picture of herself stripped down in front of her bedroom mirror."

            else:
                the_person "I thought you might be stressed so I snuck away from work to take this for you."
                python:
                    for i in range(3):
                        the_person.outfit.remove_random_upper(top_layer_first = True)
                        if the_person.outfit.panties_covered():
                            the_person.outfit.remove_random_lower(top_layer_first = True)
                $ the_person.draw_person(emotion = "happy")
                "[the_person.possessive_title] sends you a picture of herself stripped down in the office bathroom."
                the_person "I've got to get back to work. I hope nobody noticed me gone!"

            $ the_person.update_outfit_taboos()

        elif ran_num == 1:
            the_person "I thought you might enjoy this ;)"
            python:
                for i in range(3):
                    the_person.outfit.remove_random_upper(top_layer_first = True)
                    the_person.outfit.remove_random_lower(top_layer_first = True)
            $ the_person.draw_person(emotion = "happy")
            "Mom sends you a picture of herself stripped naked in front of her bathroom mirror."
            $ the_person.update_outfit_taboos()
        elif ran_num == 2:
            the_person "I've been trying on underwear all day. Would you like a peek?"

            "[the_person.possessive_title] doesn't wait for a reply and starts sending selfies."
            python:
                for i in range(3):
                    the_person.apply_outfit(the_person.wardrobe.get_random_appropriate_underwear(the_person.sluttiness, guarantee_output = True), update_taboo = True)
                    the_person.draw_person(emotion = "happy")
                    renpy.say("","")
            the_person "I hope you think your mommy looks sexy in her underwear ;)"

        elif ran_num == 3:
            python:
                while not the_person.outfit.tits_visible():
                    the_person.outfit.remove_random_upper(top_layer_first = True)

            if mc.business.is_weekend():
                the_person "I'm so glad it's the weekend, I can finally let these girls out..."
                $ the_person.draw_person(emotion = "happy")
                "She sends you a selfie fron the kitchen with her top off."
                the_person "I hope your day is going well, love you!"

            else:
                the_person "I think I'd be much more popular here at work if I was allowed to dress like this..."
                $ the_person.draw_person(emotion = "happy")
                "She sends you a selfie from her office bathroom with her top off."
                the_person "Oh well, at least I know you appreciate it. I need to get back to work, see you at dinner!"
            $ the_person.update_outfit_taboos()

    elif lowest_stat >= 40:
        #Sends you teasing pictures (ie. no shirt or something) and talks about how much she loves you.
        $ ran_num = renpy.random.randint(0,2) #Used to determine which varient we use to avoid spamming the player with the exact same texts.
        if ran_num == 0:
            the_person "You're such a hard worker [the_person.mc_title]. Here's a little gift from the woman who loves you most in the world!"
            $ the_person.outfit.remove_random_upper(top_layer_first = True)
            $ the_person.draw_person(emotion = "happy")
            if mc.business.is_weekend():
                "[the_person.possessive_title] sends you a selfie without her shirt on. The background looks like her bedroom."
            else:
                "[the_person.possessive_title] sends you a sends you a selfie without her shirt on. It looks like it was taken in the bathroom of her office."
            $ the_person.update_outfit_taboos()

        elif ran_num == 1:
            if mc.business.is_weekend():
                the_person "I wish you were here spending time with me. Maybe this will convince you your mom is a cool person to hang out with!"
                $ the_person.outfit.remove_random_upper(top_layer_first = True)
                $ the_person.draw_person(emotion = "happy")
                "Mom sends you a selfie from her bedroom without her shirt on."

            else:
                the_person "I'm busy here at work but I really wish I could be spending time with you instead. Do you think I'm pretty enough to spend time with ;)"
                $ the_person.outfit.remove_random_upper(top_layer_first = True)
                $ the_person.draw_person(emotion = "happy")
                "Mom sends you a selfie without her shirt on. It looks like she's taken in the bathroom of her office."
            $ the_person.update_outfit_taboos()

        elif ran_num == 2:
            $ the_clothing = the_person.outfit.remove_random_upper(top_layer_first = True, do_not_remove = True)
            if the_clothing:
                $ the_clothing.colour[3] = the_clothing.colour[3]*0.9 #It's translucent.
                the_person "It looks like my [the_clothing.name] didn't like being in the wash, it's gone all see-through."
                $ the_person.draw_person(emotion = "happy")
                if the_clothing.underwear:
                    "You get a selfie from [the_person.possessive_title] wearing a slightly transparent bra."
                    if the_person.has_taboo("underwear_nudity"):
                        the_person "Oops, I probably shouldn't be sending pictures like this to my son!"
                        the_person "Oh well, it's not like I'm naked. You better not show it to your friends!"
                        $ the_person.break_taboo("underwear_nudity")
                else:
                    "You get a selfie from [the_person.possessive_title] wearing a slightly transparent top."
                the_person "Oh well, I can still wear it when I'm doing chores around the house. Hope your day is going better, love you!"
            else:
                the_person "I've looked everywhere, but I just can't find my favourite bra!"
                $ the_person.draw_person(emotion = "default", the_animation = blowjob_bob, animation_effect_strength = 0.8)
                "[the_person.possessive_title] sends you a short video of herself walking around your home. Her bare tits bounce with each step."
                the_person "You don't happen to know where it is, do you? I'm wandering around looking for it and it's getting chilly!"
                if the_person.has_taboo("bare_tits"):
                    the_person "Oops! I hope nobody saw you looking at that, I wasn't thinking about my breasts being out."
                    the_person "I don't mind you seeing them though, just don't go sharing that video with your friends!"
                    $ the_person.break_taboo("bare_tits")

    elif lowest_stat >= 20:
        #Sends you normal texts but talks about wanting to get away to talk to you instead
        $ ran_num = renpy.random.randint(0,4) #Used to determine which varient we use to avoid spamming the player with the exact same texts.
        if ran_num == 0:
            the_person "I hope I'm not interrupting, I just wanted to say hi and check in. I'm stuck here at work but wish I could spend more time with you."
            the_person "Have a great day, see you later tonight. Love, Mom."

        elif ran_num == 1:
            the_person "I hope you are having a great day [the_person.mc_title]! Imagining you out there working so hard makes me prouder than you can imagine!"
            the_person "I'm looking forward to seeing you at home tonight. Love, Mom."

        elif ran_num == 2:
            the_person "I hope you aren't busy, I was thinking about you and just wanted to say hi!"
            $ the_person.draw_person(emotion = "happy")
            if mc.business.is_weekend():
                "[the_person.possessive_title] sends you a selfie she took in the living room of your house."
            else:
                "[the_person.possessive_title] sends you a selfie she took from her office at work."
        elif ran_num == 3:
            the_person "Kids these days are always sending selfies to each other, right? I hope I'm doing this right!"
            $ the_person.draw_person(emotion = "happy")
            if mc.business.is_weekend():
                "[the_person.possessive_title] sends you a selfie she took in the living room of your house."
            else:
                "[the_person.possessive_title] sends you a selfie she took from her office at work."
        elif ran_num == 4:
            the_person "All your hard work has inspired me [the_person.mc_title], I'm going out for a walk to stay in shape!"
            $ the_person.draw_person(emotion = "happy", the_animation = blowjob_bob, animation_effect_strength = 0.8)
            "[the_person.possessive_title] sends you a short video she took of herself outside. She's keeping up a brisk walk and seems slightly out of breath."
            if not the_person.outfit.wearing_bra() and the_person.has_large_tits():
                "She doesn't seem to realise, but it's very obvious [the_person.possessive_title] isn't wearing a bra under her top."
                "Her sizeable breasts heave up and down with each step."

    else:
        #Sends you normal motherly texts.
        $ ran_num = renpy.random.randint(0,2) #Used to determine which varient we use to avoid spamming the player with the exact same texts.
        if ran_num == 0:
            the_person "I hope I'm not interrupting your busy day [the_person.mc_title]. I just wanted to let you know that I'm proud of you and you're doing great work."
            the_person "Keep it up! Dinner will be at the normal time."

        elif ran_num == 1:
            the_person "Remember that your mother loves you no matter what! Have a great day!"

        elif ran_num == 2:
            the_person "Hi [the_person.mc_title], I'm just checking in to make sure you're doing okay. I hope you don't mind your "

    "It's so sweet of her to think of you."
    $ mc.end_text_convo()
    $ the_person.apply_outfit(the_person.planned_outfit)
    $ clear_scene()
    return

init 1 python:
    def mom_morning_surprise_requirement():
        if mc_at_home() and time_of_day==0 and mc.business.is_work_day(): #It is the end of the day.
            if mom.love >= 45:
                return True
        return False

    mom_morning_surprise_crisis = Action("Mom Morning Surprise", mom_morning_surprise_requirement, "mom_morning_surprise_label")
    morning_crisis_list.append([mom_morning_surprise_crisis, 5])

label mom_morning_surprise_label():
    $ the_person = mom
    if the_person.effective_sluttiness() < 50:
        the_person "[the_person.mc_title], it's time to wake up."
        "You're woken up by the gentle voice of your mother. You struggle to open your eyes and find her sitting on the edge of your bed."
        $ the_person.draw_person(position="sitting")
        mc.name "Uh... Huh?"
        the_person "You're normally up by now, but I didn't hear an alarm and I was worried you were going to be late."
        "You roll over and check your phone. It looks like you forgot to set an alarm and you've overslept."
        mc.name "Thanks Mom, you really saved me here."
        $ the_person.change_happiness(3)
        "She smiles and stands up."
        $ the_person.draw_person()
        the_person "There's some breakfast in the kitchen, make sure to grab some before you go flying out the door."
        "You sit up on the side of the bed and stretch, letting out a long yawn."
        if the_person.effective_sluttiness() < 20:
            the_person "Oh... I should... Uh..."
            "[the_person.possessive_title] blushes and turns around suddenly. It takes you a moment to realise why: your morning wood pitching an impressive tent with your underwear."
            mc.name "Sorry Mom, I didn't..."
            the_person "No, it's perfectly natural. I'll give you some privacy."
            $ the_person.change_slut_temp(2)
            "She takes one last glance at you then hurries from the room."
            $ clear_scene()
            "You get up and ready, hurrying a little to make up for lost time."
        else:
            the_person "Oh, and you might want to take care of that before you go out [the_person.mc_title]."
            "She nods towards your crotch and you realise you're pitching an impressive tent."
            mc.name "Oh, sorry about that."
            the_person "No, it's perfectly natural and nothing to be embarrassed about."
            $ the_person.change_slut_temp(3)
            "She stares at it for a short moment before pulling her eyes back up to meet yours."
            the_person "Certainly nothing to be embarrassed, but I think you should take care of it before you leave."
            "[the_person.possessive_title] turns around and starts rifling through your closet."
            $ the_person.draw_person(position = "walking_away")
            the_person "I'll find you a nice outfit to wear to save you some time. Go ahead [the_person.mc_title], pretend I'm not even here. It's nothing I haven't seen before."
            menu:
                "Masturbate.":
                    "You pull your underwear down, grab your hard cock, and start to stroke it."
                    mc.name "Thanks Mom, you're really helping me out this morning."
                    the_person "Anything to help you succeed."
                    $ the_person.draw_person(position = "back_peek")
                    "She wiggles her butt, then turns her attention back to putting together an outfit for you."
                    "You keep jerking yourself off, pulling yourself closer and closer to orgasm."
                    "You're getting close when [the_person.possessive_title] turns around and walks back towards your bed with a handful of clothes."
                    the_person "I think you'll look really cute in this. Are you almost done [the_person.mc_title]?"
                    menu:
                        "Order her to get on her knees." if the_person.obedience >= 130:
                            mc.name "I'm so close. Get on your knees Mom."
                            the_person "If... if that's what you need to finish."
                            $ the_person.draw_person(position = "blowjob")
                            menu:
                                "Order her to open her mouth." if the_person.obedience >= 140:
                                    mc.name "Open your mouth Mom."
                                    the_person "[the_person.mc_title], I don't think..."
                                    mc.name "I'm so close Mom, open your mouth!"
                                    "She hesitates for a split second, then closes her eyes and opens her mouth."
                                    $ the_person.draw_person(position = "blowjob", special_modifier = "blowjob")
                                    "Seeing [the_person.possessive_title] presenting herself for you pushes you past the point of no return."
                                    $ the_person.cum_in_mouth()
                                    $ the_person.draw_person(position = "blowjob", special_modifier = "blowjob")
                                    "You slide forward a little, place the tip of your cock on her bottom lip, and start to fire your load into her mouth."
                                    "[the_person.possessive_title] stays perfectly still while you cum. When you're done you sit back and sigh."
                                    "[the_person.title] turns away and spits your cum out into her hand. She takes a long while to say anything."
                                    the_person "I don't... That wasn't what we should do [the_person.mc_title]."
                                    mc.name "You were just being a loving mother and doing what I asked. That was amazing."
                                    $ the_person.change_obedience(5)
                                    $ the_person.change_slut_temp(5)
                                    "I... I don't know. Just don't tell anyone, okay?"
                                    mc.name "Of course, I promise Mom."
                                    $ the_person.draw_person()
                                    "She stands up and heads for the door."
                                    the_person "Well hurry up at least and get dressed, I don't want you to be late after all that!"

                                "Order her to open her mouth.\nRequires: 140 Obedience (disabled)" if the_person.obedience < 140:
                                    pass

                                "Order her to hold up her tits." if the_person.has_large_tits():
                                    mc.name "Hold up your tits, I'm going to cum!"
                                    "[the_person.possessive_title] mumbles something but does as she's told. She cups her large breasts in her hands and presents them in front of you."
                                    "You grunt and climax, firing your load out and right onto [the_person.possessive_title]'s chest."
                                    $ the_person.cum_on_tits()
                                    #TODO: have more clothing aware stuff here
                                    the_person "I... Oh [the_person.mc_title], I don't think I should have let you do that."
                                    $ the_person.draw_person()
                                    mc.name "It's okay Mom, you were just being a loving mother and doing what I asked."
                                    $ the_person.change_obedience(3)
                                    $ the_person.change_slut_temp(5)
                                    the_person "Maybe you're right... Now hurry up and get dressed before you're late!"
                                    # TODO: She should seem a little shocked, but otherwise okay with how things turned out

                        "Order her to get on her kness.\nRequires: 130 Obedience (disabled)" if the_person.obedience < 130:
                            pass

                        "Climax.":
                            "Knowing that [the_person.possessive_title] is just a step away watching you stroke your cock and waiting for you to cum pushes you over the edge."
                            "You grunt and climax, firing your load out in an arc. [the_person.title] gasps softly and watches it fly, looks away."
                            the_person "Well done. I'll make sure to clean that up while you're out today."
                            "She leans over and kisses you on the forehead."
                            the_person "Now get dressed or you'll be late for work."
                            $ clear_scene()
                            "[the_person.possessive_title] leaves and you get dressed as quickly as you can manage."

                "Ask her to leave.":
                    mc.name "I think it will take care of itself Mom. Thanks for hte offer but I can pick out my own outfit."
                    the_person "Oh, okay [the_person.mc_title]. Just make sure don't give any of those nice girls you work with a shock when you walk in."
                    $ the_person.draw_person()
                    "She turns back to you and gives you a hug and a kiss. Her eyes continue to linger on your crotch."
                    $ clear_scene()
                    "When she leaves you get dressed as quickly as you can, rushing to make up for lost time."


    elif the_person.effective_sluttiness("touching_penis") < 50:
        "You're slowly awoken by a strange, pleasant sensation. When you open your eyes it takes a moment to realise you aren't still dreaming."
        $ the_person.draw_person(position = "blowjob") #TODO: We need a handjob pose.
        "[the_person.possessive_title] is sitting on the side of your bed. The covers have been pulled down and she has your morning wood in her hand. She strokes it slowly as she speaks."
        if the_person.has_taboo("touching_penis"):
            the_person "Good morning, don't be embarrassed. I saw your... morning wood, and wanted to help you take care of it."
            "She looks away, blushing intensely."
            the_person "If you want me to stop, just tell me. We never need to talk about this again, okay!"
            the_person "Actually, I should just go. This is a mistake. What am I doing?"
            "[the_person.possessive_title] starts to stand up, but you grab her wrist and pull her back. You guide her hand back to your cock."
            mc.name "It's okay [the_person.title], I was liking it. This is a really nice suprise."
            "She nods happily and speeds up her strokes, settling back down on the bed beside you."
            $ the_person.break_taboo("touching_penis")
        else:
            the_person "Good morning [the_person.mc_title]. You forgot to set an alarm and overslept. I came in to wake you up and saw this..."
            "She speeds up her strokes."
        the_person "I thought that this would be a much nicer way to wake up, and I can't let you leave the house in this condition."
        mc.name "Right, of course. Thanks Mom."
        "You lie back, relax, and enjoy the feeling of your mothers hand caressing your hard shaft."
        the_person "Anything for you [the_person.mc_title], I just want to make sure you're happy and successful."
        "After a few minutes you can feel your orgasm starting to build. Mom rubs your precum over your shaft and keeps stroking."
        menu:
            "Order her to take your cum in her mouth." if the_person.obedience >= 130:
                mc.name "I'm almost there Mom, I need to cum in your mouth."
                $ the_person.change_obedience(5)
                "She nods and leans over, stroking your cock faster and faster as she places the tip just inside her mouth."
                "The soft touch of her lips pushes you over the edge. You gasp and climax, shooting your hot load into [the_person.possessive_title]'s waiting mouth."
                $ the_person.cum_in_mouth()
                "[the_person.title] pulls back off your cock slowly. She spits your cum out into her hand and straightens up."

            "Order her to take your cum in her mouth.\nRequires: 130 Obedience (disabled)" if the_person.obedience<130:
                pass

            "Climax":
                mc.name "I'm almost there Mom, keep going!"
                "She nods and strokes your dick as fast as she can manage, pusing you over the edge."
                "You grunt and fire your hot load into up into the air. It falls back down onto your stomach and [the_person.possessive_title]'s hand."
                "Mom strokes you slowly for a few seconds, then lets go and places her hand on her lap while you take a second to recover."

        the_person "Whew, that was a lot. I hope that leaves you feeling relaxed for the rest of the day."
        "She leans forward and kisses you on the forehead."
        mc.name "Thanks Mom, you're the best."
        $ the_person.change_love(2)
        $ the_person.change_slut_temp(5)
        $ the_person.change_happiness(5)
        $ the_person.draw_person(position = "back_peek")
        "She smiles and gets up. She pauses before she leaves your room."
        the_person "You better get ready now or you're going to be late!"


    elif the_person.effective_sluttiness("sucking_cock") < 70:
        #TODO: image a lying down blowjob pose
        "You're slowly awoken by a strange, pleasant sensation. When you open your eyes it takes a moment to realise you aren't still dreaming."
        $ the_person.draw_person(position = "blowjob")
        "[the_person.possessive_title] is lying face down between your legs, gently sucking off your morning wood."
        "She notices you waking up and pulls off of your cock to speak."
        if the_person.has_taboo("sucking_cock"):
            the_person "Don't panic [the_person.mc_title]! I came in because your alarm hadn't gone off and saw this..."
            "She wiggles your dick with her hand."
            the_person "I couldn't stop myself... I mean, I couldn't imagine you having to rush out of the door with this!"
            the_person "I'll stop if you want me too. You probably think I'm crazy!"
            mc.name "I don't think your crazy, I think you are incredibly thoughtful. This feels amazing."
            $ the_person.break_taboo("sucking_cock")
        else:
            the_person "Good morning [the_person.mc_title]. I noticed your alarm hadn't gone off and came in to wake you up..."
            "She licks your shaft absentmindedly."
            the_person "And saw this. I thought this would be a much nicer way of waking you up."
            mc.name "That feels great Mom."
            $ the_person.change_happiness(5)
        "She smiles up at you, then lifts her head and slides your hard dick back into her mouth."
        "You lie back and enjoy the feeling of [the_person.possessive_title] sucking you off."
        $ the_person.draw_person(position = "blowjob", special_modifier = "blowjob")
        "For several minutes the room is quiet save for a soft slurping sound each time [the_person.title] slides herself down your shaft."
        "You rest a hand on the back of her head as you feel your orgasm start to build, encouraging her to go faster and deeper."
        mc.name "I'm almost there Mom, keep going!"
        "She mumbles out an unintelligible response and keeps sucking your cock."
        "You arch your back and grunt as you climax, firing a shot of cum into [the_person.possessive_title]'s mouth."
        $ the_person.cum_in_mouth()
        $ the_person.draw_person(position = "blowjob")
        "She pulls back until the tip of your cock is just inside her lips and holds there, collecting each new spurt of semem until you're completely spent."
        "When you're done she pulls up and off, keeping her lips tight to avoid spilling any onto you."
        menu:
            "Order her to swallow." if the_person.obedience >= 130:
                mc.name "That was great [the_person.title], now I want you to swallow."
                "She looks at you and hesitates for a split second, then you see her throat bob as she sucks down your cum."
                $ the_person.change_obedience(5)
                "[the_person.possessive_title] takes a second gulp to make sure it's all gone, then opens her mouth and takes a deep breath."


            "Order her to swallow.\nRequires: 130 Obedience (disabled)" if the_person.obedience < 130:
                pass

            "Let her spit it out.":
                $ the_person.draw_person(position = "sitting")
                "You watch as she slides her legs off the side of your bed, holds out a hand, and spits your cum out into it."

        the_person "Whew, I'm glad I was able to help with that [the_person.mc_title]. That was a lot more than I was expecting."
        mc.name "Thanks [the_person.title], you're the best."
        $ the_person.change_love(2)
        $ the_person.change_slut_temp(5)
        "She smiles and leans over to give you a kiss on the forehead."
        the_person "My pleasure, now you should be getting up or you'll be late for work!"
        $ clear_scene()
        "[the_person.possessive_title] gets up and leaves you alone to get dressed and ready for the day. You rush a little to make up for lost time."

    else:
        # First we need to take her and remove enough clothing that we can get to her vagina, otherwise none of this stuff makes sense.
        # We do that by getting her lowest level pieces of bottom clothing and removing it, then working our way up until we can use her vagina.
        # This makes sure skirts are kept on (because this is suppose to be a quicky).
        $ bottom_list = the_person.outfit.get_lower_ordered()
        $ removed_something = False
        $ the_index = 0
        while not the_person.outfit.vagina_available() and the_index < __builtin__.len(bottom_list):
            $ the_person.outfit.remove_clothing(bottom_list[the_index])
            $ removed_something = True
            $ the_index += 1
        "You're woken up by your bed shifting under you and a sudden weight around your waist."
        $ the_person.draw_person(position = "cowgirl", emotion = "happy")
        "[the_person.possessive_title] has pulled down your sheets and underwear and is straddling you. The tip of your morning wood is brushing against her pussy."
        the_person "Good morning [the_person.mc_title]. I didn't hear your alarm go off and when I came to check on you I noticed this..."
        "She grinds her hips back and forth, rubbing your shaft along the lips of her cunt."
        the_person "Would you like me to take care of this for you?"
        menu:
            "Let [the_person.title] fuck you.":
                mc.name "That would be great Mom."
                $ the_person.change_happiness(5)
                $ the_person.change_love(2)
                "You lie back relax as [the_person.possessive_title] lowers herself down onto your hard cock."
                call fuck_person(the_person, start_position = cowgirl, start_object = bedroom.get_object_with_name("bed"), skip_intro = True, girl_in_charge = True,position_locked=True,self_strip=False) from _call_fuck_person_15
                $ the_report = _return
                if the_report.get("girl orgasms", 0) > 0:
                    $ the_person.change_love(5)
                    the_person "That was amazing [the_person.mc_title], you know how to make me feel like women again!"
                    "She rolls over and kisses you, then rests her head on your chest."
                    "After a minute she sighs and starts to get up."
                    the_person "I shouldn't be keeping you from your work, I don't want to make you any more late!"
                    "She reaches down to help you up. She smiles at you longingly, eyes lingering on your crotch, and leaves you alone in your room."
                else:
                    the_person "I'm glad I could help [the_person.mc_title]. Now you should hurry up before you're late!"
                    "[the_person.possessive_title] kisses you on the forehead and stands up to leave."
                    "You get yourself put together and rush to make up for lost time."
                $ the_person.review_outfit()

            "Ask her to get off.":
                mc.name "Sorry [the_person.title], but I need to save my energy for later today."
                $ the_person.change_happiness(-3)
                $ the_person.change_obedience(5)
                "She frowns but nods. She swings her leg back over you and stands up."
                $ the_person.draw_person()
                the_person "Of course [the_person.mc_title], if you need me for anything just let me know. I hope you aren't running too late!"
                if removed_something:
                    "[the_person.title] collects some of her discarded from your floor and heads for the door."
                else:
                    "[the_person.title] gives you a kiss on the forehead and heads for the door."
                $ clear_scene()
                "You get up and rush to get ready to make up for lost time."

    $ clear_scene()
    return

init 1 python:
    def lily_new_underwear_requirement():
        if mc_at_home() and time_of_day==4: #It is the end of the day.
            if lily.effective_sluttiness("underwear_nudity") >= 10 and lily.love >= 0: #She's slutty enough to show you her new underwear.
                return True
        return False
    lily_new_underwear_crisis = Action("Lily New Underwear Crisis", lily_new_underwear_requirement, "lily_new_underwear_crisis_label")
    crisis_list.append([lily_new_underwear_crisis, 5])

label lily_new_underwear_crisis_label():
    # Lily has some new underwear she wants to demo for you.
    # We base the underwear sluttiness on Lily's sluttiness and use Love+Sluttiness to see if she'll show you as a "full outfit".
    $ the_person = lily #Just so we can keep
    $ valid_underwear_options = []
    $ the_underwear = None
    python:
        for underwear in default_wardrobe.get_underwear_sets_list():
            #She picks underwear that is in the top 20 sluttiness of what she considers slutty underwear AND that she would feel comfortable wearing in front of her (hopefully loving) brother.
            if underwear.get_underwear_slut_score() <= the_person.sluttiness and underwear.get_underwear_slut_score() >= the_person.sluttiness-20 and the_person.judge_outfit(underwear, the_person.love+30):
                valid_underwear_options.append(underwear)

        the_underwear = get_random_from_list(valid_underwear_options)
    if the_underwear is None:
        return #Lily doesn't have any skimpy underwear to show us :(

    $ bedroom.show_background()
    $ mc.change_location(bedroom) #Make sure we're in our bedroom.
    if the_person.obedience >= 95:
        "There's a knock at your door."
        the_person "[the_person.mc_title], can I talk to you for a sec?"
        mc.name "Uh, sure. Come in."
        "Your bedroom door opens and [the_person.possessive_title] steps in. She's carrying a shopping bag in one hand."
    else:
        "There's a single knock at your bedroom door before it's opened up. [the_person.possessive_title] steps in, carrying a shopping bag in one hand."
    $ the_person.draw_person(emotion = "happy")
    if the_underwear.get_underwear_slut_score() < 10:
        the_person "This is a little awkward, but I picked up some new underwear at the mall today but I don't know if I like the way it looks."
        the_person "Would you take a look and let me know what you think?"
    elif the_underwear.get_underwear_slut_score() < 20:
        the_person "I was at the mall today and picked up some new underwear. I know Mom would say it's too skimpy, but I wanted a guys opinion."
        the_person "Would you let me try it on and tell me what you think?"
    else:
        the_person "I was at the mall today and picked up some lingerie. I was hoping you'd let me model it for you and tell me what you think."

    menu:
        "Take a look at [the_person.title]'s new underwear.":
            "You sit up from your bed and give [the_person.possessive_title] your full attention."
            mc.name "Sure thing, is it in there?"
            "You nod your head towards the bag she is holding."
            the_person "Yeah, I'll go put it on and be back in a second. Don't move!"
            $ clear_scene()
            "[the_person.title] skips out of your room, closing the door behind her."
            $ the_person.apply_outfit(the_underwear)
            "You're left waiting for a few minutes. Finally, your door cracks open and [the_person.title] slips inside."
            $ the_person.draw_person(emotion="happy")
            if the_person.update_outfit_taboos():
                the_person "Oh my god, this is so much more embarrassing than I thought it would be."
                mc.name "Come on [the_person.title], I'm your brother. You can trust me."
                "She takes a deep breath and nods."
                the_person "Yeah, sure. Just don't stare too much, okay?"
                the_person "So, what do you think?"
                mc.name "Turn around, I want to see the other side."
            else:
                the_person "Here we go. What do you think?"
            $ the_person.draw_person(emotion="happy", position = "back_peek")
            "She turns around to give you a good look from behind."
            menu:
                "She looks beautiful.": #Raises love
                    mc.name "You look beautiful [the_person.title]. You're a heartstopper."
                    $ the_person.change_love(2)
                    the_person "Aww, you really think so?"

                "She looks sexy.": #Raises sluttiness
                    mc.name "You look damn sexy in it [the_person.title]. Like you're just waiting to pounce someone."
                    $ the_person.change_slut_temp(3)
                    the_person "Ooh, I like being sexy. Rawr!"

                "She looks elegant.": #Raises obedience
                    mc.name "It makes you look very elegent, [the_person.title]. Like a proper lady."
                    $ the_person.change_obedience(2)
                    the_person "It's not too uptight, is it? Do you think Mom would wear something like this?"

                "You don't like it.": #Raises nothing.
                    mc.name "I'm not sure it's a good look on you [the_person.title]."
                    $ the_person.change_happiness(-2)
                    the_person "No? Darn, it was starting to grow on me..."

            "[the_person.title] stands in front of your mirror and poses."
            $ the_person.draw_person(emotion = "happy")
            the_person "Do you think I should keep it? I'm on the fence."
            menu:
                "Keep it.":
                    $ the_person.wardrobe.add_underwear_set(the_underwear)
                    mc.name "You should absolutely keep it. It looks fantastic on you."
                    $ the_person.change_happiness(3)
                    "[the_person.title] grins and nods."
                    the_person "You're right, of course you're right. Thank you [the_person.mc_title], you're the best!"


                "Return it.":
                    mc.name "I think you have other stuff that looks better."
                    $ the_person.change_obedience(2)
                    the_person "I think you're right, I should save my money and get something better. Thank you [the_person.mc_title], you're the best!"

            $ the_person.change_love(3)
            "[the_person.possessive_title] walks over to you and gives you a hug."
            the_person "Okay, it's getting cold. I'm going to go put some clothes on!"
            $ clear_scene()
            "[the_person.title] slips out into the hall, leaving you alone in your room."


        "Send her away.":
            mc.name "Sorry [the_person.title], but I'm busy right now. You'll have to figure out if you like it by yourself."
            the_person "Right, no problem. Have a good night!"
            $ clear_scene()
            "She leaves and closes your door behind her."

    $ clear_scene()
    return

init 1 python:
    def lily_morning_encounter_requirement():
        if mc_at_home() and time_of_day == 0:
            return True
        return False

    lily_morning_encounter_crisis = Action("Lily Morning Encounter", lily_morning_encounter_requirement, "lily_morning_encounter_label")
    morning_crisis_list.append([lily_morning_encounter_crisis, 5])

label lily_morning_encounter_label():
    # You run into Lily early in the morning as she's going to get some fresh laundry. At low sluttiness she is embarrassed, at high she is completely naked.
    $ the_person = lily
    if the_person.effective_sluttiness() >= 60:
        $ the_person.apply_outfit(Outfit("Nude"))
        # $ the_person.outfit = default_wardrobe.get_outfit_with_name("Nude 1") #If sh's very slutty she doesn't mind being naked. Chnaged v0.24.1
    else:
        $ the_person.apply_outfit(the_person.wardrobe.get_random_appropriate_underwear(the_person.sluttiness, guarantee_output = True))
        # $ the_person.outfit = the_person.wardrobe.get_random_appropriate_underwear(the_person.sluttiness, guarantee_output = True) # Otherwise get an underwear set she would wear. changed v0.24.1

    "You wake up in the morning to your alarm. You get dressed and leave your room to get some breakfast."
    $ the_person.draw_person()
    if the_person.outfit.wearing_panties():
        "The door to [the_person.possessive_title]'s room opens as you're walking past. She steps out, wearing nothing but her underwear."
    else:
        "The door to [the_person.possessive_title]'s room opens as you're walking past. She steps out, completeley naked."


    if the_person.effective_sluttiness("underwear_nudity") < 10:
        #She's startled and embarrassed.
        "[the_person.title] closes her door behind her, then notices you. She gives a startled yell."
        the_person "Ah! [the_person.mc_title], what are you doing here?"
        "She tries to cover herself with her hands and fumbles with her door handle."
        mc.name "I'm just going to get some breakfast. What are you doing?"
        "[the_person.title] gets her door open and hurries back inside. She leans out so all you can see is her head."
        the_person "I was going to get some laundry and thought you were still asleep. Could you, uh, move along?"
        $ the_person.change_slut_temp(2)
        "You shrug and continue on your way."

    elif the_person.effective_sluttiness("underwear_nudity") < 40:
        #She doesn't mind but doesn't think to tease you further
        "[the_person.title] closes her door behind her, then notices you. She turns and smiles."
        the_person "Morning [the_person.mc_title], I didn't think you'd be up yet."
        mc.name "Yep, early start today. What are you up to?"
        if the_person.outfit.wearing_panties():
            "She starts to walk alongside you and doesn't seem to mind being in her underwear."
        else:
            "She starts to walk alongside you and doesn't seem to mind being naked."
        $ the_person.update_outfit_taboos()
        the_person "I'm just up to get some laundry. I put some in last night."
        "You let [the_person.title] get a step ahead of you so you can look at her ass."
        $ the_person.draw_person(position = "walking_away")
        menu:
            "Compliment her.":
                #Bonus love and happiness
                mc.name "Well, I'm glad I ran into you. Seing you is a pretty good way to start my day."
                $ the_person.change_love(2)
                $ the_person.change_happiness(5)
                the_person "You're just saying that because you get to see me naked, you perv."
                $ the_person.draw_person(position = "back_peek")
                "She peeks back at you and winks."

            "Slap her ass.":
                #Bonus sluttiness and obedience
                mc.name "Did you know you look really cute without any clothes on?"
                "You give her a quick slap on the ass from behind. She yelps and jumps forward a step."
                the_person "Ah! Hey, I'm not dressed like this for you, this is my house too you know."
                "She reaches back and rubs her butt where you spanked it."
                the_person "And ew. I'm your sister, you shouldn't be gawking at me."
                mc.name "I'll stop gawking when you stop shaking that ass."
                $ the_person.draw_person(position = "back_peek")
                the_person "You wish this ass was for you."
                "She spanks herself lightly and winks at you."
                $ the_person.change_slut_temp(4)
                $ the_person.change_obedience(2)

        $ the_person.draw_person(position = "walking_away")
        "You reach the door to the kitchen and split up. You wait a second and enjoy the view as your [the_person.possessive_title] walks away."

    else: #sluttiness >= 40-55
        #She likes being watched and teases you a little while you walk together.
        "[the_person.title] closes her door behing her, then notices you."
        the_person "Morning [the_person.mc_title], I was wondering if you were going to be up now."
        mc.name "Yep, early start today. What are you up to?"
        the_person "I was just going to get some laundry out of the machine."
        if the_person.outfit.wearing_panties():
            "[the_person.possessive_title] thumbs her underwear playfully."
        else:
            "[the_person.possessive_title] absentmindedly runs her hands over her hips."
        $ the_person.update_outfit_taboos()
        the_person "I know you like it when I walk around naked but Mom doesn't. At least when I'm doing laundry I have an excuse."
        "You join her as she starts to walk down the hall."
        $ the_person.draw_person(position = "walking_away")
        menu:
            "Grope her as you walk.":
                "You reach behind [the_person.title] and grab her ass while she's walking. She moans softly and leans against you."
                if the_person.has_taboo("touching_body"):
                    $ the_person.call_dialogue("touching_body_taboo_break")
                    $ the_person.break_taboo("touching_body")
                else:
                    the_person "[the_person.mc_title], what are you doing? We can't doing anything here..."
                    mc.name "I know, I'm just having a feel. You've got a great ass."
                    "You spank her butt and she moans again. You work your hand down between her legs from behind and run a finger along her slit."
                    the_person "Fuck, please don't get me too wet. I don't want to have to explain that to Mom if she finds us."
                    "You flick your finger over [the_person.possessive_title]'s clit, then slide your hand back and kneed her ass some more."
                $ the_person.change_slut_temp(5)
                $ the_person.change_love(2)
                "When you reach the kitchen [the_person.title] reluctantly pulls away from you."


            "Put her hand on your cock as you walk.":
                "You take [the_person.title]'s left hand and push it against your crotch."
                if the_person.has_taboo("touching_penis"):
                    the_person "Oh my god, what are you doing!"
                    mc.name "I saw you looking at it, I thought you might be curious. Just give it a feel."
                    the_person "I can't believe you... You just made me touch it like that!"
                    mc.name "You liked it though, didn't you? Come on, let's keep walking."
                    "You hold her hand against your crotch as you walk. She looks away awkwardly, but doesn't try and pull away."
                    mc.name "You can touch it for real, if you want."
                    the_person "You're such a pervert, you know that? Tricking me into this..."
                    "Her hand slides up to your waist, then down under your underwear. She wraps her hand around your shaft and rubs it gently."
                    mc.name "Sure thing [the_person.title], I've really tricked you."

                    $ the_person.break_taboo("touching_penis")
                else:
                    the_person "What are you doing?"
                    mc.name "Look at what you do to me when you walk around like this. You're driving me crazy [the_person.title]."
                    "You let go of her hand but it stays planted on your bulge as you walk."
                    the_person "You're such a pervert, you know that? I can't believe you'd even think about me like that..."
                    "Her hand slides up to your waist, then down under your underwear. She wraps her hand around your shaft and rubs it gently."
                    mc.name "Don't pretend like you don't like it. You're just as horny as I am."
                    the_person "Hey, I'm just doing this for you, okay?"
                    mc.name "Sure thing sis. Keep going."
                $ the_person.change_slut_temp(3)
                $ the_person.change_obedience(3)
                "The two of you walk slowly towards the kitchen as [the_person.possessive_title] fondles your dick."
                "When you reach the door to the kitchen she reluctantly pulls her hand out of your pants."

        mc.name "Maybe we'll follow up on this later."
        "[the_person.possessive_title]'s face is flush. She nods and heads towards the laundry room. You get to watch her ass shake as she goes."

    $ the_person.apply_outfit(the_person.planned_outfit)
    #$ the_person.outfit = the_person.planned_outfit.get_copy() #Make sure to reset their outfits for the day. changed v0.24.1
    $ clear_scene()
    return

init 1 python:
    def family_weekend_breakfast_requirement():
        if mc_at_home() and time_of_day == 0 and mc.business.is_weekend() and mom.love > 20:
            return True
        return False

    family_morning_breakfast_crisis = Action("Family Morning Breakfast", family_weekend_breakfast_requirement, "family_morning_breakfast_label")
    morning_crisis_list.append([family_morning_breakfast_crisis,15])

label family_morning_breakfast_label():
    $ the_mom = mom
    $ the_sister = lily
    if the_mom is None or the_sister is None:
        return #If we don't have family members abort because something has gone horribly wrong!

    $ mom_slutty = False
    $ sis_slutty = False
    if the_mom.effective_sluttiness() > 40:
        $ mom_slutty = True
        $ the_mom.apply_outfit(the_mom.wardrobe.get_random_appropriate_underwear(the_mom.sluttiness, guarantee_output = True))
    #    $ the_mom.outfit = the_mom.wardrobe.get_random_appropriate_underwear(the_mom.sluttiness, guarantee_output = True) changed v0.24.1

    if the_sister.effective_sluttiness() > 40:
        $ sis_slutty = True
        $ the_sister.apply_outfit(the_sister.wardrobe.get_random_appropriate_underwear(the_sister.sluttiness, guarantee_output = True))
        #$ the_sister.outfit = the_sister.wardrobe.get_random_appropriate_underwear(the_sister.sluttiness, guarantee_output = True) Changed v0.24.1
    $ bedroom.show_background()
    "You're woken up in the morning by a knock at your door."
    mc.name "Uh, come in."
    "You groan to yourself and sit up in bed."
    if the_mom.love > the_sister.love:
        $ the_mom.draw_person()
        "Your mother cracks your door open and leans in."
        the_mom "I'm making some breakfast for you and your sister. Come on down if you'd like some."
        mc.name "Thanks Mom, I'll be down in a minute."
        $ clear_scene()
        "She flashes you a smile and closes the door."
    else:
        $ the_sister.draw_person()
        "[the_sister.possessive_title] cracks your door open and leans in. She seems just as tired as you are."
        the_sister "Hey, I think Mom's making a family breakfast for us."
        mc.name "Thanks for letting me know [the_sister.title], I'll be down in a minute."
        $ clear_scene()
        "She nods and closes your door as she leaves."

    "You get up, get dressed, and head for the kitchen."
    $ mc.change_location(kitchen)
    $ kitchen.show_background()
    $ the_mom.draw_person(position = "walking_away")
    if mom_slutty:
        if the_mom.outfit.wearing_panties():
            "[the_mom.possessive_title] is just in her underwear in front of the stove, humming as she scrambles a pan full of eggs."
        else:
            "[the_mom.possessive_title] is in front of the stove naked, humming as she scrambles a pan full of eggs."
    else:
        "[the_mom.possessive_title] is at the stove and humming to herself as she scrambles a pan full of eggs."

    $ the_mom.update_outfit_taboos()
    $ the_mom.draw_person(position = "back_peek")
    the_mom "Good morning [the_mom.mc_title]. I'm almost ready to serve, hopefully your sister will be here soon."
    the_sister "I'm coming!"
    $ the_sister.draw_person()
    if sis_slutty:
        if the_sister.outfit.wearing_panties():
            "[the_sister.possessive_title] comes into the room just wearing her underwear. She gives a dramatic yawn before sitting down at the kitchen table."
        else:
            "[the_sister.possessive_title] comes into the room naked. She gives a dramatic yawn before sitting down at the kitchen table."
    else:
        "[the_sister.possessive_title] comes into the room and gives a dramatic yawn before sitting down at the kitchen table."

    $ the_sister.update_outfit_taboos()
    if mom_slutty and sis_slutty:
        #You have breakfast with both of them stripped down like it's no big thing.
        $ the_sister.draw_person(position = "sitting")
        the_sister "Hope I'm not too late."
        $ the_mom.draw_person(position = "walking_away")
        "Your mother takes the pan off the stove and begins to slide the contents off onto three plates."
        the_mom "No, just on time."
        $ the_mom.draw_person()
        "She turns around and hands one plate to you and one plate to [the_sister.title]."
        $ the_sister.draw_person(position = "sitting")
        the_sister "Thanks Mom, you're the best!"
        $ the_mom.draw_person(position="sitting")
        the_mom "No problem, I'm just happy to spend my morning relaxing with my two favourite people!"
        "You enjoy a relaxing breakfast bonding with your mother and sister. [the_mom.possessive_title] seems particularly happy she gets to spend time with you."
        "Neither [the_sister.title] or [the_mom.possessive_title] seem to think it's strange to relax in their underwear."
        $ the_sister.change_love(3)
        $ the_sister.change_slut_temp(3)
        $ the_mom.change_love(3)
        $ the_mom.change_slut_temp(3)
        $ the_mom.change_happiness(10)
        "When you're done you help Mom put the dirty dishes away and get on with your day."



    elif mom_slutty and not sis_slutty:
        #Lily thinks her mom is embarassing and weird but Mom pulls rank.
        the_sister "Oh my god Mom, what are you wearing?"
        $ the_mom.draw_person(position = "back_peek")
        the_mom "What? It's the weekend and it's just the three of us. I didn't think anyone would mind if I was a little more casual."
        $ the_sister.draw_person(position = "sitting")
        if the_mom.outfit.vagina_visible():
            the_sister "Mom, I don't think you know what casual means. Could you at least put on some panties or something?"

        elif the_mom.outfit.tits_visible():
            the_sister "Mom, I don't think you know what casual means. I mean, couldn't you at least put a bra?"

        else:
            the_sister "Mom, you're prancing around the kitchen in your underwear. In front of your son and daughter. That's weird."
            "[the_sister.title] looks at you."
            the_sister "Right [the_sister.mc_title], that's weird?"

        if the_mom.obedience > 115:
            $ the_mom.draw_person(position = "back_peek")
            the_mom "What do you think [the_mom.mc_title], do you think it's \"weird\" for your mother to want to be comfortable in her own house?"
            menu:
                "Side with Mom.":
                    mc.name "I think Mom's right [the_sister.title]. It's nothing we haven't seen before, she's just trying to relax on her days off."
                    $ the_mom.change_obedience(-5)
                    $ the_sister.change_obedience(5)
                    "[the_sister.title] looks at the two of you like you're crazy then sighs dramatically."
                    the_sister "Fine, but this is really weird, okay?"
                    $ the_mom.draw_person(position = "sitting")
                    "[the_mom.possessive_title] dishes out three portions and sits down at the table with you. [the_sister.title] eventaully gets use to her mothers outfit and joins in on your conversation."
                    $ the_sister.change_slut_temp(5)
                    $ the_mom.change_happiness(10)


                "Side with [the_sister.title].":
                    mc.name "I actually think [the_sister.title] is right, this is a little weird. Could you go put something on, for our sakes?"
                    $ the_sister.change_obedience(-2)
                    $ the_sister.change_slut_temp(2)
                    $ the_mom.change_obedience(5)
                    $ the_mom.change_slut_temp(5)
                    the_mom "Oh you two, you're so silly. Fine, I'll be back in a moment. [the_sister.title], could you watch the eggs?"
                    $ the_sister.draw_person(position = "walking_away")
                    "Your mother leaves to get dressed. [the_sister.possessive_title] ends up serving out breakfast for all three of you."
                    $ the_mom.apply_outfit(the_mom.planned_outfit)
                    # $ the_mom.outfit = the_mom.planned_outfit.get_copy() changed v0.24.1
                    the_sister "She's been so weird lately. I don't know what's going on with her..."
                    $ the_mom.draw_person(position = "sitting")
                    $ the_sister.change_happiness(5)
                    $ the_mom.change_happiness(5)
                    "When [the_mom.possessive_title] gets back she sits down at the table and the three of you enjoy your breakfast together."

        else:
            #She likes what she likes
            $ the_mom.draw_person(position = "back_peek")
            the_mom "Well luckily I'm your mother and it doesn't matter what you think. I'm going to wear what makes me comfortable."
            "She takes the pan off the stove and slides the scrambled eggs out equally onto three plates."
            the_mom "Now, would you like some breakfast or not?"
            "[the_sister.title] sighs dramatically."
            the_sister "Fine, but this is really weird, okay?"
            $ the_sister.change_slut_temp(5)
            $ the_mom.change_happiness(10)
            $ the_mom.draw_person(position = "sitting")
            "[the_mom.possessive_title] gives everyone a plate and sits down. [the_sister.title] eventaully gets use to her mothers outfit and joins in on your conversation."
            "When you're done you help Mom put the dirty dishes away and get on with your day."


    elif sis_slutty and not mom_slutty:
        #Mom thinks lilly is way too underdressed and sends her back to get dressed.
        $ the_sister.draw_person(position = "sitting")
        "Your mother turns around and gasps."
        $ the_mom.draw_person(emotion = "angry")
        the_mom "[the_sister.title]! What are you wearing?"
        $ the_sister.draw_person(position = "sitting")
        the_sister "What do you mean? I just got up, I haven't had time to pick out an outfit yet."
        $ the_mom.draw_person(emotion = "angry")
        the_mom "You shouldn't be running around the house naked. Go put some clothes on young lady."
        $ the_sister.draw_person(position = "sitting", emotion = "angry")
        "[the_sister.possessive_title] scoffs and rolls her eyes."
        the_sister "Come on Mom, you're being ridiculous. This is my house too, I should be able to wear whatever I want!"
        "Your mother and sister lock eyes, engaged in a subtle battle of wills."
        if the_sister.obedience > the_mom.obedience:
            $ the_mom.draw_person(position = "walking_away")
            "Mom sighs loudly and turns back to the stove."
            the_mom "Fine! You're so stubborn [the_sister.title], I don't know how I survive around here!"
            $ the_sister.change_obedience(-2)
            $ the_sister.change_happiness(10)
            $ the_sister.change_slut_temp(3)
            $ the_mom.change_obedience(10)
            $ the_sister.draw_person(position = "sitting", emotion = "happy")
            "[the_sister.possessive_title] looks at you, obviously pleased with herself, and winks."

        else:
            "[the_sister.title] finally sighs loudly and looks away. She pushes her chair back and stands up in defeat."
            $ the_sister.draw_person(emotion = "angry")
            the_sister "Fine! I'll go put on some stupid clothes so my stupid mother doesn't keep worrying."
            $ the_sister.draw_person(position = "walking_away")
            "[the_sister.title] sulks out of the kitchen."
            $ the_mom.draw_person()
            the_mom "I don't know how I manage to survive with you two around!"
            $ the_sister.apply_outfit(the_sister.planned_outfit)
            #$ the_sister.outfit = the_sister.planned_outfit.get_copy() changed v0.24.1
            $ the_sister.change_obedience(10)
            $ the_sister.change_happiness(-5)
            $ the_mom.change_obedience(-2)
            $ the_sister.draw_person(position = "sitting")
            "[the_sister.possessive_title] is back by the time Mom starts to plate breakfast. She sits down and starts to eat without saying a word."
        "When you're done you help Mom put the dirty dishes away and get on with your day."



    else:
        #Neither of them are particularly slutty, so it's just a normal breakfast.
        $ the_sister.draw_person(position = "sitting")
        the_sister "So what's the occasion Mom?"
        $ the_mom.draw_person()
        "[the_mom.possessive_title] takes the pan off the stove and scoops the scrambled eggs out equally onto three waiting plates."
        the_mom "Nothing special, I just thought we could have a nice quiet weekend breakfast together."
        "She slides one plate in front of you and one plate in front of [the_sister.title], then turns around to get her own before sitting down to join you."
        $ the_mom.draw_person(position = "sitting")
        the_mom "Go ahead, eat up!"
        $ the_sister.change_love(3)
        $ the_mom.change_love(3)
        $ the_mom.change_happiness(5)
        "You enjoy a relaxing breakfast bonding with your mother and sister. Your mom seems particularly happy she gets to spend time with you."
        "When you're done you help Mom put the dirty dishes away and get on with your day."

    $ clear_scene()
    return

init 1 python:
    def morning_shower_requirement():
        if mc_at_home() and time_of_day == 0:
            return True #You're at home for the night, when you take a shower in the morning something might happen.
        return False
    morning_shower_criris = Action("Morning Shower", morning_shower_requirement, "morning_shower_label")
    morning_crisis_list.append([morning_shower_criris, 15])

label morning_shower_label(): #TODO: make a similar event for your Aunt's place.
    # You wake up and go to take a shower, lily or your mom are already in there.
    "You wake up in the morning uncharacteristically early feeling refreshed and energized. You decide to take an early shower to kickstart the day."
    $ the_person = get_random_from_list([mom, lily, None])
    if the_person is None:
        #You run into nobody, gain some extra energy. TODO: One of the girls comes to join you.
        "You head to the bathroom and start the shower. You step in and let the water just flow over you, carrying away your worries for the day."
        "After a few long, relaxing minutes it's time to get out. You start the day feeling energized."
        $ mc.change_energy(20)

    else:
        "You head to the bathroom, but hear the shower already running inside when you arrive."
        $ initial_outfit = the_person.outfit.get_copy()
        $ towel_outfit = Outfit("Towel")
        $ towel_outfit.add_dress(towel.get_copy()) #TODO: Decide if we want a head towel here, maybe just for mom or just for Lily

        menu:
            "Skip your shower.":
                "With the bathroom occupied you decide to get some extra sleep instead."

            "Knock on the door.":
                # She says she'll be "out in a minute", or invites you in. Give her a shower outfit.
                "You knock on the door a couple of times and wait for a response."
                if the_person.effective_sluttiness(["bare_tits","bare_pussy"]) > 30:
                    the_person "It's open, come on in!"
                    call girl_shower_enter(the_person, suprised = False) from _call_girl_shower_enter
                else:
                    the_person "Just a second!"
                    call girl_shower_leave(the_person) from _call_girl_shower_leave

            "Barge in anyways.":
                # Locked, unless the girl is slutty enough that you wouldn't mind (TODO: add a "make changes to the house" option where you can't lock the door so you can barge in on lily.)
                if the_person.effective_sluttiness(["bare_tits", "bare_pussy"]) < 10:
                    "You try and open the door, but find it locked."
                    the_person "One second!"
                    call girl_shower_leave(the_person) from _call_girl_shower_leave_1
                elif the_person.effective_sluttiness(["bare_tits", "bare_pussy"]) <= 20:
                    #She's angry that you've barged in on her (but she doesn't mind enough to have locked the door).
                    $ the_person.apply_outfit(Outfit("Nude"))
                    #$ the_person.outfit = Outfit("Nude") #changed v0.24.1
                    $ the_person.draw_person(emotion = "angry")
                    "You open the door. [the_person.possessive_title] is standing naked in the shower. She spins around and yells in suprise."
                    the_person "[the_person.mc_title]! I'm already in here, what are you doing?"
                    mc.name "The door was unlocked, I thought you might have already been finished."
                    the_person "Knock next time, okay? I'll be done in a minute."
                    "She shoos you out of the room, seeming more upset about being interrupted than being seen naked."
                    $ clear_scene()
                    $ the_person.change_love(-1)
                    $ the_person.change_slut_temp(2)
                    call girl_shower_leave(the_person) from _call_girl_shower_leave_2
                else:
                    call girl_shower_enter(the_person, suprised = True) from _call_girl_shower_enter_1 #TODO: Decide if we need different dialogue for this (maybe just a "suprised" tag we can pass)

        $ the_person.apply_outfit(initial_outfit)
        #$ the_person.outfit = initial_outfit #put her back in her normal outfit after her shower #changed v0.24.1

    $ clear_scene()
    return

label girl_shower_leave(the_person):
    "After a short pause the shower stops and you hear movement on the other side of the door."
    #$ the_person.outfit = towel_outfit changed v0.24.1
    $ the_person.apply_outfit(towel_outfit)
    $ the_person.draw_person()
    "The bathroom door opens and [the_person.possessive_title] steps out from the steamy room in a towel."
    if the_person is mom:
        the_person "There you go [the_person.mc_title], go right ahead."
        "She gives you a quick kiss and steps past you."
    else:
        the_person "There, it's all yours. I might have used up all of the hot water."
        "She steps past you and heads to her room."
    return

label girl_shower_enter(the_person, suprised):
    $ mc.change_location(home_bathroom)
    $ home_bathroom.show_background()
    $ the_person.apply_outfit(Outfit("Nude"))
    #$ the_person.outfit = Outfit("Nude") changed v0.24.1
    $ the_person.draw_person(position = "back_peek")
    "You open the door and see [the_person.possessive_title] in the shower."
    if suprised:
        "She looks up at you, slightly startled, and turns her body away from you."
        the_person "Oh, [the_person.mc_title]!"
        mc.name "I'm just here to have a shower."
    the_person "I should be finished soon, if you don't mind waiting."
    $ the_person.update_outfit_taboos()
    menu:
        "Wait and watch her shower.":
            "You nod and head to the sink to brush your teeth. You lean on the sink and watch [the_person.title] while you brush."
            if the_person.effective_sluttiness() > 40 - (5 * (the_person.get_opinion_score("showing her tits")+the_person.get_opinion_score("showing her ass"))):
                $ the_person.discover_opinion("showing her tits")
                $ the_person.discover_opinion("showing her ass")
                "She notices you watching, but doesn't seem to mind the attention."
                $ the_person.change_slut_temp(1+(the_person.get_opinion_score("showing her tits")+the_person.get_opinion_score("showing her ass")))
            else:
                the_person "It's strange to shower with someone else in the room."
                mc.name "Nothing to worry about, we're all family here, right?"
                "She shrugs and nods, but you notice she's always trying to shield her body from your view."
                $ the_person.change_slut_temp(1)
                $ the_person.change_obedience(1)
            $ the_person.update_outfit_taboos()
            "Soon enough she's finished. She steps out and grabs a towel, but leaves the shower running for you."

            $ the_person.apply_outfit(towel_outfit)
            $ the_person.draw_person()
            the_person "There you go. Enjoy!"
            $ clear_scene()
            "She steps past you and leaves. You get into the shower and enjoy the relaxing water yourself."
            $ mc.change_energy(20)

        "Join her in the shower." if the_person.obedience >= 120:
            mc.name "How about I just jump in, I can get your back and we'll both save some time."
            if the_person.effective_sluttiness() > 40:
                the_person "Sure, if you're okay with that. I will put you to work though."
                "She gives you a warm smile and invites you in with her."
            else:
                the_person "I'm not sure..."
                mc.name "I've got work to get to today, so I'm getting in that shower."
                "[the_person.possessive_title] nods meekly."
                the_person "Okay."

            "You strip down and get in the shower with [the_person.title]. The space isn't very big, so she puts her back to you."
            "You're left with her ass inches from your crotch, and when she leans over to pick up the shampoo she grinds up against you."
            $ mc.change_arousal(5)
            the_person "Oops, sorry about that."
            "Your cock, already swollen, hardens in response, and now even stood up the tip brushes against [the_person.possessive_title]'s ass."
            if the_person.effective_sluttiness("touching_body") <= 40:
                the_person "I think I'm just about done, so you can take care of this..."
                "She wiggles her butt and strokes your tip against her cheeks."
                $ the_person.change_slut_temp(3 + the_person.get_opinion_score("showing her ass"))
                "She steps out of the shower and grabs a towel."
                $ the_person.apply_outfit(towel_outfit)

            # elif the_person.effective_sluttiness() <= 60: #TODO: Add a "hot dog" position and make it a starting position for this.
            #     "She wiggles her butt and strokes your tip against her cheeks."
            #     the_person "Do you need some help with this? How about you just... use my butt?"
            #     $ the_person.draw_person("walking_away")
            #     "She rubs up against you while you talk, stroking your shaft with her wet, slippery ass."
            #     menu:
            #         "Jerk off with her ass.":
            #
            #         "Just have a shower.":


            else:
                the_person "What is this?"
                "She wiggles her butt and strokes your tip against her cheeks."
                the_person "Well we need to take care of this, don't we..."
                "She turns around and faces you. It might be the hot water, but her face is flush."
                $ the_person.change_slut_temp(2)
                menu:
                    "Fuck her.":
                        call fuck_person(the_person, skip_intro = True) from _call_fuck_person_1
                        $ the_report = _return

                        $ the_person.apply_outfit(towel_outfit)
                        # $ the_person.outfit = Outfit("Towel") changed v0.24.1
                        # $ the_person.outfit.add_dress(towel.get_copy())
                        $ the_person.draw_person()
                        "When you're finished [the_person.title] steps out of the shower and grabs a towel. She dries herself off, then wraps herself in it then turns to you."
                        if the_report.get("girl orgasms",0)>0:
                            the_person "Well that's a good way to start the day. See you later."
                        elif the_report.get("guy orgasms",0)>0:
                            the_person "Well I hope you enjoyed your start to the day. See you later."
                        else:
                            the_person "Well maybe we can pick this up some other time. See you later."

                        $ clear_scene()
                        "She leaves the room and you finish your shower alone, feeling refreshed by the water."

                    "Just have a shower.":
                        mc.name "Maybe some other time, I've got to hurry up though."
                        "She pouts and nods."
                        $ the_person.change_obedience(1)
                        the_person "Alright, up to you."

            $ mc.change_energy(20)


        "Join her in the shower.\nRequires: 120 Obedience (disabled)" if the_person.obedience < 120:
            pass


    $ mc.change_location(bedroom)
    return

#TODO: mall crisis requiprements.
# The girls invite you shopping on the weekend.
#
# label family_shopping_trip(): #TODO: Hook this up as a crisis.
#     $ the_mom = mom
#     $ the_sister = lily
#     #
#
#     $ clear_scene()
#     call advance_time()
#     return

init 1 python:
    def cousin_tease_crisis_requirement():
        if cousin.effective_sluttiness() >= 30 and cousin.obedience < 120 and cousin.love < 10 and cousin not in mc.location.people:
            return True
        return False
    cousin_tease_crisis = Action("Cousin text tease", cousin_tease_crisis_requirement, "cousin_tease_crisis_label")
    crisis_list.append([cousin_tease_crisis, 3])

label cousin_tease_crisis_label():
    $ the_person = cousin
    $ mc.start_text_convo(the_person)
    if the_person.effective_sluttiness("underwear_nudity") < 35: #She'll want money
        "You get a curt text from [the_person.title]."

        the_person "I need some cash. Do you have a hundred bucks?"
        menu:
            "Send [the_person.title] some money.\n-$100" if mc.business.funds >= 100:
                $ mc.business.funds += -100
                "You pull up your banking app and send [the_person.possessive_title] some money, then text back."
                mc.name "There you go, sent."
                the_person "Just like that? Well, thanks I guess."
                mc.name "It's just money, I'd rather you were happy."
                $ the_person.change_obedience(-4)
                $ the_person.change_happiness(5)
                $ the_person.change_love(1)
                the_person "Sure thing, nerd."


            "Send [the_person.title] some money.\n-$100 (disabled)" if mc.business.funds < 100:
                pass

            "Ask why she needs it.":
                mc.name "What do you need it for?"
                the_person "Why do you care? Come on, I need some cash quick."
                the_person "Come on you horny perv, I'll give you a picture of my tits if you send me the cash."
                $ the_person.draw_person()
                if the_person.outfit.tits_visible():
                    "She sends you a picture, but her tits are already out and on display."
                    the_person "Fuck, delete that. That wasn't one wasn't for you..."
                    mc.name "No, I think I've gotten everything I want already."
                    $ the_person.change_slut_temp(1)
                    $ the_person.change_obedience(1)
                    "She types, then deletes several messages, but never sends anything else to you."
                else:
                    "She sends you a picture from her phone, obviously trying to tease you a little."
                    menu:
                        "Send [the_person.title] some money.\n-$100" if mc.business.funds >= 100:
                            $ mc.business.funds += -100
                            "You send her the money from your phone."
                            mc.name "Alright, there's your cash. Whip those girls out for me."
                            the_person "Ugh, I didn't think you'd actually do it."
                            $ the_person.outfit.strip_to_tits()
                            $ the_person.draw_person(position = "back_peek")
                            "She sends you a picture, with her back turned to the camera."
                            the_person "There."
                            mc.name "What the fuck is that, I want to see those tits."
                            the_person "I've already got my cash, so whatever nerd."
                            mc.name "You know I can reverse it within ten minutes, right?"
                            the_person "Fuck. Fine!"
                            $ the_person.draw_person()
                            the_person "There. Now go jerk off in the bathroom or whatever it is you want to do with that."
                            $ the_person.change_obedience(-2)
                            $ the_person.change_slut_temp(3)

                            menu:
                                "Reverse the payment anyways.":
                                    $ mc.business.funds += 100
                                    "You don't respond to her, but you do open up your banking app again."
                                    "You flag the recent transfer as \"accidental\" and in a few minutes the money is back in your account."
                                    "It doesn't take long before you get a string of angry texts from [the_person.possessive_title]."
                                    $ the_person.change_love(-5)
                                    $ the_person.change_obedience(-3)
                                    the_person "What the FUCK!"
                                    the_person "Give me my money! We had a deal!"
                                    mc.name "Sorry, but I've already got my pics. Later nerd."
                                    "You have to block her for a few minutes as more angry texts stream in."

                                "Let her keep the money.":
                                    "You think about reversing the charges anyways, but decide it's not the best idea if you want to keep this sort of relationship going."
                                    $ the_person.break_taboo("bare_tits")


                        "Send [the_person.title] some money.\n-$100 (disabled)" if mc.business.funds < 100:
                            pass

                        "Blackmail her for some nudes." if the_person.event_triggers_dict.get("blackmail_level",-1) > 0 and the_person.event_triggers_dict.get("last_blackmailed", -5) + 5 <= day:
                            $ the_person.event_triggers_dict["last_blackmailed"] = day
                            if the_person.event_triggers_dict.get("blackmail_level",1) == 1:
                                mc.name "How about this, you send them over and I don't say anything to your mom about you stealing from my sister."

                            else: #Level 2
                                mc.name "How about this, you send them over and I don't say anything to your mom about your after hours job."

                            the_person "Oh my god, you little rat. You wouldn't."
                            mc.name "You know I would. Come on, whip those girls out and take some shots for me."
                            $ the_person.outfit.strip_to_tits()
                            $ the_person.draw_person()
                            "There's a pause, then [the_person.title] sends you some shots of herself topless."
                            the_person "There. Satisfied?"
                            if the_person.event_triggers_dict.get("blackmail_level",1) == 2:
                                menu:
                                    "Not yet.":
                                        mc.name "Not yet, I want to see those tits shaking. Send me a video."
                                        mc.name "Just imagine I slid a twenty down your g-string and you're giving me a private dance. You're good at those, right?"
                                        "There's another pause, then [the_person.title] sends you a video."
                                        $ the_person.draw_person(position = "kneeling1", emotion = "angry", the_animation = blowjob_bob, animation_effect_strength = 0.8)
                                        "She's kneeling on her bed. She sighs dramatically, then starts to bounce her body, jiggling her tits up and down."
                                        "You watch it through, but feel like she could put some more effort into it."
                                        mc.name "Come on, that was a little pathetic. Smile for me and really give it your all this time."
                                        the_person "You want another video? You're being ridiculous."
                                        mc.name "You know the deal. Get to work."
                                        "There's yet another pause, then another video."
                                        $ the_person.draw_person(position = "kneeling1", emotion = "happy", the_animation = blowjob_bob, animation_effect_strength = 1.0)
                                        if the_person.has_large_tits():
                                            "This time [the_person.title] has a nice, fake smile for you. She bounces herself a little more vigerously and really gets her big tits moving."
                                        else:
                                            "This time [the_person.title] has a nice, fake smile for you."
                                            "She bounces herself a little more vigerously, but there's not much chest for her to shake to shake."
                                        the_person "Are you satisfied now, you little perv?"

                                        mc.name "For now. See you around."

                                    "For now.":
                                        mc.name "For now, but we'll see how I'm feeling next time I see you."
                                        the_person "Ugh. Please don't remind me."

                            $ the_person.update_outfit_taboos()
                            $ the_person.change_obedience(3)
                            $ the_person.change_slut_temp(2)

                        "Blackmail her for some nudes.\nBlackmailed too recently. (disabled)" if the_person.event_triggers_dict.get("blackmail_level",-1) > 0 and the_person.event_triggers_dict.get("last_blackmailed", -5) + 5 > day:
                            pass


                        "Tell her no.":
                            mc.name "You think I'd want to pay to see your tits? You should be paying me."
                            $ the_person.change_love(-1)
                            the_person "Whatever, I can make the cash somewhere else."
                            "You don't recieve any more messages from her."



            "Tell her no.":
                mc.name "For you? Of course not."
                $ the_person.change_obedience(1)
                the_person "Oh my god, you're the worst. Whatever."

    else:
        "Out of the blue, [the_person.possessive_title] sends you a text."
        the_person "Are you at work right now?"
        if mc.is_at_work():
            mc.name "Yeah, why do you care?"
        else:
            mc.name "No. Why do you care?"

        "She sends you a picture."
        $ the_person.apply_outfit(lingerie_wardrobe.get_random_appropriate_outfit(the_person.effective_sluttiness()/2, the_person.effective_sluttiness()*2, True))
        $ the_person.draw_person(position = "kneeling1")
        "She's in her bedroom, kneeling on her bed in nothing but some lingerie."
        if the_person.update_outfit_taboos():
            the_person "I can't believe I'm showing this to a pervert like you, but I got a new outfit."
            the_person "Do you like it?"

        else:
            the_person "I got a new outfit. Do you like it?"
        menu:
            "I love it.":
                mc.name "Absolutely. Your tits look amazing in it."
                $ the_person.change_love(1)
                $ the_person.change_obedience(-2)
                the_person "You're such a pervert looking at me like that."

            "No.":
                mc.name "On you, not really."
                $ the_person.change_love(-1)
                $ the_person.change_obedience(1)
                the_person "You lying little shit. I know you love seeing me like this. You're such a pervert."
        the_person "I bet you're about to blow your load just looking at me, right?"
        if the_person.has_large_tits():
            the_person "Do you want me to take this off and show you my big, soft tits?"
        else:
            the_person "Do you want me to take this off and play with my tits for you?"
        menu:
            "Yes.":
                mc.name "Of course I do. Send me some pics."
                $ the_person.change_obedience(-1)
                the_person "I knew you would. I want you to beg me for them."
                mc.name "What?"
                the_person "I want you to beg to see my tits. Come on, you want them, right?"
                menu:
                    "Beg to see her tits.":
                        "You think about it for a moment, then give in."
                        mc.name "Fine, I'm begging you to show me your tits."
                        the_person "A little more, please."
                        if the_person.has_large_tits():
                            mc.name "All I want in life is to get a look at those huge tits. I need it so badly."
                        else:
                            mc.name "All I want in life is to get a look at your tits. I need it so badly."
                        the_person "Close..."
                        mc.name "I'm so turned on, just thinking about your tits. Please [the_person.title], I'm begging you!"
                        $ the_person.change_obedience(-2)
                        $ the_person.change_happiness(5)
                        "You wait eagerly for her response."
                        the_person "Oh my god, I can't believe you're this easy to screw with."
                        mc.name "Whatever, just send me some pics."
                        the_person "You really thought I was going to send those? Ha!"
                        the_person "Talk to you later, nerd."

                    "Refuse.":
                        mc.name "Why would I beg just to see those udders? If I wanted to see some attention starved bimbo's tits I can go online."
                        $ the_person.change_slut_temp(1)
                        the_person "Whatever nerd. You probably already blew your load in your pants."
                        "You ignore her and she doesn't message you again."

            "No.":
                mc.name "Not right now. I've got other stuff to do."
                the_person "Really? You've got to be kidding me."
                the_person "You don't want to see me spread over this bed, naked and waiting for you?"
                the_person "My poor little pussy just dripping wet, waiting for a big hard cock?"
                the_person "Just beg for it and it's yours. My tight little cunt is all yours."
                menu:
                    "Beg to see her naked.":
                        "You think about it for a moment, then give in."
                        mc.name "Fine, I'm begging you [the_person.title], let me see you naked."
                        the_person "I'm not sure I'm convinced. A little more please."
                        mc.name "All I want in life right now is to see you stripped out."
                        the_person "Close..."
                        mc.name "I'm so turned on just thinking about you. Please, I'm begging you!"
                        $ the_person.change_obedience(-4)
                        $ the_person.change_happiness(8)
                        "You wait eagerly for her response."
                        the_person "Oh my god, I'm taking a picture of this chat. I can't believe how desperate you get."
                        mc.name "What? I don't care, just send me some pics."
                        the_person "You really thought I was going to send anything? Hahahaha!"
                        the_person "Talk to you later, nerd."


                    "Refuse.":
                        mc.name "Jesus, you're looking a little desperate there [the_person.title]. I can find attention starved bimbos all over the internet if I wanted one."
                        $ the_person.change_slut_temp(2)
                        the_person "You pathetic little nerd, I bet you've just already blown your load. You should be paying me for this."
                        "You ignore her and she doesn't message you again."


    $ mc.end_text_convo()
    $ the_person.apply_outfit() #Return to her planned outfit.
    $ clear_scene()
    return
