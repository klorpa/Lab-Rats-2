init:
    python:
        against_wall = Position(name = "Against the Wall", slut_requirement = 60, slut_cap = 80, requires_hard = True, requires_large_tits = False,
            position_tag = "against_wall", requires_location = "Lean", requires_clothing = "Vagina", skill_tag = "Vaginal",
            girl_arousal = 20, girl_energy = 16,
            guy_arousal = 18, guy_energy = 16,
            connections = [],
            intro = "intro_against_wall",
            scenes = ["scene_against_wall_1","scene_against_wall_2","scene_against_wall_3"],
            outro = "outro_against_wall",
            transition_default = "transition_default_against_wall",
            strip_description = "strip_against_wall", strip_ask_description = "strip_ask_against_wall",
            orgasm_description = "orgasm_against_wall",
            taboo_break_description = "taboo_break_against_wall",
            opinion_tags = ["sex standing up"], record_class = "Vaginal Sex",
            default_animation = blowjob_bob,
            associated_taboo = "vaginal_sex")


        list_of_positions.append(against_wall)

#init 1:
#    python:
#        ##Here is where you would put connections if they existed.

label intro_against_wall(the_girl, the_location, the_object):
    "You put your arms around [the_girl.title] and spin her around, putting her face towards you and her back against the [the_object.name]."
    if the_girl.effective_sluttiness() > 80:
        "[the_girl.possessive_title] plants her back against [the_object.name] and watches you as you unzip your pants. She bites her lip and sighs under her breath when your cock springs out."
        the_girl.char "Mmm, what are you going to do to me?"
    else:
        "[the_girl.possessive_title] plants her back against [the_object.name] and waits patiently while you unzip your pants."
    "You get your hard cock out and rub it against [the_girl.title]'s stomach a couple of times, then line up with her pussy. She gasps softly as you slide yourself inside of her."
    return

label taboo_break_against_wall(the_girl, the_location, the_object):
    "You put your arms around [the_girl.title] and spin her around, putting her face towards you and her back against the [the_object.name]."
    if the_girl.effective_sluttiness(against_wall.associated_taboo) > against_wall.slut_cap:
        "She reaches down and rubs your hard cock against her, teasing the tip against the slit of her pussy."
    else:
        "You step even closer, letting your hard cock rub against her stomach, a bare few inches above her pussy."
    $ the_girl.call_dialogue(against_wall.associated_taboo+"_taboo_break")
    "You hold your shaft and line it up with [the_girl.possessive_title]'s warm cunt. She shivers in anticipation when your tip taps her clit."
    "You put one hand around her waist and pull her towards you as you push yourself forward."
    "After a moment of resistance your cock plunges into her warm, wet pussy."
    the_girl.char "Ah!"
    "You hold deep inside and let her adjust to your size for a few seconds, then start to glide in and out of her."
    return

label scene_against_wall_1(the_girl, the_location, the_object):
    #CHOICE CONCEPT: Fondle her tits // Kiss her
    if the_girl.arousal > 50:
        "[the_girl.title]'s cunt is nice and wet. You're able to speed up and fuck her a little faster."
    else:
        "[the_girl.title]'s cunt is tight and warm. She's still getting wet, so you take it easy on her."
    menu:
        "Fondle her tits.":
            if the_girl.has_large_tits():
                if the_girl.outfit.tits_available():
                    "You grab one of [the_girl.possessive_title]'s tits while you fuck her. Her [the_girl.tits]'s more than fill up your hand."
                    "You squeeze her breast and rub your thumb over her nipple a few time. It starts to harden in response."
                else:
                    $top_clothing = the_girl.outfit.get_upper_ordered()[-1]
                    "You cup one of [the_girl.possessive_title]'s [the_girl.tits] sized tits and fondle it through her [top_clothing.name]. It's pleasently soft and heavy in your hand."

                if the_girl.arousal < 50:
                    the_girl.char "Rub them just like that... Do you like my breasts [the_girl.mc_title]? Do you like my nice, big tits?"
                    mc.name "I love them, you have the most amazing tits."
                else:
                    the_girl.char "Ah! Go easy on them, they get really sensitive when I'm horny!"

            else:
                if the_girl.outfit.tits_available():
                    "You grab one of [the_girl.title]'s tits while you fuck her against the [the_object.name]. Her small [the_girl.tits] cups don't give much to work with, but you enjoy them all the same."
                    "You rub your thumb over her nipple a few times and watch as it starts to harden in response."
                else:
                    $top_clothing = the_girl.outfit.get_upper_ordered()[-1]
                    "[the_girl.title]'s small [the_girl.tits] cup tits don't give you much to work with, especially not with her [top_clothing.name] in the way, but you run your hand over them anyways."

                if the_girl.arousal < 50:
                    the_girl.char "Ah... Do you like my breasts [the_girl.mc_title]? I know they're not big, but they're all yours."

                else:
                    the_girl.char "Oh god, your hands... your cock... it feels so good!"

        "Kiss her.":
            "You pin [the_girl.title] against the [the_object.name] with your body and press your lips against hers. You keep pumping your hips, fucking her while you make out."
            if the_girl.sex_skills["Foreplay"] > 2: #Experienced kisser
                if the_girl.get_opinion_score("kissing") > 0:
                    $ the_girl.discover_opinion("kissing")
                    $ the_girl.change_arousal(the_girl.get_opinion_score("kissing"))
                    the_girl.char "[the_girl.possessive_title] shivers with pleasure when your tongues meet. She bucks her hips against yours, suddenly desperate to have you deeper inside of her."
                else:
                    the_girl.char "[the_girl.possessive_title] returns your kiss, darting her tongue out to meet yours."
                    if the_girl.outfit.tits_available():
                        "She wraps her arms around you and pulls you against her while you make out. You feel her tits pressed tight against your skin while you fuck her."
                    else:
                        "She wraps her arms around you and pulls you close while you make out. Her body rocks in time with your trusts."

            else: #Unsure about kissing
                if the_girl.get_opinion_score("kissing") > 0:
                    $ the_girl.discover_opinion("kissing")
                    $ the_girl.change_arousal(the_girl.get_opinion_score("kissing"))
                    "[the_girl.possessive_title] shivers when your tongue brushes against her lips. She opens her mouth and lets you inside."
                    "[the_girl.title] seems unsure of what to do with her tongue, but she trembles with every touch of yours. She rocks her hips against yours in time with your thrusts."
                    "After a while you break the kiss, leaving her breathing hard."
                    the_girl.char "Oh my god, my whole body... I didn't know that would feel so good! Don't stop!"
                    "She grabs the back of your head and pulls you back into a long kiss. You divide your attention between making out with [the_girl.title] and pounding her wet pussy."

                elif the_girl.get_opinion_score("kissing") < 0:
                    $ the_girl.discover_opinion("kissing")
                    $ the_girl.change_arousal(the_girl.get_opinion_score("kissing"))
                    "[the_girl.possessive_title] pulls away and after a brief kiss."
                    the_girl.char "No kissing. I never know what to do and I like being able to moan."
                    "True to her word she lets out a long, happy sigh while you fuck her against [the_object.name]."

                else:
                    "[the_girl.title] awkwardly returns your kiss. Her lips barely part when you press your tongue against them."
                    "After a few attempts you give up on making out and focus your attention on pounding her wet pussy."
    return

label scene_against_wall_2(the_girl, the_location, the_object):
    #CHOICE CONCEPT: Fuck her harder // Talk dirty to her
    if the_girl.arousal > 50:
        "You hold [the_girl.title]'s hands while you slide your cock in and out of her pussy. She's wet and obviously turned on."
    else:
        "You hold [the_girl.title]'s hands while you slide your cock in and out of her tight pussy."

    menu:
        "Fuck her harder.":
            "You lift [the_girl.possessive_title]'s hands up and pin them against the [the_object.name]. You lay into her, fucking her as hard as you can manage."
            if the_girl.get_opinion_score("being submissive"):
                $ the_girl.discover_opinion("being submissive")
                $ the_girl.change_arousal(the_girl.get_opinion_score("being submissive"))
                the_girl.char "Yes! Oh my god, yes! Use me however you want, I'll be whatever you want me to be!"
                "She bucks against you with pleasure. You respond by pushing her harder against the [the_object.name], which only makes her moan more loudly."
            else:
                if the_girl.get_opinion_score("vaginal sex") < 0:
                    $ the_girl.discover_opinion("vaginal sex")
                    $ the_girl.change_arousal(the_girl.get_opinion_score("vaginal sex"))
                    the_girl.char "Ow, slow down a little. You don't need to fuck me like you're trying to break me, you know."
                    "She pulls her hands out from under yours and uses them to guide your hips at a much more gentle pace."

                else:
                    if the_girl.sex_skills["Vaginal"] > 2:
                        "[the_girl.title] rocks her hips in time with yours to let you get as deep as possible."
                        if the_girl.get_opinion_score("creampies") > 0 or the_girl.get_opinion_score("bareback sex") > 0:
                            the_girl.char "That's it, fuck me hard you stud. Fuck me and pump then that hot load inside of me!"

                    else:
                        the_girl.char "Oh my god! [the_girl.mc_title], you feel so... Oh my god!"
                        "[the_girl.title] doesn't move much, but you're happy to just keep thrusting away at her warm cunt."




        "Talk dirty to her.":
            mc.name "Do you like this, you dirty slut? Do you like getting fucked against the [the_object.name]?"
            if the_girl.get_opinion_score("being submissive") < 0:
                $ the_girl.discover_opinion("being submissive")
                $ the_girl.change_arousal(the_girl.get_opinion_score("being submissive"))
                the_girl.char "Hey, don't talk like that. Just... Just keep going, okay?"
                "[the_girl.title] seems put off by your comments, but after a little while she's back to rocking her hips against you."

            else:
                if the_girl.core_sluttiness > 80 or the_girl.get_opinion_score("being submissive") > 0:
                    the_girl.char "Mmm, I do... I love feeling your big cock inside me."
                    mc.name "Do you want me to keep fucking you?"

                    if the_girl.get_opinion_score("bareback sex") > 0:
                        the_girl.char "Uh huh! Fuck me until you cum in me! Fuck me like you want to get me pregnant!"

                    elif the_girl.get_opinion_score("creampies") > 0:
                        the_girl.char "Uh huh! I want you to fuck me until you cum. Pin me against the [the_object.name] and pump your load into me! I want so badly!"
                    else:
                        the_girl.char "Uh huh! Please keep fucking me! I want you to fuck me and use me until you cum!"
                else:
                    the_girl.char "It feels so good... Oh my god [the_girl.mc_title], keep doing that!"

                "You certainly aren't about to disappoint her. You keep thrusting your cock into her warm cunt."

    return

label scene_against_wall_3(the_girl, the_location, the_object):
    # CHOICE CONCEPT: Grab her ass // Let her take control

    "[the_girl.title] thrusts her hips forward to meet yours with each thrust. She closes her eyes and puts her head back against [the_object.name]."
    menu:
        "Grab her ass.":
            "You reach behind [the_girl.possessive_title] and grab her butt. You pull her against you and push yourself as deep as you can manage."
            if the_girl.sex_skills["Vaginal"] < 3:
                the_girl.char "Oh my god, yes! Keep that cock deep inside of me!"
                "[the_girl.title] grabs your head and pulls you into a kiss. She gasps a little with each thrust."

            else:
                the_girl.char "Oh fuck, go easy on me... it feels like you're tearing me in half when you do that!"
                "You slow down a little bit and let [the_girl.possessive_title] get use to having your cock so deep inside of her."

            "You knead her ass cheeks while you fuck her. When she makes a happy yelp when you give them a slap."

        "Let her take control.":
            "You stop pumping your cock into [the_girl.title] and let her hips do all the work."
            if the_girl.sex_skills["Vaginal"] < 3 or the_girl.get_opinion_score("taking control") < 0:
                "After a second she stops too and looks at you."
                the_girl.char "What's wrong?"
                mc.name "Nothing, keep going."
                "[the_girl.title] starts to move her hips. After a few strokes it's obvious that she's having trouble keeping up the rhythm."
                the_girl.char "Sorry, I'm just not very good at this I guess."
                "You take the lead back and start fucking [the_girl.possessive_title] against the [the_object.name] again."
            else:
                if the_girl.get_opinion_score("taking control") > 0:
                    $ the_girl.discover_opinion("taking control")
                    $ the_girl.change_arousal(the_girl.get_opinion_score("taking control"))
                    the_girl.char "Oh, you want me to take care of this all by my self?"
                    "She puts her hands on your waist and grinds herself deeper onto your dick."
                    the_girl.char "Mmm, it's nice to get you so deep inside of me..."
                    if the_girl.get_opinion_score("creampies") > 0:
                        the_girl.char "Do you think I'll be able to make you cum? I'd love to make you cum inside me."
                        "She pauses for a moment and trembles, then starts fucking you again."
                        the_girl.char "Oh yeah, I want your hot load deep inside of me! I want to feel your dick twitch when I make you climax!"

                else:
                    "[the_girl.possessive_title] slows down for a second."
                    the_girl.char "Is something wrong?"
                    mc.name "No, I just like it when you take over."
                    "She bites her lip, puts her hands on your hips, and speeds up again."
                    the_girl.char "I'll see what I can do..."


                "[the_girl.possessive_title] clearly knows what she's doing. She uses the [the_object.name] behind her to push against you, and each stroke of her warm pussy pulls you closer and closer to climax."
    return

label outro_against_wall(the_girl, the_location, the_object):
    "[the_girl.title]'s tight cunt draws you closer to your orgasm with each thrust. You speed up as you pass the point of no return, pushing her up against the [the_object.name] and laying into her."
    $ the_girl.call_dialogue("sex_responses_vaginal")
    mc.name "Fuck, I'm going to cum!"
    $ the_girl.call_dialogue("cum_pullout")
    menu:
        "Cum inside of her.":
            if mc.condom:
                "You push forward as you climax, thrusting your cock as deep inside of [the_girl.possessive_title] as you can manage. She pants quitly as you pulse your hot cum into the condom you're wearing."
                $ the_girl.call_dialogue("cum_condom")
                "Once your climax has passed you step back and pull your cock out from [the_girl.title]. Your condom is ballooned out, filled with your seed."
                if the_girl.get_opinion_score("drinking cum") > 0 and the_girl.effective_sluttiness() > 50:
                    $ the_girl.discover_opinion("drinking cum")
                    "[the_girl.possessive_title] reaches for your cock. With delicate fingers she slides the condom off of you."
                    the_girl.char "It would be a shame to waste all of this, right?"
                    "She smiles and brings the condom to her mouth. She tips the bottom up and drains it into her mouth."
                    $ the_girl.change_slut_temp(the_girl.get_opinion_score("drinking cum"))
                else:
                    "[the_girl.possessive_title] reaches for your cock, removes the condom, and ties the end in a knot."
                    the_girl.char "Look at all that cum. Well done."
            else:
                "You push forward as you finally climax, thrusting your cock as deep inside of [the_girl.possessive_title] as you can manage. She gasps softly each time your dick pulses and shoots hot cum into her."
                $ the_girl.call_dialogue("cum_vagina")
                $ the_girl.cum_in_vagina()
                $ against_wall.redraw_scene(the_girl)
                "You wait until your orgasm has passed, then step back and sigh happily. [the_girl.title] stays leaning against the [the_object.name] for a few seconds as your semen drips down her leg."


        "Cum on her stomach.":
            $ the_girl.cum_on_stomach()
            $ against_wall.redraw_scene(the_girl)
            if mc.condom:
                "You pull out of [the_girl.possessive_title] at the last moment and step back. You whip your condom off and blow your load over her stomach while she watches."
            else:
                "You pull out of [the_girl.possessive_title] at the last moment and step back. You stroke yourself off and blow your load over her stomach while she watches."
            if the_girl.effective_sluttiness() > 120:
                the_girl.char "What a waste, that would have felt so much better inside of me..."
                "She reaches down and runs a finger through the puddles of cum you've put on her, then licks her finger clean and winks at you."
            else:
                the_girl.char "Oh wow, there's so much of it. It feels so warm..."
            "You sigh contentedly and relax for a moment, enjoying the sight of [the_girl.title] covered in your semen."
    return

label transition_default_against_wall(the_girl, the_location, the_object):
    "You press [the_girl.possessive_title] against the [the_object.name]. She plants her back against it and opens her legs, letting you step between them."
    "You run the tip of your cock along her slit a few times, then slide yourself inside of her tight cunt."
    return

label strip_against_wall(the_girl, the_clothing, the_location, the_object):
    $ the_girl.call_dialogue("sex_strip")
    $ the_girl.draw_animated_removal(the_clothing, position = against_wall.position_tag)
    "[the_girl.possessive_title] struggles out of her [the_clothing.name] and drops it beside her."
    return

label strip_ask_against_wall(the_girl, the_clothing, the_location, the_object):
    the_girl.char "Sir, I'd like to take off my [the_clothing.name], would you mind?"
    menu:
        "Let her strip.":
            mc.name "Take it off for me."
            $ the_girl.draw_animated_removal(the_clothing, position = against_wall.position_tag)
            "You slow the pace of your thrusts down while [the_girl.possessive_title] strips out of her [the_clothing.name]. When she drops it beside her you settle back into your rhythm."

        "Leave it on.":
            mc.name "No, I like how you look with it on."
            if the_girl.sluttiness < 70:
                the_girl.char "Yeah? Do I look sexy in it?"
                "You fuck her a little faster in response and she moans loudly."
            else:
                the_girl.char "Yeah? Do I look like a good little slut in it? Because that's what I feel like right now!"
                "You fuck her a little faster and she moans loudly."
    return

label orgasm_against_wall(the_girl, the_location, the_object):
    "[the_girl.possessive_title] closes her eyes and gasps suddenly. Her hands wrap around you and claw at pull hard against your back."
    $ the_girl.call_dialogue("climax_responses_vaginal")
    "You push her up against the [the_object.name] and keep fucking her through her orgasm."
    "After a couple of seconds [the_girl.title] opens her eyes again and takes a couple of deep breathes. You slow down your pace and give her a chance to recover."
    the_girl.char "Keep... keep going and see if you can make me to cum again!"
    return
