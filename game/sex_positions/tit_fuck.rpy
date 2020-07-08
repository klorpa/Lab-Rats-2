init:
    python:
        tit_fuck = Position(name = "Tit Fuck", slut_requirement = 30, slut_cap = 55, requires_hard = True, requires_large_tits = True,
            position_tag = "blowjob", requires_location = "Kneel", requires_clothing = "Tits", skill_tag = "Foreplay",
            girl_arousal = 5, girl_energy = 20,
            guy_arousal = 15, guy_energy = 5,
            connections = [],
            intro = "intro_tit_fuck",
            scenes = ["scene_tit_fuck_1","scene_tit_fuck_2"],
            outro = "outro_tit_fuck",
            transition_default = "transition_default_tit_fuck",
            strip_description = "strip_tit_fuck", strip_ask_description = "strip_ask_tit_fuck",
            orgasm_description = "orgasm_tit_fuck",
            taboo_break_description = "taboo_break_tit_fuck",
            opinion_tags = ["giving tit fucks"], record_class = "Tit Fucks",
            default_animation = tit_bob,
            associated_taboo = "touching_body")

        list_of_positions.append(tit_fuck) #TODO: Decide if this should be a girl_position too.

#init 1:
   #python:
       #Here is where you would put connections if they existed.
       #TODO: Transition to a tit-blowjob.

label intro_tit_fuck(the_girl, the_location, the_object):
    #This position requires free (and big) tits, so we can assume they're available for everything.
    "You place a hand on [the_girl.possessive_title]'s shoulder and rub it gently, then move down to her sizeable [the_girl.tits] cup tits and squeeze them."
    the_girl.char "Ah... Do you like them?"
    mc.name "Of course I like them. I'd like them even more if they were wrapped around my cock."
    "She smiles and nods, reaching down to your waist and undoing your pants zipper."
    $ tit_fuck.redraw_scene(the_girl)
    "When your cock springs out, already hard, she drops to her knees in front of you."
    "She takes her tits up in her hands and lifts them up, pressing them on either size of your shaft."
    if rank_tits(the_girl.tits) >= 7: #E sized or larger
        "They're warm, soft, and feel like they melt around your sensitive dick. Her breasts are so large the tip of your cock doesn't even make it to the top of her cleavage."
    else:
        "They're warm, soft, and feel like they melt around your sensitive dick. The tip of your cock just barely pops out of the top of her cleavage."
    return

label taboo_break_tit_fuck(the_girl, the_location, the_object):
    "You place a hands on [the_girl.possessive_title]'s shoulders and rub them gently for a few seconds."
    "Then you move them lower, towards her sizeable [the_girl.tits] cup tits."
    "You're just about to grab them when she reaches up and holds your hands, stopping you from moving them any closer."
    $ the_girl.call_dialogue(tit_fuck.associated_taboo+"_taboo_break")
    "She lets go of your hands and you slide them over her breasts. They're soft and heavy with a pleasant jiggle to them."
    mc.name "These feel amazing. Could you use them to take care of this?"
    "You grind your erection against [the_girl.title]'s thigh while you squeeze her tits."
    #TODO: Maybe also a taboo break for touching your penis
    if the_girl.effective_sluttiness(tit_fuck.associated_taboo) > tit_fuck.slut_cap:
        the_girl.char "Of course I can. You're going to have to let go of these first though."
        "She places her hands over yours and presses them against her breasts."
        the_girl.char "I promise I'll put them to good use."
        "She lets go of your hands and kneels down, taking her tits into her own hands."
    else:
        the_girl.char "I can try. You're going to have to let go of me first though."
        "She lifts your hands off of her chest and kneels down, taking her tits up into her own hands"
    $ the_girl.draw_person(position = "blowjob")
    "She hefts her breasts up and presses them on either side of your shaft."
    if rank_tits(the_girl.tits) >= 7: #E sized or larger
        "They're warm, soft, and feel like they melt around your sensitive dick. Her breasts are so large the tip of your cock doesn't even make it to the top of her cleavage."
    else:
        "They're warm, soft, and feel like they melt around your sensitive dick. The tip of your cock just barely pops out of the top of her cleavage."
    $ tit_fuck.redraw_scene(the_girl)
    "She starts to heft them up and down, working your cock with them."
    return

label scene_tit_fuck_1(the_girl, the_location, the_object):
    "[the_girl.possessive_title] works her tits up and down your cock, alternating between slow and fast strokes."
    the_girl.char "Mmm, do my tits feel good? Your cock feels so good between them."
    "She jiggles her tits in opposite directions to each other, then presses down hard on them and gives you a few powerful strokes."
    return

label scene_tit_fuck_2(the_girl, the_location, the_object):
    "You reach down and grab [the_girl.title]'s tits yourself. You place your hands over hers and hold them in place."
    the_girl.char "Mmm, fuck my tits [the_girl.mc_title], they're all yours."
    "You squeeze down hard on her breasts and work your hips, fucking her soft cleavage. [the_girl.title] moans in response."
    "When you're satisfied you let go and let her take over again."
    return

label scene_tit_fuck_3(the_girl, the_location, the_object):
    "[the_girl.possessive_title] gives you a few fast strokes with her tits, then stops and tilts her head down."
    "She lets a long line of saliva drip down between her tits and onto the tip of your cock."
    "She gives your shaft a few strokes, spreading her spit and lubricating her cleavage. She looks up at you from her knees and smiles."
    the_girl.char "There, much better."
    "She starts servicing you her tits again, now gliding quickly and easily over your hard dick."
    return


label outro_tit_fuck(the_girl, the_location, the_object):

    "Her warm, soft tits wrapped around your sensitive cock drive you closer and closer to climax with each stroke up and down."
    the_girl.char "You're so tense, are you going to cum?"
    "You nod and she speeds up."
    the_girl.char "Cum for me [the_girl.mc_title], cum for me!"
    menu:
        "Cum between her tits.":
            "You close your eyes and focus on the sensation of [the_girl.possessive_title]'s warm, soft breasts massaging your cock."
            "Your orgasm builds to a peak and you grunt, blasting your load up between [the_girl.title]'s tits and out the top of her cleavage."
            $ blocker = the_girl.outfit.get_upper_top_layer()
            if blocker: #There's something on her top
                "Your cum splatters down over [the_girl.title]'s [blocker.name]. She gasps as the warm liquid covers her and drips back down between her tits."
            else:
                "Your cum splatters down over the top of [the_girl.title]'s tits. She gasps as the warm liquid covers her and drips back down between her tits."

            $ the_person.cum_on_tits()
            $ tit_fuck.redraw_scene(the_girl)

        "Cum on her face.":
            "You close your eyes and focus on the sensation of [the_girl.possessive_title]'s warm, soft breasts massaging your cock."
            "As your orgasm builds to it's peak you step back, sliding your cock out from her cleavage and take it up in your own hand."
            if the_girl.effective_sluttiness() > 40 or the_girl.get_opinion_score("cum facials") > 0:
                "[the_girl.title] understands immediately what is about to happens and tilts her head up, giving you a clear target."
                "You stroke yourself to completion and blast your load over her face, throwing thick ropes of cum her lips and nose and eyes."
            else:
                the_girl.char "What's wrong? I...!"
                "You grunt and climax, blasting thick ropes of cum over [the_girl.title]'s surprised face. She jerks back, then waits until you're finished."
            $ the_girl.cum_on_face()
            $ tit_fuck.redraw_scene(the_girl)

    the_girl.char "Ah... Wow..."
    return

label transition_default_tit_fuck(the_girl, the_location, the_object):
    "You grab a hold of sizeable tits and give them a gentle squeeze, bringing a little moan from her lips."
    mc.name "I want to feel my cock between these lovely tits."
    "She smiles and nods, dropping to her knees in front of you. She gathers her tits up in her hands and presses them to the side of your shaft."
    return

label strip_tit_fuck(the_girl, the_clothing, the_location, the_object):
    $ the_girl.call_dialogue("sex_strip")
    "[the_girl.title] leans back, letting your cock slide out of her cleavage, and pulls off her [the_clothing.name]."
    $ the_girl.draw_animated_removal(the_clothing, position = tit_fuck.position_tag)
    "She pulls it off and drops it at her side, then leans back and engulfs your hard cock in her breasts again."
    return

label strip_ask_tit_fuck(the_girl, the_clothing, the_location, the_object):
    the_person.char "[the_person.mc_title], would you like me to take off my [the_clothing.name]?"
    "She works her tits up and down while she waits for you to respond."
    menu:
        "Let her strip.":
            mc.name "Take it off for me."
            $ the_girl.draw_animated_removal(the_clothing, position = tit_fuck.position_tag)
            "[the_girl.title] leans back, letting your cock slide out of her cleavage, and pulls off her [the_clothing.name]."
            the_person.char "Ah, so much better. Now, where were we..."
            "She leans back and engulfs your hard cock in her breasts again."

        "Leave it on.":
            mc.name "I think you look cute in it, leave it on."
            "She nods and keeps working her tits up and down."
    return

label orgasm_tit_fuck(the_girl, the_location, the_object):
    "[the_girl.title] speeds up her tit fuck, servicing your cock as fast as she can manage."
    "Suddenly she squeezes down on her tits and through them your cock, gasping softly."
    $ the_girl.call_dialogue("climax_responses_foreplay")
    "She holds her breath as her body is wracked with an orgasm, then lets it out as a loud sigh when she recovers."
    the_girl.char "I... Wow... Feeling your cock between my tits like this just made me..."
    "She moans and starts tit fucking you again, going at it with renewed vigor."
    return
