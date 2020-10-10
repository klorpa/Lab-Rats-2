# Holds all functions used to animate characters.


#from gl cimport *

init -1 python:
    if not renpy.mobile:
        import pygame_sdl2.image as pygame_save
        import shader.gpu as gpu
        from renpy.display.render import blit_lock





    if renpy.mobile:
        no_animation = VrenAnimation("No Animation", None, []) #A placeholder that can be used to explicitly not animate an image (otherwise characters grab a default animation)

        wiggle_animation = VrenAnimation("Boob Butt Wiggle", None, ["breasts","butt"], region_specific_weights = {"butt":0.2})
        idle_wiggle_animation = VrenAnimation("Idle Boob Butt Wiggle", None, ["breasts","butt"], innate_animation_strength = 1.0, region_specific_weights = {"butt":0.2})

        #sudden_bounce_animation = VrenAnimation("Sudden Wiggle", shader.PS_START_BOUNCE_2D, ["breasts", "butt"], region_specific_weights = {"butt":0.3})

        #Blowjob bob moves the top of the screen "closer" to the camera while keeping the bottom (like a girls knees) appearing fixed in one place.
        blowjob_bob = VrenAnimation("Blowjob Bob", None, ["breasts","butt"], innate_animation_strength = 1.0, region_specific_weights = {"breasts":1,"butt":0.2})

        #Missionary bob is an inverted blowjob bob, it moves the bottom of the screen while holding the top still
        missionary_bob = VrenAnimation("Missionary Style Bob", None, ["breasts","butt"], innate_animation_strength = 1.0, region_specific_weights = {"breasts":1,"butt":0.3})

        # Test animation with nothing actually manipulated, to see the performance impact of the animation vs. overhead
        none_test_animation = VrenAnimation("No Animation", None, [], innate_animation_strength = 1.0, region_specific_weights = {})

        #Ass_bob moves the center of the screen while keeping the top and bottom still.
        ass_bob = VrenAnimation("Ass Bob", None, ["breasts","butt"], innate_animation_strength = 1.0, region_specific_weights = {"breasts":0.7,"butt":0.35})
        tit_bob = VrenAnimation("Tit Bob", None, ["breasts","butt"], innate_animation_strength = 1.0, region_specific_weights = {"breasts":1,"butt":0.2})

    else:
        no_animation = VrenAnimation("No Animation", shader.PS_BOUNCE2_2D, []) #A placeholder that can be used to explicitly not animate an image (otherwise characters grab a default animation)

        wiggle_animation = VrenAnimation("Boob Butt Wiggle", shader.PS_BOUNCE2_2D, ["breasts","butt"], region_specific_weights = {"butt":0.2})
        idle_wiggle_animation = VrenAnimation("Idle Boob Butt Wiggle", shader.PS_BOUNCE2_2D, ["breasts","butt"], innate_animation_strength = 1.0, region_specific_weights = {"butt":0.2})

        #sudden_bounce_animation = VrenAnimation("Sudden Wiggle", shader.PS_START_BOUNCE_2D, ["breasts", "butt"], region_specific_weights = {"butt":0.3})

        #Blowjob bob moves the top of the screen "closer" to the camera while keeping the bottom (like a girls knees) appearing fixed in one place.
        blowjob_bob = VrenAnimation("Blowjob Bob", shader.PS_BLOWJOB_2D, ["breasts","butt"], innate_animation_strength = 1.0, region_specific_weights = {"breasts":1,"butt":0.2})

        #Missionary bob is an inverted blowjob bob, it moves the bottom of the screen while holding the top still
        missionary_bob = VrenAnimation("Missionary Style Bob", shader.PS_DOGGY_2D, ["breasts","butt"], innate_animation_strength = 1.0, region_specific_weights = {"breasts":1,"butt":0.3})

        # Test animation with nothing actually manipulated, to see the performance impact of the animation vs. overhead
        none_test_animation = VrenAnimation("No Animation", shader.PS_NONE, [], innate_animation_strength = 1.0, region_specific_weights = {})

        #Ass_bob moves the center of the screen while keeping the top and bottom still.
        ass_bob = VrenAnimation("Ass Bob", shader.PS_ASSBOUNCE_2D, ["breasts","butt"], innate_animation_strength = 1.0, region_specific_weights = {"breasts":0.7,"butt":0.35})
        tit_bob = VrenAnimation("Tit Bob", shader.PS_ASSBOUNCE_2D, ["breasts","butt"], innate_animation_strength = 1.0, region_specific_weights = {"breasts":1,"butt":0.2})


label draw_tests():
    "Test starts after this statement proceeds."
    $ mom.apply_outfit(mom.planned_outfit)
    $ lily.apply_outfit(lily.planned_outfit)
    $ the_group = GroupDisplayManager([aunt, mom, lily], mom)
    python:
        something_removed = True #Start with this True so that the first loop is always executed.
        while something_removed:
            something_removed = False # We end once both girls fail to remove something
            for the_stripper in [aunt, mom, lily]:
                next_item = the_stripper.outfit.remove_random_any(top_layer_first = True, do_not_remove = True)
                if next_item:
                    something_removed = True
                    the_group.draw_animated_removal(the_stripper, False, the_clothing = next_item)
                    #renpy.say(the_stripper.title, "Removing: " + next_item.display_name) #TOOD: Remove this, it's just here for debugging purposes

            print (renpy.get_showing_tags("solo", True))
            renpy.say("","...")
    return

label draw_tests_2():
    "Test starts after this statement proceeds."
    $ mom.apply_outfit(mom.planned_outfit)
    $ lily.apply_outfit(lily.planned_outfit)
    $ the_group = GroupDisplayManager([mom, lily], mom)

    $ something_removed = True
    while something_removed:
        $ something_removed = False
        $ next_item = mom.outfit.remove_random_any(top_layer_first = True, do_not_remove = True)
        if next_item:
            $ something_removed = True
            $ the_group.draw_animated_removal(mom, False, the_clothing = next_item)

        $ next_item = lily.outfit.remove_random_any(top_layer_first = True, do_not_remove = True)
        if next_item:
            $ something_removed = True
            $ the_group.draw_animated_removal(lily, False, the_clothing = next_item)

        "..."
    return

label zip_test():
    $ file_path = os.path.abspath(os.path.join(config.basedir, "game"))
    $ test_image = renpy.display.im.ZipFileImage(file_path + "\images\character_images\stand2.zip","white_stand2_standard_body_DD.png") #TODO: test this
    $ renpy.show(name = "Test", layer = "solo", what = test_image)
    "Wait to see if it worked"
    return

label speed_test():
    $ log_message("Beginning test.")
    $ start_time = time.time()
    $ mom.draw_person(position = "stand2")
    $ log_message("Person one time: " + str(time.time() - start_time))
    "..."
    $ clear_scene()

    $ start_time = time.time()
    $ lily.draw_person(position = "stand2")
    $ log_message("Person two time: " + str(time.time() - start_time))
    "..."
    $ clear_scene()

    "Test Complete."
    return
