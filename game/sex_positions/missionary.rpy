init:
    python:
        missionary = Position(name = "Missionary", slut_requirement = 50, slut_cap = 70, requires_hard = True, requires_large_tits = False,
            position_tag = "missionary", requires_location = "Lay", requires_clothing = "Vagina", skill_tag = "Vaginal",
            girl_arousal = 16, girl_energy = 12,
            guy_arousal = 15, guy_energy = 14,
            connections = [],
            intro = "intro_missionary",
            scenes = ["scene_missionary_1","scene_missionary_2"],
            outro = "outro_missionary",
            transition_default = "transition_default_missionary",
            strip_description = "strip_missionary", strip_ask_description = "strip_ask_missionary",
            orgasm_description = "orgasm_missionary",
            taboo_break_description = "taboo_break_missionary",
            opinion_tags = ["missionary style sex","vaginal sex"], record_class = "Vaginal Sex",
            default_animation = missionary_bob,
            associated_taboo = "vaginal_sex")
        list_of_positions.append(missionary)

init 1:
    python:
        missionary.link_positions(piledriver,"transition_missionary_piledriver")

label intro_missionary(the_girl, the_location, the_object):
    "You run your hands along [the_girl.title]'s hips, feeling the shape of her body."
    mc.name "I want you to lie down for me."
    "She nods and lies down on the [the_object.name], waiting while you climb on top of her."
    "[the_girl.possessive_title] wraps her arms around you and holds you close as you line your cock up with her pussy. She sighs happily into your ear as you slide into her."
    return

label taboo_break_missionary(the_girl, the_location, the_object):
    "You take [the_girl.title]'s hands in yours and guide her down onto the [the_object.name]. She follows your lead, lying down for you."
    "You place your hands on her knees and spread her legs, kneeling down between them."
    "You sit your hard cock on her stomach, teasingly close to her warm pussy. [the_girl.possessive_title] reaches down and gently pets your shaft."
    $ the_girl.call_dialogue(missionary.associated_taboo+"_taboo_break")
    if the_girl.effective_sluttiness(missionary.associated_taboo) > missionary.slut_cap:
        "She takes your cock and moves it down, sliding the tip into her pussy for you."

    else:
        "You grab your cock and move it down. [the_girl.title] gasps as your tip flicks over her clit and spreads her pussy lips open."
    "You lie down on top of her and thrust forward. After a moment of resistance you slide easily into her slippery, warm tunnel."
    the_girl.char "Ah..."
    "You hold yourself deep inside of her for a few seconds, then pull back and begin slowly thrust in and out."
    return

label scene_missionary_1(the_girl, the_location, the_object):
    # CHOICE CONCEPT: Kiss her neck // Talk dirty to her
    # Intro concept. Short difference depending on if she's wet or not.
    if the_girl.arousal > 50:
        "[the_girl.title]'s pussy is nice and wet as you pump your hips and fuck her."
    else:
        "[the_girl.title]'s pussy is still getting wet. You take it slow, giving her time to warm up."

    menu:
        "Kiss her neck.":
            "You lean down and start to kiss at [the_girl.possessive_title]'s neck. She tilts her head to the side to let you."
            if mc.sex_skills["Foreplay"] > 2:

                if the_girl.get_opinion_score("kissing") > 0:
                    $ the_girl.discover_opinion("kissing")
                    $ the_girl.change_arousal(the_girl.get_opinion_score("kissing"))
                the_girl.char "[the_girl.mc_title]... Oh [the_girl.mc_title] that feels so good."
                "She moans into your ear and pulls you closer to her."
                "You kiss her neck a few more times, then lean back and look into her eyes. She sighs happily and returns your gaze, locking eyes with you while you fuck her."
            else:
                "You do your best to split your focus between kissing [the_girl.title] and pumping your hips, but you find yourself slipping out of the steady rhythm you had established."
                "[the_girl.possessive_title] sighs happily and whispers in your ear."
                the_girl.char "That feels nice, but I want you to keep fucking me."
                "You kiss her one last time, then divert all of your attention to making love."

        "Talk dirty to her.":
            mc.name "You feel amazing [the_girl.title], I wish I could fuck you like this all day."
            if the_girl.core_sluttiness > 60 or the_girl.get_opinion_score("being submissive" > 0):
                the_girl.char "Then do it. Pin me against the [the_object.name] and fuck me all you want."
                "She wraps her legs around your waist and pulls you deep inside of her. The tight, warm feeling of her cunt makes your cock twitch."
                if the_girl.get_opinion_score("creampies") > 0:
                    the_girl.char "You can cum anywhere you want. You can pump your load right into me if that's what you want. If that's what would make you happy..."
                else:
                    the_girl.char "You can use me however you want [the_girl.mc_title], I'll be your obedient fuck toy, if that's what you want me to be..."
                "She moans into your ear and trembles beneath you."
            else:
                the_girl.char "Ah... I'm glad you're having a good time."
                mc.name "I bet you are too."
                the_girl.char "I... oh god, I am."
                "She blushes and turns away from you, panting for breath while you fuck her."

    # $ the_girl.call_dialogue("sex_responses_vaginal")
    # "[the_girl.title] digs her fingers into your back as you pump in and out of her tight slit. She moans into your ear, letting you hear her soft gasps and yelps."
    # if the_girl.arousal > 50:
    #     "Her pussy is dripping wet now, practically begging you to fuck it more. You kiss her and keep going."
    # else:
    #     "Her pussy is starting to get nice and wet as you fuck it. You kiss her and keep going."
    return

label scene_missionary_2(the_girl, the_location, the_object):
    # CHOICE CONCEPT: Pin her down // Kiss her
    if the_girl.sex_skills["Vaginal"] < 3 and the_girl.arousal < 50:
        # INTRO: She's inexperienced and needs some help.
        "[the_girl.title]'s slit is tight and warm, but you can tell she's still getting wet."
        the_girl.name "Could you... take it a little slower for me? Sorry, I'm just not very good at this."
        menu:
            "Go easy on her.":
                mc.name "Of course."
                "You slow your thrusts and hold [the_girl.possessive_title] close to you. You can feel her warm breath against your ear and hear her soft moans."
                mc.name "Is that better?"
                the_girl.char "Yeah. Ah..."
                "Little by little [the_girl.title] gets wetter and you're able to speed up. Her panting in your ear becomes louder and more passionate."


            "Fuck her hard anyways.":
                mc.name "Don't worry, just relax and it'll all come naturally to you."
                "You speed up and fuck [the_girl.title]s tight little cunt. She lets out a surprised gasp."
                if the_girl.get_opinion_score("being submissive") > 0:
                    "[the_girl.possessive_title] grabs at your back and moans right into your ear."
                    the_girl.char "Wait... I don't think I can... handle your big cock!"
                    $ the_girl.discover_opinion("being submissive")
                    $ the_girl.change_arousal(the_girl.get_opinion_score("being submissive"))
                    "You feel her body tremble beneath you and her pussy get suddenly wetter."
                    mc.name "It doesn't matter what you think. I'm going to fuck you until I'm done."
                    if the_girl.get_opinion_score("bareback sex") > 0:
                        the_girl.char "Oh my god, you're fucking me raw and going to get me pregnant... I'm such a worthless, dirty slut that you don't even care if you get me pregnant..."
                        $ the_girl.discover_opinion("bareback sex")
                    else:
                        the_girl.char "Oh my god... I'm just a worthless, dirty slut to you..."
                    "She shivers again, apparantly turned on by the thought."
                    "You fuck [the_girl.possessive_title] hard and fast for as long as you can manage, but eventually you need to slow down to a more maintainable pace."

                else:
                    the_girl.char "Ow! Ow, please slow down..."
                    mc.name "You can manage."
                    $ the_girl.change_arousal(-1+the_girl.get_opinion_score("being submissive"))
                    $ the_girl.change_obedience(-1+the_girl.get_opinion_score("being submissive"))
                    "[the_girl.title] pushes against you and foces you to slide out of her pussy."
                    the_girl.char "No, really, I need you to go slower or I can't do this"
                    "You finally nod and she lets you slide back inside of her. This time you move more slowly, and after a few moments you've moved past the incident."

    else:
        # INTRO: She takes you easily and wraps her arms around you.
        "[the_girl.title]'s slit is tight and wet as you fuck her. She moans into your ear."
        the_girl.char "Take me, [the_girl.mc_title], I'm all yours..."
        menu:
            "Fondle her tits.":
                if the_girl.has_large_tits() :
                    if the_girl.outfit.tits_available():
                        "You plant a hand on [the_girl.possessive_title]'s nice, soft tits and squeeze it. You use your thumb to rub her already hard nipple."
                        the_girl.char "Oh god, go easy on them. They're sensitive!"
                        "You enjoy the squishy weight of her breasts for a few moments, then shift your focus back to fucking her."

                    else:
                        $top_clothing = the_girl.outfit.get_upper_ordered()[-1]
                        "You plant a hand on [the_girl.possessive_title]'s big tits and fondle them through her [top_clothing.name]."
                        the_girl.char "Mmm, you should just pull that out of the way. I want you to be able to grab them and squeeze them."

                else:
                    if the_girl.outfit.tits_available():
                        "You run a hand over [the_girl.possessive_title]'s cute little tits, pausing to pinch one of her nipples."
                        the_girl.char "Oh! Easy there, it's sensitive."
                        "You rub her nipple for a moment and feel it get hard, then move to her other breast and do the same."
                    else:
                        $top_clothing = the_girl.outfit.get_upper_ordered()[-1]
                        "You try and feel up [the_girl.possessive_title]'s little tits, but her [top_clothing.name] stops you from getting much more than a handful of fabric."
                        "You give up and focus on fucking her instead."

            "Pin her down.":
                "You grab [the_girl.title]'s hands and lift them above her head. You push them against the [the_object.name] and pin [the_girl.title] underneath you."
                if the_girl.get_opinion_score("being submissive") > 0:
                    the_girl.char "Oh my god [the_girl.mc_title], what are you going to do to me?"
                    "She bites her lip and looks up at you."
                    mc.name "Whatever I want. Keep your legs spread for me."
                    $ the_girl.change_arousal(the_girl.get_opinion_score("being submissive"))
                    $ the_girl.discover_opinion("being submissive")
                    "You fuck her hard and fast. [the_girl.possessive_title] gasps and moans, her hips bucking with pleasure."
                    the_girl.char "Ah! You've got me held down and there's nothing I can do..."
                    "She tests your grip on her hands and shivers with pleasure when you force them back down and keep her in place. You can hear her talking softly to herself."
                    the_girl.char "I'm just a fuck toy to you right now... Just a soft wet hole for you to fuck with that big cock... Ah!"
                    if the_girl.get_opinion_score("bareback sex") > 0:
                        the_girl.char "You could fuck me until you cum inside. You might get me pregnant and all I can do is sit here and get fucked like a slut... Oh my god..."
                    elif the_girl.get_opinion_score("creampies") > 0:
                        the_girl.char "You could cum right inside me and there's nothing I could do to stop you... You would just fuck me full of your cum!"
                    "[the_girl.title]'s pussy feels great to fuck, but you can't keep this pace up forever. You let go of her hands and slow down."
                    "You're both silent for a few seconds, panting for breath."
                    the_girl.char "Don't stop..."

                elif the_girl.get_opinion_score("being submissive") < 0:
                    the_girl.char "Woah, easy there..."
                    mc.name "Keep those legs spread for me."
                    "She rolls her eyes and spreads her legs. You start to fuck her hard and fast."
                    the_girl.char "Let my hands go, I want to be able to feel you. I want to touch you."
                    $ the_girl.change_arousal(the_girl.get_opinion_score("being submissive"))
                    $ the_girl.discover_opinion("being submissive")
                    "It's clear [the_girl.title] isn't enjoying being dominated as much as you were expecting. You let her hands go and she pulls you close against her."
                    the_girl.char "Much better."

                else:
                    the_girl.char "Oh! Hello there..."
                    mc.name "Spread your legs for me, I want to get nice and deep."
                    "She does what you want and spreads her legs. You start to fuck her hard and fast."
                    the_girl.char "Fuck me... Oh fuck me harder!"
                    "She pants and moans underneath you. You keep the pace up as long as you can manage, fucking [the_girl.title]'s tight, wet cunt while she's pinned underneath you."
                    "You keep up the pace as long as you can manage, but eventually you have to slow down and catch your breath."
                    the_girl.char "That was... that felt great, it was so intense."
                    "She licks at your ear, then whispers into it."
                    the_girl.char "Don't stop..."
    return

label outro_missionary(the_girl, the_location, the_object):
    "You get to hear every little gasp and moan from [the_girl.title] as you're pressed up against her. Combined with the feeling of fucking her pussy it's not long before you're pushed past the point of no return."
    mc.name "I'm going to cum!"
    $ the_girl.call_dialogue("cum_pullout")
    menu:
        "Cum inside of her.":
            "You use your full weight to push your cock deep inside of [the_girl.possessive_title]'s cunt as you climax. She gasps and claws lightly at your back as you pump your seed into her."

            if mc.condom:
                $ the_girl.call_dialogue("cum_condom")
                "You take a moment to catch your breath, then roll off of [the_girl.possessive_title] and lie beside her."
                "Your condom is ballooned with your seed, hanging off your cock to one side."
                if the_girl.get_opinion_score("drinking cum") > 0 and the_girl.effective_sluttiness() > 50:
                    $ the_girl.discover_opinion("drinking cum")
                    "[the_girl.possessive_title] reaches over for your cock. With delicate fingers she slides the condom off of you, pinching it off do your cum doesn't spill out."
                    the_girl.char "It would be a shame to waste all of this, right?"
                    "She smiles and brings the condom to her mouth. She tips the bottom up and drains it into her mouth."
                    $ the_girl.change_slut_temp(the_girl.get_opinion_score("drinking cum"))
                else:
                    "[the_girl.possessive_title] reaches over for your cock, removes the condom, and ties the end in a knot for you."
                    the_girl.char "Look at all that cum. Well done."

            else:
                $ the_girl.call_dialogue("cum_vagina")
                $ the_girl.cum_in_vagina()
                $ missionary.redraw_scene(the_girl)
            "You take a moment to catch your breath, then roll off of [the_girl.possessive_title] and lie beside her."

        "Cum on her chest.":
            $ the_girl.cum_on_stomach()
            $ missionary.redraw_scene(the_girl)
            if mc.condom:
                "You pull out at the last moment and grab your cock. You whip off your condom and stroke yourself off, blowing your load over [the_girl.title]'s stomach."
            else:
                "You pull out at the last moment and grab your cock. You kneel and stroke yourself off, blowing your load over [the_girl.title]'s stomach."
            the_girl.char "Ah... Good job... Ah..."
            "You sit back and sigh contentedly, enjoying the sight of [the_girl.possessive_title]'s body covered in your semen."
    return

label transition_missionary_piledriver(the_girl, the_location, the_object):
    "[the_girl.title]'s pussy feels so warm and inviting, you can't help but want to get deeper inside of her. You pause for a moment and reach down for her legs."
    the_girl.char "Hey, what's... Whoa!"
    "You pull her legs up and bend them over her shoulders. You hold onto her ankles as you start to fuck her again, pushing your hard cock nice and deep."
    return

label transition_default_missionary(the_girl, the_location, the_object):
    "You put [the_girl.title] on her back and lie down on top of her, lining your hard cock up with her tight cunt."
    "After running the tip of your penis along her slit a few times you press forward, sliding inside of her. She gasps softly and closes her eyes."
    return

label strip_missionary(the_girl, the_clothing, the_location, the_object):
    $ the_girl.call_dialogue("sex_strip")
    $ the_girl.draw_animated_removal(the_clothing, position = missionary.position_tag)
    "[the_girl.possessive_title] struggles out of her [the_clothing.name] and throws it to the side. Then she gets herself lined up in front of you again."
    "She sighs happily when you slip back inside of her."
    return

label strip_ask_missionary(the_girl, the_clothing, the_location, the_object):
    the_girl.char "[the_girl.mc_title], I'd like to take off my [the_clothing.name], would you mind?"
    "[the_girl.title] pants as you fuck her."
    menu:
        "Let her strip.":
            mc.name "Take it off for me."
            $ the_girl.draw_animated_removal(the_clothing, position = missionary.position_tag)
            "You move back kneel for a moment while [the_girl.title] struggles out of her [the_clothing.name] and throws it to the side. Then she gets herself lined up in front of you again."
            "She sighs happily when you get on top of her and slide your cock back inside."

        "Leave it on.":
            mc.name "No, I like how you look with it on."
            if the_girl.sluttiness < 80:
                the_girl.char "Do you think I look sexy in it?"
                "You speed up, fucking her faster in response to her question."
            elif the_girl.sluttiness < 100:
                the_girl.char "Does it make me look like a good little slut? All I want to be is your good little slut sir."
                "She pushes her hips against yours and moans happily."
            else:
                the_girl.char "Does it make me look like the cum hungry slut that I am? That's all I want to be for you sir, your dirty little cum dumpster!"
                "She grinds her hips against you and moans ecstatically."
    return

label orgasm_missionary(the_girl, the_location, the_object):
    "[the_girl.title] turns her head and pants loudly. Suddenly she bucks her hips up against yours and gasps."
    $ the_girl.call_dialogue("climax_responses_vaginal")
    "Her pussy is dripping wet as you fuck through her climax. She paws at the [the_object.name], trying to find something to hold onto."
    "After a few seconds she lets out a long sigh and all the tension drains out of her body. You slow down your thrusts to catch your own breath."
    the_girl.char "Don't stop [the_girl.mc_title], I might be able to get there again..."
    return
