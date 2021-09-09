init -2 python:
    def breeder_fuck_requirement(the_person):
        if persistent.pregnancy_pref == 0:
            return False
        elif the_person.event_triggers_dict.get("preg_knows", False):
            return False
        else:
            return True

label breeder_fuck(the_person):
    mc.name "I've got some spare time [the_person.title], want to get knocked up?"
    $ wants_breeding = True
    if the_person.effective_sluttiness() >= the_person.get_no_condom_threshold(): #Slutty enough that she'd fuck you raw any time, no big deal just comment on it
        if the_person.fertility_percent >= 70: #Crazy high fertility
            the_person "Oh [the_person.mc_title], how did you know just what I was thinking?"
            the_person "It might sound crazy, but my entire body just feels ready for breeding today!"
            the_person "I'll probably be knocked up the second you cum inside me, but you should still try and do it a few times, okay?"
            $ mc.change_locked_clarity(30)
            the_person "Really fill me up with cum so we can be sure!"

        elif the_person.fertility_percent >= 20: #High fertility. She's "Feeling ready".
            the_person "Of course I do [the_person.mc_title]!"
            $ mc.change_locked_clarity(20)
            the_person "I've got a good feeling about today! Make sure to cum nice and deep, I want the best chances of getting pregnant!"

        elif the_person.days_from_ideal_fertility() <= 3:
            the_person "Of course I do [the_person.mc_title]!"
            the_person "The key to breeding is consistency. Each time you cum inside me is another chance for me to get knocked up."
            $ mc.change_locked_clarity(30)
            the_person "It's the right time of the month too, so keep me filled up and I'll be pregnant in no time!"

        else: #Not likely to work, but she'll give it a try anyways because it's fun. I mean, because it's necessary...
            the_person "She pauses to think for a moment, then shrugs and nods."
            the_person "It's not the right time of the month, but there's no harm in trying!"
            $ mc.change_locked_clarity(10)
            the_person "It's a fun time either way, and if I get knocked up then even better!"

    else:  #Ie. she's not slutty enough to fuck you without a condom usually. Probably comes up because of massive fertility
        if the_person.days_from_ideal_fertility() <= 3: #ie. one week out of the month. She's fertile enough that she wants to try.
            "She thinks for a moment, then nods."
            the_person "It's the right time of the month for me, we should try as much as possible."
            the_person "Well then, let's get to it!"
        else:
            "She thinks for a moment, then shakes her head."
            the_person "It's not the right time of the month for me. We need to wait until it's likely to work, okay?"
            $ wants_breeding = False
            menu:
                "Fuck her anyways." if the_person.obedience >= 140:
                    mc.name "You want to get you knocked up [the_person.title], and every load I put inside of you is one more chance for that to happen."
                    $ mc.change_locked_clarity(10)
                    "You reach around her and grab her ass, squeezing it hard. She moans, but doesn't try to pull away"
                    mc.name "So I need to get inside of you and pump you full of cum as often as possible. Even if it's not likely to knock you up."
                    the_person "I suppose that makes sense... Okay, you're right, as usual."
                    $ wants_breeding = True

                "Fuck her anyways.\nRequires: 140 Obedience" if the_person.obedience < 140:
                    pass

                "Try some other time.":
                    mc.name "We'll have to try some other time then."
                    "She nods happily."
                    the_person "There's nothing I want more, [the_person.mc_title], than to get pregnant and be a mother all over again."

    if wants_breeding:
        # Option to give her some serum (ie. ability to give her some fertility stuff right away)."
        if mc.inventory.get_any_serum_count():
            menu:
                "Give her some serum.":
                    mc.name "Before we get started, I have something for you."
                    the_person "You do? What does it do?"
                    mc.name "It'll help you get pregnant. You want the best chance possible, right?"
                    "She nods eagerly and and waits for you to hand something over."
                    call give_serum(the_person)
                    if _return is not None:
                        "[the_person.title] takes the vial of serum and drinks it down as quickly as she can."
                    else:
                        mc.name "I must have forgotten to pick some up."
                        the_person "Bring it for me next time. Until then..."

                "Don't give her anything.":
                    pass

        $ start_object = mc.location.get_object_with_trait("Lay") #In theory there is always the floor.
        if not start_object:
            "[the_person.possessive_title] looks around, then frowns."
            the_person "We're going to have to wait a bit, there's nowhere for you to fuck me here..."
            return

        $ should_be_private = True #TODO: All of these calculations are pretty common, we should group them up and put them somewhere else (this, grope, command)
        if mc.location.get_person_count() > 1: #there are other people here.
            $ extra_people_count = mc.location.get_person_count() - 1
            $ obedience_required = 130 - (10*the_person.get_opinion_score("public sex"))
            if the_person.get_opinion_score("cheating on men") < 1 and the_person.relationship != "Single" and not the_person.has_role(affair_role):
                $ obedience_required += 10 + -10*the_person.get_opinion_score("cheating on men")
            $ the_person.discover_opinion("public sex")
            if the_person.effective_sluttiness("touching_body") < 40 or the_person.get_opinion_score("public sex") < 0:
                # She's nervous about it and asks to go somewhere private.
                the_person "Before we get down to it we should find somewhere we don't be distrubed..."
                "[the_person.possessive_title] nods her head at the people nearby."
                menu:
                    "Find somewhere quiet.\n{size=22}No interruptions{/size}":
                        mc.name "Alright, come with me."
                        "You take [the_person.title] by her wrist and lead her away."
                        #TODO: have each location have a unique "find someplace quiet" descriptor with a default fallback option
                        "After a couple of minutes searching you find a quiet space with just the two of you."
                        "Finally alone, she starts to strip down for you."

                    "Stay where you are.\n{size=22}[extra_people_count] watching{/size}" if the_person.obedience >= obedience_required:
                        $ should_be_private = False
                        mc.name "No, we're going to fuck right here."
                        the_person "But they're going to be watching..."
                        mc.name "That's right, they're going to watch me knock you up."
                        $ the_person.change_happiness(5*the_person.get_opinion_score("public sex"))
                        "[the_person.possessive_title]'s anxiety about the situation is obvious, but she starts to strip down anyways."

                    "Say where you are.\nRequires: [obedience_required] Obedience (disabled)" if the_person.obedience < obedience_required:
                        pass



            else:
                # She doesn't care, but you can find someplace private.
                "[the_person.possessive_title] either doesn't notice or doesn't care, but there are other people around."
                menu:
                    "Find somewhere quiet.\n{size=22}No interruptions{/size}":
                        mc.name "Come with me, I don't like being interrupted when I'm trying to breed a slut."
                        "You take [the_person.title] by the wrist and lead her away. She follows eagerly."
                        "After searching for a couple of minutes you find a quiet space with just the two of you."
                        "Finally alone, she starts to strip down."

                    "Stay where you are.\n{size=22}[extra_people_count] watching{/size}":
                        $ should_be_private = False


        $ strip_list = the_person.outfit.get_full_strip_list()
        $ generalised_strip_description(the_person, strip_list)
        $ the_person.draw_person(position = "missionary")

        "[the_person.possessive_title] lies down on her [start_object.name] and spreads her legs, waiting for you."
        menu:
            "Fuck her.":
                "You pull down your pants and get your hard cock out. You climb onto [the_person.title]'s [start_object.name] and fit your hips between her legs."
                the_person "Get inside me [the_person.mc_title], come fuck your mother."
                "She reaches down and holds onto your shaft, rubbing the tip of your cock against her pussy lips. She strokes your cheek lovingly with her other hand."
                "You push forward, sinking your dick inside of her. Her eyes flutter and she gasps softly."
                the_person "Oh [the_person.title]..."
                call fuck_person(the_person, private = should_be_private, start_position = missionary, start_object = start_object, skip_intro = True, skip_condom = True)
                $ sex_record = _return

            "Have her suck you off first.":
                mc.name "Not so fast [the_person.title], I need you to get me ready first."
                "You pull your cock out and present it to her."
                mc.name "Get me hard and wet, I'll be sure to slide into you before I cum."
                the_person "Of course [the_person.mc_title], right away!"
                $ the_person.draw_person(position = "blowjob")
                $ mc.change_locked_clarity(20)
                "She swings her legs off of the [start_object.name] and gets onto her knees in front of you. She holds onto your shaft with one hand and slips your tip into her mouth eagerly."
                call fuck_person(the_person, private = should_be_private, start_position = blowjob, skip_intro = True, skip_condom = True)
                $ sex_record = _return


        if sex_record.get("creampies", 0) >= 3:
            "[the_person.title] puts a hand between her legs, gasping as it touches the hot cum still rushing out of her overflowing pussy."
            the_person "Oh god, there's so much! I want it all inside me but there's just too much!"
            $ mc.change_locked_clarity(50)
            "She quivers gently with pleasure, and even that small movement sends a pulse of your cum gushing out of her and onto the [start_object.name]."
            $ the_person.change_slut(1 + 3*the_person.get_opinion_score("creampies"), 120)
            $ the_person.change_happiness(15 + 5*the_person.get_opinion_score("creampies"))
        elif sex_record.get("creampies", 0) == 2:
            "[the_person.title] puts a hand between her legs, gasping when it touches her cum covered cunt."
            the_person "Oh, there's so much! You did such a good job [the_person.mc_title]."
            $ mc.change_locked_clarity(40)
            "She slips her middle finger inside her pussy and holds it there, keeping all of your seed trapped inside."
            $ the_person.change_slut(1 + 2*the_person.get_opinion_score("creampies"), 100)
            $ the_person.change_happiness(10 + 5*the_person.get_opinion_score("creampies"))
        elif sex_record.get("creampies", 0) == 1:
            $ mc.change_locked_clarity(20)
            "[the_person.title] puts a hand between her legs, petting her slit with her middle finger."
            the_person "Mmm, I can feel it deep inside me. Now I just have to hope I'm lucky."
            $ the_person.change_slut(1 + 1*the_person.get_opinion_score("creampies"), 90)
            $ the_person.change_happiness(5 + 5*the_person.get_opinion_score("creampies"))
        elif sex_record.get("guy orgasms", 0) > 0: #You came, but not inside her. She's pissed."
            the_person "You're not... done, are you?"
            mc.name "Sorry [the_person.title], but I just can't keep going."
            "[the_person.possessive_title] scowls at you."
            the_person "[the_person.mc_title], you said you were going to cum inside of me. That was our deal."
            the_person "If you were tired and couldn't finish, or even if you came inside me after, that would have been fine."
            the_person "But this... This just feels selfish."
            mc.name "I said I was sorry, I..."
            "She waves a hand and cuts you off."
            the_person "Forget it, just... Let's get dressed."
            $ the_person.change_happiness(-10)
            $ the_person.change_love(-2)
            $ the_person.apply_outfit()
            $ the_person.draw_person()
        else: #You couldn't cum. She's disappointed, but not angry
            the_person "Wait, you're not... finished already, are you?"
            mc.name "Sorry [the_person.title], but I just can't keep going."
            "She sighs and frowns. She doesn't seem angry, but she does seem disappointed."
            $ the_person.change_happiness(-10)
            the_person "Well, I suppose there's nothing you can do about it now... Try and save your energy for next time, okay?"
            mc.name "Okay [the_person.title], I will."

    else:
        pass
    return
