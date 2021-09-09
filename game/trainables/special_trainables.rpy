# Holder for all of the special trainables, which generally require a few different requirements to be met before they can be chosen.
init -2 python:
    def train_breeder_requirement(the_person):
        if persistent.pregnancy_pref == 0:
            return False
        elif the_person.has_role(breeder_role) or the_person.event_triggers_dict.get("preg_knows", False):
            return False
        elif the_person.get_known_opinion_score("creampies") == 2 and the_person.get_known_opinion_score("bareback sex") == 2:
            return True
        elif the_person.get_known_opinion_score("creampies") > 0 or the_person.get_known_opinion_score("bareback sex") > 0:
            return "Loves Creampies and Bareback Sex"
        else:
            return False

    def train_hypnotic_orgasm_requirement(the_person):
        if the_person.has_role(hypno_orgasm_role):
            return False
        elif the_person.suggestibility < 50:
            return False
        elif the_person.arousal < 1.0*the_person.arousal/the_person.max_arousal:
            return ">50% Suggestiblity, >50% Arousal"
        else:
            return True

    def train_online_attention_whore_requirement(the_person):
        if the_person.event_triggers_dict.get("insta_known", False) and the_person.event_triggers_dict.get("dikdok_known", False) and the_person.event_triggers_dict.get("onlyfans_known", False):
            return False #No point doing it if she already has all three and you know about them.
        elif the_person.get_known_opinion_score("showing her tits") >= 1 and the_person.get_known_opinion_score("showing her ass")>= 1 and the_person.get_known_opinion_score("skimpy outfits") >= 1:
            return True
        elif the_person.get_known_opinion_score("showing her tits") > 0 or the_person.get_known_opinion_score("showing her ass") > 0 or the_person.get_known_opinion_score("skimpy outfits") > 0:
            return "Likes Showing her Tits, Ass, and Skimpy Outfits"
        else:
            return

label train_breeder_label(the_person):
    mc.name "I've got something to talk to you about [the_person.title]."
    "She nods and listens attentively."
    mc.name "I know that there are two things you love more than anything else. Do you know what those are?"
    the_person "Ummm, I don't know..."
    if the_person.relationship != "Single":
        $ so_title = SO_relationship_to_title(the_person.relationship)
        the_person "Maybe my [so_title]?"
        mc.name "Not even close. What to know what they are"
    elif the_person.has_role(girlfriend_role) or the_person.has_role(affair_role):
        the_person "Maybe you?"
        mc.name "That's very sweet, but no, even more than me. Want to know what they are?"
    else:
        "[the_person.possessive_title] tries to summon up an answer, but her cum-addled brain can't quite come up with anything."" "
        mc.name "Want to know what they are?"
    "She nods, curious."
    mc.name "First, you love taking raw cock right in your tight little fertile pussy."
    $ the_person.change_arousal(10)
    if the_person.effective_sluttiness() > 50:
        "[the_person.title] doesn't argue, she just nods in agreement and stares into your eyes."
    else:
        the_person "No... I..."
        mc.name "You can't lie to me, I can see it all over your face."
        "She blushes, but doesn't object."
    mc.name "Nothing wrong with some risky sex, except..."
    mc.name "You also love getting that same little pussy flooded with cum, don't you?"
    $ the_person.change_arousal(10)
    if the_person.effective_sluttiness() > 50:
        "She bites her lip and moans in agreement."
    else:
        the_person "What? No..."
        "Even she can tell her denial is weak."
    "[the_person.possessive_title] crosses her legs and squirms a little, obviously suddenly eager for some pleasure."
    mc.name "So what do you think is going to happen if you keep that up? If your vulnurable little cunt keeps getting creampied?"
    $ the_person.change_arousal(10)
    the_person "I don't know..."
    "You can't tell if she's faking ignorance, or if it's just the cum-trance making her agreeable."
    mc.name "Yes you do. Tell me what's going to happen."
    the_person "I'm going to get..."
    the_person "Pregnant."
    "She closes her eyes for a moment and presses her thighs together desperately."
    mc.name "How does that make you feel?"
    if the_person.kids == 0:
        the_person "Scared... I've never been pregnant before, how will I know what to do?"
    elif the_person.has_role(girlfriend_role) or the_person.has_role(affair_role):
        the_person "Excited... As long as I'm making babies with you I'm happy."
    elif the_person.relationship != "Single":
        the_person "Excited... My [so_title] doesn't understand what it's like to want something so badly!"
    else:
        the_person "Scared... What will I do when I'm pregnant and all by my self?"

    mc.name "Your body wants to get knocked up. It knows that's what it was made for."
    mc.name "Every bit of pleasure you feel drives you towards that single, basic objective."
    "She nods, agreeing with your every word now."
    mc.name "Then why are you stopping it?"
    the_person "What? I'm not..."
    mc.name "Every minute you spend without cum dripping between your legs is wasted potential."
    the_person "Every minute?"
    mc.name "Every minute. You want to get knocked up."
    "[the_person.possessive_title] nods and repeats."
    the_person "I want to get knocked up."
    mc.name "You want to get fucked, creampied, and knocked up. You're just a sow for breeding."
    "She shivers with pleasure at the thought."
    "You continue to impress upon her how much she will enjoy getting pregnant, being pregnant, and getting pregnant again."
    "When you're finished it seems to be all she can think about."

    call manage_bc(the_person, start = False) #Stop taking birth control if you were before.
    $ the_person.add_role(breeder_role)
    return

label train_hypnotic_orgasm(the_person):
    mc.name "There's something I want to talk to you about."
    "[the_person.possessive_title] nods and listens attentively."
    mc.name "I can tell you're turned on right now. Don't you want to cum?"
    if the_person.effective_sluttiness() < 50:
        "She shakes her head, but it's a poor attempt at hiding her true feelings."
        the_person "What? No, of course not..."
        mc.name "Don't lie to me, I can tell."
        "She blushes and looks away"
    else:
        "She nods her head slightly, like a child admitting some wrong doing."

    mc.name "I want you to make yourself cum."
    if mc.location.get_person_count() > 1:
        the_person "Right here? There are people around..."
        mc.name "Forget about them. If you're quiet nobody else will notice."
    elif the_person.love < 40:
        the_person "Right in front of you? I don't know..."
        mc.name "Forget about me, this is about what you want. You want to cum."
    else:
        the_person "Right now? I don't know..."
        mc.name "Why not right now? Come on, you know you want to do it."
    "She thinks about it for a moment. Her trance makes the outcome all but guaranteed."
    the_person "Okay, I'll do it."

    $ the_clothing = the_person.outfit.get_lower_top_layer()
    if the_clothing:
        $ clothing_phrase = "a hand between her legs and under her [the_clothing.display_name]."
    else:
        $ clothing_phrase = "a hand between her legs."
    if mc.location.get_person_count() > 1:
        "She glances around, making sure nobody is paying attention to her, then slips [clothing_phrase]."
    else:
        "She hesitates for one last moment, then all resistance breaks down and she slips [clothing_phrase]"

    $ the_person.change_arousal(10)
    $ mc.change_locked_clarity(20)
    "You watch as she touches herself, gently petting her pussy."
    mc.name "Good. Now I want you to focus on one thing as you make yourself cum."
    the_person "Hmm? What should I focus on?"
    $ the_word = renpy.input("Pick her trigger word.")
    while not the_word or " " in  the_word:
        $ the_word = renpy.input("Pick her trigger word.")
    $ the_person.event_triggers_dict["hypno_trigger_word"] = the_word
    "You lean very close to [the_person.possessive_title] and whisper \"[the_word]\" into her ear."
    mc.name "Focus on that as you touch yourself. All that pleasure you're feeling, all that pent up desire..."
    mc.name "Focus it all onto that one word. You won't cum until you hear it."
    "[the_person.title] fingers herself a little faster."
    $ the_person.change_arousal(10)
    "You guide her closer and closer to her orgasm, whispering reminders in her ear that she can't cum until she hears her trigger word."
    $ the_person.change_arousal(the_person.max_arousal-the_person.arousal)
    "Soon enough she is panting quietly, thighs pressed tight around her own hand."
    the_person "I'm so close! I'm going to... I'm going to..."
    "She moans desperately, on the edge of climax but unable to push herself over it."
    $ mc.change_locked_clarity(20)
    the_person "[the_person.mc_title], I can't cum!"
    menu:
        "Make her cum.":
            mc.name "I can help with that. Ready?"
            "She nods frantically."

        "Play with her a little.":
            mc.name "Hmm, I don't know what I could do to help with that."
            the_person "The word... Say the word!"
            $ mc.change_locked_clarity(20)
            "She gasps and twitches, hanging uncomfortably at the edge of climax."
            mc.name "Which word was that again?"
            the_person "[the_word]! I need you to say it! Just say it!"

    "You lean close and whisper right into her ear."
    mc.name "[the_word]"
    $ the_person.draw_person(emotion = "orgasm")
    $ mc.change_locked_clarity(30)
    "The results are immediate. [the_person.possessive_title] spasms, bucking her hips and gasping for breath."
    the_person "Oh god! Ah! Ah!"
    "Her orgasm is so intense that her knees buckle and she starts to collapse to the ground."
    menu:
        "Catch her.":
            "You slide an arm around [the_person.title] and hold her up as she cums her brains out. She clings to you on instinct with her free hand."
            "Meanwhile, her other hand doesn't stop pumping in and out of her climaxing cunt."
            $ the_person.run_orgasm()
            $ the_person.change_love(2)
            $ the_person.reset_arousal()
            "She gasps and moans into your ear for a long moment, but little by little her orgasm subsides."
            "When she is in control of herself again she stands under her own power and looks at you, a dumb smile spreading across her face."

        "Let her fall.":
            "You step back and let her cliamx run its course."
            $ the_person.draw_person(position = "doggy", emotion = "orgasm")
            "[the_person.title] falls to the ground, barely catching herself at the last minute with her free hand."
            "She ends up face down, hips bucking with each new climactic spasm. Her thighs twitch in sync, all while she continues to finger herself."
            $ the_person.run_orgasm()
            $ the_person.reset_arousal()
            $ the_person.change_slut(2)
            "She moans and writhes on the floor for a long moment, but little by little her orgasm subsides and she gains control of herself again."
            $ the_person.draw_person(position = "missionary", emotion = "happy")
            "[the_person.possessive_title] rolls over and looks up at you, a dumb smile spreading across her face."

    the_person "That was so intense... Do it again."
    $ the_person.draw_person()
    "You spend some more time with [the_person.possessive_title], reinforcing the strength of her trigger word."
    "When you're finished you feel confident you can use it to make her cum on command."
    $ the_person.add_role(hypno_orgasm_role)
    return

label train_online_attention_whore(the_person):
    mc.name "I've got a question for you [the_person.title]."
    "She nods and waits for you to continue."
    mc.name "There are a ton of social media sites online. Do you have accounts on any of them?"
    $ set_something_up = False
    if the_person.has_role(instapic_role) or the_person.has_role(dikdok_role) or the_person.has_role(onlyfans_role):
        "She nods again."
        the_person "Yeah, I've signed up for those sorts of sites."
        mc.name "Tell me what your username is so I can add you..."
        "In her trance all she can do is nod and tell you what you want to know."
        if the_person.has_role(instapic_role):
            the_person "You can find me on InstaPic here..."
            $ the_person.event_triggers_dict["insta_known"] = True
            "She gives you her InstaPic name, so you can look her up later."
        if the_person.has_role(dikdok_role):
            the_person "I'm on DikDok, here's my profile name..."
            $ the_person.event_triggers_dict["dikdok_known"] = True
            $ mc.change_locked_clarity(10)
            "She gives you the name of her DikDok account. You wonder what sorts of things she's been posting lately."
        if the_person.has_role(onlyfans_role):
            the_person "I've got an OnlyFanatics account, you can find me here..."
            $ the_person.event_triggers_dict["onlyfans_known"] = True
            $ mc.change_locked_clarity(20)
            "She gives you her OnlyFanatics screen name. You're very interested in what sort of content she's been posting."

    else:
        "She shakes her head."
        if the_person.age < 40:
            the_person "No, I've never really seen the point."
        else:
            the_person "No, I'm too old to understand any of those sites."

    if not the_person.has_role(instapic_role):
        menu:
            "Make her an InstaPic account.":
                $ set_something_up = True
                mc.name "Everyone has an InstaPic account these days."
                mc.name "Let's set one up for you."
                the_person "Do you really think I need one?"
                mc.name "Of course you do! The world deserves to see you!"
                "She shrugs and pulls out her phone. You guide her to InstaPic and make sure she set up her account correctly."
                $ the_person.add_role(instapic_role)
                $ the_person.event_triggers_dict["insta_known"] = True
                "You also make sure to make note of her account name so you can look it up later."
                mc.name "Great, all done. I hear doing clothing reviews are popular, especially really slutty stuff."
                mc.name "You'd like to dress up like a slut for people online, right?"
                "[the_person.possessive_title] blushes and shrugs, but it's clear the answer is yes."

            "Skip InstaPic.":
                pass
    if not the_person.has_role(dikdok_role):
        menu:
            "Make her a DikDok account.":
                $ set_something_up = True
                mc.name "You'll absolutely need a DikDok account."
                the_person "Really? What's special about DikDok?"
                mc.name "It's a place you can post videos of doing whatever you want."
                mc.name "The moderation is really bad too, so you can post almost anything."
                the_person "Oh..."
                "She doesn't say anything, but seems to be considering the implications."
                "You speed up the process and cut to the chase."
                mc.name "That means you can show off your tits to the internet."
                the_person "Really? And I won't get in trouble?"
                mc.name "Oh yeah, everyone is doing it."
                "You're exaggerating, but only a little."
                the_person "Huh, I didn't have any idea..."
                "She does now, and it's clear she likes it."
                $ the_person.add_role(dikdok_role)
                $ the_person.event_triggers_dict["dikdok_known"] = True
                "You walk her through getting her account set up."
                "Of course you make note of the name so you can look up her content later."

            "Skip DikDok.":
                pass


    if not the_person.has_role(onlyfans_role):
        menu:
            "Make her an OnlyFanatics account.":
                $ set_something_up = True
                mc.name "Most importantly of all, you're going to need an OnlyFanatics account."
                if the_person.age < 40:
                    the_person "You really think I need a porn site?"
                    mc.name "Obviously you do! You're fucking hot, you might as well make some money from it."
                    "She thinks about this for a moment."
                    the_person "Well, I guess it could be a little bit of fun..."
                    the_person "Maybe I can just post some topless shots."
                    mc.name "That's a good start. If you like it you can just keep going."
                    "[the_person.possessive_title] blushes and shrugs."


                else:
                    the_person "I've never heard of that site, what is it for?"
                    mc.name "It's a place you can post pictures and videos of yourself, doing whatever you want."
                    mc.name "Then other people can pay for access to that content."
                    "[the_person.possessive_title] doesn't seem to immediately understand, so you keep explaining."
                    mc.name "Hot women like you will post naked pictures, videos of them stripping, or even of them getting fucked."
                    the_person "Oh... Oh!"
                    the_person "But I don't know if I want to get into porn..."
                    mc.name "It's nothing like that, this is more like freelance work. It's all online, and it can be totally anonymous if you want it to be."
                    "She considers this for a long while."
                    the_person "All I have to do is take some naked pictures and men will pay me for them?"
                    mc.name "Yeah, you've got the basic idea. Once you're comfortable with that you can just keep going."


                the_person "Maybe..."
                $ the_person.add_role(onlyfans_role)
                $ the_person.event_triggers_dict["onlyfans_known"] = True
                "You walk her through the process of setting up her account."
                "The last step is a verification picture of [the_person.title]."
                menu:
                    "They need a picture.":
                        mc.name "Last step, they need a picture with your account name in it. Here, I'll take it for you."
                        "[the_person.title] scribbles her screen name onto a piece of paper and holds it in front of her while you take the shot."
                        "You make note of the account name yourself so you can look up what she posts later."

                    "They need a picture of your tits.":
                        mc.name "Last step, they need a picture with your account name and your tits in it."
                        mc.name "Here, I'll take it for you."
                        "You take [the_person.possessive_title]'s phone out of her hands before she has a chance to read the real requirements."
                        the_person "They really need that?"
                        mc.name "It's the same stuff you'll be posting later, so they can compare your boobs to be sure it's really you."
                        "You doubt such an obvious lie would normally work, but [the_person.title] is {i}very{/i} easy to convince right now."
                        "She shrugs and nods."
                        the_person "Okay, let's get this done!"
                        if the_person.outfit.can_half_off_to_tits():
                            $ strip_list = the_person.outfit.get_half_off_to_tits_list()
                            $ generalised_strip_description(the_person, strip_list, half_off_instead = True)
                        else:
                            $ strip_list = the_person.outfit.get_tit_strip_list()
                            $ generalised_strip_description(the_person, strip_list)

                        $ mc.change_locked_clarity(20)
                        "Tits exposed, she scribbles her account name onto a piece of paper and holds it in front of her."
                        the_person "Is this right?"
                        mc.name "Perfect, just one second..."
                        "You take a moment to enjoy the view, then take a picture and submit it along with the rest of her profile information."
                        "You hope some OnlyFanatics customer service rep enjoys the surprise."
                        $ the_person.review_outfit()


            "Skip OnlyFanatics.":
                pass

    if set_something_up:
        mc.name "There, now you can be a proper twenty-first century slut."
        mc.name "Tell me, are you excited to shake that ass for the internet?"
        if the_person.sluttiness < 30:
            "[the_person.possessive_title] shrugs, pretending not to be interested."
            the_person "A little, I guess."
        else:
            the_person "Honestly? Yeah, it sounds like a lot of fun."

        mc.name "Good, because you're built for it. You're going to have guys drooling all over the world."
        "You spend a little longer reminding her to post as often as she can, and make a mental note to check in on her progress yourself."
    else:
        "You reconsider putting [the_person.possessive_title] on the internet for other men to oggle at."
        return False #You didn't actually set anything up, so you don't have to pay the training cost (you get the account info for free, congrats)

    return
