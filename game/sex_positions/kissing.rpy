init:
    python:
        kissing = Position(name = "Kissing", slut_requirement = 10, slut_cap = 40, requires_hard = False, requires_large_tits = False,
            position_tag = "kissing", requires_location = "Stand", requires_clothing = "None", skill_tag = "Foreplay",
            girl_arousal = 5, girl_energy = 10,
            guy_arousal = 5, guy_energy = 10,
            connections = [],
            intro = "intro_kissing",
            scenes = ["scene_kissing_1","scene_kissing_2"],
            outro = "outro_kissing",
            transition_default = "transition_default_kissing",
            strip_description = "strip_kissing", strip_ask_description = "strip_ask_kissing",
            orgasm_description = "orgasm_kissing",
            taboo_break_description = "taboo_break_kissing",
            verb = "kiss",
            opinion_tags = ["kissing"],
            associated_taboo = "kissing")
        list_of_positions.append(kissing)

init 1:
    python:
        kissing.link_positions(blowjob,"transition_kissing_blowjob")

label intro_kissing(the_girl, the_location, the_object):
    $ kissing.current_modifier = None
    $ kissing.redraw_scene(the_girl)
    "You put your arm around [the_girl.title]'s waist and pull her close. Her eyes close as you lean in and press your lips against hers."
    $ kissing.current_modifier = "kissing"
    $ kissing.redraw_scene(the_girl)
    "After a brief moment her arms wrap your torso in return. She pulls you close and presses against you."
    return

label taboo_break_kissing(the_girl, the_location, the_object):
    "You put your arm around [the_girl.title]'s waist and pull her close. She looks directly into your eyes."
    $ the_girl.call_dialogue(kissing.associated_taboo+"_taboo_break")
    if the_girl.effective_sluttiness(kissing.associated_taboo) > kissing.slut_cap and the_girl.sex_skills["Foreplay"] > 2:
        "You lean in and press your lips against hers. She returns the kiss immediately, opening her mouth and letting your tongue in to find hers."
    else:
        "You lean in and press your lips against hers. After a moment of hesitation you feel her press back, returning the kiss."
        "She breaks the kiss after a moment, takes a breath, then leans in herself and kisses you back."
    return

label scene_kissing_1(the_girl, the_location, the_object):
    #"You lock smoochers, gently kissing her."
    if the_girl.sex_skills["Foreplay"] > 2: #Experienced at kissing.
        #CHOICE CONCEPT: Hold her head,neck // Grab and squeeze her ass.
        "You and [the_girl.title] kiss. She uses a hand to caresses your back."
        menu:
            "Hold her tight.":
                "You place one of your hands on the small of [the_girl.title]'s back and the other on the back of her neck."
                if the_girl.get_opinion_score("kissing") > 0:
                    $ the_girl.change_arousal(the_girl.get_opinion_score("kissing"))
                    $ the_girl.discover_opinion("kissing")
                    "You pull her close. She arches her back and moans into your mouth."
                    "You make out for a few quiet moments. The whole time [the_girl.possessive_title] grinds her hips against you and moans softly."
                else:
                    "You make out for a few moments in silence, enjoying the feeling of each others bodies."

            "Squeeze her ass.":
                "You move your hands down [the_girl.title]'s waist and around to her butt. You give both cheeks a squeeze."
                if the_girl.core_sluttiness > 60:
                    $ kissing.current_modifier = None
                    $ kissing.redraw_scene(the_girl)
                    the_girl.char "Mmm, don't you want to spread those cheeks and fuck me? I'd let you, you know. Just say the word and you can fuck me."
                    $ kissing.current_modifier = "kissing"
                    $ kissing.redraw_scene(the_girl)
                    "She grinds her hips against you and kisses you agressively."
                else:
                    if the_girl.get_opinion_score("being submissive") > 0:
                        $ the_girl.discover_opinion("being submissive")
                        "[the_girl.possessive_title] presses herself tight against you when you squeeze her ass cheeks. She breaks the kiss briefly to talk."
                        $ kissing.current_modifier = None
                        $ kissing.redraw_scene(the_girl)
                        the_girl.char "Your hands are so strong... I just want to stay in your arms like this forever."
                        $ kissing.current_modifier = "kissing"
                        $ kissing.redraw_scene(the_girl)
                        "You give her ass a light spank. She lets out a happy sigh and keeps kissing you."

                    else:
                        $ kissing.current_modifier = None
                        $ kissing.redraw_scene(the_girl)
                        "[the_girl.possessive_title] breaks the kiss to speak."
                        the_girl.char "Mmm, go ahead and give me a spank. I've been a bad girl, haven't I?"
                        $ kissing.current_modifier = "kissing"
                        $ kissing.redraw_scene(the_girl)
                        "You slap her ass. She jumps slightly and giggles, then goes back to kissing you while you massage her butt."


    else: #Inexperienced.
        #INTRO CONCEPT: She's inexperienced and doesn't know what to do, where to put her hands, etc.
        $ kissing.current_modifier = "kissing"
        $ kissing.redraw_scene(the_girl)
        "You and [the_girl.title] kiss. She keeps her lips closed tight and stands completely still."
        $ kissing.current_modifier = None
        $ kissing.redraw_scene(the_girl)
        "After a moment you break the kiss and she looks away, embarrassed."
        the_girl.char "I'm sorry, I just don't know how to do this very well..."
        mc.name "Don't worry, I'll show you."
        #CHOICE CONCEPT: Teach her what to do and Go gentle // Passioante french (Good oral skill leads to great french kissing).
        menu:
            "Be gentle.":
                "You put one hand on the small of [the_girl.title]'s back and the other on her neck."
                mc.name "Just relax."
                $ kissing.current_modifier = "kissing"
                $ kissing.redraw_scene(the_girl)
                "She nods, and you press your lips to hers."
                "Little by little the tension in [the_girl.possessive_title]'s body starts to leave and she's able to enjoy herself."

            "Be passionate.":
                $ kissing.current_modifier = "kissing"
                $ kissing.redraw_scene(the_girl)
                "You put your arms around [the_girl.possessive_title] and pull her against you. Press your lips to hers and give her a long, passionate kiss."
                "She seems taken by suprise at first, but after a few moments returns the kiss. Bit by bit she begins to open her lips and lets your tongue inside her mouth."
                if the_girl.get_opinion_score("kissing") > 0:
                    $ the_girl.discover_opinion("kissing")
                    "[the_girl.title] presses her body against yours. She trembles and moans quietly as you make out."
                    "When you break the kiss she looks at you breathlessly for a moment."
                    $ kissing.current_modifier = None
                    $ kissing.redraw_scene(the_girl)
                    the_girl.char "Wow..."
                    "She pulls at your hips and grinds her body against yours."
                    the_girl.char "Do it again."
                else:
                    "After a few moments you break the kiss. [the_girl.title] takes a deep breath."
                    $ kissing.current_modifier = None
                    $ kissing.redraw_scene(the_girl)
                    the_girl.char "Wow, that was more intense than I was expecting it to be."
                    "She smiles and pulls at your hips."
                    the_girl.char "Let's do it again."

                $ kissing.current_modifier = "kissing"
                $ kissing.redraw_scene(the_girl)
                "You kiss her again and she seems more comfortable."
    return


label scene_kissing_2(the_girl, the_location, the_object):
    #"You boop snoots, tenderly staring into her eyes. She holds you close, kissing you on the neck."
    #"Your snoots boop furiously, the sound echoing around the room."
    #INTRO CONCEPT: Standard kissing, leading into kissing/fondling.
    #CHOICE CONCEPT: Kiss her neck // fondle her tits
    $ kissing.current_modifier = "kissing"
    $ kissing.redraw_scene(the_girl)
    "You and [the_girl.title] make out for a long moment before she breaks the kiss. She wraps her arms around your waist and looks deep into your eyes."
    menu:
        "Kiss her neck.":
            "You lean forward and kiss [the_girl.possessive_title]'s neck. She tilts her head to the side for you and lets out a long gasp."
            $ kissing.current_modifier = None
            $ kissing.redraw_scene(the_girl)
            the_girl.char "Oh my god..."
            "Her neck is soft and warm. You kiss it up and down while she moans happily into your ear."
            if the_girl.core_sluttiness > 65:
                the_girl.char "I hope you aren't just planning to tease me [the_girl.mc_title], I want you so badly."
            elif the_girl.core_sluttiness > 40:
                the_girl.char "Ah, when you do that it drives me crazy. Get me warmed up, then maybe we can do something else."
            else:
                the_girl.char "[the_girl.mc_title]... Hold me close and don't let go."

            $ kissing.current_modifier = "kissing"
            $ kissing.redraw_scene(the_girl)
            "You finish kissing her neck and slide back up to her lips. She pulls you tight against her and passionately returns the kiss."

        "Fondle her tits.":
            $ kissing.current_modifier = None
            $ kissing.redraw_scene(the_girl)
            if the_girl.has_large_tits():
                if the_girl.outfit.tits_available():
                    "You cup one of [the_girl.title]'s sizeable breasts and heft it, making it bounce and jiggle."
                    the_girl.char "Mmm, having fun? Go ahead, give it a squeeze."
                    "You grab [the_girl.possessive_title]'s other tit and squeeze them both. She bites her lip and sighs."
                    $ kissing.current_modifier = "kissing"
                    $ kissing.redraw_scene(the_girl)
                    "After letting you fondle her for a few more seconds [the_girl.title] pulls you back into a kiss."

                else:
                    $top_clothing = the_girl.outfit.get_upper_ordered()[-1]
                    "You cup one of [the_girl.title]'s sizeable breasts through her [top_clothing.name]. You bounce it up and down a few times."
                    the_girl.char "Mmm, that's nice. Maybe if you ask nicely I'll let you get a better feel of them."
                    "She pulls you back against her and leans in close. You can feel her warm breath against your lips."
                    the_girl.char "But don't get too distracted. Weren't you doing something already?"
                    $ kissing.current_modifier = "kissing"
                    $ kissing.redraw_scene(the_girl)
                    "She plants her lips on yours and you keep kissing."

            else:
                if the_girl.outfit.tits_available():
                    "You run one of your hands over [the_girl.title]'s small tits, taking an extra moment to rub her nipples with your thumb."
                    the_girl.char "Mmm... That feels nice."
                    $ kissing.current_modifier = "kissing"
                    $ kissing.redraw_scene(the_girl)
                    "She lets you fondle her for a few more seconds before pulling you back into a kiss."

                else:
                    $top_clothing = the_girl.outfit.get_upper_ordered()[-1]
                    "You run your hand over [the_girl.title]'s chest, feeling her small tits through her [top_clothing.name]."
                    the_girl.char "I hope you aren't getting distracted..."
                    $ kissing.current_modifier = "kissing"
                    $ kissing.redraw_scene(the_girl)
                    "She pulls you back against her and plants her lips on yours."

    return

label outro_kissing(the_girl, the_location, the_object):
    #"You part, snoots seperating slowly as you sare into her eyes. She whispers gently into your ear."
    #"Girl" "Oh god, my snoot. You booped me crazy."
    $ kissing.current_modifier = "kissing"
    $ kissing.redraw_scene(the_girl)
    "[the_girl.title]'s tongue feels like satin against your lips, it's touch sends shivers up and down your spine."
    if the_girl.arousal > 100:
        "Watching her cum has gotten you more excited than you thought you would be. You're grinding your hips against hers now, rubbing your erection against her through your pants."
    elif the_girl.arousal > 40:
        "Her soft moans and eager movement make you even more excited. You're grinding your own hips against hers now, rubbing your erection against her through your pants."
    else:
        "You're grinding your own hips against hers now, rubbing your erection against her through your pants."
    "You finally let out a low moan and hold [the_girl.possessive_title] close. A shiver runs up your spine as your climax, shooting your load out into your underwear."
    $ kissing.current_modifier = None
    $ kissing.redraw_scene(the_girl)
    "It takes a moment for you to recover from your orgasm. Once you're able to you step back and smooth out your shirt, the crotch of your pants uncomfortably wet now."
    return

label transition_kissing_blowjob(the_girl, the_location, the_object):
    #"You part smoochers, and she leans close to you."
    #"You" "I've got something else for you to boop."
    #"You wait, and soon she's on her knees, booping your second snoot."
    #"Transition from kissing to blowjob."
    $ kissing.current_modifier = None
    $ kissing.redraw_scene(the_girl)
    "You break the kiss between you and [the_girl.title] and look into her eyes, idly stroking her hair with a hand."
    the_girl.mc_title "[the_girl.title], how about you take care of this for me?"
    "You reach down with your other hand and unzip your pants. You pull your underwear down and let your hard cock spring free."
    if the_girl.effective_sluttiness() > 80:
        "[the_girl.title] stares down at your cock hungrily, licking her lips."
        the_girl.char "Mmm, let me at it."
        $ the_girl.draw_person(position="blowjob")
        "[the_girl.possessive_title] drops down to her knees quickly, shuffling right up next to you and resting your hard shaft on her cheek."
    else:
        $ the_person.draw_person(position="blowjob")
        "[the_girl.possessive_title] looks down at your erection then back up at you. She smiles and nods, dropping slowly to her knees while her hands run down your sides."
        the_girl.char "How's this?"
    "[the_girl.title] leans in close and kisses the tip of your dick gently, swirling her tongue around the tip."
    return

label transition_default_kissing(the_girl, the_location, the_object):
    $ kissing.current_modifier = "kissing"
    $ kissing.redraw_scene(the_girl)
    "You take [the_girl.title] in your arms and hold her close. She leans against you as you kiss her, breasts pressed up against your chest."
    "It's not long before the two of you are making out, arms clasped tightly around each other."
    return

label strip_kissing(the_girl, the_clothing, the_location, the_object):
    "[the_girl.title] breaks the kiss."
    $ the_girl.call_dialogue("sex_strip")
    $ the_girl.draw_animated_removal(the_clothing, position = kissing.position_tag)
    "[the_girl.possessive_title] takes off her [the_clothing.name] and drops it to the side, then pulls you close and resumes making out with you."
    $ kissing.current_modifier = "kissing"
    $ kissing.redraw_scene(the_girl)
    return

label strip_ask_kissing(the_girl, the_clothing, the_location, the_object):
    "[the_girl.title] breaks the kiss."
    $ kissing.current_modifier = None
    $ kissing.redraw_scene(the_girl)
    the_girl.char "[the_girl.mc_title], I'd like to take off my [the_clothing.name], would you mind?"
    menu:
        "Let her strip.":
            mc.name "Take it off for me."
            $ the_girl.draw_animated_removal(the_clothing, position = kissing.position_tag)
            "You watch while [the_girl.possessive_title] takes off her [the_clothing.name] and drops it to the side. She's done you pull her close and kiss her again."

        "Leave it on.":
            mc.name "No, I like how you look with it on."
            if the_girl.sluttiness < 80:
                the_girl.char "Do you think I look sexy in it?"
                "[the_girl.possessive_title] smiles and pulls you against her, kissing you passionately."
            else:
                the_girl.char "Don't you think I would look better wearing your cum? That would be so fitting for your dirty little slut, wouldn't it?"
                "[the_girl.possessive_title] smiles and pulls you against her, kissing you passionately."
    $ kissing.current_modifier = "kissing"
    $ kissing.redraw_scene(the_girl)
    return

label orgasm_kissing(the_girl, the_location, the_object):
    "[the_girl.title] suddenly pulls you tight against her. You feel her body shiver against yours."
    "It takes you a second before you realise she's cumming. You return the passion of her kiss and grind your body against hers."
    $ the_girl.call_dialogue("climax_responses_foreplay")
    "After a few seconds she twitches one last time, then relaxes as all the tension drains from her body."
    "You break the kiss and look into each others eyes."
    the_girl.char "That was... amazing [the_girl.mc_title]."
    "Before you can respond she kisses you again, seemingly eager to keep going."
    return
