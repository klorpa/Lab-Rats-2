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
        titles_function = introvert_titles, possessive_titles_function = introvert_possessive_titles, player_titles_function = introvert_player_titles)

### DIALOGUE ###
label introvert_introduction(the_person):
    mc.name "Excuse me, could I bother you for a moment?"
    "She freezes, then turns around slowly to face you."
    $ the_person.set_title("???")
    the_person.char "What do you want?"
    mc.name "I know this is sudden, but I just saw you walking by and I felt like I needed to say hi and get your name."
    "She glances around uncomfortably."
    the_person.char "Why? Why do you want to talk to me?"
    $ the_person.change_happiness(-1)
    mc.name "I don't know yet, but there's something about you that I just couldn't turn away from."
    "She seems nervous while she thinks for a second."
    $ title_choice = get_random_title(the_person)
    $ formatted_title = the_person.create_formatted_title(title_choice)
    the_person.char "My name is [formatted_title]. Is that all you wanted to know?"
    $ the_person.set_title(title_choice)
    $ the_person.set_possessive_title(get_random_possessive_title(the_person))
    $ the_person.change_happiness(-2)
    mc.name "Well I wanted to introduce myself too..."
    return

label introvert_greetings(the_person):
    if the_person.love < 0:
        the_person.char "... What? Spit it out."
    elif the_person.happiness < 90:
        the_person.char "..."
    else:
        if the_person.sluttiness > 60:
            if the_person.obedience > 130:
                the_person.char "Hello [the_person.mc_title]."
            else:
                the_person.char "Hey."
        else:
            if the_person.obedience > 130:
                the_person.char "Hello."
            else:
                "[the_person.title] gives you a nod."
    return

label introvert_sex_responses_foreplay(the_person):
    if the_person.arousal < 25:
        if the_person.sluttiness > 50:
            the_person.char "That feels nice."
        else:
            "[the_person.title]'s breathing gets louder and heavier."

    elif the_person.arousal < 50:
        if the_person.sluttiness > 50:
            the_person.char "That feels really nice... Ah..."
        else:
            "[the_person.possessive_title]'s face flushes with blood as she becomes more and more aroused."

    elif the_person.arousal < 75:
        if the_person.sluttiness > 50:
            the_person.char "I feel so nice when you touch me like this..."
        else:
            "[the_person.title] closes her eyes and bites her lower lip. The only sound she makes is a low, sensual growl."
    else:
        if the_person.sluttiness > 50:
            the_person.char "I think I'm going to cum soon..."
        else:
            "[the_person.title] pants and moans, her body barely under her control."

    return

label introvert_sex_responses_oral(the_person):
    if the_person.arousal < 25:
        if the_person.sluttiness > 50:
            the_person.char "Your tongue feels so good..."
        else:
            "[the_person.title]'s breathing gets louder and heavier."

    elif the_person.arousal < 50:
        if the_person.sluttiness > 50:
            the_person.char "That's it... that's what I want."
        else:
            "[the_person.possessive_title]'s face flushes with blood as you eat her out."

    elif the_person.arousal < 75:
        if the_person.sluttiness > 50:
            the_person.char "Oh, my pussy... It feels so good!"
        else:
            "[the_person.title] closes her eyes and bites her lower lip. The only sound she makes is a low, sensual growl."
    else:
        if the_person.sluttiness > 50:
            the_person.char "You are going to... Make me cum!"
        else:
            "[the_person.title] pants and moans, her body barely under her control."

    return

label introvert_sex_responses_vaginal(the_person):
    if the_person.arousal < 25:
        if the_person.sluttiness > 50:
            the_person.char "Your dick feels nice."
        else:
            "[the_person.title]'s breathing gets louder and heavier as you fuck her."

    elif the_person.arousal < 50:
        if the_person.sluttiness > 50:
            the_person.char "You feel so big and warm..."
        else:
            "[the_person.possessive_title]'s face flushes with blood as she becomes more and more aroused."

    elif the_person.arousal < 75:
        if the_person.sluttiness > 50:
            the_person.char "Mmm, my pussy feels so good with your dick inside!"
        else:
            "[the_person.title] closes her eyes and bites her lower lip. The only sound she makes is a low, sensual growl."
    else:
        if the_person.sluttiness > 50:
            the_person.char "Your dick is going to make cum if you keep going..."
        else:
            "[the_person.title] pants and moans, her body barely under her control."

    return

label introvert_sex_responses_anal(the_person):
    if the_person.arousal < 25:
        if the_person.sluttiness > 50:
            the_person.char "Gah!"
        else:
            "[the_person.title]'s breathing gets louder and heavier."

    elif the_person.arousal < 50:
        if the_person.sluttiness > 50:
            the_person.char "Ah... I'm so stretched out..."
        else:
            "[the_person.possessive_title]'s face flushes with blood as she struggles to take your cock."

    elif the_person.arousal < 75:
        if the_person.sluttiness > 50:
            the_person.char "Mmm. Fuck."
        else:
            "[the_person.title] closes her eyes and grunts."
    else:
        if the_person.sluttiness > 50:
            the_person.char "My ass... I'm about to cum!"
        else:
            "[the_person.title] pants and grunts, her body barely under her control."

    return

label introvert_climax_responses_foreplay(the_person):
    if the_person.sluttiness > 50:
        the_person.char "... Mmmfh!"
        "She tenses up and moans to herself."
    else:
        the_person.char "I... I think I'm going to cum!"
    return

label introvert_climax_responses_oral(the_person):
    if the_person.sluttiness > 70:
        the_person.char "Oh fuck, I'm cumming!"
    else:
        the_person.char "Oh... Oh! {b}Oh!{/b}"
    return

label introvert_climax_responses_vaginal(the_person):
    if the_person.sluttiness > 70:
        the_person.char "I'm... Cumming!"
    else:
        the_person.char "Shit..."
    return

label introvert_climax_responses_anal(the_person):
    if the_person.sluttiness > 70:
        the_person.char "Your going to make me cum! Ah!"
    else:
        the_person.char "Oh fuck, I'm..."
        "She tenses up and moans loudly."
        the_person.char "Cumming!"
    return

label introvert_clothing_accept(the_person):
    if the_person.obedience > 130:
        the_person.char "If you like it, sure."
    else:
        the_person.char "It looks okay, I guess."
    return

label introvert_clothing_reject(the_person):
    if the_person.obedience > 130:
        the_person.char "I don't really like it. Sorry."
        "[the_person.possessive_title] shrugs."
    else:
        if the_person.sluttiness > 60:
            the_person.char "Other people would see me in this? No, I'm not wearing that."
        else:
            the_person.char "I don't like it."
            "[the_person.possessive_title] shrugs."
    return

label introvert_clothing_review(the_person):
    if the_person.obedience > 130:
        the_person.char "I need to get cleaned up."
    else:
        if the_person.sluttiness > 40:
            "[the_person.title] starts to get cleaned up and dressed."
        else:
            the_person.char "Don't look at me..."
            "[the_person.title] turns her back to you while she gets put back together."
    return

label introvert_strip_reject(the_person):
    if the_person.obedience > 130:
        the_person.char "No, don't take that off please."

    elif the_person.love < 10:
        "[the_person.title] grabs your hand to stop you."
        the_person.char "Keep dreaming."
    else:
        "[the_person.title] grabs your hand shakes her head."
    return

label introvert_sex_accept(the_person):
    if the_person.sluttiness > 70:
        if the_person.obedience < 70:
            "[the_person.title] shrugs and nods."
            the_person.char "Sure. Sounds like it could be fun."
        else:
            "[the_person.possessive_title] smiles and nods."
    else:
        "[the_person.title] shrugs and looks away nervously."
        if the_person.love < 0:
            the_person.char "With you? Ugh, I guess..."
        else:
            the_person.char "Sure, I guess."
    return

label introvert_sex_obedience_accept(the_person):
    if the_person.sluttiness > 70:
        "[the_person.possessive_title] seems nervious but nods."
        the_person.char "Okay."
    else:
        if the_person.obedience > 130:
            "[the_person.possessive_title] seems shocked, but nods meekly."
            the_person.char "Okay..."
        else:
            the_person.char "I guess I could give that a try..."
    return

label introvert_sex_gentle_reject(the_person):
    if the_person.sluttiness > 50:
        "[the_person.possessive_title] shakes her head."
        the_person.char "Let's do something else."
    else:
        "[the_person.possessive_title] shakes her head."
        the_person.char "Let's do something else. Something less serious."
    return

label introvert_sex_angry_reject(the_person):
    if not the_person.relationship == "Single":
        $ so_title = SO_relationship_to_title(the_person.relationship)
        "[the_person.possessive_title] seems shocked. She shakes her head quickly and looks away, refusing to meet your eyes."
        the_person.char "I have a [so_title]. No. Never."
    elif the_person.sluttiness < 20:
        "[the_person.possessive_title] seems shocked. She looks away and shakes her head, stepping away from you."
    else:
        "[the_person.possessive_title] shakes her head."
        the_person.char "No way, not even a chance. Ugh."
    return

label introvert_seduction_response(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 50:
            "[the_person.possessive_title] bites her lip."
            the_person.char "Is that so?"
        else:
            the_person.char "Oh... I don't know what to say..."
    else:
        if the_person.sluttiness > 50:
            the_person.char "You too? Well..."
            "[the_person.title] bites her lip."
        elif the_person.sluttiness > 10:
            the_person.char "Oh... Really?"
        else:
            "[the_person.possessive_title] seems flustered and turns her head away."
            the_person.char "Oh, really? I don't... Ah, I don't even know what to say!"
    return

label introvert_seduction_accept_crowded(the_person):
    if the_person.relationship == "Single":
        if the_person.sluttiness < 20:
            "[the_person.possessive_title] glances around nervously."
            the_person.char "Fine. Let's get out of here."
        elif the_person.sluttiness < 50:
            "[the_person.possessive_title] glances around."
            the_person.char "Fine. Let's get out of here."
        else:
            "[the_person.possessive_title] glances around, blushing."
            the_person.char "Fine. Should we go somewhere else...?"
    else:
        $ so_title = SO_relationship_to_title(the_person.relationship)
        if the_person.sluttiness + (5*the_person.get_opinion_score("cheating on men")) > 50:
            "[the_person.possessive_title] glances around at the people nearby."
            the_person.char "Fine. We need to go somewhere so my [so_title] doesn't find out."
        else:
            "[the_person.possessive_title] glances around, then nods meekly."
            the_person.char "My [so_title] can never find out. Never."
    return

label introvert_seduction_accept_alone(the_person):
    if the_person.relationship == "Single":
        if the_person.sluttiness < 20:
            the_person.char "I think... Okay."
        elif the_person.sluttiness < 50:
            "[the_person.possessive_title] bites her lip and nods her approval."
        else:
            "[the_person.possessive_title] eagerly nods her approval. She seems to blush in anticipation."
    else:
        $ so_title = SO_relationship_to_title(the_person.relationship)
        if the_person.sluttiness + (5*the_person.get_opinion_score("cheating on men")) > 50:
            "[the_person.possessive_title] bites her lip."
            the_person.char "Don't tell my [so_title]."
        else:
            "[the_person.possessive_title] seems conflicted. Her face is flush in anticipation but she holds herself back."
            the_person.char "I have a [so_title]. He doesn't need to know, right?"
            mc.name "It's just me and you here. You have needs and he doesn't need to know a thing."
            "Her resistance falls away completely."
    return

label introvert_seduction_refuse(the_person):
    if the_person.sluttiness < 20:
        "[the_person.possessive_title] blushes and shakes her head."
        the_person.char "Not right now."

    elif the_person.sluttiness < 50:
        the_person.char "I... No, I don't think so."

    else:
        the_person.char "Hmm..."
        "[the_person.possessive_title] takes a long moment to make up her mind."
        the_person.char "No, I don't think so [the_person.mc_title]."
    return

label introvert_flirt_response(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 50:
            the_person.char "I was thinking of you when I put this on."
        else:
            "[the_person.title] smiles and shrugs."
            the_person.char "Actions speak louder than words."
    else:
        if the_person.sluttiness > 50:
            "[the_person.possessive_title] puts her hands behind her back and rocks her hips left and right."
        else:
            "[the_person.title] blushes and looks away."
            the_person.char "Oh... I... ah... Thanks."
    return

label introvert_flirt_response_low(the_person):
    if the_person.outfit == the_person.planned_uniform:
        if the_person.judge_outfit(the_person.outfit):
            # #She's in uniform and likes how it looks.
            "[the_person.possessive_title] blushes and looks away, suddenly shy."
            the_person.char "Thanks, it's just the company uniform though. It's not like I picked it out or anything..."
            mc.name "You're making the uniform look good, not the other way around."
            "[the_person.title] looks back at you and smiles."
            the_person.char "Thank you."
        else:
            #She's in uniform, but she thinks it's a little too slutty.
            if the_person.outfit.vagina_visible():
                the_person.char "Thanks... Do you think we could get uniforms that covered a little more?"
                the_person.char "I'm not complaining! I'm just a little shy..."
                mc.name "You don't have anything to be shy about. You have a beautiful body, and it would be a shame to cover it up."
                "[the_person.possessive_title] nods and looks away shyly."

            elif the_person.outfit.tits_visible():
                # Her tits are out
                "[the_person.possessive_title] blushes and tries to hide her breasts."
                the_person.char "Thanks. I don't know if I'll ever get use to having my... boobs out."
                if the_person.has_large_tits():
                    the_person.char "I'm normally so worried about keeping them hidden, I don't like the attention."
                mc.name "I know it's a little unusual, but you look great."
                "She nods and gives you a faint smile."

            elif the_person.outfit.underwear_visible():
                # Her underwear is visible.
                "[the_person.possessive_title] blushes."
                the_person.char "Thanks. I feel strange walking around half naked in front of other people."
                mc.name "I know the uniform is a little unconventional, but you look fantastic in it."
                "She nods and gives you a faint smile."

            else:
                # It's just generally slutty.
                "[the_person.possessive_title] blushes."
                the_person.char "I would never normally wear something like this..."
                mc.name "You don't need to worry, you look fantastic in your uniform."
                "She nods and gives a faint smile."
                the_person.char "Thanks."

    else:
        #She's in her own outfit.
        "[the_person.possessive_title] blushes and smiles."
        the_person.char "Thanks. I didn't think anyone even paid attention to what I wear."
        mc.name "Well now you know that I do."
    return

label introvert_flirt_response_mid(the_person):
    if the_person.outfit == the_person.planned_uniform:
        if the_person.judge_outfit(the_person.outfit):
            the_person.char "Oh... Thanks."
            "[the_person.possessive_title] blushes and looks away."
            the_person.char "Sorry. I'm just not use to someone paying this much attention to me."
            mc.name "It's alright, you just need to be more confident. Come on, give me a spin"
            "She hesitates for a moment, then smiles meekly and nods."
            $ the_person.draw_person(position = "back_peek")
            the_person.char "Like this?"
            $ the_person.draw_person()
            mc.name "That was perfect. We'll have to keep working on your confidence."
            the_person.char "Okay, I'll try."
        else:
            "[the_person.possessive_title] blushes and tries to cover herself up with her hands."
            if the_person.outfit.vagina_visible():
                the_person.char "Sorry! I know these are our uniforms, but I feel so naked!"
            elif the_person.outfit.tits_visible():
                the_person.char "Sorry! I know these are our uniforms, but I feel so exposed with my boobs out!"
            else:
                the_person.char "Sorry! I know these are our uniforms, but I feel so exposed!"
            mc.name "It's okay, it's a perfect chance for you to work on your confidence. Give it time and you'll get use to it."
            "She seems unconvinced, but nods anyways."

    else:
        if the_person.effective_sluttiness() < 20:
            the_person.char "Oh... Thanks."
            "[the_person.possessive_title] blushes and looks away."
            the_person.char "Sorry. I'm just not use to someone paying this much attention to me."
            mc.name "It's alright, you just need to be more confident."
            the_person.char "Maybe you're right..."
            mc.name "Let's try right now. Give me a spin and show off a little."
            "She hesitates for a moment, then smiles meekly and nods."
            $ the_person.draw_person(position = "back_peek")
            the_person.char "Okay. Like this?"
            "[the_person.title] turns around, wiggles her butt for a second, then completes the spin and faces you again."
            $ the_person.draw_person()
            mc.name "That was great. We'll keep working on your confidence, okay?"
            the_person.char "Okay."

        else:
            the_person.char "Oh, really? Well, thanks! People don't normally complimint me. Do you really think I look cute?"
            $ the_person.draw_person(position = "back_peek")
            "[the_person.possessive_title] turns around, letting you get a look at her full outfit."
            $ the_person.draw_person()
            mc.name "You're more than cute. You're stunning."
            the_person.char "I... Thank you [the_person.mc_title]. That's really nice of you to say."
    return

label introvert_flirt_response_high(the_person):
    if mc.location.get_person_count() > 1 and the_person.effective_sluttiness("kissing") < (25 - (5*the_person.get_opinion_score("public_sex"))): # There are other people here, if she's not slutty she asks if you want to find somewhere quiet
        "[the_person.possessive_title] blushes and glances around nervously."
        the_person.char "[the_person.mc_title], someone is going to hear you!"
        menu:
            "Find someplace quiet.":
                mc.name "Alright, let's find somewhere nobody will hear us."
                the_person.char "I don't know if we should..."
                "You take her hand and lead her gently. After a moment of hesitation she follows behind you."
                "After searching for a couple of minutes you find a quiet space for just the two of you. Her cheeks are red when you turn back to her."
                the_person.char "So... What do you want to do now?"
                if the_person.has_taboo("kissing"):
                    "You step close and put your arms around her waist."
                    $ the_person.call_dialogue("kissing_taboo_break")
                    $ the_person.break_taboo("kissing")
                else:
                    "You step close and put your arms around her waist. She closes her eyes, sighs happily, and waits for you to kiss her."
                "You lean forward and press your lips against hers. [the_person.possessive_title] responds, leaning her body against yours."
                call fuck_person(the_person, private = True, start_position = kissing, skip_intro = True) from _call_fuck_person_57

            "Just flirt.":
                mc.name "So if it wasn't for the audience I'd have you naked by now? That's good to know."
                "She slaps your shoulder playfully and smiles."
                the_person.char "Oh my god, you're the worst! Obviously you would have to buy me dinner too."

    else: # She wants to kiss you, leading to other things.
        if mc.location.get_person_count() == 1:  #You're alone, so she was just shy
            "[the_person.possessive_title] glances around."
            the_person.char "Well it's just the two of us here... Maybe we could just... see where things go..."
            "She steps close to you and nervously holds your hand."
        else:  #She's slutty AND you're all alone.
            "[the_person.possessive_title] doesn't say anything for a moment. Her eyes run up and down your body, taking you in."
            the_person.char "Do you want to find out?"
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

            "Just flirt.":
                $ the_person.draw_person()
                mc.name "I do, but you'll have to wait until later."
                the_person.char "Are you sure?"
                "You nod and [the_person.title] sighs, obviously disappointed."
                the_person.char "Okay, maybe later then."
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
            the_person.char "Mmm. Thank you."
        else:
            the_person.char "Mmm."
    else:
        if the_person.sluttiness > 80:
            the_person.char "Mmm, you taste great."
        else:
            the_person.char "Ugh."
    return

label introvert_cum_vagina(the_person):
    if mc.condom:
        if the_person.sluttiness > 75 or the_person.get_opinion_score("creampies") > 0:
            the_person.char "There's so much cum... Wow."
        else:
            the_person.char "Do you always cum this much?"

    else:
        if the_person.sluttiness > 75 or the_person.get_opinion_score("creampies") > 0:
            if the_person.relationship != "Single":
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person.char "Mmmm, I like having your cum in me. It's almost worth having to explain to my [so_title] how I got pregnant."

            else:
                the_person.char "How easily do you think I'd get pregnant? Maybe you just did."
                "She sighs and shrugs."
        else:
            if the_person.relationship != "Single":
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person.char "Oh shit, wait, what if I get pregnant?"
                the_person.char "I would have to explain to my [so_title] how I got pregnant. I don't want to have to do that!"

            else:
                the_person.char "Uh, please try not to get me pregnant, okay?"
    return

label introvert_cum_anal(the_person):
    if the_person.sluttiness > 75 or the_person.get_opinion_score("anal creampies") > 0:
        the_person.char "Cum inside of me, I want it!"
    else:
        the_person.char "Ah!"
    return

label introvert_suprised_exclaim(the_person):
    $rando = renpy.random.choice(["Fuck!","Shit!","Oh fuck!","Dicks!", "Fuck me!","Ah! Oh fuck!", "Ah!", "Holy shit!", "Fucking shit!", "God fucking dammit!", "Son of a bitch!", "Mother fucker!"])
    the_person.char "[rando]"
    return

label introvert_talk_busy(the_person):
    if the_person.obedience > 120:
        the_person.char "I'm busy right now. Can we talk later?"
    else:
        the_person.char "Huh? Sorry, I can't talk right now."
    return

label introvert_sex_strip(the_person):
    if the_person.sluttiness < 20:
        if the_person.arousal < 50:
            the_person.char "Don't stare at me, okay?"
        else:
            the_person.char "Ah... Don't look, okay?"

    elif the_person.sluttiness < 50:
        if the_person.arousal < 50:
            the_person.char "Look away for a second..."

    #If she's slutty she just does it without talking

    return

label introvert_sex_watch(the_person, the_sex_person, the_position):
    if the_person.sluttiness < the_position.slut_requirement - 20:
        $ the_person.draw_person(emotion = "angry")
        the_person.char "What the fuck..."
        $ the_person.change_obedience(-2)
        $ the_person.change_happiness(-3)
        "[the_person.title] shakes her head while you and [the_sex_person.name] [the_position.verb]."

    elif the_person.sluttiness < the_position.slut_requirement - 10:
        $ the_person.draw_person()
        the_person.char "Right here? Really?"
        $ the_person.change_happiness(-1)
        "[the_person.title] rolls her eyes and tries to avert her gaze as you and [the_sex_person.name] [the_position.verb]."

    elif the_person.sluttiness < the_position.slut_requirement:
        $ the_person.draw_person()
        the_person.char "Right in front of me? Really?"
        $ change_report = the_person.change_slut_temp(1)
        "[the_person.title] watches for a moment, then turns away while you and [the_sex_person.name] keep [the_position.verb]."

    elif the_person.sluttiness > the_position.slut_requirement and the_person.sluttiness < the_position.slut_cap:
        $ the_person.draw_person()
        $ change_report = the_person.change_slut_temp(2)
        "[the_person.title] blushes, watching you and [the_sex_person.name] [the_position.verb]."

    else:
        $ the_person.draw_person(emotion = "happy")
        # the_person.char "Come on [the_person.mc_title], [the_sex_person.name] is going to fall asleep at this rate! You're going to have to give her a little more than that."
        "[the_person.title] watches excitedly while you and [the_sex_person.name] [the_position.verb]. She whispers under her breath, almost to herself."
        the_person.char "Come on, give it to her. Harder..."
    return

label introvert_being_watched(the_person, the_watcher, the_position):
    if the_person.sluttiness >= the_position.slut_cap and the_watcher.sluttiness >= the_position.slut_cap:
        #They agree you should give it to her harder
        the_person.char "[the_person.mc_title], I want more!"
        $ the_person.change_arousal(1)
        "[the_person.title] seems turned on by [the_watcher.title] watching you and her [the_position.verb]."

    elif the_person.sluttiness >= the_position.slut_cap and the_watcher.sluttiness < the_position.slut_requirement:
        #She's super slutty and doesn't care what people think.
        the_person.char "Just focus on me. Just me."

    elif the_person.sluttiness >= the_position.slut_cap and the_watcher.sluttiness < the_position.slut_cap:
        #She's super slutty and encourages the watcher to be slutty.
        the_person.char "Did you know how good this feels [the_watcher.title]?"
        $ the_person.change_arousal(1)
        "[the_person.title] seems turned on by [the_watcher.title] watching you and her [the_position.verb]."

    elif the_person.sluttiness < the_position.slut_cap and the_watcher.sluttiness >= the_position.slut_cap:
        #She's into it and encouraged by the slut watching her.
        $ the_person.change_arousal(1)
        "[the_person.title] doesn't say anything, but she seems turned on by [the_watcher.title] watching you and her [the_position.verb]."

    elif the_person.sluttiness < the_position.slut_cap and the_watcher.sluttiness < the_position.slut_requirement:
        #She's into it but shamed by the prude watching her.
        the_person.char "We should go somewhere quiet..."
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
    if the_person.relationship == "Single":
        if the_person.sluttiness > the_person.love:
            if the_person.sluttiness > 40:
                the_person.char "I want you to come home with me. Want to come?"
            else:
                the_person.char "I don't normally do this. Do you want to come home with me?"
        else:
            if the_person.love > 40:
                "[the_person.title] stays close to you, before touching your arm to get your attention."
                the_person.char "I had a really good time. I... was wondering if you wanted to come home with me..."
            else:
                "[the_person.title] wrings her hands together nerviously, as if working up the courage to speak."
                the_person.char "I like you, and I want you to come home with me so I don't have to say goodbye. Do you... want to?"
    else:
        $ so_title = SO_relationship_to_title(the_person.relationship)
        if the_person.sluttiness > the_person.love:
            if the_person.sluttiness > 40:
                the_person.char "My [so_title] isn't around. Do you want to come home with me?"
            else:
                the_person.char "I know my [so_title] wouldn't like this, but do you want to come home with me? He won't be around."
        else:
            if the_person.love > 40:
                "[the_person.title] stays close to you, before touching your arm to get your attention."
                the_person.char "My [so_title] is never around. Do you want to come home with me? I would be happy if you did..."
            else:
                "[the_person.title] wrings her hands together nerviously, as if working up the courage to speak."
                the_person.char "I really like you. I have a [so_title], but I want to spend more time with you too."
                the_person.char "Do you... want to come home with me? He won't be around."
    return

label introvert_sex_end_early(the_person):
    if the_person.sluttiness > 50:
        if the_person.love > 40:
            if the_person.arousal > 60:
                the_person.char "You're done? I was hoping you'd at least help me cum."
            else:
                the_person.char "All done? I thought this was going somewhere."
        else:
            if the_person.arousal > 60:
                the_person.char "Fuck, I was hoping you'd make me cum."
            else:
                "[the_person.title] stays silent but seems dissapointed that you're finishing up early."

    else:
        if the_person.love > 40:
            if the_person.arousal > 60:
                the_person.char "Done? I hope it wasn't something I did, I was having a really good time..."
            else:
                the_person.char "Done? I hope it wasn't something I did wrong."
        else:
            if the_person.arousal > 60:
                "[the_person.title] stays silent, but her cheeks are flush and her breathing is heavier than normal."
            else:
                "[the_person.title] stays silent but seems glad that you're finishing up early."
    return


label introvert_sex_take_control (the_person):
    if the_person.arousal > 60:
        "[the_person.title] grabs your arm and moans aggressively."
        the_person.char "No, I'm not done yet!"
    else:
        the_person.char "You're staying here, I was just getting started!"
    return

label introvert_sex_beg_finish(the_person):
    "[the_person.title] grabs your arm and moans desperately."
    the_person.char "No, please I'm so close to cumming! I... I need you to keep going!"
    return

## Role Specific Section ##
label introvert_improved_serum_unlock(the_person):
    mc.name "[the_person.title], now that you've had some time in the lab there's something I wanted to talk to you about."
    "[the_person.title] nods and listens."
    mc.name "All of our research and development up until this point has been based on the limited notes I have from my university days. I'm sure there's more we could learn, and I want you to look into it for me."
    "[the_person.title] thinks about it, then nods again."
    the_person.char "Well, I may have an idea. I think it could lead to a breakthrough."
    mc.name "Go on."
    the_person.char "Our testing procedures focus on human safety. If we put that to the side we could gain much more information about the subjective effects of our serum."
    the_person.char "I want to do is take a dose of our serum myself. I would need you to record me and ask me some questions."
    return

## Taboo break dialogue ##
label introvert_kissing_taboo_break(the_person):
    if the_person.effective_sluttiness() >= 30:
        the_person.char "Well? What are you waiting for? Kiss me."
    elif the_person.love >= 20:
        the_person.char "So we're really going to do this?"
        mc.name "I think so."
        the_person.char "Well then... Don't just stand there."
    else:
        the_person.char "Are you sure about this? I don't know if..."
        mc.name "I'm sure. Just relax and enjoy yourself."
    return

label introvert_touching_body_taboo_break(the_person):
    if the_person.effective_sluttiness() >= 30:
        the_person.char "Does touching me turn you on, or is it just me?"
    elif the_person.love >= 20:
        the_person.char "Be gentle, I'm a little ticklish. Okay"
        mc.name "I'll be gentle, don't worry."
    else:
        the_person.char "I... I don't know if we should be doing this [the_person.mc_title]. We barely know each other..."
        mc.name "What better way to start then? You have a fantastic body."
        the_person.char "I... I mean..."
    return

label introvert_touching_penis_taboo_break(the_person):
    if the_person.effective_sluttiness() >= 35:
        the_person.char "Your cock looks so big when it's hard. It's just like I always dreamed it would be."
        mc.name "Go ahead and touch it. I bet it feels like you dreamed too."
    elif the_person.love >= 20:
        the_person.char "Well, I guess you're ready. Look at how big your cock is..."
        mc.name "Don't leave me waiting, you know how badly I want you to touch it."
    else:
        the_person.char "You're so big... Is it always that big when you're hard?"
        mc.name "Only when I'm really turned on."
        the_person.char "I don't know if I should go any closer... You might pop."
        mc.name "It's going to take a little more than that to get me to pop. Put your hand on it."
    return

label introvert_touching_vagina_taboo_break(the_person):
    if the_person.effective_sluttiness() >= 35:
        the_person.char "Mmm... Touch me [the_person.mc_title], I'm ready."
    elif the_person.love >= 20:
        the_person.char "I think I'm ready, but please be gentle with me [the_person.mc_title]."
        mc.name "Don't worry, I'll be gentle."
    else:
        the_person.char "Oh my god, I'm really about to let you... Oh my god."
        mc.name "Just relax, you'll enjoy yourself more."
    return

label introvert_sucking_cock_taboo_break(the_person):
    mc.name "I want you to do something for me."
    the_person.char "What?"
    mc.name "I want you to suck on my cock."
    if the_person.effective_sluttiness() >= 45:
        the_person.char "I was wondering when you would ask. Okay, I'll give it a try."
    elif the_person.love >= 30:
        the_person.char "Oh... I guess for you I can give it a try."
    else:
        the_person.char "You want me to suck... your cock? I don't know, we've never done anything like that."
        mc.name "Just the tip, just for a little bit. It would feel so good."
        "She bites her lip and seems indecisive, but you watch her resolve break down."
        the_person.char "Okay, I'll give it a try."
    return

label introvert_licking_pussy_taboo_break(the_person):
    mc.name "I want to taste your pussy [the_person.title]. Are you ready?"
    if the_person.effective_sluttiness() >= 45:
        the_person.char "You're really going to... Oh my god, yes, I'm ready!"
    elif the_person.love >= 30:
        the_person.char "You don't have to if you don't want to, you know. I don't mind."
        mc.name "Of course I want to. Now just relax and enjoy."
    else:
        if the_person.has_taboo("sucking_cock"):
            the_person.char "I... I think I am. I'm just a bit nervous."
            mc.name "Just relax and enjoy yourself. I'll make sure you feel really good."
        else:
            the_person.char "I... I am if you are. I know I sucked your cock, but you don't have to do this if you don't want to."
            mc.name "I do want to. Just relax and enjoy yourself."
        "She laughs self-consciously and nods."
        the_person.char "Okay, I'll try."
    return

label introvert_vaginal_sex_taboo_break(the_person):
    if the_person.effective_sluttiness() >= 60:
        the_person.char "Do it [the_person.mc_title], I want to feel you inside me."
    elif the_person.love >= 45:
        the_person.char "I think I'm ready [the_person.mc_title]. I want to feel even closer to you."
    else:
        if the_person.has_taboo("anal_sex"):
            the_person.char "Oh no, I'm so nervous!"
            mc.name "Don't be, I'll be gentle."
            the_person.char "You don't think... I'm a slut or something, do you?"
            menu:
                "Of course you are.":
                    if mc.condom:
                        mc.name "Of course I do. You're about to let me fuck your sweet little pussy."
                    else:
                        mc.name "Of course I do. You're about to let me fuck your pussy raw."
                    mc.name "You're a dirty little slut, but there's nothing wrong with that. You just have to embrace it."
                    "She nods."
                    $ the_person.change_slut_temp(1 + the_person.get_opinion_score("being_submissive"))
                    the_person.char "I think I've known that deep down for a while..."

                "Of course not.":
                    mc.name "Of course not. You're just doing what you want to do to be happy."
                    mc.name "Never let anyone tell you what should make you happy."
                    $ the_person.change_happiness(2)
                    "She smiles and nods."
                    the_person.char "Thank you. I've been feeling so unsure lately."
        else:
            the_person.char "You've fucked my ass, now tell me how my pussy feels."
    return

label introvert_anal_sex_taboo_break(the_person):
    if the_person.effective_sluttiness() >= 75:
        the_person.char "Oh fuck, you look so much bigger than any of the toys I've fit inside my ass before..."
        mc.name "Don't worry, I'll stretch you out just fine."
        "The thought seems to turn her on more than scare her."
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

label introvert_condomless_sex_taboo_break(the_person):
    if the_person.get_opinion_score("bareback sex") > 0:
        the_person.char "You want to fuck me raw? Fuck... That's so hot."
        if the_person.get_opinion_score("creampies") > 0:
            the_person.char "I should really tell you to pull out when you cum..."
            mc.name "{i}Are{/i} you telling me I should pull out?"
            "She bites her lip and shakes her head."
            the_person.char "No, I'm not."
        elif the_person.get_opinion_score("creampies") < 0:
            the_person.char "You'll need to pull out though. There's no way in hell I want you to cum inside me."
        else:
            the_person.char "You'll need to pull out though, okay? You really shouldn't cum inside me right now."

    elif the_person.love > 60:
        the_person.char "Okay... I want to feel close to you too [the_person.mc_title]."
        if the_person.get_opinion_score("creampies") > 0:
            the_person.char "If we're doing this, I don't want you to pull out when you finish either."
            mc.name "Are you on the pill?"
            "She shakes her head."
            the_person.char "No, but I know that whatever happens we will be together."
        elif the_person.get_opinion_score("creampies") < 0:
            the_person.char "You'll need to pull out though. I don't want you to get me pregnant, okay?"
        else:
            the_person.char "You'll need to pull out though, okay? I don't think either of us want me to get pregnant yet."

    else:
        the_person.char "You want to do me raw? That's so risky though!"
        if the_person.has_taboo("vaginal_sex"):
            mc.name "I want our first time to be special though, don't you?"
            the_person.char "I... Fine, but just please don't cum in me right away, okay?"
        else:
            mc.name "It'll feel so much better though. Didn't you hate how the condom felt last time?"
            the_person.char "I did kind of want to know what it was like without it..."
            the_person.char "Fine, but just please don't cum in me right away, okay?"
    return

label introvert_underwear_nudity_taboo_break(the_person, the_clothing):
    if the_person.effective_sluttiness() > 30 - (the_person.get_opinion_score("skimpy outfits") * 5):
        the_person.char "This is going to be the first time you've seen me in my underwear. Are you excited [the_person.mc_title]?"
        if the_person.has_taboo(["bare_tits","bare_pussy"]):
            mc.name "I am, you aren't going to make me wait, are you?"
            "She bite her lip and shakes her head."
            the_person.char "No, I'm not that mean. Go ahead, take it off."
        else:
            mc.name "I've already seen everything you're hiding under there, but I'd like to see it all again."
            the_person.char "No point in being shy then. Go ahead, take it off."

    elif the_person.love > 15:
        the_person.char "This is going to be the first time you've seen me in my underwear, isn't it [the_person.mc_title]?"
        "She laughs awkwardly."
        the_person.char "Are you excited?"
        if the_person.has_taboo(["bare_tits","bare_pussy"]):
            mc.name "I am. You aren't going to make me wait, are you?"
            "She shakes her head and you start to strip her down."

        else:
            mc.name "I've already seen everything you're hiding under there, but I like to see it anyways."
            the_person.char "Oh yeah, I guess you have. Well, no point being shy then."

    else:
        the_person.char "If I take off my [the_clothing.display_name] I'll just be wearing my underwear."
        mc.name "So?"
        the_person.char "It feels like we barely know each other, but I'm about to be half naked in front of you."
        if the_person.has_taboo(["bare_tits","bare_pussy"]):
            mc.name "You're not going to be any amount of naked if you keep worrying about it. Come on, let's take it off."
            "She nods obediently."
        else:
            mc.name "I've already seen you naked, so what's the big deal?"
            the_person.char "I guess you're right, I'm getting worked up over nothing."
    return

label introvert_bare_tits_taboo_break(the_person, the_clothing):
    if the_person.effective_sluttiness() > (40 - the_person.get_opinion_score("showing her tits") * 5):
        the_person.char "You want get a look at my tits [the_person.mc_title]? You're going to make me blush."
        if the_person.has_large_tits():
            "She shakes her chest for you, jiggling the large tits hidden underneath her [the_clothing.display_name]."
        else:
            "She shakes her chest and gives her small tits a little jiggle."

        mc.name "Of course I want to see them. Let's get that [the_clothing.display_name] off so I can finally see them."

    elif the_person.love > 25:
        the_person.char "So you want to see my... breasts?"
        if the_person.has_large_tits():
            "She looks down at her own sizeable chest, tits hidden beneath her [the_clothing.display_name]."
            the_person.char "I guess I can understand why. I'm a little shy though..."
        else:
            the_person.char "I'm a little shy about them, I wish they were bigger."
        mc.name "Don't be shy, just relax and let me take this off for you."

    else:
        the_person.char "Wait! If you take off my [the_clothing.display_name] my ti... breasts will be out!"
        mc.name "And what's wrong with that?"
        the_person.char "I don't normally do anything like this. I'm not the kind of girl to pull her... breasts out for someone."
        if the_person.has_large_tits():
            the_person.char "Plus they're always attracting attention, so I've gotten so use to covering them up."

        mc.name "You aren't really worried about that though, are you? Come on, I want to see your tits."
        "She takes a deep breath, then nods."
        the_person.char "Okay..."
    return

label introvert_bare_pussy_taboo_break(the_person, the_clothing):
    if the_person.effective_sluttiness() > (50 - the_person.get_opinion_score("showing her ass") * 5):
        the_person.char "Oh, you finally want to see what's going on down there? It's about time!"

    elif the_person.love > 35:
        the_person.char "Oh! If you take that off you're going to see my... You know."
        mc.name "That's the plan. Is there a problem with that?"
        the_person.char "No, I guess not. I just feel a little self concious about getting naked like this."
        if the_person.has_taboo("touching_vagina"):
            mc.name "Just take a deep breath and relax. You trust me, right?"
            the_person.char "Of course I do [the_person.mc_title]. Okay, go ahead..."

        else:
            mc.name "You've already let me feel your pussy, so what's wrong with taking a little look?"
            the_person.char "I guess you're right. Okay, go ahead..."

    else:
        the_person.char "Wait! If you take that off you'll be able to see my pussy."
        if the_person.has_taboo("touching_vagina"):
            mc.name "That's the point, yeah. What's wrong?"
        else:
            mc.name "You've already let me feel it, so what's the issue?"

        the_person.char "I... I don't know, I'm just nervous!"
        mc.name "Just take a deep breath and relax while I get these [the_clothing.display_name] off of you."
    return

label introvert_facial_cum_taboo_break(the_person):

    return

label introvert_mouth_cum_taboo_break(the_person):

    return

label introvert_body_cum_taboo_break(the_person):

    return

label introvert_creampie_taboo_break(the_person):

    return

label introvert_anal_creampie_taboo_break(the_person):

    return
