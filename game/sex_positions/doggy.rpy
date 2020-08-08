init:
    python:
        doggy = Position(name = "Doggy", slut_requirement = 60, slut_cap = 80, requires_hard = True, requires_large_tits = False,
            position_tag = "doggy", requires_location = "Lay", requires_clothing = "Vagina", skill_tag = "Vaginal",
            girl_arousal = 16, girl_energy = 14,
            guy_arousal = 22, guy_energy = 20,
            connections = [],
            intro = "intro_doggy",
            scenes = ["scene_doggy_1","scene_doggy_2"],
            outro = "outro_doggy",
            transition_default = "transition_default_doggy",
            strip_description = "strip_doggy", strip_ask_description = "strip_ask_doggy",
            orgasm_description = "orgasm_doggy",
            taboo_break_description = "taboo_break_doggy",
            opinion_tags = ["doggy style sex","vaginal sex"], record_class = "Vaginal Sex",
            default_animation = blowjob_bob,
            associated_taboo = "vaginal_sex")

        list_of_positions.append(doggy)

init 1:
   python:
       doggy.link_positions(doggy_anal,"transition_doggy_doggy_anal")
       #Here is where you would put connections if they existed.

label intro_doggy(the_girl, the_location, the_object):
    mc.name "[the_girl.title], I want you to get on your hands and knees for me."
    if the_girl.effective_sluttiness() > 100:
        the_girl.char "I want you inside of me so badly..."
    elif the_girl.effective_sluttiness() > 80:
        the_girl.char "Mmm, you know just what I like [the_girl.mc_title]."
    else:
        the_girl.char "Like this?"
    "[the_girl.title] gets onto all fours in front of you on the [the_object.name]. She wiggles her ass impatiently at you as you get your hard cock lined up."
    if the_girl.arousal > 60:
        "You rub the tip of your penis against [the_girl.title]'s cunt, feeling how nice and wet she is already. She moans softly when you slide the head of your dick over her clit."
    else:
        "You rub the tip of your penis against [the_girl.title]'s cunt, getting ready to slide yourself inside."
    "When you're ready you push forward, slipping your shaft deep inside of [the_girl.possessive_title]. She gasps and quivers ever so slightly as you start to pump in and out."
    return

label taboo_break_doggy(the_girl, the_location, the_object):
    "You grab [the_girl.possessive_title]'s ass and give it a squeeze, then a hard slap."
    if the_girl.effective_sluttiness(doggy.associated_taboo) > doggy.slut_cap or the_girl.get_opinion_score("showing her ass") > 0:
        mc.name "Get on your knees, I want to get a look at this ass."
        $ the_girl.draw_person(position = "back_peek", the_animation = ass_bob)
        "She turns around and jiggles her butt playfully for you."
        the_girl.char "This big fat ass? You finally want to take a closer look?"
        mc.name "I said on your knees, come on."
        $ the_girl.draw_person(position = "doggy", the_animation = ass_bob, animation_effect_strength = 0.7)
        "She gets onto the [the_object.name] and points her butt in your direction. She lowers her shoulders and works her hips for you."

    else:
        mc.name "Get on your knees."
        $ the_girl.draw_person(position = "kneeling1")
        "She gets onto her knees in front of you."
        mc.name "Good girl, now spin around and show me that ass."
        "She nods and turns around."
        $ the_girl.draw_person(position = "doggy")
        mc.name "Nice. Now shake it for me."
        the_girl.char "Like... this?"
        $ the_girl.draw_person(position = "doggy", the_animation = ass_bob, animation_effect_strength = 0.4)
        "[the_girl.title] works her hips and jiggles her ass for you."
        mc.name "Getting there, a little faster now."
        $ the_girl.draw_person(position = "doggy", the_animation = ass_bob, animation_effect_strength = 0.7)
        "She speeds up."

    the_girl.char "Is that what you wanted?"
    "You slap your cock down on her ass and drag it down between her legs, ending with your tip resting against her pussy."
    mc.name "No, this is what I really want."
    $ the_girl.call_dialogue(doggy.associated_taboo+"_taboo_break")
    "You hold onto [the_girl.title]'s hips with one hand and your cock with the other, guiding it as you push forward."
    "After a moment of resistance your cock spreads her pussy open and you slide smoothly inside of her."
    the_girl.char "Oh god.... Ah...."
    "You give her short thrusts, each time going a little bit deeper. Soon you're working your full length in and out of her wet hole."
    return

label scene_doggy_1(the_girl, the_location, the_object):
    # CHOICE CONCEPT: Slap her ass // Talk dirty to her
    "You grab onto [the_girl.title] by her hips and settle into a steady rhythm, pumping your cock in and out of her tight pussy."
    $ the_girl.call_dialogue("sex_responses_vaginal")
    menu:
        "Talk dirty to her.":
            mc.name "How does that feel? Do you like getting railed from behind?"
            if the_girl.get_opinion_score("being submissive") > 0:
                $ the_girl.discover_opinion("being submissive")
                the_girl.char "Ah... I love it..."
                mc.name "What was that? I couldn't quite hear you."
                "You tighten your grip on her hips and fuck her faster."
                $ the_girl.change_arousal(the_girl.get_opinion_score("being submissive"))
                the_girl.char "I love it! Oh my god, I love it [the_girl.mc_title]!"
                mc.name "What do you love?"
                the_girl.char "Having sex with you! Being fucked by you! Being your..."
                "She hesitates. You pull her hips back hard against you and make her yelp."
                mc.name "Say it. Tell me what you like being."
                $ the_girl.change_obedience(the_girl.get_opinion_score("being submissive"))
                the_girl.char "Being your... Being your... Being your fuck toy! Being your dirty little fuck toy slut!"
                "She yells it out and shivers with pleasure. You can see her knees quivering while you fuck her from behind."
                "You slow down and resume your slower, more sustainable rhythm."
                mc.name "That's good to hear."

            elif the_girl.get_opinion_score("taking control") > 0 and the_girl.sex_skills["Vaginal"] > 2:
                the_girl.char "Oh of course I do [the_girl.mc_title]. What about you? Do you like fucking my tight pussy?"
                "She lowers her shoulders and pushes her butt towards you while you take her doggy style."
                the_girl.char "Do you like how wet it is? Does it make you want to cum?"
                mc.name "You feel amazing."
                $ the_girl.discover_opinion("taking control")
                $ the_girl.change_arousal(the_girl.get_opinion_score("taking control"))
                if the_girl.get_opinion_score("creampies") > 0:
                    $ the_girl.discover_opinion("creampies")
                    the_girl.char "I want you to cum inside me. I want you to fill me up with every last drop of hot sperm those balls are holding!"
                else:
                    the_girl.char "Good, I want to make you cum. I want to be the one to make you fire off that big cock of yours!"
                "She moans loudly when you start to fuck her a little faster."

            else:
                the_girl.char "Mmhm!"
                "She bites down on her lower lip and nods happily."
                "You tighten your grip on her hips and fuck her faster."
                if the_girl.arousal < 50:
                    mc.name "You're nice and tight, I love fucking your hot little pussy!"
                else:
                    mc.name "You're nice and wet, I love fucking your hot dripping pussy!"
                "You fuck her a little faster for a while then settle back down to a slower, more sustainable rhythm."

        "Slap her ass.":
            "You take a hand off of [the_girl.title]'s hips and squeeze her ass cheeks with it. When she moans happily in response you give her a hard slap."
            if the_girl.get_opinion_score("being submissive") > 0:
                $ the_girl.discover_opinion("being submissive")
                the_girl.char "Oh! Have I been bad [the_girl.mc_title]?"
                "She lowers her shoulders and raises her butt a little."
                the_girl.char "I think you need to spank me some more..."
                $ the_girl.change_arousal(the_girl.get_opinion_score("being submissive"))
                "You spank her hard again. She moans instead of yelping this time."
            else:
                the_girl.char "Ah!"
                "You enjoy the way her tight ass jiggles and spank it again."
            "You leave a hand planted on [the_girl.possessive_title]'s butt while you fuck her, kneeding it and giving it the occasional slap."



    # if the_girl.has_large_tits() and the_girl.outfit.tits_visible():
    #     "You give her ass a good spank and keep fucking her. Her big tits pendulum back and forth under her body, moving in time with your thrusts."
    # else:
    #     "You give her ass a good spank and keep fucking her, enjoying the way her slit gets wetter and wetter as you go."
    return

label scene_doggy_2(the_girl, the_location, the_object):
    # CHOICE CONCEPT: Fuck her hard // Fuck her fast

    if the_girl.sex_skills["Vaginal"] > 2:
        #Experienced. She can handle it.
        if the_girl.has_large_tits() and the_girl.outfit.tits_visible():
            "[the_girl.title]'s nice big tits pendulum back and forth under her body, moving in time with your thrusts."
        else:
            "[the_girl.title] starts to work her hips in time with yours, panting softly from the effort."
        the_girl.char "Come on [the_girl.mc_title], really give it to me. I can handle it!"
        menu:
            "Fuck her hard.":
                "You take a hand off of her hips and lean forward to put it on the back of her neck. With a shove you push her shoulders down against the [the_object.name]."
                if the_girl.get_opinion_score("being submissive") > 0:
                    the_girl.char "Ah! Yes, use me!"
                    $ the_girl.discover_opinion("being submissive")
                    $ the_girl.change_arousal(the_girl.get_opinion_score("being submissive"))
                elif the_girl.get_opinion_score("being submissive") < 0:
                    the_girl.char "Hey! Easy there!"
                    $ the_girl.discover_opinion("being submissive")
                    $ the_girl.change_arousal(the_girl.get_opinion_score("being submissive"))
                else:
                    the_girl.char "Oh!"
                "You lean over [the_girl.possessive_title] and fuck her hard, slamming your cock deeep inside her."
                if the_girl.arousal > 80:
                    "[the_girl.title] tries to speak, but her words become nothing more than moans and panting while you fuck her stupid."
                else:
                    "[the_girl.title] arches her back up against you while you fuck her and pants with each thrust."
                "You slow down and back off before you tire yourself out. [the_girl.title] gets back onto her hands and knees."

            "Fuck her fast.":
                "You pull [the_girl.title]'s hips towards you and pump into her as fast as you can manage."
                the_girl.char "That's it, give it to me [the_girl.mc_title]!"
                if the_girl.has_large_tits() and the_girl.outfit.tits_visible():
                    "You reach around and grag a handful of [the_girl.possessive_title]'s big tits."
                "You keep up the pace as long as you can, but eventually you need to slow down. You settle back into a rhythm you can sustain."

    else:
        #Inexperienced. She needs time to get use to it.
        the_girl.char "Ah... go easy on me [the_girl.mc_title], I'm still figuring out how to do this..."
        menu:
            "Fondle her tits.":
                "You ease yourself deep inside of [the_girl.title] and give her a chance to get use to your size."
                the_girl.char "Oh god..."
                if the_girl.has_large_tits() :
                    if the_girl.outfit.tits_available():
                        "You occupy yourself by leaning over her and fondling her nice big tits. After a few moments she starts to grind her hips back against you."

                    else:
                        $top_clothing = the_girl.outfit.get_upper_ordered()[-1]
                        "You occupy yourself by leaning over her and fondling her tits through her [top_clothing.name]. They bounce and jiggle under her clothing."
                        "After a few moments she starts to grind her hips back against you."

                else:
                    if the_girl.outfit.tits_available():
                        "You occupy yourself by leaning over her and fondling her cute little tits. After a moment she starts to grind her hips back against you."
                    else:
                        $top_clothing = the_girl.outfit.get_upper_ordered()[-1]
                        "You occupy yourself by leaning over and trying to fondle her cute little tits."
                        "Her [top_clothing.name] gets in the way, but after a few moments she starts to grind her hips back against you."

            the_girl.char "I... I want you to keep going."
            "Fuck her hard anyways.":
                mc.name "Don't worry, just relax and you'll manage."
                "You pull hard on her hips and fuck her hard. She yelps in a combination of suprise and pain."
                if the_girl.get_opinion_score("being submissive") > 0:
                    $ the_girl.discover_opinion("being submissive")
                    $ the_girl.change_obedience(the_girl.get_opinion_score("being submissive"))
                    $ the_girl.change_arousal(the_girl.get_opinion_score("being submissive"))
                    the_girl.char "Ah! Oh god [the_girl.mc_title], you're going to rip me in half!"
                    "Despite her reservations [the_girl.title] moans in pleasure as you pound her cunt."
                    mc.name "Do you you like it."
                    the_girl.char "It's so big, I... I can't take it! I... I... I love it! Ah!"
                    "Her breath comes in short gasps between thrusts. Your own stamina forces you to slow down, so you settle into a more maintainable rhythm while [the_girl.title] recovers."
                else:
                    the_girl.char "Ow! Fuck me, I said go slowly!"
                    mc.name "You can manage."
                    $ the_girl.change_arousal(-1+the_girl.get_opinion_score("being submissive"))
                    $ the_girl.change_obedience(-1+the_girl.get_opinion_score("being submissive"))
                    "[the_girl.title] shuffles forward and your dick slides out of her pussy."
                    the_girl.char "That's not how this works. Go slowly or I won't do this at all, okay?"
                    mc.name "Fine, okay. I'm sorry."
                    "She backs up again and lets you slide your cock back inside her. This time you move more slowly, and soon she's gotten back in the mood."

    # "[the_girl.title] lowers her shoulders against [the_object.name] and moans as you fuck her from behind."
    # the_girl.char "Ah... it feels so big!"
    # "You reach forward and place a hand around [the_girl.title]'s neck, using it as leverage to thrust even faster. She arches her back and lets out a series of satisfied yelps."
    # $the_girl.call_dialogue("sex_responses_vaginal")
    # if the_girl.arousal > 80:
    #     "[the_girl.title]'s pussy is dripping wet, warm and tight around your cock. She twitches and gasps occasionally as you slide in, practically begging you to fuck her more."
    # else:
    #     "[the_girl.title]'s pussy feels warm and tight around your cock as you fuck her."
    return

label outro_doggy(the_girl, the_location, the_object):
    "[the_girl.title]'s tight cunt draws you closer to your orgasm with each thrust. You finally pass the point of no return and speed up, fucking her as hard as you can manage."
    $ the_girl.call_dialogue("sex_responses_vaginal")
    mc.name "Ah, I'm going to cum!"
    $ the_girl.call_dialogue("cum_pullout")
    menu:
        "Cum inside of her.":
            if mc.condom:
                "You pull back on [the_girl.possessive_title]'s hips and drive your cock deep inside of her as you cum. She gasps as you dump your load into her, barely contained by your condom."
                $ the_girl.call_dialogue("cum_condom")
                "You wait until your orgasm has passed completely, then pull out and sit back. The condom is ballooned and sagging with the weight of your seed."
                if the_girl.get_opinion_score("drinking cum") > 0 and the_girl.sluttiness > 50:
                    $ the_girl.discover_opinion("drinking cum")
                    "[the_girl.possessive_title] turns around and reaches for your cock. With delicate fingers she slides the condom off of you."
                    the_girl.char "It would be a shame to waste all of this, right?"
                    "She winks and brings the condom to her mouth. She tips the bottom up and drains it into her mouth."
                    $ the_girl.change_slut_temp(the_girl.get_opinion_score("drinking cum"))
                else:
                    "[the_girl.possessive_title] turns around and reaches for your cock. She removes the condom and ties the end in a knot."
                    the_girl.char "Look at all that cum. Well done."
                "You sigh contentedly and enjoy the post-orgasm feeling of relaxation."
            else:
                "You pull back on [the_girl.possessive_title]'s hips and drive your cock deep inside of her as you cum. She gasps softly in time with each new shot of hot semen inside of her."
                $ the_girl.cum_in_vagina()
                $ doggy.redraw_scene(the_girl)
                $ the_girl.call_dialogue("cum_vagina")
                "You wait until your orgasm has passed completely, then pull out and sit back. Your cum starts to drip out of [the_girl.title]'s slit almost immediately."

        "Cum on her ass.":
            if mc.condom:
                "You pull out of [the_girl.title] at the last moment. You whip your condom off and stroke your cock as you blow your load over her ass."
                "She holds still for you as you cover her with your warm sperm."
            else:
                "You pull out of [the_girl.title] at the last moment, stroking your shaft as you blow your load over her ass. She holds still for you as you cover her with your sperm."
            $ the_girl.cum_on_ass()
            $ doggy.redraw_scene(the_girl)
            if the_girl.effective_sluttiness() > 120:
                the_girl.char "What a waste, you should have put that inside of me."
                "She reaches back and runs a finger through the puddles of cum you've put on her, then licks her finger clean."
            else:
                the_girl.char "Oh wow, there's so much of it..."
            "You sit back and sigh contentedly, enjoying the sight of [the_girl.title] covered in your semen."
    return

label transition_doggy_doggy_anal(the_girl, the_location, the_object):
    #transition from normal doggy style to anal. Include section to pull off condom.
    if mc.condom:
        "You pull out of [the_girl.title]'s pussy, pausing for a moment to pull off your condom and drop it to the ground."
        "You line your cock up with her asshole, the tip just barely pressing against it."
    else:
        "You pull out of [the_girl.title]'s pussy and line your cock up with her asshole, the tip just barely pressing against it."

    if the_girl.sex_skills["Anal"] > 2 or the_girl.get_opinion_score("anal sex") > 0:
        the_girl.char "Oh god, yes. Fuck my ass [the_girl.mc_title]!"
    else:
        the_girl.char "Uh... Oh fuck, you'd tear me apart [the_girl.mc_title]..."
    menu:
        "Ram it home!":
            "You get a firm grip on her hips, make sure you're lined up, and push yourself in with all your might."
            if the_girl.get_opinion_score("being submissive") > 0 or the_girl.get_opinion_score("anal sex"):
                the_girl.char "Ah! Yes! Tear that ass up!"
                $ the_girl.change_arousal(5*( the_girl.get_opinion_score("being submissive") + the_girl.get_opinion_score("anal sex") ))
                "Using her pussy juice as lube you lay into her tight ass, waisting no time in fucking her hard."

            else:
                the_girl.char "Oh fuck! FUCK!"
                "She yells out in suprise and pain. You bottom out and hold still, giving her a second to get use to your size."
                the_girl.char "Fuck... I hate that part..."
                mc.name "It's just like ripping off a bandaid. You'll get use to it."
                "You wait a moment, then start to move again. Using her pussy juices as lube you've soon got a good rhythm going."

        "Take it slow.":
            "You keep a firm grip on her hips as you push forward, sliding into one painful inch at a time."
            "Using her pussy juice as lube, you manage to slip your full cock into her ass. You pause there, giving her a moment to adjust."
            the_girl.char "Mmmhph... Fuck..."
            "When she's finally ready you start to move, fucking her cute little ass."
    return

label transition_default_doggy(the_girl, the_location, the_object):
    "[the_girl.title] gets on her hands and knees as you kneel behind her. You bounce your hard shaft on her ass a couple of times before lining yourself up with her cunt."
    "Once you're both ready you push yourself forward, slipping your hard shaft deep inside of her. She lets out a gasp under her breath."
    return

label strip_doggy(the_girl, the_clothing, the_location, the_object):
    "[the_girl.title] leans forward a little further and pops off your cock."
    $ the_girl.call_dialogue("sex_strip")
    $ the_girl.draw_animated_removal(the_clothing, position = doggy.position_tag)
    "[the_girl.possessive_title] struggles out of her [the_clothing.name] and throws it to the side. Then she gets herself lined up in front of you again."
    "She sighs happily when you slip back inside of her."
    return

label strip_ask_doggy(the_girl, the_clothing, the_location, the_object):
    the_girl.char "[the_girl.mc_title], I'd like to take off my [the_clothing.name], would you mind?"
    "[the_girl.title] pants as you fuck her from behind."
    menu:
        "Let her strip.":
            mc.name "Take it off for me."
            $ the_girl.draw_animated_removal(the_clothing, position = doggy.position_tag)
            "[the_girl.title] struggles out of her [the_clothing.name] and throws it to the side. Then she gets herself lined up in front of you again."
            "She sighs happily when you slip back inside of her."

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

label orgasm_doggy(the_girl, the_location, the_object):
    "[the_girl.title]'s breathing gets heavier and faster, until finally she takes a sharp breath and tenses up."
    $ the_girl.call_dialogue("climax_responses_vaginal")
    "You keep up your pace while [the_girl.possessive_title] cums. You think you can feel her pussy twitch around your cock."
    "After a couple of seconds [the_girl.title] sighs and the tension drains from her body."
    the_girl.char "Keep... keep going and see if you can make me to cum again!"
    return
