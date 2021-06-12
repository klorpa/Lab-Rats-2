init -2 python:
    class Clothing(renpy.store.object):
        supported_positions = ["stand2","stand3","stand4","stand5","walking_away","kissing","doggy","missionary","blowjob","against_wall","back_peek","sitting","kneeling1","standing_doggy","cowgirl"]

        _pattern_sets = {}
        def get_pattern_sets(self):
            if not self.proper_name in self._pattern_sets:
                self._pattern_sets[self.proper_name] =  { "Default": None }
            return self._pattern_sets[self.proper_name]
        def set_pattern_sets(self, value):
            self._pattern_sets[self.proper_name] = value

        pattern_sets = property(get_pattern_sets, set_pattern_sets, None, "Clothing pattern sets")

        _position_sets = {}
        def get_position_sets(self):
            if not self.proper_name in self._position_sets:
                self._position_sets[self.proper_name] = {}
            return self._position_sets[self.proper_name]
        def set_position_sets(self, value):
            self._position_sets[self.proper_name] = value

        position_sets = property(get_position_sets, set_position_sets, None, "Clothing position sets")

        def get_crop_offset_dict(self):
            return master_clothing_offset_dict.get(self.proper_name, {})

        crop_offset_dict = property(get_crop_offset_dict, None, None, "Offset dictionary")

        _half_off_regions = {}
        def get_half_off_regions(self):
            if not self.proper_name in self._half_off_regions:
                self._half_off_regions[self.proper_name] = []
            return self._half_off_regions[self.proper_name]
        def set_half_off_regions(self, value):
            self._half_off_regions[self.proper_name] = value

        half_off_regions = property(get_half_off_regions, set_half_off_regions, None, "Clothing half off regions")

        _half_off_ignore_regions = {}
        def get_half_off_ignore_regions(self):
            if not self.proper_name in self._half_off_ignore_regions:
                self._half_off_ignore_regions[self.proper_name] = []
            return self._half_off_ignore_regions[self.proper_name]
        def set_half_off_ignore_regions(self, value):
            self._half_off_ignore_regions[self.proper_name] = value

        half_off_ignore_regions = property(get_half_off_ignore_regions, set_half_off_ignore_regions, None, "Clothing half off regions")

        _constrain_regions = {}
        def get_constrain_regions(self):
            if not self.proper_name in self._constrain_regions:
                self._constrain_regions[self.proper_name] = []
            return self._constrain_regions[self.proper_name]
        def set_constrain_regions(self, value):
            self._constrain_regions[self.proper_name] = value

        constrain_regions = property(get_constrain_regions, set_constrain_regions, None, "Clothing half off regions")

        #Slots are

        ##Feet##
        #Layer 1: Socks
        #Layer 2: Shoes

        ##Lower Body##
        #Layer 1: Panties
        #Layer 2: Pantyhose
        #Layer 3: Pants/Skirt

        ##Upper Body##
        #Layer 1: Bra
        #Layer 2: Shirt
        #Layer 3: Jacket

        ##Accessories##
        #Layer 1: Skin level
        #Layer 2: Over underwear
        #Layer 3: Over shirts
        #Layer 4: Over everything

        def __init__(self, name, layer, hide_below, anchor_below, proper_name, draws_breasts, underwear, slut_value, has_extension = None, is_extension = False, colour = None, tucked = False, body_dependant = True,
        opacity_adjustment = 1, whiteness_adjustment = 0.0, contrast_adjustment = 1.0, supported_patterns = None, pattern = None, colour_pattern = None, ordering_variable = 0, display_name = None,
        can_be_half_off = False, half_off_regions = None, half_off_ignore_regions = None, half_off_gives_access = None, half_off_reveals = None, constrain_regions = None,
        crop_offset_dict = None):
            self.name = name
            self.proper_name = proper_name #The true name used in the file system
            if display_name is None:
                self.display_name = self.name
            else:
                self.display_name = display_name #The name that shoudl be used any time the item is talked about in a more general sense (ie. "she takes off her panties" instead of "she takes of her cute lace panties")

            self.hide_below = hide_below #If true, it hides the clothing beneath so you can't tell what's on.
            self.anchor_below = anchor_below #If true, you must take this off before you can take off anything of a lower layer.
            self.layer = layer #A list of the slots above that this should take up or otherwise prevent ffrom being filled. Slots are a list of the slot and the layer.

            self.position_sets = {} #A list of position set names. When the clothing is created it will make a dict containing these names and image sets for them.
            self.pattern_sets = {} #A list of patterns for this piece of clothing that are valid. Keys are in the form "position_patternName"
            #self.supported_positions = ["stand2","stand3","stand4","stand5","walking_away","kissing","doggy","missionary","blowjob","against_wall","back_peek","sitting","kneeling1","standing_doggy","cowgirl"]
            self.supported_patterns = supported_patterns
            if not supported_patterns:
                self.supported_patterns = {"Default":None}
            self.supported_patterns["Default"] = None

            for set in self.supported_positions:
                self.position_sets[set] = Clothing_Images(proper_name,set,draws_breasts, body_dependant = body_dependant)
                if supported_patterns and not proper_name is None:
                    for the_pattern in supported_patterns:
                        pattern_name = supported_patterns[the_pattern]
                        if pattern_name:
                            self.pattern_sets[set + "_" + pattern_name] = Clothing_Images(proper_name+"_"+pattern_name, set, draws_breasts, body_dependant = body_dependant)


            # self.crop_offset_dict = master_clothing_offset_dict.get(self.proper_name, {}) # All of the offsets are stored in a single array and distributed. Saves time having to manually change values any time a clothing item render is updated.

            self.draws_breasts = draws_breasts
            self.underwear = underwear #True if the item of clothing satisfies the desire for underwear for upper or lower (bra or panties), false if it can pass as outerwear. Underwear on outside of outfit gives higher slut requirement.
            self.slut_value = slut_value #The amount of sluttiness that this piece of clothing adds to an outfit.
            self.has_extension = has_extension #If the item of clothing spans two zones (say, lower and feet or upper and lower body) has_extension points towards the placeholder item that fills the other part.
            self.is_extension = is_extension #If this is true the clothing item exists only as a placeholder. It will draw nothing and not be removed unless the main piece is removed.
            if not colour:
                self.colour = [1,1,1,1]
            else:
                self.colour = colour
            self.tucked = tucked #Items of clothign that are tucked are drawn a "half level", aka we cycle thorugh all layer 2's and do untucked items, then do all tucked items.

            self.body_dependant = body_dependant #Items that are not body dependant are always draw as if they are on a standard body, ideal for facial accessories that do not vary with emotion like earings.

            self.whiteness_adjustment = whiteness_adjustment #A modifier applied to the greyscale version of a piece of clothing to bring it closer to a white piece of clothing instead of grey. Default is 0, ranges from -1 to 1.
            self.contrast_adjustment = contrast_adjustment #Changes the contrast, good for getting proper whites and blacks after changing whiteness. Default is 1.0, 0.0 is min contrast, >1 is increasing contrast
            self.opacity_adjustment = opacity_adjustment #An opacity modifier applied to the piece of clothing before any other modifiers are considered (including colour). A value >1 makes slightly transparent clothing opaque, perfect for fixing imperfect renders.

            self.pattern = pattern #If not none this should be a string that will let us find the proper pattern mask.
            if not colour_pattern:
                self.colour_pattern = [1,1,1,1]
            else:
                self.colour_pattern = colour_pattern #If there is a pattern assigned this is the colour used for the masked section.

            self.ordering_variable = ordering_variable #Used for things like hair and pubes when we need to know what can be trimmed into what without any time taken.
            #TODO: Assign ordering variables to all hair based on length (short, medium, long) and then have haircuts and stuff be possible.

            self.half_off = False
            self.can_be_half_off = can_be_half_off
            self.half_off_gives_access = False
            if half_off_gives_access: #If True the piece of clothing does not block accessability for tits or vagina
                self.half_off_gives_access = half_off_gives_access

            self.half_off_reveals = False
            if half_off_reveals: #If True a piece of clothing does not block visability for anything underneath it when half off.
                self.half_off_reveals = half_off_reveals

            if half_off_regions is None: #A list of body region "clothing items". When self.half_off is True these regions are hidden.
                self.half_off_regions = []
            elif isinstance(half_off_regions, list):
                self.half_off_regions = half_off_regions
            else:
                self.half_off_regions = [half_off_regions]

            if half_off_ignore_regions is None: #A list of region "clothing items" that are added _back_ onto an item when half off. These use no blur, so can preserve sharp edges where, for example, arms interact with a torso.
                self.half_off_ignore_regions = []
            elif isinstance(half_off_ignore_regions, list):
                self.half_off_ignore_regions = half_off_ignore_regions
            else:
                self.half_off_ignore_regions = [half_off_ignore_regions]

            if constrain_regions is None: #an area of the body that other clothing items are "constrained" to if this item is worn over top.
                self.constrain_regions = []
            elif isinstance(constrain_regions, list):
                self.constrain_regions = constrain_regions
            else:
                self.constrain_regions = [constrain_regions]

        def __cmp__(self,other): #Checks that two pieces of clothing are _exactly_ the same, down to colour and pattern (but not check by reference)
            if type(self) is type(other):
                if (self.name == other.name
                    and self.hide_below == other.hide_below
                    and self.layer == other.layer
                    and self.is_extension == other.is_extension
                    and self.colour == other.colour
                    and hasattr(self, "pattern") and hasattr(other, "pattern") and self.pattern == other.pattern
                    and hasattr(self, "colour_pattern") and hasattr(other, "colour_pattern") and self.colour_pattern == other.colour_pattern):

                    return 0

            if self.__hash__() < other.__hash__():
                return -1
            else:
                return 1

        def is_similar(self, other): #Checks that two pieces of clothing are similar. ie. their base clothing item is the same, even if pattern or colour differs.
            if type(self) is type(other):
                if (self.name == other.name
                    and self.hide_below == other.hide_below
                    and self.layer == other.layer
                    and self.is_extension == other.is_extension):

                    return True
            return False

        def __hash__(self):
            return hash((self.name,self.hide_below,self.anchor_below,self.layer,self.draws_breasts,self.underwear,self.slut_value))

        def get_copy(self): #Returns a copy of the piece of clothing with the correct underlying references.
            return_copy = copy.copy(self)
            if self.has_extension:
                return_copy.has_extension = self.has_extension.get_copy() # Extensions need to be coppied a layer down, since they can store extra information.
            return return_copy

        def get_layer(self,body_type,tit_size):
            return self.layer

        def generate_stat_slug(self): #Generates a string of text/tokens representing what layer this clothing item is/covers
            cloth_info = ""
            if self.layer == 3:
                cloth_info += "{image=gui/extra_images/overwear_token.png}"
            if self.layer == 2:
                cloth_info += "{image=gui/extra_images/clothing_token.png}"
            if self.layer == 1:
                cloth_info += "{image=gui/extra_images/underwear_token.png}"

            if self.has_extension: #Display a second token if the clothing item is a different part (split coverage into top and bottom?)
                if self.has_extension.layer == 3:
                    cloth_info += "|{image=gui/extra_images/overwear_token.png}"
                if self.has_extension.layer == 2:
                    cloth_info += "|{image=gui/extra_images/clothing_token.png}"
                if self.has_extension.layer == 1:
                    cloth_info += "|{image=gui/extra_images/underwear_token.png}"

            cloth_info += "+" +str(self.slut_value) + "{image=gui/heart/red_heart.png}"
            return cloth_info

        def generate_item_image_name(self, body_type, tit_size, position):
            if not self.body_dependant:
                body_type = "standard_body"
            image_set = self.position_sets.get(position)
            if image_set is None:
                image_set = self.position_sets.get("stand3")

            if self.draws_breasts:
                image_name = image_set.get_image_name(body_type, tit_size)
            else:
                image_name = image_set.get_image_name(body_type, "AA")

            return image_name

        def generate_raw_image(self, body_type, tit_size, position): #Returns the raw ZipFileImage or Image, instead of the displayable (used for generating region masks)
            if not self.body_dependant:
                body_type = "standard_body"
            image_set = self.position_sets.get(position)
            if image_set is None:
                image_set = self.position_sets.get("stand3")

            if self.draws_breasts:
                return_image = image_set.get_image(body_type, tit_size)
            else:
                return_image = image_set.get_image(body_type, "AA")

            return return_image

        def get_crop_offset(self, position):
            return self.crop_offset_dict.get(position, (0,0))

        def generate_item_displayable(self, body_type, tit_size, position, lighting = None, regions_constrained = None, nipple_wetness = 0.0):
            if not self.is_extension: #We don't draw extension items, because the image is taken care of in the main object.
                if lighting is None:
                    lighting = [1,1,1]

                if not self.body_dependant:
                    body_type = "standard_body"

                image_set = self.position_sets.get(position) # The image set we are using should corrispond to the set named "positon".
                if image_set is None:
                    image_set = self.position_sets.get("stand3")

                if self.draws_breasts:
                    the_image = image_set.get_image(body_type, tit_size)
                else:
                    the_image = image_set.get_image(body_type, "AA")

                #return the_image

                if regions_constrained is None:
                    regions_constrained = []
                # else:
                #     print("Constrained regions: " + str(regions_constrained))


                converted_mask_image = None
                inverted_mask_image = None
                if self.pattern is not None:
                    pattern_set = self.pattern_sets.get(position+"_"+self.pattern)
                    if pattern_set is None:
                        mask_image = None
                    elif self.draws_breasts:
                        mask_image = pattern_set.get_image(body_type, tit_size)
                    else:
                        mask_image = pattern_set.get_image(body_type, "AA")

                    if mask_image is None:
                        self.pattern = None
                    else:
                        inverted_mask_image = im.MatrixColor(mask_image, [1,0,0,0,0, 0,1,0,0,0, 0,0,1,0,0, 0,0,0,-1,1]) #Generate the masks that will be used to determine what is colour A and B
                        #mask_image = im.MatrixColor(mask_image, [1,0,0,0,0, 0,1,0,0,0, 0,0,1,0,0, 0,0,0,1,0])



                brightness_matrix = im.matrix.brightness(self.whiteness_adjustment)
                contrast_matrix = im.matrix.contrast(self.contrast_adjustment)
                opacity_matrix = im.matrix.opacity(self.opacity_adjustment) #Sets the clothing to the correct colour and opacity.

                #This is the base greyscale image we have
                greyscale_image = im.MatrixColor(the_image, opacity_matrix * brightness_matrix * contrast_matrix) #Set the image, which will crush all modifiers to 1 (so that future modifiers are applied to a flat image correctly with no unusually large images


                colour_matrix = im.matrix.tint(self.colour[0], self.colour[1], self.colour[2]) * im.matrix.tint(*lighting)
                alpha_matrix = im.matrix.opacity(self.colour[3])
                shader_image = im.MatrixColor(greyscale_image, alpha_matrix * colour_matrix) #Now colour the final greyscale image


                if self.pattern is not None:
                    colour_pattern_matrix = im.matrix.tint(self.colour_pattern[0], self.colour_pattern[1], self.colour_pattern[2]) * im.matrix.tint(*lighting)
                    pattern_alpha_matrix = im.matrix.opacity(self.colour_pattern[3] * self.colour[3]) #The opacity of the pattern is relative to the opacity of the entire piece of clothing.
                    shader_pattern_image = im.MatrixColor(greyscale_image, pattern_alpha_matrix * colour_pattern_matrix)

                    mask_red_alpha_invert = im.MatrixColor(mask_image, [0,0,0,1,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,1]) #Inverts the pattern colour so the shader applies properly.

                    final_image = AlphaBlend(mask_image, shader_image, shader_pattern_image, alpha=False)
                else:
                    final_image = shader_image

                final_image = Composite(position_size_dict[position], self.crop_offset_dict.get(position,(0,0)), final_image) #Transform the clothing image into a composite with the image positioned correctly.
                # Images need to be put into a composite here so we can properly apply masks, which themselves need to be composited to apply correctly.

                if len(regions_constrained) > 0:
                    # We want to support clothing "constraining", or masking, lower images. This is done by region.
                    # Each constraining region effectively subtracts itself + a blurred border around it, and then the body region is added back in so it appears through clothing.

                    composite_list = None
                    for region in regions_constrained:
                        #Begin by building a total mask of all constrained regions
                        region_mask = region.generate_raw_image(body_type, tit_size, position)
                        #region_mask = Image(region.generate_item_image_name(body_type, tit_size, position))

                        if composite_list is None:
                            #x_size, y_size = renpy.render(region_mask, 0,0,0,0).get_size() #Only get the render size once, since all renders are the same size for a pose. Technically this could also be a lookup table if it was significantly impacting performacne
                            composite_list = [position_size_dict.get(position)]
                        # composite_list.append((0,0))
                        composite_list.append(region.crop_offset_dict.get(position,(0,0)))
                        composite_list.append(region_mask)

                    composite = im.Composite(*composite_list)
                    blurred_composite = im.Blur(composite, 8) #Blur the combined region mask to make it wider than the original. This would start to incorrectly include the interior of the mask, but...
                    constrained_region_mask = im.MatrixColor(blurred_composite, [1,0,0,0,0, 0,1,0,0,0, 0,0,1,0,0, 0,0,0,8,0]) #This is the area to be subracted from the image.
                    full_body_mask = all_regions.generate_raw_image(body_type, tit_size, position)
                    #full_body_mask = Image(all_regions.generate_item_image_name(body_type, tit_size, position)) #And this is the area to add back in so it is displayed only along the body in some regions
                    composite_list.extend([all_regions.crop_offset_dict.get(position, (0,0)),full_body_mask])
                    #BUG: It only seems to be using the first region constrain.
                    full_body_comp = im.Composite(*composite_list) # This ensures all constrained regions are part of the body mask, enabling support for items like skirts w/ clothing between body parts.
                    constrained_mask = AlphaBlend(constrained_region_mask, Solid("#FFFFFFFF"), full_body_comp) #This builds the proper final image mask (ie all shown, except for the region around but not including the constrained region)
                    final_image = AlphaBlend(constrained_mask, Solid("#00000000"), final_image)

                if nipple_wetness > 0: #TODO: Expand this system to a generic "Wetness" system
                    region_mask = wet_nipple_region.generate_raw_image(body_type, tit_size, position)
                    #region_mask = Image(wet_nipple_region.generate_item_image_name(body_type, tit_size, position))
                    position_size = position_size_dict[position]
                    region_mask = im.MatrixColor(region_mask, [1,0,0,0,0, 0,1,0,0,0, 0,0,1,0,0, 0,0,0,nipple_wetness,0])
                    region_composite = Composite(position_size,(0,0), Solid("00000000", xsize = position_size[0], ysize = position_size[1]), wet_nipple_region.crop_offset_dict.get(position,(0,0)), region_mask)
                    #print(str(position_size))
                    final_image = AlphaBlend(region_composite, final_image, Solid("#00000000"))


                if self.half_off or (self.has_extension and self.has_extension.half_off):
                    #NOTE: This actually produces some really good looking effects for water/stuff. We should add these kinds of effects as a general thing, probably on the pattern level.
                    #NOTE: Particularly for water/stains, this could work really well (and can use skin-tight region marking, ie. not clothing item dependant).

                    composite_list = [position_size_dict.get(position)]

                    total_half_off_regions = [] #Check what all of the half-off regions should be
                    if self.half_off:
                        total_half_off_regions.extend(self.half_off_regions)
                    if (self.has_extension and self.has_extension.half_off):
                        total_half_off_regions.extend(self.has_extension.half_off_regions) #TODO: Duplicates in this cause everything to run slightly slower. Fix that

                    for region_to_hide in total_half_off_regions: #We first add together all of the region masks so we only operate on a single displayable
                        #region_mask = Image(region_to_hide.generate_item_image_name(body_type, tit_size, position))
                        region_mask = region_to_hide.generate_raw_image(body_type, tit_size, position)
                        composite_list.append(region_to_hide.crop_offset_dict.get(position, (0,0)))
                        composite_list.append(region_mask)

                    composite = im.Composite(*composite_list)
                    blurred_composite = im.Blur(composite, 12) #Blur the combined region mask to make it wider than the original. This would start to incorrectly include the interior of the mask, but...
                    transparency_control_image = im.MatrixColor(blurred_composite, [1,0,0,0,0, 0,1,0,0,0, 0,0,1,0,0, 0,0,0,7,0]) #...We increase the contribution of alpha from the mask, so a small amount ends up being 100% (this still preserves some gradient at the edge as well)

                    if self.half_off_ignore_regions: #Sometimes you want hard edges, or a section of a piece of clothing not to be moved. These regions are not blured/enlarged and are subtracted from the mask generated above.
                        add_composite_list = None
                        for region_to_add in self.half_off_ignore_regions:
                            region_mask = region_to_add.generate_raw_image(body_type, tit_size, position)
                            #region_mask = Image(region_to_add.generate_item_image_name(body_type, tit_size, position))
                            if add_composite_list is None:
                                add_composite_list = [position_size_dict.get(position)] #We can reuse the size from our first pass building the mask.
                            #add_composite_list.append((0,0))
                            add_composite_list.append(region_to_add.crop_offset_dict.get(position, (0,0)))
                            add_composite_list.append(region_mask)
                        add_composite = im.Composite(*add_composite_list)
                        transparency_control_image = AlphaBlend(add_composite, transparency_control_image, Solid("#00000000"), True) #This alpha blend effectively subtracts the half_off_ignore mask from the half_off region mask

                    final_image = AlphaBlend(transparency_control_image, final_image, Solid("#00000000"), True) #Use the final mask to hide parts of the clothing image as appopriate.



                return final_image
