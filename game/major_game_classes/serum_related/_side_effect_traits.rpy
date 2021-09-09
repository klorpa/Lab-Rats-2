#Serum trait functions. Each serum trait can have up to four key functions: on_apply, on_remove, on_turn, and on_day. These are run at various points throughout the game.
init -1:
    python:
        ## depressant_side_effect_functions ##
        def depressant_side_effect_on_apply(the_person, the_serum, add_to_log):
            the_person.change_happiness(-20)

        ## libido_suppressant_functions ##
        def libido_suppressant_on_apply(the_person, the_serum, add_to_log):
            the_person.change_slut(-20)

        def libido_suppressant_on_remove(the_person, the_serum, add_to_log):
            the_person.change_slut(20)

        ## anxiety_provoking_functions ##
        def anxiety_provoking_on_turn(the_person, the_serum, add_to_log):
            the_person.change_happiness(-3, add_to_log)

        ## performance_inhibitor_functions ##
        def performance_inhibitor_on_apply(the_person, the_serum, add_to_log):
            the_person.change_int(-1, add_to_log)
            the_person.change_focus(-1, add_to_log)
            the_person.change_cha(-1, add_to_log)

        def performance_inhibitor_on_remove(the_person, the_serum, add_to_log):
            the_person.change_int(1, add_to_log)
            the_person.change_focus(1, add_to_log)
            the_person.change_cha(1, add_to_log)

        ## mood_swings_functions ##
        def mood_swings_on_turn(the_person, the_serum, add_to_log):
            swing = renpy.random.randint(0,1)
            if swing == 0:
                the_person.change_happiness(-10, add_to_log)
            else:
                the_person.change_happiness(10, add_to_log)

        ## Sedative functions ##
        def sedative_on_apply(the_person, the_serum, add_to_log):
            the_person.change_energy(-20, add_to_log)
            the_person.change_max_energy(-20, add_to_log)

        def sedative_on_remove(the_person, the_serum, add_to_log):
            the_person.change_max_energy(20, add_to_log) #They don't get the normal energy back instantly, it has to come back on it's own

        ## Slow release sedative functions ##
        def slow_release_sedative_on_turn(the_person, the_serum, add_to_log):
            the_person.change_energy(-10)

        ## Toxic functions ##
        def toxic_on_apply(the_person, the_serum, add_to_log):
            the_person.serum_tolerance += -1

        def toxic_on_remove(the_person, the_serum, add_to_log):
            the_person.serum_tolerance += 1

        ## libido suppresant ##
        def libido_suppresent_on_apply(the_person, the_serum, add_to_log):
            the_person.change_max_arousal(50, add_to_log)

        def libido_suppresent_on_remove(the_person, the_serum, add_to_log):
            the_person.change_max_arousal(-50, add_to_log)

        ## hair colour changes ##
        def hair_colour_wild_on_turn(the_person, the_serum, add_to_log):
            random_colour = Color((renpy.random.randint(0,255), renpy.random.randint(0,255), renpy.random.randint(0,255)))

            hair_colour_change_on_turn(random_colour, the_person, the_serum, add_to_log)

        def hair_colour_dull_on_turn(the_person, the_serum, add_to_log):
            current_colour = Color(rgb=(the_person.hair_colour[1][0], the_person.hair_colour[1][1], the_person.hair_colour[1][2]))
            goal_colour = current_colour.replace_hsv_saturation(0.0)

            hair_colour_change_on_turn(goal_colour, the_person, the_serum, add_to_log)



label instantiate_side_effect_traits(): #Creates all of the default LR2 serum trait objects.
    python:
        depressant_side_effect = SerumTrait(name = "Depressant",
            desc = "An unintended interaction produces a sudden and noticable drop in the recipients mood without any corresponding improvement when the serum expires.",
            positive_slug = "None",
            negative_slug = "-20 Happiness When Applied, -$5 Value",
            value_added = -5,
            on_apply = depressant_side_effect_on_apply,
            is_side_effect = True)

        unpleasant_taste_side_effect = SerumTrait(name =  "Unpleasant Taste",
            desc = "This serum has a prominent and decidedly unpleasant taste. While it does not decrease the effectiveness of the serum it has a large impact on its value when sold.",
            positive_slug = "None",
            negative_slug = "-$20 Value",
            value_added = -20,
            is_side_effect = True)

        bad_reputation = SerumTrait(name = "Bad Reputation",
            desc = "This serum design has developed a particularly bad reputation. Regardless of if it is based on facts is has a significant effect on the price customers are willing to pay.",
            positive_slug = "None",
            negative_slug = "-$20 Value",
            value_added = -20,
            is_side_effect = True)

        unstable_reaction = SerumTrait(name = "Unstable Reaction",
            desc = "The reaction used to create this serum was less stable than initialy hypothesised. Reduces serum duration by two turns.",
            positive_slug = "None",
            negative_slug = "-2 Turn Duration, -$5 Value",
            value_added = -5,
            duration_added = -2,
            is_side_effect = True)

        manual_synthesis_required = SerumTrait(name = "Manual Synthesis Required",
            desc = "A step in this serums manufacturing process requires manual intervention, preventing the use of time saving automation. This has no impact on effectivness or value, but increases the amount of production effort required.",
            positive_slug = "None",
            negative_slug = "+15 Production/Batch",
            production_added = 15,
            is_side_effect = True)

        libido_suppressant = SerumTrait(name = "Libido Suppressant",
            desc = "An unintended interaction results in a major decrease in the recipients sex drive for the duration of this serum.",
            positive_slug = "None",
            negative_slug = "-20 Sluttiness, -$5 Value",
            value_added = -5,
            on_apply = libido_suppressant_on_apply,
            on_remove = libido_suppressant_on_remove,
            is_side_effect = True)

        anxiety_provoking = SerumTrait(name = "Anxiety Provoking",
            desc = "An unintended interaction creates a subtle but pervasive sense of anxiety in the recipient. This has a direct effect on their happiness.",
            positive_slug = "None",
            negative_slug = "-3 Happiness/Turn, -$5 Value",
            value_added = -5,
            on_turn = anxiety_provoking_on_turn,
            is_side_effect = True)

        performance_inhibitor = SerumTrait(name = "Performance Inhibitor",
            desc = "For reasons not understood by your R&D team this serum causes a general decrease in the recipients to do work for the duration of the serum.",
            positive_slug = "None",
            negative_slug = "-1 Intelligence, Focus, and Charisma, -$5 Value",
            value_added = -5,
            on_apply = performance_inhibitor_on_apply,
            on_remove = performance_inhibitor_on_remove,
            is_side_effect = True)

        mood_swings = SerumTrait(name = "Mood Swings",
            desc = "The recipient suffers large, sudden, and unpleasant mood swings.",
            positive_slug = "None",
            negative_slug = "Random +10 or -10 Happiness/Turn, -$10 Value",
            value_added = -10,
            on_day = mood_swings_on_turn,
            is_side_effect = True)

        sedative = SerumTrait(name = "Accidental Sedative",
            desc = "This serum has the unintended side effect of minorly sedating the recipient. Their maximum energy is reduced for the duration.",
            positive_slug = "None",
            negative_slug = "-20 Maximum Energy, -$5 Value",
            value_added = -5,
            on_apply = sedative_on_apply,
            on_remove = sedative_on_remove,
            is_side_effect = True)

        slow_release_sedative = SerumTrait(name = "Slow Acting Sedative",
            desc = "This serum produces slow acting sedative effects, reducing how quickly the recipent bounces back from tiring tasks. Reduces energy gain for the duration.",
            positive_slug = "None",
            negative_slug = "-10 Energy per Turn, -$5 Value",
            value_added = -5,
            on_turn = slow_release_sedative_on_turn,
            is_side_effect = True)

        toxic_side_effect = SerumTrait(name = "Toxic",
            desc = "Mildly toxic interactions make this serum dangerous to mix with other medications at any dose. Reduces serum tolerance for the duration.",
            positive_slug = "None",
            negative_slug = "-1 Serum Tolerance, -$5 Value",
            value_added = -5,
            on_apply = toxic_on_apply,
            on_remove = toxic_on_remove,
            is_side_effect = True)

        libido_suppressant_effect = SerumTrait(name = "Stimulation Suppressant",
            desc = "Interactions with the body's nervous system makes it very difficult for the subject to orgasm. A common side effect for many medications.",
            positive_slug = "None",
            negative_slug = "+40 Max Arousal, -$5 Value",
            value_added = -5,
            on_apply = libido_suppresent_on_apply,
            on_remove = libido_suppresent_on_remove,
            is_side_effect = True)

        hair_colour_wild_effect = SerumTrait(name = "Hair Colour Shifts",
            desc = "Complex interactions produce visible changes in hair colour. Produces random and sometimes striking changes in hair colour over time.",
            positive_slug = "None",
            negative_slug = "Random Hair Colour Changes, -$5 Value",
            value_added = -5,
            on_turn = hair_colour_wild_on_turn,
            exclude_tags = "Dye",
            is_side_effect = True)

        hair_colour_dull_effect = SerumTrait(name = "Dull Hair",
            desc = "Complex interactions produce visible changes in hair colour. Has the effect of dulling down the hair colour of the subject.",
            positive_slug = "None",
            negative_slug = "Reduces Hair Saturation, -$5 Value",
            value_added = -5,
            on_turn = hair_colour_dull_on_turn,
            exclude_tags = "Dye",
            is_side_effect = True)

        list_of_side_effects.append(depressant_side_effect)
        list_of_side_effects.append(bad_reputation)
        list_of_side_effects.append(unpleasant_taste_side_effect)
        list_of_side_effects.append(unstable_reaction)
        list_of_side_effects.append(manual_synthesis_required)
        list_of_side_effects.append(libido_suppressant)
        list_of_side_effects.append(anxiety_provoking)
        list_of_side_effects.append(performance_inhibitor)
        list_of_side_effects.append(mood_swings)
        list_of_side_effects.append(sedative)
        list_of_side_effects.append(slow_release_sedative)
        list_of_side_effects.append(toxic_side_effect)
        list_of_side_effects.append(libido_suppressant_effect)
        list_of_side_effects.append(hair_colour_wild_effect)
        list_of_side_effects.append(hair_colour_dull_effect)

    return
