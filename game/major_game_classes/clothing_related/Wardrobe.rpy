init -2 python:
    class Wardrobe(renpy.store.object): #A bunch of outfits!
        def __init__(self,name,outfits = None, underwear_sets = None, overwear_sets = None): #Outfits is a list of Outfit objects, or empty if the wardrobe starts empty
            self.name = name
            self.outfits = outfits #Outfits is now used to hold full outfits.
            self.underwear_sets = underwear_sets #Limited to layer 1 clothing items.
            self.overwear_sets = overwear_sets #Limited to layer 2 and 3 clothing items.
            if outfits is None:
                self.outfits = []
            if underwear_sets is None:
                self.underwear_sets = []
            if overwear_sets is None:
                self.overwear_sets = []

            for outfit in self.outfits + self.underwear_sets + self.overwear_sets:
                outfit.restore_all_clothing() #Make sure none of them are stored half off.

        def __copy__(self):
            #TODO: see if adding a .copy() here has A) Fixed any potential bugs and B) not had a major performance impact.
            outfit_copy_list = []
            for outfit in self.outfits:
                outfit_copy_list.append(outfit.get_copy())

            under_copy_list = []
            for underwear in self.underwear_sets:
                under_copy_list.append(underwear.get_copy())

            over_copy_list = []
            for overwear in self.overwear_sets:
                over_copy_list.append(overwear.get_copy())


            return Wardrobe(self.name, outfit_copy_list, under_copy_list, over_copy_list)

        def merge_wardrobes(self, other_wardrobe, keep_primary_name = False): #Returns a copy of this wardrobe merged with the other one, with this taking priority for base outfits.
            base_wardrobe = self.__copy__() #This already redefines it's copy method, so we should be fine.
            for outfit in other_wardrobe.outfits:
                base_wardrobe.add_outfit(outfit.get_copy())

            for underwear in other_wardrobe.underwear_sets:
                base_wardrobe.add_underwear_set(underwear.get_copy())

            for overwear in other_wardrobe.overwear_sets:
                base_wardrobe.add_overwear_set(overwear.get_copy())

            if not keep_primary_name:
                base_wardrobe.name = base_wardrobe.name + " + " + other_wardrobe.name
            return base_wardrobe

        def get_random_selection(self, chance_to_pick): #Returns a wardrobe made of a random assortment of clothing from this one.
            base_wardrobe = Wardrobe(self.name)
            for outfit in self.outfits:
                is_picked = renpy.random.randint(0,100)
                if is_picked < chance_to_pick:
                    base_wardrobe.add_outfit(outfit.get_copy())

            for underwear in self.underwear_sets:
                is_picked = renpy.random.randint(0,100)
                if is_picked < chance_to_pick:
                    base_wardrobe.add_underwear_set(underwear.get_copy())

            for overwear in self.overwear_sets:
                is_picked = renpy.random.randint(0,100)
                if is_picked < chance_to_pick:
                    base_wardrobe.add_overwear_set(overwear.get_copy())

            return base_wardrobe

        def add_outfit(self, new_outfit):
            new_outfit.restore_all_clothing() #Ensure none of the outfits have half-off clothing.
            self.outfits.append(new_outfit)

        def add_underwear_set(self, the_outfit):
            the_outfit.restore_all_clothing()
            self.underwear_sets.append(the_outfit)

        def add_overwear_set(self, the_outfit):
            the_outfit.restore_all_clothing()
            self.overwear_sets.append(the_outfit)

        def remove_outfit(self, old_outfit):
            if old_outfit in self.outfits:
                self.outfits.remove(old_outfit)
            elif old_outfit in self.underwear_sets:
                self.underwear_sets.remove(old_outfit)
            elif old_outfit in self.overwear_sets:
                self.overwear_sets.remove(old_outfit)

        def pick_random_outfit(self): #TODO: We might be able to pass a reference instead of a copy here now that apply_outfit always takes a copy.
            return get_random_from_list(self.outfits).get_copy() # Get a copy of _any_ full outfit in this character's wardrobe.

        def get_random_appropriate_underwear(self, sluttiness_limit, sluttiness_min = 0, guarantee_output = False): #Get an underwear outfit that is considered appropriate (based on underwear sluttiness, not full outfit sluttiness)
            valid_underwear = []
            for underwear in self.underwear_sets:
                if underwear.get_underwear_slut_score() <= sluttiness_limit and underwear.get_underwear_slut_score() >= sluttiness_min:
                    valid_underwear.append(underwear)

            if valid_underwear:
                return get_random_from_list(valid_underwear).get_copy()
            else:
                if guarantee_output: # If an output is guaranteed we always return an Outfit object (even if it is empty). Otherwise we return None to indicate failure to find something.
                    if sluttiness_limit < 120: #Sets an effective recusion limit.
                        return self.get_random_appropriate_underwear(sluttiness_limit+5, sluttiness_min-5, guarantee_output)
                    else:
                        return Outfit("Nothing")

                else:
                    return None

        def get_random_appropriate_outfit(self, sluttiness_limit, sluttiness_min = 0, guarantee_output = False): # Get a copy of a full outfit that the character is at or below the sluttiness limit.
            valid_outfits = []
            for outfit in self.outfits:
                if outfit.slut_requirement >= sluttiness_min and outfit.slut_requirement <= sluttiness_limit:
                    valid_outfits.append(outfit)

            the_outfit = get_random_from_list(valid_outfits)
            if the_outfit:
                return the_outfit.get_copy()
            else:
                if guarantee_output:
                    if sluttiness_limit < 120:
                        return self.get_random_appropriate_outfit(sluttiness_limit+5, sluttiness_min-5, guarantee_output)
                    else:
                        return Outfit("Nothing")
                return None

        def build_appropriate_outfit(self, sluttiness_limit, sluttiness_min = 0): # Let's assume characters have a limited number of overwear sets but a larger set of underwear. Get an overwear set, then a decent underwear set.
            valid_overwear = []
            for overwear in self.overwear_sets:
                if overwear.get_overwear_slut_score() >= sluttiness_min and overwear.get_overwear_slut_score() <= sluttiness_limit:
                    valid_overwear.append(overwear)

            if len(valid_overwear) == 0:
                return default_outfit.get_copy() #If we don't have any overwear stuff we should return the default outfit to prevent a crash.

            picked_overwear = get_random_from_list(valid_overwear) #We use a reference here, we will take a full copy of the underwear and build the outfit up based on that.
            remaining_sluttiness_limit = sluttiness_limit - picked_overwear.get_overwear_slut_score()
            remaining_sluttiness_min = sluttiness_min - picked_overwear.get_overwear_slut_score()

            picked_underwear = self.get_random_appropriate_underwear(remaining_sluttiness_limit, remaining_sluttiness_min)

            if picked_underwear is None:
                return default_outfit.get_copy() #If we weren't able to find any underwear we can't make an outfit with our selection. Return the default outfit to make sure we don't crash.

            # Note: I'm not sure hwo this will work with dresses and extensions.
            for upper in picked_overwear.upper_body:
                picked_underwear.upper_body.append(upper.get_copy())

            for lower in picked_overwear.lower_body:
                picked_underwear.lower_body.append(lower.get_copy())

            for feet_wear in picked_overwear.feet:
                picked_underwear.feet.append(feet_wear.get_copy())

            for acc in picked_overwear.accessories:
                picked_underwear.accessories.append(acc.get_copy())

            picked_underwear.update_slut_requirement()
            if picked_underwear.slut_requirement < remaining_sluttiness_min or picked_underwear.slut_requirement > sluttiness_limit: #BUG: we sometimes have no valid outfits and hit our recursion limit.
                return self.build_appropriate_outfit(sluttiness_limit+1, sluttiness_min) #If for some reason our outfit violates our limits retry but with a slightly more slutty tolerance. Better to fail in favour of sluttiness then not have an outfit.

            else:
                picked_underwear.name = picked_underwear.name + " + " + picked_overwear.name #The outfit name is the hybrid of the two sets we made it out of.

            return picked_underwear


        def decide_on_outfit(self, sluttiness_limit, sluttiness_min = 0): #Has a chance to draw from full random sets if they are present or to create a completely new outfit by combinding sets.

            outfit_choice = renpy.random.randint(0,100)
            chance_to_use_full = 50 #For now we will make 50% of outfit choices use full outfits if possible.
            if outfit_choice < chance_to_use_full:
                valid_full_outfits = []
                for full_outfit in self.outfits:
                    if full_outfit.slut_requirement >= sluttiness_min and full_outfit.slut_requirement <= sluttiness_limit:
                        valid_full_outfits.append(full_outfit)

                if valid_full_outfits:
                    return get_random_from_list(valid_full_outfits).get_copy()
                else:
                    return self.build_appropriate_outfit(sluttiness_limit, sluttiness_min)
            else:
                return self.build_appropriate_outfit(sluttiness_limit, sluttiness_min)

        def decide_on_uniform(self, the_person): # Creates a uniform out of the clothing items from this wardrobe. Unlike a picked outfit sluttiness has no factor here. A girls personal underwear sets will be used for constructed uniforms.
            slut_limit, underwear_limit, limited_to_top = mc.business.get_uniform_limits()

            # Get a list of all the pieces of clothing that are valid for us to build our uniform from.
            valid_full_outfits = self.get_valid_outfit_list()
            valid_underwear_sets = self.get_valid_underwear_sets_list()
            valid_overwear_sets = self.get_valid_overwear_sets_list()


            if len(valid_full_outfits) > 0:
                #We have some full body outfits we mgiht use. 50/50 to use that or a constructed outfit.
                outfit_choice = renpy.random.randint(0,100)
                chance_to_use_full = 50 #Like normal outfits a uniform hasa 50/50 chance of being a full outfit or aa assembled outfit if both are possible.

                if outfit_choice < chance_to_use_full and len(valid_underwear_sets +valid_overwear_sets) > 0: #If we roll an assmelbed outfit and we have some parts to make it out of do that.
                    pass

                else: #Otherwise use one of the full outfits.
                    return get_random_from_list(valid_full_outfits).get_copy()

            else:
                if len(valid_underwear_sets + valid_overwear_sets) == 0:
                    #We have nothing else to make a uniform out of. Return None and let the pick uniform function handle that.
                    return None

                else:
                    pass
                    #We have something to make an outfit out of. Go with that.

            #If we get to here we are assembling an outfit out of underwear or overwear.
            uniform_over = get_random_from_list(valid_overwear_sets)
            if uniform_over:
                #We got a top, now get a bottom.
                uniform_under = get_random_from_list(valid_underwear_sets)
                if not uniform_under:
                    #We need to get a bottom from her personal wardrobe. We also want to make sure it's something she would personally wear.
                    slut_limit_remaining = the_person.sluttiness - uniform_over.get_overwear_slut_score()
                    if slut_limit_remaining < 0:
                        slut_limit_remaining = 0 #If the outfit is so slutty we're not comfortable in it we'll try and wear the most conservative underwear we can.

                    possible_unders = []
                    for under in the_person.wardrobe.underwear_sets:
                        if under.get_underwear_slut_score() <= slut_limit_remaining:
                            possible_unders.append(under)

                    uniform_under = get_random_from_list(possible_unders)


            else:
                #There are no tops, so we're going to try and get a bottom and use one of the persons tops.
                uniform_under = get_random_from_list(valid_underwear_sets) # We know we will always get something here, otherwise we would have returned None a while ago.
                slut_limit_remaining = the_person.sluttiness - uniform_under.get_underwear_slut_score()
                if slut_limit_remaining < 0:
                    slut_limit_remaining = 0 #If the outfit is so slutty we're not comfortable in it we'll try and wear the most conservative underwear we can.

                possible_overs = []
                for over in the_person.wardrobe.overwear_sets:
                    if over.get_overwear_slut_score() <= slut_limit_remaining:
                        possible_overs.append(over)

                uniform_over = get_random_from_list(possible_overs)

            #At this point we have our under and over, if at all possible.
            if not uniform_over or not uniform_under:
                return None #Something's gone wrong and we don't have one of our sets. return None and let the uniform gods sort it out.

            assembled_uniform = uniform_under.get_copy()
            assembled_uniform.name = uniform_under.name + " + " + uniform_over.name
            for upper in uniform_over.upper_body:
                assembled_uniform.upper_body.append(upper.get_copy())

            for lower in uniform_over.lower_body:
                assembled_uniform.lower_body.append(lower.get_copy())

            for feet_wear in uniform_over.feet:
                assembled_uniform.feet.append(feet_wear.get_copy())

            for acc in uniform_over.accessories:
                assembled_uniform.accessories.append(acc.get_copy())

            assembled_uniform.update_slut_requirement()
            return assembled_uniform


        def get_count(self):
            return len(self.outfits + self.underwear_sets + self.overwear_sets)

        def get_outfit_list(self):
            return self.outfits

        def get_valid_outfit_list(self):
            return_list = []
            slut_limit, underwear_limit, limited_to_top = mc.business.get_uniform_limits()
            if limited_to_top:
                return return_list
            for full_set in self.get_outfit_list():
                if full_set.slut_requirement <= slut_limit:
                    return_list.append(full_set)
            return return_list

        def get_underwear_sets_list(self):
            return self.underwear_sets

        def get_valid_underwear_sets_list(self): #List of underwear items that may possibly be valid
            return_list = []
            slut_limit, underwear_limit, limited_to_top = mc.business.get_uniform_limits()
            if limited_to_top:
                return return_list #If we're limited to just tops there are _no_ valid underwear sets, by definition
            for underwear_set in self.get_underwear_sets_list():
                if underwear_set.get_underwear_slut_score() <= underwear_limit:
                    return_list.append(underwear_set)
            return return_list


        def get_overwear_sets_list(self):
            return self.overwear_sets

        def get_valid_overwear_sets_list(self): #List of overwear items that may possibly be valid.
            return_list = []
            slut_limit, underwear_limit, limited_to_top = mc.business.get_uniform_limits()
            for overwear_set in self.get_overwear_sets_list():
                if overwear_set.get_overwear_slut_score() <= slut_limit:
                    return_list.append(overwear_set)
            return return_list

        def has_outfit_with_name(self, the_name):
            has_name = False
            for checked_outfit in self.outfits + self.underwear_sets + self.overwear_sets:
                if checked_outfit.name == the_name:
                    has_name = True
            return has_name

        def get_outfit_with_name(self, the_name):
            for outfit in self.outfits + self.underwear_sets + self.overwear_sets:
                if outfit.name == the_name:
                    return outfit.get_copy()
            return None
