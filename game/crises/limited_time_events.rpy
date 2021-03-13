## Holds definitions for limited time events/crises.
# These are a special class of event used for random events in the on_talk or on_enter list of a girl.
# If an action has a valid requirment it can be assigned to a person in the matching list, and after n number of turns it will be removed, or removed when it's triggered.

###################################
# Limited time events that exist: #
###################################

#######################
### On_talk events: ###
#######################
# Ask for a title change/mc title change

########################
### On_enter events: ###
#######################
# Walk in on sister masturbating
# Walk in on mother masturbating
# Night time walk-in
# Mom Nude Housework
# Breeding Mom
# Mom work report

init -1 python:
    limited_time_event_pool = [] #Drawn from to form the on_talk and on_enter events generated for people. Given in the form [event, weight, class], where class is "on_talk" or "on_enter"

    # Definitions for the events
    def ask_new_title_requirement(the_person):
        if the_person.obedience > 130: #If she has higher obedience she ONLY lets you change her title.
            return False
        return True

    def sister_walk_in_requirement(the_person):
        if not the_person.has_role(sister_role):
            return False
        elif the_person not in the_person.home.people:
            return False
        elif lily_bedroom.get_person_count() > 1:
            return False
        return True

    def nude_walk_in_requirement(the_person):
        if not (the_person.has_role(sister_role) or the_person.has_role(mother_role)):
            return False
        elif the_person not in the_person.home.people:
            return False
        elif the_person.home.get_person_count() > 1:
            return False
        return True

    def mom_house_work_nude_requirement(the_person):
        if not the_person.has_role(mother_role):
            return False
        elif the_person not in kitchen.people:
            return False
        elif the_person.effective_sluttiness() < (20 - the_person.get_opinion_score("not wearing anything")*3): #TODO: OR require her to work nude as one of your weekly requests
            return False
        return True

    def mom_breeding_requirement(the_person):
        if not the_person.has_role(mother_role):
            return False
        elif persistent.pregnancy_pref == 0:
            return False
        elif the_person not in mom_bedroom.people:
            return False
        elif mom_bedroom.get_person_count() > 1:
            return False
        elif the_person.effective_sluttiness() < (90 - (10*the_person.get_opinion_score("creampies"))):
            return False
        elif the_person.love < (75 - (10*the_person.get_opinion_score("creampies"))):
            return False
        return True

    def work_walk_in_requirement(the_person): #AKA she has to work for you, be at work, and be turned on
        if not the_person.has_role(employee_role):
            return False
        elif not person_at_work(the_person):
            return False
        elif the_person not in mc.business.get_employee_list():
            return False
        elif the_person.effective_sluttiness() < 20 - (5*the_person.get_opinion_score("masturbating")):
            return False
        return True

    #TODO: We really need to be able to assign LTE's to roles instead of being general events
    def sleeping_walk_in_requirement(the_person):
        if not (the_person.has_role(sister_role) or the_person.has_role(mother_role)): #If it was LTE based we could avoid this. Basically any global reference should be by role.
            return False
        elif not (time_of_day == 0 or time_of_day == 4): #ie. early morning (sleeping in) or late at night (early bed time)
            return False
        elif the_person is mom and time_of_day == 0 and day%7 == 5:
            return False #Don't want to trigger at the same time as the morning offer.
        elif not the_person.home.has_person(the_person):
            return False
        elif the_person.home.get_person_count() > 1: #Nobody else in the room.
            return False
        return True

    def mom_work_slutty_requirement(the_person):
        if not the_person.has_role(mother_role):
            return False
        elif mc.business.is_weekend():
            return False
        elif time_of_day == 1 or time_of_day >= 4:
            return False
        elif the_person.event_triggers_dict.get("mom_office_slutty_level",0) < 1:
            return False
        else:
            return True

    def new_insta_account_requirement(the_person):
        if the_person.has_role(mother_role) or the_person.has_role(sister_role):
            return False #We want explicit control of when these characters generate their Insta accounts
        elif the_person.has_role(instapic_role):
            return False
        elif renpy.random.randint(0,100) >= the_person.personality.insta_chance + 5*(the_person.get_opinion_score("showing her tits") + the_person.get_opinion_score("showing her ass")):
            return False #Personality type and Opinions has a large impact on chance to generate a new profile.
        elif the_person.love < 10: #Girls who don't like you won't tell you they've made a profile (and are assumed to either have one or not depending on their starting generation)
            return False
        else:
            return True

    def new_dikdok_account_requirement(the_person):
        if the_person.has_role(mother_role) or the_person.has_role(sister_role):
            return False #We want explicit control of when these characters generate their Insta accounts
        elif the_person.has_role(dikdok_role):
            return False
        elif renpy.random.randint(0,100) >= the_person.personality.dikdok_chance + 5*(the_person.get_opinion_score("showing her tits") + the_person.get_opinion_score("showing her ass")):
            return False #Personality type and Opinions has a large impact on chance to generate a new profile.
        elif the_person.love < 10: #Girls who don't like you won't tell you they've made a profile (and are assumed to either have one or not depending on their starting generation)
            return False
        else:
            return True

    def new_onlyfans_account_requirement(the_person):
        if the_person.has_role(mother_role) or the_person.has_role(sister_role):
            return False #We want explicit control of when these characters generate their Insta accounts
        elif the_person.has_role(onlyfans_role):
            return False
        elif renpy.random.randint(0,100) >= -5 + 10*(the_person.get_opinion_score("showing her tits") + the_person.get_opinion_score("showing her ass") + the_person.get_opinion_score("public sex")):
            return False #Personality type and Opinions has a large impact on chance to generate a new profile.
        elif the_person.effective_sluttiness() < 50 + 10*(the_person.get_opinion_score("showing her tits") + the_person.get_opinion_score("showing her ass") + the_person.get_opinion_score("public sex")):
            return False
        elif the_person.love < 10: #Girls who don't like you won't tell you they've made a profile (and are assumed to either have one or not depending on their starting generation)
            return False
        else:
            return True
        return



    ### ON TALK EVENTS ###
    ask_new_title_action = Action("Ask new title", ask_new_title_requirement, "ask_new_title_label", event_duration = 2)

    work_walk_in = Action("Employee walk in", work_walk_in_requirement, "work_walk_in_label", event_duration = 4)

    mom_work_slutty_event = Action("Mom work slutty", mom_work_slutty_requirement, "mom_work_slutty_report", event_duration = 2)


    limited_time_event_pool.append([ask_new_title_action,8,"on_talk"])
    limited_time_event_pool.append([work_walk_in,4,"on_talk"])
    limited_time_event_pool.append([mom_work_slutty_event,8,"on_talk"])
    #TODO: Add some girlfriend/paramour events where they ask right away if you want to fuck

    ### ON ENTER EVENTS ###
    sister_walk_in = Action("Sister walk in", sister_walk_in_requirement, "sister_walk_in_label", event_duration = 5)
    nude_walk_in = Action("Nude walk in", nude_walk_in_requirement, "nude_walk_in_label", event_duration = 5)
    mom_house_work_nude = Action("Mom nude house work", mom_house_work_nude_requirement, "mom_house_work_nude_label", event_duration = 5)
    breeding_mom = Action("Mom breeding", mom_breeding_requirement, "breeding_mom_label", event_duration = 5)
    sleeping_walk_in = Action("Sleeping walk in", sleeping_walk_in_requirement, "sleeping_walk_in_label", event_duration = 1)


    limited_time_event_pool.append([sister_walk_in,4,"on_enter"])
    limited_time_event_pool.append([nude_walk_in,4,"on_enter"])
    limited_time_event_pool.append([mom_house_work_nude,4,"on_enter"])
    limited_time_event_pool.append([breeding_mom,4,"on_enter"])
    limited_time_event_pool.append([sleeping_walk_in,8,"on_enter"])



label ask_new_title_label(the_person):
    if renpy.random.randint(0,100) < 50:
        call person_new_title(the_person) from _call_person_new_title
    else:
        call person_new_mc_title(the_person) from _call_person_new_mc_title

    call talk_person(the_person) from _call_talk_person_10
    return


label sister_walk_in_label(the_person):
    if the_person.effective_sluttiness() < 10:
        "You try to open the door to [the_person.title]'s room, but find it locked."
        $ the_person.change_arousal(30, add_to_log = False)
        the_person "Ah! One... One second!"
        "You hear scrambling on the other side of the door, then the lock clicks and [the_person.possessive_title] pokes her head out."
        $ the_person.draw_person()
        the_person "Oh... [the_person.mc_title], it's only you. Come on in, what's up?"
        "Her face is flush and her breathing rapid. You wonder for a moment what you almost caught her doing as she leans nonchalantly against the door frame."
        $ clear_scene()
        return

    elif the_person.effective_sluttiness() < 25:
        "You try to open the door to [the_person.title]'s room, but find it locked."
        $ the_person.change_arousal(40, add_to_log = False)
        the_person "Ah! One... One second!"
        "You hear scrambling on the other side of the door, then the lock clicks and [the_person.possessive_title] pokes her head out."
        $ the_person.draw_person()
        the_person "[the_person.mc_title], it's you. What's up?"
        "Her face is flush and her breathing rapid. Her attempt at being nonchalant is ruined when a loud moan comes from her laptop, sitting on her bed."
        "Laptop" "Ah! Fuck me! Ah! Yes!"
        the_person "Oh my god, no!"
        "She sprints to her bed, opening up her laptop and turning it off as quickly as possible."
        mc.name "Am I interupting?"
        "[the_person.possessive_title] spins around, beet red, and stammers for a moment."
        the_person "I... I don't... Umm... I think my laptop has a virus, all these crazy popups!"
        mc.name "Mmmhm? Do you want me to take a look?"
        the_person "No, no that's okay. It's probably fine."
        menu:
            "Encourage her.":
                mc.name "You know there's nothing wrong with watching porn, right?"
                the_person "I wasn't! I..."
                mc.name "Of course not, but even if you were there's nothing wrong with that. It's a natural thing, everyone does it. I certainly do."
                $ the_person.change_slut_temp(3)
                $ the_person.change_happiness(5)
                the_person "Really? Ew, I don't need to know about that."
                "She still seems more interested than her words would suggest."

            "Threaten to tell [mom.possessive_title].":
                mc.name "I can let [mom.title] know, maybe she can take it somewhere to get it fixed."
                the_person "No! I mean, you can't tell Mom. Nothing's wrong with it, okay?"
                mc.name "So you were..."
                $ the_person.change_obedience(2)
                $ the_person.change_love(-1)
                the_person "I was watching porn, okay? Can you not make such a big deal about it?"
                mc.name "You should have just told me that right away, there's nothing wrong with watching some porn and getting off."
                the_person "I wasn't getting off, I was just..."
                mc.name "Watching it for the acting?"
                the_person "Ugh, shut up. Whatever, the moment's kind of ruined, what do you need?"

    else:
        $ item = the_person.outfit.remove_random_lower(top_layer_first = True, do_not_remove = True)
        while not the_person.outfit.vagina_available() and item is not None:
            $ the_person.outfit.remove_clothing(item)
            $ item = the_person.outfit.remove_random_lower(top_layer_first = True, do_not_remove = True) #Remove all of her lower items first, which are most likely blocking her pussy
            if item is None and not the_person.outfit.vagina_available(): #If we still don't have access we move onto her top, which may be a dress and blocking things.
                $ item = the_person.outfit.remove_random_any(top_layer_first = True, do_not_remove = True)

        $ the_person.draw_person(position = "missionary")
        $ the_person.change_arousal(40, add_to_log = False)
        "You open the door to [the_person.title]'s room and find her sitting up in bed with her laptop beside her, legs splayed open and fingers deep in her own pussy."
        "Her eyes are closed, and because of her headphones it doesn't seem like she's noticed you come in. She lets out the softest moan."
        the_person "Mmmph..."
        menu:
            "Offer to help.":
                "You step into the room and close the door."
                mc.name "Having a good time?"
                if the_person.effective_sluttiness("touching_vagina") < 35:
                    the_person "Hmm? Oh my god!"
                    "She opens her eyes slowly, before yelling in suprise and grabbing desperately for her blankets in an attempt to salvage her decency."
                    the_person "Oh my god, [the_person.mc_title]! What are you... I... Get out of here!"
                    mc.name "Don't be so dramatic [the_person.title], I just want to know if you want some help."
                    the_person "Help?! Ew, oh god!"
                    "She grabs a pillow and throws it at you."
                    the_person "Get out! Get out!"
                    "You retreat from the room before [mom.title] hears what's happening and comes to investigate."
                    $ the_person.apply_outfit(the_person.planned_outfit)
                    #$ the_person.outfit = the_person.planned_outfit.get_copy() changed v0.24.1

                else:
                    the_person "Hmm?"
                    if the_person.effective_sluttiness("touching_vagina") < 55 or the_person.has_taboo(["touching_vagina","bare_pussy"]):
                        "She opens her eyes slowly, then gasps in suprise. She grabs a pillow and uses it to cover herself."
                        the_person "Oh my god, [the_person.mc_title]! What are you doing, I'm..."
                        "She blushes a little."
                        the_person "Well, you know."
                        mc.name "I just wanted to know if you need a hand."
                        the_person "I... We really shouldn't..."
                        "Despite her verbal hesitations she slides the pillow out of the way and gives you \"fuck me\" eyes."

                    else:
                        "She opens her eyes slowly."
                        the_person "Oh, it's you [the_person.mc_title]. What do you need? I was just relaxing a little."
                        "She rubs her pussy gently while she talks to you, stroking the wet pink slit with a finger."
                        mc.name "I don't need anything, but it looks like you might. Do you need a hand with that?"
                        "She nods and gives you \"fuck me\" eyes."
                    $ the_person.update_outfit_taboos()


                    "You slide onto the bed and run your fingers along [the_person.title]'s body, moving down towards her already-wet pussy."
                    $ the_person.break_taboo("touching_vagina")
                    "When you first touch her she gasps and quivers, and when you slide your middle finger into her pussy she moans."
                    "She slides her body against you, and when you pull her off the bed she doesn't argue."
                    "You stand behind her, one hand grasping a breast and the other gently pumping a finger in and out of her."
                    call fuck_person(the_person, start_position = standing_finger, private = True) from _call_fuck_person_2
                    $ the_record = _return
                    if the_record.get("girl orgasms", 0) > 0:
                        "[the_person.possessive_title] falls back on her bed and sighs happily."
                        $ the_person.change_love(2)
                        $ the_person.change_obedience(1)
                        the_person "Thank you [the_person.mc_title], that's exactly what I wanted. Ahh..."
                        "She rolls over and gathers up a collection of pink blankets on top of herself, quickly falling asleep."
                        "You step out of the room to give her some time to recover."
                        $ mc.change_location(hall)

                    elif the_record.get("guy orgasms", 0) > 0:
                        the_person "So... Is that it?"
                        mc.name "What do you mean?"
                        $ the_person.change_love(-2)
                        $ the_person.change_obedience(-2)
                        "She scoffs and falls back onto her bed, pulling her blankets over herself."
                        the_person "Nothing, I'm glad you enjoyed yourself at least. Get out of here so I can get off."
                        $ mc.change_location(hall)

                    else:
                        the_person "So... are you finished?"
                        mc.name "Heh, yeah. Sorry [the_person.mc_title], I'm just not feeling it."
                        "She frowns, but nods. She gathers her blankets over herself."
                        $ the_person.change_obedience(-2)


            "Just watch.":
                "You step into the room and close the door to [the_person.title]'s room."
                "You lean on the doorframe and watch her fingering herself."
                $ mc.change_arousal(5)
                the_person "Ah... Mmmm."
                "She opens her eyes and glances at her laptop, then finally notices you."
                if the_person.effective_sluttiness("bare_pussy") < (40 - (the_person.obedience-100)): #If she's not slutty or obedient she yells at you to get out
                    the_person "Oh my god, [the_person.mc_title]! What are you... I... Get out of here!"
                    mc.name "Don't be so dramatic [the_person.title], just keep going."
                    the_person "What?! Ew, how long have you been there? Oh god!"
                    "She grabs a pillow and throws it at you."
                    the_person "Get out! Get out!"
                    "You retreat from the room before [mom.title] hears what's happening and comes to investigate."
                    $ the_person.apply_outfit(the_person.planned_outfit)
                    #$ the_person.outfit = the_person.planned_outfit.get_copy() changd v0.24.1

                else: #Otherwise she lets you stay long enough for you to tell her to keep going.
                    the_person "Oh my god, [the_person.mc_title]! What are you doing, I'm..."
                    "She blushes a little."
                    the_person "Well, you know."

                    mc.name "Don't worry about me, just keep going."

                    if the_person.effective_sluttiness("bare_pussy") < 60: #She's a little unsure about it, but goes for it
                        the_person "Really? I... I mean, do you really want to see me like this?"
                        "[the_person.possessive_title] relaxes a little, her hand unconciously drifting back between her legs."
                        mc.name "I think it's hot, keep touching yourself for me."
                        "She shrugs and nods, spreading her legs and sliding a finger along her wet slit."
                        $ the_person.change_obedience(2)
                    else:
                        the_person "If you want..."
                        "She smiles and spreads her legs, sliding a finger along her wet slit."

                    $ the_person.update_outfit_taboos()

                    "[the_person.possessive_title] starts to finger herself again, slowly moving a pair of fingers in and out, in and out."
                    "Soon she's almost forgotten about you standing and watching at her door. She arches her back and turns her head, moaning into a pillow."
                    "She starts to rock her hips against her own hand as her fingering becomes increasingly intense."
                    "Even as she starts to climax she keeps her legs wide open, giving you a clear view of her dripping wet cunt."
                    "Her body spasms as she cums, fingers buried deep inside of herself. She holds them there for a long moment, eyes shut tight."
                    "Finally she relaxes and pulls her fingers out, trailing her own juices behind them. She glances up at you and smiles weakly."
                    the_person "Ah... That was good."
                    $ the_person.change_slut_temp(2+the_person.get_opinion_score("masturbating"))
                    $ the_person.discover_opinion("masturbating")

            "Leave her alone.":
                $ clear_scene()
                "You take a quick step back and, as quietly as you can manage, close her door."
                $ mc.change_location(hall)
                $ the_person.apply_outfit(the_person.planned_outfit)
                #$ the_person.outfit = the_person.planned_outfit.get_copy() changed v0.24.1



    $ clear_scene()
    return


label nude_walk_in_label(the_person):
    if renpy.random.randint(0,100) < 50:
        $ the_person.apply_outfit(Outfit("Nude"))
        #$ the_person.outfit = Outfit("Nude") changed v0.24.1
        $ the_person.draw_person()
        "You open the door to [the_person.possessive_title]'s room and see her standing in front of her mirror, completely nude."
        if the_person.effective_sluttiness(["bare_tits", "bare_pussy"]) < (50 - (the_person.get_opinion_score("not wearing anything")*10)):
            # She asks you to step out for a moment.
            if the_person.has_large_tits():
                "She turns and tries to cover herself with her hands, but her big tits are still easily on display."
            else:
                "She turns and tries to cover herself with her hands."
            the_person "Just... Just a minute, I was getting changed!"
            $ clear_scene()
            "[the_person.title] shoos you out of the room. You can hear her getting dressed on the other side."
            $ the_person.apply_outfit(the_person.planned_outfit)
            #$ the_person.outfit = the_person.planned_outfit.get_copy() changed v0.24.1
            $ the_person.draw_person()
            "Soon enough she opens the door and invites you in."
            $ the_person.change_slut_temp(1+the_person.get_opinion_score("not wearing anything"))
            $ the_person.discover_opinion("not wearing anything")
            the_person "Sorry about that, I always forget to lock the door."
        else:
            # She doesn't mind and invites you in to talk, while being nude
            if the_person.update_outfit_taboos():
                "She turns around and waves you in, then seems to realise that she's naked and tries to cover herself with her hands."
                the_person "Oh, I'm not dressed! If you want I can put something on."
                mc.name "Don't worry about it. We're family, we should be comfortable around each other."
                "She smiles and nods, moving her hands away from her tits and pussy."
            else:
                "She turns to you and smiles, seemingly oblivious to her own nudity."
                the_person "Come on in! Did you need something?"


    else:
        # She's in her underwear
        $ the_person.apply_outfit(the_person.wardrobe.get_random_appropriate_underwear(the_person.effective_sluttiness(), guarantee_output = True))
        $ the_person.draw_person()
        "You open the door to [the_person.possessive_title]'s room and find her sitting on her bed, wearing nothing but her underwear."
        if the_person.effective_sluttiness("underwear_nudity") < (30 - (the_person.get_opinion_score("not wearing anything")*10)):
            the_person "Oh! One second, I'm not dressed!"
            $ clear_scene()
            "She hurries to the door and closes it in your face, locking it quickly. You can hear her quickly getting dressed on the other side."
            $ the_person.apply_outfit(the_person.planned_outfit)
            $ the_person.draw_person()
            "When she opens the door she's fully dressed and invites you in."
            $ the_person.change_slut_temp(1+the_person.get_opinion_score("not wearing anything"))
            $ the_person.discover_opinion("not wearing anything")
            the_person "Sorry about that, I was just relaxing and forgot the door wasn't locked."
        else:
            if the_person.update_outfit_taboos():
                "She turns around and waves you in, then seems to realise how little she is wearing."
                the_person "Oh, I'm not fully dressed! If you mind I can put something on."
                mc.name "Of course I don't mind. We're family, we can trust each other."
                "She smiles and nods."
            else:
                "She turns to you and smiles, waving a hand to invite you in."
                the_person "Come on in, do you need something?"

    call talk_person(the_person) from _call_talk_person_19
    return


label mom_house_work_nude_label(the_person):
    # When she's in the kitchen (or any other part of the house, for later events) she'll work in her underwear or (later) nude.
    $ effective_slut = the_person.effective_sluttiness("underwear_nudity") + (the_person.get_opinion_score("not wearing anything")*10)
    if effective_slut < 20: #TODO: This method of adding clothing with specific colours is dumb. (I suppose we could do the apron as being an overwear and then add it to underwear, but we should still have a system for it).
        # She's in her underwear but self concious about it
        $ the_person.apply_outfit(the_person.wardrobe.get_random_appropriate_underwear(the_person.effective_sluttiness(), guarantee_output = True))
        $ coloured_apron = apron.get_copy()
        $ coloured_apron.colour = [0.74,0.33,0.32,1.0]
        $ coloured_apron.pattern = "Pattern_1"
        $ coloured_apron.colour_pattern = [1.0,0.83,0.90,1.0]
        $ the_person.outfit.add_dress(coloured_apron)
        $ the_person.draw_person(position = "back_peek")
        "You find [the_person.possessive_title] in the kitchen working on dinner. She glances over her shoulder when you enter, seeming meek."
        the_person "Hi [the_person.mc_title]. I hope you don't mind the way I'm dressed, it's just a little more comfortable like this after work."
        mc.name "It's fine, I don't mind."
        "She turns her attention back to prepping dinner."

    elif the_person.effective_sluttiness("underwear_nudity") < 40:
        $ the_person.apply_outfit(the_person.wardrobe.get_random_appropriate_underwear(the_person.effective_sluttiness(), guarantee_output = True))
        $ coloured_apron = apron.get_copy()
        $ coloured_apron.colour = [0.74,0.33,0.32,1.0]
        $ coloured_apron.pattern = "Pattern_1"
        $ coloured_apron.colour_pattern = [1.0,0.83,0.90,1.0]
        $ the_person.outfit.add_dress(coloured_apron)
        $ the_person.draw_person(position = "back_peek")
        "You find [the_person.possessive_title] in the kitchen working on dinner in her underwear. She glances over her shoulder when you enter."
        the_person "Hi [the_person.mc_title], I hope you've had a good day."
        "She turns back to her work and hums happily."

    elif the_person.effective_sluttiness(["bare_pussy","bare_tits"]) < 60:
        $ the_person.apply_outfit(Outfit("Nude"))
        $ coloured_apron = apron.get_copy()
        $ coloured_apron.colour = [0.74,0.33,0.32,1.0]
        $ coloured_apron.pattern = "Pattern_1"
        $ coloured_apron.colour_pattern = [1.0,0.83,0.90,1.0]
        $ the_person.outfit.add_dress(coloured_apron)
        $ the_person.draw_person(position = "back_peek")
        "You find [the_person.possessive_title] in the kitchen, completely nude except for her apron. She glances over her shoulder when you enter."
        the_person "Hi [the_person.mc_title]. If me being... naked makes you uncomfortable just let me know. It's just a nice to relax a little after work."
        mc.name "I don't mind at all Mom."
        "She turns her attention back to prepping dinner."

    else:
        $ the_person.apply_outfit(Outfit("Nude"))
        $ coloured_apron = apron.get_copy()
        $ coloured_apron.colour = [0.74,0.33,0.32,1.0]
        $ coloured_apron.pattern = "Pattern_1"
        $ coloured_apron.colour_pattern = [1.0,0.83,0.90,1.0]
        $ the_person.outfit.add_dress(coloured_apron)
        $ the_person.draw_person(position = "back_peek")
        "You find [the_person.possessive_title] in the kitchen, completely nude except for her apron. She glances over her shoulder when you enter."
        the_person "Hi [the_person.mc_title], I hope you've had a great day. Dinner should be ready soon!"
        "She turns back to her work and sings happily to herself, wiggling her butt as she works."

    $ the_person.update_outfit_taboos()
    $ the_person.discover_opinion("not wearing anything")
    $ clear_scene()
    return

label breeding_mom_label(the_person):
    $ the_person.apply_outfit(Outfit("Nude"))
    $ the_person.draw_person(position = "sitting")
    $ the_person.update_outfit_taboos()
    "You walk into [the_person.title]'s room and find her sitting on the edge of her bed, completely naked."
    the_person "[the_person.mc_title], close the door, please. I have something I need to ask you."
    "You close the door to [the_person.possessive_title]'s bedroom and walk over to her bed."
    "She pats the bed beside her and you sit down."
    the_person "I've been thinking a lot about this. You're all grown up and [lily.title] isn't far behind."
    the_person "Soon you'll both be leaving home, but I don't think I'm done being a mother yet."
    "She takes your hands in hers and looks passionately into your eyes."
    the_person "I want you to give me a child. I want you to breed me."

    if the_person.has_large_tits():
        "Her face is flush and her breathing rapid. Her breasts heave up and down."
    else:
        "Her face is flush and her breathing rapid."

    menu:
        "Fuck her and try to breed her.":
            "You nod, and the mere the confirmation makes her shiver. She lies down on the bed and holds out her hands for you."
            $ the_person.draw_person(position = "missionary")
            "You strip down and climb on top of her. The tip of your hard cock runs along the enterance of her cunt and finds it dripping wet."
            the_person "Go in raw [the_person.mc_title], enjoy my pussy and give me your cum!"
            $ the_person.break_taboo("vaginal_sex")
            $ the_person.break_taboo("condomless_sex")
            "She wraps her arms around your torso and pulls you tight against her. She gives you a breathy moan when you slide your cock home."
            the_person "Ah... Fuck me and give me your baby! I'll take such good care of them, just like I did for you and [lily.title]!"
            $ starting_creampies = the_person.sex_record.get("Vaginal Creampies",0)
            call fuck_person(the_person, start_position = missionary, start_object = mc.location.get_object_with_name("bed"), skip_intro = True, position_locked = True) from _call_fuck_person_19
            $ the_report = _return #TODO: The creampie check should now be possible with the report system instead of checking her total record.
            if the_person.sex_record.get("Vaginal Creampies", 0) > starting_creampies: #We've creampied her at least once this encounter.
                "You roll off of [the_person.possessive_title] and onto the bed beside her, feeling thoroughly spent."
                "She brings her knees up against her chest and tilts her hips up, holding all of your cum deep inside of her."
                mc.name "Do you think that did it?"
                the_person "I don't know. It's the right time of the month."
                "You lie together in silence. [the_person.possessive_title] rocks herself side to side. You imagine your cum sloshing around her womb."
                "Eventually she puts her legs down and the two of you sit up in bed."
                #TODO: Add an action where you can try and breed her some more.

            else:
                "You roll off of [the_person.possessive_title] and onto the bed beside her."
                $ the_person.change_happiness(-20)
                the_person "I'm sorry... I'm sorry I'm not good enough to make you cum. I'm not good enough to earn your child..."
                "She sounds as if she is almost on the verge of tears."
                "You wrap your arms around her and hold her close."
                mc.name "Shh... You were fantastic. It's me, I'm just not feeling it today. Maybe we can try some other day."
                the_person "I don't know, this might have all been a mistake. Let's just... be quiet for a while, okay?"
                "You hold [the_person.possessive_title] until she's feeling better, then sit up in bed with her."

        "Say no.":
            $ the_person.draw_person(position = "sitting", emotion = "sad")
            "You shake your head. [the_person.title] looks immediately crestfallen."
            the_person "But why..."
            mc.name "[the_person.title], I love you but I can't give you what you want."
            "She nods and turns her head."
            $ the_person.change_slut_temp(-2)
            $ the_person.change_love(-2)
            the_person "Of course... I was just being silly. I should know better."

    return

label sleeping_walk_in_label(the_person): #TODO: This event is currently for Mom or Lily, but we could add more generic paths and have it useable for everyone.
    $ old_location = mc.location #Record these so we can have it dark, but restore it to normal later.
    $ old_lighting = old_location.lighting_conditions
    $ mc.location.lighting_conditions = dark_lighting #ie. she's got hte lights off and the blinds drawn.

    "You open the door to [the_person.possessive_title]'s room."
    if time_of_day == 0: #Morning.
        "For a moment you think it's empty, until you see [the_person.title] lying in bed, still sound asleep."
    else: #Evening
        "For a moment you think the room is empty. Then you notice [the_person.title], already in bed and asleep."

    $ the_person.apply_outfit(the_person.wardrobe.get_random_appropriate_underwear(the_person.effective_sluttiness(), guarantee_output = True)) #She's sleeping in her underwear.
    $ the_person.draw_person(position = "missionary")
    menu:
        "Go inside.":
            "You close the door behind you slowly, careful not to wake [the_person.possessive_title] up."

            menu:
                "Wake her up.": #Wakes her up, starts a conversation. If she thinks her outfit is too slutty she'll get changed first.
                    mc.name "[the_person.title] are you awake?"
                    "You speak quietly, coaxing her back to consciousness."
                    $ the_person.change_happiness(-5)
                    if the_person == mom:
                        "She rolls over and rubs her eyes."
                        the_person "Hmm? Is everything okay [the_person.mc_title]?"
                        mc.name "Everything's fine, I just wanted to talk, if you have a moment."
                        if the_person.judge_outfit(the_person.outfit) and not the_person.has_taboo("underwear_nudity"): # No problem, get up and chat.
                            the_person "I'm always here for you [the_person.mc_title], of course we can talk."
                            $ the_person.draw_person(position = "sitting")
                            "She sits up and yawns, stretching her arms."

                        else: # She needs to get changed.
                            the_person "Of course, but..."
                            "She pulls the bed sheets up to cover her chest."
                            the_person "I'm not decent. Could you just look away for a moment while I get dressed?"
                            mc.name "Okay [the_person.title]."
                            "You avert your eyes. You can hear moving around [the_person.possessive_title] as she gets dressed."
                            $ clear_scene()
                            menu:
                                "Peek":
                                    "You reposition on the bed, sliding to the side so you can \"accidentally\" catch [the_person.title]'s reflection in her bedroom mirror."
                                    $ the_person.apply_outfit(Outfit("Nude"))
                                    $ the_person.draw_person(position = "walking_away")
                                    "You see her naked, quickly digging through her closet for something to put on."
                                    $ the_person.draw_person(position = "standing_doggy")
                                    "After searching for a moment she bends over, grabbing something from lower down."
                                    $ clear_scene()
                                    "You look away when she starts to turn around again."

                                "Wait for her to get dressed.":
                                    "You wait patiently until she's finished."
                            $ the_person.apply_outfit()
                            the_person "All done, thank you for waiting [the_person.mc_title]."
                            $ the_person.draw_person()
                            the_person "Now, what did you want to talk about?"
                    else: #Lily
                        "She rolls over and groans unhappily."
                        the_person "What? Ah... what do you want?"
                        mc.name "I wanted to talk, do you have a moment?"
                        if the_person.judge_outfit(the_person.outfit) and not the_person.has_taboo("underwear_nudity"):
                            the_person "Right now? Well, I'm already awake I guess..."
                            $ the_person.draw_person(position = "sitting")
                            "She swings her legs over the side of her bed and sit up, yawning dramatically."
                        else:
                            the_person "Right now? I'm not even dressed... Hey!"
                            "She grabs her pillow and swings at you half-heartedly."
                            the_person "Get out, I need to get dressed!"
                            mc.name "Relax! Just get dressed already, it's no big deal."
                            the_person "Just look away and let me put some clothes on."
                            mc.name "Fine. I promise I won't peek."
                            $ clear_scene()
                            "You look away, and [the_person.title] get's out of bed and starts to get dressed."
                            menu:
                                "Peek":
                                    "You reposition on the bed, sliding to the side so you can \"accidentally\" catch [the_person.title]'s reflection in her bedroom mirror."
                                    $ the_person.apply_outfit(Outfit("Nude"))
                                    $ the_person.draw_person(position = "walking_away")
                                    "You see her naked, quickly digging through her drawers for something to put on."
                                    $ the_person.draw_person(position = "standing_doggy")
                                    "After searching for a moment she bends over, grabbing something from lower down."
                                    $ clear_scene()
                                    "You look away when she starts to turn around again."

                                "Wait for her to get dressed.":
                                    "You wait patiently until she's finished."
                            $ the_person.apply_outfit()
                            the_person "Okay, you can look again."
                            $ the_person.draw_person()
                            the_person "Now what was so important you needed to wake me up?"


                    $ old_location.lighting_conditions = old_lighting
                    call talk_person(the_person) from _call_talk_person_20

                "Sleep in her bed.{image=gui/heart/Time_Advance.png}{image=gui/heart/Time_Advance.png}" if time_of_day == 4: #Only at night #TODO: Break the "sleep with" events out for more detail
                    "You move quietly to the side of [the_person.possessive_title]'s bed, lift the covers, and lie down next to her."
                    if the_person == mom:
                        "She stirs, rolling over to face you."
                        the_person "[the_person.mc_title]? Is everything alright?"
                        mc.name "Yeah, I just can't sleep [the_person.title]. Can I stay with you tonight?"
                        if the_person.love < 15:
                            the_person "You're a little old to have to be sleeping with your Mom."
                            "She gives you a gentle kiss on the forehead."
                            the_person "Go get yourself a glass of warm milk, add a little honey, and then try falling asleep again."
                            the_person "I'm sure that'll do it. Okay?"
                            mc.name "Okay, thanks for the help [the_person.title]."
                            "She smiles sleepily at you, and seems to be asleep by the time you make it to the door."
                            $ the_person.on_room_enter_event_list.append(Limited_Time_Action(sleeping_walk_in, sleeping_walk_in.event_duration)) #re-add the LTE since she's still asleep. Note that we can't have stat effects for this, otherwise it's infinitely farmable
                            $ mc.change_location(hall)
                        else:
                            $ the_person.change_love(2)
                            the_person "You still come right to your mommy when you can't sleep. That's so sweet."
                            "She gives you a gentle kiss on the forehead."
                            the_person "Of course you can stay. Let's get some rest."
                            #TODO: Break some of this out to a "sleep with Mom" event
                            $ old_location.lighting_conditions = old_lighting
                            call advance_time() from _call_advance_time_31

                    else: # Lily
                        "She groans and rolls over to face you."
                        the_person "[the_person.mc_title]? What... What are you doing here?"
                        mc.name "I can't sleep, can I stay here for a bit?"
                        if the_person.love < 25:
                            the_person "We're too old for this, I really just want to get some sleep."
                            the_person "Go bug [mom.title], maybe she'll let you stay with her."
                            mc.name "Fine, I'll leave you alone."
                            the_person "Thank... you..."
                            "You get out of bed, and [the_person.title] is asleep again by the time you make it to the door."
                            $ the_person.on_room_enter_event_list.append(Limited_Time_Action(sleeping_walk_in, sleeping_walk_in.event_duration)) #readd the LTE since she's still asleep. Note that we can't have stat effects for this, otherwise it's infinitely farmable
                            $ mc.change_location(hall)
                        else:
                            the_person "You really need your little sister, huh?"
                            $ the_person.change_love(2)
                            "She smiles and laughs sleepily."
                            the_person "You did let me sleep with you when we were younger, so sure."
                            the_person "Just stay on your side, and don't hog the blankets."
                            #TODO: Break some of this out into a "sleep with Lily" event
                            $ old_location.lighting_conditions = old_lighting
                            call advance_time() from _call_advance_time_32 #TODO: Double check advancing like this doesn't break anything.
                    #TODO: Let you try and cuddle-fuck her.
                    #TODO: Write cuddle fuck as a sex position. (Include transition from/to missionary and from/to doggy style)


                "Get a better look at her.":
                    "You wait a moment to make sure [the_person.title] is completely asleep, then creep closer to her bed."
                    "You reach out and gently pull the bed sheets down to her thighs."
                    the_person "Hmm? Mmm..." #TODO: We need an "asleep emotion" (ie. eyes closed, mouth neutral)
                    "She murmurs to herself, still asleep, and rolls onto her back."
                    call nightime_grope(the_person) from _call_nightime_grope #Break this out into a seperate function so we can loop easily. Returns True if our action woke her up
                    $ awake = _return
                    $ clear_scene()
                    if not awake:
                        $ the_person.on_room_enter_event_list.append(Limited_Time_Action(sleeping_walk_in, sleeping_walk_in.event_duration)) #Readd LTE.
                    $ mc.change_location(hall)



        "Let her sleep.":
            "You back out of the room and close door slowly, careful not to wake [the_person.possessive_title]."
            $ the_person.on_room_enter_event_list.append(Limited_Time_Action(sleeping_walk_in, sleeping_walk_in.event_duration)) # Re-add this LTE so it keeps triggering when you go back.
            $ mc.change_location(hall) #Make sure to change our location so we aren't immediately inside again.

    $ old_location.lighting_conditions = old_lighting
    $ clear_scene()
    return

label nightime_grope(the_person, masturbating = False):
    # A couple outcomes are possible:
    # 1) You do some stuff, and then get out
    # 2) You do some stuff and get caught. Large Love hit, maybe future reprecusions event. Useful way to break taboos early at the cost of Love.
    # 3) You do some stuff, get caught, but she's into it. Enter sex system.
    # Goal is to have this be relatively person agnostic, so we can use it with anyone.
    # Options to feel up/strip girl may be their own path?
    $ awake = False
    $ bra_item = the_person.outfit.get_bra()
    $ panties_item = the_person.outfit.get_panties()

    # Establish the Sluttiness requirement tokes ahead of time so we can reference them inline.
    $ grope_tits_slut_requirement = 10
    $ grope_tits_slut_token = get_red_heart(grope_tits_slut_requirement)

    $ grope_pussy_slut_requirement = 15
    $ grope_pussy_slut_token = get_red_heart(grope_pussy_slut_requirement)

    $ jerk_off_slut_requirement = 10
    $ jerk_off_slut_token = get_red_heart(jerk_off_slut_requirement)

    $ titfuck_slut_requirement = 30
    $ titfuck_slut_token = get_red_heart(titfuck_slut_requirement)

    $ facefuck_slut_requirement = 40
    $ facefuck_slut_token = get_red_heart(facefuck_slut_requirement)

    $ fuck_slut_requirement = 50
    $ fuck_slut_token = get_red_heart(fuck_slut_requirement)

    $ cum_tits_slut_requirement = 30
    $ cum_tits_slut_token = get_red_heart(cum_tits_slut_requirement)

    $ cum_face_slut_requirement = 40
    $ cum_face_slut_token = get_red_heart(cum_face_slut_requirement)

    $ cum_throat_slut_requirement = 55
    $ cum_throat_slut_token = get_red_heart(cum_throat_slut_requirement)

    $ cum_inside_slut_requirement = 65
    $ cum_inside_slut_token = get_red_heart(cum_inside_slut_requirement)


    if masturbating: #TODO: Add a few variations of this since we might loop through here a few times
        "You stroke your cock, thinking about what you want to do with [the_person.possessive_title]."

    #TODO: We may want to replace this with an Action based menu at some point to more conveniently format all of the options
    menu:
        "Grope her tits. -5{image=gui/extra_images/energy_token.png}" if mc.energy >= 5 and the_person.effective_sluttiness() >= grope_tits_slut_requirement:
            $ mc.change_energy(-5)
            if the_person.outfit.tits_available():
                "You reach out and gently place your hand on one of [the_person.possessive_title]'s tits."
                $ the_person.draw_person(position = "missionary", the_animation = tit_bob, animation_effect_strength = 0.5)
                if the_person.has_large_tits():
                    "Her breast is large, warm, and soft under your hand. [the_person.title] sighs softly when you squeeze it."
                    "You grab her other boob too and start to massage both of them. They bounce and jiggle easily with each motion."
                else:
                    "You're able to cup her entire soft breast with one hand. [the_person.title] sighs softly when you squeeze it."
                    "You plant a hand on her other boob too and massage both of them. After a moment of teasing you feel her nipples harden."
                $ the_person.change_arousal(4 + mc.sex_skills.get("Foreplay", 0))

            else:
                "You reach out and gently place your hand on one of [the_person.possessive_title]'s tits, seperated only by her [bra_item.display_name]."
                if the_person.has_large_tits():
                    "Her tits are large, barely contained by her [bra_item.display_name] and begging to be set free."
                    "You grab her other boob and massage both at once. She sighs softly in her sleep."
                else:
                    "Even with it hidden away you can enjoy her perky tit."
                    "You grab her other boob, and start to massage both of them at once through her [bra_item.display_name]."

                $ the_person.change_arousal(1 + mc.sex_skills.get("Foreplay", 0))

            the_person "Ah..."


            if renpy.random.randint(0,100) < 15:
                $ awake = True
                if masturbating:
                    "Her eyes flutter lightly. You pull your hands back and stuff your cock hastily back in your pants as she lazily opens her eyes."
                else:
                    "Her eyes flutter lightly. You pull your hands back as she lazily opens her eyes."
                the_person "[the_person.mc_title]? Is that you?"
                mc.name "Hey [the_person.title], I was just checking in on you."
                $ the_person.change_happiness(-5)
                $ the_person.change_slut_temp(1 + the_person.get_opinion_score("being submissive"))
                "She rubs her eyes."
                the_person "I'm fine, do you need anything?"
                mc.name "No, I was just going... Sorry for waking you up."
                "[the_person.possessive_title] seems slightly confused as you back quickly out of the room."
                return True
            else:
                "She murmurs softly in her sleep, unaware of you feeling up her chest."

            if not awake and bra_item is not None and the_person.outfit.is_item_unanchored(bra_item, half_off_instead = True) and not bra_item.half_off:
                menu:
                    "Move her [bra_item.display_name].":
                        "You move slowly, hooking a finger underneath her [bra_item.display_name] and lifting it up and away."
                        $ the_person.draw_animated_removal(bra_item, position = "missionary", half_off_instead = True) #TODO: Decide if we need some special position info here
                        if the_person.has_large_tits():
                            "[the_person.possessive_title]'s tits spill free, jiggling for a couple of seconds before finally coming to a stop."
                        else:
                            pass #No extra dialogue needed

                        if renpy.random.randint(0,100) < 15 - 2*the_person.get_opinion_score("not wearing underwear"):
                            the_person "Hmmm?"
                            if masturbating:
                                "[the_person.title]'s eyes flutter open. You jump back, stuffing your cock back into your pants as quickly as possible."
                            else:
                                "[the_person.title]'s eyes flutter open. You jump back, doing your best to look innocent."
                            mc.name "Sorry [the_person.title], I thought I had heard you say something and was checking in. I didn't mean to wake you up."
                            "[the_person.possessive_title] rubs her eyes and sits up, then notices her [bra_item.display_name] isn't covering her."
                            if the_person.judge_outfit(the_person.outfit):
                                the_person "I must have been having a dream and tossing in my sleep... I'm okay, thank you [the_person.mc_title]."
                            else:
                                "She yanks it back into place, then pulls the bed covers up around herself."
                                $ the_person.outfit.restore_all_clothing()
                                $ the_person.draw_person(position = "missionary") #TODO: Check if we need special position stuff here
                                the_person "I'm fine [the_person.mc_title], I must have just been having a bad dream."
                                $ the_person.change_happiness(-5)
                                $ the_person.change_love(-1)
                                $ the_person.change_slut_temp(1 + the_person.get_opinion_score("showing her tits"))
                                "She doesn't sound entirely convinced of her own explanation, but seems willing to let it go."


                            mc.name "That makes sense, sorry again!"
                            "You beat a hasty retreat from [the_person.possessive_title]'s bedroom."
                            return True
                        else:
                            the_person "Mmm..."
                            "[the_person.title] shifts in bed, but doesn't wake up."


                    "Leave it alone.":
                        "Your head wins out over your dick, and you decide not to risk it."
                        "You keep pawing at her tits through her [bra_item.display_name] instead."

            call nightime_grope(the_person, masturbating) from _call_nightime_grope_1
            return _return

        "Grope her tits. -5{image=gui/extra_images/energy_token.png} (disabled)" if mc.energy < 5 and the_person.effective_sluttiness() >= grope_tits_slut_requirement:
            pass

        "Grope her tits. -5{image=gui/extra_images/energy_token.png}\n{color=#ff0000}Requires:[grope_tits_slut_token]{/color} (disabled)" if the_person.effective_sluttiness() < grope_tits_slut_requirement:
            pass

        "Grope her pussy. -5{image=gui/extra_images/energy_token.png}" if mc.energy >= 5 and the_person.effective_sluttiness() >= grope_pussy_slut_requirement:
            "You reach a hand between [the_person.title]'s warm thighs."
            $ mc.change_energy(-5)
            $ the_person.draw_person(position = "missionary", the_animation = ass_bob, animation_effect_strength = 0.5)
            if the_person.outfit.vagina_available():
                "You gently pet her pussy, feeling her soft folds."
                "[the_person.possessive_title] shifts and moans again when you brush agaisnt the small nub of her clit."
                $ the_person.change_arousal(6 + mc.sex_skills.get("Foreplay", 0))
            else:
                "You massage her pussy through her [panties_item.display_name]."
                "Through the fabric you're able to make out the faint bump of her clit. She moans when you brush it."
                $ the_person.change_arousal(10 + mc.sex_skills.get("Foreplay", 0))
            the_person "Mmph..."

            if renpy.random.randint(0,100) < 20 - 3*the_person.get_opinion_score("being fingered"):
                "[the_person.title] shifts in bed, then groans and starts to sit up."
                if masturbating:
                    "You yank your hand back and stuff your cock back in your pants as her eyes flutter open."
                else:
                    "You yank your hand back and step away from the bed as her eyes flicker open."

                the_person "[the_person.mc_title], is that you? What... What's going on?"
                mc.name "Oh, nothing [the_person.title]. I thought I heard you say something, so I was just checking in..."
                $ the_person.change_slut_temp(1 + the_person.get_opinion_score("being submissive"))
                the_person "Oh... I must have been talking in my sleep. I was having a dream, that's all."
                mc.name "Right, that makes sense. Sorry for waking you up."
                "You beat a hastiy retreat, leaving [the_person.possessive_title] slightly confused."
                return True
            else:
                "She sighs and spreads her legs for you, instinct driving her even when asleep."

            if not awake and panties_item is not None and the_person.outfit.is_item_unanchored(panties_item, half_off_instead = True) and not panties_item.half_off:
                menu:
                    "Move her [panties_item.display_name].":
                        "You hook a finger under her [panties_item.display_name] and slowly slide them away."
                        $ the_person.draw_animated_removal(panties_item, position = "missionary", half_off_instead = True) #TODO: Decide if we need position info here
                        if renpy.random.randint(0,100) < 25 - the_person.get_opinion_score("not wearing underwear"):
                            "[the_person.title] groans and rolls over, grabbing her [panties_item.display_name] forcing you to pull your hand away."
                            if masturbating:
                                "You stuff your cock back into your pants as quickly as you can manage when her eyes start to flutter open."
                            else:
                                "You take a step back as her eyes flutter open and she starts to sit up."
                            the_person "Ugh... Is someone there? [the_person.mc_title]?"
                            mc.name "Yeah, it's me [the_person.title]. I thought you had said something, but you must have just been talking in your sleep."
                            if the_person.judge_outfit(the_person.outfit):
                                the_person "Mmm... I was having a dream. What did I say?"
                                mc.name "I'm not sure, I just thought I should check on you. It looks like you're though."
                                "You back out of her room, leaving her confused but unaware of what you had been up to."
                            else:
                                the_person "Mmm... I was having a dream and..."
                                "She glances down and realises how exposed she is. She gathers up the blankets and pulls them up to cover herself."
                                $ the_person.outfit.restore_all_clothing()
                                $ the_person.draw_person(position = "missionary") #TODO: Check if we need special position stuff here
                                $ the_person.change_happiness(-5)
                                $ the_person.change_love(-1)
                                $ the_person.change_slut_temp(1 + the_person.get_opinion_score("showing her ass"))
                                the_person "I'm fine though, really. Thanks for checking in..."
                                mc.name "Right, good to hear. Forget I was even here..."
                                "You beat a hasty retreat, unsure if [the_person.title] really believed your excuse."
                            return True
                        else:
                            "[the_person.title] murmurs something, but sleeps on peacefully."


                    "Leave it alone.":
                        "Your head wins out over your dick, and you decide not to risk it."
                        "You continue to stroke her pussy through her [panties_item.display_name] instead."

            call nightime_grope(the_person, masturbating) from _call_nightime_grope_2
            return _return

        "Grope her pussy. -5{image=gui/extra_images/energy_token.png} (disabled)" if mc.energy < 5 and the_person.effective_sluttiness() >= grope_pussy_slut_requirement:
            pass

        "Grope her pussy. -5{image=gui/extra_images/energy_token.png}\n{color=#ff0000}Requires:[grope_pussy_slut_token]{/color} (disabled)" if the_person.effective_sluttiness() < grope_pussy_slut_requirement:
            pass

        "Jerk off." if not masturbating and the_person.effective_sluttiness() >= jerk_off_slut_requirement:
            if the_person.outfit.tits_visible():
                "Seeing [the_person.possessive_title] exposed in front of you, tits out, is enough to make you rock hard."

            elif the_person.outfit.vagina_visible():
                "Seeing [the_person.possessive_title] exposed in front of you, pussy out and waiting, is enough to make you rock hard."

            else:
                "Looking at [the_person.possessive_title] laid out in front of you half naked is enough to make you rock hard."

            "You pull your pants down and grab your cock, stroking it to the sight."

            if renpy.random.randint(0,100) < 5:
                "[the_person.title] shifts in her sleep, mumbles something, then sits up in bed."
                "You hurry and stuff your cock back into your pants as she opens her eyes and looks at you."
                the_person "[the_person.mc_title], what are you... Doing here?"
                mc.name "I thought... I heard you talking in your sleep. That's all."
                if the_person.effective_sluttiness() > 30 and not (the_person.has_taboo("touching_penis") and the_person.has_taboo("sucking_cock")): #High slut, doesn't care. TODO: Add a taboo break variant
                    $ the_person.update_outfit_taboos()
                    the_person "Uh huh? Then why is your cock hard?"
                    mc.name "I... Was... Uh..."
                    "You try and invent a quick excuse, but [the_person.possessive_title] just giggles and waves her hand."
                    the_person "Do you want some help with that? It seems like it's really distracting you..."
                    menu:
                        "Let her \"help\".":
                            mc.name "Sure, come take care of this for me."
                            if (the_person.effective_sluttiness() + 10*the_person.get_opinion_score("giving blowjobs")) > 50 and not the_person.has_taboo("sucking_cock"):
                                "She nods and sits up, then slides out of bedd and gets onto her knees in front of you."
                                $ the_person.draw_person(position = "blowjob")
                                the_person "Mmm, I want to suck on that cock..."
                                "[the_person.possessive_title] kisses the tip of your dick, then opens her lips and slides you into her mouth."
                                "She looks up at you from her knees, maintaining eye contact as she begins to bob her head up and down your shaft."
                                call fuck_person(the_person, start_position = blowjob, position_locked = True, girl_in_charge = True) from _call_fuck_person_94 #Standing position should be selected by default
                                $ the_report = _return
                                call sex_report_helper(the_person, the_report) from _call_sex_report_helper

                            else:
                                $ the_person.draw_person()
                                the_person "Oh my god, look at this..."
                                "She wraps one hand gently around your shaft and strokes it experimentally."
                                the_person "Just relax, I'm going to take care of this for you [the_person.mc_title]."
                                "[the_person.possessive_title] holds you close as she begins to jerk you off."
                                call fuck_person(the_person, start_position = handjob, position_locked = True, girl_in_charge = True) from _call_fuck_person_95
                                $ the_report = _return
                                call sex_report_helper(the_person, the_report) from _call_sex_report_helper_1




                        "Just leave.":
                            mc.name "I'm fine, I can take care of it. Sorry for waking you up."
                            "[the_person.title] almost seems disappointed as you back out of her room and close the door."


                else:
                    the_person "Uh huh... Maybe you should go and take care of... That."
                    $ the_person.change_happiness(-10)
                    $ the_person.change_love(-2)
                    $ the_person.change_slut_temp(1 + the_person.get_opinion_score("being submissive"))
                    "She nods at your pants, and the obvious crotch bulge."
                    "You try and re-adjust your pants to hide it as you back out of the room."
                return True
            else:
                "[the_person.title] sleeps peacefully, unaware of your thick cock being stroked only inches away."
            call nightime_grope(the_person, True) from _call_nightime_grope_3
            return _return

        "Jerk off.\n{color=#ff0000}Requires:[jerk_off_slut_token]{/color} (disabled)" if not masturbating and the_person.effective_sluttiness() < jerk_off_slut_requirement:
            pass

        "Get ready to cum." if masturbating:
            "You speed up your strokes, aware of the limited amount of time you might have before [the_person.possessive_title] wakes up."
            "With her exposed body as motivation it doesn't take long to push yourself to the edge."
            "You take a deep breath and pass the point of no return."
            menu:
                "Cum in your hand.":
                    call sleep_cum_hand(the_person) from _call_sleep_cum_hand

                "Cum on her face." if the_person.effective_sluttiness() >= cum_face_slut_requirement:
                    call sleep_cum_face(the_person) from _call_sleep_cum_face
                    $ awake = _return

                "Cum on her face.\n{color=#ff0000}Requires:[cum_face_slut_token]{/color} (disabled)" if the_person.effective_sluttiness() < cum_face_slut_requirement:
                    pass

                "Cum on her tits." if the_person.effective_sluttiness() >= cum_tits_slut_requirement:
                    call sleep_cum_tits(the_person) from _call_sleep_cum_tits
                    $ awake = _return

                "Cum on her tits.\n{color=#ff0000}Requires:[cum_tits_slut_token]{/color} (disabled)" if the_person.effective_sluttiness() < cum_tits_slut_requirement:
                    pass

        "Tit fuck her." if the_person.has_large_tits() and the_person.outfit.tits_available() and masturbating and the_person.effective_sluttiness() >= titfuck_slut_requirement:
            "You climb onto [the_person.possessive_title]'s bed and swing one leg over her, straddling her chest."
            "You lower yourself down and settle your cock between her tits. You grab one with each hand and squeeze them gently around your shaft."
            $ the_person.draw_person(position = "missionary", the_animation = tit_bob, animation_effect_strength = 0.7)
            "You start to fuck her tits, moving as slowly as you can bear while wrapped in her warm soft mammaries."
            if renpy.random.randint(0,100) < 50 - 5*the_person.get_opinion_score("giving tit fucks"):
                the_person "Mmm... Mmmph... Hmm?"
                "[the_person.possessive_title] moans softly, then lifts her head up and opens her eyes."
                the_person "[the_person.mc_title]?"
                if the_person.effective_sluttiness("touching_body") + 5*(the_person.get_opinion_score("being submissive") + the_person.get_opinion_score("giving tit fucks")) >= 45 and not the_person.has_taboo("touching body"):
                    "She looks you up and down, her eyes eventually settling on your hard cock sandwiched between her tits."
                    the_person "Mmm... You don't have to stop, I was having the most amazing dream."
                    "She reaches down and puts her own hands over yours, squeezing her breasts together even harder."
                    "You breathe a sigh of relief and start to pump your hips again."
                    the_person "How about you stand up and let me take care of you properly, hmm?"
                    menu:
                        "Let her tit fuck you.":
                            mc.name "That sounds fantastic [the_person.title]."
                            the_person "I thought you would be interested... Stand up."
                            $ the_person.draw_person(position = "blowjob")
                            "You do as you're told, standing up again. [the_person.possessive_title] gets off of her bed and onto her knees in front of you."
                            "She takes her tits up in her hands and lifts them up, pressing them on either size of your shaft."
                            if rank_tits(the_girl.tits) >= 7: #E sized or larger
                                "They're warm, soft, and feel like they melt around your sensitive dick. Her breasts are so large the tip of your cock doesn't even make it to the top of her cleavage."
                            else:
                                "They're warm, soft, and feel like they melt around your sensitive dick. The tip of your cock just barely pops out of the top of her cleavage."
                            call fuck_person(the_person, start_position = tit_fuck, position_locked = True, girl_in_charge = True) from _call_fuck_person_96
                            $ the_report = _return
                            call sex_report_helper(the_person, the_report) from _call_sex_report_helper_2

                        "Just leave.":
                            mc.name "That sounds like a good time, but maybe some other time..."
                            "You pull your cock out from between her breasts and stand up. [the_person.title] seems disappointed."
                            the_person "Feeling shy now that I'm awake? I'm sorry [the_person.mc_title], I didn't mean to scare you off..."
                            "You stuff your cock back in your pants and hurry out of the room, leaving [the_person.possessive_title] awake and confused."

                else:
                    "She seems momentarily stunned seeing you straddling her, cock held between her tits."
                    mc.name "Hey [the_person.title], I was just..."
                    "She gasps and pushes on your thighs, trying to move you off of her."
                    $ the_person.change_happiness(-10)
                    $ the_person.change_love(-5 + (2*the_person.get_opinion_score("being submissive")))
                    $ the_person.change_slut_temp(1 + the_person.get_opinion_score("being submissive") + the_person.get_opinion_score("giving tit fucks"))
                    the_person "[the_person.mc_title]! Oh my god, what are you doing?"
                    "You shuffle backwards, then swing a leg over her and stand back up beside her bed. Her eyes are fixed on your rock hard dick."
                    the_person "You shouldn't... You can't do this [the_person.mc_title]!"
                    mc.name "It's not what it looks like, I was just..."
                    "She tears her eyes away from you and shakes her head."
                    the_person "No, just go. I don't want to talk about it. Ever."
                    "You stuff your erection back in your pants and hurry out of her room."

                return True
            else:
                "Despite the unavoidable bouncing of the mattress and your cock jammed between her breasts, [the_person.possessive_title] continues to sleep soundly."
                "You squeeze down on her tits as much as you dare, and soon your precum has turned her cleavage into a warm, slippery, fuck channel."
                "You enjoy [the_person.possessive_title]'s body for a few minutes, each stroke between her breasts pulling you closer to your orgasm."
                "Soon you're right at the edge, with nothing left to do but decide where to finish."
                menu:
                    "Cum in your hand.":
                        call sleep_cum_hand(the_person) from _call_sleep_cum_hand_1
                        $ awake = _return

                    "Cum on her tits." if the_person.effective_sluttiness() >= cum_tits_slut_requirement: #Slut Requirements
                        "You pull your cock out from between her breasts at the last moment and take aim."
                        call sleep_cum_tits(the_person, straddle = True) from _call_sleep_cum_tits_1
                        $ awake = _return

                    "Cum on her tits\n{color=#ff0000}Requires:[cum_tits_slut_token]{/color} (disabled)" if the_person.effective_sluttiness() < cum_tits_slut_requirement:
                        pass

                    "Cum on her face." if the_person.effective_sluttiness() >= cum_face_slut_requirement: #Slut requirements
                        "You pull your cock out from between her breasts at the last moment and take aim."
                        call sleep_cum_face(the_person, straddle = True) from _call_sleep_cum_face_1
                        $ awake = _return

                    "Cum on her face\n{color=#ff0000}Requires:[cum_face_slut_token]{/color} (disabled)" if the_person.effective_sluttiness() < cum_face_slut_requirement:
                        pass

        "Tit fuck her.\n{color=#ff0000}Requires:[titfuck_slut_token]{/color} (disabled)" if the_person.has_large_tits() and the_person.outfit.tits_available() and masturbating and the_person.effective_sluttiness() < titfuck_slut_requirement:
            pass

        "Face fuck her." if masturbating and the_person.effective_sluttiness() >= facefuck_slut_requirement:
            "You step closer to [the_person.possessive_title]'s bed, putting your cock right next to her face."
            "You put a finger on her chin and encourage her to turn her head to the side."
            "After a moment of resistance she sleepily rolls her head towards you, and you can feel her warm breath on the tip of your dick."
            "You take a deep breath, then move your hips and press the tip of your cock against her lips."
            the_person "Hmmm? Mmph..."
            $ the_person.draw_person(position = "missionary", special_modifier = "blowjob", the_animation = blowjob_bob, animation_effect_strength = 0.7)
            "[the_person.title] mumbles something, and you seize the moment to slide yourself past her lips."
            "Her tongue licks experimentally at your tip, exploring it's visitor."
            "You place a hand on the back of her head and hold it steady as you move even deeper into her warm, wet, mouth."
            the_person "Mmph... Umph..."
            if renpy.random.randint(0,100) < 70 - 5*the_person.get_opinion_score("giving blowjobs"):
                "You're starting to think you actually get away with this when [the_person.possessive_title]'s eyes start to flutter."
                if the_person.effective_sluttiness("sucking_cock") + 5*(the_person.get_opinion_score("being submissive") + the_person.get_opinion_score("giving blowjobs")) >= 50 and not the_person.has_taboo("sucking_cock"):
                    "Before you can react her eyes drift open."
                    "[the_person.title] blinks twice, as if suprised to find your cock in her mouth, and then starts to bob her head and suck you off."
                    mc.name "Oh fuck..."
                    $ the_person.draw_person(position = "blowjob")
                    "She gives you few playful bobs of her head, then pulls off with a satisfying pop."
                    the_person "Hey, did you need something? You could have woken me up and I would have been happy to help with this..."
                    "She kisses the tip of your cock for emphasis."
                    the_person "Do you want me to take care of it for you?"
                    menu:
                        "Let her blow you.":
                            mc.name "Sure, come take care of this for me."
                            "She nods and sits up, then slides out of bedd and gets onto her knees in front of you."
                            $ the_person.draw_person(position = "blowjob")
                            the_person "Mmm, I want to suck on that cock..."
                            "[the_person.possessive_title] kisses the tip of your dick, then opens her lips and slides you into her mouth."
                            "She looks up at you from her knees, maintaining eye contact as she begins to bob her head up and down your shaft."
                            call fuck_person(the_person, start_position = blowjob, position_locked = True, girl_in_charge = True) from _call_fuck_person_97 #Standing position should be selected by default
                            $ the_report = _return
                            call sex_report_helper(the_person, the_report) from _call_sex_report_helper_3

                        "Just leave.":
                            mc.name "I'm fine, I can take care of it. Sorry for waking you up."
                            "[the_person.title] almost seems disappointed as you back out of her room and close the door."


                else: #TODO: Use gagged text modifier if we have it ready
                    "Before you can react her eyes snap open."
                    the_person "Mmmph!"
                    $ the_person.draw_person(position = "missionary")
                    "She yanks her head back, pulling your cock suddenly out of her mouth."
                    the_person "[the_person.mc_title]! Oh my god, where you just..."
                    "She touches her lips, eyes suddenly locked on your throbbing cock in front of her."
                    mc.name "Oh, hey [the_person.title]. I, uh... Was just checking in on you."
                    $ the_person.change_happiness(-10)
                    $ the_person.change_love(-5 + (2*the_person.get_opinion_score("being submissive")))
                    $ the_person.change_slut_temp(1 + the_person.get_opinion_score("being submissive") + the_person.get_opinion_score("giving blowjobs"))
                    the_person "You should... You should go, alright?"
                    "You stuff your wet dick back into your pants and back up towards her bedroom door."
                    mc.name "Hey, I..."
                    the_person "Just go. I don't want to talk about it."
                    "You leave the room and close her bedroom door behind her."

                return True
            else:
                "You're half-expecting her to snap awake at any time, but [the_person.title] seems to adjust well to having a cock down her throat."
                "Emboldened by your success, you start to thrust in and out. Soon you're happily fucking [the_person.possessive_title]'s mouth."
                "Each stroke of your cock in and out of [the_person.title]'s mouth feels better than the last, and the added thrill of being caught only hightens the experience."
                "It doesn't take long before you're at the edge and ready to cum."
                menu:
                    "Cum in your hand.":
                        call sleep_cum_hand(the_person) from _call_sleep_cum_hand_2
                        $ awake = _return

                    "Cum on her tits." if the_person.effective_sluttiness() >= cum_tits_slut_requirement: #Slut requirements
                        call sleep_cum_tits(the_person) from _call_sleep_cum_tits_2
                        $ awake = _return


                    "Cum on her tits.\n{color=#ff0000}Requires:[cum_tits_slut_token]{/color} (disabled)" if the_person.effective_sluttiness() < cum_tits_slut_requirement:
                        pass

                    "Cum on her face." if the_person.effective_sluttiness() >= cum_face_slut_requirement:
                        call sleep_cum_face(the_person) from _call_sleep_cum_face_2
                        $ awake = _return

                    "Cum on her face.\n{color=#ff0000}Requires:[cum_face_slut_token]{/color} (disabled)" if the_person.effective_sluttiness() < cum_face_slut_requirement:
                        pass

                    "Cum down her throat." if the_person.effective_sluttiness() >= cum_throat_slut_requirement:
                        call sleep_cum_throat(the_person) from _call_sleep_cum_throat
                        $ awake = _return

                    "Cum down her throat.\n{color=#ff0000}Requires:[cum_throat_slut_token]{/color} (disabled)" if the_person.effective_sluttiness() < cum_throat_slut_requirement:
                        pass

        "Face fuck her.\n{color=#ff0000}Requires:[facefuck_slut_token]{/color} (disabled)" if masturbating and the_person.effective_sluttiness() < facefuck_slut_requirement:
            pass

        "Fuck her." if the_person.outfit.vagina_available() and masturbating and the_person.effective_sluttiness() >= fuck_slut_requirement: #TODO: Sluttiness requirements
            "You climb onto [the_person.possessive_title]'s bed and position yourself on top of her."
            "After a moment of resistance she unconciously spreads her legs to make room for you."
            "You grab your cock and tap the tip of it against her slit. She mumbles something in her sleep in response."
            menu:
                "Put on a condom.":
                    "You pause before pushing yourself into [the_person.title]'s pussy."
                    "You pull a condom out of your pocket, rip open the package, and roll it over your cock."
                    $ mc.condom = True
                    "When you're protected you lie back down on top of [the_person.possessive_title] and tease her cunt with the tip of your cock."

                "Fuck her raw.":
                    "There's no way you're about to stop now and fumble with a condom. She probably won't care, right?"

            "You push your hips forward and sink your cock into [the_person.title]. She mumbles softly in her sleep."
            if the_person.get_opinion_score("vaginal sex"):
                the_person "... Fill me up... Mmph..."
                "She rolls her hips against yours, naturally encouraging you to push your full length into her."
                $ the_person.discover_opinion("vagianl sex")
            else:
                pass #No extra dialogue needed.
            "[the_person.possessive_title]'s pussy is warm, wet, and tight around your hard cock. You pause as you bottom out inside of her, enjoying the feeling."
            $ the_person.draw_person(position = "missionary", the_animation = missionary_bob, animation_effect_strength = 0.7)
            "You can't hold still for long. You start to move your hips, fucking [the_person.title] while trying to avoid any other movements that might wake her up."
            if renpy.random.randint(0,100) < 50 - 5*the_person.get_opinion_score("vaginal sex"):
                "You're so lost in the feeling of fucking [the_person.possessive_title] that you almost don't notice when her eyes flutter open."
                the_person "... Hmm... Ah... [the_person.mc_title]?"
                if the_person.effective_sluttiness("vaginal_sex") + 5*(the_person.get_opinion_score("being submissive") + the_person.get_opinion_score("vaginal sex")) >= 60 and not the_person.has_taboo("vaginal_sex"):
                    "She takes a moment to comprehend what's happening, then rests her head back on her pillow and moans."
                    the_person "Is this a dream? Ah... Mmmm..."
                    mc.name "Hey [the_person.title], I hoep you don't mind. I just really needed to take..."
                    "You thrust hard into her, emphasising each word."
                    mc.name "Care... Of..."
                    "Thrust, moan. Thrust, moan."
                    mc.name "This!"
                    if the_person.effective_sluttiness() >= the_person.get_no_condom_threshold():
                        the_person "Oh my god... Ah... Yes!"
                    else:
                        the_person "Yes! Ah... Are you... wearing a condom?"
                        if mc.condom:
                            mc.name "Of course I am. We have to be safe, right?"
                            the_person "Good... Keep fucking me [the_person.mc_title], I want you to keep fucking me!"
                        else:
                            mc.name "I couldn't wait, I just needed to get inside of you."
                            if the_person.break_taboo("condomless_sex"):
                                the_person "Oh no, you can't... We shouldn't... What if you..."
                                "She moans as you fuck her, despite her hesitations."
                                mc.name "It's a little late for that now, isn't it?"
                                if the_person.on_birth_control:
                                    the_person "Ah... Just... Be careful!"
                                else:
                                    the_person "Ah... Okay, just be careful! I'm not on the pill, we can't have any mistakes!"
                                    $ the_person.update_birth_control_knowledge()
                                    "She moans happily and relaxes underneath you, her last worry dismissed."
                            else:

                                "She moans happily as you fuck her."
                                the_person "It's fine, just... Ah... Be sure to pull out..."

                    call fuck_person(the_person, start_position = missionary, start_object = mc.location.get_object_with_name("bed"), skip_intro = True) from _call_fuck_person_98
                    $ the_report = _return
                    call sex_report_helper(the_person, the_report) from _call_sex_report_helper_4

                else:
                    "She takes a moment to comprehend what's happening, then she gasps and shakes her head."
                    the_person "Oh my god, what are we... what are you doing! Pull out!"
                    $ the_person.change_happiness(-15)
                    $ the_person.change_love(-7 + (2*the_person.get_opinion_score("being submissive")))
                    $ the_person.change_slut_temp(2 + the_person.get_opinion_score("being submissive") + the_person.get_opinion_score("vaginal sex"))
                    $ the_person.draw_person(position = "missionary")
                    "[the_person.title] pushes on your hips. You pull out of her warm pussy reluctantly."
                    mc.name "Hey, I was just... Checking in on you."
                    the_person "And you ended up fucking me? Oh my god [the_person.mc_title]..."
                    "You roll off of [the_person.possessive_title] and stand up. She pulls the covers up around herself and looks away."
                    the_person "You should go, okay? We don't... need to talk about this."
                    "You think about responding, but decide it's better to get out while you can. You stuff your hard cock back into your pants and back out of the room."
                return True

            else:
                "You expect [the_person.possessive_title] to open her eyes at any moment, but she seems to be sleeping soundly despite being filled up by your cock."
                "You're feeling more confident and speed up, thrusting in and out of her tight pussy. Soon she's dripping wet and moaning in her sleep."
                if the_person.get_opinion_score("vaginal sex"):
                    the_person "... Yes... Cock... More..."
                    "She murmurs, still unconcious"
                else:
                    pass #No extra dialogue needed.

                "Each stroke into her warm, wet slit draws you closer and closer to your climax. The risk of being caught only makes the experience more exciting."
                "It doesn't take long before you're at the very edge, just barely holding back from cumming."
                menu:
                    "Cum in your hand.":
                        call sleep_cum_hand(the_person) from _call_sleep_cum_hand_3
                        $ awake = _return

                    "Cum on her stomach." if the_person.effective_sluttiness():
                        call sleep_cum_stomach(the_person) from _call_sleep_cum_stomach
                        $ awake = _return

                    "Cum inside her." if the_person.effective_sluttiness() >= cum_inside_slut_requirement or mc.condom:
                        call sleep_cum_vagina(the_person) from _call_sleep_cum_vagina
                        $ awake = _return

                    "Cum inside her.\n{color=#ff0000}Requires:[fuck_slut_token]{/color} (disabled)" if the_person.effective_sluttiness() < cum_inside_slut_requirement and not mc.condom:
                        pass

            $ mc.condom = False #Make sure to take the condom off at the end of the encounter

        "Fuck her.\n{color=#ff0000}Requires:[fuck_slut_token]{/color} (disabled)" if the_person.outfit.vagina_available() and masturbating and the_person.effective_sluttiness() < fuck_slut_requirement:
            pass

        "Leave.":
            if masturbating:
                if the_person.outfit.tits_visible() and mc.focus <= 2:
                    "You move to put your cock back in your pants, but the sight of [the_person.possessive_title]'s naked tits are too much for you to say no to."
                    "You keep stroking off, unable to leave until you've finished what you've started."
                    call nightime_grope(the_person, masturbating) from _call_nightime_grope_4
                    $ awake = _return
                elif the_person.outfit.vagina_visible() and mc.focus <= 2:
                    "You move to put your cock back in your pants, but the sight of [the_person.possessive_title]'s naked pussy distracts you."
                    "You keep stroking off, unable to leave until you've finished what you've started."
                    call nightime_grope(the_person, masturbating) from _call_nightime_grope_5
                    $ awake = _return

                else:
                    if the_person.outfit.tits_visible() or the_person.outfit.vagina_visible():
                        "You give your cock a few more strokes, then force yourself to put your hard cock back into your pants."
                        "It takes a significant amount of willpower to tear yourself away from [the_person.possessive_title]'s hot body."
                    else:
                        "You give your cock a few more strokes, then reluctantly stuff it back into your underwear and zip up your pants."
                    "You back slowly out of the room, leaving [the_person.possessive_title] asleep and unaware of your visit."

    return awake

#Helper funcitons for all the sleep stuff where you cum on her. Returns True if she wakes up.
label sex_report_helper(the_person, the_report): #TODO: We use this in enough places that we should have some her orgasm versions
    if the_report.get("guy orgasms", 0) > 0 and the_report.get("girl orgasms", 0) >0:
        the_person "Wow, you weren't the only one who needed that, apparently."
        "You both take a moment, panting softly as you recover from your orgasms."
        mc.name "Well I'm feeling much better now [the_person.title]."
        the_person "Me too. Come by again if you need some more help, okay"
        mc.name "I'm not going to say no to that."
    elif the_report.get("guy orgasms", 0) > 0:
        the_person "There, all taken care of. Hope that helps [the_person.mc_title]."
        mc.name "I'm feeling much better. Thanks [the_person.title]."
        the_person "For you, any time."
        "You stuff your cock back in your pants and leave [the_person.possessive_title]'s bedroom."
    elif the_report.get("girl orgasms", 0) > 0:
        the_person "Wow, I guess I needed that even more than you did."
        $ the_person.change_obedience(-(2 + the_person.get_opinion_score("being in control")))
        the_person "Sorry [the_person.mc_title], I'll make sure to finish you off next time, okay?"
        mc.name "Next time, huh? I can get behind that."
    else:
        the_person "I'm sorry [the_person.mc_title]. I guess I need a little more practice."
        the_person "Maybe we can do this again later and I can make it up to you, okay?"
        mc.name "Sure, I'm not going to say no to that."
    "You stuff your cock back in your pants and leave [the_person.possessive_title]'s bedroom."
    return

label sleep_cum_hand(the_person):
    "You grunt softly as you climax, doing your best to cum into your hand instead of all over [the_person.title]."
    "When your orgasm has passed you take a moment to catch your breath, then back carefully out of her room."
    return False

label sleep_cum_face(the_person, straddle = False):
    $ awake = False
    $ the_person.cum_on_face()
    $ the_person.draw_person(position = "missionary") #Redraw whatever position we were in previously
    "You grunt softly as you climax, spraying your hot load in an arc onto [the_person.possessive_title]'s unsuspecting face."
    if the_person.get_opinion_score("drinking cum") > 0:
        "When the first splash of cum hits her face [the_person.title] opens her mouth."
        "You watch as she begins to unconciously lick up your sperm, even as you pulse more out onto her"
        $ the_person.discover_opinion("drinking cum")
    else:
        "[the_person.title] twitches in her sleep as pulse after pulse of cum splashes across her face."

    if renpy.random.randint(0,100) < 60 - 5*the_person.get_opinion_score("being covered in cum"): #TODO: Adjust chance based on opinion
        "A moment later she opens one eye - the one not welded shut by your cum - and locks eyes with you."
        if the_person.effective_sluttiness() + 5*(the_person.get_opinion_score("being submissive") + the_person.get_opinion_score("being covered in cum")) >= 60: #TODO: Cum based taboo stuff
            #She's suprised, but fine with it
            the_person "Oh my... [the_person.mc_title]? Ah..."
            mc.name "Sorry [the_person.title], I just needed some relief and you were..."
            "She wipes a puddle of cum away from her eye and blinks."
            the_person "Oh, it's fine. You obviously really needed it."
            if straddle:
                "You climb off of [the_person.title] and stand up beside her bed, stuffing your cock back in your pants."
            else:
                "You stuff your cock back in your pants, feeling relieved."

            if the_person.get_opinion_score("drinking cum") > 0:
                "[the_person.possessive_title] starts to tidy herself up as you leave, scooping your sperm up with a finger and then licking it clean."
            else:
                "[the_person.possessive_title] starts to clean herself up as you leave, wiping off your sperm with her bed sheets."



        else: #Not okay with it
            the_person "Oh my... [the_person.mc_title]? What did you just..."
            "She reaches up and brushes a hand over her face, feeling the warm puddles of cum you've put there."
            mc.name "Sorry [the_person.title], I just got a little carried away and..."
            the_person "And you finished on my face? I... I don't know what to say [the_person.mc_title]..."
            "Her eyes are locked on your cock, still hard despite the recent orgasm."
            mc.name "I didn't mean to, it just sort of... happened."
            $ the_person.change_happiness(-10)
            $ the_person.change_love(-3 + the_person.get_opinion_score("being covered in cum"))
            $ the_person.change_slut_temp(2 + the_person.get_opinion_score("being submissive") + the_person.get_opinion_score("being covered in cum"))
            the_person "I... You should go. This isn't right, you shouldn't be here..."
            if straddle:
                "You think about what to say, but realise the first thing to do is probably to get your cock out of her face."
                "You climb off of [the_person.title]'s bed and stuff your cock back into your pants."
            else:
                "You hurry to stuff your cock back in your pants."
            mc.name "Let's just pretend this never happened, okay? Just a mistake, no big deal."
            "She nods, but seems unconvinced. You hurry out of the room, leaving her to clean up."

        $ awake = True
    else:
        "Her eyes flutter briefly, despite being solidly welded closed by your cum."
        "She murmurs something, then rolls over. You breathe a sigh of relief and stuff your cock back in your pants."
        "You back out of the room slowly. You wonder how she'll react to waking up with a face full of mystery cum." #TODO: Add some events related to this. Maybe just an additional comment as an on-talk.
        $ the_person.change_slut_temp(2 + the_person.get_opinion_score("being submissive") + the_person.get_opinion_score("being covered in cum"))
    return awake

label sleep_cum_throat(the_person): #Always assumes you're standing up
    $ awake = False
    $ the_person.cum_in_mouth()
    $ the_person.draw_person(position = "missionary", special_modifier = "blowjob") #Position specific stuff
    "You thrust forward, pushing yourself as deep down [the_person.possessive_title]'s throat as you dare."
    "With one last grunt you climax, sending a blash of hot cum to the back of her mouth."

    if the_person.get_opinion_score("drinking cum") > 0:
        $ the_person.discover_opinion("drinking cum")
        "[the_person.title] reacts instinctively, drinking down your sperm as fast as she can manage even as she sleeps."
    else:
        "[the_person.title] coughs and sputters as you pump a few more pulses down her throat."

    if renpy.random.randint(0,100) < 50 - 5*the_person.get_opinion_score("drinking cum"): #TODO: Adjust chance based on opinion
        $ awake = True
        "As your orgasm passes you relax, pulling your cock out of her mouth."
        "You think you've gotten away with it when her eyes flutter open."
        if the_person.effective_sluttiness() + 5*(the_person.get_opinion_score("being submissive") + the_person.get_opinion_score("drinking cum")) >= 75 and not the_person.has_taboo("sucking_cock"): #Fine with it #TODO: Cum based taboo stuff
            if the_person.get_opinion_score("drinking cum") > 0:
                "[the_person.possessive_title] glances up at you, then swallows proudly. She rolls over and looks up at you from her back."
            else:
                "[the_person.possessive_title] glances up at you. She wipes her lips, clears her throat, then rolls over and looks up at you from her back."
            the_person "Whew... I'm feeling a little light headed... I do need to breath, you know."
            mc.name "You seemed to manage just fine. Sorry for waking you up, I came into check on you and..."
            "She waves her hand."
            the_person "It's fine, I know... Are you all better now?"
            "You nod, stuffing your satisfied cock back into your pants."
            the_person "Good. I think I'm going to need some time to recover, if that's okay."
            mc.name "Of course. Thanks for the help."
            "She smiles, and you back out of her room."

        else: #Not fine with it
            "Her eyes are locked on your dick for a moment, then she glances up at you wide-eyed."
            the_person "[the_person.mc_title]? I..."
            "She coughs, sputtering out the last mouthful of cum you had given her."
            mc.name "Hey [the_person.title]... I was just checking in on you..."
            "[the_person.possessive_title] sits up and bed, wiping her lips with the back of her hand."
            if the_person.has_taboo("sucking_cock"):
                the_person "Was I... giving you a blowjob in my sleep?"
                $ the_person.change_happiness(-15)
                $ the_person.change_love(-4 + the_person.get_opinion_score("drinking cum"))
                mc.name "Uh... Yeah, I guess you were."
                the_person "Oh my god... Nobody can know about this, okay [the_person.mc_title]? I thought it was a dream!"
                $ the_person.change_happiness(-15)
                $ the_person.change_love(-4 + the_person.get_opinion_score("drinking cum"))
                $ the_person.change_slut_temp(2 + the_person.get_opinion_score("being submissive") + the_person.get_opinion_score("drinking cum"))
                mc.name "I thought you were acting a little strange."
                the_person "You... You should go. It was just a dream, okay? I wasn't... I didn't mean to do anything."
                "You stuff your cock back into your pants."
                mc.name "I didn't mind, though. You were pretty good at it."
                $ the_person.break_taboo("sucking_cock")
                the_person "Oh god... I can't believe it."



            else:
                $ the_person.change_happiness(-15)
                $ the_person.change_love(-4 + the_person.get_opinion_score("being covered in cum"))
                $ the_person.change_slut_temp(2 + the_person.get_opinion_score("being submissive") + the_person.get_opinion_score("being covered in cum"))
                the_person "Did you just... Can you put that thing away?"
                "You stuff your cock back into your pants."
                mc.name "Oh, right... Maybe I'll just go, okay?"
                the_person "I... I think that's a good idea."
            "You take your chance and hurry out of [the_person.title]'s room."

    else:
        "As your orgasm passes you relax and pull your cock out of her mouth. It drags out a line of spit and cum as you pull back."
        $ the_person.change_slut_temp(2 + the_person.get_opinion_score("being submissive") + the_person.get_opinion_score("being covered in cum"))
        if the_person.get_opinion_score("drinking cum") > 0:
            "She smiles happily and rolls over, swallowing down the last few drops of your sperm. It feels like she should be thanking you."
        else:
            "She mumbles something and rolls over, her sleep undisturbed by the whole ordeal. Somehow you've gotten away with it."
        "You back quietly out of the room, wondering what she'll think when she wakes up with her breath smelling of mystery cum."
    return awake

label sleep_cum_tits(the_person, straddle = False):
    $ awake = False
    $ the_person.cum_on_tits()
    $ the_person.draw_person(position = "missionary")
    if the_person.outfit.tits_available():
        "You grunt softly as you climax, spraying your load all over her chest."
    else:
        "You grunt softly as you climax, spraying your load all over her chest and [bra_item.display_name]."

    if the_person.get_opinion_score("being covered in cum") > 0:
        "[the_person.possessive_title] moans as you cum all over her. She mutters quietly in her sleep."
        the_person "Yes daddy... Mmph... Cover me..."
        $ the_person.discover_opinion("being covered in cum")
    else:
        pass #No extra dialogue needed

    if renpy.random.randint(0,100) < 40 - 5*the_person.get_opinion_score("being covered in cum"):
        $ awake = True
        "She reaches up, brushing her chest and running her fingers through your cum."
        the_person "Hmm?"
        "Her eyes flutter open, and she takes a moment to absorb the situation."
        if the_person.effective_sluttiness() + 5*(the_person.get_opinion_score("being submissive") + the_person.get_opinion_score("being covered in cum")) >= 50:
            the_person "Oh... Hello [the_person.mc_title]. What did I miss?"
            if the_person.get_opinion_score("drinking cum") > 0:
                "She idly runs a finger between her cleavage, covering it in cum. She looks at you and licks it clean while you talk."
            else:
                "She idly runs a finger between her cleavage, spreading your cum around."
            mc.name "Hey [the_person.title], I was just checking in on you and... Well, I just couldn't resist."
            "[the_person.possessive_title] shrugs."
            the_person "No harm in it, I suppose. I'm going to need to get cleaned up though."
            if straddle:
                mc.name "Oh, right..."
                "You climb off of [the_person.title] and stuff your cock back into your pants."
            else:
                "You stuff your cock back into your pants."
            mc.name "I'll leave you to it, then."
            the_person "Come by any time."
            "You back out of her room, leaving her to clean your cum off of her chest."
        else:
            if straddle:
                the_person "[the_person.mc_title]? What... What are you doing on top of me?"
                "Her eyes glance down to her chest, splattered with cum, then at your still-hard cock."
                "You hurry to climb off of her bed."
            else:
                the_person "[the_person.mc_title]? What... What did you do?"
                "Her eyes glance down to her chest, splattered with cum, then at your still-hard cock."
            mc.name "I was... Just checking in on you. When I saw you, I just couldn't resist..."
            $ the_person.change_happiness(-10)
            $ the_person.change_love(-3 + the_person.get_opinion_score("being covered in cum"))
            the_person "You... You should go, okay? We don't need to talk about this."
            mc.name "It's not what..."
            the_person "Just go. Please."
            "You take the hint and stuff your cock back into your pants, hurrying out of her bedroom."

    else:
        if the_person.get_opinion_score("being covered in cum") > 0:
            "She reaches up lazily and brushes her chest, spreading your semen around in her sleep."
            the_person "Thank you daddy..."
        else:
            "She murmurs something, then rolls over in bed."
            if straddle:
                "You breathe a sigh of relief, then carefully get off the bed and stuff your cock back into your pants."
            else:
                "You breathe a sigh of relief and stuff your cock back in your pants."
            "You back out of the room slowly. You wonder how she'll react to waking up with her tits covered in mystery cum." #TODO: Events. It doesn't take Sherlock to solve this one.
    return awake

label sleep_cum_stomach(the_person): #Note: always assumes you're stradling her
    $ awake = False
    $ the_person.cum_on_stomach()
    $ the_person.draw_person(position = "missionary")

    "You grunt softly as you climax, splattering your load over [the_person.title]'s stomach."

    if the_person.get_opinion_score("being covered in cum") > 0:
        "[the_person.possessive_title] moans as you cum on her. She mutters quietly in her sleep."
        the_person "Yes daddy... Mmph... Cover me..."
        $ the_person.discover_opinion("being covered in cum")
    else:
        pass #No extra dialogue needed

    if renpy.random.randint(0,100) < 30 - 5*the_person.get_opinion_score("being covered in cum"):
        $ awake = True
        "She mumbles, and after a brief moment of suspense her eyes flutter open."
        if the_person.effective_sluttiness() + 5*(the_person.get_opinion_score("being submissive") + the_person.get_opinion_score("being covered in cum")) >= 50:
            "[the_person.possessive_title] glances at you, then at the pool of cum on her stomach."
            the_person "Oh... I see."
            mc.name "[the_person.title], I was just checking in on you and..."
            the_person "No, no I think I understand. It's fine, really."
            if the_person.get_opinion_score("drinking cum") > 0:
                "She reaches down and runs a finger through your sperm, then brings the it to her lips and licks it clean."
                the_person "Mmm, I don't really mind. Do you need anything else, or can I get cleaned up?"
            else:
                the_person "Do you need anything else, or can I get cleaned up?"
            mc.name "You can get cleaned up, I'll leave you to it. Talk to you later."
            "You stuff your cock back into your pants and back out of the room as [the_person.possessive_title] sits up in bed."

        else:
            "[the_person.possessive_title] looks over at you. Her eyes go wide when she sees your throbbing cock, still in your hands."
            mc.name "Oh, hey [the_person.title], I..."
            the_person "Why is your... thing out? Is this..."
            "She notices the pool of warm cum on her stomach."
            $ the_person.change_happiness(-10)
            $ the_person.change_love(-3 + the_person.get_opinion_score("being covered in cum"))
            mc.name "I was just checking in on you and..."
            the_person "And you jerked off onto me? Oh my god [the_person.mc_title], this isn't right!"
            mc.name "I couldn't resist, you were looking so good."
            "She covers her face with her hands and sighs. You stuff your cock back into your pants and take a few steps towards the exit."
            the_person "You should go, okay? This never happened, understood?"
            mc.name "Yes [the_person.title]."
            "You take your chance and exit in a hurry, leaving [the_person.possessive_title] to figure out how to clean up your cum."
    else:
        if the_person.get_opinion_score("being covered in cum") > 0:
            "She reaches down and brushes her fingers over the puddles of cum, spreading it around in her sleep."
            the_person "... Thank you daddy..."
        else:
            "She mumbles something, but after a brief moment of suspense seems to still be asleep."
        "You breathe a sigh of relief and stuff your cock back in your pants."
        "As you back out of the room you wonder how she'll react to waking up covered in mystery cum."
    return awake

label sleep_cum_vagina(the_person):
    $ awake = False
    if not mc.condom:
        $ the_person.cum_in_vagina()
        $ the_person.draw_person(position = "missionary")

    $ wake_chance = 40
    if mc.condom:
        "You blow your load into [the_person.possessive_title]'s pussy, constrained only by a thin layer of latex."
        $ wake_chance += -10 #Less likely to wake up if you cum in a condom, although the same as if she loves creampies (the perfect dream!)
    else:
        "You grunt softly as you climax, blowing your load into [the_person.possessive_title]'s raw pussy."
        $ wake_chance += -5*the_person.get_opinion_score("creampies")

    if renpy.random.randint(0,100) < wake_chance - 5*the_person.get_opinion_score("creampies"):
        $ awake = True
        "She shift in bed, then blinks and opens one eye sleepily."
        the_person "[the_person.mc_title]? What are you doing here? I..."
        "[the_person.possessive_title] lifts her head and looks down, realising you're inside of her."
        if the_person.effective_sluttiness() + 5*(the_person.get_opinion_score("being submissive") + the_person.get_opinion_score("creampies")) > 70 and not the_person.has_taboo("vaginal_sex"):
            the_person "Oh... that's what I was dreaming about."
            "She puts her head back and sighs happily."
            the_person "Thank you [the_person.mc_title]. Mmm..."
            mc.name "It's my pleasure."
            the_person "Wait, are you... wearing a condom?"
            if mc.condom:
                mc.name "Of course I am."
                if the_person.has_taboo("condomless_sex"):
                    "She breathes a loud sigh of relief."
                    the_person "Okay, good. That's good."
                else:
                    the_person "That's probably a good idea. Good thinking."
            else:
                mc.name "I didn't have time, I just needed to fuck you so badly."
                if the_person.has_taboo("condomless_sex"):

                    if the_person.wants_creampie():
                        the_person "Oh, okay. I guess it's already done, so it doesn't matter."
                        the_person "You can't always cum inside me though, okay? What if I get pregnant?"
                    else:
                        if the_person.on_birth_control:
                            the_person "Oh no [the_person.mc_title], what if my birth control doesn't work?"
                            $ the_person.update_birth_control_knowledge()
                        else:
                            the_person "Oh [the_person.mc_title], what have you done? What if I get pregnant?"
                    mc.name "I'm sure it'll be fine, don't worry about it."
                    "She seems unconvinced, but let's the subject drop."
                    $ the_person.break_taboo("condomless_sex")

                else:
                    if the_person.wants_creampie():
                        "She moans softly."
                        the_person "I can feel it... It's so warm."
                    else:
                        "She sighs."
                        the_person "Oh [the_person.mc_title], you shouldn't be cumming in me. You know that."
                        mc.name "Well, it's a little late now."
                        the_person "Yeah, I guess it is."

            if mc.condom:
                "You pull out of [the_person.possessive_title]'s pussy, all of your cum trapped inside of the ballooned tip of your condom."
            else:
                "You pull out of [the_person.possessive_title]'s pussy. A small stream of cum follows, dripping down her inner thigh."

            the_person "So, are you feeling satisfied?"
            mc.name "Yeah, I think that was just what I needed."
            "You get up from [the_person.title]'s bed, stuffing your cock back into your pants."
            the_person "Good, that's what I like to hear. Talk to you later, okay?"
            "You back up towards the door, taking one last peak into the room before you close the door."
            if the_person.get_opinion_score("bareback sex") > 0 and the_person.get_opinion_score("creampies") > 0 and not mc.condom:
                "[the_person.possessive_title] lifts her knees up to her chest and holds them close, keeping all of your cum inside of her pussy."
                the_person "Mmmm, it's so deep..."
            else:
                "[the_person.possessive_title] sighs and rolls over, pulling her blankets back around her."

        else:
            the_person "You're... inside of me."
            mc.name "Hey [the_person.title]... I just couldn't resist."
            the_person "You can't... We can't have sex [the_person.mc_title], it's not right! Pull out, we can finish some other way."
            mc.name "Well, it's a little late for that..."
            "She gasps."
            the_person "You... already came? Please tell me you're wearing a condom!"
            if mc.condom:
                mc.name "Of course. You don't want to get knocked up, do you?"
                if the_person.get_opinion_score("bareback sex") > 0 and the_person.get_opinion_score("creampies") > 0:
                    the_person "Oh fuck, I do... But not by you!"
                else:
                    the_person "Of course not!"
                mc.name "Well you're fine then, okay?"
                $ the_person.break_taboo("vaginal_sex")
            else:
                mc.name "Well... I wasn't really thinking straight and may have forgot."
                the_person "You're kidding, right? What if you got me pregnant?"
                mc.name "Are you on the pill?"
                if the_person.on_birth_control:
                    the_person "I am, but what if it doesn't work?"
                else:
                    the_person "No! You came inside me without any protection!"
                $ the_person.update_birth_control_knowledge()
                mc.name "I'm sure it'll be fine. Try not to overreact, okay?"
                $ the_person.break_taboo("vaginal_sex")
                $ the_person.break_taboo("condomless_sex")

            if mc.condom:
                "You pull out of [the_person.possessive_title]'s pussy, all of your cum trapped inside of the ballooned tip of your condom."
            else:
                "You pull out of [the_person.possessive_title]'s pussy. A small stream of cum follows, dripping down her inner thigh."
            the_person "You... should go. You're finished, right?"
            mc.name "Yeah, I'm feeling pretty satisfied."
            "You stuff your cock back in your pants and retreat out of the room."

    else:
        if the_person.get_opinion_score("creampies") > 0 and not mc.condom:
            the_person "... So full..."
            "She sighs happily, enjoying a pussy full of cum even when she's asleep."
        else:
            "She moans and shifts underneath you, but doesn't wake up."

        "You pull out, trying to avoid any extra movements that might alert [the_person.title]."
        if not mc.condom:
            "A small stream of your cum follows after your cock as you clear her pussy, drippling down her inner thigh."

        "You back up off of her bed and stand up, stuffing your cock back in your pants before backing slowly out of the room."
        "You wonder when, or if, she'll notice she has a pussy full of mystery cum when she wakes up."

    return awake

label work_walk_in_label(the_person): #Walk into the room and find someone masturbating (or maybe on talk instead?)
    #TODO: Include some references to masturbating opinion
    $ the_person.change_arousal(50, add_to_log = False)
    $ the_person.change_energy(-25, add_to_log = False)
    $ the_person.draw_person(position = "sitting")
    "You approach [the_person.title] from behind while she is sitting at her desk."
    if the_person.effective_sluttiness() < 40: #She was masturbating, but is embarrassed about it.
        mc.name "[the_person.title], I..."
        the_person "Ah!"
        "She yelps and nearly falls out of her chair. When she turns around her cheeks are flush and her breathing is quick."
        the_person "Oh my god, I... I'm... You nearly gave me a heart attack!"
        mc.name "Sorry about that, I didn't mean to startle you. Is everything alright?"
        the_person "Of course! I was just... Doing work. I was very focused on my work, and you startled me, that's all..."
        $ the_item = the_person.outfit.get_lower_top_layer()
        if the_item is None:
            "You notice [the_person.possessive_title] trying to inconspicuously wipe her hand off on her thigh as you talk."
        else:
            "You notice [the_person.possessive_title] trying to inconspicuously wipe her hand off on her [the_item.display_name] as you talk."
        "She crosses her legs, face turning beet red."
        the_person "Is there... something you wanted to talk to me about, [the_person.mc_title]?"
        menu:
            "Let it go.":
                "You shrug and ignore whatever [the_person.title] is trying to hide."


            "Demand to know what she was doing." if the_person.obedience >= 120:
                mc.name "There is, now. What were you just doing [the_person.title]?"
                the_person "I... I told you, I was working."
                "She shuffles nervously in her chair."
                mc.name "No you weren't. I already know what you were doing, I just don't like you lying to me."
                #TODO: Have other girls in the room chime in.
                the_person "I... was... touching myself. I'm sorry, I know I should have waited until I was at home."
                "Once [the_person.possessive_title] has started talking she begins to speed up, babbling out excuses."
                the_person "And I absolutely shouldn't have been doing it at my desk. I'm sorry, it won't happen again."
                menu:
                    "Praise her.":
                        "You wave your hand and smile."
                        mc.name "Calm down, you haven't done anything wrong."
                        the_person "I haven't? I mean, I was just..."
                        mc.name "Let me explain. What were you doing before you started to masturbate?"
                        the_person "Well, I was reading through a report about our products and..."
                        mc.name "Have you finished reading that report?"
                        "She shakes her head."
                        the_person "No, I'm sorry [the_person.mc_title]. I was distracted by some of the effect descriptions."
                        mc.name "Exactly. You were distracted and you weren't getting any work done, so you did what you could to remove the distraction."
                        the_person "I guess you could say that..."
                        mc.name "I need my employees focused, so if you feel \"distracted\" again I expect you to solve the problem."
                        "She's still blushing, but nods obediently."
                        $ the_person.change_slut_temp(3)
                        the_person "Okay [the_person.mc_title], I will. Is there anything else you wanted to talk about?"

                    "Scold her.":
                        mc.name "Frankly, this just isn't acceptable [the_person.title]."
                        the_person "I know, I'm so sorry. I promise my... urges will never get in the way of work again."
                        mc.name "You're a grown woman, and I expect you to act like it. Not like a horny teenager, fingering herself at her own desk."
                        "[the_person.title] looks down at her lap in shame."
                        the_person "I'm sorry..."
                        mc.name "Look at me."
                        "She jerks her head up to look you in the eye."
                        mc.name "Tell me what you're sorry for."
                        the_person "I'm... I'm sorry for touching myself..."
                        "You hold up your hand and correct her."
                        mc.name "\"For fingering your pussy.\""
                        the_person "...For fingering my pussy at work."
                        mc.name "What were you acting like?"
                        "She clearly wants to look away, look anywhere but into your eyes, but her obedience holds her in place."
                        the_person "...A horny highschool slut, [the_person.mc_title]."
                        mc.name "I expect you to shape up, or I'm going to have to start treating you like one."
                        $ the_person.change_obedience(2)
                        $ the_person.change_slut_temp(1)
                        if office_punishment.is_active():
                            menu:
                                "Punish her for her inappropriate behaviour.":
                                    mc.name "Of course, this will also be going on your record. There may be furthur punishment for this inappropriate behaviour"
                                    $ the_person.add_infraction(Infraction.inappropriate_behaviour_factory())

                                "Let it go.":
                                    pass

                        else:
                            "[the_person.possessive_title] nods silently."
                        the_person "Did... you want to talk about anything else?"

            "Demand to know what she was doing.\nRequires: 120 Obedience (disabled)" if the_person.obedience < 120:
                pass

        call talk_person(the_person) from _call_talk_person_15



    elif the_person.effective_sluttiness() < 60: #She was masturbating and admits it
        the_person "Mmph..."
        "You're about to say something when you hear her moan softly, obviously trying to stifle the sound."
        $ top_item = the_person.outfit.get_lower_top_layer()
        if top_item:
            "You take a quiet step closer. She has one hand between her legs and underneath her [top_item.display_name], subtley rubbing her crotch."
        else:
            "You take a quiet step closer. She has one hand between her legs, subtley rubbing her crotch."

        menu:
            "Interrupt her.":
                mc.name "Having a good time [the_person.title]?"
                "[the_person.possessive_title] yelps and nearly falls out of her chair."
                the_person "Ah! Oh my god, [the_person.mc_title], I nearly had a heart attack!"
                mc.name "Sorry about that. I hope I wasn't interrupting anything."
                $ the_item = the_person.outfit.get_lower_top_layer()
                if the_item is None:
                    "[the_person.possessive_title] swivels her chair around to face you, wiping her hand off onto her [the_item.display_name]."
                else:
                    "[the_person.possessive_title] swivels her chair around to face you, wiping her hand off onto her thigh."
                $ the_person.change_slut_temp(1)
                the_person "I, was just... relieving some tension. Have you read some of our product reports?"
                the_person "They really got my motor running and I couldn't focus."
                "She shrugs."
                the_person "I think that scare you gave me has killed the mood though, so that problem is solved."
                the_person "Did you need to talk to me about something?"


            "Just watch.":
                "You stop a few steps behind [the_person.title]'s chair, watching and listening as she touches herself."
                the_person "Mmm... Ah..."
                "She slouches down into her chair, spreading her legs wider."
                the_person "Ah... Keep it quiet... Ah..."
                if top_item:
                    "Her breathing is getting louder, and you can now hear the faint wet sounds as she fingers her pussy underneath her [top_item.display_name]."
                else:
                    "Her breathing is getting louder, and you can now hear the faint wet sounds as she fingers her pussy."
                "Her pace quickens, and she pushes herself over the edge."
                $ the_person.draw_person(position = "sitting", emotion = "orgasm")
                the_person "Ah! Ah... Ah..."
                "[the_person.possessive_title] slumps in her chair, panting quietly. After taking a moment to recover she sits up and glances around."
                $ the_person.draw_person(position = "sitting")
                $ the_person.reset_arousal()
                "She freezes when she sees you, standing just behind her."
                the_person "... I... Hello [the_person.mc_title]. How... How long were you standing there?"
                mc.name "The whole time."
                $ the_person.discover_opinion("public sex")

                if the_person.get_opinion_score("public sex") < 0: #She's mortified
                    the_person "Oh my god, I... I'm sorry [the_person.mc_title]! I just..."
                    the_person "I didn't think anyone would notice, and I was getting so distracted."
                    mc.name "Take a breath, it's fine. If I was angry I wouldn't have just watched."
                    "Her cheeks have turned beet red. She looks away from you and nods."
                    the_person "It'll never happen again. Sorry."
                    the_person "Is there something you wanted to talk about, or can I go find someplace quiet to die of embarassment?"
                elif the_person.get_opinion_score("public sex") == 0: #Normal
                    the_person "Right... Well, I guess you can count that as my lunch break."
                    the_person "I was reading some of our case studies. They get very... descriptive."
                    the_person "I couldn't focus, so I thought I would just... you know."
                    mc.name "Finger yourself in the middle of my office."
                    the_person "Well... Yeah, basically. I think it's worked, I feel like I can focus again."
                    the_person "Is there something you wanted to talk about?"
                else: #Turned on
                    the_person "The whole time? You were watching me while I... I..."
                    $ the_person.change_arousal(15 * the_person.get_opinion_score("public sex"))
                    "She moans, instinctively biting her lower lip."
                    the_person "Fuck... I just took care of this..."
                    the_person "Did you need to talk about something? I might... I might need to go for another round before I can focus on work again."

                $ the_person.change_slut_temp((the_person.get_opinion_score("public sex") * 2) + 1)

        if office_punishment.is_active():
            menu:
                "Punish her for her inappropriate behaviour.":
                    mc.name "That was completely inappropriate for the office. I'm going to have to mark this down on your record."
                    the_person "I... Come on [the_person.mc_title], can't you let this one go?"
                    mc.name "I wish I could, but the rules are the rules. Everyone has to follow them."
                    $ the_person.add_infraction(Infraction.inappropriate_behaviour_factory())
                    "She sighs, but nods her understanding."

                "Let it go.":
                    pass

        else:
            pass
        the_person "Did... you want to talk about anything else?"

        call talk_person(the_person) from _call_talk_person_16

    else: #She was masturbating, and she doesn't want to stop.
        the_person "Ah... Ah... Mmph..."
        "You hear her panting softly under her breath."
        $ the_item = the_person.outfit.get_lower_top_layer()
        if the_item is None:
            "You take another step closer and you can see that she has her legs spread wide, one hand underneath her [the_item.display_name] fingering her cunt."
        else:
            "You take another step closer and you can see that she has her legs spread wide, one hand between them fingering her cunt."

        "She must have heard you approaching, because she spins her chair around to face you."
        $ the_person.change_arousal(40, add_to_log = False) #ie. she starts very horny
        the_person "[the_person.mc_title], I'm... I just need a moment. I'm sorry, I just really need to cum!"
        "She doesn't stop playing with herself."
        menu:
            "Let her finish.":
                mc.name "Well, hurry up then."
                if the_person.get_opinion_score("public sex") < 0:
                    the_person "I... With you right here?"
                    mc.name "You were already touching yourself in the middle of the day, in my office."
                    mc.name "If you can do that, you can cum in front of me."
                    "She nods."
                    the_person "I... I'll do my best..."
                    if office_punishment.is_active():
                        menu:
                            "Punish her for her inappropriate behaviour.":
                                mc.name "This will go on your record, obviously. I may have to punish you for your inappropriate behaviour."
                                the_person "I... Ah, understand [the_person.mc_title], but I really need this! I'll accept whatever punishment you give me!"
                                $ the_person.add_infraction(Infraction.inappropriate_behaviour_factory())

                            "Let it go.":
                                pass

                    else:
                        pass
                    "She rubs her pussy some more, trying to bring herself to orgasm. She turns her head to the side to avoid making eye contact."
                    "After a few minutes of her moaning quietly to herself she looks back at you and shakes her head."
                    the_person "I don't... I don't know if I can finish with you watching like this..."
                    menu:
                        "Make her cum.":
                            mc.name "If you can't make yourself cum, I'll have to do it for you."
                            the_person "No, I can... I'll feel fine in a little bit, I..."
                            mc.name "I can't have you distracted all day just because you never learned how to get yourself off."
                            the_person "I know how to, I just don't like being watched..."
                            mc.name "I have no such issues. Leave it to me."
                            $ the_person.add_situational_obedience("event", 20, "He promised to make me cum, I'll do what he tells me to do.")
                            call fuck_person(the_person, private = False) from _call_fuck_person_90
                            $ the_person.clear_situational_obedience("event")
                            $ the_report = _return
                            if the_report.get("girl orgasms", 0) > 0:
                                $ the_person.draw_person(position = "sitting", emotion = "orgasm")
                                "[the_person.possessive_title] collapses back into her chair and sighs happily."
                                mc.name "There, are you going to be able to focus now?"
                                "She nods obediently."
                                $ the_person.change_obedience(3 + the_person.get_opinion_score("being submissive"))
                                the_person "Yes [the_person.mc_title], thank you. What do you want to talk about?"
                            else:
                                $ the_person.draw_person(position = "sitting")
                                "[the_person.possessive_title] sits back down in her chair."
                                the_person "I told you, it just wasn't going to work..."
                                the_person "I'll be fine. What did you want to talk about?"

                        "Make her stop.":
                            mc.name "Then wait until later. I'm here to talk to you, not watch you practice masturbating."
                            "She pulls her hand out of her pussy and sits up, blushing."
                            $ the_person.change_obedience(1)
                            the_person "Right. Sorry [the_person.mc_title]. What did you want to talk about?"

                elif the_person.get_opinion_score("public sex") > 0:
                    "She moans and pants as she masturbates, legs still wide for you to watch."
                    if office_punishment.is_active():
                        menu:
                            "Punish her for her inappropriate behaviour.":
                                mc.name "This will go on your record, obviously. I may have to punish you for your inappropriate behaviour."
                                the_person "I... Ah, understand [the_person.mc_title], but I really need this! I'll accept whatever punishment you give me!"
                                $ the_person.add_infraction(Infraction.inappropriate_behaviour_factory())

                            "Let it go.":
                                pass

                    else:
                        pass
                    the_person "Do you like... watching me, [the_person.mc_title]?"
                    the_person "Is watching me finger myself making your dick hard? Thinking about is making me so wet!"
                    "She moans again, arching her back and lifting her hips away from her office chair. There's a large wet spot left where she use to be sitting."
                    $ the_person.draw_person(position = "sitting", emotion = "orgasm")
                    the_person "Fuck... Watch me cum [the_person.mc_title]! I'm cumming!"
                    "[the_person.title]'s whole body quivers, her hips thrusting out with each pulse of her climax."
                    "She holds perfectly still for a moment, back still arched, as her pussy spasms a few last times."
                    "Then she collapses down into her chair, panting loudly."
                    the_person "I... I'm going to need a minute. I... Oh my god..."
                    $ the_person.draw_person(position = "sitting")
                    "You wait patiently until [the_person.title] is able to pull herself up in her chair and look you in the eyes."
                    mc.name "Better?"
                    "She nods, almost meekly now."
                    the_person "Much, I didn't realise how badly I needed that."
                    the_person "Now, what did you want to talk about?"
                    $ the_person.change_slut_temp(the_person.get_opinion_score("public sex")*2)
                    $ the_person.reset_arousal()

                else:
                    the_person "Gladly! Ah!"
                    "[the_person.possessive_title] cups a breast with one hand while she fingers herself with the other."
                    if office_punishment.is_active():
                        menu:
                            "Punish her for her inappropriate behaviour.":
                                mc.name "This will go on your record, obviously. I may have to punish you for your inappropriate behaviour."
                                the_person "I... Ah, understand [the_person.mc_title], but I really need this! I'll accept whatever punishment you give me!"
                                $ the_person.add_infraction(Infraction.inappropriate_behaviour_factory())

                            "Let it go.":
                                pass

                    else:
                        pass
                    "She moans and pants as she stares into your eyes, right up until the moment she cums."
                    "Her breath catches in her throat and she closes her eyes as she begins to climax."
                    $ the_person.draw_person(position = "sitting", emotion = "orgasm")
                    the_person "Oh... Oh god..."
                    "She arches her back, lifting her hips away from her office chair where she has left a noticeable wet spot."
                    the_person "Ahh!"
                    "Her body quivers for a moment, then she slumps back into her chair and pants."
                    the_person "Sorry... about the wait. I just... ah, couldn't stop thinking about sex."
                    mc.name "Feeling better now?"
                    $ the_person.change_slut_temp(1)
                    "She takes a deep breath and nods, pulling herself up to sit properly in her chair."
                    the_person "I think so [the_person.mc_title]. Did you need to talk to me?"
                    $ the_person.reset_arousal()

                $ the_person.discover_opinion("public sex")


            "Demand she stops.":
                mc.name "I don't have a moment. Cut it out, I need to talk to you."
                if the_person.obedience - 100 > ((the_person.arousal/2) + 10*the_person.get_opinion_score("public sex") + 10*the_person.get_opinion_score("masturbating")):
                    "[the_person.possessive_title] seems disappointed, but she puts her legs together and sits up straight in her chair."
                    "She continues to rub her thighs together in an attempt to stimulate herself while you talk."
                    if office_punishment.is_active():
                        menu:
                            "Punish her for her inappropriate behaviour.":
                                mc.name "This will still be going on your record, of course."
                                the_person "It was just for a moment though [the_person.mc_title]... Can't I get away with it this one time?"
                                "You shake your head."
                                mc.name "If I start making exceptions every girl in this office will be fucking herself at her desk when they should be working."
                                "[the_person.title] sighs, but nods her understanding."
                                $ the_person.add_infraction(Infraction.inappropriate_behaviour_factory())

                            "Let it go.":
                                pass

                    else:
                        pass
                else: #She ignores you
                    "She pants and shakes her head, refusing to stop."
                    if the_person.get_opinion_score("public sex") > 0:
                        $ the_person.discover_opinion("public sex")
                        the_person "I can't stop, not with you watching me!"
                        "She rubs herself faster, legs spread wide for you to watch."
                        the_person "Watch me cum [the_person.mc_title]! I'm cumming!"
                    elif the_person.get_opinion_score("masturbating") > 0:
                        $ the_person.discover_opinion("masturbating")
                        the_person "I can't stop, touching myself just feels too good!"
                        "She rubs herself faster, pumping her fingers in and out of her dripping wet pussy."
                    else:
                        the_person "I'm so, so close! Just... Wait, okay?"
                        "She leans back and continues to finger herself."

                    $ the_person.draw_person(position = "sitting", emotion = "orgasm")
                    the_person "Oh... Oh god..."
                    "She arches her back, lifting her hips away from her office chair where she has left a noticeable wet spot."
                    the_person "Ahh!"
                    "Her body quivers for a moment, then she slumps back into her chair and pants."
                    if office_punishment.is_active():
                        menu:
                            "Punish her for disobedience.":
                                mc.name "I hope that was worth it, because I'm going to have to write you up for disobedience now."
                                "She sighs and shrugs."
                                the_person "It was worth it, that felt so good..."
                                $ the_person.add_infraction(Infraction.disobedience_factory())

                            "Let it go.":
                                pass

                    $ the_person.reset_arousal()
                    $ the_person.change_slut_temp(3)
                    $ the_person.change_obedience(-2)
                    the_person "Now, what did you need to talk about?"

            "Offer to help.":
                mc.name "Let's speed things up. I'll give you a hand."
                "She eyes you up and down as she considers, before nodding her approval."
                $ the_person.add_situational_obedience("event", 10, "He promised to make me cum, I'll do what he tells me to do.")
                call fuck_person(the_person, private = False) from _call_fuck_person_91
                $ the_report = _return
                $ the_person.clear_situational_obedience("event")
                if the_report.get("girl orgasms", 0) > 0:
                    $ the_person.draw_person(position = "sitting", emotion = "orgasm")
                    "[the_person.possessive_title] collapses back into her chair and sighs happily."
                    mc.name "There, are you going to be able to focus now?"
                    "She nods obediently."
                    $ the_person.change_obedience(3 + the_person.get_opinion_score("being submissive"))
                    the_person "Yes [the_person.mc_title], thank you. What do you want to talk about?"
                else:
                    $ the_person.draw_person(position = "sitting")
                    "[the_person.possessive_title] sits back down in her chair."
                    the_person "I think... you've just made things worse."
                    $ mc.business.change_team_effectiveness(-5)
                    the_person "I'll have to deal with this later. What did you want to talk about [the_person.mc_title]?"
        call talk_person(the_person) from _call_talk_person_17
    $ clear_scene()
    return

label new_insta_account(the_person): #TODO: decide if we want to have some sort of dialogue accompanying these.
    $ the_person.special_role.append(instapic_role)
    if the_person.love >= 15:
        the_person "Hey [the_person.mc_title]! Oh, you'll probably be interested in this."
        the_person "I've started an InstaPic account, you should follow me! I'm just starting out, but I think I'm figuring it all out!"
        $ the_person.event_triggers_dict["insta_known"] = True
    call talk_person(the_person) from _call_talk_person_27
    return

label new_dikdok_account(the_person):
    if the_person.love >= 15:
        the_person "Hey [the_person.mc_title]! Oh, you'll probably be interested in this. I've started a DikDok channel."
        the_person "You should follow me! I'm just starting out but I think my videos are pretty great."
        $ the_person.event_triggers_dict["dikdok_known"] = True
    $ the_person.special_role.append(dikdok_role)
    call talk_person(the_person) from _call_talk_person_28
    return

label new_onlyfans_account(the_person):
    if the_person.love >= 30 and the_person.effective_sluttiness() >= 40 and not the_person.has_role(girlfriend_role):
        the_person "Hey [the_person.mc_title], I thought you might want to know..."
        the_person "I'm starting up an OnlyFanatics account. I think it might be a fun way for me to make a little extra money."
        the_person "You should check me out some time, if you don't think that would be too weird."
        $ the_person.event_triggers_dict["onlyfans_known"] = True
    $ the_person.special_role.append(onlyfans_role)
    call talk_person(the_person) from _call_talk_person_29
    return
