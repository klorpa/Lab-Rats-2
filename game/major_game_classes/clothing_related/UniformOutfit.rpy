init -2 python:
    class UniformOutfit(renpy.store.object):
        def __init__(self, the_outfit):
            self.outfit = the_outfit.get_copy()

            self.full_outfit_flag = False #True if this uniform should belong in the overwear set of the appropriate wardrobes
            self.overwear_flag = False
            self.underwear_flag = False

            self.hr_flag = False #True if this uniform should belong to this departments wardrobe.
            self.research_flag = False
            self.production_flag = False
            self.supply_flag = False
            self.marketing_flag = False

        def set_full_outfit_flag(self, state):
            self.full_outfit_flag = state

        def set_overwear_flag(self, state):
            self.overwear_flag = state

        def set_underwear_flag(self, state):
            self.underwear_flag = state



        def set_research_flag(self, state):
            self.research_flag = state

        def set_production_flag(self, state):
            self.production_flag = state

        def set_supply_flag(self, state):
            self.supply_flag = state

        def set_marketing_flag(self, state):
            self.marketing_flag = state

        def set_hr_flag(self, state):
            self.hr_flag = state



        def can_toggle_full_outfit_state(self):
            slut_limit, underwear_limit, limited_to_top = mc.business.get_uniform_limits()
            if self.full_outfit_flag:
                return True # You can always remove uniforms.

            elif limited_to_top:
                return False

            elif self.outfit.slut_requirement > slut_limit:
                return False

            return True

        def can_toggle_overwear_state(self):
            slut_limit, underwear_limit, limited_to_top = mc.business.get_uniform_limits()
            if self.overwear_flag:
                return True

            elif self.outfit.get_overwear_slut_score() > slut_limit:
                return False

            elif not self.outfit.is_suitable_overwear_set():
                return False

            return True

        def can_toggle_underwear_state(self):
            slut_limit, underwear_limit, limited_to_top = mc.business.get_uniform_limits()
            if self.underwear_flag:
                return True

            elif limited_to_top:
                return False

            elif self.outfit.get_underwear_slut_score() > slut_limit:
                return False

            elif not self.outfit.is_suitable_underwear_set():
                return False

            return True
