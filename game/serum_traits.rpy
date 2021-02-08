#Serum trait functions. Each serum trait can have up to four key functions: on_apply, on_remove, on_turn, and on_day. These are run at various points throughout the game.
init -1:
    python:
        ## suggestion_drugs_functions ##
        def suggestion_drugs_on_apply(the_person, add_to_log):
            the_person.add_suggest_effect(10, add_to_log)

        def suggestion_drugs_on_remove(the_person, add_to_log):
            the_person.remove_suggest_effect(10)

        ## high_concentration_drug_functions ##
        def high_con_drugs_on_apply(the_person, add_to_log):
            the_person.add_suggest_effect(25, add_to_log)

        def high_con_drugs_on_remove(the_person, add_to_log):
            the_person.remove_suggest_effect(25)

        def high_con_drugs_on_turn(the_person, add_to_log):
            the_person.change_happiness(-2, add_to_log)

        ## sedatives_trait_functions ##
        def sedatives_trait_on_apply(the_person, add_to_log):
            the_person.change_obedience(10, add_to_log)
            the_person.change_cha(-1, add_to_log)
            the_person.change_focus(-1, add_to_log)
            the_person.change_int(-1, add_to_log)

        def sedatives_trait_on_remove(the_person, add_to_log):
            the_person.change_obedience(-10, add_to_log)
            the_person.change_cha(1, add_to_log)
            the_person.change_focus(1, add_to_log)
            the_person.change_int(1, add_to_log)

        ## obedience_enhancer_functions ##
        def obedience_enhancer_on_apply(the_person, add_to_log):
            the_person.change_obedience(10, add_to_log)

        def obedience_enhancer_on_remove(the_person, add_to_log):
            the_person.change_obedience(-10, add_to_log)

        ## large_obedience_enhancer_functions ##
        def large_obedience_enhancer_on_apply(the_person, add_to_log):
            the_person.change_obedience(20, add_to_log)

        def large_obedience_enhancer_on_remove(the_person, add_to_log):
            the_person.change_obedience(-20, add_to_log)

        def large_obedience_enhancer_on_turn(the_person, add_to_log):
            the_person.change_slut_temp(-2, add_to_log)
            if the_person.sluttiness < the_person.core_sluttiness:
                if renpy.random.randint(0,100) < 10:
                    the_person.change_slut_core(-2, add_to_log, fire_event = False) #If this brings her into negative relative sluttiness she might lose core sluttiness as well.

        ## aphrodisiac_functions ##
        def aphrodisiac_on_apply(the_person, add_to_log):
            the_person.change_slut_core(15, add_to_log, fire_event = False)
            the_person.change_slut_temp(15, add_to_log)

        def aphrodisiac_on_remove(the_person, add_to_log):
            the_person.change_slut_core(-15, add_to_log, fire_event = False)
            the_person.change_slut_temp(-15, add_to_log)

        def aphrodisiac_on_turn(the_person, add_to_log):
            the_person.change_obedience(-2, add_to_log)

        ## caffeine_trait functions##
        def caffeine_trait_on_apply(the_person, add_to_log):
            the_person.change_max_energy(20, add_to_log)
            the_person.change_energy(20, add_to_log)
            the_person.change_obedience(-15, add_to_log)

        def caffeine_trait_on_remove(the_person, add_to_log):
            the_person.change_max_energy(-20, add_to_log)
            the_person.change_obedience(15, add_to_log)

        ## refined_caffeine_trait functions ##
        def refined_caffeine_trait_on_apply(the_person, add_to_log):
            the_person.change_max_energy(20, add_to_log)
            the_person.change_energy(20, add_to_log)

        def refined_caffeine_trait_on_remove(the_person, add_to_log):
            the_person.change_max_energy(-20, add_to_log)

        ## slutty_caffeine_trait functions ##
        def slutty_caffeine_trait_on_apply(the_person, add_to_log):
            the_person.change_max_energy(20, add_to_log)
            the_person.change_energy(20, add_to_log)
            the_person.change_slut_temp(15, add_to_log)
            the_person.change_slut_core(15, add_to_log)

        def slutty_caffeine_trait_on_remove(the_person, add_to_log):
            the_person.change_max_energy(-20, add_to_log)
            the_person.change_slut_temp(-15, add_to_log)
            the_person.change_slut_core(-15, add_to_log)

        ## love_potion_functions ##
        def love_potion_on_apply(the_person, add_to_log):
            the_person.change_love(20, add_to_log)

        def love_potion_on_remove(the_person, add_to_log):
            the_person.change_love(-20, add_to_log)


        ## off_label_drugs_functions ##
        def off_label_drugs_on_apply(the_person, add_to_log):
            the_person.add_suggest_effect(30, add_to_log)

        def off_label_drugs_on_remove(the_person, add_to_log):
            the_person.remove_suggest_effect(30 )

        ## mood_enhancer_functions ##
        def mood_enhancer_on_turn(the_person, add_to_log):
            the_person.change_happiness(5, add_to_log)
            the_person.change_obedience(-2, add_to_log)

        ## blood_brain_pen_functions ##
        def blood_brain_pen_on_apply(the_person, add_to_log):
            the_person.add_suggest_effect(50, add_to_log)

        def blood_brain_pen_on_remove(the_person, add_to_log):
            the_person.remove_suggest_effect(50)

        ## breast_enhancement_functions ##
        def breast_enhancement_on_turn(the_person, add_to_log):
            if renpy.random.randint(0,100) < 25:
                new_tits = get_larger_tits(the_person.tits)
                if new_tits != the_person.tits: #Double check we don't already have them to avoid increasing breast weight infinitely
                    the_person.tits = new_tits
                    the_person.personal_region_modifiers["breasts"] += 0.1 #Her breasts recieve a boost in region weight because they're natural.

        def breast_reduction_on_turn(the_person, add_to_log):
            if renpy.random.randint(0,100) < 25:
                new_tits = get_smaller_tits(the_person.tits)
                if new_tits != the_person.tits:
                    the_person.tits = new_tits
                    the_person.personal_region_modifiers["breasts"] -= 0.1 #Her breasts recieve a boost in region weight because they're natural.

        ## focus_enhancement_functions ##
        def focus_enhancement_on_apply(the_person, add_to_log):
            the_person.change_focus(2, add_to_log)

        def focus_enhancement_on_remove(the_person, add_to_log):
            the_person.change_focus(-2, add_to_log)

        ## int_enhancement_functions ##
        def int_enhancement_on_apply(the_person, add_to_log):
            the_person.change_int(2, add_to_log)

        def int_enhancement_on_remove(the_person, add_to_log):
            the_person.change_int(-2, add_to_log)

        ## cha_enhancement_functions ##
        def cha_enhancement_on_apply(the_person, add_to_log):
            the_person.change_cha(2, add_to_log)

        def cha_enhancement_on_remove(the_person, add_to_log):
            the_person.change_cha(-2, add_to_log)

        ## happiness_tick_functions ##
        def happiness_tick_on_turn(the_person, add_to_log):
            the_person.change_happiness(3, add_to_log)

        ## mind_control_agent_functions ##
        def mind_control_agent_on_apply(the_person, add_to_log):
            the_person.add_suggest_effect(70, add_to_log)

        def mind_control_agent_on_remove(the_person, add_to_log):
            the_person.remove_suggest_effect(70)

        ## permanent_bimbo_functions ##
        def permanent_bimbo_on_apply(the_person, add_to_log):
            the_person.change_slut_core(10, add_to_log, fire_event = True)
            the_person.change_slut_temp(10, add_to_log)
            the_person.change_obedience(10, add_to_log)

            display_name = the_person.create_formatted_title("???")
            if the_person.title:
                display_name = the_person.title
            if the_person.int > 1:
                the_person.int = 1
                if (add_to_log):
                    mc.log_event(display_name + ": Intelligence reduced to 1", "float_text_blue")
            the_person.personality = bimbo_personality
            if add_to_log:
                mc.log_event(display_name + ": Personality changed. Now: Bimbo", "float_text_pink")

        ## Pregnancy related serum trait functions ##
        def fertility_enhancement_on_apply(the_person, add_to_log):
            the_person.fertility_percent += 20
            display_name = the_person.create_formatted_title("???")
            if the_person.title:
                display_name = the_person.title
            if add_to_log:
                mc.log_event(the_person.title + ": +20 Fertility", "float_text_red")

        def fertility_enhancement_on_remove(the_person, add_to_log):
            the_person.fertility_percent += -20

        def fertility_suppression_on_apply(the_person, add_to_log):
            the_person.fertility_percent += -20
            display_name = the_person.create_formatted_title("???")
            if the_person.title:
                display_name = the_person.title
            if add_to_log:
                mc.log_event(the_person.title + ": -20 Fertility", "float_text_red")

        def fertility_suppression_on_remove(the_person, add_to_log):
            the_person.fertility_percent += +20

        def birth_control_suppression_on_apply(the_person, add_to_log):
            the_person.bc_penalty += 40
            display_name = the_person.create_formatted_title("???")
            if the_person.title:
                display_name = the_person.title
            if add_to_log:
                mc.log_event(display_name + ": Birth control effectiveness reduced by 40%", "float_text_grey")

        def birth_control_suppression_on_remove(the_person, add_to_log):
            the_person.bc_penalty += -40

        def lactation_hormones_on_apply(the_person, add_to_log):
            the_person.lactation_sources += 1
            display_name = the_person.create_formatted_title("???")
            if the_person.title:
                display_name = the_person.title
            if add_to_log:
                if the_person.lactation_sources == 1:
                    mc.log_event(display_name + ": Has begun lactating", "float_text_blue")
                else:
                    mc.log_event(display_name + ": Lactation increases", "float_text_blue")

        def lactation_hormones_on_remove(the_person,add_to_log):
            the_person.lactation_sources += -1

        def massive_pregnancy_accelerator_on_turn(the_person, add_to_log):
            the_person.event_triggers_dict["preg_tits_date"] = the_person.event_triggers_dict.get("preg_tits_date", day) - 1
            the_person.event_triggers_dict["preg_transform_day"] = the_person.event_triggers_dict.get("preg_transform_day", day) - 1
            the_person.event_triggers_dict["preg_finish_announce_day"] = the_person.event_triggers_dict.get("preg_finish_announce_day", day) - 1

        def pregnancy_accelerator_on_day(the_person, add_to_log):
            the_person.event_triggers_dict["preg_tits_date"] = the_person.event_triggers_dict.get("preg_tits_date", day) - 1
            the_person.event_triggers_dict["preg_transform_day"] = the_person.event_triggers_dict.get("preg_transform_day", day) - 1
            the_person.event_triggers_dict["preg_finish_announce_day"] = the_person.event_triggers_dict.get("preg_finish_announce_day", day) - 1

        def pregnancy_decellerator_on_day(the_person, add_to_log):
            the_person.event_triggers_dict["preg_tits_date"] = the_person.event_triggers_dict.get("preg_tits_date", day) + 1
            the_person.event_triggers_dict["preg_transform_day"] = the_person.event_triggers_dict.get("preg_transform_day", day) + 1
            the_person.event_triggers_dict["preg_finish_announce_day"] = the_person.event_triggers_dict.get("preg_finish_announce_day", day) + 1

        ## nora_serum_up_trait ##
        def nora_suggest_up_on_apply(the_person, add_to_log):
            the_person.add_suggest_effect(50, add_to_log)

        def nora_suggest_up_on_remove(the_person, add_to_log):
            the_person.remove_suggest_effect(50)

        def nora_nightmares_on_day(the_person, add_to_log):
            the_person.change_happiness(-15, add_to_log)

        def nora_obedience_swing_on_turn(the_person, add_to_log):
            change_amount = renpy.random.randint(-15,15)
            the_person.change_obedience(change_amount)

        def nora_sluttiness_boost_on_apply(the_person, add_to_log):
            the_person.change_slut_core(20, add_to_log, fire_event = False)
            the_person.change_slut_temp(20, add_to_log)

        def nora_sluttiness_boost_on_remove(the_person, add_to_log):
            the_person.change_slut_core(-20, add_to_log, fire_event = False)
            the_person.change_slut_temp(-20, add_to_log)


        ## nora_special_unlock_taits
        def nora_reward_mother_trait_on_turn(the_person, add_to_log):
            amount_change = __builtin__.round((the_person.sluttiness - the_person.love)/10)
            if amount_change > 0:
                the_person.change_love(amount_change, add_to_log)


        def nora_reward_sister_trait_on_day(the_person, add_to_log):
            amount_change = __builtin__.round((the_person.obedience - 100)/10)
            if amount_change > 0:
                the_person.change_slut_core(amount_change, add_to_log)

        def nora_reward_cousin_trait_on_day(the_person, add_to_log):
            amount_change = __builtin__.round((the_person.love)/-5)
            if amount_change > 0:
                the_person.change_slut_core(amount_change, add_to_log)

        def nora_reward_nora_trait_on_apply(the_person, add_to_log):
            amount = 5 * mc.int
            the_person.change_slut_temp(amount, add_to_log)
            the_person.change_obedience(amount, add_to_log)

        def nora_reward_nora_trait_on_remove(the_person, add_to_log):
            amount = 5 * mc.int
            the_person.change_slut_temp(-amount, add_to_log)
            the_person.change_obedience(-amount, add_to_log)

        def nora_reward_high_love_trait_on_turn(the_person, add_to_log):
            if the_person.core_sluttiness > the_person.love:
                the_person.change_slut_core(-1, add_to_log)
                the_person.change_love(1, add_to_log)

        def nora_reward_low_love_trait_on_apply(the_person, add_to_log):
            the_person.change_love(-50, add_to_log)

        def nora_reward_low_love_trait_on_remove(the_person, add_to_log):
            the_person.change_love(50, add_to_log)

        def nora_reward_high_obedience_trait_on_turn(the_person, add_to_log):
            amount = __builtin__.round((the_person.obedience-100)/5)
            the_person.change_happiness(amount, add_to_log)

        def nora_reward_high_slut_trait_on_apply(the_person, add_to_log):
            amount = the_person.sluttiness - the_person.core_sluttiness
            if amount > 5:
                amount = 5
            if amount > 0:
                the_person.change_slut_temp(-amount)
                the_person.change_slut_core(amount, add_to_log)

        def nora_reward_genius_trait_on_apply(the_person, add_to_log):
            if (the_person.charisma < 5):
                the_person.charisma = 5
            if (the_person.int < 5):
                the_person.int = 5
            if (the_person.focus < 5):
                the_person.focus = 5

        def nora_reward_hucow_trait_on_apply(the_person, add_to_log): #TODO Hook this up so it's possible to recieve this.
            the_person.bc_penalty += 75
            the_person.fertility_percent += 70
            the_person.lactation_sources += 3

            the_person.tits = get_larger_tits(the_person.tits) #Her tits start to swell.
            the_person.tits = get_larger_tits(the_person.tits)
            the_person.personal_region_modifiers["breasts"] = the_person.personal_region_modifiers["breasts"] + 0.2 #As her tits get larger they also become softer, unlike large fake tits. (Although even huge fake tits get softer)

            display_name = the_person.create_formatted_title("???")
            if the_person.title:
                display_name = the_person.title


            if add_to_log:
                mc.log_event(display_name + ": Birth control effectiveness reduced by 75%", "float_text_grey")
                mc.log_event(the_person.title + ": +70 Fertility", "float_text_red")
                mc.log_event(display_name + ": Begins instantly lactating", "float_text_blue")
                if the_person in mc.location.people: #If you're here applying this trait in person it causes her to exclaim.
                    renpy.say(display_name,"Oh my god my tits feel... bigger!")

        def nora_reward_hucow_trait_on_remove(the_person, add_to_log):
            the_person.bc_penalty += -75
            the_person.fertility_percent += -70
            the_person.lactation_sources += -3
            the_person.tits = get_smaller_tits(the_person.tits) #Her tits start to swell.
            the_person.tits = get_smaller_tits(the_person.tits)
            the_person.personal_region_modifiers["breasts"] = the_person.personal_region_modifiers["breasts"] - 0.2 #As her tits get larger they also become softer, unlike large fake tits. (Although even huge fake tits get softer)


label instantiate_serum_traits(): #Creates all of the default LR2 serum trait objects.
    python:

        #####
        # Serum Trait template. Copy and paste this, fill in the fields that are requried and add it to the list_of_traits list to add a serum trait to LR2.
        #####
        #
        # the_serum = SerumTrait(name = "serum name",
        #     desc = "serum description",
        #     positive_slug = "description of the positive effects",
        #     negative_slug = "description of the negative effects",
        #     value_added = a_number,
        #     research_added = a_number,
        #     slots_added = a_number,
        #     production_added = a_number,
        #     duration_added = a_number,
        #     base_side_effect_chance = a_number,
        #     on_apply = a_function,
        #     on_remove = a_function,
        #     on_turn = a_function,
        #     on_day = a_function,
        #     requires = [list_of_other_traits],
        #     tier = a_number,
        #     start_researched = a_bool,
        #     research_needed = a_number,
        #     exclude_tags = [list_of_other_tags],
        #     is_side_effect = a_bool)

        #################
        # Tier 0 Traits #
        #################
        # Tier 0 traits produce almost no effect on the person taking them, or produce an effect with a significant downside. They are available for research from the start of the game.

        #TODO: Basic serum production technique. Adds starting serum slots, traits, etc.
        primitive_serum_prod = SerumTrait(name = "Primitive Serum Production",
            desc = "The fundamental serum creation technique. The special carrier molecule can deliver one other serum trait with pinpoint accuracy.",
            positive_slug = "1 Trait Slot, 3 Turn Duration, $2 Value",
            negative_slug = "+50 Serum Research, 40 Production/Batch",
            value_added = 2,
            research_added = 50,
            slots_added = 1,
            production_added = 40,
            duration_added = 3,
            base_side_effect_chance = 8,
            start_researched = True,
            research_needed = 75,
            exclude_tags = "Production")

        high_capacity_design = SerumTrait(name = "High Capacity Design",
            desc = "Removing the standard stabilizing agents allow an additional serum trait to be added to the design. This change shortens the duration of the serum and is almost certain to introduce unpleasant side effects.",
            positive_slug = "+1 Trait Slot",
            negative_slug = "-1 Turn Duration, -$5 Value, +75 Serum Research",
            value_added = -5,
            research_added = 75,
            slots_added = 2,
            duration_added = -1,
            base_side_effect_chance = 200,
            requires = primitive_serum_prod,
            research_needed = 150)

        basic_med_app = SerumTrait(name = "Basic Medical Application",
            desc = "A spread of minor medical benefits ensures this will always have value for off label treatments. The required research may suggest other effects that can be included in a serum.",
            positive_slug = "+$20 Value",
            negative_slug = "+50 Serum Research",
            value_added = 20,
            research_added = 50,
            base_side_effect_chance = 5,
            research_needed = 200)

        suggestion_drugs_trait = SerumTrait(name = "Suggestion Drugs",
            desc = "Carefully selected mind altering agents amplify the preexisting effects of the serum, making the recipient more vulnurable to behavioural changes.",
            positive_slug = "+$15 Value, +10 Suggestibility",
            negative_slug = "+50 Serum Research.",
            value_added = 15,
            research_added = 50,
            on_apply = suggestion_drugs_on_apply,
            on_remove = suggestion_drugs_on_remove,
            base_side_effect_chance = 10,
            research_needed = 100,
            exclude_tags = "Suggest")

        high_con_drugs = SerumTrait(name = "High Concentration Drugs",
            desc = "By increasing the dose of mind altering agents a larger change to suggestibility can be achieved. The increased dosage has a tendency to leave the recipient depressed.",
            positive_slug = "+$15 Value, +25 Suggestibility",
            negative_slug = "-2 Happiness/Turn, +50 Serum Research.",
            value_added = 15,
            research_added = 50,
            base_side_effect_chance = 15,
            on_apply = high_con_drugs_on_apply,
            on_remove = high_con_drugs_on_remove,
            on_turn = high_con_drugs_on_turn,
            requires = [basic_med_app, suggestion_drugs_trait],
            research_needed = 150,
            exclude_tags = "Suggest")

        sedatives_trait = SerumTrait(name = "Low Concentration Sedatives",
            desc = "A low dose of slow release sedatives makes the recipient more obedient, but have a negative effect on productivity.",
            positive_slug = "+$15 Value, +10 Obedience",
            negative_slug = "-1 To All Stats, +50 Serum Research",
            value_added = 15,
            research_added = 50,
            base_side_effect_chance = 10,
            on_apply = sedatives_trait_on_apply,
            on_remove = sedatives_trait_on_remove,
            requires = basic_med_app,
            research_needed = 100)

        caffeine_trait = SerumTrait(name = "Caffeine Infusion",
            desc = "Adding simple, well understood caffeine to the serum increase the energy levels of the recipient. Unfortunately, the stimulating effect tends to reduce obedience for the duration.",
            positive_slug = "+$15 Value, +20 Max Energy",
            negative_slug = "-15 Obedience, +50 Serum Research",
            value_added = 15,
            research_added = 50,
            base_side_effect_chance = 20,
            on_apply = caffeine_trait_on_apply,
            on_remove = caffeine_trait_on_remove,
            research_needed = 150)

        birth_control_suppression = SerumTrait(name = "Birth Control Suppression",
            desc = "Designed to interfere with the most common forms of oral birth control, reducing their effectiveness.",
            positive_slug = "+$10 Value, -40% BC Effectiveness",
            negative_slug = "+50 Serum Research",
            value_added = 10,
            research_added = 50,
            base_side_effect_chance = 30,
            on_apply = birth_control_suppression_on_apply,
            on_remove = birth_control_suppression_on_apply,
            research_needed = 100)


        #################
        # Tier 1 Traits #
        #################
        # Tier 1 traits produce minor effects, often at the cost of unpleasant mandatory side effects (lower happiness, obedience, stats)

        improved_serum_prod = SerumTrait(name = "Improved Serum Production",
            desc = "General improvements to the basic serum creation formula. Allows for two serum traits to be delivered, but requires slightly more production to produce.",
            positive_slug = "2 Trait Slots, 3 Turn Duration, $2 Value",
            negative_slug = "+50 Serum Research, 70 Production/Batch",
            value_added = 2,
            research_added = 50,
            slots_added = 2,
            production_added = 70,
            duration_added = 3,
            base_side_effect_chance = 25,
            requires = primitive_serum_prod,
            tier = 1,
            research_needed = 200,
            exclude_tags = "Production")

        obedience_enhancer = SerumTrait(name = "Obedience Enhancer",
            desc = "A blend of off the shelf pharmaceuticals will make the recipient more receptive to direct orders.",
            positive_slug = "+$20 Value, +10 Obedience",
            negative_slug = "+75 Serum Research",
            value_added = 20,
            research_added = 75,
            base_side_effect_chance = 15,
            on_apply = obedience_enhancer_on_apply,
            on_remove = obedience_enhancer_on_remove,
            requires = [basic_med_app],
            tier = 1,
            research_needed = 300)

        large_obedience_enhancer = SerumTrait(name = "Experimental Obedience Treatment.",
            desc = "The combination of several only recently released compounds should produce a larger increase in obedience. Unfortunately the effect leaves the recipient rather stuck up and stuffy.",
            positive_slug = "+$20 Value, +20 Obedience",
            negative_slug = "-2 Sluttiness/Turn, +75 Serum Research",
            value_added = 20,
            research_added = 75,
            base_side_effect_chance = 20,
            on_apply = large_obedience_enhancer_on_apply,
            on_remove = large_obedience_enhancer_on_remove,
            on_turn = large_obedience_enhancer_on_turn,
            requires = obedience_enhancer,
            tier = 1,
            research_needed = 350)

        improved_duration_trait = SerumTrait(name = "Improved Reagent Purification",
            desc = "By carefully purifying the starting materials the length of time a serum remains active.",
            positive_slug = "+$20 Value, +2 Turn Duration",
            negative_slug = "+75 Serum Research",
            value_added = 20,
            research_added = 75,
            duration_added = 2,
            base_side_effect_chance = 10,
            requires = basic_med_app,
            tier = 1,
            research_needed = 350)

        aphrodisiac = SerumTrait(name = "Distilled Aprodisac",
            desc = "Careful distilation can concentrate the active ingredient from common aprodisiacs, producing a sudden spike in sluttiness when consumed. The sexual frustration linked to this effect tends to make the recipient less obedient over time as well.",
            positive_slug = "+$20 Value, +15 Sluttiness",
            negative_slug = "-2 Obedience/Turn, +60 Serum Research",
            value_added = 20,
            research_added = 60,
            base_side_effect_chance = 20,
            on_apply = aphrodisiac_on_apply,
            on_remove = aphrodisiac_on_remove,
            on_turn = aphrodisiac_on_turn,
            requires = basic_med_app,
            tier = 1,
            research_needed = 250)

        love_potion = SerumTrait(name = "Love Potion",
            desc = "A carefully balanced combination of chemicals can replicate the brains response to loved ones. Produces an immediate but temporary feeling of love. This trait is particularly prone to introducing side effects.",
            positive_slug = "+$20 Value, +20 Love",
            negative_slug = "+75 Seum Research",
            value_added = 20,
            research_added = 75,
            base_side_effect_chance = 75,
            on_apply = love_potion_on_apply,
            on_remove = love_potion_on_remove,
            requires = [aphrodisiac, basic_med_app],
            tier = 1,
            research_needed = 250)

        off_label_drugs = SerumTrait(name = "Off Label Pharmaceuticals",
            desc = "Several existing drugs can be repurposed to increase the mental pliability of the recipient.",
            positive_slug = "+$20 Value, +30 Suggestibility",
            negative_slug = "+80 Serum Research",
            value_added = 20,
            research_added = 80,
            base_side_effect_chance = 30,
            on_apply = off_label_drugs_on_apply,
            on_remove = off_label_drugs_on_remove,
            requires = suggestion_drugs_trait,
            tier = 1,
            research_needed = 300,
            exclude_tags = "Suggest")

        clinical_testing = SerumTrait(name = "Clinical Testing Procedures",
            desc = "A set of careful tests rather than any single ingredient or process. Serums may be put through formal clinical testing, significantly boosting their value to the general public. This also significantly raises the research cost of each serum design.",
            positive_slug = "+$35 Value",
            negative_slug = "+300 Serum Research",
            value_added = 35,
            research_added = 300,
            base_side_effect_chance = 0,
            requires = [basic_med_app, improved_serum_prod],
            tier = 1,
            research_needed = 400)

        mood_enhancer = SerumTrait(name = "Mood Enhancer",
            desc = "Standard antidepressants provide a general improvement in mood. The most common side effect is a lack of respect for authority figures, brought on by the chemical endorphin rush.",
            positive_slug = "+$20 Value, +5 Happiness/Turn",
            negative_slug = "-2 Obedience/Turn, +75 Serum Research",
            value_added = 20,
            research_added = 75,
            base_side_effect_chance = 15,
            on_turn = mood_enhancer_on_turn,
            requires = basic_med_app,
            tier = 1,
            research_needed = 300)

        refined_caffeine_trait = SerumTrait(name = "Refined Stimulants",
            desc = "A more carefully refined stimulant produces the same boost to baseline energy levels as ordinary caffeine, but with none of the unpleasant side effects.",
            positive_slug = "+$20 Value, +20 Max Energy",
            negative_slug = "+50 Serum Research",
            value_added = 20,
            research_added = 50,
            base_side_effect_chance = 25,
            on_apply = refined_caffeine_trait_on_apply,
            on_remove = refined_caffeine_trait_on_remove,
            requires = [caffeine_trait],
            tier = 1,
            research_needed = 300)

        fertility_enhancement_trait = SerumTrait(name = "Fertility Enhancement",
            desc = "Targets and enhances a womans natural reproductive cycle, increasing the chance that she may become pregnant. If taken birth control will still prevent most pregnancies.",
            positive_slug = "+$20 Value, +20% Fertility",
            negative_slug = "+100 Serum Research",
            value_added = 20,
            research_added = 100,
            base_side_effect_chance = 40,
            on_apply = fertility_enhancement_on_apply,
            on_remove = fertility_enhancement_on_remove,
            requires = [birth_control_suppression, basic_med_app],
            tier = 1,
            research_needed = 250)

        fertility_suppression_trait = SerumTrait(name = "Fertility Suppression",
            desc = "Targets and dampens a womans natural reproductive cycle, decreasing the chance that she may become pregnant.",
            positive_slug = "+$15 Value, -20% Fertility",
            negative_slug = "+100 Serum Research",
            value_added = 15,
            research_added = 100,
            base_side_effect_chance = 40,
            on_apply = fertility_suppression_on_apply,
            on_remove = fertility_suppression_on_remove,
            requires = [birth_control_suppression, basic_med_app],
            tier = 1,
            research_needed = 250)

    #################
        # Tier 2 Traits #
        #################
        # Tier 2 traits can produce moderate effects at a cost or minor effects without side effects.

        advanced_serum_prod = SerumTrait(name = "Advanced Serum Production",
            desc = "Advanced improvements to the basic serum design. Adds four serum trait slots, but requires even more production points.",
            positive_slug = "4 Trait Slots, 3 Turn Duration, $2 Value",
            negative_slug = "+200 Serum Research, 80 Production/Batch",
            value_added = 2,
            research_added = 200,
            slots_added = 4,
            production_added = 80,
            duration_added = 3,
            base_side_effect_chance = 40,
            requires = [improved_serum_prod,basic_med_app],
            tier = 2,
            research_needed = 800,
            exclude_tags = "Production")

        blood_brain_pen = SerumTrait(name = "Blood Brain Penetration",
            desc = "A carefully designed delivery unit can bypass the blood-brain barrier. This will provide a large increase to the Suggestibility of the recipient.",
            positive_slug = "+$25 Value, +50 Suggestibility",
            negative_slug = "+120 Serum Research",
            value_added = 25,
            research_added = 25,
            base_side_effect_chance = 40,
            on_apply = blood_brain_pen_on_apply,
            on_remove = blood_brain_pen_on_remove,
            requires = [off_label_drugs, clinical_testing],
            tier = 2,
            research_needed = 500,
            exclude_tags = "Suggest")

        low_volatility_reagents = SerumTrait(name = "Low Volatility Reagents",
            desc = "Carefully sourced and stored reagents will greatly prolong the effects of a serum.",
            positive_slug = "+$25 Value, +5 Turn Duration",
            negative_slug = "+150 Serum Research",
            value_added = 25,
            research_added = 150,
            duration_added = 5,
            base_side_effect_chance = 15,
            requires = improved_duration_trait,
            tier = 2,
            research_needed = 600)

        breast_enhancement = SerumTrait(name = "Breast Enhancement",
            desc = "Grows breasts overnight. Has a 25% chance of increasing a girls breast size by one step with each time unit.",
            positive_slug = "+$30 Value, 25% Chance/Turn Breast Growth",
            negative_slug = "+125 Serum Research",
            value_added = 30,
            research_added = 125,
            base_side_effect_chance = 20,
            on_turn = breast_enhancement_on_turn,
            requires = basic_med_app,
            tier = 2,
            research_needed = 500)

        breast_reduction = SerumTrait(name = "Breast Reduction",
            desc = "Shrinks breasts overnight. Has a 25% chance of decreasing a girls breast size by one step with each time unit.",
            positive_slug = "+$30 Value, 25% Chance/Turn Breast Reduction",
            negative_slug = "+125 Serum Research",
            value_added = 30,
            research_added = 125,
            base_side_effect_chance = 20,
            on_turn = breast_reduction_on_turn,
            requires = basic_med_app,
            tier = 2,
            research_needed = 500)

        focus_enhancement = SerumTrait(name = "Medical Amphetamines",
            desc = "The inclusion of low doses of amphetamines help the user focus intently for long periods of time.",
            positive_slug = "+$25 Value, +2 Focus",
            negative_slug = "+150 Serum Research",
            value_added = 25,
            research_added = 150,
            base_side_effect_chance = 30,
            on_apply = focus_enhancement_on_apply,
            on_remove = focus_enhancement_on_remove,
            requires = [basic_med_app, clinical_testing],
            tier = 2,
            research_needed = 800)

        int_enhancement = SerumTrait(name = "Quick Release Nootropics",
            desc = "Nootropics enhance cognition and learning. These fast acting nootropics produce results almost instantly, but for a limited period of time.",
            positive_slug = "+$25 Value, +2 Intelligence",
            negative_slug = "+150 Serum Research",
            value_added = 25,
            research_added = 150,
            base_side_effect_chance = 30,
            on_apply = int_enhancement_on_apply,
            on_remove = int_enhancement_on_remove,
            requires = [basic_med_app, clinical_testing],
            tier = 2,
            research_needed = 800)

        cha_enhancement = SerumTrait(name = "Stress Inhibitors",
            desc = "By reducing the users natural stress response to social interactions they are able to express themselves more freely and effectively. Takes effect immediately, but lasts only for a limited time",
            positive_slug = "+$25 Value, +2 Charisma",
            negative_slug = "+150 Serum Research",
            value_added = 25,
            research_added = 150,
            base_side_effect_chance = 30,
            on_apply = cha_enhancement_on_apply,
            on_remove = cha_enhancement_on_remove,
            requires = [basic_med_app, clinical_testing],
            tier = 2,
            research_needed = 800)

        happiness_tick = SerumTrait(name = "Slow Release Dopamine",
                desc = "By slowly flooding the users dopamine receptors they can be put into a long lasting sense of optimism",
                positive_slug = "+$25 Value, +3 Happiness/Turn",
                negative_slug = "+100 Serum Research",
                value_added = 25,
                research_added = 100,
                base_side_effect_chance = 20,
                on_turn = happiness_tick_on_turn,
                requires = [basic_med_app, clinical_testing],
                tier = 2,
                research_needed = 800)

        slutty_caffeine_trait = SerumTrait(name = "Libido Stimulants",
            desc = "Careful engineering allows for the traditional side effects of stimulants to be redirected to the parasympathetic nervous system, causing an immediate spike in arousal as well as general energy levels.",
            positive_slug = " +$25 Value, +20 Max Energy, +15 Sluttiness",
            negative_slug = "+150 Serum Research",
            value_added = 25,
            research_added = 150,
            base_side_effect_chance = 60,
            on_apply = slutty_caffeine_trait_on_apply,
            on_remove = slutty_caffeine_trait_on_remove,
            requires = [refined_caffeine_trait, aphrodisiac],
            tier = 2,
            research_needed = 800)

        pregnancy_accelerator_trait = SerumTrait(name = "Pregnancy Acceleration Hormones",
            desc = "Encourages and supports the ongoing development of a fetus, increasing the effective speed at which a pregnancy develops.",
            positive_slug = "+$25 Value, +1 Pregnancy Progress per Day",
            negative_slug = "+250 Serum Research",
            value_added = 25,
            research_added = 250,
            base_side_effect_chance = 60,
            on_day = pregnancy_accelerator_on_day,
            requires = [fertility_enhancement_trait],
            tier = 2,
            research_needed = 800)

        pregnancy_decelerator_trait = SerumTrait(name = "Pregnancy Deceleration Hormones",
            desc = "Slows the ongoing development of a fetus, increasing the total amount of time needed to bring a pregnancy to term. If properly applied a pregnancy could be maintained indefinitely.",
            positive_slug = "+$20 Value, -1 Pregnancy Progress per Day",
            negative_slug = "+250 Serum Research",
            value_added = 20,
            research_added = 250,
            base_side_effect_chance = 60,
            on_day = pregnancy_decellerator_on_day,
            requires = [fertility_enhancement_trait],
            tier = 2,
            research_needed = 800)

        lactation_hormones = SerumTrait(name = "Lacation Promotion Hormones",
            desc = "Contains massive quantities of hormones normally found naturally in the body during late stage pregnancy. Triggers immediate breast lactation",
            positive_slug = "+$25 Value, Encourages Lactation",
            negative_slug = "+150 Serum Research",
            value_added = 25,
            research_added = 150,
            base_side_effect_chance = 20,
            on_apply = lactation_hormones_on_apply,
            on_remove = lactation_hormones_on_remove,
            requires = [fertility_enhancement_trait, breast_enhancement],
            tier = 2,
            research_needed = 600)

    #################
        # Tier 3 Traits #
        #################
        # Tier 3 traits produce large effects at a cost or moderate ones for free.

        futuristic_serum_prod = SerumTrait(name = "Futuristic Serum Production",
            desc = "Space age technology makes the serum incredibly versitle. Adds seven serum trait slots at an increased production cost.",
            positive_slug = "7 Trait Slots, 3 Turn Duration, $2 Value",
            negative_slug = "+500 Serum Research, 135 Production/Batch",
            value_added = 2,
            research_added = 500,
            slots_added = 7,
            production_added = 135,
            duration_added = 3,
            base_side_effect_chance = 60,
            requires = advanced_serum_prod,
            tier = 3,
            research_needed = 3000,
            exclude_tags = "Production")

        mind_control_agent = SerumTrait(name = "Mind Control Agent",
            desc = "This low grade mind control agent will massively increase the suggestibility of the recipient, resulting in rapid changes in personality based on external stimuli.",
            positive_slug = "+$40 Value, +70 Suggestibility",
            negative_slug = "+200 Serum Research",
            value_added = 40,
            research_added = 200,
            base_side_effect_chance = 50,
            on_apply = mind_control_agent_on_apply,
            on_remove = mind_control_agent_on_remove,
            requires = blood_brain_pen,
            tier = 3,
            research_needed = 1500,
            exclude_tags = "Suggest")

        permanent_bimbo = SerumTrait(name = "Permanent Bimbofication",
            desc = "This delicate chemical cocktail was reverse engineered from an experimental serum sampled in the lab and will turn the recipient into a complete bimbo. Intelligence and obedience will suffer, but she will be happy and slutty. This change is permanent. It does not end when the serum expires and cannot be reversed with other serums.",
            positive_slug = "New Personality: Bimbo, +$40 Value, +10 Permanent Sluttiness, +10 Permanent Obedience",
            negative_slug = "+400 Serum Research, Int Lowered to 1 Permanently",
            value_added = 40,
            research_added = 400,
            base_side_effect_chance = 80,
            on_apply = permanent_bimbo_on_apply,
            #on_remove = a_function, #TODO: Add a way for serums to hold parameters about the person they are used on. Use those to restore personality when forcibly removed.
            requires = mind_control_agent,
            tier = 3,
            research_needed = 2000)

        #TODO: Maybe this should also cost energy to fit thematically
        massive_pregnancy_accelerator = SerumTrait(name = "Extreme Pregnancy Hormones",
            desc = "Overloads the body with natural pregnancy hormones alongside nutrient supplements. Massively increases the pace at which a pregnancy will progress.",
            positive_slug = "+$40 Value, +1 Pregnancy Progress per Turn",
            negative_slug = "+300 Serum Research",
            value_added = 40,
            research_added = 300,
            base_side_effect_chance = 80,
            on_turn = massive_pregnancy_accelerator_on_turn,
            requires = [pregnancy_accelerator_trait],
            tier = 3,
            research_needed = 1400)

    ### SPECIAL TRAITS ###

        ### Nora research traits ###
        nora_suggest_up = SerumTrait(name = "Nora's Research Trait",
            desc = "The manufacturing details for a serum trait developed by Nora. Raises suggestibility significantly, but is guaranteed to generate a side effect and negatively effects value.",
            positive_slug = "+50 Suggestibility",
            negative_slug = "+75 Serum Research, -$150 Value",
            value_added = -150,
            research_added = 75,
            base_side_effect_chance = 1000000,
            on_apply = nora_suggest_up_on_apply,
            on_remove = nora_suggest_up_on_remove,
            tier = 2,
            start_researched = False,
            research_needed = 1000000,
            exclude_tags = "Suggest")

        nora_nightmares = SerumTrait(name = "Nora's Research Trait",
            desc = "The manufacturing details for a serum trait developed by Nora. Negatively affects the recipient's sleep, as well as generating a side effect and negatively effecting value.",
            negative_slug = "+75 Serum Research, -15 Happiness/Night, -$150 Value",
            value_added = -150,
            research_added = 75,
            base_side_effect_chance = 1000000,
            on_day = nora_nightmares_on_day,
            tier = 2,
            start_researched = False,
            research_needed = 1000000)

        nora_obedience_swing = SerumTrait(name = "Nora's Research Trait",
            desc = "The manufacturing details for a serum trait developed by Nora. Causes wild fluctuations in the recipient's willingness to follow orders, as well as generating a side effect and negatively effecting value.",
            negative_slug = "+75 Serum Research, Random Obedience Changes, -$150 Value",
            value_added = -150,
            research_added = 75,
            base_side_effect_chance = 1000000,
            on_turn = nora_obedience_swing_on_turn,
            tier = 2,
            start_researched = False,
            research_needed = 1000000)

        nora_sluttiness_boost = SerumTrait(name = "Nora's Research Trait",
            desc = "The manufacturing details for a serum trait developed by Nora. Causes a sudden spike in the recipients sluttiness, as well as generating a side effect and negatively effecting value.",
            positive_slug = "+20 Sluttiness",
            negative_slug = "+75 Serum Research, -$150 Value",
            value_added = -150,
            research_added = 75,
            base_side_effect_chance = 1000000,
            on_apply = nora_sluttiness_boost_on_apply,
            on_remove = nora_sluttiness_boost_on_remove,
            tier = 2,
            start_researched = False,
            research_needed = 1000000)


        ### Nora boss unlock traits ###

        nora_reward_mother_trait = SerumTrait(name = "Motherly Devotion",
            desc = "A special serum trait developed by Nora after studying your mother. Permanently increases the recipient's Love by 1 per turn for every 10 points that their Sluttiness is higher than Love.",
            positive_slug = "+1 Love per Turn per 10 Sluttiness greater than Love, +$35 Value",
            negative_slug = "+300 Serum Research",
            value_added = 35,
            research_added = 300,
            base_side_effect_chance = 50,
            on_turn = nora_reward_mother_trait_on_turn,
            tier = 2,
            start_researched = False,
            research_needed = 750)

        nora_reward_sister_trait = SerumTrait(name = "Sisterly Obedience",
            desc = "A special serum trait developed by Nora after studying your sister. Permanently increases the recipient's Sluttiness by 1 per day for every 10 points that their Obedience is above 100.",
            positive_slug = "+1 Core Sluttiness/day per 10 Obedience over 100, +$35 Value",
            negative_slug = "+300 Serum Research",
            value_added = 35,
            research_added = 300,
            base_side_effect_chance = 75,
            on_day = nora_reward_sister_trait_on_day,
            tier = 2,
            start_researched = False,
            research_needed = 750)

        nora_reward_cousin_trait = SerumTrait(name = "Cousinly Hate",
            desc = "A special serum trait developed by Nora after studying your cousin. Permanently increases the recipient's Sluttiness by 1 per day for every 5 Love that they are below 0.",
            positive_slug = "+1 Core Sluttiness/day per 5 Love below 0, +$35 Value",
            negative_slug = "+300 Serum Research",
            value_added = 35,
            research_added = 300,
            base_side_effect_chance = 50,
            on_day = nora_reward_cousin_trait_on_day,
            tier = 2,
            start_researched = False,
            research_needed = 750)

        nora_reward_aunt_trait = SerumTrait(name = "Auntly Potential",
            desc = "A special serum trait developed by Nora after studying your aunt. Increases the number of traits a serum design may contain by 2.",
            positive_slug = "+2 Extra Trait Slots",
            negative_slug = "+300 Serum Research",
            value_added = 0,
            research_added = 300,
            slots_added = 3,
            base_side_effect_chance = 100,
            tier = 2,
            start_researched = False,
            research_needed = 750)

        nora_reward_nora_trait = SerumTrait(name = "Meritocratic Attraction",
            desc = "A special serum trait developed by Nora after studying herself. Increases the recipients Obedience and Sluttiness for the duration by 5 for every point of Intelligence you have.",
            positive_slug = "+5 Obedience and Sluttiness per Intelligence, +$35 Value",
            negative_slug = "+300 Serum Research",
            value_added = 35,
            research_added = 300,
            base_side_effect_chance = 50,
            on_apply = nora_reward_nora_trait_on_apply,
            on_remove = nora_reward_nora_trait_on_remove,
            tier = 2,
            start_researched = False,
            research_needed = 750)

        nora_reward_high_love_trait = SerumTrait(name = "Lovers Attraction",
            desc = "A special serum trait developed by Nora after studying someone who adores you. Each turn permanently converts one point of Sluttiness into Love until they are equal.",
            positive_slug = "Converts 1 Sluttiness to Love per turn until equal, +$35 Value",
            negative_slug = "+300 Serum Research",
            value_added = 35,
            research_added = 300,
            base_side_effect_chance = 75,
            on_turn = nora_reward_high_love_trait_on_turn,
            tier = 2,
            start_researched = False,
            research_needed = 750)

        nora_reward_low_love_trait = SerumTrait(name = "Distilled Disgust",
            desc = "A special serum trait developed by Nora after studying someone who absolutely hates you. Gives a massive penalty to love for the duration of the serum.",
            positive_slug = "+$10 Value",
            negative_slug = "-50 Love, +300 Serum Research",
            value_added = 10,
            research_added = 300,
            base_side_effect_chance = 10,
            on_apply = nora_reward_low_love_trait_on_apply,
            on_remove = nora_reward_low_love_trait_on_remove,
            tier = 2,
            start_researched = False,
            research_needed = 750)

        nora_reward_high_obedience_trait = SerumTrait(name = "Pleasurable Obedience",
            desc = "A special serum trait developed by Nora after studying someone who was completely subservient to you. Increases happiness by 1 for every 5 points of Obedience over 100 per turn.",
            positive_slug = "+1 Happiness per 5 Obedience over 100 per turn, +$35 Value",
            negative_slug = "+300 Serum Research",
            value_added = 35,
            research_added = 300,
            base_side_effect_chance = 50,
            on_turn = nora_reward_high_obedience_trait_on_turn,
            tier = 2,
            start_researched = False,
            research_needed = 750)

        nora_reward_high_slut_trait = SerumTrait(name = "Rapid Corruption",
            desc = "A special serum trait developed by Nora after studying someone who was a complete slut. Instantly and permanently converts up to 5 Temporary Sluttiness into Core Sluttiness when applied.",
            positive_slug = "5 Temp to Core Sluttiness, +$35 Value",
            negative_slug = "+300 Serum Research",
            value_added = 35,
            research_added = 300,
            base_side_effect_chance = 50,
            on_apply = nora_reward_high_slut_trait_on_apply,
            tier = 2,
            start_researched = False,
            research_needed = 750)

        nora_reward_genius_trait = SerumTrait(name = "Natural Talent",
            desc = "A special serum trait developed by Nora after studying someone who was a genius. Instantly and permanetly sets the recipients Intelligence, Charisma, and Focus to 5.",
            positive_slug = "Sets Charisma, Intelligence, Focus to 5, +$50 Value",
            negative_slug = "+1000 Serum Research",
            value_added = 50,
            research_added = 1000,
            base_side_effect_chance = 300,
            on_apply = nora_reward_genius_trait_on_apply,
            tier = 2,
            start_researched = False,
            research_needed = 4000)

        nora_reward_hucow_trait = SerumTrait(name = "Human Breeding Hormones",
            desc = "A special serum trait developed by Nora after studying someone who was in the later stages of pregnancy. Massively decreases birth control effectiveness, increases fertility, and triggers breast swelling and lactation.",
            positive_slug = "+$35 Value, +70% Fertility, -75% BC Effectiveness, Increased Breast Size, Massive Lactation",
            negative_slug = "+300 Serum Research",
            value_added = 35,
            research_added = 300,
            base_side_effect_chance = 80,
            on_apply = nora_reward_hucow_trait_on_apply,
            on_remove = nora_reward_hucow_trait_on_remove,
            tier = 2,
            research_needed = 750)

    # Tier 0
        list_of_traits.append(primitive_serum_prod)
        list_of_traits.append(high_capacity_design)
        list_of_traits.append(basic_med_app)
        list_of_traits.append(suggestion_drugs_trait)
        list_of_traits.append(high_con_drugs)
        list_of_traits.append(sedatives_trait)
        list_of_traits.append(caffeine_trait)

    # Tier 1
        list_of_traits.append(improved_serum_prod)
        list_of_traits.append(improved_duration_trait)
        list_of_traits.append(off_label_drugs)
        list_of_traits.append(aphrodisiac)
        list_of_traits.append(love_potion)
        list_of_traits.append(obedience_enhancer)
        list_of_traits.append(large_obedience_enhancer)
        list_of_traits.append(clinical_testing)
        list_of_traits.append(mood_enhancer)
        list_of_traits.append(refined_caffeine_trait)
        list_of_traits.append(birth_control_suppression)
        list_of_traits.append(fertility_enhancement_trait)
        list_of_traits.append(fertility_suppression_trait)


    # Tier 2
        list_of_traits.append(advanced_serum_prod)
        list_of_traits.append(blood_brain_pen)
        list_of_traits.append(breast_enhancement)
        list_of_traits.append(breast_reduction)
        list_of_traits.append(focus_enhancement)
        list_of_traits.append(int_enhancement)
        list_of_traits.append(cha_enhancement)
        list_of_traits.append(low_volatility_reagents)
        list_of_traits.append(happiness_tick)
        list_of_traits.append(slutty_caffeine_trait)
        list_of_traits.append(pregnancy_accelerator_trait)
        list_of_traits.append(pregnancy_decelerator_trait)
        list_of_traits.append(lactation_hormones)

    # Tier 3
        list_of_traits.append(futuristic_serum_prod)
        list_of_traits.append(mind_control_agent)
        list_of_traits.append(permanent_bimbo)
        list_of_traits.append(massive_pregnancy_accelerator)

    # Nora research traits
        list_of_nora_traits.append(nora_suggest_up)
        list_of_nora_traits.append(nora_nightmares)
        list_of_nora_traits.append(nora_obedience_swing)
        list_of_nora_traits.append(nora_sluttiness_boost)

    return
