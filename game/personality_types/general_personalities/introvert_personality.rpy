### PERSONALITY CHARACTERISTICS ###
init 1300:
    python:
        def introvert_titles(the_person):
            return the_person.name

        def introvert_possessive_titles(the_person):
            return introvert_titles(the_person)

        def introvert_player_titles(the_person):
            return mc.name

        introvert_personality = Personality("introvert", #Stephanie style personality
        common_likes = ["conservative outfits", "research work", "punk", "working", "the colour black"],
        common_sexy_likes = ["big dicks", "kissing", "anal sex", "getting head", "giving blowjobs", "masturbating", "anal creampies", "giving tit fucks"],
        common_dislikes = ["skimpy outfits", "skirts", "HR work", "marketing work", "makeup", "flirting", "small talk", "pop"],
        common_sexy_dislikes = ["skimpy outfits", "not wearing underwear", "not wearing anything", "public sex", "lingerie"],
        titles_function = introvert_titles, possessive_titles_function = introvert_possessive_titles, player_titles_function = introvert_player_titles,
        insta_chance = 20, dikdok_chance = 0)

        list_of_personalities.append(introvert_personality)

### DIALOGUE ###
label introvert_introduction(the_person):
    mc.name "Excuse me, could I bother you for a moment?"
    "She freezes, then turns around slowly to face you."
    $ the_person.set_title("???")
    the_person "What do you want?"
    mc.name "I know this is sudden, but I just saw you walking by and I felt like I needed to say hi and get your name."
    "She glances around uncomfortably."
    the_person "Why? Why do you want to talk to me?"
    $ the_person.change_happiness(-1)
    mc.name "I don't know yet, but there's something about you that I just couldn't turn away from."
    "She seems nervous while she thinks for a second."
    $ title_choice = get_random_title(the_person)
    $ formatted_title = the_person.create_formatted_title(title_choice)
    the_person "My name is [formatted_title]. Is that all you wanted to know?"
    $ the_person.set_title(title_choice)
    $ the_person.set_possessive_title(get_random_possessive_title(the_person))
    $ the_person.change_happiness(-2)
    mc.name "Well I wanted to introduce myself too..."
    return

label introvert_greetings(the_person):
    if the_person.love < 0:
        the_person "... What? Spit it out."
    elif the_person.happiness < 90:
        the_person "..."
    else:
        if the_person.sluttiness > 60:
            if the_person.obedience > 130:
                the_person "Hello [the_person.mc_title]."
            else:
                the_person "Hey."
        else:
            if the_person.obedience > 130:
                the_person "Hello."
            else:
                "[the_person.title] gives you a nod."
    return

label introvert_sex_responses_foreplay(the_person):
    if the_person.arousal < 25:
        if the_person.sluttiness > 50:
            the_person "That feels nice."
        else:
            "[the_person.title]'s breathing gets louder and heavier."

    elif the_person.arousal < 50:
        if the_person.sluttiness > 50:
            the_person "That feels really nice... Ah..."
        else:
            "[the_person.possessive_title]'s face flushes with blood as she becomes more and more aroused."

    elif the_person.arousal < 75:
        if the_person.sluttiness > 50:
            the_person "I feel so nice when you touch me like this..."
        else:
            "[the_person.title] closes her eyes and bites her lower lip. The only sound she makes is a low, sensual growl."
    else:
        if the_person.sluttiness > 50:
            the_person "I think I'm going to cum soon..."
        else:
            "[the_person.title] pants and moans, her body barely under her control."

    return

label introvert_sex_responses_oral(the_person):
    if the_person.arousal < 25:
        if the_person.sluttiness > 50:
            the_person "Your tongue feels so good..."
        else:
            "[the_person.title]'s breathing gets louder and heavier."

    elif the_person.arousal < 50:
        if the_person.sluttiness > 50:
            the_person "That's it... that's what I want."
        else:
            "[the_person.possessive_title]'s face flushes with blood as you eat her out."

    elif the_person.arousal < 75:
        if the_person.sluttiness > 50:
            the_person "Oh, my pussy... It feels so good!"
        else:
            "[the_person.title] closes her eyes and bites her lower lip. The only sound she makes is a low, sensual growl."
    else:
        if the_person.sluttiness > 50:
            the_person "You are going to... Make me cum!"
        else:
            "[the_person.title] pants and moans, her body barely under her control."

    return

label introvert_sex_responses_vaginal(the_person):
    if the_person.arousal < 25:
        if the_person.sluttiness > 50:
            the_person "Your dick feels nice."
        else:
            "[the_person.title]'s breathing gets louder and heavier as you fuck her."

    elif the_person.arousal < 50:
        if the_person.sluttiness > 50:
            the_person "You feel so big and warm..."
        else:
            "[the_person.possessive_title]'s face flushes with blood as she becomes more and more aroused."

    elif the_person.arousal < 75:
        if the_person.sluttiness > 50:
            the_person "Mmm, my pussy feels so good with your dick inside!"
        else:
            "[the_person.title] closes her eyes and bites her lower lip. The only sound she makes is a low, sensual growl."
    else:
        if the_person.sluttiness > 50:
            the_person "Your dick is going to make cum if you keep going..."
        else:
            "[the_person.title] pants and moans, her body barely under her control."

    return

label introvert_sex_responses_anal(the_person):
    if the_person.arousal < 25:
        if the_person.sluttiness > 50:
            the_person "Gah!"
        else:
            "[the_person.title]'s breathing gets louder and heavier."

    elif the_person.arousal < 50:
        if the_person.sluttiness > 50:
            the_person "Ah... I'm so stretched out..."
        else:
            "[the_person.possessive_title]'s face flushes with blood as she struggles to take your cock."

    elif the_person.arousal < 75:
        if the_person.sluttiness > 50:
            the_person "Mmm. Fuck."
        else:
            "[the_person.title] closes her eyes and grunts."
    else:
        if the_person.sluttiness > 50:
            the_person "My ass... I'm about to cum!"
        else:
            "[the_person.title] pants and grunts, her body barely under her control."

    return

label introvert_climax_responses_foreplay(the_person):
    if the_person.sluttiness > 50:
        the_person "... Mmmfh!"
        "She tenses up and moans to herself."
    else:
        the_person "I... I think I'm going to cum!"
    return

label introvert_climax_responses_oral(the_person):
    if the_person.sluttiness > 70:
        the_person "Oh fuck, I'm cumming!"
    else:
        the_person "Oh... Oh! {b}Oh!{/b}"
    return

label introvert_climax_responses_vaginal(the_person):
    if the_person.sluttiness > 70:
        the_person "I'm... Cumming!"
    else:
        the_person "Shit..."
    return

label introvert_climax_responses_anal(the_person):
    if the_person.sluttiness > 70:
        the_person "Your going to make me cum! Ah!"
    else:
        the_person "Oh fuck, I'm..."
        "She tenses up and moans loudly."
        the_person "Cumming!"
    return

label introvert_clothing_accept(the_person):
    if the_person.obedience > 130:
        the_person "If you like it, sure."
    else:
        the_person "It looks okay, I guess."
    return

label introvert_clothing_reject(the_person):
    if the_person.obedience > 130:
        the_person "I don't really like it. Sorry."
        "[the_person.possessive_title] shrugs."
    else:
        if the_person.sluttiness > 60:
            the_person "Other people would see me in this? No, I'm not wearing that."
        else:
            the_person "I don't like it."
            "[the_person.possessive_title] shrugs."
    return

label introvert_clothing_review(the_person):
    if the_person.should_wear_uniform():
        the_person "I need to get back into my uniform."
    elif the_person.obedience > 130:
        the_person "I need to get cleaned up."
    else:
        if the_person.sluttiness > 40:
            "[the_person.title] starts to get cleaned up and dressed."
        else:
            the_person "Don't look at me..."
            "[the_person.title] turns her back to you while she gets put back together."
    return

label introvert_strip_reject(the_person, the_clothing, strip_type = "Full"):
    if the_person.obedience > 130:
        the_person "I'm sorry, but my [the_clothing.display_name] needs to stay on."

    elif the_person.love < 10:
        the_person "Keep dreaming."
    else:
        "[the_person.title] shakes her head."
    return

label introvert_strip_obedience_accept(the_person, the_clothing, strip_type = "Full"):
    if the_person.obedience > 130:
        "[the_person.title] seems uncomfortably as you grab onto her [the_clothing.display_name], but doesn't say anything."
    else:
        the_person "I... I don't know if you should do that."
    return

label introvert_grope_body_reject(the_person): #TODO: Might be more of a reserved response.
    if the_person.effective_sluttiness("touching_body") < 5: #Fail point for touching shoulder
        "[the_person.title] steps back suddenly to avoid your touch."
        the_person "Sorry. I don't like people touching me..."
        mc.name "Right, of course. Don't worry about it."
        "[the_person.possessive_title] doesn't say anything else, but she seems more uncomfortable than she was before."

    else: #Fail point for touching waist
        "[the_person.possessive_title] squirms in place, then finally takes a step back to get out of your reach."
        the_person "I just... Don't like people touching me. Sorry..."
        "You hold your hands up."
        mc.name "Oh, no problem. I understand."
        the_person "Thanks..."
        "She seems uncomfortable, but doesn't say anything more about it."
    return

label introvert_sex_accept(the_person):
    if the_person.sluttiness > 70:
        if the_person.obedience < 70:
            "[the_person.title] shrugs and nods."
            the_person "Sure. Sounds like it could be fun."
        else:
            "[the_person.possessive_title] smiles and nods."
    else:
        "[the_person.title] shrugs and looks away nervously."
        if the_person.love < 0:
            the_person "With you? Ugh, I guess..."
        else:
            the_person "Sure, I guess."
    return

label introvert_sex_obedience_accept(the_person):
    if the_person.sluttiness > 70:
        "[the_person.possessive_title] seems nervious but nods."
        the_person "Okay."
    else:
        if the_person.obedience > 130:
            "[the_person.possessive_title] seems shocked, but nods meekly."
            the_person "Okay..."
        else:
            the_person "I guess I could give that a try..."
    return

label introvert_sex_gentle_reject(the_person):
    if the_person.sluttiness > 50:
        "[the_person.possessive_title] shakes her head."
        the_person "Let's do something else."
    else:
        "[the_person.possessive_title] shakes her head."
        the_person "Let's do something else. Something less serious."
    return

label introvert_sex_angry_reject(the_person):
    if not the_person.relationship == "Single":
        $ so_title = SO_relationship_to_title(the_person.relationship)
        "[the_person.possessive_title] seems shocked. She shakes her head quickly and looks away, refusing to meet your eyes."
        the_person "I have a [so_title]. No. Never."
    elif the_person.sluttiness < 20:
        "[the_person.possessive_title] seems shocked. She looks away and shakes her head, stepping away from you."
    else:
        "[the_person.possessive_title] shakes her head."
        the_person "No way, not even a chance. Ugh."
    return

label introvert_seduction_response(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 50:
            "[the_person.possessive_title] bites her lip."
            the_person "Is that so?"
        else:
            the_person "Oh... I don't know what to say..."
    else:
        if the_person.sluttiness > 50:
            the_person "You too? Well..."
            "[the_person.title] bites her lip."
        elif the_person.sluttiness > 10:
            the_person "Oh... Really?"
        else:
            "[the_person.possessive_title] seems flustered and turns her head away."
            the_person "Oh, really? I don't... Ah, I don't even know what to say!"
    return

label introvert_seduction_accept_crowded(the_person):
    if the_person.relationship == "Single":
        if the_person.sluttiness < 20:
            "[the_person.possessive_title] glances around nervously."
            the_person "Fine. Let's get out of here."
        elif the_person.sluttiness < 50:
            "[the_person.possessive_title] glances around."
            the_person "Fine. Let's get out of here."
        else:
            "[the_person.possessive_title] glances around, blushing."
            the_person "Fine. Should we go somewhere else...?"
    else:
        $ so_title = SO_relationship_to_title(the_person.relationship)
        if the_person.sluttiness + (5*the_person.get_opinion_score("cheating on men")) > 50:
            "[the_person.possessive_title] glances around at the people nearby."
            the_person "Fine. We need to go somewhere so my [so_title] doesn't find out."
        else:
            "[the_person.possessive_title] glances around, then nods meekly."
            the_person "My [so_title] can never find out. Never."
    return

label introvert_seduction_accept_alone(the_person):
    if the_person.relationship == "Single":
        if the_person.sluttiness < 20:
            the_person "I think... Okay."
        elif the_person.sluttiness < 50:
            "[the_person.possessive_title] bites her lip and nods her approval."
        else:
            "[the_person.possessive_title] eagerly nods her approval. She seems to blush in anticipation."
    else:
        $ so_title = SO_relationship_to_title(the_person.relationship)
        if the_person.sluttiness + (5*the_person.get_opinion_score("cheating on men")) > 50:
            "[the_person.possessive_title] bites her lip."
            the_person "Don't tell my [so_title]."
        else:
            "[the_person.possessive_title] seems conflicted. Her face is flush in anticipation but she holds herself back."
            the_person "I have a [so_title]. He doesn't need to know, right?"
            mc.name "It's just me and you here. You have needs and he doesn't need to know a thing."
            "Her resistance falls away completely."
    return

label introvert_seduction_refuse(the_person):
    if the_person.sluttiness < 20:
        "[the_person.possessive_title] blushes and shakes her head."
        the_person "Not right now."

    elif the_person.sluttiness < 50:
        the_person "I... No, I don't think so."

    else:
        the_person "Hmm..."
        "[the_person.possessive_title] takes a long moment to make up her mind."
        the_person "No, I don't think so [the_person.mc_title]."
    return

label introvert_flirt_response(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 50:
            the_person "I was thinking of you when I put this on."
        else:
            "[the_person.title] smiles and shrugs."
            the_person "Actions speak louder than words."
    else:
        if the_person.sluttiness > 50:
            "[the_person.possessive_title] puts her hands behind her back and rocks her hips left and right."
        else:
            "[the_person.title] blushes and looks away."
            the_person "Oh... I... ah... Thanks."
    return

label introvert_flirt_response_low(the_person):
    if the_person.is_wearing_uniform():
        if the_person.judge_outfit(the_person.outfit):
            # #She's in uniform and likes how it looks.
            "[the_person.possessive_title] blushes and looks away, suddenly shy."
            the_person "Thanks, it's just the company uniform though. It's not like I picked it out or anything..."
            mc.name "You're making the uniform look good, not the other way around."
            "[the_person.title] looks back at you and smiles."
            the_person "Thank you."
        else:
            #She's in uniform, but she thinks it's a little too slutty.
            if the_person.outfit.vagina_visible():
                the_person "Thanks... Do you think we could get uniforms that covered a little more?"
                the_person "I'm not complaining! I'm just a little shy..."
                mc.name "You don't have anything to be shy about. You have a beautiful body, and it would be a shame to cover it up."
                "[the_person.possessive_title] nods and looks away shyly."

            elif the_person.outfit.tits_visible():
                # Her tits are out
                "[the_person.possessive_title] blushes and tries to hide her breasts."
                the_person "Thanks. I don't know if I'll ever get use to having my... boobs out."
                if the_person.has_large_tits():
                    the_person "I'm normally so worried about keeping them hidden, I don't like the attention."
                mc.name "I know it's a little unusual, but you look great."
                "She nods and gives you a faint smile."

            elif the_person.outfit.underwear_visible():
                # Her underwear is visible.
                "[the_person.possessive_title] blushes."
                the_person "Thanks. I feel strange walking around half naked in front of other people."
                mc.name "I know the uniform is a little unconventional, but you look fantastic in it."
                "She nods and gives you a faint smile."

            else:
                # It's just generally slutty.
                "[the_person.possessive_title] blushes."
                the_person "I would never normally wear something like this..."
                mc.name "You don't need to worry, you look fantastic in your uniform."
                "She nods and gives a faint smile."
                the_person "Thanks."

    else:
        #She's in her own outfit.
        "[the_person.possessive_title] blushes and smiles."
        the_person "Thanks. I didn't think anyone even paid attention to what I wear."
        mc.name "Well now you know that I do."
    return

label introvert_flirt_response_mid(the_person):
    if the_person.is_wearing_uniform():
        if the_person.judge_outfit(the_person.outfit):
            the_person "Oh... Thanks."
            "[the_person.possessive_title] blushes and looks away."
            the_person "Sorry. I'm just not use to someone paying this much attention to me."
            mc.name "It's alright, you just need to be more confident. Come on, give me a spin"
            "She hesitates for a moment, then smiles meekly and nods."
            $ the_person.draw_person(position = "back_peek")
            the_person "Like this?"
            $ the_person.draw_person()
            mc.name "That was perfect. We'll have to keep working on your confidence."
            the_person "Okay, I'll try."
        else:
            "[the_person.possessive_title] blushes and tries to cover herself up with her hands."
            if the_person.outfit.vagina_visible():
                the_person "Sorry! I know these are our uniforms, but I feel so naked!"
            elif the_person.outfit.tits_visible():
                the_person "Sorry! I know these are our uniforms, but I feel so exposed with my boobs out!"
            else:
                the_person "Sorry! I know these are our uniforms, but I feel so exposed!"
            mc.name "It's okay, it's a perfect chance for you to work on your confidence. Give it time and you'll get use to it."
            "She seems unconvinced, but nods anyways."

    else:
        if the_person.effective_sluttiness() < 20:
            the_person "Oh... Thanks."
            "[the_person.possessive_title] blushes and looks away."
            the_person "Sorry. I'm just not use to someone paying this much attention to me."
            mc.name "It's alright, you just need to be more confident."
            the_person "Maybe you're right..."
            mc.name "Let's try right now. Give me a spin and show off a little."
            "She hesitates for a moment, then smiles meekly and nods."
            $ the_person.draw_person(position = "back_peek")
            the_person "Okay. Like this?"
            "[the_person.title] turns around, wiggles her butt for a second, then completes the spin and faces you again."
            $ the_person.draw_person()
            mc.name "That was great. We'll keep working on your confidence, okay?"
            the_person "Okay."

        else:
            the_person "Oh, really? Well, thanks! People don't normally complimint me. Do you really think I look cute?"
            $ the_person.draw_person(position = "back_peek")
            "[the_person.possessive_title] turns around, letting you get a look at her full outfit."
            $ the_person.draw_person()
            mc.name "You're more than cute. You're stunning."
            the_person "I... Thank you [the_person.mc_title]. That's really nice of you to say."
    return

label introvert_flirt_response_high(the_person):
    if mc.location.get_person_count() > 1 and the_person.effective_sluttiness("kissing") < (25 - (5*the_person.get_opinion_score("public_sex"))): # There are other people here, if she's not slutty she asks if you want to find somewhere quiet
        "[the_person.possessive_title] blushes and glances around nervously."
        the_person "[the_person.mc_title], someone is going to hear you!"
        menu:
            "Find someplace quiet.":
                mc.name "Alright, let's find somewhere nobody will hear us."
                the_person "I don't know if we should..."
                "You take her hand and lead her gently. After a moment of hesitation she follows behind you."
                "After searching for a couple of minutes you find a quiet space for just the two of you. Her cheeks are red when you turn back to her."
                the_person "So... What do you want to do now?"
                if the_person.has_taboo("kissing"):
                    "You step close and put your arms around her waist."
                    $ the_person.call_dialogue("kissing_taboo_break")
                    $ the_person.break_taboo("kissing")
                else:
                    "You step close and put your arms around her waist. She closes her eyes, sighs happily, and waits for you to kiss her."
                "You lean forward and press your lips against hers. [the_person.possessive_title] responds, leaning her body against yours."
                call fuck_person(the_person, private = True, start_position = kissing, skip_intro = True) from _call_fuck_person_57
                $ the_report = _return
                $ the_person.call_dialogue("sex_review", the_report = the_report)

            "Just flirt.":
                mc.name "So if it wasn't for the audience I'd have you naked by now? That's good to know."
                "She slaps your shoulder playfully and smiles."
                the_person "Oh my god, you're the worst! Obviously you would have to buy me dinner too."

    else: # She wants to kiss you, leading to other things.
        if mc.location.get_person_count() == 1:  #You're alone, so she was just shy
            "[the_person.possessive_title] glances around."
            the_person "Well it's just the two of us here... Maybe we could just... see where things go..."
            "She steps close to you and nervously holds your hand."
        else:  #She's slutty AND you're all alone.
            "[the_person.possessive_title] doesn't say anything for a moment. Her eyes run up and down your body, taking you in."
            the_person "Do you want to find out?"
            if the_person.has_large_tits(): #Bounces her tits for you
                $ the_person.draw_person(the_animation = blowjob_bob)
                "She grabs her tits and jiggles them for you, beckoning you closer."
        menu:
            "Kiss her.":
                $ the_person.draw_person()
                if the_person.has_taboo("kissing"):
                    "You step close and put your arms around her waist."
                    $ the_person.call_dialogue("kissing_taboo_break")
                    $ the_person.break_taboo("kissing")
                    "You lean forward and press your lips against hers. [the_person.possessive_title] responds, leaning her body against yours."
                else:
                    "You wrap your hands around [the_person.title]'s waist and pull her close to kiss her. She returns the kiss immediately, pressing her body against yours."
                call fuck_person(the_person, start_position = kissing, skip_intro = True) from _call_fuck_person_58
                $ the_report = _return
                $ the_person.call_dialogue("sex_review", the_report = the_report)

            "Just flirt.":
                $ the_person.draw_person()
                mc.name "I do, but you'll have to wait until later."
                the_person "Are you sure?"
                "You nod and [the_person.title] sighs, obviously disappointed."
                the_person "Okay, maybe later then."
    return

label introvert_flirt_response_girlfriend(the_person):
    # Lead in: mc.name "You're so beautiful [the_person.title], I'm so lucky to have a woman like you in my life."
    if mc.location.get_person_count() > 1:
        # There are other people around, so she'll only start making out with you if she's slutty.
        if the_person.effective_sluttiness("kissing") < (25 - (5*the_person.get_opinion_score("public_sex"))):
            # Not very slutty, so she wants to find somewhere private
            "[the_person.possessive_title] blushes and looks away meekly."
            the_person "[the_person.mc_title], you're so embarrassing!"
            the_person "But I... I'm lucky to have you too."
            "She glances around, then leans close to you and kisses you on the cheek."
            the_person "That's all for now. I'm a little shy with other people around..."
            menu:
                "Find someplace quiet.":
                    mc.name "Then let's find somewhere we can be alone."
                    "She glances around again, then nods and takes your hand."
                    "You lead her away, and after a few minutes of searching you find a place for you and [the_person.title] to be alone."
                    "You put your arm around her waist and pull her close. She presses her body against you eagerly as you kiss her."
                    call fuck_person(the_person, private = True, start_position = kissing, skip_intro = True) from _call_fuck_person_81
                    $ the_report = _return
                    $ the_person.call_dialogue("sex_review", the_report = the_report)

                "Just flirt.":
                    mc.name "Well then I'll have to get you alone and see what you have planned."
                    "She bites her lower lip and shrugs innocently."

        else:
            "[the_person.possessive_title] smiles and leans close to you, whispering in her ear while she rubs your arm."
            the_person "If we were alone I'd show you just how lucky you are..."
            "Her hand runs lower, brushing your hips before she pulls it back."
            menu:
                "Kiss her.":
                    mc.name "Why wait until later? You aren't that shy, are you?"
                    "You put your arm around her waist and pull her close. She closes her eyes and leans against you as you kiss her."
                    call fuck_person(the_person, start_position = kissing, skip_intro = True) from _call_fuck_person_82
                    $ the_report = _return
                    $ the_person.call_dialogue("sex_review", the_report = the_report)

                "Just flirt.":
                    mc.name "Well when we're alone I'll make sure you feel just as lucky. I've got a few ideas how to do that..."
                    "You put an arm around her waist and rest your hand on her ass, rubbing it gently."
                    the_person "Mmm. Looking forward to it."
    else:
        # You're alone, so she's open to fooling around.
        "[the_person.possessive_title] blushes and shrugs."
        the_person "I'm just being me... Is that really so special?"
        "You put your arm around her and kiss her. She smiles and laughs happily."
        menu:
            "Make out.":
                "You lean in and kiss her more sensually. She sighs and relaxes, her body pressing against yours."
                call fuck_person(the_person, start_position = kissing, skip_intro = True) from _call_fuck_person_83
                $ the_report = _return
                $ the_person.call_dialogue("sex_review", the_report = the_report)

            "Just flirt.":
                "You lower your hand and rub [the_person.title]'s ass."
                mc.name "Of course you're special. You're smart, pretty, and..."
                "You squeeze her butt, making her laugh and press herself against you."
                mc.name "You have a great ass."
                the_person "Haha, well thank you. You're pretty cool too."
                "She hugs you, and you both enjoy the moment in silence."
    return

label introvert_flirt_response_affair(the_person):
    # Lead in: mc.name "You look so good today [the_person.title], you're making me want to do some very naughty things to you."
    $ so_title = SO_relationship_to_title(the_person.relationship) # "husband", "boyfriend", etc.
    if mc.location.get_person_count() > 1: #There are other people around, she's nervous about people finding out what you're doing.
        if (the_person.get_opinion_score("cheating on men") *15) + the_person.effective_sluttiness() > 50: #SHe's turned on by flirting in public or doesn't think anything is wrong with it
            the_person "Oh yeah? Well..."
            "She takes your hand and pulls you close, whispering in your ear."
            the_person "How about we go somewhere private and you can do all those naughty things to me."
            menu:
                "Find someplace quiet.":
                    mc.name "I can't turn that offer down. Come on."
                    "You lead [the_person.possessive_title] away. After a few minutes of searching you find a quiet spot."
                    "You put your arm around her waist and pull her into a deep, sensual kiss."
                    "She presses her body against you, grinding her hips against your leg."
                    call fuck_person(the_person, private = True, start_position = kissing, skip_intro = True) from _call_fuck_person_84
                    $ the_report = _return
                    $ the_person.call_dialogue("sex_review", the_report = the_report)

                "Just flirt.":
                    "You put your arm around [the_person.possessive_title] and rest your hand on her ass."
                    mc.name "I wish I could, but I don't have the time right now."
                    "She bites her lip and nods."
                    the_person "Okay, don't make me wait too long. I need you so badly..."

        else: #She's shy or nervous about being discovered
            the_person "Oh god, [the_person.mc_title]! Keep your voice down... I don't want my [so_title] to hear any rumours about us."
            mc.name "Relax, he's not going to hear anything. I'm just having a little fun, that's all."
            the_person "Next time we're alone you'll have a lot of fun. Until then you're going to have to keep it in your pants. Okay?"
            mc.name "I think I can contain myself."
            the_person "It won't be for too long. I promise."
    else:
        the_person "Yeah? Well there's nobody around, and I'm not going to stop you."
        menu:
            "Feel her up.":
                "You put your hands on [the_person.possessive_title]'s ass and pull her close to you, massaging her cheeks gently."
                the_person "Oh! Oh... That feels nice..."
                mc.name "Good. Just relax and leave everything to me."
                "You circle around her and grab her tits, bouncing them a couple times. [the_person.title] leans back against you."
                call fuck_person(the_person, private = True, start_position = standing_grope, skip_intro = True) from _call_fuck_person_85
                $ the_report = _return
                $ the_person.call_dialogue("sex_review", the_report = the_report)
            "Just flirt.":
                mc.name "Tempting, but I don't have the time right now."
                the_person "Aw, that's a shame. Well, if you do have the time you know where to find me."
    return

label introvert_flirt_response_text(the_person):
    mc.name "Hey, you just popped into my head and I wanted to see what you were up to."
    "There's a brief pause, then she texts back."
    if the_person.has_role(affair_role):
        the_person "I miss you too, I want to feel you against me again."
        the_person "When can we see each other? I hope it isn't going to be too long."
        mc.name "It won't be long, I promise."

    elif the_person.has_role(girlfriend_role):
        the_person "Not up to much, thinking about you too. You're just so wonderful."
        the_person "I hope we can see each other soon, it's been way too long since I got to spend time with you!"
        mc.name "It won't be long. Promise."

    elif the_person.love < 40:
        if the_person.effective_sluttiness() > the_person.love:
            the_person "Not much. So what were you thinking about when you thought of me?"
            the_person "Something nice, I hope."

        else:
            the_person "Not much."
            the_person "So.... what's up with you?"

    else:
        if the_person.effective_sluttiness() > the_person.love:
            the_person "Thinking about me, huh?"
            the_person "Well we both know what that means. I'm flattered though, really."

        else:
            the_person "Thinking of me, huh? Well, we should get together and hang out."
            the_person "Let me know when you're free and we can set something up."
    return


label introvert_cum_face(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 60:
            "[the_person.title] licks her lips, cleaning up a few drops of your semen that had run down her face."
        else:
            "[the_person.title] runs a finger along her cheek, wiping away some of your semen."
    else:
        if the_person.sluttiness > 80:
            "[the_person.title] looks you in the eye, then runs her tongue over her lips seductively."
        else:
            "[the_person.title] wipes some of your cum off her face with the back of her hand."
    return

label introvert_cum_mouth(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 60:
            the_person "Mmm. Thank you."
        else:
            the_person "Mmm."
    else:
        if the_person.sluttiness > 80:
            the_person "Mmm, you taste great."
        else:
            the_person "Ugh."
    return

label introvert_cum_pullout(the_person):
    # Lead in: "I'm going to cum!"
    if mc.condom:
        #TODO: We might want to split the ask section off into a different dialogue option
        if the_person.wants_creampie() and the_person.get_opinion_score("creampies") > 0 and not the_person.has_taboo("condomless_sex"): #TODO: FIgure out we want any more requirements for this to fire.
            if the_person.event_triggers_dict.get("preg_knows", False):
                the_person "I'm already pregnant, do you want to take that condom off and cum inside?"
            elif the_person.on_birth_control:
                the_person "Fuck, I want you to feel your cum inside me [the_person.mc_title]!"
                the_person "Do you... want to take the condom off? Just this once, I'm on the pill."
                $ the_person.update_birth_control_knowledge()
                "She moans deserately."
                the_person "Come on, I need it so badly!"
            else:
                the_person "Oh fuck... Do you want to knock me up?"
                "She seems almost desperate as asks between breathy moans."
                the_person "You can take the condom off and cum inside me. I want you to fuck my life up and get me pregnant!"
            #TODO: Add some more varients if she has a boyfriend or something
            #TODO: Add a varient if she's related to you ("Get me pregnant with our incest baby!")

            menu: #TODO: Add a varient of this normally so you can stealth a girl (don't do that in real life, it's super fucked up).
                "Take off the condom.":
                    "You don't have much time to spare. You pull out, barely clearing her pussy, and pull the condom off as quickly as you can manage."
                    $ mc.condom = False
                "Leave it on.":
                    "You ignore [the_person.possessive_title]'s cum-drunk offer and keep the condom in place."


        else:
            the_person "Yeah? Fucking do it! Cum for me [the_person.mc_title]!"


    else:
        if the_person.wants_creampie():
            if the_person.event_triggers_dict.get("preg_knows", False): #She's already knocked up, so who cares!
                the_person "Ah! Let it all out [the_person.mc_title]!"
            elif the_person.get_opinion_score("creampies") > 0:
                "[the_person.possessive_title] moans happily."
                if the_person.on_birth_control: #She just likes creampies.
                    the_person "Oh god, yes! I want you to creampie me [the_person.mc_title]! Put all of that hot cum inside me!"
                else: #Yeah, she's not on BC and asking for you to creampie her. She's looking to get pregnant.
                    the_person "Oh god, yes! Cum and knock me up! Aaah!"
            elif the_person.on_birth_control: #She's on the pill, so she's probably fine
                the_person "Yeah? Cum wherever you want, I'm on the pill. Ah!"
                $ the_person.update_birth_control_knowledge()
            else: #Too distracted to care about getting pregnant or not. Oh well, what could go wrong?
                the_person "Yeah? Do it! Cum for me [the_person.mc_title]!"
        else:
            if not the_person.on_birth_control: #You need to pull out, I'm not on the pill!
                the_person "Fuck, you've got to pull out! I'm not taking the pill!"
                $ the_person.update_birth_control_knowledge()

            elif the_person.get_opinion_score("creampies") < 0:
                the_person "Ah, make sure to pull out!"

            else:
                the_person "Ah, you should pull out, just in case!"
    return

label introvert_cum_condom(the_person):
    if the_person.effective_sluttiness() > 75 or the_person.get_opinion_score("creampies") > 0:
        the_person "There's so much cum... I just wish it was inside me."
    else:
        the_person "Do you always cum this much? Wow."
    return

label introvert_cum_vagina(the_person):
    if the_person.has_taboo("creampie"):
        $ the_person.call_dialogue("creampie_taboo_break")
        $ the_person.break_taboo("creampie")
        return

    if the_person.wants_creampie():
        if the_person.event_triggers_dict.get("preg_knows", False):
            the_person "Oh wow, it's so hot inside me."
            "She sighs happily."

        elif the_person.on_birth_control:
            if the_person.relationship != "Single":
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person "Oh fuck... My [so_title] never came like that before. It's so hot..."
            else:
                the_person "Oh wow, it's so hot inside me."
                "She sighs happily."

        elif the_person.effective_sluttiness() > 75 or the_person.get_opinion_score("creampies") > 0:
            if the_person.relationship != "Single":
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person "Mmmm, I like having your cum inside me. Even if I have to tell my [so_title] I'm pregnant this would be worth it."

            else:
                the_person "How easily do you think I get pregnant? Maybe I just did."
                "She sighs happily and shrugs."
                the_person "Whatever. I just love feeling your hot load inside me so much."
        else:
            if the_person.relationship != "Single":
                $ so_title = SO_relationship_to_title(the_person.relationship)
                "She sighs happily."
                the_person "Mmm, your cum feels so nice and warm inside me. I wonder if you got me pregnant..."
                the_person "My [so_title] wouldn't be too happy about that. Whatever, he doesn't fuck me like you do!"

            else:
                the_person "Oh... Mmm that feels so hot."
                "She sighs happily."

    else:
        if not the_person.on_birth_control:
            if the_person.relationship != "Single":
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person "Oh shit, what if I get pregnant?"
                the_person "I would have to explain to my [so_title] how I got pregnant. I don't want to have to do that!"
            else:
                the_person "Oh shit, it's all inside me... Fuck, what if I get pregnant?"
                the_person "Ugh... It's probably fine, right? Yeah..."

        elif the_person.relationship != "Single":
            $ so_title = SO_relationship_to_title(the_person.relationship)
            the_person "Fuck, you should have pulled out..."
            "She groans unhappily."
            the_person "What am I doing, I have a [so_title]! I can't believe I let you creampie me..."

        elif the_person.get_opinion_score("creampies") < 0:
            the_person "Hey, I told you to pull out!"
            "She groans unhappily."
            the_person "Ugh, you made such a mess."

        else:
            the_person "Hey, I told you to pull out! What the hell!"

    return

label introvert_cum_anal(the_person):
    if the_person.sluttiness > 75 or the_person.get_opinion_score("anal creampies") > 0:
        the_person "Cum inside of me, I want it!"
    else:
        the_person "Ah!"
    return

label introvert_suprised_exclaim(the_person):
    $rando = renpy.random.choice(["Fuck!","Shit!","Oh fuck!","Dicks!", "Fuck me!","Ah! Oh fuck!", "Ah!", "Holy shit!", "Fucking shit!", "God fucking dammit!", "Son of a bitch!", "Mother fucker!"])
    the_person "[rando]"
    return

label introvert_talk_busy(the_person):
    if the_person.obedience > 120:
        the_person "I'm busy right now. Can we talk later?"
    else:
        the_person "Huh? Sorry, I can't talk right now."
    return

label introvert_sex_strip(the_person):
    if the_person.sluttiness < 20:
        if the_person.arousal < 50:
            the_person "Don't stare at me, okay?"
        else:
            the_person "Ah... Don't look, okay?"

    elif the_person.sluttiness < 50:
        if the_person.arousal < 50:
            the_person "Look away for a second..."

    #If she's slutty she just does it without talking

    return

label introvert_sex_watch(the_person, the_sex_person, the_position):
    if the_person.sluttiness < the_position.slut_requirement - 20:
        $ the_person.draw_person(emotion = "angry")
        the_person "What the fuck..."
        $ the_person.change_obedience(-2)
        $ the_person.change_happiness(-3)
        "[the_person.title] shakes her head while you and [the_sex_person.name] [the_position.verb]."

    elif the_person.sluttiness < the_position.slut_requirement - 10:
        $ the_person.draw_person()
        the_person "Right here? Really?"
        $ the_person.change_happiness(-1)
        "[the_person.title] rolls her eyes and tries to avert her gaze as you and [the_sex_person.name] [the_position.verb]."

    elif the_person.sluttiness < the_position.slut_requirement:
        $ the_person.draw_person()
        the_person "Right in front of me? Really?"
        $ change_report = the_person.change_slut_temp(1)
        "[the_person.title] watches for a moment, then turns away while you and [the_sex_person.name] keep [the_position.verb]."

    elif the_person.sluttiness >= the_position.slut_requirement and the_person.sluttiness < the_position.slut_cap:
        $ the_person.draw_person()
        $ change_report = the_person.change_slut_temp(2)
        "[the_person.title] blushes, watching you and [the_sex_person.name] [the_position.verb]."

    else:
        $ the_person.draw_person(emotion = "happy")
        # the_person "Come on [the_person.mc_title], [the_sex_person.name] is going to fall asleep at this rate! You're going to have to give her a little more than that."
        "[the_person.title] watches excitedly while you and [the_sex_person.name] [the_position.verb]. She whispers under her breath, almost to herself."
        the_person "Come on, give it to her. Harder..."
    return

label introvert_being_watched(the_person, the_watcher, the_position):
    if the_person.sluttiness >= the_position.slut_cap and the_watcher.sluttiness >= the_position.slut_cap:
        #They agree you should give it to her harder
        the_person "[the_person.mc_title], I want more!"
        $ the_person.change_arousal(1)
        "[the_person.title] seems turned on by [the_watcher.title] watching you and her [the_position.verb]."

    elif the_person.sluttiness >= the_position.slut_cap and the_watcher.sluttiness < the_position.slut_requirement:
        #She's super slutty and doesn't care what people think.
        the_person "Just focus on me. Just me."

    elif the_person.sluttiness >= the_position.slut_cap and the_watcher.sluttiness < the_position.slut_cap:
        #She's super slutty and encourages the watcher to be slutty.
        the_person "Did you know how good this feels [the_watcher.title]?"
        $ the_person.change_arousal(1)
        "[the_person.title] seems turned on by [the_watcher.title] watching you and her [the_position.verb]."

    elif the_person.sluttiness < the_position.slut_cap and the_watcher.sluttiness >= the_position.slut_cap:
        #She's into it and encouraged by the slut watching her.
        $ the_person.change_arousal(1)
        "[the_person.title] doesn't say anything, but she seems turned on by [the_watcher.title] watching you and her [the_position.verb]."

    elif the_person.sluttiness < the_position.slut_cap and the_watcher.sluttiness < the_position.slut_requirement:
        #She's into it but shamed by the prude watching her.
        the_person "We should go somewhere quiet..."
        $ the_person.change_arousal(-1)
        $ the_person.change_slut_temp(-1)
        "[the_person.title] seems uncomfortable with [the_watcher.title] nearby."

    else: #the_person.sluttiness < the_position.slut_cap and the_watcher.sluttiness < the_position.slut_cap:
        #They're both into it but not fanatical about it.
        "[the_person.possessive_title] glances between you and [the_watcher.title]."
        $ the_person.change_arousal(1)
        $ the_person.change_slut_temp(1)
        "[the_person.title] seems more comfortable [the_position.verbing] you with [the_watcher.title] around."

    return

label introvert_work_enter_greeting(the_person):
    if the_person.happiness < 80 or the_person.love < 0:
        "[the_person.title] glances at you when you enter the room. She promptly ignores you and turns back to her work."

    elif the_person.happiness > 130:
        if the_person.sluttiness > 40:
            "[the_person.title] looks up at you, blushes, then looks away."
        else:
            "[the_person.title] looks up from her work and gives you a quick nod."

    else:
        if the_person.sluttiness > 60:
            "[the_person.title] looks up briefly from her work. She bites her lip and winks."
        else:
            "[the_person.title] doesn't notice you come in and stays focused on her work."
    return

label introvert_date_seduction(the_person):
    if the_person.has_role(girlfriend_role): #Sluttiness gates what she's willing to talk about
        the_person "That was a fun time, so..."
        "She places her hand on your arm and caresses it."
        if the_person.effective_sluttiness(["vaginal_sex", "condomless_sex"]) > 60 and the_person.wants_creampie() and the_person.effective_sluttiness() > the_person.get_no_condom_threshold() and the_person.get_opinion_score("bareback sex") >= 0 and the_person.get_opinion_score("creampies") >= 0 and not the_person.on_birth_control and not the_person.event_triggers_dict.get("preg_knows", False):
            if the_person.get_opinion_score("creampies") > 0: #No condoms, loves creampies, she's basically asking you to knock her up. So... have her ask you to knock her up!
                the_person "Do you want to come over to my place, bend me over, and put load after load inside my unprotected pussy?"
                the_person "I think I want you to get me pregnant tonight."
            else:
                the_person "Do you want to come over to my place and fuck me all night? No protection needed, I like the risk."
        elif the_person.effective_sluttiness(["vaginal_sex", "condomless_sex"]) > 60 and the_person.effective_sluttiness() > the_person.get_no_condom_threshold() and the_person.get_opinion_score("bareback sex") > 0:
            the_person "Do you want to come over to my place and fuck me all night long? No condoms allowed."
        elif the_person.effective_sluttiness(["vaginal_sex"]) > 50 and the_person.get_opinion_score("vaginal sex") > 0:
            the_person "Do you want to come over and fuck my tight pussy, all night long?"
        elif the_person.effective_sluttiness(["anal_sex"]) > 60 and the_person.get_opinion_score("anal sex") > 0:
            the_person "Do you want to come home with me and feel my ass around your cock all night long?"
        elif the_person.effective_sluttiness(["sucking_cock"]) > 40 and the_person.get_opinion_score("sucking cock") > 0:
            the_person "Do you want to come home with me so I can gag on your cock all night long?"
        elif the_person.effective_sluttiness() > 40 and the_person.get_opinion_score("being covered in cum") > 0:
            the_person "Do you want to come home with me and spend all night glazing me with your hot cum?"
        elif the_person.effective_sluttiness(["touching_body"]) > 40 and the_person.get_opinion_score("giving tit fucks") > 0 and the_person.has_large_tits():
            the_person "Do you want to come over to my place and put that big cock of yours between my tits?"
        else: #She's not very slutty, so she leaves the invitation open to interpretation
            the_person "Do you want to come over to my place? My bed is going to feel real empty without you in it."

    elif the_person.has_role(affair_role): #We know she's slutty and in this for the sex, so no sluttiness gates for her answers
        $ so_title = SO_relationship_to_title(the_person.relationship)
        the_person "My [so_title] isn't home tonight, you know..."
        "She holds onto your arm, stroking it gently."
        if the_person.wants_creampie() and the_person.effective_sluttiness() > the_person.get_no_condom_threshold() and the_person.get_opinion_score("bareback sex") >= 0 and the_person.get_opinion_score("creampies") >= 0 and not the_person.on_birth_control and not the_person.event_triggers_dict.get("preg_knows", False):
            if the_person.get_opinion_score("creampies") > 0: #No condoms, loves creampies, she's basically asking you to knock her up. So... have her ask you to knock her up!
                the_person "Do you want to come over to my place, bend me over, and put load after load inside my unprotected pussy?"
                the_person "I think I want to get pregnant tonight."
            else:
                the_person "Do you want to come over to my place and fuck me all night? No protection needed."
        elif the_person.effective_sluttiness() > the_person.get_no_condom_threshold() and the_person.get_opinion_score("bareback sex") > 0:
            the_person "Do you want to come over to my place and fuck me all night long? No condoms allowed."
        elif the_person.get_opinion_score("vaginal sex") > 0:
            the_person "Do you want to come over and fuck my tight pussy, all night long?"
        elif the_person.get_opinion_score("anal sex") > 0:
            the_person "Do you want to come home with me and feel my ass around your cock all night long?"
        elif the_person.get_opinion_score("sucking cock") > 0:
            the_person "Do you want to come home with me so I can gag on your cock all night long?"
        elif the_person.get_opinion_score("being covered in cum") > 0:
            the_person "Do you want to come home with me and spend all night glazing me with your hot cum?"
        elif the_person.get_opinion_score("giving tit fucks") > 0 and the_person.has_large_tits():
            the_person "Do you want to come over to my place and put that big cock of yours between my tits?"
        elif the_person.get_opinion_score("cheating on men") > 0:
            the_person "Do you want to come home with me? We can do all the slutty things I tell my [so_title] I don't like to do."
            the_person "The truth is I just don't like doing them with him."
        else:
            the_person "Do you want to come over to my place and use the bed he decided to leave empty?"
    elif the_person.relationship == "Single":
        if the_person.sluttiness > the_person.love:
            if the_person.sluttiness > 40:
                the_person "I want you to come home with me. Want to come?"
            else:
                the_person "I don't normally do this. Do you want to come home with me?"
        else:
            if the_person.love > 40:
                "[the_person.title] stays close to you, before touching your arm to get your attention."
                the_person "I had a really good time. I... was wondering if you wanted to come home with me..."
            else:
                "[the_person.title] wrings her hands together nerviously, as if working up the courage to speak."
                the_person "I like you, and I want you to come home with me so I don't have to say goodbye. Do you... want to?"
    else:
        $ so_title = SO_relationship_to_title(the_person.relationship)
        if the_person.sluttiness > the_person.love:
            if the_person.sluttiness > 40:
                the_person "My [so_title] isn't around. Do you want to come home with me?"
            else:
                the_person "I know my [so_title] wouldn't like this, but do you want to come home with me? He won't be around."
        else:
            if the_person.love > 40:
                "[the_person.title] stays close to you, before touching your arm to get your attention."
                the_person "My [so_title] is never around. Do you want to come home with me? I would be happy if you did..."
            else:
                "[the_person.title] wrings her hands together nerviously, as if working up the courage to speak."
                the_person "I really like you. I have a [so_title], but I want to spend more time with you too."
                the_person "Do you... want to come home with me? He won't be around."
    return

label introvert_sex_end_early(the_person):
    if the_person.sluttiness > 50:
        if the_person.love > 40:
            if the_person.arousal > 60:
                the_person "You're done? I was hoping you'd at least help me cum."
            else:
                the_person "All done? I thought this was going somewhere."
        else:
            if the_person.arousal > 60:
                the_person "Fuck, I was hoping you'd make me cum."
            else:
                "[the_person.title] stays silent but seems disappointed that you're finishing up early."

    else:
        if the_person.love > 40:
            if the_person.arousal > 60:
                the_person "Done? I hope it wasn't something I did, I was having a really good time..."
            else:
                the_person "Done? I hope it wasn't something I did wrong."
        else:
            if the_person.arousal > 60:
                "[the_person.title] stays silent, but her cheeks are flush and her breathing is heavier than normal."
            else:
                "[the_person.title] stays silent but seems glad that you're finishing up early."
    return


label introvert_sex_take_control (the_person):
    if the_person.arousal > 60:
        "[the_person.title] grabs your arm and moans aggressively."
        the_person "No, I'm not done yet!"
    else:
        the_person "You're staying here, I was just getting started!"
    return

label introvert_sex_beg_finish(the_person):
    "[the_person.title] grabs your arm and moans desperately."
    the_person "No, please I'm so close to cumming! I... I need you to keep going!"
    return

label introvert_sex_review(the_person, the_report):
    $ used_obedience = the_report.get("obedience_used", False) #True if a girl only tried a position because you ordered her to.
    $ comment_position = the_person.pick_position_comment(the_report)

    if comment_position is None:
        return #You didn't actually do anything, no need to comment.

    #She's worried about her SO finding out because it was in public
    if the_report.get("was_public", False) and the_person.relationship != "Single" and the_person.get_opinion_score("cheating on men") <= 0: #It was public and she cares.
        $ so_title = SO_relationship_to_title(the_person.relationship)
        if the_person.has_role(affair_role): #Dialogue about her being into it, but you can't do this in case she gets caught.
            the_person "That was fun, but next time we need to somewhere private."
            the_person "Don't want my [so_title] finding out, alright?"

        elif used_obedience:
            the_person "Fuck... I hope nobody tells my [so_title]. This is going to be hard to explain."
            "She glances around nervously."
            mc.name "Relax [the_person.title], nobody's going to say a word to him. I promise."
            "[the_person.possessive_title] seems unconvinced, but nods anyways."

        else:
            the_person "Fuck, everyone was watching... This is going to be hard to explain if someone tells my [so_title]."
            mc.name "Relax, I'll make sure nobody says a word to him. You trust me, right?"
            "She nods, but seems unconvinced."

    #She's single, but worried that you did in public.
    elif the_report.get("was_public", False) and (the_person.effective_sluttiness()+10*the_person.get_opinion_score("public sex") < comment_position.slut_cap):
        if used_obedience:
            the_person "Shit, people were watching us... Why couldn't we go somewhere private?"
            "She glances around, suddenly nervously."
            mc.name "Relax [the_person.title]. Nobody cares what we're doing."
            "[the_person.possessive_title] nods, but seems unconvinced."

        else:
            the_person "Shit, everyone was watching... I got carried away, I wasn't even thinking about them."
            mc.name "Relax [the_person.title]. Nobody cares what we're doing."
            "[the_person.possessive_title] shrugs and seems unconvinced."

    #No special conditions, just respond based on how orgasmed and how slutty the position was.
    elif the_report.get("girl orgasms", 0) > 0 and the_report.get("guy orgasms", 0) > 0: #You both came
        if the_person.effective_sluttiness() > comment_position.slut_cap: #She's sluttier than the position cap, it was tame
            the_person "Heh, that was a fun warm up. Go get some rest and we can take it even furthur next time."
            the_person "You must be able to think of better things to do to me, right?"

        elif the_person.effective_sluttiness() > comment_position.slut_requirement: #She thought it was fun/exciting
            the_person "Ah, that was fun... I'm done, I need to sit down and catch my breath."
            "She gives you a dopey smile, still dazed by her orgasm."

        elif used_obedience: #She only did it because she was commanded
            the_person "We're done then, right? Good..."
            "She seems relieved, but her face is still flush with blood from her climax."
            mc.name "The cute and innocent act doesn't work when you were just begging me to make you cum."
            "[the_person.possessive_title] scowls and looks away, but she can't exactly argue with you."

        else: # She's suprised she even tried that.
            the_person "Fuck... I just got so carried away, I can't believe we did that!"
            "She still seems dazed by her orgasm."

    elif the_report.get("girl orgasms", 0) > 0: #Only she came
        if the_person.effective_sluttiness() > comment_position.slut_cap: #She's sluttier than the position
            the_person "Tired already? Aww, I had so many more things I wanted to try."
            "She sighs happily."
            the_person "Oh well, there's always next time."

        elif the_person.effective_sluttiness() > comment_position.slut_requirement: #She thought it was fun/exciting
            the_person "All done? Next time I'll make you cum first, so it's fair."

        elif used_obedience: #She only did it because she was commanded
            the_person "We're done? I thought you were going to... try and finish."
            mc.name "Some other time. Making you cum was enough for me right now."
            the_person "Oh... I... Thank you?"

        else: # She's suprised she even tried that.
            the_person "Fuck, I didn't know I could cum that hard! I need a break, my head is still spinning!"

    elif the_report.get("guy orgasms", 0) > 0: #Only you came
        if the_person.effective_sluttiness() > comment_position.slut_cap: #She's sluttier than the position
            the_person "That's really all you wanted to do? Next time I want to try something more... intense."
            the_person "I promise it'll make you cum even harder."

        elif the_person.effective_sluttiness() > comment_position.slut_requirement: #She thought it was fun/exciting
            the_person "I guess we're all done then, right? I'm glad I was able to get you off."
            the_person "Maybe next time you can help me finish too?"
            mc.name "Yeah, of course."

        elif used_obedience: #She only did it because she was commanded
            the_person "...Are we done?"
            mc.name "Yeah, we're done for now."

        else:  # She's suprised she even tried that.
            the_person "Fuck, I didn't think we were going to go that far. I got carried away, I guess."
            "She looks away, suddenly embarrassed by what she's done."

    else: #Nobody came.
        if the_person.effective_sluttiness() > comment_position.slut_cap: #She's sluttier than the position
            the_person "Are you seriously tired already? Well that's disappointing."
            the_person "Don't hold back next time, alright? I want to watch you cum."

        elif the_person.effective_sluttiness() > comment_position.slut_requirement: #She thought it was fun/exciting
            the_person "Too tired? Aw come on [the_person.mc_title], I wanted to have some more fun."
            "She pouts, obviously disappointed."
            the_person "Whatever, I guess we'll have to pick this up some other time."

        elif used_obedience: #She only did it because she was commanded
            the_person "That's it? All that and you aren't even going to finish?"
            mc.name "Were you looking forward to making me cum?"
            the_person "No, I just... I don't know what I was expecting."
            the_person "Never mind. It doesn't matter."

        else:  # She's suprised she even tried that.
            the_person "Yeah, you're right. This went too far, we should stop while we can."
    return

## Role Specific Section ##
label introvert_improved_serum_unlock(the_person):
    mc.name "[the_person.title], now that you've had some time in the lab there's something I wanted to talk to you about."
    "[the_person.title] nods and listens."
    mc.name "All of our research and development up until this point has been based on the limited notes I have from my university days. I'm sure there's more we could learn, and I want you to look into it for me."
    "[the_person.title] thinks about it, then nods again."
    the_person "Well, I may have an idea. I think it could lead to a breakthrough."
    mc.name "Go on."
    the_person "Our testing procedures focus on human safety. If we put that to the side we could gain much more information about the subjective effects of our serum."
    the_person "I want to do is take a dose of our serum myself. I would need you to record me and ask me some questions."
    return

## Taboo break dialogue ##
label introvert_kissing_taboo_break(the_person):
    if the_person.effective_sluttiness() >= 30:
        the_person "Well? What are you waiting for? Kiss me."
    elif the_person.love >= 20:
        the_person "So we're really going to do this?"
        mc.name "I think so."
        the_person "Well then... Don't just stand there."
    else:
        the_person "Are you sure about this? I don't know if..."
        mc.name "I'm sure. Just relax and enjoy yourself."
    return

label introvert_touching_body_taboo_break(the_person):
    if the_person.effective_sluttiness() >= 30:
        the_person "Does touching me turn you on, or is it just me?"
    elif the_person.love >= 20:
        the_person "Be gentle, I'm a little ticklish. Okay"
        mc.name "I'll be gentle, don't worry."
    else:
        the_person "I... I don't know if we should be doing this [the_person.mc_title]. We barely know each other..."
        mc.name "What better way to start then? You have a fantastic body."
        the_person "I... I mean..."
    return

label introvert_touching_penis_taboo_break(the_person):
    if the_person.effective_sluttiness() >= 35:
        the_person "Your cock looks so big when it's hard. It's just like I always dreamed it would be."
        mc.name "Go ahead and touch it. I bet it feels like you dreamed too."
    elif the_person.love >= 20:
        the_person "Well, I guess you're ready. Look at how big your cock is..."
        mc.name "Don't leave me waiting, you know how badly I want you to touch it."
    else:
        the_person "You're so big... Is it always that big when you're hard?"
        mc.name "Only when I'm really turned on."
        the_person "I don't know if I should go any closer... You might pop."
        mc.name "It's going to take a little more than that to get me to pop. Put your hand on it."
    return

label introvert_touching_vagina_taboo_break(the_person):
    if the_person.effective_sluttiness() >= 35:
        the_person "Mmm... Touch me [the_person.mc_title], I'm ready."
    elif the_person.love >= 20:
        the_person "I think I'm ready, but please be gentle with me [the_person.mc_title]."
        mc.name "Don't worry, I'll be gentle."
    else:
        the_person "Oh my god, I'm really about to let you... Oh my god."
        mc.name "Just relax, you'll enjoy yourself more."
    return

label introvert_sucking_cock_taboo_break(the_person):
    mc.name "I want you to do something for me."
    the_person "What?"
    mc.name "I want you to suck on my cock."
    if the_person.effective_sluttiness() >= 45:
        the_person "I was wondering when you would ask. Okay, I'll give it a try."
    elif the_person.love >= 30:
        the_person "Oh... I guess for you I can give it a try."
    else:
        the_person "You want me to suck... your cock? I don't know, we've never done anything like that."
        mc.name "Just the tip, just for a little bit. It would feel so good."
        "She bites her lip and seems indecisive, but you watch her resolve break down."
        the_person "Okay, I'll give it a try."
    return

label introvert_licking_pussy_taboo_break(the_person):
    mc.name "I want to taste your pussy [the_person.title]. Are you ready?"
    if the_person.effective_sluttiness() >= 45:
        the_person "You're really going to... Oh my god, yes, I'm ready!"
    elif the_person.love >= 30:
        the_person "You don't have to if you don't want to, you know. I don't mind."
        mc.name "Of course I want to. Now just relax and enjoy."
    else:
        if the_person.has_taboo("sucking_cock"):
            the_person "I... I think I am. I'm just a bit nervous."
            mc.name "Just relax and enjoy yourself. I'll make sure you feel really good."
        else:
            the_person "I... I am if you are. I know I sucked your cock, but you don't have to do this if you don't want to."
            mc.name "I do want to. Just relax and enjoy yourself."
        "She laughs self-consciously and nods."
        the_person "Okay, I'll try."
    return

label introvert_vaginal_sex_taboo_break(the_person):
    if the_person.effective_sluttiness() >= 60:
        the_person "Do it [the_person.mc_title], I want to feel you inside me."
    elif the_person.love >= 45:
        the_person "I think I'm ready [the_person.mc_title]. I want to feel even closer to you."
    else:
        if the_person.has_taboo("anal_sex"):
            the_person "Oh no, I'm so nervous!"
            mc.name "Don't be, I'll be gentle."
            the_person "You don't think... I'm a slut or something, do you?"
            menu:
                "Of course you are.":
                    if mc.condom:
                        mc.name "Of course I do. You're about to let me fuck your sweet little pussy."
                    else:
                        mc.name "Of course I do. You're about to let me fuck your pussy raw."
                    mc.name "You're a dirty little slut, but there's nothing wrong with that. You just have to embrace it."
                    "She nods."
                    $ the_person.change_slut_temp(1 + the_person.get_opinion_score("being_submissive"))
                    the_person "I think I've known that deep down for a while..."

                "Of course not.":
                    mc.name "Of course not. You're just doing what you want to do to be happy."
                    mc.name "Never let anyone tell you what should make you happy."
                    $ the_person.change_happiness(2)
                    "She smiles and nods."
                    the_person "Thank you. I've been feeling so unsure lately."
        else:
            the_person "You've fucked my ass, now tell me how my pussy feels."
    return

label introvert_anal_sex_taboo_break(the_person):
    if the_person.effective_sluttiness() >= 75:
        the_person "Oh fuck, you look so much bigger than any of the toys I've fit inside my ass before..."
        mc.name "Don't worry, I'll stretch you out just fine."
        "The thought seems to turn her on more than scare her."
    elif the_person.love >= 60:
        the_person "I can't believe we're doing this... Do you think you'll even fit?"
        mc.name "I'll fit, but you might not be walking right for a few days."
        the_person "Haha, sure thing..."
        the_person "... You're kidding, right?"
        mc.name "Let's find out."
    else:
        if the_person.has_taboo("vaginal_sex"):
            the_person "Fuck, you must really like it tight. We've never even fucked and you're going right for my asshole!"
            the_person "Are you even sure it's going to fit?"
            mc.name "I'll make it fit, but you might not be walking right for a few days."
            the_person "Oh fuck..."
        else:
            the_person "Oh my god, you're actually going to do it! Fuck, I hope you even fit!"
            mc.name "Don't worry, I'll stetch out your ass like I've stretched out all your other holes."
    return

label introvert_condomless_sex_taboo_break(the_person):
    if the_person.get_opinion_score("bareback sex") > 0:
        the_person "You want to fuck me raw? Fuck... That's so hot."
        if the_person.on_birth_control:
            the_person "I'm on birth control, so it should be fine, right? The chance of it not working is almost zero."
            $ the_person.update_birth_control_knowledge()
        if the_person.get_opinion_score("creampies") > 0:
            the_person "I should really tell you to pull out when you cum..."
            mc.name "{i}Are{/i} you telling me I should pull out?"
            "She bites her lip and shakes her head."
            the_person "No, I'm not."
        elif the_person.get_opinion_score("creampies") < 0:
            the_person "You'll need to pull out though. There's no way in hell I want you to cum inside me."
        else:
            the_person "You'll need to pull out though, okay? You really shouldn't cum inside me right now."

    elif the_person.love > 60:
        the_person "Okay... I want to feel close to you too [the_person.mc_title]."
        if the_person.on_birth_control:
            the_person "I'm taking birth control, so it's okay if you cum inside me."
            $ the_person.update_birth_control_knowledge()
        elif the_person.get_opinion_score("creampies") > 0:
            the_person "If we're doing this, I don't want you to pull out when you finish either."
            mc.name "Are you on the pill?"
            "She shakes her head."
            the_person "No, but I know that whatever happens we will be together."
            $ the_person.update_birth_control_knowledge()
        elif the_person.get_opinion_score("creampies") < 0:
            the_person "You'll need to pull out though. I don't want you to get me pregnant, okay?"
        else:
            the_person "You'll need to pull out though, okay? I don't think either of us want me to get pregnant yet."

    else:
        if the_person.on_birth_control:
            the_person "You really want to do it raw? Well, I'm on birth control, so I guess that's okay..."
            $ the_person.update_birth_control_knowledge()
        elif the_person.has_taboo("vaginal_sex"):
            the_person "You want to do me raw? I'm not on birth control, isn't that a little risky?"
            $ the_person.update_birth_control_knowledge()
            mc.name "I want our first time to be special though, don't you?"
            the_person "I... Fine, but just please don't cum in me right away, okay?"
        else:
            the_person "You want to do me raw? I'm not on birth control, isn't that a little risky?"
            $ the_person.update_birth_control_knowledge()
            mc.name "It'll feel so much better though. Didn't you hate how the condom felt last time?"
            the_person "I did kind of want to know what it was like without it..."
            the_person "Fine, but just please don't cum in me right away, okay?"
    return

label introvert_underwear_nudity_taboo_break(the_person, the_clothing):
    if the_person.effective_sluttiness() > 30 - (the_person.get_opinion_score("skimpy outfits") * 5):
        the_person "This is going to be the first time you've seen me in my underwear. Are you excited [the_person.mc_title]?"
        if the_person.has_taboo(["bare_tits","bare_pussy"]):
            mc.name "I am, you aren't going to make me wait, are you?"
            "She bite her lip and shakes her head."
            the_person "No, I'm not that mean. Go ahead, take it off."
        else:
            mc.name "I've already seen everything you're hiding under there, but I'd like to see it all again."
            the_person "No point in being shy then. Go ahead, take it off."

    elif the_person.love > 15:
        the_person "This is going to be the first time you've seen me in my underwear, isn't it [the_person.mc_title]?"
        "She laughs awkwardly."
        the_person "Are you excited?"
        if the_person.has_taboo(["bare_tits","bare_pussy"]):
            mc.name "I am. You aren't going to make me wait, are you?"
            "She shakes her head and you start to strip her down."

        else:
            mc.name "I've already seen everything you're hiding under there, but I like to see it anyways."
            the_person "Oh yeah, I guess you have. Well, no point being shy then."

    else:
        the_person "If I take off my [the_clothing.display_name] I'll just be wearing my underwear."
        mc.name "So?"
        the_person "It feels like we barely know each other, but I'm about to be half naked in front of you."
        if the_person.has_taboo(["bare_tits","bare_pussy"]):
            mc.name "You're not going to be any amount of naked if you keep worrying about it. Come on, let's take it off."
            "She nods obediently."
        else:
            mc.name "I've already seen you naked, so what's the big deal?"
            the_person "I guess you're right, I'm getting worked up over nothing."
    return

label introvert_bare_tits_taboo_break(the_person, the_clothing):
    if the_person.effective_sluttiness() > (40 - the_person.get_opinion_score("showing her tits") * 5):
        the_person "You want get a look at my tits [the_person.mc_title]? You're going to make me blush."
        if the_person.has_large_tits():
            "She shakes her chest for you, jiggling the large tits hidden underneath her [the_clothing.display_name]."
        else:
            "She shakes her chest and gives her small tits a little jiggle."

        mc.name "Of course I want to see them. Let's get that [the_clothing.display_name] off so I can finally see them."

    elif the_person.love > 25:
        the_person "So you want to see my... breasts?"
        if the_person.has_large_tits():
            "She looks down at her own sizeable chest, tits hidden beneath her [the_clothing.display_name]."
            the_person "I guess I can understand why. I'm a little shy though..."
        else:
            the_person "I'm a little shy about them, I wish they were bigger."
        mc.name "Don't be shy, just relax and let me take this off for you."

    else:
        the_person "Wait! If you take off my [the_clothing.display_name] my ti... breasts will be out!"
        mc.name "And what's wrong with that?"
        the_person "I don't normally do anything like this. I'm not the kind of girl to pull her... breasts out for someone."
        if the_person.has_large_tits():
            the_person "Plus they're always attracting attention, so I've gotten so use to covering them up."

        mc.name "You aren't really worried about that though, are you? Come on, I want to see your tits."
        "She takes a deep breath, then nods."
        the_person "Okay..."
    return

label introvert_bare_pussy_taboo_break(the_person, the_clothing):
    if the_person.effective_sluttiness() > (50 - the_person.get_opinion_score("showing her ass") * 5):
        the_person "Oh, you finally want to see what's going on down there? It's about time!"

    elif the_person.love > 35:
        the_person "Oh! If you take that off you're going to see my... You know."
        mc.name "That's the plan. Is there a problem with that?"
        the_person "No, I guess not. I just feel a little self concious about getting naked like this."
        if the_person.has_taboo("touching_vagina"):
            mc.name "Just take a deep breath and relax. You trust me, right?"
            the_person "Of course I do [the_person.mc_title]. Okay, go ahead..."

        else:
            mc.name "You've already let me feel your pussy, so what's wrong with taking a little look?"
            the_person "I guess you're right. Okay, go ahead..."

    else:
        the_person "Wait! If you take that off you'll be able to see my pussy."
        if the_person.has_taboo("touching_vagina"):
            mc.name "That's the point, yeah. What's wrong?"
        else:
            mc.name "You've already let me feel it, so what's the issue?"

        the_person "I... I don't know, I'm just nervous!"
        mc.name "Just take a deep breath and relax while I get these [the_clothing.display_name] off of you."
    return

label introvert_facial_cum_taboo_break(the_person):

    return

label introvert_mouth_cum_taboo_break(the_person):

    return

label introvert_body_cum_taboo_break(the_person):

    return

label introvert_creampie_taboo_break(the_person):
    if the_person.wants_creampie():
        if the_person.on_birth_control:
            if the_person.relationship != "Single":
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person "Oh fuck... I've wanted this so badly!"
                the_person "I don't even care you're not my [so_title] right now, I'm just so happy someone is finally fucking me right!"

            else:
                the_person "Oh fuck, there it is... It's been so long since someone finished in me like that."
                the_person "It feels good."

        elif the_person.effective_sluttiness() > 75 or the_person.get_opinion_score("creampies") > 0:
            if the_person.relationship != "Single":
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person "Oh fuck, you really did it. You don't even care that I have a [so_title], or that I'm not on birth control..."
                $ the_person.update_birth_control_knowledge()

            else:
                the_person "Oh fuck, you really did it. You just put your whole load right into my unprotected pussy..."
                $ the_person.update_birth_control_knowledge()

            the_person "I guess now I just have to wait and see if you knocked me up. You should put a second load in me, just to be sure."
        else:
            if the_person.relationship != "Single":
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person "Oh fuck... I really shouldn't have let you do that, but it feels so good."
                the_person "Fuck... I hope you didn't get me pregnant. That would be hard to explain to my [so_title]."

            else:
                the_person "Oh fuck... I really should have told you to pull out. It feels good to have your cum inside me though."
                the_person "I just hope you didn't get me pregnant."

    else:
        if not the_person.on_birth_control:
            the_person "Wait, did you really just cum? Right inside me?"
            "She groans."
            if the_person.relationship != "Single":
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person "Fuck! I told you to pull out! What am I going to tell my [so_title] if you get me pregnant?"
            else:
                the_person "Fuck, now what if I get pregnant? You couldn't just pull out on time?"

        elif the_person.relationship != "Single":
            $ so_title = SO_relationship_to_title(the_person.relationship)
            the_person "Wait, did you actually just cum... You were suppose to pull out!"
            the_person "Fuck... Don't make a habit of it, okay? My [so_title] would be so sad if he knew someone got to cum inside me."

        elif the_person.get_opinion_score("creampies") < 0:
            the_person "Wait, did you actually just cum... You were suppose to pull out."
            the_person "Don't make a habit of it, okay? You made such a mess inside me."

        else:
            the_person "Hey, I said to pull out. Didn't you hear?"
    return

label introvert_anal_creampie_taboo_break(the_person):

    return
