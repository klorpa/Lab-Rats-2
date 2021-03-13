### PERSONALITY CHARACTERISTICS ###
init 1300:
    python:
        def aunt_titles(the_person):
            valid_titles = []
            valid_titles.append(the_person.name)
            valid_titles.append("Aunt " + the_person.name)
            if the_person.love > 20:
                valid_titles.append("Auntie")
            return valid_titles

        def aunt_possessive_titles(the_person):
            valid_possessive_titles = []
            valid_possessive_titles.append(the_person.name)
            valid_possessive_titles.append("Your aunt")

            if the_person.love > 20:
                valid_possessive_titles.append("Your loving aunt")


            if the_person.love > 40 and the_person.sluttiness > 60:
                valid_possessive_titles.append("Your personal MILF")

            if the_person.sluttiness > 100:
                valid_possessive_titles.append("Your cock hungry aunt")
                valid_possessive_titles.append("Your cumdump aunt")

            return valid_possessive_titles

        def aunt_player_titles(the_person):
            valid_player_titles = []
            valid_player_titles.append(mc.name)

            if the_person.love > 20:
                valid_player_titles.append("Sweetheart")
                valid_player_titles.append("Sweety")
            return valid_player_titles

        aunt_personality = Personality("aunt", default_prefix = "wild",
            common_likes = ["small talk", "the colour pink", "makeup", "flirting"],
            common_sexy_likes = ["lingerie", "skimpy outfits", "taking control"],
            common_dislikes = ["working", "hiking", "conservative outfits"],
            common_sexy_dislikes = ["public sex", "masturbating", "being fingered", "cheating on men"],
            titles_function = aunt_titles, possessive_titles_function = aunt_possessive_titles, player_titles_function = aunt_player_titles,
            insta_chance = 0, dikdok_chance = 0)

label aunt_sex_beg_finish(the_person):
    "Wait, I really need this [the_person.mc_title]! You're making me feel like a real women, please don't stop! Please!"
    return

label aunt_sex_review(the_person, the_report):
    $ used_obedience = the_report.get("obedience_used", False) #True if a girl only tried a position because you ordered her to.
    $ comment_position = the_person.pick_position_comment(the_report)

    if comment_position is None:
        return #You didn't actually do anything, no need to comment.

    #She's worried about her SO finding out because it was in public
    if the_report.get("was_public", False) and (the_person.effective_sluttiness()+10*the_person.get_opinion_score("public sex") < comment_position.slut_cap):
        if used_obedience:
            the_person "[the_person.mc_title], everyone is watching us... You need to find use somewhere private next time, alright?"

        else:
            the_person "[the_person.mc_title], everyone is watching us... We need to find somewhere private next time, alright?"
            the_person "People are going to start talking, and they just won't understand our special relationship."

    #No special conditions, just respond based on how orgasmed and how slutty the position was.
    elif the_report.get("girl orgasms", 0) > 0 and the_report.get("guy orgasms", 0) > 0: #You both came
        if the_person.effective_sluttiness() > comment_position.slut_cap: #She's sluttier than the position cap, it was tame
            the_person "That was great [the_person.mc_title], but we don't need to be so tame next time."
            the_person "I've got a few things I could show you. Sometimes experience is more important than youth."

        elif the_person.effective_sluttiness() > comment_position.slut_requirement: #She thought it was fun/exciting
            the_person "That was great [the_person.mc_title], ah..."
            "She sighs happily, basking in the chemical warmth of her orgasm."

        elif used_obedience: #She only did it because she was commanded
            the_person "Wow, that was... intense. I didn't think you could make me feel like that!"
            "[the_person.possessive_title] seems a little embarrassed, but hides it well."

        else: # She's suprised she even tried that.
            the_person "Oh my... That was more intense than I was expecting it to be!"
            the_person "I have to admit, I got kind of carried away. I hope I haven't made you uncomfortable [the_person.mc_title]."
            mc.name "No, not at all [the_person.title]."
            "She sighs and smiles."
            the_person "Good, that's good to hear. It's all innocent fun, right?"

    elif the_report.get("girl orgasms", 0) > 0: #Only she came
        if the_person.effective_sluttiness() > comment_position.slut_cap: #She's sluttier than the position
            the_person "All done? Don't you want me to... finish you off?"
            mc.name "Maybe next time, I'm feeling pretty tired."
            the_person "Alright, well next time I'll make sure to show you all the things my years of experience have taught me."
            the_person "I'll make you cum, that's for sure!"

        elif the_person.effective_sluttiness() > comment_position.slut_requirement: #She thought it was fun/exciting
            the_person "All tired out? Well, that was amazing [the_person.mc_title]..."
            "She sighs happily, basking in the chemical warmth of her orgasm."
            the_person "Next time I'll give you all my attention, okay? I owe you after how wonderful that was."

        elif used_obedience: #She only did it because she was commanded
            the_person "All done? I feel like I should be the one thanking you after that..."
            mc.name "I'm sure you'll repay the favour some day."
            the_person "Ha, well... We'll see, alright?"

        else: # She's suprised she even tried that.
            the_person "That's a good idea, I think I need to take a rest too."
            the_person "That got a little more intense than I was planning. I just got caught up in the moment, I guess."
            the_person "I didn't do anything to make you uncomfortable, did I [the_person.mc_title]?"
            mc.name "No, nothing at all [the_person.title]. That was great."
            "She sighs, obviously relieved, and smiles."
            the_person "Good, that's good to hear. It's all just some innocent fun, right?"

    elif the_report.get("guy orgasms", 0) > 0: #Only you came
        if the_person.effective_sluttiness() > comment_position.slut_cap: #She's sluttier than the position
            the_person "All tired out? Oh sweetheart, I need to teach you how to pace yourself."
            the_person "Other girls aren't going to be so understanding if you don't pay them any attention."
            the_person "Don't worry, I've got years of experience to pass on to you. You'll learn."

        elif the_person.effective_sluttiness() > comment_position.slut_requirement: #She thought it was fun/exciting
            the_person "Did that tire you out already? Oh sweetheart, you're going to have to work on your endurance."
            the_person "Next time, if you're about to cum, just think of your mother, okay? That should help you last longer."
            the_person "Well, I'm glad you had a good time either way."

        elif used_obedience: #She only did it because she was commanded
            the_person "All finished up? Well, obviously you enjoyed yourself, so that's good."
            mc.name "Finished for now, at least. That was nice [the_person.title]."
            the_person "That's good. You're welcome [the_person.mc_title]."

        else:  # She's suprised she even tried that.
            the_person "Oh my... that went a little furthur than I was planning, but you obviously enjoyed it!"
            the_person "Next time I should probably try and keep myself a little more in control. I don't think my sister would be very impressed by us."

    else: #Nobody came.
        if the_person.effective_sluttiness() > comment_position.slut_cap: #She's sluttier than the position
            the_person "You're already tired out, before you've even finished? Oh darling..."
            the_person "We need to work on your endurance. You aren't going to be impressing any ladies like this!"
            the_person "Oh well, I have plenty of experience to pass along. I'm sure you'll learn!"

        elif the_person.effective_sluttiness() > comment_position.slut_requirement: #She thought it was fun/exciting
            the_person "You need to stop already? Well that's a shame, I was just getting in the mood!"
            the_person "Next time we'll go a little slower, that should make it easier for you."

        elif used_obedience: #She only did it because she was commanded
            the_person "That's all? Well that's a little... surprising."
            mc.name "You aren't disappointed, are you?"
            the_person "Me? No, of course not! You were just taking it so seriously, I thought you really needed to... finish."
            the_person "Oh well, I just hope you got what you were hoping for."

        else:  # She's suprised she even tried that.
            the_person "Oh lord, of course we should stop. I'm sorry [the_person.mc_title], I got carried away and took this too far."
            the_person "I haven't made you uncomfortable, have I?"
            mc.name "No, of course not. That was fun."
            "She sighs, obviously relieved, and smiles."
            the_person "Good, I'm glad you had a good time. I don't think my sister would be very impressed with us right now."
    return

label aunt_flirt_response_low(the_person):
    the_person "Thank you [the_person.mc_title], that's very kind of you to say."
    the_person "It's nice to know my sense of style isn't too dated."
    mc.name "Not at all, I think it's fantastic."
    "She smiles and laughs."
    the_person "You better stop there or I'll drag you clothes shopping with me."
    return

label aunt_flirt_response_mid(the_person):
    if the_person.effective_sluttiness("underwear_nudity") < 20: # Not very slutty, mostly just high love
        the_person "[the_person.mc_title]! You shouldn't be saying that."
        mc.name "Why not? You're hot and I'm just trying to give you a compliment."
        the_person "Thank you, but I'm your aunt. It's not appropriate."
        "She sighs and rolls her eyes."
        the_person "I... guess it's still nice to hear though. It's been a while since anyone thought I was \"hot\"."
        mc.name "Well I'm happy to tell you that you are very, very hot [the_person.title]."
        "[the_person.possessive_title] smiles and shrugs."
        the_person "Fine, I'm hot. Just... don't tell your mother you talk to me like this. She would think it's weird."
    else:
        the_person "Thank you! You know, it's been a long time since anyone thought I was \"hot\"."
        the_person "I didn't think it would be my own nephew who thought so, but I'll take what I can get."
        "[the_person.possessive_title] smiles and runs her hands down her hips. She hesitates for a moment, then turns around and pats her ass."
        $ the_person.draw_person(position = "back_peek")
        the_person "Do... Do you think my butt still looks good? I know I shouldn't ask you, but... I'm a little self-conicous and I trust you."
        mc.name "Your ass looks fantastic [the_person.title]."
        $ the_person.draw_person()
        "She turns back and sighs with relief."
        mc.name "You don't have anything to worry about. You've got the body of a woman half your age."
        the_person "Sorry, I've been so silly. You don't want to hear me talking about myself like this."
        mc.name "It's fine, I really don't mind."
    return

label aunt_flirt_response_high(the_person):
    if mc.location.get_person_count() == 1: #If you are alone she'll flirt with you
        if the_person.effective_sluttiness() > (25 - the_person.get_opinion_score("incest")*5): # High sluttiness flirt
            if the_person.has_taboo("underwear_nudity"):
                the_person "Oh [the_person.mc_title], you're so bad! Do you really want to... see me naked?"

            else:
                the_person "Oh [the_person.mc_title], haven't you seen enough of me? Do you really need more?"
            mc.name "You're so beautiful, I always want to see more."
            "She sighs and smiles."
            the_person "I can't believe I'm even thinking about it, it's so wrong..."
            the_person "Maybe you need to convince me a little more."

            menu:
                "Kiss her.":
                    mc.name "Alright, is this going to convince you?"
                    "You put an arm around [the_person.possessive_title]'s waist and pull her close."

                    if the_person.has_taboo("kissing"):
                        $ the_person.call_dialogue("kissing_taboo_break")
                        $ the_person.break_taboo("kissing")
                        "You lean in and kiss her. She hesitates for a moment before gently pressing herself against your body."
                    else:
                        "You lean in and kiss her. She hesitates for a moment before responding, leaning her body against yours and kissing you back."
                    call fuck_person(the_person, private = True, start_position = kissing, skip_intro = True) from _call_fuck_person_59
                    $ the_report = _return
                    $ the_person.call_dialogue("sex_review", the_report = the_report)

                "Just flirt.":
                    mc.name "How about you just jiggle your tits for me, and that'll be all. I always want to see that."
                    the_person "That's not so bad, right?"
                    $ the_person.draw_person(the_animation = blowjob_bob)
                    "[the_person.possessive_title] grabs her own tits and jiggles them up and down, alternating between her left and right boob."
                    "She lets you watch for a few moments, then lets go and laughs self-conciously."
                    the_person "You're such a bad influence on me, you know that?"
                    $ the_person.draw_person()

        else: # Just high love flirt, she's not slutty enough to be sedueced by her own nephew.
            the_person "Oh [the_person.mc_title], stop! I want you to feel comfortable with me, but I'm still your aunt."
            mc.name "Relax, we're just joking around. Unless you want to get naked for me?"
            "She laughs and shakes her head in disbelief."
            if the_person.has_taboo(["bare_tits","bare_pussy"]):
                the_person "Obviously I could never do that. What would my sister think of me?"
            else:
                the_person "You've had your fun seeing me naked already. You'll have to be satisfied with that."

    else: #She shushes you and rushes you off somewhere private.
        if the_person.effective_sluttiness() > (25 - the_person.get_opinion_score("incest")*5): #She's slutty, but you need to find somewhere private so people don't find out.
            the_person "[the_person.mc_title]!"
            "[the_person.possessive_title] glances around nervously."
            the_person "You can't say things like that when there are other people around! What if someone overheard?"
            menu:
                "Find someplace quiet.":
                    mc.name "Then let's find somehwere nobody will. Come on."
                    "You take her hand and start to lead her away. She takes a step to follow, then hesitates."
                    the_person "Wait, I... I shouldn't."
                    mc.name "Relax, we'll be alone and nobody will know."
                    "After a pause she nods and follows after you. When you find a quiet spot you pull [the_person.possessive_title] close to you."
                    if the_person.has_taboo("kissing"):
                        $ the_person.call_dialogue("kissing_taboo_break")
                        $ the_person.break_taboo("kissing")
                        "You lean in and kiss her. She hesitates for a moment before gently pressing herself against your body."
                    else:
                        the_person "Oh! Now what?"
                        "You kiss her. She holds back for a second, then returns the kiss eagerly."
                    call fuck_person(the_person, private = True, start_position = kissing, skip_intro = True) from _call_fuck_person_60
                    $ the_report = _return
                    $ the_person.call_dialogue("sex_review", the_report = the_report)

                "Just flirt.":
                    mc.name "It's fine, nobody is going to overhear anything."
                    the_person "We should still be careful. If my sister found out we talked like this I wouldn't be able to see you any more."
                    the_person "Which would also mean..."
                    $ the_person.draw_person(the_animation = blowjob_bob)
                    "She checks that nobody else is looking, then grabs her tits and jiggles them for you."
                    the_person "You wouldn't get to see these any more either. You don't want that, do you?"
                    mc.name "You make a very convincing point..."
                    the_person "I'm glad you understand."
                    $ the_person.draw_person()

        else: #She's not slutty, so she's embarrassed about what you're doing.
            "[the_person.possessive_title] gasps softly and glances around, checking to see if anyone else was listening."
            the_person "[the_person.mc_title], I'm your aunt! We can joke around when we're alone, but if other people overhear they might get the wrong idea!"
            mc.name "It's fine, nobody heard anything."
            the_person "This time, maybe. What if my sister found out about this? She would never let me see you again."
            the_person "You don't want that, do you?"
            mc.name "No, of course not."
            the_person "Good. Just be a little more careful next time."
            "She places a gentle hand on your shoulder and kisses you on the cheek."
    return

## Sex dialogue ##
label aunt_cum_pullout(the_person):
    if mc.condom:
        if the_person.wants_creampie() and the_person.get_opinion_score("creampies") > 0 and not the_person.has_taboo("condomless_sex"): #TODO: FIgure out we want any more requirements for this to fire.
            if the_person.event_triggers_dict.get("preg_knows", False):
                "She moans happily."
                the_person "You've already gotten me pregnant [the_person.mc_title]. Do you want to take that condom off and cum in me again?"
            elif the_person.on_birth_control:
                the_person "I... I shouldn't say this, but just this once do you want to take the condom off and..."
                "She moans desperately."
                the_person "Cum inside of me? I'm on the pill, and it would feel so good!"
                $ the_person.update_birth_control_knowledge()
            else:
                the_person "Oh fuck... Do you want to take the condom off?"
                "She moans desperately."
                the_person "I don't even care if you get me pregnant, I just want to feel all of your cum inside of me!"

            menu: #TODO: Add a varient of this normally so you can stealth a girl (don't do that in real life, it's super fucked up).
                "Take off the condom.":
                    "You don't have much time to spare. You pull out, barely clearing her pussy, and pull the condom off as quickly as you can manage."
                    $ mc.condom = False
                "Leave it on.":
                    "You ignore [the_person.possessive_title]'s cum-drunk offer and keep the condom in place."

        else:
            the_person "Cum for me [the_person.mc_title], I want you to cum for me!"

    else:
        if the_person.wants_creampie():
            if the_person.on_birth_control or the_person.event_triggers_dict.get("preg_knows", False):
                the_person "Cum for me [the_person.mc_title]! Cum wherever you want!"
            else:
                the_person "I want it! Cum inside me!"
        else:
            if the_person.on_birth_control:
                the_person "Oh! Pull out, you can cum wherever else you want!"
            else:
                the_person "Oh no, you need to pull out! Quick!"
    return

label aunt_cum_condom(the_person):
    if the_person.on_birth_control:
        the_person "Good job [the_person.mc_title]. It looks like you had a really good time."

    elif the_person.wants_creampie():
        the_person "Ah, good job [the_person.mc_title]."
        the_person "It's a good thing you were wearing a condom, or I'm sure you would have gotten me pregnant right on the spot."
        the_person "My sister wouldn't be very happy about that."
        mc.name "What about you? Would you be happy?"
        "[the_person.possessive_title] stammers for a moment."
        the_person "I... I mean, we shouldn't. We can't, you know? This was nice though."

    else:
        the_person "Oh wow, good job [the_person.mc_title]. I like having you cum inside me, even if you have to wear a condom to do it."
        the_person "Maybe I should start taking the pill, so you don't have to wear one."
        $ the_person.update_birth_control_knowledge()
    return

label aunt_cum_vagina(the_person):
    if the_person.wants_creampie():
        if the_person.on_birth_control or the_person.event_triggers_dict.get("preg_knows", False):
            the_person "Ah... That felt amazing [the_person.mc_title]."
            the_person "You know just how to make me feel like a young woman again."

        else:
            the_person "Oh god, that feels so good..."
            "She sighs happily."
            the_person "You should try and pull out though, next time we do it."
            the_person "If you keep cumming inside me when I'm not on my birth control you're going to get me pregnant."
            $ the_person.update_birth_control_knowledge()

    else:
        if the_person.on_birth_control:
            the_person "Oh no... [the_person.mc_title], did you just..."
            "She already knows the answer."
            the_person "[the_person.mc_title], you need to have a little more restraint. I might have to make you wear a condom next time."
            the_person "I suppose it's going to happen time to time though. It's sort of flattering."
        else:
            the_person "Oh no, did you just..."
            "She already knows the answer."
            the_person "Oh no, no, no. I'm not on the pill [the_person.mc_title]! What happens if I get pregnant now?"
            $ the_person.update_birth_control_knowledge()
            "[the_person.possessive_title] sighs unhappily."
            the_person "I guess the damage is already done... Next time you're going to have to wear a condom. This can't keep happening."
    return

## Taboo break dialogue ##
label aunt_kissing_taboo_break(the_person):
    the_person "[the_person.mc_title], what are you doing? We shouldn't... We can't do whatever you're thinking about doing."
    mc.name "Come on, you think I'm a good looking guy, right?"
    the_person "Sure, but you're my nephew. I'm twice your age for goodness' sake!"
    mc.name "I don't mind. I'm into older women."
    the_person "And what do you think my sister would say about all this?"
    mc.name "She doesn't need to know."
    "She seems unsure, so you press on."
    mc.name "Please, [the_person.title]? You're older and know how to do all of this. I'm still figuring it all out..."
    the_person "It very confusing for a young man. I suppose..."
    "[the_person.possessive_title] sighs. You can see her resolve breaking down."
    the_person "I suppose it's better you experiment with someone who has experience and who you can trust."
    "She gives you a stern look."
    the_person "But you can't tell my sister about this, understood? [cousin.title] either. This is just between you and me."
    mc.name "Of course [the_person.title]. It will be our little secret."
    the_person "Alright, come here and let's see what we're working with..."
    return

label aunt_touching_body_taboo_break(the_person):
    if the_person.love > 20:
        the_person "[the_person.mc_title], we can't be doing this..."
        mc.name "Why not? You want it too, right?"
        the_person "My sister would never talk to me again if she found out!"
        the_person "I'm your aunt! I'm suppose to be looking after you, not letting you touch my..."
        "She looks away and trails off, embarrassed."
        mc.name "We're both adults, we can do what we want. She never needs to know."
        mc.name "Besides, if I can't figure all this stuff out with you how am I suppose to impress a girl when I meet one?"
        "She hesitates for a long moment, then turns back to you and nods."
        the_person "As long as you understand it's just so you can learn. This isn't... This shouldn't go any further."
        mc.name "Okay [the_person.title]. I understand."
    else:
        the_person "I shouldn't... Oh my god, I shouldn't be letting you touch me like this!"
        "She looks away from you and hides her head in her hands."
        the_person "My sister would never speak to me again if she knew what we were doing!"
        mc.name "Then we aren't going to tell her. We're both adults here, why do we need her permission?"
        the_person "But I'm... I'm your aunt, I should be taking care of you, not getting felt up and turned on!"
        mc.name "It may be a little strange, but we're family. You can trust me. I'm pretty turned on too."
        "She takes her head out of her hands and looks at you meekly."
        the_person "You are? I guess... I guess that's one way I can still take care of you."
        "The last bit of her resistance falls away."
        the_person "Okay, you can keep touching me..."
    return

label aunt_touching_penis_taboo_break(the_person):
    if the_person.love > 30:
        the_person "I... I'm sorry [the_person.mc_title], I think I've given you the wrong idea."
        mc.name "What do you mean?"
        the_person "I shouldn't be doing this, and now I've gotten you all worked up and..."
        "She looks down at your hard cock, inches from her hand. For a moment she seems entranced by it."
        the_person "Look what I've done. I'm so sorry."
        mc.name "Can you touch it for me, please? Just this once, since you got me turned on."
        the_person "I didn't mean to! I just... I want to have a good relationship with you and this felt so normal until..."
        mc.name "It's okay [the_person.title], I'm not blaming you. I want to have a close relationship too."
        "[the_person.possessive_title] is quiet for a moment, her eyes are still locked on your dick."
        the_person "Okay, I'll help you with... {i}this{/i}. But we shouldn't be doing this very often, okay?"
        mc.name "Okay. Thank you [the_person.title], I love you."
        the_person "You're welcome. I love you too."

    else:
        the_person "Oh look at you sweetheart... You should be very proud, {i}this{/i} is impressive."
        "She clears her throat and looks away from you."
        the_person "But we shouldn't... We shouldn't go any further..."
        "[the_person.possessive_title] doesn't look away for long, her eyes drifting back down to your hard cock, inches from her hand."
        mc.name "Come on, just a little touch. Please [the_person.title]? I'm so horny it hurts."
        "She bites her lip and thinks for a moment, then her hand starts to move."
        the_person "I know men your age have urges, and it can be very uncomfortable to not have them met."
        mc.name "Thank you [the_person.title], I love you."
        the_person "You're welcome. I love you too."
    return

label aunt_touching_vagina_taboo_break(the_person):
    if the_person.love > 30:
        the_person "Wait, you can't touch me down there [the_person.mc_title]."
        mc.name "Why not? Aren't you horny too?"
        the_person "I am but... Oh lord, what am I saying?!"
        mc.name "It's okay, you can be honest with me. You trust me, right?"
        the_person "Of course I trust you. Fine, I'm horny."
        mc.name "Then let me take care of you. It's only us here, it's nobody elses business what we do." #TODO: make sure it really is only them."
        the_person "This is so crazy... Alright, go ahead."

    else:
        the_person "We shouldn't [the_person.mc_title]. I know it would feel good but..."
        "She shakes her head."
        the_person "It just isn't right. I shouldn't feel this way!"
        if the_person.has_taboo("touching_penis"):
            mc.name "Come on [the_person.title], we're both having a good time. Aren't you horny right now?"
        else:
            mc.name "Come on [the_person.title], I had a good time when you jerked me off. I want you to feel the same way."
            mc.name "Aren't you horny right now?"
        the_person "I am, but... I can't believe I'm telling you that!"
        mc.name "That's okay, it's completely natural. All of this is normal, we just need to relax and enjoy it."
        the_person "I don't know if I can [the_person.mc_title]! I feel like a terrible aunt."
        mc.name "You're an amazing aunt, and I love spending time with you. Trust me, and let me make you feel good."
        "She is quiet for a long moment before responding."
        the_person "Alright, I trust you. Go ahead."
    return

label aunt_sucking_cock_taboo_break(the_person):
    mc.name "[the_person.title], I'm so turned on right now. Can you do something special for me?"
    the_person "What do you want [the_person.mc_title]?"
    mc.name "I want to feel your lips around my cock."
    if the_person.love > 40:
        "[the_person.possessive_title] covers her mouth and looks away, suddenly embarrassed."
        the_person "Oh [the_person.mc_title], stop! You know we shouldn't do that!"
        if not the_person.has_taboo("touching_penis"):
            mc.name "You probably shouldn't have had your hands all over my dick, but we did that too."

        elif not the_person.has_taboo("touching_vagina"):
            mc.name "You probably shouldn't have let me feel up your pussy, but we did that too."

        elif not the_person.has_taboo("kissing"):
            mc.name "You probably shouldn't have made out with me, but we did that too."

        else:
            mc.name "We've done a lot of things we shouldn't do together."
        mc.name "Maybe it's time we stopped worrying about what we {i}should{/i} be doing and focus on what we want to be doing."
        the_person "What do you mean?"
        mc.name "Do you love me?"
        the_person "Of course I love you!"
        mc.name "Then we don't need to hold back or lie about how we feel. I love you, and I want to share that love with you."
        "She thinks for a long moment. Her eyes keep flick down to your crotch, then away."
        the_person "Alright, if it means we're closer as family, I'll..."


    else:
        the_person "[the_person.mc_title]! I can't believe my sister raised such a filthy minded boy."
        mc.name "I think it's just been your corrupting influence."
        "Her eyes flick down to your crotch."
        the_person "Is it really that bad? I could... Give you a handjob, maybe?"
        mc.name "Come on [the_person.title], we both want more than that. Right?"
        the_person "I do, but... We shouldn't. I know it's fun but I worry we're taking this too far."
        "You take [the_person.possessive_title]'s hand and press it against your dick. Her fingers stroke it instinctively."
        the_person "Ah... Just once couldn't hurt, right? You won't think less of me for doing this?"
        mc.name "Of course not."
        the_person "Alright. I'll..."

    "[the_person.possessive_title] shakes her head and laughs self conciously."
    the_person "...This is so crazy! I'll give you a blowjob [the_person.mc_title]."
    return

label aunt_licking_pussy_taboo_break(the_person):
    if the_person.love > 40:
        if the_person.has_taboo("sucking_cock"):
            the_person "[the_person.mc_title], I know what you want to do, but we really shouldn't..."
            mc.name "Please [the_person.title], I need someone to practice with that will tell me how I'm really doing."
            the_person "You... You really trust me that much?"
            mc.name "Of course I do!"
            "She thinks for a long moment before responding."
            the_person "Okay, but this just for you to learn."
        else:
            the_person "You don't need to do this if you don't want to, you know. I know most men don't like..."
            mc.name "[the_person.title], I want to do this. Just relax and have a good time, okay?"
            the_person "Aw, my sister raised such a perfect gentleman."

    else:
        if the_person.has_taboo("sucking_cock"):
            the_person "Oh [the_person.mc_title]... I want to let you, but we really shouldn't. I'm flattered though."
            mc.name "Come on [the_person.title], I can tell how badly you want it. I want to make you feel good."
            the_person "But what if someone found out?"
            mc.name "Who is going to find out? It's just us here, you don't have to pretend you aren't excited." #TODO: Make sure it really is just them.
            the_person "Okay, we can give it a try. Look at what you have me agreeing to, you're so bad for me!"
        else:
            the_person "Oh! I wish I could tell my sister what a gentleman she's raised. Men love blowjobs, but it's rare to find one who's ready to reciprocate."
            mc.name "Well then, I'll do my part to make up for that. Let me know how I'm doing."
            the_person "Don't worry, if you're doing well you'll know."
    return

label aunt_vaginal_sex_taboo_break(the_person):
    if the_person.love > 60:
        the_person "We can't do this [the_person.mc_title]... If we do, there's no turning back."
        mc.name "I never want to turn back. I want to be with you."
        the_person "Do you really mean that?"
        mc.name "I do, I mean it with all my heart. I love you."
        the_person "Oh [the_person.mc_title], I love you too!"
        the_person "No turning back then, come on and fuck me!"
    else:
        the_person "This is... Oh [the_person.mc_title], I shouldn't feel like this!"
        mc.name "Why not? Don't you want it?"
        the_person "I do, but you're my nephew! I shouldn't want your cock inside me..."
        the_person "Lord, what am I even saying? I've gone insane!"
        mc.name "You're not insane, you just know what you want. You're a beautiful woman and you deserve to have an amazing sex life."
        the_person "It {i}has{/i} been a long time..."
        mc.name "So, what do you say?"
        "She takes a long moment to respond."
        the_person "This may be wrong, but I want it so badly! Fuck me [the_person.mc_title], before I get ahold of myself!"
    return

label aunt_anal_sex_taboo_break(the_person):
    the_person "[the_person.mc_title], how could you even suggest that!?"
    if the_person.love > 60:
        if the_person.has_taboo("vaginal_sex"):
            mc.name "Why not? It's not like I'd be fucking your pussy. Unless you want to try that instead."
            the_person "Of course not! I'm still your aunt, having sex would be completely inappropriate!"
            mc.name "So then let's try anal. It's not like we'd really be having sex."
        else:
            mc.name "Why not? We've already had sex."
            the_person "And what was wrong with that? Didn't you have a good time?"
            mc.name "Of course, but I want to try new things."
        "[the_person.possessive_title] seems unsure, but you press on anyways."
        mc.name "Have you ever tried it before?"
        the_person "Of course, when I was younger. I'll admit it's been a few years though."
        mc.name "We'll take it slow then. Ready?"
        the_person "I can't believe I let you talk me into things like this!"
        mc.name "I'll assume that means yes."

    else:
        if the_person.has_taboo("vaginal_sex"):
            mc.name "Come on [the_person.title], I'm so turned on. Can I slid into your pussy instead?"
            "Just mentioning it makes her moan softly to herself."
            the_person "Mphh...No, no we can't do that! That's going to far, we're still family!"
            mc.name "Then let's try anal. It's not even really sex."

        else:
            mc.name "We've had sex already, now I want to experiment a little bit."
        "[the_person.possessive_title] seems unsure, but you press on."
        mc.name "Have you ever tried it before?"
        the_person "Of course, when I was younger. It's been a few years though, I might need to be... stretched out a little."
        mc.name "We'll take it slow then. Ready?"
        the_person "No, but I don't think I'll ever be. Go ahead [the_person.mc_title], let's see if you even fit!"
    return

label aunt_condomless_sex_taboo_break(the_person):
    the_person "You need to wear a condom [the_person.mc_title]. What if you get a little too excited?"
    the_person "I might be older than you, but you could still get me pregnant."
    if the_person.has_taboo("vaginal_sex"):
        mc.name "Don't you want our first time to be special? I promise I'll pull out."
    else:
        mc.name "Don't you trust me by now? I promise I'll pull out."

    if the_person.on_birth_control:
        the_person "Well... Okay, but only because I'm on birth control. You should still be careful and try and pull out."
        $ the_person.update_birth_control_knowledge()
    else:
        the_person "Well... Okay, but I'm not on any birth control right now so you'll need to be very careful."
        $ the_person.update_birth_control_knowledge()
    mc.name "I will be. Thank you [the_person.title]."
    return

label aunt_underwear_nudity_taboo_break(the_person, the_clothing):
    the_person "Feeling a little curious? Well..."
    "She crosses her arms and thinks for a moment, then shrugs and smiles."
    the_person "I suppose you can take a look. It's natural for a boy your age to be curious."
    the_person "But you can only take my [the_clothing.display_name] off. My sister wouldn't be very happy with me if I showed you any more."
    return

label aunt_bare_tits_taboo_break(the_person, the_clothing):
    the_person "Hey, I don't know if you should be looking at me topless [the_person.mc_title]."
    mc.name "Why not? We both know you have tits. What's there to hide?"
    the_person "Well we're family, so it's a little different. You shouldn't be looking at my... tits."
    mc.name "Come on, don't you feel comfortable with me? They look really nice, I just want to take a look."
    "She sighs and rolls her eyes."
    the_person "Alright, alright. I guess I can't blame someone your age for being a little turned on."
    the_person "Go ahead, you can take off my [the_clothing.display_name]."
    return

label aunt_bare_pussy_taboo_break(the_person, the_clothing):
    the_person "Hey, were you going to take off my [the_clothing.display_name]?"
    mc.name "Well, yeah."
    the_person "I shouldn't be naked in front of you [the_person.mc_title]. They should probably stay on."
    if the_person.has_taboo("touching_vagina"):
        mc.name "Please [the_person.title], I just want to take a look at your pussy."
        the_person "I shouldn't... You just want to look though?"
        "You nod, and [the_person.possessive_title] thinks for a moment."
        the_person "Alright, but just so you can look. And don't tell anyone I let you take off my [the_clothing.display_name], understood?"
        mc.name "Okay, I promise I won't tell anyone."

    else:
        mc.name "There's no reason to be shy. I've already had my hand down there, I just want to see it too."
        the_person "I guess you're right, it's a little late now for me to be worried."
        the_person "Alright, but you can't tell anyone that I'm letting you take off my [the_clothing.display_name], understood?"
        mc.name "I promise I won't tell a soul."
    return
#
# label aunt_facial_cum_taboo_break(the_person):
#
#     return
#
# label aunt_mouth_cum_taboo_break(the_person):
#
#     return
#
# label aunt_body_cum_taboo_break(the_person):
#
#     return
#
label aunt_creampie_taboo_break(the_person):
    the_person "Oh my god, did you just..."
    "[the_person.possessive_title] gasps, then is silent for a moment."
    if the_person.wants_creampie():
        the_person "It's not your fault, I know I said I wanted it. I got so carried away that I wasn't thinking straight."
        mc.name "That means you had a good time, right? So what's the problem?"
        if the_person.on_birth_control:
            the_person "I... I'm your aunt! My sister would be so disappointed in me if she knew I was fucking her son behind her back!"
            the_person "I don't know what's happens to me, I just lose my mind and want even more!"

        else:
            the_person "I'm your aunt, and I'm not even on birth control! What happens if I got pregnant? What would we tell my sister?"
            $ the_person.update_birth_control_knowledge()
            the_person "I don't know what's happens to me, I just lose my mind and want even more!"
        mc.name "Trust your body, what is it telling you?"
        the_person "...That I love you, and I love this."
        mc.name "Then that's all that matters. We'll worry about my mom later, alright."
        the_person "Okay, I trust you [the_person.mc_title]."


    else:
        if the_person.on_birth_control:
            the_person "I told you to pull out."
            mc.name "Sorry, I got a little carried away. It felt amazing for me, how about for you?"
            the_person "It felt good for me to, but I know it shouldn't."
            the_person "I'm your aunt, I shouldn't be so turned on by having a pussy full of your cum!"
            mc.name "It's what your body craves [the_person.title]. You shouldn't be resisting those urges, and who else could you trust as much as family?"
            "She takes a deep, slow breath as she tries to calm herself."
            the_person "You're probably right."

        else:
            the_person "What have you done [the_person.mc_title]? I'm not on the pill, I might get pregnant!"
            $ the_person.update_birth_control_knowledge()
            the_person "What would we do then? My sister would find out I'm fucking her son behind her back!"
            mc.name "[the_person.possessive_title], calm down. You probably aren't going to get pregnant, and nobody needs to know what we're doing."
            "She takes a deep, slow breath as she tries to calm herself."
            the_person "You're probably right, but you need to be so much more careful! Maybe you should wear a condom next time, just to be extra safe."
            mc.name "Maybe. We'll worry about that later."

    return

# label aunt_anal_creampie_taboo_break(the_person):
#
#     return
