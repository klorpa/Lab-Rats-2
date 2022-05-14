init -2 python:
    class Outfit(renpy.store.object): #A bunch of clothing added together, without slot conflicts.
        @staticmethod
        def get_visible_list(list):
            temp_list = sorted(list, key=lambda clothing: clothing.layer) #Get a sorted list
            return_list = []
            visible = True #top layer is always visisble
            for cloth in reversed(temp_list): #Starting at the top layer (ie. 3, jackets and such)
                if visible == True: #If it's visible, add it to the list
                    return_list.append(cloth)
                    if cloth.hide_below: #If it hides everything below, do stop it from being visible. Nothing else will be added to the retrn list now.
                        visible = False
            return return_list

        def __init__(self,name):
            self.name = name
            self.upper_body = []
            self.lower_body = []
            self.feet = []
            self.accessories = [] #Extra stuff that doesn't fit anywhere else. Hats, glasses, ect.
            self.slut_requirement = 0 #The slut score requirement for this outfit.
            self.update_slut_requirement()

        def get_copy(self):
            copy_outfit = Outfit(self.name)

            for feet in self.feet:
                copy_outfit.feet.append(feet.get_copy())

            for lower in self.lower_body:
                if not lower.is_extension:
                    copy_outfit.lower_body.append(lower.get_copy())

            for upper in self.upper_body:
                upper_copy = upper.get_copy()
                copy_outfit.upper_body.append(upper_copy)
                if upper.has_extension:
                    copy_outfit.lower_body.append(upper_copy.has_extension)

            for accessory in self.accessories:
                copy_outfit.accessories.append(accessory.get_copy())
            copy_outfit.update_slut_requirement() #Make sure to properly set sluttiness because we haven't used the correct functions to add otherwise.

            return copy_outfit

        def generate_draw_list(self, the_person, position, emotion = "default", special_modifiers = None, lighting = None, hide_layers = None): #Generates a sorted list of displayables that when drawn display the outfit correctly.
            nipple_wetness = 0.0 # Used to simulate a girl lactating through clothing. Ranges from 0 (none) to 1 (Maximum Effect)
            if the_person is None:
                body_type = "standard_body"
                tit_size = "D"
                face_style = "Face_1"


            else:
                body_type = the_person.body_type
                tit_size = the_person.tits
                face_style = the_person.face_style
                if the_person.lactation_sources > 0:
                    nipple_wetness = (0.1*(float(Person.rank_tits(the_person.tits)+the_person.lactation_sources))) * (the_person.arousal*1.0/the_person.max_arousal)
                    if nipple_wetness > 1.0:
                        nipple_wetness = 1.0

            if hide_layers is None:
                hide_layers = []

            all_items = self.generate_clothing_list() #First generate a list of the clothing objects

            currently_constrained_regions = []
            ordered_displayables = []
            for item in reversed(all_items): #To properly constrain items we need to figure out how they look from the outside in, even though we eventually draw from the inside out
                if type(item) is Facial_Accessory:
                    if item.layer not in hide_layers:
                        ordered_displayables.append(item.generate_item_displayable(position, face_style, emotion, special_modifiers, lighting = lighting))
                else:
                    if not item.is_extension:
                        if item.layer not in hide_layers:
                            ordered_displayables.append(item.generate_item_displayable(body_type, tit_size, position, lighting = lighting, regions_constrained = currently_constrained_regions, nipple_wetness = nipple_wetness))
                        for region in item.constrain_regions:
                            if item.half_off and region in item.half_off_regions:
                                pass # If an item is half off the regions that are hidden while half off are also not constrained by the clothing.
                            elif item.has_extension and item.has_extension.half_off and region in item.has_extension.half_off_regions:
                                pass # If the extension for an item (a dress bottom, for example) is half off and hiding something that section is not contrained.
                            else:
                                currently_constrained_regions.append(region)
            return ordered_displayables[::-1] #We iterated over all_items backwards, so our return list needs to be inverted

        def generate_split_draw_list(self, split_on_clothing, the_person, position, emotion = "default", special_modifiers = None, lighting = None): #Mirrors generate draw list but returns only the clothing above and below the given item as two lists with the item in between (in a tuple)
            if the_person is None:
                body_type = "standard_body"
                tit_size = "D"
                face_style = "Face_1"

            else:
                body_type = the_person.body_type
                tit_size = the_person.tits
                face_style = the_person.face_style

            on_bottom = True #Checks to see if we are adding things to the top or bottom list, flips when it sees the split_on_clothing item
            bottom_items = [] #Things drawn below the middle item
            middle_item = None #The displayable for the middle item
            top_items = [] #Things drawn on top of the middle item
            all_items = self.generate_clothing_list()


            for item in all_items:
                currently_constrained_regions = []
                if type(item) is Facial_Accessory:
                    item_check = item.generate_item_displayable(position, face_style, emotion, special_modifiers, lighting = lighting)
                else:
                    if not item.is_extension:
                        item_check = item.generate_item_displayable(body_type, tit_size, position, lighting = lighting, regions_constrained = currently_constrained_regions)
                        for region in item.constrain_regions:
                            if item.half_off and region in item.constrain_regions:
                                pass # If an item is half off the regions that are hidden while half off are also not constrained by the clothing.
                            elif item.has_extension and item.has_extension.half_off and region in item.has_extension.half_off_regions:
                                pass # If the extension for an item (a dress bottom, for example) is half off and hiding something that section is not contrained.
                            else:
                                currently_constrained_regions.append(region)

                if not item.is_extension:
                    if item == split_on_clothing:
                        middle_item = item_check
                        on_bottom = False
                    else:
                        if on_bottom:
                            bottom_items.append(item_check)
                        else:
                            top_items.append(item_check)
            return (bottom_items,middle_item,top_items)

        def get_forced_modifier(self): #Returns, if one exists, a forced modifier caused by one of the facial accessories (Currently used to support ball gags)
            forced_special_modifier = None
            for item in self.accessories:
                if isinstance(item, Facial_Accessory) and item.modifier_lock is not None:
                    forced_special_modifier = item.modifier_lock #TODO: Decide what to do if multiple accessories add a forced modifier. Probably limit outfits so only 1 can contribute a modifier
            return forced_special_modifier

        def generate_clothing_list(self): #Returns a properly ordered list of clothing. If used to draw them they would be displayed correctly.
            # I don't believe position is needed for anything here. Actually body_type and tit_size aren't either any more. We'll clean that up at some point.
            items_to_draw = self.accessories + self.feet + self.lower_body + self.upper_body #Throw all of our items in a list.
            items_to_draw.sort(key= lambda clothing: clothing.tucked, reverse = True)
            items_to_draw.sort(key= lambda clothing: clothing.layer) #First, sort by clothing layer.
             #Next, modify things that are tucked into eachother.
            return items_to_draw

        def merge_outfit(self, other_outfit):
            # Takes other_outfit
            for an_item in other_outfit.upper_body:
                self.add_upper(an_item.get_copy())
            for an_item in other_outfit.lower_body:
                self.add_lower(an_item.get_copy())
            for an_item in other_outfit.feet:
                self.add_feet(an_item.get_copy())
            for an_item in other_outfit.accessories:
                self.add_accessory(an_item.get_copy())
            self.update_slut_requirement()
            return self

        def can_add_dress(self, new_clothing):
            return self.can_add_upper(new_clothing)

        def add_dress(self, new_clothing, re_colour = None, pattern = None, colour_pattern = None):
            self.add_upper(new_clothing, re_colour = None, pattern = None, colour_pattern = None)

        def can_add_upper(self, new_clothing):
            allowed = True
            for cloth in self.upper_body:
                if cloth.layer == new_clothing.layer:
                    allowed = False

            if new_clothing.has_extension: #It's a dress with a top and a bottom, make sure we can add them both!
                for cloth in self.lower_body:
                    if cloth.layer == new_clothing.has_extension.layer:
                        allowed = False

            return allowed

        def add_upper(self, new_clothing, re_colour = None, pattern = None, colour_pattern = None):
            if re_colour is not None:
                new_clothing.colour = re_colour

            if pattern is not None:
                new_clothing.pattern = pattern
                if colour_pattern is not None:
                    new_clothing.colour_pattern = colour_pattern
                else:
                    new_clothing.colour_pattern = new_clothing.colour

            if self.can_add_upper(new_clothing): ##Always check to make sure the clothing is valid before you add it.
                self.upper_body.append(new_clothing)
                if new_clothing.has_extension:
                    self.lower_body.append(new_clothing.has_extension)
                self.update_slut_requirement()

        def can_add_lower(self,new_clothing):
            allowed = True
            for cloth in self.lower_body:
                if cloth.layer == new_clothing.layer:
                    allowed = False
            return allowed

        def add_lower(self, new_clothing, re_colour = None, pattern = None, colour_pattern = None):
            if re_colour is not None:
                new_clothing.colour = re_colour
            if pattern is not None:
                new_clothing.pattern = pattern
                if colour_pattern is not None:
                    new_clothing.colour_pattern = colour_pattern
                else:
                    new_clothing.colour_pattern = new_clothing.colour

            if self.can_add_lower(new_clothing):
                self.lower_body.append(new_clothing)
                self.update_slut_requirement()

        def can_add_feet(self, new_clothing):
            allowed = True
            for cloth in self.feet:
                if cloth.layer == new_clothing.layer:
                    allowed = False
            return allowed

        def add_feet(self, new_clothing, re_colour = None, pattern = None, colour_pattern = None):
            if re_colour is not None:
                new_clothing.colour = re_colour

            if pattern is not None:
                new_clothing.pattern = pattern
                if colour_pattern is not None:
                    new_clothing.colour_pattern = colour_pattern
                else:
                    new_clothing.colour_pattern = new_clothing.colour

            if self.can_add_feet(new_clothing):
                self.feet.append(new_clothing)
                self.update_slut_requirement()

        def can_add_accessory(self, new_clothing):
            allowed = True #For now all we do not filter what accessories we let people apply. All we require is that this exact type of accessory is not already part of the outfit.
            for accessory in self.accessories:
                if accessory.is_similar(new_clothing):
                    allowed = False
            return allowed

        def add_accessory(self,new_clothing, re_colour = None, pattern = None, colour_pattern = None):
            if re_colour is not None:
                new_clothing.colour = re_colour
            if pattern is not None:
                new_clothing.pattern = None
                if colour_pattern is not None:
                    new_clothing.colour_pattern = colour_pattern
                else:
                    new_clothing.colour_pattern = new_clothing.colour

            if self.can_add_accessory(new_clothing):
                self.accessories.append(new_clothing)
                self.update_slut_requirement()

        def has_clothing(self, the_clothing): #Returns True if this outfit includes the given clothing item, false otherwise. Checks for exact parameter match (colour, name, ect), but not reference match.
            for cloth in self.upper_body + self.lower_body + self.feet + self.accessories:
                if cloth == the_clothing:
                    return True
            return False

        def remove_clothing(self, old_clothing):
            #TODO: make sure this works with dresses when you remove the bottom (ie. extension) first.
            if old_clothing.has_extension:
                self.remove_clothing(old_clothing.has_extension)

            if old_clothing in self.upper_body:
                self.upper_body.remove(old_clothing)
            elif old_clothing in self.lower_body:
                self.lower_body.remove(old_clothing)
            elif old_clothing in self.feet:
                self.feet.remove(old_clothing)
            elif old_clothing in self.accessories:
                self.accessories.remove(old_clothing)

            self.update_slut_requirement()

        def half_off_clothing(self, the_clothing):
            the_clothing.half_off = True
            self.update_slut_requirement()

        def remove_clothing_list(self, the_list, half_off_instead = False):
            for item in the_list:
                if half_off_instead:
                    self.half_off_clothing(item)
                else:
                    self.remove_clothing(item)

        def restore_all_clothing(self):
            for cloth in self.upper_body + self.lower_body + self.feet + self.accessories:
                cloth.half_off = False

        def get_upper_ordered(self): #Returns a list of pieces from bottom to top, on the upper body. Other functions do similar things, but to lower and feet.
            return sorted(self.upper_body, key=lambda clothing: clothing.layer)

        def get_lower_ordered(self):
            return sorted(self.lower_body, key=lambda clothing: clothing.layer)

        def get_upper_top_layer(self):
            if self.get_upper_ordered():
                return self.get_upper_ordered()[-1]
            return None

        def get_lower_top_layer(self):
            if self.get_lower_ordered():
                return self.get_lower_ordered()[-1]
            return None

        def get_feet_ordered(self):
            return sorted(self.feet, key=lambda clothing: clothing.layer)

        def get_upper_visible(self):
            return self.get_visible_list(self.upper_body)

        def get_lower_visible(self):
            return self.get_visible_list(self.lower_body)

        def get_feet_visible(self):
            return self.get_visible_list(self.feet)

        def remove_random_any(self, top_layer_first = False, exclude_upper = False, exclude_lower = False, exclude_feet = False, do_not_remove = False):
            #Picks a random upper, lower, or feet object to remove. Is guaranteed to remove something if possible, or return None if nothing on the person is removable (They're probably naked).
            functs_to_try = []
            if not exclude_upper:
                functs_to_try.append(self.remove_random_upper)
            if not exclude_lower:
                functs_to_try.append(self.remove_random_lower)
            if not exclude_feet:
                functs_to_try.append(self.remove_random_feet)
            renpy.random.shuffle(functs_to_try) #Shuffle the functions so they appear in a random order.
            for remover in functs_to_try: #Try removing each of an upper, lower, and feet. If any succeed break there and return what we removed. Otherwise keep trying. If we run out of things to try we could not remove anything.
                success = remover(top_layer_first, do_not_remove)
                if success:
                    return success
            return None

        def remove_random_upper(self, top_layer_first = False, do_not_remove = False):
            #if top_layer_first only the upper most layer is removed, otherwise anything unanchored is a valid target.
            #if do_not_remove is set to True we only use this to find something valid to remove and return that clothing item. this lets us use this function to find thigns to remove with an animation.
            #Returns None if there is nothing to be removed.
            to_remove = None
            if top_layer_first:
                #Just remove the very top layer
                if self.get_upper_unanchored():
                    to_remove = self.get_upper_unanchored()[0]
                    if to_remove.is_extension:
                        return None #Extensions can't be removed directly.
                else:
                    return None
            else:
                to_remove = get_random_from_list(self.get_upper_unanchored())
                if to_remove and to_remove.is_extension:
                    return None

            if to_remove and not do_not_remove:
                self.remove_clothing(to_remove)
            return to_remove

        def remove_random_lower(self, top_layer_first = False, do_not_remove = False):
            to_remove = None
            if top_layer_first:
                #Just remove the very top layer
                if self.get_lower_unanchored():
                    to_remove = self.get_lower_unanchored()[0]
                    if to_remove.is_extension:
                        return None #Extensions can't be removed directly.
                else:
                    return None
            else:
                to_remove = get_random_from_list(self.get_lower_unanchored())
                if to_remove and to_remove.is_extension:
                    return None

            if to_remove and not do_not_remove:
                self.remove_clothing(to_remove)
            return to_remove

        def remove_random_feet(self, top_layer_first = False, do_not_remove = False):
            to_remove = None
            if top_layer_first:
                #Just remove the very top layer
                if self.get_foot_unanchored():
                    to_remove = self.get_foot_unanchored()[0]
                    if to_remove.is_extension:
                        return None #Extensions can't be removed directly.
                else:
                    return None
            else:
                to_remove = get_random_from_list(self.get_foot_unanchored())
                if to_remove and to_remove.is_extension:
                    return None

            if to_remove and not do_not_remove:
                self.remove_clothing(to_remove)
            return to_remove

        def get_unanchored(self, half_off_instead = False): #Returns a list of the pieces of clothing that can be removed.
            #Question: should be be able to remove accessories like this? We would need a way to flag some things like makeup as unremovable.
            # Note: half_off_instead returns a list of clothing items that can be half-offed, which means eitehr they are completely unanchored, or they are anchored but all upper layers are half-off and half-off gives access
            return_list = []
            return_list.extend(self.get_upper_unanchored(half_off_instead))
            return_list.extend(self.get_lower_unanchored(half_off_instead))
            return_list.extend(self.get_foot_unanchored(half_off_instead))

            return return_list

        def is_item_unanchored(self, the_clothing, half_off_instead = False): #Returns true if the clothing item passed is unanchored, ie. could be logically taken off.
            if the_clothing in self.upper_body:
                if the_clothing in self.get_upper_unanchored(half_off_instead):
                    return True
                else:
                    return False

            elif the_clothing in self.lower_body:
                if the_clothing in self.get_lower_unanchored(half_off_instead):
                    return True
                else:
                    return False

            elif the_clothing in self.feet:
                if the_clothing in self.get_foot_unanchored(half_off_instead):
                    return True
                else:
                    return False

            else:
                return True

        def get_upper_unanchored(self, half_off_instead = False):
            return_list = []
            for top in reversed(sorted(self.upper_body, key=lambda clothing: clothing.layer)):
                if top.has_extension is None or self.is_item_unanchored(top.has_extension, half_off_instead): #Clothing items that cover two slots (dresses) are unanchored if both halves are unanchored.
                    if not half_off_instead or (half_off_instead and top.can_be_half_off):
                        return_list.append(top) #Always add the first item because the top is, by definition, unanchored


                if top.anchor_below and not (half_off_instead and top.half_off and top.half_off_gives_access):
                    break #Search the list, starting at the outermost item, until you find something that anchors the stuff below it.
            return return_list

        def get_lower_unanchored(self, half_off_instead = False):
            return_list = []
            for bottom in reversed(sorted(self.lower_body, key=lambda clothing: clothing.layer)):
                if bottom.has_extension is None or self.is_item_unanchored(bottom.has_extension, half_off_instead):
                    if not half_off_instead or (half_off_instead and bottom.can_be_half_off):
                        return_list.append(bottom)

                if bottom.anchor_below and not (half_off_instead and bottom.half_off and bottom.half_off_gives_access):
                    break
            return return_list

        def get_foot_unanchored(self, half_off_instead = False):
            return_list = []
            for foot in reversed(sorted(self.feet, key=lambda clothing: clothing.layer)):
                if foot.has_extension is None or self.is_item_unanchored(foot.has_extension, half_off_instead):
                    if not half_off_instead or (half_off_instead and foot.can_be_half_off):
                        return_list.append(foot)

                if foot.anchor_below and not (half_off_instead and foot.half_off and foot.half_off_gives_access):
                    break
            return return_list


        def vagina_available(self): ## Doubles for asshole for anal.
            reachable = True
            for cloth in self.lower_body:
                if cloth.anchor_below and not (cloth.half_off and cloth.half_off_gives_access):
                    reachable = False
            return reachable

        def vagina_visible(self):
            visible = True
            for cloth in self.lower_body:
                if cloth.hide_below and not (cloth.half_off and cloth.half_off_reveals):
                    visible = False
            return visible

        def tits_available(self):
            reachable = True
            for cloth in self.upper_body:
                if cloth.anchor_below and not (cloth.half_off and cloth.half_off_gives_access):
                    reachable = False
            return reachable

        def tits_visible(self):
            visible = True
            for cloth in self.upper_body:
                if cloth.hide_below and not (cloth.half_off and cloth.half_off_reveals):
                    visible = False
            return visible

        def underwear_visible(self):
            if (self.wearing_bra() and not self.bra_covered()) or (self.wearing_panties() and not self.panties_covered()):
                return True
            else:
                return False

        def wearing_bra(self):
            if self.get_upper_ordered():
                if self.get_upper_ordered()[0].underwear:
                    return True
            return False

        def get_bra(self): #returns our bra object if one exists, None otherwise
            if self.get_upper_ordered():
                if self.get_upper_ordered()[0].underwear:
                    return self.get_upper_ordered()[0]
            return None

        def wearing_panties(self):
            if self.get_lower_ordered():
                if self.get_lower_ordered()[0].underwear:
                    return True
            return False

        def get_panties(self):
            if self.get_lower_ordered():
                if self.get_lower_ordered()[0].underwear:
                    return self.get_lower_ordered()[0]
            return None

        def bra_covered(self):
            if self.wearing_bra():
                for cloth in self.get_upper_ordered()[::-1]: #Traverse list from outside in
                    if cloth.underwear:
                        return False
                    elif cloth.hide_below and not (cloth.half_off and cloth.half_off_reveals):
                        return True
                    else:
                        pass # Check the next layer
            else:
                return False

        def panties_covered(self):
            if self.wearing_panties():
                for cloth in self.get_lower_ordered()[::-1]: #Traverse list from outside in
                    if cloth.underwear:
                        return False
                    elif cloth.hide_below and not (cloth.half_off and cloth.half_off_reveals):
                        return True
                    else:
                        pass # Check the next layer
            else:
                return False

        def is_suitable_underwear_set(self): #Returns true if the outfit could qualify as an underwear set ie. Only layer 1 clothing.
            for cloth in self.accessories + self.upper_body + self.lower_body + self.feet:
                if cloth.layer > 1:
                    return False
            return True

        def is_suitable_overwear_set(self): #Returns true if the outfit could qualify as an overwear set ie. contains no layer 1 clothing.
            for cloth in self.accessories + self.upper_body + self.lower_body + self.feet:
                if cloth.layer < 2:
                    return False
            return True

        def get_total_slut_modifiers(self): #Calculates the sluttiness boost purely do to the different pieces of clothing and not what is hidden/revealed.
            new_score = 0
            for cloth in self.accessories + self.upper_body + self.lower_body + self.feet: #Add the extra sluttiness values of any of the pieces of clothign we're wearing.
                new_score += cloth.slut_value
            return new_score

        def get_underwear_slut_score(self): #Calculates the sluttiness of this outfit assuming it's an underwear set. We assume a modest overwear set is used (ie. one that covers visibility).
            new_score = 0
            if self.tits_available():
                new_score += 20

            if self.vagina_available():
                new_score += 20

            new_score += self.get_total_slut_modifiers()

            return new_score

        def get_overwear_slut_score(self): #Calculates the sluttiness of this outfit assuming it's an overwear set. That means we assume a modest underwear set is used (ie. one that denies access).
            new_score = 0
            if self.tits_visible():
                new_score += 20

            if self.vagina_visible():
                new_score += 20

            new_score += self.get_total_slut_modifiers()

            return new_score


        def get_full_outfit_slut_score(self): #Calculates the sluttiness of this outfit assuming it's a full outfit. Full penalties and such apply.
            new_score = 0

            if self.tits_available(): # You can reach your tits easily for a titfuck.
                new_score += 20

            if self.tits_visible(): # Everyone can see your tits clearly.
                new_score += 20
            else:
                if self.wearing_bra(): #We're wearing a bra, is it covered though?
                    if not self.bra_covered(): #You're wearing a bra but no top over it, in between nude and clothed in terms of sluttiness.
                        new_score += 20

                else: #We aren't wearing a bra but it would have helped.
                    new_score += 10

            if self.vagina_available(): # You can reach your tits easily for a titfuck.
                new_score += 20
            if self.vagina_visible(): # Everyone can see your tits clearly.
                new_score += 20
            else:
                if self.wearing_panties():
                    if not self.panties_covered():
                        new_score += 20
                else:
                    new_score += 10

            new_score += self.get_total_slut_modifiers()

            return new_score

        def update_slut_requirement(self): # Recalculates the slut requirement of the outfit. Should be called after each new addition.
            self.slut_requirement = self.get_full_outfit_slut_score()

        def get_slut_requirement(self): #A getter function for slut_requriement to be used for functional programming stuff.
            return self.slut_requirement

        def get_full_strip_list(self, strip_feet = True, strip_accessories = False): #TODO: This should support visible_enough at some point.
            items_to_strip = self.lower_body + self.upper_body
            if strip_feet:
                items_to_strip.extend(self.feet)
            if strip_accessories:
                items_to_strip.extend(self.accessories)
            items_to_strip.sort(key= lambda clothing: clothing.tucked, reverse = True) #Tucked upper body stuff draws after lower body.
            items_to_strip.sort(key= lambda clothing: clothing.layer) #Sort the clothing so it is removed top to bottom based on layer.

            extension_items = []
            for item in items_to_strip:
                if item.is_extension:
                    extension_items.append(item)

            for item in extension_items:
                items_to_strip.remove(item) #Don't try and strip extension directly.
            return items_to_strip[::-1] #Put it in reverse order so when stripped it will be done from outside in.

        def get_underwear_strip_list(self, visible_enough = True, avoid_nudity = False, strip_shoes = False): #Gets a list of things to strip until this outfit would have a girl in her underwear
            #If a girl isn't wearning underwear this ends up being a full strip. If she is wearing only a bra/panties she'll strip until they are visible, and the other slot is naked.
            test_outfit = self.get_copy() #We'll use a copy of the outfit. Slightly less efficent, but makes it easier to ensure we are generating valid strip orders.
            items_to_strip = []

            keep_stripping = not ((self.wearing_bra() and not self.bra_covered()) or self.tits_visible())
            while keep_stripping:
                keep_stripping = False
                item = test_outfit.remove_random_upper(top_layer_first = True, do_not_remove = True)
                if item is not None:
                    if item.underwear:
                        pass
                    else:
                        test_outfit.remove_clothing(item)
                        if avoid_nudity and ((visible_enough and self.tits_visible()) or self.tits_available()):
                            test_outfit.add_upper(item) #Stripping this would result in nudity, which we need to avoid.
                            pass
                        elif visible_enough and (self.wearing_bra() and not self.bra_covered()) or self.tits_visible():
                            items_to_strip.append(item)
                        else:
                            items_to_strip.append(item)
                            keep_stripping = True


            keep_stripping = not ((self.wearing_panties() and not self.panties_covered()) or self.vagina_visible())
            while keep_stripping:
                keep_stripping = False
                item = test_outfit.remove_random_lower(top_layer_first = True, do_not_remove = True)
                if item is not None:
                    if item.underwear:
                        pass
                    else:
                        test_outfit.remove_clothing(item)
                        if avoid_nudity and ((visible_enough and self.vagina_visible()) or self.vagina_available()):
                            test_outfit.add_lower(item) #Stripping this would result in nudity, which we need to avoid.
                            pass
                        elif visible_enough and (self.wearing_panties() and not self.panties_covered()) or self.vagina_visible():
                            items_to_strip.append(item)
                        else:
                            items_to_strip.append(item)
                            keep_stripping = True

            if strip_shoes:
                for item in self.get_feet_ordered():
                    if item.layer == 2:
                        items_to_strip.insert(0, item) #Inserts shoes atthe start of the list, since they're the first thing that should be removed.
            return items_to_strip

        def strip_to_underwear(self, visible_enough = True, avoid_nudity = False, strip_shoes = False): #Used to off screen strip a girl down to her underwear, or completely if she isn't wearing any.
            items_to_strip = self.get_underwear_strip_list(visible_enough, avoid_nudity, strip_shoes)
            for item in items_to_strip:
                self.remove_clothing(item)

        def get_tit_strip_list(self, visible_enough = True): #Generates a list of clothing that, when removed from this outfit, result in tits being visible. Useful for animated clothing removal.
            test_outfit = self.get_copy()
            items_to_strip = []
            if visible_enough:
                while not test_outfit.tits_visible():
                    the_item = test_outfit.remove_random_upper(top_layer_first = True)
                    if not the_item:
                        break
                    else:
                        items_to_strip.append(the_item)
            else:
                while not (test_outfit.tits_visible() and test_outfit.tits_available()):
                    the_item = test_outfit.remove_random_upper(top_layer_first = True)
                    if not the_item:
                        break
                    else:
                        items_to_strip.append(the_item)
            return items_to_strip

        def strip_to_tits(self, visible_enough = True): #Removes all clothing from this item until breasts are visible.
            if visible_enough:
                while not self.tits_visible():
                    the_item = self.remove_random_upper(top_layer_first = True)
                    if not the_item:
                        break
            else:
                while not (self.tits_visible() and self.tits_available()):
                    the_item = self.remove_random_upper(top_layer_first = True)
                    if not the_item:
                        break
            return

        def get_vagina_strip_list(self, visible_enough = False):
            test_outfit = self.get_copy()
            items_to_strip = []

            while not ((test_outfit.vagina_visible() and visible_enough) or (test_outfit.vagina_available() and not visible_enough)):
                the_item = test_outfit.remove_random_lower(top_layer_first = True) #Try and remove lower layer clothing first each loop
                if the_item is None:
                    the_item = test_outfit.remove_random_any(top_layer_first = True, exclude_feet = True) #If that fails to make progress (ie. due to upper body items blocking things) remove upper body stuff until we can make progress again.

                if the_item is None:
                    break
                else:
                    items_to_strip.append(the_item)

            return items_to_strip

        def strip_to_vagina(self, visible_enough = False):
            self.remove_clothing_list(self.get_vagina_strip_list(visible_enough = visible_enough))
            return

        def can_half_off_to_tits(self, visible_enough = True):
            # Returns true if all of the clothing blocking her tits can be moved half-off to gain access, or if you already have access
            if (visible_enough and self.tits_visible()) or (not visible_enough and self.tits_available()) or self.get_half_off_to_tits_list(visible_enough = visible_enough):
                return True
            return False

        def get_half_off_to_tits_list(self, visible_enough = True):
            # If possible returns the list of clothing items, from outer to inner, that must be half-offed to gain view/access to her tits
            # If not possible returns an empty list.
            return_list = []
            possible = True
            anchored = None #Set to true when we hit something that stays anchored even if half-off. If that
            for item in self.get_upper_ordered()[::-1]: #Ordered top to bottom
                if visible_enough:
                    if item.hide_below and not (item.can_be_half_off and item.half_off_reveals): #If a piece of clothing hides what's be below and it's anchored or
                        possible = False
                        break
                    elif item.hide_below:
                        if anchored:
                            if item.can_be_half_off and item.half_off_gives_access:
                                if anchored not in return_list:
                                    return_list.append(anchored)
                                anchord = None #Something would anchor the clothing, but it can be removed easily enough.
                            else:
                                possible = False #Something is in the way and we can't get it off because of something else
                                break
                        if item not in return_list:
                            return_list.append(item) #Half-off the anchoring item, then the thing in the way.

                    if item.anchor_below:
                        anchored = item

                else:
                    if item.anchor_below and not (item.can_be_half_off and item.half_off_gives_access):
                        hidden = True
                        break

                    elif item.anchor_below:
                        if item not in return_list:
                            return_list.append(item)

            if not possible:
                return []

            else:
                return return_list

        def can_half_off_to_vagina(self, visible_enough = True):
            # Returns true if all of the clothing blocking her vagina can be moved half-off to gain access
            if (visible_enough and self.vagina_visible()) or (not visible_enough and self.vagina_available()) or self.get_half_off_to_vagina_list(visible_enough = visible_enough):
                return True
            return False

        def get_half_off_to_vagina_list(self, visible_enough = True):
            # If possible returns the list of clothing items, from outer to inner, that must be half-offed to gain view/access to her vagina
            # If not possible returns an empty list.
            return_list = []
            possible = True
            anchored = None #Set to true when we hit something that stays anchored even if half-off. If that
            for item in self.get_lower_ordered()[::-1]: #Ordered top to bottom
                if visible_enough:
                    if item.hide_below and not (item.can_be_half_off and item.half_off_reveals): #If a piece of clothing hides what's be below and it's anchored or
                        possible = False
                        break
                    elif item.hide_below:
                        if anchored:
                            if item.can_be_half_off and item.half_off_gives_access:
                                if anchored not in return_list:
                                    return_list.append(anchored)
                                anchord = None #Something would anchor the clothing, but it can be removed easily enough.
                            else:
                                possible = False #Something is in the way and we can't get it off because of something else
                                break

                        if item not in return_list:
                            return_list.append(item) #Half-off the anchoring item if we didn't already

                    if item.anchor_below:
                        anchored = item

                else:
                    if item.anchor_below and not (item.can_be_half_off and item.half_off_gives_access):
                        hidden = True
                        break

                    elif item.anchor_below:
                        if item not in return_list:
                            return_list.append(item)

            if not possible:
                return []

            else:
                return return_list

        def cum_covered(self): #Returns True if the person has some cum clothing item as part of their outfit. #TODO: Also have this check layer/visibility, so girls can be creampied but just put panties back on and have nobody notice.
            if self.has_clothing(ass_cum) or self.has_clothing(tits_cum) or self.has_clothing(stomach_cum) or self.has_clothing(face_cum):
                #NOTE: Does not include "internal" cum:  creampie_cum and mouth_cum
                return True

            return False
