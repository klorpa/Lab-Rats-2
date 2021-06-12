transform basic_bounce(the_animation = idle_wiggle_animation): #TODO: Replicate old shader effects. Test using various parameters instead of individual shaders if possible.
    shader the_animation.shader
    u_animation_strength the_animation.innate_animation_strength #How far the effect displaces the image's pixels.
    u_animation_speed the_animation.innate_animation_speed # The speed at which the animation cycles
    block:
        u_animation_time 0.0 #Start time, fed seperately for smoother value.
        linear 3600.0 u_animation_time 3600.0 #Feeds the animation a smoother animation time.

    # TODO: Check to see if some effects can be achieved by combining different shaders. Ie. breast jiggle seperate from body breathing.
    # |-> Possible, but likely results in less readable shader code even if it's shorter.

init -1 python:
    # vren.topbounce moves moves the entire character image, scaled so the top moves while the absolute bottom is stationary.
    # Also includes boob/ass bounce.
    renpy.register_shader("vren.topbounce",
        variables = """
        uniform sampler2D tex0;
        uniform sampler2D tex1;
        uniform float u_animation_time;
        uniform float u_animation_strength;
        uniform float u_animation_speed;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
        """,
        vertex_320 = """
        v_tex_coord = a_tex_coord;""",
        fragment_320 = """
        float time_scale_factor = 1.0 * u_animation_speed;
        float effect_scale_factor = 0.02 * u_animation_strength;

        float time_effect = (sin(u_animation_time * time_scale_factor)+1.0)/2.0;

        float x_percent = v_tex_coord.x - 0.5;
        float y_percent = 1.0 - v_tex_coord.y;

        float xShift = x_percent * effect_scale_factor * y_percent;
        float yShift = log((y_percent * effect_scale_factor * 1.0)+1.0)/2.3;
        xShift = xShift * time_effect;
        yShift = yShift * time_effect;
        vec2 bounce_shift = vec2(xShift, yShift);

        float influence = effect_scale_factor * texture2D(tex1, v_tex_coord.xy).g;
        vec2 boob_Shift;
        if (influence > 0.0) {
            float time_effect = (sin((u_animation_time-0.2) * time_scale_factor)+1.0)/2.0;
            float boob_xShift = 0.0;
            float boob_yShift = time_effect * influence;
            boob_Shift = vec2(boob_xShift, boob_yShift);
        }
        else {
            boob_Shift = vec2(0, 0);
        }

        gl_FragColor = texture2D(tex0, v_tex_coord + bounce_shift +  boob_Shift);
        """)

    # vren.middlebounce moves the entire character, centered on the middle of the image while keeping the top and bottom stationary.
    # Also jiggles boob/ass bounce.
    renpy.register_shader("vren.middlebounce",
        variables = """
        uniform sampler2D tex0;
        uniform sampler2D tex1;
        uniform float u_animation_time;
        uniform float u_animation_strength;
        uniform float u_animation_speed;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
        """,
        vertex_320 = """
        v_tex_coord = a_tex_coord;""",
        fragment_320 = """
        float time_scale_factor = 1.0 * u_animation_speed;
        float effect_scale_factor = 0.02 * u_animation_strength;

        float time_effect = (sin(u_animation_time * time_scale_factor)+1.0)/2.0;

        float x_percent = v_tex_coord.x - 0.5;
        float y_percent = 0.5 - abs(v_tex_coord.y-0.5);

        float xShift = x_percent * effect_scale_factor * y_percent;
        float yShift = log((y_percent * effect_scale_factor * 1.0)+1.0)/2.3;
        xShift = xShift * time_effect;
        yShift = yShift * time_effect;
        vec2 bounce_shift = vec2(xShift, yShift);

        float influence = effect_scale_factor * texture2D(tex1, v_tex_coord.xy).g;
        vec2 boob_Shift;
        if (influence > 0.0) {
            float time_effect = (sin((u_animation_time-0.2) * time_scale_factor)+1.0)/2.0;
            float boob_xShift = 0.0;
            float boob_yShift = time_effect * influence;
            boob_Shift = vec2(boob_xShift, boob_yShift);
        }
        else {
            boob_Shift = vec2(0, 0);
        }

        gl_FragColor = texture2D(tex0, v_tex_coord + bounce_shift +  boob_Shift);
        """)


    class ShaderPerson(renpy.Displayable):
        def __init__(self, child, weight, **kwargs):
            super(ShaderPerson, self).__init__(**kwargs)

            self.child = renpy.displayable(child) #Takes a displayable, runs a shader over it based on a given mask.
            self.weight = renpy.displayable(weight) #Takes a displayable, uses the colour channels to provide info to shaders.

        def render(self, width, height, st, at):
            child_render = self.child.render(width, height, st, at)
            child_render.place(self.child)

            w, h = child_render.get_size()
            weight_render = renpy.display.render.Render(w, h)
            weight_render.place(self.weight, main=False)

            rv = renpy.display.render.Render(w, h)

            rv.mesh = True
            rv.add_shader("renpy.texture")



            rv.blit(child_render, (0,0))
            rv.blit(weight_render, (0,0)) #TODO: check that the platform has support for mesh rendering.
            return rv

        def visit(self):
            return [self.weight, self.child]



    ### LEGACY STUFF BELOW ###
    # if not renpy.mobile:
    #     import pygame_sdl2.image as pygame_save
    #     import shader.gpu as gpu
    #     from renpy.display.render import blit_lock




    # if renpy.mobile:
    #     no_animation = VrenAnimation("No Animation", None, []) #A placeholder that can be used to explicitly not animate an image (otherwise characters grab a default animation)
    #
    #     wiggle_animation = VrenAnimation("Boob Butt Wiggle", None, ["breasts","butt"], region_specific_weights = {"butt":0.2})
    #     idle_wiggle_animation = VrenAnimation("Idle Boob Butt Wiggle", None, ["breasts","butt"], innate_animation_strength = 1.0, region_specific_weights = {"butt":0.2})
    #
    #     #sudden_bounce_animation = VrenAnimation("Sudden Wiggle", shader.PS_START_BOUNCE_2D, ["breasts", "butt"], region_specific_weights = {"butt":0.3})
    #
    #     #Blowjob bob moves the top of the screen "closer" to the camera while keeping the bottom (like a girls knees) appearing fixed in one place.
    #     blowjob_bob = VrenAnimation("Blowjob Bob", None, ["breasts","butt"], innate_animation_strength = 1.0, region_specific_weights = {"breasts":1,"butt":0.2})
    #
    #     #Missionary bob is an inverted blowjob bob, it moves the bottom of the screen while holding the top still
    #     missionary_bob = VrenAnimation("Missionary Style Bob", None, ["breasts","butt"], innate_animation_strength = 1.0, region_specific_weights = {"breasts":1,"butt":0.3})
    #
    #     # Test animation with nothing actually manipulated, to see the performance impact of the animation vs. overhead
    #     none_test_animation = VrenAnimation("No Animation", None, [], innate_animation_strength = 1.0, region_specific_weights = {})
    #
    #     #Ass_bob moves the center of the screen while keeping the top and bottom still.
    #     ass_bob = VrenAnimation("Ass Bob", None, ["breasts","butt"], innate_animation_strength = 1.0, region_specific_weights = {"breasts":0.7,"butt":0.35})
    #     tit_bob = VrenAnimation("Tit Bob", None, ["breasts","butt"], innate_animation_strength = 1.0, region_specific_weights = {"breasts":1,"butt":0.2})
    #
    # else:
    no_animation = VrenAnimation("No Animation", "vren.topbounce", []) #A placeholder that can be used to explicitly not animate an image (otherwise characters grab a default animation)

    wiggle_animation = VrenAnimation("Boob Butt Wiggle", "vren.topbounce", ["breasts","butt"], region_specific_weights = {"butt":0.2})
    idle_wiggle_animation = VrenAnimation("Idle Boob Butt Wiggle", "vren.topbounce", ["breasts","butt"], innate_animation_strength = 1.0, innate_animation_speed = 1.0, region_specific_weights = {"butt":0.2})

    #sudden_bounce_animation = VrenAnimation("Sudden Wiggle", shader.PS_START_BOUNCE_2D, ["breasts", "butt"], region_specific_weights = {"butt":0.3})

    #Blowjob bob moves the top of the screen "closer" to the camera while keeping the bottom (like a girls knees) appearing fixed in one place.
    blowjob_bob = VrenAnimation("Blowjob Bob", "vren.topbounce", ["breasts","butt"], innate_animation_strength = 1.0, innate_animation_speed = 3.0, region_specific_weights = {"breasts":1,"butt":0.2})

    #Missionary bob is an inverted blowjob bob, it moves the bottom of the screen while holding the top still
    missionary_bob = VrenAnimation("Missionary Style Bob", "vren.middlebounce", ["breasts","butt"], innate_animation_strength = 1.0, innate_animation_speed = 2.0, region_specific_weights = {"breasts":1,"butt":0.3})

    # Test animation with nothing actually manipulated, to see the performance impact of the animation vs. overhead
    #none_test_animation = VrenAnimation("No Animation", shader.PS_NONE, [], innate_animation_strength = 1.0, region_specific_weights = {})

    #Ass_bob moves the center of the screen while keeping the top and bottom still.
    ass_bob = VrenAnimation("Ass Bob", "vren.middlebounce", ["breasts","butt"], innate_animation_strength = 1.0, innate_animation_speed = 2.0, region_specific_weights = {"breasts":0.7,"butt":0.35})
    tit_bob = VrenAnimation("Tit Bob", "vren.middlebounce", ["breasts","butt"], innate_animation_strength = 1.0, innate_animation_speed = 2.0, region_specific_weights = {"breasts":1,"butt":0.2})


# label draw_tests():
#     "Test starts after this statement proceeds."
#     $ mom.apply_outfit(mom.planned_outfit)
#     $ lily.apply_outfit(lily.planned_outfit)
#     $ the_group = GroupDisplayManager([aunt, mom, lily], mom)
#     python:
#         something_removed = True #Start with this True so that the first loop is always executed.
#         while something_removed:
#             something_removed = False # We end once both girls fail to remove something
#             for the_stripper in [aunt, mom, lily]:
#                 next_item = the_stripper.outfit.remove_random_any(top_layer_first = True, do_not_remove = True)
#                 if next_item:
#                     something_removed = True
#                     the_group.draw_animated_removal(the_stripper, False, the_clothing = next_item)
#                     #renpy.say(the_stripper.title, "Removing: " + next_item.display_name) #TOOD: Remove this, it's just here for debugging purposes
#
#             print (renpy.get_showing_tags("solo", True))
#             renpy.say("","...")
#     return
#
# label draw_tests_2():
#     "Test starts after this statement proceeds."
#     $ mom.apply_outfit(mom.planned_outfit)
#     $ lily.apply_outfit(lily.planned_outfit)
#     $ the_group = GroupDisplayManager([mom, lily], mom)
#
#     $ something_removed = True
#     while something_removed:
#         $ something_removed = False
#         $ next_item = mom.outfit.remove_random_any(top_layer_first = True, do_not_remove = True)
#         if next_item:
#             $ something_removed = True
#             $ the_group.draw_animated_removal(mom, False, the_clothing = next_item)
#
#         $ next_item = lily.outfit.remove_random_any(top_layer_first = True, do_not_remove = True)
#         if next_item:
#             $ something_removed = True
#             $ the_group.draw_animated_removal(lily, False, the_clothing = next_item)
#
#         "..."
#     return
#
# label zip_test():
#     $ file_path = os.path.abspath(os.path.join(config.basedir, "game"))
#     $ test_image = renpy.display.im.ZipFileImage(file_path + "\images\character_images\stand2.zip","white_stand2_standard_body_DD.png") #TODO: test this
#     $ renpy.show(name = "Test", layer = "solo", what = test_image)
#     "Wait to see if it worked"
#     return
#
# label speed_test():
#     $ log_message("Beginning test.")
#     $ start_time = time.time()
#     $ mom.draw_person(position = "stand2")
#     $ log_message("Person one time: " + str(time.time() - start_time))
#     "..."
#     $ clear_scene()
#
#     $ start_time = time.time()
#     $ lily.draw_person(position = "stand2")
#     $ log_message("Person two time: " + str(time.time() - start_time))
#     "..."
#     $ clear_scene()
#
#     "Test Complete."
#     return
