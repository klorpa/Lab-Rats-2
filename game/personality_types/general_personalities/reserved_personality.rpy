### PERSONALITY CHARACTERISTICS ###
init 1300:
    python:
        def reserved_titles(the_person):
            if the_person.love > 10:
                return the_person.name
            else:
                return "Mrs."+the_person.last_name
        def reserved_possessive_titles(the_person):
            return reserved_titles(the_person)
        def reserved_player_titles(the_person):
            return mc.name
        reserved_personality = Personality("reserved", #Mom style personality
        common_likes = ["pants", "research work", "HR work", "Mondays", "working", "makeup", "the colour blue", "conservative outfits","jazz","classical"],
        common_sexy_likes = ["missionary style sex", "kissing", "lingerie", "being submissive", "vaginal sex", "creampies", "giving tit fucks"],
        common_dislikes = ["the colour red", "marketing work", "flirting"],
        common_sexy_dislikes = ["masturbating", "giving head", "getting head", "doggy style sex", "public sex", "not wearing underwear", "not wearing anything", "bareback sex", "cum facials"],
        titles_function = reserved_titles, possessive_titles_function = reserved_possessive_titles, player_titles_function = reserved_player_titles,
        insta_chance = 0, dikdok_chance = 0)

        list_of_personalities.append(reserved_personality)


### DIALOGUE ###
################################
##### Reserved Personality #####
################################
# <editor-fold
label reserved_introduction(the_person):
    mc.name "Excuse me, could I bother you for a moment?"
    "She turns around and looks at you quizzically."
    $ the_person.set_title("???")
    the_person "I suppose you could. How can I help you?"
    mc.name "I'm so sorry, I know this is silly but I just couldn't let you walk by without knowing your name."
    "She laughs and rolls her eyes."
    $ title_choice = get_random_title(the_person)
    $ formatted_title = the_person.create_formatted_title(title_choice)
    the_person "Well then, I suppose I shouldn't disappoint you. You can call me [formatted_title]."
    $ the_person.set_title(title_choice)
    $ the_person.set_possessive_title(get_random_possessive_title(the_person))
    "[the_person.possessive_title] holds her hand out to shake yours."
    the_person "What about you, what's your name?"
    return

label reserved_greetings(the_person):
    if the_person.love < 0:
        the_person "... Do you need something?"
    elif the_person.happiness < 90:
        the_person "Hello..."
    else:
        if the_person.sluttiness > 60:
            if the_person.obedience > 130:
                the_person "Hello [the_person.mc_title]."
            else:
                the_person "Hello, are you feeling as good as you're looking today?"
        else:
            if the_person.obedience > 130:
                the_person "Hello [the_person.mc_title]."
            else:
                the_person "Hello, I hope you're doing well."
    return

label reserved_sex_responses_foreplay(the_person):
    if the_person.arousal < 25:
        if the_person.sluttiness > 50:
            the_person "Mmm, you know just what I like, don't you?"
        else:
            the_person "Oh my... that feels very good, [the_person.mc_title]!"

    elif the_person.arousal < 50:
        if the_person.sluttiness > 50:
            "[the_person.title] closes her eyes and lets out a loud, sensual moan."
        else:
            the_person "Keep doing that [the_person.mc_title]... Wow, you're good!"

    elif the_person.arousal < 75:
        if the_person.sluttiness > 50:
            the_person "Oh gods above taht feels amazing!"
        else:
            the_person "Oh lord... I could get use to you touching me like this!"
    else:
        if the_person.sluttiness > 50:
            if the_person.relationship == "Single":
                the_person "Touch me [the_person.mc_title], I want you to touch me!"
            else:
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person "I should feel bad... but my [so_title] never touches me this way!"
                the_person "I need this, so badly!"
        else:
            the_person "I want you to keep touching me. I never thought you could make me feel this way, but I want more of it!"

    return

label reserved_sex_responses_oral(the_person):
    if the_person.arousal < 25:
        if the_person.sluttiness > 50:
            the_person "Oh [the_person.mc_title], you're so good to me."
        else:
            the_person "Oh my... that feels..."
            "She sighs happily."
            the_person "Good!"

    elif the_person.arousal < 50:
        if the_person.sluttiness > 50:
            the_person "Yes, just like that! Mmm!"
        else:
            the_person "Keep doing that [the_person.mc_title], it's making me feel... very aroused."

    elif the_person.arousal < 75:
        if the_person.sluttiness > 50:
            the_person "Mmm, you really know how to put that tongue of yours to good use. That feels amazing!"
        else:
            the_person "Oh lord... your tongue is addictive, I just want more of it!"
    else:
        if the_person.sluttiness > 50:
            if the_person.relationship == "Single":
                the_person "Oh I need this so badly [the_person.mc_title]! If you keep going you'll make me climax!"
            else:
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person "I should feel bad, but you make me feel so good and my [so_title] never does this for me!"
        else:
            the_person "Oh sweet lord in heaven... This feeling is intoxicating!"

    return

label reserved_sex_responses_vaginal(the_person):
    if the_person.arousal < 25:
        if the_person.sluttiness > 50:
            the_person "Mmm, I love feeling you inside of me!"
        else:
            the_person "Oh lord, you're so big... Whew!"

    elif the_person.arousal < 50:
        if the_person.sluttiness > 50:
            "[the_person.title] closes her eyes and lets out a loud, sensual moan."
        else:
            the_person "Oh that feels very good, keep doing that!"

    elif the_person.arousal < 75:
        if the_person.sluttiness > 50:
            the_person "Yes! Oh god yes, fuck me!"
        else:
            the_person "Oh lord your... cock feels so big!"
    else:
        if the_person.sluttiness > 50:
            if the_person.relationship == "Single":

                the_person "Keep... keep going [the_person.mc_title]! I'm going to climax soon!"
            else:
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person "Keep going! My [so_title]'s tiny dick never makes me climax and I want it so badly!"
                the_person "I should feel bad, but all I want is your cock in me right now!"
        else:
            "[the_person.title]'s face is flush as she pants and gasps."
    return

label reserved_sex_responses_anal(the_person):
    if the_person.arousal < 25:
        if the_person.sluttiness > 50:
            the_person "Mmm, you feel so big when you're inside me like this."
        else:
            the_person "Be gentle, it feel like you're going to tear me in half!"

    elif the_person.arousal < 50:
        if the_person.sluttiness > 50:
            the_person "Give it to me, [the_person.mc_title], give me every last inch!"
        else:
            the_person "Oh god! Oww!"

    elif the_person.arousal < 75:
        if the_person.sluttiness > 50:
            the_person "I hope my ass isn't too tight for you, I don't want you to cum early."
        else:
            the_person "I don't think I will be able to walk straight after this!"
    else:
        if the_person.sluttiness > 50:
            if the_person.relationship == "Single":
                the_person "You're cock feels so stuffed inside me! Keep going, I might actually climax!"
            else:
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person "My [so_title] always wanted to try anal, but I told him it would never happen. My ass belongs to you , [the_person.mc_title]!"
        else:
            the_person "Oh lord, this is actually starting to feel good... I might be able to climax after all!"

    return

label reserved_climax_responses_foreplay(the_person):
    if the_person.sluttiness > 50:
        the_person "Oh my... I'm going to... cum!"
    else:
        the_person "I... Oh my god, this feeling is..."
        "She pauses and moans excitedly."
        the_person "So good!"
    return

label reserved_climax_responses_oral(the_person):
    if the_person.sluttiness > 70:
        the_person "Keep going [the_person.mc_title], you're going to make me..."
        "She barely finishes her sentence as her body shivers with pleasure."
        the_person "... Orgasm!"
    else:
        the_person "This feeling... Oh... Oh!"
        "Her eyes close and she takes a deep breath."
    return

label reserved_climax_responses_vaginal(the_person):
    if the_person.sluttiness > 70:
        the_person "You're going to... Ah! You're going to make me climax [the_person.mc_title]!"
        "She closes her eyes as she tenses up. She freezes for a long second, then lets out a long, slow breath."
    else:
        the_person "Oh, I think I'm about to... Oh yes!"
    return

label reserved_climax_responses_anal(the_person):
    if the_person.sluttiness > 70:
        the_person "Mmmm, fuck me [the_person.mc_title], fuck my ass and make me cum!"
    else:
        the_person "Oh lord, I think I'm going to climax. You're going to make me cum by fucking my ass!"
    return

label reserved_clothing_accept(the_person):
    if the_person.obedience > 130:
        the_person "You're too kind [the_person.mc_title]. I'll add it to my wardrobe right away."
    else:
        the_person "For me? Oh, I'm not use to getting gifts like this..."
    return

label reserved_clothing_reject(the_person):
    if the_person.obedience > 130:
        the_person "You're too kind [the_person.mc_title], really. I don't think I can accept such a... beautiful gift from you though."
    else:
        if the_person.sluttiness > 60:
            the_person "It's very nice [the_person.mc_title], but I think it's a little too revealing, even for me. Maybe when I'm feeling a little more bold, okay?"
        else:
            the_person "Really [the_person.mc_title]? Just suggesting that I would wear something like that is a little too forward, don't you think?"
    return

label reserved_clothing_review(the_person):
    if the_person.should_wear_uniform():
        the_person "One moment [the_person.mc_title], I need to get my uniform sorted out."
    elif the_person.obedience > 130:
        the_person "I'm such a mess right now [the_person.mc_title], I just have to go and get tidied up for you. I'll be back in a moment."
    else:
        if the_person.sluttiness > 40:
            the_person "Oh dear, my clothes are just a mess after all of that. Not that I'm complaining, of course, but I should go get tidied up. Back in a moment."
        else:
            the_person "Oh, I look like such a mess right now. I'll be back in a moment."
    return

label reserved_strip_reject(the_person, the_clothing, strip_type = "Full"):
    if the_person.obedience > 130:
        the_person "I'm sorry [the_person.mc_title], but I think my [the_clothing.display_name] should stay where it is for now. For modesty's sake."
    elif the_person.obedience < 70:
        the_person "That's going to stay right there for now. I'll decide when I want it to come off, okay?."
    else:
        the_person "[the_person.mc_title], I don't feel comfortable taking that off. Just leave it put."
    return

label reserved_strip_obedience_accept(the_person, the_clothing, strip_type = "Full"):
    "[the_person.title] speaks quietly as you start to move her [the_clothing.display_name]."
    if the_person.obedience > 130:
        the_person "I... I'm sorry, but I don't know if you should take that off [the_person.mc_title]..."
    else:
        the_person "I really shouldn't take that off [the_person.mc_title]..."
    return

label reserved_grope_body_reject(the_person):
    if the_person.effective_sluttiness("touching_body") < 5: #Fail point for touching shoulder
        "She shoots you a cold look and steps back, away from your touch."
        the_person "I'm sorry, I'd prefer if you didn't touch me without permission."
        mc.name "Of course, I was just trying to be friendly."
        the_person "I understand, it just makes me... Uncomfortable."
        "She seems more guarded, but you both try and move past the awkward moment."
    else: #Fail point for touching waist
        "[the_person.title] shifts and tries to move away from you."
        the_person "Sorry, but could you... Move your hand? I'm just not comfortable with this."
        "You take a step back and pull your hand away."
        mc.name "Of course, no problem. Just trying to be friendly."
        "She seems unconvinced, but decides not to say anything else."
    return

label reserved_sex_accept(the_person):
    if the_person.sluttiness > 70:
        if the_person.obedience < 70:
            the_person "Good, I didn't want to be the one to suggest it but that sounds like fun."
        else:
            the_person "Mmm, you think we should give that a try? I'm feeling adventurous today, lets go."
    else:
        the_person "Oh, I know I shouldn't [the_person.mc_title]... but I think you've managed to convince me."
    return

label reserved_sex_obedience_accept(the_person):
    if the_person.sluttiness > 70:
        the_person "I shouldn't... I really shouldn't. But I know you want me, and I think I want you too. Promise you'll make me feel good too?"
    else:
        if the_person.obedience > 130:
            the_person "Okay [the_person.mc_title], if that's what you want. I'll do what I can to serve you."
        else:
            the_person "If it were anyone other than you I'd say no [the_person.mc_title]. Don't get too use to this, okay?"
    return

label reserved_sex_gentle_reject(the_person):
    if the_person.sluttiness > 50:
        the_person "Wait, a lady must be romanced first [the_person.mc_title]. At least get me warmed up first."
    else:
        the_person "This doesn't seem like the kind of thing a proper lady would do. Lets do something else, please."
    return

label reserved_sex_angry_reject(the_person):
    if not the_person.relationship == "Single":
        $ so_title = SO_relationship_to_title(the_person.relationship)
        the_person "Excuse me? I have a wonderful [so_title] and I would never dream of doing anything to betray him!"
        "She glares at you and shakes her head."
        the_person "I need some space, [the_person.mc_title]. I didn't think you were that kind of man."
    elif the_person.sluttiness < 20:
        the_person "Excuse me? Do I look like some sort of prostitute?"
        the_person "Get away from me, you're lucky I don't turn you into the police for that! Give me some space, I don't want to talk after that."
    else:
        the_person "Um, what do you think you're doing [the_person.mc_title]? That's disgusting, and certainly no way to act around a lady!"
    return

label reserved_seduction_response(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 50:
            the_person "Hello [the_person.mc_title], is there something I can help you with? Something of a personal nature perhaps?"
        else:
            the_person "Hello [the_person.mc_title], is there something I can help you with?"
    else:
        if the_person.sluttiness > 50:
            the_person "You've got that look in your eye again. there's just no satisfying you, is there? You're lucky I'm such a willing participant."
        elif the_person.sluttiness > 10:
            the_person "Oh [the_person.mc_title], you always know how to make a woman feel wanted..."
        else:
            the_person "[the_person.mc_title], isn't that a little bit forward of you? I'm not saying no though..."
    return

label reserved_seduction_accept_crowded(the_person):
    if the_person.relationship == "Single":
        if the_person.sluttiness < 20:
            the_person "I don't think anyone will miss us for a few minutes. We can... get closer and see where things go."
        elif the_person.sluttiness < 50:
            the_person "Come on, let's go find someplace quiet then."
        else:
            the_person "Well then, do you want to take me right here or should we get a room?"
    else:
        $ so_title = SO_relationship_to_title(the_person.relationship)
        if the_person.sluttiness + (5*the_person.get_opinion_score("cheating on men")) > 50:
            the_person "Well you have my attention. We should find some place private, unless you want my [so_title] to hear about us."
        else:
            the_person "I know I shouldn't... We need to keep it quiet, so my [so_title] doesn't find out."
    return

label reserved_seduction_accept_alone(the_person):
    if the_person.relationship == "Single":
        if the_person.sluttiness < 20:
            the_person "How about we start with a little kissing and just see where it goes."
        elif the_person.sluttiness < 50:
            the_person "Oh [the_person.mc_title], you're going to make me blush! Come over here!"
        else:
            the_person "Mmm, that sounds so nice [the_person.mc_title]. Don't make me wait, get over here!"
    else:
        $ so_title = SO_relationship_to_title(the_person.relationship)
        if the_person.sluttiness + (5*the_person.get_opinion_score("cheating on men")) > 50:
            the_person "Come here [the_person.mc_title], I want you to touch me in ways my [so_title] never does!"
        else:
            the_person "This is so improper."
            "She locks eyes with you, deadly serious."
            the_person "You can never tell my [so_title] about this, is that understood?"
            "You nod and she melts into your arms."
    return

label reserved_seduction_refuse(the_person):
    if the_person.sluttiness < 20:
        the_person "Oh... I'm sorry [the_person.mc_title] but I couldn't imagine doing anything like that."

    elif the_person.sluttiness < 50:
        the_person "I'm sorry, but I'm just not in the mood for any fooling around right now. Maybe some other time though."

    else:
        the_person "Oh [the_person.mc_title], that sounds like a lot of fun, but I think we should save it for another time."
    return

label reserved_flirt_response(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 50:
            the_person "It would be so improper, but for you I'm sure I could arange something special."
        else:
            the_person "Thank you for the compliment, [the_person.mc_title], I appreciate it."

    elif not the_person.relationship == "Single":
        $so_title = SO_relationship_to_title(the_person.relationship)
        if the_person.sluttiness + (the_person.get_opinion_score("cheating on men")*5) > 50:
            the_person "I'm glad you appreciate it. My [so_title] hardly even looks at me any more."
            "She spins, giving you a full look at her body."
            the_person "His loss, right?"
        else:
            the_person "[the_person.mc_title], I should remind you I have a [so_title]. We can be friendly with each other, but that's where it should end."
            "She seems more worried about maintaining appearances than she was about actually flirting with you."
    else:
        if the_person.sluttiness > 50:
            the_person "Oh [the_person.mc_title], that's so naughty of you to even think about..."
            "[the_person.title] winks at you and spins, giving you a full look at her body."
            the_person "How will I ever get you to contain yourself?"
        else:
            the_person "Please [the_person.mc_title], a woman like me likes a little romance in her relationships. At least buy me dinner first."
    return

label reserved_flirt_response_low(the_person):
    if the_person.is_wearing_uniform():
        if the_person.judge_outfit(the_person.outfit):
            # She's in uniform and likes how it looks.
            the_person "Thank you [the_person.mc_title]. I think these are nice uniforms as well."
            mc.name "It helps having such an attractive employees to wear it."
            "[the_person.possessive_title] smiles."
            the_person "Well, thank you. I appreciate the complement."
        else:
            #She's in uniform, but she thinks it's a little too slutty.
            if the_person.outfit.vagina_visible():
                # Her pussy is on display.
                the_person "It's not much of an outfit at all though."
                the_person "I understand it's the company uniform, but it would be nice to have a little more coverage."
                mc.name "It will take some getting use to, but I think it would be a shame to cover up your wonderful figure."
                "[the_person.possessive_title] doesn't seem so sure, but she smiles and nods anyways."

            elif the_person.outfit.tits_visible():
                # Her tits are out
                if the_person.has_large_tits():
                    the_person "Thank you, but I can tell this uniform was designed by a man."
                    the_person "Larger chested women, like myself, appreciate a little more support in their outfits."
                else:
                    the_person "Thank you, but I do hope you'll consider a uniform with a proper top in the future."
                    the_person "It still doesn't feel natural having my... breasts so visible."
                mc.name "I understand it's a little uncomfortable, but I'm sure you'll get use to it."
                the_person "Yes, given enough time I'm sure I will."

            elif the_person.outfit.underwear_visible():
                # Her underwear is visible.
                the_person "Thank you. I always feel a touch self-concious when I put it on. I wish it kept me a little more covered."
                mc.name "I know it can take some getting use to, but you look fantastic in it. You're a perfect fit for it."
                "[the_person.possessive_title] doesn't seem so sure, but she smiles and nods anyways."

            else:
                # It's just generally slutty.
                "[the_person.possessive_title] smiles warmly."
                the_person "Thank you, although I don't think I would ever wear this if it wasn't company policy."
                mc.name "Well you look fantastic in it either way. Maybe you should rethink your normal wardrobe."
                the_person "I'll think about it."

    else:
        #She's in her own outfit.
        "[the_person.possessive_title] seems caught off guard by the compliment."
        the_person "Oh, thank you! I'm not wearing anything special, it's just one of my normal outfits."
        mc.name "Well, you make it look good."
        "She smiles and laughs self-conciously."
        the_person "Oh stop."
    return

label reserved_flirt_response_mid(the_person):
    if the_person.is_wearing_uniform():
        if the_person.judge_outfit(the_person.outfit):
            if the_person.outfit.tits_visible():
                the_person "What it shows off most are my breasts. I'm not complaining though. Between you and me, I kind of like it."
                "She winks and shakes her shoulders, jiggling her tits for you."
            else:
                the_person "With my body and your fashion taste, how could I look bad? These uniforms are very flattering."
                mc.name "It's easy to make a beautiful model look wonderful."
                if the_person.effective_sluttiness() > 20:
                    $ the_person.draw_person(position = "back_peek")
                    the_person "It makes my butt look pretty good too. I don't think that was an accident."
                    "She gives her ass a little shake."
                    mc.name "It would be a crime to not try and show your ass off."
                    $ the_person.draw_person()
                "She smiles softly."
                the_person "You know just what to say to make a woman feel special."

        else:
            # the_person "I think it shows off a little too much!"
            if the_person.outfit.vagina_visible():
                the_person "What doesn't this outfit show off!"

            elif the_person.outfit.tits_visible():
                the_person "It certainly shows off my breasts!"

            else:
                the_person "And it shows off a {i}lot{/i} of my body!"

            the_person "I don't mind it so much if it's just me and you, but when there are other people around I wish it kept me a little more covered."
            mc.name "It may take some time to adjust, but with enough time you'll be perfectly comfortable in it."
            "She smiles and nods."
            the_person "You're right, of course. If you think it's the best option for the company I trust you."
    else:
        if the_person.effective_sluttiness() < 20 and mc.location.get_person_count() > 1:
            "[the_person.possessive_title] smiles, then glances around self-conciously."
            the_person "Keep your voice down [the_person.mc_title], there are other people around."
            mc.name "I'm sure they're all thinking the same thing."
            "She rolls her eyes and laughs softly."
            the_person "Maybe they are, but it's still embarrassing."
            the_person "You'll have better luck if you save your flattery for when we're alone."
            mc.name "I'll keep that in mind."

        else:
            "[the_person.possessive_title] gives a subtle smile and nods her head."
            the_person "Thank you [the_person.mc_title]. I'm glad you like it... And me."
            the_person "What do you think of it from the back? It's hard for me to get a good look."
            $ the_person.draw_person(position = "back_peek")
            "She turns and bends over a little bit, accentuating her butt."
            if not the_person.outfit.wearing_panties() and not the_person.outfit.vagina_visible(): #Not wearing underwear, but you cna't see so she coments on it.
                the_person "My panties were always leaving unpleasant lines, so I had to stop wearing them. I hope you can't tell."
            else:
                the_person "Well?"
            mc.name "You look just as fantastic from the back as you do from the front."
            $ the_person.draw_person()
            "She turns back and smiles warmly."
    return

label reserved_flirt_response_high(the_person):
    if mc.location.get_person_count() > 1 and the_person.effective_sluttiness() < (25 - (5*the_person.get_opinion_score("public_sex"))): # There are other people here, if she's not slutty she asks if you want to find somewhere quiet
        the_person "[the_person.mc_title], there are people around."
        "She bites her lip and leans close to you, whispering in your ear."
        the_person "But if we were alone, maybe we could figure something out..."
        menu:
            "Find someplace quiet.":
                mc.name "Follow me."
                "[the_person.possessive_title] nods and follows a step behind you."
                "After searching for a couple of minutes you find a quiet, private space."
                "Once you're alone you put one hand around her waist, pulling her close against you. She looks into your eyes."
                the_person "Well? What now?"

                if the_person.has_taboo("kissing"):
                    $ the_person.call_dialogue("kissing_taboo_break")
                    $ the_person.break_taboo("kissing")
                    "You lean in and kiss her. She closes her eyes and leans her body against yours."
                else:
                    "You answer with a kiss. She closes her eyes and leans her body against yours."
                call fuck_person(the_person, private = True, start_position = kissing, skip_intro = True) from _call_fuck_person_51
                $ the_report = _return
                $ the_person.call_dialogue("sex_review", the_report = the_report)

            "Just flirt.":
                mc.name "I'll just have to figure out how to get you alone then. Any thoughts?"
                the_person "You're a smart man, you'll figure something out."
                "She leans away from you again and smiles mischeviously."

    else:
        if mc.location.get_person_count() == 1: #She's shy but you're alone
            "[the_person.title] blushes and stammers out a response."
            the_person "I... I don't know what you mean [the_person.mc_title]."
            mc.name "It's just the two of us, you don't need to hide how you feel. I feel the same way."
            "She nods and takes a deep breath, steadying herself."
            the_person "Okay. You're right. What... do you want to do then?"

        else:  #You're not alone, but she doesn't care.
            the_person "Well I wouldn't want you to go crazy. You'll just have to do something to get me out of this outfit then..."
            if the_person.has_large_tits(): #Bounces her tits for you
                $ the_person.draw_person(the_animation = blowjob_bob)
                "[the_person.possessive_title] bites her lip sensually and grabs her boobs, jiggling them for you."

            else: #No big tits, so she can't bounce them (as much
                "[the_person.possessive_title] bites her lip sensually and looks you up and down, as if mentally undressing you."

            the_person "Well? What do you want to do?"

        menu:
            "Kiss her.":
                $ the_person.draw_person()
                "You step close to [the_person.title] and put an arm around her waist."

                if the_person.has_taboo("kissing"):
                    $ the_person.call_dialogue("kissing_taboo_break")
                    $ the_person.break_taboo("kissing")
                    "You lean in and kiss her. She presses her body up against yours."
                else:
                    "When you lean in and kiss her she responds by pressing her body tight against you."
                call fuck_person(the_person, start_position = kissing, skip_intro = True) from _call_fuck_person_52
                $ the_report = _return
                $ the_person.call_dialogue("sex_review", the_report = the_report)

            "Just flirt.":
                $ the_person.draw_person()
                mc.name "Nothing right now, but I've got a few ideas for later."
                "If [the_person.title] is disappointed she does a good job hiding it. She nods and smiles."
                the_person "Well maybe if you take me out for dinner we can talk about those ideas. I'm interested to hear about them."
    return

label reserved_flirt_response_girlfriend(the_person):
    # Lead in: mc.name "You're so beautiful [the_person.title], I'm so lucky to have a woman like you in my life."
    if mc.location.get_person_count() > 1:
        # There are other people around, so she'll only start making out with you if she's slutty.
        if the_person.effective_sluttiness("kissing") < (25 - (5*the_person.get_opinion_score("public_sex"))):
            # Not very slutty, so she wants to find somewhere private
            "[the_person.title] smiles happily."
            the_person "Oh, well thank you [the_person.mc_title]. You're so sweet."
            "She leans in and gives you a quick peck on the cheek."
            the_person "I wish we had a little more privacy. Oh well, maybe later."
            menu:
                "Find someplace quiet.":
                    mc.name "Why wait until later? Come on."
                    "You take [the_person.possessive_title]'s hand. She hesitates for a moment, then follows as you lead her away."
                    "After a few minutes of searching you find a quiet spot. You put your arm around [the_person.title]'s waist and pull her close to you."
                    mc.name "So, what did you want that privacy for again?"
                    the_person "Oh, a few things. Let's start with this..."
                    "She leans in and kisses you passionately while rubbing her body against you."
                    call fuck_person(the_person, private = True, start_position = kissing, skip_intro = True) from _call_fuck_person_66
                    $ the_report = _return
                    $ the_person.call_dialogue("sex_review", the_report = the_report)

                "Just flirt.":
                    mc.name "Aw, you're going to make me wait? That's so cruel."
                    "You reach around and place a hand on [the_person.possessive_title]'s ass, rubbing it gently."
                    "She sighs and bites her lip, then clears her thraot and glances around to see if anyone else noticed."
                    the_person "I'll make sure to make it worth the wait, but let's take it easy while other people are around."
                    "You give her butt one last squeeze, then slide your hand off."

        else:
            # the_person "Oh [the_person, mc_title], you're so sweet. Come on, kiss me!"
            "She smiles and sighs happily."
            the_person "Ahh, you're so sweet. Here..."
            "[the_person.possessive_title] leans in and kisses you. Her lips lingering against yours for a few long seconds."
            the_person "Was that nice? You're very nice to kiss."
            menu:
                "Make out.":
                    "You respond by putting your arm around her waist and pulling her tight against you."
                    "You kiss her, and she eagerly grinds her body against you."
                    call fuck_person(the_person, start_position = kissing, skip_intro = True) from _call_fuck_person_67
                    $ the_report = _return
                    $ the_person.call_dialogue("sex_review", the_report = the_report)

                "Just flirt.":
                    mc.name "It was very nice. I've got some other nice things for you to kiss too, if you'd like."
                    if the_person.effective_sluttiness("sucking_cock") >= 60 or the_person.get_opinion_score("giving blowjobs") > 0:
                        "She bites her lip and runs her eyes up and down your body."
                        the_person "Mmmm, stop it [the_person.mc_title]. You're going to get me all wet in public."
                        "You reach around and place your hand on her ass, rubbing it gently."
                        mc.name "Well we don't want that. I'll keep my thoughts to myself then."
                        "You give her butt one last squeeze, then slide your hand away."

                    else:
                        "She laughs and glances around."
                        the_person "Oh my god, [the_person.mc_title]! Save it for later though, I like what you're thinking..."
    else:
        # You're alone, so she's open to fooling around.
        "She smiles happily."
        the_person "Oh, well thank you [the_person.mc_title]. I'm lucky to have you too."
        "[the_person.possessive_title] leans in and kisses you. Her lips linger against yours for a few seconds."
        menu:
            "Kiss her more.":
                "You put your arm around her waist and pull her against you, returning her sensual kiss."
                "She presses her body against you and hugs you back. Her hands run down your hips and grab at your ass as you make out."
                call fuck_person(the_person, start_position = kissing, skip_intro = True) from _call_fuck_person_68
                $ the_report = _return
                $ the_person.call_dialogue("sex_review", the_report = the_report)

            "Just flirt.":
                "You reach around [the_person.title] and place a hand on her ass, rubbing it gently. She sighs and leans her body against you."
                the_person "Mmm, that's nice... Maybe when we have some more time together we can take this further."
                mc.name "That sounds like fun. I'm looking forward to it."
                "You give her butt a light slap, then move your hand away."

    return

label reserved_flirt_response_affair(the_person):
    # Lead in: mc.name "You look so good today [the_person.title], you're making me want to do some very naughty things to you."
    $ so_title = SO_relationship_to_title(the_person.relationship) # "husband", "boyfriend", etc.
    if mc.location.get_person_count() > 1: #There are other people around, she's nervous about people finding out what you're doing.
        if (the_person.get_opinion_score("cheating on men") *15) + the_person.effective_sluttiness() > 50: #SHe's turned on by flirting in public or doesn't think anything is wrong with it
            the_person "Oh [the_person.mc_title], stop. If you keep talking like that you're going to get me turned on."
            mc.name "And what would be so bad about that?"
            the_person "It would be so frustrating being in public and not being able to do anything to get my satisfaction."
            menu:
                "Find someplace quiet.":
                    mc.name "Then let's go find someplace that isn't public. Come on, follow me."
                    "[the_person.possessive_title] glances around, then follows behind you as you search for a quiet spot."
                    "Soon enough you find a place where you and [the_person.title] can be alone."
                    "Neither of you say anything as you put your hands around her and pull her into a tight embrace."
                    "You kiss her, slowly and sensually. She moans and presses her body against you in return."
                    call fuck_person(the_person, private = True, start_position = kissing, skip_intro = True) from _call_fuck_person_69
                    $ the_report = _return
                    $ the_person.call_dialogue("sex_review", the_report = the_report)

                "Just flirt.":
                    mc.name "Well that would just be cruel of me..."
                    "You put your arm around [the_person.possessive_title] and rest your hand on her ass."
                    mc.name "...If I got you all excited thinking about the next time I'm going to fuck you."
                    "She leans her body against yours for a moment and sighs happily. You give her butt a final slap and let go of her."

        else: #She's shy or nervous about being discovered
            "[the_person.possessive_title] glances around, then glares at you sternly."
            the_person "[the_person.mc_title], you can't talk like that when there are other people around."
            the_person "You don't want my [so_title] to hear any rumours, do you? If he gets suspicious you might not get to see me so much..."
            "She runs a hand discretely along your arm."
            the_person "That would be such a shame, wouldn't it?"
            mc.name "Alright, I'll be more careful."
            the_person "Thank you. Just hold onto all those naughty thoughts and we can check them off one by one when we're alone."
    else:
        the_person "Oh is that so [the_person.mc_title]? Well, maybe you need to work out some of those naughty instincts..."
        "She stands close to you and runs her hand teasingly along your chest."
        menu:
            "Feel her up.":
                mc.name "That sounds like a good idea. Come here."
                "You wrap your arms around [the_person.possessive_title]'s waist, resting your hands on her ass."
                "Then you pull her tight against you, squeezing her tight butt. She sighs happily and starts to kiss your neck."
                "You massage her ass for a moment, then spin her around and cup a tit with one hand. You move your other hand down to caress her inner thigh."
                call fuck_person(the_person, private = True, start_position = standing_grope, skip_intro = True) from _call_fuck_person_70
                $ the_report = _return
                $ the_person.call_dialogue("sex_review", the_report = the_report)

            "Just flirt.":
                mc.name "I want to, but I'm going to have to wait until we have more time together for that."
                "Her hand moves lower down, brushing over your crotch and sending a brief shiver up your spine."
                the_person "I understand. When we have the chance we'll take our time and really enjoy each other."
    return

label reserved_flirt_response_text(the_person):
    mc.name "Hey [the_person.title]. Hope you're doing well."
    mc.name "I was thinking of you and wanted to talk."
    "There's a brief pause, then she texts back."
    if the_person.has_role(affair_role):
        the_person "If you were here we could do more than just talk."
        the_person "I hope you don't make me wait too long to see you again."
        mc.name "It won't be long. Promise."

    elif the_person.has_role(girlfriend_role):
        the_person "It's sweet of you to think of me. I hope we can see each other soon."
        the_person "I want to spend more time with you in person. Texting isn't the same."
        mc.name "It won't be long, I promise."

    elif the_person.love < 40:
        if the_person.effective_sluttiness() > the_person.love:
            the_person "Oh? And what did you want to talk about?"
        else:
            the_person "Oh, that's nice of you to say."
            the_person "What did you want to talk to me about."

    else:
        if the_person.effective_sluttiness() > the_person.love:
            the_person "Mhmm, what to tell me what sort of dirty things you were thinking about me?"
            the_person "That would be somthing fun to talk about."

        else:
            the_person "It's sweet of you to be thinking of me."
            the_person "I'd love to chat, what would you like to talk about?"
    return

label reserved_cum_face(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 60:
            the_person "Ah, that's always a pleasure, [the_person.mc_title]."
        else:
            the_person "Well that's certainly a lot. I hope that means I did a satisfactory job."
    else:
        if the_person.sluttiness > 80:
            the_person "Oh [the_person.mc_title], what are you doing to me? I'm beginning to like looking like this!"
        else:
            the_person "Oh god [the_person.mc_title], could you imagine if someone saw me like this? I really should go and get cleaned up."
    return

label reserved_cum_mouth(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 60:
            the_person "Mmm, always a pleasure to taste you [the_person.mc_title]. I hope you had a good time."
        else:
            "[the_person.title] puckers her lips, obviously not happy with the taste but too polite to say anything."
    else:
        if the_person.sluttiness > 80:
            the_person "You're making me act like such a slut [the_person.mc_title], what would the other women think if they knew what I just did?"
        else:
            the_person "Well, at least there's no mess to clean up. I need to go wash my mouth out after that though."
    return

label reserved_cum_pullout(the_person):
    # Lead in: "I'm going to cum!"
    if mc.condom:
        if the_person.wants_creampie() and the_person.get_opinion_score("creampies") > 0 and not the_person.has_taboo("condomless_sex"): #TODO: FIgure out we want any more requirements for this to fire.
            if the_person.event_triggers_dict.get("preg_knows", False):
                the_person "I'm already pregnant, do you want to cum inside me again?"
            elif the_person.on_birth_control:
                the_person "Do you want to cum inside of me? I shouldn't, but..."
                "She moans desperately."
                the_person "I want you to take that condom off and pump me full of your seed!"
            else:
                "She pants eagerly."
                the_person "Take... Take off the condom, I want you to cum inside of me!"
                the_person "I don't care if you get me pregnant, I need it [the_person.mc_title]!"

                # the_person "Oh fuck... Do you want to knock me up?"

            menu: #TODO: Add a varient of this normally so you can stealth a girl (don't do that in real life, it's super fucked up).
                "Take off the condom.":
                    "You don't have much time to spare. You pull out, barely clearing her pussy, and pull the condom off as quickly as you can manage."
                    $ mc.condom = False
                "Leave it on.":
                    "You ignore [the_person.possessive_title]'s cum-drunk offer and keep the condom in place."

        else:
            the_person "Finish whenever you're ready [the_person.mc_title]!"

    else:
        if the_person.wants_creampie():
            if the_person.event_triggers_dict.get("preg_knows", False): #She's already knocked up, so who cares!
                the_person "Cum for me [the_person.mc_title], I want you to cum for me!"
            elif the_person.get_opinion_score("creampies") > 0:
                "[the_person.possessive_title] moans happily."
                if the_person.on_birth_control: #She just likes creampies.
                    the_person "Oh [the_person.mc_title], I want you to cum inside me! I want to feel every last drop!"
                else: #Yeah, she's not on BC and asking for you to creampie her. She's looking to get pregnant.
                    the_person "Oh [the_person.mc_title], I want you cum inside me and get me pregnant! I want you to make me a mother!"
            elif the_person.on_birth_control: #She's on the pill, so she's probably fine
                the_person "Cum for me! I'm on birth control, you can let it out wherever you want!"
                $ the_person.update_birth_control_knowledge()
            else: #Too distracted to care about getting pregnant or not. Oh well, what could go wrong?
                the_person "Cum for me [the_person.mc_title], I want you to cum for me!"
        else:
            if not the_person.on_birth_control: #You need to pull out, I'm not on the pill!
                the_person "Wait! You need to pull out, I'm not taking birth control!"
                $ the_person.update_birth_control_knowledge()

            elif the_person.get_opinion_score("creampies") < 0:
                the_person "I want you to pull out, okay? You can finish somewhere else!"

            else:
                the_person "We should be safe, you should pull out and finish somewhere else!"
    return

label reserved_cum_condom(the_person):
    if the_person.effective_sluttiness() > 75 or the_person.get_opinion_score("creampies") > 0:
        the_person "Oh... your seed is so close to me. Just a thin, thin condom in the way..."
    else:
        the_person "I can feel your seed through the condom. Well done, there's a lot of it."
    return

label reserved_cum_vagina(the_person):
    if the_person.has_taboo("creampie"):
        $ the_person.call_dialogue("creampie_taboo_break")
        $ the_person.break_taboo("creampie")
        return

    if the_person.wants_creampie():
        if the_person.event_triggers_dict.get("preg_knows", False):
            the_person "Oh my... There's so much of it..."
            "She closes her eyes and sighs happily."
            the_person "It's no mystery how you got me pregnant."

        elif the_person.on_birth_control:
            if the_person.relationship != "Single":
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person "You've making such a mess of my pussy. I never let my [so_title] do this to me."
                "She closes her eyes and sighs happily as you cum inside of her."
                the_person "Oh [the_person.mc_title], look what you've done."
            else:
                the_person "Oh [the_person.mc_title]... I can feel your cum inside me. It's so warm."
                "She closes her eyes and sighs happily as you cum."

        elif the_person.effective_sluttiness() > 75 or the_person.get_opinion_score("creampies") > 0:
            if the_person.relationship != "Single":
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person "Yes, give me all of your cum!"
                the_person "If I become pregnant I can say it's my [so_title]'s. I'm sure he would believe it."
            else:
                the_person "Mmm, your semen is so nice and warm. I wonder how potent it is. You might have gotten me pregnant, you know."
        else:
            if the_person.relationship != "Single":
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person "Oh my... That's a lot of cum. It feels so nice."
                the_person "I hope my [so_title] doesn't mind if I get pregnant."

            else:
                the_person "Oh my... That's a lot of cum. It feels so nice."
                the_person "I wonder if today was a risky day? I haven't been keeping track."


    else: #She's angry
        if not the_person.on_birth_control:
            if the_person.relationship != "Single":
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person "Oh no... You need to cum outside of me [the_person.mc_title]."
                the_person "What would I tell my [so_title] if I got pregnant? He might not believe it's his!"
            else:
                the_person "Oh no... You need to cum outside of me [the_person.mc_title]."
                the_person "I'm in no position to be getting pregnant."
                the_person "Well, I suppose you have me in the literal position to get pregnant, but you know what I mean."

        elif the_person.relationship != "Single":
            $ so_title = SO_relationship_to_title(the_person.relationship)
            the_person "[the_person.mc_title], I told you to pull out!"
            the_person "I know you're having a good time, but I still have an [so_title]. There are boundries."

        elif the_person.get_opinion_score("creampies") < 0:
            the_person "[the_person.mc_title], I told you to pull out. Now look at what a mess you've made... It's everywhere."

        else:
            the_person "[the_person.mc_title], I told you to pull out. I guess you just lost control."

    return

label reserved_cum_anal(the_person):
    if the_person.sluttiness > 75 or the_person.get_opinion_score("anal creampies") > 0:
        the_person "Cum inside me [the_person.mc_title], fill my ass with your cum!"
    else:
        the_person "Oh lord, I hope I'm ready for this!"
    return

label reserved_suprised_exclaim(the_person):
    $rando = renpy.random.choice(["Oh my!","Oh, that's not good!", "Whoa!", "Ah!", "My word!", "Oops!", "Bah!", "Dangnabbit!"])
    the_person "[rando]"
    return

label reserved_talk_busy(the_person):
    if the_person.obedience > 120:
        the_person "I'd love to chat some more, but I've already spent far to much time getting distracted. Maybe we can catch up some other day, okay?"
    else:
        the_person "Sorry to interupt, but I've got some work I really need to see to. I'd love to catch up some other time though."
    return

label reserved_sex_strip(the_person):
    if the_person.sluttiness < 20:
        if the_person.arousal < 50:
            the_person "I think I can do away with this for a few minutes..."
        else:
            the_person "Oh, I bet this has been in your way the whole time..."

    elif the_person.sluttiness < 60:
        if the_person.arousal < 50:
            the_person "I think I'm past the point of needing this..."
        else:
            the_person "I don't need this any more, one second!"

    else:
        if the_person.arousal < 50:
            the_person "One moment, I'm wearing entirely too much right now."
        else:
            the_person "I need this off, I want to feel you against more of me!"

    return

label reserved_sex_watch(the_person, the_sex_person, the_position):
    if the_person.sluttiness < the_position.slut_requirement - 20:
        $ the_person.draw_person(emotion = "angry")
        the_person "Oh my god, I can't believe you're doing that here in front of everyone. Don't either of you have any decency?"
        $ the_person.change_obedience(-2)
        $ the_person.change_happiness(-1)
        "[the_person.title] looks away while you and [the_sex_person.name] [the_position.verb]."

    elif the_person.sluttiness < the_position.slut_requirement - 10:
        $ the_person.draw_person()
        $ the_person.change_happiness(-1)
        "[the_person.title] shakes her head and tries to avoid watching you and [the_sex_person.name] [the_position.verb]."

    elif the_person.sluttiness < the_position.slut_requirement:
        $ the_person.draw_person()
        $ change_report = the_person.change_slut_temp(1)
        "[the_person.title] tries to avert her gaze, but keeps glancing over while you and [the_sex_person.name] [the_position.verb]."

    elif the_person.sluttiness >= the_position.slut_requirement and the_person.sluttiness < the_position.slut_cap:
        $ the_person.draw_person()
        the_person "Oh my..."
        $ change_report = the_person.change_slut_temp(2)
        "[the_person.title] watches quietly while you and [the_sex_person.name] [the_position.verb]."

    else:
        $ the_person.draw_person(emotion = "happy")
        the_person "Glad to see you two are having a good time. [the_person.mc_title], careful you aren't too rough with her."
        "[the_person.title] watches quietly while you and [the_sex_person.name] [the_position.verb]."
    return

label reserved_being_watched(the_person, the_watcher, the_position):
    if the_person.sluttiness >= the_position.slut_cap and the_watcher.sluttiness >= the_position.slut_cap:
        #They agree you should give it to her harder
        the_person "It's okay [the_person.mc_title], you don't have to be gentle with me."
        $ the_person.change_arousal(1)
        "[the_person.title] seems turned on by [the_watcher.title] watching you and her [the_position.verb]."

    elif the_person.sluttiness >= the_position.slut_cap and the_watcher.sluttiness < the_position.slut_requirement:
        #She's super slutty and doesn't care what people think.
        "[the_person.title] ignores [the_watcher.title] and keeps [the_position.verb] you."

    elif the_person.sluttiness >= the_position.slut_cap and the_watcher.sluttiness < the_position.slut_cap:
        #She's super slutty and encourages the watcher to be slutty.
        the_person "Mmm, come on [the_person.mc_title], let's give [the_watcher.title] a show!"
        $ the_person.change_arousal(1)
        "[the_person.title] seems turned on by [the_watcher.title] watching you and her [the_position.verb]."

    elif the_person.sluttiness < the_position.slut_cap and the_watcher.sluttiness >= the_position.slut_cap:
        #She's into it and encouraged by the slut watching her.
        the_person "Being watched shouldn't... I didn't think it would feel so good!"
        $ the_person.change_arousal(1)
        "[the_person.title] seems turned on by [the_watcher.title] watching you and her [the_position.verb]."

    elif the_person.sluttiness < the_position.slut_cap and the_watcher.sluttiness < the_position.slut_requirement:
        #She's into it but shamed by the prude watching her.
        the_person "Maybe [the_watcher.title] is right, we shouldn't be doing this..."
        $ the_person.change_arousal(-1)
        $ the_person.change_slut_temp(-1)
        "[the_person.title] seems uncomfortable with [the_watcher.title] nearby."

    else: #the_person.sluttiness < the_position.slut_cap and the_watcher.sluttiness < the_position.slut_cap:
        #They're both into it but not fanatical about it.
        the_person "Oh [the_watcher.title], you shouldn't be watching me do this..."
        $ the_person.change_arousal(1)
        $ the_person.change_slut_temp(1)
        "[the_person.title] seems more comfortable [the_position.verbing] you with [the_watcher.title] around."

    return

label reserved_work_enter_greeting(the_person):
    if the_person.happiness < 80 or the_person.love < 0:
        "[the_person.title] pretends not to notice you come into the room."

    elif the_person.happiness > 130:
        "[the_person.title] smiles happily when you come into the room."
        the_person "Hello [the_person.mc_title], always glad to have you stop by."

    else:
        if the_person.obedience < 100:
            "You pass by [the_person.title] as you enter the room. She's absorbed by her work and only gives you a grunt and a nod."
        else:
            "You pass by [the_person.title] as you enter the room. She looks up, startled."
            the_person "Oh! Sorry [the_person.mc_title], I was distracted and didn't notice you come in. Let me know if you need help with anything."
    return

label reserved_date_seduction(the_person):
    if the_person.has_role(girlfriend_role):
        "[the_person.possessive_title] takes your hand and holds it in hers."
        the_person "I had a wonderful evening [the_person.mc_title]."
        "She gazes romantically into your eyes."
        if the_person.effective_sluttiness(["vaginal_sex", "condomless_sex"]) > 60 and the_person.wants_creampie() and the_person.effective_sluttiness() > the_person.get_no_condom_threshold() and the_person.get_opinion_score("bareback sex") >= 0 and the_person.get_opinion_score("creampies") >= 0 and not the_person.on_birth_control and not the_person.event_triggers_dict.get("preg_knows", False):
            if the_person.get_opinion_score("creampies") > 0: #No condoms, loves creampies, she's basically asking you to knock her up. So... have her ask you to knock her up!
                the_person "Come home with me, fuck me, and dump your virile cum inside my unprotected pussy."
                the_person "I want you to breed me, okay? I want to fuck and get pregnant."
            else:
                the_person "Come home with me and fuck me. Any way you want - no condoms, no protection."
                the_person "I'm yours [the_person.mc_title], heart and body."
        elif the_person.effective_sluttiness(["vaginal_sex", "condomless_sex"]) > 60 and the_person.effective_sluttiness() > the_person.get_no_condom_threshold() and the_person.get_opinion_score("bareback sex") > 0:
            the_person "Come home with me and fuck me. I want your cock [the_person.mc_title]. I want it hard and raw inside of me."
        elif the_person.effective_sluttiness(["vaginal_sex"]) > 50 and the_person.get_opinion_score("vaginal sex") > 0:
            the_person "Come home with me and we can have sex. Feeling you slide into me would be the perfect end to a perfect night."
        elif the_person.effective_sluttiness(["anal_sex"]) > 60 and the_person.get_opinion_score("anal sex") > 0:
            the_person "Come home with me. Feeling you slide your cock into my ass would be the perfect end to an already amazing date."
            the_person "Doesn't that sound like fun?"
        elif the_person.effective_sluttiness(["sucking_cock"]) > 40 and the_person.get_opinion_score("sucking cock") > 0:
            the_person "Come home with me. I want to repay you for this wonderful night by throating your cock."
            the_person "Doesn't that sound like fun?"
        elif the_person.effective_sluttiness() > 40 and the_person.get_opinion_score("being covered in cum") > 0:
            the_person "Come home with me. I want to end tonight in my favourite way: covered in cum."
            the_person "Do you think you could help me out with that?"
        elif the_person.effective_sluttiness(["touching_body"]) > 40 and the_person.get_opinion_score("giving tit fucks") > 0 and the_person.has_large_tits():
            the_person "Come home with me [the_person.mc_title]. I want to repay you for this wonderful night by working your cock with my tits."
            the_person "Does that sound like fun to you?"
        else: #She's not very slutty, so she leaves the invitation open to interpretation
            the_person "Come home with me [the_person.mc_title]. We can share another drink and keep each other company for the evening."

    elif the_person.has_role(affair_role):
        $ so_title = SO_relationship_to_title(the_person.relationship)
        the_person "My [so_title] is staying at the office over night."
        "She holds onto your arm and leans close, whispering softly into your ear."
        if the_person.wants_creampie() and the_person.effective_sluttiness() > the_person.get_no_condom_threshold() and the_person.get_opinion_score("bareback sex") >= 0 and the_person.get_opinion_score("creampies") >= 0 and not the_person.on_birth_control and not the_person.event_triggers_dict.get("preg_knows", False):
            if the_person.get_opinion_score("creampies") > 0: #No condoms, loves creampies, she's basically asking you to knock her up. So... have her ask you to knock her up!
                the_person "Come home with me. You'll have all night to fill my fertile pussy with your cum. I'm sure by morning you'll have me pregnant."
            else:
                the_person "Come home with me. You can fuck me all night long, any way you want, with no protection."
        elif the_person.effective_sluttiness() > the_person.get_no_condom_threshold() and the_person.get_opinion_score("bareback sex") > 0:
            the_person "Come home with me. I want to ride your cock raw, all night long."
        elif the_person.get_opinion_score("vaginal sex") > 0:
            the_person "Come home with me, and you can fuck my sweet little pussy all night long."
        elif the_person.get_opinion_score("anal sex") > 0:
            the_person "Come home with me. I want to spend all night with your cock pounding my tight little asshole."
        elif the_person.get_opinion_score("sucking cock") > 0:
            the_person "Come home with me. I want to worship that big cock of yours with my mouth, slide it into my throat..."
            the_person "Mmm... You can fuck my face and make me gag on it. Wouldn't you like that?"
        elif the_person.get_opinion_score("being covered in cum") > 0:
            $ her_title = girl_relationship_to_title(the_person.relationship)
            the_person "Come home with me. Lay me out on his bed and cover his [her_title] with cum from head to toe."
        elif the_person.get_opinion_score("giving tit fucks") > 0 and the_person.has_large_tits():
            the_person "Come home with me. Let me worship your cock with my tits all night long."
            the_person "I'll massage you with them, fuck you with them, and make you cum with them. Over, and over again."
        elif the_person.get_opinion_score("cheating on men") > 0:
            the_person "Come home with me. My [so_title] tries to treat me like a lady..."
            the_person "But you know that I just want to be treated like a dirty fucking whore."
        else:
            the_person "Come home with me. We can spend all night together."
    elif the_person.relationship == "Single":
        if the_person.sluttiness > the_person.love:
            if the_person.sluttiness > 40:
                the_person "[the_person.mc_title], would you like to come back home with me? I've got some wonderful wine that makes me do crazy things."
            else:
                the_person "You were a fantastic date [the_person.mc_title]. I know I should be getting to bed soon, but would you like to come back for a quick drink?"
        else:
            if the_person.love > 40:
                the_person "You're such great company [the_person.mc_title]. Would you like to come back to my place so we can spend some more time together?"
            else:
                the_person "I had a fantastic night [the_person.mc_title]. Before you head home would you like to share a glass of wine with me?"
    else:
        $ so_title = SO_relationship_to_title(the_person.relationship)
        if the_person.sluttiness > the_person.love:
            if the_person.sluttiness > 40:
                the_person "[the_person.mc_title], would you like to come home with me tonight? My [so_title] is away on business and I'd love to drink some of his wine with you."
            else:
                the_person "This was a lot of fun. I shouldn't be out too late, but could I invite you back for a drink? My [so_title] shouldn't be home until much later."
        else:
            if the_person.love > 40:
                the_person "You're making me feel the same way I did when I first fell in love... Do you want to come back to my house to share one last drink?"
                the_person "My [so_title] won't be home until much later. I think he stays at work so late to avoid me."

            else:
                the_person "I had a fantastic night [the_person.mc_title], it's been so long since my [so_title] treated me this way."
                the_person "Would you like to share one last glass of wine at my house? My [so_title] is away on business, so I would be home all alone..."
    return

label reserved_sex_end_early(the_person):
    if the_person.sluttiness > 50:
        if the_person.love > 40:
            if the_person.arousal > 60:
                the_person "You're done? You're going to drive me crazy [the_person.mc_title], I'm so horny..."
            else:
                the_person "All done? I hope you were having a good time."
        else:
            if the_person.arousal > 60:
                the_person "That's all? I don't know how you can stop, I'm so horny after that!"
            else:
                the_person "Is that all? Well, that's disappointing."

    else:
        if the_person.love > 40:
            if the_person.arousal > 60:
                the_person "You're done? Well, you could have at least thought about me."
            else:
                the_person "All done? Maybe we can pick this up another time when we're alone."
        else:
            if the_person.arousal > 60:
                the_person "I... I don't know what to say, you've worn me out."
            else:
                the_person "That's all you wanted? I guess we're finished then."
    return


label reserved_sex_take_control (the_person):
    if the_person.arousal > 60:
        the_person "I can't let you go [the_person.mc_title], I'm going to finish what you started!"
    else:
        the_person "Do you think you're going somewhere? We're just getting started [the_person.mc_title]."
    return

label reserved_sex_beg_finish(the_person):
    "Wait, you aren't stopping are you? Please [the_person.mc_title], I'm so close to cumming, I'll do anything!"
    return

label reserved_sex_review(the_person, the_report):
    $ used_obedience = the_report.get("obedience_used", False) #True if a girl only tried a position because you ordered her to.
    $ comment_position = the_person.pick_position_comment(the_report)

    if comment_position is None:
        return #You didn't actually do anything, no need to comment.

    #She's worried about her SO finding out because it was in public
    if the_report.get("was_public", False) and the_person.relationship != "Single" and the_person.get_opinion_score("cheating on men") <= 0: #It was public and she cares.
        $ so_title = SO_relationship_to_title(the_person.relationship)
        if the_person.has_role(affair_role): #Dialogue about her being into it, but you can't do this in case she gets caught.
            the_person "Oh [the_person.mc_title], we really need to be more discrete in the future."
            the_person "We might have to stop seeing each other if my [so_title] starts to get suspicious."

        elif used_obedience:
            the_person "[the_person.mc_title], I can't be doing this where people are watching."
            the_person "What am I going to tell my [so_title] when he hears about this?"
            mc.name "Relax, nobody here is going to tell him. You have my word."
            the_person "I suppose we'll find out..."

        else:
            the_person "Oh no, what did I just do... [the_person.mc_title], if people tell my [so_title] I..."
            mc.name "Relax, nobody here is going to tell him. You have my word."
            the_person "I hope you're right..."

    #She's single, but worried that you did in public.
    elif the_report.get("was_public", False) and (the_person.effective_sluttiness()+10*the_person.get_opinion_score("public sex") < comment_position.slut_cap):
        if used_obedience:
            the_person "I can't believe I let you talk me into that [the_person.mc_title]... There are people around, they all saw!"
            mc.name "Relax, nobody here really cares what we were doing."
            the_person "I still don't like it..."
        else:
            the_person "I can't believe we just did that, I just... Oh lord, I wasn't thinking."
            the_person "What are people going to say about me? I..."
            mc.name "Relax, nobody here cares what we were doing. It isn't a big deal."
            "She scowls, seeming unconvinced."
            the_person "I hope you're right. Can we find somewhere more private next time?"

    #No special conditions, just respond based on how orgasmed and how slutty the position was.
    elif the_report.get("girl orgasms", 0) > 0 and the_report.get("guy orgasms", 0) > 0: #You both came
        if the_person.effective_sluttiness() > comment_position.slut_cap: #She's sluttier than the position cap, it was tame
            the_person "Ah, that was nice. Maybe next time we can... go a little further. Does that sound like fun to you?"
            "She gives you a dirty smile, already imagining your next encounter."

        elif the_person.effective_sluttiness() > comment_position.slut_requirement: #She thought it was fun/exciting
            the_person "Ah, that was exciting. I think I'm all finished too, I need to catch my breath."

        elif used_obedience: #She only did it because she was commanded
            "[the_person.possessive_title] looks away, embarrassed by what she's done with you."
            the_person "You're all finished? Good, that went too far for me..."
            mc.name "You didn't seem to mind when you were cumming your brains out."
            the_person "I just... I wasn't thinking straight. I have myself under control now."

        else: # She's suprised she even tried that.
            "[the_person.possessive_title] looks away, embarrassed by what she's done with you."
            the_person "Oh my... I'm sorry, I think I lost control of myself."
            mc.name "Hey, I'm not complaining. That was a great time."
            the_person "Yeah, it was. I think I need a moment to catch my breath."

    elif the_report.get("girl orgasms", 0) > 0: #Only she came
        if the_person.effective_sluttiness() > comment_position.slut_cap: #She's sluttier than the position
            the_person "Don't you want to finish, or are you too tired already?"
            mc.name "Maybe next time, I'm just happy to make you happy."
            the_person "Such a gentleman. I'll make it up to you next time."

        elif the_person.effective_sluttiness() > comment_position.slut_requirement: #She thought it was fun/exciting
            the_person "All tired out? Sorry to hear that."
            "She sighs happily, still enjoying the chemical rush from her orgasm."

        elif used_obedience: #She only did it because she was commanded
            "[the_person.possessive_title] looks away, embarrassed by what you've just done together."
            the_person "Are we finished?"
            mc.name "For now, yeah. Don't be so shy, you were obviously had a good time."
            the_person "I just... wasn't myself, that's all. I'm in control again."
            mc.name "If you say so, but I like you when you lose control."

        else: # She's suprised she even tried that.
            the_person "Finished? That's good, I think I need to sit down. My head is still spinning."
            the_person "I didn't think I was going to... climax like that. I wasn't prepared."
            mc.name "Hopefully you will be next time."
            the_person "Maybe. I don't think I could ever get use to that."

    elif the_report.get("guy orgasms", 0) > 0: #Only you came
        if the_person.effective_sluttiness() > comment_position.slut_cap: #She's sluttier than the position
            the_person "All done? Well, I think we can call that a success."
            the_person "If we do this again I have some ideas we can try out. I think you'll {i}really{/i} enjoy them."

        elif the_person.effective_sluttiness() > comment_position.slut_requirement: #She thought it was fun/exciting
            the_person "All done then? Oh, I thought I was going to get to..."
            "She trails off, a little disappointed."
            mc.name "Sorry, I'm just a little worn out. Next time, I promise."

        elif used_obedience: #She only did it because she was commanded
            the_person "Finished? Good."
            "She looks away, embarassed by what you've just done."
            mc.name "Yeah, all done for now."

        else:  # She's suprised she even tried that.
            the_person "Ah... We're done? Right, of course. Sorry, I don't even know what I'm thinking."
            "She laughs nervously."
            the_person "I just got a little carried away, I'm, ah... I'm fine now."

    else: #Nobody came.
        if the_person.effective_sluttiness() > comment_position.slut_cap: #She's sluttier than the position
            the_person "That's all? Well, that's a little dissapointing. I was just getting excited."
            the_person "Make it up to me next time, okay?"
            mc.name "Yeah, sure thing."

        elif the_person.effective_sluttiness() > comment_position.slut_requirement: #She thought it was fun/exciting
            the_person "Finished already?"
            "[the_person.possessive_title] seems a little disappointed."
            the_person "Next time you're going to have to pace yourself, or you're going to keep disappointing me."
            # the_person "Done already? We'll have to take it more slowly so you don't get so tired next time."
            # "[the_person.possessive_title] seems a little disappointed."

        elif used_obedience: #She only did it because she was commanded
            the_person "Finished? I thought you were going to..."
            the_person "Never mind. If you're done that's fine with me."

        else:  # She's suprised she even tried that.
            the_person "You're right, we should stop. I'm getting far too excited, I might do something I regret."
    return


## Role Specific Section ##
label reserved_improved_serum_unlock(the_person):
    mc.name "[the_person.title], now that you've had some time in the lab there's something I wanted to talk to you about."
    the_person "Okay, how can I help?"
    mc.name "All of our research and development up until this point has been based on the limited notes I have from my university days. I'm sure there's more we could learn, and I want you to look into it for me."
    "[the_person.title] nods in agreement."
    the_person "I think I have an idea that could really help us along. All of our testing procedures focus on human safety, but what I really need to know about are the subjective effects of our creations."
    the_person "With your permission, I would like to take a dose of serum myself and have you record my experience with it."
    return

## Taboo break dialogue ##
label reserved_kissing_taboo_break(the_person):
    if the_person.effective_sluttiness() >= 30:
        the_person "Oh, well hello there! Do you... Want to do anything with me?"
    elif the_person.love >= 20:
        the_person "So you feel it too?"
        "She sighs happily."
        the_person "I... I want to kiss you. Would you kiss me?"
    else:
        the_person "I don't know if this is a good idea [the_person.mc_title]..."
        mc.name "Let's just see how it feels. Trust me."
        "[the_person.title] eyes you warely, but you watch her resolve break down."
        the_person "Okay... Just one kiss, to start."
    return

label reserved_touching_body_taboo_break(the_person):
    if the_person.effective_sluttiness() >= 30:
        the_person "Do you want to know something?"
        mc.name "What?"
        the_person "I've had dreams just like this before. They always stop just before you touch me."
        mc.name "Well, let's fix that right now."

    elif the_person.love >= 20:
        the_person "I want you to know I take this very seriously, [the_person.mc_title]."
        mc.name "Of course. So do I [the_person.title]."
        the_person "I normally wouldn't even think about letting someone like you touch me."
        mc.name "What do you mean \"Someone like me\"?"
        the_person "You're a trouble maker. I always get the feeling you're bad news for me, but..."
        the_person "But I just can't say no to you."
    else:
        the_person "You shouldn't be doing this [the_person.mc_title]. We... We barely know each other."
        mc.name "You don't want me to stop though, do you?"
        the_person "I don't... I don't know what I want."
        mc.name "Then let me show you."
    return

label reserved_touching_penis_taboo_break(the_person):
    if the_person.effective_sluttiness() >= 35:
        the_person "Look at how big your penis is. You poor thing, that must be very uncomfortable."
        the_person "Just relax and I'll see what I can do about it, okay?"
    elif the_person.love >= 20:
        the_person "Oh my... If I'm honest I wasn't expecting it to be quite so... Big."
        mc.name "Don't worry, it doesn't bite. Go ahead and touch it, I want to feel your hand on me."
        "She bites her lip playfully."
    else:
        the_person "We should stop here... I don't want you to get the wrong idea about me."
        mc.name "Look at me [the_person.mc_title], I'm rock hard. Nobody would ever know if you gave it a little feel."
        "You see her resolve waver."
        the_person "It is very... Big. Just feel it for a moment?"
        mc.name "Just a moment. No longer than you want to."
        "She bites her lip as her resolve breaks completely."
    return

label reserved_touching_vagina_taboo_break(the_person):
    if the_person.effective_sluttiness() >= 35:
        the_person "Do it [the_person.mc_title]. Touch my pussy."
    elif the_person.love >= 20:
        the_person "I'm so nervous [the_person.mc_title], do you feel that way too?"
        mc.name "Just take a deep breath and relax. You trust me, right?"
        the_person "Of course. I trust you."
    else:
        the_person "I don't know if we should be doing this [the_person.mc_title]..."
        mc.name "Just take a deep breath and relax. I'm just going to touch you a little, and if you don't like it I'll stop."
        the_person "Just a little?"
        mc.name "Just a little. Trust me, it's going to feel amazing."
    return

label reserved_sucking_cock_taboo_break(the_person):
    mc.name "I want you to do something for me."
    the_person "What would you like?"
    mc.name "I'd like you to suck on my cock."
    if the_person.effective_sluttiness() >= 45:
        the_person "I... I really should say no."
        mc.name "But you aren't going to."
        "She shakes her head."
        the_person "I've told people all my life that I didn't do things like this, but now it's all I can think about."
    elif the_person.love >= 30:
        the_person "Oh [the_person.mc_title]! Really? I know most men are into that sort of thing, but I..."
        the_person "Well, I think I'm a little classier than that."
        mc.name "What's not classy about giving your partner pleasure? Come on [the_person.title], aren't you a little curious?"
        the_person "I'm curious, but I... Well... How about I just give it a taste and see how that feels?"
        mc.name "Alright, we can start slow and go from there."
    else:
        the_person "I'm sorry, I think I misheard you."
        mc.name "No you didn't. I want you to put my cock in your mouth and suck on it."
        the_person "I could never do something like that [the_person.mc_title], what would people think?"
        the_person "I'm not some kind of slut, I don't \"suck cocks\"."
        mc.name "Yeah you do, and you're going to do it for me."
        the_person "Why would I do that?"
        mc.name "Because deep down, you want to. You can be honest with me, aren't you a little bit curious what it's going to be like?"
        "She looks away, but you both know the answer."
        mc.name "Just get on your knees, put it in your mouth, and if you don't like how it feels you can stop."
        the_person "What are you doing to me [the_person.mc_title]? I use to think I was better than this..."
    return

label reserved_licking_pussy_taboo_break(the_person):
    mc.name "I want to taste your pussy [the_person.title]. Are you ready?"
    if the_person.effective_sluttiness() >= 45:
        the_person "Oh what a gentleman I have! I'm ready [the_person.mc_title], eat me out!"
    elif the_person.love >= 30:
        the_person "You're such a gentleman [the_person.mc_title], but you don't have to do that."
        mc.name "I don't think you understand. I {i}want{/i} to eat you out, I'm not doing it as a favour."
        "[the_person.title] almost seems confused by the idea."
        the_person "Oh... Well then, I suppose you can get right to it."
    else:
        the_person "You're a gentleman [the_person.mc_title], but you don't need to do that."
        if not the_person.has_taboo("sucking_cock"):
            the_person "It's flattering that you'd want to return the favour though, so thank you."

        mc.name "No, I don't think you understand what I'm saying. I {i}want{/i} to eat you out, I'm not doing it as a favour."
        "[the_person.title] almost seems confused by the idea."
        the_person "Really? I mean... I just haven't met many men who want to do that."
        mc.name "Well you have one now. Just relax and enjoy yourself."
    return

label reserved_vaginal_sex_taboo_break(the_person):
    if the_person.effective_sluttiness() >= 60:
        the_person "[the_person.mc_title], I'm not ashamed to say I'm very excited right now!"
        "She giggles gleefully."
        the_person "Come on and fuck me!"
    elif the_person.love >= 45:
        the_person "Go ahead [the_person.mc_title]. I think we're both ready for this."
    else:
        if the_person.has_taboo("anal_sex"):
            the_person "Oh my god, what am I doing here [the_person.mc_title]?"
            the_person "I'm not the type of person to do this... Am I? Is this who I've always been, and I've just been lying to myself?"
            mc.name "Don't overthink it. Just listen to your body and you'll know what you want to do."
            "She closes her eyes and takes a deep breath."
            the_person "I... I want to have sex with you. I'm ready."
        else:
            the_person "I'm glad you're doing this properly this time."
            "It might be the hot new thing to do, but I just don't enjoy anal. I think your cock will feel much better in my vagina."
    return

label reserved_anal_sex_taboo_break(the_person):
    if the_person.effective_sluttiness() >= 75:
        "She takes a few deep breaths."
        the_person "I'm ready if you are [the_person.mc_title]. Come and fuck my ass."

    elif the_person.love >= 60:
        the_person "This is really something you want to do then [the_person.mc_title]?"
        mc.name "Yeah, it is."
        the_person "Okay then. It wouldn't be my first pick, but we can give it a try."
        the_person "I don't know if you'll even fit though. You're penis is quite large."
        mc.name "You'll stretch out more than you think."
    else:
        if the_person.has_taboo("vaginal_sex"):
            the_person "Oh lord, what happened to me?"
            the_person "I thought I was a respectable lady, now I'm about to get fucked in the ass..."
            the_person "We've never even had sex before and now I'm doing anal!"

            #TODO: "At least my vagina still belongs to my SO... At least I still have that one thing."

        else:
            the_person "I'm not sure about this [the_person.mc_title]... I'm not even sure if you can fit inside me there!"
            mc.name "I can stretch you out, don't worry about that."
            the_person "Oh lord, what happened to me..."
            the_person "I use to think I was a respectable lady, now I'm about to get fucked in the ass..."
        mc.name "Relax, you'll be fine and this isn't the end of the world. Who knows, you might even enjoy yourself."
        the_person "I doubt it. Come on then, there's no point stalling any longer."
    return

label reserved_condomless_sex_taboo_break(the_person):
    if the_person.get_opinion_score("bareback sex") > 0:
        the_person "You want to have sex without any protection? I'll admit, that would really turn me on."
        if the_person.on_birth_control:
            the_person "I am on birth control, so it should be perfectly safe. I do want to know what you feel like raw..."
            $ the_person.update_birth_control_knowledge()
        elif the_person.get_opinion_score("creampies") > 0:
            the_person "It would be very naughty if you came inside me though. I'm not on any birth control..."
            $ the_person.update_birth_control_knowledge()
            mc.name "Don't you think we're being naughty already?"
            "She bites her lip and nods."
            the_person "I think we are."
        elif the_person.get_opinion_score("creampies") < 0:
            the_person "You will need to pull out though. I hate having cum dripping out of me all day."
        else:
            the_person "I'm not on birth control, so you will need to pull out. Understood? Good."
            $ the_person.update_birth_control_knowledge()

    elif the_person.love > 60:
        the_person "If you think you're ready for this commitment, I am to. I want to feel close to you."
        if the_person.on_birth_control:
            the_person "I'm on birth control, so the chances of getting me pregnant are slim, but you should know they still exist."
            $ the_person.update_birth_control_knowledge()
        elif the_person.get_opinion_score("creampies") > 0:
            the_person "When you're going to finish you don't have to pull out unless you want to. Okay?"
            mc.name "Are you on the pill?"
            "She shakes her head."
            the_person "No, but I trust you to make the decision that is right for both of us."
            $ the_person.update_birth_control_knowledge()
        elif the_person.get_opinion_score("creampies") < 0:
            if the_person.kids == 0:
                the_person "You will have to pull out though, okay? I really don't plan on being a mother."
            else:
                the_person "You will have to pull out though, okay? I've been pregnant before and it isn't pretty."
        else:
            if the_person.kids == 0:
                the_person "You will have to pull out though. I don't want you to make me a mother."
            else:
                the_person "You will have to pull out though, understood? I don't think either of us are ready for that."

    else:
        the_person "You want to have sex without protection? That's very risky [the_person.mc_title]."
        if the_person.on_birth_control:
            the_person "I'm on birth control, but nothing is one hundred percent effective."
            $ the_person.update_birth_control_knowledge()
            mc.name "I'm willing to take that chance. Are you?"
            "She thinks for a moment, then nods."
            the_person "I believe I am."
        elif the_person.has_taboo("vaginal_sex"):
            mc.name "I want our first time to be special though, don't you?"
            "She takes a second to think, then nods."
            the_person "I do. You need to be very careful where you finish, okay?"
        else:
            mc.name "It will feel so much better raw, for both of us."
            the_person "I have wondered what it would be like..."
            "She takes a moment to think, then nods."
            the_person "Fine, you don't need a condom. Please be very careful where you finish, okay?"
    return

label reserved_underwear_nudity_taboo_break(the_person, the_clothing):
    if the_person.effective_sluttiness() > 30 - (the_person.get_opinion_score("skimpy outfits") * 5):
        the_person "This is the first time you've gotten to see my underwear. I hope you like what you see."
        if the_person.has_taboo(["bare_tits","bare_pussy"]):
            mc.name "I'm sure I will. You have good taste."
            the_person "Well then, what are you waiting for then?"
        else:
            mc.name "I've already seen you out of your underwear, but I'm sure it complaments your form."
            the_person "Time to find out. What are you waiting for?"

    elif the_person.love > 15:
        the_person "This is going to be the first time you've seen me in my underwear. I have to admit, I'm feeling a little nervous."
        if the_person.has_taboo(["bare_tits","bare_pussy"]):
            mc.name "Don't be, I'm sure you look stunning in it."
            the_person "Well then, take off my [the_clothing.display_name] for me."

        else:
            mc.name "I already know you have a beautiful body, some nice underwear can only enhance the experience."
            the_person "You're too kind. Help me take off my [the_clothing.display_name]."

    else:
        the_person "If I take off my [the_clothing.display_name] you'll see me in my underwear."
        mc.name "That's the plan, yes."
        the_person "I shouldn't be going around half naked for men I barely know. What would people think?"
        mc.name "Why do you care what other people think? Forget about them and just focus on us."

        if the_person.has_taboo(["bare_tits","bare_pussy"]):
            mc.name "Why do you care what other people think? Forget about them and just focus on the moment."
            the_person "I'll try..."

        else:
            mc.name "You might have wanted to worry about that before I saw you naked. You don't have anything left to hide."
            the_person "I suppose you're right..."
    return

label reserved_bare_tits_taboo_break(the_person, the_clothing):
    if the_person.effective_sluttiness() > (40 - the_person.get_opinion_score("showing her tits") * 5):
        the_person "Oh, so you want to take a look at my breasts?"
        if the_person.has_large_tits():
            "She bounces her chest for you, jiggling the big tits hidden underneath her [the_clothing.display_name]."
        else:
            "She bounces her chest and gives her small tits a little jiggle."
        the_person "Well it would be a shame not to let you get a glimpse, right? I've been waiting for you to ask."
        mc.name "Let's get that [the_clothing.display_name] off so I can see them then."

    elif the_person.love > 25:
        the_person "Oh, you want to get my breasts out?"
        if the_person.has_large_tits():
            "She looks down at her own large rack, tits hidden restrained by her [the_clothing.display_name]."
            the_person "I don't have to ask why. I'm glad you're interested in them."
        else:
            the_person "I'm glad you're still interested in smaller breasts. It seems like every man is mad boob-crazy these days."
        mc.name "Of course I'm interested. let's get that [the_clothing.display_name] out of the way so I can get a good look at you."

    else:
        the_person "Hey there! If you take off my [the_clothing.display_name] I won't be decent any more!"
        mc.name "I want to see your tits and it's in the way."
        the_person "I'm aware it's \"in the way\", that's why I put it on this morning."
        if the_person.has_large_tits() and the_clothing.underwear:
            the_person "Besides, a girl like me needs a little support. These aren't exactly light."
        mc.name "Come on [the_person.title]. You're gorgeous, I'm just dying to see more of you."
        the_person "Well I'm glad I have that effect on you. I suppose..."
        "She takes a moment to think, then sighs and nods."
        the_person "You can take off my [the_clothing.display_name] and have a look. Just be kind to me, I'm feeling very vulnerable."
    return

label reserved_bare_pussy_taboo_break(the_person, the_clothing):
    if the_person.effective_sluttiness() > (50 - the_person.get_opinion_score("showing her ass") * 5):
        the_person "You want to get me out of my [the_clothing.display_name]? Well, I'm glad you've finally asked."

    elif the_person.love > 35:
        the_person "Oh, careful there [the_person.mc_title]. If you take off my [the_clothing.display_name] I won't be decent any more."
        if the_person.has_taboo("touching_vagina"):
            mc.name "I don't particularly want you to be decent at the moment, though. I want to get a look at your sweet pussy."
            the_person "Oh stop, you're going to make me blush."
            "She thinks for a moment, then nods timidly."
            the_person "Okay, you can take it off and have a look, if you'd like."

        else:
            mc.name "I think you stopped being decent when you let me touch your pussy."
            the_person "Oh stop, you. I suppose you can take it off and have a look, if you'd like."

    else:
        the_person "Oh! Careful, or you're going to have me showing you everything!"
        mc.name "That is what I was hoping for, yeah."
        the_person "Well! I mean... I'm not that sort of woman [the_person.mc_title]!"
        if the_person.has_taboo("touching_vagina"):
            mc.name "Don't you want to be though? Don't you want me to enjoy your body?"
            the_person "I... I mean, I might, but I shouldn't... You shouldn't..."
        else:
            mc.name "Of course you are! I've had my hand on your pussy already, I just want to see what I was feeling before."
            the_person "I... I mean, that wasn't... I..."

        "You can tell her protests are just to maintain her image, and she already knows what she wants."
        mc.name "Just relax and let it happen, you'll have a good time."
    return

label reserved_facial_cum_taboo_break(the_person):

    return

label reserved_mouth_cum_taboo_break(the_person):

    return

label reserved_body_cum_taboo_break(the_person):

    return

label reserved_creampie_taboo_break(the_person):
    if the_person.wants_creampie():
        if the_person.on_birth_control:
            if the_person.relationship != "Single":
                $ so_title = girl_relationship_to_title(the_person.relationship)
                the_person "Oh... I feel like such a bad [so_title], but I think I needed this. I'm sure he would understand."

            else:
                the_person "Oh lord, I've wanted this so badly for so long!"

        elif the_person.effective_sluttiness() > 75 or the_person.get_opinion_score("creampies") > 0:
            if the_person.relationship != "Single":
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person "Oh lord, I've needed this so badly!"
                the_person "I don't care about my [so_title], I just want you to treat me like a real woman and get me pregnant!"

            else:
                the_person "Oh lord, I've needed this so badly! I want you to treat me like a real woman and get me pregnant!"

            "She sighs happily."
            the_person "If you've got the energy we should do it again, to give me the best chance."

        else:
            if the_person.relationship != "Single":
                $ so_title = girl_relationship_to_title(the_person.relationship)
                the_person "I can't believe I let you do that... I'm such a terrible [so_title], but it felt so good!"


            else:
                the_person "I can't believe I let you do that, but it feels so good!"

            the_person "I'll just have to hope you haven't gotten me pregnant. We shouldn't do this again, it's too risky."

    else:
        if not the_person.on_birth_control:
            the_person "Oh no, did you just finish [the_person.mc_title]?"
            "She sighs unhappily."
            if the_person.relationship != "Single":
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person "What if I get pregnant now? My [so_title] is going to start asking a lot of questions."

            else:
                the_person "Have you thought about what you would do if you got me pregnant?"

            the_person "Maybe next time you should wear a condom, in case you get carried away again."

        elif the_person.relationship != "Single":
            $ so_title = girl_relationship_to_title(the_person.relationship)
            the_person "[the_person.mc_title], I told you to pull out."
            the_person "I'm being a already a terrible [so_title], and this just makes me feel even worse."
            the_person "Maybe next time you should wear a condom in case you get too excited."

        elif the_person.get_opinion_score("creampies") < 0:
            the_person "Oh [the_person.mc_title], I told you to pull out. I hope you're satisfied, you've made such a mess."

        else:
            the_person "[the_person.mc_title], did you just finish inside?"
            the_person "I guess boys will be boys, but try not to make a habit of it when I tell you to pull out."
    return

label reserved_anal_creampie_taboo_break(the_person):

    return
