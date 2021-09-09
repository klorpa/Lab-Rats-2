#Holds all of the info for SerumTraitBlueprints, which generate new unique traits when unlocked (to allow a single trait to do variations of the same action.)
init -1 python:
    def update_hair_colour(the_person):
        the_person.hair_style.colour = the_person.hair_colour[1]
        the_person.pubes_colour = the_person.pubes_colour

    def hair_colour_change_on_turn(goal_colour, the_person, the_serum, add_to_log): #NOTE: This function must be partially filled and assigned when the blueprint is realised.
        change_per_turn = 0.3 #At 1 it changes in a single turn, at 0 it never changes at all. At 0.5 it gets 50% closer each turn.

        #Set their hair...
        current_colour_raw = the_person.hair_colour[1] #NOTE: Hair colour also comes with a discriptor, but we need a way to override/replace that at some point in the future.
        current_colour = Color(rgb=(current_colour_raw[0], current_colour_raw[1], current_colour_raw[2]), alpha = current_colour_raw[3]) #Generate a proper Colour object
        new_colour = current_colour.interpolate(goal_colour, change_per_turn) #Each turn it gets 30% closer to the goal (but never _quite_ gets there).
        the_person.set_hair_colour(new_colour)

    def eye_colour_change_on_turn(goal_colour, the_person, the_serum, add_to_log):
        change_per_turn = 0.3
        current_colour_raw = the_person.eyes[1]
        current_colour = Color(rgb=(current_colour_raw[0], current_colour_raw[1], current_colour_raw[2]), alpha = current_colour_raw[3]) #Generate a proper Colour object
        new_colour = current_colour.interpolate(goal_colour, change_per_turn) #Each turn it gets 30% closer to the goal (but never _quite_ gets there).
        the_person.set_eye_colour(new_colour)

    def breast_milk_serum_production_on_apply(target_design, the_person, the_serum, add_to_log):
        if not the_person.has_role(lactating_serum_role):
            the_person.add_role(lactating_serum_role)
            the_person.event_triggers_dict["serum_in_breasts"] = 0
            
        if the_person.event_triggers_dict.get("lactating_serum_types", False):
            the_person.event_triggers_dict["lactating_serum_types"].append(target_design)
        else:
            the_person.event_triggers_dict["lactating_serum_types"] = [target_design]

    def breast_milk_serum_production_on_remove(target_design, the_person, the_serum, add_to_log):
        the_person.event_triggers_dict["lactating_serum_types"].remove(target_design) #We know this exists because we added it on_apply.
        if not the_person.event_triggers_dict.get("lactating_serum_types"):
            the_person.remove_role(lactating_serum_role) #If there are no serums to lactate recorded we can safely remove the role - needed in case you double dose her with this production serum.
            the_person.event_triggers_dict["serum_in_breasts"] = 0

label name_blueprint_trait(new_trait, effect_label): #This is called first to ensure all new traits are properly given a new name.
    $ renpy.call(effect_label, new_trait)
    if new_trait in mc.business.blueprinted_traits: #If the effect_label has removed the trait from the blueprinted list it means something failed and the design has not actually been made.
        $ new_trait.name = renpy.input("Give this trait a name.", default = new_trait.name)
    return

label basic_hair_dye_unlock_label(new_trait):
    $ goal_colour = None
    $ hair_list = []
    python:
        for base_hair_colour in list_of_hairs:
            hair_colour = generate_hair_colour(base_hair_colour[0]) # Generate a variant hair colour so we don't apply the exact same thing every time.
            hair_descriptor = hair_colour[0]
            hair_colour = Color(rgb=(hair_colour[1][0], hair_colour[1][1], hair_colour[1][2]))
            hair_list.append(("{color=" + hair_colour.hexcode + "}" + hair_descriptor.capitalize()+"{/color}", hair_colour))

    $ renpy.say("","Select target hair colour.", interact = False)
    $ chosen_colour = renpy.display_menu(hair_list, screen = "choice")

    $ new_trait.on_turn = partial(hair_colour_change_on_turn, chosen_colour)
    $ new_trait.desc += "\n{color=" + chosen_colour.hexcode + "}" + " This is the target colour." + "{/color}"
    return

label hair_colour_change_unlock_label(new_trait):
    call screen colour_selector(title = "Pick the target hair colour.")
    $ return_colour = _return
    $ return_colour = Color(rgb = return_colour.rgb) #Set the alpha value to 1.0, we don't want partially transparent hair.
    $ new_trait.on_turn = partial(hair_colour_change_on_turn, return_colour) #Generates a partially filled function


    $ new_trait.desc += "\n{color=" + return_colour.hexcode + "}" + " This is the target colour." + "{/color}"
    return

label eye_colour_change_unlock_label(new_trait):
    call screen colour_selector(title = "Pick the target eye colour.")
    $ return_colour = _return
    $ return_colour = Color(rgb = return_colour.rgb) #Set the alpha value to 1.0, we don't want partially transparent hair.
    $ new_trait.on_turn = partial(eye_colour_change_on_turn, return_colour) #Generates a partially filled function

    $ new_trait.desc += "\n{color=" + return_colour.hexcode + "}" + " This is the target colour." + "{/color}"
    return

label breast_milk_serum_production_unlock_label(new_trait):
    call screen review_designs_screen(show_traits = False, select_instead_of_delete = True)
    $ return_design = _return
    if isinstance(return_design, SerumDesign):

        $ new_trait.on_apply = partial(breast_milk_serum_production_on_apply, return_design)
        $ new_trait.on_remove = partial(breast_milk_serum_production_on_remove, return_design)
        $ new_trait.desc += "\nProduces: " + return_design.name

    else:
        $ mc.add_clarity(new_trait.clarity_cost)
        $ mc.business.remove_trait(new_trait)
        $ mc.business.active_research_design = None
    return

label instantiate_serum_trait_blueprints(): # Called from instantiate_serum_traits.
    python:

        # the_serum = SerumTraitBlueprint(name = "serum name",
        #     unlock_label = "a label",
        #     desc = "serum description",
        #     positive_slug = "description of the positive effects",
        #     negative_slug = "description of the negative effects",
        #     value_added = a_number,
        #     research_added = a_number,
        #     slots_added = a_number,
        #     production_added = a_number,
        #     duration_added = a_number,
        #     base_side_effect_chance = a_number,
        #     clarity_added = a_number,
        #     on_apply = a_function,
        #     on_remove = a_function,
        #     on_turn = a_function,
        #     on_day = a_function,
        #     requires = [list_of_other_traits],
        #     tier = a_number,
        #     start_researched = a_bool,
        #     research_needed = a_number,
        #     exclude_tags = [list_of_other_tags],
        #     is_side_effect = a_bool,
        #     clarity_cost = a_number)

        #################
        # Tier 1 Traits #
        #################
        # Tier 1 traits produce minor effects, often at the cost of unpleasant mandatory side effects (lower happiness, obedience, stats)

        basic_hair_dye_trait = SerumTraitBlueprint(
            unlock_label = "basic_hair_dye_unlock_label",
            name = "Encapsulated Hair Dyes",
            desc = "Precise delivery of commonly available hair dyes recolours the targets hair over the course of hours. Only a limited ranges of hair colours are suitable for this procedure.",
            positive_slug = "+$15 Value, Shifts Hair Colour Towards Selected Preset Colour",
            negative_slug = "+40 Research Needed",
            value_added = 15,
            research_added = 40,
            base_side_effect_chance = 5,
            requires = [hair_lighten_dye, hair_darken_dye],
            tier = 1,
            research_needed = 100,
            exclude_tags = "Dye",
            clarity_cost = 50)

        #################
        # Tier 2 Traits #
        #################
        # Tier 2 traits can produce moderate effects at a cost or minor effects without side effects.

        hair_dye_trait = SerumTraitBlueprint(
            unlock_label = "hair_colour_change_unlock_label",
            name = "Organic Hair Chemicals",
            desc = "Triggers the production of natural hair dyes, which quickly recolour the subject's hair over the course of hours. Application for several days is suggested for perfect colour accuracy. Test on hidden patch first.",
            positive_slug = "+$30 Value, Shifts Hair Colour Towards Set Target Colour",
            negative_slug = "+80 Serum Research",
            value_added = 30,
            research_added = 80,
            base_side_effect_chance = 20,
            requires = [basic_hair_dye_trait],
            tier = 2,
            research_needed = 400,
            exclude_tags = "Dye",
            clarity_cost = 300)

        eye_dye_trait = SerumTraitBlueprint(
            unlock_label = "eye_colour_change_unlock_label",
            name = "Occular Dyes",
            desc = "Modifies the cells of the subject's iris, causing them change to the target colour over the course of hours. This method can achieve eye colours not normally seen.",
            positive_slug = "+$30 Value, Shifts Eye Colour Towards Set Target Colour",
            negative_slug = "+40 Serum Research",
            value_added = 30,
            research_added = 40,
            base_side_effect_chance = 40,
            requires = [basic_hair_dye_trait],
            tier = 2,
            research_needed = 200,
            clarity_cost = 150)

        breast_milk_serum_production = SerumTraitBlueprint(name = "Serum Lactation",
            unlock_label = "breast_milk_serum_production_unlock_label",
            desc = "Temporarily reprograms the mammary glands of the subject, causing them to produce the selected Serum Design along with their natural milk when they lactate. The number of doses that can be collected depends primarily on the subject's breast size and lactation intensity, although other factors are suspected to exist.",
            positive_slug = "0 Slots, 6 Turn Duration, Lactation Produces Serum Milk, $2 Value",
            negative_slug = "+1200 Serum Research, +500 Clarity Cost, 120 Production/Batch",
            value_added = 2,
            research_added = 1200,
            slots_added = 0,
            production_added = 0,
            duration_added = 6,
            base_side_effect_chance = 100,
            clarity_added = 500,
            on_apply = breast_milk_serum_production_on_apply,
            on_remove = breast_milk_serum_production_on_remove,
            # on_turn = a_function, #TODO: Decide if we want some sort of on/turn or on/day effect for this.
            # on_day = a_function,
            requires = [lactation_hormones, advanced_serum_prod],
            tier = 2,
            research_needed = 1000,
            exclude_tags = "Production",
            clarity_cost = 1500)

        # TIER 1 #
        list_of_traits.append(basic_hair_dye_trait)

        # TIER 2 #
        list_of_traits.append(hair_dye_trait)
        list_of_traits.append(eye_dye_trait)
        list_of_traits.append(breast_milk_serum_production)

    return
