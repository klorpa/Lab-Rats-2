### PERSONALITY CHARACTERISTICS ###
init 1300:
    python:
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
        common_sexy_likes = ["taking control", "being submissive", "bareback sex", "creampies"],
        common_dislikes = ["production work", "sports"],
        common_sexy_dislikes = ["anal sex", "drinking cum", "sex standing up"],
        titles_function = mom_titles, possessive_titles_function = mom_possessive_titles, player_titles_function = mom_player_titles)

### DIALOGUE ###
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
            the_person.char "I'm your mother [the_person.mc_title], you shouldn't be complimenting me on things like that."
    return

label mom_flirt_response_low(the_person):
    the_person.char "Aww, thank you [the_person.mc_title]. I'm really not wearing anything special though."
    mc.name "Well you're looking good, that's all I know."
    the_person.char "You're so sweet. Come here!"
    "[the_person.possessive_title] opens her arms up and gives you a warm, motherly hug."

    return

label mom_flirt_response_mid(the_person):
    if the_person.effective_sluttiness("underwear_nudity") < 20: #Not very slutty, so it must be high love.
        the_person.char "Oh [the_person.mc_title], you shouldn't be saying things like that about me."
        mc.name "Like what? That you're hot?"
        the_person.char "Yes, that. I appreciate the thought, but I'm still your mother."
        mc.name "That doesn't make me blind. I'm just telling you what I see [the_person.title], it's suppose to be a compliment."
        "She sighs and smiles."
        the_person.char "Well then thank you for the compliment. Come here."
        "[the_person.possessive_title] gives you a quick, motherly hug."
        the_person.char "You're always so good to me. I love you."
        mc.name "I love you too [the_person.title]."
    else:
        the_person.char "Oh, well thank you [the_person.mc_title]! That's nice to hear!"
        "She places a hand on her stomach and sighs."
        the_person.char "I don't have the same body I did when I was young though. I've put on a few pounds since then."
        mc.name "If you did you've put it in all the right places. Turn around for me."
        "[the_person.possessive_title] raises an eyebrow and hesitates, then shrugs and turns around for you."
        $ the_person.draw_person(position = "back_peek")
        the_person.char "Like this?"
        mc.name "Just like that. Look, have great hips and a fantastic ass. You should be showing them off more."
        $ the_person.draw_person()
        "[the_person.possessive_title] turns around and slaps you lightly on the shoulder, smiling and blushing."
        the_person.char "[the_person.mc_title]! Stop it, you're making me blush!"
    return

label mom_flirt_response_high(the_person):
    if mc.location.get_person_count() == 1: #If you are alone she'll flirt with you
        if the_person.effective_sluttiness() > (25 - the_person.get_opinion_score("incest")*5): # High sluttiness flirt
            the_person.char "Oh [the_person.mc_title], you know you shouldn't be saying things like that to me."
            the_person.char "You should be thinking about women your own age. Isn't there anyone else you think is pretty?"
            mc.name "You're the most beautiful woman I know [the_person.title]. No matter how much I try I can't get you out of my head."
            the_person.char "Aww... I suppose I can't be too angry at you then. Come here."
            "She opens her arms up and pulls you into a hug. After a quick squeeze she steps back to arms length and smiles, looking into your eyes."
            the_person.char "No matter what you're always going to be my amazing little boy."
            menu:
                "Kiss her.":
                    if the_person.has_taboo("kissing"):
                        $ the_person.call_dialogue("kissing_taboo_break")
                        "You lean in and kiss [the_person.possessive_title]. She does her best to kiss you back, but it's clear she's still adjusting."
                        $ the_person.break_taboo("kissing")
                    else:
                        "You lean in and kiss her. She seems startled for a second, then wraps her arms around you and returns the kiss."
                    call fuck_person(the_person, private = True, start_position = kissing, skip_intro = True) from _call_fuck_person_20

                "Just flirt.":
                    mc.name "And you'll always be my beautiful, loving mom."
                    "[the_person.possessive_title] smiles warmly and hugs you again. This time you let your hands slide down her back and rest them on her ass."
                    the_person.char "You shouldn't... Oh what's the harm. Go ahead, give it a squeeze."
                    "You grab [the_person.possessive_title]'s ass and massage it gently. She sighs softly into your ear as you play with her."
                    the_person.char "Okay... That's enough for now. I don't want you getting too excited."
                    mc.name "Okay [the_person.title]."
                    "You give her ass one last slap and leave it jiggling as you step back. She rolls her eyes."
                    the_person.char "Oh... Some days I don't know what I'm going to do with you."

        else: # Just high love flirt
            the_person.char "[the_person.mc_title], I'm your mother. That's not funny."
            mc.name "Oh come on [the_person.title], there's nobody else around. You don't have to be so uptight."
            the_person.char "It's not right though, you shouldn't be... looking at me like this."
            mc.name "You're an attractive woman and I'm a young man, it's just how my brain work. Just take it as a compliment."
            "She sighs and rolls her eyes."
            the_person.char "Okay, thank you. Just... Don't expect me to actually take anything off for you."

    else: #She shushes you and rushes you off somewhere private.
        if the_person.effective_sluttiness() > (25 - the_person.get_opinion_score("incest")*5): #She's slutty, but you need to find somewhere private so people don't find out.
            the_person.char "[the_person.mc_title], watch what you're saying! There are other people around."
            mc.name "It's fine [the_person.title], nobody else is listening."
            "She puts her hands on her hips and shakes her head severly."
            the_person.char "Do we need to go somewhere private to talk about your behaviour?"
            menu:
                "Find someplace quiet.":
                    mc.name "I think we should, we don't want to bother anyone else."
                    "[the_person.possessive_title] leads you away. When you're alone she turns back to you."
                    the_person.char "I don't mind you joking around like that, but if there are other people around you should be more... discrete."
                    mc.name "I know [the_person.title], but you're so beautiful I just get carried away."
                    "Her stern glare soften. She sighs and smilse."
                    the_person.char "I can't be angry, you're just feeling the same way every young man does. Come here."
                    "She pulls you into a hug and kisses you on the cheek. You put your hands around her and move them down her back."
                    if the_person.has_taboo("kissing"):
                        $ the_person.call_dialogue("kissing_taboo_break")
                        "You lean in and kiss [the_person.possessive_title]. She does her best to kiss you back, but it's clear she's still adjusting."
                        $ the_person.break_taboo("kissing")
                    else:
                        the_person.char "Hey... What are you doing? We shouldn't..."
                        "You slide your hands onto her ass and rub it gently."
                        mc.name "Come on, just for a few minutes. I'm so horny right now..."
                        "You rub [the_person.possessive_title]'s butt while she thinks. Finally she sighs reluctantly and nods."
                        the_person.char "Only because you really need it."
                        "You lean forward and kiss her passionately. It takes her a few seconds to warm up, but soon she is kissing you back with just as much enthusiasm."
                    call fuck_person(the_person, private = True, start_position = kissing, skip_intro = True) from _call_fuck_person_21

                "Just flirt.":
                    mc.name "Relax, I'm just joking around. What I mean is you're looking stunning today."
                    the_person.char "Thank you, that's a much more appropriate way of saying it."
                    "Her eyes soften and she sighs."
                    the_person.char "I'm sorry, I didn't mean to be so tough on you. If we're alone you can joke around like that, but when there are other people around..."
                    the_person.char "I just don't want anyone to misunderstand our... relationship."
                    mc.name "I understand [the_person.title]. I'll be more careful."

        else: #She's not slutty, so she's embarassed about what you're doing.
            "[the_person.possessive_title] gasps and covers her mouth."
            the_person.char "Oh my god, [the_person.mc_title]!"
            mc.name "Relax [the_person.tite], I'm just joking around."
            "She shakes her head sternly."
            the_person.char "Well I don't find it very funny when other people are around. It's embarrassing."
            mc.name "I'm sorry, I'll wait until we're alone next time."
            the_person.char "I'm not even sure if you should be making comments like that to me alone, but... It's fine."
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
            the_person.char "Mmm, you taste great sweetheart. Thank you for giving mommy such a wonderful reward."
        else:
            the_person.char "Oh sweetheart... We really shouldn't have done that."
    return

label mom_cum_vagina(the_person):
    if mc.condom:
        if the_person.effective_sluttiness() > 75 or the_person.get_opinion_score("creampies") > 0:
            the_person.char "Give me your cum sweetheart! I don't care if the condom works, I want to feel your seed in me!"
        else:
            the_person.char "Pump it out into that condom sweetheart, it's perfectly fine to cum in me as long as it's on!"
    elif the_person.sluttiness > 75 or the_person.get_opinion_score("creampies") > 0:
            the_person.char "Give mommy your cum, I want every last drop inside of me! Try and get mommy pregnant!"

    else:
        the_person.char "Oh sweety, you can't cum inside of me! You're so young and virile, it wouldn't take much to get mommy pregnant."

    return

label mom_cum_anal(the_person):
    if the_person.sluttiness > 75 or the_person.get_opinion_score("anal creampies") > 0:
        the_person.char "Cum inside of mommy's ass! I want you to give it all to me!"
    else:
        the_person.char "Oh lord, I hope I can take this!"
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
        "[the_person.title] seems more comfortable [the_position.verbing] you with [the_watcher.title] around."

    return

label mom_climax_responses_foreplay(the_person):
    if the_person.sluttiness > 50:
        the_person.char "Oh my..."
        "She pauses and moans passionately."
        the_person.char "You know just what to do to your mother feel alive. I'm going to cum!"
    else:
        the_person.char "I... I shouldn't be feeling like this... I shouldn't but you're going to..."
        "She hesitates before continuing, almost at a whisper."
        the_person.char "Make me cum."
    return

label mom_climax_responses_oral(the_person):
    if the_person.sluttiness > 70:
        the_person.char "Keep going [the_person.mc_title], make your mommy cum!"
        "[the_person.possessive_title] closes her eyes and moans passionately."
    else:
        the_person.char "This feeling... Oh... Oh this is so wrong!"
        "Her eyes close and she takes a slow, deep breath."
    return

label mom_climax_responses_vaginal(the_person):
    if the_person.sluttiness > 70:
        the_person.char "That's it, fuck me [the_person.mc_title]! Fuck me like you mean it, you're going to make your mommy cum!"
        "She closes her eyes as she tenses up. She freezes for a long second, then lets out a long, slow breath."
    else:
        the_person.char "Oh god, I shouldn't be... I shouldn't be feeling like this..."
        the_person.char "I'm going to cum sweetheart, you're about to make mommy cum! Ah!"
    return

label mom_climax_responses_anal(the_person):
    if the_person.sluttiness > 70:
        the_person.char "Fuck me [the_person.mc_title], fuck mommy in the ass with your big cock and make her cum!"
    else:
        the_person.char "Oh no, this isn't happening... I'm about to..."
        "She gasps and shivers with pleasure."
        the_person.char "Cum! Ah!"
    return

label mom_date_seduction(the_person):
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

label mom_sex_take_control (the_person):
    if the_person.arousal > 60:
        the_person.char "[the_person.mc_title], you just sit back and let me take care of you. Mommy's going to get what she needs from you..."
    else:
        the_person.char "Oh sweetheart, you can't get a women all worked up then just walk away. Here, let me take care of both of us."
    return

label mom_sex_beg_finish(the_person):
    "Wait [the_person.mc_title], you can't stop now, I'm so close! Please, please help your mother cum!"
    return

## Taboo break dialogue ##
label mom_kissing_taboo_break(the_person):
    the_person.char "[the_person.mc_title], what are you doing?"
    mc.name "I want to kiss you."
    the_person.char "Oh, well..."
    "She turns her cheek to you."
    the_person.char "It's so sweet of you to..."
    "You press a finger to her chin and turn her back to you."
    mc.name "I mean really kiss you, [the_person.title]."
    the_person.char "Oh, I see..."
    the_person.char "I'm sorry if I've been confusing, but we really can't do that..."
    mc.name "You're the most important woman in the world to me. Other people never need to know, I just really want to feel close to you."
    "Her eyes melt."
    the_person.char "Oh sweetheart! I want to be close to you too! You know you'll always be my special man, right?"
    the_person.char "Okay, we can kiss just a little bit if that's how you want to show your love. I understand how you feel."
    the_person.char "And um... Let's just not tell anyone else about this, okay? There's nothing wrong with it, but other people might get the wrong idea."
    mc.name "Of course [the_person.title]."
    return

label mom_touching_body_taboo_break(the_person):
    "[the_person.mc_title], what are you doing? You shouldn't be touching me like this!"
    if the_person.love > 20: # Love varient
        mc.name "Why not? You love me, don't you?"
        the_person.char "Of course I love you, but I'm still your mother!"
        mc.name "Please [the_person.title]? I feel so lonely sometimes, and I feel loved when I'm close to you."
        the_person.char "Oh [the_person.mc_title]... It's still not right though..."
        mc.name "I know, but nobody else needs to know, right? We can keep this all a secret."
        "You feel the last bit of resistance leave her body."
        the_person.char "I guess you're just very... affectionate. I can't be angry about that."
        mc.name "Thank you [the_person.mc_title], you're the best."
        the_person.char "It's just part of the way we bond as a mother and son. Yes, that's it..."
        "She seems to be trying to convince herself more than you."


    else: # High slut varient
        mc.name "Why not? Don't you like it?"
        the_person.char "That's... That's not the point! I'm your mother! I'm twice your age!"
        mc.name "So? I think older women are hot."
        the_person.char "That wasn't the important part! My son shouldn't be feeling me up..."
        mc.name "Well you didn't answer me: do you like it?"
        the_person.char "I..."
        mc.name "It's okay if you do. I don't mind telling you I like touching you."
        "You watch her struggle with herself for a moment before she answers."
        the_person.char "I... Like how it feels. It's been a long time since someone touched me like this."
        mc.name "There you go. We both like it, we're both adults. Nobody else ever needs to know."
        "You feel the last bit of resistance leave her body."
        the_person.char "Maybe you're right. Nobody else is going to find out?"
        mc.name "Do you plan on telling someone?"
        the_person.char "Of course not! Do you know what people would say if they knew my own son was... touching me?"
        mc.name "Well I won't tell anyone either. This is just part of our mother-son bonding."
    return

label mom_touching_penis_taboo_break(the_person):
    # She's in control here.
    if the_person.love > 30: # Love varient
        the_person.char "Oh my god, what am I doing!"
        "She looks away from you, on the brink of walking away entirely."
        mc.name "[the_person.title], it's okay. I'm your son and you love me, right?"
        "She turns back and nods."
        the_person.char "Of course I do. I love you more than I could ever tell you."
        mc.name "And I love you too. There's nothing wrong about a mother who wants to make sure her son is taken care of."
        "She looks at your hard cock and stares at it for a moment."
        the_person.char "You don't think this is wrong? I'm your mother... I shouldn't be touching you like this."
        mc.name "I don't think it's anyones business but our own how we show our love for each other."
        "She thinks for a long moment, eyes still locked on your dick."
        the_person.char "Okay, but only because I love you [the_person.mc_title]."
        "[the_person.possessive_title] looks you in the eyes again and laughs self-conciously."
        the_person.char "I guess it's fine to tell you then that your... Penis is very impressive. You should be very proud."

    else: #High Slut version
        the_person.char "Oh my god... Look how big you are. The ladies must be very impressed."
        mc.name "You can touch it, if you want."
        the_person.char "I... No, you're my son! That would be crossing a line. I can't be stroking off my son."
        mc.name "I didn't say you should stroke me off, that's your idea. I'm just saying you can touch it if you're curious how it feels."
        the_person.char "I'll admit I'm a little curious. My big man has grown up in so many different ways."
        mc.name "Touch it then [the_person.title], I promise you I won't mind."
        mc.name "It's just another way we can come closer together as mother and son, right?"
        the_person.char "Yes, right."
    return

label mom_touching_vagina_taboo_break(the_person):
    the_person.char "Wait! You can't touch mommy there [the_person.mc_title]."
    if the_person.love > 30:
        mc.name "Why not? You trust me, don't you?"
        the_person.char "I would trust you with my life sweetheart, but that's a very private place for a woman."
        if the_person.has_taboo("touching_penis"):
            "Almost as an afterthought, she remembers to add:"
            the_person.char "And you're my son! You shouldn't be trying to touch your mom's..."
            mc.name "Pussy."
            the_person.char "Hey, who raised you to be so crass? I know I certainly didn't!"

        else:
            mc.name "My cock is very private, but I let you touch that."
            the_person.char "[the_person.mc_title], that's different. That's your mother taking care of you."
            mc.name "But I feel the same way about you, I want to know that you're taken care of."
            the_person.char "You shouldn't have to take care of me though, that's not your responsibility."
        mc.name "Please [the_person.title], I just want to see how it feels with someone I trust."
        "[the_person.possessive_title] takes a long moment to think, but you can see her resistance is breaking down."
        the_person.char "I suppose... It's alright if it's just to show you what it's like. For when you meet a nice girl and want to impress her."
        mc.name "Exactly. Thank you [the_person.title]."
    else:
        mc.name "Why not? Don't you think it would feel good?"
        the_person.char "Of course it would feel good, I..."
        "Her eyes go wide and she shakes her head in disbelief."
        the_person.char "What am I saying! You're my son, you shouldn't be touching me. Not even if it would feel good."
        mc.name "If it would feel good for you, and I want to do it, why shouldn't I do it?"
        the_person.char "Because... Because it's just not what a good mother should let her son do, okay?"
        if the_person.has_taboo("touching_penis"):
            mc.name "According to who? Why should anyone else tell us what we should enjoy doing together as a family?"
            mc.name "It might not be \"normal\", but who cares about being normal. I just want to be with you."

        else:
            mc.name "But a good mother touches her sons cock?"
            the_person.char "That was different! It is my responsibility to make sure you are taken care of."
            mc.name "Well that felt good for me, and you wanted to do it. This is just the golden rule in action:"
            mc.name "\"Do unto others as you would have them do unto you.\", Right?"

        "She looks away and thinks for a long second, but you can see her resistance breaking down."
        the_person.char "Okay... As long as you can keep this secret, you can touch me down there."
    return

label mom_sucking_cock_taboo_break(the_person):
    mc.name "[the_person.title], can you do something special for me?"
    the_person.char "Maybe, what do you want sweetheart?"
    mc.name "I want you to give me a blowjob."
    if the_person.love > 40:
        "She stares at you in disbelief for a moment."
        the_person.char "I must have misheard you... A what?"
        mc.name "A blowjob, [the_person.title]. You know, putting your mouth on my..."
        the_person.char "I know what a blowjob is! I just... Have I really let this go so far that you think I would give you a blowjob?"
        the_person.char "I'm your mother! You're my son! I could never do that to you!"
        if not the_person.has_taboo("kissing"):
            mc.name "That's what you said about us kissing..."
            if not the_person.has_taboo("touching_penis"):
                the_person.char "That was diff..."
                mc.name "And what you said about feeling up my cock."
                if not the_person.has_taboo("touching_vagina"):
                    the_person.char "No, that wasn't... It was different!"
                    mc.name "And it was what you said when I wanted to touch your pussy."

        else:
            mc.name "I'm not normal [the_person.title], and I don't think you are either. Normal families don't feel like we do."

        mc.name "So maybe we should stop pretending that we have a normal mother-son relationship and embrace what we do have."
        "You see something in her eyes break."
        the_person.char "You're right, we aren't normal. So... What do we do? Where do we go from here?"
        mc.name "You've given a blowjob before, right?"
        "She nods meekly."
        the_person.char "When I was younger. It's been a long time..."
        mc.name "Then you know what to do. Just kneel down, put slide your lips onto it, and it'll all come back to you."
        "[the_person.possessive_title] grabs your head and kisses you passionately. You wrap your arms around her reciprocate."
        "She finally breaks the kiss, pulling back her head and staring into your eyes."
        the_person.char "I love you [the_person.mc_title]."
        mc.name "I love you too [the_person.title]. I've loved you my whole life."

    else:
        the_person.char "I'm sorry, I think I misheard you."
        mc.name "I don't think you did. I want you to give me a blowjob."
        "She shakes her head in disbelief."
        the_person.char "Come on [the_person.mc_title], you know I shouldn't do that. No matter how much I love you."
        if not the_person.has_taboo("kissing"):
            mc.name "That's what you said about us kissing, but you liked doing that."
            if not the_person.has_taboo("touching_penis"):
                the_person.char "I did, but..."
                mc.name "And it's what you said about feeling up my cock, but I think we both had a good time with that."
                if not the_person.has_taboo("touching_vagina"):
                    the_person.char "It was very impressive... But that doesn't mean we should go any furthur! Does it?"
                    mc.name "We went furthur when I touched your pussy, and you got really turned on by that, didn't you?"

        else:
            mc.name "I'm not normal [the_person.title], and I don't think you are either. We do lots of things normal families shouldn't do."

        mc.name "So let's stop worrying about what we should or shouldn't do. It's all bullshit anyways."
        "[the_person.possessive_title] stares intently into your eyes as she listens to you."
        mc.name "Let's just do what we want, and be the happiest mother and son on the whole planet."
        the_person.char "This... Really makes you happy?"
        mc.name "It does, more than I could ever explain."
        the_person.char "It makes me happy too. You're right, I should never have been worried when happiness was right in front of me."
        "[the_person.possessive_title] grabs your head and kisses you passionately. You wrap your arms around her reciprocate."
        "She finally breaks the kiss, pulling back her head and staring into your eyes."
        the_person.char "It's been a long time, but I think I still remember how to suck a man off."
        mc.name "Get on your knees and I'm sure it'll come back to you."
    return

label mom_licking_pussy_taboo_break(the_person):
    if the_person.love > 40:
        the_person.char "You can look, but you can't do any more than that sweetheart."

        if the_person.has_taboo("sucking_cock"):
            mc.name "Why not? Your pussy looks really sweet, I don't mind giving it a taste."
            the_person.char "[the_person.mc_title]! I'm your mother, that's no way to talk to me!"
            mc.name "I'm sorry. I just want to find a way make you feel as special as you are to me."
            the_person.char "Oh sweetheart... I'm very flattered, but there are other things we could do, aren't there?"
            mc.name "Why are those things okay for us to do, but this isn't?"
            the_person.char "Well... I... I don't know [the_person.mc_title]."
            mc.name "Exactly. Just relax and let me treat you [the_person.title]. Let me show you how much I love you by making you feel good."
            "She sighs loudly and nods."
            the_person.char "Fine, but only because you're being so persistent. That attitude is going to make some girl very happy one day."
            mc.name "I just want to make you happy today."
            the_person.char "Aww."


        else:
            mc.name "Why not? You've had your lips around my cock. Just relax and let me repay the favour, okay?"
            the_person.char "You... You really don't mind doing that for me?"
            mc.name "Of course not! You're the most important woman in my life [the_person.title], I want to make you feel special."
            "She thinks about it, then nods happily."
            the_person.char "Okay. That would be really nice sweetheart."
    else:
        the_person.char "Get a good look, if that's what you're after."
        mc.name "I want to do more than look. I want to know how you taste."
        the_person.char "Oh [the_person.mc_title]! I'm flattered, but you don't have to do this just to try and impress me."

        if the_person.has_taboo("sucking_cock"):
            mc.name "I don't want to do it to impress you, I want to do it to make you feel good. It would feel good, wouldn't it?"
            the_person.char "It would... But don't you think you'd enjoy doing something else more?"
            mc.name "This is for both of us to enjoy. Just relax and let me take care of you for once."
            the_person.char "I must have raised you right. You're going to make some girl very happy one day."


        else:
            mc.name "You've done the same for me, I just want to return the favour."
            the_person.char "Well, men who think like you are very rare. You're going to make some girl very happy one day."
        mc.name "For today, I just want to make you happy."
        the_person.char "Aww. You're too sweet. Okay then, you can do whatever you'd like."
    return

label mom_vaginal_sex_taboo_break(the_person):
    #TODO: Add a "How do we tell your sister?" Event after this has been triggered.
    if the_person.love > 60:
        the_person.char "We should stop... If we do this there is no going back to the way things were."
        mc.name "I don't want to go back [the_person.title]. I want to be with you."
        the_person.char "I... I do too, but you shouldn't be taking your mother as your lover."
        mc.name "I want to be your lover, your son, your best friend, and your confidant."
        mc.name "I want to be your whole world, just like you're already mine."
        the_person.char "Aww... How did I raise such a romantic gentleman?"
        the_person.char "Okay, if you're ready then I'm ready. Take me [the_person.mc_title]!"


    else:
        the_person.char "I should stop you here... This is so wrong. Isn't it?"
        mc.name "I don't think there's anything wrong. Why do you?"
        the_person.char "My son has his cock out and I'm actually thinking about letthing him have sex with me!"
        the_person.char "Isn't that crazy!? Did we both go insane?"
        mc.name "I'm not just your son though, am I? We've done so much together already, isn't this just natural?"
        the_person.char "Nothing about this is natural..."
        mc.name "Yeah it is. It's natural for a young, virile man to want to fuck a beautiful woman like you."
        mc.name "And it's natural for you, a beautiful woman, to want to get fucked by someone she loves and trusts."
        mc.name "You love me, don't you?"
        the_person.char "I do..."
        mc.name "Then there's no good reason to hold back our love. We need to follow our hearts and do what makes us happy."
        mc.name "[the_person.title], you make me happy."
        the_person.char "You make me happy too. Okay, if you're ready then I think I'm ready."
        the_person.char "Come and fuck your mother!"
    return

label mom_anal_sex_taboo_break(the_person):
    if the_person.love > 60:
        the_person.char "Oh my god, you mean my butt! I... That's not where that goes, [the_person.title]!"
        if the_person.has_taboo("vaginal_sex"):
            mc.name "Should I slide it into your pussy then?"
            the_person.char "Of course not! You're my son, which means we absolutely should not be having sex."
            mc.name "That's why I want to try anal. I couldn't get you pregnant, so it's not really incest."
            mc.name "I love you so much [the_person.title], I want to try every way possible to be close to each other."
            the_person.char "I guess it wouldn't really count. It's no different than me using my hand or my boobs, right?"
            mc.name "That's what I'm saying. Have you ever tried this before?"


        else:
            mc.name "Trust me [the_person.title], we can make it work."
            the_person.char "Isn't my pussy enough? Why do you want to try anal all of a sudden?"
            if the_person.has_taboo("condomless_sex"):
                mc.name "If I'm fucking your pussy I need to wear a condom, but I don't need one if we do it like this."
                the_person.char "Does it really feel that much better?"
                mc.name "It really does."
                the_person.char "Okay, for your happiness I'll give it a try."

            else:
                mc.name "If I'm fucking your pussy I might get you pregnant, but with anal that can't hapen."
                the_person.char "Or you could put on a condom."
                mc.name "Those feel like crap though [the_person.title]. I want to feel you wrapped around my cock."
                the_person.char "Well... Okay, if it would make you happy we can give it a try."
            mc.name "Thank you [the_person.title]. Have you ever done this before?"


        "[the_person.possessive_title] shakes her head sheepishly."
        the_person.char "No. I never thought I would either."
        mc.name "I'll be as gentle as possible then."
        the_person.char "Thank you. I love you [the_person.mc_title]."
        mc.name "I love you [the_person.title]."
    else:
        the_person.char "Whoa! You mean you want to try anal? Right now?"
        if the_person.has_taboo("vaginal_sex"):
            mc.name "Why not? It's not really incest if you can't get pregnant from it, right?"
            the_person.char "I kind of see what you mean..."

        else:
            if the_person.has_taboo("condomless_sex"):
                mc.name "Why not? If I want to fuck your pussy I need to wear a condom, and they really kill the sensation."
                mc.name "If we do anal I can go in raw and feel you wrapped around me."

            else:
                mc.name "Why not? If I fuck your pussy I might get you pregnant, but that can't happen with anal."
                the_person.char "Or you could wear a condom."
                mc.name "They really kill the sensation. I want to feel you wrapped around my cock."

        the_person.char "That does sound nice..."
        mc.name "Have you ever tried anal before?"
        "She shakes her head."
        the_person.char "No. I've thought about it, but I've never been brave enough to try it."
        mc.name "I'll be as gentle as possible then, so you have time to adjust."
        the_person.char "It feels so naughty to give my anal vaginity to my own son. It's kind of turning me on."
    return

label mom_condomless_sex_taboo_break(the_person):
    # mc.name "No way. I want to feel you wrapped around me."
    the_person.char "No no no, we really can't do that! I may be old, but I could still get pregnant!"
    mc.name "That would only happen if I came inside you. You trust me to pull out, don't you?"
    the_person.char "I trust you, but accidents can happen. We should be safe."


    if the_person.has_taboo("vaginal_sex"): #You're going raw your very first time.
        mc.name "Please [the_person.title]? It's our first time, I really want this to be special."
        mc.name "Next time I'll wear a condom, I promise. Just this once, please?"
        the_person.char "Just for our first time? Okay, but you need to be extra careful, understand?"

    else:
        mc.name "It doesn't feel as good with a condom on though. Don't you want me to enjoy myself?"
        the_person.char "I do... Okay, but you need to be extra careful, understand?"

    mc.name "I understand, [the_person.title]."
    the_person.char "Good. If you don't pull out I'll have you cleaning the house for a week to make up for it."
    return

label mom_underwear_nudity_taboo_break(the_person, the_clothing):
    the_person.char "Oh! Well, I guess it's natural for a man your age to be curious about a woman's body."
    the_person.char "We can take off my [the_clothing.display_name] so you can get a look."
    "She gives you a stern, motherly look."
    the_person.char "No more than that though, okay? I don't think it's right for you to see your own mother naked."
    mc.name "Okay [the_person.title]."
    return

label mom_bare_tits_taboo_break(the_person, the_clothing):
    the_person.char "Slow down there, if you take off my [the_clothing.display_name] mommy won't be covered."
    mc.name "What's wrong with that? I've seen it all when I was younger."
    the_person.char "Well yes, but you're all grown up now. It's different."
    mc.name "Please [the_person.title]? I've always thought you had very nice boobs and I just want to get a look."
    "She sighs and rolls her eyes."
    the_person.char "I suppose it's normal for a man your age to be interested in a womans breasts..."
    the_person.char "Okay, we can take it off and you can have a look. You should be able to explore these things with someone you trust."
    mc.name "Thank you [the_person.title]."
    return

label mom_bare_pussy_taboo_break(the_person, the_clothing):
    the_person.char "Careful [the_person.mc_title], mommy doesn't want you to be able to see her delicate parts."
    mc.name "Please [the_person.title], I want to know what it looks like."
    if the_person.has_taboo("touching_vagina"):
        the_person.char "Just what it looks like?"
        mc.name "I've always been curious. I saw it when I was younger but I didn't really understand what it was for."
        the_person.char "I suppose you should be able to ask any questions you have to someone you trust..."
        "She thinks for a moment, then nods."
        the_person.char "Fine, you can take off my [the_clothing.display_name]. If you need me to explain anything you just ask, okay?"

    else:
        mc.name "You've already let me touch it, so why can't I look at it?"
        the_person.char "I suppose we have already crossed that line... Okay, you can take off my [the_clothing.display_name]."
        the_person.char "If you have any questions about my... vagina, you just ask, alright?"

    mc.name "Okay [the_person.title], I will."
    return

label mom_facial_cum_taboo_break(the_person):

    return

label mom_mouth_cum_taboo_break(the_person):

    return

label mom_body_cum_taboo_break(the_person):

    return

label mom_creampie_taboo_break(the_person):

    return

label mom_anal_creampie_taboo_break(the_person):

    return
