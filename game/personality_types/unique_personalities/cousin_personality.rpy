### PERSONALITY CHARACTERISTICS ###
init 1300:
    python:
        def cousin_titles(the_person):
            valid_titles = []
            valid_titles.append(the_person.name)
            if the_person.love > 20:
                valid_titles.append("Cuz")

            if the_person.love < -30:
                valid_titles.append("Hellspawn")
            return valid_titles

        def cousin_possessive_titles(the_person):
            valid_possessive_titles = []
            valid_possessive_titles.append(the_person.name)
            valid_possessive_titles.append("Your cousin")
            if the_person.love > 20:
                valid_possessive_titles.append("Your cuz")

            if the_person.love < -30:
                valid_possessive_titles.append("Your bitchy cousin")

            if the_person.sluttiness > 40:
                valid_possessive_titles.append("Your cock-goth cousin")

            return valid_possessive_titles

        def cousin_player_titles(the_person):
            valid_player_titles = []
            valid_player_titles.append(mc.name)
            if the_person.love < -20:
                valid_player_titles.append("Asshat")
                valid_player_titles.append("Dickwad")
                valid_player_titles.append("Dick-for-brains")

            if the_person.love > 20:
                valid_player_titles.append("Cuz")

            if the_person.love < 0 and the_person.sluttiness > 40:
                valid_player_titles.append("Dildo")

                if the_person.obedience < 20:
                    valid_player_titles.append("Cock slave")
                    valid_player_titles.append("Slave")
            return valid_player_titles

        cousin_personality = Personality("cousin", default_prefix = "introvert",
            common_likes = ["the colour black","heavy metal","punk","makeup","skimpy outfits"],
            common_sexy_likes = ["lingerie","masturbating","taking control","getting head"],
            common_dislikes = ["small talk","flirting","working"],
            common_sexy_dislikes = ["kissing", "giving blowjobs", "bareback sex"],
            titles_function = cousin_titles, possessive_titles_function = cousin_possessive_titles, player_titles_function = cousin_player_titles)

### DIALOGUE ###
label cousin_flirt_response_low(the_person):
    #You've salvaged your relationship with her if your love is this high.
    "[the_person.possessive_title] seems caught off guard by the compliment."
    the_person.char "Uh, wow. Thanks, I guess. It's not like it's anything special."
    mc.name "Well it turns out you can look cute without even trying."
    "She laughs and rolls her eyes."
    the_person.char "You're weird, you know that?"
    return

label cousin_flirt_response_mid(the_person):
    if the_person.effective_sluttiness("underwear_nudity") < 20: #Not very slutty, so it must be high love.
        the_person.char "Oh my god, can you stop perving on me for, like, two seconds?"
        mc.name "What? Don't you want to know when you're looking good?"
        "She sighs and rolls her eyes."
        the_person.char "Whatever, it's fine I guess. Thanks."
    else:
        the_person.char "Oh yeah? You're really checking out your own cousin, huh?"
        "She runs her hands down her hips, outlining the shape of her body."
        the_person.char "That's so wrong, but you know that. I bet you're getting turned on, just from looking at me."
        $ the_person.draw_person(position = "back_peek")
        "[the_person.possessive_title] turns around and leans forward, sticking her butt towards you and wiggling it."
        the_person.char "Is this what you wanted to see?"
        mc.name "It's a good start."
        $ the_person.draw_person()
        "She turns back to you and smiles mischievously."
        the_person.char "Keep being a good boy and maybe you'll get to see more."
    return

label cousin_flirt_response_high(the_person):
    if mc.location.get_person_count() == 1: #If you are alone she'll flirt with you
        if the_person.effective_sluttiness() > (25 - the_person.get_opinion_score("incest")*5): # High sluttiness flirt
            the_person.char "Oh I'm sorry, am I turning you on with my big, juicy tits?"
            $ the_person.draw_person(the_animation = blowjob_bob)
            "[the_person.possessive_title] grabs her boobs and bounces them up and down for you."
            mc.name "I mean... Yeah."
            "She smiles and squeezes down on her own breasts."
            the_person.char "Good, I like having that kind of power over you."
            menu:
                "Kiss her.":
                    mc.name "Yeah? How do you like this?"
                    $ the_person.draw_person()
                    if the_person.has_taboo("kissing"):
                        "You put an arm around her waist and pull her close. She hesitates and leans away just before you kiss her."
                        $ the_person.call_dialogue("kissing_taboo_break")
                        $ the_person.break_taboo("kissing")
                        "You kiss her, and after a moment of hesitation she kisses you back."
                    else:
                        "You put your arm around her waist and kiss her. She hesitates for a moment, then leans her body eagerly against yours."
                    call fuck_person(the_person, private = True, start_position = kissing, skip_intro = True) from _call_fuck_person_53

                "Just flirt.":
                    mc.name "Yeah? What are you planning to do with that power?"
                    the_person.char "If I told you it would ruin the surprise. Don't worry, I promise I'm only going to use it for evil."
                    "She winks and lets go of her tits. It takes a second before they stop jiggling completely."
                    $ the_person.draw_person()

        else: # Just high love flirt
            "She laughs and rolls her eyes."
            the_person.char "How likely am I to strip for my cousin? Pretty close to zero."
            mc.name "So you're saying there's a chance?"
            the_person.char "Oh my god, you're the worst. It's kind of fun knowing I have this effect on you."
            "She sways her hips side to side, accentuating her curves."
            the_person.char "But no, I don't think you have much of a chance."


    else: #She shushes you and rushes you off somewhere private.
        if the_person.effective_sluttiness() > (25 - the_person.get_opinion_score("incest")*5): #She's slutty, but you need to find somewhere private so people don't find out.
            the_person.char "Oh my god you little perv, there are people around! Keep it in your pants."
            "She glances around nervously, checking to see if anyone was listening."
            the_person.char "If you want to talk to me like that you'll have to wait until we're alone."
            menu:
                "Find someplace quiet.":
                    mc.name "I don't feel like waiting. Come on, let's sneak away."
                    the_person.char "Like, right now? Ugh, fine."
                    "You lead [the_person.possessive_title] away and find a quiet spot where you can be alone."
                    if the_person.has_taboo("kissing"):
                        "You put your arm around her and pull her close, moving to kiss her."
                        $ the_person.call_dialogue("kissing_taboo_break")
                        $ the_person.break_taboo("kissing")
                        "You kiss her, and after a moment of hesitation she kisses you back."
                    else:
                        "When you finally have some privacy you don't waste any time. You put an arm around [the_person.title] and pull her into a passionate kiss."
                    call fuck_person(the_person, private = True, start_position = kissing, skip_intro = True) from _call_fuck_person_54

                "Just flirt.":
                    mc.name "Come on, you're really going to make me wait?"
                    $ the_person.draw_person(the_animation = blowjob_bob)
                    "[the_person.possessive_title] smiles mischeviously and grabs her tits, jiggling them in front of your face."
                    the_person.char "Yeah, I am. Be a patient boy and maybe you'll get to see these later."
                    "She winks and lets go of her tits. It takes a second before they stop jiggling completely."
                    $ the_person.draw_person()

        else: #She's not slutty, so she's embarassed about what you're doing.
            the_person.char "Oh my god, you little perv."
            "She glances around nervously, checking to see if anyone was listening."
            the_person.char "Can you try and keep it in your pants when there are other people around?"
            mc.name "Relax, I'm just joking around."
            the_person.char "Uh huh? So you're telling me you don't want to play with my big, juicy tits?"
            $ the_person.draw_person(the_animation = blowjob_bob)
            "She grabs her tits and jiggles them in front of your face."
            mc.name "Well... I wouldn't say no."
            the_person.char "Yeah, that's what I thought. So let's try not to get in trouble, okay?"
            $ the_person.draw_person()
            "She legs go of her boobs and lets them drop. It takes a second before they stop jiggling completley."
            mc.name "Alright, I get it."

    return

## Taboo break dialogue ##
label cousin_kissing_taboo_break(the_person):
    the_person.char "Oh my god... Were you going to kiss me?"
    "She scoffs and turns her head away from you."
    the_person.char "As if! You're such a freak!"
    mc.name "You know what?"
    the_person.char "What?"
    mc.name "Shut up. I don't care."
    "She snaps her head back and glares at you."
    the_person.char "Aww, his balls finally dropped!"
    return

label cousin_touching_body_taboo_break(the_person):
    if the_person.love > 20: #ie. You've managed to drag her up to normal stats levels. Good!
        the_person.char "Hey, stop that you little perv."
        mc.name "Why would I stop? We both know you like it."
        the_person.char "Because you're my cousin, you nerd. My mom would flip if she knew."
        mc.name "So would mine, but they aren't going to know. When did you start caring what she thought?"
        the_person.char "I don't!"
        mc.name "Well then relax and just enjoy yourself."


    else: # She hates you and is doing this because she is either a massive slut or being commanded to.
        the_person.char "Hey! You better move that hand or I'll snap it off."
        mc.name "Don't you get tired of being a bitch? We both know you love it."
        the_person.char "Don't you ever get tired of being a pervert?"
        mc.name "Not really, no."
        the_person.char "Whatever. You're probably going to blow your load just touching me."
        mc.name "Sounds like you want to find out."
        "She sighs and rolls her eyes."
        the_person.char "You're the worst."
    return

label cousin_touching_penis_taboo_break(the_person):
    if the_person.love > 30:
        the_person.char "Oh my god, look at your cock! You're dripping precum, are you really that turned on by me?"
        "She gives you a dirty look."
        the_person.char "I'm your cousin you freak. That's so fucking wrong..."
        mc.name "Do I look like I care? You want to touch it, right?"
        "She nods silently."
        mc.name "Do it then. Wrap your hand around it and stroke me off."
    else:
        the_person.char "I bet you're desperate to have me touch your cock. Look at it, it's so hard."
        mc.name "Touch it [the_person.title]. I want you to stroke me off"
        the_person.char "God, you're so pathetic. Asking your cousin to touch your penis because you're so horny..."
        "She bites her lip and zones out for a moment, staring at your throbbing cock."
        mc.name "Come on, don't make me wait."
        "She seems to snaps out of it and glares at you."
        the_person.char "It's a shame such a nice cock ended up on a dick like you. Whatever, it's not like I'm doing this for you."
        mc.name "Sure thing, whatever helps you sleep at night."
    return

label cousin_touching_vagina_taboo_break(the_person):
    if the_person.love > 30:
        the_person.char "Hey, we shouldn't do that..."
        mc.name "So? You still want to, right?"
        "She nods her head silently."
        mc.name "Exactly. Fuck what anyone else things."
        the_person.char "You're right. Fuck 'em!"

    else:
        the_person.char "Hold it, you little fucking perv."
        mc.name "What, scared I'll notice how wet you are?"
        the_person.char "Ha! It's so cute you think you could get me wet."
        mc.name "What are scared about then?"
        the_person.char "I'm not nervous, I just don't know if you deserve to touch my pussy."
        if not the_person.has_taboo("touching_penis"):
            mc.name "You've had your hands wrapped around my cock, don't pretend to be some prissy choir girl."
            the_person.char "You should be thanking me for even touching you."

        mc.name "Oh lord, stop being such a stuck up bitch! Do you want to get fingered or not?"
        "Her confidence cracks and looks to the side nervously, shrugging."
        the_person.char "Whatever, I don't care."
        mc.name "You really do make this difficult for me, you know that?"
    return

label cousin_sucking_cock_taboo_break(the_person):
    mc.name "[the_person.title], I think it's time you finally got on your knees and sucked my cock."
    if the_person.love > 40:
        the_person.char "What the fuck [the_person.mc_title], we've taken this too far already!"
        if the_person.has_taboo("licking_pussy"):
            mc.name "Then why stop? Do you think people are going to say \"She made out with her cousin, but at least she never sucked his cock.\"?"
            "Her reluctant sigh sounds almost like a growl."
            the_person.char "You convince me to do the stupidest fucking things..."
            mc.name "But you always have a good time."
        else:
            mc.name "You didn't think it was too far when I was eating you out. It's time you repaid the favour."
            "She sighs and rolls her eyes."
            the_person.char "Ugh, fine. I can't believe I'm doing this!"

    else:
        the_person.char "What the fuck makes you think I would {i}ever{/i} put that thing in my mouth?"
        if the_person.obedience >= 120:
            mc.name "Because you're an obedient little slut who does what she's told."
        else:
            mc.name "Because you're a slut, and I know you want to."
        "She scoffs and looks away from you."
        the_person.char "You're so pathetic. You need your cousin to give you a blowjob because no other girl will come anywhere near your pathetic little dick."
        mc.name "You'll wish it was small once you're gagging on it."
        the_person.char "Whatever. It's going to feel like sucking on a toothpick, but..."
        "She smirks at you."
        the_person.char "Since you're so obviously desperate, I'll do it for you just this once."
        the_person.char "That way you have something to think about when you're jerking off in your room, all alone."
    return

label cousin_licking_pussy_taboo_break(the_person):
    if the_person.love > 40:
        the_person.char "What... What are you doing?"
        mc.name "Spread your legs, I want to lick your pussy."
        if the_person.has_taboo("sucking_cock"):
            the_person.char "Fuck, haven't we gone too far already?"
            mc.name "We have, so why stop now? You know this is going to feel amazing, right?"
            the_person.char "Sure, but..."
            "She leans her head back and sighs."
            the_person.char "Fine! You convince me to do the stupidest things."
            mc.name "You always have a good time though, don't you?"
            the_person.char "...Yeah."
        else:
            "[the_person.possessive_title] hesitates."
            mc.name "You've sucked my cock already, I want to do the same for you."
            the_person.char "Whatever, I guess if you want to..."

    else:
        the_person.char "You look good on your knees, but what the {i}fuck{/} are you doing?"
        if the_person.has_taboo("sucking_cock"):
            mc.name "I'm going to eat you out. Are you really going to complain about getting head?"
            the_person.char "Oh my god, this is amazing. You're so pathetic you want to lick my pussy just so you can touch a real girl."
            "She laughs condesendingly."
            the_person.char "Alright then, let's see if you're any good at this."

        else:
            mc.name "Are you always an bitch when a guy is about to eat you out?"
            the_person.char "Oh, just for you. Well then, what are you waiting for?"
    return

label cousin_vaginal_sex_taboo_break(the_person):
    if the_person.love > 60:
        the_person.char "Fuck... So we're really doing this, huh?"
        mc.name "We can stop if you want, but I don't think you really want to."
        "She bites her lip and shakes her head."
        the_person.char "What are you waiting for then, an invitation?"
        mc.name "It wouldn't hurt."
        "She gives a melodramatic sigh>"
        the_person.char "Just hurry up before someone walks in on us and I have to flee the country from embarrassment."

    else:
        the_person.char "This is so fucking dumb... How did I end up here, with {i}you{/i} of all people?"
        mc.name "Tell me you want it."
        the_person.char "What?"
        mc.name "Tell me that you want me to fuck you. Or do you want to get dressed and leave?"
        "She gives a defeated sigh."
        the_person.char "No, I've put up with enough of your shit that I should at least get laid."
        mc.name "So what do you say?..."
        the_person.char "You ass. Fine: I want you to fuck me [the_person.mc_title]. Fuck my tight little snatch and make me cum."
        mc.name "There, that wasn't so hard."
    return

label cousin_anal_sex_taboo_break(the_person):
    if the_person.love > 60:
        if the_person.has_taboo("vaginal_sex"):
            the_person.char "Jesus, really? Fuck, that's a big step."
            mc.name "I could slip into your pussy if you prefer."
            "She shakes her head."
            the_person.char "I'm not going to have sex with my cousin, no matter how hopelessly turned on I get."
            mc.name "But anal is on the table? Seems a little arbitrary."
            the_person.char "Anal doesn't count, alright. It's just... I don't know, it's just different."
            mc.name "Alright, well I'm not going to argue with you. Ready?"
            the_person.char "As ready as I'll ever be..."


        else:
            the_person.char "What is it with men and anal? Don't you like my pussy?"
            mc.name "Come on, where's your sense of adventure?"
            "She sighs dramatically."
            the_person.char "Ugh, fine. Why do I put up with you?"
            mc.name "Here, let me show you why."
    else:
        the_person.char "Jesus, you don't fuck around do you... Obviously no, I'm not letting you fuck my ass."
        mc.name "Why not? Scared you won't be able to take it?"
        if the_person.has_taboo("vaginal_sex"):
            the_person.char "No, you idiot, because you're my cousin and that's fucked up!"
            if the_person.has_taboo("sucking_cock"):
                mc.name "You're already naked, and I can see you're wet just thinking about getting pounded. We passed the \"fucked up\" line a long time ago."
            else:
                mc.name "You've sucked my cock, I think we passed the \"fucked up\" line a long time ago."
            the_person.char "Ugh, fuck... Fine, fucking fine... But don't think this is going to be a normal thing, okay?"
            the_person.char "I'm just really fucking horny, and at least you can't get me pregnant fucking my ass."
        else:
            the_person.char "Why does every single guy want to try anal? Can't you just fuck me normally."
            mc.name "Oh come on, where's your sense of adventure? Take a deep breath, you'll be fine."
            the_person.char "Ugh. Fuck you."
            mc.name "Love you too."
    return

label cousin_condomless_sex_taboo_break(the_person):
    if the_person.love > 60:
        if the_person.has_taboo("vaginal_sex"):
            the_person.char "You want to take me bareback our very first time, huh?"
            mc.name "Why not? Afraid I'm going to get you knocked up?"
            if the_person.on_birth_control:
                the_person.char "As if. That's why I'm on the pill."
                mc.name "So you can fuck your cousin?"
                "She groans and rolls her eyes."
            else:
                the_person.char "You better not, or you'll be the one telling both of our moms."
                mc.name "Wait, are you on the pill?"
                the_person.char "Obviously not, or I wouldn't be worried."

        else:
            if the_person.on_birth_control:
                the_person.char "Me too. Fuck it, I'm on the pill so why not?"
            else:
                the_person.char "Me too, but we need to be really careful if you're going to take me bareback. I'm not on birth control."
                mc.name "Fine, I'll pull out."
            the_person.char "You better. If you get me prengant you're going to be the one to tell both of our moms."
        the_person.char "Come on, hurry up and fuck me before I realise this is a bad idea."

    else:
        if the_person.has_taboo("vaginal_sex"):
            the_person.char "Hell no! You're probably going to cum as soon as you're inside me."
            mc.name "You want to feel it raw too though, right?"
            the_person.char "That's not the point [the_person.mc_title], I don't want you getting me fucking pregnant!"
            mc.name "So I'll pull out. Come on, it's our first time."
        else:
            the_person.char "Hell no! You're probably going to cum as soon as you're inside me."
            mc.name "You want to feel it raw too though, right?"
            the_person.char "That's not the point [the_person.mc_title], I don't want you getting me fucking pregnant!"
            mc.name "So I'll pull out. Come on, we both already know where this is going."
        "She thinks for a long moment, then sighs and nods."
        if the_person.on_birth_control:
            the_person.char "Fine... But I swear to God if you don't pull out..."
        else:
            the_person.char "Fine, but I'm not on the pill so you better be damn sure to pull out. If you don't, I swear to God..."
        mc.name "What, you'll tell your Mom that you're banging your own cousin? You might want to think of a better threat than that."
        the_person.char "Ugh, whatever. Just hurry up and fuck me."
    return

label cousin_underwear_nudity_taboo_break(the_person, the_clothing):
    the_person.char "You're such a freak. You really want to see me in my underwear?"
    "She shakes her head and sighs."
    the_person.char "Whatever. Hurry up."
    return

label cousin_bare_tits_taboo_break(the_person, the_clothing):
    the_person.char "Whoa, wait up there. Did you really think I going to let you take off my [the_clothing.display_name]?"
    "She shakes her head and laughs condescending."
    if the_person.has_large_tits():
        the_person.char "Oh no, these big, juicy tits aren't for you to enjoy."
    else:
        the_person.char "Oh no, my tits aren't for you to enjoy."
    mc.name "Why not? Are you too scared, or are they malformed or something?"
    "She stares daggers at you."
    the_person.char "No I'm not scared, and my tits are perfect for your information. I bet you've never even gotten to real boobs before. Pathetic."
    "You let her keep talking. It seems like she's convincing herself rather than you."
    the_person.char "You know what, fine. I'll let you see my tits, but only so you know what you're missing out on."
    "[the_person.possessive_title] gives you an arogant smile, as if she's somehow won."
    the_person.char "Well, what are you waiting for?"
    return

label cousin_bare_pussy_taboo_break(the_person, the_clothing):
    the_person.char "You want to take off my [the_clothing.display_name]?"
    the_person.char "You really want to see a pussy that badly? You can't find anyone other than your cousin to gawk at?"
    if the_person.has_taboo("touching_vagina"):
        "She shakes her head and sighs."
        the_person.char "That's so sad. You know what?"
        "She puts her hands on her hips."
        the_person.char "Fine. I bet you get one look at it and panic, because you've never been this close to a real girl before."

    else:
        mc.name "You're acting real high and mighty for someone who got fingered by that same cousin. Just shut up and let me get naked."
        "She rolls her eyes."
        the_person.char "Whatever. You're probably going to cum just looking at me. It's actually really sad."
    return

# label cousin_facial_cum_taboo_break(the_person):
#
#     return
#
# label cousin_mouth_cum_taboo_break(the_person):
#
#     return
#
# label cousin_body_cum_taboo_break(the_person):
#
#     return
#
# label cousin_creampie_taboo_break(the_person):
#
#     return
#
# label cousin_anal_creampie_taboo_break(the_person):
#
#     return