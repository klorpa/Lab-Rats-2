### All information, events, and requirements related to the affair roll.

init -1 python:
    def so_morning_breakup_requirement(the_person):
        return True #ALways valid for now.

    def leave_SO_love_calculation(the_person): #Standalone calculation so we can use these values in multiple dfferent events
        love_required = 80 - (the_person.get_opinion_score("cheating on men") * 10) #This should never be lower than the love reuqirement for her being your girlfriend.
        if the_person.relationship == "Fiancée":
            love_required += 10
        elif the_person.relationship == "Married":
            love_required += 20
        return love_required

    def ask_leave_SO_requirement(the_person):
        love_required = leave_SO_love_calculation(the_person)
        if the_person.love < love_required:
            return "Requires: " + str(love_required) + " Love"
        else:
            return True

    def fuck_date_requirement(the_person):
        if mc.business.event_triggers_dict.get("date_scheduled", False):
            return "You already have a date planned!"
        else:
            return True

    def caught_affair_cheating_requirement(the_person): #Event when you have public sex in front of someone you're having an affair with.
        return True


label ask_leave_SO_label(the_person): #
    # Ask her to leave her significant other. Requires high love (and no negatively impactful opinions).
    # If successful, sets their SO to None (store it for future use in crises if we want), removes the affair role, and gives them the girlfriend role.

    mc.name "Can we talk about something?"
    the_person "You know I've always got five minutes for you."
    $ so_title = SO_relationship_to_title(the_person.relationship)
    mc.name "I want you to leave your [so_title]. I want you to be with me, and only me."
    the_person "[the_person.mc_title]... Do you really mean that?"
    "You nod. She takes a long moment to think, then finally nods back and smiles happily."
    the_person "Okay, I'll do it for you!"
    call transform_affair(the_person) from _call_transform_affair_3
    $ the_person.change_love(10)
    $ the_person.change_obedience(5)
    $ the_person.draw_person(emotion = "happy")
    "You put your arms around her waist and she kisses you immediately. When you break the kiss she's grinning ear to ear."
    $ ex_title = so_title[:4] #Get's only the first 4 characters of any title for some hesitant-sounding speach.
    the_person "It feels so good to not have to hide anything anymore! I'll break the news to my [ex_title]... My ex-[so_title] later today."
    return

label plan_fuck_date_label(the_person):
    # A special date available to people you're in an affair with. Just hard core fucking, as long as you have the energy for.
    # Raises her love and sluttiness, with a small chance each time that her SO will come home and catch you.
    # If he comes home, chance to assert dominance and just keep fucking her (if she would normally leave her SO, or if you can make her cum when he comes in).

    $ so_title = SO_relationship_to_title(the_person.relationship)
    "You place a hand on [the_person.possessive_title]'s hips and caress her leg. She smiles and leans into your hand."
    mc.name "I want to be alone with you. When will your [so_title] be out of the way so I can have you all to myself?"
    if the_person.kids > 0:
        the_person "He normally stays late at work on Fridays. I can make sure the house is empty and we can get down to business the moment you're in the door."
    else:
        the_person "He's normally stuck late at work on Fridays. Just come on over and we can get down to business."

    menu:
        "Plan a date for Friday night.":
            mc.name "Good, I'll be there."
            the_person "I'll be ready and waiting."
            "She winks at you and smiles."
            $ fuck_date_action = Action("Fuck date", evening_date_trigger, "fuck_date_label", args = the_person, requirement_args = 4) #Happens on a friday
            $ mc.business.mandatory_crises_list.append(fuck_date_action)
            $ mc.business.event_triggers_dict["date_scheduled"] = True

        "Maybe some other time.":
            mc.name "Damn, that's not going to work for me."
            the_person "Aww, I guess I'll be spending the night alone then..."
            "She pouts and shrugs."
            the_person "Oh well, your loss."

    return

label fuck_date_label(the_person):
    #You go to her home and fuck her as much as your energy can support. Small chance her SO either calls or walks in.
    # Occures at night. You go to her place.

    $ mc.business.event_triggers_dict["date_scheduled"] = False #Deflag this event so you can schedule a date with another person for next week.
    if the_person.relationship == "Single":
        return #If she's single she must have broken up with her SO at some point, which means you're no longer having an affair with her. Clear out your date and move on with your life.

    "You have a fuck date planned with [the_person.title]."
    menu:
        "Get ready for the date. {image=gui/heart/Time_Advance.png}":
            pass

        "Cancel the date. (tooltip)She won't be happy with you canceling last minute.":
            "You get your phone out and text [the_person.title]."
            mc.name "I'm sorry, but something important came up at the last minute. We'll have to reschedule."
            $ the_person.change_love(-5)
            $ the_person.change_happiness(-5)
            "There's a pause before she responds."
            the_person "And I just finished getting all dressed up for you. Oh well."
            return

    $ mc.change_location(the_person.home)
    $ so_title = SO_relationship_to_title(the_person.relationship) #TODO: Make sure she's still in a relationship, or void this date if she isn't (because she's your girlfriend now).

    if the_person.home not in mc.known_home_locations:
        $ mc.known_home_locations.append(the_person.home)
        "You make your way to [the_person.possessive_title]'s house for the first time. You text her first, in case her [so_title] is unexpectedly home."
    else:
        "You make your way to [the_person.possessive_title]'s house. You text her first, in case her [so_title] is unexpectedly home."
    mc.name "I'm here. Are you ready?"
    the_person "Come on in, the door is unlocked. I'm in the bedroom"
    $ mc.location.show_background()
    "You go inside. The only light in the house comes from a room with its door ajar. When you swing it open you see [the_person.title] waiting."
    $ the_person.add_situational_slut("Date", 20, "There's no reason to hold back, he's here to fuck me!") # Bonus to sluttiness since you're in an affair and this is blatently a date to get fucked on.
    call fuck_date_event(the_person) from _call_fuck_date_event
    return "Advance Time"

label fuck_date_event(the_person): #A breakout function so we can call the fuck_date stuff any time you go back to a girls place.
    #Figure out her outfit for this
    $ so_title = SO_relationship_to_title(the_person.relationship)

    if the_person.get_opinion_score("not wearing anything") > the_person.get_opinion_score("lingerie"):
        $ the_person.apply_outfit(Outfit("Nude"), update_taboo = True) #She's wearing nothing at all. nothing at all. nothing at all...

    elif the_person.get_opinion_score("lingerie") >= 0:
        $ the_person.apply_outfit(lingerie_wardrobe.get_random_appropriate_outfit(the_person.sluttiness + 20, 0 + (the_person.sluttiness/2), guarantee_output = True), update_taboo = True) #She's just wearing lingerie for the evening.

    else:
        $ the_person.apply_outfit(the_person.wardrobe.decide_on_outfit(the_person.sluttiness, 0), update_taboo = True) #She picks a slutty outfit, but nothing truely "special".

    if the_person.obedience > 130 or the_person.get_opinion_score("being submissive") > 0 or the_person.get_opinion_score("giving blowjobs") > 0:
        #She's on her knees and ready to suck you off as soon as you come in.
        $ the_person.draw_person(position = "kneeling1")
        the_person "Hello, I'm ready for you [the_person.mc_title]..."
        "She licks her lips and watches you from her knees."
        the_person "Don't waste any time, I want you in my mouth."
        call fuck_person(the_person, private = True, start_position = blowjob) from _call_fuck_person_34

    else:
        #She's standing and ready to make out as soon as you come in."
        $ the_person.draw_person()
        the_person "Hello [the_person.mc_title]... I've been thinking about this all day."
        "You step inside. She reaches past you and closes the bedroom door." #Note that you never end up with submissive people down this branch
        "She wastes no time wrapping her arms around you and kissing you."
        call fuck_person(the_person, private = True, start_position = kissing) from _call_fuck_person_35

    $ the_report = _return

    $ done = False
    $ girl_came = False
    $ so_called = False
    $ energy_gain_amount = 50 #Drops each round, representing your flagging endurance.
    while not done:
        if the_report.get("girl orgasms", 0) > 0: #TODO: Have some variation to this based on how many times we've looped around.
            $ the_person.change_love(2 + the_person.get_opinion_score("cheating on men"))
            $ the_person.change_slut_temp(1)
            the_person "Oh god... That was amazing. You're so much better at that than my [so_title]."
            "[the_person.title] lies down on her bed and catches her breath."
            the_person "Ready to get back to it?"
            $ girl_came = True

        else:
            the_person "Whew, good job. Get some water and let's go for another!"
            "You take some time to catch your breath, drink some water, and wait for your refractory period to pass."
            "You hold [the_person.title] in bed while she caresses you and touches herself, keeping herself ready for you."



        if mc.energy < 40 and energy_gain_amount <= 20: #Forced to end the fuck date, so we set done to True.
            "The spirit is willing, but the flesh is spent. Try as she might [the_person.title] can't coax your erection back to life."
            if girl_came:
                the_person "Well, I guess that's all I'm going to be drawing out of you for tonight. That was fun."
                "She kisses you and runs her hand over your back."
                the_person "Now you should get going before my [so_title] gets home."

            else:

                $ the_person.change_love(-1)
                $ the_person.change_slut_temp(-1)
                the_person "Well I guess we're done then... Maybe next time you can get me off as well."

            $ done = True
            "You get dressed, triple check you haven't forgotten anything, and leave. [the_person.title] kisses you goodbye at the door."
        else:
            "After a short rest you've recovered some of your energy and [the_person.possessive_title]'s eager to get back to work."
            $ mc.change_energy(energy_gain_amount)
            $ the_person.change_energy(energy_gain_amount) #She gains some back too
            if energy_gain_amount >= 10:
                $ energy_gain_amount += -10 #Gain less and less energy back each time until eventually you're exhausted and gain nothing back.
            menu:
                "Fuck her again.":
                    "Soon you're ready to go again and you wrap your arms around [the_person.title]."
                    mc.name "Come here you little slut."
                    $ random_num = renpy.random.randint(0,100)
                    if random_num < 8 and not so_called:
                        #Her SO Comes home (unless he's called, in which case we know where he is.)
                        "She smiles and wraps her arms around you in return, pressing her body against yours."
                        the_person "Come and take me. I..."
                        "She freezes as shafts of light shine through the window curtains. You both listen as a car pulls in and turns its engine off."
                        mc.name "Is that..."
                        the_person "My [so_title]. Oh my god, what are we going to do?"

                        menu:
                            "Hide!":
                                $ done = True
                                "You jump up from [the_person.possessive_title]'s bed and look around the room. You hear her [so_title] close the car door."
                                $ random_num = renpy.random.randint(0,100)
                                $ hiding_under_bed = True
                                if random_num < 50:
                                    "Without many options you drop to the ground and shimmy yourself under her bed, trying to make sure you can't be seen from the bedroom door."
                                    "Above you [the_person.title] lies down on her bed and waits. You hear her [so_title] open the front door, then walk through the house toward you."


                                else:
                                    "Without many options you rush to her closet. You force your way past coats and dresses, pressing yourself to the very back."
                                    "You pull the flimsy closet doors closed behind you, peering nervously through the crack left between them."
                                    "[the_person.title] lies down on her bed and waits. You both listen as her [so_title] opens the front door, then walk through the house toward you."
                                    $ hiding_under_bed = False

                                "The door to the bedroom opens."
                                the_person.SO_name "I'm home! I hope I didn't startle you sweetheart."
                                the_person "Maybe a little, I didn't think you were going to be home tonight."
                                #TODO: IF they have kids reference that
                                the_person.SO_name "The client extended our deadline, so no more late nights for a while. Hopefully, at least."
                                if the_person.outfit.tits_visible() or the_person.outfit.vagina_visible() or the_person.outfit.slut_requirement > 40:
                                    #She's dressed (or undressed) like she's ready to have sex, so he takes the hint.
                                    if hiding_under_bed:
                                        "You feel [the_person.title]'s bed sink as her [so_title] slides onto it."
                                    else:
                                        "You watch her [so_title] slide onto the bed beside her and run a hand from her shoulder down her arm."
                                    the_person.SO_name "I'm so lucky you were going to wait for me like this. Now we have all night to spend with each other."
                                    the_person "Yes... Of course! Of course, I knew you would be late but I wanted to surprise you when you got home!"

                                    if hiding_under_bed:
                                        "You hear [the_person.title]'s [so_title] kissing her above you. Soon enough you feel them shift and the bed begins to rhythmically rise and sink ."
                                    else:
                                        "You see [the_person.title]'s [so_title] kiss her and climb on top of her. Soon enough he has his pants off and is between her legs."

                                    the_person.SO_name "Oh my god, you're so wet... Fuck, this is amazing!"
                                    the_person "Yeah... All for you sweetheart! You get me so turned on!"
                                    "You hear him grunt for a minute or two, then, almost as soon as he's started, he finishes. With a satisfied moan he rolls off of [the_person.title]."
                                    the_person.SO_name "Mmmm, that was great..."
                                    the_person "Yep. So great."
                                    the_person.SO_name "Could you get the lights? I think you've wiped me out."

                                else:
                                    "[the_person.title]'s [so_title] lies down in bed and sighs loudly."
                                    the_person.SO_name "Finally a chance to catch up on some sleep. Could you get the lights, I'm wiped."


                                the_person "Of course, sweetheart."
                                "[the_person.title] walks to the door and turns out the lights, then climbs back into bed."
                                if hiding_under_bed:
                                    "Within minutes you can hear him snoring loudly. [the_person.possessive_title] peeks under the bed and nods her head at the door."
                                    "You slide out from under the bed as quietly as you can, then sneak out of the bedroom and hurry to the front door."
                                else:
                                    "Within minutes you can hear him snoring loudly. [the_person.possessive_title] looks in your direction and nods her head at the door."
                                    "You crack the closet door open and step out as quietly as you can. You sneak out of the bedroom, then hurry to the front door."
                                $ clear_scene()
                                "As soon as you're outside you sprint to the sidewalk, then slow down and walk casually away."

                            "Run for it!":
                                $ done = True
                                mc.name "Fuck!"
                                "You don't waste any time, throwing your clothes on as quickly as possible. By the time you hear the front door open you're already rushing for the back yard."
                                $ random_num = renpy.random.randint(0,100)
                                if random_num < 20:
                                    # You get caught (but she's the one who has to deal with it).
                                    "[the_person.title] rushes to the door to intercept her [so_title]. She's trying to stall, but he doesn't stop. You're almost free and clear, when you hear him yell."
                                    the_person.SO_name "Hey! Who are you!?"
                                    "You don't stop. You slam the door and sprint away as quickly as your legs will carry you."
                                    $ morning_so_breakup_crisis = Action("Morning SO breakup", so_morning_breakup_requirement, "so_morning_breakup", args = the_person, requirement_args = the_person)
                                    $ mc.business.mandatory_morning_crises_list.append(morning_so_breakup_crisis)
                                else:
                                    "[the_person.title] rushes to the door to intercept her [so_title]. You hear her stalling for you as you open the side door and break into the night."

                            "Fuck her anyways!" if the_person.love + the_person.effective_sluttiness("vaginal_sex") >= leave_SO_love_calculation(the_person) + 60:
                                # You assert dominance and fuck her as he comes in. He breaks down as you claim her as your own.

                                mc.name "Well, I think I'm still going to bend you over and fuck you. He was going to find out eventually, right?"
                                the_person "What? Oh my god..."
                                "You grab [the_person.title] by her hips and roll her over, bending her over the side of the bed."
                                $ the_person.draw_person(position = "doggy")
                                the_person "I... I can't believe I'm actually doing this! Oh my god!"
                                if not the_person.outfit.vagina_available():
                                    "You strip her down as quickly as you can, not a minute to spare."
                                    while not the_person.outfit.vagina_available():
                                        $ the_item = the_person.outfit.remove_random_upper(top_layer_first = True, do_not_remove = True)
                                        $ the_person.draw_animated_removal(the_item)
                                        ""

                                    while not the_person.outfit.vagina_available():
                                        $ the_item = the_person.outfit.remove_random_any(top_layer_first = True, do_not_remove = True)
                                        $ the_person.draw_animated_removal(the_item)
                                        ""

                                menu:
                                    "Put on a condom.":
                                        "You pause for a second to put on a condom, spreading it over your hard cock before lining it up with her wet pussy."
                                        $ mc.condom = True

                                    "Fuck her bareback.":
                                        "You give her ass a smack and line your cock up with her wet pussy."

                                if the_person.effective_sluttiness("condomless_sex") < the_person.get_no_condom_threshold() and not mc.condom:
                                    the_person "Wait, you need a condom!"
                                    mc.name "No time!"

                                if not mc.condom:
                                    $ the_person.break_taboo("condomless_sex")
                                "You don't waste any time, ramming your cock home. [the_person.title] gasps as you bottom out inside her warm cunt, then start to pump back and forth."
                                "You hear [the_person.title]'s [so_title] come inside and close the door."
                                the_person.SO_name "I'm home! Good news, the client pushed the project back so I'll be out late less often!"
                                the_person "Oh god... I don't know if we should do this... Oh god."
                                "You place a hand on her shoulder and push her into the bed. She rolls her hips up against you, her body enjoying itself despite her moral dilemma."
                                mc.name "Shh, it's going to be okay. Just do what you know is right."
                                "She moans into the bed. You can hear her [so_title] approaching the bedroom and speed up."
                                "The bedroom door opens and [the_person.title] glances up at it."
                                the_person.SO_name "Are you in here sweetheart... Oh my..."
                                the_person "I'm so sorry, you weren't supposed to see me like this! Oh my god I'm so sorry!"
                                "Her [so_title] freezes in the door, eyes wide, transfixed by what he's seeing. [the_person.title] lifts herself up onto her arms."
                                the_person "I'm sorry, but he just makes me feel so good! His cock drives me mad and it's all I can think about!"
                                "You hold onto her hips and fuck her from behind. Her [so_title] just stares."
                                mc.name "You should go, there's nothing for you here."
                                the_person.SO_name "Honey... I..."
                                the_person "He's right, you don't need to be here to see this. I'm sorry!"
                                "You give her ass a hard smack. [the_person.title] lowers her head and moans."
                                the_person "All I want is his cock!"
                                "He gibbers weakly to himself and turns around, leaving the room. Shortly after you hear the engine of his car start up and he drives away."

                                call fuck_person(the_person, private = True, start_position = doggy, start_object = mc.location.get_object_with_name("bed"), skip_intro = True, skip_condom = True) from _call_fuck_person_101
                                $ the_report = _return
                                call transform_affair(the_person) from _call_transform_affair_1 #She's no longer with her husband, obviously.

                                $ the_person.change_obedience(5)
                                the_person "Oh my god, that was actually it. It's just me and you, nobody else in our way."
                                "She holds onto you tightly and rests her head on your chest."

                    elif random_num < 20 and not so_called:
                        #Her SO calls home. Depending on Love/Sluttiness she might want to stop, or keep going while talking to him.
                        $ so_called = True
                        "She smiles and moves to kiss you, when a happy little jingle fills the room."
                        the_person "That's my phone, I'm so sorry. One second."
                        $ the_person.draw_person(position = "doggy")
                        "She crawls over the bed and looks at her phone."
                        the_person "Fuck, it's my [so_title]. Just be quiet, okay?"
                        $ the_person.draw_person(position = "sitting")
                        "She sits on the edge of the bed and clears her throat, then answers the call."
                        the_person "Hey sweetheart! How are you doing?"
                        the_person "Good, that's good to hear. I'm doing fine, it's a little lonely here without you..."
                        menu:
                            "Stay quiet.":
                                #Time passes then you fuck her as normal.
                                "You lie back and get comfortable on [the_person.title]'s bed while she's talking. You wonder briefly if this is her side of the bed or her [so_title]'s."
                                the_person "Yeah? You don't say... Uh huh..."
                                "She leans over and runs her hand over your chest while she's talking."
                                the_person "Hmm? Sorry, I'm still listening. I'm just a little tired..."
                                the_person "You're probably right, I should get to bed. We'll talk again soon. Love you."
                                "She makes a kissing noise into her phone and hangs up."
                                mc.name "Do you think he knows?"
                                the_person "He doesn't have a clue. Now, where were we?"
                                call fuck_person(the_person, private = True) from _call_fuck_person_37 #Just normal start.
                                $ the_report = _return

                            "Grope her.":
                                #Basically an extended intro.
                                "You shuffle across [the_person.title]'s bed while she is talking and wrap your arms around her torso. She places a hand on your forearm and caresses it."
                                the_person "Yeah? You don't say... Uh huh... Mhmm."
                                if the_person.has_large_tits():
                                    "You cup her tits and squeeze them together, then slide your hands down her chest and stomach toward her waist."
                                else:
                                    "You run your hands over her tits, stomach, and then down toward her waist."
                                the_person "Ah... Oh, it's nothing sweetheart. I'm just lying down in bed and it feels nice to be off my feet."
                                "You kneel on the bed behind [the_person.possessive_title] and move your hands lower. You stroke her inner thighs and she opens her legs for you."
                                "Your hand finally slides over her pussy, gently brushing her clit, and she moves the phone away from her face to moan softly."
                                the_person "Hmm? Yes, I'm still here. Just yawning. I think it's time for bed."
                                "You slide a finger into her pussy and she holds her breath for a second."
                                the_person "Goodnight, I love you. Talk to you soon!"
                                $ the_person.change_obedience(1)
                                $ the_person.change_slut_core(the_person.get_opinion_score("cheating on men"))
                                $ the_person.change_arousal((mc.sex_skills["Foreplay"] + the_person.get_opinion_score("cheating on men") + the_person.get_opinion_score("being fingered")) * 5) #Arousal boost to start the encounter.
                                "She hangs up quickly and moans in relief."
                                the_person "Oh god, you're so bad!"
                                "[the_person.title] laughs and sits back into your arms."
                                the_person "Now come here and fuck me!"
                                call fuck_person(the_person, private = True) from _call_fuck_person_38
                                $ the_report = _return

                            "Make her suck your cock." if the_person.effective_sluttiness("sucking_cock") >= 50:
                                #Basically an extended intro
                                "You shuffle across the bed and stand up in front of [the_person.title]. She looks at you quizzically before noticing your hard cock at face level."
                                if the_person.has_taboo("sucking_cock"):
                                    the_person "Yeah? I... One second."
                                    "She looks up at you and shakes her head, pointing to her phone."
                                    "You take a small step forward, pressing the tip of your cock to her cheek."
                                    "[the_person.possessive_title] glares at you. You shrug and flex your dick in her face."
                                    "[the_person.title] rolls her eyes and holds up a finger, moving the phone back to her face."
                                    the_person "I'm back. Go ahead, tell me all about it."
                                    $ the_person.break_taboo("sucking_cock")
                                    "Then she moves it away again and leans forward, kissing the tip of your cock before sliding it past her lips."
                                else:
                                    the_person "Yeah? You don't say.... Uh huh?"
                                    "You brush her cheek with the back of your hand. She pivots her phone away from her face and leans forward, opening her mouth and kissing the tip of your cock."
                                    "She looks up at you from her sitting position while her tongue works around the tip in circles."
                                the_person "Mhmm? Mmmm. Hmmm. Uhmmmm."
                                "She mumbles responses to her [so_title] as she takes your cock deeper into her mouth. You can hear his voice on the other side of the phone, tinny and far away."
                                "With a soft, wet smack she slides back off and takes a breath."
                                the_person "Of course everything is fine. I'm just having something to eat before bed. That might be what you're hearing."
                                "She licks the bottom of your dick and winks at you."
                                the_person "Mhmm, it's delicious. I can't wait to get into bed though, it's been a long day."
                                the_person "I love you too, goodnight sweetheart."
                                "She slides you back into her mouth and holds her phone up to show you as she ends the call."
                                call fuck_person(the_person, private = True, start_position = blowjob, skip_intro = True) from _call_fuck_person_39
                                $ the_report = _return

                            "Fuck her while she's talking." if the_person.effective_sluttiness("vaginal_sex") >= 80:
                                #This is basically an extended intro
                                "You shuffle behind [the_person.title] and wrap your arms around her, grabbing a tit with one hand while the other slides down to her waist and caresses her pussy."
                                the_person "Yeah? You don't say... Uh huh?"
                                "With a little bit of pressure on her shoulders you guide [the_person.possessive_title] down onto her back."
                                $ the_person.draw_person(position = "missionary")
                                if the_person.outfit.vagina_available():
                                    "She spreads her legs as you climb on top of her, still talking to her [so_title] on her phone."

                                else:
                                    # You undress her so you can get to the point you can fuck her
                                    "You undress her while she's still on the phone with her [so_title]."
                                    while not the_person.outfit.vagina_available():
                                        $ the_item = the_person.outfit.remove_random_upper(top_layer_first = True, do_not_remove = True)
                                        $ the_person.draw_animated_removal(the_item)
                                        ""

                                    while not the_person.outfit.vagina_available():
                                        $ the_item = the_person.outfit.remove_random_any(top_layer_first = True, do_not_remove = True)
                                        $ the_person.draw_animated_removal(the_item)
                                        ""

                                    "Once her cute little pussy is available, she spreads her legs for you."
                                    $ the_person.update_outfit_taboos()

                                $ wanted_condom = False
                                if the_person.effective_sluttiness("condomless_sex") < the_person.get_no_condom_threshold():
                                    $ wanted_condom = True
                                    "She pauses and points towards your cock and mouthes \"C-O-N-D-O-M\""
                                else:
                                    "She reaches down with her free hand and strokes your hard cock, sliding the tip against her wet slit."

                                menu:
                                    "Wear a condom.":
                                        if not wanted_condom:
                                            "You pause for a moment to grab a condom from her bedstand. [the_person.possessive_title] rolls her eyes impatiently underneath you."
                                        else:
                                            "You pause for a moment to grab a condom from her bedstand and put it on."
                                        $ mc.condom = True


                                    "Fuck her bareback.":
                                        if wanted_condom:
                                            "You hold a finger up to your lips, reminding her to be quiet, and slide into her anyway."
                                            $ the_person.change_obedience(2 + the_person.get_opinion_score("bareback sex"))
                                            "Her eyes go wide as your hard dick slides into her raw pussy. She glares up at you, but has to snap her attention back to her [so_title]."
                                        else:
                                            "She closes her eyes and bites her lip as your hard dick slides into her raw pussy. She's barely able to keep her voice together while talking to her [so_title]."
                                        $ the_person.break_taboo("condomless_sex")

                                $ the_person.break_taboo("vaginal_sex")
                                the_person "Mmmhm? Oh sweetheart, it sounds like you're having a long hard day"
                                "She holds the phone to her chest and turns her head to the side as you start to pump into her. You hear the tinny voice of her [so_title] through the cellphone speaker."
                                "She moans softly, then lifts the phone back to her face."
                                the_person "Everything's more than fine here. I'm just really tired. I think I'm going to have to go to bed..."
                                the_person "... Okay... I love you too! Bye!"
                                "She finally hangs up and practically throws the phone away from her."
                                the_person "Oh fuck, you're crazy [the_person.mc_title]! What if we get caught?"
                                mc.name "We'll deal with that if it happens. Just relax and enjoy."

                                call fuck_person(the_person, private = True, start_position = missionary, start_object = mc.location.get_object_with_name("bed"), skip_intro = True, skip_condom = True) from _call_fuck_person_102
                                $ the_report = _return

                        #TODO: At this point run a check on her arousal.

                    # elif random_num < 30 and has_kid: #TODO: AND she has an adult kid who we have either met or can generate.
                    #     #TODO: This
                    #     #TODO: What happens if her daughter is around AND her husband comes home. Definitely write some "I'm fucking your whole family" stuff, even if it's going to be super rare.
                    #     pass

                    else:
                        call fuck_person(the_person) from _call_fuck_person_41
                        $ the_report = _return

                "Call it a night.":
                    mc.name "I have to get going. This was fun."
                    "You kiss [the_person.title], then get up and start collecting your clothes."
                    if girl_came:
                        the_person "Okay then. We need to do this again, you rocked my world [the_person.mc_title]."
                        "She sighs happily and lies down on her bed."

                    else:
                        the_person "Really? I didn't even get to cum yet..."
                        $ the_person.change_love(-1)
                        $ the_person.change_slut_temp(-1)
                    $ done = True
                    "You shrug and pull up your pants."



    #As soon as done is True we finish looping. This means each path should narrate it's own end of encounter stuff.
    #Generic stuff to make sure we don't keep showing anyone.
    $ the_person.clear_situational_slut("Date")
    $ clear_scene()
    return "Advance Time"


label blackmail_person(the_person):
    # Threaten the girl and claim you are going to reveal your relationship. Lowers love, but can be used to convert her into a "Slave" role.
    # TODO: Slave role, basically a girlfriend but with low love.
    return


label transform_affair(the_person):
    # If a girl leaves her SO for crisis reasons call this, which transforms her affair you had into a boyfriend-girlfriend relationship.
    if affair_role in the_person.special_role: # Technically we can use this to immediately jump to girlfrined with someone who is in a relationship as well.
        $ the_person.remove_role(affair_role)
    $ the_person.add_role(girlfriend_role)
    $ the_person.relationship = "Single" #Technically they aren't "single", but the MC has special roles for their girlfriend.
    $ the_person.SO_name = None #Clear the name of their ex so that it doesn't get used in
    #TODO: Maybe add a crisis that is created to introduce you to the idea that they're now broken up, or maybe handle that in an individual event.
    return

label so_morning_breakup(the_person): #Used as a mandatory event after a girls SO catches you and she informs you that she has broken up with him.
    "You get a call from [the_person.title]. You can only assume it is about last night. You pick up."
    mc.name "Hey [the_person.title]."
    the_person "Hi [the_person.mc_title]. I have some news."
    "She sounds tired but happy."
    $ so_title = SO_relationship_to_title(the_person.relationship)
    the_person "My [so_title] found out what was going on between us... He won't be getting between us anymore."
    call transform_affair(the_person) from _call_transform_affair_2
    mc.name "That's good news then. I love you [the_person.title]."
    the_person "I love you, too. I hope we can see each other soon!"
    mc.name "Me too, I'll be in touch."
    the_person "Talk to you soon."

    return

label caught_affair_cheating_label(the_other_girl, the_girlfriend):
    #TODO: She confronts you about being with another owman. You point out that she's ALSO with another guy. She asks you to tone it down a bit, she wants to be your main thing.
    # OR, if you lose enough Love, she ends the affair.

    if affair_role not in the_girlfriend.special_role:
        return #Something's changed, so don't worry about getting caught any more.

    "[the_girlfriend.title] walks up to you."
    $ the_girlfriend.draw_person(emotion = "angry")
    the_girlfriend "Hey, what the hell was that earlier?"
    mc.name "What was what?"
    the_girlfriend "I saw you with some other woman. Is there something going on between you two? Is it serious?"
    mc.name "That? We were just having some fun. Come on, you of all people have to understand that."
    $ the_girlfriend.change_love(-10)
    if the_girlfriend.love < 60:
        the_girlfriend "I thought we were a little more serious than that. Son of a bitch, I cared about you..."
        $ the_girlfriend.change_happiness(-10)
        $ the_girlfriend.draw_person(emotion = "sad")
        mc.name "It's not important, okay? Just let it go."
        the_girlfriend "I don't think I can... I thought I could do this with you, but I obviously care more about you than you care about me."
        $ the_girlfriend.remove_role(affair_role)
        the_girlfriend "Just... Let's just go back to being friends and pretend this never happened."
        "She shakes her head mournfully and walks away."
    else:
        the_girlfriend "I guess, but I thought we had something special. Could you at least cut back a little with other women?"
        mc.name "Alright, I'll do that if it makes you happy."
        $ the_girlfriend.change_obedience(3)
        the_girlfriend "Thank you. And come on, you know if you ever need a little fun you can just find me, right?"
        "She gives you a smile and a wink before walking away."

    $ clear_scene()
    return
