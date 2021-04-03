init -2 python:
    class SerumInventory(renpy.store.object): #A bag class that lets businesses and people hold onto different types of serums, and move them around.
        def __init__(self,starting_list):
            self.serums_held = starting_list ##Starting list is a list of tuples, going [SerumDesign,count]. Count should be possitive.

        def get_serum_count(self, serum_design):
            for design in self.serums_held:
                if design[0] == serum_design:
                    return design[1]
            return 0

        def get_any_serum_count(self):
            count = 0
            for design in self.serums_held:
                count += design[1]
            return count

        def change_serum(self, serum_design,change_amount): ##Serum count must be greater than 0. Adds to stockpile of serum_design if it is already there, creates it otherwise.
            found = False
            for design in self.serums_held:
                if design[0] == serum_design and not found:
                    design[1] += int(change_amount)
                    found = True
                    if design[1] <= 0:
                        self.serums_held.remove(design)

            if not found:
                if change_amount > 0:
                    self.serums_held.append([serum_design,int(change_amount)])


        def get_serum_type_list(self): ## returns a list of all the serum types that are in the inventory, without their counts.
            return_values = []
            for design in self.serums_held:
                return_values.append(design[0])
            return return_values
