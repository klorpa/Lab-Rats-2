init -2 python:
    class ProductionLine(renpy.store.object):
        def __init__(self, destination_inventory): #TODO: Consider storing things like efficency, batch size, ect. on a per assembly line basis (maybe define it per serum you're producing?)
            self.destination_inventory = destination_inventory

            self.selected_design = None #What type of serum is this line working towards producing?
            self.production_weight = 0 #How much of the total production points produced are going into this serum?
            self.spare_production_points = 0 #If there aren't enough production points spare to make a batch they are stored here.
            self.autosell = False
            self.autosell_amount = 0 # If autsell is toggled then any doses of serum beyond this number are sold automatically.

        def set_product(self, the_serum, unused_production = 0):
            if self.selected_design != the_serum:
                self.spare_production_points = 0
                self.autosell = False
                self.autosell_amount = 0
                self.selected_design = the_serum

                self.production_weight = unused_production + self.production_weight

        def add_production(self, total_production):
            if not self.selected_design:
                return 0

            effective_production = __builtin__.int(total_production * 0.01 * self.production_weight)
            serum_production_cost = self.selected_design.production_cost
            if serum_production_cost <= 0:
                serum_production_cost = 10 #Defensive programing in case we assign serum trait costs wrong.

            self.spare_production_points += effective_production

            while self.spare_production_points >= serum_production_cost: #In case we produce multiple batches within 1 turn.
                self.spare_production_points += -self.selected_design.production_cost
                self.destination_inventory.change_serum(self.selected_design, mc.business.batch_size)
                mc.business.add_counted_message("Produced " + self.selected_design.name, mc.business.batch_size)

            return effective_production

        def change_line_weight(self, change):
            self.production_weight += change
            if self.production_weight < 0:
                self.production_weight = 0
            elif self.production_weight > 100:
                self.production_weight = 100

        def toggle_line_autosell(self):
            self.autosell = not self.autosell

        def change_line_autosell(self, amount_change):
            self.autosell_amount += amount_change
            if self.autosell_amount < 0:
                self.autosell_amount = 0

        def get_progress_percentage(self):
            return (1.0*self.spare_production_points) / (1.0*self.selected_design.production_cost)
