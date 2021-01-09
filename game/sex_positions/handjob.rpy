init:
    python:
        handjob = Position(name = "Handjob", slut_requirement = 15, slut_cap = 40, requires_hard = False, requires_large_tits = False,
            position_tag = "stand3", requires_location = "Stand", requires_clothing = "None", skill_tag = "Foreplay",
            girl_arousal = 5, girl_energy = 10,
            guy_arousal = 10, guy_energy = 2,
            connections = [],
            intro = "intro_handjob",
            scenes = ["scene_handjob_1","scene_handjob_2","scene_handjob_3"],
            outro = "outro_handjob",
            transition_default = "transition_default_handjob",
            strip_description = "strip_handjob", strip_ask_description = "strip_ask_handjob",
            orgasm_description = "orgasm_handjob",
            taboo_break_description = "taboo_break_handjob",
            verb = "stroke", verbing = "stroking",
            opinion_tags = ["giving handjobs"], record_class = "Handjobs",
            associated_taboo = "touching_penis")

        list_of_girl_positions.append(handjob)

#init 1:
   #python:
       #Here is where you would put connections if they existed.

label intro_handjob(the_girl, the_location, the_object):
    "[the_girl.title] places her hand on your chest and strokes it gently."
    "She looks into your eyes as her hand runs down your torso, running gently over your abs, down to your waist."
    the_girl.char "Mmm, what do we have here?"
    "Her hand runs tight against your body, into your pants and down to your bulge."
    "A shiver of pleasure shoots up your spine as she strokes it gently over your underwear, caressing your package."
    the_girl.char "Do you want to give me a hand with this? These buttons can be so tricky..."
    "You undo your pants for her and she pull them down, followed quicky by your underwear."
    "Your hard cock springs free into her waiting hand, and she starts to stroke it slowly while holding you close."
    return

label taboo_break_handjob(the_girl, the_location, the_object):
    "[the_girl.title] places a hand on your chest and strokes it tenderly."
    "She looks into your eyes as her hand moves lower, running over your abs, down to your waist."
    if the_girl.effective_sluttiness(handjob.associated_taboo) > handjob.slut_cap:
        "Her fingers slide into your pubic hair, then to the side of your cock and between your legs."
        "She strokes your inner thigh on one side, purposefully avoiding your cock with each movement."
    else:
        "You feel her fingers brush your pubic hair, then pull back and rest on your stomach."

    $ the_girl.call_dialogue(handjob.associated_taboo+"_taboo_break")

    if the_girl.sex_skills["Foreplay"] >= 3:
        "She runs a finger along the bottom of your shaft, ending at the sensitive spot under your tip."
        "Then she wraps her full hand around it and slides it back down to the base."
        "[the_person.possessive_title] begins to stroke you off with long, deliberate motions."
    else:
        "She wraps her fingers around the base of your shaft and squeezes it lightly, then begins to slide her hand up and down your length."
    return

label scene_handjob_1(the_girl, the_location, the_object):
    if not mc.recently_orgasmed:
        "[the_girl.possessive_title]'s hand is warm and soft as it slides up and down your dick."
        if mc.arousal > 40:
            "She rubs her thumb over your tip, spreading your precum over it and then working it back to the shaft."
        else:
            "She rubs her thumb over your tip, then moves to the sensitive underside."
        the_girl.char "You're so big in my hand... Mmm."
    else:
        "[the_girl.possessive_title] fondles your soft cock, rubbing the tip with her thumb."
        the_girl.char "Mmm, even soft you're so big..."
    return

label scene_handjob_2(the_girl, the_location, the_object):
    "[the_girl.title] moves her hand down and cups your balls, massaging them gently."
    the_person.char "I want you to let all of your cum out of here for me..."
    "She holds your body against her and slides her hand back to your shaft."
    return

label scene_handjob_3(the_girl, the_location, the_object):
    "[the_girl.possessive_title] gives you a few fast strokes, then lets go."
    the_girl.char "One second..."
    "She brings her hand up to her mouth and sticks her tongue out, running it from her palm to the tips of her fingers."
    "She reaches back down and wraps her slippery hand around your cock again. She starts to gently stroke it."
    return

label outro_handjob(the_girl, the_location, the_object):
    # describe wanting to cum
    "[the_girl.title]'s touch pulls you closer and closer to your climax. She smiles at you and speeds up."
    the_girl.char "Are you close? I want you to cum for me."
    "Her hand makes wet, sloppy noises as she jerks you towards completion."
    $ slut_willingness = the_girl.effective_sluttiness()
    if slut_willingness > (60 - the_girl.get_opinion_score("drinking cum")*5):
        "Just as you're about to fire your load [the_girl.possessive_title] drops to the ground in front of you."
        $ the_person.draw_person(position = "blowjob")
        the_girl.char "I want you to put that hot load in my mouth."
        "Just hearing her say that would have pushed you over the edge - her soft, wet hand working your cock is just a bonus."
        "She opens up her mouth and sticks out her tongue, presenting you with a clear target."
        $ the_girl.cum_in_mouth()
        "You spasm and shoot out a pulse of hot sperm, splashing it over her tongue and down the back of her throat."
        "She maintains eye contact as you fire off the rest of your load, then closes her mouth and swallows quietly."
        $ the_girl.call_dialogue("cum_mouth")

    elif slut_willingness > (40 - (the_girl.get_opinion_score("cum facials")*5 + the_girl.get_opinion_score("being covered in cum")*5)):
        "Just as you're about to fire your load [the_girl.possessive_title] drops to the ground in front of you."
        $ the_girl.draw_person(position = "blowjob")
        the_girl.char "I want you to cum all over my face. Make me a mess!"
        "Just hearing her say that would have pushed you over the edge - her soft, wet hand working your cock is just a bonus."
        "She strokes you to completion, closing her eyes and aiming your cock as you spasm and start to pulse out your hot load."
        $ the_girl.cum_on_face()
        $ the_girl.draw_person(position = "blowjob")
        "You fire rope after rope of thick cum over [the_person.title]'s waiting face. When you're finished she opens her eyes again and smiles up at you."
        $ the_girl.call_dialogue("cum_face")

    elif slut_willingness > (25 - (the_girl.get_opinion_score("being covered in cum")*5)) and the_girl.has_large_tits():
        # You cum on her tits
        "Just as you're about to fire your load [the_girl.possessive_title] drops to the ground in front of you."
        $ the_girl.draw_person(position = "blowjob")
        the_girl.char "I want you to put your cum all over my tits [the_girl.mc_title]!"
        "Just hearing her say that would have pushed you over the edge, but her soft, wet hand working your cock doesn't hurt either."
        $ the_girl.cum_on_tits()
        if the_girl.outfit.tits_available(): #You can shoot it directly onto her tits
            "She aims your cock and strokes you to completion. You fire your load in thick ropes onto her large and ready tits."
        else:
            $ blocker = the_girl.outfit.get_upper_top_layer()
            if blocker:
                "She aims your cock and strokes you to completion. You fire your load in thick ropes over the shape of her tits and onto her [blocker.name]."
            else:
                "She strokes you to completion and you fire your load onto her tits." # just in case something weird happens and we get None.
        #TODO: Add a "cum_tits" dialogue section for personalities.

    else:
        # You cum into the air/floor
        the_girl.char "Cum for me [the_girl.mc_title], do it!"
        "You reach your limit and start to pulse your load out in thick ropes, past [the_girl.possessive_title]'s thigh and onto the floor."
        "She gives you a few more strokes until you're completely spent, then lets go and gives you a kiss."

    return

label transition_default_handjob(the_girl, the_location, the_object):
    "[the_girl.title] has you stand and faces you, grabbing your cock while she stares into your eyes."
    "She starts to stroke it, slowly sliding her hand up and down your hard shaft."
    return

label strip_handjob(the_girl, the_clothing, the_location, the_object):
    "[the_girl.title] starts to strip off her [the_clothing.name] while stroking you off."
    $ the_girl.call_dialogue("sex_strip")
    $ the_girl.draw_animated_removal(the_clothing, position = handjob.position_tag)
    "She pulls it off and drops it to the ground."
    return

label strip_ask_handjob(the_girl, the_clothing, the_location, the_object):
    the_person.char "[the_person.mc_title], would you like me to take off my [the_clothing.name]?"
    "She keeps stroking your cock while you respond."
    menu:
        "Let her strip.":
            mc.name "Take it off for me."
            $ the_girl.draw_animated_removal(the_clothing, position = handjob.position_tag)
            "[the_girl.possessive_title] strips out of her [the_clothing.name] and drops it to the side."
            the_person.char "Ah, so much better."

        "Leave it on.":
            mc.name "I think you look cute in it, leave it on."
            "She nods and keeps jerking you off."
    return

label orgasm_handjob(the_girl, the_location, the_object):
    "[the_girl.possessive_title]'s breathing picks up and her grip on your cock gets firmer."
    "She holds you tight, her breath warm on your ear and whispers."
    the_person.char "Oh god, I think I'm going to cum... Thinking about this big cock, so close to me..."
    "With one final gasp she shivers with pleasure. She struggles to stroke you off as she climaxes, each movement jerky and wild."
    "The moment passes quickly and she gets her body back under control."
    return
