init -2 python:
    class VrenAnimation(renpy.store.object):
        def __init__(self, name, shader, tex_1_regions, innate_animation_strength = 1.0, innate_animation_speed = 1.0, region_specific_weights = None):
            self.name = name #Plain text name of this animation.
            self.shader = shader #Reference string reference the shader that should be used. Default is vren.bounce
            self.tex_1_regions = tex_1_regions #A list containing strings referencing all of the regions this animation should affect (ie. ["breasts", "butt"])
            #self.other_texture_groups = other_texture_groups #A list of lists, each one containing regions that should be combined to form a texture for a region. TODO: Implement
            self.innate_animation_strength = innate_animation_strength # A foat that should range from 0 to 1, with 0 being no effect and 1 being full effect.
            self.innate_animation_speed = innate_animation_speed
            if region_specific_weights is None:
                self.region_specific_weights = {} # A dict that stores the name of a region, ex. "butt" or "breasts", and a weight for that region (on top of the innate strength)
            else:
                self.region_specific_weights = region_specific_weights

        def get_copy(self):
            return copy.copy(self)


        def get_weight_items(self):
            return_dict = {}
            for region in self.tex_1_regions:
                if region == "breasts":
                    return_dict["breasts"] = breast_region

                elif region == "butt":
                    return_dict["butt"] = butt_region
            return return_dict
            
