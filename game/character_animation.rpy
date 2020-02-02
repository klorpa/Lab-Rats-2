# Holds all functions used to animate characters.
#TODO: See how this is going to affect the android community.



#from gl cimport *

init -1 python:
    import pygame_sdl2.image as pygame_save
    from openGL import GL as gl2
    import shader.gpu as gpu
    from renpy.display.render import blit_lock

    import io

    wiggle_animation = VrenAnimation("Boob Butt Wiggle", shader.PS_BOUNCE2_2D, ["breasts","butt"], region_specific_weights = {"butt":0.2})
    idle_wiggle_animation = VrenAnimation("Idle Boob Butt Wiggle", shader.PS_BOUNCE2_2D, ["breasts","butt"], innate_animation_strength = 1.0, region_specific_weights = {"butt":0.2})

    #sudden_bounce_animation = VrenAnimation("Sudden Wiggle", shader.PS_START_BOUNCE_2D, ["breasts", "butt"], region_specific_weights = {"butt":0.3})

    #Blowjob bob moves the top of the screen "closer" to the camera while keeping the bottom (like a girls knees) appearing fixed in one place.
    blowjob_bob = VrenAnimation("Blowjob Bob", shader.PS_BLOWJOB_2D, ["breasts","butt"], innate_animation_strength = 1.0, region_specific_weights = {"breasts":1,"butt":0.2})

    #Missionary bob is an inverted blowjob bob, it moves the bottom of the screen while holding the top still
    missionary_bob = VrenAnimation("Missionary Style Bob", shader.PS_DOGGY_2D, ["breasts","butt"], innate_animation_strength = 1.0, region_specific_weights = {"breasts":1,"butt":0.3})



    # def convert_to_animation(the_person, the_displayable, background_fill = "#0026a5", a_shader = shader.PS_WALK_2D):
    #     #the_displayable = the_person.build_person_displayable(position, emotion, special_modifier, show_person_info, lighting, background_fill = "#0026a5")
    #     the_size = the_displayable.render(10,10,0,0).get_size() # Get the size. Without it our displayable would be stuck in the top left when we changed the size ofthings inside it.
    #     x_size = __builtin__.int(the_size[0])
    #     y_size = __builtin__.int(the_size[1])
    #
    #     the_surftree = renpy.display.render.render_screen(the_displayable, renpy.config.screen_width, renpy.config.screen_height)
    #     the_surface = renpy.display.draw.screenshot(the_surftree, False)
    #     surface_file = io.BytesIO()
    #     #save_surface (the_surface, "FullAnimTest.png")
    #     renpy.display.module.save_png(the_surface, surface_file, 0)
    #     static_image = im.Data(surface_file.getvalue(), "animation_temp_image.png")
    #
    #
    #     the_image_name = "TEST"
    #     the_mask_name = "test_images/FullAnimTest_Mask.png"
    #
    #
    #     #background_mask = Solid("#0000", size = the_size)
    #     the_animation = ShaderDisplayable(shader.MODE_2D, static_image, the_image_name, shader.VS_2D, a_shader,{"tex1":the_mask_name}, {}, None, None)
    #     the_animated_displayable = Crop((0,0,x_size,y_size), the_animation)
    #
    #     renpy.show(the_image_name, at_list=[character_right], layer = "Active", what = the_animated_displayable)
    #     return the_animated_displayable#The shaderdisplayable







    def test_shader(the_person):
        image_name = "test_images/FullAnimTest.png"
        mask_name = "test_images/Test_Mask.png"
        the_animation = ShaderDisplayable(shader.MODE_2D, image_name, image_name, shader.VS_2D, shader.PS_WALK_2D,{"tex1":mask_name}, {}, None, None)
        renpy.show(image_name, layer = "Active", what = the_animation)

        return

    def save_surface(the_surface, the_name):
        file_path = os.path.abspath(os.path.join(config.basedir, "game"))
        file_name = os.path.join(file_path,"images/test_images/"+the_name + ".png")

        pygame.image.save(the_surface, file_name)

    def test_anim_6(the_person): #WORKS! Generates a centered displayable of the person built from their surface
        the_displayable = the_person.build_person_displayable()
        the_psudo = PsudoSurface(the_displayable)
        renpy.show("Test", layer = "Active", what = the_psudo)

    def test_anim_7(the_person): #WORKS! Generates a .png file for a character.
        #Bug: Backround is always black because the draw_screen function
        the_displayable = the_person.build_person_displayable()
        the_surftree = renpy.display.render.render_screen(the_displayable, renpy.config.screen_width, renpy.config.screen_height)
        the_surface = renpy.display.draw.screenshot(the_surftree, False)
        save_surface(the_surface, "TEST35")
