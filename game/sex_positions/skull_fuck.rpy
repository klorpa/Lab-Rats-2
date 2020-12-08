init:
    python:
        skull_fuck = Position(name = "Skull Fuck", slut_requirement = 65, slut_cap = 100, requires_hard = True, requires_large_tits = False,
            position_tag = "blowjob", requires_location = "Kneel", requires_clothing = "None", skill_tag = "Oral",
            girl_arousal = 5, girl_energy = 10, #TODO: Balance energy costs
            guy_arousal = 25, guy_energy = 12,
            connections = [],
            intro = "intro_skull_fuck",
            scenes = ["scene_skull_fuck_1","scene_skull_fuck_2","scene_skull_fuck_3"],
            outro = "outro_skull_fuck",
            transition_default = "transition_default_skull_fuck",
            strip_description = "strip_skull_fuck", strip_ask_description = "strip_ask_skull_fuck",
            orgasm_description = "orgasm_skull_fuck",
            taboo_break_description = "taboo_break_skull_fuck",
            verb = "throat fuck",
            opinion_tags = ["giving blowjobs","being submissive"], record_class = "Blowjobs",
            default_animation = idle_wiggle_animation, modifier_animations = {"blowjob":blowjob_bob},
            associated_taboo = "sucking_cock")


init 1:
    python:
        skull_fuck.link_positions(deepthroat,"transition_skull_fuck_deepthroat")


label intro_skull_fuck(the_girl, the_location, the_object):
    # In theory this event is only reachable while deepthroating someone, but who knows...

    "You unzip your pants and pull your hard cock out."
    mc.name "[the_girl.title], I want you on your knees. I want to fuck that pretty little mouth."
    "[the_girl.possessive_title] nods and obediently kneels down in front of you."
    "You rub your dick along her cheek a few times, then slide it back and line it up with her lips."
    $ skull_fuck.current_modifier = "blowjob"
    $ skull_fuck.redraw_scene(the_girl)
    "You grab her head firmly and pull it towards you. Her eyes go wide as you ram yourself balls deep."
    return

label taboo_break_skull_fuck(the_girl, the_location, the_object): #In theory you can only reach this from a transition that would have already broken the taboo, so this shouldn't come up.
    $ the_girl.call_dialogue(skull_fuck.associated_taboo+"_taboo_break") #Convince dialogue is handled here.
    if the_girl.effective_sluttiness(skull_fuck.associated_taboo) > skull_fuck.slut_cap:
        #She's eager to try this
        "[the_girl.possessive_title] kneels down in front of you, eyes locked on your hard cock."
        $ skull_fuck.current_modifier = "blowjob"
        $ skull_fuck.redraw_scene(the_girl)
        "She leans in, turning her head to the side to run her tongue down the bottom of your shaft."
        "She licks your balls briefly, then works back up to the tip and slides it past her lips."
        "You sigh happily as you feel [the_girl.title]'s warm mouth envelop your cock."
        "She wastes no time picking up speed, happily bobbing her head up and down over your sensitive tip."

    else:
        "[the_girl.possessive_title] hesitantly gets onto her knees, eyes locked on your hard cock."
        "She gently holds onto your shaft with one hand and brings the tip closer to her lips."
        "She looks up at you just before the moment of truth, locking eyes as she opens her lips and slides the tip of your cock past them."
        $ skull_fuck.current_modifier = "blowjob"
        $ skull_fuck.redraw_scene(the_girl)
        "You sigh happily as you feel [the_girl.title]'s warm mouth envelop your cock."
        "She moves slowly at first, gently working her head up and down over your sensitive tip."
    mc.name "I think we can do better than that. Come here!"
    "You grab onto [the_girl.title]'s head with both hands and slam it forward onto your cock. She gags loudly, blowing spit around your base as you bottom out."
    "For a few seconds you just enjoy the feeling of her throat as it struggles to adjust to your size. Then you pull back and slam your cock home again."
    return

label scene_skull_fuck_1(the_girl, the_location, the_object):
    # Mantle her and pin her down.
    $ skull_fuck.current_modifier = "blowjob"
    $ skull_fuck.redraw_scene(the_girl)
    "[the_person.title]'s throat is warm and tight around your shaft as you slide yourself in and out."
    "She closes her eyes, struggling to keep herself under control."
    mc.name "Fuck your throat feels good!"
    "You take a half step forward, putting her between your legs with her head tilted upwards."
    "You pull her face against your crotch, flexing your cock."
    mc.name "Can you feel that? Do you like choking on a big, hard cock?"
    "Her only response is to gag softly, spit running down her chin."
    "You hold the position for a second before moving your hips and fucking her face."
    return

label scene_skull_fuck_2(the_girl, the_location, the_object):
    # Standard "You hold her head in place and fuck her throat raw"
    "You hold tight onto [the_girl.possessive_title]'s head, keeping it in place as you move your hips and fuck her face."
    "She gags and gurgles as you bottom your cock out with each stroke, but manages to keep her arms down at her sides."
    mc.name "Look up at me [the_girl.title]."
    "She struggles to turn her eyes up to meet yours. When she manages it you hold yourself deep and grind your hips against her face."
    mc.name "You're such a perfect cock socket, you know that? Fuck, this feels good."
    "You grab onto her hair at the roots and piston her head back and forth. Each thrust comes with a fresh gurgle from her ravaged throat."
    return

label scene_skull_fuck_3(the_girl, the_location, the_object):
    # Push extra deep and get her gagging on it.

    "You slow down and enjoy every inch of [the_girl.possessive_title]'s tight throat."
    "You keep one hand firm on the back of her head and move the other down to her throat, wrapping your fingers around it."
    "You can feel it bulge as you slide your full length inside of her."
    "She sputters as you throat her. Her spit bubbles around your shaft and drips down her chin, dropping onto her tits below."
    mc.name "That's it, gag on it you cock slut!"
    "You massage her throat with your hand and can feel the pressure on your own cock."
    "When you're satisfied she's had it down long enough you pull back, freeing her windpipe and letting her pull in a deep breath through her nose."
    "You don't wait long before sliding back into her, holding her head in place and fucking it like a toy."
    return

label outro_skull_fuck(the_girl, the_location, the_object):
    "[the_girl.title]'s warm, wet throat wrapped around your cock sends shivers up your spine and the sound of her gagging on your dick pushes you past your limits."
    "You have a brief moment to consider how you want to finish as you jackhammer yourself in and out of her mouth."
    menu:
        "Cum on her face.":
            mc.name "Fuck, here I cum!"
            "With both hands firmly on [the_girl.possessive_title]'s head you wait until the last possible moment to stop skull fucking her and pull out."
            $ skull_fuck.current_modifier = None
            $ skull_fuck.redraw_scene(the_girl)
            "You step back, dragging your hard cock from her lips just as it starts to spasm out your hot load."
            $ the_girl.cum_on_face()
            $ skull_fuck.redraw_scene(the_girl)
            "She opens her mouth to gasp for air and gets a mouthful of cum along with it."
            "You take one hand off [the_girl.title]'s head and grab your cock, guiding it as you pulse your semen all over her face."
            if the_girl.get_opinion_score("drinking cum") > 0:
                "When you're done she closes her mouth and happily gulps down all of the cum you had landed in there."
            else:
                "When you're done she lets your cum dripple out of her mouth, down her chin, and finally between her tits."
            $ the_girl.call_dialogue("cum_face")


        "Cum down her throat.":
            mc.name "Fuck, here I cum!"
            if the_girl.obedience >= 130 or the_girl.get_opinion_score("drinking cum") > 0: #She takes it like a champ
                "With both hands firmly on [the_girl.possessive_title]'s head you pull her as far down your cock as she'll go."
                "You grunt and release your load, firing pulse after pulse of hot cum down her throat and directly into her stomach."
                $ skull_fuck.current_modifier = None
                $ skull_fuck.redraw_scene(the_girl)
                "[the_girl.title] struggles to drink it all down, but doesn't try and pull off."
                $ the_girl.cum_in_mouth()
                $ skull_fuck.redraw_scene(the_girl)
                "When the last moments of your climax have passed you pull back, cock trailing spit and cum as you leave her mouth."
                if the_girl.get_opinion_score("drinking cum") > 0:
                    the_girl.char "I thought you were going to drown me with your cum for a moment... Mmmm."
                    $ the_girl.change_slut_temp(1)
                    $ the_girl.change_happiness(1)
                    "She shivers with pleasure at the thought."
                else:
                    "She runs the back of her hand along her lips, removing the cum trails and sits back to catch her breath."
                    $ the_girl.call_dialogue("cum_mouth")
            else:
                "With both hands firmly on [the_girl.possessive_title]'s head you pull her as far down your cock as she'll go."
                "[the_girl.title]'s eyes go wide as she  realises you don't intend to her off your cock as you cum."
                "She tries to pull her head back, but you hold it in place as you begin to unload your hot, sticky load directly into her throat."
                "For a brief second she manages to keep up with the torrent of cum, then it overwhelms her."
                "She spasms and gags. A mix of her spit and your semen bubble around the base of your cock, collecting in drops that roll down her chin and onto her tits."
                "She gags and coughs again, this time blowing little cum bubbles out of her nose as her body struggles to find somewhere to put more and more of your sperm."
                $ the_girl.cum_in_mouth()
                $ skull_fuck.redraw_scene(the_girl)
                "Finally you're spent and you finally let [the_person.title] pull off of your cock."
                the_girl.char "Guahh... Guahh... Ah.... Ah...."
                mc.name "Fuck that felt good."
                the_girl.char "There was so much... Ah... I thought I was going to drown in it..."
                "Still gasping for air, she wipes your sperm away from her nose and chin, then swallows loudly to get rid of the rest of it."
                $ the_girl.call_dialogue("cum_mouth")

    return

label transition_skull_fuck_deepthroat(the_girl, the_location, the_object):
    "You give [the_girl.possessive_title]'s mouth a few more fast, powerful thrusts. She gags, spit dripping down her chin, as you bottom out each time."
    $ skull_fuck.special_modifier = None
    $ skull_fuck.redraw_scene(the_girl)
    "With one final thrust you let go of her, letting her pull back and away from your hard shaft. She sputters and coughs, desperate for a full breath of air."
    "You give her a moment to catch her breath, then place a hand on her cheek and guide her back towards your throbbing shaft."
    $ skull_fuck.special_modifier = "blowjob"
    $ skull_fuck.redraw_scene(the_girl)
    "She takes a deep breath, then slides it back into her mouth. You keep your hand light on her head and let her set her own pace and depth as she works your cock."
    return

label transition_default_skull_fuck(the_girl, the_location, the_object):
    "You place your hands on either side of [the_girl.title]'s head and level your hard cock with her mouth."
    "You rest the tip on her lower lip and feel her warm breath on the sensitive skin each time she exhales."
    mc.name "Ready?"
    the_girl.char "Take me however you want."
    "She kisses the tip. You pull her head hard towards you and push your hips forward, slamming your cock to it's base in a single stroke."
    "Her eyes go wide and she gags loudly"
    the_girl.char "Guaaah!"
    "Her arms come up instinctively, but she struggles against the urge to push you away. She balls her fists and holds them close against her body."

    return

label strip_skull_fuck(the_girl, the_clothing, the_location, the_object):
    "[the_girl.title] taps on your thigh and tries to move her head back."
    menu:
        "Ignore her.": #You're really in control here.
            mc.name "I can't stop now, this feels too good!"

        "Let her up.":
            $ skull_fuck.current_modifier = None
            $ skull_fuck.redraw_scene(the_girl)
            "You give her throat one last thrust, then let her slide back until the tip of your cock clears her lips."
            the_girl.char "Ah... One... Sec..."
            $ the_girl.call_dialogue("sex_strip")
            $ the_girl.draw_animated_removal(the_clothing, position = deepthroat.position_tag)
            "She gasps for air while pulling off her [the_clothing.name]. She drops it to the ground, then nods up at you."
            the_girl.char "Much better. Well, what are you waiting for?"
            "She opens her mouth and you slam your dick back down her throat."
            $ skull_fuck.current_modifier = "blowjob"
            $ skull_fuck.redraw_scene(the_girl)
    return

label strip_ask_skull_fuck(the_girl, the_clothing, the_location, the_object):
    "[the_girl.title] taps on your thigh and tries to move her head back."
    menu:
        "Ignore her.": #You're really in control here.
            mc.name "I can't stop now, this feels too good!"

        "Let her up.":
            $ skull_fuck.current_modifier = None
            $ skull_fuck.redraw_scene(the_girl)
            "You give her throat one last thrust, then let her slide back until the tip of your cock just barely clears her lips."
            the_girl.char "I'm going to take off my [the_clothing.name], if that's okay with you."
            menu:
                "Let her strip.":
                    mc.name "Take it off."
                    $ the_girl.draw_animated_removal(the_clothing, position = blowjob.position_tag)
                    "[the_girl.possessive_title] strips out of her [the_clothing.name], your hard shaft hovering inches from her face."
                    "When she drops it to the side you press yourself forward, parting her lips and sliding your cock back down her throat."

                "Leave it on.":
                    mc.name "No, I like how you look with it on."
                    the_girl.char "Well then, what are you waiting for?"
                    "She opens her mouth wide and you slam your dick back down her throat."
            $ skull_fuck.current_modifier = "blowjob"
            $ skull_fuck.redraw_scene(the_girl)
    return

label orgasm_skull_fuck(the_girl, the_location, the_object):
    "You're happily fucking [the_girl.possessive_title]'s warm, wet throat when you notice her closer her eyes."
    "Her thighs quiver and her hands drop instinctively to her crotch. She begins to rub her pussy furiously, driving herself to orgasm."
    mc.name "Cum for me you dirty slut!"
    "Watching [the_girl.title]'s body writhe as she climaxes from your cock encourages you to go faster."
    "You clamp down on her head and slam yourself in and out of her throat."
    "[the_girl.possessive_title] is so lost in her orgasm that her body seems to have forgotten to gag at all, letting you get yourself balls deep with each trust."
    "Soon the moment has passed and she begins to recover her wits. She opens her eyes and looks up at you, still half drunk with pleasure."
    return
