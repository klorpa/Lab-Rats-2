# Holds all relationship dependant relationships (your girlfriend, paramour, friends, enemies, ect.)


init 1 python:
    def so_relationship_improve_requirement():
        for place in list_of_places:
            for a_person in place.people:
                if (a_person.love > 10 or employee_role in a_person.special_role) and not a_person.title is None and not a_person.relationship == "Married":
                    if not affair_role in a_person.special_role and not girlfriend_role in a_person.special_role and not mother_role in a_person.special_role and not sister_role in a_person.special_role and not cousin_role in a_person.special_role and not aunt_role in a_person.special_role:
                    # You have at least one person you know who is in a relationship. People you're having an affair never have it get better.
                    # Your also family never forms relationships, because we do that through direct story stuff.
                        return True
        return False

    def so_relationship_worsen_requirement():
        for place in list_of_places:
            for a_person in place.people:
                if (a_person.love > 10 or employee_role in a_person.special_role) and not a_person.title is None and not a_person.relationship == "Single":
                    if not mother_role in a_person.special_role and not sister_role in a_person.special_role and not cousin_role in a_person.special_role and not aunt_role in a_person.special_role:
                    # We only change thse relationships in events. If we can find anyone who meets the requirements the event can proceed.
                        return True
        return False

    so_relationship_improve_crisis = Action("Friend SO relationship improve", so_relationship_improve_requirement, "so_relationship_improve_label")
    crisis_list.append([so_relationship_improve_crisis, 3])

    so_relationship_worsen_crisis = Action("Friend SO relationship worsen", so_relationship_worsen_requirement, "so_relationship_worsen_label")
    crisis_list.append([so_relationship_worsen_crisis, 1])

label so_relationship_improve_label():
    $ potential_people = []
    python:
        for place in list_of_places:
            for a_person in place.people:
                if a_person.love > 10 and not a_person.title is None and not a_person.relationship == "Married":
                    if not affair_role in a_person.special_role and not girlfriend_role in a_person.special_role and not mother_role in a_person.special_role and not sister_role in a_person.special_role and not cousin_role in a_person.special_role and not aunt_role in a_person.special_role:
                        if a_person is not emily and a_person is not christina: #Cludge to stop them from getting in relationships. TODO: Add a flag to stop people from changing their relationship status.
                            potential_people.append(a_person)

    $ the_person = get_random_from_list(potential_people)
    if the_person is None:
        return #Something's changed and there is no longer a valid person

    $ mc.start_text_convo(the_person)
    if the_person.relationship == "Single":
        $ the_person.change_happiness(10)
        "You get a notification on your phone."
        $ guy_name = get_random_male_name()
        "[the_person.title] has just changed her status on social media. She's now in a relationship with someone named [guy_name]."
        $ the_person.relationship = "Girlfriend"
        $ the_person.SO_name = guy_name

    elif the_person.relationship == "Girlfriend":
        $ the_person.change_happiness(20)
        if the_person.love > 30: #You're a good friend.
            "You get a text from [the_person.title]."
            the_person "Hey [the_person.mc_title], I have some exciting news!"
            the_person "My boyfriend proposed, me and [the_person.SO_name] are getting married! I'm so excited, I just had to tell you!"
            menu:
                "Congratulate her.":
                    "You text back."
                    mc.name "Congratulations! I'm sure you're the happiest girl in the world."
                    $ the_person.change_love(1)
                    the_person "I am! I've got other people to tell now, talk to you later!"

                "Warn her against it.":
                    "You text back."
                    mc.name "I don't know if that's such a good idea. Do you even know him that well?"
                    "Her response is near instant."
                    the_person "What? What do you even mean by that?"
                    mc.name "I mean, what if he isn't who you think he is? Maybe he isn't the one for you."
                    $ the_person.change_happiness(-10)
                    the_person "I wasn't telling you because I wanted your opinion. If you can't be happy for me, you can at least be quiet."
                    $ the_person.change_love(-5)
                    "She seems pissed, so you take her advice and leave her alone."
        else: #You see it on social media
            "You get a notification on your phone."
            "It seems [the_person.title] has gotten engaged to her boyfriend, [the_person.SO_name]. You take a moment to add your own well wishes to her social media pages."
        $ the_person.relationship = "Fiancée"

    elif the_person.relationship == "Fiancée":
        #TODO: Add an event where you're invited to their wedding and fuck the bride.
        "You get a notification on your phone."
        "It seems [the_person.title]'s just had her wedding to her Fiancé, [the_person.SO_name]. You take a moment to add your congradulations to her wedding photo."
        $ the_person.relationship = "Married"

    $ potential_people = []
    $ mc.end_text_convo()
    return



label so_relationship_worsen_label():
    $ potential_people = []
    python:
        for place in list_of_places:
            for a_person in place.people:
                if a_person.love > 10 and not a_person.title is None and not a_person.relationship == "Single":
                    if not mother_role in a_person.special_role and not sister_role in a_person.special_role and not cousin_role in a_person.special_role and not aunt_role in a_person.special_role:
                        if a_person is not emily and a_person is not christina:
                            potential_people.append(a_person)

    $ the_person = get_random_from_list(potential_people)
    if the_person is None:
        return #Something's changed and there is no longer a valid person

    $ so_title = SO_relationship_to_title(the_person.relationship)
    if affair_role in the_person.special_role:
        "You get a call from [the_person.title]. When you pick up she sounds tired, but happy."
        the_person "Hey [the_person.mc_title], I've got some news. Me and my [so_title], [the_person.SO_name], had a fight. We aren't together any more."
        the_person "We don't have to hide what's going on between us any more."
        call transform_affair(the_person) from _call_transform_affair
        mc.name "That's good news! I'm sure you'll want some rest, so we can talk more later. I love you."
        $ the_person.change_love(5)
        the_person "I love you too. Bye."

    else:
        $ the_person.change_happiness(-20)
        "You get a notification on your phone."
        "It looks like [the_person.title] has left her [so_title] and is single now."

    $ the_person.relationship = "Single"
    $ the_person.SO_name = None
    return

init 1 python:
    def affair_dick_pic_requirement():
        if time_of_day == 3 or time_of_day == 4:
            for place in list_of_places:
                for a_person in place.people:
                    if affair_role in a_person.special_role and a_person not in mc.location.people: #Soemone is in an affair with you and wants a dic pic
                        return True
        return False

    affair_dick_pic_crisis = Action("Affair dic pic", affair_dick_pic_requirement, "affair_dick_pick_label")
    crisis_list.append([affair_dick_pic_crisis, 5])


label affair_dick_pick_label():
    $ possible_people = []
    python:
        for place in list_of_places:
            for a_person in place.people:
                if affair_role in a_person.special_role and a_person not in mc.location.people: #Soemone is in an affair with you and wants a dic pic
                    possible_people.append(a_person)
    $ the_person = get_random_from_list(possible_people)
    if the_person is None:
        return

    $ mc.start_text_convo(the_person)
    "You get a text from [the_person.title]."
    the_person "I'm so horny right now. I'm touching myself and thinking about you, [the_person.mc_title]."
    "She sends you a picture, which you immediately open up."
    $ the_person.apply_outfit(lingerie_wardrobe.pick_random_outfit(), update_taboo = True)
    $ the_person.draw_person(position = "missionary")
    "[the_person.possessive_title] is lying face up in her bed, one hand cradling a breast while the other fingers her wet pussy."
    menu:
        "Send her a dick pic back.":
            if mc.location.get_person_count() > 0:
                "You find a quiet spot and whip out your dick for a quick glamour shot."
            else:
                "You whip out your dick for a quick glamour shot."
            "[the_person.title]'s picture was enough to get you ready, but you give yourself a few strokes to make sure you're at full size."
            "You take a shot of your rock hard cock and send it off to [the_person.title] in return."
            "After a short wait you get a response."
            the_person "That's what I want! I wish I could feel that hard thing down my throat right now."
            the_person "God, I'm such a dirty fucking slut for your cock!"
            $ the_person.change_slut_temp(2)
            $ the_person.change_obedience(1)
            mc.name "Good, then be a good slut and cum your brains out for me."
            "After another short pause she messages you again."
            the_person "I just came so hard. You're so bad for me [the_person.mc_title]. Hope to see you soon."



        "Tell her you're busy.":
            "As much as you enjoy the picture, you've got important work to do. You text her back."
            mc.name "I've got work to get done [the_person.title]. Stop bothing me just because you're a bitch in heat."
            if the_person.get_opinion_score("being submissive") > 0:
                $ the_person.change_slut_temp(2)
                $ the_person.change_obedience(2)
                "There's a long pause, then she texts back."
                the_person "That is what I am. Your horny bitch, desperate for your cock!"
                the_person "Fuck, I just came so hard!"

            else:
                $ the_person.change_slut_temp(1)
                $ the_person.change_obedience(2)
                $ the_person.change_love(-1)
                "There's a long pause, then she texts you back."
                the_person "Just don't make me wait too long, I need to feel your cock again!"
    $ the_person.apply_outfit(the_person.planned_outfit)
    $ mc.end_text_convo()
    $ clear_scene()
    return

init 1 python:
    def girlfriend_nudes_requirement():
        if time_of_day == 3 or time_of_day == 4:
            for place in list_of_places:
                for a_person in place.people:
                    if girlfriend_role in a_person.special_role and a_person not in mc.location.people: #Soemone is in an affair with you and wants a dic pic
                        return True
        return False

    girlfriend_nudes_crisis = Action("Girlfriend nudes", girlfriend_nudes_requirement, "girlfriend_nudes_label")
    crisis_list.append([girlfriend_nudes_crisis, 5])

label girlfriend_nudes_label():
    $ possible_people = []
    python:
        for place in list_of_places:
            for a_person in place.people:
                if girlfriend_role in a_person.special_role and a_person not in mc.location.people: #Soemone is in an affair with you and wants a dic pic
                    possible_people.append(a_person)
    $ the_person = get_random_from_list(possible_people)
    if the_person is None:
        return

    $ mc.start_text_convo(the_person)
    if the_person.effective_sluttiness() < 20:
        "You get a text from [the_person.possessive_title]."
        the_person "Hey [the_person.mc_title]. I was just thinking about you and wanted to say hi."
        the_person "Hope we can spend some time together soon."
        mc.name "Me too, we'll talk when I have some time."

    elif the_person.effective_sluttiness() < 40:
        "You get a text from [the_person.possessive_title], followed shortly after by a video."
        the_person "Hey [the_person.mc_title]. I was playing around a little and hope this brightens your day."
        $ the_person.draw_person(position = "doggy", the_animation = missionary_bob)
        "You open up the video and see [the_person.title] on her bed, ass towards the camera. She's working her hips and shaking her ass for you."
        if the_person.age >= 35:
            the_person "You kids call this twerking, right? I think it's pretty hot."
            the_person "I could use more practice. Come by some time and maybe you can give me some advice."
        else:
            the_person "I wish I could twerk this ass for you in person. Swing by some time, okay?"

    elif the_person.effective_sluttiness() < 60:
        $ the_person.apply_outfit(lingerie_wardrobe.pick_random_outfit())
        "You get a text from [the_person.possessive_title], followed shortly by a video."
        the_person "Here's a little gift for you, hope you like it!"
        "You open the video."
        $ the_person.draw_person(position = "stand5", the_animation = blowjob_bob, animation_effect_strength = 0.8)
        "It's [the_person.title] in her room in front of a mirror. She smiles and waves at you, then bounces her tits up and down."
        $ tit_strip_list = the_person.outfit.get_tit_strip_list(visible_enough = True)
        if tit_strip_list: #She has something to strip to show off her tits more
            "She dances for a moment, then starts to strip down even more."
            python:
                for the_item in tit_strip_list:
                    the_person.draw_animated_removal(the_item, position = "stand5", the_animation = blowjob_bob, animation_effect_strength = 0.8)
                    if the_person.outfit.tits_visible():
                        renpy.say("", "She pulls her " + the_item.name + " off and lets her tits fall free.")
                        renpy.say("", "She at the camera and shakes them for you.")
                    else:
                        renpy.say("","")
            if the_person.has_large_tits():
                "Tits out, she dances a little more for you, then blows a kiss and waves goodbye. Her breasts dangle directly in front of the camera as she turns it off."
            else:
                "Tits out, she dances a little more for you, then blows a kiss and waves goodbye."

        else:
            "She dances for a moment, then blows you a kiss and waves goodbye."
        $ the_person.update_outfit_taboos()
        $ the_person.apply_outfit(the_person.planned_outfit)
    else:
        $ the_person.apply_outfit(Outfit("Nude"))
        "You get a text from [the_person.possessive_title], followed shortly by a video."
        the_person "Thinking of you, wish you were here!"
        "You open up the video."
        $ the_person.draw_person(position = "missionary", the_animation = missionary_bob, animation_effect_strength = 0.5)
        "[the_person.title] is lying naked in bed, one hand already between her legs."
        "She smiles at the camera and starts to finger herself, slowly at first but quickly picking up speed."
        "After a moment she reaches out of frame for a bringing a shiny chrome vibrator."
        "She maintains eye contact with the camera as she licks it, then sucks on it a little bit, before sliding it between her legs."
        $ the_person.draw_person(position = "missionary", the_animation = missionary_bob, animation_effect_strength = 0.75)
        "[the_person.possessive_title] arches her back as the vibrator touches her clit."
        "Before long her thighs are quivering. You watch as [the_person.title] drives herself to orgasm with her vibrator."
        "Her legs clamp down on her own hand as she cums. After a moment she relaxes, leaving the vibrator running on the bed."
        "She looks into the camera again and sighs happily, then reaches forward and ends the video."
        $ the_person.update_outfit_taboos()
        $ the_person.apply_outfit(the_person.planned_outfit)
    #TODO: A blojob/deepthroat training video, or an anal stretching video she sends you to show she's "getting ready."
    $ mc.end_text_convo()
    $ clear_scene()
    return

init 1 python:
    def friends_help_friends_be_sluts_requirement():
        if mc.is_at_work() and mc.business.is_open_for_business():
            if town_relationships.get_business_relationships(["Friend","Best Friend"]):
                return True
        return False

    friends_help_friends_be_sluts_crisis = Action("Friends Help Friends Be Sluts",friends_help_friends_be_sluts_requirement,"friends_help_friends_be_sluts_label")
    crisis_list.append([friends_help_friends_be_sluts_crisis,5])

label friends_help_friends_be_sluts_label():
    #A slutty girl helps her less slutty friend be more slutty.

    $ the_relationship = get_random_from_list(town_relationships.get_business_relationships(["Friend","Best Friend"])) #Get a random rival or nemesis relationship within the company
    if the_relationship is None:
        return
    $ person_one = None #Sluttier person
    $ person_two = None #Person being convinced to be sluttier.
    if the_relationship.person_a.effective_sluttiness() > the_relationship.person_b.effective_sluttiness():
        $ person_one = the_relationship.person_a
        $ person_two = the_relationship.person_b
    else:
        $ person_one = the_relationship.person_b
        $ person_two = the_relationship.person_a


    $ the_group = GroupDisplayManager([person_one, person_two], primary_speaker = person_one)
    if person_one.effective_sluttiness() < 30: #If our slutty person isn't very slutty in the first place.
        "You decide to take a walk, both to stretch your legs and to make sure your staff are staying on task."
        "When you peek in the break room you see [person_one.title] and [person_two.title] chatting with each other as they make coffee."
        $ the_group.draw_group()
        menu:
            "Stop to listen.":
                person_one "... Following so far? Then he takes your..."
                "You can't quite hear what they're talking about. [person_two.title] gasps and blushes."
                $ the_group.draw_person(person_two)
                person_two "No! Does that even..."
                $ the_group.draw_person(person_one)
                person_one "It feels amazing! Or so I've been told."
                $ the_group.draw_person(person_two)
                "[person_two.title] shakes her head in disbelief and turns away. When she notices you in the doorway she gasps and stammers."
                person_two "[person_two.mc_title], we were just... I was just... How much did you hear of that?"
                person_two "Oh no, this is so embarrassing!"
                $ the_group.draw_person(person_one)
                person_one "[person_two.title], relax. Sorry [person_one.mc_title], we were just chatting about some girl stuff."
                person_one "She doesn't have much experience, so I was just explaining..."
                $ the_group.draw_person(person_two)
                person_two "[person_one.title]! [person_two.mc_title] doesn't need to hear about this."
                mc.name "This isn't highschool, I'm not going to punish you for being bad girls and talking about sex."
                $ the_group.draw_person(person_one)
                person_one "Well maybe she wants to be punished a little. Maybe a quick spanking?"
                "[person_one.possessive_title] slaps [person_two.title]'s butt."
                $ the_group.draw_person(person_two)
                person_two "Hey! That's... Come on [person_one.title], we should get back to work. Goodbye [person_one.mc_title]."
                $ clear_scene()
                $ person_one.draw_person()
                "She hurries out of the room, blushing."
                $ person_one.change_slut_temp(2)
                person_one "She's so cute when she's embarrassed. See you around [person_two.mc_title]."
            "Ignore them.":
                "You leave them to their discussion and circle back to your desk."

    elif person_one.effective_sluttiness() < 60: #Our sluttiest is moderately slutty
        "You decide to take a walk, both to stretch your legs and to make sure your staff are staying on task."
        "You're passing by the break room when an unusual noise catches your attention. It sounds like distant and passionate feminine moaning."
        $ the_group.draw_group(position = "walking_away")
        "Intrigued, you peak your head in and see [person_one.title] and [person_two.title]. They are staring intently at [person_one.title]'s phone while they stand next to the coffee machine."
        menu:
            "Investigate.":
                if person_two.effective_sluttiness() < 30: #But the other girl is low sluttiness.
                    # The sluttier is showing her friend some porn. She panics/is embarrassed when you walk in and see what it is
                    "You clear your throat and [person_two.title] yelps and spins around."
                    $ the_group.draw_person(person_one, make_primary = False)
                    $ the_group.draw_person(person_two)
                    person_two "[person_two.mc_title]! I was... We were..."
                    $ the_group.draw_person(person_one)
                    "[person_one.title] rolls her eyes and speaks up."
                    person_one "I was just showing [person_two.title] a video I found last night. I thought she might be into it."
                    person_one "Do you want to see?"
                    $ the_group.draw_person(person_two)
                    person_two "[person_one.title]! I'm sorry [person_two.mc_title], I know this isn't what we should be doing here."
                    mc.name "Why would I care? You're taking a break and relaxing the way you want to."
                    "The moans from the phone grow louder. You notice [person_one.possessive_title] has turned her attention back to the screen."
                    mc.name "[person_one.title] seems to have the right idea."
                    $ the_group.draw_person(person_one)
                    person_one "Yeah, just relax [person_two.title]. You said you had something you wanted to show me too, right?"
                    "She hands the phone to [person_two.title], who looks at you and takes it hesitantly."
                    $ the_group.draw_person(person_two)
                    person_two "You're sure?"
                    mc.name "Of course I'm sure, but if I'm making you self conscious I'll give you some privacy."
                    mc.name "Once you're done your break I expect to see you both back at work."
                    $ person_two.change_slut_temp(3)
                    $ person_two.change_obedience(2)
                    "You leave the room, and a few seconds later you can hear them resume watching porn together."


                else: #And her friend is pretty slutty too.
                    # You catch them watching some porn on break, the less slutty is slightly worried about you seeing but neither mind a ton.
                    "You clear your throat and both girls look up."
                    $ the_group.draw_group()
                    person_one "Oh, hey [person_one.mc_title]."
                    $ the_group.draw_person(person_two)
                    person_two "Hi [person_two.mc_title], we were just taking our break together."
                    "The moaning on the phone grows louder and [person_two.title] seems suddenly self conscious."
                    person_two "I hope you don't mind that we're watching... [person_one.title] just wanted to show me something quickly."
                    mc.name "I certainly don't mind."
                    $ the_group.draw_person(person_two)
                    person_one "I told you it was fine. I found this last night and thought it was so hot. Do you want to take a look [person_one.mc_title]."
                    "She holds her phone up for you to see. You lean in close and join the ladies watching porn on [person_one.title]'s phone."
                    # Discover something new about her sexuality
                    $ person_one.discover_opinion(person_one.get_random_opinion(include_known = True, include_sexy = True, include_normal = False, only_positive = True))
                    $ person_one.discover_opinion(person_one.get_random_opinion(include_known = True, include_sexy = True, include_normal = False, only_positive = True))
                    $ person_one.change_love(1)
                    $ person_two.change_slut_temp(3+person_two.get_opinion_score("public sex"))
                    $ person_two.change_love(1)
                    "After a few minutes the video ends and you've discovered a few things about [person_one.title]'s sexual preferences."
                    $ the_group.draw_person(person_two)
                    person_two "You're right [person_one.title], that was hot. Can you send that to me for later?"
                    $ the_group.draw_person(person_one)
                    person_one "Sure thing. We should be getting to work before [person_one.mc_title] gets too distracted though."
                    "Her eyes drift conspicuously down your body to the noticeable bulge in your pants."
                    $ the_group.draw_person(person_two)
                    person_two "Uh, right. Talk to you later [person_two.mc_title]."
                    "You watch them walk out then get back to work."

            "Ignore them.":
                "You leave them to their discussion and circle back to your desk."


    else:
        "You decide to take a walk, both to stretch your legs and to make sure your staff are staying on task."
        "When you pass by the break room you overhear [person_one.title] and [person_two.title] chatting at the coffee machine."
        menu:
            "Investigate.":
                "You stop at the door and listen for a moment."
                if person_two.effective_sluttiness() < 20:
                    # The sluttier girl is talking about how horny she's feeling today when you walk in. Her friend seems embarrassed to be hearing about it.
                    # The sluttier girl then spanks/plays with the less slutty girls ass for your benefit.
                    # When you walk in the sluttier girl makes some passes at you that her friend apologizes for, but that you reenforce.
                    $ the_group.draw_group()
                    person_one "I can't wait to get home, I've been feeling so worked up all day I just want to get naked and have some me time."
                    person_one "I got a new vibrator and it's mind blowing. I want to be riding it all day long now."
                    $ the_group.draw_person(person_two)
                    person_two "[person_one.title], you're such a slut!"
                    $ the_group.draw_person(person_one)
                    person_one "Oh come on, so are you. Wouldn't you like to be at home right now with a vibe pressed up against your clit?"
                    $ the_group.draw_person(person_two)
                    "[person_two.title] laughes and shrugs, then suddenly tenses up and starts to blush when she notices you at the door."
                    person_two "Uh, hello [person_two.mc_title]. I was just... Uhh..."
                    $ the_group.draw_person(person_one)
                    person_one "Hey [person_one.mc_title], don't mind her, she's just horny and thinking about her vibrator at home."
                    $ the_group.draw_person(person_two)
                    person_two "Shut up, [person_two.mc_title] doesn't want to hear about this."
                    $ the_group.draw_person(person_one)
                    person_one "Sure he does, men love to hear about slutty, horny women. Right [person_one.mc_title]?"
                    $ the_group.draw_person(person_two)
                    person_two "I'm so sorry [person_two.mc_title], she doesn't know what she's saying."
                    mc.name "I think she does, because I agree, especially when they're as beautiful as you two."
                    $ the_group.draw_person(person_one)
                    person_one "See? Come on, we should probably get back to work. Nice seeing you [person_one.mc_title]."
                    $ the_group.draw_person(person_two)
                    person_two "Uh... See you around."
                    "They head for the door. [person_one.title] pauses and waits for [person_two.title] to pass her."
                    $ the_group.draw_person(person_one, position = "back_peek")
                    "She looks at you and winks, then gives her friend a hard slap on the ass."
                    person_one "After you!"
                    $ the_group.set_primary(person_two)
                    $ the_group.draw_group(position = "walking_away")
                    person_two "Ah! You..."
                    "You hear them chatting and laughing as they head back to work."
                    $ person_one.change_obedience(1)
                    $ person_two.change_slut_temp(3)
                    $ person_two.change_obedience(2)

                elif person_two.effective_sluttiness() < 40:
                    # The sluttier girl is talking about the less slutty girls tits when you walk in. She wants you to give a comparison, the less slutty girl begrudgingly agrees
                    # Note: At high love she hints that she's doing this as a favour to you.
                    $ the_group.draw_group(person_one)
                    if rank_tits(person_one.tits) < rank_tits(person_two.tits):
                        # The slutty girl wants smaller, perkier tits.
                        person_one "Look at them though, they're the perfect shape. Mine just don't have the same perk yours do."
                        $ the_group.draw_person(person_two)
                        person_two "But they're so nice and big, I'd kill to have them like that. I bet they're nice and soft, too."
                        $ the_group.draw_person(person_one)
                        person_one "Want to give them a feel? I... Oh, hey [person_one.mc_title]."

                    else:
                        # The slutty girl wants larger tits.
                        person_one "Look at those puppies, they're the perfect size. I'd kill for a pair of tits like yours."
                        $ the_group.draw_person(person_two)
                        person_two "They're big, but yours look perkier. I know lots of guys who are into that."
                        $ the_group.draw_person(person_one)
                        person_one "I still just want to grab yours by the handful and... Oh, hey [person_one.mc_title]."
                    "[person_one.possessive_title] notices you at the door."
                    $ the_group.draw_person(person_two)
                    person_two "Ah, hi... We were just getting back to work, right [person_one.title]?"
                    $ the_group.draw_person(person_one)
                    person_one "Yeah, in a moment. [person_one.mc_title], you're just who we need right now to settle this for us."
                    mc.name "Settle what?"
                    person_one "[person_two.title] won't admit she's got the better tits of the two of us. Talk some sense into her for me."
                    $ the_group.draw_person(person_two)
                    person_two "Oh god, what are you getting us into."
                    menu:
                        "[person_one.title] has nicer tits.": #She's already slutty, but gets a love boost
                            "You take a moment to consider, then nod towards [person_one.title]."
                            if rank_tits(person_one.tits) < rank_tits(person_two.tits):
                                mc.name "I've got to give it to [person_one.title]. I like them perky."
                            else:
                                mc.name "I've got to give it to [person_one.title]. I like them big."
                            $ person_one.change_happiness(5)
                            $ person_one.change_love(1 + person_one.get_opinion_score("showing her tits"))
                            $ the_group.draw_person(person_two)
                            person_two "See? Now that we've settled that, can we get back to work. It feels weird to be talking about our breasts with our boss."
                            $ the_group.draw_person(person_one)
                            person_one "I suppose. Thanks for the help [person_one.mc_title]."

                        "[person_two.title] has nicer tits.": # She gets a sluttiness boost along with a small love boost.
                            if rank_tits(person_one.tits) > rank_tits(person_two.tits):
                                mc.name "I've got to give it to [person_two.title]. I like them perky."
                            else:
                                mc.name "I've got to give it to [person_two.title]. I like them big."
                            $ the_group.draw_person(person_one)
                            person_one "Exactly! You're just going to have to accept that you're smoking hot [person_two.title]."
                            $ the_group.draw_person(person_two)
                            $ person_two.change_slut_temp(2 + person_one.get_opinion_score("showing her tits"))
                            $ person_two.change_love(1 + person_one.get_opinion_score("showing her tits"))
                            person_two "Fine, I guess my tits are pretty nice. Shouldn't we be getting back to work."
                            $ the_group.draw_person(person_one)
                            person_one "I suppose. Thanks for the help [person_one.mc_title]."
                            "She gives you a smile and a wink, then leaves the room with [person_two.title]."

                        "I'm going to need a closer look." if not person_one.outfit.tits_visible() or not person_two.outfit.tits_visible(): #Requires high obedience, sluttiness, or a uniform policy for the less slutty girl.
                            mc.name "Hmm. It's a close call, I'm going to need to take a moment for this and get a better look."
                            $ the_group.draw_person(person_one)
                            if person_one.outfit.tits_visible():
                                # If her tits are already out then it must be her friend who has a shirt on.
                                "[person_one.title] thrusts her chest forward and displays her tits proudly."
                                person_one "Well, here are mine. Come on [person_two.title], whip 'em out!"
                            else:
                                person_one "Of course."
                                $ strip_list = person_one.outfit.get_half_off_to_tits_list()
                                if strip_list:
                                    $ generalised_strip_description(person_one, strip_list, half_off_instead = True, group_display = the_group)

                                else: #We need to strip something off completely.
                                    $ strip_list = person_one.outfit.get_tit_strip_list()
                                    $ generalised_strip_description(person_one, strip_list, group_display = the_group)

                                if person_two.outfit.tits_visible():
                                    $ person_one.break_taboo("bare_tits")
                                    person_one "There, what do you think now [person_one.mc_title]?"




                            if not person_two.outfit.tits_visible():
                                $ the_group.draw_person(person_two)
                                person_two "Oh my god, are we really doing this?"
                                $ the_group.draw_person(person_one)
                                person_one "Come on, cut loose a little! It's just a little friendly competition, right?"
                                $ the_group.draw_person(person_two)
                                $ strip_list = person_two.outfit.get_half_off_to_tits_list()
                                $ half_off_instead = True
                                if not strip_list:
                                    $ half_off_instead = False
                                    $ strip_list = person_two.outfit.get_tit_strip_list()

                                $ the_item = strip_list[0]
                                #$ the_item = person_two.outfit.remove_random_upper(top_layer_first = True, do_not_remove = True)
                                if person_two.get_opinion_score("showing her tits") > 0:
                                    $ person_two.discover_opinion("showing her tits")
                                    "[person_two.title] bites her lip and giggles."
                                    person_two "Fine! I can't believe I'm doing this!"
                                    if half_off_instead:
                                        "She starts to strip down, eagerly pulling her [the_item.display_name] up."
                                    else:
                                        "She starts to strip down, eagerly pulling off her [the_item.display_name]."
                                    $ person_two.change_slut_temp(person_two.discover_opinion("showing her tits"))
                                elif person_two.obedience >= 120:
                                    person_two "Do you really want me to do this [person_two.mc_title]?"
                                    mc.name "I do, now show them to us."
                                    if half_off_instead:
                                        "She nods meekly and starts to pull her [the_item.display_name] up."
                                    else:
                                        "She nods meekly and starts to strip down, starting with her [the_item.display_name]."
                                    $ person_two.change_obedience(1)

                                elif corporate_enforced_nudity_policy.is_active() or maximal_arousal_uniform_policy.is_active():
                                    "[person_two.title] hesitates for a second."
                                    mc.name "Just consider this a temporary change to your uniform, [person_two.title]. I could have you walking around topless all day if I wanted to."
                                    person_two "Fine, I guess I did agree to that..."
                                    if half_off_instead:
                                        "She starts to pull her [the_item.display_name] up."
                                    else:
                                        "She starts to strip down, starting with her [the_item.display_name]."
                                    $ person_two.change_obedience(1)
                                else:
                                    person_two "I can't do this, [person_one.title]! You're crazy!"
                                    $ the_group.draw_person(person_one)
                                    "[person_one.title] jiggles her tits."
                                    person_one "Look at me, I'm doing it! Here, let me help you."
                                    $ the_group.draw_person(person_two)
                                    "[person_one.title] moves behind [person_two.title] and starts to dress her down, starting with her [the_item.name]."


                                $ generalised_strip_description(person_two, strip_list, half_off_instead = half_off_instead, group_display = the_group)
                                    # if half_off_instead:
                                    #     for clothing in strip_list: # TODO: Loops like this should probably have some way of stripping only what is required, and half-offing the rest
                                    #         the_group.draw_animated_removal(person_one, the_clothing = clothing, half_off_instead = True)
                                    #         if person_one.outfit.tits_visible(): #Last loop
                                    #             if person_one.has_large_tits():
                                    #                 renpy.say("", "Her breasts drop free as she pulls her " + clothing.display_name + " up, jiggling briefly.")
                                    #             else:
                                    #                 renpy.say("", "She pulls her " + clothing.display_name + " up, letting her well shaped breasts jump free.")
                                    #         else:
                                    #             renpy.say("",person_one.title + " pulls her " + clothing.display_name + " up and out of the way.")
                                    #
                                    # else: #We need to strip something off completely.
                                    #     strip_list = person_one.outfit.get_tit_strip_list()
                                    #     for clothing in strip_list:
                                    #         the_group.draw_animated_removal(person_one, the_clothing = clothing)
                                    #         if person_one.outfit.tits_visible(): #Last loop
                                    #             if person_one.has_large_tits():
                                    #                 renpy.say("", "Her breasts drop free as she pulls her " + clothing.display_name + " off. They jiggle briefly before coming to a stop.")
                                    #             else:
                                    #                 renpy.say("", "She pulls her " + clothing.display_name + " off, and her well shaped breasts jump free as soon as possible.")
                                    #         else:
                                    #             renpy.say("",person_one.title + " pulls her " + clothing.display_name + " off and puts it to the side.")

                                if person_two.get_opinion_score("showing her tits") > 0:
                                    "When she has her tits out she crosses her arms in front of her in a small attempt to preserve her modesty."
                                    $ the_group.draw_person(person_one)
                                    person_one "[person_one.mc_title] can't see them if you keep them covered up. Here..."
                                    $ the_group.draw_person(person_two)
                                    "[person_one.title] takes her friend's hands and move them to her hips, then cups them and gives them a squeeze in front of you."
                                else:
                                    "When she has her tits out she puts her hands on her hips and smiles at you, exposed and ready for your inspection."
                                    $ the_group.draw_person(person_one)
                                    person_one "That's it, look at these puppies [person_one.title]..."
                                    $ the_group.draw_person(person_two)
                                    "She gets behind her friend and cups her breasts, giving them a squeeze."

                                $ person_one.break_taboo("bare_tits")
                                person_two "Hey, go easy on them! Well then [person_two.mc_title], who's your pick? Me or [person_one.title]?"
                            menu:
                                "[person_one.title] has nicer tits.": #She's already slutty, but gets a love boost
                                    "You take a moment to consider both of their naked racks, then nod towards [person_one.title]."
                                    if rank_tits(person_one.tits) < rank_tits(person_two.tits):
                                        mc.name "I've got to give it to [person_one.title]. I like them perky."
                                    else:
                                        mc.name "I've got to give it to [person_one.title]. I like them big."
                                    $ the_group.draw_person(person_one)
                                    $ person_one.change_happiness(5)
                                    $ person_one.change_love(1 + person_one.get_opinion_score("showing her tits"))
                                    $ person_two.change_slut_temp(2 + person_two.get_opinion_score("showing her tits"))
                                    person_two "So I got naked just to lose, huh?"
                                    $ the_group.draw_person(person_one)
                                    person_one "I guess you did, but at least you get to see some nice tits."
                                    "She jiggles her chest at her friend, who laughs and waves her off."
                                    $ the_group.draw_person(person_one)
                                    person_two "Uh huh. Come on, you've had your fun. We need to get back to work."

                                "[person_two.title] has nicer tits.": # She gets a sluttiness boost along with a small love boost.
                                    if rank_tits(person_one.tits) > rank_tits(person_two.tits):
                                        mc.name "I've got to give it to [person_two.title]. I like them perky."
                                    else:
                                        mc.name "I've got to give it to [person_two.title]. I like them big."
                                    $ the_group.draw_person(person_two)
                                    person_two "Well, at least I didn't get naked just to lose."
                                    $ person_two.change_slut_temp(4 + person_one.get_opinion_score("showing her tits"))
                                    $ person_two.change_love(1 + person_one.get_opinion_score("showing her tits"))
                                    $ the_group.draw_person(person_one)
                                    person_one "You've got some award winning tits on you, you should be proud of them!"
                                    $ the_group.draw_person(person_two)
                                    person_two "I feel like [person_two.mc_title] was the real winner here. Come on, we should be getting back to work."
                            $ the_group.draw_person(person_one)
                            person_one "Yeah, you're probably right."
                            "[person_one.title] gives you a smile and a wink, then leaves the room with [person_two.title]."
                            $ person_one.review_outfit()
                            $ person_two.review_outfit()

                        "Punish them for inappropriate behaviour." if office_punishment.is_active():
                            mc.name "[person_one.title], [person_two.title], this is completely inappropriate, even if you're on your break."
                            mc.name "I don't have any choice but to record this for disciplinary action later."
                            $ person_one.add_infraction(infraction.inappropriate_behaviour_factory())
                            $ person_two.add_infraction(Infraction.inappropriate_behaviour_factory())
                            $ the_group.draw_person(person_one)
                            person_one "Really? I..."
                            $ the_group.draw_person(person_two)
                            person_two "Don't get us in any more trouble [person_one.title]. Sorry [person_two.mc_title], we'll get back to work right away."
                            $ the_group.draw_person(person_one)
                            person_one "Ugh, whatever. Come on [person_two.title], let's go."
                            "They turn and leave the room together."


                else: #She wants to suck your dick, but is embarrassed about it.
                    $ the_group.draw_group()
                    "You're thinking about taking a break and stretching your legs when you see [person_one.title] and [person_two.title] through your office door."
                    "They're talking quietly with each other, occasionally glancing in your direction. When [person_two.title] sees you watching she looks away quickly."
                    "[person_one.title] stands up and grabs her friend's hand, pulling her out of her chair. They walk over to you together."
                    person_one "[person_one.mc_title], could me and [person_two.title] talk to you privately for a moment?"
                    if person_two.effective_sluttiness("sucking_cock") < 50: #She's embarrassed, but wants to do it
                        $ the_group.draw_person(person_two)
                        person_two "It's nothing important, it could probably wait until later. In fact, never mind at all."
                        $ the_group.draw_person(person_one)
                        person_one "[person_two.title], I know you want to do this. Don't chicken out now."
                        mc.name "I can spare a moment. Close the door."
                        "[person_one.title] closes the door, then stands behind [person_two.title]."
                        mc.name "So, what can I help you two with?"
                        $ the_group.draw_person(person_two)
                        person_two "I... I mean, we... Uh..."
                        $ the_group.draw_person(person_one)
                        person_one "She's very nervous, let me her out help out."
                        if person_two.sex_record.get("Blowjobs", 0) == 0:
                            person_one "[person_two.title] has always wanted to suck your cock, but was too scared to ask."
                        else:
                            person_two "[person_one.title] really liked sucking your cock and wants to do it again, but was too scared to ask."
                        $ the_group.draw_person(person_two)
                        if person_two.get_opinion_score("giving blowjobs") < 0:
                            $ person_two.discover_opinion("giving blowjobs")
                            person_two "I actually don't like giving blowjobs, but [person_one.title] says it's an important skill for a woman to have."
                        else:
                            "[person_two.possessive_title] nods, blushing intensely."
                            person_two "I swear I don't normally do things like this..."

                    else: #She's a major slut herself and wants to get some dick down her throat.
                        $ the_group.draw_person(person_two)
                        person_two "It won't take long, I promise."
                        mc.name "I can spare a moment. Close the door."
                        "[person_one.title] closes the door, then stands behind [person_two.title]."
                        mc.name "So, what can I help you two with?"
                        person_two "I was talking to [person_one.title] and we started talking about your cock..."
                        if person_two.sex_record.get("Blowjobs", 0) > 0:
                            person_two "It brought back some good memories, so I was hoping you'd let me suck you off."
                        else:
                            person_two "I haven't had it in my mouth before, and I really want to. Would you let me suck you off?"


                    menu:
                        "Let [person_one.title] give you a blowjob.":
                            mc.name "I'm not about to say no to an offer like that."
                            $ the_group.draw_person(person_one)
                            if girlfriend_role in person_one.special_role or affair_role in person_one.special_role:
                                person_one "I didn't think you would sweetheart."
                                "[person_one.title] leans over your desk and gives you a kiss, then whispers in your ear."
                                person_one "A little gift from me. You two have fun."
                                "She smiles and steps out of the room, leaving you and [person_two.title] alone."

                            else:
                                person_one "I didn't think you would. You two enjoy yourselves."
                                "She gives [person_two.title] a smack on the ass as she leaves the room."
                                person_one "Go get him girl."

                            $ clear_scene()
                            $ person_two.draw_person()
                            call fuck_person(person_two, start_position = blowjob,  position_locked = True, affair_ask_after = True) from _call_fuck_person_18
                            $ the_report = _return
                            if the_report.get("guy orgasms", 0) > 0:
                                "You sit down in your office chair, thoroughly drained. [person_two.title] smiles, seemingly proud of her work."
                                mc.name "So, was that everything you wanted it to be?"
                                person_two "It was fun, I can't wait to tell [person_one.title] all about it."

                            else:
                                "You sit down in your office chair and sigh."
                                person_two "I'm sorry, I'm not doing a good job, am I?"
                                mc.name "You were doing fine, I'm just not in the mood. You should get back to work."
                                $ person_two.change_happiness(-5)
                            $ person_two.review_outfit(dialogue = False)
                            "[person_two.possessive_title] takes a moment to get herself tidied up, then steps out of your office."

                        "Decline her offer.":
                            mc.name "I'm flattered, but I'm not in the mood right now."
                            person_two "Of course, sorry I even brought it up [person_two.mc_title]!"
                            "She hurries out of your office. [person_one.title] shakes her head and sighs."
                            $ clear_scene()
                            $ person_one.draw_person()
                            person_one "Really? I bring you a cute girl to suck your dick and you're not in the mood? I'll never understand men..."
                            "She shrugs and leaves your office, following her friend."


                        "Punish them for inappropriate behaviour." if office_punishment.is_active():
                            mc.name "[person_one.title], [person_two.title], I expected better from both of you."
                            mc.name "This is completely inappropriate, I'm going to have to write both of you up for this."
                            $ person_one.add_infraction(infraction.inappropriate_behaviour_factory())
                            $ person_two.add_infraction(Infraction.inappropriate_behaviour_factory())
                            person_two "I... Of course, I'm sorry I even brought it up [person_two.mc_title]!"
                            "She hurries out of your office. [person_one.title] sighs and rolls her eyes."
                            $ clear_scene()
                            $ person_one.draw_person()
                            person_one "Really? I bring you a cute girl to suck your dick and you decide you need to punish both of us? What more do you want?"
                            mc.name "I'm sorry, but rules are rules. You didn't leave me much of a choice."
                            person_one "Whatever, I need to go make sure [person_one.title] is fine."
                            "She turns and leaves your office, following after her friend."

            "Ignore them.":
                "You leave them to their discussion and circle back to your desk."



    $ clear_scene()
    return

init 1 python:
    def work_relationship_change_crisis_requirement():
        if mc.business.is_open_for_business():
            if mc.business.get_employee_count() >= 2: #Quick check to avoid doing a full array check on a starting company
                if town_relationships.get_business_relationships(types = "Acquaintance"):
                    return True
        return False
    work_relationship_change_crisis = Action("Work Relationship Change Crisis", work_relationship_change_crisis_requirement, "work_relationship_change_label")
    crisis_list.append([work_relationship_change_crisis,12])

label work_relationship_change_label():
    $ the_relationship = get_random_from_list(town_relationships.get_business_relationships())
    if the_relationship is None:
        return

    if renpy.random.randint(0,1) == 0:
        $ person_one = the_relationship.person_a
        $ person_two = the_relationship.person_b
    else:
        $ person_one = the_relationship.person_b
        $ person_two = the_relationship.person_a

    $ friend_chance = 50
    python:
        for an_opinion in person_one.opinions:
            if person_one.get_opinion_score(an_opinion) == person_two.get_opinion_score(an_opinion):
                friend_chance += 10
            elif (person_one.get_opinion_score(an_opinion) > 0 and person_two.get_opinion_score(an_opinion) < 0) or (person_two.get_opinion_score(an_opinion) > 0 and person_one.get_opinion_score(an_opinion) < 0):
                friend_chance += -10

        friend_chance += (person_one.get_opinion_score("small talk")*5) + (person_two.get_opinion_score("small talk")*5)


    if renpy.random.randint(0,100) < friend_chance:
        #Their relationship improves
        $ town_relationships.improve_relationship(person_one, person_two)
        if mc.is_at_work():
            "While working you notice [person_one.title] and [person_two.title] are spending more time together. They seem to have become friends!"
    else:
        #Their relationship worsens
        $ town_relationships.worsen_relationship(person_one, person_two)
        if mc.is_at_work():
            "While working you notice [person_one.title] and [person_two.title] aren't getting along with each other. They seem to have developed an unfriendly rivalry."

    return
