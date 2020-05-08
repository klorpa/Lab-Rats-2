### PERSONALITY CHARACTERISTICS ###
init 1300:
    python:
        def wild_titles(the_person):
            return the_person.name
        def wild_possessive_titles(the_person):
            return wild_titles(the_person)
        def wild_player_titles(the_person):
            return mc.name
        wild_personality = Personality("wild", #Stephanie style personality
        common_likes = ["skirts", "small talk", "Fridays", "the weekend", "the colour red", "makeup", "flirting", "marketing work","heavy metal","punk"],
        common_sexy_likes = ["anal creampies", "doggy style sex", "giving blowjobs", "getting head", "anal sex", "public sex", "skimpy outfits", "showing her tits", "showing her ass", "taking control", "not wearing underwear", "creampies", "bareback sex"],
        common_dislikes = ["Mondays", "the colour pink", "supply work", "conservative outfits", "work uniforms"],
        common_sexy_dislikes = ["being submissive", "being fingered", "missionary style sex", "giving handjobs"],
        titles_function = wild_titles, possessive_titles_function = wild_possessive_titles, player_titles_function = wild_player_titles)

        list_of_personalities.append(wild_personality)

### DIALOGUE ###
label wild_introduction(the_person):
    mc.name "Excuse me, could I bother you for a moment?"
    "She turns around and looks you up and down."
    #TODO: Have this differ based on personality
    $ the_person.set_title("???")
    the_person.char "Uh, sure? What do you want?"
    mc.name "I know this sounds crazy, but I saw you and just wanted to say hi and get your name."
    "She laughs and crosses her arms."
    $ title_choice = get_random_title(the_person)
    $ formatted_title = the_person.create_formatted_title(title_choice)
    the_person.char "Yeah? Well I like the confidence, I'll say that. My name's [formatted_title]."
    $ the_person.set_title(title_choice)
    $ the_person.set_possessive_title(get_random_possessive_title(the_person))
    the_person.char "And what about you, random stranger? What's your name?"
    return

label wild_greetings(the_person):
    if the_person.love < 0:
        the_person.char "Oh god, what do you want now?"
    elif the_person.happiness < 90:
        the_person.char "Hey. I hope you're having a better day than I am."
    else:
        if the_person.sluttiness > 60:
            if the_person.obedience > 130:
                the_person.char "Hello there [the_person.mc_title]. How can I help you, do you have anything that needs attention? Anything at all?"
            else:
                the_person.char "Hey there [the_person.mc_title], I hope this is for pleasure and not business."
        else:
            if the_person.obedience > 130:
                the_person.char "Hello [the_person.mc_title]"
            else:
                the_person.char "Hey, how's it going?"
    return

label wild_sex_responses_foreplay(the_person):
    if the_person.arousal < 25:
        if the_person.sluttiness > 50:
            the_person.char "Oh fuck, I love the way you touch me!"
        else:
            the_person.char "Oh... Oh fuck that feels nice!"

    elif the_person.arousal < 50:
        if the_person.sluttiness > 50:
            the_person.char "It feels so fucking good when you touch me like that!"
        else:
            the_person.char "Mmm, keep going [the_person.mc_title]. Just keep going."

    elif the_person.arousal < 75:
        if the_person.sluttiness > 50:
            the_person.char "Mmm, touch me all over. I'm your dirty slut and you can do anything you want with me!"
        else:
            the_person.char "Touch me, [the_person.mc_title], I'm all yours!"
    else:
        if the_person.sluttiness > 50:
            if the_person.relationship == "Single":
                the_person.char "Oh fuck, I'm going to cum soon. I can feel it happening, you're getting me so close!"
            else:
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person.char "The way you feel is so different from my [so_title]. For some reason your touch is the one that drives me crazy."
        else:
            the_person.char "Don't stop! You're going to make me cum - don't you dare stop!"

    return

label wild_sex_responses_oral(the_person):
    if the_person.arousal < 25:
        if the_person.sluttiness > 50:
            the_person.char "Mmm, I love getting some good head."
        else:
            the_person.char "Fuck me that feels real nice."

    elif the_person.arousal < 50:
        if the_person.sluttiness > 50:
            the_person.char "Eat me out [the_person.mc_title], your tongue feels amazing!"
        else:
            the_person.char "That feels so good, you have no idea!"

    elif the_person.arousal < 75:
        if the_person.sluttiness > 50:
            the_person.char "Mmm, lick that pussy! Ah!"
        else:
            the_person.char "Oh god, yes! Yes!"
    else:
        if the_person.sluttiness > 50:
            if the_person.relationship == "Single":
                the_person.char "Fuck fuck fuck, that's it right there!"
            else:
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person.char "My [so_title] never eats me out like this, [the_person.mc_title]!"
                the_person.char "Make me cum my brains out and forget about him!"
        else:
            the_person.char "Don't stop! You're going to make me cum, don't you dare stop!"

    return

label wild_sex_responses_vaginal(the_person):
    if the_person.arousal < 25:
        if the_person.sluttiness > 50:
            the_person.char "Oh fuck, I never get tired of feeling you inside me!"
        else:
            the_person.char "Oh... Oh fuck me your cock feels nice..."

    elif the_person.arousal < 50:
        if the_person.sluttiness > 50:
            the_person.char "Mmm, you feel so good fucking my pussy!"
        else:
            the_person.char "Ah, fuck me just like that!"

    elif the_person.arousal < 75:
        if the_person.sluttiness > 50:
            the_person.char "That's right, use me like your dirty little slut and fuck my pussy raw!"
        else:
            the_person.char "Oh fuck yes, fuck yes!"
    else:
        if the_person.sluttiness > 50:
            if the_person.relationship == "Single":
                the_person.char "Fuck! I'm... You're cock is going to make me cum! I want you to make me cum!"
            else:
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person.char "Your cock is stretching me out, my [so_title] is never going to be enough for me after this!"
                the_person.char "Oh well, fuck him! Keep going and make me cum!"

        else:
            the_person.char "Don't stop fucking me! You're going to make me cum, I can feel it!"

    return

label wild_sex_responses_anal(the_person):
    if the_person.arousal < 25:
        if the_person.sluttiness > 50:
            the_person.char "Oh fuck, I'm never get use to being stretched out like this."
        else:
            the_person.char "Oh... Oh fuck my ass!"

    elif the_person.arousal < 50:
        if the_person.sluttiness > 50:
            the_person.char "Gah! Ah! Fuck!"
        else:
            the_person.char "God, I won't be able to sit for a week after this..."

    elif the_person.arousal < 75:
        if the_person.sluttiness > 50:

            the_person.char "Give it to me, fuck my asshole raw!"
        else:
            the_person.char "Ah! Why does your cock have to be so fucking big?!"
    else:
        if the_person.sluttiness > 50:
            if the_person.relationship == "Single":
                the_person.char "Fuck, I can't believe I'm going to cum from your cock up my ass!"
            else:
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person.char "Wreck my ass [the_person.mc_title], send me back to my [so_title] gaping and ruined! Ah!"

                the_person.char "I might have a [so_title], but he doesn't drive me crazy like you do [the_person.mc_title]!"
                the_person.char "Make me cum my brains out! Screw my [so_title], he's not half the man you are!"
        else:
            the_person.char "Fuck, I can't believe it but I think I'm going to cum soon!"

    return

label wild_climax_responses_foreplay(the_person):
    if the_person.sluttiness > 50:
        the_person.char "Oh fuck yes, I'm going to cum! I'm cumming!"
    else:
        the_person.char "Oh fuck, you're going to make me cum! Fuck!"
        "She goes silent, then lets out a shuddering moan."
    return

label wild_climax_responses_oral(the_person):
    if the_person.sluttiness > 70:
        the_person.char "Fuck yes, I'm going to cum! Make me cum!"
    else:
        the_person.char "Oh my god, you're good at that! I'm going to... I'm going to cum!"
    return

label wild_climax_responses_vaginal(the_person):
    if the_person.sluttiness > 70:
        the_person.char "Ah! More! I'm going to... Ah! Cum! Fuck!"
        "She closes her eyes and squeals with pleasure."
    else:
        the_person.char "Oh god, I'm going to... Oh fuck me! Ah!"
    return

label wild_climax_responses_anal(the_person):
    if the_person.sluttiness > 70:
        the_person.char "Oh fuck, your cock feels so huge in my ass! It's going to make me cum!"
        the_person.char "Ah! Mmhmmm!"
    else:
        the_person.char "Oh fucking shit, I think you're going to make me..."
        "She barely finishes her sentence before her body is wracked with pleasure."
        the_person.char "Cum!"
    return

label wild_clothing_accept(the_person):
    if the_person.obedience > 130:
        the_person.char "You think it will look good on me? I guess that's all I need to hear then."
    else:
        the_person.char "Hey, thanks. That's a good look, I like it."
    return

label wild_clothing_reject(the_person):
    if the_person.obedience > 130:
        the_person.char "I don't... I'm sorry, but I really don't think I could get away with wearing something like this. I appreciate the thought though."
    else:
        if the_person.sluttiness > 60:
            the_person.char "Jesus, you didn't leave much to the imagination, did you? I don't think I can wear this."
        else:
            the_person.char "There's not much of an outfit to this outfit. Thanks for the thought, but there's no way I could wear this."
    return

label wild_clothing_review(the_person):
    if the_person.obedience > 130:
        the_person.char "Oh man, I'm a mess. I'll be back in a moment, I'm just going to get cleaned up for you."
    else:
        if the_person.sluttiness > 40:
            the_person.char "I don't think everyone else would appreciate me going around dressed like this as much as you would. I'll be back in a second, I just want to get cleaned up."
        else:
            the_person.char "Damn, everything's out of place after that. Wait here a moment, I'm just going to find a mirror and try and look presentable."
    return

label wild_strip_reject(the_person):
    if the_person.obedience > 130:
        the_person.char "Could we leave that where it is for now, please?"
    elif the_person.obedience < 70:
        the_person.char "No, no, no, I'll decide what comes off and when, okay?"
    else:
        the_person.char "Not yet... get me a little warmed up first, okay?"
    return

label wild_sex_accept(the_person):
    if the_person.sluttiness > 70:
        if the_person.obedience < 70:
            the_person.char "Let's do it. Once you've had your fill I have a few ideas we could try out."
        else:
            the_person.char "I was hoping you would suggest that, just thinking about it gets me excited."
    else:
        the_person.char "You want to give it a try? Okay, let's try it."
    return

label wild_sex_obedience_accept(the_person):
    if the_person.sluttiness > 70:
        the_person.char "God, what have you done to me? I should say no, but... I just want you to use me however you want, [the_person.mc_title]."
    else:
        if the_person.obedience > 130:
            the_person.char "If that's what you want to do then I'll what you tell me to do."
        else:
            the_person.char "I shouldn't... but if you want to try it out I'm game. Try everything once, right?"
    return

label wild_sex_gentle_reject(the_person):
    if the_person.sluttiness > 50:
        the_person.char "Not yet [the_person.mc_title], get me warmed up first."
    else:
        the_person.char "Wait, I just... I don't think I'm ready for this. I want to fool around, but let's keep it casual."
    return

label wild_sex_angry_reject(the_person):
    if not the_person.relationship == "Single":
        $ so_title = SO_relationship_to_title(the_person.relationship)
        the_person.char "What? I have a [so_title], so you can forget about doing anything like that. Ever."
        "She glares at you, then walks away."
    elif the_person.sluttiness < 20:
        the_person.char "I'm sorry, what!? No, you've massively misread the situation, get the fuck away from me!"
        "[the_person.title] glares at you and steps back."
    else:
        the_person.char "What? That's fucking disgusting, I can't believe you'd even suggest that to me!"
        "[the_person.title] glares at you and steps back."
    return

label wild_seduction_response(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 50:
            the_person.char "Oh, I think I know what you need right now. Let me take care of you."
        else:
            the_person.char "Right now? Okay, lead the way I guess."
    else:
        if the_person.sluttiness > 50:
            the_person.char "Mmm, you're feeling as horny as me then? Come on, let's go."
            "[the_person.title] takes your hand and leads you off to find some place out of the way."
        elif the_person.sluttiness > 10:
            the_person.char "I know that look you're giving me, I think I know what you want."
        else:
            the_person.char "[mc.name], I know what you mean... Okay, I can spare a few minutes."
    return

label wild_seduction_accept_crowded(the_person):
    if the_person.relationship == "Single":
        if the_person.sluttiness < 20:
            the_person.char "Alright, let's slip away for a few minutes and you can convince me a little more."
        elif the_person.sluttiness < 50:
            the_person.char "Come on, I know someplace nearby where we can get a few minutes privacy."
        else:
            the_person.char "Oh my god. I hope you aren't planning on making me wait [the_person.mc_title], because I don't know if I can!"
    else:
        $ so_title = SO_relationship_to_title(the_person.relationship)
        if the_person.sluttiness + (5*the_person.get_opinion_score("cheating on men")) > 50:
            the_person.char "Fuck, let's get this party started!"
            the_person.char "I hope you don't mind that I've got a [so_title], because I sure as hell don't right now!"
        else:
            the_person.char "God damn it, you're bad for me [the_person.mc_title]... Come on, we need to go somewhere quiet so my [so_title] doesn't find out about this."
    return

label wild_seduction_accept_alone(the_person):
    if the_person.relationship == "Single":
        if the_person.sluttiness < 20:
            the_person.char "Well, I think you deserve a chance to impress me."
        elif the_person.sluttiness < 50:
            the_person.char "Mmm, well let's get this party started and see where it goes."
        else:
            the_person.char "Fuck, I'm glad you're as horny as I am right now. Come on, I can't wait any more!"
    else:
        $ so_title = SO_relationship_to_title(the_person.relationship)
        if the_person.sluttiness + (5*the_person.get_opinion_score("cheating on men")) > 50:
            the_person.char "Fuck, you know how to turn me on in ways my [so_title] never can. Come here!"
        else:
            the_person.char "You're such bad news [the_person.mc_title]... I have a [so_title], but all I can ever think of is you!"
    return

label wild_seduction_refuse(the_person):
    if the_person.sluttiness < 20:
        the_person.char "Sorry [the_person.mc_title], I'm not really in the mood to flirt or fool around."
        "[the_person.title] shrugs unapologetically."

    elif the_person.sluttiness < 50:
        the_person.char "I'll admit it, you're tempting me, but I'm not in the mood to fool around right now. Maybe some other time though, I think we could have a lot of fun together."

    else:
        the_person.char "Shit, that sounds like a lot of fun [the_person.mc_title], but I'm not feeling it right now. Hang onto that thought and we can fool around some other time."
    return

label wild_flirt_response(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 50:
            the_person.char "You know that all you have to do is ask and it's all yours."
        else:
            the_person.char "Thank you [the_person.mc_title], I'm glad you're enjoying the view."

    elif not the_person.relationship == "Single":
        $so_title = SO_relationship_to_title(the_person.relationship)
        if the_person.sluttiness + (the_person.get_opinion_score("cheating on men")*5) > 50:
            the_person.char "Then why don't you do something about it? Come on, we don't have to tell my [so_title] anything at all, right?"
            "[the_person.title] winks and spins around, giving you a full look at her body."
        else:
            the_person.char "You're playing with fire [the_person.mc_title]. I've got a [so_title], and I don't think he'd appreciate you flirting with me."
            mc.name "What about you, do you appreciate it?"
            "She gives a coy smiles and shrugs."
            the_person.char "Maybe I do."

    else:
        if the_person.sluttiness > 50:
            the_person.char "Then why don't you do something about it? Come on, all you have to do is ask."
            "[the_person.title] smiles at you and spins around, giving you a full look at her body."
        else:
            the_person.char "Well thank you, play your cards right and maybe you'll get to see a little bit more."
            the_person.char "You'll have to really impress me though, I have high standards."
    return

label wild_flirt_response_low(the_person):
    if the_person.outfit == the_person.planned_uniform:
        if the_person.judge_outfit(the_person.outfit):
            #She's in uniform and likes how it looks.
            the_person.char "Thanks! I think I look pretty cute in it too."
            the_person.char "It's nice to work somewhere where I can show off a little."
            "She smiles and gives you a quick turn to either side, showing off her hips."
        else:
            #She's in uniform, but she thinks it's a little too slutty.
            if the_person.outfit.vagina_visible():
                # Her pussy is on display.
                the_person.char "I'm sure you like it; I'm practically naked!"
                mc.name "Well, you know that it's..."
                the_person.char "I know, I know. It's company policy. I'm not complaining, exactly. It's kind of fun."
                mc.name "Give it some time and you'll get use to it."
                "She smiles and nods."
                the_person.char "I'm sure I will."

            elif the_person.outfit.tits_visible():
                # Her tits are out
                the_person.char "Thanks! I'm still getting use to being so... exposed in this uniform. At least I don't have to wear a bra!"
                mc.name "You look incredible and you're comfortable. I call that a success."
                "She laughs and shrugs."
                the_person.char "Sure, I guess you could call it that."
    #
            elif the_person.outfit.underwear_visible():
                # Her underwear is visible.
                the_person.char "Thanks! I probably would have picked something that kept me a little more covered, but at our uniform is comfortable."
                mc.name "It may be a little unconventional, but you look fantastic. You've got exactly the right kind of body for it."
                the_person.char "Well that's good to know."
                "She smiles and gives you a quick turn to either side, showing off her body."
            else:
                # It's just generally slutty.
                the_person.char "Well thank you! Our uniforms are a little bold for my taste, but I'm glad I look good in it."
                "She smiles and gives you a quick turn to either side, showing off her body for you."

    else:
        #She's in her own outfit.
        the_person.char "Thanks! It's really cute, right?"
        $ the_person.draw_person(position = "walking_away")
        "She smiles and gives you a quick spin, showing off her outfit from every angle."
        $ the_person.draw_person()
    return

label wild_flirt_response_mid(the_person):
    if the_person.outfit == the_person.planned_uniform:
        if the_person.judge_outfit(the_person.outfit):
            if the_person.outfit.tits_visible():
                the_person.char "Are you sure you don't mean my tits look good in this outfit?"
                "She winks and wiggles her shoulders, setting her boobs jiggling for you."
                mc.name "All of you looks good, tits included."
                the_person.char "Good answer. I think these uniforms are pretty hot too. You've got some good fashion sense."
            else:
                the_person.char "Aw, thanks! I think your uniforms look pretty hot on me too. You've got some good fashion sense."
            the_person.char "Maybe I'll invite you shopping one day and you can tell me what else you want to see me in."
            mc.name "Sounds like a good time."

        else:
            # the_person.char "I think it shows off a little too much!"
            the_person.char "Thanks, but I think these uniforms show off just a little too much of my fabulous body."
            if the_person.outfit.vagina_visible():
                the_person.char "I mean, look at me! I feel like you should be throwing twenties at me every time I walk away."
            elif the_person.outfit.tits_visible():
                the_person.char "I mean, look at me! I feel like you should be tucking a twenty into my underwear every time I want to talk to you."
            else:
                the_person.char "I mean, look at it! I feel like an underwear model every time I get dressed for work."
            mc.name "I understand, but I promise it's important for the business."
            "She sighs and nods."
            the_person.char "Yeah, I know. At least you're having a good time. I don't mind that so much."

    else:
        if the_person.effective_sluttiness() < 20 and mc.location.get_person_count() > 1:
            if the_person.outfit.tits_visible():
                the_person.char "Are you sure you don't mean my tits look good in this outfit?"
                "She winks and wiggles her shoulders, setting her boobs jiggling for you."
                mc.name "All of you looks good, tits included."
                the_person.char "Good answer. I knew you would like this look when I was picking it out this morning."
            else:
                the_person.char "Aw, thanks! I thought this was a pretty hot look when I was getting dressed this morning."

            the_person.char "Maybe I'll invite you shopping one day, so you can tell me else you want to see me in."
            mc.name "I can think of a few things already."
            the_person.char "I'm sure you can."

        else:
            the_person.char "Thanks, I thought I looked pretty hot in it too."
            the_person.char "You want a better look, right? Here, how does it make my ass look?"
            $ the_person.draw_person(position = "back_peek")
            the_person.char "Good, right?"
            mc.name "Fantastic. I wish I could get an even better look at it."
            "[the_person.possessive_title] smiles and turns back to face you."
            $ the_person.draw_person()
            the_person.char "I'm sure you do. Take me out for a drink and maybe we can work something out."
    return

label wild_flirt_response_high(the_person):
    if mc.location.get_person_count() > 1 and the_person.effective_sluttiness() < (25 - (5*the_person.get_opinion_score("public_sex"))): # There are other people here, if she's not slutty she asks if you want to find somewhere quiet
        the_person.char "Driving you crazy, huh? Well..."
        "She glances around before smiling mischievously."
        the_person.char "We'll have to do something about that, but not here."
        menu:
            "Find someplace quiet.":
                mc.name "Then let's find somewhere that isn't here."
                the_person.char "Eager, huh? Alright, let's go find somewhere."
                "You and [the_person.possessive_title] leave and find a quiet spot where you won't be interupted."
                the_person.char "So... Now what's your plan?"

                if the_person.has_taboo("kissing"):
                    "You step close to [the_person.title] and put your arm around her waist, pulling her close."
                    $ the_person.call_dialogue("kissing_taboo_break")
                    $ the_person.break_taboo("kissing")
                    "You kiss her. She eagerly presses her body against yours in response."
                else:
                    "You step close to [the_person.title] and put your arm around her waist, pulling her close and kissing her."
                    "She responds immediately and eagerly presses her body against yours."
                call fuck_person(the_person, private = True, start_position = kissing, skip_intro = True) from _call_fuck_person_49

            "Just flirt.":
                mc.name "Not here, huh? How about back at your place then?"
                the_person.char "Bold. I like it. Maybe if you buy me dinner you'll get your chance."

    else:
        if mc.location.get_person_count() == 1: #You're alone, so she just didn't meet the sluttiness threshold
            "[the_person.possessive_title] bites her lower lip and glances around, confirming you're alone."
            the_person.char "Well it's just the two of us here, so now's your chance to find out. What's your plan?"

        else:  # You aren't alone but she's still into it.
            the_person.char "Feeling bold today, huh? Well I think your chances are pretty good."
            if the_person.has_large_tits(): #Bounces her tits for you
                $ the_person.draw_person(the_animation = blowjob_bob)
                "[the_person.title] grabs her tits and jiggles them for you."
                the_person.char "Maybe I can get these girls out for you. Does that sound nice?"

            else: #No big tits, so she can't bounce them (as much)
                "[the_person.title] runs her hands over her hips sensually, obviously encouraging you to take things furthur."

        menu:
            "Kiss her.":

                $ the_person.draw_person()
                if the_person.has_taboo("kissing"):
                    "You put your arm around [the_person.possessive_title] and lean in close."
                    $ the_person.call_dialogue("kissing_taboo_break")
                    $ the_person.break_taboo("kissing")
                    "You kiss her. She returns the kiss and presses her body against you."
                else:
                    "You put your arm around [the_person.possessive_title] and pull her close, leaning in to kiss her."
                    "She responds immediately, pressing her body against yours and kissing you back."
                call fuck_person(the_person, start_position = kissing, skip_intro = True) from _call_fuck_person_50

            "Just flirt.":
                $ the_person.draw_person()
                mc.name "Very tempting, but you're going to have to contain yourself for now."
                "[the_person.title] pouts melodramatically."
                the_person.char "You're so cruel. Maybe you can take me out to dinner to make up for it."
    return

label wild_cum_face(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 60:
            the_person.char "What do you think? Is this a good look [the_person.mc_title]?"
            "[the_person.title] licks her lips, cleaning up a few drops of your semen that had run down her face."
        else:
            the_person.char "I hope you had a good time [the_person.mc_title]. It certainly seems like you did."
            "[the_person.title] runs a finger along her cheek, wiping away some of your semen."
    else:
        if the_person.sluttiness > 80:
            the_person.char "Mmm that's such a good feeling. Do you think I look cute like this?."
            "[the_person.title] runs her tongue along her lips, then smiles and laughs."
        else:
            the_person.char "Whew, glad you got that over with. Take a good look while it lasts."
    return

label wild_cum_mouth(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 60:
            the_person.char "Mmm, thank you [the_person.mc_title]."
        else:
            "[the_person.title]'s face grimaces as she tastes your cum in her mouth."
            the_person.char "Ugh. There, all taken care of [the_person.mc_title]."
    else:
        if the_person.sluttiness > 80:
            the_person.char "Mmm, you taste great [the_person.mc_title]. Was it nice to watch me take your load in my mouth?"
        else:
            the_person.char "Ugh, that's such a... unique taste."
    return

label wild_cum_vagina(the_person):
    if mc.condom:
        if the_person.sluttiness > 75 or the_person.get_opinion_score("creampies") > 0:
            the_person.char "Oh god, it's so warm. If your condom broke it would all be inside me."
        else:
            the_person.char "Oh god, I hope you buy good condoms because that's a lot of cum."
            the_person.char "But then again, maybe you're dreaming of knocking me up."

    else:
        if the_person.sluttiness > 75 or the_person.get_opinion_score("creampies") > 0:
            if the_person.relationship != "Single":
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person.char "Fuck yes, pump that cum into me! I don't care if I get pregnant, I'll just tell my [so_title] that it's his!"

            else:
                the_person.char "Mmm, give me that baby batter, pump my pussy full of it! I'll worry about being pregnant later!"
        else:
            if the_person.relationship != "Single":
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person.char "Oh fuck. [the_person.mc_title], you can't cum inside me. My [so_title] would kill me if he found out I got pregnant."
                if the_person.kids > 0:
                    the_person.char "...Again."

            else:
                the_person.char "Oh fuck, [the_person.mc_title], you can't get me pregnant. Please, I don't want to do the whole \"single mother\" thing."
    return

label wild_cum_anal(the_person):
    if the_person.sluttiness > 75 or the_person.get_opinion_score("anal creampies") > 0:
        the_person.char "Mmm, pump my ass full of your hot cum!"
    else:
        the_person.char "Oh fuck, oh fuck!"
    return

label wild_suprised_exclaim(the_person):
    $rando = renpy.random.choice(["Fuck!","Shit!","Oh fuck!","Fuck me!","Ah! Oh fuck!", "Ah!", "Fucking tits!", "Holy shit!", "Fucking shit!", "God fucking dammit!", "Son of a bitch!", "Mother fucker!", "Whoah!"])
    the_person.char "[rando]"
    return

label wild_talk_busy(the_person):
    if the_person.obedience > 120:
        the_person.char "I've got a ton of things I need to get to, could we talk some other time [the_person.mc_title]?"
    else:
        the_person.char "Hey, I'd love to chat but I have a million things to get done right now. Maybe later?"
    return

label wild_sex_strip(the_person):
    if the_person.sluttiness < 20:
        if the_person.arousal < 50:
            the_person.char "One sec, I want to take something off."
        else:
            the_person.char "Ah, I'm wearing way too much right now. One sec!"

    elif the_person.sluttiness < 60:
        if the_person.arousal < 50:
            the_person.char "Why do I bother wearing all this?"
        else:
            the_person.char "Wait, I want to get a little more naked for you."

    else:
        if the_person.arousal < 50:
            the_person.char "Give me a second, I'm going to strip something off just. For. You."
        else:
            the_person.char "Ugh let me get this off. I want to feel your pressed against every inch!"
    return

label wild_sex_watch(the_person, the_sex_person, the_position):
    if the_person.sluttiness < the_position.slut_requirement - 20:
        $ the_person.draw_person(emotion = "angry")
        the_person.char "Ugh, jesus you two. Get a room or something, nobody wants to see this."
        $ the_person.change_obedience(-2)
        $ the_person.change_happiness(-1)
        "[the_person.title] looks away while you and [the_sex_person.name] [the_position.verb]."

    elif the_person.sluttiness < the_position.slut_requirement - 10:
        $ the_person.draw_person()
        the_person.char "Could you two at least keep it down? This is fucking ridiculous."
        $ the_person.change_happiness(-1)
        "[the_person.title] tries to avert her gaze and ignore you and [the_sex_person.name] [the_position.verb]."

    elif the_person.sluttiness < the_position.slut_requirement:
        $ the_person.draw_person()
        the_person.char "You're certainly feeling bold today [the_sex_person.name]. At least it looks like you're having a good time..."
        $ change_report = the_person.change_slut_temp(1)
        "[the_person.title] watches for a moment, then turns away while you and [the_sex_person.name] keep [the_position.verb]."

    elif the_person.sluttiness > the_position.slut_requirement and the_person.sluttiness < the_position.slut_cap:
        $ the_person.draw_person()
        the_person.char "Oh wow that's hot. You don't mind if I watch, do you?"
        $ change_report = the_person.change_slut_temp(2)
        "[the_person.title] watches you and [the_sex_person.name] [the_position.verb]."

    else:
        $ the_person.draw_person(emotion = "happy")
        the_person.char "Come on [the_person.mc_title], [the_sex_person.name] is going to fall asleep at this rate! You're going to have to give her a little more than that."
        "[the_person.title] watches eagerly while you and [the_sex_person.name] [the_position.verb]."
    return

label wild_being_watched(the_person, the_watcher, the_position):
    if the_person.sluttiness >= the_position.slut_cap and the_watcher.sluttiness >= the_position.slut_cap:
        #They agree you should give it to her harder
        the_person.char "Come on [the_person.mc_title], be rough with me. I can handle it!"
        $ the_person.change_arousal(1)
        "[the_person.title] seems turned on by [the_watcher.title] watching you and her [the_position.verb]."

    elif the_person.sluttiness >= the_position.slut_cap and the_watcher.sluttiness < the_position.slut_requirement:
        #She's super slutty and doesn't care what people think.
        the_person.char "I bet she just wishes she was the one being [the_position.verb]ed you."

    elif the_person.sluttiness >= the_position.slut_cap and the_watcher.sluttiness < the_position.slut_cap:
        #She's super slutty and encourages the watcher to be slutty.
        the_person.char "Oh god, you need to get a little of this yourself, [the_watcher.title]!"
        $ the_person.change_arousal(1)
        "[the_person.title] seems turned on by [the_watcher.title] watching you and her [the_position.verb]."

    elif the_person.sluttiness < the_position.slut_cap and the_watcher.sluttiness >= the_position.slut_cap:
        #She's into it and encouraged by the slut watching her.
        the_person.char "[the_watcher.title], I'm giving him all I can right now. Any more and he's going to break me!"
        $ the_person.change_arousal(1)
        "[the_person.title] seems turned on by [the_watcher.title] watching you and her [the_position.verb]."

    elif the_person.sluttiness < the_position.slut_cap and the_watcher.sluttiness < the_position.slut_requirement:
        #She's into it but shamed by the prude watching her.
        the_person.char "Fuck, maybe we should go somewhere a little quieter..."
        $ the_person.change_arousal(-1)
        $ the_person.change_slut_temp(-1)
        "[the_person.title] seems uncomfortable with [the_watcher.title] nearby."

    else: #the_person.sluttiness < the_position.slut_cap and the_watcher.sluttiness < the_position.slut_cap:
        #They're both into it but not fanatical about it.
        the_person.char "Ah, now this is a party! Maybe when he's done you can tap in and take a turn [the_watcher.title]!"
        $ the_person.change_arousal(1)
        $ the_person.change_slut_temp(1)
        "[the_person.title] seems more comfortable [the_position.verbing] you with [the_watcher.title] around."

    return

label wild_work_enter_greeting(the_person):
    if the_person.happiness < 80 or the_person.love < 0:
        "[the_person.title] glances at you when you enter the room. She scoffs and turns back to her work."

    elif the_person.happiness > 130:
        if the_person.sluttiness > 40:
            the_person.char "Hey [the_person.mc_title], down here for business or pleasure?"
            "The smile she gives you tells you which one she's hoping for."
        else:
            "[the_person.title] looks up from her work and smiles at you when you enter the room."
            the_person.char "Hey [the_person.mc_title], it's nice to have you stop by. Let me know if you need anything!"

    else:
        if the_person.sluttiness > 60:
            "[the_person.title] walks over to you when you come into the room."
            the_person.char "Just the person I was hoping would stop by. I'm here if you need anything."
            "She winks and slides a hand down your chest, stomach, and finally your crotch."
            the_person.char "Anything at all."
        else:
            the_person.char "Hey [the_person.mc_title]. Need anything?"
    return

label wild_date_seduction(the_person):
    if the_person.relationship == "Single":
        if the_person.sluttiness > the_person.love:
            if the_person.sluttiness > 40:
                the_person.char "I've had a blast [the_person.mc_title], but there are a few more things I'd like to do with you. Want to come back to my place and find out what they are?"
            else:
                the_person.char "You've been a blast [the_person.mc_title]. Want to come back to my place, have a few drinks, and see where things lead?"
        else:
            if the_person.love > 40:
                the_person.char "Tonight's been amazing [the_person.mc_title], I just don't want to say goodbye. Do you want to come back to my place and have a few drinks?"
            else:
                the_person.char "This might be crazy, but I had a great time tonight and you make me a little crazy. Do you want to come back to my place and see where things go?"
    else:
        $ so_title = SO_relationship_to_title(the_person.relationship)
        if the_person.sluttiness > the_person.love:
            if the_person.sluttiness > 40:
                the_person.char "I've had a blast [the_person.mc_title], but I'm not done with you yet. Want to come back to my place?"
                the_person.char "My [so_title] won't be home until morning, so we would have plenty of time."
            else:
                the_person.char "This might be crazy, but do you want to come back to have another drink with me?"
                the_person.char "My [so_title] is stuck at work and I don't want to be left all alone."
        else:
            if the_person.love > 40:
                the_person.char "You're making me feel crazy [the_person.mc_title]. Do you want to come have a drink at my place?"
                the_person.char "My [so_title] won't be home until morning, and we have a big bed you could help me warm up."
            else:
                the_person.char "This is crazy, but would you want to have one last drink at my place? My [so_title] won't be home until morning..."
    return

label wild_sex_end_early(the_person):
    if the_person.sluttiness > 50:
        if the_person.love > 40:
            if the_person.arousal > 60:
                the_person.char "You're really done? Fuck [the_person.mc_title], I'm still so horny..."
            else:
                the_person.char "That's all you wanted? I was prepared to do so much more to you..."
        else:
            if the_person.arousal > 60:
                the_person.char "Fuck, I'm so horny... you're sure you're finished?"
            else:
                the_person.char "That was a little bit of fun, I suppose."

    else:
        if the_person.love > 40:
            if the_person.arousal > 60:
                the_person.char "[the_person.mc_title], you got me so turned on..."
            else:
                the_person.char "I hope you had a good time."
        else:
            if the_person.arousal > 60:
                the_person.char "Oh god, that was intense..."
            else:
                the_person.char "Done? Good, nice and quick."
    return


label wild_sex_take_control (the_person):
    if the_person.arousal > 60:
        the_person.char "Oh hell no, you can't just get me wet and then walk away!"
    else:
        the_person.char "Are you getting bored already? Get back here, we aren't done yet!"
    return

label wild_sex_beg_finish(the_person):
    "Wait [the_person.mc_title], I'm going to cum soon and I just really need this... I'll do anything for you, just let me cum!"
    return

## Role Specific Section ##
label wild_improved_serum_unlock(the_person):
    mc.name "[the_person.title], now that you've had some time in the lab there's something I wanted to talk to you about."
    the_person.char "Okay, how can I help?"
    mc.name "All of our research and development up until this point has been based on the limited notes I have from my university days. I'm sure there's more we could learn, and I want you to look into it for me."
    "[the_person.title] smiles mischievously."
    the_person.char "Well, I've got an idea in mind. It's risky, but I think it could really push our research to a new level."
    mc.name "Go on, I'm interested."
    the_person.char "Our testing procedures focus on human safety, which I'll admit is important, but it doesn't leave us with much information about the subjective effects of our creations."
    the_person.char "What I want to do is take a dose of our serum myself, then have you record me while you run me through some questions."
    return

## Taboo break dialogue ##
label wild_kissing_taboo_break(the_person):
    if the_person.effective_sluttiness() >= 30:
        the_person.char "Come on then, we both know where this is going. You've always wanted to kiss me, right?"
    elif the_person.love >= 20:
        the_person.char "So we're doing this, huh?"
        mc.name "I guess we are. What do you think?"
        the_person.char "It's about time, I've wanted to make out with you for a long time."
    else:
        the_person.char "I don't know about this [the_person.mc_title], do you think we're taking this too fast?"
        mc.name "Are you scared?"
        the_person.char "No! Just... Nervous. Excited, maybe."
        mc.name "Then just trust me."
    return

label wild_touching_body_taboo_break(the_person):
    if the_person.effective_sluttiness() >= 30:
        the_person.char "Are you sure about this? I don't want you to chicken out on me..."
        mc.name "Oh, I'm sure."
        the_person.char "Good. Come on then!"
    elif the_person.love >= 20:
        the_person.char "So you're ready for this?"
        "You nod."
        the_person.char "Me too, I think. I didn't think I'd be so nervous when you actually made a move."
        mc.name "Just relax. You trust me, right."
        the_person.char "Of course."
    else:
        the_person.char "I think you're getting a little ahead of yourself here [the_person.mc_title]."
        mc.name "What do you mean?"
        the_person.char "I mean I don't just let anyone feel me up. Maybe we should cool things down."
        mc.name "You're not scared, are you?"
        the_person.char "Scared? Of course not!"
        mc.name "Well then just relax and go with it. It doesn't have to mean anything unless we want it to."
        "You see her answer in her eyes before she says anything."
        the_person.char "You'r so bad for me, you know that?"
        mc.name "Well let me make up for it then."
    return

label wild_touching_penis_taboo_break(the_person):
    if the_person.effective_sluttiness() >= 35:
        the_person.char "Mmm, you're really turned on too, right? Look how big you are."
        mc.name "Do you want to feel it?"
        the_person.char "I thought you'd never ask."

    elif the_person.love >= 20:
        the_person.char "Your cock looks so nice when it's hard. Can I touch it?"
        mc.name "Go ahead, it doesn't bite."
        the_person.char "If you're lucky it might choke me though."

    else:
        mc.name "My cock is so hard right now [the_person.title]. Put your hand on it and touch it for me."
        the_person.char "What? That's taking things a little far, don't you think?"
        mc.name "Come on, you know you want to. Just a few strokes, then if you aren't impressed you can stop."
    return

label wild_touching_vagina_taboo_break(the_person):
    if the_person.effective_sluttiness() >= 35:
        the_person.char "Don't chicken out now on me, you've got your chance to stroke my pussy now."
    elif the_person.love >= 20:
        the_person.char "Oh fuck, you've got my pussy tingling. I want you to touch it [the_person.mc_title]."
    else:
        the_person.char "I don't know if we should be doing this [the_person.mc_title]..."
        mc.name "Just take a deep breath and relax. I'm just going to touch you a little, and if you don't like it I'll stop."
        the_person.char "Just a little?"
        mc.name "Just a little. Trust me, it's going to feel amazing."
    return

label wild_sucking_cock_taboo_break(the_person):
    mc.name "I want you to do something for me."
    the_person.char "Oh yeah? What do you want me to do to you?"
    mc.name "I want you to suck on my cock."
    if the_person.effective_sluttiness() >= 45:
        the_person.char "Mmm, I think I'm up for that. It's not going to be too big for me, is it?"
        mc.name "I think you'll be able to handle it."
        the_person.char "Alright, I don't want it choking me."
        "She bites her lip and winks at you."
        the_person.char "That's a lie. A little choking is okay."
    elif the_person.love >= 30:
        the_person.char "I guess we've been dancing around it for a while."
        "She bites her lip and looks your body up and down."
        the_person.char "Alright, let's do this."
    else:
        the_person.char "Oh, I was wondering if this was going to come up..."
        "She laughs nervously and looks away from you."
        the_person.char "I don't know [the_person.mc_title]..."
        "You reach up and hold her chin, turning her head back to face you."
        mc.name "Don't overthink it. Just kneel down and suck on it for me. If you don't like doing it, we can just forget it happened."
        "You can see in her eyes the moment her resolve breaks. She bites her lip and nods."
        the_person.char "Alright, let's do this."
    return

label wild_licking_pussy_taboo_break(the_person):
    mc.name "I want to taste your pussy [the_person.title]. Are you ready?"
    if the_person.effective_sluttiness() >= 45:
        the_person.char "I was just about to ask you to try that. So yeah, I'm ready!"
    elif the_person.love >= 30:
        the_person.char "Oooh, finally a man who doesn't expect blowjobs all day but never licks a pussy."
        "She bites her lip and smiles at you."
        the_person.char "Alright then, get to it lover boy."
    else:
        if the_person.has_taboo("sucking_cock"):
            the_person.char "Really? I haven't even sucked your cock yet and you're ready to go down on me?"
            "She bites her lip and smiles."
            the_person.char "I could get use to this! Get to it!"

        else:
            the_person.char "It's about time you offered to repay the favour! Most guys think they're the only one who should get some head."
            "She bites her lip and smiles."
            the_person.char "Alright then, get to it!"
    return

label wild_vaginal_sex_taboo_break(the_person):
    if the_person.effective_sluttiness() >= 60:
        the_person.char "It's about time we did this. Come on then, get that cock inside me and fuck me!"
    elif the_person.love >= 45:
        the_person.char "Are you ready for this? I hope you're planning to rock my world."
        mc.name "That is the plan, I hope you can handle it."
        the_person.char "I can handle anything you can throw at me. Come on then, fuck me like you mean it!"
    else:
        if the_person.has_taboo("anal_sex"):
            the_person.char "Look at that cock... Fuck, I hope you don't stretch out my pussy too badly."

        else:
            the_person.char "If your cock feels half as big in my pussy as it did up my ass I'm in for a good time."
            the_person.char "Come on, fuck me [the_person.mc_title]!"
    return

label wild_anal_sex_taboo_break(the_person):
    if the_person.effective_sluttiness() >= 75:
        the_person.char "Oh god, it always suprises me how big your cock is! You're going to tear my ass in half with that monster!"
        "She seems more turned on by the idea than worried."
        mc.name "Don't worry, you'll be stretched out soon enough."

    elif the_person.love >= 60:
        the_person.char "So you really want to do this? It might be a little hard to fit all of your cock inside me..."
        mc.name "Don't worry about that, I'll have you stretched out soon enough."
        the_person.char "Fuck, just try and make sure you don't break me permanently!"
    else:
        if the_person.has_taboo("vaginal_sex"):
            the_person.char "Are you sure my pussy wouldn't be tight enough for you, I don't even know if I can fit your cock in my ass!"
            mc.name "I'll make it fit, but you might not be walking right for a few days."
            the_person.char "Oh fuck..."
        else:
            "She closes her eyes and talks quietly to herself."
            the_person.char "Whew, deep breathes [the_person.name]. You can do this..."
            mc.name "Are you okay?"
            the_person.char "Yeah, of course. I'm just... a little nervous. Fuck, I don't normally feel like this."
            "She laughs and shakes her head."
            the_person.char "Not that I normally do, you know, this. I don't know what's gotten into me."
            mc.name "Hopefully me, soon."
            the_person.char "No time like the present then. Do it, before I chicken out!"
    return

label wild_condomless_sex_taboo_break(the_person):
    if the_person.get_opinion_score("bareback sex") > 0:
        the_person.char "You want to fuck me raw? That's pretty hot."
        if the_person.get_opinion_score("creampies") > 0:
            the_person.char "It would be so easy for you to cum inside me though."
            the_person.char "So easy for you to pump my little cunt full of hot cum..."
            "She doesn't sound like she would mind very much at all."

        elif the_person.get_opinion_score("creampies") < 0:
            the_person.char "You better make sure you pull out though. I'd be pissed if you got me knocked up."
        else:
            the_person.char "You'll need to pull out so you don't knock me up then. Got it? Good."

    elif the_person.love > 60:
        the_person.char "I guess if I can't trust you I can't trust anyone. You make me make terrible decisions, you know that?"
        if the_person.get_opinion_score("creampies") > 0:
            the_person.char "Well fuck it, if we're doing this I want you to go the whole nine yards and fininh inside of me."
            mc.name "Are you on the pill?"
            "She shakes her head."
            the_person.char "Of course not. If we're fucking raw I want you to be trying to get me knocked up every single time."
        elif the_person.get_opinion_score("creampies") < 0:
            the_person.char "You'll need to pull out though. If you get me knocked up there's no way we're ever doing it unprotected again."
        else:
            if the_person.kids == 0:
                the_person.char "I need you to pull out though. I'm not quite ready to be a mother, even with you."
            elif the_person.kids == 1:
                the_person.char "I need you to pull out though. I've already got a kid, I don't need another one."
            else:
                the_person.char "I need you to pull out though. I've already got kids, I don't need another one."

    else:
        the_person.char "You really don't think we should use a condom? Aren't you worried about knocking me up?"
        the_person.char "Or is this your master plan to sneak a baby into me?"
        if the_person.has_taboo("vaginal_sex"):
            mc.name "I promise I'll pull out. Don't you want our first time together to be special?"
            "She rolls her eyes and sighs."
            the_person.char "God damn it, now you're getting me all sentimental. Fine, you don't need to put anything on."
            the_person.char "But you better fucking pull out, understand? Good."
        else:
            mc.name "I promise I'll pull out. It'll feel so much better without anything between us."
            the_person.char "Fuck, I know. I'm trying to make this decision with my head and not my clit."
            "She sighs dramatically."
            the_person.char "Fine, you don't need to put anything on. Just be fucking sure to pull out, understand? Good."
    return

label wild_underwear_nudity_taboo_break(the_person, the_clothing):
    if the_person.effective_sluttiness() > 30 - (the_person.get_opinion_score("skimpy outfits") * 5):
        the_person.char "You want to see me in my underwear, huh? It's about time you asked."
        if the_person.has_taboo(["bare_tits","bare_pussy"]):
            mc.name "What are we waiting for then, let's get this off of you."
        else:
            mc.name "About time? Are you forgetting I've seen you naked already?"
            "She shrugs."
            the_person.char "It's something called fashion, some men are into it. Come on, let's get this off."

    elif the_person.love > 15:
        the_person.char "You want me to strip me down a little? It's about time, I was wondering why you were taking things so slow."
        if the_person.has_taboo(["bare_tits","bare_pussy"]):
            mc.name "Well then let's stop wasting time and get your [the_clothing.display_name] off."

        else:
            mc.name "Slow? I've already seen you naked, remember?"
            the_person.char "I guess, but being in my underwear feels more romantic, you know?"
            mc.name "Well let's get more romantic then and get your [the_clothing.display_name] off."

    else:
        the_person.char "If you take my [the_clothing.display_name] I'll only have my underwear on, you know that?"
        if the_person.has_taboo(["bare_tits","bare_pussy"]):
            mc.name "Yeah, that's kind of the point."
            "She shakes her head and laughs to herself."
            the_person.char "Oh [the_person.title], what have you gotten yourself into! Come on, let's do this before I chicken out!"
        else:
            mc.name "Yeah, that's kind of the point. I've already seen you naked, so what are you worrying about?"
            the_person.char "Whatever, I guess you're right. Come on, let's get it off."
    return

label wild_bare_tits_taboo_break(the_person, the_clothing):
    if the_person.effective_sluttiness() > (40 - the_person.get_opinion_score("showing her tits") * 5):
        the_person.char "You finally want a look at my tits [the_person.mc_title], huh?"
        if the_person.has_large_tits():
            "She shakes her chest for you, jiggling the large tits hidden underneath her [the_clothing.display_name]."
        else:
            "She shakes her chest and gives her small tits a little jiggle."
        the_person.char "What took you so long to ask?"
        if the_person.has_large_tits():
            mc.name "No time like the present, right? Let's get those puppies out where I can enjoy them."
        else:
            mc.name "No time like the present, right? Let's get those cute little things out."

    elif the_person.love > 25:
        the_person.char "Ready to see my tits [the_person.mc_title]?"
        if the_person.has_large_tits():
            "She shakes her chest and jiggles her nice large tits, barely restrained by her [the_clothing.display_name]."
        else:
            "She shakes her chest, giving her small tits a little jiggle."
        mc.name "Oh yeah, I'm ready."
        the_person.char "Let 'em out then, and have fun."

    else:
        the_person.char "Wait a second! Jesus, you should at least ask a girl before you try and put her tits on full display."
        mc.name "Come on, don't you want to show them off? I bet they look great."
        the_person.char "Oh, they do. I just... Feel a little self concious about being naked around you, alright?"
        mc.name "There's no need to be, just relax and let me take your [the_clothing.display_name] off for you."
        the_person.char "Oh man, what are you getting me into [the_person.mc_title]? Fine, let's do it!"
    return

label wild_bare_pussy_taboo_break(the_person, the_clothing):
    if the_person.effective_sluttiness() > (50 - the_person.get_opinion_score("showing her ass") * 5):
        the_person.char "It's about time you got me out of my [the_clothing.display_name]!"

    elif the_person.love > 35:
        the_person.char "You want to get me out of my [the_clothing.display_name] and get a look at my pussy?"
        if the_person.has_taboo("touching_vagina"):
            mc.name "I know, that was the plan."
            the_person.char "Well... I guess we both knew where this was going. Okay, go for it."
        else:
            mc.name "I've already felt it up, I thought I should see it too."
            the_person.char "I think you're right. Go on then, I'm not going to stop you."

    else:
        the_person.char "Already trying to get me out of my [the_clothing.display_name], huh?"
        if the_person.has_taboo("touching_vagina"):
            mc.name "Yep, I am. Any problems with that?"
            the_person.char "Well... Maybe if you ask nicely."
            mc.name "[the_person.title], can I please take your [the_clothing.display_name] off and get a look at your pussy?"
            the_person.char "You're such a charmer. Of course you can."
        else:
            mc.name "Yep, I am. I've already felt your pussy up, I want to get a look at it now."
            the_person.char "Oh you're such a charmer. Alright then, what are you waiting for?"
    return

label wild_facial_cum_taboo_break(the_person):

    return

label wild_mouth_cum_taboo_break(the_person):

    return

label wild_body_cum_taboo_break(the_person):

    return

label wild_creampie_taboo_break(the_person):

    return

label wild_anal_creampie_taboo_break(the_person):

    return
