init:
    python:
        deepthroat = Position(name = "Deepthroat", slut_requirement = 55, slut_cap = 80, requires_hard = True, requires_large_tits = False,
            position_tag = "blowjob", requires_location = "Kneel", requires_clothing = "None", skill_tag = "Oral",
            girl_arousal = 3, girl_energy = 20,
            guy_arousal = 23, guy_energy = 5,
            connections = [],
            intro = "intro_deepthroat",
            scenes = ["scene_deepthroat_1","scene_deepthroat_2","scene_deepthroat_3"],
            outro = "outro_deepthroat",
            transition_default = "transition_default_deepthroat",
            strip_description = "strip_deepthroat", strip_ask_description = "strip_ask_deepthroat",
            orgasm_description = "orgasm_deepthroat",
            taboo_break_description = "taboo_break_deepthroat",
            verb = "throat fuck",
            opinion_tags = ["giving blowjobs","being submissive"], record_class = "Blowjobs",
            default_animation = idle_wiggle_animation, modifier_animations = {"blowjob":blowjob_bob},
            associated_taboo = "sucking_cock")

        list_of_positions.append(deepthroat)

init 1:
    python:
        deepthroat.link_positions(blowjob,"transition_deepthroat_blowjob")
        deepthroat.link_positions(skull_fuck, "transition_deepthroat_skull_fuck")

label intro_deepthroat(the_girl, the_location, the_object):
    "You unzip your pants and pull your underwear down, letting your hard cock spring free."
    mc.name "[the_girl.title], mind getting on your knees and taking this nice and deep for me?"
    if the_girl.effective_sluttiness() > 60:
        "[the_girl.possessive_title] reaches down and runs a finger along the top of your dick, then smiles and drops to her knees and looks up at you."
        the_girl.char "Okay [the_girl.mc_title], I'll see what I can do."
    else:
        "[the_girl.possessive_title] reaches down and runs a finger along the top of your dick. She hesitates for a few moments, then drops to her knees."
        the_girl.char "I'll... I'll do my best."

    if the_girl.sex_skills["Oral"] < 3:
        "She kisses the tip of your cock, then slides it into her mouth. Gets your length half way down, then gags softly on it and pauses."
        $ deepthroat.current_modifier = "blowjob"
        $ deepthroat.redraw_scene(the_girl)
        "[the_girl.possessive_title] collects herself then keeps going, fighting her gag reflex until she manages to fit your entire shaft down her throat."
    else:
        $ deepthroat.current_modifier = "blowjob"
        $ deepthroat.redraw_scene(the_girl)
        "She kisses the tip of your cock, then slides it into her mouth. Bit by bit she takes it deeper, until you have your entire shaft down her throat."
        "She pauses there for a moment, then starts to bob her head up and down slowly."
    return

label taboo_break_deepthroat(the_girl, the_location, the_object):
    $ the_girl.call_dialogue(deepthroat.associated_taboo+"_taboo_break") #All of the convincing happens in the dialogue here.
    if the_girl.effective_sluttiness(deepthroat.associated_taboo) > deepthroat.slut_cap:
        "[the_girl.possessive_title] kneels down in front of you, eyes locked on your hard cock."
        $ deepthroat.current_modifier = "blowjob"
        $ deepthroat.redraw_scene(the_girl)
        "She leans in, turning her head to the side to run her tongue down the bottom of your shaft."
        "She licks your balls briefly, then works back up to the tip and slides it past her lips."
        "You sigh happily as you feel [the_girl.title]'s warm mouth envelop your cock."
        "She wastes no time picking up speed, happily bobbing her head up and down over your sensitive tip."

    else:
        "[the_girl.possessive_title] hesitantly gets onto her knees, eyes locked on your hard cock."
        "She gently holds onto your shaft with one hand and brings the tip closer to her lips."
        "She looks up at you just before the moment of truth, locking eyes as she opens her lips and slides the tip of your cock past them."
        $ deepthroat.current_modifier = "blowjob"
        $ deepthroat.redraw_scene(the_girl)

        "You sigh happily as you feel [the_girl.title]'s warm mouth envelop your cock."
        "She moves slowly at first, gently working her head up and down over your sensitive tip."

    mc.name "Don't be shy, you can take it a little deeper than that."
    if the_girl.effective_sluttiness(deepthroat.associated_taboo) > deepthroat.slut_cap or the_girl.sex_skills["Oral"] >= 2:
        "[the_girl.possessive_title] takes your advice. She moves past the tip and tries to put your shaft down her throat."
        mc.name "That's it. You're a natural."

    else:
        "[the_girl.possessive_title] tries to move deeper, but gags and has to pull back."
        mc.name "Don't worry, you'll get it eventually."
    return

label scene_deepthroat_1(the_girl, the_location, the_object):
    $ deepthroat.current_modifier = "blowjob"
    $ deepthroat.redraw_scene(the_girl)
    if the_girl.sex_skills["Oral"] < 3: #Inexperienced
        "[the_girl.title] tries to look up at you while she goes down on your cock. You feel her throat spasm around you as she gags, struggling to take your length."
        menu:
            "You're doing a great job.":
                mc.name "God that feels good, you're doing a great job [the_girl.title]."
                "She gags one more time then slides off your cock, gasping for air when she comes free."
                $ deepthroat.current_modifier = None
                $ deepthroat.redraw_scene(the_girl)
                the_girl.char "Ah... Thank... Thank you... I'm trying my best. It feels so big when I try to slide it down..."


            "You can do better than that.":
                mc.name "Come on, I know you're a better cocksucker than that. Show me what you've really got."
                "[the_girl.title] tries to slide you deeper into her mouth and gags hard. She pulls back and gasps for air as soon as your dick is out of the way."
                $ deepthroat.current_modifier = None
                $ deepthroat.redraw_scene(the_girl)
                if the_person.obedience > 120:

                    the_girl.char "I'm... I swear I'm trying, it's just so... so big when I try and go deeper."
                else:
                    the_girl.char "I'm trying my best... Just be quiet and let me do this at my own pace, okay?"

        $ deepthroat.current_modifier = "blowjob"
        $ deepthroat.redraw_scene(the_girl)
        "[the_girl.possessive_title] takes a deep breath and slips your tip back into her mouth. She licks the tip of your cock before trying to fit it back down her throat."

    else: #Experienced
        "[the_girl.title] holds herself down on your hard cock for a few long seconds. She looks up at you, maintaining eye contact as she licks at the bottom of your shaft with her tongue."
        mc.name "Fuck, that feels great [the_girl.title]."
        $ deepthroat.current_modifier = None
        $ deepthroat.redraw_scene(the_girl)
        "She pushes you just a little bit deeper, then slides back and off. She pauses for a moment, panting while she tries to catch her breath."
        the_girl.char "Ah... Glad you like it."
        menu:
            "Stroke it for me.":
                mc.name "Don't just leave me standing here with my dick out, stroke me off."
                the_girl.char "Oh, right"
                if the_girl.sex_skills["Foreplay"] > 4:
                    "[the_girl.possessive_title] wraps her hand around your wet cock and starts to stroke it slowly. She leans close and puts your shaft right against her face."
                    the_girl.char "How's this. Is this better?"
                    "She looks at your dick and gives it a light kiss on the side, then looks back up at you."
                    the_girl.char "Look how big it is... and I'm going to slide it all down my throat. I'll take every last inch, just for you."
                else:
                    "[the_girl.possessive_title] wraps her hand around your wet cock and starts to stroke you off. You enjoy the sound of her heavy breathing and the quiet, wet slop of her handjob."


            "Bounce your cock on her face.":
                "You hold onto the base of your shaft and tap the tip against [the_girl.title]'s cheek. She looks up into your eyes."
                if the_girl.obedience > 120 or the_girl.get_opinion_score("being submissive") > 0:
                    $ the_girl.discover_opinion("being submissive")
                    the_girl.char "Oh, I'm sorry to keep you waiting. You can rub that all over me if you'd like."
                    "[the_girl.possessive_title] rubs the side of her face back against your wet cock, spreading her own spit over it."
                    "You hold your cock and flop it down more forcefully, flopping it over her mouth and nose. She opens her mouth and sticks out her tongue, panting softly."
                    "While [the_girl.title] catches her breath you rub your cock against her tongue, then across her cheeks, then up over her forehead, spreading her spit all over her face."

                else:
                    the_girl.char "That desperate for it, huh?"
                    "She nuzzles against your cock and tilts her head, letting you bounce your dick off of her cheek a few more times."


        the_girl.char "Okay, I think I'm ready to get back down to business."
        $ deepthroat.current_modifier = "blowjob"
        $ deepthroat.redraw_scene(the_girl)
        "[the_girl.possessive_title] pops your tip back into her mouth and slides you right back down her throat."
        "She gags a little as she bottoms out on your cock. Her mouth feels amazingly warm wrapped around your air-chilled shaft."
    return

label scene_deepthroat_2(the_girl, the_location, the_object):
    $ deepthroat.current_modifier = "blowjob"
    $ deepthroat.redraw_scene(the_girl)
    "You place a firm hand on the back of [the_girl.title]'s head, guiding her up and down your shaft."
    "With a little pressure you encourage her to speed up, while making sure she keeps you nice and deep down her throat."

    if the_girl.sex_skills["Oral"] < 3:
        "[the_girl.possessive_title] tries to slow down and go shallower on your cock."
        menu:
            "Give her a break.":
                "You move your hand off of the back of her head, and cradle her chin instead. She pauses and looks up at you, the tip of your dick still in her mouth."
                mc.name "How about you take a break, I think you've earned one."
                $ deepthroat.current_modifier = None
                $ deepthroat.redraw_scene(the_girl)
                "[the_girl.title] lets your cock fall out of her mouth and takes a deep breath."
                the_girl.char "Oh my god, it looks so big when it's in front of me like this... Do you really think I could fit this all in my mouth?"
                "You keep your hand on her chin and slide your thumb into [the_girl.possessive_title]'s mouth instead. She hesitates for a moment then starts to suck on that instead."
                mc.name "We'll make it fit, I'll give a hand if you need it."
                $ deepthroat.current_modifier = "blowjob"
                $ deepthroat.redraw_scene(the_girl)
                "You pull your thumb from her mouth and replace it with the tip of your cock. She licks at it then bobs her head forward and tries to take your length back down her throat."

            "Force her deeper.":
                mc.name "Come on, no slacking off..."
                "You pull hard on the back of [the_girl.title]'s head, forcing her to bottom out on your cock. She puts her her hands on your thighs and tries to pull back but you hold her in place."
                if the_girl.get_opinion_score("being submissive") > 0:
                    $ the_girl.change_arousal(the_girl.get_opinion_score("being submissive" * 5))
                    $ the_girl.discover_opinion("being submissive")
                    "[the_girl.possessive_title]'s knees quiver while her throat spasms around your shaft. You hold her deep while her body twitches with pleasure."
                    $ deepthroat.current_modifier = None
                    $ deepthroat.redraw_scene(the_girl)
                    "After a long moment you let go of her head. [the_girl.title] stays balls deep on your dick for a full second before sliding off slowly and looking up at you."
                    the_girl.char "Oh my god, that was... That was so... good!"
                    $ deepthroat.current_modifier = "blowjob"
                    $ deepthroat.redraw_scene(the_girl)
                    "She shivers with pleasure again and plunges your cock back into her mouth, gagging herself on your length."
                else:
                    "[the_girl.possessive_title] gags on your cock, blowing little spit bubbles around the base. After a moment she gets her body under control and she's able to keep your full length down."
                    mc.name "That's it, you've got it now."
                    $ deepthroat.current_modifier = None
                    $ deepthroat.redraw_scene(the_girl)
                    "You let go of her head and she pulls back quickly. She gasps for air as soon as she's able to take a breath."
                    if the_girl.obedience > 130:
                        the_girl.char "I... Ah... Sorry, sir. I'll do better next time."
                        mc.name "You're doing fine, I just saw you needed a little help."
                        $ deepthroat.current_modifier = "blowjob"
                        $ deepthroat.redraw_scene(the_girl)
                        "She nods and pants for a few seconds, then slides you pack into her mouth. [the_girl.title] seems more comfortable taking your full length down when she starts to throat you again."
                    else:
                        the_girl.char "What... What the fuck..."
                        mc.name "You were struggling a little, so I helped you out."
                        the_girl.char "Just... leave it to me next time, okay?"
                        $ deepthroat.current_modifier = "blowjob"
                        $ deepthroat.redraw_scene(the_girl)
                        "She pants for a few seconds, then slides you back into her mouth and starts to throat you again. Despite her objections she seems more comfortable taking your full length down."

    else:
        if the_girl.effective_sluttiness() > 80 or the_girl.get_opinion_score("giving blowjobs") > 0:
            "[the_girl.title] turns her eyes up and meets your gaze as she throats you, her tongue eagerly licking at the bottom of your shaft."
        else:
            "[the_girl.title] closes her eyes and focuses entirely on throating your long cock."

        menu:
            "Compliment her cock sucking.":
                mc.name "God, you're good at that [the_girl.title]. Do you have a lot of practice or are you just a natural at throating big dicks?"
                if the_girl.get_opinion_score("giving blowjobs") > 0:
                    "In response she bottoms out on your dick. She rocks her head left and right, grinding her face into your crotch to take as much of your length as possible."
                    "She tenses and and relaxes her throat rhythmically, gently massaging your shaft with it."
                    mc.name "Oh... maybe it's both then. A talent and a passion for gagging on dick. Either way, you're a perfect little cock sucker, aren't you."
                    "After a long moment she bobs her head back and breathes deeply through her nose. You let her recover before putting pressure on the back of her head to encourage her to go back to sucking you off."
                elif the_girl.get_opinion_score("giving blowjobs") < 0:
                    $ deepthroat.current_modifier = None
                    $ deepthroat.redraw_scene(the_girl)
                    "She pulls off your dick and sighs."
                    $ the_girl.discover_opinion("giving blowjobs")
                    the_girl.char "I don't normally do this for guys, so..."
                    $ deepthroat.current_modifier = "blowjob"
                    $ deepthroat.redraw_scene(the_girl)
                    "You press the tip of your cock against her lips and put a little bit of pressure on the back of her head. She takes the hint and goes back to sucking you off."
                    mc.name "Well then congratulations, you're just a natural born cock sucker. It's a good thing I figured that out, it would be a shame for your natural talent to go to waste..."
                    "You moan softly as [the_girl.possessive_title]'s warm throat massages your shaft."
                else:
                    $ deepthroat.current_modifier = None
                    $ deepthroat.redraw_scene(the_girl)
                    "She pulls off your dick and shrugs."
                    the_girl.char "No more practice than other girls, I guess."
                    mc.name "Uh huh, and how much dick do you think other girls suck? You don't get this good by accident."
                    "You press the tip of your cock against her lips and put a litttle bit of pressure on the back of her head. She takes the hint and goes back to sucking you off."


            "Force her even deeper.":
                mc.name "Do you need a little help?"
                "When [the_girl.title] reaches the bottom of her next stroke you push down on the back of her head and hold her in place."
                mc.name "That's it, hold it right there for a moment."
                if the_girl.get_opinion_score("being submissive") > 0 or the_girl.obedience > 130:
                    "[the_girl.possessive_title] seems happy to let you take control. When you add a little pressure to the back of her head she manages to slide your cock a little further down her throat."
                else:
                    "[the_girl.possessive_title] stays still with almost all of your cock down her throat. You add a little more pressure and she gags softly. The sudden spasm of her throat around your shaft feels amazing."
                $ deepthroat.current_modifier = None
                $ deepthroat.redraw_scene(the_girl)
                "You keep her there until she taps you on the thigh. When you let go of her head she pulls off your shaft and takes a sharp breath."
                the_girl.char "Ah... one second..."
                "You wait until she's caught her breath, then press your tip against her lips. She takes the hint and slides you back into her mouth."


    if mc.arousal > 70:
        mc.name "Fuck, keep that up and I'll be cumming soon!"
    else:
        mc.name "That's it, keep it up. You're doing a great job [the_girl.title]!"

    return

label scene_deepthroat_3(the_girl, the_location, the_object):
    if the_girl.sex_skills["Oral"] < 4:
        "[the_girl.title] is struggling to take the full length of your dick down her throat. She pulls off and pants for air."
        the_girl.char "Ah... let me see if I can fit this all down..."
        "Once she's caught her breath she slides your cock back into her mouth. She swirls her tongue around your tip, then slides you back until you tap the back of her throat."
        "[the_girl.possessive_title] pauses there for a second and closes her eyes in concentration."
        if the_girl.sex_skills["Oral"] < 2:
            "She tries to push herself further, but her inexperience stops her from making any progress. She lurches backwards, gagging and gasping for air."
            the_girl.char "Maybe I... Ah... Just need more practice..."
            "She shrugs, wipes some spit from her lips, and slips you back into her mouth."
        else:
            "Fighting her gag reflex, she inches her way down your shaft. It's slow going, but after a moment she succeeds in deepthroating your entire cock."
            "She lurches backwards and gasps for air, then claps her hands together and laughs."
            the_girl.char "Haha! I did it! I didn't think I could do it for a moment. I guess now I need to work on time, right?"
            "She smiles and slips you back into her mouth."
    else:
        "[the_girl.title] stops throating you for a second."
        the_girl.char "I wonder how long I could keep you in my mouth. Want to find out?"
        "You nod and she smiles. [the_girl.possessive_title] plunges you back into her mouth and right down her throat. Your balls tap against her chin."
        "[the_girl.title] holds up a hand, counting with her fingers how long she's lasted."
        $ duration = __builtin__.str(renpy.random.randint(10, 30+(the_girl.sex_skills["Oral"]*10)))
        "She gets all the way up to [duration] before she has to pull off and gasp for air."
        if the_girl.get_opinion_score("being submissive") > 0 and the_girl.get_opinion_score("giving blowjobs") > 0:
            the_girl.char "Whew... that was pretty good, but I think I could do better..."
            the_girl.char "I want to try again. [the_girl.mc_title], could you... hold me down so I can't pull off?"
            "You place a steady hand on the back of her head and pull her closer to you in response."
            mc.name "I'll help you do the best you could possibly do."
            $ the_girl.change_happiness(4+the_girl.get_opinion_score("giving blowjobs"))
            "She grins up at you, then takes a few deep breaths and slides you back into her mouth and all the way to the back of her throat."
            "Again she holds up a hand and starts to keep track of how long she's lasted."
            "[duration] seconds come and go with your dick shoved down [the_girl.title]'s throat. You put a little pressure on the back of her head."
            "[the_girl.possessive_title]'s throat spasms around your shaft as she starts to reach her limit. She closes her eyes and focuses hard on her task."
            $ second_duration = __builtin__.str(renpy.random.randint(10,20))
            "Another [second_duration] seconds pass by before you feel her start to pull her head back."
            menu:
                "Hold her in place." if the_girl.obedience >= 110:
                    mc.name "Not yet, you can do better than that."
                    "You pull [the_girl.title]'s head against your crotch. She doesn't resist."
                    "After a few more seconds [the_girl.title] tries to pull off again, forcing you put on light but constant pressure."
                    menu:
                        "Hold her in place." if the_girl.obedience >= 120:
                            "A little more force and [the_girl.title] stays where she is. Her eyes are closed tight as she struggles to stay in control."
                            "More time passes. [the_girl.title] starts to squirm on her knees."
                            $ the_girl.change_arousal(the_girl.get_opinion_score("being submissive"))
                            menu:
                                "Hold her in place." if the_girl.obedience >= 130:
                                    mc.name "Don't give up now [the_girl.title], you're doing great."
                                    "You grab a handful of her hair to give you a better grip and don't let her go anywhere."
                                    "[the_girl.title]'s throat starts to rhythmically clench down on the shaft of your dick."
                                    $ the_girl.change_arousal(the_girl.get_opinion_score("being submissive"))
                                    $ mc.change_arousal(1)
                                    "[the_girl.possessive_title]'s grabs at your legs, looking for support."
                                    menu:
                                        "Hold her in place." if the_girl.obedience >= 150:
                                            mc.name "You're going to choke on this dick until I'm satisfied. Don't you dare move now."
                                            "[the_girl.title] moans, her throat rumbling around your cock. Her eyes roll up as she tries to make eye contact with you."
                                            $ the_girl.change_arousal(the_girl.get_opinion_score("being submissive"))
                                            "Several more long seconds pass. Pushed to her limit, [the_girl.title] pulls back harder and starts to tap on your leg."
                                            menu:
                                                "Choke her out." if the_girl.obedience >= 170:
                                                    mc.name "I said don't move. Not until I'm done with you."
                                                    "[the_girl.title] squirms and fidgets on her knees, but obeys your commands like a good girl."
                                                    "Little by little her movements slow down, her eyelids start to droop down over her rolled up eyes, and she slips into a half-conscious state."
                                                    $ the_girl.change_arousal(the_girl.get_opinion_score("being submissive"))
                                                    "[the_girl.possessive_title]'s body doesn't stop reacting to you and your cock. Her tongue licks lazily at the base of your shaft and she keeps moaning softly."
                                                    "Satisfied, you take your hand off of [the_girl.title]'s head. She doesn't move and keeps sucking on you in her oxygen deprived stupor."
                                                    mc.name "That's enough [the_girl.title], you've done enough."
                                                    "You put your hand under her chin and pull her back. She leaves your cock with a satisfying, wet pop followed by a huge gasp for air."
                                                    "It takes a few long moments until [the_girl.title] shakes her head and comes to her senses."
                                                    the_girl.char "I... Oh my god... How long was I... Ah... Ah..."
                                                    $ the_girl.change_arousal(the_girl.get_opinion_score("being submissive"))
                                                    "The thought of passing out on your cock seems to turn her on."
                                                    mc.name "Long enough, I think you've got a new personal best."
                                                    "[the_girl.possessive_title] bites her lip and moans to herself for a second."
                                                    the_girl.char "Thank you [the_girl.mc_title], you really pushed me there. Now... I can't make this all about me."
                                                    "She takes a deep breath, opens wide, and fits you right back into her mouth. This time she bobs her head back and forth, taking quick breaths when she can."
                                                    return #Don't do the rest of the scene because we have our special case here.

                                                "Choke her out.\n Requires: 170 Obedience (disabled)" if the_girl.obedience < 170:
                                                    pass

                                                "Let her up.":
                                                    pass
                                        "Hold her in place.\n Requires: 150 Obedience (disabled)" if the_girl.obedience < 150:
                                            pass

                                        "Let her up.":
                                            pass
                                "Hold her in place.\n Requires: 130 Obedience (disabled)" if the_girl.obedience < 130:
                                    pass

                                "Let her up.":
                                    pass

                        "Hold her in place.\n Requires: 120 Obedience (disabled)" if the_girl.obedience < 120:
                            pass

                        "Let her up.":
                            pass

                "Hold her in place.\n Requires: 110 Obedience (disabled)" if the_girl.obedience < 110:
                    pass

                "Let her up.":
                    pass

            "[the_girl.title] yanks her head back and off of your hard cock. She gasps for breath as soon as you're clear."
            the_girl.char "That... was... intense... Ah..."
            "It takes her a moment to catch her breath. You run your fingers through her hair while you let her recover."
            the_girl.char "That was a long time, but I think I could do better next time... Don't go so easy on me, okay?"
            "With that she leans forward and starts to suck your hard cock again."
        else:
            the_girl.char "Whew... that was pretty good, right?"
            $ the_girl.change_happiness(1+the_girl.get_opinion_score("giving blowjobs"))
            the_girl.char "Ah... Right, where was I..."
            "She slips you back into her mouth and starts to throat you again."
    return

label outro_deepthroat(the_girl, the_location, the_object):
    $ deepthroat.current_modifier = "blowjob"
    $ deepthroat.redraw_scene(the_girl)
    "The warm, tight feeling of [the_girl.title]'s throat wrapped around your shaft pulls you closer and closer to orgasm. You feel yourself pass the point of no return and let out a soft moan."
    menu:
        "Cum on her face.":
            mc.name "Fuck, here I come!"
            $ deepthroat.current_modifier = None
            $ deepthroat.redraw_scene(the_girl)
            "You take a step back, pulling your cock out of [the_girl.possessive_title]'s throat with a satisfyingly wet pop, and take aim at her face."
            if the_girl.sluttiness > 80:
                "[the_girl.title] sticks out her tongue for you and holds still, eager to take your hot load."
                $ the_girl.cum_on_face()
                $ deepthroat.redraw_scene(the_girl)
                "You let out a shudder moaning as you cum, pumping your sperm onto [the_girl.title]'s face and into her open mouth. She makes sure to wait until you're completely finished."
            elif the_girl.sluttiness > 60:
                "[the_girl.title] closes her eyes and waits patiently for you to cum."
                $ the_girl.cum_on_face()
                $ deepthroat.redraw_scene(the_girl)
                "You let out a shudder moaning as you cum, pumping your sperm onto [the_girl.title]'s face. She waits until she's sure you're finished, then opens one eye and looks up at you."
            else:
                "[the_girl.title] closes her eyes and turns away, presenting her cheek to you as you finally climax."
                $ the_girl.cum_on_face()
                $ deepthroat.redraw_scene(the_girl)
                "You let out a shudder moaning as you cum, pumping your sperm onto [the_girl.title]'s face. She flinches as the first splash of warm liquid lands on her cheek, but doesn't pull away entirely."
            "You take a deep breath to steady yourself once you've finised orgasming. [the_girl.possessive_title] looks up at you from her knees, face covered in your semen."
            $ the_girl.call_dialogue("cum_face")

        "Cum in her mouth.":
            mc.name "Fuck, I'm about to cum! I'm going to fill that cute mouth of yours up!"
            "You keep your hand on the back of [the_girl.title]'s head to make it clear you want her to keep sucking. She keeps throating you until you tense up and start to pump your load out into her mouth."
            if the_girl.sluttiness > 70:
                "[the_girl.title] doesn't even flinch as you shoot your hot cum across the back of her throat."
                "She keeps bobbing her head up and down until you've let out every last drop, then slides back carefully and looks up with a mouth full of sperm."
            else:
                "[the_girl.title] stops when you shoot your first blast of hot cum across the back of her throat."
                "She pulls back, leaving just the tip of your cock in her mouth as you fill it up with semen. Once you've finished she slides off and looks up to show you a mouth full of sperm."

            $ the_girl.cum_in_mouth()
            $ deepthroat.redraw_scene(the_girl)
            if the_girl.sluttiness > 80:
                "Once you've had a good long look at your work [the_girl.possessive_title] closes her mouth and swallows loudly."
                "It takes a few big gulps to get every last drop of your cum down, but when she opens up again it's all gone."
            else:
                "Once you've had a good long look at your work [the_girl.possessive_title] leans over to the side and lets your cum dribble out slowly onto the ground."
                "She straightens up and wipes her lips with the back of her hand."
            $ the_girl.call_dialogue("cum_mouth")

        "Cum down her throat.":
            mc.name "Fuck, here I come!"
            "You use your hand on the back of [the_girl.title]'s head to pull her close, pushing your cock as deep down her throat as you can manage."
            "You grunt and twitch as you start to empty your balls right into her stomach."
            if the_girl.sluttiness > 90:
                "[the_girl.possessive_title] looks up at you and stares into your eyes as you climax. She tightens and relaxes her throat, as if to draw out every last drop of semen from you."
                $ the_girl.cum_in_mouth()
                $ deepthroat.redraw_scene(the_girl)
                "Whn you're completely finished she pulls off slowly, kissing the tip before leaning back."
                $ the_girl.call_dialogue("cum_mouth")
            elif the_girl.sluttiness > 60:
                "[the_girl.possessive_title] closes her eyes and holds still as you climax. You feel her throat spasm a few times as she struggles to keep your cock in place."
                $ the_girl.cum_in_mouth()
                $ deepthroat.redraw_scene(the_girl)
                "When you're finished she pulls off quickly, gasping for air. It takes a few seconds for her to regain her composure."
                $ the_girl.call_dialogue("cum_mouth")
            else:
                "[the_girl.possessive_title] closes her eyes and tries to hold still as you climax. Her throat spasms as soon as the first blast of sperm splashes across the back, and she pulls back suddenly."
                "With no other choice, you stroke yourself off onto her face as she coughs and gasps for breath."
                $ the_girl.cum_on_face()
                $ deepthroat.redraw_scene(the_girl)
                $ the_girl.call_dialogue("cum_face")
    return

label transition_deepthroat_blowjob(the_girl, the_location, the_object):
    "You move your hand from the back of [the_girl.title]'s head and sigh contentedly."
    mc.name "Fuck that felt nice."
    "[the_girl.possessive_title] slides your cock out of her mouth and strokes it with one hand while she talks to you."
    the_girl.char "Mmm, glad you liked it. I think I'm going to have a sore throat in the morning after all that."
    "She smiles and kisses the tip of your dick, then slides it back into her mouth and starts to suck on it some more, paying more attention to the shaft now."
    return

label transition_deepthroat_skull_fuck(the_girl, the_location, the_object):
    "You place two strong hands on either side of [the_girl.title]'s head."
    mc.name "I want to take control for a bit. Ready?"
    $ deepthroat.current_modifier = None
    $ deepthroat.redraw_scene(the_girl)
    "She pops off your cock and looks up at you."
    if the_girl.obedience >= 130 or the_girl.get_opinion_score("being submissive") > 0:
        the_girl.char "My body is yours [the_girl.mc_title], take me however you want me!"
    else:
        the_girl.char "I think so, let's see what you can do, big boy."
    "She opens her mouth wide for you. You rest the tip of your cock on her lower lip, then ram it forward."
    "Her eyes go wide you immediately bottom out, rubbing against the back of her throat and making her gag."
    mc.name "I believe in you [the_girl.title]. You can take it."
    "You have no intention of stopping either way as you skull fuck [the_girl.possessive_title]'s tight throat."
    $ deepthroat.current_modifier = "blowjob"
    $ deepthroat.redraw_scene(the_girl)
    return

label transition_default_deepthroat(the_girl, the_location, the_object):
    "[the_girl.title] gets ready in front of you, on her knees with her mouth open. You place a hand on the back of her head and pull her towards you, sliding your cock down her throat."
    "After giving her a second to get use to your size you start to guide her back and forth, keeping yourself buried nice and deep in her mouth."
    return

label strip_deepthroat(the_girl, the_clothing, the_location, the_object):
    "[the_girl.title] pops off your cock and looks up at you."
    $ the_girl.call_dialogue("sex_strip")
    $ the_girl.draw_animated_removal(the_clothing, position = deepthroat.position_tag)
    "[the_girl.possessive_title] stands and strips off her [the_clothing.name]. She drops it to the ground, then gets back on her knees and slides your cock inside her mouth."
    return

label strip_ask_deepthroat(the_girl, the_clothing, the_location, the_object):
    "[the_girl.title] pops off your cock and looks up at you from her knees."
    the_girl.char "[the_girl.mc_title], I'd like to take off my [the_clothing.name], would you mind?"
    menu:
        "Let her strip.":
            mc.name "Take it off for me."
            $ the_girl.draw_animated_removal(the_clothing, position = deepthroat.position_tag)
            "[the_girl.possessive_title] stands up and strips out of her [the_clothing.name]. She gets back onto her knees and slides your cock all the way to the back of her mouth."


        "Leave it on.":
            mc.name "No, I like how you look with it on."
            if the_girl.sluttiness < 60:
                the_girl.char "Yeah? Do I look sexy in it?"
                "She licks the length of your shaft, then slides your tip into her mouth and starts to blow you again."
            else:
                the_girl.char "Does it make me look like a good little slut? Or is your cock in my mouth enough for that?"
                "She slides you back into her mouth and presses you all the way to the back, rubbing your tip against the back of her throat."
    return


label orgasm_deepthroat(the_girl, the_location, the_object):
    $ deepthroat.current_modifier = "blowjob"
    $ deepthroat.redraw_scene(the_girl)
    "[the_girl.title] pulls back on your cock, almost letting it fall out of her mouth. She closes her eyes and quivers slightly."
    menu:
        "Face fuck her while she cums.":
            "You put your hands on the back of [the_girl.title]'s head and pull her back down onto your shaft, hard."
            mc.name "Cum for me you dirty little slut!"
            if the_girl.sex_skills["Oral"] > 3:
                "[the_girl.possessive_title] keeps her mouth wide open for you, even as she twitches and writhes through her climax."
                "You fuck her tight throat until she finishes twitching."
            else:
                "[the_girl.possessive_title] gags on your cock as you push her down onto it."
                "Her body tightens up as she climaxes, and you make sure to take advantage of her tight throat by fucking it hard."

            if the_girl.get_opinion_score("being submissive") > 0:
                if the_girl.sluttiness > the_girl.core_sluttiness and the_girl.core_sluttiness < blowjob.slut_cap:
                    $ the_girl.change_slut_core(the_girl.get_opinion_score("being submissive")) #If she likes being submissive this makes her cum and become sluttier super hard.
                    $ the_girl.change_slut_temp(-the_girl.get_opinion_score("being submissive"))
                $ the_girl.change_obedience(2*the_girl.get_opinion_score("being submissive"))
                if the_girl.outfit.vagina_visible():
                    "You can see that [the_girl.title]'s pussy is dripping wet as she cums."
                else:
                    $ top_piece = the_girl.outfit.get_lower_ordered()[-1]
                    if top_piece.underwear:
                        "[the_girl.title]'s dripping wet pussy has managed to soak through her underwear, leaving a wet mark on her [top_piece.name]."
                    else:
                        "[the_girl.title] clenches her thighs together and rides out her orgasm."
                $ blowjob.current_modifier = None
                $ blowjob.redraw_scene(the_girl)
                "When she's finished cumming you let [the_girl.title] pull back off your shaft. She gasps loudly for air."
                the_girl.char "That was... oh my god [the_girl.mc_title], I want you to do that again!"

            else:
                $ blowjob.current_modifier = None
                $ blowjob.redraw_scene(the_girl)
                "When she's finsihed cumming you let [the_girl.title] pull back off your shaft. She gasps loudly for air and rubs her throat."
                $ the_girl.change_obedience(1)
                $ the_girl.change_happiness(-2)
                the_girl.char "Ah... fuck. Go a little easier on me next time, okay?"
                "She clears her throat, then kisses the side of your dick."
                the_girl.char "I think I'm ready to get back to it though."

        "Be gentle while she cums.":
            "You wait patiently while [the_girl.possessive_title] climaxes. She keeps her lips wrapped around the tip of your cock the entire time."
            mc.name "That's it, cum for me [the_girl.title]. Suck on my cock and cum for me."
            "You hear her whimper and a final shiver runs through her body."
            "It takes a few seconds before she fully recovers, but when she has she goes right back to throating you."
    return
