init:
    python:
        piledriver = Position(name = "Piledriver", slut_requirement = 70, slut_cap = 90, requires_hard = True, requires_large_tits = False,
            position_tag = "missionary", requires_location = "Lay", requires_clothing = "Vagina", skill_tag = "Vaginal",
            girl_arousal = 14, girl_energy = 12,
            guy_arousal = 26, guy_energy = 20,
            connections = [],
            intro = "intro_piledriver",
            scenes = ["scene_piledriver_1","scene_piledriver_2"],
            outro ="outro_piledriver",
            transition_default = "transition_default_piledriver",
            strip_description = "strip_piledriver", strip_ask_description = "strip_ask_piledriver",
            orgasm_description = "orgasm_piledriver",
            taboo_break_description = "taboo_break_piledriver",
            opinion_tags = ["missionary style sex","vaginal sex","being submissive"], record_class = "Vaginal Sex",
            default_animation = missionary_bob,
            associated_taboo = "vaginal_sex")
        list_of_positions.append(piledriver)

init 1:
    python:
        piledriver.link_positions(missionary,"transition_piledriver_missionary")

label intro_piledriver(the_girl, the_location, the_object):
    mc.name "[the_girl.title], I want you to lie down for me."
    "[the_girl.possessive_title] nods, glancing briefly at the bulge in your pants. She gets onto the [the_object.name] and waits for you."
    the_girl.char "How's this?"
    "You get your hard cock out and kneel down in front of her. She yelps in suprise when you grab her ankles and bring them up and over her waist."
    mc.name "There we go, this will be even better."
    "You rub the tip of your cock against her clit a few times, then press forward and slide yourself inside of her."
    $the_girl.call_dialogue("sex_responses_vaginal")
    return

label taboo_break_piledriver(the_girl, the_location, the_object):
    "You take [the_girl.title]'s hands in yours and guide her down onto the [the_object.name]. She follows your lead, lying down for you."
    "You place your hands on her knees and spread her legs, kneeling down between them."
    "You sit your hard cock on her stomach, teasingly close to her warm pussy. [the_girl.possessive_title] reaches down and gently pets your shaft."
    $ the_girl.call_dialogue(piledriver.associated_taboo+"_taboo_break")
    "You grab onto [the_girl.title]'s ankles and lift them up, bringing her knees up to your shoulders."
    if the_girl.effective_sluttiness(piledriver.associated_taboo) > piledriver.slut_cap:
        the_girl.char "Ooh, I like it!"
        "She reaches down between her legs and holds onto your cock, lining it up with her pussy for you."
        "She rubs your tip against her clit a few times before moving it down, just barely spreading her slit open for you."


    else:
        the_girl.char "Ah! What are you doing?"
        mc.name "Trust me, this will feel great."
        "You reach down between your legs and hold onto your cock, lining it up with [the_girl.possessive_title]'s pussy."
        "She gasps as your tip flicks over her clit and into place, just barely spreading open her slit."

    "You hold onto [the_girl.title]'s legs and push forward. After a moment of resistance you slide smoothly into her slippery, warm cunt."
    the_girl.char "Ohhhh....."
    "You hold yourself deep inside of her for a few seconds, then pull back and begin slowly thrust in and out."
    return

label scene_piledriver_1(the_girl, the_location, the_object):
    #CHOICE CONCEPT: Talk dirty to her // Fuck her in silence
    "You hold onto [the_girl.title]'s ankles and lean into her, using the position to push yourself nice and deep inside of her."
    if the_girl.sex_skills["Vaginal"] < 3:
        #Struggles taking you that deep.
        the_girl.char "Ah! Oh fuck me, I think I need you to slow down..."
        menu:
            "Go slowly.":
                "You pause and give [the_girl.possessive_title] a chance to get use to having your cock buried inside of her cunt."
                "She takes a few deep breaths, then nods to you."
                the_girl.char "Okay, I think I'm ready. Take it slow though."
                if the_girl.arousal < 50:
                    "You start to pump your hips. [the_girl.title]'s pussy is tight but wet, giving you just enough lubrication to slide in and out easily."
                    mc.name "There you go, I knew you could manage it."
                    the_girl.char "Oh... I can... I can do this..."
                else:
                    "You start to pump your hips. [the_girl.title]'s pussy is tight and clamps down on your dick with each thrust."
                    mc.name "Give it some time and you'll be nice and wet."
                    "[the_girl.possessive_title] closes her eyes and grits her teeth as you fuck her."


            "Fuck her hard anyways.":
                mc.name "Don't worry, I know you can handle it."
                "You speed up instead of slowing down. Having her bent over gives you all the leverage you need to drive your cock deep into her cunt."
                if the_girl.get_opinion_score("being submissive") > 0:
                    the_girl.char "Wait, oh my god! Oh fuck, you're going to tear me in half! Ah!"
                    $ the_girl.discover_opinion("being submissive")
                    $ the_girl.change_arousal(the_girl.get_opinion_score("being submissive"))
                    "She closes her eyes and trembles. You feel her pussy twitch around your shaft while you fuck her."
                    mc.name "Do you like getting fucked hard like this? I think you do. I think you like being a little slutty fuck hole."
                    the_girl.char "I... Oh my god I do! I do! I shouldn't but I want you to fuck me harder! Fuck me!"
                    "She turns her head to the side and her pants like a dog. You push her legs farther over her head and pound her into the [the_object.name]."

                else:
                    the_girl.char "Ow, fuck! I said slow down, I'm not ready yet!"
                    "[the_girl.title] struggles a little underneath you, but her position doesn't give her any chance of moving."
                    if the_girl.arousal < 50:
                        "Her pussy is tight around your cock, but she's still getting wet. You slow down again to give her some more time."
                        the_girl.char "I wasn't ready for how... deep you would be going."
                        "You push her ankles to the side, spreading her legs so you have a great look of her pussy impailed by your cock. You take a few slow thrusts and listen to her moan."
                        "After a few moments she nods up at you."
                        the_girl.char "Okay, I think I'm ready. Take it slow, please."
                        "You pump your hips again, slowly this time, and soon [the_girl.possessive_title] is enjoying being fucked again."
                    else:
                        "Her pussy is tight and wet around your cock, letting you slide in and out easily despite her complaints."
                        mc.name "See, you're ready for this. Just take a deep breath and you'll be fine."
                        $ the_girl.discover_opinion("being submissive")
                        $ the_girl.change_happiness(the_girl.get_opinion_score("being submissive"))
                        $ the_girl.change_arousal(the_girl.get_opinion_score("being submissive"))
                        the_girl.char "Wait, I... Ah! Oh fuck!"
                        "You lay into her, pounding her against the [the_object.name]."
                        "With her legs up over her shoulders you can see her face while you fuck her; her discomfort melts away into pleasure after a few thrusts, and you leave her panting and moaning."



    else:
        #Takes it fine, asks for more.
        $ the_girl.call_dialogue("sex_responses_vaginal")
        "[the_girl.title] holds her legs out wide for you, spreading herself so you can fuck her hard and fast against the [the_object.name]."
        menu:
            "Talk dirty to her.":
                mc.name "You look really good with my cock inside you, did you know that?"
                if the_girl.sex_skills["Foreplay"] > 2: #She's good at foreplay, flirting, etc.
                    "She looks up at you and bites her lip."
                    the_girl.char "And you look good on top of me... Fucking my poor little pussy raw."
                    mc.name "I know you can handle it, you're a well trained little slut who knows how to take a dick."
                    "[the_girl.possessive_title] moans loudly, enjoying the combination of your dirty talk and getting fucked."
                    if the_girl.get_opinion_score("creampies") > 0 or the_girl.get_opinion_score("bareback sex") > 0:
                        the_girl.char "Oh... I want to watch you cum [the_girl.mc_title]. I want to watch you unload deep inside of me. I want to feel your hot dripping out of me..."

                    elif the_girl.get_opinion_score("cum facials") > 0 or the_girl.get_opinion_score("being covered in cum") > 0:
                        the_girl.char "Oh... I want to watch you cum [the_girl.mc_title]. I want to watch you pull that cock out and fire your load right over my face. Paint me with it like the cum slut I am..."
                    else:
                        the_girl.char "Ah... I wonder how long until you cum. I can feel your cock tensing up already..."
                    "You fuck her faster and she moans in response."

            "Fuck her in silence.":
                "For a few moments neither of you say anything. The only sounds are you and [the_girl.possessive_title] panting for breath and the soft smack as you slam your cock deep inside of her."
                if the_girl.get_opinion_score("small talk") < 0:
                    $ the_girl.discover_opinion("small talk")
                    $ the_girl.change_happiness(-the_girl.get_opinion_score("small talk"))
                    "[the_girl.title] seems glad she doesn't have to try and make small talk with you while you fuck her brains out."
                else:
                    "In the relative silence you can hear [the_girl.title] mumbling under her breath."
                    the_girl.char "Oh fuck... Oh fuck yes... Ah..."
                    "The softly spoken words turn you on even more."

    #
    # the_girl.char "Oh... Fuck... Ah..."
    # mc.name "Does that feel good?"
    # if the_girl.effective_sluttiness > 100:
    #     "All [the_girl.title] can do is nod and moan loudly in response. You do your best to drive your cock all the way to it's base, fitting every last inch into [the_girl.title]'s cunt."
    # else:
    #     the_girl.char "It's certainly... Ah... Deep... Wow..."
    #     "She bites her lip and moans softly. You do your best to drive your cock all the way to it's base, fitting every last inch into [the_girl.title]'s cunt."
    return

label scene_piledriver_2(the_girl, the_location, the_object):
    #CHOICE CONCEPT: Fondle a tit // Hold her ankles
    "You settle into a steady rhythm pumping in and out of [the_girl.title]'s pussy. Having her legs bent over lets you get deeper than you normally can."
    #TODO: Minor line depending on her vaginal skill.
    if the_girl.sex_skills["Vaginal"] < 3:
        the_girl.char "Ah... Take it easy, I'm not... use to doing this."
    else:
        the_girl.char "I can feel you so deep inside me..."

    menu:
        "Hold her ankles.": #TODO: Add more stuff to this choice?
            "You grab [the_girl.title]'s ankles and hold them out to the side, spreading her legs and putting her pussy front and center."
            "The position doesn't leave [the_girl.possessive_title] much to do other than get fucked by you. She pants loudly underneath you."
            the_girl.char "I feel so open like this... What are you doing to me [the_girl.mc_title], you're making me into such a slut..."
            if the_girl.core_sluttiness > 90:
                "She moans loudly and turns her head to the side."
                the_girl.char "And I think I like it!"

        "Fondle her tits.":
            if the_girl.has_large_tits():
                if the_girl.outfit.tits_available():
                    "You reach down between [the_girl.title]'s legs with one hand to grab onto one of her tits. It's soft and weighty in your hand."
                    "You give her tit a squeeze and she moans in pleasure. After a few seconds you feel her nipple getting hard."
                    the_girl.char "Be gentle with them, they're sensative."
                    "You play with [the_girl.possessive_title]'s nice big tits for a few seconds. When you're done with that you shift yoru focus back to pounding her tight pussy."

                else:
                    $top_clothing = the_girl.outfit.get_upper_ordered()[-1]
                    "You reach down between [the_girl.title]'s legs with one hand and grab onto a tit. Through her [top_clothing.name] you can feel how weighty they are."
                    "You squeeze it, then shift your hand to the other one and bounce it around. [the_girl.title] moans in pleasure."
                    "After a few seconds you notice [the_girl.possessive_title]'s nipples getting hard and poking up into her [top_clothing.name]."
                    "You play with [the_girl.title]'s nice big tits for a little while longer, then shift your focus back to pounding her tight pussy."

            else:
                if the_girl.outfit.tits_available():
                    "You reach down between [the_girl.title]'s legs with one hand and grab onto one of her small tits. It's nice and perky, bouncing around when you play with it."
                    "After a little stimulation her nipples get hard. You pinch them with between your thumb and fore finger, making her squeek."
                    the_girl.char "Ah! Easy, those are sensitive you know."
                    "You play with [the_girl.possessive_title]'s cute tits for a little while longer, then shift your focus back to pounding her tight pussy."

                else:
                    $top_clothing = the_girl.outfit.get_upper_ordered()[-1]
                    "You reach down between [the_girl.title]'s legs with one hand and try to feel up her tits through her [top_clothing.name]."
                    "After a few seconds of trying you give up, foiled by the fabric in the way."
                    "You settle for pounding her tight little pussy instead."


    # if the_girl.outfit.tits_available():
    #     "You reach down with one hand and fondle [the_girl.title]'s tits, squeezing them and pinching her nipples."
    #     the_girl.char "Ah... That feels so strange..."
    #     mc.name "Do you like it?"
    #     "[the_girl.title] nods and moans in response. You fuck her a little faster."
    # else:
    #     "You reach down with one hand and run it over [the_girl.title]'s tits over her clothes."
    #     mc.name "Wish I could get a better look at these girls."
    #     the_girl.char "Then you'd have to stop fucking me though..."
    #     "You fuck her a little faster and listen to her moan while you consider your dilemma."
    return

label outro_piledriver(the_girl, the_location, the_object):
    "[the_girl.title]'s pussy is warm, tight and wet as you pump in and out of it, pulling you closer and closer to climaxing with each thrust."
    "You reach your limit and feel your orgasm approaching quickly."
    mc.name "Fuck me, I'm going to cum!"
    $ the_girl.call_dialogue("cum_pullout")
    menu:
        "Cum inside of her.":
            if mc.condom:
                "You push yourself as deep as you can manage and pump your load out into her cunt, hopefully contained by your condom."
                $ the_girl.call_dialogue("cum_condom")
                "You take a moment to catch your breath, then you pull your cock out of [the_girl.title] and sit back down. The condom tip is ballooned out, hanging to one side and filled with your cum."
                if the_girl.get_opinion_score("drinking cum") > 0 and the_girl.sluttiness > 50:
                    $ the_girl.discover_opinion("drinking cum")
                    "When you let [the_girl.possessive_title] down she reaches for your cock. With delicate fingers she slides the condom off of you."
                    the_girl.char "It would be a shame to waste all of this, right?"
                    "She smiles and brings the condom to her mouth. She tips the bottom up and drains it into her mouth."
                    $ the_girl.change_slut_temp(the_girl.get_opinion_score("drinking cum"))
                else:
                    "When you let [the_girl.possessive_title] down she reaches for your cock, removes the condom, and ties the end in a knot."
                    the_girl.char "Look at all that cum. Well done."

            else:
                "You gasp and push yourself as deep as you can, draining your balls into [the_girl.title]'s cunt."
                $ the_girl.cum_in_vagina()
                $ piledriver.redraw_scene(the_girl)
                $ the_girl.call_dialogue("cum_vagina")
                "You take a moment to catch your breath, then sit back and pull your cock out of [the_girl.title]."
                "You keep her on her back for a few more seconds, enjoying the way the position keeps your semen pooled inside of her."

        "Cum on her face.":
            if mc.condom:
                "You pull your cock out at the last minute, whipping the condom off with one hand as you aim it towards [the_girl.possessive_title]'s face."
            else:
                "You pull your cock out at the last minute, stroking it off with one hand as you point it towards [the_girl.possessive_title]'s face."
            $ the_girl.cum_on_face()
            $ piledriver.redraw_scene(the_girl)
            if the_girl.sluttiness > 80:
                "[the_girl.title] sticks out her tongue and stares into your eyes as you climax. You spray your load onto her face, splattering some over her tongue and sending some right into her mouth."
                "She closes her mouth and swallows quickly, then bites her lip and smiles at you."
            else:
                "[the_girl.title] closes her eyes and waits for you to climax. You spray your load over her face and dribble a few drops of sperm onto her chest."
            "You sit back and let [the_girl.possessive_title]'s legs down. You enjoy the sight of her covered in your semen when she looks at you."
    return

label transition_piledriver_missionary(the_girl, the_location, the_object):
    "You slide back and let [the_girl.title] lower her legs. You go back to fucking her missionary style."
    the_girl.char "Fuck, you really stretched me out like that..."
    return

label transition_default_piledriver(the_girl, the_location, the_object):
    "You put [the_girl.title] on her back, then lift her legs up and bend her over at the waist. You kneel over her, lining your hard cock up with her tight pussy."
    mc.name "Ready?"
    "[the_girl.possessive_title] nods, and you slip yourself deep, deep inside of her."
    return

label strip_piledriver(the_girl, the_clothing, the_location, the_object):
    the_girl.char "Wait, wait a second."
    $ the_girl.call_dialogue("sex_strip")
    $ the_girl.draw_animated_removal(the_clothing, position = piledriver.position_tag)
    "You let your cock pop out of [the_girl.title]'s pussy and watch as she struggles out of her [the_clothing.name] and throws it to the side."
    the_girl.char "Okay, keep going!"
    "You throw her legs over your shoulders and slide yourself as deep into her cunt as you can get it."
    return

label strip_ask_piledriver(the_girl, the_clothing, the_location, the_object):
    the_girl.char "[the_girl.mc_title], I'd like to ah... take off my... my [the_clothing.name], would you mind?"
    "[the_girl.title] pants as you fuck her hard."
    menu:
        "Let her strip.":
            mc.name "Take it off for me."
            $ the_girl.draw_animated_removal(the_clothing, position = piledriver.position_tag)
            "You let your cock pop out of [the_girl.possessive_title]'s pussy and watch as she struggles out of her [the_clothing.name] and throws it to the side."
            the_girl.char "Okay, keep going now sir!"
            "You throw her legs over your shoulders and slide yourself as deep into her cunt as you can get it."

        "Leave it on.":
            mc.name "No, I like how you look with it on."
            if the_girl.sluttiness < 80:
                the_girl.char "Do you think I look sexy in it?"
                "You speed up, fucking her faster in response to her question."
            elif the_girl.sluttiness < 100:
                the_girl.char "Does it make me look like a good little slut? All I want to be is your good little slut sir."
                "She pushes her hips back into you and moans happily."
            else:
                the_girl.char "Does it make me look like the cum hungry slut that I am? That's all I want to be for you sir, your dirty little cum dumpster!"
                "She grinds her hips back into you and moans ecstatically."
    return

label orgasm_piledriver(the_girl, the_location, the_obejct):
    "[the_girl.title] takes a sharp breath in and you feel her legs try and clench together."
    $ the_girl.call_dialogue("climax_responses_vaginal")
    "You keep fucking [the_girl.possessive_title] through her climax, enjoying her sopping wet cunt while she twitches and moans underneath you."
    "A few seconds later she relaxes and all the tension drains from her body."
    the_girl.char "Keep going [the_girl.mc_title], please make me cum again!"
    return
