init:
    python:
        doggy_anal = Position(name = "Anal Doggy", slut_requirement = 70, slut_cap = 90, requires_hard = True, requires_large_tits = False,
            position_tag = "doggy", requires_location = "Lay", requires_clothing = "Vagina", skill_tag = "Anal",
            girl_arousal = 11, girl_energy = 11,
            guy_arousal = 14, guy_energy = 11,
            connections = [],
            intro = "intro_doggy_anal",
            scenes = ["scene_doggy_anal_1","scene_doggy_anal_2"],
            outro = "outro_doggy_anal",
            transition_default = "transition_default_doggy_anal",
            strip_description = "strip_doggy_anal", strip_ask_description = "strip_ask_doggy_anal",
            orgasm_description = "orgasm_doggy_anal",
            taboo_break_description = "taboo_break_doggy_anal",
            opinion_tags = ["doggy style sex","anal sex"], record_class = "Anal Sex",
            default_animation = blowjob_bob,
            associated_taboo = "anal_sex")

        list_of_positions.append(doggy_anal)

init 1:
   python:
       doggy_anal.link_positions(doggy,"transition_doggy_anal_doggy")
       #Here is where you would put connections if they existed.



label intro_doggy_anal(the_girl, the_location, the_object):
    mc.name "Get down on all fours, I want to fuck your tight ass."
    if the_girl.sex_skills["Anal"] > 2 or the_girl.get_opinion_score("anal sex") > 0:
        if the_girl.effective_sluttiness() > 100:
            the_girl.char "Get inside of me and fuck my ass raw!"
        else:
            the_girl.char "Okay, but take it slowly. I need some time to adjust..."
    else: #She's inexperienced and doesn't quite know what to do.
        if the_girl.effective_sluttiness() > 100:
            the_girl.char "Oh fuck, I want you inside me but I need you to slowly."
        else:
            "[the_girl.possessive_title] looks worried for a moment."
            the_girl.char "I'll let you try, but I don't know if you'll be able to fit. I haven't done this much..."

    "[the_girl.title] gets onto her hands and knees on the [the_object.name]. You spit into your hand and use it to lube up your cock, then line it up with her pretty little asshole."
    mc.name "Ready?"
    if the_girl.sex_skills["Anal"] > 2 or the_girl.get_opinion_score("anal sex") > 0:
        the_girl.char "Yes!"
    else:
        the_girl.char "No, but I don't know if I ever will be. Let's try it."
    "You hold onto her hips and push yourself in. She gasps as the tip of your cock slips into her ass."
    "[the_girl.title] grunts and gasps as you slowy fit your whole dick inside of her. When you bottom out you hold still, giving her time to adjust to your size."
    "After a long moment it seems like she's ready and you start to move, slowly at first then picking up speed."
    return

label taboo_break_doggy_anal(the_girl, the_location, the_object):
    "You grab [the_girl.possessive_title]'s ass and give it a squeeze, then a hard slap."
    if the_girl.effective_sluttiness(doggy_anal.associated_taboo) > doggy_anal.slut_cap or the_girl.get_opinion_score("showing her ass") > 0:
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
    "You slap your cock down on her ass and grab her tight cheeks, spreading them apart to get a look at her asshole."
    mc.name "Almost. I think it's time we stretched you open."
    $ the_girl.call_dialogue(doggy_anal.associated_taboo+"_taboo_break")
    "You hold onto [the_girl.title]'s hips with one hand and your cock with the other, guiding it as you press it against her tight hole."
    if the_girl.sex_skills["Anal"] > 2:
        "She gasps as your tip starts to spread her open. She lowers her shoulders and pushes her hips against you, helping the process."
        the_girl.char "Oh god... Mfphhhh!"

    else:
        "She gasps as your tip tries to spread open her impossibly tight asshole. She tries to pull away, but you pull on her waist and bring her closer."
        mc.name "Come on, you'll get there."
        "You spit onto your cock and try again. This time making better progress, sliding the tip of your dick into [the_girl.title]'s ass."
        the_girl.char "Oh god... Fuck!"
    "Inch by inch you slide your entire length into [the_girl.possessive_title]. She grunts and gasps the whole way down."
    "When stop when you've bottomed out, to give your cock time to properly stretch her out."
    the_girl.char "I think... I'm ready for you to move some more..."
    "You pull back a little bit and give her a few testing strokes. When she can handle those you speed up, until you're thrusting your entire length."
    return

label scene_doggy_anal_1(the_girl, the_location, the_object):

    "You hold onto [the_girl.title]'s hips and settle into a steady rhythm, sliding your cock in and out out of her tight ass."
    $ the_girl.call_dialogue("sex_responses_anal")

    if the_girl.has_large_tits() and the_girl.outfit.tits_visible():
        "With each thrust [the_girl.title]'s large tits pendulum underneath her. You reach a hand around and grab one of them, squeezing it hard."
    else:
        "With each thrust [the_girl.title]'s ass shakes and jiggles. You give it a hard slap, making her yelp."

    return

label scene_doggy_anal_2(the_girl, the_location, the_object):

    if the_girl.sex_skills["Anal"] > 2:
        "[the_girl.title] works her hips back against you with each thrust, moaning happily to herself as your cock stretches out her asshole."
    else:
        "[the_girl.title] grunts and pants as your cock stretches out her asshole. Her hands ball into fists as she tries to adjust."

    "You reach forward and place your hands on her shoulders, pulling her against you with each stroke."
    $ the_girl.call_dialogue("sex_responses_anal")
    "Her ass squeezes down on your dick, so tight it's almost difficult to move."
    return

label outro_doggy_anal(the_girl, the_location, the_object):

    "Fucking [the_girl.possessive_title]'s tight asshole feels amazing, and you come closer and closer to your climax."
    "You pass the point of no return and speed up, slamming your cock into her with each thrust."
    $ the_girl.call_dialogue("sex_responses_anal")
    mc.name "Fuck, here I cum!"

    menu:
        "Cum inside of her.":
            "You push yourself balls deep into [the_girl.title]'s ass and dump your load."
            #This is where the "cum in me" section would go instead
            #the_girl.char "Ah! Ah!"
            "You hold yourself inside of her until your climax has passed, then pull out slowly and sit back."
            "She is left on her hands and knees, trying to catch her breath, as your cum drips out of her gaping asshole."
            $ the_girl.cum_in_ass()
            $ doggy_anal.redraw_scene(the_girl)
            if the_girl.get_opinion_score("anal creampies") > 0:
                # If she's into both...
                $ the_girl.discover_opinion("anal creampies")
                the_girl.char "Oh fuck... I'm so full cum. Put it back in me."
                mc.name "What?"
                the_girl.char "Your cock, put it back in me... Just a little bit more, please!"
                "She lowers her shoulders to the [the_object.name] and wiggles ass at you. You slide the tip of your still-hard dick into her asshole."
                the_girl.char "Ah..."
                "Your semen gives you the lubrication you need to slide into her smoothly and easily. She shivers with pleasure as you push yourself in balls deep."
                the_girl.char "Just... hold it there. Mphfhhh."
                "She bites her lip, closes her eyes, and moans."
                "Eventually your dick starts to soften and you pull out."


            else:
                the_girl.char "Wow, that was intense. I hope you didn't stretch me out too badly."


        "Cum on her ass.":
            "You pull out of [the_girl.possessive_title]'s asshole, leaving it gaping while you stroke yourself to completion."
            if the_girl.sex_skills["Anal"] > 2:
                "She sighs in relief as you pull out."
                the_girl.char "Oh thank god..."

            "You grunt and climax, shooting your hot cum out onto [the_girl.title]'s back and ass."
            $ the_girl.cum_on_ass()
            $ doggy_anal.redraw_scene(the_girl)
            if the_girl.sluttiness > 120:
                the_girl.char "Aw, I feel so empty now. You should have filled my ass with your cum instead."
            else:
                the_girl.char "Mmm, it's so warm."
    return

label transition_doggy_anal_doggy(the_girl, the_location, the_object):
#     #transition from anal to normal doggy style.
    "You pull out of [the_girl.title]'s asshole, leaving it gaping and her sighing in relief."
    "You shift your cock downwards and rub the tip of it along the slit of her vagina."
    $ wants_condom = True
    if the_girl.effective_sluttiness() < the_girl.get_no_condom_threshold(): #She wants a condom
        the_girl.char "Mmm, fuck me [the_girl.mc_title]. Use all of my holes for your pleasure!"
        $ wants_condom = False
    else: #She doesn't care.
        the_girl.char "Wait, wait... I can't risk getting pregnant, I need you to put on a condom."
        $ wants_condom = True

    menu:
        "Put on a condom.":
            "You pull your dick back and find a condom in your wallet. It takes you a moment to spread it over your cock, then you line yourself up again."

        "Ram it home!":
            if wants_condom:
                mc.name "Don't worry, I'll pull out."
                $ the_girl.change_happiness(-5)

            else:
                pass

    "You pull on her hips and thrust yourself inside her tight, wet pussy."
    return

label transition_default_doggy_anal(the_girl, the_location, the_object):

    "[the_girl.title] gets on her hands and knees as you kneel behind her. You bounce your hard shaft on her ass a couple of times before lining yourself up with tight asshole."
    mc.name "Ready?"
    the_girl.char "I... I think so."
    "You hold onto her hips and push forward, spreading her ass with your large cock. She gasps and balls her fists, until finally you've buried your shaft in her."
    "After giving her a second to acclimatise you start to thrust in and out, slowly at first but picking up speed."
    return

label strip_doggy_anal(the_girl, the_clothing, the_location, the_object):

    "[the_girl.title] leans foward, pulling your cock out of her."
    $ the_girl.call_dialogue("sex_strip")
    $ the_girl.draw_animated_removal(the_clothing, position = doggy.position_tag)
    "[the_girl.possessive_title] struggles out of her [the_clothing.name] and throws it to the side."
    "You line your cock back up with her ass and slide back in, a little easier than the first itme now that it's been stretched out."
    return

label strip_ask_doggy_anal(the_girl, the_clothing, the_location, the_object):
    the_girl.char "[the_girl.mc_title], what do you think of me taking off my [the_clothing.name]?"
    "[the_girl.title] pants as you fuck her ass from behind."
    menu:
        "Let her strip.":
            mc.name "Take it off for me."
            $ the_girl.draw_animated_removal(the_clothing, position = doggy.position_tag)
            "She leans forward and pops off your dick. [the_girl.possessive_title] struggles out of her [the_clothing.name] and throws it to the side."
            "When she's ready you line your cock back up with her asshole and slide back in, a little easier than the first itme now that it's been stretched out."

        "Leave it on.":
            mc.name "No, I want you to keep it on."
            if the_girl.sluttiness < 80:
                the_girl.char "Do I look sexy in it? Does it turn you on?"
                "You speed up, fucking her faster in response to her question."
            elif the_girl.sluttiness < 100:
                the_girl.char "Does it make me look like a good little slut? All I want to be is your good little slut [the_girl.mc_title]."
                "She pushes her hips back into you and grinds against you."
            else:
                the_girl.char "Does it look good on me, when you're fucking my ass? When you're stirring up my insides with your big cock?"
                "She pushes her hips back into you and grinds against you."
    return

label orgasm_doggy_anal(the_girl, the_location, the_object):
    "[the_girl.title]'s grunts and pants turn to moans of pleasure."
    $ the_girl.call_dialogue("climax_responses_anal")
    "She balls her fists and tenses up, her whole body quivering as she cums."
    "You fuck her ass through her climax, making her moan and pant with each thrust. After a few seconds it passes and she relaxes."
    the_girl.char "Oh god, keep fucking me [the_girl.mc_title]!"
    return
