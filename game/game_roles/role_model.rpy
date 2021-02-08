### Takes the old events that use to be Alexia specific and breaks them out into it's own role.
init -2 python:

    def model_photography_list_requirement(the_person):
        # if not mc.business.event_triggers_dict.get("has_expensive_camera",False):
        #     return False
        # elif not the_person.event_triggers_dict.get("ad_photography_enabled",False):
        #     return False
        if not mc.business.is_open_for_business():
            return False
        elif mc.business.get_employee_workstation(the_person) is None:
            return False
        elif time_of_day >= 4:
            return "Too late to start taking pictures."
        elif mc.business.event_triggers_dict.get("Last Ad Shot Day", -7) + 7 > day:
            return "An ad is already running."
        else:
            return True

    def fire_model_requirment(the_person):
        return True

label fire_model_label(the_person):
    mc.name "I'm sorry [the_person.title], but I will no longer be needing you to star in our ad campaigns."
    $ the_person.change_happiness(-5)
    the_person "Oh... Okay."
    $ mc.business.company_model = None
    $ the_person.remove_role(company_model_role) #TODO: Investigate a crash where Alxia sometimes has this action but not the role itself??
    return

label model_photography_list_label(the_person):
    #TODO: Add a chance for her to drink some serum before this happens for maximum manipulation potential.
    mc.name "I want you to put together a new company ad. We'll need some promotional pictures to go with it."
    the_person "Sounds like a good idea to me. I've got the camera right here."
    "[the_person.title] grabs the camera from her desk and hands it to you."

    if the_person.is_wearing_uniform(): #Check to see if she should have a uniform on.
        if the_person.judge_outfit(the_person.outfit, the_person.get_opinion_score("skimpy uniforms")*5):
            the_person "Is my uniform fine for the shoot, or should I put something else on?"

        else:
            the_person "Do I get to change into something more reasonable, or do you want me in my uniform?"
    else:
        the_person "How do I look? Do you think I should wear something else for this?"
        $ the_person.draw_person(position = "back_peek")
        "She gives you a quick spin."
        the_person "I want to make sure I show my best side for the business."

    menu:
        "Your outfit is fine.":
            mc.name "You look great already, I don't think you need to change a thing."
            $ the_person.discover_opinion("skimpy uniforms")
            $ the_person.change_slut_temp(the_person.get_opinion_score("skimpy uniforms"))
            the_person "Okay, I think I'm ready to go then!"

        "Put something else on for me.":
            mc.name "I think you could use something with a little more pop."
            if the_person.effective_sluttiness() < 20 and the_person.relationship != "Single":
                the_person "Nothing too crazy though, okay? I don't want my boyfriend to freak out when he hears about this."
            else:
                the_person "Sex sells, right, so it should be something skimpy. Did you have something in mind?"
                "She seems excited to see what you have in mind."

            call outfit_master_manager(slut_limit = the_person.sluttiness, show_overwear = False, show_underwear = False) from _call_outfit_master_manager_7
            if _return:
                if the_person.judge_outfit(the_person.outfit, _return.slut_requirement):
                    the_person "Yeah, I think that would look good. I'll go put that on."

                $ clear_scene()
                "[the_person.possessive_title] leaves to get changed and is back in a moment."
                $ the_person.apply_outfit(_return, update_taboo = True)
                $ the_person.draw_person()

            else:
                mc.name "On second thought, I think you look perfect in that."

    "You lead [the_person.possessive_title] to a supply room. She stands against a blank wall while you get the camera ready."
    mc.name "Okay, strike a pose for me."
    $ the_person.draw_person(position = "stand4", emotion = "happy")
    "She smiles at the camera and poses for you."
    the_person "Tell me what you want me to do."

    #Outfit checks that let us be sure a girl isn't already naked before asking her to strip.
    $ outfit_state = 0 #0 = relatively normal outfit. 1 = just underwear, can't be stripped down further without being naked. 2 = already naked.
    if the_person.outfit.wearing_bra() and the_person.outfit.wearing_panties() and the_person.outfit.bra_covered() and the_person.outfit.panties_covered(): #She has underwear on and something over both.
        $ outfit_state = 0 #She's wearing enough we can have a "strip to your underwear" scene.
    elif (the_person.outfit.wearing_bra() and not the_person.outfit.bra_covered()) or (the_person.outfit.wearing_panties() and not the_person.outfit.panties_covered()) or (not the_person.outfit.tits_visible() and not the_person.outfit.vagina_visible()):
        $ outfit_state = 1 #She's wearing enough that we can have a strip scene.
    else:
        $ outfit_state = 2 #She's practically naked with no clothing on.

    $ slut_willingness = the_person.effective_sluttiness()
    if the_person.obedience > 100:
        $ slut_willingness += the_person.obedience - 100

    # These are "checkpoint" options for future passes through this event.
    menu:
        "Be playful.":
            call photo_be_playful(the_person) from _call_photo_be_playful

        "Be flirty." if the_person.event_triggers_dict.get("camera_flirt", False) and slut_willingness+(5*the_person.get_opinion_score("skimpy uniforms")) >= 15:
            mc.name "Be flirty for me. You're young and sexy, I want you to show that to the camera."
            call photo_be_sexy(the_person) from _call_photo_be_sexy

        "Strip to your underwear." if the_person.event_triggers_dict.get("camera_flash", False) and outfit_state == 0 and slut_willingness+(5*the_person.get_opinion_score("skimpy uniforms")) >= 30:
            mc.name "I want to take some sexy, bold photos of you in your underwear. I want you to strip down for the camera."
            call photo_flash(the_person) from _call_photo_flash

        "Get naked." if the_person.event_triggers_dict.get("camera_naked", False) and outfit_state in [0,1] and slut_willingness+(5*the_person.get_opinion_score("not wearing anything")) >= 50:
            mc.name "Strip everything off for me, I want to get some nude shots."
            call photo_naked(the_person) from _call_photo_naked

        "Touch yourself." if the_person.event_triggers_dict.get("camera_masterbate", False) and slut_willingness+(5*the_person.get_opinion_score("masturbating")) >= 60:
            if not outfit_state == 2:
                mc.name "Get naked and lean against that wall. I want to get some shots of you touching yourself."
                "[the_person.title] nods and starts to strip naked."
                call photo_strip_naked(the_person) from _call_photo_strip_naked
            else:
                mc.name "Lean up against that wall, I want to get some shots of you touching yourself."
            call photo_touch(the_person) from _call_photo_touch

        "Suck my dick." if the_person.event_triggers_dict.get("camera_suck", False) and slut_willingness+(5*the_person.get_opinion_score("giving blowjobs")) >= 70:
            if not outfit_state == 2:
                mc.name "Get naked and on your knees. I want to get some close ups of you sucking my cock."
                "[the_person.title] nods and starts to strip naked."
                call photo_strip_naked(the_person) from _call_photo_strip_naked_1
            else:
                mc.name "Come and kneel down in front of me. I want to get some close ups of you sucking my cock."
            call photo_blowjob(the_person) from _call_photo_blowjob

        "Get fucked on camera." if the_person.event_triggers_dict.get("camera_fuck", False) and slut_willingness+(5*the_person.get_opinion_score("vaginal sex")) >= 80:
            if not outfit_state == 2:
                mc.name "Get naked first, then I'm going to lay you down and get some pictures of you getting fucked."
            else:
                mc.name "I want you to come over here and lay down so I can take some pictures of you getting fucked."
            call photo_sex(the_person) from _call_photo_sex

    $ sexy_score = _return # Each scene returns the sexiness it produced (mainly based on her outfit).
    "You hand the camera over to [the_person.title] and go back to her desk. She pulls out the memory card and puts into the computer."
    $ the_person.draw_person(position = "sitting")
    "You go through the pictures you got, discarding the poor ones and finally settling on best ones to use."
    if the_person.relationship != "Single" and sexy_score > 30 :
        $ SO_title = SO_relationship_to_title(the_person.relationship)
        "You wonder what her [SO_title] would think about [the_person.title] showing so much skin for this ad."


    $ ad_multiplier = 1
    if sexy_score <= 10:
        "The photos you took of [the_person.title] are perfect for an ad placed at the back of a small medical journal."
        "Putting an ad here will boost serum value sales by {b}%%5{/b} for the next week."
        $ ad_multiplier = 1.05
    elif sexy_score <= 30:
        "The photos you took of [the_person.title] are perfect for an ad placed in a lifestyle magazine."
        "Putting an ad here will boost serum value sales by {b}%%10{/b} for the next week."
        $ ad_multiplier = 1.1
    elif sexy_score <= 50:
        "The photos you took of [the_person.title] are perfect for a sexy ad in a local tabloid."
        "Putting an ad here will boost serum value sales by {b}%%20{/b} for the next week."
        $ ad_multiplier = 1.2
    elif sexy_score <= 100:
        "The photos you took of [the_person.title] are perfect for a sexy ad in a soft core porn magazine."
        "Putting an ad here will boost serum value sales by {b}%%40{/b} for the next week."
        $ ad_multiplier = 1.4
    else:
        "The photos you took of [the_person.title] are perfect for a sexy ad in a hard core porn magazine."
        "Putting an ad here will boost serum value sales by {b}%%80{/b} for the next week."
        $ ad_multiplier = 1.8

    the_person "What do you think [the_person.mc_title]? Should I get this ad made up and sent out?"
    menu:
        "Pay for the ad space. -$300" if mc.business.funds >=300:
            mc.name "The picutres look good, get to work and get that pushed out as soon as possible."
            the_person "You got it!"
            $ mc.business.funds += -300
            $ mc.business.add_sales_multiplier("Ad Campaign", ad_multiplier)
            $ ad_expire_trigger = Action("Ad Expire", ad_expire_requirement, "ad_expire", args = ad_multiplier, requirement_args = day+7)
            $ mc.business.mandatory_crises_list.append(ad_expire_trigger) #It'll expire in 7 days.
            $ mc.business.event_triggers_dict["Last Ad Shot Day"] = day


        "Pay for the ad space. -$300 (disabled)" if mc.business.funds < 300:
            pass

        "Scrap the plan.":
            mc.name "I think our budget is better spent somewhere else. Sorry to put you through all that work."
            the_person "I understand. Maybe if we start selling more it'll be worth it."

    call advance_time from _call_advance_time_20
    return

label photo_be_playful(the_person):
    mc.name "Be playful. Give the camera a smile and just have fun with it."
    $ the_person.draw_person(position = "stand3", emotion = "happy")
    "She gives you a few more poses and seems to be enjoying herself."
    $ the_person.draw_person(position = "stand5", emotion = "happy")

    $ slut_willingness = the_person.effective_sluttiness() + (5*the_person.get_opinion_score("skimpy uniforms"))
    if the_person.obedience > 100:
        $ slut_willingness += the_person.obedience - 100
    menu:
        "Push her to be flirty." if slut_willingness >= 15:
            mc.name "That's great [the_person.title]. Give me a little more attitude now. You're sexy, you're young, let me feel it!"
            call photo_be_sexy(the_person) from _call_photo_be_sexy_1

        "Push her to be flirty.\n{color=#ff0000}Not slutty or obedient enough{/color} (disabled)" if slut_willingness < 15:
            pass

        "Finish the shoot.":
            "You take a few final pictures."
            mc.name "I think that's all we need. Good job [the_person.title], you look great."
            $ the_person.change_happiness(3)
            the_person "Glad to hear it, that was fun!"
            return the_person.outfit.slut_requirement
    return _return

label photo_be_sexy(the_person):
    $ the_person.event_triggers_dict["camera_flirt"] = True
    if the_person.effective_sluttiness() >= 15:
        #She's totally onboard with this idea.
        $ the_person.draw_person(position = "back_peek", emotion = "happy")
        "[the_person.possessive_title] spins around, peeking over her shoulder."
        the_person "Like this? Get a good shot of my butt, that's the kind of shot you probably want."
        "She wiggles her ass for the camera."

    else:
        #She's only doing it because you're commanding her.
        the_person "Oh my god, I feel so awkward trying to do this. This isn't me at all!"
        mc.name "Trust me, just give it a try. Turn around and shake your ass, that'll be sexy."
        $ the_person.draw_person(position = "back_peek", emotion = "happy")
        $ the_person.change_obedience(1)
        "She timidly wiggles her butt for the camera."

    $ slut_willingness = the_person.effective_sluttiness()
    if the_person.obedience > 100:
        $ slut_willingness += the_person.obedience - 100

    $ skimpy_uniform_bonus = (5*the_person.get_opinion_score("skimpy uniforms"))
    $ no_clothing_bonus = (5*the_person.get_opinion_score("not wearing anything"))
    $ masturbate_bonus = (5*the_person.get_opinion_score("masturbating"))

    $ outfit_state = 0 #0 = relatively normal outfit. 1 = just underwear, can't be stripped down further without being naked. 2 = already naked.
    if the_person.outfit.wearing_bra() and the_person.outfit.wearing_panties() and the_person.outfit.bra_covered() and the_person.outfit.panties_covered(): #She has underwear on and something over both.
        $ outfit_state = 0 #She's wearing enough we can have a "strip to your underwear" scene.
    elif (the_person.outfit.wearing_bra() and not the_person.outfit.bra_covered()) or (the_person.outfit.wearing_panties() and not the_person.outfit.panties_covered()) or (not the_person.outfit.tits_visible() and not the_person.outfit.vagina_visible()):
        $ outfit_state = 1 #She's wearing enough that we can have a strip scene.
    else:
        $ outfit_state = 2 #She's practically naked with no clothing on.
    menu:
        "Strip to your underwear." if slut_willingness+skimpy_uniform_bonus >= 30 and outfit_state == 0: #TODO: Also check to make sure she's got the right type of clothign TO strip down to her underwear
            #Into her flashing the camera.
            mc.name "These are looking great. Now let's trying something a little more bold. Get into your underwear for me [the_person.title]."
            call photo_flash(the_person) from _call_photo_flash_1

        "Strip to your underwear.\n{color=#ff0000}Not slutty or obedient enough{/color} (disabled)" if slut_willingness+skimpy_uniform_bonus < 30 and outfit_state == 0:
            pass

        "Get naked for the camera." if slut_willingness+no_clothing_bonus >= 50 and outfit_state == 1: #If that's the only possible next step based on her outfit.
            mc.name "Let's kick it up another notch. Get completely naked for these next shots."
            call photo_naked(the_person) from _call_photo_naked_1

        "Get naked for the camera.\n{color=#ff0000}Not slutty or obedient enough{/color} (disabled)" if slut_willingness+skimpy_uniform_bonus < 50 and outfit_state == 1:
            pass

        "Touch yourself." if slut_willingness+masturbate_bonus >= 60 and outfit_state == 2:
            mc.name "You're already undressed for the occasion, so lean against that wall and touch yourself for the camera. I want to see you really get into it."
            call photo_touch(the_person) from _call_photo_touch_1

        "Touch yourself.\n{color=#ff0000}Not slutty or obedient enough{/color} (disabled)" if slut_willingness+masturbate_bonus < 60 and outfit_state == 2:
            pass

        "Finish the shoot.":
            "You take a few final pictures."
            mc.name "I think I got everything we need. Good job [the_person.title], you look great."
            $ the_person.change_happiness(3)
            the_person "Glad to hear it, that was fun!"
            return the_person.outfit.slut_requirement
    return _return

label photo_flash(the_person):
    $ the_person.event_triggers_dict["camera_flash"] = True

    $ first_item = the_person.outfit.get_upper_top_layer()
    if the_person.effective_sluttiness("underwear_nudity") >= 30:
        # She's slutty enough to do it.
        "[the_person.title] nods and starts to take off her [first_item.name]."

    else:
        # She's doing it for obedience or has a taboo
        "[the_person.possessive_title] hesitates."
        the_person "This is really what you think we need to do for the ad?"
        mc.name "Come on [the_person.title], I'm counting on you."
        "She takes a deep breath, then presses on and starts to take off her [first_item.name]."

    $ the_person.draw_animated_removal(first_item)
    if not person.outfit.panties_covered():
        "When she drops it she's wearing only her underwear."
    else:
        $ covering_item = the_person.outfit.get_lower_top_layer()

        "She pulls it off and drops it to the ground, then starts to pull off her [covering_item.name]."
        $ the_person.draw_animated_removal(covering_item)
        "When that comes off she's left wearing only her underwear."

    if the_person.judge_outfit(the_person.outfit):
        the_person "Time for you to get those shots [the_person.mc_title]!"
        $ the_person.draw_person(position = "stand3", emotion = "happy")
        "[the_person.title] gives you a few different poses in her underwear."
        $ the_person.draw_person(position = "stand4", emotion = "happy")

    else:
        the_person "Take those pictures before I have second thoughts..."
        $ the_person.draw_person(position = "stand3")
        "[the_person.title] switches quickly between a few different poses, obviously a little uncomfortable with her state of undress."
        $ the_person.draw_person(position = "stand4")

    if the_person.break_taboo("underwear_nudity"):
        the_person "She seems to relax after her initial hesitation and becomes more comfortable in her underwear as the shoot goes on."
    $ the_person.update_outfit_taboos()


    $ slut_willingness = the_person.effective_sluttiness(["bare_tits","bare_pussy"]) + (5*the_person.get_opinion_score("not wearing anything"))
    if the_person.obedience > 100:
        $ slut_willingness += the_person.obedience - 100
    menu:
        "Strip naked." if slut_willingness >= 50:
            mc.name "That's great [the_person.title], this is great material. Next up I want to get some nude shots, so keep stripping for me."
            call photo_naked(the_person) from _call_photo_naked_2

        "Strip naked.\n{color=#ff0000}Not slutty or obedient enough{/color} (disabled)" if slut_willingness < 50:
            pass

        "Finish the shoot.":
            mc.name "I think I've got all the pictures we need, we can call it there."
            the_person "Yay, glad to help!"
            $ the_person.change_slut_temp(1)
            $ the_person.change_obedience(2)
            $ the_person.review_outfit()
            return the_person.outfit.slut_requirement

    return _return

label photo_naked(the_person):
    $ the_person.event_triggers_dict["camera_naked"] = True
    if the_person.effective_sluttiness(["bare_tits","bare_pussy"]) >= 40:
        the_person "You got it [the_person.mc_title], I'm up for a little taseful nudity."
        "You make sure to get some pictures as she strips off her underwear."
    else:
        the_person "Okay... I think I can do that..."
        "She takes a few deep breaths before she starts to take off her underwear. You make sure to get some pictures as she strips down."

    call photo_strip_naked(the_person) from _call_photo_strip_naked_2


    if the_person.judge_outfit(the_person.outfit, 5*the_person.get_opinion_score("not wearing anything")) and not the_person.has_taboo(["bare_tits", "bare_pussy"]):
        "[the_person.title] drops her underwear to the side and turns to face you."
        the_person "There! How do I look? Good?"
        $ the_person.draw_person(position = "back_peek")
        "She winks at you and gives you a quick spin, showing off her ass."

    else:
        "[the_person.title] seems unsure of what to do now that she's completely naked."
        the_person "Oh my god [the_person.mc_title], my heart is pounding... I feel so vulnerable like this."
        mc.name "You look great [the_person.title], just give me a little spin and relax. Let me do all the hard work, you just have to look pretty."
        $ the_person.draw_person(position = "back_peek")
        if the_person.relationship != "Single":
            $ SO_title = SO_relationship_to_title(the_person.relationship)
            the_person "Do.... do you think my [SO_title] would be okay with this?"
            $ the_person.draw_person()
            the_person "It's not like we're doing anything wrong, this is all just for work."
            menu:
                "Reassure her.":
                    mc.name "If he was a reasonable person he'd be fine with this."
                    mc.name "You're using your, uh, natural talents to perform your job as well as you can. That's an admirable thing to do."
                    $ the_person.change_happiness(2)
                    $ the_person.change_slut_temp(1)
                    "She smiles and nods."
                    the_person "Yeah, that's what I think too."

                "Make her worry.":
                    mc.name "I don't know [the_person.title]. Some men would be very jealous that you were showing off your body to anyone but them."
                    mc.name "Me and you both know it's for the good of the company, but he might not see it that way."
                    $ the_person.change_happiness(-5)
                    $ the_person.draw_person(emotion = "sad")
                    mc.name "But I wouldn't worry about it too much. We can keep it our little secret if you'd like."
                    $ the_person.change_obedience(3)
                    the_person "That... might be a good idea. Thanks [the_person.mc_title]."
                    mc.name "No problem. Now smile for the camera and let me get a good look at your tits for this next shot."

        else:
            the_person "She gives you a quick spin before turning back."

        if the_person.has_taboo(["bare_tits", "bare_pussy"]):
            "Despite her initial hesitation, [the_person.title] soon seems quite comfortable in front of the camera without her clothes on."
            $ the_person.update_outfit_taboos()


    $ the_person.draw_person()
    the_person "Do you have all the shots you want, or did you have something more in mind?"
    $ slut_willingness = the_person.effective_sluttiness()
    if the_person.obedience > 100:
        $ slut_willingness += the_person.obedience - 100
    $ slut_willingness += the_person.get_opinion_score("masturbating") * 5

    menu:
        "Touch yourself." if slut_willingness >= 45:
            mc.name "I want to get some more sensual shots of you. Lean back against the wall and touch yourself."
            call photo_touch(the_person) from _call_photo_touch_2

        "Touch yourself.\n{color=#ff0000}Not slutty or obedient enough{/color} (disabled)" if slut_willingness < 60:
            pass

        "Finish the shoot.":
            mc.name "I think that's everything we need."
            $ the_person.change_obedience(2)
            $ the_person.change_slut_temp(2)
            $ the_person.review_outfit()
            "[the_person.title] collects her things and you finish up the photo shoot."
            return the_person.outfit.slut_requirement
    return _return

label photo_touch(the_person):
    $ the_person.event_triggers_dict["camera_touch"] = True
    if the_person.effective_sluttiness() >= 45:
        "[the_person.title] doesn't hesistate at all. She takes a step back and leans against the wall, spreading her legs slightly."
    else:
        the_person "Touch myself? What do you... what do you mean [the_person.mc_title]? I couldn't... do that in front of you."
        "[the_person.title] looks nervous. She seems suddenly self conscious, turning side-on to the camera to limit how much it can see."
        mc.name "Just relax. It's not like you haven't done it before, right?"
        the_person "Well obviously not, but..."
        mc.name "And it's not like you're the first person to touch themselves in front of a camera."
        the_person "Yeah, I know but..."
        mc.name "And it's for the business. You want us to do well, right?"
        if the_person.relationship != "Single":
            $ SO_title = SO_relationship_to_title(the_person.relationship)
            the_person "But what do I tell my [SO_title]? What happens if he sees our ad and sees all of this?"
            mc.name "Tell him whatever you want, he doesn't control you. The only important question is if you want to do this."
            "She thinks about it for a long moment."
            the_person "Yeah, I do. For you. Uh, I mean, for your business."
            mc.name "Then he should respect what you want to do. If he doesn't, that's his problem."
            $ the_person.change_obedience(-1)
            $ the_person.change_slut_temp(1 + the_person.get_opinion_score("cheating on men"))
            $ the_person.discover_opinion("cheating on men")
            "[the_person.possessive_title] seems filled with a sudden resolve. She takes a deep breath and turns back towards the camera."
            the_person "You're right. Fuck him if he isn't happy about it."
            "She leans back against the wall and spreads her legs slightly."

        else:
            the_person "Yeah... Of course I do. You're right."
            "She takes a deep breath shakes her arms out, like an athlete about to perform. Her cute tits jiggle as she moves."
            the_person "You can do this. Just relax [the_person.title], you can do this."
            "She leans back against the wall and spreads her legs slightly."

    "[the_person.possessive_title] slowly runs her hand up her inner thigh. You can hear her breath catch in her throat as she comes closer to the top."
    "She stops just before she reaches her pussy and does it again, this time moving along the other thigh."
    "You take a few steps to the side to get a better angle of [the_person.title] as she sensually feels herself up."
    mc.name "That's great, now a little higher."
    "Her hand slides all the way up and her fingers glide gently over her slit."
    the_person "Ah..."
    "She hesitates for a second, then slips her middle finger into herself with a soft, throaty moan."
    "You take a few steps closer and take some more pictures."
    "[the_person.title]'s other hand comes up subconciously and cradles a breast as she starts to slowly finger herself."
    "Without any prompting she starts to speed up. Her breathing gets louder and she slides a second finger inside."

    $ slut_willingness = the_person.effective_sluttiness("sucking_cock")
    if the_person.obedience > 100:
        $ slut_willingness += the_person.obedience - 100
    $ slut_willingness += the_person.get_opinion_score("giving blowjobs") * 5
    menu:
        "Suck my cock." if slut_willingness >= 55:
            mc.name "That's perfect [the_person.title]. Now just get onto your knees for me, we're going to get some hard core shots."
            call photo_blowjob(the_person) from _call_photo_blowjob_1

        "Suck my cock.\n{color=#ff0000}Not slutty or obedient enough{/color} (disabled)" if slut_willingness < 70:
            pass

        "Take photos as she climaxes.":
            the_person "Ah... Hah..."
            "[the_person.possessive_title] turns her head away from the camera and closes her eyes to focus on the task at hand."
            "She moves both hands down to her pussy, fingering herself with one and rubbing her clit with the other."
            the_person "Do... oh god, do you want me to go all the way?"
            mc.name "Yes, I do. We'll get some great photos out of this."
            "She moans louder and tilts her head back."
            the_person "I'm... going to cum! Fuck!"
            $ the_person.change_slut_temp(3)
            $ the_person.change_happiness(5)
            "She gasps and tenses up, both hands moving as fast as she can make them."
            "Then the tension melts away and she slumps a little against the wall. She sighs and opens her eyes."
            the_person "Did you get that?"
            mc.name "Yeah, I got it."
            the_person "Good, I don't think I could manage that again. Whew..."
            "[the_person.title] goes to get cleaned up and you finish up the shoot."
            $ the_person.review_outfit()
            return the_person.outfit.slut_requirement + (the_person.sex_skills["Foreplay"] * 5)
    return _return

label photo_blowjob(the_person):
    $ the_person.event_triggers_dict["camera_suck"] = True
    #TODO: boyfriend might call while she's "busy with work." Alternates between talking to him and sucking your cock on the phone.

    if the_person.effective_sluttiness("sucking_cock") >= 55 and not the_person.has_taboo("sucking_cock"):
        "You step towards her and [the_person.title] kneels down."
        the_person "Make sure I'm in focus."
        "She reaches for your pants and unzips your fly."

    else:
        if the_person.relationship != "Single":
            $ SO_title = SO_relationship_to_title(the_person.relationship)
            the_person "Wait, wait, wait. This really crosses a line, don't you think?"
            mc.name "What do you mean?"
            the_person "I can justify doing some nude shots. I can understand wanting some sensual shots with me touching myself."
            the_person "But how could I ever tell my [SO_title] about giving someone else a blowjob?"
            "She crosses her arms and looks away."
            "You lower the camera and take a step closer to [the_person.possessive_title]. You reach out and touch her shoulder. She looks up at you."
            mc.name "Don't think about your [SO_title] right now. Think about me, and the business, and what you want to do."
            mc.name "We can make sure he never sees these ads. I need you, [the_person.title]."
            "Her expression softens. Finally she sighs and uncrosses her arms."
            the_person "I... I can't believe I'm going to do this. Make sure to get plenty of good shots, make this worth it."
            "She kneels down in front of you and unzips your fly for you."

        else:
            "She takes unsteady step forward, then pauses."
            the_person "I don't know [the_person.mc_title]..."
            mc.name "It's for the company [the_person.title], don't let me down now."
            "After a moment of hesitation she comes closer and kneels down. She reaches out and undoes your fly."


    $ the_person.draw_person(position = "blowjob")
    "You hold the camera in one hand, positioning it to the side as [the_person.possessive_title] pulls your pants down."
    the_person "Let's see what I'm working with down here."
    "Your hard cock springs free of your underwear as she yanks it down."
    if the_person.effective_sluttiness("sucking_cock") >= 65 or the_person.get_opinion_score("giving blowjobs") > 0:
        the_person "Mmm, that's what I like to see."
    else:
        the_person "Sweet Jesus..."
    $ the_person.draw_person(position = "blowjob", special_modifier = "blowjob")
    "She licks at the tip a couple of times, then slips it into her mouth."
    $ the_person.break_taboo("sucking_cock")
    "You feel [the_person.title]'s tounge lick at the bottom of your shaft as she starts to move her head, bobbing it back and forth."
    "You try to stay focused and snap a few more pictures as she sucks you off."


    $ slut_willingness = the_person.effective_sluttiness("sucking_cock")
    if the_person.obedience > 100:
        $ slut_willingness += the_person.obedience - 100
    $ slut_willingness += the_person.get_opinion_score("vaginal sex") * 5
    menu:
        "Fuck her." if the_person.effective_sluttiness("vaginal_sex") >= 65:
            mc.name "We've come this far, there's only one more thing we can do. Lie down so I can fuck you."
            $ the_person.draw_person(position = "blowjob")
            call photo_sex(the_person) from _call_photo_sex_1

        "Take photos as you cum.":
            mc.name "I'm going to cum, get ready!"
            $ the_person.draw_person(position = "blowjob")
            "You pull your cock out of [the_person.possessive_title]'s mouth and stroke it off with your left hand, working the camera with your right."
            "She looks up at you as you cum, blowing your hot load over her face. You struggle to keep the camera pointed in the right direction."
            $ the_person.cum_on_face()
            $ the_person.draw_person(position = "blowjob")
            $ the_person.change_slut_temp(the_person.get_opinion_score("being covered in cum"))
            $ the_person.discover_opinion("being covered in cum")
            "It takes you a couple long seconds to recover from your orgasm."
            "When you're able to you recenter the camera and take a few pictures of [the_person.title]'s cum splattered face."
            the_person "How do I look?"
            mc.name "Beautiful. Smile for the camera!"
            "Once you've taken all the pictures you think you'll need you get cleaned up."
            $ the_person.review_outfit()
            return the_person.outfit.slut_requirement + 10 + (5* the_person.sex_skills["Oral"])
    return _return

label photo_sex(the_person):
    $ the_person.event_triggers_dict["camera_fuck"] = True
    #TODO: Add a crisis where her boyfriend recognizes her after this event has taken place.

    if the_person.effective_sluttiness("vaginal_sex") < 65 or the_person.has_taboo("vaginal_sex"):
        if the_person.relationship != "Single":
            $ SO_title = SO_relationship_to_title(the_person.relationship)
            the_person "I can't do that [the_person.mc_title], my [SO_title]..."
            mc.name "We've gone so far already, what's the difference? Just relax and do what feel natural."
            "Her resistance wavers, then melts away."
        else:
            the_person "I can't do that [the_person.mc_title]..."
            mc.name "We've gone so far already, what's the difference? Just relax and do what feel natural."
            "Her resistance wavers, then melts away."
    else:
        "[the_person.title] nods excitedly."

    $ the_person.draw_person(position = "missionary")
    "She lies down and you get on your knees. You pull her close to you, legs to either side with her pussy in line with your hard cock."
    if the_person.has_taboo("vaginal_sex"):
        $ the_person.call_dialogue("vaginal_sex_taboo_break")
        $ the_person.break_taboo("vaginal_sex")
    $ mc.condom = False #Just in case we didn't maintain it properly or something
    call condom_ask(the_person) from _call_condom_ask_2
    if not _return: #We don't have an easy case to fail out to here, so we just "pretend" you have a second chance to do the right thing with some stat penalties.
        $ the_person.change_happiness(-5)
        $ the_person.change_obedience(-2)
        mc.name "But we need these shots [the_person.title]."
        the_person "Then you {i}need{/i} to put on a condom. I'm not going to ask again. Do it or I'm done here."
        "You sigh and put the camera to the side, pulling a condom over your cock as quickly as you can manage."
        $ mc.condom = True
    "You pull on [the_person.title]'s hips and thrust forward. Her pussy is warm and wet, inviting you in."
    $ the_person.call_dialogue("sex_responses_vaginal")
    "You thrust as best you can from a kneeling position, your hands busy with the camera."
    "You take pictures of [the_person.possessive_title]'s face as you fuck her and her cunt as you slide in and out."
    if the_person.relationship != "Single" and the_person.effective_sluttiness() > 65:
        "You hear [the_person.title] mumble to herself."
        the_person "I'm sorry sweetheart, but this feels so good..."

    "You lay into her, fucking her until you feel your orgasm approaching."
    $ the_person.change_slut_temp(5)
    $ came_inside_mod = 0
    menu:
        "Cum on [the_person.title].":
            $ the_person.change_slut_temp(the_person.get_opinion_score("being covered in cum"))
            $ the_person.discover_opinion("being covered in cum")
            if mc.condom:
                "You pull out of [the_person.title]'s tight pussy. You whip the condom off with your left hand, then start to stroke yourself to completion."

            else:
                "You pull out of [the_person.title]'s tight pussy and grab it with your left hand, stroking yourself to completion."

            "You fire your load out over her, struggling to keep the camera pointed in the right direction."
            $ the_person.cum_on_stomach()
            $ the_person.draw_person(position = "missionary")
            "She gasps softly as she is spattered with your hot cum. For a few seconds you're both quiet as you catch your breath."

        "Creampie her." if not mc.condom:
            $ the_person.change_slut_temp(the_person.get_opinion_score("creampies"))
            $ the_person.discover_opinion("creampies")
            "You pull on [the_person.title]'s hips one handed and thrust as deep as you can into her."
            $ the_person.cum_in_vagina()
            "You stay tight against her while you pump your hot load deep inside of her pussy. She closes her eyes and moans."
            "For a few seconds you're both quiet, panting for breath. You make sure to get some pictures as you pull out and your cum drips out of her cunt."
            if the_person.relationship != "Single":
                if the_person.effective_sluttiness() < 90 - (the_person.get_opinion_score("cheating on men") * 10):
                    the_person "I'm so sorry... I'm so sorry sweetheart."
                else:
                    $ SO_title = SO_relationship_to_title(the_person.relationship)
                    the_person "I hope my [SO_title] doesn't mind if I get pregnant. I'll just say it's his I guess."

            else:
                the_person "Fuck, that was intense."

            $ came_inside_mod = 10

        "Creampie her. (disabled)" if mc.condom:
            pass

    mc.name "I think I got all the pictures I'll need."
    the_person "I would hope so. Hell of a time to realise the lens cap was on."
    $ mc.condom = False
    $ the_person.review_outfit()
    return the_person.outfit.slut_requirement + 15 + (5* the_person.sex_skills["Vaginal"]) + came_inside_mod

label photo_strip_naked(the_person): #A helper label that strips a girl until her top and bottom are available for whatever you want to use them fore
    #Possible alternative: just strip until tits and vagina are usable.
    while the_person.outfit.get_upper_top_layer() is not None or the_person.outfit.get_lower_top_layer() is not None: #Strip until the top and bottom are empty, ie not None.
        $ the_item = the_person.outfit.remove_random_any(top_layer_first = True, exclude_feet = True, do_not_remove = True)
        $ the_person.draw_animated_removal(the_item)
        "" #Just so they can click through and see each thing removed.
    return

label ad_expire(the_amount):
    $ mc.business.remove_sales_multiplier("Ad Campaign", the_amount)
    return
