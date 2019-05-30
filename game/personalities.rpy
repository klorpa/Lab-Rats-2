init 1300:

    #These are the different personality specific responses/dialogue options called through the game. These must all be defined for core personalites.

    # @_greetings - short convo used when you start a convo with someome.
    # @_sex_responses - exclamation used while having sex, generally vaginal.
    # @_climax_responses - exclamation used when a girl climaxes.
    # @_clothing_accept - dialogue used when you add an outfit to a girls wardrobe and she accepts it.
    # @_clothing_reject - dialogue used when you offer an outfit to a girl but she refuses it because it's too slutty.
    # @_clothing_review - dialogue used after sex when a girl checks her outfit and realises she needs to get redressed.
    # @_strip_reject - dialogue used when you try and strip a piece of clothing off of a girl but she wants it in place.
    # @_sex_accept - dialogue when you offer a sex position to a girl and she agrees because she's slutty. (Not just when you seduce them, that's below!)
    # @_sex_obedience_accept - dialogue used when you offer a sex position to a girl but she only agrees because she's obedient
    # @_sex_gentle_reject - dialouge used when you try and offer a sex position to a girl but she refuse without being angry
    # @_sex_angry_reject - dialogue used when you try and offer a sex position to a girl with a psotiion she finds rediculously inappropriate.
    # @_seduction_response - dialogue used when you seduce a girl and she accepts
    # @_flirt_response - dialogue when you "chat with" and "flirt" with a girl.
    # @_cum_face - dialogue when you cum on a girls face.
    # @_cum_mouth - dialogue when you cum in a girls mouth
    # @_suprised_exclaim - List of random exclimations used when a character is suprised.
    # @_talk_busy - dialogue used when you've used "chat with" option too many times
    # @_improved_serum_unlock - dialogue used for the serum unlock head researcher event.
    # @_sex_strip - dialogue used when a girl strips for you (but she's not asking permission).
    # @_sex_watch - dialogue used when you're having sex in front of this girl.
    # @_being_watched - dialogue when you're having sex with the girl and being watched by another person
    # @_work_enter_greeting - dialogue used when you walk into a room at work with an employee in it.
    # @_date_seduction -



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
        common_likes = ["skirts", "the weekend", "small talk", "the colour pink", "HR work", "supply work", "flirting"],
        common_sexy_likes = ["missionary style sex", "kissing", "masturbating", "being submissive", "drinking cum", "cum facials"],
        common_dislikes = ["Mondays", "pants", "the colour yellow", "research work", "work uniforms"],
        common_sexy_dislikes = ["taking control", "doggy style sex", "showing her tits", "showing her ass", "risking getting pregnant", "creampies"],
        titles_function = relaxed_titles, possessive_titles_function = relaxed_possessive_titles, player_titles_function = relaxed_player_titles)

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
        common_likes = ["pants", "research work", "HR work", "Mondays", "working", "makeup", "the colour blue", "conservative outfits"],
        common_sexy_likes = ["missionary style sex", "kissing", "lingerie", "being submissive", "vaginal sex", "creampies"],
        common_dislikes = ["the colour red", "marketing work", "flirting"],
        common_sexy_dislikes = ["masturbating", "giving head", "getting head", "doggy style sex", "public sex", "not wearing underwear", "not wearing anything", "risking getting pregnant", "cum facials"],
        titles_function = reserved_titles, possessive_titles_function = reserved_possessive_titles, player_titles_function = reserved_player_titles)

        def wild_titles(the_person):
            return the_person.name
        def wild_possessive_titles(the_person):
            return wild_titles(the_person)
        def wild_player_titles(the_person):
            return mc.name
        wild_personality = Personality("wild", default_prefix = "wild", #Stephanie style personality
        common_likes = ["skirts", "small talk", "Fridays", "the weekend", "the colour red", "makeup", "flirting", "marketing work"],
        common_sexy_likes = ["doggy style sex", "giving blowjobs", "getting head", "anal sex", "public sex", "skimpy outfits", "showing her tits", "showing her ass", "taking control", "not wearing underwear", "creampies", "risking getting pregnant"],
        common_dislikes = ["Mondays", "the colour pink", "supply work", "conservative outfits", "work uniforms"],
        common_sexy_dislikes = ["being submissive", "being fingered", "missionary style sex", "giving handjobs"],
        titles_function = wild_titles, possessive_titles_function = wild_possessive_titles, player_titles_function = wild_player_titles)

        list_of_personalities = [relaxed_personality,reserved_personality,wild_personality]

        #SPECIAL PERSOANLITIES#
        def bimbo_titles(the_person):
            return the_person.name
        def bimbo_possessive_titles(the_person):
            return bimbo_titles(the_person)
        def bimbo_player_titles(the_person):
            return mc.name
        bimbo_personality = Personality("bimbo", #Currently used in the head researcher event line.
        common_likes = ["skirts", "small talk", "the colour pink", "makeup"],
        common_sexy_likes = ["giving blowjobs", "missionary style sex", "being submissive", "skipmy outfits", "showing her tits", "showing her ass", "not wearing anything", "not wearing underwear", "lingerie", "cum facials"],
        common_dislikes = ["working", "research work", "work uniforms", "conservative outfits", "Mondays"],
        common_sexy_dislikes = ["taking control", "masturbating"],
        titles_function = bimbo_titles, possessive_titles_function = bimbo_possessive_titles, player_titles_function = bimbo_player_titles)

        #UNIQUE PERSONALITIES#
        def stephanie_titles(the_person):
            valid_titles = [the_person.name]
            if the_person.love > 10:
                valid_titles.append("Steph")
            return valid_titles

        def stephanie_possessive_titles(the_person):
            return "Your friend"
        def stephanie_player_titles(the_person):
            return mc.name
        stephanie_personality = Personality("stephanie", default_prefix = "wild",
        common_likes = ["pants", "research work", "Fridays", "makeup", "the colour red"],
        common_sexy_likes = ["giving blowjobs", "drinking cum"],
        common_dislikes = ["Mondays", "HR work", "marketing work", "conservative outfits"],
        common_sexy_dislikes = ["anal sex", "being submissive"],
        titles_function = stephanie_titles, possessive_titles_function = stephanie_possessive_titles, player_titles_function = stephanie_player_titles)

        def lily_titles(the_person):
            valid_titles = [the_person.name]
            if the_person.love > 15:
                valid_titles.append("Sis")

            return valid_titles
        def lily_possessive_titles(the_person):
            valid_possessive_titles = ["Your sister",the_person.title]

            if the_person.sluttiness > 60:
                valid_possessive_titles.append("Your slut of a sister")

            if the_person.sluttiness > 100:
                valid_possessive_titles.append("Your cock hungry sister")
                valid_possessive_titles.append("The family cumdump")
            return valid_possessive_titles
        def lily_player_titles(the_person):
            return mc.name
        lily_personality = Personality("lily", default_prefix = "relaxed",
        common_likes = ["skirts", "small talk", "the colour pink", "makeup"],
        common_sexy_likes = ["lingerie", "masturbating", "being submissive", "doggy style sex"],
        common_dislikes = ["working", "conservative outfits", "research work", "production work"],
        common_sexy_dislikes = ["taking control", "anal sex", "creampies"],
        titles_function = lily_titles, possessive_titles_function = lily_possessive_titles, player_titles_function = lily_player_titles)

        def mom_titles(the_person):
            valid_titles = ["Mother"]
            if the_person.love > 10:
                valid_titles.append("Mom")
            return valid_titles

        def mom_possessive_titles(the_person):
            valid_possessive_titles = ["Your mother"]
            if the_person.love > 10:
                valid_possessive_titles.append("Your mom")

            if the_person.sluttiness > 60 and the_person.love > 60:
                valid_possessive_titles.append("Your personal MILF")

            if the_person.sluttiness > 100:
                valid_possessive_titles.append("Your cock hungry mom")
                valid_possessive_titles.append("The family cumdump")
            return valid_possessive_titles

        def mom_player_titles(the_person):
            valid_player_titles = [mc.name]
            if the_person.happiness < 70:
                valid_player_titles.append(mc.name + " " + mc.last_name)

            if the_person.love > 20:
                valid_player_titles.append("Sweetheart")
                valid_player_titles.append("Sweety")
            return valid_player_titles


        mom_personality = Personality("mom", default_prefix = "reserved",
        common_likes = ["pants", "conservative outfits", "work uniforms", "HR work", "makeup"],
        common_sexy_likes = ["taking control", "being submissive", "risking getting pregnant"],
        common_dislikes = ["production work", "sports"],
        common_sexy_dislikes = ["anal sex", "drinking cum", "sex standing up"],
        titles_function = mom_titles, possessive_titles_function = mom_possessive_titles, player_titles_function = mom_player_titles)


        def get_random_personality():
            return get_random_from_list(list_of_personalities)

###############################
##### Relaxed Personality #####
###############################
label relaxed_greetings(the_person):
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

label relaxed_sex_responses(the_person):
    if the_person.sluttiness > 50:
        if the_person.obedience > 130:
            the_person.char "Oh... Please keep doing that to me!"
        else:
            the_person.char "Fuck that feels nice... Keep doing that!"
    else:
        "[the_person.title] closes her eyes and moans quietly to herself."
    return

label relaxed_climax_responses(the_person):
    if the_person.sluttiness > 70:
        the_person.char "I'm going to cum! Ah! Make me cum [the_person.mc_title], I want to cum so badly! Ah!"
        "She closes her eyes and squeals with pleasure."
    else:
        the_person.char "Ah! I'm cumming! Oh fuck! Ah!"
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
    if the_person.sluttiness < 20:
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
    if the_person.sluttiness < 20:
        the_person.char "I suppose we could sneak away for a few minutes. There's nothing wrong with that, right?"
    elif the_person.sluttiness < 50:
        the_person.char "Come on, let's go find someplace quiet where we won't be interupted."
    else:
        the_person.char "No point waisting any time then, right? Let's get to it!"
    return

label relaxed_seduction_accept_alone(the_person):
    if the_person.sluttiness < 20:
        the_person.char "Well, there's nobody around to stop us..."
    elif the_person.sluttiness < 50:
        the_person.char "Mmm, that's a fun idea. Come on, let's get to it!"
    else:
        the_person.char "Oh [the_person.mc_title], don't make me wait!"
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
        "[the_person.title] seems more comfortable [the_position.verb]ing you with [the_watcher.title] around."

    return

label relaxed_work_enter_greeting(the_person):
    if the_person.happiness < 80:
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
    if the_person.sluttiness > the_person.love:
        if the_person.sluttiness > 40:
            the_person.char "I had a great time [the_person.mc_title], but I can think of a few more things we could do together. Want to come back to my place?"
            # the_person.char "I had a great night [the_person.mc_title], would you like to come back to my place and let me repay the favour?"
        else:
            the_person.char "I had a really good time tonight [the_person.mc_title]. I don't normally do this but... would you like to come back to my place?"
            #the_person.char "I had a great night [the_person.mc_title], but I don't see why it should end here. If you want to come back to my place I can think of a few things we could do."
    else:
        if the_person.love > 40:
            the_person.char "You're such great company [the_person.mc_title]. Would you like to come back to my place and spend some more time together?"
        else:
            the_person.char "I had a great night [the_person.mc_title]. Would you like to come back to my place for a quick drink?"
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


################################
##### Reserved Personality #####
################################
label reserved_greetings(the_person):
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

label reserved_sex_responses(the_person):
    if the_person.sluttiness > 50:
        if the_person.obedience > 130:
            the_person.char "Mmmf, please keep doing that [the_person.mc_title]!"
        else:
            the_person.char "Wow that feels... nice. Please don't stop."
    else:
        "[the_person.title] closes her eyes and moans quietly to herself."
    return

label reserved_climax_responses(the_person):
    if the_person.sluttiness > 70:
        the_person.char "You're going to... Ah! You're going to make me climax [the_person.mc_title]!"
        "She closes her eyes as she tenses up. She freezes for a long second, then lets out a long, slow breath."
    else:
        the_person.char "Oh, I think I'm about to... Oh yes!"
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
    if the_person.sluttiness < 20:
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
    if the_person.sluttiness < 20:
        the_person.char "I don't think anyone will miss us for a few minutes. We can... get closer and see where things go."
    elif the_person.sluttiness < 50:
        the_person.char "Come on, let's go find someplace quiet then."
    else:
        the_person.char "Well then, do you want to take me right here or should we get a room?"
    return

label reserved_seduction_accept_alone(the_person):
    if the_person.sluttiness < 20:
        the_person.char "How about we start with a little kissing and just see where it goes."
    elif the_person.sluttiness < 50:
        the_person.char "Oh [the_person.mc_title], you're going to make me blush! Come over here!"
    else:
        the_person.char "Mmm, that sounds so nice [the_person.mc_title]. Don't make me wait, get over here!"
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

label reserved_improved_serum_unlock(the_person):
    mc.name "[the_person.title], now that you've had some time in the lab there's something I wanted to talk to you about."
    the_person.char "Okay, how can I help?"
    mc.name "All of our research and development up until this point has been based on the limited notes I have from my university days. I'm sure there's more we could learn, and I want you to look into it for me."
    "[the_person.title] nods in agreement."
    the_person.char "I think I have an idea that could really help us along. All of our testing procedures focus on human safety, but what I really need to know about are the subjective effects of our creations."
    the_person.char "With your permission, I would like to take a dose of serum myself and have you record my experience with it."
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
        "[the_person.title] seems more comfortable [the_position.verb]ing you with [the_watcher.title] around."

    return

label reserved_work_enter_greeting(the_person):
    if the_person.happiness < 80:
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
    return


############################
##### Wild Personality #####
############################

label wild_greetings(the_person):
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

label wild_sex_responses(the_person):
    if the_person.sluttiness > 50:
        if the_person.obedience > 130:
            the_person.char "That's it, use me like your dirty little slut. I'll be your slut if that's what you want me to be [the_person.mc_title]!"
        else:
            the_person.char "Ah, don't you dare stop doing that! Ah!"
    else:
        "Mmm, that feels... Ugh, that feels really good."
    return

label wild_climax_responses(the_person):
    if the_person.sluttiness > 70:
        the_person.char "Ah! More! I'm going to... Ah! Cum! Fuck!"
        "She closes her eyes and squeals with pleasure."
    else:
        the_person.char "Oh god, I'm going to... Oh fuck me! Ah!"
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
    if the_person.sluttiness < 20:
        the_person.char "I'm sorry, what!? No, you've massively misread the situation, get the fuck away from me!"
        "[the_person.title] glares at you and steps back."
    else:
        the_person.char "What? That's fucking disgusting, I can't believe you'd even suggest that to me!"
        "[the_person.title] glars at you and steps back."
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
            the_person.char "[mc.nam], I know what you mean... Okay, I can spare a few minutes."
    return

label wild_seduction_accept_crowded(the_person):
    if the_person.sluttiness < 20:
        the_person.char "Alright, let's slip away for a few minutes and you can convince me a little more."
    elif the_person.sluttiness < 50:
        the_person.char "Come on, I know someplace nearby where we can get a few minutes privacy."
    else:
        the_person.char "Oh my god. I hope you aren't planning on making me wait [the_person.mc_title], because I don't know if I can!"
    return

label wild_seduction_accept_alone(the_person):
    if the_person.sluttiness < 20:
        the_person.char "Well, I think you deserve a chance to impress me."
    elif the_person.sluttiness < 50:
        the_person.char "Mmm, well let's get this party started and see where it goes."
    else:
        the_person.char "Fuck, I'm glad you're as horny as I am right now. Come on, I can't wait any more!"
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
    else:
        if the_person.sluttiness > 50:
            the_person.char "Then why don't you do something about it? Come on, all you have to do is ask."
            "[the_person.title] smiles at you and spins around, giving you a full look at her body."
        else:
            the_person.char "Well thank you, play your cards right and maybe you'll get to see a little bit more."
            the_person.char "You'll have to really impress me though, I have high standards."
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
        "[the_person.title] watches for a moment, then turns away  while you and [the_sex_person.name] keep [the_position.verb]."

    elif the_person.sluttiness > the_position.slut_requirement and the_person.sluttiness < the_position.slut_cap:
        $ the_person.draw_person()
        the_person.char "Oh wow that's hot. You don't mind if I watch, do you?"
        $ change_report = the_person.change_slut_temp(2)
        "[the_person.title] watches you and [the_sex_person.name] [the_position.verb]."

    else:
        $ the_person.draw_person(emotion = "happy")
        the_person.char "Come on [the_person.player_title], [the_sex_person.name] is going to fall asleep at this rate! You're going to have to give her a little more than that."
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
        "[the_person.title] seems more comfortable [the_position.verb]ing you with [the_watcher.title] around."

    return

label wild_work_enter_greeting(the_person):
    if the_person.happiness < 80:
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

label wild_date_seduction(the_person): #TODO: Change this to be different.
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

###############################
###### Bimbo Personality ######
###############################
label bimbo_greetings(the_person):
    if the_person.sluttiness > 60:
        if the_person.obedience > 130:
            the_person.char "Hey there [the_person.mc_title]. I mean sir! Hey there, sir!"
        else:
            the_person.char "Hey [the_person.mc_title], what are you doing here? Can I help with anything? Anything at all?"
    else:
        if the_person.obedience > 130:
            the_person.char "Hi there [the_person.mc_title], what can I do for you?"
        else:
            the_person.char "Hi there [the_person.mc_title]!"
    return

label bimbo_sex_responses(the_person):
    if the_person.sluttiness > 50:
        if the_person.obedience > 130:
            the_person.char "More of that, please. Keep doing that!"
        else:
            the_person.char "Ahhh, that's just what I need!"
    else:
        "[the_person.title] giggles softly."
        the_person.char "Hehe, this feels so dirty!"
    return

label bimbo_climax_responses(the_person):
    if the_person.sluttiness > 70:
        the_person.char "Oh god I'm going to cum! Ahh, make me cum [the_person.mc_title], it's all I want right now!"
        "She closes her eyes and squeals with pleasure."
    else:
        the_person.char "Yes, yes, yes! Make me cum! Make me cum hard!"
    return

label bimbo_clothing_accept(the_person):
    if the_person.obedience > 130:
        the_person.char "Oh that's cute! You have such a good sense of style [the_person.mc_title], this is just what I like to wear!"
    else:
        the_person.char "It's so cute! I love getting new clothes - you should see my closet at home, there's no such thing as too many shoes, right?"
    return

label bimbo_clothing_reject(the_person):
    if the_person.obedience > 130:
        the_person.char "Uh... I don't think I'm allowed to wear that. I really wish I could though, just for you!"
    else:
        if the_person.sluttiness > 60:
            the_person.char "That's not really an outfit, is it? I like something a little cuter - some heels, add a dash of pink, and a top to show off my tits!"
            "[the_person.title] looks the outfit over again for a momnt and shakes her head."
            the_person.char "Yeah, this just isn't going to do it. Thanks for the thought though!"
        else:
            the_person.char "Aww, I don't think I could ever wear something like that! I wish I could though, could you imagine the looks I would get? It would be. So. Hot."
    return

label bimbo_clothing_review(the_person):
    if the_person.obedience > 130:
        the_person.char "Hehe, you really made a mess of me. I should go get tidied up, I'm suppose to be a proper lady here!"
    else:
        if the_person.sluttiness > 40:
            "[the_person.title] looks down at herself and giggles."
            the_person.char "Hehe, I'm all messed up after that! I need to go sort this out, this outfit just doesn't work right now!"
        else:
            the_person.char "Oh darn, my outfit's all confuzzled! I'm going to go fix this up, I'll be back before you know it!"
    return

label bimbo_strip_reject(the_person):
    if the_person.obedience > 130:
        the_person.char "Don't you think I look cuter with it on? Leave it alone for now, okay?"
    elif the_person.obedience < 70:
        the_person.char "Oh no-no-no, I'm going to decide when that comes off. I want to see you work for it!"
    else:
        "[the_person.title] giggles and bats your hand away playfully."
        the_person.char "Not yet, there's so much fun stuff we have to do first!"
    return

label bimbo_sex_accept(the_person):
    if the_person.sluttiness > 70:
        if the_person.obedience < 70:
            the_person.char "Oh yeah, that's one of my favourite things to do! Come on, let's do it!"
        else:
            the_person.char "Yeah, let's do it! You're so cute when you're horny, did you know that?"
    else:
        the_person.char "Oh? Oh! Yeah, lets do that!"
    return

label bimbo_sex_obedience_accept(the_person):
    if the_person.sluttiness > 70:
        the_person.char "Wow that's a... does that even work? I thought... well I guess I should try it before I knock it!"
    else:
        if the_person.obedience > 130:
            the_person.char "If that's what you want, boss man, that's what you'll get!"
        else:
            the_person.char "You bring out the worst in me, you know that [the_person.mc_title]? I was a nice, respectable girl before you showed up!"
    return

label bimbo_sex_gentle_reject(the_person):
    if the_person.sluttiness > 50:
        the_person.char "No, no, no, not yet. I want you to make me wait for it a little bit, get me really begging for it."
    else:
        the_person.char "Uh, I don't think that sounds fun. Let's do something else. Come on, you pick!"
    return

label bimbo_sex_angry_reject(the_person):
    if the_person.sluttiness < 20:
        the_person.char "Uh, what the ACTUAL FUCK?! What do you think you're doing? Just saying that must be... illegal, or something!"
        "[the_person.title] glares at you you and walks away."
    else:
        the_person.char "Eew! No, no, no! I will NEVER do that with ANYONE! Eew!"
        "[the_person.title] shakes her head and stalkes away."
    return

label bimbo_seduction_response(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 50:
            the_person.char "Oh yay, I know how to deal with this! You just relax and I'll make you feel very, very good!"
        else:
            the_person.char "All I can think about is that cute little dress I saw this morning. Oh, that's not you meant, was it..."
            "[the_person.title] giggles."
            the_person.char "Nevermind, lead the way!"
    else:
        if the_person.sluttiness > 50:
            the_person.char "Yay! I was getting so horny that I was ready to jump you in the hall!"
        elif the_person.sluttiness > 10:
            the_person.char "Hehe, I thought you had the that look in your eye. I have a sixth sense, but it's for horny guys instead of ghosts!"
        else:
            the_person.char "Oh, I don't really know what to say [the_person.mc_title]..."
    return

label bimbo_flirt_response(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 50:
            the_person.char "Just make it an official order and it's all yours, boss man."
        else:
            the_person.char "Hehe, thank you, you're way too nice to me!"
    else:
        if the_person.sluttiness > 50:
            the_person.char "You should try your luck sometimes. Maybe take me out for a drink, I get wild after I've had a few. Wild-er, I guess."
        else:
            the_person.char "Oh you, stop it! You're going to make me blush!"
    return

label bimbo_cum_face(the_person):
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

label bimbo_cum_mouth(the_person):
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

label bimbo_suprised_exclaim(the_person):
    $rando = renpy.random.choice(["Fuck!","Shit!","Oh fuck!","Fuck me!","Ah! Oh fuck!", "Ah!", "Fucking tits!", "Holy shit!", "Fucking shit!"])
    the_person.char "[rando]"
    return

label bimbo_talk_busy(the_person):
    if the_person.obedience > 120:
        the_person.char "Hi, I'm like, really sorry but I have way more stuff than you can imagine that I have to get done right now. Could we catch up later?"
    else:
        the_person.char "Hey, I'm sorry but I'm just suuuper busy right now! Hit me up later though, I'd love to chat once I get all this stupid work done!"
    return

label bimbo_sex_strip(the_person):
    if the_person.sluttiness < 20:
        if the_person.arousal < 50:
            the_person.char "Oh wait, I know what you want to see more of..."
        else:
            the_person.char "Ugh, all this clothing is getting in the way!"

    elif the_person.sluttiness < 60:
        if the_person.arousal < 50:
            the_person.char "I spent so much time this morning picking out this outfit, but I think you'd enjoy it more if I took it off, right?"
        else:
            the_person.char "Ah... I need to get all of this silly stuff off of me!"

    else:
        if the_person.arousal < 50:
            the_person.char "Teehee, just wait a moment and I'll strip this off for you..."
        else:
            the_person.char "Oh my god, let me strip for you [the_person.mc_title], let me be your slutty stripper!"

    return

label bimbo_sex_watch(the_person, the_sex_person, the_position):
    if the_person.sluttiness < the_position.slut_requirement - 20:
        $ the_person.draw_person(emotion = "angry")
        the_person.char "Is that, like, allowed? I thought that was illegal or something. Ugh."
        $ the_person.change_obedience(-2)
        $ the_person.change_happiness(-1)
        "[the_person.title] looks away while you and [the_sex_person.name] [the_position.verb]."

    elif the_person.sluttiness < the_position.slut_requirement - 10:
        $ the_person.draw_person()
        the_person.char "Could you two get a room or something? There are some of us here who are trying to focus and you're being very distracting."
        $ the_person.change_happiness(-1)
        "[the_person.title] tries to avert her gaze while you and [the_sex_person.name] [the_position.verb]."

    elif the_person.sluttiness < the_position.slut_requirement:
        $ the_person.draw_person()
        the_person.char "Wow [the_sex_person.name] you're so adventurous, I don't think I could ever do that. But it looks, like, super fun!"
        $ change_report = the_person.change_slut_temp(1)
        "[the_person.title] averts her gaze, but keeps glancing over while you and [the_sex_person.name] [the_position.verb]."

    elif the_person.sluttiness > the_position.slut_requirement and the_person.sluttiness < the_position.slut_cap:
        $ the_person.draw_person()
        the_person.char "Oh. My. God. That is so fucking hot... Keep it up girl, you're doing great!"
        $ change_report = the_person.change_slut_temp(2)
        "[the_person.title] watches you and [the_sex_person.name] [the_position.verb]."

    else:
        $ the_person.draw_person(emotion = "happy")
        the_person.char "Mmm, come on [the_person.mc_title], you should do something more to her. I bet she wants it real bad. I know I do..."
        "[the_person.title] watches eagerly while you and [the_sex_person.name] [the_position.verb]."
    return

label bimbo_being_watched(the_person, the_watcher, the_position):
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
        "[the_person.title] seems more comfortable [the_position.verb]ing you with [the_watcher.title] around."

    return

label bimbo_work_enter_greeting(the_person):
    if the_person.happiness < 80:
        "[the_person.title] looks at you, pouts, then looks back at her work."

    elif the_person.happiness > 120:
        if the_person.sluttiness > 40:
            "[the_person.title] looks at you when you enter the room and smiles."
            the_person.char "[the_person.mc_title]! I'm so glad you're stopping by, I've been so bored without you."
            "She pouts at you, eyes running up and down your body shamelessly."
            the_person.char "I hope you're here for something fun!"
        else:
            "[the_person.title] looks up from her work when you come into the room and smiles."
            the_person.char "[the_person.mc_title]! It's so good to see you! I've been having, like, the best day!"

    else:
        if the_person.obedience < 100:
            the_person.char "Hi [the_person.mc_title]! Do you need anything, any way I can help you?"
        else:
            the_person.char "Hi [the_person.mc_title]! Duh, I mean sir! Hi sir!"
            "[the_person.title] sticks out her tongue, then smiles and turns back to her work."

    return

label bimbo_date_seduction(the_person): #TODO: Change this to be different.
    if the_person.sluttiness > the_person.love:
        if the_person.sluttiness > 40:
            the_person.char "So [the_person.mc_title], don't you think it's time you came back home with me and we had some real fun?"
            "[the_person.title] bites her lip and puffs out her chest just a little bit."

        else:
            the_person.char "[the_person.mc_title], I swear you're driving me crazy. Do you, like, want to come home with me and just get wild?"


    else:
        if the_person.love > 40:
            the_person.char "[the_person.mc_title], I don't know how you do it but I swear you've been driving me, like, totally crazy all night."
            "[the_person.title] runs her hand along your arm and giggles."
            the_person.char "I want you to come back to my place so I can have you all to my self."
        else:
            the_person.char "Oh my god [the_person.mc_title], tonight has been so much fun. Do you want to, like, come back home with me and drink some more?"
    return

## Role Specific Section ##
label bimbo_improved_serum_unlock(the_person):
    mc.name "[the_person.title], now that you've had some time in the lab there's something I wanted to talk to you about."
    the_person.char "Okay, how can I help?"
    mc.name "All of our research and development up until this point has been based on the limited notes I have from my university days. I'm sure there's more we could learn, and I want you to look into it for me."
    "[the_person.title] nods happily."
    "There's a long pause."
    mc.name "Do you know what to do?"
    the_person.char "Uh, duh! Look into the serum-stuff we make and make it better-er!"
    mc.name "Right, and do you have any idea how to actually do that?"
    "[the_person.title]'s eyebrows knit together as she tries to think."
    the_person.char "Uhm... not yet but... what if..."
    "You imagine you can see the little hamster in her head running as fast as it can."
    the_person.char "I've got it! What if you test it on me!"
    mc.name "Do you think that's a good idea!"
    the_person.char "Duh, that's why I thought of it! Come on, how bad could it be? Just let me try it! Record it or something and I'll tell you what it feels like!"
    return



############################
#### Unique - Stephanie ####
############################

label stephanie_greetings(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 60:
            the_person.char "Good to see you [the_person.mc_title], I hope you're here to see me about something fun."
        else:
            the_person.char "Good to see you [the_person.mc_title], how can I help?"
    else:
        if the_person.sluttiness > 60:
            the_person.char "Hey [the_person.mc_title], are you here for business or pleasure?"
            "[the_person.title] smiles playfully."
        else:
            "Hey [the_person.mc_title], what's up?"
    return

label stephanie_cum_face(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 60:
            the_person.char "Mmm, that feels nice. I bet it would feel even nicer in my mouth next time, [the_person.mc_title]."
        else:
            the_person.char "There we go, all taken care of. You can cum in my mouth next time if you want, it would make cleaning up a lot faster."
    else:
        if the_person.sluttiness > 80:
            the_person.char "Aww, you should shoot it into my mouth next time. I love how your hot cum tastes."
            "[the_person.title] runs a finger through a puddle of your cum and then licks it clean, winking at you while she does."
        else:
            the_person.char "Oh man, you really got me covered, didn't you. I wish you would just cum in my mouth so I don't have to worry about getting cleaned up."
    return

label stephanie_cum_mouth(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 60:
            the_person.char "Oh god, you taste so good. Thank you for the treat [the_person.mc_title]."
        else:
            the_person.char "Mmm, thank you [the_person.mc_title]."
    else:
        if the_person.sluttiness > 80:
            the_person.char "Mmm, your cum tastes so great [the_person.mc_title], are you sure there isn't any more of it for me?"
            "[the_person.title] licks her lips and sighs happily."
        else:
            "[the_person.title] licks her lips and smiles at you."
            the_person.char "Mmm, that was nice."
    return

label stephanie_improved_serum_unlock(the_person):
    mc.name "[the_person.title], now that you've had some time in the lab there's something I wanted to talk to you about."
    the_person.char "Okay, how can I help?"
    mc.name "All of our research and development up until this point has been based on the limited notes you and I have from our days at the lab. I wanted to ask if you think there's more we could be doing."
    "[the_person.title] smiles mischieviously."
    the_person.char "I've got an idea then, I'm sure it's something you'll like."
    mc.name "What's your plan?"
    the_person.char "All of the testing that I've been doing so far focuses on not getting people killed, which is important, but I really need to know more about what subjective effects there are."
    the_person.char "I want to take a dose of serum myself and have you record the effects. You can ask me a few questions, gauge how much it affects me."
    mc.name "Do you think that's a good idea?"
    the_person.char "Nora would never let me do it, but that's why I work for you now and not for her. Come on [the_person.mc_title], this is chance to do real, proper science!"
    return

label stephanie_sex_strip(the_person):
    if the_person.sluttiness < 20:
        if the_person.arousal < 50:
            the_person.char "Ugh I've started to dress like Nora. Let me take some of this off."
        else:
            the_person.char "Is it getting warm in here? I need to take something off."

    elif the_person.sluttiness < 60:
        if the_person.arousal < 50:
            the_person.char "You saw more of me back at the lab, I think I can lose a little more clothing, don't you?"
        else:
            the_person.char "One second, let me take some of this off for you. Feel free to watch."

    else:
        if the_person.arousal < 50:
            the_person.char "Ugh, fuck this stupid outfit. I hope you don't mind if I take it off."
        else:
            the_person.char "Wait, I need to take this off, I want to feel you against me."

    return


#######################
#### Unique - Lily ####
#######################

label lily_greetings(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 60:
            the_person.char "Hey [the_person.mc_title], do you need your little sister for something?"
            "[the_person.title] crosses her arms behind her back."
        else:
            the_person.char "Hi [the_person.mc_title]."
    else:
        if the_person.sluttiness > 60:
            the_person.char "Oh hey [the_person.mc_title], I was just thinking about you."
            "[the_person.title] smiles playfully."
        else:
            the_person.char "Hey, need something?"
    return

label lily_clothing_accept(the_person):
    if the_person.obedience > 140:
        the_person.char "You're right, that looks cute! I'm glad I've got a brother with good fashion sense!"
    else:
        the_person.char "You think this would look good on me? I'll keep that in mind!"
    return

label lily_clothing_reject(the_person):
    if the_person.obedience > 140:
        the_person.char "Oh, I wish I could wear this [the_person.mc_title], but I don't think I could ever explain it to Mom if she saw."
    else:
        if the_person.sluttiness > 60:
            the_person.char "Oh my god [the_person.mc_title]... It's hot, but there's no way I could ever actually wear it!"
        else:
            the_person.char "Oh my god [the_person.mc_title], you perv. There's no way I'm going to wear something like that!"
    return

label lily_clothing_review(the_person):
    if the_person.obedience > 130:
        the_person.char "Sorry [the_person.mc_title], I should really get myself dressed properly again! Just a second!"
    else:
        if the_person.sluttiness > 50:
            the_person.char "You shouldn't be looking at your sister like that [the_person.mc_title]. I'll get dressed so you won't be so distracted."
        else:
            the_person.char "Oh my god, I shouldn't be dressed like this around my own brother. Just... Just look away and give me a moment."
    return

label lily_strip_reject(the_person):
    if the_person.obedience > 130:
        the_person.char "I wish I could let you, but I don't think I should be taking that off in front of my brother."
    elif the_person.obedience < 70:
        the_person.char "Sorry [the_person.mc_title], your little sister likes being a tease. I want to leave that on for a bit."
    else:
        the_person.char "I couldn't take that off in front of you [the_person.mc_title]. You're my brother, I'd die of embarrassment!"
    return

label lily_sex_accept(the_person):
    if the_person.sluttiness > 70:
        if the_person.obedience < 100:
            the_person.char "You're definitely my brother, I was thinking the same thing."
        else:
            the_person.char "You want to do that with your little sister [the_person.mc_title]? Well, you're lucky I'm just as perverted."
    else:
        the_person.char "Okay, let's do it. Just make sure Mom never finds out, okay?"
    return

label lily_sex_obedience_accept(the_person):
    if the_person.sluttiness > 70:
        the_person.char "Oh god [the_person.mc_title], I know I shouldn't... We shouldn't be doing any of this together."
        the_person.char "But I just can't say no to you."
    else:
        if the_person.obedience > 130:
            the_person.char "If that's what my big brother needs me to do..."
        else:
            the_person.char "How do I keep letting you talk me into this? You're my brother for Gods sake..."
            "She seems conflicted for a second."
            the_person.char "Okay, just promise me Mom will never know."
    return

label lily_sex_gentle_reject(the_person):
    if the_person.sluttiness > 50:
        the_person.char "Not yet, I need to get warmed up first. Let's start out with something a little more tame."
    else:
        the_person.char "I... we can't do that [the_person.mc_title]. I'm your sister; there are lines we just shouldn't cross."
    return

label lily_sex_angry_reject(the_person):
    if the_person.sluttiness < 20:
        the_person.char "Oh my god, what? I'm your sister you fucking pervert, how could you even talk about that to me?"
        the_person.char "Even if you're joking that's just... it's just fucked up, okay?"
    else:
        the_person.char "What the fuck [the_person.mc_title], I'm your sister! How could you think that's okay?"
        the_person.char "I... Just get out of here. You're lucky I don't want to have to explain how this happened to Mom."
    return

label lily_seduction_response(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 50:
            the_person.char "What's up [the_person.mc_title]? Do you need your little sister to pay attention to you?"
        else:
            the_person.char "What're you thinking about? You look like you're up to something."
    else:
        if the_person.sluttiness > 50:
            the_person.char "Do you have something in mind for your innocent little sister?"
        elif the_person.sluttiness > 10:
            the_person.char "What do you mean [the_person.mc_title]? Do you want to do something together?"
        else:
            the_person.char "I... what do you mean [the_person.mc_title]?"
    return

label lily_seduction_accept_crowded(the_person):
    if the_person.sluttiness < 20:
        "[the_person.title] grabs your arm and blushes."
        the_person.char "Oh my god, you can't say things like that when there are other people around [the_person.mc_title]! let's at least find someplace quiet."

    elif the_person.sluttiness < 50:
        the_person.char "I... I mean, we shouldn't do anything like that when there are other people around. What would we do if people found out what we do together?"

    else:
        the_person.char "Oh god, that sounds so hot. I hope nobody here recognizes me"
    return

label lily_seduction_accept_alone(the_person):
    if the_person.sluttiness < 20:
        the_person.char "Let's just make sure nobody finds out, okay? I mean, what would my friends think if I was doing... stuff with my brother?"
    elif the_person.sluttiness < 50:
        the_person.char "I know we shouldn't, but there's nobody around to know, right? So what's the harm..."
    else:
        the_person.char "God, you're such a pervert [the_person.mc_title], taking advantage of your poor, innocent sister..."
        "[the_person.title] winks at you and holds onto your arm."
    return

label lily_seduction_refuse(the_person):
    if the_person.sluttiness < 20:
        the_person.char "Ugh, I'm your sister [the_person.mc_title], how could you even suggest that? Gross..."

    elif the_person.sluttiness < 50:
        the_person.char "No, wait, we really shouldn't be doing this [the_person.mc_title]... What if Mom knew, or my friends knew?"
        the_person.char "It would be so embarrassing if they found out what we do sometimes."

    else:
        the_person.char "I'm sorry [the_person.mc_title], but I just don't feel like fooling around today, okay? I'm sure I'll find a way to make it up to you later."
    return

label lily_flirt_response(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 50:
            the_person.char "I know you're my brother, but it's still really hot to hear you say that."
        else:
            the_person.char "Stop it [the_person.mc_title], you're my brother and I know you're just flattering me."
    else:
        if the_person.sluttiness > 50:
            the_person.char "Don't forget I'm your sister [the_person.mc_title], don't get too carried away. But I guess looking doesn't hurt, right?"
            "[the_person.title] smiles at you and spins around, giving you a full look at her body."
        else:
            the_person.char "Are you really checking me out? I'm your sister [the_person.mc_title], that's a little weird."
            the_person.char "But, uh... it's still nice to hear."
    return

label lily_cum_face(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 60:
            the_person.char "Oh wow, you really covered me. Do I look cute like this bro?"
        else:
            the_person.char "Oh my god, you got it all over me... You can never let Mom know about this, okay?"
    else:
        if the_person.sluttiness > 80:
            the_person.char "Mmm, it feels so warm. I know it's wrong but I love being covered in your cum."
        else:
            the_person.char "Oh my god... what are we doing [the_person.mc_title], we shouldn't be doing this..."
    return

label lily_cum_mouth(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 60:
            the_person.char "Wow, you really needed that... I guess that's why you need a sister like me."
        else:
            the_person.char "Oh my god... Mom can never know about this [the_person.mc_title]. She'd kill us both."
    else:
        if the_person.sluttiness > 80:
            the_person.char "Mmm, who knew my brother had such good tasting cum... If I had known I would have done this with you way earlier!"
        else:
            the_person.char "I... I can't believe we just did that. We really shouldn't do it again, okay?"
    return

label lily_sex_strip(the_person):
    if the_person.sluttiness < 20:
        if the_person.arousal < 50:
            the_person.char "I feel like Mom in this outfit. One second..."
        else:
            the_person.char "Oh god, I can't believe you're making me feel this way [the_person.mc_title]."

    elif the_person.sluttiness < 60:
        if the_person.arousal < 50:
            the_person.char "I'm just going to take this off. It's nothing you haven't seen before anyways..."
        else:
            the_person.char "I know it's wrong for me to feel this way about your brother..."
            "She pauses for a second, as if gathering her confidence."
            the_person.char "But I really want to get naked right now."

    else:
        if the_person.arousal < 50:
            the_person.char "I bet you want to see more of your little sister, right? God [the_person.mc_title], you're so bad."
        else:
            the_person.char "Oh my god, I can't keep this on any longer!"

    return

label lily_talk_busy(the_person):
    if the_person.obedience > 120:
        the_person.char "Hey, I'd love to catch up with my big brother but I've got some work to get done. Could we chat later?"
    else:
        the_person.char "Sorry [the_person.mc_title], but I've got a ton of school work to get done. We'll have to chat later."
    return

label lily_sex_watch(the_person, the_sex_person, the_position):
    if the_person.sluttiness < the_position.slut_requirement - 20:
        $ the_person.draw_person(emotion = "angry")
        the_person.char "Oh my god, [the_person.mc_title]! How can you do that in front of your sister?"
        $ the_person.change_obedience(-2)
        $ the_person.change_happiness(-1)
        "[the_person.title] looks away while you and [the_sex_person.name] [the_position.verb]."

    elif the_person.sluttiness < the_position.slut_requirement - 10:
        $ the_person.draw_person()
        $ the_person.change_happiness(-1)
        the_person.char "I... oh my god I can't believe you're my brother..."
        "[the_person.title] tries to avert her gaze while you and [the_sex_person.name] [the_position.verb]."

    elif the_person.sluttiness < the_position.slut_requirement:
        $ the_person.draw_person()
        the_person.char "Oh my god, you two are just... Wow..."
        $ change_report = the_person.change_slut_temp(1)
        "[the_person.possessive_title] averts her gaze, but she keeps stealing glances while you and [the_sex_person.name] [the_position.verb]."

    elif the_person.sluttiness > the_position.slut_requirement and the_person.sluttiness < the_position.slut_cap:
        $ the_person.draw_person()
        the_person.char "Oh my god, [the_person.mc_title], where did you learn to do that? I shouldn't be watching this, but..."
        $ change_report = the_person.change_slut_temp(2)
        "[the_person.title] watches you and [the_sex_person.name] [the_position.verb]."

    else:
        $ the_person.draw_person(emotion = "happy")
        the_person.char "Give it to her [the_person.mc_title], don't hold back just because I'm here."
        the_person.char "You're not nervious because your sister is watching, are you?"
        "[the_person.title] watches eagerly while you and [the_sex_person.name] [the_position.verb]."

    return

label lily_being_watched(the_person, the_watcher, the_position):
    if the_person.sluttiness >= the_position.slut_cap and the_watcher.sluttiness >= the_position.slut_cap:
        #They agree you should give it to her harder
        the_person.char "I can handle it [the_person.mc_title], you can play rough with your little sister."
        $ the_person.change_arousal(1)
        "[the_person.title] seems turned on by [the_watcher.title] watching you and her [the_position.verb]."

    elif the_person.sluttiness >= the_position.slut_cap and the_watcher.sluttiness < the_position.slut_requirement:
        #She's super slutty and doesn't care what people think.
        the_person.char "Don't listen to [the_watcher.title], I'm having a great time. She's just jealous her brother doesn't treat her like this!"

    elif the_person.sluttiness >= the_position.slut_cap and the_watcher.sluttiness < the_position.slut_cap:
        #She's super slutty and encourages the watcher to be slutty.
        $ the_person.change_arousal(1)
        the_person.char "We just love each other so much [the_watcher.title]. You understand, right?"
        "[the_person.title] seems turned on by [the_watcher.title] watching you and her [the_position.verb]."

    elif the_person.sluttiness < the_position.slut_cap and the_watcher.sluttiness >= the_position.slut_cap:
        #She's into it and encouraged by the slut watching her.
        the_person.char "Oh [the_person.mc_title], I know it's be wrong but being with you just feels so right!"
        $ the_person.change_arousal(1)
        "Your little sister seems turned on by [the_watcher.title] watching you and her [the_position.verb]."

    elif the_person.sluttiness < the_position.slut_cap and the_watcher.sluttiness < the_position.slut_requirement:
        #She's into it but shamed by the prude watching her.
        the_person.char "[the_person.mc_title], we shouldn't be doing this here. What if people talk?"
        $ the_person.change_arousal(-1)
        $ the_person.change_slut_temp(-1)
        "[the_person.title] seems uncomfortable with [the_watcher.title] nearby."

    else: #the_person.sluttiness < the_position.slut_cap and the_watcher.sluttiness < the_position.slut_cap:
        #They're both into it but not fanatical about it.
        the_person.char "[the_watcher.title], I'm so glad you don't think this is too weird."
        the_person.char "I know it's suppose to be wrong, but then why does it feel so good?"
        $ the_person.change_arousal(1)
        $ the_person.change_slut_temp(1)
        "[the_person.title] seems more comfortable [the_position.verb]ing you with [the_watcher.title] around."

    return

label lily_date_seduction(the_person):
    if the_person.sluttiness > the_person.love:
        if the_person.sluttiness > 40:
            the_person.char "Hey [the_person.mc_title], wait up a sec."
            "[the_person.title] stops you before you open the front door to the house."
            the_person.char "I've had a great night, do you want to come back to my room and have some more fun?"

        else:
            the_person.char "Hey [the_person.mc_title], wait up a sec."
            "[the_person.title] stops you before you open the front door to your house."
            the_person.char "I, uh... I had a really good night with you. I know it's a little weird, but do you want to come back to my room and just hang out?"

    else:
        if the_person.love > 40:
            "[the_person.title] stops you when you get in the door. She takes your hand in hers and looks into your eyes."
            the_person.char "I had a great night. It was so nice to be with you and just pretend that we weren't... that we could be together."
            "Her hand tightens around yours."
            the_person.char "Do you want to come back to my room and just pretend a little bit longer?"

        else:
            "[the_person.title] stops you when you get inside. She takes your hand, then looks away and blushes."
            the_person.char "I had a fun time [the_person.mc_title], thanks for taking me out."
            "She hesitates for a second before continuing."
            the_person.char "If you want to come back to my room and chat for a while I wouldn't say no."
    return


######################
#### Unique - Mom ####
######################


label mom_greetings(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 60:
            the_person.char "Hello sweetheart. Is there anything your mother can take care of for you?"
        else:
            the_person.char "Hello sweetheart. I hope everything is going well, if there's anything I can help with let me know."
    else:
        if the_person.sluttiness > 60:
            the_person.char "Hello [the_person.mc_title], how has your day been? I was... well, I was thinking about you, that's all."
        else:
            if time_of_day == 0 or time_of_day == 1:
                the_person.char "Good morning, sweetheart!"
            elif time_of_day == 1 or time_of_day == 2:
                the_person.char "Good afternoon, sweetheart!"
            else:
                the_person.char "Good evening, sweetheart!"
    return

label mom_clothing_accept(the_person):
    if the_person.obedience > 140:
        the_person.char "Well, if you think it'll look good on me then I'm not going to argue."
        the_person.char "Thank you for the wardrobe suggestions sweety."
    else:
        the_person.char "Oh that's a cute idea! I'll ask your sister about it later and see what she thinks."
    return

label mom_clothing_reject(the_person):
    if the_person.obedience > 140:
        the_person.char "I know it would make your day if I wore this for you sweetheart, but what if Lily saw me in this?"
        the_person.char "I'm sorry, I know you must be so disappointed in me."
    else:
        if the_person.sluttiness > 60:
            the_person.char "I... [the_person.mc_title], you don't think a women of my... experience could get away wearing this, do you?"
            "[the_person.possessive_title] laughs and shakes her head."
            the_person.char "No, risque stuff like this should be worn by people your sisters age!"
        else:
            the_person.char "[the_person.mc_title]! I'm your mother, I can't go walking around in something like that!"
            "[the_person.possessive_title] shakes her head and scoffs at the idea."
    return

label mom_clothing_review(the_person):
    if the_person.obedience > 130:
        the_person.char "I'm so sorry [the_person.mc_title], I'm really not looking ladylike right now. Just give me a moment to get dressed..."
    else:
        if the_person.sluttiness > 50:
            the_person.char "Oh [the_person.mc_title], you shouldn't be seeing your mother like this... Just give me a moment and I'll get dressed."
        else:
            the_person.char "Oh [the_person.mc_title], I'm not decent, am I? Turn around, I need to get myself covered!"
    return

label mom_strip_reject(the_person):
    if the_person.obedience > 130:
        the_person.char "I know it would make your day sweety, but I don't think I should take anything else off. I'm your mother, after all."
    elif the_person.obedience < 70:
        the_person.char "Not yet sweety. You just need to relax and let mommy take care of you."
    else:
        the_person.char "Don't touch that [the_person.mc_title]. Could you imagine if it came off? I'm your mother, there are lines we just shouldn't cross."
    return

label mom_sex_accept(the_person):
    if the_person.sluttiness > 70:
        if the_person.obedience < 100:
            the_person.char "This can't be wrong... not if I get so turned on by it, right?"
        else:
            the_person.char "Whatever you want me to do sweetheart. I just want to make sure you're happy."
    else:
        the_person.char "Okay, lets try it. I just hope this brings us closer together as mother and son."
    return

label mom_sex_obedience_accept(the_person):
    if the_person.sluttiness > 70:
        the_person.char "I know we shouldn't be doing this. I know I should say no..."
        the_person.char "But just a little more couldn't hurt, right?"
    else:
        if the_person.obedience > 130:
            the_person.char "I... We really shouldn't... But I know it would make you so happy. Okay sweetheart, let's try it"
        else:
            the_person.char "How does this keep happening sweety? You know I love you but we shouldn't be doing this..."
            "[the_person.possessive_title] looks away, conflicted."
            the_person.char "I... You just have to make sure your sister never knows about this. Nobody can know..."
    return

label mom_sex_gentle_reject(the_person):
    if the_person.sluttiness > 50:
        the_person.char "Not yet, I need to get warmed up first. Let's start out with something a little more tame."
    else:
        the_person.char "I... we can't do that [the_person.mc_title]. I'm your mother; there are lines we just shouldn't cross."
    return

label mom_sex_angry_reject(the_person):
    if the_person.sluttiness < 20:
        the_person.char "Oh god, what did you just say [the_person.mc_title]? I'm your mother, how could you even think about that!"
    else:
        the_person.char "What? Oh god, I... I'm your mother [the_person.mc_title]! We can't do things like that, ever."
        "[the_person.possessive_title] turns away from you."
        the_person.char "You should go. This was a mistake. I should have known it was a mistake. I don't know what came over me."
    return

label mom_seduction_response(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 50:
            the_person.char "Do you need some personal attention [the_person.mc_title]? I know how stressed you can get you."
        else:
            the_person.char "Oh well... What do you need help with [the_person.mc_title]?."
    else:
        if the_person.sluttiness > 50:
            the_person.char "Well, how about you let your mother help you get focused again?"
        elif the_person.sluttiness > 10:
            the_person.char "What do you mean [the_person.mc_title]? Do you want to spend some time together?"
        else:
            the_person.char "I'm not sure I understand. I'm your mother, after all."
    return

label mom_seduction_accept_crowded(the_person):
    if the_person.sluttiness < 20:
        "[the_person.title] bats at your shoulder and scoffs."
        the_person.char "You can't say things like that [the_person.mc_title]! Not when we're out in public."
        "She looks around quickly to see if anyone heard you, then takes your hand in hers."
        the_person.char "Come on, we can find someplace quiet to take care of you."

    elif the_person.sluttiness < 50:
        "[the_person.title] blushes and glances around nervously, making sure nobody around you is listening."
        the_person.char "Okay, but we need to be careful. I don't think people would understand the way we show our love. Let's find someplace quiet."

    else:
        the_person.char "Oh my, [the_person.mc_title]... I think we need to take care of you right away!"
    return

label mom_seduction_accept_alone(the_person):
    if the_person.sluttiness < 20:
        the_person.char "I can't believe I'm saying this... I'll play along, as long as you promise nobody will ever know."
        mc.name "Of course Mom, I promise."
    elif the_person.sluttiness < 50:
        the_person.char "Oh sweetheart, what kind of mother would I be if I said no? Come on, let's see what we can do."
    else:
        the_person.char "Oh sweetheart, I'm so glad I make you feel that way. Come on, let's get started!"
    return


label mom_seduction_refuse(the_person):
    if the_person.sluttiness < 20:
        the_person.char "Oh my god, what are you saying sweetheart! I'm your mother, we certainly couldn't do anything... physical!"

    elif the_person.sluttiness < 50:
        the_person.char "I'm sorry sweetheart, but we really shouldn't be doing anything together any more. It's just... not the way we're suppose to act."

    else:
        the_person.char "I'm sorry sweety, I know how much you like to spend time with me, but now isn't a good time for me. I'll make it up to you though, I promise."
    return

label mom_flirt_response(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 50:
            the_person.char "Oh sweetheart stop, you're making your mother think some... impure thoughts."
        else:
            the_person.char "Oh stop [the_person.mc_title], it's not nice to make fun of your mother like that."
            "[the_person.possessive_title] blushes and looks away."
    else:
        if the_person.sluttiness > 50:
            the_person.char "Oh jeez... I... I don't know what to say about that sweetheart. Thank you, I suppose."
            "[the_person.title] smiles at you and spins around, giving you a full look at her body."
            the_person.char "Thank you for paying attention to someone like me."
        else:
            the_person.char "I'm your mother [the_person.mc_title], you shouldn't be complementing me on things like that."
    return

label mom_cum_face(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 50:
            the_person.char "Ah... is this what you like to see [the_person.mc_title]? I hope you had a good time."
        else:
            the_person.char "Oh, it's everywhere! I... I just hope you had a good time sweetheart. I'm doing this all for you."
    else:
        if the_person.sluttiness > 70:
            the_person.char "Oh, you got it all over me. I hope that means you had a good time!"
        else:
            the_person.char "I... I don't know what to say about all this. It's so... wrong."
    return

label mom_cum_mouth(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 50:
            the_person.char "I guess that means I did a good job, right sweetheart?"
        else:
            the_person.char "I... Oh I'm not sure I'm going to be able to to get use to that. I'll try for you though sweetheart."
    else:
        if the_person.sluttiness > 70:
            the_person.char "Mmm, you taste great sweetheart. Thank you for giving your mom such a wonderful reward."
        else:
            the_person.char "Oh sweetheart... We really shouldn't have done that."
    return

label mom_sex_strip(the_person):
    if the_person.sluttiness < 20:
        if the_person.arousal < 50:
            the_person.char "I hope you don't mind if I slip this off..."
        else:
            the_person.char "I'm just going to take this off for you sweetheart..."

    elif the_person.sluttiness < 60:
        if the_person.arousal < 50:
            the_person.char "We're all family here, right? There's nothing about me you haven't seen before."
        else:
            the_person.char "Oh [the_person.mc_title], you make me feel so young again!"
            the_person.char "I shouldn't... I know I shouldn't, but I'm going to take some more off."

    else:
        if the_person.arousal < 50:
            the_person.char "You're all worked up, I bet you want to see some more of me."
        else:
            the_person.char "I just can't keep this on any longer! I want to feel you pressed up against me!"

    return

label mom_talk_busy(the_person):
    if the_person.obedience > 120:
        the_person.char "I'm really sorry sweetheart, but I've got some work to do right now. Could we chat later?"
        the_person.char "Maybe you can stop by for dinner and talk to me and your sister!"
    else:
        the_person.char "I'm sorry [the_person.mc_title], but I'm really busy right now. If it can wait we can talk about it later."
    return

label mom_sex_watch(the_person, the_sex_person, the_position):
    if the_person.sluttiness < the_position.slut_requirement - 20:
        $ the_person.draw_person(emotion = "angry")
        the_person.char "[the_person.mc_title]! I'm your mother, how can you be doing that in front of me!"
        $ the_person.change_obedience(-2)
        $ the_person.change_happiness(-1)
        "[the_person.title] looks away while you and [the_sex_person.name] [the_position.verb]."

    elif the_person.sluttiness < the_position.slut_requirement - 10:
        $ the_person.draw_person()
        $ the_person.change_happiness(-1)
        the_person.char "[the_person.mc_title]! Could you at least try and not do this in front of your mother?"
        "[the_person.title] tries to avert her gaze while you and [the_sex_person.name] [the_position.verb]."

    elif the_person.sluttiness < the_position.slut_requirement:
        $ the_person.draw_person()
        the_person.char "[the_person.mc_title], I'm... You really shouldn't be doing this here..."
        $ change_report = the_person.change_slut_temp(1)
        "[the_person.possessive_title] averts her gaze, but she keeps stealing glances while you and [the_sex_person.name] [the_position.verb]."

    elif the_person.sluttiness > the_position.slut_requirement and the_person.sluttiness < the_position.slut_cap:
        $ the_person.draw_person()
        the_person.char "Who taught you this [the_person.mc_title]? It certainly wasn't me..."
        $ change_report = the_person.change_slut_temp(2)
        "[the_person.title] watches you and [the_sex_person.name] [the_position.verb]."

    else:
        $ the_person.draw_person(emotion = "happy")
        the_person.char "Treat her the way she deserves [the_person.mc_title]. I think you could try something a little more exciting with her."
        "[the_person.title] watches eagerly while you and [the_sex_person.name] [the_position.verb]."

    return

label mom_being_watched(the_person, the_watcher, the_position):
    if the_person.sluttiness >= the_position.slut_cap and the_watcher.sluttiness >= the_position.slut_cap:
        #They agree you should give it to her harder
        the_person.char "I can handle it [the_person.mc_title], you can use me however you want."
        $ the_person.change_arousal(1)
        "[the_person.title] seems turned on by [the_watcher.title] watching you and her [the_position.verb]."

    elif the_person.sluttiness >= the_position.slut_cap and the_watcher.sluttiness < the_position.slut_requirement:
        #She's super slutty and doesn't care what people think.
        the_person.char "Don't listen to [the_watcher.title]. I'm just taking care of my son, any way he needs!"

    elif the_person.sluttiness >= the_position.slut_cap and the_watcher.sluttiness < the_position.slut_cap:
        #She's super slutty and encourages the watcher to be slutty.
        $ the_person.change_arousal(1)
        the_person.char "[the_person.mc_title], I love you so much. I hope [the_watcher.title] understands that."
        "[the_person.title] seems turned on by [the_watcher.title] watching you and her [the_position.verb]."

    elif the_person.sluttiness < the_position.slut_cap and the_watcher.sluttiness >= the_position.slut_cap:
        #She's into it and encouraged by the slut watching her.
        the_person.char "Oh [the_person.mc_title], I know it's be wrong but being with you just feels so right!"
        $ the_person.change_arousal(1)
        "[the_person.possessive_title] seems turned on by [the_watcher.title] watching you and her [the_position.verb]."

    elif the_person.sluttiness < the_position.slut_cap and the_watcher.sluttiness < the_position.slut_requirement:
        #She's into it but shamed by the prude watching her.
        the_person.char "[the_person.mc_title], we shouldn't be doing this. Not here. What if people recognize us? What if they talk?"
        $ the_person.change_arousal(-1)
        $ the_person.change_slut_temp(-1)
        "[the_person.title] seems uncomfortable with [the_watcher.title] nearby."

    else: #the_person.sluttiness < the_position.slut_cap and the_watcher.sluttiness < the_position.slut_cap:
        #They're both into it but not fanatical about it.
        the_person.char "[the_watcher.title], I'm glad you're so supportive."
        the_person.char "People say we shouldn't do this, but this is the closest I've ever felt to my son."
        $ the_person.change_arousal(1)
        $ the_person.change_slut_temp(1)
        "[the_person.title] seems more comfortable [the_position.verb]ing you with [the_watcher.title] around."

    return

label mom_date_seduction(the_person): #TODO: Change this to be different.
    if the_person.sluttiness > the_person.love:
        if the_person.sluttiness > 40:
            "When you get home your mother takes your hand and starts to lead you through the house."
            the_person.char "You've shown me such a good time tonight. Come with me and I think I can show you a few things too."
        else:
            "When you get home your mother takes your hand and holds it in hers."
            the_person.char "You were a perfect gentleman tonight sweety. I think you've earned this."
            "She leans forward and kisses you on the lips. She lingers there for a couple of seconds before pulling back and sighing."
            the_person.char "Would you... like to come to my room and share a quick drink before I get to bed? Maybe you could tuck me in too."
    else:
        if the_person.love > 40:
            the_person.char "Sweetheart..."
            "When you get home your mother takes your hand and holds it in both of hers."
            the_person.char "I had such a wonderful time tonight. You make me feel so young and alive."
            "She leans in and kisses you on the cheek. She lingers there for a second, her breath warm on our ear."
            the_person.char "Would you like to share a drink in my room before we head to bed? "
        else:
            the_person.char "Sweetheart..."
            "When you get home your mother gets your attention. She leans over and kisses you on the cheek."
            the_person.char "You've been a wonderful date. Would you like to share a drink with me before we head to bed?"
    return


#TODO: Go through and add unique stephanie versions for these events.
#TODO: Go through existing crises and events and add personality calls so we can get some different looking dialogue.
#TODO: Write some bimbo answers for the head researcher's new personality (and possibly as a personality you can give someone with a serum later.
#TODO: Add a screen to let you select a new Head Researcher.
#TODO: Add a tutorial!
#Idea for turorial: Add a crisis style mandatory event for each major thing we want the player to experience.
