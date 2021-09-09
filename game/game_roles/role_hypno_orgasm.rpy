init -2 python:
    def hypno_orgasm_on_turn(the_person):
        the_person.event_triggers_dict["hypno_trigger_orgasm_requirement"] = False

    def hypno_trigger_orgasm_requirement(the_person):
        if the_person.event_triggers_dict.get("hypno_orgasmed_recently", False):
            return "She needs a break."
        else:
            return True


label hypno_trigger_orgasm(the_person, use_intro = True):
    if use_intro:
        mc.name "Hey [the_person.title]..."
        the_person "Yeah?"

    $ the_person.event_triggers_dict["hypno_orgasmed_recently"] = True
    $ the_word = the_person.event_triggers_dict.get("hypno_trigger_word","Cum")
    $ the_word.capitalize()
    mc.name "[the_word]."
    if the_person.arousal < 25:
        "[the_person.possessive_title] gasps, eyelids fluttering and thighs clamping together."
        "She doesn't say anything as the comletely unexpected orgasm shoots through her body."
        $ the_person.run_orgasm(trance_chance_modifier = -the_person.get_opinion_score("being in control")) #ie. negative opinions of being in control make her more likely to trance off of this.
        $ the_person.reset_arousal()
        "The moment passes quickly, and she lets out a long, unsteady breath."

    elif the_person.arousal < the_person.max_arousal:
        $ the_person.draw_person(emotion = "orgasm")
        "[the_person.possessive_title] gasps loudly, with a quiver obvious in both her voice and her legs."
        the_person "Oh god! Ah..."
        "Her knees wobble, and for a moment it seems like she might not be able to stay on her feet."
        $ the_person.run_orgasm(trance_chance_modifier = -the_person.get_opinion_score("being in control")) #ie. negative opinions of being in control make her more likely to trance off of this.
        $ the_person.reset_arousal()
        "She manages to recover, and after a few long seconds unclenches her legs and takes a steadying breath."
        $ the_person.draw_person()

    else:
        "The results are immediate. [the_person.possessive_title] spasms, bucking her hips and gasping for breath."
        the_person "Oh god! Ah! Ah!"
        "Her orgasm is so intense that her knees buckle and she starts to collapse to the ground."
        menu:
            "Catch her.":
                "You slide an arm around [the_person.title] and hold her up as she cums her brains out."
                "She clings to you, more instinct than conscious decision."
                $ the_person.run_orgasm(trance_chance_modifier = -the_person.get_opinion_score("being in control"))
                $ the_person.reset_arousal()
                $ the_person.change_love(2)
                "She gasps and moans into your ear for a long moment, but little by little her orgasm subsides."
                $ the_person.draw_person(emotion = "happy")
                "When she is in control of herself again she stands under her own power and looks at you, a dumb smile spreading across her face."

            "Let her fall.":
                "You step back and let her cliamx run its course."
                $ the_person.draw_person(position = "doggy", emotion = "orgasm")
                "[the_person.title] falls to the ground, barely catching herself at the last minute."
                "She ends up face down, hips bucking with each new climactic spasm. Her thighs twitch in sync with her hands free orgasm."
                $ the_person.run_orgasm(trance_chance_modifier = -the_person.get_opinion_score("being in control"))
                $ the_person.reset_arousal()
                $ the_person.change_slut(2)
                "She moans and writhes on the floor for a long moment, but little by little her orgasm subsides and she gains control of herself again."
                $ the_person.draw_person(position = "missionary", emotion = "happy")
                "[the_person.possessive_title] rolls over and looks up at you, a dumb smile spreading across her face."
                "When she realises where she is she pulls herself up off of the floor, looking more than a little embarrassed."
                $ the_person.draw_person(emotion = "happy")

    the_person "Sorry, did you say something?"
    mc.name "Never mind, it wasn't important."
    return


label hypno_trigger_online(the_person):
    $ the_person.event_triggers_dict["hypno_orgasmed_recently"] = True
    $ the_word = the_person.event_triggers_dict.get("hypno_trigger_word","Cum")
    $ the_word.capitalize()

    mc.name "Hey [the_person.title], you around?"
    if mc.location.has_person(the_person):
        "[the_person.possessive_title] glances at her phone, then looks up at you and laughs."
        $ mc.end_text_convo()
        $ the_person.draw_person()
        the_person "I'm right here, what's up?"
        mc.name "[the_word]."
        call hypno_trigger_orgasm(the_person, use_intro = False)
        return

    "There's a short pause before [the_person.possessive_title] responds."
    the_person "Yeah, what's up?"
    mc.name "[the_word]."
    $ the_person.run_orgasm(trance_chance_modifier = -the_person.get_opinion_score("being in control"), show_dialogue = False, add_to_log = False) #ie. negative opinions of being in control make her more likely to trance off of this.
    $ the_person.reset_arousal()
    $ mc.change_locked_clarity(10)
    "[the_person.title] isn't around, so you're forced to use your imagination of her cumming her brains out the moment she checks her phone."
    if the_person.sluttiness < 30:
        "After a few moments you get your confirmation."
        the_person "What the hell! How did you do that?!"
    elif the_person.sluttiness < 60:
        "After a few moments you get your confirmation."
        the_person "Oh my god, you can do that over your phone?"
    else:
        "After a few moments you get your confirmation."
        the_person "Fuukkk, nww I cnnt loook at my phone wiiithout cumming!"
        "She's clearly having a hard time just writing out her message."
    "You chuckle to yourself and don't say anything more."
    return
