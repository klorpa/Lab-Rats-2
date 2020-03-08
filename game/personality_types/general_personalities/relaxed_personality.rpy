### PERSONALITY CHARACTERISTICS ###
init 1300:
    python:
        def relaxed_titles(the_person):
            if the_person.love < 0:
                return "Mrs." + the_person.last_name #If she doesn't like you she's much more formal.
            else:
                return the_person.name
        def relaxed_possessive_titles(the_person):
            return relaxed_titles(the_person) #If we don't have a special possessive just use their normal title.
        def relaxed_player_titles(the_person):
            return mc.name
        #Default personality is a well rounded personaity, without any strong tendencies. Default "Lily" personality.
        relaxed_personality = Personality("relaxed", #Lily style personality
        common_likes = ["skirts", "the weekend", "small talk", "the colour pink", "HR work", "supply work", "flirting","punk","pop"],
        common_sexy_likes = ["missionary style sex", "kissing", "masturbating", "being submissive", "drinking cum", "cum facials"],
        common_dislikes = ["Mondays", "pants", "the colour yellow", "research work", "work uniforms"],
        common_sexy_dislikes = ["taking control", "doggy style sex", "showing her tits", "showing her ass", "bareback sex", "creampies"],
        titles_function = relaxed_titles, possessive_titles_function = relaxed_possessive_titles, player_titles_function = relaxed_player_titles)

        list_of_personalities.append(relaxed_personality)

### DIALOGUE ###
label relaxed_introduction(the_person):
    mc.name "Excuse me, could I bother you for a moment?"
    "She turns around."
    $ the_person.set_title("???")
    the_person.char "I guess? What do you need?"
    mc.name "I know this is strange, but I saw you and I just needed to know your name."
    "She laughs and blushes."
    the_person.char "Really? You're just saying that to impress me, aren't you."
    mc.name "Really, I really just wanted to talk to you."
    $ title_choice = get_random_title(the_person)
    $ formatted_title = the_person.create_formatted_title(title_choice)
    the_person.char "Well fine, my name is [formatted_title]. It's nice to meet you..."
    $ the_person.set_title(title_choice)
    $ the_person.set_possessive_title(get_random_possessive_title(the_person))
    "She waits expectantly for you to introduce yourself."
    return

label relaxed_greetings(the_person):
    if the_person.love < 0:
        the_person.char "Ugh, what do you want?"
    elif the_person.happiness < 90:
        the_person.char "Hey..."
    else:
        if the_person.sluttiness > 60:
            if the_person.obedience > 130:
                the_person.char "Hello [the_person.mc_title], it's good to see you."
            else:
                the_person.char "Hey there handsome, feeling good?"
        else:
            if the_person.obedience > 130:
                the_person.char "Hello [the_person.mc_title]."
            else:
                the_person.char "Hey there!"
    return

label relaxed_sex_responses_foreplay(the_person):
    if the_person.arousal < 25:
        if the_person.sluttiness > 50:
            the_person.char "Mmm.... You're good at getting me warmed up..."
        else:
            the_person.char "Mmmm... Ah..."

    elif the_person.arousal < 50:
        if the_person.sluttiness > 50:
            the_person.char "Oh that's it. Mmm."
            "She purs warmly."
        else:
            the_person.char "Oh my god..."
            "It seems like she's trying not to moan too loudly."

    elif the_person.arousal < 75:
        if the_person.sluttiness > 50:
            if the_person.outfit.wearing_panties():
                the_person.char "Ah... If you get me any wetter I'm going to soak right through my panties."
            elif the_person.outfit.vagina_available():
                the_person.char "Good thing I'm not wearing any panties, you'd have me soaking right through them..."
            else:
                the_person.char "Oh god, if I get any wetter it's going to soak right through my clothes."
        else:
            the_person.char "I can't believe you're getting me this wet..."

    else:
        if the_person.sluttiness > 50:
            if the_person.relationship == "Single":
                the_person.char "Oh god, you might actually make me cum like this... Wow!"
            else:
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person.char "I wish my [so_title] knew how to touch me like this. You might actually make me cum!"
        else:
            the_person.char "Oh god... I think I might cum soon!"

    return

label relaxed_sex_responses_oral(the_person):
    if the_person.arousal < 25:
        if the_person.sluttiness > 50:
            the_person.char "Oh you know what I want [the_person.mc_title]... Ah..."
        else:
            the_person.char "Oh wow... that's... Mph!"

    elif the_person.arousal < 50:
        if the_person.sluttiness > 50:
            the_person.char "Mmmm, that's so good. Ah..."
        else:
            the_person.char "That... that feels so good [the_person.mc_title]... So fucking good."

    elif the_person.arousal < 75:
        if the_person.sluttiness > 50:
            the_person.char "God, your tongue feels so good!"

        else:
            "You're so good at that... Fuck, it's starting to drive me crazy!"
    else:
        if the_person.sluttiness > 50:
            if the_person.relationship == "Single":
                the_person.char "You're going to get me there [the_person.mc_title], you're going to get me to cum!"
            else:
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person.char "My [so_title] never does this for me any more... I feel horrible, but I need this so badly!"
        else:
            the_person.char "Oh no... Oh god, you're going to make me..."
            the_person.char "Cum!"

    return

label relaxed_sex_responses_vaginal(the_person):
    if the_person.arousal < 25:
        if the_person.sluttiness > 50:
            the_person.char "Mmm, your cock feels real good inside me."
        else:
            the_person.char "Oh my god... Ah..."

    elif the_person.arousal < 50:
        if the_person.sluttiness > 50:
            the_person.char "Keep fucking me [the_person.mc_title], it feels fantastic!"
        else:
            the_person.char "Oh my god, that feeling..."

    elif the_person.arousal < 75:
        if the_person.sluttiness > 50:
            "Ah, fuck me [the_person.mc_title]! Give me that big cock!"

        else:
            "[the_person.possessive_title] mumbles softly to herself."
            the_person.char "Fuck... Oh fuck... My pussy..."
    else:
        if the_person.sluttiness > 50:
            if the_person.relationship == "Single":
                the_person.char "Ah! Fuck me, make me cum!"
            else:
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person.char "Fuck me, fuck me harder! My [so_title] never fucks me like this, it feels so good!"
        else:
            the_person.char "Oh god, I think you're cock is going to make me cum soon!"

    return

label relaxed_sex_responses_anal(the_person):
    if the_person.arousal < 25:
        if the_person.sluttiness > 50:
            the_person.char "Oh fuck, you're really stretching me out!"
        else:
            the_person.char "Fuck, it feels so big... That's all of it, right? I can't take any more!"

    elif the_person.arousal < 50:
        if the_person.sluttiness > 50:
            the_person.char "Fuck my ass [the_person.mc_title], I can take it!"
        else:
            the_person.char "Oh fuck, my poor ass..."
            "Her groan is a mixture of pain and pleasure."

    elif the_person.arousal < 75:
        if the_person.sluttiness > 50:
            the_person.char "Oh my poor little ass, you're going to ruin me..."
            "She doesn't seem very upset with the idea."
        else:
            "[the_person.title] bites down on her lip and growls defiantly."
            the_person.char "Oh fuck... Fuck you're big!"
    else:
        if the_person.sluttiness > 50:
            if the_person.relationship == "Single":
                the_person.char "Oh god, keep going! Stuff my ass and make me cum!"
            else:
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person.char "I never let my [so_title] do this, you know? My tight ass is only for you!"
        else:
            the_person.char "I can't..."
            "She struggles to catch her breath."
            the_person.char "...I can't believe you might make me cum!"
    return


label relaxed_climax_responses_foreplay(the_person):
    if the_person.sluttiness > 50:
        the_person.char "Oh my god! I'm going to... I'm going to..."
        the_person.char "{b}Cum!{/b} Ah!"
    else:
        the_person.char "Mmmmhm!"
    return

label relaxed_climax_responses_oral(the_person):
    if the_person.sluttiness > 70:
        the_person.char "Oh fuck! Oh fuck, make me cum [the_person.mc_title]!"
        "She closes her eyes and squeals with pleasure."
    else:
        the_person.char "Oh my god, I'm going to cum. I'm going to cum!"
        "She closes her eyes and squeals with pleasure."
    return

label relaxed_climax_responses_vaginal(the_person):
    if the_person.sluttiness > 70:
        the_person.char "I'm going to cum! Ah! Fuck me [the_person.mc_title], I want to cum so badly! Ah!"
        "She closes her eyes and squeals with pleasure."
    else:
        the_person.char "Ah! I'm cumming! Oh fuck! Ah!"
    return

label relaxed_climax_responses_anal(the_person):
    if the_person.sluttiness > 80:
        the_person.char "I'm going to cum! Fuck my ass and make me cum!"
    else:
        the_person.char "Oh fuck, I think... I think I'm going to cum!"
    return

label relaxed_clothing_accept(the_person):
    if the_person.obedience > 130:
        the_person.char "It's for me? Thank you [the_person.mc_title], I'll add it to my wardrobe."
    else:
        the_person.char "Oh, it's cute! Thank's [the_person.mc_title]!"
    return

label relaxed_clothing_reject(the_person):
    if the_person.obedience > 130:
        the_person.char "Is that really for me [the_person.mc_title]? I want to... but I don't think I could wear that without getting in some sort of trouble."
    else:
        if the_person.sluttiness > 60:
            the_person.char "Wow. I'm usually up for anything but I think that's going too far."
        else:
            the_person.char "Wow. It's a little... skimpy. I don't think I could wear that."
    return

label relaxed_clothing_review(the_person):
    if the_person.obedience > 130:
        the_person.char "I'm sorry [the_person.mc_title], you shouldn't have to see me like this. I'll go and get cleaned up so I'm presentable again."
    else:
        if the_person.sluttiness > 40:
            the_person.char "Whew, I think we messed up my clothes a bit. Just give me a quick second to get dressed into something more decent."
        else:
            the_person.char "My clothes are a mess! I'll be back in a moment, I'm going to go get cleaned up."
    return

label relaxed_strip_reject(the_person):
    if the_person.obedience > 130:
        the_person.char "I'm sorry, but can we leave that where it is for now?"
    elif the_person.obedience < 70:
        the_person.char "Slow down there, I'll decide when that comes off."
    else:
        the_person.char "I think that should stay where it is for now."
    return

label relaxed_sex_accept(the_person):
    if the_person.sluttiness > 70:
        if the_person.obedience < 70:
            the_person.char "I was just about to suggest the same thing."
        else:
            the_person.char "Mmm, you have a dirty mind [the_person.mc_title], I like it."
    else:
        the_person.char "Okay, we can give that a try."
    return

label relaxed_sex_obedience_accept(the_person):
    if the_person.sluttiness > 70:
        the_person.char "Oh god [the_person.mc_title], I should really say no... But you always make me feel so good, I can't say no to you."
    else:
        if the_person.obedience > 130:
            the_person.char "Yes [the_person.mc_title], if that's what you want to do I'll give it a try."
        else:
            the_person.char "I... Okay, if you really want to, lets give it a try."
    return

label relaxed_sex_gentle_reject(the_person):
    if the_person.sluttiness > 50:
        the_person.char "Wait, I don't think I'm warmed up enough for this [the_person.mc_title]. How about we do something else first?"
    else:
        the_person.char "Wait. I don't think I'm comfortable with this. Could we just do something else instead?"
    return

label relaxed_sex_angry_reject(the_person):
    if not the_person.relationship == "Single":
        $ so_title = SO_relationship_to_title(the_person.relationship)
        the_person.char "Wait, what? I have a [so_title], what did you think we were going to be doing?"
        "She glares at you and walks away."
    elif the_person.sluttiness < 20:
        the_person.char "What the fuck! Do you think I'm just some whore who puts out for anyone who asks?"
        the_person.char "Ugh! Get away from me, I don't even want to talk to you after that."
    else:
        the_person.char "What the fuck do you think you're doing, that's disgusting!"
        the_person.char "Get the fuck away from me, I don't even want to talk to you after that!"
    return

label relaxed_seduction_response(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 50:
            the_person.char "Yes [the_person.mc_title]? Do you need help relieving some stress?"
        else:
            the_person.char "Yes [the_person.mc_title]? Is there something I can help you with?"
    else:
        if the_person.sluttiness > 50:
            the_person.char "Mmm, I know that look. Do you want to fool around a little?"
        elif the_person.sluttiness > 10:
            the_person.char "Oh, do you see something you like?"
        else:
            the_person.char "Oh, I don't really know what to say [the_person.mc_title]..."
    return

label relaxed_seduction_accept_crowded(the_person):
    if the_person.relationship == "Single":
        if the_person.sluttiness < 20:
            the_person.char "I suppose we could sneak away for a few minutes. There's nothing wrong with that, right?"
        elif the_person.sluttiness < 50:
            the_person.char "Come on, let's go find someplace quiet where we won't be interupted."
        else:
            the_person.char "No point waisting any time then, right? Let's get to it!"
    else:
        $ so_title = SO_relationship_to_title(the_person.relationship)
        if the_person.sluttiness + (5*the_person.get_opinion_score("cheating on men")) > 50:
            the_person.char "No point wasting any time, right? I hope my [so_title] won't be too jealous."
        else:
            the_person.char "I guess we could sneak away for a few minutes, but we have to make sure my [so_title] doesn't find out what we're doing."
    return

label relaxed_seduction_accept_alone(the_person):
    if the_person.relationship == "Single":
        if the_person.sluttiness < 20:
            the_person.char "Well, there's nobody around to stop us..."
        elif the_person.sluttiness < 50:
            the_person.char "Mmm, that's a fun idea. Come on, let's get to it!"
        else:
            the_person.char "Oh [the_person.mc_title], don't make me wait!"
    else:
        $ so_title = SO_relationship_to_title(the_person.relationship)
        if the_person.sluttiness + (5*the_person.get_opinion_score("cheating on men")) > 50:
            the_person.char "Don't make me wait then [the_person.mc_title]!"
        else:
            the_person.char "This is so dumb, I have a [so_title], I shouldn't be doing this..."
            "It's clear she wants to do it anyways."
    return

label relaxed_seduction_refuse(the_person):
    if the_person.sluttiness < 20:
        "[the_person.title] blushes and looks away from you awkwardly."
        the_person.char "I, uh... Sorry [the_person.mc_title], I just don't feel that way about you."

    elif the_person.sluttiness < 50:
        the_person.char "Oh, it's tempting, but I'm just not feeling like it right now. Maybe some other time?"
        "[the_person.title] smiles and gives you a wink."

    else:
        the_person.char "It's so, so tempting, but I don't really feel up to it right now [the_person.mc_title]. Hold onto that thought though."
    return

label relaxed_flirt_response(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 50:
            the_person.char "If that's what you want I'm sure I could help with that [the_person.mc_title]."
        else:
            the_person.char "Thank you for the compliment, [the_person.mc_title]."
    elif not the_person.relationship == "Single":
        $so_title = SO_relationship_to_title(the_person.relationship)
        if the_person.sluttiness + (the_person.get_opinion_score("cheating on men")*5) > 50:
            the_person.char "Well thank you [the_person.mc_title]. Don't let my [so_title] hear you say that though, he might get jealous."
            "She smiles and winks mischievously."
        else:
            the_person.char "I have a [so_title], you really shouldn't be talking to me like that..."
            "She seems more worried about being caught than flirting with you."
    else:
        if the_person.sluttiness > 50:
            the_person.char "Mmm, if that's what you want I'm sure I could find a chance to give you a quick peak."
            "[the_person.title] smiles at you and spins around, giving you a full look at her body."
        else:
            the_person.char "Hey, maybe if you buy me dinner first."
            "[the_person.title] gives you a wink and smiles."
    return

label relaxed_cum_face(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 60:
            the_person.char "Do I look cute covered in your cum, [the_person.mc_title]?"
            "[the_person.title] licks her lips, cleaning up a few drops of your semen that had run down her face."
        else:
            the_person.char "I hope this means I did a good job."
            "[the_person.title] runs a finger along her cheek, wiping away some of your semen."
    else:
        if the_person.sluttiness > 80:
            the_person.char "Ah... I love a nice, hot load on my face. Don't you think I look cute like this?"
        else:
            the_person.char "Fuck me, you really pumped it out, didn't you?"
            "[the_person.title] runs a finger along her cheek, wiping away some of your semen."
    return

label relaxed_cum_mouth(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 60:
            the_person.char "That was very nice [the_person.mc_title], thank you."
        else:
            "[the_person.title]'s face grimaces as she tastes your sperm in her mouth."
            the_person.char "Thank you [the_person.mc_title], I hope you had a good time."
    else:
        if the_person.sluttiness > 80:
            the_person.char "Your cum tastes great [the_person.mc_title], thanks for giving me so much of it."
            "[the_person.title] licks her lips and sighs happily."
        else:
            the_person.char "Bleh, I don't know if I'll ever get use to that."
    return

label relaxed_cum_vagina(the_person):
    if mc.condom:
        if the_person.sluttiness > 75 or the_person.get_opinion_score("creampies") > 0:
            the_person.char "Mmm, your cum feels so warm. I wish you weren't wearing a condom; I bet you would feel amazing raw."
        else:
            the_person.char "Whew... I can feel how warm your cum is through the condom. It feels nice."

    else:
        if the_person.sluttiness > 75 or the_person.get_opinion_score("creampies") > 0:
            if the_person.relationship != "Single":
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person.char "Your cum is so nice and warm..."
                the_person.char "If you get me pregnant I guess I'll have to tell my [so_title] it's his."
            else:
                the_person.char "Mmm, it's so warm... I wonder if it's going to get me pregnant."
        else:
            if the_person.relationship != "Single":
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person.char "Fuck. You need to pull out next time, okay? I have a [so_title], what if I got pregnant?"
            else:
                the_person.char "Fuck... You really shouldn't be cumming inside of me."
                "She closes her eyes and mutters to herself."
                the_person.char "What would I do if I got pregnant?"
    return

label relaxed_cum_anal(the_person):
    if the_person.sluttiness > 75 or the_person.get_opinion_score("anal creampies") > 0:
        the_person.char "Oh god yes, cum inside me!"
    else:
        the_person.char "Oh god, ah!"
    return

label relaxed_suprised_exclaim(the_person):
    $rando = renpy.random.choice(["Fuck!","Shit!","Oh fuck!","Fuck me!","Ah! Oh fuck!", "Ah!", "Fucking tits!", "Holy shit!", "Fucking shit!"])
    the_person.char "[rando]"
    return

label relaxed_talk_busy(the_person):
    if the_person.obedience > 120:
        the_person.char "Hey, I'm really sorry but I've got some stuff I need to take care of. Could we catch up some other time?"
    else:
        the_person.char "Hey, sorry [the_person.mc_title] but I've got some stuff to take care of. It was great talking though!"
    return

label relaxed_sex_strip(the_person):
    if the_person.sluttiness < 20:
        if the_person.arousal < 50:
            the_person.char "Let me get this out of the way..."
        else:
            the_person.char "Let me get this out of the way for you..."

    elif the_person.sluttiness < 60:
        if the_person.arousal < 50:
            the_person.char "This is just getting in the way..."
        else:
            the_person.char "Ah... I need to get this off."

    else:
        if the_person.arousal < 50:
            the_person.char "Let me get this worthless thing off..."
        else:
            the_person.char "Oh god, I need all of this off so badly!"

    return

label relaxed_sex_watch(the_person, the_sex_person, the_position):
    if the_person.sluttiness < the_position.slut_requirement - 20:
        $ the_person.draw_person(emotion = "angry")
        the_person.char "Holy shit, are you really doing this in front of everyone?"
        $ the_person.change_obedience(-2)
        $ the_person.change_happiness(-1)
        "[the_person.title] looks away while you and [the_sex_person.name] [the_position.verb]."

    elif the_person.sluttiness < the_position.slut_requirement - 10:
        $ the_person.draw_person()
        $ the_person.change_happiness(-1)
        "[the_person.title] tries to avert her gaze while you and [the_sex_person.name] [the_position.verb]."

    elif the_person.sluttiness < the_position.slut_requirement:
        $ the_person.draw_person()
        the_person.char "Oh my god, you two are just... Wow..."
        $ change_report = the_person.change_slut_temp(1)
        "[the_person.title] averts her gaze, but keeps glancing over while you and [the_sex_person.name] [the_position.verb]."

    elif the_person.sluttiness > the_position.slut_requirement and the_person.sluttiness < the_position.slut_cap:
        $ the_person.draw_person()
        the_person.char "Oh my god that's... Wow that looks...Hot."
        $ change_report = the_person.change_slut_temp(2)
        "[the_person.title] watches you and [the_sex_person.name] [the_position.verb]."

    else:
        $ the_person.draw_person(emotion = "happy")
        the_person.char "Come on [the_person.mc_title], you can give her a little more than that. I'm sure she can handle it."
        "[the_person.title] watches eagerly while you and [the_sex_person.name] [the_position.verb]."

    return

label relaxed_being_watched(the_person, the_watcher, the_position):
    if the_person.sluttiness >= the_position.slut_cap and the_watcher.sluttiness >= the_position.slut_cap:
        #They agree you should give it to her harder
        the_person.char "I can handle it [the_person.mc_title], you can be rough with me."
        $ the_person.change_arousal(1)
        "[the_person.title] seems turned on by [the_watcher.title] watching you and her [the_position.verb]."

    elif the_person.sluttiness >= the_position.slut_cap and the_watcher.sluttiness < the_position.slut_requirement:
        #She's super slutty and doesn't care what people think.
        the_person.char "Don't listen to [the_watcher.title], I'm having a great time. Look, she can't stop peeking over."

    elif the_person.sluttiness >= the_position.slut_cap and the_watcher.sluttiness < the_position.slut_cap:
        #She's super slutty and encourages the watcher to be slutty.
        $ the_person.change_arousal(1)
        "[the_person.title] seems turned on by [the_watcher.title] watching you and her [the_position.verb]."

    elif the_person.sluttiness < the_position.slut_cap and the_watcher.sluttiness >= the_position.slut_cap:
        #She's into it and encouraged by the slut watching her.
        the_person.char "Oh god, having you watch us like this..."
        $ the_person.change_arousal(1)
        "[the_person.title] seems turned on by [the_watcher.title] watching you and her [the_position.verb]."

    elif the_person.sluttiness < the_position.slut_cap and the_watcher.sluttiness < the_position.slut_requirement:
        #She's into it but shamed by the prude watching her.
        the_person.char "[the_person.mc_title], maybe we shouldn't be doing this here..."
        $ the_person.change_arousal(-1)
        $ the_person.change_slut_temp(-1)
        "[the_person.title] seems uncomfortable with [the_watcher.title] nearby."

    else: #the_person.sluttiness < the_position.slut_cap and the_watcher.sluttiness < the_position.slut_cap:
        #They're both into it but not fanatical about it.
        the_person.char "Oh my god, having you watch us do this feels so dirty. I think I like it!"
        $ the_person.change_arousal(1)
        $ the_person.change_slut_temp(1)
        "[the_person.title] seems more comfortable [the_position.verbing] you with [the_watcher.title] around."

    return

label relaxed_work_enter_greeting(the_person):
    if the_person.happiness < 80 or the_person.love < 0:
        if the_person.obedience > 120:
            "[the_person.title] gives you a curt nod and then turns back to what she was doing."
        else:
            "[the_person.title] glances at you when you enters the room then looks away quickly to avoid starting a conversation."

    elif the_person.happiness > 120:
        if the_person.sluttiness > 50:
            "[the_person.title] looks up from her work when you enter the room."
            the_person.char "Hey [the_person.mc_title]. Let me know if you need any help with anything. Anything at all."
            "She smiles and winks, then turns back to what she was doing."
        else:
            "[the_person.title] turns to you when you enter the room and shoots you a smile."
            the_person.char "Hey, good to see you!"

    else:
        if the_person.obedience < 90:
            "[the_person.title] glances up from her work."
            the_person.char "Hey, how's it going?"
        else:
            "[the_person.title] waves at you as you enter the room."
            the_person.char "Hey, let me know if you need anything [the_person.mc_title]."
    return

label relaxed_date_seduction(the_person):
    if the_person.relationship == "Single":
        if the_person.sluttiness > the_person.love:
            if the_person.sluttiness > 40:
                the_person.char "I had a great time [the_person.mc_title], but I can think of a few more things we could do together. Want to come back to my place?"
            else:
                the_person.char "I had a really good time tonight [the_person.mc_title]. I don't normally do this but... would you like to come back to my place?"
        else:
            if the_person.love > 40:
                the_person.char "You're such great company [the_person.mc_title]. Would you like to come back to my place and spend some more time together?"
            else:
                the_person.char "I had a great night [the_person.mc_title]. Would you like to come back to my place for a quick drink?"
    else:
        $ so_title = SO_relationship_to_title(the_person.relationship)
        if the_person.sluttiness > the_person.love:
            if the_person.sluttiness > 40:
                the_person.char "I had a great time [the_person.mc_title]. My [so_title] is suppose to be out for the rest of the night with his friends so..."
                the_person.char "Would you like to swing by my place tonight?"
            else:
                the_person.char "I had such a good time tonight [the_person.mc_title]. It's been years since I had this much fun with my [so_title]."
                the_person.char "He's out with some friends tonight. Would you like to come to my place and have a drink?"
        else:
            if the_person.love > 40:
                the_person.char "I don't want this night to end. My [so_title] is out with friends, do you want to come home with me so we can spend more time together?"
            else:
                the_person.char "Tonight was fantastic. I think my [so_title] is out for the night, so we could go back to my place for a quick drink. What do you say?"
    return

label relaxed_sex_end_early(the_person):
    if the_person.sluttiness > 50:
        if the_person.love > 40:
            if the_person.arousal > 60:
                the_person.char "Oh damn it [the_person.mc_title], I want more of you so badly!"
            else:
                the_person.char "Is that all you wanted to do? I was happy just being close to you."
        else:
            if the_person.arousal > 60:
                the_person.char "Is that really all? [the_person.mc_title], I was just getting started!"
            else:
                the_person.char "Aww, we were just getting started and you're already finished?"

    else:
        if the_person.love > 40:
            if the_person.arousal > 60:
                the_person.char "You don't want to take this any further? I thought we had a real connction."
            else:
                the_person.char "That's all? Well, maybe we can try again some other time."
        else:
            if the_person.arousal > 60:
                the_person.char "Oh my god... you've got me all out of breath..."
            else:
                the_person.char "That's all? Alright."
    return

label relaxed_sex_take_control(the_person):
    if the_person.arousal > 60:
        the_person.char "No no no, you can't just get worked up and then leave. We're finishing this, one way or another."
    else:
        the_person.char "Wait, we're just getting started! You just relax and leave this to me."
    return

label relaxed_sex_beg_finish(the_person):
    "No no no, please [the_person.mc_title] you can't stop now. I'll do whatever you want, please just let me cum!"
    return

## Role Specific Section ##
label relaxed_improved_serum_unlock(the_person):
    mc.name "[the_person.title], now that you've had some time in the lab there's something I wanted to talk to you about."
    the_person.char "Okay, how can I help?"
    mc.name "All of our research and development up until this point has been based on the limited notes I have from my university days. I'm sure there's more we could learn, and I want you to look into it for me."
    "[the_person.title] smiles mischievously."
    the_person.char "I've got an idea that you might want to hear then. It's not the most... orthodox testing procedure but I think it is nessesary if we want to see rapid results."
    mc.name "Go on, I'm interested."
    the_person.char "Our testing procedures focus on human safety, which I'll admit is important, but it doesn't leave us with much information about the subjective effects of our creations."
    the_person.char "What I want to do is take a dose of our serum myself, then have you record me while you run me through some questions."
    return

## Taboo break dialogue ##
label relaxed_kissing_taboo_break(the_person):
    if the_person.effective_sluttiness() >= 30:
        the_person.char "Don't be shy [the_person.mc_title], come on and kiss me."
    elif the_person.love >= 20:
        the_person.char "So... Do you want to kiss me?"
        mc.name "I do."
        the_person.char "Good, because I've really wanted to kiss you too."
    else:
        the_person.char "Hey there..."
        mc.name "Hey."
        the_person.char "Are you sure we should be doing this? I mean, I barely know you, when you think about it."
        mc.name "I'm sure. Just close your eyes and relax."
    return

label relaxed_touching_body_taboo_break(the_person):
    if the_person.effective_sluttiness() >= 30:
        the_person.char "Are you as excited as I am? I... I've always wanted to feel your hands on me."
    elif the_person.love >= 20:
        the_person.char "Do you think we're ready for this? I like you, but it seems like a big step..."
        mc.name "Tell me what you think?"
        "You can see the answer in her eyes before she says anything."
        the_person.char "I'm ready if you are."
    else:
        the_person.char "I don't know if I'm ready for this [the_person.mc_title]."
        the_person.char "It feel like we barely know each other, you know?"
        mc.name "This doesn't have to mean anything unless we want it to. Just relax and let your body tell you what's right."
    return

label relaxed_touching_penis_taboo_break(the_person):
    if the_person.effective_sluttiness() >= 35:
        the_person.char "Are you ready? I've wondered what your cock would feel like for a while."
        mc.name "Don't let me stop you then. Go for it."
    elif the_person.love >= 20:
        the_person.char "Your cock looks so big. I guess I shouldn't keep you waiting any longer then."
    else:
        the_person.char "Oh my god, look at how hard you've gotten. I didn't think it would be so big."
        mc.name "Go on, give it a touch."
        the_person.char "I... I don't know if I should."
        mc.name "Why not? It's right there, I certainly don't mind."
        the_person.char "Fine, but just for a second or two..."
    return

label relaxed_touching_vagina_taboo_break(the_person):
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

label relaxed_sucking_cock_taboo_break(the_person):
    mc.name "I want you to do something for me."
    the_person.char "Mhmm? What do you want me to do for you?"
    mc.name "I want you to suck on my cock."
    if the_person.effective_sluttiness() >= 45:
        the_person.char "Do you really want me to try? I'm up for it if you are."
        "You nod and she bites her lip in anticipation."
    elif the_person.love >= 30:
        the_person.char "I guess knew this was coming."
        mc.name "So..."
        "She rolls her eyes and sighs dramatically."
        the_person.char "Alright, I'll do it."
    else:
        the_person.char "Oh my god, do you really want me to do that?"
        "She laughs nerviously and shakes her head."
        the_person.char "You're crazy! I couldn't..."
        mc.name "Sure you could. Just kneel down and give it a taste."
        the_person.char "No, I mean what would people think?"
        mc.name "Who's going to know, and why do you care what people think?"
        mc.name "Just suck on it a little, and if you don't like doing it you can stop."
        "She shakes her head again, but you can see her resolve breaking the more she thinks about it."
        the_person.char "...Fine. I'll do it."
        mc.name "Do what?"
        "She smiles and laughs."
        the_person.char "You're the worst. I'll suck on your cock, [the_person.mc_title]. Happy?"
        mc.name "Not as happy as I'm about to be, that's for sure."
    return

label relaxed_licking_pussy_taboo_break(the_person):
    mc.name "I want to taste your pussy [the_person.title]. Are you ready?"
    if the_person.effective_sluttiness() >= 45:
        the_person.char "Oh, well that sounds like some fun. I'd be crazy to say no, right?"
        mc.name "Yeah, you would be."
        the_person.char "Well then, go to town!"
    elif the_person.love >= 30:
        the_person.char "I'm not sure if \"ready\" is the right word, but you can keep going."
        mc.name "Just relax and enjoy, you'll have a great time."
    else:
        if the_person.has_taboo("sucking_cock"):
            the_person.char "Whoa, really?"
            "She laughs nervously, but watch a wave of arousal sweep through her."
            the_person.char "Alright... You can eat me out if you really want to [the_person.mc_title]."

        else:
            the_person.char "I was wondering if you were going to repay the favour."
            the_person.char "Alright then, you go for it."
        mc.name "Just relax and enjoy."
    return

label relaxed_vaginal_sex_taboo_break(the_person):
    if the_person.effective_sluttiness() >= 60:
        the_person.char "Whew, here we go! I'm so excited!"
    elif the_person.love >= 45:
        "[the_person.title] nods eagerly."
        the_person.char "I'm ready [the_person.mc_title], I'm ready to feel you inside me."
    else:
        if the_person.has_taboo("anal_sex"):
            the_person.char "So this is it, huh?"
            mc.name "Looks like it. Are you ready?"
            the_person.char "No... But I don't want you to stop either."
        else:
            "[the_person.title] giggles."
            the_person.char "This feels so backwards! You've already been in my ass, but now we're doing it properly."
            "She shrugs."
            the_person.char "At lest this time it should be easier for you to fit inside."
    return

label relaxed_anal_sex_taboo_break(the_person):
    if the_person.effective_sluttiness() >= 75:
        "[the_person.title] takes a few deep breaths."
        the_person.char "Whew, I think I'm ready!"
        the_person.char "Fuck me in the ass [the_person.mc_title]! Stretch me out and ruin me!"

    elif the_person.love >= 60:
        the_person.char "I can't believe we're doing this... Do you think you'll even fit?"
        mc.name "I'll fit, but you might not be walking right for a few days."
        the_person.char "Haha, sure thing..."
        the_person.char "... You're kidding, right?"
        mc.name "Let's find out."
    else:
        if the_person.has_taboo("vaginal_sex"):
            the_person.char "Fuck, you must really like it tight. We've never even fucked and you're going right for my asshole!"
            the_person.char "Are you even sure it's going to fit?"
            mc.name "I'll make it fit, but you might not be walking right for a few days."
            the_person.char "Oh fuck..."
        else:
            the_person.char "Oh my god, you're actually going to do it! Fuck, I hope you even fit!"
            mc.name "Don't worry, I'll stetch out your ass like I've stretched out all your other holes."
    return

label relaxed_condomless_sex_taboo_break(the_person):
    if the_person.get_opinion_score("bareback sex") > 0:
        the_person.char "You want to do me raw? That's so hot."
        if the_person.get_opinion_score("creampies") > 0:
            the_person.char "It's probably smart for you to pull out when you cum though."
            mc.name "Do you feel smart today?"
            "She bites her lip and shakes her head."
            the_person.char "No, not particularly."
        elif the_person.get_opinion_score("creampies") < 0:
            the_person.char "You'll need to pull out though. The last thing in the world I want is to get knocked up."
        else:
            the_person.char "You'll need to pull out so you don't knock me up, got it?"

    elif the_person.love > 60:
        the_person.char "I want to feel close to you too [the_person.mc_title]."
        if the_person.get_opinion_score("creampies") > 0:
            the_person.char "If we're doing this, I don't want you to pull out when you finish either."
            mc.name "Are you on the pill?"
            "She shakes her head."
            the_person.char "No, but for you I'm okay with that risk."
        elif the_person.get_opinion_score("creampies") < 0:
            the_person.char "You'll need to pull out though. I don't want you to get me pregnant, okay?"
        else:
            if the_person.kids == 0:
                the_person.char "You'll need to pull out though. I don't think either of us want a kid yet, right?"
            else:
                the_person.char "You'll need to pull out though. I've spent enough time being a mother."

    else:
        the_person.char "You don't want to use protection? What if you get me pregnant though?"
        if the_person.has_taboo("vaginal_sex"):
            mc.name "I'll pull out. Don't you want our first time to be special?"
            the_person.char "I do... Fine, just please be careful where you cum."
        else:
            mc.name "I'll pull out. Don't you want to know how much better it feels without a condom on?"
            the_person.char "I do... Okay, you can go in raw. Please be careful where you cum though."
    return

label relaxed_underwear_nudity_taboo_break(the_person, the_clothing):
    if the_person.effective_sluttiness() > 30 - (the_person.get_opinion_score("skimpy outfits") * 5):
        the_person.char "You want to get a look at my underwear, huh?"
        if the_person.has_taboo(["bare_tits","bare_pussy"]):
            mc.name "I do. You've got good fashion sense, I bet you wear wear some cute underwear too."
            the_person.char "Well, let's get this off and you can check for yourself."
        else:
            mc.name "I do. I've already seen you naked, but I appreciate your fashion sense."
            the_person.char "Let's get this off then."

    elif the_person.love > 15:
        the_person.char "You want to see me in my underwear, huh? That's really cute."
        if the_person.has_taboo(["bare_tits","bare_pussy"]):
            mc.name "Damn right I do. Come on, let's get you out of this..."

        else:
            mc.name "I've already seen you naked, so what's there to hide? Let's get this off..."

    else:
        the_person.char "But I'll only be in my underwear if I take off my [the_clothing.display_name]."

        if the_person.has_taboo(["bare_tits","bare_pussy"]):
            mc.name "Yeah, that's kind of the point."
            the_person.char "I get that, but don't you think it's going a little far?"
            mc.name "What's so different between your underwear and your [the_clothing.display_name]? It's all just clothing."
            the_person.char "I guess... Okay, let's do this before I chicken out!"
        else:
            mc.name "Yeah, that's kind of the point. I've already seen you naked, what's special about your underwear?"
            the_person.char "I guess you're right. Okay, let's do it!"
    return

label relaxed_bare_tits_taboo_break(the_person, the_clothing):
    if the_person.effective_sluttiness() > (40 - the_person.get_opinion_score("showing her tits") * 5):
        the_person.char "So you want to see my tits, huh? I bet you're going to love them."
        if the_person.has_large_tits():
            "She shakes her chest for you, jiggling the large tits hidden underneath her [the_clothing.display_name]."
        else:
            "She shakes her chest and gives her small tits a little jiggle."
        mc.name "I bet I will, I just have to get your [the_clothing.display_name] out of the way."
        the_person.char "Go for it then, I'm not going to stop you."

    elif the_person.love > 25:
        the_person.char "So you want to see my boobs?"
        mc.name "Yeah, I do. Are you ready for that?"
        "She takes a long moment to respond, then nods."
        the_person.char "Yeah, I think I am. I didn't realise how nervous I was going to be though!"
        mc.name "Don't be nervous. Just relax and let me get rid of this [the_clothing.display_name] for you."

    else:
        the_person.char "Wait, wait, wait! I..."
        mc.name "What's wrong?"
        the_person.char "I'm... Not sure I'm ready to show you my boobs. I'm just feeling really nervous."
        if the_person.has_large_tits():
            mc.name "You don't have anything to be nervous about. Most girls would kill to have tits as big as yours, you should be proud to show them off."
        else:
            mc.name "You don't have anything to be nervous about. Most girls would kill to have tits as cute as yours."
        "She takes a deep breath and shakes out her shoulders, inadvertently jiggling her tits while she's at it."
        the_person.char "Okay, fuck it! Let's do it!"
    return

label relaxed_bare_pussy_taboo_break(the_person, the_clothing):
    if the_person.effective_sluttiness() > (50 - the_person.get_opinion_score("showing her ass") * 5):
        the_person.char "Ready to see my pussy? Well, what are you waiting for?"

    elif the_person.love > 35:
        the_person.char "If you take that off my pussy's going to be out, you know."
        if the_person.has_taboo("touching_vagina"):
            mc.name "I know, that was the plan."
            the_person.char "Well... I guess we both knew where this was going. Okay, go for it."
        else:
            mc.name "You've let me touch it already, so what's the big deal about taking a look?"
            the_person.char "Nothing, it's just... It feels like a big step, but I trust you."

    else:
        the_person.char "Wait! If you take that off you'll be able to see my pussy."
        if the_person.has_taboo("touching_vagina"):
            mc.name "That's the point, yeah. What's wrong?"
        else:
            mc.name "You've already let me feel it, so what's the issue?"

        the_person.char "I... I don't know, I'm just nervous!"
        mc.name "Just take a deep breath and relax. I'm going to get these [the_clothing.display_name] off of you."
    return

label relaxed_facial_cum_taboo_break(the_person):

    return

label relaxed_mouth_cum_taboo_break(the_person):

    return

label relaxed_body_cum_taboo_break(the_person):

    return

label relaxed_creampie_taboo_break(the_person):

    return

label relaxed_anal_creampie_taboo_break(the_person):

    return
