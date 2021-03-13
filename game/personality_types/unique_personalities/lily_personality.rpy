### PERSONALITY CHARACTERISTICS ###
init 1300:
    python:
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
        titles_function = lily_titles, possessive_titles_function = lily_possessive_titles, player_titles_function = lily_player_titles,
        insta_chance = 0, dikdok_chance = 0)

### DIALOGUE ###
label lily_sex_review(the_person, the_report):
    $ used_obedience = the_report.get("obedience_used", False) #True if a girl only tried a position because you ordered her to.
    $ comment_position = the_person.pick_position_comment(the_report)

    if comment_position is None:
        return #You didn't actually do anything, no need to comment.

    #She's worried about her SO finding out because it was in public
    if the_report.get("was_public", False) and the_person.relationship != "Single" and the_person.get_opinion_score("cheating on men") <= 0: #It was public and she cares.
        $ so_title = SO_relationship_to_title(the_person.relationship)
        if the_person.has_role(affair_role): #Dialogue about her being into it, but you can't do this in case she gets caught. #NOTE: Shouldn't currently be possible, but might be useful for mods/ updates
            the_person "[the_person.mc_title], we need to be more sneaky next time. What do I tell my [so_title] if someone tells him about this?"
            mc.name "Don't worry, nobody knows who we are and nobody is going to tell your [so_title]."
            "[the_person.possessive_title] seems unconvinced, but nods anyways."
        elif used_obedience:
            the_person "I can't believe you made me do that right here... What if people recognise us [the_person.mc_title]?"
            the_person "How would I explain any of this to my [so_title] if they tell him?"
            mc.name "Don't worry, nobody knows who we are and nobody is going to tell your [so_title]."
            "[the_person.possessive_title] seems unconvinced, but nods anyways."

        else:
            the_person "We should have found somewhere else, people are looking at us now... What if someone recognises us?"
            mc.name "Nobody knows who we are, and nobody really cares anyways. Just relax, everything's alright."
            "[the_person.possessive_title] seems unconvinced, but nods anyways."

    #She's single, but worried that you did in public.
    elif the_report.get("was_public", False) and (the_person.effective_sluttiness()+10*the_person.get_opinion_score("public sex") < comment_position.slut_cap):
        if used_obedience:
            the_person "I can't believe you made me do that right here... What if people recognise us [the_person.mc_title]?"
            mc.name "Don't worry, nobody knows who you are, and nobody cares what we do together. Just relax, everything's alright."
            "[the_person.possessive_title] seems unconvinced, but nods anyways."

        else:
            the_person "We really should have found somewhere private, I don't know what I was thinking..."
            the_person "What if someone recognises us? [mom.title] could find out!"
            mc.name "Relax, [mom.title] isn't going to find out. Nobody here knows who you are, and nobody cares what we do together."
            "[the_person.possessive_title] seems unconvinced, but nods anyways."

    #No special conditions, just respond based on how orgasmed and how slutty the position was.
    elif the_report.get("girl orgasms", 0) > 0 and the_report.get("guy orgasms", 0) > 0: #You both came
        if the_person.effective_sluttiness() > comment_position.slut_cap: #She's sluttier than the position cap, it was tame
            the_person "That was fun [the_person.mc_title], but don't you think that next time we could..."
            "She hesitates, obviously still a little embarrassed."
            the_person "Uh... Go a little furthur? I think that could be even better."

        elif the_person.effective_sluttiness() > comment_position.slut_requirement: #She thought it was fun/exciting
            the_person "Oh my god, that was fun [the_person.mc_title]! Whew, I think I need to sit down."
            "She gives you a dopey smile, still reeling from her climax."

        elif used_obedience: #She only did it because she was commanded
            "[the_person.possessive_title] looks away, embarrassed by what you've just done."
            the_person "Are we finished?"
            mc.name "Don't act so innocent [the_person.title], you obviously had a great time."
            mc.name "Did you know you look really cute when you cum?"
            the_person "It was... nice, I guess. Can we just talk about something other than me touching my own brother, please?"

        else: # She's suprised she even tried that.
            the_person "Oh wow, that was... I can't believe we just did that."
            "She seems dazed by her orgasm as she struggles to put full sentences together."
            the_person "We shouldn't have done that... But it felt really good."

    elif the_report.get("girl orgasms", 0) > 0: #Only she came
        if the_person.effective_sluttiness() > comment_position.slut_cap: #She's sluttier than the position
            the_person "Is that all? I mean, I had a great time, but you should get to cum too."
            mc.name "Maybe next time, making you feel good was fun enough."
            the_person "Well, maybe we can go even furthur next time, alright? I've got some fun ideas for both of us."
            "She gives you a dirty smile, already imagining your next encounter."

        elif the_person.effective_sluttiness() > comment_position.slut_requirement: #She thought it was fun/exciting
            the_person "Don't you want to finish too? I had a great time, it's only fair..."
            mc.name "Maybe next time. Watching you cum is all I really wanted."
            the_person "Well, it was amazing. Ah..."
            "She gives you a dopey smile, still riding the chemical high of her orgasm."

        elif used_obedience: #She only did it because she was commanded
            "[the_person.possessive_title] looks away, embarrassed by what she's done with you."
            the_person "Is that it? Did you really just want to make me... climax?"
            mc.name "Yeah, that's all for now. You look really cute when you cum, did you know that?"
            "She blushes more intensely, still avoiding making eye contact."
            the_person "Thanks, I guess... Can we talk about something else now?"

        else: # She's suprised she even tried that.
            the_person "Oh my god, that was intense! I... don't think we should have done that though."
            mc.name "Why not? Obviously you enjoyed yourself."
            the_person "Yeah, but it's wrong, isn't it? Whatever, it's happened now..."

    elif the_report.get("guy orgasms", 0) > 0: #Only you came
        if the_person.effective_sluttiness() > comment_position.slut_cap: #She's sluttier than the position
            the_person "I hope that was everything you wanted it to be [the_person.mc_title]."
            the_person "But I think we could take it a little furthur next time, if you want. I can think of a bunch of fun things for us to try."
            the_person "Just something for you to keep in mind, okay?"

        elif the_person.effective_sluttiness() > comment_position.slut_requirement: #She thought it was fun/exciting
            the_person "All done then, huh?"
            "She seems a little disappointed, but is trying to hide it."
            the_person "Maybe, uh... You could make me cum too next time?"
            mc.name "Yeah, sure thing [the_person.title]."

        elif used_obedience: #She only did it because she was commanded
            the_person "We're done then?"
            "[the_person.possessive_title] avoids making eye contact with you, obviously embarrassed."
            mc.name "Yeah, we're all done for now. Thanks [the_person.title], that felt great."
            the_person "I... Good, I'm glad you liked it."

        else:  # She's suprised she even tried that.
            the_person "We're done? I mean, I hope that felt good for you."
            "She laughs nervously, trying to hide her embarrassment."
            the_person "I think we took things a little too far, though. It got kind of crazy, huh?"
            the_person "Whatever, let's just talk about something else..."

    else: #Nobody came.
        if the_person.effective_sluttiness() > comment_position.slut_cap: #She's sluttier than the position
            the_person "Done already? But we just barely started!"
            the_person "Well... I guess you'll have to make it up to me later, okay?"

        elif the_person.effective_sluttiness() > comment_position.slut_requirement: #She thought it was fun/exciting
            the_person "You're tired out already? Aww, but I was just starting to have fun!"
            "[the_person.possessive_title] seems a little disappointed."

        elif used_obedience: #She only did it because she was commanded
            the_person "You're done? But you didn't... climax."
            "She looks away, suddenly embarrassed."
            the_person "Never mind, it doesn't matter. Let's just talk about something else, this is getting awkward."

        else:  # She's suprised she even tried that.
            the_person "Oh my god, you're totally right. I don't know what I was thinking, agreeing to that..."
            "She laughs nervously, trying to hide her embarrassment."
            the_person "Let's not tell [mom.title] about this, obviously."
    return

label lily_greetings(the_person):
    if the_person.love < 0:
        the_person "Ugh, can you tell Mom whatever you want to say to me right now? I don't want to hear it."
    elif the_person.happiness < 90:
        the_person "Hey [the_person.mc_title]..."
    else:
        if the_person.obedience > 130:
            if the_person.sluttiness > 60:
                the_person "Hey [the_person.mc_title], do you need your little sister for something?"
                "[the_person.title] crosses her arms behind her back."
            else:
                the_person "Hi [the_person.mc_title]."
        else:
            if the_person.sluttiness > 60:
                the_person "Oh hey [the_person.mc_title], I was just thinking about you."
                "[the_person.title] smiles playfully."
            else:
                the_person "Hey, need something?"
    return

label lily_sex_responses_foreplay(the_person):
    if the_person.arousal < 25:
        if the_person.sluttiness > 50:
            the_person "Are you trying to get me turned on? Because it might be working..."
        else:
            the_person "[the_person.mc_title], maybe we should stop before we get too excited..."
            "She moans happily, obviously not interested in taking her own advice."

    elif the_person.arousal < 50:
        if the_person.sluttiness > 50:
            the_person "Fuck, that feels good... Do it again."
        else:
            the_person "Oh my god... Where did you learn how to do this? You're so good at it..."

    elif the_person.arousal < 75:
        if the_person.sluttiness > 50:
            if the_person.outfit.wearing_panties():
                the_person "Ah... If you get me any wetter I'm going to soak right through my panties [the_person.mc_title]."
            elif the_person.outfit.vagina_available():
                the_person "Fuck, you're getting me so wet [the_person.mc_title]! I can feel it dripping down my thighs..."
            else:
                $ item_name = the_person.outfit.get_lower_top_layer().display_name
                the_person "Fuck, you're getting me so wet I'm going to soak right through my [item_name]..."
        else:
            the_person "I can't believe my own brother is getting me so wet. It feels so good [the_person.mc_title]."

    else:
        if the_person.sluttiness > 50:
            the_person "[the_person.mc_name], do you want to make me cum? Keep going!"
        else:
            the_person "Oh god, I feel strange, I think... I think you're going to make me cum soon!"

    return

label lily_sex_responses_oral(the_person):
    if the_person.arousal < 25:
        if the_person.sluttiness > 50:
            the_person "Oh god, you're such a good big brother..."
            "[the_person.possessive_title] sighs happily."
        else:
            the_person "Oh god, ah! Ah..."
            "[the_person.title] tries and fails to stiffle her moans."

    elif the_person.arousal < 50:
        if the_person.sluttiness > 50:
            the_person "Mmm, that feels so good [the_person.mc_title], you're amazing!"
        else:
            the_person "Where.... Mmmm.... Where did you learn to do this? You're so good at it!"

    elif the_person.arousal < 75:
        if the_person.sluttiness > 50:
            the_person "How does my pussy taste [the_person.mc_title]? Do you like eatting me out?"
            "You respond by making her moan even louder."
            the_person "Oh fuck..."

        else:
            the_person "My own brother is really licking my pussy! It's fucked up, but you've got me so turned on!"
    else:
        if the_person.sluttiness > 50:
            the_person "Fuck, keep licking my clit like that and you're going to make me cum!"

        else:
            the_person "Oh god, I think... I think I'm going to cum soon [the_person.mc_title]!"
            the_person "Ah! Mmmm!"
    return

label lily_sex_responses_vaginal(the_person):
    if the_person.arousal < 25:
        if the_person.sluttiness > 50:
            the_person "Oh god, you're cock feel so good inside me..."
            "She moans happily to herself."
        else:
            the_person "You're so big, is it even all in yet? Ah..."

    elif the_person.arousal < 50:
        if the_person.sluttiness > 50:
            the_person "Fuck... Ah..."
        else:
            the_person "Oh my god, that feeling..."

    elif the_person.arousal < 75:
        if the_person.sluttiness > 50:
            "Mmm, give it to me [the_person.mc_title]! Stretch out my teen pussy so it will only fit your big, hot cock!"

        else:
            "[the_person.possessive_title] moans enthusiastically."
            the_person "Fuck, right there! Keep fucking me like that!"
    else:
        if the_person.sluttiness > 50:
            the_person "I'm getting close, I'm going to cum soon..."
            "She moans, almost pleadingly."
            the_person "Make me cum! Make your little sister cum on your dick!"
        else:
            "[the_person.possessive_title] mumbles softly to herself between happy moans."
            the_person "Oh fuck, I'm going to cum... I'm going to cum on my brothers cock... Oh fuck!"

    return

label lily_sex_responses_anal(the_person):
    if the_person.arousal < 25:
        if the_person.sluttiness > 50:
            the_person "Fuck, I can feel you stretching me out..."
        else:
            the_person "Oh fuck, I don't know if I can do this... It feels like you're tearing me in half!"

    elif the_person.arousal < 50:
        if the_person.sluttiness > 50:
            the_person "Ah! Ah! I can take it, don't hold back! Ah!"
        else:
            "[the_person.title] growls defiantly."
            the_person "Fuuuuuuuck!"

    elif the_person.arousal < 75:
        if the_person.sluttiness > 50:
            the_person "Your cock is so big, it feels like you're moulding me to it!"
        else:
            the_person "I think you're starting to stretch me out, I'm starting to..."
            "She moans loudly."
            the_person "... enjoy this!"
    else:
        if the_person.sluttiness > 50:
            the_person "Fuck, I think... I think I'm going to cum soon!"
            the_person "Stuff me full of your big cock [the_person.mc_title]! Make your sister cum like a desperate anal slut!"
        else:
            the_person "Oh god, I'm... I think I'm going to cum soon!"
            the_person "I can't belive... My brother's cock is in my ass and it's going to make me cum! I feel like such a slut!"
            "The way she's moaning makes her sound more proud than ashamed."
    return

label lily_clothing_accept(the_person):
    if the_person.obedience > 140:
        the_person "You're right, that looks cute! I'm glad I've got a brother with good fashion sense!"
    else:
        the_person "You think this would look good on me? I'll keep that in mind!"
    return

label lily_clothing_reject(the_person):
    if the_person.obedience > 140:
        the_person "Oh, I wish I could wear this [the_person.mc_title], but I don't think I could ever explain it to Mom if she saw."
    else:
        if the_person.sluttiness > 60:
            the_person "Oh my god [the_person.mc_title]... It's hot, but there's no way I could ever actually wear it!"
        else:
            the_person "Oh my god [the_person.mc_title], you perv. There's no way I'm going to wear something like that!"
    return

label lily_clothing_review(the_person):
    if the_person.obedience > 130:
        the_person "Sorry [the_person.mc_title], I should really get myself dressed properly again! Just a second!"
    else:
        if the_person.sluttiness > 50:
            the_person "You shouldn't be looking at your sister like that [the_person.mc_title]. I'll get dressed so you won't be so distracted."
        else:
            the_person "Oh my god, I shouldn't be dressed like this around my own brother. Just... Just look away and give me a moment."
    return

label lily_strip_reject(the_person, the_clothing, strip_type = "Full"):
    if the_person.obedience > 130:
        the_person "I wish I could let you, but I don't think I should be taking off my [the_clothing.display_name] in front of my brother."
    elif the_person.obedience < 70:
        the_person "Sorry [the_person.mc_title], your little sister likes being a tease. I'm going to keem my [the_clothing.display_name] on for a little bit longer."
    else:
        the_person "I couldn't take off my [the_clothing.display_name] in front of you [the_person.mc_title]. You're my brother, I'd die of embarrassment!"
    return

label lily_strip_obedience_accept(the_person, the_clothing, strip_type = "Full"):
    "[the_person.title] speaks up meekly as you start to move her [the_clothing.display_name]."
    if the_person.obedience > 130:
        the_person "Maybe you shouldn't..."
    else:
        if the_clothing.underwear:
            the_person "Wait, do you really want to take off my underwear? [the_person.mc_title], you shouldn't..."
        else:
            the_person "Wait, I don't know about this..."
    return

label lily_grope_body_reject(the_person):
    if the_person.effective_sluttiness("touching_body") < 5: #Fail point for touching shoulder
        the_person "Hey, what are you doing?"
        mc.name "I was just... going to give you a brotherly hug?"
        if the_person.love > 20:
            the_person "Aww, that's sweet."
            "She gives you a quick hug, then steps back and smiles."
            $ the_person.change_love(1) #Just cancels out the -1 Love you'd get otherwise.

        else:
            the_person "We're a little old for that, aren't we?"
            "She looks away awkwardly until you move your hand away."
            mc.name "Yeah, I guess you're right. Never mind."
    else: #Fail point for touching waist
        the_person "Could... You maybe move your hand [the_person.mc_title]?"
        mc.name "What? Why, is there something wrong?"
        the_person "It just feels weird, you know? I don't know, I can't really explain it."
        "She squirms uncomfortably until you move your hand back."
        mc.name "Sorry, don't worry about it [the_person.title]."
    return

label lily_sex_accept(the_person):
    if the_person.sluttiness > 70:
        if the_person.obedience < 100:
            the_person "You're definitely my brother, I was thinking the same thing."
        else:
            the_person "You want to do that with your little sister [the_person.mc_title]? Well, you're lucky I'm just as perverted."
    else:
        the_person "Okay, let's do it. Just make sure Mom never finds out, okay?"
    return

label lily_sex_obedience_accept(the_person):
    if the_person.sluttiness > 70:
        the_person "Oh god [the_person.mc_title], I know I shouldn't... We shouldn't be doing any of this together."
        the_person "But I just can't say no to you."
    else:
        if the_person.obedience > 130:
            the_person "If that's what my big brother needs me to do..."
        else:
            the_person "How do I keep letting you talk me into this? You're my brother for Gods sake..."
            "She seems conflicted for a second."
            the_person "Okay, just promise me Mom will never know."
    return

label lily_sex_gentle_reject(the_person):
    if the_person.sluttiness > 50:
        the_person "Not yet, I need to get warmed up first. Let's start out with something a little more tame."
    else:
        the_person "I... we can't do that [the_person.mc_title]. I'm your sister; there are lines we just shouldn't cross."
    return

label lily_sex_angry_reject(the_person):
    if the_person.sluttiness < 20:
        the_person "Oh my god, what? I'm your sister you fucking pervert, how could you even talk about that to me?"
        the_person "Even if you're joking that's just... it's just fucked up, okay?"
    else:
        the_person "What the fuck [the_person.mc_title], I'm your sister! How could you think that's okay?"
        the_person "I... Just get out of here. You're lucky I don't want to have to explain how this happened to Mom."
    return

label lily_seduction_response(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 50:
            the_person "What's up [the_person.mc_title]? Do you need your little sister to pay attention to you?"
        else:
            the_person "What're you thinking about? You look like you're up to something."
    else:
        if the_person.sluttiness > 50:
            the_person "Do you have something in mind for your innocent little sister?"
        elif the_person.sluttiness > 10:
            the_person "What do you mean [the_person.mc_title]? Do you want to do something together?"
        else:
            the_person "I... what do you mean [the_person.mc_title]?"
    return

label lily_seduction_accept_crowded(the_person):
    if the_person.sluttiness < 20:
        "[the_person.title] grabs your arm and blushes."
        the_person "Oh my god, you can't say things like that when there are other people around [the_person.mc_title]! let's at least find someplace quiet."

    elif the_person.sluttiness < 50:
        the_person "I... I mean, we shouldn't do anything like that when there are other people around. What would we do if people found out what we do together?"

    else:
        the_person "Oh god, that sounds so hot. I hope nobody here recognizes me!"
    return

label lily_seduction_accept_alone(the_person):
    if the_person.sluttiness < 20:
        the_person "Let's just make sure nobody finds out, okay? I mean, what would my friends think if I was doing... stuff with my brother?"
    elif the_person.sluttiness < 50:
        the_person "I know we shouldn't, but there's nobody around to know, right? So what's the harm..."
    else:
        the_person "God, you're such a pervert [the_person.mc_title], taking advantage of your poor, innocent sister..."
        "[the_person.title] winks at you and holds onto your arm."
    return

label lily_seduction_refuse(the_person):
    if the_person.sluttiness < 20:
        the_person "Ugh, I'm your sister [the_person.mc_title], how could you even suggest that? Gross..."

    elif the_person.sluttiness < 50:
        the_person "No, wait, we really shouldn't be doing this [the_person.mc_title]... What if Mom knew, or my friends knew?"
        the_person "It would be so embarrassing if they found out what we do sometimes."

    else:
        the_person "I'm sorry [the_person.mc_title], but I just don't feel like fooling around today, okay? I'm sure I'll find a way to make it up to you later."
    return

label lily_flirt_response(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 50:
            the_person "I know you're my brother, but it's still really hot to hear you say that."
        else:
            the_person "Stop it [the_person.mc_title], you're my brother and I know you're just flattering me."
    else:
        if the_person.sluttiness > 50:
            the_person "Don't forget I'm your sister [the_person.mc_title], don't get too carried away. But I guess looking doesn't hurt, right?"
            "[the_person.title] smiles at you and spins around, giving you a full look at her body."
        else:
            the_person "Are you really checking me out? I'm your sister [the_person.mc_title], that's a little weird."
            the_person "But, uh... it's still nice to hear."
    return

label lily_flirt_response_low(the_person):
    the_person "Thanks! It's a cute look, right?"
    $ the_person.draw_person(position = "walking_away")
    "[the_person.possessive_title] gives you a quick spin, showing off her body at the same time as her outfit."
    $ the_person.draw_person()
    if mom.judge_outfit(the_person.outfit, 5, use_taboos = False): # Mom is sluttier or similar
        the_person "[mom.title] helped me pick it out. You should come shopping with us some day!"

    else: #It's sluttier than Mom would like
        the_person "[mom.title] really didn't like it when I bought this, but I just couldn't say no."
        the_person "Maybe you can come shopping with us one day and convince her to relax a little!"
    mc.name "Maybe I will."
    return

label lily_flirt_response_mid(the_person):
    if the_person.effective_sluttiness("underwear_nudity") < 20: #Not very slutty, so it must be high love.
        "[the_person.possessive_title] gasps and blushes."
        the_person "Oh my god, [the_person.mc_title]! Why do you have to say it like that?"
        mc.name "Like what? I'm just telling you that you're looking hot. Isn't that a good thing to hear?"
        the_person "Yeah, but not from my own brother! It's... weird, that's all."
        the_person "I'm sorry, I shouldn't make such a big deal about it. Thank you."

    else:
        the_person "Aw, thanks! I thought I looked really cute in this too."
        $ the_person.draw_person(position = "back_peek")
        "[the_person.possessive_title] smiles and turns around, peeking over her shoulder to talk to you."
        the_person "How do I look from behind? It's hard to get a good look in the mirror and [mom.title] is always judging what I'm wearing."
        "You take a moment to check out [the_person.possessive_title]'s ass before responding."
        mc.name "You look fantastic. I could watch you all day long."
        $ the_person.draw_person()
        "She turns back and sticks her tongue out at you."
        the_person "Maybe if I get bored enough I'll put on a fashion show."
    return

label lily_flirt_response_high(the_person):
    if mc.location.get_person_count() == 1: #If you are alone she'll flirt with you
        if the_person.effective_sluttiness() > (25 - the_person.get_opinion_score("incest")*5): # High sluttiness flirt
            the_person "Oh my god, you're so bad [the_person.mc_title]! Do I... Do I really look that good?"
            mc.name "Yeah you do! You look amazing."
            "She blushes and smiles."
            the_person "Thank you. I think you look good too."
            menu:
                "Kiss her.":
                    "You step closer to [the_person.possessive_title] and put your hand around her waist. She looks into your eyes."
                    if the_person.has_taboo("kissing"):
                        $ the_person.call_dialogue("kissing_taboo_break")
                        $ the_person.break_taboo("kissing")
                        "You kiss her. She hesitates for a second before relaxing and leaning her body against yours."
                    else:
                        the_person "What are you doing..."
                        "You respond by kissing her. She hesitates for a second, then relaxes and leans her body against you."
                    call fuck_person(the_person, private = True, start_position = kissing, skip_intro = True) from _call_fuck_person_45
                    $ the_report = _return
                    $ the_person.call_dialogue("sex_review", the_report = the_report)

                "Just flirt.":
                    mc.name "Thanks. Do you want to get me out of my clothes?"
                    "She giggles and slaps your shoulder gently."
                    the_person "Oh my god, stop!"
                    mc.name "It's fine if you do, I totally get it."
                    "You catch her eyes glancing down at your crotch, then she turns away and laughs you off."
                    the_person "You're my brother, that would be weird."

        else: # Just high love flirt
            "[the_person.possessive_title] laughs and blushes."
            the_person "[the_person.mc_title], I'm your sister! Don't be so weird."
            mc.name "I'm just joking around. You're looking good, that's all."
            the_person "Thanks! I don't really mind, but I think [mom.title] would freak out if she heard you talking like that."


    else: #She shushes you and rushes you off somewhere private.
        if the_person.effective_sluttiness() > (25 - the_person.get_opinion_score("incest")*5): #She's slutty, but you need to find somewhere private so people don't find out.
            "[the_person.possessive_title] blushes, then glances around nervously."
            the_person "Shhh... What if someone heard you?"
            mc.name "Relax, we're not doing anything wrong, are we?"
            the_person "No but... They might not understand, you know?"

            menu:
                "Find someplace quiet.":
                    mc.name "Fine, come with me then."
                    "You take [the_person.title]'s hand and start to lead her away."
                    the_person "Where are we going?"
                    mc.name "We're going somewhere nobody will overhear us, so that you don't have to worry about that any more."
                    "When you find a private spot you turn to [the_person.possessive_title] and pull her close to you."
                    the_person "Ah! We... Nobody is going to find out, right?"
                    mc.name "Nobody is going to find out."

                    if the_person.has_taboo("kissing"):
                        "You lean down to kiss her. She pulls her head back, surprised."
                        $ the_person.call_dialogue("kissing_taboo_break")
                        $ the_person.break_taboo("kissing")
                    else:
                        "You lean down and kiss her. She hesitates for a split second before returning the kiss, pressing her body against yours."
                    call fuck_person(the_person, private = True, start_position = kissing, skip_intro = True) from _call_fuck_person_46
                    $ the_report = _return
                    $ the_person.call_dialogue("sex_review", the_report = the_report)

                "Just flirt.":
                    mc.name "I'll save all the really dirty stuff for when we're alone then."
                    the_person "Oh my god, you're so bad!"
                    "She blushes and slaps you playfully on the shoulder."
                    the_person "Isn't my big brother suppose to be taking care of me? You're just going to get us in trouble!"
                    mc.name "Don't worry, I'll always be around to take care of you. We're just having a little fun."
                    "[the_person.possessive_title] smiles and gives you a quick hug."

        else: #She's not slutty, so she's embarrassed about what you're doing.
            "[the_person.possessive_title] blushes, then glances around nervously."
            the_person "Oh my god, you can't just say stuff like that when there are people around!"
            mc.name "So it's fine if I say things like that when we're alone?"
            the_person "Well... I don't really mind, as long as we're just joking around. I just don't want [mom.title] to get upset with us."
            mc.name "Don't worry, I promise she won't find out."
            the_person "Okay, then it's fine. I actually kind of like hearing I look pretty."
    return

label lily_flirt_response_text(the_person):
    mc.name "Hey [the_person.title], how's it going? Thought I'd check in and say hi."
    "There's a brief pause, then she text back."
    if the_person.has_role(affair_role): #NOTE: In theory neither of these roles are possible, but they might be in the future.
        the_person "Well hi! Going well, wish I was with you though."
        the_person "Think you can sneak into my room tonight? We can have some fun as long as Mom doesn't know."

    elif the_person.has_role(girlfriend_role):
        the_person "Well hi! It's going well, but I wish I was hanging out with you instead."
        the_person "Come by my room and we can spend some more time together."

    elif the_person.love < 40:
        if the_person.effective_sluttiness() > the_person.love:
            the_person "Hey, it's going fine I guess. Nothing exciting going on."

        else:
            the_person "Hey. It's going fine, I guess. How about you? Doing well?"

    else:
        if the_person.effective_sluttiness() > the_person.love:
            the_person "Hey [the_person.mc_title], I'm doing good. A little bored though."
            the_person "We should hang out, I'm sure could get into some trouble together."
        else:
            the_person "Hey [the_person.mc_title], it's going fine. Are you up to anything?"
            the_person "I'm a little bored, we could hang out or something."
    return

label lily_cum_face(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 60:
            the_person "Oh wow, you really covered me. Do I look cute like this bro?"
        else:
            the_person "Oh my god, you got it all over me... You can never let Mom know about this, okay?"
    else:
        if the_person.sluttiness > 80:
            the_person "Mmm, it feels so warm. I know it's wrong but I love being covered in your cum."
        else:
            the_person "Oh my god... what are we doing [the_person.mc_title], we shouldn't be doing this..."
    return

label lily_cum_mouth(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 60:
            the_person "Wow, you really needed that... I guess that's why you need a sister like me."
        else:
            the_person "Oh my god... Mom can never know about this [the_person.mc_title]. She'd kill us both."
    else:
        if the_person.sluttiness > 80:
            the_person "Mmm, who knew my brother had such good tasting cum... If I had known I would have done this with you way earlier!"
        else:
            the_person "I... I can't believe we just did that. We really shouldn't do it again, okay?"
    return

label lily_cum_pullout(the_person):
    # Lead in: "I'm going to cum!"
    if mc.condom:
        if the_person.wants_creampie() and the_person.get_opinion_score("creampies") > 0 and not the_person.has_taboo("condomless_sex"): #TODO: FIgure out we want any more requirements for this to fire.
            if the_person.event_triggers_dict.get("preg_knows", False):
                the_person "Wait... Do you want to take the condom off and cum inside of me?"
                the_person "I'm already pregnant, and it felt so good before..."

            elif the_person.on_birth_control:
                the_person "Take... Take the condom off, I want you to cum inside of me raw!"
                the_person "I'm on the pill, so it doesn't even matter, and creampies feel so good!"
                $ the_person.update_birth_control_knowledge()
                "She moans happily."
            else:
                the_person "Wait, take the condom off first! I... I want you to cum bareback!"
                "She pants happily."
                the_person "It's my fault if I get pregnant, okay? You don't need to worry, I know it would be my fault!"

            menu: #TODO: Add a varient of this normally so you can stealth a girl (don't do that in real life, it's super fucked up).
                "Take off the condom.":
                    "You don't have much time to spare. You pull out, barely clearing her pussy, and pull the condom off as quickly as you can manage."
                    $ mc.condom = False
                "Leave it on.":
                    "You ignore [the_person.possessive_title]'s cum-drunk offer and keep the condom in place."

        else:
            the_person "Oh my god, do it! Cum [the_person.mc_title]!"

    else:
        if the_person.wants_creampie():
            if the_person.event_triggers_dict.get("preg_knows", False): #She's already knocked up, so who cares!
                the_person "Cum wherever you want [the_person.mc_title]!"
            elif the_person.get_opinion_score("creampies") > 0:
                "[the_person.possessive_title] moans happily."
                if the_person.on_birth_control: #She just likes creampies.
                    the_person "Yes! Cum inside me [the_person.mc_title], I want it!"
                else: #Yeah, she's not on BC and asking for you to creampie her. She's looking to get pregnant.
                    the_person "I... Oh god, I want you to cum inside me [the_person.mc_title]!"
                    the_person "Go ahead and knock your little sister up!"
            elif the_person.on_birth_control: #She's on the pill, so she's probably fine
                the_person "Cum wherever you want [the_person.mc_title], I'm on the pill!"
                $ the_person.update_birth_control_knowledge()
            else: #Too distracted to care about getting pregnant or not. Oh well, what could go wrong?
                the_person "Oh god, I'm going to make my brother cum! Ah!"
        else:
            if not the_person.on_birth_control: #You need to pull out, I'm not on the pill!
                the_person "Oh god, pull out! I don't want to get pregnant!"

            elif the_person.get_opinion_score("creampies") < 0:
                the_person "Pull out, I want you to cum all over me [the_person.mc_title]!"

            else:
                the_person "Ah! You... You need to pull out! We can't any risks!"
    return

label lily_cum_condom(the_person):
    if mc.condom:
        if the_person.effective_sluttiness() > 75 or the_person.get_opinion_score("creampies") > 0:
            the_person "Fill up that condom [the_person.mc_title], it's so close to being inside me!"
            "The thought seems to be turning her on."
        else:
            the_person "Oh fuck, good thing you've got a condom on. I mean, could you imagine if you had put all of that into your own sister?"
    return

label lily_cum_vagina(the_person):
    if the_person.has_taboo("creampie"):
        $ the_person.call_dialogue("creampie_taboo_break")
        $ the_person.break_taboo("creampie")
        return

    if the_person.wants_creampie():
        if the_person.event_triggers_dict.get("preg_knows", False):
            the_person "Oh god, your cum feels so nice and warm inside me..."
            "She sighs happily."
            the_person "I guess that's one perk of you knocking me up. No more condoms to worry about."

        elif the_person.on_birth_control:
            the_person "Oh god, you really did it... You came inside your own sister."

        elif the_person.effective_sluttiness() > 75 or the_person.get_opinion_score("creampies") > 0:
            if the_person.relationship != "Single":
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person "I know I shouldn't, but I love having my own brother's cum inside me."
                the_person "I guess if I you get me pregnant I'll have to say it's my [so_title]'s though, so people don't judge us."
            else:
                the_person "Pump me full of your hot cum, I don't care that you're my brother, I want you to get me pregnant!"
        else:
            if the_person.relationship != "Single":
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person "Oh god, you really did it... I'm not on the pill and you still came inside me."
                $ the_person.update_birth_control_knowledge()
                the_person "I hope my [so_title] never finds out about this..."

            else:
                the_person "Oh god, you really did it... I'm not on the pill and you still came inside me."
                $ the_person.update_birth_control_knowledge()
                the_person "I can't believe I let you do that."


    else: #She's angry
        if not the_person.on_birth_control:
            if the_person.relationship != "Single":
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person "Fuck, fuck! You can't cum in me, I'm not on the pill!"
                $ the_person.update_birth_control_knowledge()
                the_person "What if you got me pregnant? What would [mom.title] say?"
                "She groans unhappily."
                the_person "What would my [so_title] say? I don't know if I could lie to him."
            else:
                the_person "Oh god no, you can't cum inside me, I'm not on the pill!"
                $ the_person.update_birth_control_knowledge()
                "She groans unhappily."
                the_person "What would I do if my own brother got me pregnant?"
                the_person "I'd die of embarrassment if anyone found out!"

        elif the_person.relationship != "Single":
            $ so_title = SO_relationship_to_title(the_person.relationship)
            the_person "Oh god, I can't believe you just came inside me... What if my birth control doesn't work?"
            $ the_person.update_birth_control_knowledge()
            "She takes a deep breath and tries to calm herself down."
            the_person "I would have to tell everyone it was my [so_title]'s, but I would still know..."

        elif the_person.get_opinion_score("creampies") < 0:
            the_person "Hey, I told you to pull out! Ugh, you've made such a mess inside me now."

        else:
            the_person "Oh god, I can't believe you just came inside me... What if my birth control doesn't work?"
            $ the_person.update_birth_control_knowledge()
            "She takes a deep breath and calms herself down."
            the_person "It's probably fine... Right? Yeah, I'm sure it's fine. The pill is like a ninety nine percent effective, right?"

    return

label lily_cum_anal(the_person):
    if the_person.sluttiness > 75 or the_person.get_opinion_score("anal creampies") > 0:
        the_person "Fill me up!"
    else:
        the_person "Oh fuck, my brother's cumming into my ass..."
        "She doesn't seem very upset by the idea."
    return

label lily_sex_strip(the_person):
    if the_person.sluttiness < 20:
        if the_person.arousal < 50:
            the_person "I feel like Mom in this outfit. One second..."
        else:
            the_person "Oh god, I can't believe you're making me feel this way [the_person.mc_title]."

    elif the_person.sluttiness < 60:
        if the_person.arousal < 50:
            the_person "I'm just going to take this off. It's nothing you haven't seen before anyways..."
        else:
            the_person "I know it's wrong for me to feel this way about your brother..."
            "She pauses for a second, as if gathering her confidence."
            the_person "But I really want to get naked right now."

    else:
        if the_person.arousal < 50:
            the_person "I bet you want to see more of your little sister, right? God [the_person.mc_title], you're so bad."
        else:
            the_person "Oh my god, I can't keep this on any longer!"

    return

label lily_talk_busy(the_person):
    if the_person.obedience > 120:
        the_person "Hey, I'd love to catch up with my big brother but I've got some work to get done. Could we chat later?"
    else:
        the_person "Sorry [the_person.mc_title], but I've got a ton of school work to get done. We'll have to chat later."
    return

label lily_sex_watch(the_person, the_sex_person, the_position):
    if the_person.sluttiness < the_position.slut_requirement - 20:
        $ the_person.draw_person(emotion = "angry")
        the_person "Oh my god, [the_person.mc_title]! How can you do that in front of your sister?"
        $ the_person.change_obedience(-2)
        $ the_person.change_happiness(-1)
        "[the_person.title] looks away while you and [the_sex_person.name] [the_position.verb]."

    elif the_person.sluttiness < the_position.slut_requirement - 10:
        $ the_person.draw_person()
        $ the_person.change_happiness(-1)
        the_person "I... oh my god I can't believe you're my brother..."
        "[the_person.title] tries to avert her gaze while you and [the_sex_person.name] [the_position.verb]."

    elif the_person.sluttiness < the_position.slut_requirement:
        $ the_person.draw_person()
        the_person "Oh my god, you two are just... Wow..."
        $ change_report = the_person.change_slut_temp(1)
        "[the_person.possessive_title] averts her gaze, but she keeps stealing glances while you and [the_sex_person.name] [the_position.verb]."

    elif the_person.sluttiness >= the_position.slut_requirement and the_person.sluttiness < the_position.slut_cap:
        $ the_person.draw_person()
        the_person "Oh my god, [the_person.mc_title], where did you learn to do that? I shouldn't be watching this, but..."
        $ change_report = the_person.change_slut_temp(2)
        "[the_person.title] watches you and [the_sex_person.name] [the_position.verb]."

    else:
        $ the_person.draw_person(emotion = "happy")
        the_person "Give it to her [the_person.mc_title], don't hold back just because I'm here."
        the_person "You're not nervious because your sister is watching, are you?"
        "[the_person.title] watches eagerly while you and [the_sex_person.name] [the_position.verb]."

    return

label lily_being_watched(the_person, the_watcher, the_position):
    if the_person.sluttiness >= the_position.slut_cap and the_watcher.sluttiness >= the_position.slut_cap:
        #They agree you should give it to her harder
        the_person "I can handle it [the_person.mc_title], you can play rough with your little sister."
        $ the_person.change_arousal(1)
        "[the_person.title] seems turned on by [the_watcher.title] watching you and her [the_position.verb]."

    elif the_person.sluttiness >= the_position.slut_cap and the_watcher.sluttiness < the_position.slut_requirement:
        #She's super slutty and doesn't care what people think.
        the_person "Don't listen to [the_watcher.title], I'm having a great time. She's just jealous her brother doesn't treat her like this!"

    elif the_person.sluttiness >= the_position.slut_cap and the_watcher.sluttiness < the_position.slut_cap:
        #She's super slutty and encourages the watcher to be slutty.
        $ the_person.change_arousal(1)
        the_person "We just love each other so much [the_watcher.title]. You understand, right?"
        "[the_person.title] seems turned on by [the_watcher.title] watching you and her [the_position.verb]."

    elif the_person.sluttiness < the_position.slut_cap and the_watcher.sluttiness >= the_position.slut_cap:
        #She's into it and encouraged by the slut watching her.
        the_person "Oh [the_person.mc_title], I know it's be wrong but being with you just feels so right!"
        $ the_person.change_arousal(1)
        "Your little sister seems turned on by [the_watcher.title] watching you and her [the_position.verb]."

    elif the_person.sluttiness < the_position.slut_cap and the_watcher.sluttiness < the_position.slut_requirement:
        #She's into it but shamed by the prude watching her.
        the_person "[the_person.mc_title], we shouldn't be doing this here. What if people talk?"
        $ the_person.change_arousal(-1)
        $ the_person.change_slut_temp(-1)
        "[the_person.title] seems uncomfortable with [the_watcher.title] nearby."

    else: #the_person.sluttiness < the_position.slut_cap and the_watcher.sluttiness < the_position.slut_cap:
        #They're both into it but not fanatical about it.
        the_person "[the_watcher.title], I'm so glad you don't think this is too weird."
        the_person "I know it's suppose to be wrong, but then why does it feel so good?"
        $ the_person.change_arousal(1)
        $ the_person.change_slut_temp(1)
        "[the_person.title] seems more comfortable [the_position.verbing] you with [the_watcher.title] around."

    return

label lily_date_seduction(the_person):
    if the_person.sluttiness > the_person.love:
        if the_person.sluttiness > 40:
            the_person "Hey [the_person.mc_title], wait up a sec."
            "[the_person.title] stops you before you open the front door to the house."
            the_person "I've had a great night, do you want to come back to my room and have some more fun?"

        else:
            the_person "Hey [the_person.mc_title], wait up a sec."
            "[the_person.title] stops you before you open the front door to your house."
            the_person "I, uh... I had a really good night with you. I know it's a little weird, but do you want to come back to my room and just hang out?"

    else:
        if the_person.love > 40:
            "[the_person.title] stops you when you get in the door. She takes your hand in hers and looks into your eyes."
            the_person "I had a great night. It was so nice to be with you and just pretend that we weren't... that we could be together."
            "Her hand tightens around yours."
            the_person "Do you want to come back to my room and just pretend a little bit longer?"

        else:
            "[the_person.title] stops you when you get inside. She takes your hand, then looks away and blushes."
            the_person "I had a fun time [the_person.mc_title], thanks for taking me out."
            "She hesitates for a second before continuing."
            the_person "If you want to come back to my room and chat for a while I wouldn't say no."
    return

## Taboo break dialogue ##
label lily_kissing_taboo_break(the_person):
    the_person "Hey... What are you doing?"
    mc.name "I'm going to kiss you [the_person.title]."
    the_person "Ew. You're my brother, that's weird."
    mc.name "Why? We use to kiss when we were kids."
    the_person "Oh my god, I forgot about that. That was different, we were young and just practicing."
    mc.name "Let's practice some more. I'm sure we can both get better at it if we try."
    the_person "You're serious? I... I don't know [the_person.mc_title], what if [mom.title] finds out?"
    mc.name "She doesn't need to know. Nobody does. It will be our little secret."
    mc.name "Plus it gives me a reason to spend time with my awesome little sister. Isn't that nice?"
    "She nods meekly and doesn't say anything."
    return

label lily_touching_body_taboo_break(the_person):
    if the_person.love > 20:
        the_person "Hey, stop that..."
        mc.name "Why?"
        the_person "Why do you think? You're my brother, and you're touching me like you want to... Do other things."
        mc.name "And you're my little sister, who I love more than anyone else in the world."
        the_person "Oh yeah? What about Mom?"
        mc.name "Even more than her. I would die to keep you safe, and I would never do anything to hurt you."
        the_person "Really? I... We still shouldn't do this though..."
        "You can hear her resolve breaking down in her voice."
        mc.name "Maybe not, but I want more than anything to be close to you right now."
        "She looks away and sighs, then turns back and nods."
        the_person "Just don't make this weird, okay?"
        the_person "Oh, and don't say anything to Mom. She would probably freak out and kick you out or something."

    else:
        the_person "Hey, you shouldn't be doing that..."
        mc.name "Why?"
        the_person "Because it's incest, you're my brother. That's wrong, isn't it?"
        mc.name "Come on, it's only incest if I could get you pregnant."
        mc.name "I hope you know that a guy can't get you pregnant by touching your butt."
        "She laughs and looks away."
        the_person "I know that, but... Does that really mean it's not incest?"
        mc.name "Yeah, of course. I just want to be close to my baby sister. Don't you feel close right now."
        "She looks away from you and nods meekly."
        mc.name "Me too. Just relax and enjoy yourself, you know you can trust me."
        the_person "Okay, you're right [the_person.mc_title]. Just don't tell Mom okay?"
        the_person "I feel like she wouldn't understand and freak out."
    mc.name "I won't tell her a word. I promise."
    return

label lily_touching_penis_taboo_break(the_person):
    if the_person.love > 30:
        the_person "Holy shit. Are all guys as big as you, or are you... Unusual?"
        "You shrug?"
        mc.name "I've never checked. You can touch it if you want."
        the_person "Touch it?"
        mc.name "Yeah, go ahead. Have you ever touched one this big?"
        "She shakes her head sheepishly."
        mc.name "Well this is a perfect time for you to learn how to handle it."
        the_person "You don't think it's weird for your sister to touch your... You know."
        mc.name "My cock? No, I think this is the perfect place for you to learn about stuff like this."
        mc.name "Who can you trust more than your own brother?"
        "She smiles and nods."
        the_person "Thanks [the_person.mc_title], you're awesome. Okay Lily... You've got this!"
        "She takes a deep breath and gathers her courage."

    else:
        the_person "Wow. I can't believe my brother actually has a big cock."
        the_person "Oh my god, what am I saying? You're my {i}brother{/i}, that's fucked up!"
        mc.name "Go ahead and touch it."
        the_person "What? Ew, no way."
        mc.name "Come on [the_person.title], you know you want to"
        the_person "Maybe a little... You aren't going to make this weird, are you?"
        mc.name "Of course not, why would I do that?"
        the_person "I don't know, you just have a way of pushing things and for some reason I never say no until it's too late."
        mc.name "We trust each other, don't we? It's just our way of experimenting in a safe place."
        the_person "Okay... I'm just going to stroke it for a moment, so I know what it feels like."
    return

label lily_touching_vagina_taboo_break(the_person):
    the_person "Jesus, careful! Were you going to touch my pussy?"
    if the_person.love > 30:
        if the_person.has_taboo("touching_penis"):
            mc.name "I want to. Will you let me?"
            the_person "You shouldn't... Mom would be so angry if she knew what we were doing."
            mc.name "It's a good thing she's not here then. Please [the_person.title], I need more practice and I trust you."
            the_person "Really? You need practice?"
            mc.name "Yeah, I don't meet many women. I don't want to embarrass myself if I get the chance."
            "She thinks for a long moment, then sighs and nods."
            the_person "Okay, you can touch it."

        else:
            mc.name "Of course I was. You've gotten to feel my cock, why can't I touch you?"
            the_person "I mean... You can, I guess, but I thought you were going to ask first."

    else:
        mc.name "I was. It'll feel good, why are you worried?"
        the_person "I mean, yeah of course it would, but you're my brother!"
        if the_person.has_taboo("touching_penis"):
            mc.name "I'm your brother, so you should trust me. Relax, enjoy yourself."
            "She puts her face in her hands and shakes her head."
            the_person "I can't believe I'm letting you do this. I'm so embarrassed!"
        else:
            mc.name "You're my sister, but you've still had your hand wrapped around my cock."
            the_person "I can't believe I did that. I'm so embarrassed!"
            mc.name "Don't be. Just relax and enjoy yourself."
    return

label lily_sucking_cock_taboo_break(the_person):
    mc.name "Hey [the_person.title], do you want to try something special?"
    the_person "What?"
    mc.name "I want you to try sucking my cock."
    if the_person.love > 40:
        the_person "Haha, very funny. Come on, what do you really mean?"
        mc.name "I'm serious. I want to have my cock sucked."
        the_person "Oh my god, you really are serious. [the_person.mc_title], that's so fucked up!"
        if the_person.has_taboo("kissing"):
            mc.name "Come on, it's not like we've even kissed before. We're experimenting."

        else:
            mc.name "Come on, we've made out before, right?"
            the_person "Yeah..."
            mc.name "So it's just your lips on a different part of me."
            "She sighs and shakes her head in disbelief."
            mc.name "It means even less than kissing. We're just experimenting."

        the_person "Normal familes don't experiment with each other! Do you know anyone else who has their sister suck their dick?"
        mc.name "No, but I don't know anyone who loves their little sister as much as I do either."
        mc.name "We aren't a normal family [the_person.title], we have something special. You love me, right?"
        the_person "Yeah, I love you [the_person.mc_title]."
        mc.name "I love you too, so let's forget about what other people call normal and do what feels right for us."
        "[the_person.possessive_title] takes a long moment to think, then nods enthusiastically."
        the_person "You're right. Fuck what other people think!"
        "She wraps her arms around you and hugs you tight. You return the gesture, kissing the top of her head."
        "She's smiling when she breaks the hug and looks up at you."
        the_person "So... I guess we're doing this then!"
        mc.name "Looks like it. Have you given a blowjob before, or should I walk you through it?"


    else:
        the_person "Wait, really?"

        if the_person.has_taboo("kissing"):
            mc.name "Yeah, why not? It feels good and I'd bet you're really good at it."

        else:
            mc.name "Yeah, why not? I know you're a good kisser, I bet your mouth is good at sucking cock too."

        the_person "Why not? Because I'm your sister and Mom would kill us both if she found out!"
        mc.name "So we'll just make sure she doesn't find out. Come on [the_person.title], you want to try it too, right?"
        "[the_person.possessive_title] blushes and nods meekly."
        the_person "I've thought about it before."
        mc.name "Does thinking about sucking my cock get you turned on."
        "She looks away shyly and shrugs."
        the_person "I guess a little."
        mc.name "So then what's stopping you. We're both adults, you want to do it, I want you to do it. Hey..."
        "You place a gentle hand on her cheek and turn her head to look at you. You look each other in the eyes."
        mc.name "Mom is never going to find out about this. Nobody is, so we don't have to worry what other people say is normal."
        mc.name "We aren't normal. I don't want to be normal, and I don't think you want to be either."
        "She shakes her head, then wraps her arms around you and hugs you tight. You return the gesture, holding her head to your chest."
        "When she breaks the hug she's smiling."
        the_person "You're right [the_person.mc_title]! Okay, I guess I should get on my knees then."
        mc.name "That would be the next step, yeah. Have you ever given a blowjob before, or should I walk you through it?"

    the_person "Oh my god, I'm not a kid. I know how to give a blowjob."
    mc.name "Alright, you show me what you know."
    return

label lily_licking_pussy_taboo_break(the_person):
    if the_person.love > 40:
        the_person "Wait, what are you doing?"
        mc.name "I'm going to lick your pussy."
        "[the_person.possessive_title] seems embarrassed by the idea. She looks away and blushes."
        the_person "I don't know [the_person.mc_title], maybe we shouldn't..."
        if the_person.has_taboo("sucking_cock"):
            mc.name "Why not? Don't you trust me?"
            the_person "I do, but... you're my brother, you know? Mom would be so angry if she knew."
            mc.name "She won't ever find out about it. You want this too, don't you?"
            "She blushes and nods meekly."
            mc.name "I thought so. Just spread your legs, relax, and let your brother take care of you."
        else:
            mc.name "Why not? You've already sucked my cock, I'm just going to do the same for you."
            the_person "I guess... It would feel really nice."
            mc.name "Exactly. Just spread your legs, relax, and let me take care of you."

    else:
        the_person "Are you going to do what I think you're going to do?"
        mc.name "That depends on what you think I'm going to do."
        the_person "Are you going to... lick my pussy?"
        mc.name "That was what I was going to do, yeah. Do you want me to?"
        if the_person.has_taboo("sucking_cock"):
            the_person "We shouldn't... Mom would be so angry."
            mc.name "I didn't ask if Mom would be angry. I asked if you want me to."
            "She hesitates, then nods her head."
            the_person "I do. Do you promise she won't find out?"
            mc.name "I promise. Just spread your legs, relax, and let your big brother take care of you."

        else:
            the_person "I already sucked you off, so it would be pretty fair..."
            mc.name "Exactly. Just spread your legs, relax, and let your big brother take care of you."
    return

label lily_vaginal_sex_taboo_break(the_person):
    if the_person.love > 60:
        the_person "This is so crazy! We should really stop, we've taken this too far..."
        if the_person.has_taboo("kissing"):
            mc.name "[the_person.title], stop. You love me, right?"

        else:
            if the_person.has_taboo("sucking_cock"):
                mc.name "Was it too far when we kissed? I liked doing that a lot."
                the_person "I did too, but that was different. We were just experimenting. Right?"
                mc.name "That's what we told ourselves, but I think we both knew it meant more. Do you love me?"


            else:
                mc.name "Was it too far when we kissed? What about when you sucked my cock?"
                the_person "That was... Maybe that was a mistake."
                mc.name "I don't think it was. I think we've been lying to ourselves."
                the_person "What do you mean?"
                mc.name "Do you love me?"


        the_person "You're my brother, of course I love you, but..."
        mc.name "\"But\" nothing. I love you too and want to share that with you."
        "She is quiet for a long moment, then nods uncertainly."
        the_person "Okay... We can do this, but we can't let anyone know! And we aren't, like, a couple, okay?"
        the_person "You're still my brother, we just... Do other things together. Understand?"
        mc.name "Sure thing sis."


    else:
        the_person "I can't believe we are really doing this... Is it wrong? Should we stop?"
        mc.name "What do you think? Do you want to stop?"
        "She bites her lip and shakes her head."
        the_person "No. I want to see what it feels like."
        mc.name "What do you want to feel?"
        the_person "Stop teasing me [the_person.mc_title]! I want to feel your... cock inside me."
        mc.name "That's a good girl. Well, let's give it a try!"
    return

label lily_anal_sex_taboo_break(the_person):
    if the_person.love > 60:
        the_person "Wait, do you really mean you want to try anal?"
        if the_person.has_taboo("vaginal_sex"):
            mc.name "Yeah, I do. I want to have sex, but you probably don't want me fucking your pussy yet."
            the_person "Ever. That would be actual, full incest [the_person.mc_title]."
            mc.name "Exactly, so we can cheat a little like this."
            "[the_person.possessive_title] seems unsure."
            mc.name "Come on, don't you want to experiment with someone you trust?"
        else:
            mc.name "Yeah, why not? I've already fucked all of your other holes, what's special about this one?"
            the_person "It's not special, I just thought you'd want to fuck my pussy some more. Didn't you enjoy it last time."
            mc.name "It was great, but I want to experiment a little more. Come on, don't you want to try something new?"

    else:
        the_person "Wait, do you want to try anal?"
        mc.name "Yeah, I do. You've got a cute butt."
        if the_person.has_taboo("vaginal_sex"):
            the_person "You're crazy [the_person.mc_title]! We're related, we shouldn't  be fucking!"
            mc.name "It's not like it's real sex. If you want I can go to town on your pussy though, it looks just as tight."
            the_person "I guess anal isn't as bad as my own brother fucking my pussy..."


        else:
            the_person "What's wrong with my pussy? Didn't you enjoy it last time?"
            mc.name "It was great, I just want to try something new. Come on, you like experimenting, right?"
            the_person "I guess this way I don't have to worry about you pulling out..."

    "She sighs and gives in."
    the_person "Okay, but you need to be gentle with me."
    mc.name "I promise I will. Have you ever tried this before?"
    the_person "With toys a couple of times... Never with a guy."
    mc.name "You'll probably be really tight then. I'll go nice and slow to give you time to stretch out."
    the_person "Okay. Thank you [the_person.mc_title]."
    return

label lily_condomless_sex_taboo_break(the_person):
    the_person "I don't like condoms either, but we need to be careful. What would we tell [mom.title] if you got me pregnant?"
    mc.name "Wait, are you on birth control?"
    if the_person.on_birth_control:
        the_person "I am, but what if it didn't work?"
    else:
        "She shakes her head meekly."
    $ the_person.update_birth_control_knowledge()
    if the_person.has_taboo("vaginal_sex"):
        mc.name "We won't need to tell [mom.title] anything. I'm not going to get you pregnant the very first time we have sex."
        "[the_person.possessive_title] still seems uncertain."
        mc.name "Come on [the_person.title], don't you want our first time to be special? I promise I'll pull out."
        the_person "Since it's our first time... Okay, as long as you are really careful when you're going to cum."

    else:
        mc.name "We won't need to tell [mom.title] anything. I'm not going to get you pregnant the very first time we fuck raw."
        "[the_person.possessive_title] still seems uncertain."
        mc.name "Come on [the_person.title], don't you trust me? It'll feel so much better without a condom."
        the_person "Okay, fine. But you need to be {i}really{/i} careful not to cum in me."
    mc.name "I promise I'll be careful. Ready?"
    "She gives you a nervous nod."
    return

label lily_underwear_nudity_taboo_break(the_person, the_clothing):
    the_person "Oh my god, I can't believe you want to see your own sister in her underwear!"
    mc.name "Come on, we're family. There's nothing to be shy about."
    "She rolls her eyes and shrugs."
    the_person "Fine. You're so strange sometimes."
    return

label lily_bare_tits_taboo_break(the_person, the_clothing):
    the_person "Hey, why are you playing with my [the_clothing.display_name]?"
    mc.name "I want to take it off."
    "[the_person.possessive_title] seems equal parts embarrassed and excited."
    the_person "Oh my god, you want to look at your sisters boobs? Do you... think they're cute?"
    if not the_person.has_large_tits():
        the_person "I hoped they would be big like [mom.title]'s, but I don't think that's going to happen."
    mc.name "They look great, let's take a closer look..."
    "She stands passively as you take off her [the_clothing.display_name]."
    return

label lily_bare_pussy_taboo_break(the_person, the_clothing):
    the_person "Hey, what are you doing? If you take off my [the_clothing.display_name] you'll be able to see my... Pussy."
    "[the_person.possessive_title] seems excited rather than scared of the idea, but needs a little more convincing."
    if the_person.has_taboo("touching_vagina"):
        mc.name "Come on [the_person.title], I saw it when we were kids and it wasn't a big deal."
        the_person "Yeah, but you never looked at me like... This."
        mc.name "We've both grown up, but I've always thought you were beautiful. I can appreciate you as a woman now, not just as my sister."
        "She sighs and nods."
        the_person "Okay, just a quick look. That can't be too wrong, right?"
        mc.name "Yeah, right."
    else:
        mc.name "Come on [the_person.title], I've already felt up your pussy. What do you have left to hide?"
        the_person "Fine. Just a little look won't be too bad, right?"

    "She stands passively and lets you pull down her [the_clothing.display_name]."
    return

# label lily_facial_cum_taboo_break(the_person):
#
#     return
#
# label lily_mouth_cum_taboo_break(the_person):
#
#     return
#
# label lily_body_cum_taboo_break(the_person):
#
#     return
#
label lily_creampie_taboo_break(the_person):
    if the_person.wants_creampie():
        the_person "Oh my god [the_person.mc_title], you just came inside of me!"
        "She seems shocked, but not entirely unhappy."
        mc.name "Yeah, isn't that what you wanted?"
        if the_person.on_birth_control:
            the_person "It does feel really good..."
            mc.name "It feels good for me too. Don't worry [the_person.title], there's nothing to worry about."
            the_person "Yeah, you're right. It's just such a new feeling, I needed a second to get use to it."
        else:
            the_person "It does feel really good, but I'm not on my birth control. What if I, you know..."
            mc.name "Get pregnant?"
            the_person "Yeah, that. Shouldn't we be trying to avoid that? I don't want to have to explain that to [mom.title]."
            mc.name "The chances you're going to get pregnant after your first cumshot are really low. You really don't need to worry about it."
            the_person "I guess you're right, but we need to be careful, okay? We can't be doing this all the time, even if it feels awesome."
    else:
        the_person "Oh my god [the_person.mc_title], I told you to pull out!"
        mc.name "Yeah, sorry about that. I got a little carried away."
        "[the_person.possessive_title] seems a little shocked."
        if the_person.on_birth_control:
            the_person "You just... came inside me. I've got my brothers cum inside of my pussy..."
            mc.name "Yeah, and it felt really good too. Did it feel good for you?"
            the_person "...It did."
            mc.name "Then what's the problem? You're on the pill, right?"
            "She nods."
            the_person "Yeah, I am. I guesss you're right, it's not such a big deal as long as you don't do it too often."
            $ the_person.update_birth_control_knowledge()

        else:
            the_person "You just... came inside of me. I've got a pussy full of my brothers cum, and I'm not on birth control."
            mc.name "Yeah, and it felt really good to put it there. Did it feel good for you too?"
            the_person "...It did, but what if you get me pregnant?"
            mc.name "The chances of that happening the very first time are so low, we don't need to worry about it."
            the_person "Really?"
            mc.name "Yeah, they're super low. Don't you trust me [the_person.title]?"
            "She nods."
            the_person "Of course I do. Okay, I guess it's not a big deal as long as you don't do it again. You need to be careful with me."
    return
#
# label lily_anal_creampie_taboo_break(the_person):
#
#     return
