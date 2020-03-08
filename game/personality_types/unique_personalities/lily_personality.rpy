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
        titles_function = lily_titles, possessive_titles_function = lily_possessive_titles, player_titles_function = lily_player_titles)

### DIALOGUE ###
label lily_greetings(the_person):
    if the_person.love < 0:
        the_person.char "Ugh, can you tell Mom whatever you want to say to me right now? I don't want to hear it."
    elif the_person.happiness < 90:
        the_person.char "Hey [the_person.mc_title]..."
    else:
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
        the_person.char "Oh god, that sounds so hot. I hope nobody here recognizes me!"
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

label lily_cum_vagina(the_person):
    if mc.condom:
        if the_person.sluttiness > 75 or the_person.get_opinion_score("creampies") > 0:
            the_person.char "Fill up that condom [the_person.mc_title], it's so close to being inside me!"
            "The thought seems to be turning her on."
        else:
            the_person.char "Oh fuck, good thing you've got a condom on. I mean, could you imagine if you had put all of that into your own sister?"

    else:
        if the_person.sluttiness > 75 or the_person.get_opinion_score("creampies") > 0:
            if the_person.relationship != "Single":
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person.char "I know I shouldn't, but I love having my own brother's cum inside me."
                the_person.char "I guess if I you get me pregnant I'll have to say it's my [so_title]'s though, so people don't judge us."
            else:
                the_person.char "Pump me full of your hot cum, I don't care that you're my brother, I want you to get me pregnant!"
        else:
            if the_person.relationship != "Single":
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person.char "Fuck, fuck! You can't cum in me, what if you got me pregnant? What would Mom say?"
                the_person.char "What would my [so_title] say? I don't know if I could lie to him."
            else:
                the_person.char "Oh god no, you can't cum inside me! What would I do if my own brother got me pregnant?"
                the_person.char "I'd die of embarrassment if people found out!"
    return

label lily_cum_anal(the_person):
    if the_person.sluttiness > 75 or the_person.get_opinion_score("anal creampies") > 0:
        the_person.char "Fill me up!"
    else:
        the_person.char "Oh fuck, my brother's cumming into my ass..."
        "She doesn't seem very upset by the idea."
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
        "[the_person.title] seems more comfortable [the_position.verbing] you with [the_watcher.title] around."

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

## Taboo break dialogue ##
label lily_kissing_taboo_break(the_person):
    the_person.char "Hey... What are you doing?"
    mc.name "I going to kiss you [the_person.title]."
    the_person.char "Ew. You're my brother, that's weird."
    mc.name "Why? We use to kiss when we were kids."
    the_person.char "Oh my god, I forgot about that. That was different, we were young and just practicing."
    mc.name "Let's practice some more. I'm sure we can both get better at it if we try."
    the_person.char "You're serious? I... I don't know [the_person.mc_title], what if [mom.title] finds out?"
    mc.name "She doesn't need to know. Nobody does. It will be our little secret."
    mc.name "Plus it gives me a reason to spend time with my awesome little sister. Isn't that nice?"
    "She nods meekly and doesn't say anything."
    return

label lily_touching_body_taboo_break(the_person):
    if the_person.love > 20:
        the_person.char "Hey, stop that..."
        mc.name "Why?"
        the_person.char "Why do you think? You're my brother, and you're touching me like you want to... Do other things."
        mc.name "And you're my little sister, who I love more than anyone else in the world."
        the_person.char "Oh yeah? What about Mom?"
        mc.name "Even more than her. I would die to keep you safe, and I would never do anything to hurt you."
        the_person.char "Really? I... We still shouldn't do this though..."
        "You can hear her resolve breaking down in her voice."
        mc.name "Maybe not, but I want more than anything to be close to you right now."
        "She looks away and sighs, then turns back and nods."
        the_person.char "Just don't make this weird, okay?"
        the_person.char "Oh, and don't say anything to Mom. She would probably freak out and kick you out or something."

    else:
        the_person.char "Hey, you shouldn't be doing that..."
        mc.name "Why?"
        the_person.char "Because it's incest, you're my brother. That's wrong, isn't it?"
        mc.name "Come on, it's only incest if I could get you pregnant."
        mc.name "I hope you know that a guy can't get you pregnant by touching your butt."
        "She laughs and looks away."
        the_person.char "I know that, but... Does that really mean it's not incest?"
        mc.name "Yeah, of course. I just want to be close to my baby sister. Don't you feel close right now."
        "She looks away from you and nods meekly."
        mc.name "Me too. Just relax and enjoy yourself, you know you can trust me."
        the_person.char "Okay, you're right [the_person.mc_title]. Just don't tell Mom okay?"
        the_person.char "I feel like she wouldn't understand and freak out."
    mc.name "I won't tell her a word. I promise."
    return

label lily_touching_penis_taboo_break(the_person):
    if the_person.love > 30:
        the_person.char "Holy shit. Are all guys as big as you, or are you... Unusual?"
        "You shrug?"
        mc.name "I've never checked. You can touch it if you want."
        the_person.char "Touch it?"
        mc.name "Yeah, go ahead. Have you ever touched one this big?"
        "She shakes her head sheepishly."
        mc.name "Well this is a perfect time for you to learn how to handle it."
        the_person.char "You don't think it's weird for your sister to touch your... You know."
        mc.name "My cock? No, I think this is the perfect place for you to learn about stuff like this."
        mc.name "Who can you trust more than your own brother?"
        "She smiles and nods."
        the_person.char "Thanks [the_person.mc_title], you're awesome. Okay Lily... You've got this!"
        "She takes a deep breath and gathers her courage."

    else:
        the_person.char "Wow. I can't believe my brother actually has a big cock."
        the_person.char "Oh my god, what am I saying? You're my {i}brother{/i}, that's fucked up!"
        mc.name "Go ahead and touch it."
        the_person.char "What? Ew, no way."
        mc.name "Come on [the_person.title], you know you want to"
        the_person.char "Maybe a little... You aren't going to make this weird, are you?"
        mc.name "Of course not, why would I do that?"
        the_person.char "I don't know, you just have a way of pushing things and for some reason I never say no until it's too late."
        mc.name "We trust each other, don't we? It's just our way of experimenting in a safe place."
        the_person.char "Okay... I'm just going to stroke it for a moment, so I know what it feels like."
    return

label lily_touching_vagina_taboo_break(the_person):
    the_person.char "Jesus, careful! Were you going to touch my pussy?"
    if the_person.love > 30:
        if the_person.has_taboo("touching_penis"):
            mc.name "I want to. Will you let me?"
            the_person.char "You shouldn't... Mom would be so angry if she knew what we were doing."
            mc.name "It's a good thing she's not here then. Please [the_person.title], I need more practice and I trust you."
            the_person.char "Really? You need practice?"
            mc.name "Yeah, I don't meet many women. I don't want to embarrass myself if I get the chance."
            "She thinks for a long moment, then sighs and nods."
            the_person.char "Okay, you can touch it."

        else:
            mc.name "Of course I was. You've gotten to feel my cock, why can't I touch you?"
            the_person.char "I mean... You can, I guess, but I thought you were going to ask first."

    else:
        mc.name "I was. It'll feel good, why are you worried?"
        the_person.char "I mean, yeah of course it would, but you're my brother!"
        if the_person.has_taboo("touching_penis"):
            mc.name "I'm your brother, so you should trust me. Relax, enjoy yourself."
            "She puts her face in her hands and shakes her head."
            the_person.char "I can't believe I'm letting you do this. I'm so embarrassed!"
        else:
            mc.name "You're my sister, but you've still had your hand wrapped around my cock."
            the_person.char "I can't believe I did that. I'm so embarrassed!"
            mc.name "Don't be. Just relax and enjoy yourself."
    return

label lily_sucking_cock_taboo_break(the_person):
    mc.name "Hey [the_person.title], do you want to try something special?"
    the_person.char "What?"
    mc.name "I want you to try sucking my cock."
    if the_person.love > 40:
        the_person.char "Haha, very funny. Come on, what do you really mean?"
        mc.name "I'm serious. I want to have my cock sucked."
        the_person.char "Oh my god, you really are serious. [the_person.mc_title], that's so fucked up!"
        if the_person.has_taboo("kissing"):
            mc.name "Come on, it's not like we've even kissed before. We're experimenting."

        else:
            mc.name "Come on, we've made out before, right?"
            the_person.char "Yeah..."
            mc.name "So it's just your lips on a different part of me."
            "She sighs and shakes her head in disbelief."
            mc.name "It means even less than kissing. We're just experimenting."

        the_person.char "Normal familes don't experiment with each other! Do you know anyone else who has their sister suck their dick?"
        mc.name "No, but I don't know anyone who loves their little sister as much as I do either."
        mc.name "We aren't a normal family [the_person.title], we have something special. You love me, right?"
        the_person.char "Yeah, I love you [the_person.mc_title]."
        mc.name "I love you too, so let's forget about what other people call normal and do what feels right for us."
        "[the_person.possessive_title] takes a long moment to think, then nods enthusiastically."
        the_person.char "You're right. Fuck what other people think!"
        "She wraps her arms around you and hugs you tight. You return the gesture, kissing the top of her head."
        "She's smiling when she breaks the hug and looks up at you."
        the_person.char "So... I guess we're doing this then!"
        mc.name "Looks like it. Have you given a blowjob before, or should I walk you through it?"


    else:
        the_person.char "Wait, really?"

        if the_person.has_taboo("kissing"):
            mc.name "Yeah, why not? It feels good and I'd bet you're really good at it."

        else:
            mc.name "Yeah, why not? I know you're a good kisser, I bet your mouth is good at sucking cock too."

        the_person.char "Why not? Because I'm your sister and Mom would kill us both if she found out!"
        mc.name "So we'll just make sure she doesn't find out. Come on [the_person.title], you want to try it too, right?"
        "[the_person.possessive_title] blushes and nods meekly."
        the_person.char "I've thought about it before."
        mc.name "Does thinking about sucking my cock get you turned on."
        "She looks away shyly and shrugs."
        the_person.char "I guess a little."
        mc.name "So then what's stopping you. We're both adults, you want to do it, I want you to do it. Hey..."
        "You place a gentle hand on her cheek and turn her head to look at you. You look each other in the eyes."
        mc.name "Mom is never going to find out about this. Nobody is, so we don't have to worry what other people say is normal."
        mc.name "We aren't normal. I don't want to be normal, and I don't think you want to be either."
        "She shakes her head, then wraps her arms around you and hugs you tight. You return the gesture, holding her head to your chest."
        "When she breaks the hug she's smiling."
        the_person.char "You're right [the_person.mc_title]! Okay, I guess I should get on my knees then."
        mc.name "That would be the next step, yeah. Have you ever given a blowjob before, or should I walk you through it?"

    the_person.char "Oh my god, I'm not a kid. I know how to give a blowjob."
    mc.name "Alright, you show me what you know."
    return

label lily_licking_pussy_taboo_break(the_person):
    if the_person.love > 40:
        the_person.char "Wait, what are you doing?"
        mc.name "I'm going to lick your pussy."
        "[the_person.possessive_title] seems embarrassed by the idea. She looks away and blushes."
        the_person.char "I don't know [the_person.mc_title], maybe we shouldn't..."
        if the_person.has_taboo("sucking_cock"):
            mc.name "Why not? Don't you trust me?"
            the_person.char "I do, but... you're my brother, you know? Mom would be so angry if she knew."
            mc.name "She won't ever find out about it. You want this too, don't you?"
            "She blushes and nods meekly."
            mc.name "I thought so. Just spread your legs, relax, and let your brother take care of you."
        else:
            mc.name "Why not? You've already sucked my cock, I'm just going to do the same for you."
            the_person.char "I guess... It would feel really nice."
            mc.name "Exactly. Just spread your legs, relax, and let me take care of you."

    else:
        the_person.char "Are you going to do what I think you're going to do?"
        mc.name "That depends on what you think I'm going to do."
        the_person.char "Are you going to... lick my pussy?"
        mc.name "That was what I was going to do, yeah. Do you want me to?"
        if the_person.has_taboo("sucking_cock"):
            the_person.char "We shouldn't... Mom would be so angry."
            mc.name "I didn't ask if Mom would be angry. I asked if you want me to."
            "She hesitates, then nods her head."
            the_person.char "I do. Do you promise she won't find out?"
            mc.name "I promise. Just spread your legs, relax, and let your big brother take care of you."

        else:
            the_person.char "I already sucked you off, so it would be pretty fair..."
            mc.name "Exactly. Just spread your legs, relax, and let your big brother take care of you."
    return

label lily_vaginal_sex_taboo_break(the_person):
    if the_person.love > 60:
        the_person.char "This is so crazy! We should really stop, we've taken this too far..."
        if the_person.has_taboo("kissing"):
            mc.name "[the_person.title], stop. You love me, right?"

        else:
            if the_person.has_taboo("sucking_cock"):
                mc.name "Was it too far when we kissed? I liked doing that a lot."
                the_person.char "I did too, but that was different. We were just experimenting. Right?"
                mc.name "That's what we told ourselves, but I think we both knew it meant more. Do you love me?"


            else:
                mc.name "Was it too far when we kissed? What about when you sucked my cock?"
                the_person.char "That was... Maybe that was a mistake."
                mc.name "I don't think it was. I think we've been lying to ourselves."
                the_person.char "What do you mean?"
                mc.name "Do you love me?"


        the_person.char "You're my brother, of course I love you, but..."
        mc.name "\"But\" nothing. I love you too and want to share that with you."
        "She is quiet for a long moment, then nods uncertainly."
        the_person.char "Okay... We can do this, but we can't let anyone know! And we aren't, like, a couple, okay?"
        the_person.char "You're still my brother, we just... Do other things together. Understand?"
        mc.name "Sure thing sis."


    else:
        the_person.char "I can't believe we are really doing this... Is it wrong? Should we stop?"
        mc.name "What do you think? Do you want to stop?"
        "She bites her lip and shakes her head."
        the_person.char "No. I want to see what it feels like."
        mc.name "What do you want to feel?"
        the_person.char "Stop teasing me [the_person.mc_title]! I want to feel your... cock inside me."
        mc.name "That's a good girl. Well, let's give it a try!"
    return

label lily_anal_sex_taboo_break(the_person):
    if the_person.love > 60:
        the_person.char "Wait, do you really mean you want to try anal?"
        if the_person.has_taboo("vaginal_sex"):
            mc.name "Yeah, I do. I want to have sex, but you probably don't want me fucking your pussy yet."
            the_person.char "Ever. That would be actual, full incest [the_person.mc_title]."
            mc.name "Exactly, so we can cheat a little like this."
            "[the_person.possessive_title] seems unsure."
            mc.name "Come on, don't you want to experiment with someone you trust?"
        else:
            mc.name "Yeah, why not? I've already fucked all of your other holes, what's special about this one?"
            the_person.char "It's not special, I just thought you'd want to fuck my pussy some more. Didn't you enjoy it last time."
            mc.nmae "It was great, but I want to experiment a little more. Come on, don't you want to try something new?"

    else:
        the_person.char "Wait, do you want to try anal?"
        mc.name "Yeah, I do. You've got a cute butt."
        if the_person.has_taboo("vaginal_sex"):
            the_person.char "You're crazy [the_person.mc_title]! We're related, we shouldn't  be fucking!"
            mc.name "It's not like it's real sex. If you want I can go to town on your pussy though, it looks just as tight."
            the_person.char "I guess anal isn't as bad as my own brother fucking my pussy..."


        else:
            the_person.char "What's wrong with my pussy? Didn't you enjoy it last time?"
            mc.name "It was great, I just want to try something new. Come on, you like experimenting, right?"
            the_person.char "I guess this way I don't have to worry about you pulling out..."

    "She sighs and gives in."
    the_person.char "Okay, but you need to be gentle with me."
    mc.name "I promise I will. Have you ever tried this before?"
    the_person.char "With toys a couple of times... Never with a guy."
    mc.name "You'll probably be really tight then. I'll go nice and slow to give you time to stretch out."
    the_person.char "Okay. Thank you [the_person.mc_title]."


    return

label lily_condomless_sex_taboo_break(the_person):
    the_person.char "I don't like condoms either, but we need to be careful. What would we tell Mom if you got me pregnant?"
    if the_person.has_taboo("vaginal_sex"):
        mc.name "We won't need to tell her anything. I'm not going to get you pregnant the very first time we have sex."
        "[the_person.possessive_title] still seems uncertain."
        mc.name "Come on [the_person.title], don't you want our first time to be special? I promise I'll pull out."
        the_person.char "Since it's our first time... Okay, as long as you are really careful when you're going to cum."

    else:
        mc.name "We won't need to tell her anything. I'm not going to get you pregnant the very first time we fuck raw."
        "[the_person.possessive_title] still seems uncertain."
        mc.name "Come on [the_person.title], don't you trust me? It will feel so much better without a condom."
        the_person.char "Okay, fine. But you need to be {i}really{/i} careful not to cum in me."
    mc.name "I promise I'll be careful. Ready?"
    "She gives you a nervous nod."
    return

label lily_underwear_nudity_taboo_break(the_person, the_clothing):
    the_person.char "Oh my god, I can't believe you want to see your own sister in her underwear!"
    mc.name "Come on, we're family. There's nothing to be shy about."
    "She rolls her eyes and shrugs."
    the_person.char "Fine. You're so strange sometimes."
    return

label lily_bare_tits_taboo_break(the_person, the_clothing):
    the_person.char "Hey, why are you playing with my [the_clothing.display_name]?"
    mc.name "I want to take it off."
    "[the_person.possessive_title] seems equal parts embarrassed and excited."
    the_person.char "Oh my god, you want to look at your sisters boobs? Do you... think they're cute?"
    if not the_person.has_large_tits():
        the_person.char "I hoped they would be big like [mom.title]'s, but I don't think that's going to happen."
    mc.name "They look great, let's take a closer look..."
    "She stands passively as you take off her [the_clothing.display_name]."
    return

label lily_bare_pussy_taboo_break(the_person, the_clothing):
    the_person.char "Hey, what are you doing? If you take off my [the_clothing.display_name] you'll be able to see my... Pussy."
    "[the_person.possessive_title] seems excited rather than scared of the idea, but needs a little more convincing."
    if the_person.has_taboo("touching_vagina"):
        mc.name "Come on [the_person.title], I saw it when we were kids and it wasn't a big deal."
        the_person.char "Yeah, but you never looked at me like... This."
        mc.name "We've both grown up, but I've always thought you were beautiful. I can appreciate you as a woman now, not just as my sister."
        "She sighs and nods."
        the_person.char "Okay, just a quick look. That can't be too wrong, right?"
        mc.name "Yeah, right."
    else:
        mc.name "Come on [the_person.title], I've already felt up your pussy. What do you have left to hide?"
        the_person.char "Fine. Just a little look won't be too bad, right?"

    "She stands passively and lets you pull down her [the_clothing.display_name]."

    # the_person.char "Careful there [the_person.mc_title], mommy doesn't want you to be able to see her delicate parts."
    # mc.name "Please [the_person.title], I want to know what it looks like."
    # if the_person.has_taboo("touching_vagina"):
    #     the_person.char "Just what it looks like?"
    #     mc.name "I've always been curious. I saw it when I was younger but I didn't really understand what it was for."
    #     the_person.char "I suppose you should be able to ask any questions you have to someone you trust..."
    #     "She thinks for a moment, then nods."
    #     the_person.char "Fine, you can take off my [the_clothing.display_name]. If you need me to explain anything you just ask, okay?"
    #
    # else:
    #     mc.name "You've already let me touch it, so why can't I look at it?"
    #     the_person.char "I suppose we have already crossed that line... Okay, you can take off my [the_cloting.display_name]."
    #     the_person.char "If you have any questions about my... vagina, you just ask, alright?"
    #
    # mc.name "Okay [the_person.title], I will."
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
# label lily_creampie_taboo_break(the_person):
#
#     return
#
# label lily_anal_creampie_taboo_break(the_person):
#
#     return
