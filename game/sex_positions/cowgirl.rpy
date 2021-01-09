init:
    python:
        cowgirl = Position(name = "Cowgirl", slut_requirement = 60, slut_cap = 80, requires_hard = True, requires_large_tits = False,
            position_tag = "cowgirl", requires_location = "Lay", requires_clothing = "Vagina", skill_tag = "Vaginal",
            girl_arousal = 18, girl_energy = 14,
            guy_arousal = 14, guy_energy = 10,
            connections = [],
            intro = "intro_cowgirl",
            scenes = ["scene_cowgirl_1","scene_cowgirl_2","scene_cowgirl_3"],
            outro = "outro_cowgirl",
            transition_default = "transition_default_cowgirl",
            strip_description = "strip_cowgirl", strip_ask_description = "strip_ask_cowgirl",
            orgasm_description = "orgasm_cowgirl",
            taboo_break_description = "taboo_break_cowgirl",
            opinion_tags = ["taking control", "vaginal sex"], record_class = "Vaginal Sex",
            default_animation = blowjob_bob,
            associated_taboo = "vaginal_sex")

        list_of_girl_positions.append(cowgirl)

#init 1:
#    python:
#        ##Here is where you would put connections if they existed.

label intro_cowgirl(the_girl, the_location, the_object):
    the_girl.char "Lie down for me, I want to be on top."
    "You lie down on the [the_object.name] and undo your pants. [the_girl.title] swings a leg over your body and straddles you."
    if the_girl.outfit.vagina_visible():
        "She leans back and grinds herself against you. The shaft of your cock rubs against the lips of her pussy."
    else:
        $ blocking_item = the_girl.outift.get_visible_lower()[0]
        "She leans back and grinds herself against you. Underneath her [blocking_item.name] you can feel the lips of her pussy sliding along the length of your shaft."
    the_girl.char "Ready?"
    if the_girl.sex_skills["Vaginal"] >= 3:
        "You nod. She grinds forward one last time, then lifts herself up and lets your tip fall into place. With one smooth movement she slides you deep into her tight cunt."
    else:
        "You nod and she lifts herself up. She reaches down with one hand and holds onto your cock to hold it steady."
        "When she has you in place she lowers herself down slowly, sliding you inch by inch into her tight cunt."
    the_girl.char "Ah..."
    "After pausing for a second to adjust [the_girl.possessive_title] starts to ride your dick."
    return

label taboo_break_cowgirl(the_girl, the_location, the_object):
    "[the_girl.possessive_title] leads you to the [the_object.name]."
    the_girl.char "Lie down for me [the_girl.mc_title]..."
    "You nod and follow her instructions. She steps over you and kneels down, straddling your hips."
    if the_girl.effective_sluttiness(cowgirl.associated_taboo) > cowgirl.slut_cap:
        "She reaches between her legs and grabs your cock, bringing it towards her and running the tip against her clit."
        "You feel her thighs tremble with pleasure."
    else:
        "She reaches between her legs and grabs your cock, rubbing it against her stomach and stroking it gently."
    $ the_girl.call_dialogue(cowgirl.associated_taboo+"_taboo_break")
    "[the_girl.title] lifts herself up, puts your hard cock in line with her pussy, and starts to lower herself down."
    "You feel a moment of resistance as your cock spreads her open, then her body weight carries her all the way down your shaft."
    "She closes her eyes and moans, holding your entire length inside of her for a few seconds."
    "When she's ready she leans forward and starts to move her hips up and down, sliding your cock in and out of her wet pussy."
    return

label scene_cowgirl_1(the_girl, the_location, the_object):
    if the_girl.arousal > 50:
        "[the_girl.title] leans back, putting her hands in line with your feet."
        "In her reclined position you have a perfect view of her pussy wrapped around your dick. She pumps her hips up and down while you enjoy the show."
        the_girl.char "Does that feel good? You feel so big inside me..."

    else:
        "[the_girl.title] leans back, putting her hands in line with your feet, and slows down her rhythm."
        the_girl.char "I need to take it a little slow until I get wet."
        "You have a perfect view of her pussy wrapped around your dick. She moves herself up and down it at a leisurely pace and each stroke feels like warm satin."
        mc.name "Take all the time you need."
    return

label scene_cowgirl_2(the_girl, the_location, the_object):
    "[the_girl.title] speeds up, working her thighs to pump herself up and down your cock."
    if the_girl.has_large_tits():
        if the_girl.outfit.tits_visible():
            "Her large, unconstrained tits bouncse up and down with each stroke."
            the_girl.char "Fuck, hold onto these!"
            "[the_girl.possessive_title] reaches down and grabs your hands. She brings them up to her tits and plants them there."
            "She moans and grinds your hands into her breasts, then puts her hands on your chest and focuses on fucking you."
        else:
            $ the_clothing = the_girl.outfit.get_upper_visible()[0]
            "Her large tits are barely contained by her [the_clothing.name]. You watch them bounce around as she fucks you vigorously."
    else:
        if the_girl.outfit.tits_visible():
            "She reaches up and grabs onto one of her own small tits, squeezing it while she rides you."
            the_girl.char "Ah!"
        else:
            $ the_clothing = the_girl.outfit.get_upper_visible()[0]
            "She reaches up and grabs onto one of her small tits through her [the_clothing.name]. She kneeds it through the fabric and moans loudly while she rides you."
            the_girl. char "Ah!"
    return

label scene_cowgirl_3(the_girl, the_location, the_object):
    "You put your hands on [the_girl.title]'s hips and guide her up and down at a steady pace."
    if the_girl.arousal > 75:
        "Your cock glides effortlessly in and out of her dripping wet pussy. The warm, tight sensation feels incredible."
    else:
        "Her pussy is warm, tight, and getting wetter by the second."
    "With [the_girl.possessive_title] in control you're able to relax and focus entirely on enjoying the feeling."
    return

label outro_cowgirl(the_girl, the_location, the_object):
    "With each stroke of her hips [the_girl.title] brings you closer and closer to cumming. You're finally driven past the point of no return."
    mc.name "Fuck, I'm going to cum!"

    #Perhaps an option where she hesitates and you grab her hips and pull her down while you cum.
    if the_girl.wants_creampie() or mc.condom:
        #She drops down on you as you cum.
        the_girl.char "Yes! Ah!"
        "[the_girl.title] drops herself down, grinding her hips against yours and pushing cock as deep into her as possible."
        "Her breath catches in her throat when you pulse out your hot load of cum deep inside of her."
        #the_girl.char "Oh my god... Give it all to me [the_girl.mc_title]... Fill me up..."
        if mc.condom:
            $ the_girl.call_dialogue("cum_condom")
            "She rocks herself back and forth on you until you're completely spent, then she pulls up and lets your dick fall out of her."
            "The tip of your condom is ballooned out and hanging to the side, filled with your warm seed."
            if the_girl.get_opinion_score("drinking cum") > 0 and the_girl.sluttiness > 50:
                $ the_girl.discover_opinion("drinking cum")
                "[the_girl.possessive_title] reaches below her for your cock. With delicate fingers she slides your condom off, pinching above the bulge to keep your cum from spilling out."
                the_girl.char "It would be a shame to waste all of this, right?"
                "She smiles and brings the condom to her mouth. She tips the bottom up and drains it into her mouth."
                $ the_girl.change_slut_temp(the_girl.get_opinion_score("drinking cum"))
            else:
                "[the_girl.possessive_title] reaches for your cock, removes the condom carefully, and ties the end in a knot."
                the_girl.char "Look at all that cum. Well done."
        else:
            $ the_girl.call_dialogue("cum_vagina")
            $ the_girl.cum_in_vagina()
            $ cowgirl.redraw_scene(the_girl)
            "She rocks herself back and forth on you until you're completely spent, then she pulls up and lets your dick fall out of her."
            "[the_girl.possessive_title] straddles you for a few more seconds as she catches her breath. Your cum drips out of her and onto your stomach."
        "She rolls off and lies next to you on the [the_object.name]."

    elif the_girl.effective_sluttiness("creampie") < 60:
        #She always pull off and you cum on her stomach.
        #There is no condom branch here because 100% of the condom branches go to the first version.
        the_girl.char "Oh shit, you can't cum inside me!"
        "[the_girl.possessive_title] jerks up, pulls off your cock, and lowers herself back down."
        "She leans back and uses one hand to push your shaft against the lips of her pussy, grinding against it until you climax."
        the_girl.char "Cum for me [the_girl.mc_title], I want you to cum on me!"
        "You tense up and cum, shooting your thick load up and onto [the_girl.title]'s stomach. She keeps grinding against you're completely spent."
        $ the_girl.cum_on_stomach()
        $ cowgirl.redraw_scene(the_girl)

    else:
        #She hesitates and you can decide to pull her down or not.
        #There is no condom branch here because 100% of the condom branches go to the first version.
        "[the_girl.title] starts to pull up and off of you. She hesistates with the tip of your cock just inside of her pussy."
        the_girl.char "I... I really shouldn't let you..."
        "She bites her lip and moans, unsure of what to do."
        menu:
            "Pull her down and cum inside her.":
                "You reach up and grab [the_girl.possessive_title] by the hips. With one confident pull she plunges back onto your cock, gasping with pleasure."
                "The feeling of her warm, wet pussy sliding down and englufing your cock again pushes you over the edge. You pull [the_girl.title] tight against you and unload inside of her."
                the_girl.char "Ah! Just... Just this once!"
                $ the_girl.call_dialogue("cum_vagina")
                $ the_girl.cum_in_vagina()
                $ the_girl.change_obedience(3)
                "You give a few half-hearted pumps when you're done, then tap [the_girl.title] on the ass. She slides off of your dick and collapses beside you."

            "Let her pull off and cum on her stomach.":
                "You stay silent. [the_girl.possessive_title] waits another second, as if waiting to be convinced, then pulls off of your cock."
                "She grinds the lips of her pussy against your shaft as you climax. You fire your hot load over her stomach."
                $ the_girl.cum_on_stomach()
                $ cowgirl.redraw_scene(the_girl)
                the_girl.char "Whew, that was close..."
                "She rolls off and lies next to you on the [the_object.name]."
    return

label transition_default_cowgirl(the_girl, the_location, the_object):
    "You lie down on [the_object.name]. [the_girl.title] swings a leg over your waist and straddles you."
    if the_girl.sex_skills["Vaginal"] >= 3:
        "She grinds her pussy against your shaft, then lifts herself up and lets your tip fall into place. With one smooth movement she slides you deep into her tight cunt."
    else:
        "She lifts herself up and reaches down with one hand. She holds onto your cock to hold it steady while she lines it up with herself."
        "When she has you in place she lowers herself down slowly, sliding you inch by inch into her tight cunt."
    return

label strip_cowgirl(the_girl, the_clothing, the_location, the_object):
    $ the_girl.call_dialogue("sex_strip")
    $ the_girl.draw_animated_removal(the_clothing, position = cowgirl.position_tag)
    "[the_girl.title] struggles out of her [the_clothing.name] and throws it to the side."
    return

label strip_ask_cowgirl(the_girl, the_clothing, the_location, the_object):
    the_girl.char "[the_girl.mc_title], I'd like to take off my [the_clothing.name]. Would you mind?"
    menu:
        "Let her strip.":
            mc.name "Take it off for me."
            $ the_girl.draw_animated_removal(the_clothing, position = cowgirl.position_tag)
            "[the_girl.title] slows down her pace while she strips out of her [the_clothing.name]. When she's free of it she puts her hands on your chest and fucks you faster again."

        "Leave it on.":
            mc.name "No, I like how you look with it on."
            if the_girl.sluttiness < 70:
                the_girl.char "Yeah? Do I look sexy in it?"
                "She sighs happily while she rides you."
            else:
                the_girl.char "Yeah? Do I look like a good little slut in it? Because that's what I feel like right now!"
                "She sighs happily while she rides your cock hard and fast."
    return

label orgasm_cowgirl(the_girl, the_location, the_object):
    "[the_girl.title] works her hips faster and her breathing grows heavier."
    $ the_girl.call_dialogue("climax_responses_vaginal")
    the_girl.char "With one last gasp she collapses down against you. Her thighs quiver as she climaxes."
    "After a second [the_girl.title] regains control of herself. Her breath is warm against your ear as she whispers to you."
    the_girl.char "I can't stop now, I want you to make me cum again!"
    "She leans back and starts to ride you faster than ever."
    return
