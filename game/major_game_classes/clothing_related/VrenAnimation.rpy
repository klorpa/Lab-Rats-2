init -2 python:
    class VrenAnimation(renpy.store.object):
        def __init__(self, name, shader, tex_1_regions, innate_animation_strength = 1.0, region_specific_weights = None):
            self.name = name #Plain text name of this animation.
            self.shader = shader #Reference to the shader being used, ex. shader.PS_WALK_2D
            self.tex_1_regions = tex_1_regions #A list containing strings referencing all of the regions this animation should affect (ie. ["breasts", "butt"])
            #self.other_texture_groups = other_texture_groups #A list of lists, each one containing regions that should be combined to form a texture for a region. TODO: Implement
            self.innate_animation_strength = innate_animation_strength # A foat that should range from 0 to 1, with 0 being no effect and 1 being full effect.
            if region_specific_weights is None:
                self.region_specific_weights = {} # A dict that stores the name of a region, ex. "butt" or "breasts", and a weight for that region (on top of the innate strength)
            else:
                self.region_specific_weights = region_specific_weights

            self.uniforms = {"innate_strength":self.innate_animation_strength}

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

        def update_innate_strength(self, new_strength):
            self.innate_animation_strength = new_strength
            self.uniforms["inntate_strength"] = new_strength
