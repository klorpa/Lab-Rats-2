init -2 python:
    class SerumInventory(renpy.store.object): #A bag class that lets businesses and people hold onto different types of serums, and move them around.
        def __init__(self,starting_list = None):
            if starting_list is None:
                self.serums_held = []
            else:
                self.serums_held = starting_list ##Starting list is a list of tuples, going [SerumDesign,count]. Count should be possitive.

        def get_serum_count(self, serum_design):
            for design in self.serums_held:
                if design[0].is_same_design(serum_design):
                    return design[1]
            return 0

        def get_any_serum_count(self):
            count = 0
            for design in self.serums_held:
                count += design[1]
            return count

        def get_matching_serum_count(self, check_function): #Hand a function to the inventory and get a count of the number of serums that match that requirement.
            count = 0
            for design in self.get_serum_type_list():
                if check_function(design):
                    count += self.get_serum_count(design)
            return count

        def get_max_serum_count(self): #Returns the count of the highest group of serums you have available.
            highest_count = 0
            for design in self.get_serum_type_list():
                if self.get_serum_count(design) > highest_count:
                    highest_count = self.get_serum_count(design)

            return highest_count

        def change_serum(self, serum_design, change_amount): ##Serum count must be greater than 0. Adds to stockpile of serum_design if it is already there, creates it otherwise.
            found = False
            remove_list = []
            for design in self.serums_held:
                if design[0].is_same_design(serum_design) and not found:
                    design[1] += int(change_amount)
                    found = True
                    if design[1] <= 0:
                        remove_list.append(design)

            if remove_list: #Avoid removing items while we traverse the list
                for design in remove_list:
                    self.serums_held.remove(design)

            if not found:
                if change_amount > 0:
                    self.serums_held.append([serum_design,int(change_amount)])


        def get_serum_type_list(self): ## returns a list of all the serum types that are in the inventory, without their counts.
            return_values = []
            for design in self.serums_held:
                return_values.append(design[0])
            return return_values

        def get_highest_serum_count(self):
            return_value = none
            largest_amount = -1
            for design in self.serums_held:
                if self.get_serum_count(design) > largest_amount:
                    return_value = design
                    largest_amount = self.get_serum_count(design)

            return return_value
