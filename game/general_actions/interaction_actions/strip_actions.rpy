
label pay_strip_scene(the_person):
    # TODO: Figure out where this scene should go, since this file should be a pure role-define section.
    #A loop where someone strips if you pay them. Not nessicarily limited to the Lily-MC relationship.
    #Concept: tell the girl what position to stand in and ask her to take things off for you. If her outfit is conservative she'll strip for free, when it starts to get slutty she'll want extra cash.
    #High obedience will sub in for sluttiness; an obedient girl will strip just because you ask.
    #Compliment, insult, etc. to change some of her stats.

    #Requirements: Person can be told to stand in a few different positions. Some are unlocked at higher sluttiness.
    #Requirements: Person can be asked to take off clothing.
    #Requirements: Some they will strip off on their own.
    #Requirements: Person will demand some amount of $$$ while stripping if they feel it's slutty.
    #Requirements: Person will have different descriptions of stripping/dancing depending on sluttiness.
    #Optional: Some way to ask the person to change into a different outfit.
    #Optional: Way to progress from strip tease to sex and/or mastribation.

    $ pose_list = [["Turn around","walking_away"],["Turn around and look back","back_peek"],["Be flirty","stand2"],["Be casual","stand3"],["Strike a pose","stand4"],["Move your hands out of the way","stand5"],["Hands down, ass up.","standing_doggy"]]
    $ pose_dances = {} #Dict that maps poses to animations that look good for them.


    $ picked_pose = the_person.idle_pose #She starts in her idle pose (which is a string)
    $ rand_strip_desc = renpy.random.randint(0,3) #Produce 4 different descriptions at each level to help keep this interesting.

    # strip_willingness is a measure of how into the whole strip process the girl is. The less dressed she get the more embarrassed she'll get,
    # the more slutty the more she'll tease you, take clothing off willingly, etc.
    $ strip_willingness = the_person.effective_sluttiness("underwear_nudity") + (5*the_person.get_opinion_score("not wearing anything")) - the_person.outfit.slut_requirement
    #If there are other things that influence how willing a person is to strip they go here!

    $ keep_stripping = True #When set to false the loop ends and the strip show stops.

    while keep_stripping:
        $ the_person.draw_person(position = picked_pose)
        if strip_willingness < 0:
            if rand_strip_desc == 0:
                "[the_person.title] blushes intensely while you watch her."
            elif rand_strip_desc == 1:
                if the_person.has_large_tits():
                    "[the_person.title] instinctively tries to cover herself with her hands, but her large tits make it a difficult task."
                else:
                    "[the_person.title] instinctively tries to cover herself with her hands."
            elif rand_strip_desc == 2:
                the_person "Oh my god..."
                "[the_person.title] covers her eyes for a moment and looks away."
            else:
                "[the_person.title] shakes her head and mutters to herself."
                the_person "I can't believe I'm doing this..."

        elif strip_willingness < 10:
            if rand_strip_desc == 0:
                "[the_person.title] stands awkwardly in front of you and avoids making eye contact."
            elif rand_strip_desc == 1:
                if the_person.has_large_tits():
                    "[the_person.title] shifts her weight from side to side while you watch her. The small movements still make her big tits jiggle around."
                else:
                    "[the_person.title] shifts her weight from side to side while you watch her."
            elif rand_strip_desc == 2:
                "You get a good look at [the_person.title] while she stands in front of you."
            else:
                "[the_person.title] blushes and looks around the room to avoid making eye contact."

        elif strip_willingness < 30:
            $tease_clothing = the_person.outfit.remove_random_any(top_layer_first = True, exclude_feet = True, do_not_remove = True) #She's slutty enough that she wants to tease you a little more
            if rand_strip_desc == 0:
                if tease_clothing is not None:
                    "[the_person.title] pulls at her [tease_clothing.name] seductively."
                    the_person "Mmm, I bet you want me to take this off, right?"
                else:
                    "[the_person.title] runs her hands down her body seductively."
                    the_person "Mmm, I bet you want to get your hands on me now, right?"

            elif rand_strip_desc == 1:
                if the_person.has_large_tits():
                    "[the_person.title] moves her body side to side for you, letting her large tits bounce and jiggle while you watch."
                else:
                    "[the_person.title] moves her body side to side for you while you watch."

            elif rand_strip_desc == 2:
                if tease_clothing is not None:
                    "[the_person.title] slips a hand under her [tease_clothing.name] and starts to pull it off."
                    the_person "Maybe I should just... slip this off. What do you think?"
                else:
                    if the_person.has_large_tits():
                        "[the_person.title]'s hands slide up and down her body. She cups one of her sizeable breast and squeezes it, pinching her own nipple while she does."
                    else:
                        "[the_person.title]'s hands slide up and down her body. She rubs her small breasts, paying special attention to their firm nipples."
            else:
                the_person "I hope you're enjoying the show [the_person.mc_title]."
                "She wiggles her hips for you and winks."

        else: #strip_willingness >= 30
            $tease_clothing = the_person.outfit.remove_random_any(top_layer_first = True, exclude_feet = True, do_not_remove = True) #She's slutty enough that she wants to tease you a little more
            if rand_strip_desc == 0:
                if tease_clothing is not None:
                    "[the_person.title] pulls at her [tease_clothing.name]."
                    the_person "I'm going to have to get this out of the way before we can have any fun."
                else:
                    "[the_person.title] runs her hands over her own body."
                    the_person "Oh [the_person.mc_title], I think I'm going to need more than your eyes on me soon..."

            elif rand_strip_desc == 1:
                "[the_person.title] puts her hands up in the air and spins around. You get a great look at her body as she enjoys herself."

            elif rand_strip_desc == 2:
                if tease_clothing is not None:
                    the_person "Don't you just think all of this clothing is just useless? How about I take it all off for you... would you like that?"
                else:
                    "[the_person.title] takes a wider stances and slides her hands down her own thighs, all while maintaining eye contact with you."
                    the_person "You're looking so good today [the_person.mc_title], did you know that?"

            else:
                "[the_person.title] wiggles her hips side to side and bites her bottom lip, as if imagining some greater pleasure yet to come."

        $pay_strip_list = ["Strip"] #Tuple of menu things.
        # High obedience characters are more willing to be told to strip down (althoug they still expect to be paid for it)
        # Low obedience characters will strip off less when told but can be left to run the show on their own and will remove some.
        python:
            for item in the_person.outfit.get_unanchored():
                if not item.is_extension:
                    test_outfit = the_person.outfit.get_copy()
                    test_outfit.remove_clothing(item)
                    new_willingness = the_person.effective_sluttiness("underwear_nudity") + (5*the_person.get_opinion_score("not wearing anything")) - test_outfit.slut_requirement

                    taboo_break = False
                    if test_outfit.vagina_visible() and the_person.has_taboo("bare_pussy"):
                        taboo_break = "bare_pussy"
                    elif test_outfit.tits_visible() and the_person.has_taboo("bare_tits"):
                        taboo_break = "bare_tits"
                    elif test_outfit.underwear_visible() and the_person.has_taboo("underwear_nudity"):
                        taboo_break = "underwear_nudity"

                    if new_willingness + (the_person.obedience-100) >= -20:
                        #They're willing to strip it off.
                        price = 0 # Default value
                        price_display = "Free"
                        if taboo_break == "bare_pussy" or taboo_break == "bare_tits":
                            price = (strip_willingness - new_willingness) * 10

                        elif taboo_break == "underwear_nudity":
                            price = (strip_willingness - new_willingness) * 5

                        elif new_willingness >= 40:
                            price = 0 #They'll do it for free!

                        elif new_willingness >= 20:
                            price = (strip_willingness - new_willingness) * 1 #They feel pretty good about how they'll be dressed after, so the price is decent.

                        else:
                            price = (strip_willingness - new_willingness) * 3 #THey will feel pretty uncomfortable, so they expect to be paid well.

                        if price < 0:
                            price = 0

                        price = math.ceil((price/5.0))*5 #Round up to the next $5 increment
                        if price > 0:
                            price_display = "$" + str(price)

                        display_string = item.display_name
                        if taboo_break:
                            display_string = "{image=gui/extra_images/taboo_break_token.png} " + display_string + " {image=gui/extra_images/taboo_break_token.png}"

                        display_string += "\n{size=22}" + price_display + "{/size}"
                        if price > mc.business.funds:
                            display_string += " (disabled)"

                        pay_strip_list.append([display_string, [item,price]])

                    else:
                        display_string = item.display_name
                        if taboo_break:
                            display_string = "{image=gui/extra_images/taboo_break_token.png} " + display_string + " {image=gui/extra_images/taboo_break_token.png}"
                        pay_strip_list.append([display_string + "\n{size=22}Too Slutty{/size} (disabled)", [item,-1]])

            other_options_list = ["Other Options"]
            other_options_list.append(["Just watch.","Watch"])
            other_options_list.append(["Tell her to pose.","Pose"])
            #TODO: This is where the "jerk off" option should be.
            #TODO: If Jerking off there should be some way to transition into having sex.
            other_options_list.append(["Finish the show.","Finish"])
        call screen main_choice_display([pay_strip_list, other_options_list])
        $ strip_choice = _return
        if strip_choice == "Watch":
            if renpy.random.randint(0,1) == 0:
                $ tease_item = the_person.outfit.remove_random_any(top_layer_first = True, exclude_feet = True, do_not_remove = True) #The clothing item she's considering taking off
                $ free_spirit_threshold = 40 + (100 - the_person.obedience)
                if renpy.random.randint(0,100) < free_spirit_threshold: #She's independant enough to strip, change pose, etc. on her own.
                    if tease_item is not None and new_willingness >= (the_person.obedience-100): #A more obedient person is less willing to strip without being told to. A less obedient person will strip further on their own.
                        $ test_outfit = the_person.outfit.get_copy()
                        $ test_outfit.remove_clothing(tease_item)
                        $ new_willingness = the_person.sluttiness + (5*the_person.get_opinion_score("not wearing anything")) - test_outfit.slut_requirement
                        $ price = 0
                        $ taboo_break = False

                        if test_outfit.vagina_visible() and the_person.has_taboo("bare_pussy"):
                            $ price = (strip_willingness - new_willingness) * 10
                            $ taboo_break = "bare_pussy"
                        elif test_outfit.tits_visible() and the_person.has_taboo("bare_tits"):
                            $ price = (strip_willingness - new_willingness) * 10
                            $ taboo_break = "bare_tits"
                        elif test_outfit.underwear_visible() and the_person.has_taboo("underwear_nudity"):
                            $ price = (strip_willingness - new_willingness) * 5
                            $ taboo_break = "underwear_nudity"
                        elif new_willingness >= 30: #She's slutty enough to do it for free!
                            $ price = 0
                        elif new_willingness >= 10:
                            $ price = (strip_willingness - new_willingness) * 1
                        else:
                            $ price = (strip_willingness - new_willingness) * 3

                        $ price = math.ceil((price/5.0))*5 #Round up to the next $5 increment
                        if price > 0:
                            "[the_person.title] steps a little closer to you and plays with the edge of her [tease_item.display_name]."
                            if taboo_break: #TODO: If this style of stripping becomes more important this dialogue should be personality based (mainly for family related dialogue)
                                if taboo_break == "bare_pussy":
                                    the_person "Would you like a look at my pussy? How about... $[price] and I'll take off my [tease_item.display_name]."
                                elif taboo_break == "bare_tits":
                                    the_person "So, would you like to see my tits? Just, oh... $[price] and I'll take off my [tease_item.display_name]."
                                else: #Underwear_nudity
                                    the_person "Want to see what I'm wearing underneath this [tease_item.display_name]? Just $[price] and I'll show you."
                            else:
                                the_person "$[price] and I'll take this off for you..."

                            menu:
                                "Pay her $[price]." if mc.business.has_funds(price):
                                    "You pull the cash out of your wallet and hand it over."
                                    $ mc.business.change_funds(-price)
                                    $ the_person.change_obedience(-1)
                                    $ the_person.change_slut(1, 40)
                                    $ the_person.draw_animated_removal(tease_item, position = picked_pose)
                                    $ mc.change_locked_clarity(10)
                                    "[the_person.title] takes it, puts it to the side, and starts to slide her [tease_item.name] off."
                                    if the_person.update_outfit_taboos():
                                        "She seems momentarily uneasy about undressing, but shakes the feeling quickly and returns her attention to you."

                                "Pay her $[price]. (disabled)" if not mc.business.has_funds(price):
                                    pass

                                "Don't pay her.":
                                    mc.name "I think you look good with it on."
                                    "[the_person.title] seems disappointed but shrugs and keeps going."

                        else:
                            $ the_person.draw_animated_removal(tease_item, position = picked_pose)
                            $ mc.change_locked_clarity(10)
                            "You watch as [the_person.title] grabs their [tease_item.name] and pulls it off."
                    else:
                        #She has nothing to strip off or she's as slutty as she's willing to get
                        "[the_person.title] seems comfortable just the way she is."

                else: #She doesn't quite know what to do without you telling her.
                    "Without any direction [the_person.title] just keeps doing what she was doing."

            else:
                #She decides to change pose half the time.
                $ new_pose = get_random_from_list(pose_list)
                if not new_pose[1] == picked_pose:
                    $ picked_pose = new_pose[1]
                    "While you're watching [the_person.title] changes pose so you can see her from a different angle."
                else:
                    "[the_person.title] seems comfortable just the way she is."


        elif strip_choice == "Pose":
            #You ask her to change into a different pose
            mc.name "I want to see you from a different angle."
            $pose_menu_tuple = []
            python:
                for pose_tuple in pose_list:
                    if not pose_tuple[1] == picked_pose:
                        pose_menu_tuple.append(pose_tuple)
                pose_menu_tuple.append(["Nevermind.",None])

            $ pose_choice = renpy.display_menu(pose_menu_tuple,True,"Choice")
            if pose_choice is not None:
                $ picked_pose = pose_choice
                "[the_person.title] nods and moves for you."

            else:
                mc.name "Nevermind, you look perfect like this."

        elif strip_choice == "Finish":
            $ keep_stripping = False
            mc.name "That was fun [the_person.title], I think that's enough."
            if strip_willingness < 0:
                "[the_person.title] sighs happily."
                the_person "Oh my god, I thought I was going to die of embarrassment!"
            elif strip_willingness < 20:
                the_person "Oh, okay. That... wasn't as bad as I thought it was going to be, at least."
            else:
                the_person "Oh, is that all you wanted to see? I feel like we were just getting started!"

        else: #The only other result is an actual strip. Pay the cash, remove the piece and loop or end.
            $ mc.business.change_funds(-strip_choice[1])
            $ test_outfit = the_person.outfit.get_copy() #We use a temp copy so that we can get her reaction first.
            $ test_outfit.remove_clothing(strip_choice[0])
            $ the_clothing = strip_choice[0]

            $ taboo_break = False
            if test_outfit.vagina_visible() and the_person.has_taboo("bare_pussy"):
                $ taboo_break = "bare_pussy"
            elif test_outfit.tits_visible() and the_person.has_taboo("bare_tits"):
                $ taboo_break = "bare_tits"
            elif test_outfit.underwear_visible() and the_person.has_taboo("underwear_nudity"):
                $ taboo_break = "underwear_nudity"

            $ strip_willingness = the_person.effective_sluttiness("underwear_nudity") + (5*the_person.get_opinion_score("not wearing anything")) - test_outfit.slut_requirement
            mc.name "Take off your [the_clothing.display_name] for me."
            if taboo_break: #Always use special dialogue for the taboo breaks
                $ the_person.call_dialogue(taboo_break + "_taboo_break", the_clothing = the_clothing)
                $ the_person.break_taboo(taboo_break)

            if strip_choice[1] > 0:
                if strip_willingness < 0:
                    "You pull some cash from your wallet and offer it to [the_person.title]. She takes it and looks at it for a long second."
                    the_person "Oh my god... I shouldn't be doing this..."
                    $ the_person.change_obedience(2)
                    $ the_person.change_slut(1, 40)
                    $ the_person.draw_animated_removal(strip_choice[0], position = picked_pose)
                    $ mc.change_locked_clarity(10)
                    "Nevertheless, she keeps the money and pulls off her [the_clothing.display_name]."
                elif strip_willingness < 20:
                    "You pull some cash out from your wallet and hand it over to [the_person.title]. She puts it to the side and grabs her [the_clothing.display_name]."
                    the_person "Ready?"
                    $ the_person.change_obedience(1)
                    $ the_person.change_slut(1, 40)
                    $ the_person.draw_animated_removal(strip_choice[0], position = picked_pose)
                    $ mc.change_locked_clarity(10)
                    "You nod and [the_person.title] pulls off the piece of clothing, throwing it to the side."
                else:
                    $ mc.change_locked_clarity(10)
                    "You're still pulling out cash as [the_person.title] strips off her [the_clothing.display_name] and chucks it to the side."
                    $ the_person.draw_animated_removal(strip_choice[0], position = picked_pose)
                    the_person "Thank you!"
                    "She plucks the cash from your hand and quickly puts it away."

            else: #She'll only do it for free if she's becoming less slutty (ie taking off lingerie, bondage gear, etc.) or if she's very slutty anyways.
                the_person "Is that all? Well, I think that's easy."
                $ the_person.draw_animated_removal(strip_choice[0], position = picked_pose)
                $ mc.change_locked_clarity(10)
                "[the_person.title] strips off her [the_clothing.display_name] for free, leaving it on the ground at her feet."
    return

label strip_tease(the_person, in_private = True, for_pay = False, start_girl_direction = None, start_guy_state = None, start_girl_state = None, skip_intro = False):
    #TODO: Generate a report like we do when having sex, so we can check for orgasms, if we escalated to having sex, etc.

    # She can have a couple of different states (kind of like actions she could choose)
    # -> Awkwardly standing - She just stands there while you stare at her
    # -> Dancing - Moving her body while you watch.
    # -> Close Dancing - Tits and ass in your face. Close enough to touch.
    # -> Lapdance - Grinding her body against yours. If your cock is out she's rubbing it between her ass cheeks, if not it's uncomfortablly hard.

    #Each stripposition needs to have an:
    # Intro - what we describe when we _start_ in that position_name
    # Transition - what we describe when we transition into that state (maybe from one we already know)
    # Watching state - A few different descriptions of you just watching her.
    # Touching state - If she's close enough to touch, a few different descriptions of you touching her.
    # Jerking state - If you have your cock out a few different descriptions of you jerking off.
    # Outro state for her - You made her cum by touching her, or just by looking at her.
    # Outro state for you - She made you cum (maybe while jerking off)
    # Strip state - She takes off a piece of clothing (maybe for money).

    #NOTE: We calculate starting pose before adding the love modifiers, so girlfriends are tame but can be convinced to go further by you.
    if start_girl_state is None:
        $ girl_state = strip_awkward_stand
        $ slut_requirement = 35 - 5*(the_person.get_opinion_score("showing her tits")+the_person.get_opinion_score("showing her ass"))
        if not in_private:
            $ slut_requirement += 15
        if the_person.effective_sluttiness() >= slut_requirement or (in_private and the_person.love >= slut_requirement):
            $ girl_state = strip_dancing
    else:
        $ girl_state = start_girl_state


    call apply_sex_slut_modifiers(the_person, in_private = in_private)

    if start_guy_state is None:
        $ guy_state = "watching" # Other posibilities include: Jerking off, Touching.
    else:
        $ guy_state = start_guy_state

    if start_girl_direction is None:
        $ girl_direction = "towards"
    else:
        $ girl_direction = start_girl_direction

    if not skip_intro:
        $ girl_state.call_pose(the_person, girl_direction)
        $ girl_state.call_intro(the_person, guy_state = guy_state, for_pay = False)

    $ should_continue = True
    while should_continue:
        $ chosen_action = None
        $ action_options = ["Do something..."]
        $ command_options = ["Say something..."]
        $ strip_options = ["Tell her to strip her..."]

        ### Build the guy actions list ###
        if guy_state == "watching": #Start with the "continue" actions.
            $ action_options.append(["Keep watching her.", "continue"])
        elif guy_state == "jerking":
            $ action_options.append(["Keep jerking off.", "continue"])
        elif guy_state == "touching":
            $ action_options.append(["Keep feeling her up.", "continue"])

        if girl_state.allows_jerking and not guy_state == "jerking" and mc.arousal > 20:
            $ action_options.append(["Pull out your cock out.", "start_jerking"])

        if girl_state.allows_touching and not guy_state == "touching":
            $ action_options.append(["Start feeling her up.", "start_touching"])
        #TODO: Maybe a dirty talk state?


        ### Build the command actions ###

        if girl_state.allows_turning:
            $ command_options.append(["Tell her to turn around.", "turn_around"])

        if the_person.has_role(hypno_orgasm_role) and not the_person.event_triggers_dict.get("hypno_orgasmed_recently", False):
            $ command_options.append(["Trigger an orgasm.", "hypno_orgasm"])

        python:
            for next_position in girl_state.leads_to:
                if the_person.effective_sluttiness() < next_position[0].slut_requirement:
                    command_options.append([next_position[1] + "\nRequires: " + get_red_heart(next_position[0].slut_requirement) + " (disabled)", next_position[0]])
                else:
                    command_options.append([next_position[1], next_position[0]]) # Adds a tuple of "description", strip position to the list.

        $ command_options.append(["Tell her to stop.", "end"])

        ### Build up the strip list ###
        python:
            for item in the_person.outfit.get_unanchored():
                if not item.is_extension:
                    strip_options.append([item.display_name, item]) #Note that this is just for the _request_. She might refuse, ask for cash, ect.


        call screen main_choice_display([action_options, command_options, strip_options])
        $ the_choice = _return


        if isinstance(the_choice, Clothing): #Strip if you've offered to pay her something.
            call strip_tease_remove(the_person, the_choice, girl_state, girl_direction, guy_state, for_pay)
            $ the_choice = "description"

        elif isinstance(the_choice, StripteasePosition):
            if the_person.effective_sluttiness() >= the_choice.slut_requirement:
                $ girl_state = the_choice
                $ girl_state.call_transition(the_person, guy_state, for_pay)
                if guy_state == "touching" and not girl_state.allows_touching:
                    $ guy_state == "watching"
                elif guy_state == "jerking" and not girl_state.allows_jerking:
                    $ guy_state == "watching"
            else:
                "[the_person.possessive_title] shakes her head, unwilling to go any further."

            $ the_choice = "description"

        elif the_choice == "start_jerking":
            "You unzip your pants and pull out your cock. It's hard shaft falls easily into your hand as you watch [the_person.title]."
            $ guy_state = "jerking"
            if the_person.effective_sluttiness() < girl_state.slut_requirement + 10:
                #Angry about it. You need some way to convince her.
                if girl_direction == "away":
                    "It takes a moment for [the_person.title] to look over her shoulder and notice what you're doing."
                    "When she does she gasps and glares at you."
                    the_person "Oh my god, what are you doing?"

                else:
                    "[the_person.possessive_title] is shocked to the point of silence for a moment."
                    the_person "I... Oh my god, what are you doing?"
                mc.name "I think it's pretty self-explanatory."
                "You stroke your shaft a few times to drive the idea home."
                the_person "Put that away! That's... "
                "She stares at your hard cock and stumbles over her words as she tries to think of anything other than \"impressive\"."
                the_person "...Disgusting! That's what it is!"
                menu:
                    "Pay her. -$200" if mc.business.has_funds(200) and for_pay:
                        "You sigh dramatically and pull out your wallet, cock still standing at attention."
                        mc.name "Here, two hundred dollars. This is why you're doing this in the first place, right?"
                        "You hold up the cash and motion for her to take it."
                        the_person "I... I mean..."
                        "She stammers for a moment, caught by her own justifications."
                        "Finally she snatches the money away from you and puts it away."
                        $ the_person.change_slut(1, 30)
                        $ the_person.change_obedience(1)
                        $ the_person.change_love(-1)
                        $ mc.business.change_funds(-200)
                        the_person "Fine, just don't... think this is going any further!"

                    "Pay her. -$200 (disabled)" if not mc.business.has_funds(200) and for_pay:
                        pass

                    "Order her." if the_person.obedience >= 120:
                        "You shrug and continue to jerk off."
                        mc.name "Whatever. Keep going."
                        "Your tone doesn't leave any other option. She glares at you, but doesn't complain any more."
                        $ the_person.change_slut(1, 30)
                        $ the_person.change_love(-1)

                    "Order her.\nRequires: 120 Obedience (disabled)" if the_person.obedience < 120:
                        pass

                    "Stop jerking off.":
                        "You stare at each other for a long moment, but it becomes increasingly clear that you aren't going to change her mind."
                        "You sigh dramatically and stuff your hard cock back into your pants."
                        mc.name "Fine, just get back to it."
                        $ the_person.change_obedience(-1)
                        "She glares at you for a moment more, but finally seems convinced you'll keep your word and continues."
                        $ guy_state = "watching"

            elif the_person.effective_sluttiness() < girl_state.slut_requirement + 20:
                #Unsure about it, but you convince her without any issues.
                if girl_direction == "away":
                    "It takes a few moments for [the_person.title] to notice what's going on behind her."
                    "When she finally glances over her shoulder she stops and gasps in surprise."
                else:
                    "[the_person.title] blushes and looks away in surprise."
                the_person "[the_person.mc_title], what are you doing?"
                mc.name "I think it's pretty obvious, isn't it?"
                the_person "I... You shouldn't..."
                mc.name "How can I not when there's a beautiful woman like you in front of me?"
                mc.name "Just keep going, no need to stop."
                "She seems uncertain for a few long seconds, but finally sighs and shrugs."
                $ the_person.change_slut(1,30)
                the_person "Just don't think this is going to go any further, alright?"

            else:
                #Happy you're having a good time.
                if girl_direction == "away":
                    "It takes a few moments for [the_person.title] to notice what's going on behind her."
                    "When she glances over her shoulder she smiles at you."
                else:
                    "[the_person.title] bites her lip and watches you jerk off for a moment."

                the_person "Just couldn't contain yourself, huh?"
                mc.name "Can you blame me? Now don't stop, this is great."
            $ the_choice = "description"

        elif the_choice == "start_touching":
            $ guy_state = "touching"
            if girl_direction == "away":
                "You reach out and place your hands on [the_person.title]'s body, running your hands over her ass and legs."
            else:
                "You reach out and place your hands on [the_person.title]'s body, running your hands over her hips and up towards her tits."

            if the_person.effective_sluttiness("touching_body") < girl_state.slut_requirement + 20:
                "[the_person.possessive_title] jumps away from you in surprise."
                the_person "Hey! What are you doing?"
                mc.name "What? It was right in front of me..."
                $ the_person.change_love(-1)
                the_person "That doesn't mean you can grab whatever you want!"
                "You hold up your hands innocently. She glares at you, but seems willing to let it drop for now."

            elif the_person.effective_sluttiness("touching_body") < girl_state.slut_requirement + 40:
                if for_pay:
                    "[the_person.possessive_title] jumps away from you, more surprise than anger."
                    the_person "Hey! What do you think you're doing?"
                    mc.name "You can't blame me, you just look so tempting!"
                    "She sighs and shakes her head disapprovingly."
                    the_person "You should know that touching costs extra. How about... $200?"
                    menu:
                        "Pay her. -$200" if mc.business.has_funds(200) and for_pay:
                            mc.name "Well that's not a hard decision, here you go."
                            "You pull out the cash and hold it up for her to take."
                            if the_person.has_taboo("touching_body"):
                                "She looks at it for a moment, having second thoughts now that you're actually willing to put up the money."
                                the_person "I don't know actually."
                                mc.name "Come on, a deal is a deal, right?"
                                "You wiggle the bills and her resistance breaks. She snatches them and tucks them away."
                                the_person "Fine, but this is as far as it goes!"
                            else:
                                "She grabs the bills and counts them quickly before tucking them away."
                                the_person "But this is as far as it goes!"

                            $ mc.business.change_funds(-200)

                            "You hold up the cash and motion for her to take it."
                            the_person "I... I mean..."
                            "She stammers for a moment, caught by her own justifications."
                            "Finally she snatches the money away from you and puts it away."
                            $ the_person.change_slut(1, 30)
                            $ the_person.change_obedience(-1)
                            the_person "Fine, just don't... think this is going any further!"

                        "Pay her. -$200 (disabled)" if not mc.business.has_funds(200) and for_pay:
                            pass

                        "Order her." if the_person.obedience >= 125:
                            "You shrug and pull her closer to you."
                            mc.name "Whatever. Keep going."
                            "Your tone doesn't leave any other option. She glares at you, but eventually continues."
                            $ the_person.change_slut(1, 30)
                            $ the_person.change_love(-1)

                        "Order her.\nRequires: 125 Obedience (disabled)" if the_person.obedience < 125:
                            pass

                        "Stop touching her.":
                            "You stare at each other for a long moment, but it becomes increasingly clear that you aren't going to change her mind."
                            "You hold your hands up innocently and shrug."
                            mc.name "Alright, alright. You've made your point."
                            $ the_person.change_love(-1)
                            "She glares at you for a moment more, but finally seems convinced you'll keep your word and continues."
                            $ guy_state = "watching"
                else:
                    if the_person.has_taboo("touching_body"):
                        $ the_person.call_taboo_break("touching_body")
                    else:
                        "[the_person.title] gasps in surprise, but doesn't say anything and certainly doesn't tell you to stop."

            else:
                "[the_person.possessive_title] leans her body into your hands seductively, encouraging you to touch her more."


            if guy_state == "touching":
                if the_person.has_taboo("touching_body"):
                    "[the_person.possessive_title] seems nervous at first, but quickly becomes comfortable having your hands all over her."
                    $ the_person.break_taboo("touching_body")

            $ the_choice = "description"

        elif the_choice == "turn_around":
            if girl_direction == "towards":
                mc.name "Turn around, I want to see you from behind."
                $ girl_direction = "away"

            elif girl_direction == "away":
                mc.name "Turn around, I don't just want to look at your back."
                $ girl_direction = "towards"
            $ girl_state.call_turn_description(the_person, girl_direction, guy_state, for_pay)
            $ girl_state.call_pose(the_person, girl_direction)
            $ the_choice = "description"

        elif the_choice == "hypno_orgasm":
            $ the_person.event_triggers_dict["hypno_orgasmed_recently"] = True
            $ the_word = the_person.event_triggers_dict.get("hypno_trigger_word","Cum")
            $ the_word.capitalize()
            mc.name "[the_word]."
            $ the_person.change_arousal(the_person.max_arousal)
            "[the_person.possessive_title] whimpers with pleasure as your training takes hold of her brain."
            $ the_choice = "orgasm"

        elif the_choice == "end":
            mc.name "Alright, that's enough."
            if the_person.effective_sluttiness() < 15:
                "[the_person.possessive_title] is visibly relieved. She takes a deep sigh and smiles."
            elif the_person.effective_sluttiness() < 30:
                "[the_person.possessive_title] nods and smiles."
                the_person "I guess that wasn't so bad..."
            else:
                "[the_person.possessive_title] looks a little disappointed."
                the_person "Aw, I hope I wasn't boring you..."
            $ should_continue = False

        elif the_choice == "continue": #Girl can decide to do something. Do that here. (Offer to strip, advance to another position, tell you to touch her, ect)

            $ possible_girl_actions = ["nothing"]
            #TODO: Decide if we want any random chance in this. Maybe make it random if she'll do multiple things.
            if the_person.judge_outfit(the_person.outfit): # She's comfortable wearing what she has on, she'll consider stripping something off.
                if the_person.outfit.remove_random_any(top_layer_first = True, exclude_feet = True, do_not_remove = True) is not None: #Checks that something can actually be stripped, as is nessesary below
                    $ possible_girl_actions.append("strip")

            if girl_state.has_acceptable_transition(the_person):
                $ possible_girl_actions.append("transition")

            if guy_state == "watching" and girl_state.allows_touching and the_person.effective_sluttiness("touching_body") > girl_state.slut_requirement + 20:
                $ possible_girl_actions.append("start_touching")

            #TODO: Have her request you get your cock out if there's more we can do with that later.
            if girl_state.allows_turning:
                $ possible_girl_actions.append("turn_around")



            $ girl_action = get_random_from_list(possible_girl_actions)
            if girl_action == "nothing":
                pass
            elif girl_action == "strip": #TODO Maybe have an option to tell her not to strip down on you unless you tell her to.
                $ test_outfit = the_person.outfit.get_copy()
                $ the_clothing = test_outfit.remove_random_any(top_layer_first = True, exclude_feet = True)

                if the_clothing is None:
                    pass #SHouldn't be possible, but let's avoid failing if it is
                else:
                    $ test_outfit.remove_clothing(the_clothing) #Build a copy so we can check the effects the removal will have.

                    $ taboo_break = None
                    if test_outfit.vagina_visible() and the_person.has_taboo("bare_pussy"):
                        $ taboo_break = "bare_pussy"
                    elif test_outfit.tits_visible() and the_person.has_taboo("bare_tits"):
                        $ taboo_break = "bare_tits"
                    elif test_outfit.underwear_visible() and the_person.has_taboo("underwear_nudity"):
                        $ taboo_break = "underwear_nudity"

                    $ do_strip = True

                    if taboo_break is None and (the_person.judge_outfit(test_outfit, -20 + 5*the_person.get_opinion_score(["showing her tits", "showing her ass"])) or (not for_pay and the_person.judge_outfit(test_outfit))):
                        the_person "Let's get this out of the way..."
                        "[the_person.possessive_title] hooks a thumb under her [the_clothing.display_name]."
                        # She strips it off because it barely effects her sluttiness, or because she's comfortable and not expecting money anyways
                        #TODO: Have some taboo break stuff based on what she removes.

                    else:
                        $ strip_cost = 10
                        if the_clothing.underwear:
                            $ strip_cost = 25
                        if taboo_break:
                            $ strip_cost = strip_cost * 2

                        "[the_person.title] plays with the edge of her [the_clothing.display_name] as she entertains you."
                        if for_pay:
                            if taboo_break == "bare_pussy":
                                the_person "Would you like a look at my pussy? How about... $[strip_cost] and I'll take off my [the_clothing.display_name]."
                            elif taboo_break == "bare_tits":
                                the_person "So, would you like to see my tits? Just, oh... $[strip_cost] and I'll take off my [the_clothing.display_name]."
                            elif taboo_break == "underwear_nudity": #Underwear_nudity
                                the_person "Want to see what I'm wearing underneath this [the_clothing.display_name]? Just $[strip_cost] and I'll show you."
                            else:
                                the_person "You know, for just $[strip_cost] I'll take this off for you..."
                        else:

                            if taboo_break == "bare_pussy":
                                the_person "I don't know if I should take off my [the_clothing.display_name]... I would be so exposed!"
                                the_person "Maybe some other time..."
                            elif taboo_break == "bare_tits":
                                the_person "All that's hiding my tits away is this little [the_clothing.display_name]."
                                the_person "Maybe I'll take it off for you one day..."
                            elif taboo_break == "underwear_nudity":
                                the_person "Are you curious what I'm wearing under my [the_clothing.display_name]? I kind of want to show you."
                                the_person "I don't know though, maybe that's going too far..."
                            else:
                                the_person "Hmm, should I take off my [the_clothing.display_name]?"
                                the_person "That's probably going too far. Probably..."

                            "She sounds like she's looking for an excuse to keep going."

                        menu:
                            "Pay her.\n-$[strip_cost]" if mc.business.has_funds(strip_cost) and for_pay:
                                $ top_layer = the_person.outfit.get_lower_top_layer()
                                if girl_state.is_close and top_layer and top_layer.underwear: #Slip it into her g-string or similar.
                                    "You pull out some cash and slip it carefully into the waist of her [top_layer.display_name]."
                                    if girl_direction == "away":
                                        "Then you give her ass a quick slap."
                                        mc.name "There you go [the_person.title], it's all there."
                                    else:
                                        "Then you give her thigh a quick tap and smile."
                                        mc.name "You can trust me, it's all there."

                                else:
                                    "You pull out some cash and motion for her to take it."
                                    mc.name "You drive a hard bargin. Here you go..."
                                    "She takes the cash, checks that it's the correct amount, and smiles at you."
                                    the_person "Alright then..."

                                if the_person.get_opinion_score("taking control") < 0:
                                    $ the_person.change_obedience(-the_person.get_opinion_score("taking control")) #Putting her in control builds her confidence.
                                $ mc.business.change_funds(-strip_cost)

                            "Pay her.\n-$[strip_cost] (disabled)" if not mc.business.has_funds(strip_cost) and for_pay:
                                pass

                            "Encourage her." if not for_pay:
                                mc.name "Come on, do it for me [the_person.title]. Take it off."
                                if renpy.random.randint(0,100) < (the_person.love + the_person.obedience - 100):
                                    "[the_person.possessive_title] thinks for a moment, then nods and smiles."
                                    the_person "Alright, only because it's you."
                                    if the_person.get_opinion_score("taking control") < 0:
                                        $ the_person.change_obedience(-the_person.get_opinion_score("taking control")) #Putting her in control builds her confidence.

                                else:
                                    "[the_person.possessive_title] thinks for a moment, then shakes her head."
                                    the_person "No, no, I really shouldn't!"
                                    $ do_strip = False

                            "Don't pay." if for_pay:
                                mc.name "That's more than I'm willing to pay."
                                "She looks a little disappointed, but moves on without comment."
                                $ do_strip = False

                            "Say nothing." if not for_pay:
                                "You don't say anything. [the_person.possessive_title] moves on, quickly, but seems a little disappointed she couldn't take things further."
                                $ do_strip = False

                    if do_strip:
                        if taboo_break:
                            $ the_person.call_dialogue(taboo_break + "_taboo_break", the_clothing = the_clothing)
                            $ the_person.break_taboo(taboo_break)

                        if girl_direction == "away":
                            $ generalised_strip_description(the_person, the_clothing, position = girl_state.position_away_pose)
                        else:
                            $ generalised_strip_description(the_person, the_clothing, position = girl_state.position_towards_pose)

            elif girl_action == "transition": # She'll move to a more advanced stripping pose (come closer, start grinding on you, ect)
                $ possible_states = []
                python:
                    for a_state in girl_state.leads_to:
                        if the_person.effective_sluttiness() < a_state[0].slut_requirement:
                            possible_states.append(a_state[0])

                if possible_states:
                    $ girl_state = get_random_from_list(possible_states)
                    $ girl_state.call_transition(the_person, guy_state, for_pay)
                    if guy_state == "touching" and not girl_state.allows_touching:
                        $ guy_state == "watching"
                    elif guy_state == "jerking" and not girl_state.allows_jerking:
                        $ guy_state == "watching"

            elif girl_action == "start_touching":
                if the_person.has_taboo("touching_body"):
                    the_person "You don't have to be so shy, you know. Go on, touch me..."
                else:
                    the_person "Mmm, touch me [the_person.title]..."

                menu:
                    "Feel her up.":
                        if girl_direction == "away":
                            "You reach out and place your hands on [the_person.title]'s body, running your hands over her ass and legs."
                        else:
                            "You reach out and place your hands on [the_person.title]'s body, running your hands over her hips and up towards her tits."

                    "Don't do anything.":
                        mc.name "I'm just here for the show."
                        "[the_person.possessive_title] seems a little disappointed, but doesn't say any more."

            elif girl_action == "turn_around":
                if girl_direction == "towards":
                    $ girl_direction = "away"

                elif girl_direction == "away":
                    $ girl_direction = "towards"
                $ girl_state.call_turn_description(the_person, girl_direction, guy_state, for_pay)
                $ girl_state.call_pose(the_person, girl_direction)

            $ the_choice = "description" #And then we probably run a description.

        if the_choice == "description": #NOTE: Not an else-if, this is always run if the results above call for a description.
            $ guy_energy_cost = girl_state.guy_energy_cost
            if guy_state == "touching":
                $ guy_energy_cost += 4
            elif guy_state == "jerking":
                $ guy_energy_cost += 4

            if girl_state.girl_energy_cost > the_person.energy:
                $ the_choice = "exhausted"
            elif guy_energy_cost > mc.energy:
                $ the_choice = "guy_exhausted"
            else:
                $ the_person.change_energy(-girl_state.girl_energy_cost)
                $ mc.change_energy(-guy_energy_cost) #NOTE: Usually 0, but might be higher for specific sex-like positions

                $ girl_state.call_pose(the_person, girl_direction)
                $ girl_state.call_description(the_person, girl_direction, guy_state, for_pay)

                $ clarity_added = (girl_state.girl_arousal_gain/2) + the_person.sex_skills["Foreplay"] #Note that this _isn't_ expodential like actual sex is.
                if the_person.outfit.tits_visible():
                    $ clarity_added += 10
                if the_person.outfit.vagina_visible():
                    $ clarity_added += 10
                if the_person.outfit.underwear_visible():
                    $ clarity_added += 5
                if guy_state == "touching":
                    $ clarity_added += 5

                $ mc.change_locked_clarity(clarity_added)
                $ guy_arousal_change = girl_state.guy_arousal_gain + the_person.sex_skills["Foreplay"]
                $ girl_arousal_change = girl_state.girl_arousal_gain # This should usually be 0 unless they have some specific Opinions.
                $ girl_arousal_change += the_person.get_opinion_score(["showing her tits", "showing her ass"])
                if not in_private and mc.location.get_person_count() > 1:
                    $ girl_arousal_change += the_person.get_opinion_score("public sex")

                if guy_state == "jerking": #Ideal for adding arousal to yourself
                    $ guy_arousal_change += mc.sex_skills["Foreplay"] + 1 #Add one in case their Foreplay is 0, jerking off should add _something_
                    $ girl_arousal_change += mc.sex_skills["Foreplay"]/2
                elif guy_state == "touching": #Adds arousal to _her_. Similar to groping w/ 1 bonus, only your Foreplay.
                    $ girl_arousal_change += mc.sex_skills["Foreplay"] + 1
                else: #Just watching. YOur foreplay increases her arousal for dirty talk, ect.
                    $ girl_arousal_change += mc.sex_skills["Foreplay"]/2


                $ mc.change_arousal(guy_arousal_change)
                $ the_person.change_arousal(girl_arousal_change)


                if mc.arousal >= 80:
                    call climax_check() #Uses teh same check as the sex_mechanics
                    $ is_cumming = _return
                    if is_cumming:
                        call strip_tease_guy_cum(the_person, girl_state, girl_direction, guy_state, for_pay = False)

                if the_person.arousal >= the_person.max_arousal:
                    $ the_choice = "orgasm"

        if the_choice == "orgasm": #Note that this is broken out from above in case something else (like an orgasm trigger word) changes her arousal.
            $ girl_state.call_climax(the_person, guy_state, for_pay) #NOTE: the actual climax states shoudl all include a call to the_person.run_orgasm
            $ the_person.reset_arousal()


        if the_choice == "exhausted":
            "[the_person.possessive_title] looks tired. She wipes her brow and sighs."
            the_person "That's all I have in me, I need to take a break."
            $ should_continue = False
        elif the_choice == "guy_exhausted":
            if guy_state == "jerking":
                "You're exhausted, and even just jerking off is proving to be too much work."
            elif guy_state == "touching":
                "You're exhausted, and even just feeling up [the_person.title]'s body is proving to be too much work."
            else:
                "You're exhausted, and just don't have the energy to keep going."
            mc.name "That's enough for me, I need a break."
            $ should_continue = False

    call clear_sex_slut_modifiers(the_person)
    return


label strip_tease_remove(the_person, the_clothing, girl_state, girl_direction, guy_state, for_pay = False):
    $ rand_choice = renpy.random.randint(0,3) #Randomzie dialogue for a litte more variation.
    if rand_choice == 0:
        mc.name "Your [the_choice.display_name], take it off."
    elif rand_choice == 1:
        mc.name "Take off that [the_choice.display_name] for me."
    elif rand_choice == 2:
        mc.name "You don't need your [the_choice.display_name], take it off for me."
    else:
        mc.name "Want to take your [the_choice.display_name] for me?"

    $ test_outfit = the_person.outfit.get_copy()
    $ test_outfit.remove_clothing(the_clothing) #Build a copy so we can check the effects the removal will have.
    $ taboo_break = False
    if test_outfit.vagina_visible() and the_person.has_taboo("bare_pussy"):
        $ taboo_break = "bare_pussy"
    elif test_outfit.tits_visible() and the_person.has_taboo("bare_tits"):
        $ taboo_break = "bare_tits"
    elif test_outfit.underwear_visible() and the_person.has_taboo("underwear_nudity"):
        $ taboo_break = "underwear_nudity"

    $ resists_strip = False #If True we bring up the menu, otherwise we just do it.
    $ resist_level = None # Just a flag so we can know how much she resists and have some matchign dialogue.

    $ base_strip_cost = 10
    if the_clothing.underwear:
        $ base_strip_cost = 25

    $ obedience_requirement = 100
    if the_person.judge_outfit(test_outfit, -20) and not taboo_break:
        pass # She's super fine with it, even if you're paying she'll do it for free.
    elif the_person.judge_outfit(test_outfit, 0 + 5*the_person.get_opinion_score(["showing her tits", "showing her ass"])):
        pass # If she's doing it for pay she'll want to be paid (or be commanded), otherwise she's fine with it
        if for_pay:
            $ resists_strip = True
            $ resist_level = "low"
            $ strip_cost = base_strip_cost
            $ obedience_requirement = 115

    elif the_person.judge_outfit(test_outfit, 20 + 5*the_person.get_opinion_score(["showing her tits", "showing her ass"])): #She's uncomfortable with it, but she'll do it if you command her or pay her a lot.
        $ resists_strip = True
        $ resist_level = "mid"
        $ strip_cost = base_strip_cost * 4
        $ obedience_requirement = 130
    else:
        $ resists_strip = True
        $ resist_level = "high"
        $ strip_cost = base_strip_cost * 4
        $ obedience_requirement = 160
        $ pay_obedience_requirement = 130 - the_person.get_opinion_score("being submissive") * 5
        pass #She won't do it for just money, but you can force her with high Obedience OR moderate Obedience and cash.

    if for_pay:
        $ obedience_requirement += 15 #Harder to order her if she's doing it for money.

    if taboo_break and resists_strip:
        $ strip_cost = strip_cost * 2 #ie. showing your her tits will probably cost you $200 the first time

    if resists_strip: #TODO: All of this could probably be personality based dialogue, with different sections for the different resist levels.
        if resist_level == "low": #NOTE: All low resists are because they want cash.
            if taboo_break == "bare_pussy":
                the_person "Oh, I don't know if I'm ready to show you my pussy..."
                the_person "You could convince me for, oh... $[strip_cost]. Does that sound worth it to you?"

            elif taboo_break == "bare_tits":
                the_person "You want to see my tits? I'm not sure [the_person.mc_title]..."
                "She thinks for a moment before picking a price."
                the_person "How about $[strip_cost]. You think they're worth that much, right?"

            elif taboo_break == "underwear_nudity":
                the_person "You want to get a look at what I wear under my clothes, huh? Well..."
                the_person "I'm not sure about this, but I suppose I could do it for... $[strip_cost]."
                the_person "So, do you want a peek?"

            else:
                the_person "I can do that for you, I'll just need, oh..."
                the_person "$[strip_cost]. Do we have a deal?"

        elif resist_level == "mid":
            if for_pay:
                if taboo_break == "bare_pussy":
                    the_person "I don't know if I'm ready to show you my... pussy."
                    "[the_person.possessive_title] thinks for a long moment, obviously conflicted."
                    the_person "Maybe if you pay me something silly, like... $[strip_cost]. Then I could take off my [the_clothing.display_name] for you."

                elif taboo_break == "bare_tits":
                    the_person "You really want to see my boobs, huh? Well..."
                    "[the_person.possessive_title] thinks for a long moment, obviously conflicted."
                    the_person "Are you going to make it worth it for me? I'm going to need, uh... $[strip_cost]."
                    the_person "Hand it over and I'll slip this [the_clothing.display_name] off for you."

                elif taboo_break == "underwear_nudity":
                    the_person "I don't know if I'm ready for you to see me half-naked..."
                    "She thinks for a long moment, then comes to a decision."
                    the_person "If you give me $[strip_cost] I'll take it off. Otherwise you'll just have to be satisfied with me like this."
                else:
                    the_person "Oh I don't know [the_person.mc_title]. I guess if you paid me..."
                    "She thinks for a moment, coming up with a price on the spot."
                    the_person "$[strip_cost]. Still interested?"

            else:
                if taboo_break == "bare_pussy":
                    the_person "Oh, you want to see my... pussy? Well..."
                    the_person "I don't know [the_person.mc_title], I don't think I'm ready for that."

                elif taboo_break == "bare_tits":
                    "[the_person.possessive_title] looks uncomfortable for a moment and shakes her head."
                    the_person "I'm just not sure if I'm ready to get my tits out for you."
                    the_person "Maybe later, alright?"

                elif taboo_break == "underwear_nudity":
                    the_person "I don't think I'm ready to get that naked in front of you..."
                    the_person "Maybe I'll give you a peek later, alright?"

                else:
                    "[the_person.possessive_title] seems uncomfortable with the idea."
                    the_person "I don't think I'm ready for that [the_person.mc_title]."

        elif resist_level == "high":
            if taboo_break == "bare_pussy":
                the_person "I couldn't do that [the_person.mc_title], I wouldn't have anything covering my..."
                "She takes a moment to work up the courage to continue."
                the_person "... pussy."

            elif taboo_break == "bare_tits":
                the_person "[the_person.mc_title], I wouldn't have anything covering me up!"
                the_person "I don't think I want you to be ogling my breasts!"

            elif taboo_break == "underwear_nudity":
                the_person "And let you see me in my underwear? I don't think so!"

            else:
                the_person "I don't think so [the_person.mc_title], I'm just not ready for that!"


        $ do_strip = False
        menu:
            "Pay her.\n-$[strip_cost]" if mc.business.has_funds(strip_cost) and for_pay and not resist_level == "high":
                $ top_layer = the_person.outfit.get_lower_top_layer()
                if girl_state.is_close and top_layer and top_layer.underwear: #Slip it into her g-string or similar.
                    "You pull out some cash and slip it carefully into the waist of her [top_layer.display_name]."
                    if girl_direction == "away":
                        "Then you give her ass a quick slap."
                        mc.name "There you go [the_person.title], it's all there."
                    else:
                        "Then you give her thigh a quick tap and smile."
                        mc.name "You can trust me, it's all there."

                else:
                    "You pull out some cash and motion for her to take it."
                    mc.name "You drive a hard bargin. Here you go..."
                    "She takes the cash, checks that it's the correct amount, and smiles at you."
                    the_person "Alright then..."

                if resist_level == "mid":
                    $ the_person.change_obedience(1)
                $ mc.business.change_funds(-strip_cost)
                $ do_strip = True

            "Pay her.\n-$[strip_cost] (disabled)" if not mc.business.has_funds(strip_cost) and for_pay and not resist_level == "high":
                pass

            "Pay her.\n-$[strip_cost]" if resist_level == "high" and for_pay and mc.business.has_funds(strip_cost) and the_person.obedience >= pay_obedience_requirement:
                mc.name "I'm not paying you to stand around and be a prude."
                "You ignore her and pull a wad of cash out of your wallet."
                mc.name "Now take this, stop bitching, and take it off."
                $ the_person.change_love(-1)
                "[the_person.possessive_title] looks shocked, but she can't take her eyes off of your money."
                "After a long moment of thought her resolve breaks down."
                "She snatches the money from you, looking guilty while she does so."
                $ mc.business.change_funds(-strip_cost)
                $ do_strip = True

            "Pay her.\n-$[strip_cost], Requires: [pay_obedience_requirement] Obedience (disabled)" if resist_level == "high" and for_pay and (not mc.business.has_funds(strip_cost) or the_person.obedience < pay_obedience_requirement):
                pass

            "Order her." if the_person.obedience >= obedience_requirement:
                $ do_strip = True
                if resist_level == "high":
                    mc.name "I'm not here to listen to you complain, I'm here to watch you strip."
                    mc.name "So hurry up and take it off."
                    "[the_person.possessive_title] nods and follows your instructions."
                else:
                    if for_pay:
                        mc.name "I'm not going to pay you just to take off your [the_clothing.display_name]."
                        mc.name "Keep stripping and maybe you'll change my mind."
                        "[the_person.possessive_title] understands and follows your instructions."
                    else:
                        mc.name "Come on, you know how badly I want this [the_person.title]."
                        mc.name "Just take it off for me."
                        "Your tone seems to make an impression. She nods and starts to move again."

            "Order her.\nRequires: [obedience_requirement] Obedience (disabled)" if the_person.obedience < obedience_requirement:
                pass

            "Never mind.":
                if for_pay and not resist_level == "high":
                    mc.name "That's more than I'm willing to pay."
                    "She shrugs and moves on."
                else:
                    mc.name "Alright, just keep going then."

        if do_strip:
            if taboo_break:
                $ the_person.call_dialogue(taboo_break + "_taboo_break", the_clothing = the_clothing)
                $ the_person.break_taboo(taboo_break)
            if girl_direction == "away":
                $ generalised_strip_description(the_person, the_clothing, position = girl_state.position_away_pose)
            else:
                $ generalised_strip_description(the_person, the_clothing, position = girl_state.position_towards_pose)

    else:
        if taboo_break:
            $ the_person.call_dialogue(taboo_break + "_taboo_break", the_clothing = the_clothing)
            $ the_person.break_taboo(taboo_break)
        elif for_pay:
            the_person "You're right, let's get it out of the way so we can get to the fun stuff."
        else:
            the_person "You want it gone, then it's gone."

        if girl_direction == "away":
            $ generalised_strip_description(the_person, the_clothing, position = girl_state.position_away_pose)
        else:
            $ generalised_strip_description(the_person, the_clothing, position = girl_state.position_towards_pose) #TODO: Add more descriptions for this since it comes up a lot.
    return

label strip_tease_guy_cum(the_person, girl_state, girl_direction, guy_state, for_pay = False): #TODO: The rest of this
    if guy_state == "watching":
        "Watching her is too much for you to handle. You feel your cock tense as you pass the point of no return."
    elif guy_state == "touching":
        "Just feeling up her body is more than you can handle. Your cock twitches, then tenses as it prepares for your climax."
    elif guy_state == "jerking":
        "Her body is too much for you to handle. Your cock twitches and tenses in your hand, and you have no choice but to stroke yourself towards climax."

    $ girl_aware = False
    #Aware is the variable we use to track the concept that the girl knows you're going to cum before you actually do.
    $ already_came = False
    if not guy_state == "jerking":
        $ climax_controller = ClimaxController(["Pull out your cock.", None], ["Cum your pants.", "air"])
        $ the_choice = climax_controller.show_climax_menu()
        if the_choice == "Pull out your cock.":
            $ guy_state = "jerking"
            "You don't have much time to waste. You unzip your pants and let your throbbing cock fall out into your hand."
            if girl_direction == "towards":
                $ girl_aware = True
            else:
                if renpy.random.randint(0,100) < 20*the_person.focus+10:
                    "[the_person.possessive_title] glances over her shoulder, immediately noticing your twitching dick."
                    $ girl_aware = True
                else:
                    "[the_person.possessive_title] has her back to you, and is completely unaware."

            if girl_aware:
                if the_person.effective_sluttiness() < 20:
                    the_person "Oh my god, what are you doing?"
                    mc.name "Fuck, I can't take it, I'm going to cum!"
                    "Her eyes goes wide and she takes a few steps back."
                elif the_person.effective_sluttiness() < 40:
                    the_person "[the_person.mc_title], what are you doing?"
                    the_person "You really shouldn't..."
                    mc.name "Fuck, I'm going to cum!"
                    "[the_person.possessive_title] takes a moment to process that as you stroke yourself off."
                    the_person "Oh? Oh!"
                else:
                    the_person "Oh my god, it's twitching! Are you about to..."
                    "You have to cut her off. There's no time to waste!"
                    mc.name "Cum? Yes!"

            #TODO: If she has a way to make you cum (ie. she starts blowing you) she does that here.


        elif the_choice == "Cum your pants.":
            "You stifle a moan and try not to let [the_person.possessive_title] know what's happening right now."
            $ climax_controller.do_clarity_release(the_person)
            "A wave of warm pleasure shoots through your body. When it passes you're left with a satisfied fuzzy feeling in your brain and a mess to clean up in your pants."
            $ already_came = True
            #TODO: Possiblity that she notices here and judges you.


        #TODO: If she's looking towards you we'll do some basic checks, and she always becomes aware (because you can't hide why you whipepd your cock out.)


    if not already_came:
        if not girl_aware:
            menu:
                "Let her know.":
                    $ girl_aware = True
                    mc.name "Fuck, I'm going to cum!"
                    #TODO: Dialogue: You let her know you're about to cum,
                    if the_person.effective_sluttiness() < 20:
                        the_person "What? I didn't say you could do that!"
                        "Her eyes goes wide and she takes a steps back."
                        mc.name "It's a little late for that!"
                    elif the_person.effective_sluttiness() < 40:
                        the_person "Really? Oh my god, uh..."
                        "It's clear [the_person.possessive_title] wasn't really prepared to deal with this."
                    else:
                        the_person "I'm making you cum? Mmm, do it! Cum!"

                    #TODO: If she has a way to make you cum (ie. starts blowing you) she does that here and

                "Surprise her.":
                    pass

        if not already_came:
            call strip_cum_question_loop(the_person, girl_state, girl_direction, girl_aware, for_pay)


    return


label strip_cum_question_loop(the_person, girl_state, girl_direction, girl_aware, for_pay):
    $ climax_list = []
    if not girl_state.is_close:
        $ climax_list.append(["Cum on the floor.", "air"])
    if girl_direction == "away" and girl_state.is_close:
        $ climax_list.append(["Cum on her ass.","body"])
    if girl_direction == "towards" and girl_state.is_close:
        $ climax_list.append(["Cum on her legs.", "body"])

    if girl_aware:
        $ climax_list.append(["Ask to cum on her tits.", "tits"])
        $ climax_list.append(["Ask to cum on her face.", "face"])
        $ climax_list.append(["Ask to cum in her mouth.", "mouth"])
    $ climax_controller = ClimaxController(*climax_list)

    $ the_choice = climax_controller.show_climax_menu()
    if the_choice == "Cum on the floor.":
        "You grunt and climax, blowing your load out onto the floor in thick ropes of hot cum."
        $ climax_controller.do_clarity_release(the_person)
        if girl_aware or girl_direction == "towards":
            if the_person.effective_sluttiness() < 20:
                "[the_person.title] watches, speachless."
                the_person "Oh my god... I... I didn't say you could cum!"
                "You pant and shrug."
                mc.name "Sorry, I didn't have much of an option."
                $ the_person.change_happiness(-5)
                $ the_person.change_obedience(-2)
                $ the_person.change_love(-1)
                "She scowls, clearly upset."
            elif the_person.effective_sluttiness() < 40:
                "[the_person.title] watches, eyes wide and locked on your twitching cock."
                the_person "Oh my god... Wow, that was close..."
            else:
                "[the_person.title] watches eagerly, enjoying each twitch and pulse of your cock."
                the_person "Oh god, that's so hot..."

        else: #Not aware and looking away
            the_person "What's going on? I..."
            "She glances back at you and immediately realises what's happening."
            if the_person.effective_sluttiness() < 20:
                the_person "Oh my god! What... What are you doing!"
                "She jumps away, making sure she isn't in the splash zone."
                mc.name "I just couldn't hold it any more."
                $ the_person.change_happiness(-5)
                $ the_person.change_obedience(-3)
                $ the_person.change_love(-2)
                the_person "You need to give me some warning! And I told you I didn't want to take things this far!"
                "You shrug and take a few deep breaths, trying to recover."
                mc.name "Sorry, but I didn't have much time to think things through."
                "She glares at you, but at this point there isn't much she can do."
            elif the_person.effective_sluttiness() < 40:
                the_person "Oh my god!"
                "Her eyes lock onto your throbbing shaft as you cum."
                "She watches you in silence until you're finished. You give your shaft a few final strokes then let go and let it fall limp."
                mc.name "Sorry about that, I didn't have much warning either."
                the_person "Right, yeah... Just give me a heads up next time..."
                "She still hasn't taken her eyes off of your dick."
            else:
                the_person "Oh yeah, cum for me [the_person.mc_title]!"
                "She shakes her ass for you. The enthusiastic encouragement makes you cum even harder."
                "When you're finished she turns around and gives you a dirty smile."
                if the_person.get_opinion_score(["drinking cum", "being covered in cum", "cum facials"]) > 0:
                    the_person "That was hot. Such a shame you wasted it on the floor instead of putting it on me."
                    the_person "Oh well, maybe next time."
                else:
                    the_person "That was hot. Did it feel good?"
                    mc.name "I think it's obvious it did."
                    the_person "I still like hearing it."

    elif the_choice == "Cum on her ass.": #ALways facing away
        "You hold your shaft and blow your load, aiming your cock to spray it over [the_person.possessive_title]'s ass."
        $ climax_controller.do_clarity_release(the_person)
        $ the_person.cum_on_ass()
        $ the_person.draw_person(position = girl_state.position_away_pose)
        if girl_aware:
            if the_person.effective_sluttiness() + 5 * the_person.get_opinion_score("being covered in cum") < 20:
                the_person "Oh my god, what the hell!"
                "[the_person.title] turns around and glares daggers into you."
                "You shrug and pant, trying to catch your breath."
                mc.name "Sorry, you just pushed me over the edge and I couldn't stop myself."
                $ the_person.change_love(-2)
                $ the_person.change_happiness(-10)
                $ the_person.change_slut(1 + the_person.get_opinion_score("being covered in cum"), 40)
                the_person "So this is my fault?"
                "You shrug again. She scowls at you, but doesn't have much more she can say about it."
            elif the_person.effective_sluttiness() + 5 * the_person.get_opinion_score("being covered in cum") < 40:
                "[the_person.title] turns around and looks at you, eyes flicking between your face and your still-hard cock."
                the_person "Oh my god! Is that... Did you just cum on me?"
                $ the_person.change_happiness(-5 + 5*the_person.get_opinion_score("being covered in cum"))
                $ the_person.change_slut(1 + the_person.get_opinion_score("being covered in cum"), 40)
                mc.name "Yeah, sorry about that. I just couldn't hold back any more."
                the_person "Right..."
            else:
                "[the_person.title] looks over her shoulder and bites her lip."
                the_person "Yeah, that's it... Oh, it's so warm."
                $ the_person.change_happiness(5*the_person.get_opinion_score("being covered in cum"))
                if the_person.get_opinion_score("being covered in cum") > 0:
                    $ the_person.discover_opinion("being covered in cum")
                    the_person "Mmm, I love feeling cum sprayed all over me... It's intoxicating!"
                mc.name "Thanks [the_person.title], you're a fun target."
                the_person "My pleasure."
        else:
            if the_person.effective_sluttiness() + 5 * the_person.get_opinion_score("being covered in cum")< 20:
                "[the_person.title] stops moving and glances over her shoulder."
                "Her eyes lock onto your still-twitching cock."
                "You see a series of emotions pass across her face - surprise, understanding, maybe a hint of arousal, and finally anger."
                the_person "What the hell! Did you just... Oh my god, you just came on me!"
                $ the_person.change_love(-4)
                $ the_person.change_happiness(-10)
                $ the_person.change_slut(2 + the_person.get_opinion_score("being covered in cum"), 40)
                "You take a few deep breaths to try and recover from your orgasm, then shrug."
                mc.name "Yeah, sorry about that. It just sort of... happened."
                "Her eyes keep darting between your dick and your face, as if she can't decide which deserves her focus right now."
                the_person "\"Just happened\"? Oh my god, how did I let this happen..."
                "She sighs and shakes her head in disbelief."
            elif the_person.effective_sluttiness() + 5 * the_person.get_opinion_score("being covered in cum") < 40:
                "[the_person.title] turns around and looks at you, eyes flicking between your face and your still-hard cock."
                the_person "Oh my god! Is that... Did you just cum on me?"
                $ the_person.change_happiness(-5 + 5*the_person.get_opinion_score("being covered in cum"))
                $ the_person.change_obedience(-1)
                $ the_person.change_slut(2 + the_person.get_opinion_score("being covered in cum"), 40)
                mc.name "Yeah, sorry about that. I just couldn't hold back any more."
                the_person "Right... Just give me some warning next time, alright?"
                the_person "I really don't appreciate the surprise."
            else:
                "[the_person.title] looks over her shoulder and bites her lip."
                the_person "Yeah, that's it, cum for me [the_person.mc_title]!"
                $ the_person.change_happiness(5*the_person.get_opinion_score("being covered in cum"))
                if the_person.get_opinion_score("being covered in cum") > 0:
                    $ the_person.discover_opinion("being covered in cum")
                    the_person "Mmm, I love feeling your cum sprayed all over me... It's intoxicating!"
                "you take a moment and catch your breath."
                mc.name "Thanks [the_person.title], you're a fun target."
                the_person "My pleasure."
    elif the_choice == "Cum on her legs.": #Always looking towards
        "You hold your shaft and blow your load, sending it pulsing out in an arc onto [the_person.possessive_title]'s legs."
        $ climax_controller.do_clarity_release(the_person)
        if girl_aware:
            if the_person.effective_sluttiness() + 5 * the_person.get_opinion_score("being covered in cum") < 20:
                the_person "Oh my god, what the hell!"
                "[the_person.title] glares daggers at you."
                "You shrug and pant, trying to catch your breath."
                mc.name "Sorry, you just pushed me over the edge and I couldn't stop myself."
                $ the_person.change_love(-2)
                $ the_person.change_happiness(-10)
                $ the_person.change_slut(1 + the_person.get_opinion_score("being covered in cum"), 40)
                the_person "So this is my fault?"
                "You shrug again. She scowls at you, but doesn't have much more she can say about it."
            elif the_person.effective_sluttiness() + 5 * the_person.get_opinion_score("being covered in cum") < 40:
                "[the_person.title] looks at you, eyes flicking between your face and your still-hard cock."
                the_person "Oh my god! Is that... Did you just cum on me?"
                $ the_person.change_happiness(-5 + 5*the_person.get_opinion_score("being covered in cum"))
                $ the_person.change_slut(1 + the_person.get_opinion_score("being covered in cum"), 40)
                mc.name "Yeah, sorry about that. I just couldn't hold back any more."
                the_person "Right..."
            else:
                the_person "You got it on me... It's so warm."
                $ the_person.change_happiness(5*the_person.get_opinion_score("being covered in cum"))
                if the_person.get_opinion_score("being covered in cum") > 0:
                    $ the_person.discover_opinion("being covered in cum")
                    the_person "Mmm, I love feeling cum sprayed all over me... It's intoxicating!"
                mc.name "Thanks [the_person.title], you're a fun target."
                the_person "My pleasure."
        else:
            if the_person.effective_sluttiness() + 5 * the_person.get_opinion_score("being covered in cum") < 20:
                "[the_person.title] stops moving, her eyes locked onto your still-pulsing cock."
                "You see a series of emotions pass across her face - surprise, understanding, maybe a hint of arousal, and finally anger."
                the_person "What the hell! Did you just... Oh my god, you just came on me!"
                $ the_person.change_love(-4)
                $ the_person.change_happiness(-10)
                $ the_person.change_slut(2 + the_person.get_opinion_score("being covered in cum"), 40)
                "You take a few deep breaths to try and recover from your orgasm, then shrug."
                mc.name "Yeah, sorry about that. It just sort of... happened."
                "Her eyes keep darting between your dick and your face, as if she can't decide which deserves her focus right now."
                the_person "\"Just happened\"? Oh my god, how did I let this happen..."
                "She sighs and shakes her head in disbelief."
            elif the_person.effective_sluttiness() + 5 * the_person.get_opinion_score("being covered in cum") < 40:
                "[the_person.title] stops moving, her eyes locked onto your still-pulsing cock."
                the_person "Oh my god! Is that... Did you just cum on me?"
                $ the_person.change_happiness(-5 + 5*the_person.get_opinion_score("being covered in cum"))
                $ the_person.change_obedience(-1)
                $ the_person.change_slut(2 + the_person.get_opinion_score("being covered in cum"), 40)
                mc.name "Yeah, sorry about that. I just couldn't hold back any more."
                the_person "Right... Just give me some warning next time, alright?"
                the_person "I really don't appreciate the surprise."
            else:
                "[the_person.title] looks at your twitching cock and bites her lip."
                the_person "Yeah, that's it, cum for me [the_person.mc_title]!"
                $ the_person.change_happiness(5*the_person.get_opinion_score("being covered in cum"))
                if the_person.get_opinion_score("being covered in cum") > 0:
                    $ the_person.discover_opinion("being covered in cum")
                    the_person "Mmm, I love feeling your cum sprayed all over me... It's intoxicating!"
                "you take a moment and catch your breath."
                mc.name "Thanks [the_person.title], you're a fun target."
                the_person "My pleasure."

    elif the_choice == "Ask to cum on her tits.":
        mc.name "Get on your knees, I want to cum on your tits!"
        $ cum_on_floor_instead = False
        $ pay_after = False
        if the_person.effective_sluttiness() + 5 * the_person.get_opinion_score("being covered in cum") < 25: #Not willing no matter what.
            "[the_person.title] shakes her head."
            the_person "What? Of course not!"
            "You want to argue, but you're out of time!"
            $ cum_on_floor_instead = True

        elif the_person.effective_sluttiness() + 5 * the_person.get_opinion_score("being covered in cum") < 45:
            $ cum_cost = 50
            $ obedience_requirement = 130 - 5*the_person.get_opinion_score("being covered in cum")
            if the_person.get_opinion_score("being covered in cum") < 0:
                $ cum_cost = cum_cost * -the_person.get_opinion_score("being covered in cum")

            if for_pay:
                the_person "Fine, but I want $[cum_cost]."
                "You don't have any time to haggle with her over the price!"
            else:
                the_person "I don't know..."
                "You don't have time to argue with her!"

            menu:
                "Pay her.\n-$[cum_cost]" if not mc.business.has_funds(cum_cost) and for_pay:
                    $ pay_after = True
                    mc.name "Fine! Whatever you want!"
                    $ the_person.change_obedience(-(1 + the_person.get_opinion_score("being submissive"))) #She loses obedience, more if she likes being submissive (you're betgging her!)
                    "You struggle to hold back your orgasm while [the_person.title] gets onto her knees."

                "Pay her.\n-$[cum_cost] (disabled)" if mc.business.funds > cum_cost and for_pay:
                    pass

                "Order her." if the_person.obedience >= obedience_requirement:
                    mc.name "Just get on your knees!"
                    if the_person.get_opinion_score("being covered in cum") < 0:
                        $ the_person.discover_opinion("being covered in cum")
                        $ the_person.change_obedience(-the_person.get_opinion_score("being covered in cum")) #Increases her obedience if you force her to take a cumshot in a way she doesn't like.
                        "[the_person.possessive_title] seems appalled by the idea, but obeys and gets onto her knees."
                    else:
                        "You struggle to hold back your orgasm while [the_person.title] obeys and gets onto her knees."

                "Order her.\nRequires: [obedience_requirement] Obedience (disabled)" if the_person.obedience < obedience_requirement:
                    pass

                "Ignore her.":
                    "No time, here I cum!"
                    "[the_person.possessive_title] takes a step back, clearing the splash zone."
                    $ cum_on_floor_instead = True


        else:
            "[the_person.title] nods and hurries into position for you."

        if cum_on_floor_instead:
            $ climax_controller = ClimaxController(["Cum on the floor.", "air"])
            $ climax_controller.show_climax_menu()
            $ climax_controller.do_clarity_release(the_person)
            "You grunt and climax, blowing your load out onto the floor in thick ropes of hot cum."
            $ the_person.change_slut(the_person.get_opinion_score(["being covered in cum","cum facials", "creampies", "drinking cum"]), 40)
            "She watches from a safe distance, eyes locked on your dick as it spasms and twitches."
            "When you're finished you let go of your cock and take a deep breath."
            the_person "Finished?"
            "You nod."

        else:
            $ the_person.draw_person(position = "kneeling1")
            if the_person.outfit.tits_available():
                if the_person.has_large_tits():
                    "She hefts her big tits up and presents them for you to cum on."
                else:
                    "She leans back on her arms and presents her chest for you to cum on."

            else:
                if the_person.outfit.can_half_off_to_tits():
                    $ strip_list = the_person.outfit.get_half_off_to_tits_list()
                    $ generalised_strip_description(the_person, strip_list, position = "kneeling1", half_off_instead = True)
                    "Tits out, she leans back and presents her chest for you to cum on."
                else:
                    "She leans back and presents her chest to you to cum on."

            $ climax_controller.do_clarity_release(the_person)
            $ the_person.cum_on_tits()
            $ the_person.draw_person(position = "kneeling1")
            "You moan and cum, pulsing thick ropes of cum onto her body."

            if pay_after:
                the_person "Wow... Well, I hope that was worth it to you."
                "You nod wordlessly and hand her the cash she demanded."
                $ mc.business.change_funds(cum_cost)
            else:
                the_person "Wow, you were really saving that up..."


    elif the_choice == "Ask to cum on her face.":
        mc.name "Get on your knees, I want to cum on your face!"
        $ cum_on_floor_instead = False
        $ pay_after = False
        if the_person.effective_sluttiness() + 5 * the_person.get_opinion_score("cum facials") < 35:
            "[the_person.title] shakes her head."
            the_person "What? Of course not!"
            "You want to argue, but you're out of time!"
            $ cum_on_floor_instead = True

        elif the_person.effective_sluttiness() + 5 * the_person.get_opinion_score("cum facials") < 55:
            $ cum_cost = 100
            $ obedience_requirement = 130 - 5*the_person.get_opinion_score("cum facials")
            if the_person.get_opinion_score("cum facials") < 0:
                $ cum_cost = cum_cost * -the_person.get_opinion_score("cum facials")

            if for_pay:
                the_person "Fine, but I want $[cum_cost]."
                "You don't have any time to haggle with her over the price!"
            else:
                the_person "I don't know..."
                "You don't have time to argue with her!"

            menu:
                "Pay her.\n-$[cum_cost]" if not mc.business.has_funds(cum_cost) and for_pay:
                    $ pay_after = True
                    mc.name "Fine! Whatever you want!"
                    $ the_person.change_obedience(-(1 + the_person.get_opinion_score("being submissive")))
                    "You struggle to hold back your orgasm while [the_person.title] gets onto her knees."

                "Pay her.\n-$[cum_cost] (disabled)" if mc.business.funds > cum_cost and for_pay:
                    pass

                "Order her." if the_person.obedience >= obedience_requirement:
                    mc.name "Just get on your knees!"
                    if the_person.get_opinion_score("cum facials") < 0:
                        $ the_person.discover_opinion("cum facials")
                        $ the_person.change_obedience(-the_person.get_opinion_score("cum facials"))
                        "[the_person.possessive_title] seems appalled by the idea, but obeys and gets onto her knees."
                    else:
                        "You struggle to hold back your orgasm while [the_person.title] obeys and gets onto her knees."

                "Order her.\nRequires: [obedience_requirement] Obedience (disabled)" if the_person.obedience < obedience_requirement:
                    pass

                "Ignore her.":
                    "No time, here I cum!"
                    "[the_person.possessive_title] takes a step back, clearing the splash zone."
                    $ cum_on_floor_instead = True
        else:
            "[the_person.title] nods and hurries into position for you."

        if cum_on_floor_instead:
            $ climax_controller = ClimaxController(["Cum on the floor.", "air"])
            $ climax_controller.show_climax_menu()
            $ climax_controller.do_clarity_release(the_person)
            "You grunt and climax, blowing your load out onto the floor in thick ropes of hot cum."
            $ the_person.change_slut(the_person.get_opinion_score(["being covered in cum","cum facials", "creampies", "drinking cum"]), 40)
            "She watches from a safe distance, eyes locked on your dick as it spasms and twitches."
            "When you're finished you let go of your cock and take a deep breath."
            the_person "Finished?"
            "You nod."

        else:
            $ the_person.draw_person(position = "kneeling1")
            if the_person.get_opinion_score("drinking cum") > 0:
                "[the_person.possessive_title] looks up at you from her knees and sticks her tongue out, ready to take your load."
            else:
                "[the_person.possessive_title] looks up at you from her knees, waiting for her facial."
            $ climax_controller.do_clarity_release(the_person)
            $ the_person.cum_on_face()
            $ the_person.draw_person(position = "kneeling1")
            "You moan and cum, pulsing thick ropes of cum onto her face."

            if pay_after:
                the_person "Wow... Well, I hope that was worth it to you."
                "You nod wordlessly and hand her the cash she demanded."
                $ mc.business.change_funds(cum_cost)
            else:
                the_person "Wow, you were really saving that up..."

    elif the_choice == "Ask to cum in her mouth.":
        mc.name "Get on your knees, I want to cum in your mouth!"
        $ cum_on_floor_instead = False
        $ pay_after = False
        if the_person.effective_sluttiness() + 5 * the_person.get_opinion_score("drinking cum") < 45:
            "[the_person.title] shakes her head."
            the_person "What? In my mouth? Of course not!"
            "You want to argue, but you're out of time!"
            $ cum_on_floor_instead = True

        elif the_person.effective_sluttiness() + 5 * the_person.get_opinion_score("drinking cum") < 65:
            $ cum_cost = 200
            $ obedience_requirement = 130 - 5*the_person.get_opinion_score("drinking cum")
            if the_person.get_opinion_score("drinking cum") < 0:
                $ cum_cost = cum_cost * -the_person.get_opinion_score("drinking cum")

            if for_pay:
                the_person "Fine, but I want $[cum_cost]."
                "You don't have any time to haggle with her over the price!"
            else:
                the_person "I don't know..."
                "You don't have time to argue with her!"

            menu:
                "Pay her.\n-$[cum_cost]" if not mc.business.has_funds(cum_cost) and for_pay:
                    $ pay_after = True
                    mc.name "Fine! Whatever you want! Just get my cock in your mouth!"
                    $ the_person.change_obedience(-(1 + the_person.get_opinion_score("being submissive")))
                    "You struggle to hold back your orgasm while [the_person.title] gets onto her knees."

                "Pay her.\n-$[cum_cost] (disabled)" if mc.business.funds > cum_cost and for_pay:
                    pass

                "Order her." if the_person.obedience >= obedience_requirement:
                    mc.name "Just get my cock in your mouth!"
                    if the_person.get_opinion_score("drinking cum") < 0:
                        $ the_person.discover_opinion("drinking cum")
                        $ the_person.change_obedience(-the_person.get_opinion_score("drinking cum"))
                        "[the_person.possessive_title] seems appalled by the idea, but obeys and gets onto her knees."
                    else:
                        "You struggle to hold back your orgasm while [the_person.title] obeys and gets onto her knees."

                "Order her.\nRequires: [obedience_requirement] Obedience (disabled)" if the_person.obedience < obedience_requirement:
                    pass

                "Ignore her.":
                    "No time, here I cum!"
                    "[the_person.possessive_title] takes a step back, clearing the splash zone."
                    $ cum_on_floor_instead = True
        else:
            "[the_person.title] nods and hurries into position for you."

        if cum_on_floor_instead:
            $ climax_controller = ClimaxController(["Cum on the floor.", "air"])
            $ climax_controller.show_climax_menu()
            $ climax_controller.do_clarity_release(the_person)
            "You grunt and climax, blowing your load out onto the floor in thick ropes of hot cum."
            $ the_person.change_slut(the_person.get_opinion_score(["being covered in cum","cum facials", "creampies", "drinking cum"]), 40)
            "She watches from a safe distance, eyes locked on your dick as it spasms and twitches."
            "When you're finished you let go of your cock and take a deep breath."
            the_person "Finished?"
            "You nod."

        else:
            $ the_person.draw_person(position = "kneeling1")
            if the_person.get_opinion_score("drinking cum") > 0:
                "[the_person.possessive_title] looks up at you and licks her lips."
                the_person "Give me all of that hot cum, I'm going to guzzle it down for you!"
                $ the_person.discover_opinion("drinking cum")
            else:
                "[the_person.possessive_title] looks up at you from her knees, mouth open and ready for her load."

            #TODO: Add a "Cum down her throat" path.

            $ climax_controller = ClimaxController(["Cum in her mouth.", "mouth"],["Slam your cock down her throat!", "throat"])
            $ the_choice = climax_controller.show_climax_menu()
            if the_choice == "Cum in her mouth.":
                "You slap the tip of your cock down onto her soft lips and give yourself up to the pleasure."
                $ climax_controller.do_clarity_release(the_person)
                $ the_person.cum_in_mouth()
                $ the_person.draw_person(position = "kneeling1")
                if the_person.get_opinion_score("drinking cum") > 0:
                    "Her eyes flutter as you shoot thick ropes of cum to the back of her mouth. She moans, apparently happy about it."
                else:
                    "You moan and cum, pulsing thick ropes of cum into her mouth and across her tongue."

                if the_person.get_opinion_score("drinking_cum") > 0 or the_person.effective_sluttiness() >= 60:
                    "When you're finished [the_person.possessive_title] gives your cock a gentle kiss, then closes her lips and swallows."
                    "She gives a satisfied sigh when she's finished gulping it all down."
                else:
                    "She stays still until you're finished, then leans back from your dick and spits your cum out onto the floor."


                if pay_after:
                    the_person "Wow... Well, I hope that was worth it to you."
                    "You nod wordlessly and hand her the cash she demanded."
                    $ mc.business.change_funds(cum_cost)
                else:
                    the_person "Wow, you were really saving that up..."

            elif the_choice == "Slam your cock down her throat!":
                "You slap the tip of your cock down onto her soft lips and place a hand on the back of her head."
                "Without any warning you pull her down onto your cock, pushing it all the way to the back of her mouth."
                "Your feel your tip glide against the very back of her throat, and the feeling makes you cum."
                $ demands_money = False
                if the_person.effective_sluttiness() + 10*the_person.get_opinion_score(["drinking cum", "being submissive"]) < 40:
                    if the_person.sex_skills["Oral"] < 4:
                        "[the_person.title]'s eyes flash open as wide as they will go. She gags immediately and hard."
                        "Your body acts on auto-pilot, pulling your dick free of her mouth before teeth get involved."
                        "She gasps loudly, half-choking, as you moan and start to fire your load onto her beet-red face."
                        $ climax_controller = ClimaxController(["Cum on her face.", "face"])
                        $ climax_controller.show_climax_menu()
                        $ climax_controller.do_clarity_release(the_person)
                        $ the_person.cum_on_face()
                        $ the_person.draw_person(position = "kneeling1")
                        "Your hot cum splashes onto [the_person.possessive_title] while she tries to recover from your assault on her throat."
                        "After a long while she wipes some tears from her eyes and looks up at you."
                        the_person "What... The... Hell... Was that?"
                        mc.name "Sorry, I just kind of got carried away. I thought you'd be into it..."

                    else:
                        "[the_person.title] gags as you slam you launch your surprise assault on her throat, but seems to manage it decently well."
                        "She pounds on your thighs, trying to get you to pull back, but it's too late for that!"
                        $ climax_controller.do_clarity_release(the_person)
                        $ the_person.cum_in_mouth()
                        $ the_person.draw_person(position = "kneeling1")
                        "[the_person.possessive_title] has to close her eyes and focus as you dump your load down her throat."
                        "She gulps loudly, trying not to choke on the sudden rush of cum. As soon as you're finished she pounds her fists on your thighs again."
                        "You let go of her head and pull your hips back. She gasps for air as soon as your cock ic clear of her mouth."
                        the_person "What the fuck was that? I could have bitten your dick off, you know!"
                        mc.name "I didn't think you were that kind of girl. Sorry, I thought you'd be into it..."

                    $ the_person.change_love(-5 + 2*the_person.get_opinion_score(["drinking cum","being submissive"]))
                    $ the_person.change_obedience(-5 + 2*the_person.get_opinion_score(["drinking cum", "being submissive"]))
                    $ the_person.change_slut(2*the_person.get_opinion_score(["drinking cum","being submissive"]))
                    "She shakes her head angrily."
                    the_person "No, I wasn't into it!"

                    if the_person.get_opinion_score("being_submissive") <= 0 and for_pay:
                        $ demands_money = True
                else:
                    if the_person.sex_skills["Oral"] < 4:
                        "[the_person.title]'s eyes flash open as wide as they will go. She gags immediately and hard."
                        "You briefly worry about her, but after a split second of surprise she pushes herself deeper onto your cock."
                        "This doesn't have much more success, and all she does is make herself gag more, but you appreciate the effort."
                        $ climax_controller.do_clarity_release(the_person)
                        $ the_person.cum_in_mouth()
                        $ the_person.draw_person(position = "kneeling1")
                        "You close your eyes and moan, dumping your load down her waiting throat."
                        "[the_person.possessive_title] gags and chokes, blowing bubbles of spit and cum out her nose and around the base of your shaft."
                        "She tries her best to drink it all down, gulping between choking fits."
                        "Soon enough the worst of it has passed, and you let go of her head."
                        "She slides herself off of your dick, gasping for fresh air as soon as you're out of her mouth."
                        the_person "Oh fuck... Give a girl some warning next time..."
                        mc.name "Sorry, it just felt right."
                        if the_person.get_opinion_score("being submissive") > 0:
                            the_person "Don't be sorry, it was hot. The look on your face, your hand on my head..."
                            $ the_person.discover_opinion("being submissive")
                            "She bites her lip and gives a soft moan."
                        else:
                            the_person "I'm going to need a little more practice before I can do that without any warm up."
                            "She coughs one last time and wipes her lips with the back of her hand."

                    else:

                        "[the_person.title]'s eyes turn up to look at you, eyelids fluttering with surprise."
                        "Despite the ambush she takes you like a champ, swallowing the entirety of your cock without flinching."
                        $ climax_controller.do_clarity_release(the_person)
                        $ the_person.cum_in_mouth()
                        $ the_person.draw_person(position = "kneeling1")
                        "You close your eyes and moan, dumping your load down her waiting throat. Her eyelids flutter some more with each pulse of cum."
                        "[the_person.possessive_title] takes your load, gulping it as fast as you can give it to her."
                        "Soon enough you're finished, and you take your hand off of the back of her head."
                        "She lingers for a moment, then pulls her head back with slow deliberateness. Her tongue trails across your sensitive tip before she breaks contact entirely."
                        the_person "Whew, that was a... surprise. You might want to give me some warning next time."
                        "You shrug and smile."
                        mc.name "It doesn't look like you needed it. That was impressive."
                        if the_person.get_opinion_score("being submissive") > 0:
                            the_person "Your hand on my head makes a cock in my throat feel so right."
                            $ the_person.discover_opinion("being submissive")
                            "She bites her lip and gives a soft moan."
                        else:
                            the_person "It's a talent of mine, I'll admit that."
                            "She wipes her lips with the back of her hand."


                if demands_money and for_pay: #Demands extra cash for the stunt you just pulled.
                    $ bribe_cost = 100
                    if the_person.get_opinion_score(["drinking cum","being submissive"]) < 0:
                        $ bribe_cost = 200

                    the_person "Now you know that stunt is going to cost you extra."
                    the_person "$[bribe_cost] and maybe I can overlook what you've just done."
                    menu:
                        "Pay her. -$[bribe_cost]" if bribe_cost <= mc.business.funds:
                            "You sigh and roll your eyes, but [the_person.title] seems unlikely to budge on the price."
                            "You pull out the cash, thinking to yourself that you're lucky she'll take a bribe at all."
                            $ mc.business.change_funds(-bribe_cost)
                            $ the_person.change_obedience(1 - the_person.get_opinion_score("taking control")) #If she likes taking control she may actually lose Obedience by demanding a bribe.

                        "Pay her. -$[bribe_cost] (disabled)" if bribe_cost > mc.business.funds:
                            pass

                        "Refuse.":
                            mc.name "I'm not paying you, I've already gotten what I paid for."
                            "[the_person.title] glares at you, but quickly realises she doesn't have much leverage right now."
                            $ the_person.change_happiness(-10 + 2*the_person.get_opinion_score("being submissive"))
                            $ the_person.change_love(-5 + the_person.get_opinion_score("being submissive"))
                            $ the_person.change_obedience(-5 + the_person.get_opinion_score("being submissive"))
                            $ the_person.change_slut(the_person.get_opinion_score("being submissive"))
                            the_person "Whatever, you better not expect me to be doing this again for you..."


    return
