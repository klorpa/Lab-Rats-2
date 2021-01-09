init:
    python:
        blowjob = Position(name = "Blowjob", slut_requirement = 40, slut_cap = 60, requires_hard = True, requires_large_tits = False,
            position_tag = "blowjob", requires_location = "Kneel", requires_clothing = "None", skill_tag = "Oral",
            girl_arousal = 3, girl_energy = 13,
            guy_arousal = 16, guy_energy = 5,
            connections = [],
            intro = "intro_blowjob",
            scenes = ["scene_blowjob_1","scene_blowjob_2"],
            outro = "outro_blowjob",
            transition_default = "transition_default_blowjob",
            strip_description = "strip_blowjob", strip_ask_description = "strip_ask_blowjob",
            orgasm_description = "orgasm_blowjob",
            taboo_break_description = "taboo_break_blowjob",
            verb = "throat",
            opinion_tags = ["giving blowjobs"], record_class = "Blowjobs",
            default_animation = idle_wiggle_animation, modifier_animations = {"blowjob":blowjob_bob},
            associated_taboo = "sucking_cock")

        list_of_positions.append(blowjob)

init 1:
    python:
        blowjob.link_positions(deepthroat,"transition_blowjob_deepthroat")

label intro_blowjob(the_girl, the_location, the_object):
    "You unzip your pants and pull your underwear down far enough to let your hard cock out."
    mc.name "How about your take care of this for me?"
    if the_girl.effective_sluttiness() > 35:
        "[the_girl.possessive_title] looks at your shaft for a moment, then drops to her knees in front of you. She runs her hands along your hips, then leans foward and slides her lips over the tip of your dick."
    else:
        "[the_girl.possessive_title] looks down at your shaft for a moment, thinks about it for a moment, then drops to her knees in front of you. She leans forward and kisses the tip of your dick gingerly."
    $ blowjob.current_modifier = "blowjob"
    $ blowjob.redraw_scene(the_girl)
    return

label taboo_break_blowjob(the_girl, the_location, the_object):
    $ the_girl.call_dialogue(blowjob.associated_taboo+"_taboo_break") #Personality dialogue includes all associated "convince me" dialogue
    if the_girl.effective_sluttiness(blowjob.associated_taboo) > blowjob.slut_cap:
        #She's eager to try this
        "[the_girl.possessive_title] kneels down in front of you, eyes locked on your hard cock."
        $ blowjob.current_modifier = "blowjob"
        $ blowjob.redraw_scene(the_girl)
        "She leans in, turning her head to the side to run her tongue down the bottom of your shaft."
        "She licks your balls briefly, then works back up to the tip and slides it past her lips."
        "You sigh happily as you feel [the_girl.title]'s warm mouth envelop your cock."
        "She wastes no time picking up speed, happily bobbing her head up and down over your sensitive tip."

    else:
        "[the_girl.possessive_title] hesitantly gets onto her knees, eyes locked on your hard cock."
        "She gently holds onto your shaft with one hand and brings the tip closer to her lips."
        "She looks up at you just before the moment of truth, locking eyes as she opens her lips and slides the tip of your cock past them."
        $ blowjob.current_modifier = "blowjob"
        $ blowjob.redraw_scene(the_girl)

        "You sigh happily as you feel [the_girl.title]'s warm mouth envelop your cock."
        "She moves slowly at first, gently working her head up and down over your sensitive tip."
    return

label scene_blowjob_1(the_girl, the_location, the_object):
    $ blowjob.current_modifier = "blowjob"
    $ blowjob.redraw_scene(the_girl)
    if the_girl.sex_skills["Oral"] < 2: #Inexperienced.
        "You rest your hand on [the_girl.title]'s head as she bobs her head back and forth. She struggles to take your very deep, and focuses on licking and sucking your tip instead."
        menu:
            "Encourage her to go deeper.":
                mc.name "Come on, you'll never get better if you don't try and take it deeper."
                "[the_girl.possessive_title] hesitates for a moment, then tries to slide you to the back of her throat. She manages to get half your shaft into her mouth before she pauses, then gags and pulls off."
                $ blowjob.current_modifier = None
                $ blowjob.redraw_scene(the_girl)
                if the_girl.get_opinion_score("giving blowjobs") < 0:
                    $ the_girl.discover_opinion("giving blowjobs")
                    the_girl.char "Ugh... I hate that feeling."
                    mc.name "Give it time, you'll get use to it."
                else:
                    the_girl.char "Ah... Ah..."
                    mc.name "Better. Now keep it up."

                $ blowjob.current_modifier = "blowjob"
                $ blowjob.redraw_scene(the_girl)
                "You put a little pressure on the back of her head. She takes the hint and slips you back into her soft mouth."

            "Tell her to use her hand too.":
                mc.name "There's plenty of shaft still left. Stroke me off a little."
                if the_girl.sex_skills["Foreplay"] < 2:
                    "[the_girl.possessive_title] wraps her right hand around the base of your cock. She tries jerk off the base of your cock while licking at the tip, but can't quite coordinate the movements."
                    "After trying for a few seconds she takes a break and sighs."
                    the_girl.char "Ugh, I'm just so bad at this..."
                    mc.name "Keep trying, you'll get better. Don't worry, I promise I'm having a good time."
                    "You press the tip of your cock against her lips and she lets you slide it back in. She resumes sucking and licking the tip, without trying to stroke you off at the same time."
                else:
                    "[the_girl.possessive_title] wraps her right hand around the base of your cock and starts to slide it back and forth in time with her blowjob."
                    if (the_girl.get_opinion_score("cum facials") > 0 or the_girl.get_opinion_score("being covered in cum") > 0 ) and the_girl.sluttiness > 40:
                        "After a moment she takes her lips off your dick and looks up at you."
                        the_girl.char "Mmm, look at this. Don't you just want to cum all over my face?"
                        "She strokes you off faster and holds your cock right against her face."
                        the_girl.char "I want you to cum on me. I want you to pump your load right onto my face!"
                        $ the_girl.discover_opinion("cum facials")
                        $ the_girl.discover_opinion("being covered in cum")
                        "[the_girl.title] trembles slightly and slides your cock back into her mouth, sucking at it with renewed vigor."
                    elif the_girl.get_opinion_score("drinking cum") > 0 and the_girl.sluttiness > 40:
                        "After a moment she takes her lips off your dick and looks up at you."
                        the_girl.char "Come on, I want you to unload right in my mouth [the_girl.mc_title]."
                        "She pops back onto your cock, sucking at the tip eagerly before letting it slip out again."
                        the_girl.char "I want you to fire it right down my throat. Ugh, I want it so badly!"
                        "[the_girl.title] slides you back into her mouth and sucks your dick with renewed vigor."
                    else:
                        "You relax for a little while while [the_girl.possessive_title] services your cock, stroking your shaft and sucking gently on your tip."
                        "You're pleasantly surprised when she reaches her other hand up and starts to gently play with your balls. You run your fingers through her hair and sigh contentedly."


    else: #competent at blowjobs.
        "[the_girl.title] keeps her mouth open wide and bobs her head back and forth to slide your cock in and out. The feeling of her soft, warm mouth sends shivers up your spine."
        menu:
            "Talk dirty to her.":
                mc.name "That feels great [the_girl.title]. You look good on your knees, sucking my cock."
                if the_girl.get_opinion_score("giving blowjobs") > 0:
                    "She slides your cock out of her mouth to speak."
                    the_girl.char "Mmm, and you feel so good in my mouth. You're so big I can barely manage."
                    $ the_girl.discover_opinion("giving blowjobs")
                    "She rubs her cheek against your wet shaft."
                    if the_girl.get_opinion_score("drinking cum") > 0:
                        the_girl.char "Now just relax and enjoy. I want you cum right into my mouth, okay?"
                        $ the_girl.discover_opinion("drinking cum")
                    else:
                        the_girl.char "Now just relax and enjoy, I'll take care of everything."
                    "She slips you back into her mouth and resumes blowing you."

                elif the_girl.get_opinion_score("giving blowjobs") < 0:
                    "She pulls off of your cock to speak."
                    the_girl.char "How about we try some other position? My knees are killing me, and I keep feeling like I'm going to gag on this."
                    $ the_girl.discover_opinion("giving blowjobs")
                    mc.name "Maybe in a little bit. Come on, back to work."
                    "[the_girl.possessive_title] sighs and slides your dick back into her mouth, settling back into the steady rhythm of her blowjob."

                else:
                    "[the_girl.possessive_title] stays focused on the task at hand. You run a hand through her hair, then settle the hand on the back of her head to encourage her to keep up the pace."

            "Stay quiet.":
                "You rest your hand on her head, guiding her as she sucks you off."
                if the_girl.get_opinion_score("masturbating") > 0:
                    if the_girl.outfit.vagina_available():
                        "[the_girl.title] puts a hand between her legs and starts to touch herself while she she blows you."
                        $ the_girl.change_arousal(the_girl.get_opinion_score("masturbating"))
                        $ the_girl.discover_opinion("masturbating")
                        if the_girl.arousal > 60:
                            "Her moans are muffled by your cock when she slides a finger into her pussy and starts to finger herself."

                        else:
                            "She rubs her clit with her middle finger, making little circles around the sensitive nub."


                    else:
                        if the_girl.arousal > 60:
                            "[the_girl.title] puts a hand between her legs and eagerly rubs at her crotch through her clothing."
                        else:
                            "[the_girl.title] puts a hand between her legs and rubs at her crotch absentmindedly."

                else:
                    "[the_girl.title] keeps up a steady pace, bobbing her head back and forth and running your cock in and out of her soft mouth."
                    if the_girl.get_opinion_score("giving blowjobs") < 0:
                        "After a minute she pulls off and wipes at her lips."
                        the_girl.char "Are you almost done? My jaw is getting sore."
                        $ the_girl.discover_opinion("giving blowjobs")
                        mc.name "Keep going, I'll finish soon."
                        "She sighs and slips you back into her mouth."

    return

label scene_blowjob_2(the_girl, the_location, the_object):
    $ blowjob.current_modifier = None
    $ blowjob.redraw_scene(the_girl)

    "[the_girl.title] pulls your cock out of her her mouth and leans in even closer. She runs her tongue along the bottom of your shaft, pausing at the top to kiss the tip a few times."
    the_girl.char "Does that feel good?"
    menu:
        "Encourage her.":
            mc.name "Yeah, it does. Keep licking it for me."
            "[the_girl.possessive_title] smiles and keeps working her tongue over your cock. She licks it bottom to top, then sucks on the tip, then licks it from the top back to the bottom."
            if the_girl.get_opinion_score("taking control") > 0:
                the_girl.char "Mmm, I love this so much. I love being in control of your pleasure. Being able to..."
                "She runs her tongue along the underside of your cock, licking the sensitive spot just below the tip. You moan in response."
                $ the_girl.discover_opinion("taking control")
                $ the_girl.change_arousal(the_girl.get_opinion_score("taking control"))
                the_girl.char "Make you moan, just like that."
            else:
                the_girl.char "Just relax and enjoy, I'll take care of you as best I can."
                if the_girl.sex_skills["Oral"] < 2:
                    "[the_girl.title] keeps on licking your cock. You enjoy the feeling for a while, but you're glad when she finally opens her mouth and starts to blow you again."
                else:
                    "[the_girl.title] keeps on licking your cock. Her tongue hits all the right places and sends shivers up your spine."
                    "You're almost disapointed when she opens her mouth wide and starts to blow you again."
            $ blowjob.current_modifier = "blowjob"
            $ blowjob.redraw_scene(the_girl)



        "Insult her.":
            mc.name "Of course it does, you filthy little cocksucker."
            if the_girl.get_opinion_score("being submissive") > 0:
                "You grab hold of your dick with one hand and bounce it against [the_girl.possessive_title]'s face. She gasps loudly when you do."
                $ the_girl.discover_opinion("being submissive")
                $ the_girl.change_arousal(the_girl.get_opinion_score("being submissive"))
                mc.name "Do you like having a wet cock slapped against your face? I bet you're a total slut for it, right?"
                "You do it again. Your cock makes a wet thwack against her face. This time she moans."
                the_girl.char "Yes..."
                "She responds softly, as if she's suddenly distracted."
                mc.name "I didn't hear you."
                "Thwack. You flop your cock over her face again. She moans again."
                the_girl.char "Yes... Yes I like having your cock all over my face!"
                "She opens her mouth wide and sticks her tongue out. You bounce your cock against her soft tongue, then against her cheeks and onto her forehead. She moans with each hit."
                $ the_girl.change_obedience(the_girl.get_opinion_score("being submissive"))
                mc.name "Good girl. Now be a good slut for me and keep sucking me off."
                "You present your cock to [the_girl.possessive_title]. She nods and slips her lips around it."

            elif the_girl.get_opinion_score("being submissive") < 0:
                $ the_girl.discover_opinion("being submissive")
                $ the_girl.change_arousal(the_girl.get_opinion_score("being submissive"))
                "[the_girl.title] leans away from you."
                the_girl.char "Ugh, could you not say stuff like that, please? It really kills the mood."
                "She sighs and slips your cock back into her mouth."

            else:
                "You grab hold of your dick with one hand and bounce it against [the_girl.title]'s face. She gasps in suprise."
                if the_girl.sex_skills["Foreplay"] > 3:
                    the_girl.char "Filthy cocksucker, huh? Is that what you want me to be?"
                    "She leans forward and rubs her cheek against your wet cock, nuzzling it like a cat."
                    the_girl.char "Okay then, I'll be your filthy little cocksucker [the_girl.mc_title]. I'll take this monster cock nice and deep..."
                    "She kisses the side of it, then sticks her tongue out and runs it along the entire length of your shaft."
                    the_girl.char "I'll gag on it until you're ready to cum, if that's what you want me to do."
                    the_girl.char "Because deep down I'm just a cock hungry slut, begging to be used."
                    "Hearing [the_girl.title] gets you even more aroused. Your dick flexes in response and bumps against her face."
                    the_girl.char "Mmm, I thought so. Everyone likes a bit of dirty talk..."
                    "She opens her mouth and slides you inside."
                else:
                    the_girl.char "Hey, I'm..."
                    "You interupt her and flop your cock onto her face again."
                    the_girl.char "Ugh, fine. Go to town."
                    "She closes her eyes and points her face up. You enjoy a few moments rubbing your cock all over [the_girl.possessive_title]'s face."
                    the_girl.char "Happy now?"
                    mc.name "Very."
                    "She opens her mouth back up and slides you inside."

    return

label outro_blowjob(the_girl, the_location, the_object):
    $ blowjob.current_modifier = "blowjob"
    $ blowjob.redraw_scene(the_girl)
    "Little by little the soft, warm mouth of [the_girl.title] brings you closer to orgasm. One last pass across her velvet tongue is enough to push you past the point of no return."
    menu:
        "Cum on her face.":
            mc.name "Fuck, here I come!"
            "You take a step back, pulling your cock out of [the_girl.possessive_title]'s mouth with a satisfyingly wet pop, and take aim at her face."
            $ blowjob.current_modifier = None
            $ blowjob.redraw_scene(the_girl)
            if the_girl.effective_sluttiness() > 80:
                "[the_girl.title] sticks out her tongue for you and holds still, eager to take your hot load."
                $ the_girl.cum_on_face()
                $ blowjob.redraw_scene(the_girl)
                "You let out a shuddering moan as you cum, pumping your sperm onto [the_girl.possessive_title]'s face and into her open mouth. She makes sure to wait until you're completely finished."
            elif the_girl.effective_sluttiness() > 60:
                "[the_girl.title] closes her eyes and waits patiently for you to cum."
                $ the_girl.cum_on_face()
                $ blowjob.redraw_scene(the_girl)
                "You let out a shuddering moan as you cum, pumping your sperm onto [the_girl.possessive_title]'s face. She waits until she's sure you're finished, then opens one eye and looks up at you."
            else:
                "[the_girl.title] closes her eyes and turns away, presenting her cheek to you as you finally climax."
                $ the_girl.cum_on_face()
                $ blowjob.redraw_scene(the_girl)
                "You let out a shuddering moan as you cum, pumping your sperm onto [the_girl.possessive_title]'s face. She flinches as the first splash of warm liquid lands on her cheek, but doesn't pull away entirely."
            "You take a deep breath to steady yourself once you've finised orgasming. [the_girl.title] looks up at you from her knees, face covered in your semen."
            $ the_girl.call_dialogue("cum_face")

        "Cum in her mouth.":
            $ blowjob.current_modifier = "blowjob"
            $ blowjob.redraw_scene(the_girl)
            mc.name "Fuck, I'm about to cum!"
            "You keep a hand on the back of [the_girl.title]'s head to make it clear you want her to keep sucking. She keeps blowing you until you tense up and start to pump your load out into her mouth."
            if the_girl.effective_sluttiness() > 70:
                "[the_girl.possessive_title] doesn't even flinch as you shoot your hot cum across the back of her throat. She keeps bobbing her head up and down until you've let out every last drop, then slides back carefully and looks up with a mouth full of sperm."
            else:
                "[the_girl.possessive_title] stops when you shoot your first blast of hot cum across the back of her throat. She pulls back, leaving just the tip of your cock in her mouth as you fill it up with semen. Once you've finished she slides off and looks up to show you a mouth full of sperm."

            $ the_girl.cum_in_mouth()
            $ blowjob.redraw_scene(the_girl)
            if the_girl.effective_sluttiness() > 80:
                "Once you've had a good long look at your work [the_girl.title] closes her mouth and swallows loudly. It takes a few big gulps to get every last drop of your cum down, but when she opens up again it's all gone."
            else:
                "Once you've had a good long look at your work [the_girl.title] leans over to the side and lets your cum dribble out slowly onto the ground. She straightens up and wipes her lips with the back of her hand."

            $ blowjob.current_modifier = None
            $ blowjob.redraw_scene(the_girl)
            $ the_girl.call_dialogue("cum_mouth")
    return

label transition_blowjob_deepthroat(the_girl, the_location, the_object):
    mc.name "Fuck that feels great [the_girl.title]. Think you can take it any deeper?"
    $ blowjob.current_modifier = None
    $ blowjob.redraw_scene(the_girl)
    "[the_girl.possessive_title] slides off your dick with a wet pop and takes a few breaths."
    the_girl.char "Well, I can try."
    $ blowjob.current_modifier = "blowjob"
    $ blowjob.redraw_scene(the_girl)
    "Once she's caught her breath she opens her mouth wide and slides you back down her throat. She doesn't stop until her nose taps your stomach and she has your entire cock in her mouth."
    return

label transition_default_blowjob(the_girl, the_location, the_object):
    $ blowjob.current_modifier = "blowjob"
    $ blowjob.redraw_scene(the_girl)
    "[the_girl.possessive_title] gets onto her knees in front of you and takes your hard cock in her hands. She strokes it tentativly a few times, then leans in and slides the tip into her mouth."
    mc.name "That's it, that's a good girl."
    return

label strip_blowjob(the_girl, the_clothing, the_location, the_object):
    $ blowjob.current_modifier = None
    $ blowjob.redraw_scene(the_girl)

    "[the_girl.title] pops off your cock and looks up at you."
    $ the_girl.call_dialogue("sex_strip")
    $ the_girl.draw_animated_removal(the_clothing)
    "[the_girl.possessive_title] stands and strips off her [the_clothing.name]. She drops it to the ground, then gets back on her knees and slides your cock inside her mouth."
    $ blowjob.current_modifier = "blowjob"
    $ blowjob.redraw_scene(the_girl)
    return

label strip_ask_blowjob(the_girl, the_clothing, the_location, the_object):
    $ blowjob.current_modifier = None
    $ blowjob.redraw_scene(the_girl)

    "[the_girl.title] pops off your cock and looks up at you from her knees."
    the_girl.char "[the_girl.mc_title], I'd like to take off my [the_clothing.name], would you mind?"
    menu:
        "Let her strip.":
            mc.name "Take it off for me."
            $ the_girl.draw_animated_removal(the_clothing, position = blowjob.position_tag)
            "[the_girl.possessive_title] stands up and strips out of her [the_clothing.name]. Then she gets back onto her knees and slides your cock all the way to the back of her mouth."
            $ blowjob.current_modifier = "blowjob"
            $ blowjob.redraw_scene(the_girl)


        "Leave it on.":
            mc.name "No, I like how you look with it on."
            if the_girl.sluttiness < 60:
                the_girl.char "Yeah? Do I look sexy in it?"
                $ blowjob.current_modifier = "blowjob"
                "She licks the length of your shaft, then slides your tip into her mouth and starts to blow you again."
            else:
                the_girl.char "Does it make me look like a good little slut? Or is your cock in my mouth enough for that?"
                $ blowjob.current_modifier = "blowjob"
                $ blowjob.redraw_scene(the_girl)
                "She slides you back into her mouth and presses you all the way to the back, rubbing your tip against the back of her throat for a second before she goes back to blowing you."
    return

label orgasm_blowjob(the_girl, the_location, the_object):
    $ blowjob.current_modifier = "blowjob"
    $ blowjob.redraw_scene(the_girl)
    "[the_girl.title] pauses suddenly. You hear her whimper softly - the noise party muffled by your cock."
    menu:
        "Be rough as she cums.":
            "[the_girl.possessive_title] starts to pull back off of your cock. You place a firm hand on the back of her head."
            mc.name "Did I tell you to stop sucking, you dirty little slut?"
            if the_girl.sex_skills["Oral"] > 2:
                "You push her back down, hard. [the_girl.title] keeps her mouth open wide and fits you all the way in, quivering as she climaxes."
            else:
                "You push her back down, hard. [the_girl.title] gags and coughs, but you make sure she gets your cock back into her mouth. She quivers as she climaxes"

            mc.name "A cock sleeve like you deserves to have her throat stuffed when she cums."
            if the_girl.get_opinion_score("being submissive") > 0:
                if the_girl.sluttiness > the_girl.core_sluttiness and the_girl.core_sluttiness < blowjob.slut_cap:
                    $ the_girl.change_slut_core(the_girl.get_opinion_score("being submissive")) #If she likes being submissive this makes her cum and become sluttier super hard.
                    $ the_girl.change_slut_temp(-the_girl.get_opinion_score("being submissive"))
                $ the_girl.change_obedience(2*the_girl.get_opinion_score("being submissive"))
                "[the_girl.possessive_title] closes her eyes tight. You can feel her throat spasm around your shaft in time with her orgasmic contractions."
                if the_girl.outfit.vagina_visible():
                    "You can see that [the_girl.title]'s pussy is dripping wet as she cums."
                else:
                    $ top_piece = the_girl.outfit.get_lower_ordered()[-1]
                    if top_piece.underwear:
                        "[the_girl.possessive_title]'s dripping wet pussy has managed to soak through her underwear, leaving a wet mark on her [top_piece.name]."
                    else:
                        "[the_girl.possessive_title] clenches her thighs together and rides out her orgasm."
                $ blowjob.current_modifier = None
                $ blowjob.redraw_scene(the_girl)
                "When she's stopped twitching and moaning you let [the_girl.title] slide back. She pants loudly, then licks along the length of your cock."
                the_girl.char "That was... incredible... I want more!"
            else:
                "[the_girl.possessive_title] closes her eyes as her orgasm peaks. She holds almost perfectly still, your dick still sitting in her mouth, until she's finished."
                $ blowjob.current_modifier = None
                $ blowjob.redraw_scene(the_girl)
                "She pulls off and takes a long, deep breath."
                $ the_girl.change_obedience(1)
                $ the_girl.change_happiness(-2)
                the_girl.char "Just... Let me handle things next time, okay?"

        "Be gentle as she cums.":
            $ blowjob.current_modifier = None
            $ blowjob.redraw_scene(the_girl)
            mc.name "That's it, cum for me [the_girl.title]."
            "[the_girl.possessive_title] pulls off your cock as she climaxes. She nuzzles up against your hot, wet shaft as her body shivers uncontrollably."
            "You stroke her hair and wait until she's over the worst of it."
            $ the_girl.change_happiness(2)
            the_girl.name "Wow... Thanks for waiting, that was really intens."
            "She licks your shaft and looks up at you."
            the_girl.name "Should I get going again?"
            "She doesn't wait for an answer and starts sucking your cock again."
    return
