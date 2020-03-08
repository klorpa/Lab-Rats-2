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
        titles_function = reserved_titles, possessive_titles_function = reserved_possessive_titles, player_titles_function = reserved_player_titles)

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
    the_person.char "I suppose you could. How can I help you?"
    mc.name "I'm so sorry, I know this is silly but I just couldn't let you walk by without knowing your name."
    "She laughs and rolls her eyes."
    $ title_choice = get_random_title(the_person)
    $ formatted_title = the_person.create_formatted_title(title_choice)
    the_person.char "Well then, I suppose I shouldn't disappoint you. You can call me [formatted_title]."
    $ the_person.set_title(title_choice)
    $ the_person.set_possessive_title(get_random_possessive_title(the_person))
    "[the_person.possessive_title] holds her hand out to shake yours."
    the_person.char "What about you, what's your name?"
    return

label reserved_greetings(the_person):
    if the_person.love < 0:
        the_person.char "... Do you need something?"
    elif the_person.happiness < 90:
        the_person.char "Hello..."
    else:
        if the_person.sluttiness > 60:
            if the_person.obedience > 130:
                the_person.char "Hello [the_person.mc_title]."
            else:
                the_person.char "Hello, are you feeling as good as you're looking today?"
        else:
            if the_person.obedience > 130:
                the_person.char "Hello [the_person.mc_title]."
            else:
                the_person.char "Hello, I hope you're doing well."
    return

label reserved_sex_responses_foreplay(the_person):
    if the_person.arousal < 25:
        if the_person.sluttiness > 50:
            the_person.char "Mmm, you know just what I like, don't you?"
        else:
            the_person.char "Oh my... that feels very good, [the_person.mc_title]!"

    elif the_person.arousal < 50:
        if the_person.sluttiness > 50:
            "[the_person.title] closes her eyes and lets out a loud, sensual moan."
        else:
            the_person.char "Keep doing that [the_person.mc_title]... Wow, you're good!"

    elif the_person.arousal < 75:
        if the_person.sluttiness > 50:
            the_person.char "Oh gods above taht feels amazing!"
        else:
            the_person.char "Oh lord... I could get use to you touching me like this!"
    else:
        if the_person.sluttiness > 50:
            if the_person.relationship == "Single":
                the_person.char "Touch me [the_person.mc_title], I want you to touch me!"
            else:
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person.char "I should feel bad... but my [so_title] never touches me this way!"
                the_person.char "I need this, so badly!"
        else:
            the_person.char "I want you to keep touching me. I never thought you could make me feel this way, but I want more of it!"

    return

label reserved_sex_responses_oral(the_person):
    if the_person.arousal < 25:
        if the_person.sluttiness > 50:
            the_person.char "Oh [the_person.mc_title], you're so good to me."
        else:
            the_person.char "Oh my... that feels..."
            "She sighs happily."
            the_person.char "Good!"

    elif the_person.arousal < 50:
        if the_person.sluttiness > 50:
            the_person.char "Yes, just like that! Mmm!"
        else:
            the_person.char "Keep doing that [the_person.mc_title], it's making me feel... very aroused."

    elif the_person.arousal < 75:
        if the_person.sluttiness > 50:
            the_person.char "Mmm, you really know how to put that tongue of yours to good use. That feels amazing!"
        else:
            the_person.char "Oh lord... your tongue is addictive, I just want more of it!"
    else:
        if the_person.sluttiness > 50:
            if the_person.relationship == "Single":
                the_person.char "Oh I need this so badly [the_person.mc_title]! If you keep going you'll make me climax!"
            else:
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person.char "I should feel bad, but you make me feel so good and my [so_title] never does this for me!"
        else:
            the_person.char "Oh sweet lord in heaven... This feeling is intoxicating!"

    return

label reserved_sex_responses_vaginal(the_person):
    if the_person.arousal < 25:
        if the_person.sluttiness > 50:
            the_person.char "Mmm, I love feeling you inside of me!"
        else:
            the_person.char "Oh lord, you're so big... Whew!"

    elif the_person.arousal < 50:
        if the_person.sluttiness > 50:
            "[the_person.title] closes her eyes and lets out a loud, sensual moan."
        else:
            the_person.char "Oh that feels very good, keep doing that!"

    elif the_person.arousal < 75:
        if the_person.sluttiness > 50:
            the_person.char "Yes! Oh god yes, fuck me!"
        else:
            the_person.char "Oh lord your... cock feels so big!"
    else:
        if the_person.sluttiness > 50:
            if the_person.relationship == "Single":

                the_person.char "Keep... keep going [the_person.mc_title]! I'm going to climax soon!"
            else:
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person.char "Keep going! My [so_title]'s tiny dick never makes me climax and I want it so badly!"
                the_person.char "I should feel bad, but all I want is your cock in me right now!"
        else:
            "[the_person.title]'s face is flush as she pants and gasps."
    return

label reserved_sex_responses_anal(the_person):
    if the_person.arousal < 25:
        if the_person.sluttiness > 50:
            the_person.char "Mmm, you feel so big when you're inside me like this."
        else:
            the_person.char "Be gentle, it feel like you're going to tear me in half!"

    elif the_person.arousal < 50:
        if the_person.sluttiness > 50:
            the_person.char "Give it to me, [the_person.mc_title], give me every last inch!"
        else:
            the_person.char "Oh god! Oww!"

    elif the_person.arousal < 75:
        if the_person.sluttiness > 50:
            the_person.char "I hope my ass isn't too tight for you, I don't want you to cum early."
        else:
            the_person.char "I don't think I will be able to walk straight after this!"
    else:
        if the_person.sluttiness > 50:
            if the_person.relationship == "Single":
                the_person.char "You're cock feels so stuffed inside me! Keep going, I might actually climax!"
            else:
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person.char "My [so_title] always wanted to try anal, but I told him it would never happen. My ass belongs to you , [the_person.mc_title]!"
        else:
            the_person.char "Oh lord, this is actually starting to feel good... I might be able to climax after all!"

    return

label reserved_climax_responses_foreplay(the_person):
    if the_person.sluttiness > 50:
        the_person.char "Oh my... I'm going to... cum!"
    else:
        the_person.char "I... Oh my god, this feeling is..."
        "She pauses and moans excitedly."
        the_person.char "So good!"
    return

label reserved_climax_responses_oral(the_person):
    if the_person.sluttiness > 70:
        the_person.char "Keep going [the_person.mc_title], you're going to make me..."
        "She barely finishes her sentence as her body shivers with pleasure."
        the_person.char "... Orgasm!"
    else:
        the_person.char "This feeling... Oh... Oh!"
        "Her eyes close and she takes a deep breath."
    return

label reserved_climax_responses_vaginal(the_person):
    if the_person.sluttiness > 70:
        the_person.char "You're going to... Ah! You're going to make me climax [the_person.mc_title]!"
        "She closes her eyes as she tenses up. She freezes for a long second, then lets out a long, slow breath."
    else:
        the_person.char "Oh, I think I'm about to... Oh yes!"
    return

label reserved_climax_responses_anal(the_person):
    if the_person.sluttiness > 70:
        the_person.char "Mmmm, fuck me [the_person.mc_title], fuck my ass and make me cum!"
    else:
        the_person.char "Oh lord, I think I'm going to climax. You're going to make me cum by fucking my ass!"
    return

label reserved_clothing_accept(the_person):
    if the_person.obedience > 130:
        the_person.char "You're too kind [the_person.mc_title]. I'll add it to my wardrobe right away."
    else:
        the_person.char "For me? Oh, I'm not use to getting gifts like this..."
    return

label reserved_clothing_reject(the_person):
    if the_person.obedience > 130:
        the_person.char "You're too kind [the_person.mc_title], really. I don't think I can accept such a... beautiful gift from you though."
    else:
        if the_person.sluttiness > 60:
            the_person.char "It's very nice [the_person.mc_title], but I think it's a little too revealing, even for me. Maybe when I'm feeling a little more bold, okay?"
        else:
            the_person.char "Really [the_person.mc_title]? Just suggesting that I would wear something like that is a little too forward, don't you think?"
    return

label reserved_clothing_review(the_person):
    if the_person.obedience > 130:
        the_person.char "I'm such a mess right now [the_person.mc_title], I just have to go and get tidied up for you. I'll be back in a moment."
    else:
        if the_person.sluttiness > 40:
            the_person.char "Oh dear, my clothes are just a mess after all of that. Not that I'm complaining, of course, but I should go get tidied up. Back in a moment."
        else:
            the_person.char "Oh, I look like such a mess right now. I'll be back in a moment."
    return

label reserved_strip_reject(the_person):
    if the_person.obedience > 130:
        the_person.char "I'm sorry [the_person.mc_title], but I think that should stay where it is for now. For modesty's sake."
    elif the_person.obedience < 70:
        the_person.char "That's going to stay right there for now. I'll decide when I want it to come off, okay?."
    else:
        the_person.char "[the_person.mc_title], I don't feel comfortable taking that off. Just leave it put."
    return

label reserved_sex_accept(the_person):
    if the_person.sluttiness > 70:
        if the_person.obedience < 70:
            the_person.char "Good, I didn't want to be the one to suggest it but that sounds like fun."
        else:
            the_person.char "Mmm, you think we should give that a try? I'm feeling adventurous today, lets go."
    else:
        the_person.char "Oh, I know I shouldn't [the_person.mc_title]... but I think you've managed to convince me."
    return

label reserved_sex_obedience_accept(the_person):
    if the_person.sluttiness > 70:
        the_person.char "I shouldn't... I really shouldn't. But I know you want me, and I think I want you too. Promise you'll make me feel good too?"
    else:
        if the_person.obedience > 130:
            the_person.char "Okay [the_person.mc_title], if that's what you want. I'll do what I can to serve you."
        else:
            the_person.char "If it were anyone other than you I'd say no [the_person.mc_title]. Don't get too use to this, okay?"
    return

label reserved_sex_gentle_reject(the_person):
    if the_person.sluttiness > 50:
        the_person.char "Wait, a lady must be romanced first [the_person.mc_title]. At least get me warmed up first."
    else:
        the_person.char "This doesn't seem like the kind of thing a proper lady would do. Lets do something else, please."
    return

label reserved_sex_angry_reject(the_person):
    if not the_person.relationship == "Single":
        $ so_title = SO_relationship_to_title(the_person.relationship)
        the_person.char "Excuse me? I have a wonderful [so_title] and I would never dream of doing anything to betray him!"
        "She glares at you and shakes her head."
        the_person.char "I need some space, [the_person.mc_title]. I didn't think you were that kind of man."
    elif the_person.sluttiness < 20:
        the_person.char "Excuse me? Do I look like some sort of prostitute?"
        the_person.char "Get away from me, you're lucky I don't turn you into the police for that! Give me some space, I don't want to talk after that."
    else:
        the_person.char "Um, what do you think you're doing [the_person.mc_title]? That's disgusting, and certainly no way to act around a lady!"
    return

label reserved_seduction_response(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 50:
            the_person.char "Hello [the_person.mc_title], is there something I can help you with? Something of a personal nature perhaps?"
        else:
            the_person.char "Hello [the_person.mc_title], is there something I can help you with?"
    else:
        if the_person.sluttiness > 50:
            the_person.char "You've got that look in your eye again. there's just no satisfying you, is there? You're lucky I'm such a willing participant."
        elif the_person.sluttiness > 10:
            the_person.char "Oh [the_person.mc_title], you always know how to make a woman feel wanted..."
        else:
            the_person.char "[the_person.mc_title], isn't that a little bit forward of you? I'm not saying no though..."
    return

label reserved_seduction_accept_crowded(the_person):
    if the_person.relationship == "Single":
        if the_person.sluttiness < 20:
            the_person.char "I don't think anyone will miss us for a few minutes. We can... get closer and see where things go."
        elif the_person.sluttiness < 50:
            the_person.char "Come on, let's go find someplace quiet then."
        else:
            the_person.char "Well then, do you want to take me right here or should we get a room?"
    else:
        $ so_title = SO_relationship_to_title(the_person.relationship)
        if the_person.sluttiness + (5*the_person.get_opinion_score("cheating on men")) > 50:
            the_person.char "Well you have my attention. We should find some place private, unless you want my [so_title] to hear about us."
        else:
            the_person.char "I know I shouldn't... We need to keep it quiet, so my [so_title] doesn't find out."
    return

label reserved_seduction_accept_alone(the_person):
    if the_person.relationship == "Single":
        if the_person.sluttiness < 20:
            the_person.char "How about we start with a little kissing and just see where it goes."
        elif the_person.sluttiness < 50:
            the_person.char "Oh [the_person.mc_title], you're going to make me blush! Come over here!"
        else:
            the_person.char "Mmm, that sounds so nice [the_person.mc_title]. Don't make me wait, get over here!"
    else:
        $ so_title = SO_relationship_to_title(the_person.relationship)
        if the_person.sluttiness + (5*the_person.get_opinion_score("cheating on men")) > 50:
            the_person.char "Come here [the_person.mc_title], I want you to touch me in ways my [so_title] never does!"
        else:
            the_person.char "This is so improper."
            "She locks eyes with you, deadly serious."
            the_person.char "You can never tell my [so_title] about this, is that understood?"
            "You nod and she melts into your arms."
    return

label reserved_seduction_refuse(the_person):
    if the_person.sluttiness < 20:
        the_person.char "Oh... I'm sorry [the_person.mc_title] but I couldn't imagine doing anything like that."

    elif the_person.sluttiness < 50:
        the_person.char "I'm sorry, but I'm just not in the mood for any fooling around right now. Maybe some other time though."

    else:
        the_person.char "Oh [the_person.mc_title], that sounds like a lot of fun, but I think we should save it for another time."
    return

label reserved_flirt_response(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 50:
            the_person.char "It would be so improper, but for you I'm sure I could arange something special."
        else:
            the_person.char "Thank you for the compliment, [the_person.mc_title], I appreciate it."

    elif not the_person.relationship == "Single":
        $so_title = SO_relationship_to_title(the_person.relationship)
        if the_person.sluttiness + (the_person.get_opinion_score("cheating on men")*5) > 50:
            the_person.char "I'm glad you appreciate it. My [so_title] hardly even looks at me any more."
            "She spins, giving you a full look at her body."
            the_person.char "His loss, right?"
        else:
            the_person.char "[the_person.mc_title], I should remind you I have a [so_title]. We can be friendly with each other, but that's where it should end."
            "She seems more worried about maintaining appearances than she was about actually flirting with you."
    else:
        if the_person.sluttiness > 50:
            the_person.char "Oh [the_person.mc_title], that's so naughty of you to even think about..."
            "[the_person.title] winks at you and spins, giving you a full look at her body."
            the_person.char "How will I ever get you to contain yourself?"
        else:
            the_person.char "Please [the_person.mc_title], a woman like me likes a little romance in her relationships. At least buy me dinner first."
    return

label reserved_cum_face(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 60:
            the_person.char "Ah, that's always a pleasure, [the_person.mc_title]."
        else:
            the_person.char "Well that's certainly a lot. I hope that means I did a satisfactory job."
    else:
        if the_person.sluttiness > 80:
            the_person.char "Oh [the_person.mc_title], what are you doing to me? I'm beginning to like looking like this!"
        else:
            the_person.char "Oh god [the_person.mc_title], could you imagine if someone saw me like this? I really should go and get cleaned up."
    return

label reserved_cum_mouth(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 60:
            the_person.char "Mmm, always a pleasure to taste you [the_person.mc_title]. I hope you had a good time."
        else:
            "[the_person.title] puckers her lips, obviously not happy with the taste but too polite to say anything."
    else:
        if the_person.sluttiness > 80:
            the_person.char "You're making me act like such a slut [the_person.mc_title], what would the other women think if they knew what I just did?"
        else:
            the_person.char "Well, at least there's no mess to clean up. I need to go wash my mouth out after that though."
    return

label reserved_cum_vagina(the_person):
    if mc.condom:
        if the_person.sluttiness > 75 or the_person.get_opinion_score("creampies") > 0:
            the_person.char "Oh... your seed is so close to me. Just a thin, thin condom in the way..."
        else:
            the_person.char "I can feel your seed through the condom. Well done, there's a lot of it."

    else:
        if the_person.sluttiness > 75 or the_person.get_opinion_score("creampies") > 0:
            if the_person.relationship != "Single":
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person.char "Yes, give me your seed!"
                the_person.char "If I become pregnant I can say it's my [so_title]'s. I'm sure he would believe it."
            else:
                the_person.char "Mmm, your semen is so nice and warm. I wonder how potent it is. You might have gotten me pregnant, you know."
        else:
            if the_person.relationship != "Single":
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person.char "Oh no... You need to cum outside of me [the_person.mc_title]."
                the_person.char "What would I tell my [so_title] if I got pregnant? He might not believe it's his!"
            else:
                the_person.char "Oh no... You need to cum outside of me [the_person.mc_title]."
                the_person.char "I'm in no position to be getting pregnant."
                the_person.char "Well, I suppose you have me in the literal position to get pregnant, but you know what I mean."
    return

label reserved_cum_anal(the_person):
    if the_person.sluttiness > 75 or the_person.get_opinion_score("anal creampies") > 0:
        the_person.char "Cum inside me [the_person.mc_title], fill my ass with your cum!"
    else:
        the_person.char "Oh lord, I hope I'm ready for this!"
    return

label reserved_suprised_exclaim(the_person):
    $rando = renpy.random.choice(["Oh my!","Oh, that's not good!", "Whoa!", "Ah!", "My word!", "Oops!", "Bah!", "Dangnabbit!"])
    the_person.char "[rando]"
    return

label reserved_talk_busy(the_person):
    if the_person.obedience > 120:
        the_person.char "I'd love to chat some more, but I've already spent far to much time getting distracted. Maybe we can catch up some other day, okay?"
    else:
        the_person.char "Sorry to interupt, but I've got some work I really need to see to. I'd love to catch up some other time though."
    return

label reserved_sex_strip(the_person):
    if the_person.sluttiness < 20:
        if the_person.arousal < 50:
            the_person.char "I think I can do away with this for a few minutes..."
        else:
            the_person.char "Oh, I bet this has been in your way the whole time..."

    elif the_person.sluttiness < 60:
        if the_person.arousal < 50:
            the_person.char "I think I'm past the point of needing this..."
        else:
            the_person.char "I don't need this any more, one second!"

    else:
        if the_person.arousal < 50:
            the_person.char "One moment, I'm wearing entirely too much right now."
        else:
            the_person.char "I need this off, I want to feel you against more of me!"

    return

label reserved_sex_watch(the_person, the_sex_person, the_position):
    if the_person.sluttiness < the_position.slut_requirement - 20:
        $ the_person.draw_person(emotion = "angry")
        the_person.char "Oh my god, I can't believe you're doing that here in front of everyone. Don't either of you have any decency?"
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

    elif the_person.sluttiness > the_position.slut_requirement and the_person.sluttiness < the_position.slut_cap:
        $ the_person.draw_person()
        the_person.char "Oh my..."
        $ change_report = the_person.change_slut_temp(2)
        "[the_person.title] watches quietly while you and [the_sex_person.name] [the_position.verb]."

    else:
        $ the_person.draw_person(emotion = "happy")
        the_person.char "Glad to see you two are having a good time. [the_person.mc_title], careful you aren't too rough with her."
        "[the_person.title] watches quietly while you and [the_sex_person.name] [the_position.verb]."
    return

label reserved_being_watched(the_person, the_watcher, the_position):
    if the_person.sluttiness >= the_position.slut_cap and the_watcher.sluttiness >= the_position.slut_cap:
        #They agree you should give it to her harder
        the_person.char "It's okay [the_person.mc_title], you don't have to be gentle with me."
        $ the_person.change_arousal(1)
        "[the_person.title] seems turned on by [the_watcher.title] watching you and her [the_position.verb]."

    elif the_person.sluttiness >= the_position.slut_cap and the_watcher.sluttiness < the_position.slut_requirement:
        #She's super slutty and doesn't care what people think.
        "[the_person.title] ignores [the_watcher.title] and keeps [the_position.verb] you."

    elif the_person.sluttiness >= the_position.slut_cap and the_watcher.sluttiness < the_position.slut_cap:
        #She's super slutty and encourages the watcher to be slutty.
        the_person.char "Mmm, come on [the_person.mc_title], let's give [the_watcher.title] a show!"
        $ the_person.change_arousal(1)
        "[the_person.title] seems turned on by [the_watcher.title] watching you and her [the_position.verb]."

    elif the_person.sluttiness < the_position.slut_cap and the_watcher.sluttiness >= the_position.slut_cap:
        #She's into it and encouraged by the slut watching her.
        the_person.char "Being watched shouldn't... I didn't think it would feel so good!"
        $ the_person.change_arousal(1)
        "[the_person.title] seems turned on by [the_watcher.title] watching you and her [the_position.verb]."

    elif the_person.sluttiness < the_position.slut_cap and the_watcher.sluttiness < the_position.slut_requirement:
        #She's into it but shamed by the prude watching her.
        the_person.char "Maybe [the_watcher.title] is right, we shouldn't be doing this..."
        $ the_person.change_arousal(-1)
        $ the_person.change_slut_temp(-1)
        "[the_person.title] seems uncomfortable with [the_watcher.title] nearby."

    else: #the_person.sluttiness < the_position.slut_cap and the_watcher.sluttiness < the_position.slut_cap:
        #They're both into it but not fanatical about it.
        the_person.char "Oh [the_watcher.title], you shouldn't be watching me do this..."
        $ the_person.change_arousal(1)
        $ the_person.change_slut_temp(1)
        "[the_person.title] seems more comfortable [the_position.verbing] you with [the_watcher.title] around."

    return

label reserved_work_enter_greeting(the_person):
    if the_person.happiness < 80 or the_person.love < 0:
        "[the_person.title] pretends not to notice you come into the room."

    elif the_person.happiness > 130:
        "[the_person.title] smiles happily when you come into the room."
        the_person.char "Hello [the_person.mc_title], always glad to have you stop by."

    else:
        if the_person.obedience < 100:
            "You pass by [the_person.title] as you enter the room. She's absorbed by her work and only gives you a grunt and a nod."
        else:
            "You pass by [the_person.title] as you enter the room. She looks up, startled."
            the_person.char "Oh! Sorry [the_person.mc_title], I was distracted and didn't notice you come in. Let me know if you need help with anything."
    return

label reserved_date_seduction(the_person):
    if the_person.relationship == "Single":
        if the_person.sluttiness > the_person.love:
            if the_person.sluttiness > 40:
                the_person.char "[the_person.mc_title], would you like to come back home with me? I've got some wonderful wine that makes me do crazy things."
            else:
                the_person.char "You were a fantastic date [the_person.mc_title]. I know I should be getting to bed soon, but would you like to come back for a quick drink?"
        else:
            if the_person.love > 40:
                the_person.char "You're such great company [the_person.mc_title]. Would you like to come back to my place so we can spend some more time together?"
            else:
                the_person.char "I had a fantastic night [the_person.mc_title]. Before you head home would you like to share a glass of wine with me?"
    else:
        $ so_title = SO_relationship_to_title(the_person.relationship)
        if the_person.sluttiness > the_person.love:
            if the_person.sluttiness > 40:
                the_person.char "[the_person.mc_title], would you like to come home with me tonight? My [so_title] is away on business and I'd love to drink some of his wine with you."
            else:
                the_person.char "This was a lot of fun. I shouldn't be out too late, but could I invite you back for a drink? My [so_title] shouldn't be home until much later."
        else:
            if the_person.love > 40:
                the_person.char "You're making me feel the same way I did when I first fell in love... Do you want to come back to my house to share one last drink?"
                the_person.char "My [so_title] won't be home until much later. I think he stays at work so late to avoid me."

            else:
                the_person.char "I had a fantastic night [the_person.mc_title], it's been so long since my [so_title] treated me this way."
                the_person.char "Would you like to share one last glass of wine at my house? My [so_title] is away on business, so I would be home all alone..."
    return

label reserved_sex_end_early(the_person):
    if the_person.sluttiness > 50:
        if the_person.love > 40:
            if the_person.arousal > 60:
                the_person.char "You're done? You're going to drive me crazy [the_person.mc_title], I'm so horny..."
            else:
                the_person.char "All done? I hope you were having a good time."
        else:
            if the_person.arousal > 60:
                the_person.char "That's all? I don't know how you can stop, I'm so horny after that!"
            else:
                the_person.char "Is that all? Well, that's disappointing."

    else:
        if the_person.love > 40:
            if the_person.arousal > 60:
                the_person.char "You're done? Well, you could have at least thought about me."
            else:
                the_person.char "All done? Maybe we can pick this up another time when we're alone."
        else:
            if the_person.arousal > 60:
                the_person.char "I... I don't know what to say, you've worn me out."
            else:
                the_person.char "That's all you wanted? I guess we're finished then."
    return


label reserved_sex_take_control (the_person):
    if the_person.arousal > 60:
        the_person.char "I can't let you go [the_person.mc_title], I'm going to finish what you started!"
    else:
        the_person.char "Do you think you're going somewhere? We're just getting started [the_person.mc_title]."
    return

label reserved_sex_beg_finish(the_person):
    "Wait, you aren't stopping are you? Please [the_person.mc_title], I'm so close to cumming, I'll do anything!"
    return


## Role Specific Section ##
label reserved_improved_serum_unlock(the_person):
    mc.name "[the_person.title], now that you've had some time in the lab there's something I wanted to talk to you about."
    the_person.char "Okay, how can I help?"
    mc.name "All of our research and development up until this point has been based on the limited notes I have from my university days. I'm sure there's more we could learn, and I want you to look into it for me."
    "[the_person.title] nods in agreement."
    the_person.char "I think I have an idea that could really help us along. All of our testing procedures focus on human safety, but what I really need to know about are the subjective effects of our creations."
    the_person.char "With your permission, I would like to take a dose of serum myself and have you record my experience with it."
    return

## Taboo break dialogue ##
label reserved_kissing_taboo_break(the_person):
    if the_person.effective_sluttiness() >= 30:
        the_person.char "Oh, well hello there! Do you... Want to do anything with me?"
    elif the_person.love >= 20:
        the_person.char "So you feel it too?"
        "She sighs happily."
        the_person.char "I... I want to kiss you. Would you kiss me?"
    else:
        the_person.char "I don't know if this is a good idea [the_person.mc_title]..."
        mc.name "Let's just see how it feels. Trust me."
        "[the_person.title] eyes you warely, but you watch her resolve break down."
        the_person.char "Okay... Just one kiss, to start."
    return

label reserved_touching_body_taboo_break(the_person):
    if the_person.effective_sluttiness() >= 30:
        the_person.char "Do you want to know something?"
        mc.name "What?"
        the_person.char "I've had dreams just like this before. They always stop just before you touch me."
        mc.name "Well, let's fix that right now."

    elif the_person.love >= 20:
        the_person.char "I want you to know I take this very seriously, [the_person.mc_title]."
        mc.name "Of course. So do I [the_person.title]."
        the_person.char "I normally wouldn't even think about letting someone like you touch me."
        mc.name "What do you mean \"Someone like me\"?"
        the_person.char "You're a trouble maker. I always get the feeling you're bad news for me, but..."
        the_person.char "But I just can't say no to you."
    else:
        the_person.char "You shouldn't be doing this [the_person.mc_title]. We... We barely know each other."
        mc.name "You don't want me to stop though, do you?"
        the_person.char "I don't... I don't know what I want."
        mc.name "Then let me show you."
    return

label reserved_touching_penis_taboo_break(the_person):
    if the_person.effective_sluttiness() >= 35:
        the_person.char "Look at how big your penis is. You poor thing, that must be very uncomfortable."
        the_person.char "Just relax and I'll see what I can do about it, okay?"
    elif the_person.love >= 20:
        the_person.char "Oh my... If I'm honest I wasn't expecting it to be quite so... Big."
        mc.name "Don't worry, it doesn't bite. Go ahead and touch it, I want to feel your hand on me."
        "She bites her lip playfully."
    else:
        the_person.char "We should stop here... I don't want you to get the wrong idea about me."
        mc.name "Look at me [the_person.mc_title], I'm rock hard. Nobody would ever know if you gave it a little feel."
        "You see her resolve waver."
        the_person.char "It is very... Big. Just feel it for a moment?"
        mc.name "Just a moment. No longer than you want to."
        "She bites her lip as her resolve breaks completely."
    return

label reserved_touching_vagina_taboo_break(the_person):
    if the_person.effective_sluttiness() >= 35:
        the_person.char "Do it [the_person.mc_title]. Touch my pussy."
    elif the_person.love >= 20:
        the_person.char "I'm so nervous [the_person.mc_title], do you feel that way too?"
        mc.name "Just take a deep breath and relax. You trust me, right?"
        the_person.char "Of course. I trust you."
    else:
        the_person.char "I don't know if we should be doing this [the_person.mc_title]..."
        mc.name "Just take a deep breath and relax. I'm just going to touch you a little, and if you don't like it I'll stop."
        the_person.char "Just a little?"
        mc.name "Just a little. Trust me, it's going to feel amazing."
    return

label reserved_sucking_cock_taboo_break(the_person):
    mc.name "I want you to do something for me."
    the_person.char "What would you like?"
    mc.name "I'd like you to suck on my cock."
    if the_person.effective_sluttiness() >= 45:
        the_person.char "I... I really should say no."
        mc.name "But you aren't going to."
        "She shakes her head."
        the_person.char "I've told people all my life that I didn't do things like this, but now it's all I can think about."
    elif the_person.love >= 30:
        the_person.char "Oh [the_person.mc_title]! Really? I know most men are into that sort of thing, but I..."
        the_person.char "Well, I think I'm a little classier than that."
        mc.name "What's not classy about giving your partner pleasure? Come on [the_person.title], aren't you a little curious?"
        the_person.char "I'm curious, but I... Well... How about I just give it a taste and see how that feels?"
        mc.name "Alright, we can start slow and go from there."
    else:
        the_person.char "I'm sorry, I think I misheard you."
        mc.name "No you didn't. I want you to put my cock in your mouth and suck on it."
        the_person.char "I could never do something like that [the_person.mc_title], what would people think?"
        the_person.char "I'm not some kind of slut, I don't \"suck cocks\"."
        mc.name "Yeah you do, and you're going to do it for me."
        the_person.char "Why would I do that?"
        mc.name "Because deep down, you want to. You can be honest with me, aren't you a little bit curious what it's going to be like?"
        "She looks away, but you both know the answer."
        mc.name "Just get on your knees, put it in your mouth, and if you don't like how it feels you can stop."
        the_person.char "What are you doing to me [the_person.mc_title]? I use to think I was better than this..."
    return

label reserved_licking_pussy_taboo_break(the_person):
    mc.name "I want to taste your pussy [the_person.title]. Are you ready?"
    if the_person.effective_sluttiness() >= 45:
        the_person.char "Oh what a gentleman I have! I'm ready [the_person.mc_title], eat me out!"
    elif the_person.love >= 30:
        the_person.char "You're such a gentleman [the_person.mc_title], but you don't have to do that."
        mc.name "I don't think you understand. I {i}want{/i} to eat you out, I'm not doing it as a favour."
        "[the_person.title] almost seems confused by the idea."
        the_person.char "Oh... Well then, I suppose you can get right to it."
    else:
        the_person.char "You're a gentleman [the_person.mc_title], but you don't need to do that."
        if not the_person.has_taboo("sucking_cock"):
            the_person.char "It's flattering that you'd want to return the favour though, so thank you."

        mc.name "No, I don't think you understand what I'm saying. I {i}want{/i} to eat you out, I'm not doing it as a favour."
        "[the_person.title] almost seems confused by the idea."
        the_person.char "Really? I mean... I just haven't met many men who want to do that."
        mc.name "Well you have one now. Just relax and enjoy yourself."
    return

label reserved_vaginal_sex_taboo_break(the_person):
    if the_person.effective_sluttiness() >= 60:
        the_person.char "[the_person.mc_title], I'm not ashamed to say I'm very excited right now!"
        "She giggles gleefully."
        the_person.char "Come on and fuck me!"
    elif the_person.love >= 45:
        the_person.char "Go ahead [the_person.mc_title]. I think we're both ready for this."
    else:
        if the_person.has_taboo("anal_sex"):
            the_person.char "Oh my god, what am I doing here [the_person.mc_title]?"
            the_person.char "I'm not the type of person to do this... Am I? Is this who I've always been, and I've just been lying to myself?"
            mc.name "Don't overthink it. Just listen to your body and you'll know what you want to do."
            "She closes her eyes and takes a deep breath."
            the_person.char "I... I want to have sex with you. I'm ready."
        else:
            the_person.char "I'm glad you're doing this properly this time."
            "It might be the hot new thing to do, but I just don't enjoy anal. I think your cock will feel much better in my vagina."
    return

label reserved_anal_sex_taboo_break(the_person):
    if the_person.effective_sluttiness() >= 75:
        "She takes a few deep breaths."
        the_person.char "I'm ready if you are [the_person.mc_title]. Come and fuck my ass."

    elif the_person.love >= 60:
        the_person.char "This is really something you want to do then [the_person.mc_title]?"
        mc.name "Yeah, it is."
        the_person.char "Okay then. It wouldn't be my first pick, but we can give it a try."
        the_person.char "I don't know if you'll even fit though. You're penis is quite large."
        mc.name "You'll stretch out more than you think."
    else:
        if the_person.has_taboo("vaginal_sex"):
            the_person.char "Oh lord, what happened to me?"
            the_person.char "I thought I was a respectable lady, now I'm about to get fucked in the ass..."
            the_person.char "We've never even had sex before and now I'm doing anal!"

            #TODO: "At least my vagina still belongs to my SO... At least I still have that one thing."

        else:
            the_person.char "I'm not sure about this [the_person.mc_title]... I'm not even sure if you can fit inside me there!"
            mc.name "I can stretch you out, don't worry about that."
            the_person.char "Oh lord, what happened to me..."
            the_person.char "I use to think I was a respectable lady, now I'm about to get fucked in the ass..."
        mc.name "Relax, you'll be fine and this isn't the end of the world. Who knows, you might even enjoy yourself."
        the_person.char "I doubt it. Come on then, there's no point stalling any longer."
    return

label reserved_condomless_sex_taboo_break(the_person):
    if the_person.get_opinion_score("bareback sex") > 0:
        the_person.char "You want to have sex without any protection? I'll admit, that would really turn me on."
        if the_person.get_opinion_score("creampies") > 0:
            the_person.char "It would be very naughty if you came inside me though..."
            mc.name "Don't you think we're being naughty already?"
            "She bites her lip and nods."
            the_person.char "I think we are."
        elif the_person.get_opinion_score("creampies") < 0:
            the_person.char "You will need to pull out though. I hate having dripping out of me all day."
        else:
            the_person.char "You will need to pull out though, understood? Good."

    elif the_person.love > 60:
        the_person.char "If you think you're ready for this commitment, I am to. I want to feel close to you."
        if the_person.get_opinion_score("creampies") > 0:
            the_person.char "When you're going to finish you don't have to pull out unless you want to. Okay?"
            mc.name "Are you on the pill?"
            "She shakes her head."
            the_person.char "No, but I trust you to make the decision that is right for both of us."
        elif the_person.get_opinion_score("creampies") < 0:
            if the_person.kids == 0:
                the_person.char "You will have to pull out though, okay? I really don't plan on being a mother."
            else:
                the_person.char "You will have to pull out though, okay? I've been pregnant before and it isn't pretty."
        else:
            if the_person.kids == 0:
                the_person.char "You will have to pull out though. I don't want you to make me a mother."
            else:
                the_person.char "You will have to pull out though, understood? I don't think either of us are ready for that."

    else:
        the_person.char "You want to have sex without protection? That's very risky [the_person.mc_title]."
        if the_person.has_taboo("vaginal_sex"):
            mc.name "I want our first time to be special though, don't you?"
            "She takes a second to think, then nods."
            the_person.char "I do. You need to be very careful where you finish, okay?"
        else:
            mc.name "It will feel so much better raw, for both of us."
            the_person.char "I have wondered what it would be like..."
            "She takes a moment to think, then nods."
            the_person.char "Fine, you don't need a condom. Please be very careful where you finish, okay?"
    return

label reserved_underwear_nudity_taboo_break(the_person, the_clothing):
    if the_person.effective_sluttiness() > 30 - (the_person.get_opinion_score("skimpy outfits") * 5):
        the_person.char "This is the first time you've gotten to see my underwear. I hope you like what you see."
        if the_person.has_taboo(["bare_tits","bare_pussy"]):
            mc.name "I'm sure I will. You have good taste."
            the_person.char "Well then, what are you waiting for then?"
        else:
            mc.name "I've already seen you out of your underwear, but I'm sure it complaments your form."
            the_person.char "Time to find out. What are you waiting for?"

    elif the_person.love > 15:
        the_person.char "This is going to be the first time you've seen me in my underwear. I have to admit, I'm feeling a little nervous."
        if the_person.has_taboo(["bare_tits","bare_pussy"]):
            mc.name "Don't be, I'm sure you look stunning in it."
            the_person.char "Well then, take off my [the_clothing.display_name] for me."

        else:
            mc.name "I already know you have a beautiful body, some nice underwear can only enhance the experience."
            the_person.char "You're too kind. Help me take off my [the_clothing.display_name]."

    else:
        the_person.char "If I take off my [the_clothing.display_name] you'll see me in my underwear."
        mc.name "That's the plan, yes."
        the_person.char "I shouldn't be going around half naked for men I barely know. What would people think?"
        mc.name "Why do you care what other people think? Forget about them and just focus on us."

        if the_person.has_taboo(["bare_tits","bare_pussy"]):
            mc.name "Why do you care what other people think? Forget about them and just focus on the moment."
            the_person.char "I'll try..."

        else:
            mc.name "You might have wanted to worry about that before I saw you naked. You don't have anything left to hide."
            the_person.char "I suppose you're right..."
    return

label reserved_bare_tits_taboo_break(the_person, the_clothing):
    if the_person.effective_sluttiness() > (40 - the_person.get_opinion_score("showing her tits") * 5):
        the_person.char "Oh, so you want to take a look at my breasts?"
        if the_person.has_large_tits():
            "She bounces her chest for you, jiggling the big tits hidden underneath her [the_clothing.display_name]."
        else:
            "She bounces her chest and gives her small tits a little jiggle."
        the_person.char "Well it would be a shame not to let you get a glimpse, right? I've been waiting for you to ask."
        mc.name "Let's get that [the_clothing.display_name] off so I can see them then."

    elif the_person.love > 25:
        the_person.char "Oh, you want to get my breasts out?"
        if the_person.has_large_tits():
            "She looks down at her own large rack, tits hidden restrained by her [the_clothing.display_name]."
            the_person.char "I don't have to ask why. I'm glad you're interested in them."
        else:
            the_person.char "I'm glad you're still interested in smaller breasts. It seems like every man is mad boob-crazy these days."
        mc.name "Of course I'm interested. let's get that [the_clothing.display_name] out of the way so I can get a good look at you."

    else:
        the_person.char "Hey there! If you take off my [the_clothing.display_name] I won't be decent any more!"
        mc.name "I want to see your tits and it's in the way."
        the_person.char "I'm aware it's \"in the way\", that's why I put it on this morning."
        if the_person.has_large_tits() and the_clothing.underwear:
            the_person.char "Besides, a girl like me needs a little support. These aren't exactly light."
        mc.name "Come on [the_person.title]. You're gorgeous, I'm just dying to see more of you."
        the_person.char "Well I'm glad I have that effect on you. I suppose..."
        "She takes a moment to think, then sighs and nods."
        the_person.char "You can take off my [the_clothing.display_name] and have a look. Just be kind to me, I'm feeling very vulnerable."
    return

label reserved_bare_pussy_taboo_break(the_person, the_clothing):
    if the_person.effective_sluttiness() > (50 - the_person.get_opinion_score("showing her ass") * 5):
        the_person.char "You want to get me out of my [the_clothing.display_name]? Well, I'm glad you've finally asked."

    elif the_person.love > 35:
        the_person.char "Oh, careful there [the_person.mc_title]. If you take off my [the_clothing.display_name] I won't be decent any more."
        if the_person.has_taboo("touching_vagina"):
            mc.name "I don't particularly want you to be decent at the moment, though. I want to get a look at your sweet pussy."
            the_person.char "Oh stop, you're going to make me blush."
            "She thinks for a moment, then nods timidly."
            the_person.char "Okay, you can take it off and have a look, if you'd like."

        else:
            mc.name "I think you stopped being decent when you let me touch your pussy."
            the_person.char "Oh stop, you. I suppose you can take it off and have a look, if you'd like."

    else:
        the_person.char "Oh! Careful, or you're going to have me showing you everything!"
        mc.name "That is what I was hoping for, yeah."
        the_person.char "Well! I mean... I'm not that sort of woman [the_person.mc_title]!"
        if the_person.has_taboo("touching_vagina"):
            mc.name "Don't you want to be though? Don't you want me to enjoy your body?"
            the_person.char "I... I mean, I might, but I shouldn't... You shouldn't..."
        else:
            mc.name "Of course you are! I've had my hand on your pussy already, I just want to see what I was feeling before."
            the_person.char "I... I mean, that wasn't... I..."

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

    return

label reserved_anal_creampie_taboo_break(the_person):

    return
