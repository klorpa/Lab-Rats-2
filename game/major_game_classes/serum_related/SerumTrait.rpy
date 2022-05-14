init -2 python:
    class SerumTrait(renpy.store.object):
        def __init__(self,name,desc, positive_slug = "", negative_slug = "",
            research_added = 0, slots_added = 0, production_added = 0, duration_added = 0, base_side_effect_chance = 0, clarity_added = 0,
            on_apply = None, on_remove = None, on_turn = None, on_day = None, on_move = None,
            requires = None, tier = 0, start_researched = False, research_needed=50, exclude_tags=None, is_side_effect = False,
            clarity_cost = 50, start_unlocked = False,
            mental_aspect = 0, physical_aspect = 0, sexual_aspect = 0, medical_aspect = 0, flaws_aspect = 0, attention = 0):

            # Display info #
            self.name = name
            self.desc = desc #A fluff text description.
            self.positive_slug = positive_slug #A short numerical list of positive effects
            self.negative_slug = negative_slug #The negative costs


            # Serum trait values #
            self.research_added = research_added
            self.slots = slots_added
            self.production_cost = production_added
            self.duration = duration_added
            self.base_side_effect_chance = base_side_effect_chance #A percentage chance that this trait will introduce a side effect to the finished design.
            self.mastery_level = 1.0 #The amount of experience the MC has with this serum. Divide base side effect chance by mastery level to get effective side effect chance.
            self.clarity_added = clarity_added #Amount of Clarity added to the serum design when it will be made.

            # Serum trait effects #
            self.on_apply = on_apply #The function applied to the person when the serum is first applied.
            self.on_remove = on_remove #The function applied to the person when the serum is removed (it should generally undo the on_apply effects)
            self.on_turn = on_turn #The function applied to the person at the end of a turn under the effect of the serum. Effectively "End" of turn.
            self.on_move = on_move #The function applied to the person on the move phase. Effectively "Start" of turn
            self.on_day = on_day #The function applied to the person at the end of the day.

            # Research details #
            if requires is None: #A list of other traits that must be researched before this.
                self.requires = []
            elif isinstance(requires, list):
                self.requires = requires
            else:
                self.requires = [requires]

            self.tier = tier #The tier of research that the business must have unlocked to research this, in addition to the other prerequisits.
            self.researched = start_researched
            self.research_needed = research_needed
            self.current_research = 0

            self.clarity_cost = clarity_cost #How much clarity has to be spent to unlock this trait before it can be researched.
            self.unlocked = start_unlocked or start_researched #Only unlocked traits can be researched

            if exclude_tags is None:#A list of tags (strings) that this trait cannot be paired with. If a trait has the same excluded tag this cannot be added to a trait.
                self.exclude_tags = []
            elif isinstance(exclude_tags, list):
                self.exclude_tags = exclude_tags
            else:
                self.exclude_tags = [exclude_tags]

            self.is_side_effect = is_side_effect #If true this trait is a side effect and not counted towards serum max traits and such. It also cannot be added to a serum on purpose.

            self.mental_aspect = mental_aspect
            self.physical_aspect = physical_aspect
            self.sexual_aspect = sexual_aspect
            self.medical_aspect = medical_aspect
            self.flaws_aspect = flaws_aspect
            self.attention = attention

        def is_similar(self, other): #Returns True if these two traits are near-identical, even if they aren't the same object (primarily for dynamic traits like breast milk)
            if other is None:
                return False

            same = False
            if self.name == other.name and self.desc == other.desc:
                same = True
                if self.on_apply != other.on_apply:
                    same = False
                elif self.on_remove != other.on_remove:
                    same = False
                elif self.on_turn != other.on_turn:
                    same = False
                elif self.on_move != other.on_move:
                    same = False
                elif self.on_day != other.on_day:
                    same = False
                elif self.tier != other.tier:
                    same = False
                elif self.researched != other.researched:
                    same = False
                elif self.is_side_effect != other.is_side_effect:
                    same = False
                elif self.mental_aspect != other.mental_aspect:
                    same = False
                elif self.physical_aspect != other.physical_aspect:
                    same = False
                elif self.sexual_aspect != other.sexual_aspect:
                    same = False
                elif self.medical_aspect != other.medical_aspect:
                    same = False
                elif self.flaws_aspect != other.flaws_aspect:
                    same = False
                elif self.attention != other.attention:
                    same = False

            return same

        def run_on_apply(self, the_person, the_serum, add_to_log = True):
            if self.on_apply is not None:
                self.on_apply(the_person, the_serum, add_to_log)

        def run_on_remove(self, the_person, the_serum, add_to_log = False):
            if self.on_remove is not None:
                self.on_remove(the_person, the_serum, add_to_log)

        def run_on_turn(self, the_person, the_serum, add_to_log = False):
            if self.on_turn is not None:
                self.on_turn(the_person, the_serum, add_to_log)

        def run_on_move(self, the_person, the_serum, add_to_log = False):
            if self.on_move is not None:
                self.on_move(the_person, the_serum, add_to_log)

        def run_on_day(self, the_person, the_serum, add_to_log = False):
            if self.on_day is not None:
                self.on_day(the_person, the_serum, add_to_log)

        def add_research(self, amount):
            self.current_research += amount
            if self.current_research >= self.research_needed:
                if self.researched:
                    while (self.current_research >= self.research_needed): #For large businesses when the research produced is much larger than the total research needed you can gain multiple levels.
                        self.add_mastery(0.5)
                        self.current_research += -self.research_needed
                else:
                    self.current_research += -self.research_needed
                self.researched = True

                return True
            else:
                return False

        def unlock_trait(self, pay_clarity = True):
            if pay_clarity:
                mc.spend_clarity(self.clarity_cost)
            self.unlocked = True
            return self #Return self so we can unlock and set as selected research as an atomic action in research UI.

        def add_mastery(self, amount):
            self.mastery_level += amount

        def get_effective_side_effect_chance(self): #Generates the effective side effect chance percent as an integer.
            the_chance = self.base_side_effect_chance/self.mastery_level
            return __builtin__.int(the_chance)

        def test_effective_side_effect_chance(self): #Gets the effective side effect chance and tests it against a random 1 to 100 roll
            the_chance = self.get_effective_side_effect_chance()
            the_roll = renpy.random.randint(0,100)
            if the_roll < the_chance:
                return True
            else:
                return False

        def build_negative_slug(self):
            return_slug = self.negative_slug

            if self.research_added > 0:
                if return_slug:
                    return_slug += ", "
                return_slug += "+" + str(self.research_added) + " Serum Research"

            if self.clarity_added > 0:
                if return_slug:
                    return_slug += ", "
                return_slug += "+" + str(self.clarity_added) + " Clarity to Unlock"

            if self.is_side_effect:
                pass #For side effects we do not want to display the side effect chance as a negative modifier.
            else:
                if return_slug:
                    return_slug += ", "
                if self.get_effective_side_effect_chance() >= 10000:
                    return_slug += "Guaranteed Side Effect"
                else:
                    return_slug += str(self.get_effective_side_effect_chance()) + "% Chance of Side Effect (" + str(self.mastery_level) + " Mastery)"

            return return_slug

        def has_required(self):
            has_prereqs = True
            for trait in self.requires:
                if not trait.researched:
                    has_prereqs = False
            if self.tier > mc.business.research_tier:
                has_prereqs = False
            return has_prereqs
