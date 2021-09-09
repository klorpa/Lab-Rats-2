init -2 python:
    class SerumDesign(renpy.store.object): #A class that represents a design for a serum built up from serum traits.
        def __init__(self):
            self.name = ""
            self.traits = []
            self.side_effects = []

            self.researched = False
            self.unlocked = False
            self.obsolete = False
            self.current_research = 0

            self.research_needed = 0
            self.clarity_needed = 0
            self.slots = 0
            self.value = 0
            self.production_cost = 0

            self.duration = 0
            self.duration_counter = 0

            self.expires = True #If set to false the serum does not tick up the duration_counter, meaning it will never expire.

            self.effects_dict = {} # A dict that can be used to store information about this serum when appied to people. For example, tracking how much Sluttiness was added so the same amount can be removed at the end of the duration.

        def is_same_design(self, other): #Checks if two serums are the same design (but not necessarily the same _dose_ of that design).
            same = False
            if self.name == other.name:
                same = True #At this point assume this is true unless something else is wrong.
                for trait in self.traits:
                    if trait not in other.traits:
                        same = False
                        break

                for trait in other.traits:
                    if trait not in self.traits:
                        same = False
                        break

                for side_effect in self.side_effects:
                    if side_effect not in other.side_effects:
                        same = False
                        break

                for side_effect in other.side_effects:
                    if side_effect not in self.side_effects:
                        same = False
                        break

            return same


        def reset(self): #Resets the serum to the default serum values.
            self.__init__()

        def has_tag(self, the_tag): #Returns true if at least one of the traits has the tag "the_tag". Used to confirm a production trait is included.
            for trait in self.traits:
                if the_tag in trait.exclude_tags:
                    return True
            return False

        def add_trait(self, the_trait, is_side_effect = False): #Used when the serum is being built in the serum designer.
            if the_trait not in self.traits and the_trait not in self.side_effects:
                if is_side_effect:
                    self.side_effects.append(the_trait)
                else:
                    self.traits.append(the_trait) #Add the trait to the serums list of traits.

                #Add the trait effects on the core develpment stats of the serum.
                self.research_needed += the_trait.research_added
                self.clarity_needed += the_trait.clarity_added
                self.value += the_trait.value_added
                self.slots += the_trait.slots
                self.production_cost += the_trait.production_cost
                self.duration += the_trait.duration

        def remove_trait(self, the_trait): #Used when the serum is being built in the serum designer.
            if the_trait in self.traits or the_trait in self.side_effects:
                if the_trait in self.traits:
                    self.traits.remove(the_trait) #Remove the trait from our list of traits.
                else:
                    self.side_effects.remove(the_trait)

                #Remove the trait effects on the core development stats of the serum.
                self.research_needed += -the_trait.research_added
                self.clarity_needed += -the_trait.clarity_added
                self.value += -the_trait.value_added
                self.slots += -the_trait.slots
                self.production_cost += -the_trait.production_cost
                self.duration += -the_trait.duration

        def duration_expired(self): #Returns true if the serum has expired (ie. duration counter equal to or over duration.).
            if self.duration_counter >= self.duration:
                return True #Returns true when it has expired
            else:
                return False #Returns false when there is more time to go

        def run_on_apply(self, the_person):
            self.effects_dict = {} #Ensure this is clear and it isn't a reference to the main dict.
            for trait in self.traits + self.side_effects:
                trait.run_on_apply(the_person, self)

        def run_on_remove(self, the_person):
            for trait in self.traits + self.side_effects:
                trait.run_on_remove(the_person, self)

        def run_on_turn(self, the_person): #Increases the counter, applies serum effect if there is still some duration left
            if self.duration_counter < self.duration:
                for trait in self.traits + self.side_effects:
                    trait.run_on_turn(the_person, self)
            if self.expires:
                self.duration_counter += 1

        def run_on_move(self, the_person):
            for trait in self.traits + self.side_effects:
                trait.run_on_move(the_person, self)

        def run_on_day(self, the_person):
            for trait in self.traits + self.side_effects:
                trait.run_on_day(the_person, self)

        def add_research(self, amount): #Returns true if "amount" research completes the research
            self.current_research += amount
            if self.current_research >= self.research_needed:
                self.researched = True
                return True
            else:
                return False

        def unlock_design(self, pay_clarity = True):
            if pay_clarity:
                mc.spend_clarity(self.clarity_needed)
            self.unlocked = True

        def generate_side_effects(self): #Called when a serum is finished development. Tests all traits against their side effect chance and adds an effect for any that fail.
            for trait in self.traits:
                if trait.test_effective_side_effect_chance():
                    valid_side_effects = []
                    for side_effect_trait in list_of_side_effects:
                        valid_side_effect = True #Check to make sure we don't have conflicting trait tags.
                        for tag in side_effect_trait.exclude_tags:
                            for checking_trait in self.traits + self.side_effects:
                                if tag in checking_trait.exclude_tags:
                                    valid_side_effect = False
                        if valid_side_effect:
                            valid_side_effects.append(side_effect_trait)

                    the_side_effect = get_random_from_list(valid_side_effects)
                    self.add_trait(the_side_effect, is_side_effect = True)
                    mc.log_event(self.name + " developed side effect " + the_side_effect.name + " due to " + trait.name, "float_text_blue")

        def build_positive_slug(self):
            the_slug = ""
            traits_with_slugs = []
            for trait in self.traits + self.side_effects:
                if trait.positive_slug is not None and trait.positive_slug != "":
                    traits_with_slugs.append(trait)

            for trait in traits_with_slugs:
                the_slug += trait.positive_slug
                if trait is not traits_with_slugs[-1]: #If it isn't the last element.
                        the_slug += ", " #This gets us a nice formatted string in the form A, B, C, D.

        def build_negative_slug(self):
            the_slug = ""
            traits_with_slugs = []
            for trait in self.traits + self.side_effects:
                if trait.negative_slug is not None and trait.negative_slug != "":
                    traits_with_slugs.append(trait)

            for trait in traits_with_slugs:
                the_slug += trait.negative_slug
                if trait is not traits_with_slugs[-1]: #If it isn't the last element.
                        the_slug += ", " #This gets us a nice formatted string in the form A, B, C, D.
