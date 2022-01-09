init -2 python:
    class Contract(renpy.store.object):
        def __init__(self, name, description, contract_length, mental_requirement, physical_requirement, sexual_requirement, medical_requirement, flaw_tolerance, attention_tolerance, amount_desired):
            self.name = name #A descirptive name of the contract.
            self.description = description #A sentence or two describing the contract/vendor, ect. "So-and-so is looking for a product to ensure greater obedience within their company.")
            self.contract_length = contract_length
            self.mental_aspect = mental_requirement
            self.physical_aspect = physical_requirement
            self.sexual_aspect = sexual_requirement
            self.medical_aspect = medical_requirement
            self.flaws_aspect = flaw_tolerance
            self.attention = attention_tolerance
            self.amount_desired = amount_desired

            self.contract_started = False

            self.time_elapsed = 0

            self.inventory = SerumInventory()

            self.price_per_aspect = 30 + (20*(renpy.random.random()-0.5))
            self.price_per_dose = round(self.price_per_aspect * (self.mental_aspect + self.physical_aspect + self.sexual_aspect + self.medical_aspect))

        def run_day(self):
            if self.contract_started:
                self.time_elapsed += 1
            if self.time_elapsed > self.contract_length:
                return True
            return False

        def check_serum(self, the_serum):
            effective_attention = the_serum.attention
            if attention_floor_increase_1_policy.is_active():
                effective_attention += -1
            if attention_floor_increase_2_policy.is_active():
                effective_attention += -1

                
            if the_serum.mental_aspect < self.mental_aspect:
                return False
            elif the_serum.physical_aspect < self.physical_aspect:
                return False
            elif the_serum.sexual_aspect < self.sexual_aspect:
                return False
            elif the_serum.medical_aspect < self.medical_aspect:
                return False
            elif the_serum.flaws_aspect > self.flaws_aspect:
                return False
            elif the_serum.attention > self.attention:
                return False
            return True

        def start_contract(self):
            self.contract_started = True

        def get_current_serum_count(self):
            count = 0
            for serum_bag_item in self.inventory.serums_held:
                if self.check_serum(serum_bag_item[0]):
                    count += serum_bag_item[1]

        def can_finish_contract(self):
            if self.inventory.get_matching_serum_count(self.check_serum) >= self.amount_desired:
                return True
            else:
                return False

        def finish_contract(self):
            for serum_type in self.inventory.get_serum_type_list():
                mc.business.sell_serum(serum_type, self.inventory.get_serum_count(serum_type), fixed_price = self.price_per_dose, external_serum_source = True)

            self.inventory = SerumInventory()

        def abandon_contract(self):
            for serum_bag_item in self.inventory.serums_held:
                mc.business.inventory.change_serum(serum_bag_item[0], serum_bag_item[1])

            self.inventory = SerumInventory()
            self.contract_started = False
