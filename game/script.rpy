init -2: # Establis hsome platform specific stuff.
    if renpy.macintosh:
        default persistent.vren_animation = True
        $ persistent.vren_mac_scale = 1.0 #2.0 # Changes to the way the surface size is calculated has made a mac specific setting like this oboslete. This section is only here until I can confirm everything is working properly.

    else:
        default persistent.vren_animation = True
        $ persistent.vren_mac_scale = 1.0


    default persistent.pregnancy_pref = 0 # 0 = no content, 1 = predictable, 2 = realistic

init -2 python:
    import os
    import copy
    import math
    import __builtin__
    import xml.etree.ElementTree as ET
    import time
    import zipfile
    import io
    from collections import defaultdict

    if not renpy.mobile: #Mobile platforms do not support animation, so we only want to try to import it if we're going to use it.
        import shader

    test_zip = True # Debug setting. If set to False won't work on your system, unless you pack all of the position images into appropriately named zip files.

    # if renpy.mobile or test_zip:
    global mobile_zip_dict
    mobile_zip_dict = {}
    for position in ["stand2", "stand3", "stand4", "stand5", "walking_away", "back_peek", "sitting", "kissing", "doggy", "missionary", "blowjob", "against_wall", "standing_doggy", "kneeling1", "cowgirl"]:
        file_path = "images/character_images/" + position + ".zip"
        renpy_file = renpy.file(file_path)
        mobile_zip_dict[position] = zipfile.ZipFile(renpy_file, "a") #Cache all of the zip files so we have a single static pointer to them.

    #config.use_cpickle = False #Set to True for more useful save failure info



    def take_animation_screenshot(): #Called on every interact beginning, if animation_draw_requested is True it makes the screenshot and starts a new thread to display the image.
        # This approach is needed because draw.screenshot is fast, but must be done in the main thread. Rendering is slower, but can be threaded. This lets us get the best of both worlds.
        global animation_draw_requested #This might have some race conditions if character images are drawn very quickly, but I doubt it will be something to worry about.
        #log_message("General" + " | CLBK | " + str(time.time()))

        for draw_layer in draw_layers: #If multiple draws are prepared in a single interaction we want to screenshot all of them.
            if animation_draw_requested[draw_layer]:
                remove_list = [] #Don't modify the list while iterating, but remove all draws completed when finished.
                for draw_package in animation_draw_requested[draw_layer]:
                    global prepared_animation_render
                    global global_draw_number
                    remove_list.append(draw_package)

                    the_person = draw_package[0]
                    reference_draw_number = draw_package[1]

                    the_render = prepared_animation_render[draw_layer].get(the_person.character_number, None) #TODO: Change how we are stashing things in prepared_animation_render
                    del prepared_animation_render[draw_layer][the_person.character_number] #Clear the render, we don't need to track it any more. Without this image renders build up over the course of the day, consuming massive amounts of memory.

                    if reference_draw_number == the_person.draw_number[draw_layer]+global_draw_number[draw_layer] and the_render is not None: #Only make draws taht are current. If eitehr the personal or global draw number has increased we do not need to draw this.
                        if isinstance(the_render, list): #It's a removal draw (Which makes prepared_animation_render a list of renders, the first (old) one should be drawn on top and faded out.
                            surface_old = renpy.display.draw.screenshot(the_render[0], False)
                            surface_new = renpy.display.draw.screenshot(the_render[1], False)
                            the_render = None

                            position = prepared_animation_arguments[draw_layer][the_person.character_number][1]
                            the_person.draw_person_animation(surface_new, *prepared_animation_arguments[draw_layer][the_person.character_number]) #TODO make sure changing the animation arguments doesn't require us to copy the list to avoid an incorrect shared reference.
                            prepared_animation_arguments[draw_layer][the_person.character_number][11].append(clothing_fade) #Add clothing fade to the extra arguments
                            the_person.draw_person_animation(surface_old, *prepared_animation_arguments[draw_layer][the_person.character_number], clear_active = False) #clear_active is a hack that overrides the normal clear of a character so we can reuse the drawing code.

                            surface_old = None
                            surface_new = None
                            the_render = None

                        else: #It's just a normal draw
                            log_message(the_person.name + " | SCR1 | " + str(time.time()))
                            the_surface = renpy.display.draw.screenshot(the_render, False) #This is the operation that must be in the main thread, and is the major time-consumer for the animation system at the moment.
                            log_message(the_person.name + " | SCR2 | " + str(time.time()))
                            the_render = None
                            the_person.draw_person_animation(the_surface, *prepared_animation_arguments[draw_layer][the_person.character_number])
                            the_surface = None

                for item in remove_list: #Don't just set the list to empty in case a new thread has returned and placed something in the list.
                    animation_draw_requested[draw_layer].remove(item)
        return

    def add_draw_layer(layer_name): #Sets up a character draw layer under the name of "layer name". This can be used to draw multiple characters on the screen at once.
        global draw_layers
        global global_draw_number
        global prepared_animation_render
        global prepared_animation_arguments
        global animation_draw_requested

        if layer_name not in draw_layers:
            draw_layers.append(layer_name)
            renpy.add_layer(layer_name, above = "master")
            config.menu_clear_layers.append(layer_name)
            config.context_clear_layers.append(layer_name)

            global_draw_number[layer_name] = 0
            prepared_animation_render[layer_name] = {}
            prepared_animation_arguments[layer_name] = {} #Stores the arguments based on dict.
            animation_draw_requested[layer_name] = []



    config.interact_callbacks.append(take_animation_screenshot)

    def text_message_history_callback(history_entry): #Manages taking the history entry and slotting it into the appropriate list
        if hasattr(store,"mc"): #Make sure the main character has been instantiated
            if mc.having_text_conversation: #This is set to a Person when talking via text, to allow us to log the interation correctly.
                if history_entry.who is not None and not mc.text_conversation_paused: #Record the dialogue, we'll figure out in the history display section if it's messages from us or a Person.
                    mc.phone.add_message(mc.having_text_conversation, history_entry)
                else:
                    pass #Nothing to do. We don't record narration.

    def text_message_say_callback(who, *args, **kwargs): #Manually sets the style of anything sent as part of a text conversation #NOTE: No longer used or hooked up once the proper phone UI was added
        if hasattr(store,"mc"):
            if mc.having_text_conversation:
                kwargs["what_color"] = "#19e9f7" #We need to define these explicitly so they are not overridden by the characters defaults.
                kwargs["what_font"] = "Autobusbold-1ynL.ttf"
        return args, kwargs

    config.history_callbacks.append(text_message_history_callback) #Ensures conversations had via text are recorded properly
    # config.say_arguments_callback = text_message_say_callback #Recolours and re-fonts say statements made while having a text conversation #NOTE: NOt needed now that we properly store messages into the phone and display them from a custom screen.

    config.predict_screen_statements = True
    config.predict_statements = 50
    config.predict_screens = True

    config.cache_surfaces = True
    config_image_cache_size = 8

    config.has_autosave = False
    config.autosave_frequency = None
    config.has_quicksave = True


    config.rollback_enabled = True #Disabled for the moment because there might be unexpected side effects of such a small rollback length.
    config.rollback_length = 32

    if persistent.colour_palette is None:
        persistent.colour_palette = [[1,1,1,1], [1,1,1,1], [1,1,1,1], [1,1,1,1], [1,1,1,1], [1,1,1,1], [1,1,1,1], [1,1,1,1], [1,1,1,1], [1,1,1,1]]

    config.autoreload = False

    #config.debug_text_overflow = True
    config.debug_text_overflow = False #If enabled finds locations with text overflow. Turns out I have a lot, kind of blows up when enabled and generates a large text file. A problem for another day.

    config.debug_image_cache = False
    config.debug = True

    # THIS IS WHAT PREVENTS IT FROM INDEXING IMAGES
    # SEE 00images.rpy for where this is created
    config.images_directory = None
    preferences.gl_tearing = True ## Prevents juttery animation with text while using advanced shaders to display images

    _preferences.show_empty_window = False #Prevents Ren'py from incorrectly showing the text window in complex menu sitations (which was a new bug/behaviour in Ren'py v7.2)

    global animation_draw_requested #Note that this is broken down by draw layer so that multiple threads can return safely in a single interaction.
    animation_draw_requested = {} #This dict holds each draw layer request. Inside of each draw layer request are lists, which hold the character and their personal reference draw number, so that we can cull out of date draws

    global global_draw_number # Holds the draw numbers for all possible scenes ("solo" is the main one). This value is increased by one every time a scene is cleared, and is used to prevent animations from being drawn after moving on from a scene.
    global_draw_number = {}

    global prepared_animation_render #The render that has been prepared by a separate thread should be placed here.
    prepared_animation_render = {}

    global prepared_animation_arguments #Holds all of the extra arguments that should be passed onto the display code.
    prepared_animation_arguments = {}

    global draw_layers
    draw_layers = []

    add_draw_layer("front_1") # Layers used for extra characters. In theory this can be expanded infinitely, but it reacts poorly to being adjusted mid-game.
    add_draw_layer("solo") # Add the main default draw layer, used for all single character displays
    add_draw_layer("back_1")
    add_draw_layer("back_2")

    # All versions of LR2 now us a .zip based image storage structure, no need for Renpy archives at all any more.
    # build.archive("stand2", "renpy")
    # build.archive("stand3", "renpy")
    # build.archive("stand4", "renpy")
    # build.archive("stand5", "renpy")
    # build.archive("walking_away", "renpy")
    # build.archive("back_peek", "renpy")
    # build.archive("sitting", "renpy")
    # build.archive("kissing", "renpy")
    # build.archive("doggy", "renpy")
    # build.archive("missionary", "renpy")
    # build.archive("blowjob", "renpy")
    # build.archive("against_wall", "renpy")
    # build.archive("standing_doggy", "renpy")
    # build.archive("kneeling1", "renpy")
    # build.archive("cowgirl", "renpy")
    #
    # build.classify("game/images/character_images/**stand2**.png", "stand2") #Package the individual images into archives for the PC versions
    # build.classify("game/images/character_images/**stand3**.png", "stand3")
    # build.classify("game/images/character_images/**stand4**.png", "stand4")
    # build.classify("game/images/character_images/**stand5**.png", "stand5")
    # build.classify("game/images/character_images/**walking_away**.png", "walking_away")
    # build.classify("game/images/character_images/**back_peek**.png", "back_peek")
    # build.classify("game/images/character_images/**sitting**.png", "sitting")
    # build.classify("game/images/character_images/**kissing**.png", "kissing")
    # build.classify("game/images/character_images/**doggy**.png", "doggy")
    # build.classify("game/images/character_images/**missionary**.png", "missionary")
    # build.classify("game/images/character_images/**blowjob**.png", "blowjob")
    # build.classify("game/images/character_images/**against_wall**.png", "against_wall")
    # build.classify("game/images/character_images/**standing_doggy**.png", "standing_doggy")
    # build.classify("game/images/character_images/**kneeling1**.png", "kneeling1")
    # build.classify("game/images/character_images/**cowgirl**.png", "cowgirl")

    build.classify("game/images/character_images/**stand2**.png", None) # unarchived images for the different positiosn are not needed, they are all included in .zip files.
    build.classify("game/images/character_images/**stand3**.png", None)
    build.classify("game/images/character_images/**stand4**.png", None)
    build.classify("game/images/character_images/**stand5**.png", None)
    build.classify("game/images/character_images/**walking_away**.png", None)
    build.classify("game/images/character_images/**back_peek**.png", None)
    build.classify("game/images/character_images/**sitting**.png", None)
    build.classify("game/images/character_images/**kissing**.png", None)
    build.classify("game/images/character_images/**doggy**.png", None)
    build.classify("game/images/character_images/**missionary**.png", None)
    build.classify("game/images/character_images/**blowjob**.png", None)
    build.classify("game/images/character_images/**against_wall**.png", None)
    build.classify("game/images/character_images/**standing_doggy**.png", None)
    build.classify("game/images/character_images/**kneeling1**.png", None)
    build.classify("game/images/character_images/**cowgirl**.png", None)

    build.classify("game/images/character_images/**.zip", "all")


    # build.classify("game/images/character_images/**_Face_10**.png", None) # Bad render, don't add it to any of the builds
    #
    # build.classify("game/images/character_images/**_Face_9**.png", "renpy") # These faces are excluded from the android build due to file size limitaionts
    # build.classify("game/images/character_images/**_Face_11**.png", "renpy")
    # build.classify("game/images/character_images/**_Face_12**.png", "renpy")
    # build.classify("game/images/character_images/**_Face_13**.png", "renpy")
    # build.classify("game/images/character_images/**_Face_14**.png", "renpy")

    def get_obedience_plaintext(obedience_amount):
        obedience_string = "ERROR - Please Tell Vren!"
        if obedience_amount < 50: #49 or less
            obedience_string = "Completely Wild"

        elif obedience_amount < 70: #50 to 69
            obedience_string = "Disobedient"

        elif obedience_amount < 95: #70 to 94
            obedience_string = "Free Spirited"

        elif obedience_amount < 105: #95 to 104
            obedience_string = "Respectful"

        elif obedience_amount < 130: #105 to 129
            obedience_string = "Loyal"

        elif obedience_amount < 150: #130 to 149
            obedience_string = "Docile"

        else: #150 or more
            obedience_string = "Subservient"

        return obedience_string

    def format_titles(the_person):
        person_title = the_person.title
        if person_title is None:
            person_title = "???"
        return_title = "{color=" + the_person.char.who_args["color"] + "}" + "{font=" + the_person.char.what_args["font"] + "}" + person_title + "{/font}{/color}"
        return return_title


    def get_coloured_arrow(direction):
        if direction < 0:
            return "{image=gui/heart/Red_Down.png}"

        elif direction > 0:
            return "{image=gui/heart/Green_Up.png}"

        else:
            return "{image=gui/heart/Grey_Steady.png}"

    def get_red_heart(sluttiness): #A recursive function, feed it a sluttiness and it will return a string of all red heart images for it. Hearts that are entirely empty are left out.
        #TODO: Expand this to let you ask for a minimum number of empty hearts.
        the_final_string = ""
        if sluttiness >= 20:
            the_final_string += "{image=gui/heart/red_heart.png}"
            the_final_string += get_red_heart(sluttiness - 20) #Call it recursively if we might have another heart after this.
        elif sluttiness >= 15:
            the_final_string += "{image=gui/heart/three_quarter_red_quarter_empty_heart.png}"
        elif sluttiness >= 10:
            the_final_string += "{image=gui/heart/half_red_half_empty_heart.png}"
        elif sluttiness >= 5:
            the_final_string += "{image=gui/heart/quarter_red_three_quarter_empty_heart.png}"

        return the_final_string

    def get_gold_heart(sluttiness):
        the_final_string = ""
        if sluttiness >= 20:
            the_final_string += "{image=gui/heart/gold_heart.png}"
            the_final_string += get_gold_heart(sluttiness - 20) #Call it recursively if we might have another heart after this.
        elif sluttiness >= 15:
            the_final_string += "{image=gui/heart/three_quarter_gold_quarter_empty_heart.png}"
        elif sluttiness >= 10:
            the_final_string += "{image=gui/heart/half_gold_half_empty_heart.png}"
        elif sluttiness >= 5:
            the_final_string += "{image=gui/heart/quarter_gold_three_quarter_empty_heart.png}"

        return the_final_string


    def get_heart_image_list(the_person): ##Returns a formatted string that will add coloured hearts in line with text, perfect for menu choices, ect.
        heart_string = "{image=" + get_individual_heart(the_person.core_sluttiness, the_person.sluttiness, the_person.core_sluttiness+the_person.suggestibility) + "}"
        heart_string += "{image=" + get_individual_heart(the_person.core_sluttiness-20, the_person.sluttiness-20, the_person.core_sluttiness+the_person.suggestibility-20) + "}"
        heart_string += "{image=" + get_individual_heart(the_person.core_sluttiness-40, the_person.sluttiness-40, the_person.core_sluttiness+the_person.suggestibility-40) + "}"
        heart_string += "{image=" + get_individual_heart(the_person.core_sluttiness-60, the_person.sluttiness-60, the_person.core_sluttiness+the_person.suggestibility-60) + "}"
        heart_string += "{image=" + get_individual_heart(the_person.core_sluttiness-80, the_person.sluttiness-80, the_person.core_sluttiness+the_person.suggestibility-80) + "}"

        # if the_person.suggestibility <= 0:
        #     heart_string += "{image=gui/heart/Grey_Steady.png}"
        # elif the_person.sluttiness > the_person.core_sluttiness:
        #     heart_string += "{image=gui/heart/Green_Up.png}"
        # elif the_person.sluttiness < the_person.core_sluttiness:
        #     heart_string += "{image=gui/heart/Red_Down.png}"
        # else:
        #     heart_string += "{image=gui/heart/Grey_Steady.png}"
        return heart_string


    def get_individual_heart(core_slut, temp_slut, suggest_slut): #Give this the core, temp, core+suggest slut, minus 20*(current heart-1) each and it will find out the current heart status for that chunk of the heart array.
        image_string = "gui/heart/"
        #suggest_slut += 10 #Add 10, which is the default limit to temp slut if they have no serum in them. #No longer added, testing more direct way of increasing sluttiness.
        #None of the core heart statuses were reached. We must be in a duel or tri-colour heart state.
        if core_slut < 5:
            #There is no gold to draw.
            if temp_slut < 5:
                #There's no temp to draw either.
                if suggest_slut < 5:
                    image_string += "empty_heart.png"
                    #can't happen, we checked for this above, it's a pure heart.

                elif suggest_slut < 10:
                    #It's a quarter grey, three quarter empty
                    image_string += "quarter_grey_three_quarter_empty_heart.png"

                elif suggest_slut < 15:
                    #It's half grey, half empty
                    image_string += "half_grey_half_empty_heart.png"

                elif suggest_slut < 20:
                    #It's three quarters grey, 1 quarter empty
                    image_string += "three_quarter_grey_quarter_empty_heart.png"

                else:
                    image_string += "grey_heart.png"

            elif temp_slut < 10:
                #It's a quarter red and...
                if suggest_slut < 10:
                    #There's no suggest to draw, the rest is empty.
                    image_string += "quarter_red_three_quarter_empty_heart.png"

                elif suggest_slut < 15:
                    #it's got a half grey, then empty
                    image_string += "quarter_red_quarter_grey_half_empty_heart.png"

                elif suggest_slut < 20:
                    #the rest is grey
                    image_string += "quarter_red_half_grey_quarter_empty_heart.png"

                else:
                    #It's three quarters grey
                    image_string += "quarter_red_three_quarter_grey_heart.png"

            elif temp_slut < 15:
                #It's two quarters red and...
                if suggest_slut < 15:
                    # Nothing, it's half red, half empty
                    image_string += "half_red_half_empty_heart.png"

                elif suggest_slut < 20:
                    # half red, quarter grey, quarter empty
                    image_string += "half_red_quarter_grey_quarter_empty_heart.png"

                else:
                    # half red, half grey
                    image_string += "half_red_half_grey_heart.png"

            elif temp_slut < 20:
                #It's three quarters red and...
                if suggest_slut < 15:
                    # three quarters red and 1 empty
                    image_string += "three_quarter_red_quarter_empty_heart.png"

                else:
                    # three quarters red and 1 grey
                    image_string += "three_quarter_red_quarter_grey_heart.png"

            else:
                image_string += "red_heart.png"

        elif core_slut < 10:
            #It fits in the 5 catagory
            if temp_slut < 10:
                #There's no temp slut worth worrying about
                if suggest_slut < 10:
                    # quarter gold, rest empty.
                    image_string += "quarter_gold_three_quarter_empty_heart.png"

                elif suggest_slut < 15:
                    #quarter gold, quarter grey, empty.
                    image_string += "quarter_gold_quarter_grey_half_empty_heart.png"

                elif suggest_slut < 20:
                    #quarter gold, half grey, empty
                    image_string += "quarter_gold_half_grey_quarter_empty_heart.png"

                else:
                    #quarter gold, rest grey
                    image_string += "quarter_gold_three_quarter_grey_heart.png"

            elif temp_slut < 15:
                #quarter gold, quarter red, and...
                if suggest_slut < 15:
                    #quarter gold, quarter red, rest empty
                    image_string += "quarter_gold_quarter_red_half_empty_heart.png"
                elif suggest_slut < 20:
                    #quarter gold, quarter red, quarter grey, rest empty
                    image_string += "quarter_gold_quarter_red_quarter_grey_quarter_empty_heart.png"
                else:
                    #quarter gold, quarter red, half grey
                    image_string += "quarter_gold_quarter_red_half_grey_heart.png"

            elif temp_slut < 20:
                #quarter gold, half red, and..
                if suggest_slut < 20:
                    #quarter gold, half red, empty
                    image_string += "quarter_gold_half_red_quarter_empty_heart.png"
                else:
                    #quarter gold, half red, quarter grey
                    image_string += "quarter_gold_half_red_quarter_grey_heart.png"

            else:
                #quarter gold, rest red
                image_string += "quarter_gold_three_quarter_red_heart.png"

        elif core_slut < 15:
            #It fits in the 10 catagory, half is gold
            if temp_slut < 15:
                #No temp slut
                if suggest_slut < 15:
                    #half gold, rest empty
                    image_string += "half_gold_half_empty_heart.png"
                elif suggest_slut < 20:
                    # half gold, quarter grey, empty
                    image_string += "half_gold_quarter_grey_quarter_empty_heart.png"
                else:
                    #Half gold, half grey
                    image_string += "half_gold_half_grey_heart.png"
            elif temp_slut < 20:
                #half gold, quarter red...
                if suggest_slut < 20:
                    #half gold, quarter red, rest empty
                    image_string += "half_gold_quarter_red_quarter_empty_heart.png"
                else:
                    #half gold, quarter red, rest grey
                    image_string += "half_gold_quarter_red_quarter_grey_heart.png"
            else:
                #half gold, half red
                image_string += "half_gold_half_red_heart.png"

        elif core_slut < 20:
            #three quarters gold and..
            if temp_slut < 20:
                #No temp slut
                if suggest_slut < 20:
                    #three quarters gold, rest empty
                    image_string += "three_quarter_gold_quarter_empty_heart.png"
                else:
                    #three quarters gold, rest grey
                    image_string += "three_quarter_gold_quarter_grey_heart.png"
            else:
                image_string += "three_quarter_gold_quarter_red_heart.png"
                #three quarters gold, rest red

        else:
            image_string += "gold_heart.png"

        return image_string

    def opinion_score_to_string(the_score): #Takes an opinion score and puts it into a plain string.
        if the_score == -2:
            return "hates"

        elif the_score == -1:
            return "dislikes"

        elif the_score == 0:
            return "has no opinion on"

        elif the_score == 1:
            return "likes"

        else: #the_score == 2:
            return "loves"

    def SO_relationship_to_title(relationship_string): #Takes a character relationship (Girlfriend, Fiancée, Married) and returns the male equivalent
        if relationship_string == "Girlfriend":
            return "boyfriend"
        elif relationship_string == "Fiancée":
            return "fiancé"
        elif relationship_string == "Married":
            return "husband"
        else:
            return "ERROR - relationship incorrectly defined"

    def girl_relationship_to_title(relationship_string):
        if relationship_string == "Girlfriend":
            return "girlfriend"
        elif relationship_string == "Fiancée":
            return "fiancée"
        elif relationship_string == "Married":
            return "wife"
        else:
            return "ERROR - relationship incorrectly defined"

    def can_use_animation(): #Checks key properties to determine if we can or cannot use animation (mainly rendering type and config option
        if renpy.mobile: #Unfortunately no animation support for mobile devices.
            return False

        if renpy.display.draw.info["renderer"] == "sw": #Software rendering does not support the screen capture technique we use, so we can only use static images for it. (also it runs painfully slow, so it needs everything it can get).
            return False

        if not persistent.vren_animation:
            return False

        return True

    def clear_scene(specific_layers = None): # Clears the current scene of characters. Both calls Renpy.scene("solo") as well as advances the current draw count so nothing is drawn by an out of date thread.
        global draw_layers
        if specific_layers is not None and not isinstance(specific_layers, list):
            specific_layers = [specific_layers] #Allows for passing lists or single names.

        for a_layer in draw_layers:
            if specific_layers is None or a_layer in specific_layers:
                global_draw_number[a_layer] += 1
                renpy.scene(a_layer)

    class Business(renpy.store.object):
        # main jobs to start with:
        # 1) buying raw supplies.
        # 2) researching new serums.
        # 2a) The player (only) designs new serums to be researched.
        # 3) working in the lab to produce serums.
        # 4) Working in marketing. Increases volumn you can sell, and max price you can sell for.
        # 5) Packaging and selling serums that have been produced.
        # 6) General secretary work. Starts at none needed, grows as your company does (requires an "HR", eventually). Maybe a general % effectivness rating.
        def __init__(self, name, m_div, p_div, r_div, s_div, h_div):
            self.name = name
            self.funds = 1000 #Your starting wealth.

            self.bankrupt_days = 0 #How many days you've been bankrupt. If it hits the max value you lose.
            self.max_bankrupt_days = 3 #How many days you can be negative without loosing the game. Can be increased through research.

            self.m_div = m_div #The phsyical locations of all of the teams, so you can move to different offices in the future.
            self.p_div = p_div
            self.r_div = r_div
            self.s_div = s_div
            self.h_div = h_div

            #Uniforms are stored as a wardrobe specific to each department. There is also a company wide wardrobe that can be accessed.
#            self.all_uniform = Wardrobe(self.name + " All Wardrobe")
            self.m_uniform = Wardrobe(self.name + " Marketing Wardrobe")
            self.p_uniform = Wardrobe(self.name + " Production Wardrobe")
            self.r_uniform = Wardrobe(self.name + " Research Wardrobe")
            self.s_uniform = Wardrobe(self.name + " Supply Wardrobe")
            self.h_uniform = Wardrobe(self.name + " HR Wardrobe")
            self.all_uniform = Wardrobe(self.name + " Shared Uniform Wardrobe")

            self.m_serum = None #These are the serums given to the different departments if the daily serum dosage policy is researched.
            self.p_serum = None
            self.r_serum = None
            self.s_serum = None
            self.h_serum = None

            self.research_team = [] #Researches new serums that the player designs, does theoretical research into future designs, or improves old serums slightly over time
            self.market_team = [] # Increases company marketability. Raises max price serum can be sold for, and max volumn that can be sold.
            self.supply_team = [] # Buys the raw supplies used by the other departments.
            self.production_team = [] # Physically makes the serum and sends it off to be sold.
            self.hr_team = [] # Manages everyone else and improves effectiveness. Needed as company grows.

            self.head_researcher = None #A reference to the head researcher is stored here, for use in important events.
            self.company_model = None #A reference to the currnet company model. May be used for some events.

            self.max_employee_count = 5

            self.supply_count = 0
            self.supply_goal = 250
            self.auto_sell_threshold = None
            self.marketability = 0
            #self.production_points = 0 Use to be used to store partial progress on serum. is now stored in the assembly line array
            self.team_effectiveness = 100 #Ranges from 50 (Chaotic, everyone functions at 50% speed) to 200 (masterfully organized). Normal levels are 100, special traits needed to raise it higher.
            self.effectiveness_cap = 100 #Max cap, can be raised.

            self.research_tier = 0 #The tier of research the main charcter has unlocked with storyline events. 0 is starting, 3 is max.

            self.serum_designs = [] #Holds serum designs that you have researched.
            self.active_research_design = None #The current research (serum design or serum trait) the business is working on

            self.batch_size = 5 #How many serums are produced in each production batch
            self.production_lines = 2 #How many different production lines the player has access to.
            self.serum_production_array = {} #This dict will hold tuples of int(line number):[SerumDesign, int(weight), int(production points), int(autosell)]


            self.inventory = SerumInventory([])
            self.sale_inventory = SerumInventory([])

            self.policy_list = [] #This is a list of Policy objects.
            self.active_policy_list = [] #This is a list of currently active policies (vs just owned ones)

            self.message_list = [] #This list of strings is shown at the end of each day on the business update screen. Cleared each day.
            self.counted_message_list = {} #This is a dict holding the count of each message stored in it. Used when you want to have a message that is counted and the total shown at the end of the day.
            self.production_potential = 0 #How many production points the team was capable of
            self.supplies_purchased = 0
            self.production_used = 0 #How many production points were actually used to make something.
            self.research_produced = 0 #How much research the team produced today.
            self.sales_made = 0
            self.serums_sold = 0

            self.sales_multipliers = [] #This list holds ["Source_type",multiplier_as_float]. The multiplier is applied to the value of serums when they are sold.
            # Only the most positive modifier of any source type is used. (This means a 1.0 modifier can be used to replace a negative modifier).


            self.mandatory_crises_list = [] #A list of crises to be resolved at the end of the turn, generally generated by events that have taken place.
            self.mandatory_morning_crises_list = [] #A list of specifically morning crises that need to be resolved.

            self.event_triggers_dict = {} #This dictionary will be used to hold flags for story events and triggers. In general a string is the key and a bool is the value stored.
            self.event_triggers_dict["policy_tutorial"] = 1 #We have a policy tutorial.
            self.event_triggers_dict["research_tutorial"] = 1 #We have a research tutorial.
            self.event_triggers_dict["design_tutorial"] = 1 #We have a serum design tutorial.
            self.event_triggers_dict["production_tutorial"] = 1 #We have a production tutorial.
            self.event_triggers_dict["outfit_tutorial"] = 1 #We have an outfit design tutorial.
            self.event_triggers_dict["hiring_tutorial"] = 1 #We have an outfit design tutorial.

            self.listener_system = Listener_Management_System()

        def run_turn(self): #Run each time the time segment changes. Most changes are done here.
            if time_of_day == 1 and daily_serum_dosage_policy.is_active() and self.is_work_day(): #Not done on run_day because we want it to apply at the _start_ of the day.
                self.give_daily_serum()

            #Compute efficency drop
            for person in self.supply_team + self.research_team + self.production_team + self.market_team:
                if person in self.s_div.people + self.r_div.people + self.p_div.people + self.m_div.people: #Only people in the office lower effectiveness, no loss on weekends, not in for the day, etc.
                    self.team_effectiveness += -1 #TODO: Make this dependant on charisma (High charisma have a lower impact on effectiveness) and happiness.

            #Compute effiency rise from HR
            for person in self.hr_team:
                if person in self.h_div.people:
                    self.hr_progress(person.charisma,person.int,person.hr_skill)
                    person.change_happiness(person.get_opinion_score("working")+person.get_opinion_score("HR work"), add_to_log = False)

            if self.team_effectiveness < 50:
                self.team_effectiveness = 50

            if self.team_effectiveness > self.effectiveness_cap:
                self.team_effectiveness = self.effectiveness_cap

            #Compute other deparement effects
            for person in self.supply_team:
                if person in self.s_div.people: #Check to see if the person is in the room, otherwise don't count their progress (they are at home, dragged away by PC, weekend, etc.)
                    self.supply_purchase(person.focus,person.charisma,person.supply_skill)
                    person.change_happiness(person.get_opinion_score("working")+person.get_opinion_score("supply work"), add_to_log = False)

            for person in self.research_team:
                if person in self.r_div.people:
                    self.research_progress(person.int,person.focus,person.research_skill)
                    person.change_happiness(person.get_opinion_score("working")+person.get_opinion_score("research work"), add_to_log = False)

            for person in self.production_team:
                if person in self.p_div.people:
                    self.production_progress(person.focus,person.int,person.production_skill)
                    person.change_happiness(person.get_opinion_score("working")+person.get_opinion_score("production work"), add_to_log = False)

            self.mark_autosale() #Mark extra serums to be sold by marketing.

            for person in self.market_team:
                if person in self.m_div.people:
                    if person.should_wear_uniform():
                        self.sale_progress(person.charisma,person.focus, person.market_skill, slut_modifier = person.outfit.slut_requirement) #If there is a uniform pass it's sluttiness along.
                    else:
                        self.sale_progress(person.charisma, person.focus, person.market_skill) #Otherwise their standard outfit provides no bonuses.
                    person.change_happiness(person.get_opinion_score("working")+person.get_opinion_score("marketing work"), add_to_log = False)

            for policy in self.active_policy_list:
                policy.on_turn()

        def run_move(self):
            for policy in self.active_policy_list:
                policy.on_move()



        def run_day(self): #Run at the end of the day.
            #Pay everyone for the day
            if mc.business.is_work_day():
                cost = self.calculate_salary_cost()
                self.funds += -cost

                for policy in self.active_policy_list:
                    policy.on_day()
            return

        def is_open_for_business(self): #Checks to see if employees are currently working
            if not self.is_work_day(): #It is the weekend, people have the day off.
                return False

            elif time_of_day == 1 or time_of_day == 2 or time_of_day == 3: #It is the work period of the day
                return True

            return False #If all else fails, give them some time off.

        def is_work_day(self):
            if day % 7 == 5 or day % 7 == 6: #TODO: add support for expanding workdays
                return False
            return True

        def is_weekend(self):#TODO: add support for expanding/changing the weekend
            if day % 7 == 5 or day % 7 == 6: #Checks to see if it is saturday or sunday. Note that days might eventually be both neither weekend or workday, or both weekend AND workday!
                return True
            return False

        def get_uniform_wardrobe(self,title): #Takes a title and returns the correct uniform for that division, if one exists. If it is None, returns false. TODO: get this working.
            if title == "Marketing":
                return self.m_uniform.merge_wardrobes(self.all_uniform)
            elif title == "Researcher":
                return self.r_uniform.merge_wardrobes(self.all_uniform)
            elif title == "Production":
                return self.p_uniform.merge_wardrobes(self.all_uniform)
            elif title == "Supply":
                return self.s_uniform.merge_wardrobes(self.all_uniform)
            elif title == "Human Resources":
                return self.h_uniform.merge_wardrobes(self.all_uniform)
            else:
                return None

        def get_uniform_wardrobe_for_person(self, the_person):
            return self.get_uniform_wardrobe(self.get_employee_title(the_person))

        def get_uniform_limits(self): #Returns three values: the max sluttiness of a full outfit, max sluttiness of an underwear set, and if only overwear sets are allowed or notself.
            slut_limit = 0
            underwear_limit = 0
            limited_to_top = True
            if maximal_arousal_uniform_policy.is_active():
                slut_limit = 999 #ie. no limit at all.
                underwear_limit = 999
                limited_to_top = False
            elif corporate_enforced_nudity_policy.is_active():
                slut_limit = 80
                underwear_limit = 999
                limited_to_top = False
            elif minimal_coverage_uniform_policy.is_active():
                slut_limit = 60
                underwear_limit = 15
                limited_to_top = False
            elif reduced_coverage_uniform_policy.is_active():
                slut_limit = 40
                underwear_limit = 10
                limited_to_top = False
            elif casual_uniform_policy.is_active():
                slut_limit = 25
                underwear_limit = 0
                limited_to_top = True
            elif relaxed_uniform_policy.is_active():
                slut_limit = 15
                underwear_limit = 0
                limited_to_top = True
            elif strict_uniform_policy.is_active():
                slut_limit = 5
                underwear_limit = 0
                limited_to_top = True
            else:
                slut_limit = 0
                underwear_limit = 0
                limited_to_top = True
            return slut_limit, underwear_limit, limited_to_top

        def clear_messages(self): #clear all messages for the day.
            self.message_list = []
            self.counted_message_list = {}
            self.production_potential = 0
            self.supplies_purchased = 0
            self.production_used = 0
            self.research_produced = 0
            self.sales_made = 0
            self.serums_sold =0

        def add_counted_message(self,message,new_count):
            if message in self.counted_message_list:
                self.counted_message_list[message] += new_count
            else:
                self.counted_message_list[message] = new_count

        def add_normal_message(self,message): #Adds an uncounted message, only ever listed once per day
            if message not in self.message_list:
                self.message_list.append(message)

        def calculate_salary_cost(self):
            daily_cost = 0
            for person in self.supply_team + self.research_team + self.production_team + self.market_team + self.hr_team:
                daily_cost += person.salary
            return daily_cost

        def add_serum_design(self,the_serum):
            self.serum_designs.append(the_serum)

        def remove_serum_design(self,the_serum):
            self.serum_designs.remove(the_serum)
            if the_serum is self.active_research_design:
                self.active_research_design = None

            delete_list = []
            for line in self.serum_production_array:
                if the_serum is self.serum_production_array[line][0]:
                    delete_list.append(line) #Store a list of all the keys we need to delete to avoid modifying while interating. Needed in case two lines are making the same serum.

            for key in delete_list: #Now delete the production lines.
                del self.serum_production_array[key]

        def set_serum_research(self,new_research):
            self.active_research_design = new_research

        def research_progress(self,int,focus,skill):
            research_amount = __builtin__.round(((3*int) + (focus) + (2*skill) + 10) * (self.team_effectiveness))/100

            if self.head_researcher:
                bonus_percent = (self.head_researcher.int - 2)*0.05
                research_amount = research_amount * (1.0 + bonus_percent) #Every point above int 2 gives a 5% bonus.
                if bonus_percent > 0:
                    self.add_normal_message("Head researcher " + self.head_researcher.title + "'s intelligence resulted in a " + str(bonus_percent*100) + "% increase in research produced!")
                else:
                    self.add_normal_message("Head researcher " + self.head_researcher.title + "'s intelligence resulted in a " + str(bonus_percent*100) + "% change in research produced.")
            else:
                research_amount = research_amount * 0.9 #No head researcher is treated like int 0.
                self.add_normal_message("No head researcher resulted in a 10% reduction in research produced! Assign a head researcher at R&D!")

            if self.active_research_design is not None:
                the_research = self.active_research_design
                is_researched = the_research.researched # If it was researched before we added any research then we are increasing the mastery level of a trait (does nothing to serum designs)
                self.research_produced += research_amount
                if the_research.add_research(research_amount): #Returns true if the research is completed by this amount'
                    if isinstance(the_research, SerumDesign):
                        the_research.generate_side_effects() #The serum will generate any side effects that are needed.
                        self.mandatory_crises_list.append(Action("Research Finished Crisis",serum_creation_crisis_requirement,"serum_creation_crisis_label",the_research)) #Create a serum finished crisis, it will trigger at the end of the round
                        self.add_normal_message("New serum design researched: " + the_research.name)
                        self.active_research_design = None
                    elif isinstance(the_research, SerumTrait):
                        if is_researched: #We've reseached it already, increase mastery level instead.
                            self.add_normal_message("Serum trait mastery improved: " + the_research.name + ", Now " + str(the_research.mastery_level))
                        else:
                            self.add_normal_message("New serum trait researched: " + the_research.name)
                            self.active_research_design = None #If it's a newly discovered trait clear it so we don't start mastering it without player input.

            else:
                research_amount = 0 #We didn't actually research anything because there is nothing to research!

            return research_amount

        def player_research(self):
            amount_researched = self.research_progress(mc.int,mc.focus,mc.research_skill)
            self.listener_system.fire_event("general_work")
            self.listener_system.fire_event("player_research", amount = amount_researched)
            renpy.say("","You spend time in the lab, experimenting with different chemicals and techniques and producing " + str(amount_researched) + " research points.")
            return amount_researched

        def player_buy_supplies(self):
            amount_bought = self.supply_purchase(mc.focus,mc.charisma,mc.supply_skill)
            self.listener_system.fire_event("general_work")
            self.listener_system.fire_event("player_supply_purchase", amount = amount_bought)
            renpy.say("","You spend time securing new supplies for the lab, purchasing " + str(amount_bought) + " units of serum supplies.")
            return amount_bought

        def supply_purchase(self,focus,cha,skill):
            max_supply = __builtin__.round(((3*focus) + (cha) + (2*skill) + 10) * (self.team_effectiveness))/100
            max_supply = int(max_supply)
            if max_supply + self.supply_count > self.supply_goal:
                max_supply = self.supply_goal - self.supply_count
                if max_supply <= 0:
                    return 0

            self.funds += -max_supply
            self.supply_count += max_supply
            self.supplies_purchased += max_supply #Used for end of day reporting
            return max_supply

        def player_market(self):
            amount_sold = self.sale_progress(mc.charisma,mc.focus,mc.market_skill)
            self.listener_system.fire_event("player_serums_sold_count", amount = amount_sold)
            self.listener_system.fire_event("general_work")
            renpy.say("","You spend time making phone calls to clients and shipping out orders. You sell " + str(amount_sold) + " doses of serum.")
            return amount_sold

        def sale_progress(self,cha,focus,skill, slut_modifier = 0):

            serum_value_multiplier = 1.00 #For use with value boosting policies. Multipliers are multiplicative.
            if male_focused_marketing_policy.is_active(): #Increase value by the character's outfit sluttiness if you own that policy.
                sluttiness_multiplier = (slut_modifier/100.0) + 1
                serum_value_multiplier = serum_value_multiplier * (sluttiness_multiplier)

            multipliers_used = {} #Generate a dict with only the current max multipliers of each catagory.
            for multiplier_source in self.sales_multipliers:
                if not multiplier_source[0] in multipliers_used:
                    multipliers_used[multiplier_source[0]] = multiplier_source[1]
                elif multiplier_source[1] > multipliers_used.get(multiplier_source[0]):
                    multipliers_used[multiplier_source[0]] = multiplier_source[1]

            for maxed_multiplier in multipliers_used:
                value_change = multipliers_used.get(maxed_multiplier)
                serum_value_multiplier = serum_value_multiplier * value_change
                if value_change > 1:
                    self.add_normal_message("+" + str((value_change-1)*100) + "% serum value due to " + maxed_multiplier + ".")
                elif value_change < 1: #No message shown for exactly 1.
                    self.add_normal_message(str((value_change-1)*100) + "% serum value due to " + maxed_multiplier + ".") #Duplicate normal messages are not shown twice, so this should only exist once per turn, per multiplier.

            serum_sale_count = __builtin__.round(((3*cha) + (focus) + (2*skill) + 5) * (self.team_effectiveness))/100 #Total number of doses of serum that can be sold by this person.
            serum_sale_count = __builtin__.int(serum_sale_count)
            sorted_by_value = sorted(self.sale_inventory.serums_held, key = lambda serum: serum[0].value) #List of tuples [SerumDesign, count], sorted by the value of each design. Used so most valuable serums are sold first.
            if self.sale_inventory.get_any_serum_count() < serum_sale_count:
                serum_sale_count = self.sale_inventory.get_any_serum_count()

            this_batch_serums_sold = 0
            if serum_sale_count > 0: #ie. we have serum in our inventory to sell, and the capability to sell them.
                for serum in sorted_by_value:
                    if serum_sale_count <= serum[1]:
                        #There are enough to satisfy order. Remove, add value to wallet, and break
                        value_sold = serum_sale_count * serum[0].value * serum_value_multiplier
                        if value_sold < 0:
                            value_sold = 0
                        self.funds += value_sold
                        self.sales_made += value_sold
                        self.listener_system.fire_event("serums_sold_value", amount = value_sold)
                        self.serums_sold += serum_sale_count
                        this_batch_serums_sold += serum_sale_count
                        self.sale_inventory.change_serum(serum[0],-serum_sale_count)
                        serum_sale_count = 0
                        break
                    else:
                        #There are not enough in this single order, remove _all_ of them, add value, go onto next thing.
                        serum_sale_count += -serum[1] #We were able to sell this number of serum.
                        value_sold = serum[1] * serum[0].value * serum_value_multiplier
                        if value_sold < 0:
                            value_sold = 0
                        self.funds += value_sold
                        self.sales_made += value_sold
                        self.listener_system.fire_event("serums_sold_value", amount = value_sold)
                        self.serums_sold += serum_sale_count
                        this_batch_serums_sold += serum_sale_count
                        self.sale_inventory.change_serum(serum[0],-serum[1]) #Should set serum count to 0.
                        #Don't break, we haven't used up all of the serum count
            return this_batch_serums_sold



        def production_progress(self,focus,int,skill):
            #First, figure out how many production points we can produce total. Subtract that much supply and mark that much production down for the end of day report.
            production_amount = __builtin__.round(((3*focus) + (int) + (2*skill) + 10) * (self.team_effectiveness))/100
            self.production_potential += production_amount

            if self.serum_production_array is None:
                return #If we don't have anything in production just tally how much we could have produced and move on.

            if production_amount > self.supply_count:
                production_amount = self.supply_count #Figure out our total available production, before we split it up between tasks (which might not have 100% usage!)

            #Now go through each production line we have marked.
            for production_line in self.serum_production_array:
                # A production line is a tuple of [SerumDesign, production weight (int), production point progress (int)].
                serum_weight = self.serum_production_array[production_line][1]
                the_serum = self.serum_production_array[production_line][0]

                proportional_production = (serum_weight/100.0) * production_amount #Get the closest integer value for the weighted production we put into the serum
                self.production_used += proportional_production #Update our usage stats and subract supply needed.
                self.supply_count += -proportional_production

                self.serum_production_array[production_line][2] += proportional_production
                serum_prod_cost = the_serum.production_cost
                if serum_prod_cost <= 0:
                    serum_prod_cost = 1
                serum_count = self.serum_production_array[production_line][2]//serum_prod_cost #Calculates the number of batches we have made (previously for individual serums, now for entire batches)
                if serum_count > 0:
                    self.add_counted_message("Produced " + self.serum_production_array[production_line][0].name,serum_count*self.batch_size) #Give a note to the player on the end of day screen for how many we made.
                    self.serum_production_array[production_line][2] -= serum_count * self.serum_production_array[production_line][0].production_cost
                    self.inventory.change_serum(self.serum_production_array[production_line][0],serum_count*self.batch_size) #Add the number serums we made to our inventory.

            return production_amount

        def change_production(self,new_serum,production_line):
            if production_line in self.serum_production_array: #If it already exists, change the serum type and production points stored, but keep the weight for that line (it can be changed later)
                self.serum_production_array[production_line][0] = new_serum
                self.serum_production_array[production_line][1] = int(100 - self.get_used_line_weight() + self.serum_production_array[production_line][1]) #Set the production weight to everything we have remaining
                self.serum_production_array[production_line][2] = 0 #Set production points stored to 0 for the new serum
                self.serum_production_array[production_line][3] = -1 #Set autosell to -1, ie. don't auto sell.
            else: #If the production line didn't exist before, add a key for that line.
                self.serum_production_array[production_line] = [new_serum, int(100 - self.get_used_line_weight()), 0, -1]

        def get_used_line_weight(self):
            used_production = 0
            for existing_lines in self.serum_production_array:
                used_production += self.serum_production_array[existing_lines][1] #Tally how much weight we are using so far.
            return used_production

        def change_line_weight(self,line,weight_change):
            if line in self.serum_production_array:
                used_production = self.get_used_line_weight()
                if weight_change > 0 and weight_change + used_production > 100:
                    weight_change = 100 - used_production #If the full weight change would put us above our 100% max cap it at as much as can be assigned.

                self.serum_production_array[line][1] += weight_change
                if self.serum_production_array[line][1] < 0:
                    self.serum_production_array[line][1] = 0 #We cannot have a value less than 0%

        def change_line_autosell(self, line, threshold_change):
            if line in self.serum_production_array:
                if threshold_change > 0 and self.serum_production_array[line][3] < 0: #We use negative values as a marker for no threshold. If it's negative always treat it as -1 when we start adding again.
                    self.serum_production_array[line][3] = -1
                self.serum_production_array[line][3] += threshold_change

        def mark_autosale(self):
            for line in self.serum_production_array:
                if self.serum_production_array[line][3] >= 0: #There is an auto sell threshold set.
                    if self.inventory.get_serum_count(self.serum_production_array[line][0]) > self.serum_production_array[line][3]:
                        difference = int(self.inventory.get_serum_count(self.serum_production_array[line][0]) - self.serum_production_array[line][3]) #Check how many serums we need to sell to bring us to the threshold.
                        self.inventory.change_serum(self.serum_production_array[line][0], -difference) #Remove them from the production inventory.
                        self.sale_inventory.change_serum(self.serum_production_array[line][0], difference) #Add them to the sales inventory.

        def get_random_weighed_production_serum(self): #Return the serum design of one of our activly produced serums, relative probability by weight.
            used_production = 0
            for key in self.serum_production_array:
                used_production += self.serum_production_array[key][1] #Sum how much production we are using, usually 100%
            if used_production == 0:
                return None #If we are not _actually_ producing anything, return None.

            random_serum_number = renpy.random.randint(0,used_production)
            for key in self.serum_production_array:
                if random_serum_number <= self.serum_production_array[key][1]:
                    return self.serum_production_array[key][0]
                else:
                    random_serum_number -= self.serum_production_array[key][1] #Subtract the probability of this one from our number to make progress in our search.




        def player_production(self):
            production_amount = self.production_progress(mc.focus,mc.int,mc.production_skill)
            self.listener_system.fire_event("player_production", amount = production_amount)
            self.listener_system.fire_event("general_work")
            renpy.say("","You spend time in the lab synthesizing serum from the it's raw chemical precursors. You generate " + str(production_amount) + " production points.")
            return production_amount

        def player_hr(self):
            eff_amount = self.hr_progress(mc.charisma,mc.int,mc.hr_skill)
            self.listener_system.fire_event("player_efficiency_restore", amount = eff_amount)
            self.listener_system.fire_event("general_work")
            renpy.say("","You settle in and spend a few hours filling out paperwork, raising company efficency by " + str(eff_amount )+ "%%.")
            return eff_amount

        def hr_progress(self,cha,int,skill): #Don't compute efficency cap here so that player HR effort will be applied against any efficency drop even though it's run before the rest of the end of the turn.
            restore_amount = (3*cha) + (int) + (2*skill) + 5
            self.team_effectiveness += restore_amount
            return restore_amount

        def change_team_effectiveness(self, the_amount):
            self.team_effectiveness += the_amount
            if self.team_effectiveness > self.effectiveness_cap:
                self.team_effectiveness = self.effectiveness_cap
            elif self.team_effectiveness < 50:
                self.team_effectiveness = 50

        def add_employee_research(self, new_person):
            self.research_team.append(new_person)
            new_person.job = self.get_employee_title(new_person)

        def add_employee_production(self, new_person):
            self.production_team.append(new_person)
            new_person.job = self.get_employee_title(new_person)

        def add_employee_supply(self, new_person):
            self.supply_team.append(new_person)
            new_person.job = self.get_employee_title(new_person)

        def add_employee_marketing(self, new_person):
            self.market_team.append(new_person)
            new_person.job = self.get_employee_title(new_person)

        def add_employee_hr(self, new_person):
            self.hr_team.append(new_person)
            new_person.job = self.get_employee_title(new_person)

        def remove_employee(self, the_person, remove_linked = False):
            if the_person in self.research_team:
                self.research_team.remove(the_person)
            elif the_person in self.production_team:
                self.production_team.remove(the_person)
            elif the_person in self.supply_team:
                self.supply_team.remove(the_person)
            elif the_person in self.market_team:
                self.market_team.remove(the_person)
            elif the_person in self.hr_team:
                self.hr_team.remove(the_person)

            the_person.set_work(None)
            the_person.remove_role(employee_role, remove_linked = remove_linked) #Some events only shuffle employees around, leaving employee related roles in place. For those, set remove_linked to True

            #Roles can have an on_remove function, but these have special events that we want to make sure are triggered properly.
            if the_person == self.head_researcher:
                renpy.call("fire_head_researcher", the_person) #Call the label we use for firing the person as a role action. This should trigger it any time you fire or move your head researcher.

            if the_person == self.company_model:
                renpy.call("fire_model_label", the_person)

        def get_employee_list(self):
            return self.research_team + self.production_team + self.supply_team + self.market_team + self.hr_team

        def get_employee_count(self):
            return len(self.get_employee_list())

        def get_max_employee_slut(self):
            max = -1 #Set to -1 for an empty business, all calls should require at least sluttiness 0
            for person in self.get_employee_list():
                if person.sluttiness > max:
                    max = person.sluttiness
            return max

        def get_employee_title(self, the_person):
            if the_person in self.research_team:
                return "Researcher"

            elif the_person in self.market_team:
                return "Marketing"

            elif the_person in self.supply_team:
                return "Supply"

            elif the_person in self.production_team:
                return "Production"

            elif the_person in self.hr_team:
                return "Human Resources"
            else:
                return "None"

        def get_employee_workstation(self, the_person): #Returns the location a girl should be working at, or "None" if the girl does not work for you
            if the_person in self.research_team:
                return self.r_div

            elif the_person in self.market_team:
                return self.m_div

            elif the_person in self.supply_team:
                return self.s_div

            elif the_person in self.production_team:
                return self.p_div

            elif the_person in self.hr_team:
                return self.h_div
            else:
                return None

        def get_requirement_employee_list(self, exclude_list = None, **kargs): #Get a list of employees who pass the validrequirements. Pass the same arguments as person_meets_requirements expects as named args.
            employees_meeting_requirement = []
            if exclude_list is None:
                exclude_list = []
            for person in self.get_employee_list():
                if person not in exclude_list:
                    if person.person_meets_requirements(**kargs):
                        employees_meeting_requirement.append(person)
            return employees_meeting_requirement

        def give_daily_serum(self):
            if self.r_serum:
                the_serum = self.r_serum
                for person in self.research_team:
                    if self.inventory.get_serum_count(the_serum) > 0:
                        self.inventory.change_serum(the_serum,-1)
                        person.give_serum(copy.copy(the_serum), add_to_log = False) #use a copy rather than the main class, so we can modify and delete the effects without changing anything else.
                    else:
                        the_message = "Stockpile ran out of " + the_serum.name + " to give to the research division."
                        if not the_message in self.message_list:
                            self.add_normal_message(the_message)

            if self.m_serum:
                the_serum = self.m_serum
                for person in self.market_team:
                    if self.inventory.get_serum_count(the_serum) > 0:
                        self.inventory.change_serum(the_serum,-1)
                        person.give_serum(copy.copy(the_serum), add_to_log = False) #use a copy rather than the main class, so we can modify and delete the effects without changing anything else.
                    else:
                        the_message = "Stockpile ran out of " + the_serum.name + " to give to the marketing division."
                        if not the_message in self.message_list:
                            self.add_normal_message(the_message)

            if self.p_serum:
                the_serum = self.p_serum
                for person in self.production_team:
                    if self.inventory.get_serum_count(the_serum) > 0:
                        self.inventory.change_serum(the_serum,-1)
                        person.give_serum(copy.copy(the_serum), add_to_log = False) #use a copy rather than the main class, so we can modify and delete the effects without changing anything else.
                    else:
                        the_message = "Stockpile ran out of " + the_serum.name + " to give to the production division."
                        if not the_message in self.message_list:
                            self.add_normal_message(the_message)

            if self.s_serum:
                the_serum = self.s_serum
                for person in self.supply_team:
                    if self.inventory.get_serum_count(the_serum) > 0:
                        self.inventory.change_serum(the_serum,-1)
                        person.give_serum(copy.copy(the_serum), add_to_log = False) #use a copy rather than the main class, so we can modify and delete the effects without changing anything else.
                    else:
                        the_message = "Stockpile ran out of " + the_serum.name + " to give to the supply procurement division."
                        if not the_message in self.message_list:
                            self.add_normal_message(the_message)

            if self.h_serum:
                the_serum = self.h_serum
                for person in self.hr_team:
                    if self.inventory.get_serum_count(the_serum) > 0:
                        self.inventory.change_serum(the_serum,-1)
                        person.give_serum(copy.copy(the_serum), add_to_log = False) #use a copy rather than the main class, so we can modify and delete the effects without changing anything else.
                    else:
                        the_message = "Stockpile ran out of " + the_serum.name + " to give to the human resources division."
                        if not the_message in self.message_list:
                            self.add_normal_message(the_message)

        def advance_tutorial(self, tutorial_name):
            self.event_triggers_dict[tutorial_name] += 1 #advance our tutorial slot.

        def reset_tutorial(self, tutorial_name):
            self.event_triggers_dict[tutorial_name] = 1 #Reset it when the reset tutorial button is used.

        def add_sales_multiplier(self, multiplier_class, multiplier):
            mc.log_event("Serum sale value increased by " + str((multiplier - 1) * 100) + "% due to " + multiplier_class + ".", "float_text_grey")
            self.sales_multipliers.append([multiplier_class, multiplier])

        def remove_sales_multiplier(self, multiplier_class, multiplier):
            if [multiplier_class, multiplier] in self.sales_multipliers:
                mc.log_event("No longer reciving " + str((multiplier - 1) * 100) + "% serum value increase from " + multiplier_class + ".", "float_text_grey")
                self.sales_multipliers.remove([multiplier_class, multiplier])

    class SerumDesign(renpy.store.object): #A class that represents a design for a serum built up from serum traits.
        def __init__(self):
            self.name = ""
            self.traits = []
            self.side_effects = []

            self.researched = False
            self.obsolete = False
            self.current_research = 0

            self.research_needed = 0
            self.slots = 0
            self.value = 0
            self.production_cost = 0

            self.duration = 0
            self.duration_counter = 0

            self.expires = True #If set to false the serum does not tick up the duration_counter, meaning it will never expire.

        def reset(self): #Resets the serum to the default serum values.
            self.__init__()

        def has_tag(self, the_tag): #Returns true if at least one of the traits has the tag "the_tag". Used to confirm a production trait is included.
            for trait in self.traits:
                if the_tag in trait.exclude_tags:
                    return True
            return False

        def add_trait(self, the_trait, is_side_effect = False): #Used when the serum is being built in the serum designer.
            if the_trait not in self.traits or the_trait not in self.side_effects:
                if is_side_effect:
                    self.side_effects.append(the_trait)
                else:
                    self.traits.append(the_trait) #Add the trait to the serums list of traits.

                #Add the trait effects on the core develpment stats of the serum.
                self.research_needed += the_trait.research_added
                self.value += the_trait.value_added
                self.slots += the_trait.slots
                self.production_cost += the_trait.production_cost
                self.duration += the_trait.duration

        def remove_trait(self, the_trait): #Used when the serum is being built in the serum designer.
            if the_trait in self.traits or the_trait in self.side_effects:
                if the_trait in self.traits:
                    self.traits.remove(the_trait) #Remove the trait from our list of traits.
                else:
                    self.side_effects.remove(the_trait)

                #Remove the trait effects on the core development stats of the serum.
                self.research_needed += -the_trait.research_added
                self.value += -the_trait.value_added
                self.slots += -the_trait.slots
                self.production_cost += -the_trait.production_cost
                self.duration += -the_trait.duration

        def duration_expired(self): #Returns true if the serum has expired (ie. duration counter equal to or over duration.).
            if self.duration_counter >= self.duration:
                return True #Returns true when it has expired
            else:
                return False #Returns false when there is more time to go

        def run_on_turn(self,the_person): #Increases the counter, applies serum effect if there is still some duration left
            if self.duration_counter < self.duration:
                for trait in self.traits + self.side_effects:
                    trait.run_on_turn(the_person)
            if self.expires:
                self.duration_counter += 1

        def run_on_apply(self, the_person):
            for trait in self.traits + self.side_effects:
                trait.run_on_apply(the_person)

        def run_on_remove(self, the_person):
            for trait in self.traits + self.side_effects:
                trait.run_on_remove(the_person)

        def run_on_day(self, the_person):
            for trait in self.traits + self.side_effects:
                trait.run_on_day(the_person)

        def add_research(self, amount): #Returns true if "amount" research completes the research
            self.current_research += amount
            if self.current_research >= self.research_needed:
                self.researched = True
                return True
            else:
                return False

        def generate_side_effects(self): #Called when a serum is finished development. Tests all traits against their side effect chance and adds an effect for any that fail.
            for trait in self.traits:
                if trait.test_effective_side_effect_chance():
                    the_side_effect = get_random_from_list(list_of_side_effects)
                    self.add_trait(the_side_effect, is_side_effect = True)
                    mc.log_event(self.name + " developed side effect " + the_side_effect.name + " due to " + trait.name, "float_text_blue")

        def build_positive_slug(self):
            the_slug = ""
            traits_with_slugs = []
            for trait in self.traits + self.side_effects:
                if trait.positive_slug is not None and trait.positive_slug != "":
                    traits_with_slugs.append(trait)

            for trait in traits_with_slugs:
                the_slug += trait.positive_slug
                if trait is not traits_with_slugs[-1]: #If it isn't the last element.
                        the_slug += ", " #This gets us a nice formatted string in the form A, B, C, D.

        def build_negative_slug(self):
            the_slug = ""
            traits_with_slugs = []
            for trait in self.traits + self.side_effects:
                if trait.negative_slug is not None and trait.negative_slug != "":
                    traits_with_slugs.append(trait)

            for trait in traits_with_slugs:
                the_slug += trait.negative_slug
                if trait is not traits_with_slugs[-1]: #If it isn't the last element.
                        the_slug += ", " #This gets us a nice formatted string in the form A, B, C, D.



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


    class SerumTrait(renpy.store.object):
        def __init__(self,name,desc, positive_slug = "", negative_slug = "", value_added = 0, research_added = 0, slots_added = 0, production_added = 0, duration_added = 0, base_side_effect_chance = 0, on_apply = None, on_remove = None, on_turn = None, on_day = None ,requires= None, tier = 0, start_researched=False,research_needed=50,exclude_tags=None, is_side_effect = False): #effect is a function that takes a serumDesign as a parameter and modifies it based on whatever effect this trait has.

            self.name = name
            self.desc = desc #A fluff text description.
            self.positive_slug = positive_slug #A short numerical list of positive effects
            self.negative_slug = negative_slug #The negative costs

            self.value_added = value_added
            self.research_added = research_added
            self.slots = slots_added
            self.production_cost = production_added
            self.duration = duration_added
            self.base_side_effect_chance = base_side_effect_chance #A percentage chance that this trait will introduce a side effect to the finished design.
            self.mastery_level = 1.0 #The amount of experience the MC has with this serum. Divide base side effect chance by mastery level to get effective side effect chance.


            self.on_apply = on_apply #The function applied to the person when the serum is first applied.
            self.on_remove = on_remove #The function applied to the person when the serum is removed (it should generally undo the on_apply effects)
            self.on_turn = on_turn #The function applied to the person at the end of a turn under the effect of the serum.
            self.on_day = on_day #The function applied to the person at the end of the day.


            if requires is None: #A list of other traits that must be researched before this.
                self.requires = []
            elif isinstance(requires, list):
                self.requires = requires
            else:
                self.requires = [requires]

            self.tier = tier #The tier of research that the business must have unlocked to research this, in addition to the other prerequisits.
            self.researched = start_researched
            self.research_needed = research_needed
            self.current_research = 0

            if exclude_tags is None:#A list of tags (strings) that this trait cannot be paired with. If a trait has the same excluded tag this cannot be added to a trait.
                self.exclude_tags = []
            elif isinstance(exclude_tags, list):
                self.exclude_tags = exclude_tags
            else:
                self.exclude_tags = [exclude_tags]

            self.is_side_effect = is_side_effect #If true this trait is a side effect and not counted towards serum max traits and such. It also cannot be added to a serum on purpose.


        def run_on_apply(self, the_person, add_to_log = True):
            if self.on_apply is not None:
                self.on_apply(the_person, add_to_log)

        def run_on_remove(self, the_person, add_to_log = False):
            if self.on_remove is not None:
                self.on_remove(the_person, add_to_log)

        def run_on_turn(self, the_person, add_to_log = False):
            if self.on_turn is not None:
                self.on_turn(the_person, add_to_log)

        def run_on_day(self, the_person, add_to_log = False):
            if self.on_day is not None:
                self.on_day(the_person, add_to_log)

        def add_research(self, amount):
            self.current_research += amount
            if self.current_research >= self.research_needed:
                if self.researched:
                    while (self.current_research >= self.research_needed): #For large businesses when the research produced is much larger than the total research needed you can gain multiple levels.
                        self.add_mastery(0.5)
                        self.current_research += -self.research_needed
                else:
                    self.current_research += -self.research_needed
                self.researched = True

                return True
            else:
                return False

        def add_mastery(self, amount):
            self.mastery_level += amount

        def get_effective_side_effect_chance(self): #Generates the effective side effect chance percent as an integer.
            the_chance = self.base_side_effect_chance/self.mastery_level
            return __builtin__.int(the_chance)

        def test_effective_side_effect_chance(self): #Gets the effective side effect chance and tests it against a random 1 to 100 roll
            the_chance = self.get_effective_side_effect_chance()
            the_roll = renpy.random.randint(0,100)
            if the_roll < the_chance:
                return True
            else:
                return False

        def build_negative_slug(self):
            if self.is_side_effect:
                return self.negative_slug #For side effects we do not want to display the side effect chance as a negative modifier.
            else:
                if self.get_effective_side_effect_chance() >= 10000:
                    return self.negative_slug + ", Guaranteed Side Effect"
                else:
                    return self.negative_slug + ", " + str(self.get_effective_side_effect_chance()) + "% Chance of Side Effect"

        def has_required(self):
            has_prereqs = True
            for trait in self.requires:
                if not trait.researched:
                    has_prereqs = False
            if self.tier > mc.business.research_tier:
                has_prereqs = False
            return has_prereqs

    class Infraction(renpy.store.object):
        #These are common infractions that may be used throughout the game
        @staticmethod
        def bureaucratic_mistake_factory(name = "Bureaucratic Mistake", desc = None, severity = 1, days_valid = 3):
            if desc is None:
                desc = "Failure to dot all i's and cross all t's. It's impossible to do anything right here!"
            return Infraction(name, desc, severity, days_valid)

        @staticmethod
        def underperformance_factory(name = "Underperformance", desc = None, severity = 1, days_valid = 7):
            if desc is None:
                desc = "Work performance lower than expected of the employee."
            return Infraction(name, desc, severity, days_valid)

        @staticmethod
        def careless_accident_factory(name = "Careless Accident", desc = None, severity = 2, days_valid = 7):
            if desc is None:
                desc = "Damage to company equipment or waste of company supplies due to a careless mistake."
            return Infraction(name, desc, severity, days_valid)

        @staticmethod
        def office_disturbance_factory(name = "Workplace Disturbance", desc = None, severity = 2, days_valid = 7):
            if desc is None:
                desc = "Actions that have upset the normal peace and quiet of the office."
            return Infraction(name, desc, severity, days_valid)

        @staticmethod
        def out_of_uniform_factory(name = "Out of Uniform", desc = None, severity = 3, days_valid = 7):
            if desc is None:
                desc = "Failure to wear a company mandated uniform."
            return Infraction(name, desc, severity, days_valid)

        @staticmethod
        def disobedience_factory(name = "Disobedience", desc = None, severity = 3, days_valid = 7):
            if desc is None: #Not in the parameters to keep things a little tidier.
                desc = "Intentional disregard of a direct order order or instruction."
            return Infraction(name, desc, severity, days_valid)

        @staticmethod
        def inappropriate_behaviour_factory(name = "Inappropriate Behaviour", desc = None, severity = 3, days_valid = 7):
            if desc is None:
                desc = "Actions inappropriate for a workplace setting. Strange how this never applies to the owner..."
            return Infraction(name, desc, severity, days_valid)

        def __init__(self, name, desc, severity, days_valid, days_existed = 0):
            self.name = name #The name of the infraction, as might show up on a menu
            self.desc = desc #A short, two or three sentence explanation for what the infraction is, for tooltip purposes.
            self.severity = severity #An int from 1 (least severe) to 5 (most severe). Punishments are gated by the severity of the infraciton
            if strict_enforcement.is_active():
                self.severity += 1
            if draconian_enforcement.is_active():
                self.severity += 1

            self.days_valid = days_valid #How many days from the creation of the infraction it is valid to punish someone for
            self.days_existed = days_existed #How long this infraction has existed on someone.

    class MainCharacter(renpy.store.object):
        def __init__(self, location, name, last_name, business, stat_array, skill_array, sex_array):
            self.location = location
            self.name = name
            self.last_name = last_name
            self.energy = 50
            self.designed_wardrobe = Wardrobe("Designed Wardrobe")
            self.money = 100 ## Personal money that can be spent however you wish. Company funds are seperate (but can be manipulated in your favour)
            self.business = business
            self.inventory = SerumInventory([])

            ##Mental stats##
            #Mental stats are generally fixed and cannot be changed permanently.
            self.charisma = stat_array[0]#How likeable the person is. Mainly influences marketing, also determines how well interactions with other characters go. Main stat for HR and sales
            self.int = stat_array[1] #How smart the person is. Mainly influences research, small bonuses to most tasks. #Main stat for research and production.
            self.focus = stat_array[2]#How on task the person stays. Influences most tasks slightly. #Main stat for supplies

            ##Work Skills##
            #Skills can be trained up over time, but are limited by your raw stats.
            self.hr_skill = skill_array[0]
            self.market_skill = skill_array[1]
            self.research_skill = skill_array[2]
            self.production_skill = skill_array[3]
            self.supply_skill = skill_array[4]

            ##Sex Stats##
            # These are phyical stats about the character that impact how they behave in a sex scene. Future values might include penis size or sensitivity.
            self.arousal = 0 #How close to an orgasm you are. You cum when you reawch your max_arousal, default 100.
            self.max_arousal = 100



            ##Sex Skills##
            # These skill represent your knowledge and experience with different types of intimacy. Useful for raising a girls arousal faster than your own.
            self.sex_skills = {}
            self.sex_skills["Foreplay"] = sex_array[0] # A catch all for everything that goes on before blowjobs, sex, etc. Includes things like kissing, massages, etc.
            self.sex_skills["Oral"] = sex_array[1] # Your skill at eating a girl out.
            self.sex_skills["Vaginal"] = sex_array[2] # Your skill at different positions that involve vaginal sex.
            self.sex_skills["Anal"] = sex_array[3] # Your skill skill at different positions that involve anal sex.
            #
            # self.max_stamina = 2 # How many times you can seduce someone each day
            # self.current_stamina = 2 # Current stamina.

            self.max_energy = 100 #Your physical energy. Mainly consumed by having sex, slowly comes back during the day (with some actions speeding this up), and a lot of it returns at the end of the day
            self.energy = self.max_energy

            self.main_character_actions = [] # A list of actions enabld for the main character when they talk to people. Kind of like a "role" for the MC.

            self.condom = False #True if you currently have a condom on. (maintained by sex scenes). TODO: Allow a third "broken" state and add dialgoue and descriptions for that.
            self.recently_orgasmed = False #If True you recently orgasmsed and aren't hard until your arousal rises to 10 or the encounter ends.

            self.known_home_locations = [] #When the MC learns a character's home location the room reference should be added here. They can then get to it from the map.

            self.having_text_conversation = None #Set to a Person when dialogue should be taking place on the phone. Logs dialogue (but not narration) as appropriate.
            self.text_conversation_paused = False #Shows the say window as normal for all dialogue with the phone display underneath if having_text_conversation is set to a Person

            self.phone = Text_Message_Manager()

            self.listener_system = Listener_Management_System() #A listener manager to let us enroll to events and update goals when they are triggered.

            #How many free points does the main character have to spend on their skills/abilities
            self.free_stat_points = 0
            self.free_work_points = 0
            self.free_sex_points = 0

            #The maximum score you can have in each of the major skill catagories
            self.max_stats = 8
            self.max_work_skills = 8
            self.max_sex_skills = 8
            self.max_energy_cap = 200

            #The current goals set for the player to achieve. On completion they gain 1 point towards that class of skills
            self.stat_goal = None
            self.work_goal = None
            self.sex_goal = None

            #The difficulty of goals. Some goals will be removed once the difficulty is highe enough, others will be added, and some will have completion requirements based on the difficulty.
            self.stat_goal_difficulty = 0
            self.work_goal_difficulty = 0
            self.sex_goal_difficulty = 0

            self.log_items = [] #A list of items to display as a log. is a tuple of: [string_to_display, text_style, unix_time]
            self.log_max_size = 20

            self.scrap_goal_available = True

            self.can_skip_time = False #A flag used to determine when it is safe to skip time and when it is not. Left in as of v0.19.0 to ensure missed references do not cause a crash; has no function.

        def change_location(self,new_location): #TODO: Check if we can add the "show_background" command for our new location here. Is there any time where we want to be in a location but _not_ show it's background?
            self.location = new_location

        def use_energy(self,amount):
            self.energy = self.energy - amount
            if self.energy < 0:
                self.energy = 0

        def change_arousal(self,amount):
            self.arousal += amount
            if self.arousal < 0:
                self.arousal = 0

        def reset_arousal(self):
            self.arousal = 0

        def change_energy(self, amount, add_to_log = True):
            amount = __builtin__.round(amount)
            self.energy += amount
            if self.energy > self.max_energy:
                self.energy = self.max_energy
            elif self.energy < 0:
                self.energy = 0

            log_string = ""
            if amount  > 0:
                log_string += "You: +" + str(amount)  + " Energy"
            else:
                log_string += "You: " + str(amount)  + " Energy"
            if add_to_log and amount != 0:
                mc.log_event(log_string, "float_text_yellow")
            return

        def change_max_energy(self, amount ,add_to_log = True):
            amount = __builtin__.round(amount)
            self.max_energy += amount
            if self.max_energy < 0:
                self.max_energy = 0

            if self.energy > self.max_energy: #No having more energy than max in case we lower max
                self.energy = self.max_energy

            log_string = ""
            if amount > 0:
                log_string += "You: +" + str(amount) + " Max Energy"
            else:
                log_string += "You: " + str(amount) + " Max Energy"
            if add_to_log and amount != 0:
                mc.log_event(log_string, "float_text_yellow")
            return

        def save_design(self, the_outfit, new_name, outfit_type = "full"):
            the_outfit.name = new_name
            if outfit_type == "under":
                self.designed_wardrobe.add_underwear_set(the_outfit)
            elif outfit_type == "over":
                self.designed_wardrobe.add_overwear_set(the_outfit)
            else: #Generally outfit_type == full, or some other uncaught error.
                self.designed_wardrobe.add_outfit(the_outfit)

        def is_at_work(self): #Checks to see if the main character is at work, generally used in crisis checks.
            if self.location == self.business.m_div or self.location == self.business.p_div or self.location == self.business.r_div or self.location == self.business.s_div or self.location == self.business.h_div:
                return True
            else:
                return False

        def run_turn(self):
            self.listener_system.fire_event("time_advance")
            self.change_arousal(-20)
            self.change_energy(20)
            return

        def run_day(self):
            self.listener_system.fire_event("end_of_day")
            self.change_energy(60)
            self.reset_arousal()
            self.scrap_goal_available = True

        def complete_goal(self, the_finished_goal):
            if the_finished_goal == self.stat_goal:
                self.free_stat_points += 1 #The player gets some new points to spend
                self.stat_goal_difficulty += 1 #Future goals become more difficult
                self.stat_goal = create_new_stat_goal(self.stat_goal_difficulty) #Generate a new goal

            elif the_finished_goal == self.work_goal:
                self.free_work_points += 1
                self.work_goal_difficulty += 1
                self.work_goal = create_new_work_goal(self.work_goal_difficulty)

            elif the_finished_goal == self.sex_goal:
                self.free_sex_points += 1
                self.sex_goal_difficulty += 1
                self.sex_goal = create_new_sex_goal(self.sex_goal_difficulty)

        def scrap_goal(self, the_finished_goal):
            if the_finished_goal == self.stat_goal:
                self.stat_goal = create_new_stat_goal(self.stat_goal_difficulty) #Generate a new goal

            elif the_finished_goal == self.work_goal:
                self.work_goal = create_new_work_goal(self.work_goal_difficulty)

            elif the_finished_goal == self.sex_goal:
                self.sex_goal = create_new_sex_goal(self.sex_goal_difficulty)

            self.scrap_goal_available = False

        def generate_goals(self):
            self.stat_goal = create_new_stat_goal(self.stat_goal_difficulty)
            self.work_goal = create_new_work_goal(self.work_goal_difficulty)
            self.sex_goal = create_new_sex_goal(self.sex_goal_difficulty)

        def improve_stat(self, stat_string, amount = 1):
            if amount > self.free_stat_points:
                amount = self.free_stat_points
            if stat_string == "int":
                self.int += amount
            elif stat_string == "cha":
                self.charisma += amount
            elif stat_string == "foc":
                self.focus += amount

            self.free_stat_points += -amount

        def improve_work_skill(self, skill_string, amount = 1):
            if amount > self.free_work_points:
                amount = self.free_work_points

            if skill_string == "hr":
                self.hr_skill += amount
            elif skill_string == "market":
                self.market_skill += amount
            elif skill_string == "research":
                self.research_skill += amount
            elif skill_string == "production":
                self.production_skill += amount
            elif skill_string == "supply":
                self.supply_skill += amount

            self.free_work_points += -amount

        def improve_sex_skill(self, sex_string, amount = 1):
            if amount > self.free_sex_points:
                amount = self.free_sex_points

            if sex_string in self.sex_skills:
                self.sex_skills[sex_string] += amount
            elif sex_string == "stam":
                self.energy += amount * 20
                self.max_energy += amount * 20

            self.free_sex_points += -amount


        def log_event(self, the_text, the_text_style):
            if the_text is None: # Make sure we're not passing None items accidentily, which could cause crashes for the main hud.
                the_text = "???"
            if the_text_style is None:
                the_text_style = "float_text_grey"

            event_tuple = (the_text, the_text_style, time.time()) #Stores the unix time the event was added so we can run a little animation.
            self.log_items.insert(0,event_tuple)
            while len(self.log_items) > self.log_max_size:
                self.log_items.pop() #Pop off extra items until we are down to size.

        def start_text_convo(self, the_person): #Triggers all the appropriate variables so say entries will go into the phone text log.
            self.having_text_conversation = the_person
            self.text_conversation_paused = False

            # renpy.show_screen("text_message_log", the_person)
            return

        def end_text_convo(self): #Resets all triggers from texting someone, so say messages are displayed properly again, ect.
            self.having_text_conversation = None
            self.text_conversation_paused = False

            # renpy.hide_screen("text_message_log")
            return

        def pause_text_convo(self): #Keeps the phone UI and display up, but your dialogue and dialogue from any girl other than the one you're texting will display as normal and not be logged.
            self.text_conversation_paused = True #TODO: We no longer need to give characters a specific phone font, because it all goes right into the phone log itself. Otherwise this breaks the MC dialogue.
            return

        def resume_text_convo(self): #Start hiding the phone UI again. Use after you have paused a text convo
            self.text_conversation_paused = False
            return

        def log_text_message(self, the_person, the_message):
            #TODO: Allow you to insert arbitrary messages by building history entries here! Use this for a narrator sytle "[Sent a picture]"!
            return


    class Person(renpy.store.object): #Everything that needs to be known about a person.
        global_character_number = 0 #This is increased for each character that is created.

        def __init__(self,name,last_name,age,body_type,tits,height,body_images,expression_images,hair_colour,hair_style,pubes_colour,pubes_style,skin,eyes,job,wardrobe,personality,stat_list,skill_list,
            sluttiness=0,obedience=0,suggest=0,sex_list=[0,0,0,0], love = 0, happiness = 100, home = None, work = None,
            font = "Avara.tff", name_color = "#ffffff", dialogue_color = "#ffffff",
            face_style = "Face_1",
            special_role = None,
            title = None, possessive_title = None, mc_title = None,
            relationship = None, SO_name = None, kids = None, base_outfit = None,
            generate_insta = False, generate_dikdok = False, generate_onlyfans = False):

            ## Personality stuff, name, ect. Non-physical stuff.
            self.name = name
            self.last_name = last_name
            self.character_number = Person.global_character_number #This is a gunique number for each character. Used as a tag when showing a character to identify if they are already drawn (and thus need to be hidden)
            Person.global_character_number += 1

            self.draw_number = defaultdict(int) #Used while drawing a character to avoid drawing an animation that has already been replaced with a new draw. Defaults to 0

            self.title = title #Note: We format these down below!
            self.possessive_title = possessive_title #The way the girl is refered to in relation to you. For example "your sister", "your head researcher", or just their title again.
            if mc_title:
                self.mc_title = mc_title #What they call the main character. Ie. "first name", "mr.last name", "master", "sir".
            else:
                self.mc_title = "Stranger"

            self.home = home #The room the character goes to at night. If none a ranjdom public location is picked.
            self.work = work #The room the character goes to for work.
            self.schedule = {}
            for x in range(0,7):
                self.schedule[x] = {0:home,1:None,2:None,3:None,4:home}
            #If there is a place in the schedule the character will go there. Otherwise they have free time and will do whatever they want.
            self.job = job

            # Relationship and family stuff
            if relationship:
                self.relationship = relationship
            else:
                self.relationship = "Single" #Should be Single, Girlfriend, Fiancée, or Married.

            if SO_name:
                self.SO_name = SO_name
            else:
                self.SO_name = None #If not single, name of their SO (for guilt purposes or future events).

            if kids:
                self.kids = kids
            else:
                self.kids = 0


            self.personality = personality


            # Loves, likes, dislikes, and hates determine some reactions in conversations, options, etc. Some are just fluff.
            self.opinions = {} #Key is the name of the opinion (see random list), value is a list holding [value, known]. Value ranges from -2 to 2 going from hate to love (things not on the list are assumed 0). Known is a bool saying if the player knows about their opinion.

            self.sexy_opinions = {}
            # We establish random opinions first and will overwrite any that conflict with generated personality opinions.
            for x in __builtin__.range(1,5):
                the_opinion_key = get_random_opinion()
                degree = renpy.random.randint(-2,2)
                if not degree == 0: #ie. ignore 0 value opinions.
                    self.opinions[the_opinion_key] = [degree, False]

            for x in __builtin__.range(1,2):
                the_opinion_key = get_random_sexy_opinion()
                degree = renpy.random.randint(-2,2)
                if not degree == 0: #ie. ignore 0 value opinions.
                    self.sexy_opinions[the_opinion_key] = [degree, False]

            #Now we get our more likely default personality ones.
            for x in __builtin__.range(1,4):
                the_opinion_key, opinion_list = self.personality.generate_default_opinion()
                if the_opinion_key:
                    self.opinions[the_opinion_key] = opinion_list

            for x in __builtin__.range(1,3):
                the_opinion_key, opinion_list = self.personality.generate_default_sexy_opinion()
                if the_opinion_key:
                    self.sexy_opinions[the_opinion_key] = opinion_list



            #TODO: Relationship with other people (List of known people plus relationship with them.)

            #Using char instead of a string lets us customize the font and colour we are using for the character.
            self.char = Character("???", #The name to be displayed above the dialogue.
                what_font = font, #The font to be used for the character.
                who_font = font,
                color = name_color, #The colour of the character's NAME section
                what_color = dialogue_color, #The colour of the character's dialogue.
                what_style = "general_dialogue_style") #Used to describe everything that isn't character specific.

            if title: #Format the given titles, if any, so they appear correctly the first time you meet at person.
                self.set_title(title) #The way the girl is refered to by the MC. For example: "Mrs. Whatever", "Lily", or "Mom". Will reset "???" if appropriate
            else:
                self.char.name = self.create_formatted_title("???")
            if possessive_title:
                self.set_possessive_title(possessive_title)

            self.text_modifiers = [] #A list of functions, each of which take Person, String and return a modified String. Used to modify text to dynamically highlight words, or reflect a speech difference.

            ## Physical things.
            self.age = age
            self.body_type = body_type
            self.tits = tits
            self.height = height * 0.8 #This is the scale factor for height, with the talest girl being 1.0 and the shortest being 0.8
            self.body_images = body_images #instance of Clothing class, which uses full body shots.
            self.face_style = face_style
            self.expression_images = expression_images #instance of the Expression class, which stores facial expressions for different skin colours
            self.hair_colour = hair_colour #A list of [description, color value], where colour value is a standard RGBA list.
            self.hair_style = hair_style

            if pubes_colour is None:
                self.pubes_colour = get_darkened_colour(hair_colour[1], 0.07) #Unless otherwise specifified they are 10% darker than normal hair
            else:
                self.pubes_colour = pubes_colour #generally hair colour but a little darker.

            if pubes_style is None:
                self.pubes_style = shaved_pubes #An empty image place holder so we can always call on them to draw.
            else:
                self.pubes_style = pubes_style


            self.skin = skin
            self.eyes = eyes #A list of [description, color value], where colour value is a standard RGBA list.
            #TODO: Tattoos eventually
            #TODO: a "mandatory" or "default" set of accessories that characters will always wear. Do as a third "personal_effects" outfit that they always merge in if possible?

            self.serum_effects = [] #A list of all of the serums we are under the effect of.

            if not special_role:  #Characters may have a special role that unlocks additional actions. By default this is an empty list.
                self.special_role = []
            elif isinstance(special_role, Role):
                self.special_role = [special_role] #Support handing a non-list special role, in case we forget to wrap it in a list one day.
            elif isinstance(special_role, list):
                self.special_role = special_role #Otherwise we've handed it a list
            else:
                self.special_role = []
                log_message("Person \"" + name + " " + last_name + "\" was handed an incorrect special role parameter.")


            self.on_room_enter_event_list = [] #Checked when you enter a room with this character. If an event is in this list and enabled it is run (and no other event is until the room is reentered)
                # If handed a list of [action, positive_int], the integer is how many turns this action is kept around before being removed, triggered or not.
            self.on_talk_event_list = [] #Checked when you start to interact with a character. If an event is in this list and enabled it is run (and no other event is until you talk to the character again.)\
                # If handed a list of [action, positive_int], the integer is how many turns this action is kept around before being removed, triggered or not.

            self.event_triggers_dict = {} #A dict used to store extra parameters used by events, like how many days has it been since a performance review.
            self.event_triggers_dict["employed_since"] = 0

            ##Mental stats##
            #Mental stats are generally fixed and cannot be changed permanently. Ranges from 1 to 5 at start, can go up or down (min 0)
            self.charisma = stat_list[0] #How likeable the person is. Mainly influences marketing, also determines how well interactions with other characters go. Main stat for HR and sales
            self.int = stat_list[1] #How smart the person is. Mainly influences research, small bonuses to most tasks. #Main stat for research and production.
            self.focus = stat_list[2] #How on task the person stays. Influences most tasks slightly. #Main stat for supplies

            self.charisma_debt = 0 #Tracks how far into the negative a characters stats are, for the purposes of serum effects. Effective stats are never lower than 0.
            self.int_debt = 0
            self.focus_debt = 0

            ##Work Skills##
            #Skills can be trained up over time, but are limited by your raw stats. Ranges from 1 to 5 at start, can go up or down (min 0)
            self.hr_skill = skill_list[0]
            self.market_skill = skill_list[1]
            self.research_skill = skill_list[2]
            self.production_skill = skill_list[3]
            self.supply_skill = skill_list[4]

            self.max_energy = 100
            self.energy = self.max_energy

            self.salary = self.calculate_base_salary()

            # self.employed_since = 0 #Default this to 0, it will almost always be overwritten but in case it sneaks through this makes sure that nothing breaks.

            self.idle_pose = get_random_from_list(["stand2","stand3","stand4","stand5"]) #Get a random idle pose that you will use while people are talking to you.
            self.idle_animation = idle_wiggle_animation #If we support animation we use this to jiggle their tits and ass just a little to give the screen some movement.
            #self.idle_animation.innate_animation_strength += 0.05 * rank_tits(self.tits) # Larger tits swing more #TODO: Implement region specific weighting.

            self.personal_region_modifiers = {"breasts":0.1+0.1 * rank_tits(self.tits)} #A dict that stores information about modifiers that should be used for specific regions of animations. Default is 1.

            ##Personality Stats##
            #Things like sugestability, that change over the course of the game when the player interacts with the girl
            self.suggestibility = 0 + suggest #How quickly/efficently bleeding temporary sluttiness is turned into core sluttiness.
            self.suggest_bag = [] #This will store a list of ints which are the different suggestion values fighting for control. Only the highest is used, maintained when serums are added and removed.

            self.happiness = happiness #Higher happiness makes a girl less likely to quit and more willing to put up with you pushing her using obedience.
            self.love = love
            self.sluttiness = 0 + sluttiness #How slutty the girl is by default. Higher will have her doing more things just because she wants to or you asked.
            self.core_sluttiness = self.sluttiness #Core sluttiness is the base level of what a girl considers normal. normal "sluttiness" is the more variable version, technically refered to as "temporary slutiness".
            self.obedience = 100 + obedience #How likely the girl is to listen to commands. Default is 100 (normal person), lower actively resists commands, higher follows them.

            #Situational modifiers are handled by events. These dicts and related functions provide a convenient way to avoid double contributions. Remember to clear your situational modifiers when you're done with them!!
            self.situational_sluttiness = {} #A dict that stores a "situation" string and the corrisponding amount it is contributing to the girls sluttiness.
            self.situational_obedience = {} #A dict that stores a "situation" string and a corrisponding amount that it has affected their obedience by.

            ##Sex Stats##
            #These are physical stats about the girl that impact how she behaves in a sex scene. Future values might include things like breast sensitivity, pussy tighness, etc.
            self.arousal = 0 #How actively horny a girl is, and how close she is to orgasm.
            self.max_arousal = 100 #Her maximum arousal. TODO: Keep this hidden until you make her cum the first time?

            ##Sex Skills##
            #These represent how skilled a girl is at different kinds of intimacy, ranging from kissing to anal. The higher the skill the closer she'll be able to bring you to orgasm (whether you like it or not!)
            self.sex_skills = {}
            self.sex_skills["Foreplay"] = sex_list[0] #A catch all for everything that goes on before blowjobs, sex, etc. Includes things like kissing and strip teases.
            self.sex_skills["Oral"] = sex_list[1] #The girls skill at giving head.
            self.sex_skills["Vaginal"] = sex_list[2] #The girls skill at different positions that involve vaginal sex.
            self.sex_skills["Anal"] = sex_list[3] #The girls skill at different positions that involve anal sex.

            self.sex_record = {}
            self.sex_record["Handjobs"] = 0
            self.sex_record["Blowjobs"] = 0
            self.sex_record["Cunnilingus"] = 0
            self.sex_record["Tit Fucks"] = 0
            self.sex_record["Vaginal Sex"] = 0
            self.sex_record["Anal Sex"] = 0
            self.sex_record["Cum Facials"] = 0
            self.sex_record["Cum in Mouth"] = 0
            self.sex_record["Cum Covered"] = 0
            self.sex_record["Vaginal Creampies"] = 0
            self.sex_record["Anal Creampies"] = 0

            self.broken_taboos = [] #Taboos apply a penalty to the _first_ time you are trying to push some boundry (first time touching her pussy, first time seeing her tits, etc.), and trigger special dialogue when broken.

            bc_chance = 100 - (self.age + (self.get_opinion_score("bareback sex")*15))
            if persistent.pregnancy_pref == 2 and renpy.random.randint(0,100) > bc_chance:
                self.on_birth_control = False #If this character is on birth control or not. Note that this may be overridden by a game wide setting preventing pregnancy. (and on other settings may not be 100% effective)
            else:
                self.on_birth_control = True
            self.bc_penalty = 0 #Lowers the chance of birht control preventing a pregnancy. (Default is 100% if predictable or 90% if realistic). #TODO: Add serum traits that affect this.
            self.fertility_percent = 20.0 - ((self.age-18.0)/3.0) #The chance, per creampie, that a girl gets pregnant.
            self.ideal_fertile_day = renpy.random.randint(0,30) #Influences a girls fertility chance. It is double on the exact day of the month, dropping down to half 15 days before/after. Only applies on realistic setting.

            self.lactation_sources = 0 #How many things are causing this girl to lactate. Mainly serum traits, side effects, or pregnancy.

            ## Clothing things.
            self.wardrobe = copy.copy(wardrobe) #Note: we overwrote default copy behaviour for wardrobes so they do not have any interference issues with eachother.
            if base_outfit is None:
                self.base_outfit = Outfit(name + "'s Base Outfit")
            else:
                self.base_outfit = base_outfit


            self.infractions = [] #List of infractions this character has committed.

            self.planned_outfit = self.wardrobe.decide_on_outfit(self.sluttiness) #planned_outfit is the outfit the girl plans to wear today while not at work. She will change back into it after work or if she gets stripped. Cop0y it in case the outfit is changed during the day.
            self.planned_uniform = None #The uniform the person was planning on wearing for today, so they can return to it if they need to while at work.
            self.apply_outfit(self.planned_outfit)


            ## Internet things ##
            if generate_insta: #NOTE: By default all of these are not visible to the player.
                self.special_role.append(instapic_role)
            if generate_dikdok:
                self.special_role.append(dikdok_role)
            if generate_onlyfans:
                self.special_role.append(onlyfans_role)

            ## Conversation things##
            self.sexed_count = 0


        def generate_home(self, set_home_time = True): #Creates a home location for this person and adds it to the master list of locations so their turns are processed.
            if self.home is None:
                start_home = Room(self.name+"'s home", self.name+"'s home", [], standard_bedroom_backgrounds[:], [],[],[],False,[0.5,0.5], visible = False, hide_in_known_house_map = False, lighting_conditions = standard_indoor_lighting)
                #start_home.link_locations_two_way(downtown)

                start_home.add_object(make_wall())
                start_home.add_object(make_floor())
                start_home.add_object(make_bed())
                start_home.add_object(make_window())

                self.home = start_home
                if set_home_time:
                    self.set_schedule(start_home, times = [0,4])
                list_of_places.append(start_home)
            return self.home

        def generate_daughter(self, force_live_at_home = False): #Generates a random person who shares a number of similarities to the mother
            age = renpy.random.randint(18, self.age-16)

            if renpy.random.randint(0,100) < 60:
                body_type = self.body_type
            else:
                body_type = None

            if renpy.random.randint(0,100) < 40: #Slightly lower for facial similarities to keep characters looking distinct
                face_style = self.face_style
            else:
                face_style = None

            if renpy.random.randint(0,100) < 60: #60% of the time they share hair colour
                hair_colour = self.hair_colour
            else:
                hair_colour = None

            if renpy.random.randint(0,100) < 60: # 60% they share the same breast size
                tits = self.tits
            else:
                tits = None

            if renpy.random.randint(0,100) < 60: #Share the same eye colour
                eyes = self.eyes
            else:
                eyes = None

            if renpy.random.randint(0,100) < 60: #Have heights that roughly match (but not exactly, and readjusted for the the general scaling factor.)
                height = (self.height/0.8) * (renpy.random.randint(95,105)/100.0)
                if height > 1.0:
                    height = 1.0
                elif height < 0.9:
                    height = 0.9
            else:
                height = None

            if renpy.random.randint(0,100) < 85 - age or force_live_at_home: #It is less likely she lives at home the older she is.
                start_home = self.home
            else:
                start_home = None


            the_daughter = create_random_person(last_name = self.last_name, age = age, body_type = body_type, face_style = face_style, tits = tits, height = height,
                hair_colour = hair_colour, skin = self.skin, eyes = eyes, start_home = start_home)

            if start_home is None:
                the_daughter.generate_home()
            the_daughter.home.add_person(the_daughter)

            for sister in town_relationships.get_existing_children(self): #First find all of the other kids this person has
                town_relationships.update_relationship(the_daughter, sister, "Sister") #Set them as sisters

            town_relationships.update_relationship(self, the_daughter, "Daughter", "Mother") #Now set the mother/daughter relationship (not before, otherwise she's a sister to herself!)

            return the_daughter


        def run_turn(self):
            self.change_energy(20, add_to_log = False)
            self.bleed_slut() #if our sluttiness is over our core slut, bleed some off and, if we have suggest, turn it into core slut.

            remove_list = []
            for serum in self.serum_effects: #Compute the effects of all of the serum that the girl is under.
                serum.run_on_turn(self) #Run the serum's on_turn funcion if it has one.
                if serum.duration_expired(): #Returns true if the serum effect is suppose to expire in this time, otherwise returns false. Always updates duration counter when called.
                    remove_list.append(serum) #Use a holder "remove" list to avoid modifying list while iterating.

            for serum in remove_list:
                serum.run_on_remove(self)
                self.serum_effects.remove(serum)

            #Now we want to see if she's unhappy enough to quit. We will tally her "happy points", a negative number means a chance to quit.
            for a_role in self.special_role:
                a_role.run_turn(self)



        def run_move(self,location): #Move to the apporpriate place for the current time unit, ie. where the player should find us.

            #Move the girl the appropriate location on the map. For now this is either a division at work (chunks 1,2,3) or downtown (chunks 0,5). TODO: add personal homes to all girls that you know above a certain amount.
            self.sexed_count = 0 #Reset the counter for how many times you've been seduced, you might be seduced multiple times in one day!

            if time_of_day == 0: #It's a new day, get a new outfit out to wear!
                self.planned_outfit = self.wardrobe.decide_on_outfit(self.sluttiness)
                self.apply_outfit(self.planned_outfit)
                self.planned_uniform = None

            destination = self.get_desination() #None destination means they have free time
            if destination == self.work and not mc.business.is_open_for_business():
                destination = None #TODO: We can now do day-of-the-week scheduling, so this is no longer needed.

            if destination is not None: #We have somewhere scheduled to be for this time chunk. Let's move over there.
                location.move_person(self, destination) #Always go where you're scheduled to be.
                if self.get_desination() == self.work: #We're going to work.
                    if self.should_wear_uniform(): #Get a uniform if we should be wearing one.
                        self.wear_uniform()
                        self.change_happiness(self.get_opinion_score("work uniforms"),add_to_log = False)
                        if self.planned_uniform and self.planned_uniform.slut_requirement > self.sluttiness*0.75: #A skimpy outfit/uniform is defined as the top 25% of a girls natural sluttiness.
                            self.change_slut_temp(self.get_opinion_score("skimpy uniforms"), add_to_log = False)

                elif destination == self.home:
                    self.apply_outfit(self.planned_outfit)

                #NOTE: There is no else here because all of the desitnations should be set. If it's just a location they travel there and that's the end of it.

            else:
                #She finds somewhere to burn some time
                self.apply_outfit(self.planned_outfit)
                available_locations = [] #Check to see where is public (or where you are white listed) and move to one of those locations randomly
                for potential_location in list_of_places:
                    if potential_location.public:
                        available_locations.append(potential_location)
                location.move_person(self, get_random_from_list(available_locations))

            #We do uniform/outfit checks in run move because it happens at the _start_ of the time chunk. The girl looks forward to wearing her outfit (or dreads it) rather than responds to actually doing it.
            if self.outfit and self.planned_outfit.slut_requirement > self.sluttiness*0.75: #A skimpy outfit is defined as the top 25% of a girls natural sluttiness.
                self.change_slut_temp(self.get_opinion_score("skimpy outfits"), add_to_log = False)
            elif self.outfit and self.planned_outfit.slut_requirement < self.sluttiness*0.25: #A conservative outfit is defined as the bottom 25% of a girls natural sluttiness.
                self.change_happiness(self.get_opinion_score("conservative outfits"), add_to_log = False)

            if self.outfit.tits_available() and self.outfit.tits_visible() and self.outfit.vagina_available() and self.outfit.vagina_visible():
                self.change_slut_temp(self.get_opinion_score("not wearing anything"), add_to_log = False)

            if not self.outfit.wearing_bra() or not self.outfit.wearing_panties(): #We need to determine how much underwear they are not wearing. Each piece counts as half, so a +2 "love" is +1 slut per chunk.
                underwear_bonus = 0
                if not self.outfit.wearing_bra():
                    underwear_bonus += self.get_opinion_score("not wearing underwear")
                if not self.outfit.wearing_panties():
                    underwear_bonus += self.get_opinion_score("not wearing underwear")
                underwear_bonus = __builtin__.int(underwear_bonus/2.0) #I believe this rounds towards 0. No big deal if it doesn't, very minor detail.
                self.change_slut_temp(underwear_bonus, add_to_log = False)

            if self.outfit.tits_visible():
                self.change_slut_temp(self.get_opinion_score("showing her tits"), add_to_log = False)
            if self.outfit.vagina_visible():
                self.change_slut_temp(self.get_opinion_score("showing her ass"), add_to_log = False)

            for event_list in [self.on_room_enter_event_list, self.on_talk_event_list]: #Go through both of these lists and curate them, ie trim out events that should have expired.
                removal_list = [] #So we can iterate through without removing and damaging the list.
                for an_action in event_list:
                    if isinstance(an_action, Limited_Time_Action): #It's a LTA holder, so it has a turn counter
                        an_action.turns_valid += -1
                        if an_action.turns_valid <= 0:
                            removal_list.append(an_action)

                for action_to_remove in removal_list:
                    event_list.remove(action_to_remove)

            for a_role in self.special_role:
                a_role.run_move(self)



        def run_day(self): #Called at the end of the day.
            #self.outfit = self.wardrobe.decide_on_outfit(self.sluttiness) #Put on a new outfit for the day!

            self.change_energy(60, add_to_log = False)
            if self.arousal > (self.max_arousal/2): #TODO: Have this trigger an LTE where girls might be getting off when you walk in.
                self.arousal = __builtin__.int(self.arousal/2) # If her arousal is high she masturbates at night, generating a small amount of sluttiness
                self.change_slut_temp(1, add_to_log = False)
                self.change_happiness(5*self.get_opinion_score("masturbating"), add_to_log = False)

            #Now we will normalize happiness towards 100 over time. Every 5 points of happiness above or below 100 results in a -+1 per time chunk, rounded towards 0.
            hap_diff = self.happiness - 100
            hap_diff = __builtin__.int(hap_diff/5.0) #python defaults to truncation towards 0, so this gives us the number we should be changing our happinss by
            self.change_happiness(-hap_diff, add_to_log = False) #Apply the change

            remove_list = []
            for serum in self.serum_effects:
                serum.run_on_turn(self) #If a run_on_turn is called and the serum has expired no effects are calculated, so we can safely call this as many times as we want.
                serum.run_on_turn(self) #Night is 3 turn chunks, but one is already called when time progresses. Run serums twice more, and if we've gotten here we also run the on day function.
                serum.run_on_day(self) #Serums that effect people at night must effect two of the three time chunks.
                if serum.duration_expired(): #Night is 3 segments, but 1 is allready called when run_turn is called.
                    remove_list.append(serum)

            for serum in remove_list:
                serum.run_on_remove(self)
                self.serum_effects.remove(serum)

            for infraction in self.infractions:
                infraction.days_existed += 1
                if infraction.days_existed > infraction.days_valid:
                    self.remove_infraction(infraction)


            if day%7 == 0: #If the new day is Monday
                self.change_happiness(self.get_opinion_score("Mondays")*10, add_to_log = False)

            elif day%7 == 5: #If the new day is Friday
                self.change_happiness(self.get_opinion_score("Fridays")*10, add_to_log = False)

            elif day%7 == 6 or day%7 == 7: #If the new day is a weekend day
                self.change_happiness(self.get_opinion_score("the weekend")*10, add_to_log = False)

            for a_role in self.special_role:
                a_role.run_day(self)


        def build_person_displayable(self,position = None, emotion = None, special_modifier = None, lighting = None, background_fill = "#0026a5", no_frame = False): #Encapsulates what is done when drawing a person and produces a single displayable.
            if position is None:
                position = self.idle_pose #Easiest change is to call this and get a random standing posture instead of a specific idle pose. We redraw fairly frequently so she will change position frequently.

            displayable_list = [] # We will be building up a list of displayables passed to us by the various objects on the person (their body, clothing, etc.)

            if emotion is None:
                emotion = self.get_emotion()

            forced_special_modifier = self.outfit.get_forced_modifier()
            if forced_special_modifier is not None:
                special_modifier = forced_special_modifier # Overrides all other things, supports people with ball gags always having an open mouth (mechanically, not emotionally)

            x_size = position_size_dict.get(position)[0]
            y_size = position_size_dict.get(position)[1]

            displayable_list.append(self.body_images.generate_item_displayable(self.body_type,self.tits,position,lighting)) #Add the body displayable
            displayable_list.append(self.expression_images.generate_emotion_displayable(position,emotion, special_modifier = special_modifier, eye_colour = self.eyes[1], lighting = lighting)) #Get the face displayable
            displayable_list.append(self.pubes_style.generate_item_displayable(self.body_type,self.tits, position, lighting = lighting)) #Add in her pubes. #TODO: See if we need to mask this with her body profile for particularly bush-y bushes to prevent clothing overflow.

            displayable_list.extend(self.outfit.generate_draw_list(self,position,emotion,special_modifier, lighting = lighting)) #Get the displayables for everything we wear. Note that extnsions do not return anything because they have nothing to show.
            displayable_list.append(self.hair_style.generate_item_displayable("standard_body",self.tits,position, lighting = lighting)) #Get hair
            #NOTE: Positional modifiers like xanchor that expect pixles need to be given ints, they do not auto convert from floats.

            composite_list = [(x_size,y_size)] #Now we build a list of our parameters, done like this so they are arbitrarily long
            if background_fill: #If we have a background add it now.
                composite_list.append((0,0))
                composite_list.append(Solid(background_fill))

            for display in displayable_list:
                if isinstance(display, __builtin__.tuple):
                    composite_list.extend(display)
                else:
                    composite_list.append((0,0)) #Displayables are all handed over as composites with the image centered, so no extra work is needed here.
                    composite_list.append(display) #Append the actual displayable

            if background_fill and not no_frame: #no_frame allows us to add the frame after for animated displayables, to avoid warping the frame itself.
                composite_list.append((0,0))
                composite_list.append(Frame("/gui/Character_Window_Frame.png", 12, 12))

            final_image = Flatten(Composite(*composite_list)) # Create a composite image using all of the displayables
            return final_image

        def prepare_animation_screenshot_render(self, position, emotion, special_modifier, lighting, background_fill, given_reference_draw_number, draw_layer):
            log_message(self.name + " | PREP | " + str(time.time()))
            if background_fill is None:
                background_fill = "#0026a5"


            the_displayable = self.build_person_displayable(position, emotion, special_modifier, lighting, background_fill, no_frame = True)
            if the_displayable is None:
                renpy.notify("NONE IMAGE ERROR!")



            x_size = position_size_dict.get(position)[0]
            y_size = position_size_dict.get(position)[1]
            log_message(self.name + " | DISB | " + str(time.time()))
            the_render = the_displayable.render(x_size,y_size,0,0)
            log_message(self.name + " | REND | " + str(time.time()))

            global prepared_animation_render
            prepared_animation_render[draw_layer][self.character_number] = the_render

            global animation_draw_requested
            animation_draw_requested[draw_layer].append([self, given_reference_draw_number])
            return

        def prepare_animation_screenshot_render_multi(self, position, old_precalculated_render, new_precalculated_render, given_reference_draw_number, draw_layer):

            x_size, y_size = position_size_dict.get(position)

            old_render = old_precalculated_render
            new_render = new_precalculated_render

            global prepared_animation_render
            prepared_animation_render[draw_layer][self.character_number] = [old_render, new_render]

            global animation_draw_requested
            animation_draw_requested[draw_layer].append([self, given_reference_draw_number])
            return

        # Renamed from "build_person_animtion" in v0.30, now assuems it is handed a screenshot surface from take_animation_screenshot
        def draw_person_animation(self, the_surface, the_animation, position, emotion, special_modifier, lighting, background_fill = None, animation_effect_strength = 1.0, show_person_info = True, draw_reference_number = None,
            draw_layer = "solo", display_transform = None, extra_at_arguments = None, display_zorder = None, clear_active = True): #Note: clear_active needs to be the last parameter here for the animation call to properly insert it as a parameter.

            log_message(self.name + " | ASTR | " + str(time.time()))
            if display_zorder is None:
                display_zorder = 0

            x_size, y_size = position_size_dict.get(position)

            physical_x, physical_y = the_surface.get_size() #Use the surface render to figure out how large the displayed area is.

            physical_x = physical_x*1.0
            physical_y = physical_y*1.0

            config_x = config.screen_width * 1.0
            config_y = config.screen_height * 1.

            if physical_x/(16.0/9.0) > physical_y: #Account for the screen resolution difference from 16x9
                # TODO: Remove references to vren_mac_scale once we are sure they are no longer needed
                y_scale = 1*(config_y/(physical_y*persistent.vren_mac_scale)) #This should adjust for high DPI displays that have a higher physical pixel density than their stated resolution

                x_scale = y_scale
            else:
                x_scale = 1*(config_x/(physical_x*persistent.vren_mac_scale))

                y_scale = x_scale

            surface_file = io.BytesIO()
            the_surface = the_surface.subsurface((0,0,(x_size/x_scale),(y_size/y_scale))) # Take a subsurface of the surface screenshotted, so that we only save what is strictly nessesary.

            log_message(self.name + " | ACP1 | " + str(time.time()))
            #TODO: Check if we can use display.pgrender.load_image(file, filename) to load the surface data without needing to screenshot it somehow.
            renpy.display.module.save_png(the_surface, surface_file, 0) #This is a relatively time expensive operation, taking 0.12 to 0.14 seconds to perform. #TODO: Retest how long this takes with the trimmed surface
            static_image = im.Data(surface_file.getvalue(), "animation_temp_image.png")
            surface_file.close()


            log_message(self.name + " | ACP2 | " + str(time.time()))

            scaled_image = im.FactorScale(static_image, x_scale, y_scale)

            the_image_name = self.name + " | " + str(time.time()) #Note: use to make use of a unique time stamp

            composite_components = []
            region_weight_items_dict = the_animation.get_weight_items()
            for region_weight_name in region_weight_items_dict: #Goes through each region ie. "breasts", "butt", and others to come, and applies the animation strength, the personal region strength, and animation region strength
                the_weight_item = region_weight_items_dict[region_weight_name]
                composite_components.append(the_weight_item.crop_offset_dict.get(position, (0,0)))
                region_weight_modifier = animation_effect_strength * self.personal_region_modifiers.get(region_weight_name, 1) * the_animation.innate_animation_strength * the_animation.region_specific_weights.get(region_weight_name, 1)
                if region_weight_modifier > 1:
                    region_weight_modifier = 1
                #renpy.notify(str(animation_effect_strength) + " | " + str(self.personal_region_modifiers.get(region_weight_name, 1)) + " | " + str(the_animation.innate_animation_strength) + " | " + str(the_animation.region_specific_weights.get(region_weight_name, 1)))

                region_brightness_matrix = im.matrix.brightness(-1 + region_weight_modifier)
                region_mask = the_weight_item.generate_raw_image(self.body_type, self.tits, position)
                region_mask = im.MatrixColor(region_mask, region_brightness_matrix)
                composite_components.append(region_mask)



            the_mask_composite = im.Composite((x_size, y_size), *composite_components)

            mask_image = im.Blur(the_mask_composite, 2)
            mask_image_name = self.name + "_tex | " + str(self.character_number)

            animation_uniforms = the_animation.uniforms #Copy the default uniforms for the animation
            animation_uniforms["animation_strength"] = animation_effect_strength

            log_message(self.name + " | MASK | " + str(time.time()))

            raw_animated_displayable = ShaderDisplayable(shader.MODE_2D, scaled_image, the_image_name, shader.VS_2D, the_animation.shader,{"tex1":mask_image}, animation_uniforms, None, None, mask_name = mask_image_name)

            log_message(self.name + " | DISP | " + str(time.time()))

            cropped_animated_displayable = Crop((0,0,x_size,y_size), raw_animated_displayable)
            framed_animated_displayable = Composite((x_size,y_size),(0,0),cropped_animated_displayable,(0,0),Frame("/gui/Character_Window_Frame.png", 12, 12))

            if show_person_info:
                renpy.show_screen("person_info_ui", self)

            if display_transform is None:
                display_transform = character_right

            at_list_arguments = [display_transform, scale_person(self.height)]

            if extra_at_arguments:
                if not isinstance(extra_at_arguments, list):
                    extra_at_arguments = [extra_at_arguments]
                at_list_arguments.extend(extra_at_arguments)
            else:
                extra_at_arguments = []

            character_tag = str(self.character_number)

            if clear_active: #Clear out the old version of this character, if they exist.
                self.hide_person()
            else:
                character_tag += "_extra" #Allows for two varients of teh same character to be drawn, useful when fading from one to another to show clothing being removed.

            renpy.show(character_tag,at_list=at_list_arguments,layer=draw_layer,what=framed_animated_displayable,zorder=display_zorder, tag=character_tag)
            log_message(self.name + " | Anim | " + str(time.time()))

        def draw_person(self,position = None, emotion = None, special_modifier = None, show_person_info = True, lighting = None, background_fill = "#0026a5", the_animation = None, animation_effect_strength = 1.0,
            draw_layer = "solo", display_transform = None, extra_at_arguments = None, display_zorder = None, wipe_scene = True): #Draw the person, standing as default if they aren't standing in any other position
            log_message(self.name + " | Start | " + str(time.time()))

            if position is None:
                position = self.idle_pose #Easiest change is to call this and get a random standing posture instead of a specific idle pose. We redraw fairly frequently so she will change position frequently.

            if the_animation is None:
                the_animation = self.idle_animation

            if not can_use_animation():
                the_animation = None

            if lighting is None:
                lighting = mc.location.get_lighting_conditions()

            character_image = self.build_person_displayable(position, emotion, special_modifier, lighting, background_fill)

            if display_transform is None:
                display_transform = character_right

            at_arguments = [display_transform, scale_person(self.height)]
            if extra_at_arguments:
                if isinstance(extra_at_arguments, list):
                    at_arguments.extend(extra_at_arguments)
                else:
                    at_arguments.append(extra_at_arguments)
            else:
                extra_at_arguments = []

            if display_zorder is None:
                display_zorder = 0

            character_tag = str(self.character_number)

            self.draw_number[draw_layer] += 1
            self.hide_person()
            if wipe_scene:
                clear_scene() #Make sure no other characters are drawn either.

            renpy.show(character_tag, at_list=at_arguments, layer=draw_layer, what=character_image, zorder = display_zorder, tag=character_tag) #Display a static image of the character as soon as possible
            log_message(self.name + " | Flat | " + str(time.time()))
            if show_person_info:
                renpy.show_screen("person_info_ui",self)

            if the_animation:
                global global_draw_number
                animation_draw_number = self.draw_number[draw_layer] + global_draw_number[draw_layer]

                global prepared_animation_arguments
                prepared_animation_arguments[draw_layer][self.character_number] = [the_animation, position, emotion, special_modifier, lighting, background_fill, animation_effect_strength, show_person_info, animation_draw_number, draw_layer, display_transform, extra_at_arguments, display_zorder] #Effectively these are being stored and passed to draw_person_animation once take_animation_screenshot returns the surface
                renpy.invoke_in_thread(self.prepare_animation_screenshot_render, position, emotion, special_modifier, lighting, background_fill, animation_draw_number, draw_layer) #This thread prepares the render. When it is finished it is caught by the interact_callback function take_animation_screenshot

        def hide_person(self, draw_layer = "solo"): #Hides the person. Makes sure to hide all posible known tags for the character.
            # We keep track of tags used to display a character so that they can always be unique, but still tied to them so they can be hidden
            character_tag = str(self.character_number)
            renpy.hide(character_tag, draw_layer)
            renpy.hide(character_tag+"_extra", draw_layer)


        def draw_animated_removal(self, the_clothing, position = None, emotion = None, special_modifier = None, show_person_info = True, lighting = None, background_fill = "#0026a5", the_animation = None, animation_effect_strength = 1.0, half_off_instead = False,
            draw_layer = "solo", display_transform = None, extra_at_arguments = None, display_zorder = None, wipe_scene = True):
            #The new animated_removal method generates two image, one with the clothing item and one without. It then stacks them and layers one on top of the other and blends between them.

            if position is None:
                position = self.idle_pose

            if not can_use_animation():
                the_animation = None

            elif the_animation is None:
                the_animation = self.idle_animation

            if lighting is None:
                lighting = mc.location.get_lighting_conditions()

            global draw_layers
            if draw_layer not in draw_layers:
                add_draw_layer(draw_layer)

            if display_transform is None:
                display_transform = character_right

            at_arguments = [display_transform, scale_person(self.height)]
            if extra_at_arguments:
                if isinstance(extra_at_arguments, list):
                    at_arguments.extend(extra_at_arguments)
                else:
                    at_arguments.append(extra_at_arguments)
            else:
                extra_at_arguments = []

            self.draw_number[draw_layer] += 1

            if display_zorder is None:
                display_zorder = 0


            if the_animation:
                # Normally we would display a quick flat version, but we can assume we are already looking at the girl pre-clothing removal.
                bottom_displayable = Flatten(self.build_person_displayable(position, emotion, special_modifier, lighting, background_fill, no_frame = True)) #Get the starting image without the frame
                if isinstance(the_clothing, list):
                    for cloth in the_clothing:
                        if half_off_instead:
                            self.outfit.half_off_clothing(cloth) #Half-off the clothing
                        else:
                            self.outfit.remove_clothing(cloth) #Remove the clothing
                else:
                    if half_off_instead:
                        self.outfit.half_off_clothing(the_clothing) #Half-off the clothing
                    else:
                        self.outfit.remove_clothing(the_clothing) #Remove the clothing
                top_displayable = Flatten(self.build_person_displayable(position, emotion, special_modifier, lighting, background_fill, no_frame = True)) #Get the top image, with frame.

                x_size, y_size = position_size_dict.get(position)
                bottom_render = bottom_displayable.render(x_size, y_size, 0, 0)
                top_render = top_displayable.render(x_size, y_size, 0, 0)

                global global_draw_number
                animation_draw_number = self.draw_number[draw_layer] + global_draw_number[draw_layer]

                global prepared_animation_arguments
                prepared_animation_arguments[draw_layer][self.character_number] = [the_animation, position, emotion, special_modifier, lighting, background_fill, animation_effect_strength, show_person_info, animation_draw_number, draw_layer, display_transform, extra_at_arguments, display_zorder]

                renpy.invoke_in_thread(self.prepare_animation_screenshot_render_multi, position, bottom_render, top_render, animation_draw_number, draw_layer)

            else:
                if wipe_scene:
                    clear_scene()

                if show_person_info:
                    renpy.show_screen("person_info_ui",self)

                bottom_displayable = Flatten(self.build_person_displayable(position, emotion, special_modifier, lighting, background_fill)) #Get the starting image
                if isinstance(the_clothing, list):
                    for cloth in the_clothing:
                        if half_off_instead:
                            self.outfit.half_off_clothing(cloth) #Half-off the clothing
                        else:
                            self.outfit.remove_clothing(cloth) #Remove the clothing
                else:
                    if half_off_instead:
                        self.outfit.half_off_clothing(the_clothing) #Half-off the clothing
                    else:
                        self.outfit.remove_clothing(the_clothing) #Remove the clothing
                top_displayable = self.build_person_displayable(position, emotion, special_modifier, lighting, background_fill) #Get the top image

                self.hide_person()
                character_tag = str(self.character_number)
                renpy.show(character_tag, at_list=at_arguments, layer = draw_layer, what = top_displayable, zorder = display_zorder, tag = character_tag)
                fade_at_arguments = at_arguments[:]
                fade_at_arguments.append(clothing_fade)
                renpy.show(character_tag + "_extra", at_list=fade_at_arguments, layer = draw_layer, what = bottom_displayable, zorder = display_zorder, tag = character_tag + "_extra") #Blend from old to new.

            return

        def get_emotion(self): # Get the emotion state of a character, used when the persons sprite is drawn and no fixed emotion is required.
            if self.arousal>= self.max_arousal:
                return "orgasm"

            if self.happiness > 100:
                return "happy"

            elif self.happiness < 80:
                if self.love > 0:
                    return "sad"
                else:
                    return "angry"

            else:
                return "default"

        def call_dialogue(self, type, **extra_args): #Passes the paramater along to the persons personality and gets the correct dialogue for the event if it exists in the dict.
            return self.personality.get_dialogue(self, type, **extra_args)


        def get_opinion_score(self, topic): #Like get_opinion_topic, but only returns the score and not a tuple. Use this when determining a persons reaction to a relavent event.
            if topic in self.opinions:
                return self.opinions[topic][0]

            if topic in self.sexy_opinions:
                return self.sexy_opinions[topic][0]

            return 0

        def get_opinion_topic(self, topic): #topic is a string matching the topics given in our random list (ie. "the colour blue", "sports"). Returns a tuple containing the score: -2 for hates, -1 for dislikes, 0 for no opinion, 1 for likes, and 2 for loves, and a bool to say if the opinion is known or not.
            if topic in self.opinions:
                return self.opinions[topic]

            if topic in self.sexy_opinions:
                return self.sexy_opinions[topic]

            return None

        def get_random_opinion(self, include_known = True, include_sexy = False, include_normal = True, only_positive = False, only_negative = False): #Gets the topic string of a random opinion this character holds. Includes options to include known opinions and sexy opinions. Returns None if no valid opinion can be found.
            the_dict = {} #Start our list of valid opinions to be listed as empty

            if include_normal: #if we include normal opinions build a dict out of the two
                the_dict = dict(the_dict, **self.opinions)

            if include_sexy: #If we want sexy opinions add them in too.
                the_dict = dict(the_dict, **self.sexy_opinions)


            known_keys = []
            if not include_known: #If we do not want to talk about known values
                for k in the_dict: #Go through each value in our combined normal and sexy opinion dict
                    if the_dict[k][1]: #Check if we know about it...
                        known_keys.append(k) #We build a temporary list of keys to remove because otehrwise we are modifying the dict while we traverse it.
                for del_key in known_keys:
                    del the_dict[del_key]

            remove_keys = []
            if only_positive or only_negative: # Let's us filter opinions so they only include possitive or negative ones.
                if only_positive:
                    for k in the_dict:
                        if self.get_opinion_score(k) < 0:
                            remove_keys.append(k)

                if only_negative:
                    for k in the_dict:
                        if self.get_opinion_score(k) > 0:
                            remove_keys.append(k)

                for del_key in remove_keys:
                    del the_dict[del_key]

            if the_dict:
                return get_random_from_list(the_dict.keys()) #If we have something in the list we can return the topic string we used as a key for it. This can then be used with get_opinion_score to get the actual opinion
            else:
                return None #If we have nothing return None, make sure to deal with this when we use this function.


        def discover_opinion(self, topic, add_to_log = True): #topic is a string matching the topics given in our random list (ie. "the colour blue"). If the opinion is in either of our opinion dicts we will set it to known, otherwise we do nothing. Returns True if the opinion was updated, false if nothing was changed.
            display_name = self.create_formatted_title("???")
            updated = False
            if self.title:
                display_name = self.title
            if topic in self.opinions:
                if not self.opinions[topic][1]:
                    updated = True
                    if add_to_log and self.title is not None:
                        mc.log_event("Discovered: " + display_name + " " + opinion_score_to_string(self.opinions[topic][0]) + " " + topic,"float_text_grey")
                self.opinions[topic][1] = True

            if topic in self.sexy_opinions:
                if not self.sexy_opinions[topic][1]:
                    updated = True
                    if add_to_log and self.title is not None:
                        mc.log_event("Discovered: " + display_name + " " + opinion_score_to_string(self.sexy_opinions[topic][0]) + " " + topic,"float_text_grey")
                self.sexy_opinions[topic][1] = True

            return updated

        def has_taboo(self, the_taboos):
            if the_taboos is None:
                return False

            if isinstance(the_taboos, basestring):
                the_taboos = [the_taboos]

            for a_taboo in the_taboos: #We also handle lists, if we wnat to check if someone has _any_ of several taboos at once
                if a_taboo not in self.broken_taboos:
                    return True
            return False

        def break_taboo(self, the_taboo, add_to_log = True):
            if the_taboo not in self.broken_taboos:
                self.broken_taboos.append(the_taboo)
                display_name = self.create_formatted_title("???")
                if self.title:
                    display_name = self.title
                if add_to_log:
                    mc.log_event(" Taboo broken with " + display_name + "!", "float_text_red")
                return True
            return False

        def pick_position_comment(self, the_report): #Takes a report and has the person pick the most notable thing out of it. Generally used to then have them comment on it.
            highest_slut_position = None
            highest_slut_opinion = 0
            for position in the_report.get("positions_used", []):
                slut_opinion = position.slut_requirement
                if position.opinion_tags is not None:
                    for opinion_tag in position.opinion_tags:
                        slut_opinion += 5*self.get_opinion_score(opinion_tag)
                if highest_slut_position is None or slut_opinion > highest_slut_opinion:
                    highest_slut_position = position
                    highest_slut_opinion = slut_opinion

            return highest_slut_position


        def add_outfit(self,the_outfit, outfit_type = "full"):
            if outfit_type == "under":
                self.wardrobe.add_underwear_set(the_outfit)
            elif outfit_type == "over":
                self.wardrobe.add_overwear_set(the_outfit)
            else: #outfit_type = full
                self.wardrobe.add_outfit(the_outfit)

        def set_outfit(self,new_outfit):
            if new_outfit is not None:
                self.planned_outfit = new_outfit.get_copy() #Get a copy to return to when we are done.
                self.apply_outfit(new_outfit)

        def set_uniform(self,uniform, wear_now = False):
            if uniform is not None:
                self.planned_uniform = uniform.get_copy()
                if wear_now:
                    self.wear_uniform()

        def apply_outfit(self, the_outfit = None, ignore_base = False, update_taboo = False): #Hand over an outfit, we'll take a copy and apply it to the person, along with their base accessories unless told otherwise.
            if the_outfit is None:
                the_outfit = self.planned_outfit
                if the_outfit is None:
                    return #We don't have a planned outfit, so trying to return to it makes no sense.
            if ignore_base:
                self.outfit = the_outfit.get_copy()
            else:
                self.outfit = the_outfit.get_copy().merge_outfit(self.base_outfit)

            if update_taboo: #If True, we assume this outfit is being put on or shown to the MC. It can break taboos about showing underwear, tits, pussy.
                self.update_outfit_taboos()

        def update_outfit_taboos(self):
            return_value = False
            if self.outfit.tits_visible():
                if self.break_taboo("bare_tits"):
                    return_value = True
            if self.outfit.vagina_visible():
                if self.break_taboo("bare_pussy"):
                    return_value = True
            if (self.outfit.wearing_panties() and not self.outfit.panties_covered()) or (self.outfit.wearing_bra() and not self.outfit.bra_covered()):
                if self.break_taboo("underwear_nudity"):
                    return_value = True
            return return_value


        def give_serum(self,the_serum_design, add_to_log = True): ##Make sure you are passing a copy of the serum, not a reference.
            self.serum_effects.append(the_serum_design)
            the_serum_design.run_on_apply(self)

        def is_under_serum_effect(self):
            if self.serum_effects:
                return True
            else:
                return False

        def apply_serum_study(self, add_to_log = True): #Called when the person is studied by the MC. Raises mastery level of all traits used in active serums by 0.2
            studied_something = False
            for serum in self.serum_effects:
                for trait in serum.traits:
                    trait.add_mastery(0.2)
                    studied_something = True
            if studied_something and add_to_log:
                display_name = self.create_formatted_title("???")
                if self.title:
                    display_name = self.title
                mc.log_event("Observed " + display_name + ", mastery of all active serum traits increased by 0.2", "float_text_blue")


        def change_suggest(self,amount): #This changes the base, usually permanent suggest. Use add_suggest_effect to add temporary, only-highest-is-used, suggestion values
            self.suggestibility += amount
            if self.suggestibility < 0:
                self.suggestibility = 0

        def add_suggest_effect(self,amount, add_to_log = True):
            if amount > __builtin__.max(self.suggest_bag or [0]):
                self.change_suggest(-__builtin__.max(self.suggest_bag or [0])) #Subtract the old max and...
                self.change_suggest(amount) #add our new suggest.
                if add_to_log and amount != 0 and self.title:
                    mc.log_event(self.title + ": Suggestibility increased, now " + str(amount), "float_text_blue")
            else:
                if add_to_log and amount != 0 and self.title:
                    mc.log_event(self.title + ": Suggestiblity " + str(amount) + " lower than current " + str(self.suggestibility) + " amount. Suggestibility unchanged.", "float_text_blue")
            self.suggest_bag.append(amount) #Add it to the bag, so we can check to see if it is max later.


        def remove_suggest_effect(self,amount):
            if amount in self.suggest_bag: # Avoid removing the "amount" if we don't actually have it in the bag.
                self.change_suggest(- __builtin__.max(self.suggest_bag or [0])) #Subtract the max
                self.suggest_bag.remove(amount)
                self.change_suggest(__builtin__.max(self.suggest_bag or [0])) # Add the new max. If we were max, it is now lower, otherwie it cancels out.

        def change_happiness(self,amount, add_to_log = True):
            self.happiness += amount
            if self.happiness < 0:
                self.happiness = 0

            log_string = ""
            if amount > 0:
                log_string = "+" + str(amount) + " Happiness"
            else:
                log_string = str(amount) + " Happiness"

            if add_to_log and amount != 0:
                display_name = self.create_formatted_title("???")
                if self.title:
                    display_name = self.title
                mc.log_event(display_name + ": " + log_string, "float_text_yellow")

        def change_love(self, amount, add_to_log = True, max_modified_to = None):
            log_string = ""
            amount = __builtin__.int(amount)
            if max_modified_to is not None and self.love + amount > max_modified_to:
                if amount != 0:
                    log_string += "Love limit reached for interaction. "
                amount = max_modified_to - self.love
                if amount < 0: #Never subtract love because of a cap, only limit how much they gain.
                    amount = 0


            self.love += amount
            if self.love < -100:
                self.love = -100
            elif self.love > 100:
                self.love = 100


            if amount > 0:
                log_string += "+" + str(amount) + " Love"
            else:
                log_string += str(amount) + " Love"

            if add_to_log and amount != 0:
                display_name = self.create_formatted_title("???")
                if self.title:
                    display_name = self.title
                mc.log_event(display_name + ": " + log_string, "float_text_pink")

        def change_slut_temp(self,amount, add_to_log = True): #Adds the amount to our slut value. If over our max, add only to the max instead (but don't lower). If subtracting, don't go lower than 0.
            return_report = "" #This is the string that is returned that will report what the final value of the change was.
            if amount > 0:
                self.sluttiness += amount
                return_report = "+" + str(amount) + " Sluttiness"

                # We're experimenting with uncapping the sluttiness and having sluttiness in excess of your suggestability cap bleed off quickly and inefficently.
                # if self.sluttiness > self.core_sluttiness + self.suggestibility + 10:
                #     self.sluttiness = self.core_sluttiness + self.suggestibility + 10 #Set it to our max.
                #     return_report = "Sluttiness Cap Reached." #If we hit the cap, let them know that instead of the numeric amount.
                #     if self.suggestibility == 0:
                #         return_report += "\nUse Serum to Increase Cap."

            elif amount < 0:
                self.sluttiness += amount
                return_report = str(amount) + " Sluttiness"
                # if self.sluttiness < 0: #TODO: confirm that letting temp sluttiness drop below 0 does not cause any problems.
                #     self.sluttiness = 0

            else: #It is exactly 0
                return_report = "No Effect on Sluttiness"

            if add_to_log:
                display_name = self.create_formatted_title("???")
                if self.title:
                    display_name = self.title
                mc.log_event(display_name + ": " + return_report, "float_text_pink")

            # return return_report #Return this so we can display the effective change or cap message. #Depreciated as of phone log approach


        def change_slut_core(self,amount, add_to_log = True, fire_event = True): #Adds set amount to core slut.
            self.core_sluttiness += amount
            # if self.core_sluttiness < 0: #TODO: Confirm that letting core sluttiness drop below 0 does not cause any problems.
            #     self.core_sluttiness = 0
            if fire_event:
                mc.listener_system.fire_event("core_slut_change", the_person = self, amount = amount)
            log_string = ""
            if amount > 0:
                log_string = "+" + str(amount) + " Core Sluttiness"
            else:
                log_string = str(amount) + " Core Sluttiness"

            if add_to_log and amount != 0:
                display_name = self.create_formatted_title("???")
                if self.title:
                    display_name = self.title
                mc.log_event(display_name + ": " + log_string, "float_text_pink")

        def add_situational_slut(self, source, amount, description = ""):
            #Adds a conditional, temporary sluttiness amount. This is added now and removed when clear_situational is called, or when another add_situational is called with the same source.
            if source in self.situational_sluttiness:
                difference = amount - self.situational_sluttiness[source][0]
                self.change_slut_core(difference, add_to_log = False, fire_event = False)
                self.change_slut_temp(difference, add_to_log = False)

            else:
                self.change_slut_core(amount, add_to_log = False, fire_event = False)
                self.change_slut_temp(amount, add_to_log = False)

            self.situational_sluttiness[source] = (amount,description)

        def clear_situational_slut(self, source):
            self.add_situational_slut(source, 0) #We don't actually ever care if we remove the key, we just want to set the amount to 0.

        def add_situational_obedience(self, source, amount, description = ""):
            if source in self.situational_obedience:
                difference = amount - self.situational_obedience[source][0]
                self.change_obedience(difference, add_to_log = False)
            else:
                self.change_obedience(amount, add_to_log = False)
            self.situational_obedience[source] = (amount,description)

        def clear_situational_obedience(self, source):
            self.add_situational_obedience(source, 0)


        def bleed_slut(self): #Reduce temp slut in order to increase core slut at a ratio determined by the suggest score.
            if self.sluttiness > self.core_sluttiness: #We need to bleed away sluttiness.
                if self.suggestibility == 0 and self.title: #TODO: think about how much we need this now.
                    mc.business.add_normal_message(self.title + " has a sluttiness higher then her core sluttiness. Raising her suggestibility with serum will turn temporary sluttiness into core sluttiness more quickly and efficently!")

                if self.sluttiness > self.core_sluttiness + self.suggestibility:
                    #We need to bleed a lot because our suggestibility dropped.
                    difference = self.sluttiness - (self.core_sluttiness + self.suggestibility)
                    if difference > 5:
                        difference = 5

                    if renpy.random.randint(1,5) <= difference: #ie. there's a 20% chance per point over to increase it by a point.
                        self.change_slut_core(1, add_to_log = False) #We're experimenting with sluttiness above your suggestability amount converting inefficently (instead of not at all)
                    self.change_slut_temp(-difference, add_to_log = False)

                # self.change_slut_temp(-3, add_to_log = False) #We're experimenting with only lowering the temporary sluttiness when the core sluttiness goes up.
                elif renpy.random.randint(0,100) < self.suggestibility: # If we're not over our suggestability amount we turn it into core slut effectively.
                    self.change_slut_core(3, add_to_log = False)
                    self.change_slut_temp(-3, add_to_log = False)

            if self.sluttiness < self.core_sluttiness: #If we're lower than core we quickly return to it.
                difference = self.core_sluttiness - self.sluttiness
                if difference > 5:
                    difference = 5
                self.change_slut_temp(difference, add_to_log = False)


        def change_obedience(self,amount, add_to_log = True):
            self.obedience += amount
            if self.obedience < 0:
                self.obedience = 0
            log_string = ""
            if add_to_log and amount != 0: #If we don't know the title don't add it to the log, because we know nothing about the person
                display_name = self.create_formatted_title("???")
                if self.title:
                    display_name = self.title
                if amount > 0:
                    log_string = display_name + ": +" + str(amount) + " Obedience"
                else:
                    log_string = display_name + ": " + str(amount) + " Obedience"

                mc.log_event(log_string,"float_text_grey")

        def change_cha(self,amount, add_to_log = True):
            self.charisma += self.charisma_debt #Set our charisma to be our net score
            self.charisma_debt = 0 #We are currently holding no stat debt.

            self.charisma += amount #Adjust our stat now, may be positive or negative.
            if self.charisma < 0:
                self.charisma_debt = self.charisma #If we are less than 0 store it as a debt.
                self.charisma = 0

            log_string = ""
            if amount != 0 and add_to_log:
                display_name = self.create_formatted_title("???")
                if self.title:
                    display_name = self.title
                if amount > 0:
                    log_string = display_name + ": +" + str(amount) + " Charisma"
                else:
                    log_string = display_name + ": " + str(amount) + " Charisma"

                mc.log_event(log_string, "float_text_grey")

        def change_int(self,amount, add_to_log = True):
            self.int += self.int_debt
            self.int_debt = 0

            self.int += amount
            if self.int < 0:
                self.int_debt = self.int
                self.int = 0

            log_string = ""

            if amount != 0 and add_to_log:
                display_name = self.create_formatted_title("???")
                if self.title:
                    display_name = self.title

                if amount > 0:
                    log_string = display_name + ": +" + str(amount) + " Intelligence"
                else:
                    log_string = display_name + ": " + str(amount) + " Intelligence"

                mc.log_event(log_string, "float_text_grey")

        def change_focus(self,amount, add_to_log = True): #See charisma for full comments
            self.focus += self.int_debt
            self.focus_debt = 0

            self.focus += amount
            if self.focus < 0:
                self.focus_debt = self.focus
                self.focus = 0

            log_string = ""

            if amount != 0 and add_to_log:
                display_name = self.create_formatted_title("???")
                if self.title:
                    display_name = self.title

                if amount > 0:
                    log_string = display_name + ": +" + str(amount) + " Focus"
                else:
                    log_string = display_name + ": " + str(amount) + " Focus"


                mc.log_event(log_string, "float_text_grey")

        def review_outfit(self, dialogue = True, draw_person = True):
            if self.should_wear_uniform() and not self.is_wearing_uniform():
                self.apply_outfit()#Reset uniform
                if dialogue:
                    self.call_dialogue("clothing_review")
                if draw_person():
                    self.draw_person()


                #if dialogue:
                    #TODO: Have this call a dialogue branch
#                self.call_uniform_review() #TODO: actually impliment this call, but only when her outfit significantly differs from the real uniform.

            elif not self.judge_outfit(self.outfit):
                self.apply_outfit()
                if dialogue:
                    self.call_dialogue("clothing_review")
                if draw_person():
                    self.draw_person()


        def judge_outfit(self,outfit, temp_sluttiness_boost = 0, use_taboos = True, as_underwear = False, as_overwear = False): #Judge an outfit and determine if it's too slutty or not. Can be used to judge other people's outfits to determine if she thinks they look like a slut.
            # temp_sluttiness can be used in situations (mainly crises) where an outfit is allowed to be temporarily more slutty than a girl is comfortable wearing all the time.
            #Returns true if the outfit is wearable, false otherwise
            if as_underwear or as_overwear:
                use_taboos = False

            if use_taboos and not (outfit.bra_covered() and outfit.panties_covered()) and "underwear_nudity" not in self.broken_taboos:
                taboo_modifier = "underwear_nudity"
            elif use_taboos and outfit.tits_visible() and "bare_tits" not in self.broken_taboos:
                taboo_modifier = "bare_tits"
            elif use_taboos and outfit.vagina_visible() and "bare_pussy" not in self.broken_taboos:
                taboo_modifier = "bare_pussy"
            else:
                taboo_modifier = None

            slut_require = outfit.slut_requirement
            if as_underwear:
                slut_require = outfit.get_underwear_slut_score()

            elif as_overwear:
                slut_require = outfit.get_overwear_slut_score()

            if (outfit.get_bra() or outfit.get_panties()) and not as_overwear: #Girls who like lingerie judge outfits with lingerie as less slutty than normal
                lingerie_bonus = 0
                if outfit.get_bra() and outfit.get_bra().slut_value > 2: #We consider underwear with an innate sluttiness of 3 or higher "lingerie" rather than just underwear.
                    lingerie_bonus += self.get_opinion_score("lingerie")
                if outfit.get_panties() and outfit.get_panties().slut_value > 2:
                    lingerie_bonus += self.get_opinion_score("lingerie")
                lingerie_bonus = __builtin__.int(lingerie_bonus*2) # Up to an 8 point swing in either direction
                slut_require += -lingerie_bonus #Treated as less slutty if she likes it, more slutty if she dislikes lingerie

            # Considers the outfit less slutty if she likes showing her tits and ass and that's what it would do.
            if outfit.vagina_visible() or (outfit.wearing_panties() and not outfit.panties_covered()):
                slut_require += -2*self.get_opinion_score("showing her ass")

            if outfit.tits_visible() or (outfit.wearing_bra() and not outfit.bra_covered()):
                slut_require += -2*self.get_opinion_score("showing her tits")


            if slut_require > (self.effective_sluttiness(taboo_modifier) + temp_sluttiness_boost): #Arousal is important for judging potential changes to her outfit while being stripped down during sex.
                return False
            else:
                return True

        def is_wearing_uniform(self): # Returns True if the clothing the girl is wearing contains all of the uniform clothing items. #TODO: may want to support more flexibility for over/underwear sets that had optional bits chosen by the girl.
            #May want to make this a Business side check. Make "is_valid_uniform" check like this against all uniforms available for the character. Would provide the flexiblity I mentioned above.
            if self.planned_uniform is None:
                return False #If no uniform is set you aren't wearing one at all.

            uniform_wardrobe = mc.business.get_uniform_wardrobe_for_person(self)
            matching_full = False
            full_set = False #Boolean used to track if we have at least one full set we _could_ have been wearing

            matching_overwear = False
            overwear_set = False #Tracks if we had at least one overwear we _could_ have been wearing

            matching_underwear = False
            underwear_set = False #Tracks if we had an underwear set we could have been wearing

            for potential_uniform in uniform_wardrobe.get_valid_outfit_list(): #Check if we match any of the full uniforms
                full_set = True
                if not matching_full:
                    matching_full = True #Assume they match, then find a counter example. When we do, break and try the next one.
                    for cloth in potential_uniform.generate_clothing_list():
                        if not self.outfit.has_clothing(cloth):
                            matching_full = False
                            break

            for potential_uniform in uniform_wardrobe.get_valid_overwear_sets_list(): #Check if we match the overwear and underwear sets.
                overwear_set = True
                if not matching_overwear:
                    matching_overwear = True
                    for cloth in potential_uniform.generate_clothing_list():
                        if not self.outfit.has_clothing(cloth):
                            matching_overwear = False
                            break

            for potential_uniform in uniform_wardrobe.get_valid_underwear_sets_list():
                underwear_set = True
                if not matching_underwear:
                    matching_underwear = True
                    for cloth in potential_uniform.generate_clothing_list():
                        if not self.outfit.has_clothing(cloth):
                            matching_underwear = False
                            break

            if matching_full:
                return True

            elif matching_overwear and matching_underwear:
                return True

            elif matching_overwear or matching_underwear: #Sometimes this is okay
                if matching_overwear and not underwear_set:
                    return True
                elif matching_underwear and not overwear_set:
                    return True

            return False

        def should_wear_uniform(self):
            #Check to see if we are: 1) Employed by the PC. 2) At work right now. 3) there is a uniform set for our department.
            employment_title = mc.business.get_employee_title(self)
            if employment_title != "None":
                if mc.business.is_open_for_business(): #We should be at work right now, so if there is a uniform we should wear it.
                    if mc.business.get_uniform_wardrobe(employment_title).get_count() > 0 or self.event_triggers_dict.get("forced_uniform", False): #Check to see if there's anything stored in the uniform section.
                        return True

            return False #If we fail to meet any of the above conditions we should return false.

        def wear_uniform(self): #Puts the girl into her uniform, if it exists.
            if self.planned_uniform is None:
                the_uniform = mc.business.get_uniform_wardrobe(mc.business.get_employee_title(self)).decide_on_uniform(self)
                if self.event_triggers_dict.get("forced_uniform", False):
                    the_uniform = self.event_triggers_dict.get("forced_uniform")
                self.set_uniform(the_uniform, False) #If we don't have a uniform planned for today get one.

            if self.planned_uniform is not None: #If our planned uniform is STILL None it means we are unable to construct a valid uniform. Only assign it as our outfit if we have managed to construct a uniform.
                self.apply_outfit(self.planned_uniform) #We apply clothing taboos to uniforms because the character is assumed to have seen them in them.

        def get_job_happiness_score(self):
            happy_points = self.happiness - 100 #Happiness over 100 gives a bonus to staying, happiness less than 100 gives a penalty
            happy_points += self.obedience - 95 #A more obedient character is more likely to stay, even if they're unhappy. Default characters can be a little disobedint without any problems.
            happy_points += self.salary - self.calculate_base_salary() #A real salary greater than her base is a bonus, less is a penalty. TODO: Make this dependent on salary fraction, not abosolute pay.

            if (day - self.event_triggers_dict.get("employed_since",0)) < 14:
                happy_points += 14 - (day - self.event_triggers_dict.get("employed_since",0)) #Employees are much less likely to quit over the first two weeks.
            return happy_points

        def get_no_condom_threshold(self, situational_modifier = 0):
            if pregnant_role in self.special_role and self.event_triggers_dict.get("preg_knows", False):
                return 0 #You can't get more pregnant, so who cares?

            no_condom_threshold = 50 + (self.get_opinion_score("bareback sex") * -10) + situational_modifier
            if any(relationship in [sister_role,mother_role,aunt_role,cousin_role] for relationship in self.special_role):
                no_condom_threshold += 10

            if persistent.pregnancy_pref == 0:
                no_condom_threshold += 10 #If pregnancy content is being ignored we return to the baseline of 60
            elif the_person.on_birth_control: #If there is pregnancy content then a girl is less likely to want a condom when using BC, much more likely to want it when not using BC.
                no_condom_threshold -= 20

            return no_condom_threshold

        def wants_condom(self, situational_modifier = 0, use_taboos = True):
            taboo_modifier = 0
            if use_taboos and self.effective_sluttiness("condomless_sex") >= self.get_no_condom_threshold(situational_modifier = situational_modifier):
                return True
            elif self.effective_sluttiness() >= self.get_no_condom_threshold(situational_modifier = situational_modifier):
                return True
            else:
                return False

        def has_family_taboo(self): #A check to see if we should use an incest taboo modifier.
            if self.get_opinion_score("incest") > 0: #If she thinks incest is hot she doesn't have an incest taboo modifier. Maybe she should, but it should just be reduced? For now this is fine.
                return False

            elif self.is_family():
                return True

            return False

        def is_family(self):
            if any(relationship in [sister_role,mother_role,aunt_role,cousin_role] for relationship in self.special_role):
                return True

        def change_arousal(self,amount, add_to_log = True):
            self.arousal += __builtin__.round(amount) #Round it to an integer if it isn't one already.
            if self.arousal < 0:
                self.arousal = 0

            log_string = ""
            display_name = self.create_formatted_title("???")
            if self.title:
                display_name = self.title

            if amount > 0:
                log_string = display_name + ": +" + str(amount) + " Arousal"
            else:
                log_string = display_name + ": " + str(amount) + " Arousal"

            if add_to_log and amount != 0:
                mc.log_event(log_string, "float_text_red")

        def reset_arousal(self):
            self.arousal = 0

        def change_energy(self, amount, add_to_log = True):
            amount = __builtin__.round(amount)
            self.energy += amount
            if self.energy > self.max_energy:
                self.energy = self.max_energy
            elif self.energy < 0:
                self.energy = 0

            log_string = ""
            display_name = self.create_formatted_title("???")
            if self.title:
                display_name = self.title
            if amount > 0:
                log_string +=  display_name+ ": +" + str(amount) + " Energy"
            else:
                log_string +=  display_name + ": " + str(amount) + " Energy"
            if add_to_log and amount != 0:
                mc.log_event(log_string, "float_text_yellow")
            return

        def change_max_energy(self, amount ,add_to_log = True):
            amount = __builtin__.round(amount)
            self.max_energy += amount
            if self.max_energy < 0:
                self.max_energy = 0

            if self.energy > self.max_energy: #No having more energy than max
                self.energy = self.max_energy

            log_string = ""
            display_name = self.create_formatted_title("???")
            if self.title:
                display_name = self.title
            if amount > 0:
                log_string +=  display_name + ": +" + str(amount) + " Max Energy"
            else:
                log_string +=  display_name + ": " + str(amount) + " Max Energy"
            if add_to_log and amount != 0:
                mc.log_event(log_string, "float_text_yellow")
            return

        def has_large_tits(self): #Returns true if the girl has large breasts. "D" cups and up are considered large enough for titfucking, swinging, etc.
            if self.tits == "D" or self.tits == "DD" or self.tits == "DDD" or self.tits == "E" or self.tits == "F" or self.tits == "FF":
                return True
            else:
                return False

        def wants_creampie(self): #Returns True if the girl is going to use dialogue where she wants you to creampie her, False if she's going to be angry about it. Used to help keep dialogue similar throughout events
            creampie_threshold = 75
            effective_slut = the_person.effective_sluttiness("creampie") + (10*the_person.get_opinion_score("creampies"))
            if the_person.on_birth_control:
                effective_slut += -20 #Much more willing to let you creampie her if she's on BC

            if affair_role in the_person.special_role:
                effective_slut += 5 - (10 * the_person.get_opinion_score("cheating on men"))
            elif the_person.relationship != "Single": # Less likely to want to be creampied if she's in a relationship, but cares less if you're officially cheating.
                effective_slut += 15 - (10 * the_person.get_opinion_score("cheating on men"))

            if girlfriend_role in the_person.special_role:
                effective_slut += -(10 + (5*the_person.get_opinion_score("being submissive"))) #Desire to be a "good wife"

            if the_person.is_family():
                effective_slut += 10 - (10 * the_person.get_opinion_score("incest"))

            if effective_slut >= creampie_threshold or the_person.event_triggers_dict.get("preg_knows", False):
                return True

            return False

        def calculate_realistic_fertility(self):
            day_difference = self.days_from_ideal_fertility() # Gets the distance between the current day and the ideal fertile day.
            multiplier = 2 - (float(day_difference)/10.0) # The multiplier is 2 when the day difference is 0, 0.5 when the day difference is 15.
            effective_fertility = self.fertility_percent * multiplier
            return effective_fertility

        def days_from_ideal_fertility(self):
            day_difference = abs((day % 30) - self.ideal_fertile_day)
            if day_difference > 15:
                day_difference = 30 - day_difference #Wrap around to get correct distance between months.
            return day_difference

        def fertility_cycle_string(self): #Turns the difference of days from her ideal fertile day into a string
            day_difference = self.days_from_ideal_fertility
            if day_difference >= 12:
                return "Very Safe"
            elif day_difference >= 8:
                return "Safe"
            elif day_difference >= 3:
                return "Normal"
            else:
                return "Risky"

        def update_birth_control_knowledge(self, force_known_state = None, force_known_day = None): #Called any time a girl gives you information about her BC. Allows for an up to date detailed info screen that doesn't give more than you know
            if force_known_state is None: #Useful when you an event changes a girls BC and you can expect that she's not going to be on birth control the next day.
                known_state = self.on_birth_control

            if force_known_day is None:
                known_day = day

            self.event_triggers_dict["birth_control_status"] = known_state
            self.event_triggers_dict["birth_control_known_day"] = known_day


        def effective_sluttiness(self, taboos = None): #Used in sex scenes where the girl will be more aroused, making it easier for her to be seduced.
            if taboos is None:
                taboos = []
            elif not isinstance(taboos, list): #Handles handing over a single item without pre-wrapping it for "iteration".
                taboos = [taboos]
            return_amount = __builtin__.int(self.sluttiness + (self.arousal/4))

            for taboo in taboos:
                if taboo not in self.broken_taboos: #If any of the taboo handed over are not already broken this person has a -15 effective sluttiness.
                    return_amount += -10
                    break #Only appies once, so break once the mallus is applied.
            return return_amount

        def cum_in_mouth(self): #Add the appropriate stuff to their current outfit, and peform any personal checks if rquired.
            mc.listener_system.fire_event("sex_cum_mouth", the_person = self)
            if self.outfit.can_add_accessory(mouth_cum):
                the_cumshot = mouth_cum.get_copy()
                the_cumshot.layer = 0
                self.outfit.add_accessory(the_cumshot)

            self.change_slut_temp(5*self.get_opinion_score("drinking cum"))
            self.change_happiness(5*self.get_opinion_score("drinking_cum"))
            self.discover_opinion("drinking cum")

            self.sex_record["Cum in Mouth"] += 1


        def cum_in_vagina(self):
            mc.listener_system.fire_event("sex_cum_vagina", the_person = self)
            if self.outfit.can_add_accessory(creampie_cum):
                the_cumshot = creampie_cum.get_copy()
                the_cumshot.layer = 0
                self.outfit.add_accessory(the_cumshot)

            slut_change_amount = 5*self.get_opinion_score("creampies")

            if the_person.wants_creampie():
                self.change_happiness(5*self.get_opinion_score("creampies"))
            else:
                self.change_happiness(-5 + (5*self.get_opinion_score("creampies")))
                self.change_love(-2 + self.get_opinion_score("creampies"))
                slut_change_amount += 1 + self.get_opinion_score("being_submissive")

            self.change_slut_temp(slut_change_amount)
            self.discover_opinion("creampies")

            self.sex_record["Vaginal Creampies"] += 1

            # Pregnancy Check #
            if persistent.pregnancy_pref > 0 and pregnant_role not in self.special_role:
                if persistent.pregnancy_pref == 1 and self.on_birth_control: #Establish how likely her birth contorl is to work (if needed, and if present)
                    bc_percent = 100 - self.bc_penalty
                elif persistent.pregnancy_pref == 2 and self.on_birth_control:
                    bc_percent = 90 - self.bc_penalty
                else:
                    bc_percent = 0

                preg_chance = renpy.random.randint(0,100)
                bc_chance = renpy.random.randint(0,100)
                if persistent.pregnancy_pref == 2: # On realistic pregnancy a girls chance to become pregnant fluctuates over the month.
                    modified_fertility = self.calculate_realistic_fertility()
                else:
                    modified_fertility = self.fertility_percent

                if preg_chance < modified_fertility and pregnant_role not in self.special_role: #There's a chance she's pregnant
                    if bc_chance >= bc_percent : # Birth control failed to prevent the pregnancy
                        become_pregnant(self) #Function in role_pregnant establishes all of the pregnancy related variables and events.


        def cum_in_ass(self):
            mc.listener_system.fire_event("sex_cum_ass", the_person = self)
            #TODO: Add an anal specific cumshot once we have renders for it.
            if self.outfit.can_add_accessory(creampie_cum):
                the_cumshot = creampie_cum.get_copy()
                the_cumshot.layer = 0
                self.outfit.add_accessory(the_cumshot)
            self.change_slut_temp(5*self.get_opinion_score("creampies"))
            self.change_happiness(5*self.get_opinion_score("creampies"))
            self.discover_opinion("creampies")

            self.sex_record["Anal Creampies"] += 1

        def cum_on_face(self):
            if self.outfit.can_add_accessory(face_cum):
                the_cumshot = face_cum.get_copy()
                the_cumshot.layer = 0
                self.outfit.add_accessory(the_cumshot)

            self.change_slut_temp(5*self.get_opinion_score("cum facials"))
            self.change_happiness(5*self.get_opinion_score("cum facials"))
            self.discover_opinion("cum facials")

            self.change_slut_temp(5*self.get_opinion_score("being covered in cum"))
            self.change_happiness(5*self.get_opinion_score("being covered in cum"))
            self.discover_opinion("being covered in cum")

            self.sex_record["Cum Facials"] += 1

        def cum_on_tits(self):
            if self.outfit.can_add_accessory(tits_cum):
                the_cumshot = tits_cum.get_copy()
                if self.outfit.get_upper_visible():
                    top_layer = self.outfit.get_upper_visible()[0].layer #Get the top most pice of clothing and get it's layer.
                else:
                    top_layer = -1
                the_cumshot.layer = top_layer+1 #The cumshot lives on a layer it hit, above the one it hit. Accessories are drawn first in the hirearchy, so they have to be on a level higehr than what they hit.
                self.outfit.add_accessory(the_cumshot)

            self.change_slut_temp(5*self.get_opinion_score("being covered in cum"))
            self.change_happiness(5*self.get_opinion_score("being covered in cum"))
            self.discover_opinion("being covered in cum")

            self.sex_record["Cum Covered"] += 1

        def cum_on_stomach(self):
            if self.outfit.can_add_accessory(stomach_cum):
                the_cumshot = stomach_cum.get_copy()
                if self.outfit.get_upper_visible():
                    top_layer = self.outfit.get_upper_visible()[0].layer #Get the top most pice of clothing and get it's layer.
                else:
                    top_layer = -1
                the_cumshot.layer = top_layer+1 #The cumshot lives on a layer it hit, above the one it hit. Accessories are drawn first in the hirearchy, so they have to be on a level higehr than what they hit.
                self.outfit.add_accessory(the_cumshot)

            self.change_slut_temp(5*self.get_opinion_score("being covered in cum"))
            self.change_happiness(5*self.get_opinion_score("being covered in cum"))
            self.discover_opinion("being covered in cum")

            self.sex_record["Cum Covered"] += 1

        def cum_on_ass(self):
            if self.outfit.can_add_accessory(ass_cum):
                the_cumshot = ass_cum.get_copy()
                if self.outfit.get_lower_visible():
                    top_layer = self.outfit.get_lower_visible()[0].layer #Get the top most pice of clothing and get it's layer.
                else:
                    top_layer = -1
                the_cumshot.layer = top_layer+1 #The cumshot lives on a layer it hit, above the one it hit. Accessories are drawn first in the hirearchy, so they have to be on a level higehr than what they hit.
                self.outfit.add_accessory(the_cumshot)

            self.change_slut_temp(5*self.get_opinion_score("being covered in cum"))
            self.change_happiness(5*self.get_opinion_score("being covered in cum"))
            self.discover_opinion("being covered in cum")

            self.sex_record["Cum Covered"] += 1

        def change_salary(self, amount, add_to_log = True):
            amount = __builtin__.round(amount)
            self.salary += amount
            if self.salary < 0:
                self.salary = 0

            log_string = ""
            display_name = self.create_formatted_title("???")
            if self.title:
                display_name = self.title
            if amount > 0:
                log_string = display_name + ": +$" + str(amount) + "/Day"
            else:
                log_string = display_name + ": -$" + str(-amount) + "/Day"

            if add_to_log and amount != 0:
                mc.log_event(log_string, "float_text_green")

        def calculate_base_salary(self): #returns the default value this person should be worth on a per day basis.
            return (self.int + self.focus + self.charisma)*2 + (self.hr_skill + self.market_skill + self.research_skill + self.production_skill + self.supply_skill)

        def set_work(self, the_location, work_days = None, work_times = None): #Sets the person's schedule so they visit their location at those times.
            if work_days is None:
                work_days = [0,1,2,3,4] #Standard values
            if work_times is None:
                work_times = [1,2,3] #Standard values

            if the_location is None: #Setting Location as None clears their work schedule completely
                for the_day in range(0,7):
                    for the_time in range(0,5):
                        if self.schedule[the_day][the_time] == self.work:
                            self.schedule[the_day][the_time] = None

            else:
                self.set_schedule(the_location, work_days, work_times) #Set them to work M-F, morning till afternoon

            self.work = the_location

        def set_schedule(self, the_location, days = None, times = None):
            if days is None:
                days = [0,1,2,3,4,5,6] #Full week if not specified
            if times is None:
                times = []

            for the_day in days:
                for time_chunk in times:
                    self.schedule[the_day][time_chunk] = the_location

        def get_desination(self, specified_day = None, specified_time = None):
            if specified_day is None:
                specified_day = day%7 #Today
            if specified_time is None:
                specified_time = time_of_day #Now
            return self.schedule[specified_day][specified_time] #Returns the Room this person should be in during the specified time chunk.


        def person_meets_requirements(self, slut_required = 0, core_slut_required = 0, obedience_required = 0, obedience_max = 2000, love_required = -200):
            if self.sluttiness >= slut_required and self.core_sluttiness >= core_slut_required and self.obedience >= obedience_required and self.obedience <= obedience_max and self.love >= love_required:
                return True
            return False

        def valid_role_actions(self):
            count = 0
            for role in self.special_role:
                for act in role.actions:
                    if act.is_action_enabled(self) or act.is_disabled_slug_shown(self): #We should also check if a non-action disabled slug would be available so that the player can check what the requirement would be.
                        count += 1
                return count


        def create_formatted_title(self, the_title):
            formatted_title = "{color=" + self.char.who_args["color"] + "}" + "{font=" + self.char.what_args["font"] + "}" + the_title + "{/font}{/color}"
            return formatted_title

        def set_title(self, new_title): #Takes the given title and formats it so that it will use the characters font colours when the_person.title is used.
            self.char.name = new_title #This ensures the dialogue name is correct for the new title.
            self.title = self.create_formatted_title(new_title)

        def set_possessive_title(self, new_title):
            self.possessive_title = self.create_formatted_title(new_title)

        def set_mc_title(self, new_title):
            self.mc_title = new_title

        def personalise_text(self, what):
            for text_modifier in self.text_modifiers:
                what = text_modifier(self, what)

            return what

        def add_role(self, the_role):
            self.special_role.append(the_role)

        def remove_role(self, the_role, remove_all = False, remove_linked = True):
            if the_role in self.special_role:
                self.special_role.remove(the_role)
                if remove_linked:
                    for linked_role in the_role.linked_roles:
                        self.remove_role(linked_role, remove_all, remove_linked)
                if remove_all:
                    self.remove_role(the_role, remove_all, remove_linked)

        def has_role(self, the_role):
            if the_role in self.special_role:
                return True
            else:
                return False

        def get_role_reference_by_name(self, the_role):
            for role in self.special_role:
                if role.role_name == the_role:
                    return role
            return None

        def add_infraction(self, the_infraction, add_to_log = True, require_policy = True):
            if office_punishment.is_active() or not require_policy:
                self.infractions.append(the_infraction)
                if add_to_log:
                    display_name = self.create_formatted_title("???")
                    if self.title:
                        display_name = self.title
                    mc.log_event(display_name + " committed infraction: " + the_infraction.name + ", Severity " + str(the_infraction.severity), "float_text_grey")

        def remove_infraction(self, the_infraction):
            if the_infraction in self.infractions:
                self.infractions.remove(the_infraction)

    class Personality(): #How the character responds to various actions
        def __init__(self, personality_type_prefix, default_prefix = None,
            common_likes = None, common_dislikes = None, common_sexy_likes = None, common_sexy_dislikes = None,
            titles_function = None, possessive_titles_function = None, player_titles_function = None,
            insta_chance = 0, dikdok_chance = 0):

            self.personality_type_prefix = personality_type_prefix
            self.default_prefix = default_prefix

            self.titles_function = titles_function
            self.possessive_titles_function = possessive_titles_function
            self.player_titles_function = player_titles_function

            self.insta_chance = insta_chance
            self.dikdok_chance = dikdok_chance
            #NOTE: Girls never generate with Onlyfans naturally

            #These are the labels we will be trying to get our dialogue. If the labels do not exist we will get their defaults instead. A default should _always_ exist, if it does not our debug check will produce an error.
            self.response_label_ending = ["greetings",
            "sex_responses_foreplay", "sex_responses_oral", "sex_responses_vaginal", "sex_responses_anal",
            "climax_responses_foreplay", "climax_responses_oral", "climax_responses_vaginal", "climax_responses_anal",
            "clothing_accept", "clothing_reject", "clothing_review",
            "strip_reject", "strip_obedience_accept", "grope_body_reject", "sex_accept", "sex_obedience_accept", "sex_gentle_reject", "sex_angry_reject",
            "seduction_response", "seduction_accept_crowded", "seduction_accept_alone", "seduction_refuse",
            "flirt_response", "flirt_response_low", "flirt_response_mid", "flirt_response_high", "flirt_response_girlfriend", "flirt_response_affair", "flirt_response_text",
            "cum_face", "cum_mouth", "cum_pullout", "cum_condom", "cum_vagina", "cum_anal", "suprised_exclaim", "talk_busy",
            "improved_serum_unlock", "sex_strip", "sex_watch", "being_watched", "work_enter_greeting", "date_seduction", "sex_end_early", "sex_take_control", "sex_beg_finish", "sex_review" ,"introduction",
            "kissing_taboo_break", "touching_body_taboo_break", "touching_penis_taboo_break", "touching_vagina_taboo_break", "sucking_cock_taboo_break", "licking_pussy_taboo_break", "vaginal_sex_taboo_break", "anal_sex_taboo_break",
            "condomless_sex_taboo_break", "underwear_nudity_taboo_break", "bare_tits_taboo_break", "bare_pussy_taboo_break",
            "facial_cum_taboo_break", "mouth_cum_taboo_break", "body_cum_taboo_break", "creampie_taboo_break", "anal_creampie_taboo_break"]

            self.response_dict = {}
            for ending in self.response_label_ending:
                if renpy.has_label(self.personality_type_prefix + "_" + ending):
                    self.response_dict[ending] = self.personality_type_prefix + "_" + ending
                elif default_prefix is not None: #A default is used when one personality is similar to anouther and has only specific responses overwritten (ex. Stephanie is a modified wild personality).
                    self.response_dict[ending] = self.default_prefix + "_" + ending
                else:
                    self.response_dict[ending] = "relaxed_" + ending #If nothing is given we assume we don't want to crash and we should put in some sort of value.



            #Establish our four classes of favoured likes and dislikes. Intensity (ie. love vs like, dislike vs hate) is decided on a person to person basis.
            if common_likes:
                self.common_likes = common_likes
            else:
                self.common_likes = []

            if common_sexy_likes:
                self.common_sexy_likes = common_sexy_likes
            else:
                self.common_sexy_likes = []

            if common_dislikes:
                self.common_dislikes = common_dislikes
            else:
                self.common_dislikes = []

            if common_sexy_dislikes:
                self.common_sexy_dislikes = common_sexy_dislikes
            else:
                self.common_sexy_dislikes = []

        def get_dialogue(self, the_person, type, **extra_args):
            renpy.call(self.response_dict[type], the_person, **extra_args)
            return

        def generate_default_opinion(self):
            if renpy.random.randint(1,2) == 1:
                #Positive
                degree = renpy.random.randint(1,2)
                the_key = get_random_from_list(self.common_likes)
                return (the_key,[degree,False])

            else:
                #Negative
                degree = renpy.random.randint(-2,-1)
                the_key = get_random_from_list(self.common_dislikes)
                return (the_key,[degree,False])


        def generate_default_sexy_opinion(self):
            if renpy.random.randint(1,2) == 1:
                #Positive
                degree = renpy.random.randint(1,2)
                the_key = get_random_from_list(self.common_sexy_likes)
                return (the_key,[degree,False])

            else:
                #Negative
                degree = renpy.random.randint(-2,-1)
                the_key = get_random_from_list(self.common_sexy_dislikes)
                return (the_key,[degree,False])

        def get_personality_titles(self, the_person): #This should be a function defined for each
            if self.titles_function:
                return self.titles_function(the_person)
            else:
                return the_person.name

        def get_personality_possessive_titles(self, the_person):
            if self.possessive_titles_function:
                return self.possessive_titles_function(the_person)
            else:
                return the_person.name

        def get_personality_player_titles(self, the_person):
            if self.player_titles_function:
                return self.player_titles_function(the_person)
            else:
                return the_person.name


    def make_person(): #This will generate a person, using a pregen body some of the time if they are available.
        split_proportion = 20 #1/5 characters generated will be a premade character.
        return_character = None
        if renpy.random.randint(1,100) < split_proportion:
            return_character = get_premade_character()

        if return_character is None: #Either we aren't getting a premade, or we are out of them.
            return_character = create_random_person()
        return return_character

    # create_random_person is used to generate a Person object from a list of random or provided stats. use "make_a_person" to properly get premade characters mixed with randoms.
    def create_random_person(name = None, last_name = None, age = None, body_type = None, face_style = None, tits = None, height = None,
        hair_colour = None, hair_style = None, pubes_colour = None, pubes_style = None, skin = None, eyes = None, job = None,
        personality = None, custom_font = None, name_color = None, dial_color = None, starting_wardrobe = None, stat_array = None, skill_array = None, sex_array = None,
        start_sluttiness = None, start_obedience = None, start_happiness = None, start_love = None, start_home = None,
        title = None, possessive_title = None, mc_title = None, relationship = None, kids = None, SO_name = None, base_outfit = None,
        generate_insta = None, generate_dikdok = None, generate_onlyfans = None):

        if personality is None:
            personality = get_random_personality()

        if generate_insta is None:
            if renpy.random.randint(0,100) < personality.insta_chance:
                generate_insta = True
            else:
                generate_insta = False

        if generate_dikdok is None:
            if renpy.random.randint(0,100) < personality.dikdok_chance:
                generate_dikdok = True
            else:
                generate_dikdok = False

        if generate_onlyfans is None:
            generate_onlyfans = False


        if name is None:
            name = get_random_name()
        if last_name is None:
            last_name = get_random_last_name()
        if age is None:
            age = renpy.random.randint(18,50)
        if body_type is None:
            body_type = get_random_body_type()
        if tits is None:
            tits = get_random_tit()
        if height is None:
            height = 0.9 + (renpy.random.random()/10)

        if hair_colour is None: #If we pass nothing we can pick a random hair colour
            hair_colour = generate_hair_colour() #Hair colour is a list of [string, [colour]], generated with variations by this function,
        elif isinstance(hair_colour, basestring):
            hair_colour = generate_hair_colour(hair_colour) #If we pass a string assume we want to generate a variation based on that colour.
        #else: we assume a full colour list was passed and everything is okay.

        if hair_style is None:
            hair_style = get_random_from_list(hair_styles).get_copy()
        else:
            hair_style = hair_style.get_copy() #Get a copy so we don't modify the master.

        hair_style.colour = hair_colour[1]

        if pubes_style is None:
            pubes_style = get_random_from_list(pube_styles).get_copy()

        pubes_colour = get_darkened_colour(hair_colour[1])
        pubes_style.colour = pubes_colour

        if eyes is None:
            eyes = generate_eye_colour()
        elif isinstance(eyes, basestring):
            eyes = generate_eye_colour(eyes) #If it's a string assume we want a variation within that eye catagory
        # else: we assume at this point what was passed is a correct [description, colour] list.

        if skin is None:
            skin = get_random_skin()
        if face_style is None:
            face_style = get_random_face()
        if skin == "white":
            body_images = white_skin
        elif skin == "tan":
            body_images = tan_skin
        else:
            body_images = black_skin

        emotion_images = Expression(name+"\'s Expression Set", skin, face_style)

        if eyes is None:
            eyes = get_random_eye()

        if job is None:
            job = get_random_job()


        if custom_font is None:
            #Get a font
            my_custom_font = get_random_font()

        if name_color is None:
            # Get a color
            name_color = get_random_readable_color()

        if dial_color is None:
            # Use name_color
            dial_color = copy.copy(name_color) #Take a copy

        skill_cap = 5
        stat_cap = 5

        if recruitment_skill_improvement_policy.is_active():
            skill_cap += 2

        if recruitment_stat_improvement_policy.is_active():
            stat_cap += 2

        if skill_array is None:
            skill_array = [renpy.random.randint(1,skill_cap),renpy.random.randint(1,skill_cap),renpy.random.randint(1,skill_cap),renpy.random.randint(1,skill_cap),renpy.random.randint(1,skill_cap)]

        if stat_array is None:
            stat_array = [renpy.random.randint(1,stat_cap),renpy.random.randint(1,stat_cap),renpy.random.randint(1,stat_cap)]

        if sex_array is None:
            sex_array = [renpy.random.randint(0,5),renpy.random.randint(0,5),renpy.random.randint(0,5),renpy.random.randint(0,5)]

        if start_love is None:
            start_love = 0

        if start_happiness is None:
            start_happiness = 100 + renpy.random.randint(-10,10)

        start_suggest = 0

        if start_obedience is None:
            start_obedience = renpy.random.randint(-10,10)

        if recruitment_obedience_improvement_policy.is_active():
            start_obedience += 10

        if start_sluttiness is None:
            start_sluttiness = renpy.random.randint(0,10)

        if recruitment_slut_improvement_policy.is_active():
            start_sluttiness += 20

        if relationship is None:
            relationship = get_random_from_weighted_list([["Single",120-age],["Girlfriend",50],["Fiancée",120-(age*2)],["Married",20+(age*4)]]) #Age plays a major factor.

        if starting_wardrobe is None:
            starting_wardrobe = Wardrobe(name +"'s Wardrobe")
            starting_wardrobe = starting_wardrobe.merge_wardrobes(default_wardrobe.get_random_selection(25))

        if base_outfit is None:
            base_outfit = Outfit(name + "'s base accessories")
            if relationship == "Fiancée" or relationship == "Married":
                base_outfit.add_accessory(diamond_ring.get_copy())

            if renpy.random.randint(0,100) < age:
                #They need/want glasses.
                the_glasses = None
                if renpy.random.randint(0,100) < 50:
                    the_glasses = modern_glasses.get_copy()
                else:
                    the_glasses = big_glasses.get_copy()
                the_glasses.colour = get_random_glasses_frame_colour()
                base_outfit.add_accessory(the_glasses)

        if kids is None:
            kids = 0
            if age >=28:
                kids += renpy.random.randint(0,1) #Young characters don't have as many kids

            if age >= 38:
                kids += renpy.random.randint(0,1) #As you get older you're more likely to have one

            if relationship == "Girlfriend":
                kids += renpy.random.randint(0,1) #People who are dating have kids more often than single people

            elif relationship != "Single":
                kids += renpy.random.randint(0,3) #And married/engaged people have more kids still

            if age <= 22:
                kids += -1 #Young people have less time to have kids in general, so modify their number down a bit.
                if kids < 0:
                    kids = 0

        if SO_name is None and relationship != "Single":
            SO_name = get_random_male_name()

        return Person(name,last_name,age,body_type,tits,height,body_images,emotion_images,hair_colour,hair_style,pubes_colour,pubes_style,skin,eyes,job,starting_wardrobe,personality,
            stat_array,skill_array,sex_list=sex_array,sluttiness=start_sluttiness,obedience=start_obedience,suggest=start_suggest, love=start_love, happiness=start_happiness, home = start_home,
            font = my_custom_font, name_color = name_color , dialogue_color = dial_color,
            face_style = face_style,
            title = title, possessive_title = possessive_title, mc_title = mc_title,
            relationship = relationship, kids = kids, SO_name = SO_name, base_outfit = base_outfit,
            generate_insta = generate_insta, generate_dikdok = generate_dikdok, generate_onlyfans = generate_onlyfans)

    class GroupDisplayManager(renpy.store.object):
        default_shift_amount = 0.15
        adjust_per_person = 0.05
        def __init__(self, group_of_people, primary_speaker = None):
            self.group_of_people = group_of_people #First person in the list is drawn on the left size, with new people being added to the right
            if primary_speaker is not None and primary_speaker in self.group_of_people:
                self.primary_speaker = primary_speaker
            else:
                self.primary_speaker = group_of_people[0]

            self.last_draw_commands = {} # Tracks the list of arguments for the last draw_person or draw_animated_removal called for a person, sorted by character_number. Allows for characters to be redrawn when they are moved behind a new primary.

        def add_person(self, the_person, make_primary = False): #Add a person to the character list. Doesn't provoke a redraw automatically.
            if the_person not in self.group_of_people:
                self.group_of_people.append(the_person)

            if make_primary:
                self.primary_speaker = the_person

        def remove_person(self, the_person, new_primary = None): #Remove the_person from the list of people being drawn. Does not redraw (call redraw_group for that)
            if the_person in self.group_of_people:
                self.group_of_people.remove(the_person)
                if the_person is self.primary_speaker:
                    self.primary_speaker = None
                if the_person.character_number in self.last_draw_commands:
                    del self.last_draw_commands[the_person.character_number]

            if new_primary is not None:
                self.set_primary(the_person)

        def set_primary(self, the_person): #Note: Does not redraw #TODO: maybe it should?
            if the_person in self.group_of_people:
                self.primary_speaker = the_person

        def pick_arbitrary_primary(self): #Picks a new primary if none exists (because they have left, for example). Usually not needed, events should manage who is primary themselves.
            if len(self.group_of_people) > 0: #If there's nobody in the group by definition there is no primary.
                self.set_primary(get_random_from_list(self.group_of_people))

        # NOTE: It is most convenient to pass everything through as a key word argument, to avoid issues with normally defaulted arguments inside of draw_person or draw_animated_removal eating them as the wrong argument.
        def draw_person(self, the_person, make_primary = True, *args, **kwargs): #Seperate accessor methods to maintain consistency between group and single draws, while keeping all similar code in one place.
            self.last_draw_commands[the_person.character_number] = [args, kwargs]
            self.do_draw(the_person, Person.draw_person, make_primary, *args, **kwargs)

        def draw_animated_removal(self, the_person, make_primary = True, *args, **kwargs): #Removal draws need to have some arguments removed so we can redraw the character without redrawing the clothing removal
            # Remove animated_removal specific arguments so we can store a "draw_person" compatable set of arguments

            last_args = [] #Note: We are assuming all parameter are passed through as key words
            last_kwargs = kwargs.copy() #Note this is a shallow copy, so no copies of clothing items, ect are being made.
            if "half_off_instead" in last_kwargs:
                del last_kwargs["half_off_instead"] #Technically this could also be provided inside of args, but in practice that is a massive number of items to specify.
            if "the_clothing" in last_kwargs:
                del last_kwargs["the_clothing"]

            self.last_draw_commands[the_person.character_number] = [last_args, last_kwargs]
            self.do_draw(the_person, Person.draw_animated_removal, make_primary, *args, **kwargs)

        def draw_group(self, *args, **kwargs): #Draws every member in the group. Parameters passed are applied to everyone in the group. Draw one person at a time if you need that level of control.
            clear_scene() #We can assume we are clearing the scene if we are drawing a group.
            for group_member in self.group_of_people:
                self.draw_person(group_member, False, *args, **kwargs)

        def redraw_person(self, the_person, make_primary = True): # Draws the_person using the last recorded set of draw commands. Useful to redraw people as primary speaker change but their position does not.
            the_args, the_kwargs = self.last_draw_commands.get(the_person.character_number, [[],{}]) #If we have drawn them before reuse those parameters.
            self.draw_person(the_person, make_primary, *the_args, **the_kwargs)


        def redraw_group(self): #Attemps to redraw everyone in the group using hte last known set of draw commands. Useful when you add in a new person or someone's spacing changes
            clear_scene()
            for group_member in self.group_of_people:
                self.redraw_person(group_member, make_primary = False)

        def do_draw(self, the_person, the_draw_method, make_primary = True, *args, **kwargs): # Holds all of the similar code for all group based drawing methods (ie. passes through all information, keeping what is needed to redraw a character)
            #TODO: have the positioning account for different position widths.
            if self.primary_speaker is None: #Ensure there is always technically a primary, even if one was just removed.
                self.pick_arbitrary_primary()

            if make_primary and the_person is not self.primary_speaker: #We're replacing the primary speaker, so we need to redraw them into the background
                old_primary = self.primary_speaker
                self.set_primary(the_person)
                last_args, last_kwargs = self.last_draw_commands.get(old_primary.character_number, [[],{}]) #Get the last arguments provided.
                #last_kwargs["display_zorder"] = None #Ensures their z-position is reset and drawn properly #TODO: This is going to fuck with manually set z-levels, but we don't have a good way of dealing with that.
                self.draw_person(old_primary, make_primary = False, *last_args, **last_kwargs) #Redraw the character in their previous state, but now in the background.

            character_index = self.group_of_people.index(the_person)
            primary_index = self.group_of_people.index(self.primary_speaker)



            if len(self.group_of_people) > 1:
                posible_shift_amount = GroupDisplayManager.default_shift_amount + (GroupDisplayManager.adjust_per_person*len(self.group_of_people))
                shift_amount = 1.0 - (posible_shift_amount/(len(self.group_of_people)-1))*(character_index+1/len(self.group_of_people))
            else:
                shift_amount = 1.0

            scale_amount = 1.0
            if character_index != primary_index: #Scale down everyone who isn't the primary
                scale_amount = 0.8


            z_level = -abs(character_index - primary_index)
            # When drawing a character they are only animated if they are one of the 2 closest people to the primary speaker.
            # Note that they _stay_ animated even if the primary changes; It is almost identical to just redraw the entire group for most groups of size 5 or so.
            if primary_index == 0 or primary_index == len(self.group_of_people): #Side position primary, only animate them and 2 slots away
                if z_level < -2:
                    kwargs["the_animation"] = no_animation
            else: #Some middle psoition primary
                if z_level < -1: # Only animate characters on either side from the primary speaker.
                    kwargs["the_animation"] = no_animation

            if kwargs.get("display_transform", None) is None: # If the event specifies a specific display transform let it override (and trust the event to handle multi-person display somehow), otherwise, apply a position shift
                kwargs["display_transform"] = position_shift(shift_amount, scale_amount)

            if kwargs.get("display_zorder", None) is None:
                kwargs["display_zorder"] = z_level

            if kwargs.get("wipe_scene", None) is None:
                kwargs["wipe_scene"] = False #Don't clear the scene of other characters, we need them to remain so the whole group can be drawn/redrawn.

            the_draw_method(the_person, *args, **kwargs)



    def height_to_string(the_height): #Height is a value between 0.9 and 1.0 which corisponds to 5' 0" and 5' 10"
        rounded_height = __builtin__.round(the_height,2) #Round height to 2 decimal points.
        if rounded_height >= 1.00:
            return "5' 10\""
        elif rounded_height == 0.99:
            return "5' 9\""
        elif rounded_height == 0.98:
            return "5' 8\""
        elif rounded_height == 0.97:
            return "5' 7\""
        elif rounded_height == 0.96:
            return "5' 6\""
        elif rounded_height == 0.95:
            return "5' 5\""
        elif rounded_height == 0.94:
            return "5' 4\""
        elif rounded_height == 0.93:
            return "5' 3\""
        elif rounded_height == 0.92:
            return "5' 2\""
        elif rounded_height == 0.91:
            return "5' 1\""
        elif rounded_height <= 0.90:
            return "5' 0\""
        else:
            return "Problem, height not found in chart."

    class Expression(renpy.store.object):
        def __init__(self,name,skin_colour,facial_style):
            self.name = name
            self.skin_colour = skin_colour
            self.facial_style = facial_style #The style of face the person has, currently creatively named "Face_1", "Face_2", "Face_3", etc..
            self.emotion_set = ["default","happy","sad","angry","orgasm"]
            self.positions_set = ["stand2","stand3","stand4","stand5","walking_away","kissing","missionary","blowjob","against_wall","back_peek","sitting","kneeling1","standing_doggy","cowgirl"] #The set of images we are going to draw emotions for. These are positions that look towards the camera
            self.special_modifiers = {"kissing":["kissing"]} #Special modifiers that are sometimes applied to expressions, but not always. ie. for blowjobs that may be either in normal crouching mode or blowjob mode.
            self.ignore_position_set = ["doggy","walking_away","standing_doggy"] #The set of positions that we are not goign to draw emotions for. These look away from the camera TODO: This should reference the Position class somehow.
            self.position_dict = {}
            for position in self.positions_set: #All positions support the blowjob special modifier now.
                if position in self.special_modifiers.keys():
                    self.special_modifiers[position].extend(["blowjob"])
                else:
                    self.special_modifiers[position] = ["blowjob"]

            for position in self.positions_set+self.ignore_position_set:
                self.position_dict[position] = {}

            for position in self.positions_set:
                for emotion in self.emotion_set:
                    self.position_dict[position][emotion] = emotion + "_" + facial_style + "_" + position + "_" + skin_colour + ".png"

            for position in self.ignore_position_set: #Positions that ignore emotions always use the "default" emotion for the back of the head.
                for emotion in self.emotion_set:
                    self.position_dict[position][emotion] = "default" + "_" + facial_style + "_" + position + "_" + skin_colour + ".png" ##An empty image to be drawn when we don't want to draw any emotion, because the character's face is turned away.

            for position, modifiers in self.special_modifiers.iteritems(): #Position is the key of our special modifers dict, get all the positions with a special modifier assigned.
                for modifier in modifiers: #If that position has multiple special modifers we want to add them all.
                    for emotion in self.emotion_set:
                        modified_emotion = emotion + "_" + modifier
                        self.position_dict[position][modified_emotion] = modified_emotion + "_" + facial_style + "_" + position + "_" + skin_colour + ".png"#Add a new emotion titled "<emotion>_<modifier>", for example "sad_blowjob".


        def generate_emotion_displayable(self,position,emotion, special_modifier = None, eye_colour = None, lighting = None):

            if not position in self.positions_set+self.ignore_position_set:
                position = "stand3"
            if not emotion in self.emotion_set:
                emotion = "default" #Get our default emotion to show if we get an incorrect one.
            elif special_modifier is not None and special_modifier in self.special_modifiers:
                emotion = emotion + "_" + special_modifier

            if lighting is None:
                lighting = [1,1,1]

            if eye_colour is None:
                eye_colour = [0.8,0.8,0.8,1] #grey by default.

            # if renpy.mobile or test_zip: #On mobile platforms we use .zip files to hold all of the individual images to bypass the andorid file limit. This results in significantly slower animation (for reasons currently unknown), but android douesn't animate anyways.

            base_name = self.position_dict[position][emotion]
            base_image = VrenZipImage(position, base_name)

            mask_name = self.position_dict[position][emotion].replace("_" + self.skin_colour,"_Pattern_1")
            mask_image = VrenZipImage(position, mask_name)

            # else:
            #     base_name = "character_images/" + self.position_dict[position][emotion]
            #     base_image = Image(base_name)
            #
            #     mask_name = base_name.replace("_" + self.skin_colour,"_Pattern_1") # Match the naming scheme used for the eye patterns.
            #     mask_image = Image(mask_name)



            inverted_mask_image = im.MatrixColor(mask_image, [1,0,0,0,0, 0,1,0,0,0, 0,0,1,0,0, 0,0,0,-1,1])
            #mask_image = im.MatrixColor(mask_image, [1,0,0,0,0, 0,1,0,0,0, 0,0,1,0,0, 0,0,0,1,0]) #Does this even do anything??? #TODO: Check that this does something. (Might have been used to ensure image values were capped properly)

            colour_pattern_matrix = im.matrix.tint(eye_colour[0], eye_colour[1], eye_colour[2]) * im.matrix.tint(*lighting)
            shader_pattern_image = im.MatrixColor(base_image, colour_pattern_matrix)

            base_image = im.MatrixColor(base_image, im.matrix.tint(*lighting)) #To support the lighting of the room we also retint it here.
            final_image = AlphaBlend(mask_image, base_image, shader_pattern_image, alpha=False)

            return final_image

    class Relationship(): #A class used to store information about the relationship between two people. Do not manipulate directly, use RelationshipArray to change things.
        def __init__(self, person_a, person_b, type_a, type_b = None, visible = None):
            self.person_a = person_a #Person a and b are Person objects.
            self.person_b = person_b
            self.type_a = type_a #person_a TO person_b, written so you could tell what person_b is if you listed them. Ie. "Lily - Daughter".
            if type_b is None: #Type can vary depending on what direction you view the relationship ie. mother-daughter, employee-boss.
                self.type_b = type_a
            else:
                self.type_b = type_b

            if visible is None:
                self.visible = True
            else:
                self.visible = visible

        def get_other_person(self, the_person): #Used to make it simpler to get a relationship for one person and know who the "other" person is.
            if the_person == self.person_a:
                return self.person_b
            elif the_person == self.person_b:
                return self.person_a
            else:
                return None #In theory this shouldn't come up unless this class is being abused in some way. (But some classes are into that sort of thing. I don't judge)

        def get_type(self, the_person = None):
            if the_person is None or the_person == self.person_a:
                return self.type_a
            elif the_person == self.person_b:
                return self.type_b

    class RelationshipArray():
        def __init__(self):
            self.relationships = [] #List of relationships. Relationships are bi-directional, so if you look for person_a, person_b you'll get the same object as person_b, person_a (but the type can be relative to the order).
            ### Types of Relationships (* denotes currently unused but planned roles)
            # Family: Mother, Daughter, Cousin, Niece, Aunt, Grandmother*, Granddaughter*
            # Positive: Acquaintance, Friend, Best Friend, Girlfriend*, Fiancée*, Wife*
            # Negative: Rival, Nemesis*

        def update_relationship(self, person_a, person_b, type_a, type_b = None, visible = None): #Note that type_a is required, but if you want to do just one half of a relationship you can flip the person order around.
            if person_a is person_b: #Don't form relationships with yourself!
                return

            the_relationship = self.get_relationship(person_a, person_b)
            if the_relationship is None: #No relationship exists yet, make one.
                self.relationships.append(Relationship(person_a, person_b, type_a, type_b, visible))

            else: #A relationship exists, update it to the new state.
                if person_a == the_relationship.person_a: #Relationships may have been refered to in the opposite order, so flip the references around if needed.
                    if type_a is not None:
                        the_relationship.type_a = type_a

                    if type_b is None:
                        the_relationship.type_b = type_a
                    else:
                        the_relationship.type_b = type_b

                elif person_a == the_relationship.person_b:
                    if type_a is not None:
                        the_relationship.type_b = type_a

                    if type_b is None:
                        the_relationship.type_a = type_a
                    else:
                        the_relationship.type_a = type_b

                if visible is not None:
                    the_relationship.visible = visible


        def get_relationship(self, person_a, person_b):
            for relationship in self.relationships:
                if (relationship.person_a == person_a and relationship.person_b == person_b) or (relationship.person_a == person_b and relationship.person_b == person_a):
                    return relationship #If we find a relationship containing the same two people (but perhaps with their position inverted) return it.

            return None #Otherwise these people have no relationship.

        def get_relationship_list(self, the_person, types = None, visible = None):
            return_list = []
            if isinstance(types, basestring):
                types = [types]
            for relationship in self.relationships:
                if (the_person == relationship.person_a and (types is None or relationship.type_a in types)) or (the_person == relationship.person_b and (types is None or relationship.type_b in types)): #What type we are looking at depends on if this is person A or B.
                    if visible is None or visible == relationship.visible:
                        return_list.append(relationship)

            return return_list

        def get_relationship_type_list(self, the_person, types = None, visible = None):
            return_list = []
            if isinstance(types, basestring):
                types = [types]
            for relationship in self.get_relationship_list(the_person, types, visible):
                return_list.append([relationship.get_other_person(the_person), self.get_relationship_type(the_person, relationship.get_other_person(the_person))]) #Creates a tuple of [Person, Type] for every entry in the list.
            return return_list

        def get_business_relationships(self, types = None): #Returns a list containing all relationships between people in your company.
            return_list = []
            if isinstance(types, basestring):
                types = [types]
            employee_list = mc.business.get_employee_list()
            for person in employee_list:
                for relationship in self.get_relationship_list(person, types):
                    if relationship.get_other_person(person) in employee_list and relationship not in return_list:
                        return_list.append(relationship)
            return return_list


        def get_relationship_type(self, person_a, person_b): #Note that getting relationship for (person_a, person_b) may yield a different result from (person_b, person_a), because the perspective is different.
            the_relationship = self.get_relationship(person_a, person_b)
            if the_relationship is not None:
                return the_relationship.get_type(person_a)
            else:
                return None

        def get_existing_children(self, the_person):
            return_list = []
            for relationship in self.get_relationship_type_list(the_person):
                if relationship[1] == "Daughter": #The only people we keep track of as characters are women, so the only child relationships we care about are daughters
                    return_list.append(relationship[0])
            return return_list

        def get_existing_child_count(self, the_person): #Returns a count of how many children this character has who are "real" characters, vs just a stat.
            return len(self.get_existing_children(the_person))

        def remove_all_relationships(self, the_person): #Clears this person out of the relationship database (if, for example, we want to delete a person from the game)
            for relationship in self.get_relationship_list(the_person):
                self.relationship.remove(relationship)

        def improve_relationship(self, person_a, person_b, visible = None): #Improves a non-familial relationship between the two people.
            the_relationship = self.get_relationship(person_a, person_b)
            if the_relationship is not None: #If it exists we're going to improve it by one step, up to best friend.
                the_type = the_relationship.get_type()
                relationship_scale = ["Nemesis", "Rival", "Acquaintance", "Friend", "Best Friend"]
                if the_type in relationship_scale: #You can only change non-family and non-romantic relationships like this.
                    the_state = relationship_scale.index(the_type)
                    the_state += 1
                    if the_state+1 >= len(relationship_scale): #Get the current state and increase it by one.
                        the_state = len(relationship_scale)-1

                    self.update_relationship(person_a,person_b, relationship_scale[the_state], visible)

            else:
                self.update_relationship(person_a, person_b, "Acquaintance", visible)

        def worsen_relationship(self, person_a, person_b, visible = None): #Worsens a non-familial relationship between two people
            the_relationship = self.get_relationship(person_a, person_b)
            if the_relationship is not None: #If it exists we're going to improve it by one step, up to best friend.
                the_type = the_relationship.get_type()
                relationship_scale = ["Nemesis", "Rival", "Acquaintance", "Friend", "Best Friend"]
                if the_type in relationship_scale: #You can only change non-family and non-romantic relationships like this.
                    the_state = relationship_scale.index(the_type)
                    the_state -= 1
                    if the_state < 0: #Get the current state and increase it by one.
                        the_state = 0

                    self.update_relationship(person_a,person_b, relationship_scale[the_state], visible)

            else:
                self.update_relationship(person_a, person_b, "Rival", visible)

        def begin_relationship(self, person_a, person_b, visible = None): #Sets their relationship to Acquaintance if they do not have one, otherwise leaves it untouched.
            the_relationship = self.get_relationship(person_a, person_b)
            if the_relationship is None: #Only sets a relationship for these people if one does not exist, so as to not override friendships or familial relationships
                self.update_relationship(person_a, person_b, "Acquaintance")


    # Aaaand immediately after creating this class I've decided it's not wanted. All I expect it to do for now is to act as a per-character message log.
    class Text_Message_Manager(): #Manages text conversations you've had with other girls. Also stores information for other phone related stuff
        def __init__(self): #TODO: Add support for manufacturing a message history.
            self.message_history = {} # A dict that stores entries of Person:[HistoryEntry,HistoryEntry...] representing your recorded conversation with this girl.
            self.current_message = None # Set to a tuple of [who, what] when someone texts you, allowing for it to be displayed immediately (instead of after the statement is passed into history). Should be
            #TODO: Then figure out how we are gong to store pictures, videos, allow custom avatar pics, ect. We could either store them as .pngs, or store all the required parameters (including outfit).

        def register_number(self, the_person): #Now just used to keep track of who's number we know
            if not self.has_number(the_person):
                self.message_history[the_person] = []

        def add_message(self, the_person, history_entry):
            self.register_number(the_person)
            self.message_history[the_person].append(history_entry)

        def add_non_convo_message(self, the_person, the_message): #Allows you to add an entry to the log without it having to appear as dialogue.
            new_entry = renpy.character.HistoryEntry() #TODO: Check if this results in double entries (it might be grabbed by the history callback immediately)
            new_entry.who = the_person.title
            new_entry.what = the_message
            self.add_message(the_person, new_entry)


        def add_system_message(self, the_person, the_message): #Adds a history entry that does not have a "who" variable set. Use to add phone messages like "[SENT A PICTURE]".
            new_entry = renpy.character.HistoryEntry()
            new_entry.who = None
            new_entry.what = the_message
            self.add_message(the_person, new_entry)

        def get_person_list(self):
            return self.message_history.keys()

        def has_number(self, the_person):
            if the_person in self.message_history:
                return True
            else:
                return False

        def get_message_list(self, the_person):
            if self.has_number(the_person):
                return self.message_history[the_person]
            else:
                return []


    #     def add_new_message(self, the_person, the_action):
    #         if the_person not in self.pending_messages:
    #             self.register_number(the_person)
    #
    #         self.pending_messages[the_person].append(the_action)
    #
    #     def has_new_message(self, the_person):
    #         return len(self.pending_messages[the_person]) > 0
    #
    #     def get_next_new_message(self, the_person):
    #         return self.pending_messages[the_person].pop(0) #NOTE: Assumes there is an event to get. Otherwise throws an error.
    #
    #     def call_new_message(self, the_person):
    #         the_message = self.get_next_new_message(the_person)
    #         the_message.call_action(the_person)


    #     def get_person_list(self):
    #         # Returns a tuple of (Person, Bool) for each person you know of.
    #         return_list = []
    #         for a_person in self.pending_messages:
    #             if self.has_new_message(a_person):
    #                 return_list.append((a_person, True))
    #             else:
    #                 return_list.append((a_person, False))
    #         return return_list



    class Room(renpy.store.object): #Contains people and objects.
        def __init__(self,name,formalName,connections,background_image,objects,people,actions,public,map_pos,
            tutorial_label = None, visible = True, hide_in_known_house_map = True, lighting_conditions = None):


            self.name = name
            self.formalName = formalName
            self.connections = connections
            self.background_image = background_image #If a string this is used at all points in the day. If it is a list each entry corrisponds to the background for a different part of the day
            self.objects = objects
            self.objects.append(Object("stand",["Stand"], sluttiness_modifier = 0, obedience_modifier = -5)) #Add a standing position that you can always use.
            self.people = people
            self.actions = actions #A list of Action objects
            self.public = public #If True, random people can wander here.
            self.map_pos = map_pos #A tuple of two int values giving the hex co-ords, starting in the top left. Using this guarantees locations will always tessalate.
            self.visible = visible #If true this location is shown on the map. If false it is not on the main map and will need some other way to access it.
            self.hide_in_known_house_map = hide_in_known_house_map #If true this location is hidden in the house map, usually because their house is shown on the main map.

            self.tutorial_label = tutorial_label #When the MC first enters the room the tutorial will trigger.
            self.trigger_tutorial = True #Flipped to false once the tutorial has been done once
            self.accessable = True #If true you can move to this room. If false it is disabled

            if lighting_conditions is None: #Default is 100% lit all of the time.
                self.lighting_conditions = [[1,1,1], [1,1,1], [1,1,1], [1,1,1], [1,1,1]] #A colour array that tints characters in this location. Perfect default light is 1,1,1
            else:
                self.lighting_conditions = lighting_conditions

            #TODO: add an "appropriateness" or something trait that decides how approrpaite it would be to have sex, be seduced, etc. in this location.

        def show_background(self):
            if isinstance(self.background_image, list):
                the_background_image = self.background_image[time_of_day]
            else: #I assume it's a list that contains one string per
                the_background_image = self.background_image


            renpy.scene("master")
            renpy.show(name = self.name, what = the_background_image, layer = "master")

        def link_locations(self,other): #This is a one way connection!
            self.connections.append(other)

        def link_locations_two_way(self,other): #Link it both ways. Great for adding locations after the fact, when you don't want to modify existing locations.
            self.link_locations(other)
            other.link_locations(self)

        def add_object(self,the_object):
            self.objects.append(the_object)

        def add_person(self,the_person):
            self.people.append(the_person)
            #TODO: add situational modifiers for the location

        def remove_person(self,the_person):
            self.people.remove(the_person)

        def move_person(self,the_person,the_destination):
            if not the_person in the_destination.people: # Don't bother moving people who are already there.
                if the_person in self.people: #Don't try and move if we aren't actually here!
                    self.remove_person(the_person)
                    the_destination.add_person(the_person)

        def has_person(self,the_person):
            if the_person in self.people:
                return True
            else:
                return False

        def get_person_list(self):
            return self.people

        def get_person_count(self):
            return len(self.people)

        def objects_with_trait(self,the_trait):
            return_list = []
            for object in self.objects:
                if object.has_trait(the_trait):
                    return_list.append(object)
            return return_list

        def has_object_with_trait(self,the_trait):
            if the_trait == "None":
                return True
            for object in self.objects:
                if object.has_trait(the_trait):
                    return True
            return False

        def get_object_with_name(self,name): #Use this to get objects from a room when you know what they should be named but don't have an object reference yet (ik
            for obj in self.objects:
                if obj.name == name:
                    return obj
            return None

        def valid_actions(self):
            count = 0
            for act in self.actions:
                if act.is_action_enabled() or act.is_disabled_slug_shown(): #We should also check if a non-action disabled slug would be available so that the player can check what the requirement would be.
                    count += 1
            return count

        def get_valid_actions(self):
            return_list = []
            for act in self.actions:
                if act.is_action_enabled() or act.is_disabled_slug_shown():
                    return_list.append(act)
            return return_list

        def get_lighting_conditions(self):
            return self.lighting_conditions[time_of_day]

    class Action(renpy.store.object): #Contains the information about actions that can be taken in a room. Dispayed when you are asked what you want to do somewhere.
        # Also used for crises, those are not related to any partiular room and are not displayed in a list. They are forced upon the player when their requirement is met.
        def __init__(self,name,requirement,effect,args = None, requirement_args = None, menu_tooltip = None, priority = 0, event_duration = 99999):
            self.name = name

            # A requirement returns False if the action should be hidden, a string if the action should be disabled but visible (the string is the reason it is not enabled), and True if the action is enabled
            self.requirement = requirement #Requirement is a function that is called when the action is checked.

            self.effect = effect #effect is a string for a renpy label that is called when the action is taken.
            if not args:
                self.args = [] #stores any arguments that we want passed to the action or requirement when the action is created. Should be a list of variables.
            elif type(args) is not list:
                self.args = [args] #Make sure our list of arguments is a list.
            else:
                self.args = args


            if not requirement_args:
                self.requirement_args = [] #A list of arguments handed to the requirement but not the actual event.
            elif not isinstance(requirement_args, list):
                self.requirement_args = [requirement_args]
            else:
                self.requirement_args = requirement_args

            self.menu_tooltip = menu_tooltip # A string added to any menu item where this action is displayed
            self.priority = priority #Used to order actions when displayed in a list. Higher priority actions are displaybed before lower ones, and disabled actions are shown after enabled actions.

            self.event_duration = event_duration # Used for actions turned into limtied time actions as the starting duration.

        def __cmp__(self,other): ##This and __hash__ are defined so that I can use "if Action in List" and have it find identical actions that are different instances.
            if type(other) is Action:
                if self.name == other.name and self.requirement == other.requirement and self.effect == other.effect and self.args == other.args:
                    return 0
                else:
                    if self.__hash__() < other.__hash__(): #Use hash values to break ties.
                        return -1
                    else:
                        return 1
            else:
                if other is None:
                    return -1
                elif self.__hash__() < other.__hash__(): #Use hash values to break ties.
                    return -1
                else:
                    return 1

        def __hash__(self):
            return hash((self.name,self.requirement,self.effect))

        def check_requirement(self, extra_args = None): #Calls the requirement function associated with this action.
        # Effectively private. Use "is_action_enabled" and "is_disabled_slug_shown" to figure out if there are important actions to display or take.
            if not extra_args: #We need to make sure we package all potential extra args as a list and hand them over.
                extra_args = []
            elif not isinstance(extra_args, list):
                extra_args = [extra_args]
            extra_args = extra_args + self.requirement_args
            return self.requirement(*extra_args)

        def is_action_enabled(self, extra_args = None):
            requirement_return = self.check_requirement(extra_args)
            if isinstance(requirement_return, basestring):
                # Any string returned means the action is not enabled
                return False
            else:
                # If it's not a string it must be a bool
                return requirement_return

        def is_disabled_slug_shown(self, extra_args = None): # Returns true if this action is not enabled but should show something when it is disabled.
            requirement_return = self.check_requirement(extra_args)
            if isinstance(requirement_return, basestring):
                return True
            else:
                return False

        def get_disabled_slug_name(self, extra_args = None): #Returns a formated name for when the
            requirement_return = self.check_requirement(extra_args)
            return self.name + "\n{size=16}{color=#ff0000}" + requirement_return + "{/color}{/size} (disabled)"

        def call_action(self, extra_args = None): #Can only use global variables. args is a list of elements you want to include as arguments. None is default
            if not extra_args:
                extra_args = []
            elif not isinstance(extra_args, list):
                extra_args = [extra_args]

            return_value = renpy.call(self.effect,*(self.args+extra_args))
            renpy.return_statement(return_value) #NOTE: _return may _already_ hold the value of the most recent return, so this might be redundent, or even cause bugs. Need to test. TODO

    class Limited_Time_Action(Action): #A wrapper class that holds an action and the amount of time it will be valid. This acts like an action everywhere
        #except it also has a turns_valid value to decide when to get rid of this reference to the underlying action
        def __init__(self, the_action, turns_valid):
            self.the_action = the_action
            self.turns_valid = turns_valid

        def __hash__(self):
            return hash((self.the_action.__hash__(), self.turns_valid))

        def __cmp__(self,other):
            if type(self) is type(other):
                if self.__hash__() == other.__hash__():
                    return 0

            if self.__hash__() > other.__hash__():
                return 1
            else:
                return -1

        def __getattr__(self, attr): # If we try and access an attribute not in this class return the matching attribute from the action. This is likely going to be a funciton like "check_is_active" or "call_action"
            if vars(self.the_action).has_key(attr):
                return self.the_action.__dict__[attr]
            else:
                raise AttributeError

        def __getstate__(self):
            return vars(self)

        def __setstate__(self, state):
            vars(self).update(state)

    def sort_display_list(the_item): #Function to use when sorting lists of actions (and potentially people or strings)
        extra_args = None
        if isinstance(the_item, list): #If it's a list it's actually an item of some sort with extra args. Break those out and continue.
            extra_args = the_item[1]
            the_item = the_item[0]

        if isinstance(the_item, Action):
            if the_item.is_action_enabled(extra_args):
                return the_item.priority
            else:
                return the_item.priority - 1000 #Apply a ranking penalty to disabled items. They will appear in priority order but below enabled events (Unless something has a massive priority).

        elif isinstance(the_item, Person):
            return the_item.core_sluttiness #Order people by sluttiness? Love? Something else?

        else:
            return 0

    class Role(renpy.store.object): #Roles are assigned to special people. They have a list of actions that can be taken when you talk to the person and acts as a flag for special dialogue options.
        def __init__(self, role_name, actions, hidden = False, on_turn = None, on_move = None, on_day = None):
            self.role_name = role_name
            self.actions = actions # A list of actions that can be taken. These actions are shown when you talk to a person with this role if their requirement is met.
            # At some point we may want a seperate list of role actions that are available when you text someone.
            self.hidden = hidden #A hidden role is not shown on the "Roles" list
            self.on_turn = on_turn #A function that is run each turn on every person with this Role.
            self.on_move = on_move #A function that is run each move phase on every person with this Role.
            self.on_day = on_day

            self.linked_roles = [] #A list of other roles. If this role is removed, all linked roles are removed as well.

        def run_turn(self, the_person):
            if self.on_turn is not None:
                self.on_turn(the_person)

        def run_move(self, the_person):
            if self.on_move is not None:
                self.on_move(the_person)

        def run_day(self, the_person):
            if self.on_day is not None:
                self.on_day(the_person)

        def link_role(self, the_role):
            if the_role not in self.linked_roles:
                self.linked_roles.append(the_role)

    class Listener_Management_System(renpy.store.object): #Used to manage listeners in objects. Contains functiosn for enrolling and removing triggers as well as firing notices to those triggers.
        def __init__(self):
            self.event_dict = {} #THis dictionary uses strings as keys (the trigger that is called) and each key holds a list of goals. When an event is triggered each listener enrolled to the key recieves a notice (the on_trigger_funciton is called)

        def enroll_goal(self, trigger_name, the_goal):
            if trigger_name in self.event_dict:
                self.event_dict[trigger_name].append(the_goal) #Add the goal to the list.

            else: #The trigger_name is not in our dict, we need to add it then add the goal to it.
                self.event_dict[trigger_name] = [the_goal]

        def fire_event(self, trigger_name, **kwargs):
            if trigger_name in self.event_dict: #Make sure we have the key first before we go grabbing lists.
                completed_goals = [] #We store completed goals in a seperate list to let us flag things for removal without
                for goal in self.event_dict[trigger_name]:
                    if goal.call_trigger(**kwargs): #on_trigger returns true if the goal is finished and we can stop letting it know.
                        completed_goals.append(goal)
                for goal in completed_goals:
                    goal.complete_goal()
                    self.event_dict[trigger_name].remove(goal) #Remove all completed goals, they are no longer important.



    class Goal(renpy.store.object):
        def __init__(self, goal_name, goal_description, event_name, listener_type, valid_goal_function, on_trigger_function, arg_dict = None, difficulty_scale_function = None, report_function = None, progress_fraction_function = None, mandatory = False):
            self.name = goal_name #Short form name to be displayed to the player, generally on a progress bar of some sort.
            self.description = goal_description #A long form fluff description of the goal purpose.
            self.event_name = event_name #The event (aka a string to give to a listnener manager) that this goal listens to.
            self.listener_type = listener_type #Either "MC" or "Business", decides which object the goal will grab as their listener manager when you ask it to enroll.
            self.valid_goal_function = valid_goal_function #A function called to check to see if the goal is a valid/reasonable one to give to the player. Also is used to make sure goals aren't completed when they are assigned.
            self.on_trigger_function = on_trigger_function #A function called by an event listener that that this goal is hooked up to.
            if arg_dict: #A dict to hold arguments you want to be used by the on_trigger function without having to get specific about what they are here.
                self.arg_dict = arg_dict
            else:
                self.arg_dict = {}

            self.completed = False #A flag set to true when the goal is finished, so the player can complete the objective and claim their bonus point.

            self.difficulty_scale_function = difficulty_scale_function #A function called when the goal is activated (aka when it is copied from the default goal) to scale the paramaters to the current difficulty.
            self.report_function = report_function
            self.progress_fraction_function = progress_fraction_function
            self.mandatory = mandatory

        def __cmp__(self,other):
            if self.name == other.name:
                if self.description == other.description:
                    if self.valid_goal_function == other.valid_goal_function:
                        if self.on_trigger_function == other.on_trigger_function:
                            if self.arg_dict == other.arg_dict:
                                return 0
            if self.__hash__() > other.__hash__():
                return 1
            else:
                return -1


        def __hash__(self):
            return hash((self.name, self.description, self.valid_goal_function, self.on_trigger_function))

        def check_valid(self, difficulty):
            if self.valid_goal_function is not None:
                return self.valid_goal_function(self, difficulty)
            else:
                return True #If a goal does not have a valid goal function it is always valid.

        def activate_goal(self, difficulty):
            if self.listener_type == "MC": #Figure out what listener we should be listening to
                listener = mc.listener_system
            else: #== "Business"
                listener = mc.business.listener_system

            if self.difficulty_scale_function:
                self.difficulty_scale_function(self, difficulty) #If we have a function for changing difficulty hand it ourselves and the difficulty we were activated at.

            listener.enroll_goal(self.event_name, self) #Enroll us to the proper listener and hand it us so it will call our trigger when we need it to.

        def get_reported_progress(self): #Returns a string corisponding to the current progress of the goal. Generally something like "5 of 10" or "3/20".
            if self.completed:
                return "Completed"
            elif self.report_function:
                return self.report_function(self)
            else:
                return "In Progress"

        def get_progress_fraction(self):
            if self.progress_fraction_function:
                return self.progress_fraction_function(self)
            else:
                return 0.0

        def call_trigger(self, **kwargs):
            return self.on_trigger_function(self, **kwargs)

        def complete_goal(self):
            self.completed = True




    class Policy(renpy.store.object): # An upgrade that can be purchased by the character for their business.
        def __init__(self,name,desc,requirement,cost, toggleable = False, on_buy_function = None, extra_arguments = None, on_apply_function = None, on_remove_function = None, on_turn_function = None, on_move_function = None, on_day_function = None, dependant_policies = None):
            self.name = name #A short name for the policy.
            self.desc = desc #A text description of the policy.
            self.requirement = requirement #a function that is run to see if the PC can purchase this policy.
            self.cost = cost #Cost in dollars.

            self.toggleable = toggleable #If True this policy can be toggled on and off. Otherwise, it is set "active" when bought and can never be deactivated.


            if extra_arguments is None:
                self.extra_arguments = {}
            else:
                self.extra_arguments = extra_arguments #A dictionary of extra values that can be used by the various on_buy, on_apply, etc. functions

            self.on_buy_function = on_buy_function #A function to be called when purchased
            self.on_apply_function = on_apply_function
            self.on_remove_function = on_remove_function
            self.on_turn_function = on_turn_function #These functions are applied to anyone with the Employee role. Policies that affect people with specific sub-roles
            self.on_move_function = on_move_function
            self.on_day_function = on_day_function

            if dependant_policies is None:
                self.dependant_policies = []
            elif isinstance(dependant_policies, Policy):
                self.dependant_policies = [dependant_policies] #If we hand a single item wrap it in a list for iteration purposes
            else:
                self.dependant_policies = dependant_policies # Otherwise we have a list already.

            self.depender_policies = [] #These policies depend _on_ us, and are declared when other policies are defined. If they are on, we cannot toggle off.
            for policy in self.dependant_policies:
                policy.depender_policies.append(self) #Esentially builds a two way linked list of policies while allowing us to only define the requirements from the base up. Also conveniently stops dependency cycles from forming.


        def __cmp__(self,other): #
            if type(other) is Policy:
                if self.name == other.name and self.desc == other.desc and self.cost == other.cost:
                    return 0
                else:
                    if self.__hash__() < other.__hash__(): #Use hash values to break ties.
                        return -1
                    else:
                        return 1

            else:
                if self.__hash__() < other.__hash__(): #Use hash values to break ties.
                    return -1
                else:
                    return 1

        def __hash__(self):
            return hash((self.name,self.desc,self.cost))

        def is_owned(self):
            if self in mc.business.policy_list:
                return True
            else:
                return False

        def is_active(self):
            if self in mc.business.active_policy_list:
                return True
            else:
                return False

        def is_toggleable(self):
            return_toggle = True
            if self.is_owned and self.toggleable: #If a policy is suppose to be toggleable:
                if self in mc.business.active_policy_list: # We are currently active, so we are only disable-able if all of the dependers are off.
                    for policy in self.depender_policies:
                        if policy.is_active(): #If any of the policies that rely on this are active we cannot toggle off.
                            return_toggle = False

                else: # We are owned but not active. We can only be toggled if every policy in our dependant list is active
                    for policy in self.dependant_policies:
                        if not policy.is_active():
                            return_toggle = False

            else:
                return_toggle = False

            return return_toggle

        def buy_policy(self, ignore_cost = False):
            mc.business.policy_list.append(self)
            if not ignore_cost:
                mc.business.funds -= self.cost
            if self.on_buy_function is not None:
                self.on_buy_function(**self.extra_arguments)

        def apply_policy(self):
            mc.business.active_policy_list.append(self)
            if self.on_apply_function is not None:
                self.on_apply_function(**self.extra_arguments)
            return

        def remove_policy(self):
            if self in mc.business.active_policy_list:
                mc.business.active_policy_list.remove(self)
                if self.on_remove_function is not None:
                    self.on_remove_function(**self.extra_arguments)
            return

        def on_turn(self):
            if self.on_turn_function is not None:
                self.on_turn_function(**self.extra_arguments)
            return

        def on_move(self):
            if self.on_move_function is not None:
                self.on_move_function(**self.extra_arguments)
            return

        def on_day(self):
            if self.on_day_function is not None:
                self.on_day_function(**self.extra_arguments)
            return




    class Object(renpy.store.object): #Contains a list of traits for the object which decides how it can be used.
        def __init__(self,name,traits,sluttiness_modifier = 0, obedience_modifier = 0):
            self.traits = traits
            self.name = name
            self.sluttiness_modifier = sluttiness_modifier #Changes a girls sluttiness when this object is used in a sex scene
            self.obedience_modifier = obedience_modifier #Changes a girls obedience when this object is used in a sex scene.

        def has_trait(self,the_trait):
            for trait in self.traits:
                if trait == the_trait:
                    return True
            return False

        def get_formatted_name(self):
            if not (self.sluttiness_modifier == 0 and self.obedience_modifier == 0):
                the_string = self.name + "\n{size=22}"
                if self.sluttiness_modifier != 0 or self.obedience_modifier != 0:
                    the_string += "Temporary Modifiers\n"

                if self.sluttiness_modifier < 0:
                    the_string += str(self.sluttiness_modifier) + " Sluttiness"
                    if not self.obedience_modifier == 0:
                        the_string += ", "
                if self.sluttiness_modifier > 0:
                    the_string += "+" + str(self.sluttiness_modifier) + " Sluttiness"
                    if not self.obedience_modifier == 0:
                        the_string += ", "

                if self.obedience_modifier < 0:
                    the_string += str(self.obedience_modifier) + " Obedience"

                if self.obedience_modifier >0:
                    the_string += "+" + str(self.obedience_modifier) + " Obedience"

                the_string += "{/size} (tooltip)The object you have sex on influences how enthusiastic and obedient a girl will be."
                return the_string
            else:
                return self.name

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

        def __cmp__(self,other):
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
                return_imge = image_set.get_image(body_type, tit_size)
            else:
                return_imge = image_set.get_image(body_type, "AA")

            return return_imge

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

                #
                # if self.crop_offset_dict:
                #     offset_tuple = self.crop_offset_dict.get(position, (0,0))
                # else:
                #     offset_tuple = (0,0)

                return final_image


    class Facial_Accessory(Clothing): #This class inherits from Clothing and is used for special accessories that require extra information
        supported_positions = ["stand2","stand3","stand4","stand5","walking_away","kissing","doggy","missionary","blowjob","against_wall","back_peek","sitting","kneeling1","standing_doggy","cowgirl"]

        _position_sets = {}
        def get_position_sets(self):
            if not self.proper_name in self._position_sets:
                self._position_sets[self.proper_name] = {}
            return self._position_sets[self.proper_name]
        def set_position_sets(self, value):
            self._position_sets[self.proper_name] = value

        position_sets = property(get_position_sets, set_position_sets, None, "Facial Accessory position sets")

        def get_crop_offset_dict(self):
            return master_clothing_offset_dict.get(self.proper_name, {})

        crop_offset_dict = property(get_crop_offset_dict, None, None, "Offset dictionary")

        def __init__(self, name, layer, hide_below, anchor_below, proper_name, draws_breasts, underwear, slut_value, has_extension = None, is_extension = False, colour = None, tucked = False,
            opacity_adjustment = 1, whiteness_adjustment = 0.0, contrast_adjustment = 1.0, display_name = None, crop_offset_dict = None, modifier_lock = None):

            self.name = name
            if display_name is None:
                self.display_name = name
            else:
                self.display_name = display_name
            self.proper_name = proper_name
            self.hide_below = hide_below #If true, it hides the clothing beneath so you can't tell what's on.
            self.anchor_below = anchor_below #If true, you must take this off before you can take off anything of a lower layer.f
            self.layer = layer #A list of the slots above that this should take up or otherwise prevent from being filled. Slots are a list of the slot and the layer.

            self.position_sets = {} #A list of position set names. When the clothing is created it will make a dict containing these names and image sets for them.
        #    self.supported_positions = ["stand2","stand3","stand4","stand5","walking_away","kissing","doggy","missionary","blowjob","against_wall","back_peek","sitting","kneeling1","standing_doggy","cowgirl"]

            self.half_off = False # Avoids any problems with the half-off system using facial accessories
            self.half_off_reveals = False
            self.half_off_clothing = False

            self.half_off_regions = []
            self.half_off_ignore_regions = []

            for set in self.supported_positions:
                self.position_sets[set] = Facial_Accessory_Images(proper_name,set)

            # self.crop_offset_dict = master_clothing_offset_dict.get(self.proper_name, {})

            self.draws_breasts = draws_breasts
            self.underwear = underwear #True if the item of clothing satisfies the desire for underwear for upper or lower (bra or panties), false if it can pass as outerwear. Underwear on outside of outfit gives higher slut requirement.
            self.slut_value = slut_value #The amount of sluttiness that this piece of clothing adds to an outfit.
            self.has_extension = has_extension
            self.is_extension = is_extension #If this is true the clothing item exists only as a placeholder. It will draw nothing and not be removed unless the main piece is removed.
            if not colour:
                self.colour = [1,1,1,1]
            else:
                self.colour = colour
            self.tucked = tucked #Items of clothing that are tucked are drawn a "half level", aka we cycle thorugh all layer 2's and do untucked items, then do all tucked items.

            self.opacity_adjustment = opacity_adjustment
            self.whiteness_adjustment = whiteness_adjustment
            self.contrast_adjustment = contrast_adjustment

            self.modifier_lock = modifier_lock #If set to something other than None this facial accessory adds the modifier to all positions if possible.


        def generate_item_displayable(self, position, face_type, emotion, special_modifiers = None, lighting = None):
            if not self.is_extension:
                if lighting is None:
                    lighting = [1,1,1]

                image_set = self.position_sets.get(position)
                if image_set is None:
                    image_set = self.position_sets.get("stand3") #Get a default image set if we are looking at a position we do not have.

                the_image = image_set.get_image(face_type, emotion, special_modifiers)
                if not the_image:
                    the_image = image_set.get_image(face_type, emotion) # If we weren't able to get something with the special modifier just use a default to prevent a crash.

                brightness_matrix = im.matrix.brightness(self.whiteness_adjustment)
                contrast_matrix = im.matrix.contrast(self.contrast_adjustment)
                opacity_matrix = im.matrix.opacity(self.opacity_adjustment) #Sets the clothing to the correct colour and opacity.

                greyscale_image = im.MatrixColor(the_image, opacity_matrix * brightness_matrix * contrast_matrix) #Set the image, which will crush all modifiers to 1 (so that future modifiers are applied to a flat image correctly with no unusually large images

                colour_matrix = im.matrix.tint(self.colour[0], self.colour[1], self.colour[2]) * im.matrix.tint(*lighting)
                alpha_matrix = im.matrix.opacity(self.colour[3])
                shader_image = im.MatrixColor(greyscale_image, alpha_matrix * colour_matrix) #Now colour the final greyscale image

                #shader_image = im.Recolor(the_image.filename,int(self.colour[0]*255),int(self.colour[1]*255),int(self.colour[2]*255),int(self.colour[3]*255))
                # shader_image = ShaderDisplayable(shader.MODE_2D, the_image.filename, shader.VS_2D,PS_COLOUR_SUB_LR2,{},uniforms={"colour_levels":self.colour})

                final_image = Composite(position_size_dict[position], self.crop_offset_dict.get(position,(0,0)), shader_image)

                return final_image


    class Facial_Accessory_Images(renpy.store.object):
        def __init__(self,accessory_name,position):
            self.images = {}
            self.position_name = position
            self.supported_faces = ["Face_1","Face_2","Face_3","Face_4","Face_5","Face_6","Face_7","Face_8","Face_9","Face_11","Face_12","Face_13","Face_14"]
            self.supported_emotions = ["default","sad","happy","angry","orgasm"]
            self.special_modifiers = {self.position_name:"blowjob","kissing":"kissing"} #As of v0.35 all positions support the blowjob modifier so we can have good looking gags and a wider variety of facial expressions.

            for face in self.supported_faces:
                for emotion in self.supported_emotions:
                    #Add the image string to the dict. We do not use Image obects directly because it greatly slows down the game (character objects become huge.)
                    self.images[face + "_" + emotion] = accessory_name + "_" + position + "_" + face + "_" + emotion + ".png" # Save the file string so we can generate a proper image from it easily later.
                    if position in self.special_modifiers:
                        self.images[face + "_" + emotion + "_" + self.special_modifiers[position]] = accessory_name + "_" + position + "_" + face + "_" + emotion + "_" + self.special_modifiers[position] + ".png"
                        #There is a special modifier, we need to add that version as well.

        def get_image(self, face, emotion, special_modifier = None):
            index_string = face + "_" + emotion
            global mobile_zip_dict
            file = mobile_zip_dict[self.position_name]
            if special_modifier is not None:
                if index_string+"_"+special_modifier in file.namelist():
                    index_string += "_" + special_modifier #We only want to try and load special modifier images if they exist. Otherwise we use the unmodified image to avoid a crash. This lets us omit images we do not plan on actually using, such as glasses not needing blowjob poses.

            the_image = VrenZipImage(self.position_name, self.images[index_string])
            return the_image
        def get_image_name(self, face, emotion, special_modifier = None):
            index_string = face + "_" + emotion
            global mobile_zip_dict
            file = mobile_zip_dict[self.position_name]
            if special_modifier is not None:
                if index_string+"_"+special_modifier in file.namelist():
                    index_string += "_" + special_modifier #We only want to try and load special modifier images if they exist. Otherwise we use the unmodified image to avoid a crash. This lets us omit images we do not plan on actually using, such as glasses not needing blowjob poses.

            return self.images[index_string]

    class Clothing_Images(renpy.store.object): # Stores a set of images for a single piece of clothing in a single position. The position is stored when it is put into the clothing object dict.
        def __init__(self,clothing_name,position_name,is_top, body_dependant = True):

            self.images = {}
            self.clothing_name = clothing_name #Used for some debugging, not needed for the actual game logic.
            self.position_name = position_name #Used so we can access the correct .zip file
            if body_dependant:
                self.body_types = ["standard_body","thin_body","curvy_body","standard_preg_body"]
            else:
                self.body_types = ["standard_body"]

            self.breast_sizes = ["AA","A","B","C","D","DD","DDD","E","F","FF"]

            for body in self.body_types:
                if is_top:
                    for breast in self.breast_sizes:
                        if clothing_name is None:
                            self.images [body + "_" + breast] = "empty_holder.png" #Placeholder for clothing items that exist but don't get drawn for some reason (or that don't have image sets yet).
                        else:
                            self.images [body + "_" + breast] = clothing_name+"_"+position_name+"_"+body+"_"+breast+".png"
                else:
                    if clothing_name is None:
                        self.images [body + "_AA"] = "empty_holder.png"
                    else:
                        self.images[body + "_AA"] = clothing_name+"_"+position_name+"_"+body+"_AA.png"

        def get_image(self, body_type, breast_size = "AA" ): #Generates a proper Image object from the file path strings we have stored previously. Prevents object bloat by storing large objects repeatedly for everyone.
            index_string = body_type + "_" + breast_size
            return_image = VrenZipImage(self.position_name, self.images[index_string])

            if return_image:
                return return_image
            else:
                return

        def get_image_name(self, body_type, breast_size = "AA" ): #Generates a proper Image object from the file path strings we have stored previously. Prevents object bloat by storing large objects repeatedly for everyone.
            index_string = body_type + "_" + breast_size
            return self.images[index_string]

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


    class Outfit(renpy.store.object): #A bunch of clothing added together, without slot conflicts.
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
                    nipple_wetness = (0.1*(float(rank_tits(the_person.tits)+the_person.lactation_sources))) * (the_person.arousal/the_person.max_arousal)
                    if nipple_wetness > 1.0:
                        nipple_wetness = 1.0

            if hide_layers is None:
                hide_layers = []

            all_items = self.generate_clothing_list(body_type, tit_size, position) #First generate a list of the clothing objects

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
            all_items = self.generate_clothing_list(body_type, tit_size, position)


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

        def generate_clothing_list(self, body_type = None, tit_size = None, position = None): #Returns a properly ordered list of clothing. If used to draw them they would be displayed correctly.
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
                if accessory == new_clothing:
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
            return get_visible_list(self.upper_body)

        def get_lower_visible(self):
            return get_visible_list(self.lower_body)

        def get_feet_visible(self):
            return get_visible_list(self.feet)

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
            if (self.wearing_bra and not self.bra_covered()) or (self.wearing_panties() and not self.panties_covered()):
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

        def get_underwear_strip_list(self, visible_enough = True, avoid_nudity = False): #Gets a list of things to strip until this outfit would have a girl in her underwear
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
            return items_to_strip

        def strip_to_underwear(self, visible_enough = True, avoid_nudity = False): #Used to off screen strip a girl down to her underwear, or completely if she isn't wearing any.
            items_to_strip = self.get_underwear_strip_list(visible_enough, avoid_nudity)
            for item in items_to_strip:
                self.remove_clothing(item)

        def get_tit_strip_list(self, visible_enough = True): #Generates a list of clothing that, when removed from this outfit, result in tits being visible. Useful for animated clothing removal.
            # TODO: Add a way to generate this while including half-off options.
            #TODO: Add some pussy equivalent functions, I'll get to them when I need them for a crisis.
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
        #TODO: Update existing crises to make use of these centralised functions instead of handeling stripping as a special case each time.

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

    def make_wall(): #Helper functions for creating instances of commonly used objects.
        the_wall = Object("wall",["Lean"], sluttiness_modifier = 0, obedience_modifier = 5)
        return the_wall

    def make_window():
        the_window = Object("window",["Lean"], sluttiness_modifier = -5, obedience_modifier = 5)
        return the_window

    def make_chair():
        the_chair = Object("chair",["Sit","Low"], sluttiness_modifier = 0, obedience_modifier = 0)
        return the_chair

    def make_desk():
        the_desk = Object("desk",["Sit","Lay","Low"], sluttiness_modifier = 0, obedience_modifier = 0)
        return the_desk

    def make_table():
        the_table = Object("table",["Sit","Lay","Low"], sluttiness_modifier = 0, obedience_modifier = 0)
        return the_table

    def make_bed():
        the_bed = Object("bed",["Sit","Lay","Low"], sluttiness_modifier = 10, obedience_modifier = 10)
        return the_bed

    def make_couch():
        the_couch = Object("couch",["Sit","Lay","Low"], sluttiness_modifier = 5, obedience_modifier = -5)
        return the_couch

    def make_floor():
        the_floor = Object("floor",["Lay","Kneel"], sluttiness_modifier = -10, obedience_modifier = -10)
        return the_floor

    def make_grass():
        the_grass = Object("grass",["Lay","Kneel"], sluttiness_modifier = -5, obedience_modifier = -10)
        return the_grass

    def make_stage():
        the_stage = Object("stripclub stage",["Lay","Sit"], sluttiness_modifier = 5, obedience_modifier = -5)
        return the_stage



    class Position(renpy.store.object):
        def __init__(self,name,slut_requirement,slut_cap,requires_hard, requires_large_tits,
            position_tag,requires_location,requires_clothing,skill_tag,
            girl_arousal,girl_energy,guy_arousal,guy_energy,connections,
            intro,scenes,outro,transition_default,
            strip_description, strip_ask_description,
            orgasm_description,
            taboo_break_description,
            verb = "fuck", verbing = None, opinion_tags = None, record_class = None,
            default_animation = None, modifier_animations = None,
            associated_taboo = None):


            self.name = name
            self.slut_requirement = slut_requirement #The required slut score of the girl. Obedience will help fill the gap if possible, at a happiness penalty. Value from 0 (almost always possible) to ~100
            self.slut_cap = slut_cap #The maximum sluttiness that this position will have an effect on.
            self.requires_hard = requires_hard
            self.requires_large_tits = requires_large_tits

            self.girl_arousal = girl_arousal # The base arousal the girl recieves from this position.
            self.girl_energy = girl_energy # The amount of energy the girl spends on this position.

            self.guy_arousal = guy_arousal # The base arousal the guy recieves from this position.
            self.guy_energy = guy_energy # The base energy the guy spends on this position.

            self.position_tag = position_tag # The tag used to get the correct position image set.
            self.requires_location = requires_location # A tag that must match an object to have sex on it (eg. "lean", which needs something like a wall to lean against)
            self.requires_clothing = requires_clothing # A tag that notes what (lack of) clothing requirements the position has. Vaginal requires access to her vagina, tits her tits.
            self.skill_tag = skill_tag #The skill that will provide a bonus to this position.
            self.opinion_tags = opinion_tags #The opinion that will be checked each round.
            self.connections = connections
            self.intro = intro
            self.taboo_break_description = taboo_break_description #Called instead of the intro/transition when you break a taboo with someone. Should include call to personality taboo specific dialogue.
            self.scenes = scenes
            self.outro = outro
            self.transition_default = transition_default #TODO: add transitions that go between related positions but with different objects. Things like standing sex into fucking her against a window.
            self.transitions = []
            self.strip_description = strip_description
            self.strip_ask_description = strip_ask_description
            self.orgasm_description = orgasm_description
            self.verb = verb #A verb used to describe the position. "Fuck" is default, and mostly used for sex positions or blowjobs etc. Kiss, Fool around, etc. are also possibilities.
            if verbing is None: #The verb used as "Go back to [verbing] her.". Added specifically to support things like grope/groping, which have different spellings depending.
                self.verbing = verb + "ing"
            else:
                self.verbing = verbing
            self.record_class = record_class #A key to Person.sex_record[] that is updated once (and only once!) per sexual encounter if this position is picked.

            self.current_modifier = None #We will update this if the posisiion has a special modifier that shoudl be applied, like blowjob.

            if default_animation is None:
                self.default_animation = idle_wiggle_animation
            else:
                self.default_animation = default_animation #If not None this is used to animate the character if nothing else is specifically handed over.

            if modifier_animations is None: #If an animation exists for a special modifier it is used instead of the default one.
                self.modifier_animations = {}
            else:
                self.modifier_animations = modifier_animations

            self.associated_taboo = associated_taboo #What taboo tag, if any, is associated with this position. Until broken a taboo makes a position harder to select, but the taboo is broken once it is done once.
            # Current sex related taboo are:
            # kissing, touching_body, touching_penis, touching_vagina, sucking_cock, licking_pussy, vaginal_sex, anal_sex
            # And as a special case for vaginal sex: condomless_sex

        def link_positions(self,other,transition_label): #This is a one way link!
            self.connections.append(other)
            self.transitions.append([other,transition_label])

        def link_positions_two_way(self,other,transition_label_1,transition_label_2): #Link it both ways. Great for adding a modded position without modifying other positions.
            self.link_positions(other,transition_label_1)
            other.link_positions(self,transition_label_2)

        def call_intro(self, the_person, the_location, the_object):
            renpy.call(self.intro,the_person, the_location, the_object)

        def call_taboo_break(self, the_person, the_location, the_object):
            renpy.call(self.taboo_break_description, the_person, the_location, the_object)

        def call_scene(self, the_person, the_location, the_object):
            random_scene = renpy.random.randint(0,len(self.scenes)-1)
            renpy.call(self.scenes[random_scene],the_person, the_location, the_object)

        def call_outro(self, the_person, the_location, the_object):
            renpy.call(self.outro,the_person, the_location, the_object)

        def call_transition(self, the_position, the_person, the_location, the_object):
            if the_position is None:
                transition_scene = self.transition_default #If we don't care what position we started in we can call the transition "in reverse" by setting the position to None and using our own default.
            else:
                transition_scene = the_position.transition_default
                for position_tuple in self.transitions:
                    if position_tuple[0] == the_position: ##Does the position match the one we are looking for?
                        transition_scene = position_tuple[1] ##If so, set it's label as the one we are going to change to.
            renpy.call(transition_scene, the_person, the_location, the_object)

        def call_strip(self, the_clothing, the_person, the_location, the_object):
            renpy.call(self.strip_description, the_clothing, the_person, the_location, the_object)

        def call_strip_ask(self, the_clothing, the_person, the_location, the_object):
            renpy.call(self.strip_ask_description, the_clothing, the_person, the_location, the_object)

        def call_orgasm(self, the_person, the_location, the_object):
            renpy.call(self.orgasm_description, the_person, the_location, the_object)

        def check_clothing(self, the_person):
            if self.requires_clothing == "Vagina":
                return the_person.outfit.vagina_available()
            elif self.requires_clothing == "Tits":
                return the_person.outfit.tits_available()
            else:
                return True ##If you don't have one of the requirements listed above just let it happen.

        def calculate_arousal_modified_speed(self, the_person):
            male_energy_fraction = (1.0*self.guy_energy) / (self.guy_energy+self.girl_energy)  # Animation strength is divided based on who is spending more energy (ie. girls giving blowjobs speed up as they get horny, not you).
            male_animation_effect = male_energy_fraction * (mc.arousal/mc.max_arousal)  # Being closer to max arousal increases the speed of the animation.

            female_energy_fraction = (1.0*self.girl_energy) / (self.guy_energy+self.girl_energy)
            female_animation_effect = female_energy_fraction * (the_person.arousal/the_person.max_arousal)

            the_animation_speed = 0.5 + (0.5 * (male_animation_effect + female_animation_effect)) #Scales the animation strength from 50% to 100%, increasing as each party gets more aroused.

            return the_animation_speed

        def redraw_scene(self, the_person, emotion = None): #redraws the scene, call this when something is modified.
            the_animation_speed = self.calculate_arousal_modified_speed(the_person)

            if self.current_modifier in self.modifier_animations:
                position_animation = self.modifier_animations[self.current_modifier]
            else:
                position_animation = self.default_animation

            the_person.draw_person(self.position_tag, emotion = emotion, special_modifier = self.current_modifier, the_animation = position_animation, animation_effect_strength = the_animation_speed)

        def her_position_willingness_check(self, the_person, ignore_taboo = False): #Checks if the given girl would/can pick this position. A mirror of the main character's options.
            possible = True

            position_taboo = self.associated_taboo
            if ignore_taboo:
                position_taboo = None

            final_slut_requirement = self.slut_requirement
            final_slut_cap = self.slut_cap
            if self.skill_tag == "Anal" and the_person.has_family_taboo():
                final_slut_requirement += -10 #It's easier to convince a family member to have anal sex, since it's not "real" incest or something.
                final_slut_cap += -10
            elif self.skill_tag == "Vaginal" and the_person.has_family_taboo():
                final_slut_requirement += 10 #It's harder to convince a family member to have vaginal sex
                final_slut_cap += 10


            if final_slut_requirement > the_person.effective_sluttiness(position_taboo):
                possible = False # Too slutty for her.
            elif not self.check_clothing(the_person):
                possible = False # Clothing is in the way.
            elif mc.energy < self.guy_energy or the_person.energy < self.girl_energy:
                possible = False # One of them is too tired.
            elif self.requires_hard and mc.recently_orgasmed:
                possible = False # The mc has cum recently and isn't hard.
            elif self.requires_large_tits and not the_person.has_large_tits():
                possible = False # You need large tits for this and she doesn't have it.

            return possible

        def build_position_willingness_string(self, the_person, ignore_taboo = False): #Generates a string for this position that includes a tooltip and coloured willingness for the person given.
            willingness_string = ""
            tooltip_string = ""

            # girl_expected_arousal = str(int(self.girl_arousal * (1 + 0.1 * mc.sex_skills[self.skill_tag]))) #Estimate what they'll gain based on both of your skills to make the predictions as accurate as possible.
            # guy_expected_arousal = str(int(self.guy_arousal * (1 + 0.1 * the_person.sex_skills[self.skill_tag])))

            # energy_string = build_energy_string(the_person)
            # arousal_string = build_arousal_string(the_person)

            disable = False

            position_taboo = self.associated_taboo
            if ignore_taboo:
                position_taboo = None

            taboo_break_string = ""
            if the_person.has_taboo(position_taboo):
                taboo_break_string = " {image=gui/extra_images/taboo_break_token.png} "

            final_slut_requirement = self.slut_requirement
            final_slut_cap = self.slut_cap
            if self.skill_tag == "Anal" and the_person.has_family_taboo():
                final_slut_requirement += -10 #It's easier to convince a family member to have anal sex, since it's not "real" incest or something.
                final_slut_cap += -10
            elif self.skill_tag == "Vaginal" and the_person.has_family_taboo():
                final_slut_requirement += 10 #It's harder to convince a family member to have vaginal sex
                final_slut_cap += 10

            if the_person.effective_sluttiness(position_taboo) > final_slut_cap:
                if the_person.arousal > final_slut_cap:
                    willingness_string = "{color=#6b6b6b}Boring{/color}" #No sluttiness gain AND half arousal gain
                    tooltip_string = " (tooltip)This position is too boring to interest her when she is this horny. No sluttiness increase and her arousal gain is halved."
                else:
                    willingness_string = "{color=#3C3CFF}Comfortable{/color}" #No sluttiness
                    tooltip_string = " (tooltip)This position is too tame for her tastes. No sluttiness increase, but it may still be a good way to get warmed up and ready for other positions."
            elif the_person.effective_sluttiness(position_taboo) >= final_slut_requirement:
                willingness_string = "{color=#3DFF3D}Exciting{/color}" #Normal sluttiness gain
                tooltip_string = " (tooltip)This position pushes the boundry of what she is comfortable with. Increases temporary sluttiness, which may become permanent over time or with serum application."
            elif the_person.effective_sluttiness(position_taboo) + the_person.obedience-100 >= final_slut_requirement:
                willingness_string = "{color=#FFFF3D}Likely Willing if Commanded{/color}"
                tooltip_string = " (tooltip)This position is beyond what she would normally consider. She is obedient enough to do it if she is commanded, at the cost of some happiness."
            else:
                willingness_string = "{color=#FF3D3D}Likely Too Slutty{/color}"
                tooltip_string = " (tooltip)This position is so far beyond what she considers appropriate that she would never dream of it."

            if the_person.has_taboo(position_taboo):
                tooltip_string +="\nSuccessfully selecting this position will break a taboo, making it easier to convince " + the_person.title + " to do it and similar acts in the future."


            if not self.check_clothing(the_person):
                disable = True
                willingness_string += "\nObstructed by clothing"
            elif mc.recently_orgasmed and self.requires_hard:
                disable = True
                willingness_string += "\nRecently orgasmed"
            elif mc.energy < self.guy_energy and the_person.energy < self.girl_energy:
                disable = True
                willingness_string += "\nYou're both too tired"
            elif mc.energy < self.guy_energy:
                disable = True
                willingness_string += "\nYou're too tired"
            elif the_person.energy < self.girl_energy:
                disable = True
                willingness_string += "\nShe's too tired"
            #else:

            if disable:
                return taboo_break_string + self.name + taboo_break_string + "\n{size=22}"+ willingness_string + "{/size}" + " (disabled)" #Don't show the arousal and energy string if it's disabled to prevent overrun
            else:
                return taboo_break_string + self.name + taboo_break_string  + "\n{size=22}" + willingness_string + "\n" + self.build_energy_arousal_line(the_person) + "{/size}" + tooltip_string

        def build_energy_string(self, the_person):
            return "{color=#3C3CFF}" + str(self.guy_energy) + "{/color}/{color=#F0A8C0}" + str(self.girl_energy) + "{/color} {image=gui/extra_images/energy_token.png}"

        def build_arousal_string(self, the_person):
            girl_expected_arousal = str(int(self.girl_arousal * (1 + 0.1 * mc.sex_skills[self.skill_tag]))) #Estimate what they'll gain based on both of your skills to make the predictions as accurate as possible.
            guy_expected_arousal = str(int(self.guy_arousal * (1 + 0.1 * the_person.sex_skills[self.skill_tag])))
            return "{color=#3C3CFF}" + guy_expected_arousal + "{/color}/{color=#F0A8C0}" + girl_expected_arousal + "{/color} {image=gui/extra_images/arousal_token.png}"

        def build_energy_arousal_line(self, the_person):
            return "{size=22}" + self.build_energy_string(the_person) + " | " + self.build_arousal_string(the_person) + "{/size}"


    ##Initialization of requirement functions go down here. Can also be moved to init -1 eventually##

    def sleep_action_requirement():
        if time_of_day != 4:
            return "Too early to sleep."
        else:
            return True

    def faq_action_requirement():
        return True

    def hr_work_action_requirement():
        if time_of_day >= 4:
            return "Too late to work."
        else:
            return True

    def research_work_action_requirement():
        if time_of_day >= 4:
            return "Too late to work."
        elif mc.business.active_research_design == None:
            return "No research project set."
        else:
            return True

    def supplies_work_action_requirement():
        if time_of_day >= 4:
            return "Too late to work."
        else:
            return True

    def market_work_action_requirement():
        if time_of_day >= 4:
            return "Too late to work."
        else:
            return True

    def production_work_action_requirement():
        if time_of_day >= 4:
            return "Too late to work."
        elif len(mc.business.serum_production_array) == 0:
            return "No serum design set."
        else:
            return True

    def interview_action_requirement():
        if time_of_day >= 4:
            return "Too late to work."
        elif mc.business.get_employee_count() >= mc.business.max_employee_count:
            return "At employee limit."
        else:
            return True

    def serum_design_action_requirement():
        if time_of_day >= 4:
            return "Too late to work."
        else:
            return True

    def research_select_action_requirement():
        return True

    def production_select_action_requirement():
        return True

    def trade_serum_action_requirement():
        return True

    def sell_serum_action_requirement():
        return True

    def pick_supply_goal_action_requirement():
        return True

    def policy_purchase_requirement():
        return True

    def head_researcher_select_requirement():
        if mc.business.head_researcher is not None:
            return False
        elif __builtin__.len(mc.business.research_team) == 0:
            return "Nobody to pick."
        else:
            return True

    def pick_company_model_requirement():
        if mc.business.company_model is not None:
            return False
        elif not public_advertising_license_policy.is_active():
            return False
        elif mc.business.get_employee_count() == 0:
            return "Nobody to pick."
        else:
            return True

    def set_uniform_requirement():
        return strict_uniform_policy.is_active()

    def set_serum_requirement():
        if daily_serum_dosage_policy.is_owned() and not daily_serum_dosage_policy.is_active():
            return "Policy not active."
        else:
            return daily_serum_dosage_policy.is_active()

    def review_designs_action_requirement():
        return True

    ##Creator Defined Displayables, used in custom menues throughout the game##

    class VrenZipImage(renpy.display.im.ImageBase): #TODO: Move this to a more obvious file. Probably something to do along with a bunch of other refactoring.
        def __init__(self, position, filename, mtime=0, **properties):
            super(VrenZipImage, self).__init__(position, filename, mtime, **properties)
            self.position = position
            self.filename = filename

        def load(self):
            tries = 0
            max_tries = 5
            while tries < max_tries:
                global mobile_zip_dict
                try:
                    data = mobile_zip_dict[self.position].read(self.filename)
                    sio = io.BytesIO(data)
                    the_image = renpy.display.pgrender.load_image(sio, self.filename)
                    return the_image

                except (zipfile.BadZipfile, RuntimeError): #Not my fault! See: https://github.com/pfnet/pfio/issues/104
                    e = sys.exc_info()[1]
                    log_message("ERR " + str(tries) + ": "  + str(e))
                    tries += 1
                    if tries >= max_tries:
                        renpy.notify("Unsuccessful Recovery: " + self.position + ", Item: " + self.filename)
                        return renpy.display.pgrender.surface((2, 2), True)

                    else:
                        file_name = mobile_zip_dict[self.position].filename
                        mobile_zip_dict[self.position].close()
                        mobile_zip_dict[self.position] = zipfile.ZipFile(file_name, "a") #May have to convert to a renpy_file first, but I dthink Zipfile will have alreayd done that

    class Vren_Line(renpy.Displayable): # Caused large amounts of lag when used! No longer in use.
        def __init__(self, start, end, thickness, color, **kwargs):
            super(Vren_Line,self).__init__(**kwargs)
            ##Base attributes
            self.start = start ## tuple of x,y coords
            self.end = end ## tuple of x,y coords
            self.thickness = thickness
            self.color = color

            ##Store normal values for drawing anti-aliased lines
            self.normal_temp = [self.end[0]-self.start[0],self.end[1]-self.start[1]]
            self.normal = [0,0]
            self.normal[0] = -self.normal_temp[1]
            self.normal[1] = self.normal_temp[0]
            self.mag = math.sqrt(math.pow(self.normal[0],2) + math.pow(self.normal[1],2))
            self.normal = [(self.normal[0]*self.thickness)/self.mag,(self.normal[1]*self.thickness)/self.mag]

            ##Store point list so we don't have to calculate it each time
            self.start_right = [self.start[0]+self.normal[0],self.start[1]+self.normal[1]]
            self.start_left = [self.start[0]-self.normal[0],self.start[1]-self.normal[1]]
            self.end_left = [self.end[0]+self.normal[0],self.end[1]+self.normal[1]]
            self.end_right = [self.end[0]-self.normal[0],self.end[1]-self.normal[1]]

            self.point_list = [self.start_left,self.start_right,self.end_left,self.end_right]

        def render(self, the_width, the_height, st, at):

            render = renpy.Render(the_width,the_height)
            canvas = render.canvas()

            canvas.polygon(self.color,self.point_list) ##Draw the polygon. It will have jagged edges so we...
            canvas.aalines(self.color,False,self.point_list) ##Also draw a set of antialiased lines around the edge so it doesn't look jagged any more.
            return render

        def __eq__(self,other): ## Used to see if two Vren_Line objects are equivelent and thus don't need to be redrawn each time any of the variables is changed.
            if not type(other) is Vren_Line:
                return False

            if not (self.start == other.start and self.end == other.end and self.thickness == other.thickness and self.color == other.color): ##ie not the same
                return False
            else:
                return True

        def per_interact(self):
            renpy.redraw(self,0)

init -1:
    python:
        list_of_positions = [] # These are sex positions that the PC can make happen while having sex.
        list_of_girl_positions = [] # These are sex positiosn that the girl can make happen while having sex.

        day_names = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"] #Arrays that hold the names of the days of the week and times of day. Arrays start at 0.
        time_names = ["Early Morning","Morning","Afternoon","Evening","Night"]

transform scale_person(height_factor = 1):
    zoom height_factor

transform character_right():
    yalign 0.95
    yanchor 1.0
    xalign 1.0
    xanchor 1.0

transform position_shift(character_xalign = 1.0, scale_mod = 1.0, character_alpha = 1.0):
    yalign 0.95
    yanchor 1.0
    xanchor 1.0
    xalign character_xalign
    zoom scale_mod
    alpha character_alpha

transform clothing_fade():
    linear 1.0 alpha 0.0

transform breathe_animation():
    subpixel True
    ease 3.0 yzoom 0.995
    ease 3.0 yzoom 1.0
    repeat

transform hair_backplate_zoom(): #Zooms out, shrinking the hair backplate displayable by 10% so that it covers head gaps for small heads.
    zoom 0.9

init -2 style textbutton_style: ##The generic style used for text button backgrounds. TODO: Replace this with a pretty background image instead of a flat colour.
    padding [5,5]
    margin [5,5]
    background "#000080"
    insensitive_background "#222222"
    hover_background "#aaaaaa"

init -2 style textbutton_text_style: ##The generic style used for the text within buttons
    size 20
    italic True
    bold True
    color "#dddddd"
    outlines [(2,"#222222",0,0)]
    text_align 0.5

init -2 style menu_text_style:
    size 18
    italic True
    bold True
    color "#dddddd"
    outlines [(2,"#222222",0,0)]
    text_align 0.5

init -2 style outfit_style: ##The text style used for text inside of the outfit manager.
    size 16
    italic True
    color "#dddddd"
    outlines [(1,"#666666",0,0)]
    insensitive_color "#222222"
    hover_color "#ffffff"

init -2:
    default name = "Input Your First Name"
    default l_name = "Input Your Last Name"
    default b_name = "Input Your Business Name"

    python:
        def name_func(new_name):
            store.name = new_name

        def b_name_func(new_name):
            store.b_name = new_name

        def l_name_func(new_name):
            store.l_name = new_name

screen character_create_screen():

    default cha = 0
    default int = 0
    default foc = 0

    default h_skill = 0
    default m_skill = 0
    default r_skill = 0
    default p_skill = 0
    default s_skill = 0

    default F_skill = 0
    default O_skill = 0
    default V_skill = 0
    default A_skill = 0


    default name_select = 0

    default character_points = 20
    default stat_max = 4
    default work_skill_max = 4
    default sex_skill_max = 4

    imagebutton auto "/gui/Text_Entry_Bar_%s.png" action [SetScreenVariable("name_select",1), SetVariable("name","")] pos (320,800) xanchor 0.5 yanchor 0.5 alternate SetScreenVariable("name_select",0)
    imagebutton auto "/gui/Text_Entry_Bar_%s.png" action [SetScreenVariable("name_select",3), SetVariable("l_name","")] pos (320,880) xanchor 0.5 yanchor 0.5 alternate SetScreenVariable("name_select",0)
    imagebutton auto "/gui/Text_Entry_Bar_%s.png" action [SetScreenVariable("name_select",2), SetVariable("b_name","")] pos (320,960) xanchor 0.5 yanchor 0.5 alternate SetScreenVariable("name_select",0)
    imagebutton auto "/gui/button/choice_%s_background.png" action Return([[cha,int,foc],[h_skill,m_skill,r_skill,p_skill,s_skill],[F_skill,O_skill,V_skill,A_skill]]) pos (1560,900) xanchor 0.5 yanchor 0.5 sensitive character_points == 0


    if name_select == 1: #Name
        input default name pos(320,800) changed name_func xanchor 0.5 yanchor 0.5 style "menu_text_style" length 25
    else:
        text name pos(320,800) xanchor 0.5 yanchor 0.5 style "menu_text_style"

    if name_select == 3: #Last Name
        input default l_name pos(320,880) changed l_name_func xanchor 0.5 yanchor 0.5 style "menu_text_style" length 25
    else:
        text l_name pos(320,880) xanchor 0.5 yanchor 0.5 style "menu_text_style"

    if name_select == 2: #Business Name
        input default b_name pos(320,960) changed b_name_func xanchor 0.5 yanchor 0.5 style "menu_text_style" length 25
    else:
        text b_name pos(320,960) xanchor 0.5 yanchor 0.5 style "menu_text_style"


    if character_points > 0:
        text "Spend All Character Points to Proceed" style "menu_text_style" anchor(0.5,0.5) pos(1560,900)
    else:
        text "Finish Character Creation" style "menu_text_style" anchor(0.5,0.5) pos(1560,900)

    text "Character Points Remaining: [character_points]" style "menu_text_style" xalign 0.5 yalign 0.1 size 30
    hbox: #Main Stats Section
        yalign 0.7
        xalign 0.5
        xanchor 0.5
        frame:
            background "#1a45a1aa"
            vbox:
                xsize 550
                text "Main Stats (3 points/level)" style "menu_text_style" size 25
                null height 40
                hbox:
                    text "Charisma: " style "menu_text_style"
                    textbutton "<" action [SetScreenVariable("cha",cha-1), SetScreenVariable("character_points", character_points+3)] sensitive cha>0 style "textbutton_style" text_style "textbutton_text_style"
                    text str(cha) + "/[stat_max]" style "textbutton_text_style"
                    textbutton ">" action [SetScreenVariable("cha",cha+1), SetScreenVariable("character_points", character_points-3)] sensitive character_points>2 and cha<stat_max style "textbutton_style" text_style "textbutton_text_style"
                text "     Your visual appearance and force of personality. Charisma is the key attribute for selling serums and managing your business." style "menu_text_style"
                null height 30
                hbox:
                    text "Intelligence: " style "menu_text_style"
                    textbutton "<" action [SetScreenVariable("int",int-1), SetScreenVariable("character_points", character_points+3)] sensitive int>0 style "textbutton_style" text_style "textbutton_text_style"
                    text str(int) + "/[stat_max]" style "textbutton_text_style"
                    textbutton ">" action [SetScreenVariable("int",int+1), SetScreenVariable("character_points", character_points-3)] sensitive character_points>2 and int<stat_max style "textbutton_style" text_style "textbutton_text_style"
                text "     Your raw knowledge and ability to think quickly. Intelligence is the key attribute for research and development of serums." style "menu_text_style"
                null height 30
                hbox:
                    text "Focus: " style "menu_text_style"
                    textbutton "<" action [SetScreenVariable("foc",foc-1), SetScreenVariable("character_points", character_points+3)] sensitive foc>0 style "textbutton_style" text_style "textbutton_text_style"
                    text str(foc) + "/[stat_max]" style "textbutton_text_style"
                    textbutton ">" action [SetScreenVariable("foc",foc+1), SetScreenVariable("character_points", character_points-3)] sensitive character_points>2 and foc<stat_max style "textbutton_style" text_style "textbutton_text_style"
                text "     Your mental endurance and precision. Focus is the key attribute for production and supply procurement." style "menu_text_style"

        null width 40
        frame:
            background "#1a45a1aa"
            vbox:
                xsize 550
                text "Work Skills (1 point/level)" style "menu_text_style" size 25
                null height 40
                hbox:
                    text "Human Resources: " style "menu_text_style"
                    textbutton "<" action [SetScreenVariable("h_skill",h_skill-1), SetScreenVariable("character_points", character_points+1)] sensitive h_skill>0 style "textbutton_style" text_style "textbutton_text_style"
                    text str(h_skill)+"/[work_skill_max]" style "textbutton_text_style"
                    textbutton ">" action [SetScreenVariable("h_skill",h_skill+1), SetScreenVariable("character_points", character_points-1)] sensitive character_points>0 and h_skill<work_skill_max style "textbutton_style" text_style "textbutton_text_style"
                text "     Your skill at human resources. Crutial for maintaining an efficient business." style "menu_text_style"
                null height 30
                hbox:
                    text "Marketing: " style "menu_text_style"
                    textbutton "<" action [SetScreenVariable("m_skill",m_skill-1), SetScreenVariable("character_points", character_points+1)] sensitive m_skill>0 style "textbutton_style" text_style "textbutton_text_style"
                    text str(m_skill)+"/[work_skill_max]" style "textbutton_text_style"
                    textbutton ">" action [SetScreenVariable("m_skill",m_skill+1), SetScreenVariable("character_points", character_points-1)] sensitive character_points>0 and m_skill<work_skill_max style "textbutton_style" text_style "textbutton_text_style"
                text "     Your skill at marketing. Higher skill will allow you to ship more doses of serum per day." style "menu_text_style"
                null height 30
                hbox:
                    text "Research and Development: " style "menu_text_style"
                    textbutton "<" action [SetScreenVariable("r_skill",r_skill-1), SetScreenVariable("character_points", character_points+1)] sensitive r_skill>0 style "textbutton_style" text_style "textbutton_text_style"
                    text str(r_skill)+"/[work_skill_max]" style "textbutton_text_style"
                    textbutton ">" action [SetScreenVariable("r_skill",r_skill+1), SetScreenVariable("character_points", character_points-1)] sensitive character_points>0 and r_skill<work_skill_max style "textbutton_style" text_style "textbutton_text_style"
                text "     Your skill at researching new serum traits and designs. Critical for improving your serum inventory." style "menu_text_style"
                null height 30
                hbox:
                    text "Production: " style "menu_text_style"
                    textbutton "<" action [SetScreenVariable("p_skill",p_skill-1), SetScreenVariable("character_points", character_points+1)] sensitive p_skill>0 style "textbutton_style" text_style "textbutton_text_style"
                    text str(p_skill)+"/[work_skill_max]" style "textbutton_text_style"
                    textbutton ">" action [SetScreenVariable("p_skill",p_skill+1), SetScreenVariable("character_points", character_points-1)] sensitive character_points>0 and p_skill<work_skill_max style "textbutton_style" text_style "textbutton_text_style"
                text "     Your skill at producing serum in the production lab. Produced serums can then be sold for profit or kept for personal use." style "menu_text_style"
                null height 30
                hbox:
                    text "Supply Procurement: " style "menu_text_style"
                    textbutton "<" action [SetScreenVariable("s_skill",s_skill-1), SetScreenVariable("character_points", character_points+1)] sensitive s_skill>0 style "textbutton_style" text_style "textbutton_text_style"
                    text str(s_skill)+"/[work_skill_max]" style "textbutton_text_style"
                    textbutton ">" action [SetScreenVariable("s_skill",s_skill+1), SetScreenVariable("character_points", character_points-1)] sensitive character_points>0 and s_skill<work_skill_max style "textbutton_style" text_style "textbutton_text_style"
                text "     Your skill at obtaining raw supplies for your production division. Without supply, nothing can be created in the lab." style "menu_text_style"
                null height 30
        null width 40
        frame:
            background "#1a45a1aa"
            vbox:
                xsize 550
                text "Sex Skills (1 point/level)" style "menu_text_style" size 25
                null height 40
                hbox:
                    text "Foreplay: " style "menu_text_style"
                    textbutton "<" action [SetScreenVariable("F_skill",F_skill-1), SetScreenVariable("character_points", character_points+1)] sensitive F_skill>0 style "textbutton_style" text_style "textbutton_text_style"
                    text str(F_skill)+"/[sex_skill_max]" style "textbutton_text_style"
                    textbutton ">" action [SetScreenVariable("F_skill",F_skill+1), SetScreenVariable("character_points", character_points-1)] sensitive character_points>0 and F_skill<sex_skill_max style "textbutton_style" text_style "textbutton_text_style"
                text "     Your skill at foreplay, including fingering, kissing, and groping." style "menu_text_style"
                null height 30
                hbox:
                    text "Oral: " style "menu_text_style"
                    textbutton "<" action [SetScreenVariable("O_skill",O_skill-1), SetScreenVariable("character_points", character_points+1)] sensitive O_skill>0 style "textbutton_style" text_style "textbutton_text_style"
                    text str(O_skill)+"/[sex_skill_max]" style "textbutton_text_style"
                    textbutton ">" action [SetScreenVariable("O_skill",O_skill+1), SetScreenVariable("character_points", character_points-1)] sensitive character_points>0 and O_skill<sex_skill_max style "textbutton_style" text_style "textbutton_text_style"
                text "     Your skill at giving oral to women, as well as being a pleasant recipient." style "menu_text_style"
                null height 30
                hbox:
                    text "Vaginal: " style "menu_text_style"
                    textbutton "<" action [SetScreenVariable("V_skill",V_skill-1), SetScreenVariable("character_points", character_points+1)] sensitive V_skill>0 style "textbutton_style" text_style "textbutton_text_style"
                    text str(V_skill)+"/[sex_skill_max]" style "textbutton_text_style"
                    textbutton ">" action [SetScreenVariable("V_skill",V_skill+1), SetScreenVariable("character_points", character_points-1)] sensitive character_points>0 and V_skill<sex_skill_max style "textbutton_style" text_style "textbutton_text_style"
                text "     Your skill at vaginal sex in any position." style "menu_text_style"
                null height 30
                hbox:
                    text "Anal: " style "menu_text_style"
                    textbutton "<" action [SetScreenVariable("A_skill",A_skill-1), SetScreenVariable("character_points", character_points+1)] sensitive A_skill>0 style "textbutton_style" text_style "textbutton_text_style"
                    text str(A_skill)+"/[sex_skill_max]" style "textbutton_text_style"
                    textbutton ">" action [SetScreenVariable("A_skill",A_skill+1), SetScreenVariable("character_points", character_points-1)] sensitive character_points>0 and A_skill<sex_skill_max style "textbutton_style" text_style "textbutton_text_style"
                text "     Your skill at anal sex in any position." style "menu_text_style"
                null height 30

screen main_ui(): #The UI that shows most of the important information to the screen.
    frame:
        background "Info_Frame_1.png"
        xsize 600
        ysize 400
        yalign 0.0
        vbox:
            spacing -5
            text day_names[day%7] + " - " + time_names[time_of_day] + " (day [day])" style "menu_text_style" size 18
            textbutton "Outfit Manager" action Call("outfit_master_manager",from_current=True) style "textbutton_style" text_style "textbutton_text_style" xsize 220 tooltip "Design outfits to set as uniforms or give to suggest to women."
            textbutton "Check Inventory" action ui.callsinnewcontext("check_inventory_loop") style "textbutton_style" text_style "textbutton_text_style" xsize 220 tooltip "Check what serums you are currently carrying."
            if mc.stat_goal.completed or mc.work_goal.completed or mc.sex_goal.completed:
                textbutton "Character Sheet" action Show("mc_character_sheet") style "textbutton_style" text_style "textbutton_text_style" xsize 220 background "#44BB44" insensitive_background "#222222" hover_background "#aaaaaa" tooltip "Check your stats, skills, and goals."
            else:
                textbutton "Character Sheet" action Show("mc_character_sheet") style "textbutton_style" text_style "textbutton_text_style" xsize 220 tooltip "Check your stats, skills, and goals."

            textbutton "Arousal: [mc.arousal]/[mc.max_arousal] {image=gui/extra_images/arousal_token.png}":
                ysize 28
                text_style "menu_text_style"
                tooltip "Your personal arousal. When you reach your limit you will be forced to climax and your energy will drop."
                action NullAction()
                sensitive True

            textbutton "Energy: [mc.energy]/[mc.max_energy] {image=gui/extra_images/energy_token.png}":
                ysize 28
                text_style "menu_text_style"
                tooltip "Many actions require energy to perform, sex especially. Energy comes back slowly throughout the day, and most of it is recovered after a good nights sleep."
                action NullAction()
                sensitive True


screen tooltip_screen():
    zorder 50
    default hovered_enough_time = False
    $ tooltip = GetTooltip()
    if tooltip and len(tooltip) > 0:
        timer 0.7 action SetScreenVariable("hovered_enough_time",True)
        if hovered_enough_time:
            $ mouse_xy = renpy.get_mouse_pos()
            frame:
                if mouse_xy[1] > 1080/2:
                    background "#888888DD" xsize 450 xpos mouse_xy[0] ypos mouse_xy[1] yanchor 1.0
                else:
                    background "#888888DD" xsize 450 xpos mouse_xy[0] ypos mouse_xy[1]
                text "[tooltip]" style "menu_text_style"
    else:
        timer 0.1 action SetScreenVariable("hovered_enough_time",False)


screen goal_hud_ui():
    frame:
        background "Goal_Frame_1.png"
        yalign 0.5
        xsize 260
        ysize 250
        vbox:
            textbutton "Goal Information" action Show("mc_character_sheet") style "textbutton_style" text_style "textbutton_text_style" xsize 245 text_align 0.5 tooltip "Complete goals to earn experience, and spend experience to improve your stats and skills."
            for goal in [mc.stat_goal,mc.work_goal,mc.sex_goal]:
                if goal:
                    frame:
                        ysize 60
                        background None
                        bar value goal.get_progress_fraction() range 1 xalign 0.5
                        textbutton goal.name + "\n" + goal.get_reported_progress() text_style "menu_text_style" xalign 0.5 yanchor 0.5 yalign 0.5 text_size 12 text_text_align 0.5 action NullAction() sensitive True tooltip goal.description

transform phone_slide(start_yalign, goal_yalign, duration = 0.4):
    yalign start_yalign
    linear duration yalign goal_yalign

transform background_fade(max_time, time_used):
    alpha (max_time-time_used)/max_time
    linear max_time - time_used alpha 0

screen phone_hud_ui():
    default phone_up = False
    default start_phone_pos = 1.4
    default end_phone_pos = 1.4
    default start = True
    frame:
        background "#1a45a1aa"
        xsize 340
        ysize 400
        xanchor 1.0
        xalign 0.99
        at phone_slide(start_phone_pos, end_phone_pos)
        vbox:
            spacing 0
            if phone_up:
                textbutton "" style "textbutton_style":
                    text_style "textbutton_text_style" xsize 320 ysize 20 action [SetScreenVariable("phone_up",False), SetScreenVariable("end_phone_pos",1.4), SetScreenVariable("start_phone_pos",1.0)]
            else:
                textbutton "" style "textbutton_style":
                    text_style "textbutton_text_style" xsize 320 ysize 20 action [SetScreenVariable("phone_up",True), SetScreenVariable("end_phone_pos",1.0), SetScreenVariable("start_phone_pos",1.4)]

            null height 5

            for log_item in mc.log_items:
                if log_item is not None and log_item[0] is not None and log_item[1] is not None: #Minor hack to try and prevent any crashes. In theory log items should always exist.
                    $ fade_time = 5
                    $ time_diff = time.time() - log_item[2]
                    if time_diff > fade_time:
                        $ time_diff = fade_time

                    frame:
                        background "#33333388"
                        xsize 320
                        padding (0,0)
                        text log_item[0] style log_item[1] size 18 xsize 320 first_indent 20
                    frame:
                        background "#ff0000aa"
                        xsize 320
                        ysize 8
                        yanchor 1.0
                        yalign 0.95
                        xpadding 0
                        ypadding 0
                        at background_fade(5, time_diff)
                    null height 4





screen business_ui(): #Shows some information about your business.
    frame:
        background im.Flip("Info_Frame_1.png",vertical=True)
        xsize 600
        ysize 400
        yalign 1.0
        vbox:
            yanchor 1.0
            yalign 1.0
            spacing 5
            text "[mc.business.name]" style "menu_text_style" size 18 xalign 0.2
            textbutton "Employee Count: " + str(mc.business.get_employee_count()) + "/" + str(mc.business.max_employee_count):
                ysize 28
                text_style "menu_text_style"
                tooltip "Your current and maximum number of employees. Purchase new business policies from your main office to increase the number of employees you can have."
                action NullAction()
                sensitive True

            if mc.business.funds < 0:
                textbutton "Company Funds: $[mc.business.funds]":
                    ysize 28
                    text_style "menu_text_style"
                    text_color "#DD0000"
                    tooltip "The amount of money in your business account. If you are in the negatives for more than three days your loan defaults and the game is over!"
                    action NullAction()
                    sensitive True
            else:
                textbutton "Company Funds: $[mc.business.funds]":
                    ysize 28
                    text_style "menu_text_style"
                    tooltip "The amount of money in your business account. If you are in the negatives for more than three days your loan defaults and the game is over!"
                    action NullAction()
                    sensitive True

            textbutton "Daily Salary Cost: $"+ str(mc.business.calculate_salary_cost()):
                ysize 28
                text_style "menu_text_style"
                tooltip "The amount of money spent daily to pay your employees. Employees are not paid on weekends."
                action NullAction()
                sensitive True

            textbutton "Company Efficency: [mc.business.team_effectiveness]%":
                ysize 28
                text_style "menu_text_style"
                tooltip "The more employees you have the faster your company will become inefficent. Perform HR work at your office or hire someone to do it for you to raise your company efficency. All productivity is modified by company efficency."
                action NullAction()
                sensitive True

            textbutton "Current Raw Supplys: " + str(int(mc.business.supply_count)) +"/[mc.business.supply_goal]":
                ysize 28
                text_style "menu_text_style"
                tooltip "Your current and goal amounts of serum supply. Manufacturing serum requires supplies, spend time ordering supplies from your office or hire someone to do it for you. Raise your supply goal from your office if you want to keep more supply stockpiled."
                action NullAction()
                sensitive True

            if not mc.business.active_research_design == None:
                text "  Current Research: " style "menu_text_style"
                textbutton "    [mc.business.active_research_design.name] (" + str(int(mc.business.active_research_design.current_research))+"/[mc.business.active_research_design.research_needed])":
                    ysize 28
                    text_style "menu_text_style"
                    tooltip "The current research task of your R&D division. Visit them to set a new goal or to assemble a new serum design."
                    action NullAction()
                    sensitive True

            else:
                textbutton "Current Research: None!":
                    ysize 28
                    text_style "menu_text_style"
                    text_color "#DD0000"
                    tooltip "The current research task of your R&D division. Visit them to set a new goal or to assemble a new serum design."
                    action NullAction()
                    sensitive True

            textbutton "Review Staff" action Show("employee_overview") style "textbutton_style" text_style "textbutton_text_style" xsize 220 tooltip "Review all of your current employees."
            textbutton "Check Stock" action ui.callsinnewcontext("check_business_inventory_loop") style "textbutton_style" text_style "textbutton_text_style" xsize 220 tooltip "Check the doses of serum currently waiting to be sold or sitting in your production area."


screen end_of_day_update():
    add "Paper_Background.png"
    zorder 100
    text mc.business.name:
        style "textbutton_text_style"
        xanchor 0.5
        xalign 0.5
        yalign 0.07
        size 40

    frame:
        background "#1a45a1aa"
        xalign 0.1
        yalign 0.22
        xanchor 0.0
        vbox:
            xsize 1500
            ysize 200
            text "Daily Statistics:" style "textbutton_text_style" size 20
            text "     " + "Current Efficency Modifier: " + str(mc.business.team_effectiveness) + "%" style "textbutton_text_style"
            text "     " + "Production Potential: " + str(mc.business.production_potential) style "textbutton_text_style"
            text "     " + "Supplies Procured: " + str(mc.business.supplies_purchased) + " Units" style "textbutton_text_style"
            text "     " + "Production Used: " + str(mc.business.production_used) style "textbutton_text_style"
            text "     " + "Research Produced: " + str(mc.business.research_produced) style "textbutton_text_style"
            text "     " + "Sales Made: $" + str(mc.business.sales_made) style "textbutton_text_style"
            text "     " + "Daily Salary Paid: $" + str(mc.business.calculate_salary_cost()) style "textbutton_text_style"
            text "     " + "Serums Sold Today: " + str(mc.business.serums_sold) style "textbutton_text_style"
            text "     " + "Serums Ready for Sale: " + str(mc.business.sale_inventory.get_any_serum_count()) style "textbutton_text_style"

    frame:
        background "#1a45a1aa"
        xalign 0.1
        yalign 0.48
        xanchor 0.0
        yanchor 0.0

        viewport:
            mousewheel True
            scrollbars "vertical"
            xsize 1500
            ysize 350
            vbox:
                text "Highlights:" style "textbutton_text_style" size 20
                for item in mc.business.message_list:
                    text "     " + item style "textbutton_text_style" text_align 0.0

                for item in mc.business.counted_message_list:
                    text "     " + item + " x " + str(int(mc.business.counted_message_list[item])) style "textbutton_text_style" text_align 0.0

    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.9]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action Return()
        textbutton "End Day" align [0.5,0.5] style "button_text" text_style "textbutton_text_style"

screen employee_overview(white_list = None, black_list = None, person_select = False): #If select is True it returns the person's name who you click on. If it is false it is a normal overview menu that lets you bring up their detailed info.
    modal True
    zorder 100
    add "Paper_Background.png"
    default division_select = "none"
    default division_name = "All"
    python:
        if not white_list: #If a white list is passed we will only display people that are on the list
            white_list = []
        if not black_list:
            black_list = [] #IF a black list is passed we will not include anyone on the blacklist. Blacklist takes priority

    $ showing_team = []
    $ display_list = []
    $ valid_person_count = 0

    python:
        if division_select == "none":
            showing_team = [] + mc.business.research_team + mc.business.production_team + mc.business.supply_team + mc.business.market_team + mc.business.hr_team
            division_name = "Everyone"
        elif division_select == "r":
            showing_team = mc.business.research_team #ie. take a shallow copy, so we can modify the team without everything exploding.
            division_name = "Research"
        elif division_select == "p":
            showing_team = mc.business.production_team
            division_name = "Production"
        elif division_select == "s":
            showing_team = mc.business.supply_team
            division_name = "Supply Procurement"
        elif division_select == "m":
            showing_team = mc.business.market_team
            division_name = "Marketing"
        elif division_select == "h":
            showing_team = mc.business.hr_team
            division_name = "Human Resources"

        display_list = [person for person in showing_team if (not white_list or person in white_list) and (not black_list or person not in black_list)] #Create our actual display list using people who are either on the white list or not on the black list


    vbox:
        xalign 0.5
        xanchor 0.5
        yalign 0.05
        yanchor 0.0
        spacing 20
        frame:
            background "#1a45a1aa"
            xsize 1800
            ysize 100
            if person_select:
                text "Staff Selection" xalign 0.5 xanchor 0.5 yalign 0.5 yanchor 0.5 size 36 style "menu_text_style"
            else:
                text "Staff Review" xalign 0.5 xanchor 0.5 yalign 0.5 yanchor 0.5 size 36 style "menu_text_style"
        frame:
            background "#1a45a1aa" xsize 1800
            hbox:
                xalign 0.5
                xanchor 0.5
                spacing 40
                $ button_mappings = [["All","none"],["Research","r"],["Production","p"],["Supply","s"],["Marketing","m"],["Human Resources","h"]]
                for button_map in button_mappings:
                    frame:
                        ysize 80
                        if division_select == button_map[1]:
                            background "#4f7ad6"
                        else:
                            background "#1a45a1"
                        button:
                            action SetScreenVariable("division_select", button_map[1])
                            xsize 200
                            ysize 60
                            text button_map[0] xalign 0.5 xanchor 0.5 yalign 0.5 yanchor 0.5 style "textbutton_text_style"




        # text "Position: " + division_name style "menu_text_style" size 24 yalign 0.18 xalign 0.02 xanchor 0.0
        frame:
            yanchor 0.0
            background "#1a45a1aa"
            xsize 1800
            $ grid_count = 15
            # if person_select:
            #     $ grid_count += 1
            viewport:
                xsize 1800
                ysize  585
                scrollbars "vertical"
                mousewheel True

                grid grid_count len(display_list)+1:
                    text "Name" style "menu_text_style" xsize 120 size 14
                    # if person_select:
                    #     text "" style "menu_text_style" xsize 120 size 14
                    text "Salary" style "menu_text_style" xsize 120 size 14
                    text "Happiness" style "menu_text_style" xsize 120 size 14
                    text "Obedience" style "menu_text_style" xsize 120 size 14
                    text "Love" style "menu_text_style" xsize 120 size 14
                    text "Sluttiness" style "menu_text_style" xsize 120 size 14
                    text "Suggest" style "menu_text_style" xsize 120 size 14
                    text "Charisma" style "menu_text_style" xsize 120 size 14
                    text "Int" style "menu_text_style" xsize 120 size 14
                    text "Focus" style "menu_text_style" xsize 120 size 14
                    text "Research" style "menu_text_style" xsize 120 size 14
                    text "Production " style "menu_text_style" xsize 120 size 14
                    text "Supply" style "menu_text_style" xsize 120 size 14
                    text "Marketing " style "menu_text_style" xsize 120 size 14
                    text "HR" style "menu_text_style" xsize 120 size 14


                    for person in display_list:
                        vbox:
                            textbutton person.name + "\n" + person.last_name style "textbutton_style" text_style "menu_text_style" action Show("person_info_detailed",None,person) xmaximum 120 xfill True text_size 12
                            if person_select:
                                textbutton "Select" style "textbutton_style" text_style "menu_text_style" action Return(person) xsize 120 yalign 0.5 text_size 12
                        text "$" + str(person.salary) + "/day" style "menu_text_style" xsize 120 yalign 0.5 size 12
                        text str(int(person.happiness)) style "menu_text_style" xsize 120 yalign 0.5 size 12
                        text str(int(person.obedience)) style "menu_text_style" xsize 120 yalign 0.5 size 12
                        text str(int(person.love)) style "menu_text_style" xsize 120 yalign 0.5 size 12
                        text str(int(person.sluttiness)) style "menu_text_style" xsize 120 yalign 0.5 size 12
                        text str(int(person.suggestibility)) style "menu_text_style" xsize 120 yalign 0.5 size 12
                        text str(int(person.charisma)) style "menu_text_style" xsize 120 yalign 0.5 size 12
                        text str(int(person.int)) style "menu_text_style" xsize 120 yalign 0.5 size 12
                        text str(int(person.focus)) style "menu_text_style" xsize 120 yalign 0.5 size 12
                        text str(int(person.research_skill)) style "menu_text_style" xsize 120 yalign 0.5 size 12
                        text str(int(person.production_skill)) style "menu_text_style" xsize 120 yalign 0.5 size 12
                        text str(int(person.supply_skill)) style "menu_text_style" xsize 120 yalign 0.5 size 12
                        text str(int(person.market_skill)) style "menu_text_style" xsize 120 yalign 0.5 size 12
                        text str(int(person.hr_skill)) style "menu_text_style" xsize 120 yalign 0.5 size 12


    if not person_select:
        frame:
            background None
            anchor [0.5,0.5]
            align [0.5,0.88]
            xysize [500,125]
            imagebutton:
                align [0.5,0.5]
                auto "gui/button/choice_%s_background.png"
                focus_mask "gui/button/choice_idle_background.png"
                action Hide("employee_overview")
            textbutton "Return" align [0.5,0.5] style "return_button_style" text_style "return_button_style"


screen person_info_ui(the_person, display_layer = "solo"): #Used to display stats for a person while you're talking to them.
    layer "solo" #It is cleared whenever we draw a person or clear them off the screen.
    $ formatted_tooltip = ""
    $ formatted_obedience_tooltip = ""
    python:
        positive_effects = ""
        negative_effects = ""
        for situation in the_person.situational_sluttiness:
            if the_person.situational_sluttiness[situation][0] > 0: #We purposefully ignore 0 so we don't show null sluttiness modifiers.
                positive_effects += get_coloured_arrow(1)+get_red_heart(the_person.situational_sluttiness[situation][0])+" - " + the_person.situational_sluttiness[situation][1] + "\n"
            elif the_person.situational_sluttiness[situation][0] < 0:
                negative_effects += get_coloured_arrow(-1)+get_red_heart(-the_person.situational_sluttiness[situation][0])+" - " + the_person.situational_sluttiness[situation][1] + "\n"
        formatted_tooltip += positive_effects + negative_effects
        formatted_tooltip += "The higher a girls sluttiness the more slutty actions she will consider acceptable and normal. Temporary sluttiness (" + get_red_heart(20) + ") is easier to raise but drops slowly over time. Core sluttiness (" + get_gold_heart(20) + ") is permanent, but only increases slowly unless a girl is suggestable."

        positive_effects = ""
        negative_effects = ""
        for situation in the_person.situational_obedience:
            if the_person.situational_obedience[situation][0] > 0:
                positive_effects += get_coloured_arrow(1)+"+"+__builtin__.str(the_person.situational_obedience[situation][0])+ " Obedience - " + the_person.situational_obedience[situation][1] + "\n"
            elif the_person.situational_obedience[situation][0] < 0:
                negative_effects += get_coloured_arrow(1)+""+__builtin__.str(the_person.situational_obedience[situation][0])+ " Obedience - " + the_person.situational_obedience[situation][1] + "\n"
        formatted_obedience_tooltip += positive_effects + negative_effects
        formatted_obedience_tooltip += "Girls with high obedience will listen to commands even when they would prefer not to and are willing to work for less pay. Girls who are told to do things they do not like will lose happiness, and low obedience girls are likely to refuse altogether."

    frame:
        background "gui/topbox.png"
        xsize 1100
        ysize 200
        yalign 0.0
        xalign 0.5
        xanchor 0.5
        hbox:
            xanchor 0.5
            xalign 0.5
            yalign 0.3
            spacing 100
            vbox:
                if the_person.title:
                    text the_person.title style "menu_text_style" size 30
                else:
                    text "???" style "menu_text_style" font the_person.char.what_args["font"] color the_person.char.what_args["color"] size 30

                if mc.business.get_employee_title(the_person) == "None":
                    text "     Job: Not employed." style "menu_text_style"
                else:
                    text "     Job: " + mc.business.get_employee_title(the_person) style "menu_text_style"

                for role in the_person.special_role:
                    if not role.hidden:
                        text "       - " + role.role_name style "menu_text_style" size 14

            vbox:
                if the_person.arousal >= 20:
                    textbutton "Arousal: [the_person.arousal]/[the_person.max_arousal] (+" + get_red_heart(__builtin__.int(the_person.arousal/4)) + ") {image=gui/extra_images/arousal_token.png}":
                        ysize 24
                        text_style "menu_text_style"
                        tooltip "When a girl is brought to 100% arousal she will start to climax. Climaxing will instantly turn temporary sluttiness into core sluttiness, as well as make the girl happy. The more aroused you make a girl the more sex positions she is willing to consider."
                        action NullAction()
                        sensitive True
                else:
                    textbutton "Arousal: 0/[the_person.max_arousal] {image=gui/extra_images/arousal_token.png}":
                        ysize 24
                        text_style "menu_text_style"
                        tooltip "When a girl is brought to 100% arousal she will start to climax. Climaxing will instantly turn temporary sluttiness into core sluttiness, as well as make the girl happy. The more aroused you make a girl the more sex positions she is willing to consider."
                        action NullAction()
                        sensitive True

                textbutton "Energy: [the_person.energy]/[the_person.max_energy] {image=gui/extra_images/energy_token.png}":
                    ysize 24
                    text_style "menu_text_style"
                    tooltip "Energy is spent while having sex, with more energy spent on positions that give the man more pleasure. Some energy comes back each turn, and a lot of energy comes back over night."
                    action NullAction()
                    sensitive True

                textbutton "Happiness: [the_person.happiness]":
                    ysize 24
                    text_style "menu_text_style"
                    tooltip "The happier a girl the more tolerant she will be of low pay and unpleasant interactions. High or low happiness will return to it's default value over time."
                    action NullAction()
                    sensitive True

                textbutton "Suggestibility: [the_person.suggestibility]%":
                    ysize 24
                    text_style "menu_text_style"
                    tooltip "How likely this character is to increase her core sluttiness. Every time chunk there is a chance to change 1 point of temporary sluttiness (" + get_red_heart(5) + ") into core sluttiness (" + get_gold_heart(5) + ") as long as temporary sluttiness is higher."
                    action NullAction()
                    sensitive True

                textbutton "Sluttiness: " + get_heart_image_list(the_person):
                    ysize 24
                    text_style "menu_text_style"
                    tooltip formatted_tooltip
                    action NullAction()
                    sensitive True

                textbutton "Love: [the_person.love]":
                    ysize 24
                    text_style "menu_text_style"
                    tooltip "Girls who love you will be more willing to have sex when you're in private (as long as they aren't family) and be more devoted to you. Girls who hate you will have a lower effective sluttiness regardless of the situation."
                    action NullAction()
                    sensitive True

                textbutton "Obedience: [the_person.obedience] - " + get_obedience_plaintext(the_person.obedience):
                    ysize 24
                    text_style "menu_text_style"
                    tooltip formatted_obedience_tooltip
                    action NullAction()
                    sensitive True

            vbox:
                textbutton "Detailed Information" action Show("person_info_detailed",the_person=the_person) style "textbutton_style" text_style "textbutton_text_style"



screen person_info_detailed(the_person):
    add "Paper_Background.png"
    modal True
    zorder 100
    default hr_base = the_person.charisma*3 + the_person.hr_skill*2 + the_person.int + 10
    default market_base = the_person.charisma*3 + the_person.market_skill*2 + the_person.focus + 10
    default research_base = the_person.int*3 + the_person.research_skill*2 + the_person.focus + 10
    default prod_base = the_person.focus*3 + the_person.production_skill*2 + the_person.int + 10
    default supply_base = the_person.focus*3 + the_person.supply_skill*2 + the_person.charisma + 10
    vbox:
        spacing 25
        xalign 0.5
        xanchor 0.5
        yalign 0.2
        frame:
            xsize 1750
            ysize 120
            xalign 0.5
            background "#1a45a1aa"
            vbox:
                xalign 0.5 xanchor 0.5
                text "[the_person.name] [the_person.last_name]" style "menu_text_style" size 30 xalign 0.5 yalign 0.5 yanchor 0.5 color the_person.char.who_args["color"] font the_person.char.what_args["font"]
                if not mc.business.get_employee_title(the_person) == "None":
                    text "Position: " + mc.business.get_employee_title(the_person) + " ($[the_person.salary]/day)" style "menu_text_style" xalign 0.5 yalign 0.5 yanchor 0.5

                $ visible_roles = []
                $ role_string = "Special Roles: "
                python:
                    for role in the_person.special_role:
                        if not role.hidden:
                            visible_roles.append(role.role_name)

                    if visible_roles:
                        role_string += visible_roles[0]
                        for role in visible_roles[1::]: #Slicing off the first manually let's us use commas correctly.
                            role_string += ", " + role
                if visible_roles:
                    text role_string style "menu_text_style" xalign 0.5 yalign 0.5 yanchor 0.5

        hbox:
            xsize 1750
            xalign 0.5
            xanchor 0.5
            spacing 30
            frame:
                background "#1a45a1aa"
                xsize 325
                ysize 450
                vbox:
                    text "Status and Info" style "menu_text_style" size 22
                    text "Happiness: [the_person.happiness]" style "menu_text_style"
                    text "Suggestibility: [the_person.suggestibility]" style "menu_text_style"
                    text "Sluttiness: [the_person.sluttiness]" style "menu_text_style"
                    text "Love: [the_person.love]" style "menu_text_style"
                    text "Obedience: [the_person.obedience] - " + get_obedience_plaintext(the_person.obedience) style "menu_text_style"

                    text "Age: [the_person.age]" style "menu_text_style"
                    text "Cup Size: [the_person.tits]" style "menu_text_style"
                    if girlfriend_role in the_person.special_role:
                        text "Relationship: Girlfriend" style "menu_text_style"
                    else:
                        text "Relationship: [the_person.relationship]" style "menu_text_style"

                    if the_person.relationship != "Single":
                        text "Significant Other: [the_person.SO_name]" style "menu_text_style"
                    elif girlfriend_role in the_person.special_role:
                        text "Significant Other: [mc.name]" style "menu_text_style"

                    text "Kids: [the_person.kids]" style "menu_text_style"
                    #TODO: Decide how much of this information we want to give to the player directly and how much we want to have delivered in game.
                    if persistent.pregnancy_pref > 0:
                        if persistent.pregnancy_pref == 1:
                            text "Fertility: " + str(round(the_person.fertility_percent)) + "%" style "menu_text_style"
                        if persistent.pregnancy_pref == 2:
                            $ modified_fertility = the_person.calculate_realistic_fertility()
                            text "Fertility: " + str(round(modified_fertility)) + "%" style "menu_text_style"
                            text "Monthly Peak Day: " + str(the_person.ideal_fertile_day ) style "menu_text_style"
                            #TODO: replace this with less specific info. Replace fertility peak with the_person.fertility_cycle_string()

                        if the_person.event_triggers_dict.get("birth_control_status", None) is None:
                            text "Birth Control: Unknown" style "menu_text_style" size 16
                        else:
                            if the_person.event_triggers_dict.get("birth_control_status"):
                                #text "Taking Birth Control: Yes" style "menu_text_style"
                                text "Birth Control: Yes {size=12}(Known " + str(day - the_person.event_triggers_dict.get("birth_control_known_day")) + " days ago){/size}" style "menu_text_style" size 16
                            else:
                                text "Birth Control: No {size=12}(Known " + str(day - the_person.event_triggers_dict.get("birth_control_known_day")) + " days ago){/size}" style "menu_text_style" size 16
                        #text "Birth Control: " + str(the_person.on_birth_control) style "menu_text_style" #TODO less specific info

            frame:
                background "#1a45a1aa"
                xsize 325
                ysize 450
                vbox:
                    text "Characteristics" style "menu_text_style" size 22
                    text "Charisma: [the_person.charisma]" style "menu_text_style"
                    text "Intelligence: [the_person.int]" style "menu_text_style"
                    text "Focus: [the_person.focus]" style "menu_text_style"

                    $ list_of_relationships = town_relationships.get_relationship_type_list(the_person, visible = True)
                    if list_of_relationships:
                        text "Other relationships:"  style "menu_text_style"
                        viewport:
                            xsize 325
                            yfill True
                            scrollbars "vertical"
                            mousewheel True
                            vbox:
                                for relationship in list_of_relationships:
                                    #TODO: Once we have more relationship stuff going on make this only show when the relationship is known.
                                    text "    " + relationship[0].name + " " + relationship[0].last_name + " - " + relationship[1] style "menu_text_style" size 14
            frame:
                background "#1a45a1aa"
                xsize 325
                ysize 450
                vbox:
                    text "Work Skills" style "menu_text_style" size 22
                    text "HR Skill: [the_person.hr_skill]" style "menu_text_style"
                    text "Marketing Skill: [the_person.market_skill]" style "menu_text_style"
                    text "Researching Skill: [the_person.research_skill]" style "menu_text_style"
                    text "Production Skill: [the_person.production_skill]" style "menu_text_style"
                    text "Supply Skill: [the_person.supply_skill]" style "menu_text_style"

            frame:
                background "#1a45a1aa"
                xsize 325
                ysize 450
                vbox:
                    text "Sex Skills" style "menu_text_style" size 22
                    text "Foreplay Skill: " + str(the_person.sex_skills["Foreplay"]) style "menu_text_style"
                    text "Oral Skill: " + str(the_person.sex_skills["Oral"]) style "menu_text_style"
                    text "Vaginal Skill: " + str(the_person.sex_skills["Vaginal"]) style "menu_text_style"
                    text "Anal: " + str(the_person.sex_skills["Anal"]) style "menu_text_style"
                    text "Sex Record:"  style "menu_text_style" size 22
                    viewport:
                        xsize 325
                        yfill True
                        scrollbars "vertical"
                        mousewheel True
                        vbox:
                            for the_record in the_person.sex_record:
                                text the_record + ": " + str(the_person.sex_record.get(the_record, 0)) style "menu_text_style" size 14
                            # for relationship in list_of_relationships:
                            #     #TODO: Once we have more relationship stuff going on make this only show when the relationship is known.
                            #     text "    " + relationship[0].name + " " + relationship[0].last_name + " - " + relationship[1] style "menu_text_style" size 14

            frame:
                background "#1a45a1aa"
                xsize 325
                ysize 450
                vbox:
                    text "Currently Affected By:" style "menu_text_style" size 22
                    if the_person.serum_effects:
                        default selected_serum = None
                        for serum in the_person.serum_effects:
                            if serum == selected_serum:
                                textbutton serum.name + " : " + str(serum.duration - serum.duration_counter) + " Turns Left":
                                    action [SetScreenVariable("selected_serum", None), Hide("serum_tooltip")]
                                    style "textbutton_style"
                                    text_style "textbutton_text_style"
                                    text_size 12
                                    background "#888888"
                            else:
                                textbutton serum.name + " : " + str(serum.duration - serum.duration_counter) + " Turns Left":
                                    action SetScreenVariable("selected_serum", serum)
                                    hovered [SetScreenVariable("selected_serum", None), Show("serum_tooltip", None, serum, 0.65)]
                                    unhovered Hide("serum_tooltip")
                                    style "textbutton_style"
                                    text_style "textbutton_text_style"
                                    text_size 12

                    else:
                        text "No active serums." style "menu_text_style"

                    null height 20


        hbox:
            xsize 1750
            spacing 30
            $ master_opinion_dict = dict(the_person.opinions, **the_person.sexy_opinions)
            frame:
                background "#1a45a1aa"
                xsize 415
                ysize 200
                vbox:
                    text "Loves" style "menu_text_style" size 22
                    for opinion in master_opinion_dict:
                        if master_opinion_dict[opinion][0] == 2:
                            if master_opinion_dict[opinion][1]:
                                text "   " + opinion style "menu_text_style"
                            else:
                                text "   ????" style "menu_text_style"

            frame:
                background "#1a45a1aa"
                xsize 415
                ysize 200
                vbox:
                    text "Likes" style "menu_text_style" size 22
                    for opinion in master_opinion_dict:
                        if master_opinion_dict[opinion][0] == 1:
                            if master_opinion_dict[opinion][1]:
                                text "   " + opinion style "menu_text_style"
                            else:
                                text "   ????" style "menu_text_style"

            frame:
                background "#1a45a1aa"
                xsize 415
                ysize 200
                vbox:
                    text "Dislikes" style "menu_text_style" size 22
                    for opinion in master_opinion_dict:
                        if master_opinion_dict[opinion][0] == -1:
                            if master_opinion_dict[opinion][1]:
                                text "   " + opinion style "menu_text_style"
                            else:
                                text "   ????" style "menu_text_style"

            frame:
                background "#1a45a1aa"
                xsize 415
                ysize 200
                vbox:
                    text "Hates" style "menu_text_style" size 22
                    for opinion in master_opinion_dict:
                        if master_opinion_dict[opinion][0] == -2:
                            if master_opinion_dict[opinion][1]:
                                text "   " + opinion style "menu_text_style"
                            else:
                                text "   ????" style "menu_text_style"

    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action [Hide("serum_tooltip"), Hide("person_info_detailed")]
        textbutton "Return" align [0.5,0.5] text_style "return_button_style"


screen mc_character_sheet():
    add "Paper_Background.png"
    modal True
    zorder 100
    vbox:
        xanchor 0.5
        xalign 0.5
        yalign 0.2
        frame:
            background "#1a45a1aa"
            vbox:
                xsize 1620
                text mc.name + " " + mc.last_name style "menu_text_style" size 40 xanchor 0.5 xalign 0.5
                text "Owner of: " + mc.business.name style "menu_text_style" size 30 xanchor 0.5 xalign 0.5
        null height 60
        hbox:
            xanchor 0.5
            xalign 0.5
            yalign 0.4
            spacing 40
            frame:
                background "#1a45a1aa"
                xalign 0.5
                xanchor 0.5
                vbox:
                    xsize 500
                    text "Main Stats" style "menu_text_style" size 32 xalign 0.5
                    text "Unspent Points: " + str(mc.free_stat_points) style "menu_text_style" xalign 0.5
                    hbox:
                        xalign 0.5
                        text "Charisma: " + str(mc.charisma) + "/" + str(mc.max_stats) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_stat, "cha") sensitive mc.free_stat_points > 0 and mc.charisma<mc.max_stats yanchor 0.5 yalign 0.5

                    hbox:
                        xalign 0.5
                        text "Intelligence: " + str(mc.int) + "/" + str(mc.max_stats) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_stat, "int") sensitive mc.free_stat_points > 0 and mc.int<mc.max_stats yanchor 0.5 yalign 0.5

                    hbox:
                        xalign 0.5
                        text "Focus: " + str(mc.focus) + "/" + str(mc.max_stats) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_stat, "foc") sensitive mc.free_stat_points > 0 and mc.focus<mc.max_stats yanchor 0.5 yalign 0.5


                    null height 40
                    frame:
                        background "#888888"
                        xsize 500
                        vbox:
                            xalign 0.5
                            if mc.stat_goal:
                                text "Goal: " + mc.stat_goal.name style "menu_text_style" xalign 0.5 size 24
                                text "    " + mc.stat_goal.description style "menu_text_style" xalign 0.5
                                frame:
                                    ysize 60
                                    background None
                                    bar value mc.stat_goal.get_progress_fraction() range 1 xalign 0.5
                                    text mc.stat_goal.get_reported_progress() style "menu_text_style" xalign 0.5 yanchor 0.5 yalign 0.5
                                if mc.stat_goal.completed:
                                    textbutton "Collect Reward" xalign 0.5 action Function(mc.complete_goal,mc.stat_goal) style "textbutton_style" text_style "textbutton_text_style"
                                else:
                                    textbutton "Replace Goal (1/day)" xalign 0.5 action Function(mc.scrap_goal,mc.stat_goal) style "textbutton_style" text_style "textbutton_text_style" sensitive mc.scrap_goal_available and not mc.stat_goal.mandatory
                            else:
                                text "Goal: No goals available!" style "menu_text_style" xalign 0.5

            frame:
                background "#1a45a1aa"
                xalign 0.5
                xanchor 0.5
                vbox:
                    xsize 500
                    text "Work Skills" style "menu_text_style" size 32 xalign 0.5
                    text "Unspent Points: " + str(mc.free_work_points) style "menu_text_style" xalign 0.5
                    hbox:
                        xalign 0.5
                        text "Human Resources: " + str(mc.hr_skill) + "/" + str(mc.max_work_skills) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_work_skill, "hr") sensitive mc.free_work_points > 0 and mc.hr_skill < mc.max_work_skills yanchor 0.5 yalign 0.5
                    hbox:
                        xalign 0.5
                        text "Marketing: " + str(mc.market_skill) + "/" + str(mc.max_work_skills) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_work_skill, "market") sensitive mc.free_work_points > 0 and mc.market_skill < mc.max_work_skills yanchor 0.5 yalign 0.5
                    hbox:
                        xalign 0.5
                        text "Research and Development: " + str(mc.research_skill) + "/" + str(mc.max_work_skills) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_work_skill, "research") sensitive mc.free_work_points > 0 and mc.research_skill < mc.max_work_skills yanchor 0.5 yalign 0.5
                    hbox:
                        xalign 0.5
                        text "Production: " + str(mc.production_skill) + "/" + str(mc.max_work_skills) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_work_skill, "production") sensitive mc.free_work_points > 0 and mc.production_skill < mc.max_work_skills yanchor 0.5 yalign 0.5
                    hbox:
                        xalign 0.5
                        text "Supply Procurement: " + str(mc.supply_skill) + "/" + str(mc.max_work_skills) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_work_skill, "supply") sensitive mc.free_work_points > 0 and mc.supply_skill < mc.max_work_skills yanchor 0.5 yalign 0.5

                    null height 40
                    frame:
                        background "#888888"
                        xsize 500
                        vbox:
                            xalign 0.5
                            if mc.work_goal:
                                text "Goal: " + mc.work_goal.name style "menu_text_style" xalign 0.5 size 24
                                text "    " + mc.work_goal.description style "menu_text_style" xalign 0.5
                                frame:
                                    ysize 60
                                    background None
                                    bar value mc.work_goal.get_progress_fraction() range 1 xalign 0.5
                                    text mc.work_goal.get_reported_progress() style "menu_text_style" xalign 0.5 yanchor 0.5 yalign 0.5
                                if mc.work_goal.completed:
                                    textbutton "Collect Reward" xalign 0.5 action Function(mc.complete_goal,mc.work_goal) style "textbutton_style" text_style "textbutton_text_style"
                                else:
                                    textbutton "Replace Goal (1/day)" xalign 0.5 action Function(mc.scrap_goal,mc.work_goal) style "textbutton_style" text_style "textbutton_text_style" sensitive mc.scrap_goal_available and not mc.work_goal.mandatory
                            else:
                                text "Goal: No goals available!" style "menu_text_style" xalign 0.5

            frame:
                background "#1a45a1aa"
                xalign 0.5
                xanchor 0.5
                vbox:
                    xsize 500
                    text "Sex Skills" style "menu_text_style" size 32 xalign 0.5
                    text "Unspent Points: " + str(mc.free_sex_points) style "menu_text_style" xalign 0.5
                    hbox:
                        xalign 0.5
                        text "Stamina: " + str(mc.max_energy) + "/" +str(mc.max_energy_cap) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_sex_skill, "stam") sensitive mc.free_sex_points > 0 and mc.max_energy<mc.max_energy_cap yanchor 0.5 yalign 0.5
                    hbox:
                        xalign 0.5
                        text "Foreplay: " + str(mc.sex_skills["Foreplay"]) + "/" + str(mc.max_sex_skills) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_sex_skill, "Foreplay") sensitive mc.free_sex_points > 0 and mc.sex_skills["Foreplay"]<mc.max_sex_skills yanchor 0.5 yalign 0.5
                    hbox:
                        xalign 0.5
                        text "Oral: " + str(mc.sex_skills["Oral"]) + "/" + str(mc.max_sex_skills) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_sex_skill, "Oral") sensitive mc.free_sex_points > 0 and mc.sex_skills["Oral"]<mc.max_sex_skills yanchor 0.5 yalign 0.5
                    hbox:
                        xalign 0.5
                        text "Vaginal: " + str(mc.sex_skills["Vaginal"]) + "/" + str(mc.max_sex_skills) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_sex_skill, "Vaginal") sensitive mc.free_sex_points > 0 and mc.sex_skills["Vaginal"]<mc.max_sex_skills yanchor 0.5 yalign 0.5
                    hbox:
                        xalign 0.5
                        text "Anal: " + str(mc.sex_skills["Anal"]) + "/" + str(mc.max_sex_skills) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_sex_skill, "Anal") sensitive mc.free_sex_points > 0 and mc.sex_skills["Anal"]<mc.max_sex_skills yanchor 0.5 yalign 0.5

                    null height 40
                    frame:
                        background "#888888"
                        xsize 500
                        vbox:
                            xalign 0.5
                            if mc.sex_goal:
                                text "Goal: " + mc.sex_goal.name style "menu_text_style" xalign 0.5 size 24
                                text "    " + mc.sex_goal.description style "menu_text_style" xalign 0.5
                                frame:
                                    ysize 60
                                    background None
                                    bar value mc.sex_goal.get_progress_fraction() range 1 xalign 0.5
                                    text mc.sex_goal.get_reported_progress() style "menu_text_style" xalign 0.5 yanchor 0.5 yalign 0.5
                                if mc.sex_goal.completed:
                                    textbutton "Collect Reward" xalign 0.5 action Function(mc.complete_goal,mc.sex_goal) style "textbutton_style" text_style "textbutton_text_style"
                                else:
                                    textbutton "Replace Goal (1/day)" xalign 0.5 action Function(mc.scrap_goal,mc.sex_goal) style "textbutton_style" text_style "textbutton_text_style" sensitive mc.scrap_goal_available and not mc.sex_goal.mandatory
                            else:
                                text "Goal: No goals available!" style "menu_text_style" xalign 0.5

    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action Hide("mc_character_sheet")
        textbutton "Return" align [0.5,0.5] text_style "return_button_style"





screen interview_ui(the_candidates,count):
    default current_selection = 0
    default the_candidate = the_candidates[current_selection]
    vbox:
        yalign 0.2
        xalign 0.4
        xanchor 0.5
        spacing 30
        frame:
            background "#1a45a1aa"
            ysize 80
            xsize 1320
            xalign 0.5
            xanchor 0.5
            text "[the_candidate.name] [the_candidate.last_name]" style "menu_text_style" size 50 xanchor 0.5 xalign 0.5 color the_candidate.char.who_args["color"] font the_candidate.char.what_args["font"]

        hbox:
            xsize 1320
            spacing 30
            frame:
                background "#1a45a1aa"
                xsize 420
                ysize 550
                vbox:
                    text "Personal Information" style "menu_text_style" size 26 xalign 0.5 xanchor 0.5 #Info about the person: age, height, happiness, obedience, etc.
                    text "Age: [the_candidate.age]" style "menu_text_style" size 16
                    text "Required Salary: $[the_candidate.salary]/day" style "menu_text_style" size 16


            frame:
                background "#1a45a1aa"
                xsize 420
                ysize 550
                vbox:
                    text "Stats and Skills" style "menu_text_style" size 26 xalign 0.5 xanchor 0.5 #Info about the persons raw stats, work skills, and sex skills
                    text "Stats" style "menu_text_style" size 20
                    text "    Charisma: [the_candidate.charisma]" style "menu_text_style" size 16
                    text "    Intelligence: [the_candidate.int]" style "menu_text_style" size 16
                    text "    Focus: [the_candidate.focus]" style "menu_text_style" size 16
                    text "Work Skills" style "menu_text_style" size 20
                    text "    HR: [the_candidate.hr_skill]" style "menu_text_style" size 16
                    text "    Marketing: [the_candidate.market_skill]" style "menu_text_style" size 16
                    text "    Research: [the_candidate.research_skill]" style "menu_text_style" size 16
                    text "    Production: [the_candidate.production_skill]" style "menu_text_style" size 16
                    text "    Supply: [the_candidate.supply_skill]" style "menu_text_style" size 16
                    if recruitment_knowledge_four_policy.is_active():
                        text "Sex Skills" style "menu_text_style" size 20
                        text "    Foreplay: " + str(the_candidate.sex_skills["Foreplay"]) style "menu_text_style" size 16
                        text "    Oral: " + str(the_candidate.sex_skills["Oral"]) style "menu_text_style" size 16
                        text "    Vaginal: " + str(the_candidate.sex_skills["Vaginal"]) style "menu_text_style" size 16
                        text "    Anal: " + str(the_candidate.sex_skills["Anal"]) style "menu_text_style" size 16

            frame:
                $ master_opinion_dict = dict(the_candidate.opinions, **the_candidate.sexy_opinions)
                background "#1a45a1aa"
                xsize 420
                ysize 550
                vbox:
                    text "Opinions" style "menu_text_style" size 26 xalign 0.5 xanchor 0.5 #Info about the persons loves, likes, dislikes, and hates
                    text "Loves" style "menu_text_style" size 20
                    for opinion in master_opinion_dict:
                        if master_opinion_dict[opinion][0] == 2:
                            if master_opinion_dict[opinion][1]:
                                text "    " + opinion style "menu_text_style" size 16
                            else:
                                text "    ????" style "menu_text_style" size 16

                    text "Likes" style "menu_text_style" size 20
                    for opinion in master_opinion_dict:
                        if master_opinion_dict[opinion][0] == 1:
                            if master_opinion_dict[opinion][1]:
                                text "    " + opinion style "menu_text_style" size 16
                            else:
                                text "    ????" style "menu_text_style"

                    text "Dislikes" style "menu_text_style" size 20
                    for opinion in master_opinion_dict:
                        if master_opinion_dict[opinion][0] == -1:
                            if master_opinion_dict[opinion][1]:
                                text "    " + opinion style "menu_text_style" size 16
                            else:
                                text "    ????" style "menu_text_style" size 16


                    text "Hates" style "menu_text_style" size 20
                    for opinion in master_opinion_dict:
                        if master_opinion_dict[opinion][0] == -2:
                            if master_opinion_dict[opinion][1]:
                                text "    " + opinion style "menu_text_style" size 16
                            else:
                                text "    ????" style "menu_text_style" size 16

        frame:
            background "#1a45a1aa"
            xsize 1320
            ysize 200
            vbox:
                text "Expected Production" style "menu_text_style" size 30
                text "    Human Resources: +" + str(the_candidate.hr_skill*2 + the_candidate.charisma*3 + the_candidate.int + 10) + "% Company efficency per time chunk." style "menu_text_style" size 16
                text "    Marketing: " + str(the_candidate.market_skill*2 + the_candidate.charisma*3 + the_candidate.focus + 10) + " Units of serum sold per time chunk." style "menu_text_style" size 16
                text "    Research and Development: " + str(the_candidate.research_skill*2 + the_candidate.int*3 + the_candidate.focus + 10) + " Research points per time chunk." style "menu_text_style" size 16
                text "    Production: " + str(the_candidate.production_skill*2 + the_candidate.focus*3 + the_candidate.int + 10) + " Production points per time chunk." style "menu_text_style" size 16
                text "    Supply Procurement: " + str(the_candidate.supply_skill*2 + the_candidate.focus*3 + the_candidate.charisma + 10) + " Units of supply per time chunk." style "menu_text_style" size 16

        frame:
            background "#1a45a1aa"
            xsize 1320
            ysize 100
            hbox:
                yalign 0.5
                yanchor 0.5
                xalign 0.5
                xanchor 0.5
                textbutton "Previous Candidate" action [SetScreenVariable("current_selection",current_selection-1),
                    SetScreenVariable("the_candidate",the_candidates[current_selection-1]),
                    Function(show_candidate,the_candidates[current_selection-1])] sensitive current_selection > 0 selected False style "textbutton_style" text_style "textbutton_text_style" xanchor 0.5 xalign 0.5 yalign 0.5 yanchor 0.5

                null width 300
                textbutton "Hire Nobody" action Return("None") style "textbutton_style" text_style "textbutton_text_style" xanchor 0.5 xalign 0.5 yalign 0.5 yanchor 0.5

                textbutton "Hire " action Return(the_candidate) style "textbutton_style" text_style "textbutton_text_style" xanchor 0.5 xalign 0.5 yalign 0.5 yanchor 0.5
                null width 300
                textbutton "Next Candidate" action [SetScreenVariable("current_selection",current_selection+1),
                    SetScreenVariable("the_candidate",the_candidates[current_selection+1]),
                    Function(show_candidate,the_candidates[current_selection+1])] sensitive current_selection < count-1 selected False style "textbutton_style" text_style "textbutton_text_style"  xanchor 0.5 xalign 0.5 yalign 0.5 yanchor 0.5


    imagebutton:
        auto "/tutorial_images/restart_tutorial_%s.png"
        xsize 54
        ysize 54
        yanchor 1.0
        xanchor 1.0
        xalign 1.0
        yalign 1.0
        action Function(mc.business.reset_tutorial,"hiring_tutorial")


    $ hiring_tutorial_length = 5 #The number of  tutorial screens we have.
    if mc.business.event_triggers_dict["hiring_tutorial"] > 0 and mc.business.event_triggers_dict["hiring_tutorial"] <= hiring_tutorial_length: #We use negative numbers to symbolize the tutorial not being enabled
        imagebutton:
            auto
            sensitive True
            xsize 1920
            ysize 1080
            idle "/tutorial_images/hiring_tutorial_"+__builtin__.str(mc.business.event_triggers_dict["hiring_tutorial"])+".png"
            hover "/tutorial_images/hiring_tutorial_"+__builtin__.str(mc.business.event_triggers_dict["hiring_tutorial"])+".png"
            action Function(mc.business.advance_tutorial,"hiring_tutorial")



init -2 python: # Some functions used only within screens for modifying variables
    def show_candidate(the_candidate):
        clear_scene()
        the_candidate.draw_person(show_person_info = False, background_fill = "444444", the_animation = no_animation)


screen show_serum_inventory(the_inventory, extra_inventories = [],inventory_names = []): #You can now pass extra inventories, as well as names for all of the inventories you are passing. Returns nothing, but is used to view inventories.
    add "Science_Menu_Background.png"
    hbox:
        $ count = 0
        xalign 0.05
        yalign 0.05
        spacing 40
        for an_inventory in [the_inventory] + extra_inventories:
            frame:
                background "#888888"
                xsize 400
                vbox:
                    xalign 0.02
                    yalign 0.02
                    if len(inventory_names) > 0 and count < len(inventory_names):
                        text inventory_names[count] style "menu_text_style" size 25
                    else:
                        text "Serums in Inventory" style "menu_text_style" size 25

                    default selected_serum = None
                    for design in an_inventory.serums_held:
                        if design == selected_serum:
                            textbutton design[0].name + ": " + str(design[1]) + " Doses":
                                style "textbutton_style" text_style "textbutton_text_style"
                                action [SetScreenVariable("selected_serum", None), Hide("serum_tooltip")]
                                sensitive True
                                #hovered Show("serum_tooltip",None,design[0])
                                background "#666666"
                        else:
                            textbutton design[0].name + ": " + str(design[1]) + " Doses":
                                style "textbutton_style" text_style "textbutton_text_style"
                                action SetScreenVariable("selected_serum", design)
                                sensitive True
                                hovered [SetScreenVariable("selected_serum", None), Show("serum_tooltip",None,design[0])]
                                unhovered Hide("serum_tooltip")
                $ count += 1

    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action Return()
        textbutton "Return" align [0.5,0.5] style "return_button_style" text_style "return_button_style"



screen serum_design_ui(starting_serum,current_traits):
    add "Science_Menu_Background.png"
    python:
        effective_traits = 0
        for trait_count in starting_serum.traits:
            if not "Production" in trait_count.exclude_tags:
                effective_traits += 1
    hbox:
        yalign 0.15
        xanchor 0.5
        xalign 0.5
        xsize 1080
        spacing 40
        frame:
            background "#888888"
            ysize 800
            vbox:
                xsize 550
                #text "Add a trait" style "menu_text_style" size 25 xanchor 0.5 xalign 0.5
                viewport:
                    xsize 550
                    ysize 480
                    scrollbars "vertical"
                    mousewheel True
                    frame:
                        xsize 550
                        background None
                        vbox:
                            xsize 530
                            text "Pick Production Type" style "menu_text_style" size 25 xanchor 0.5 xalign 0.5 xsize 530
                            for trait in sorted(sorted(list_of_traits, key = lambda trait: trait.exclude_tags, reverse = True), key=lambda trait: trait.tier, reverse = True): # Sort traits by exclude tags (So all production traits are grouped, for example), then by tier (so the highest tier production tag ends up at the top
                                if trait not in starting_serum.traits and trait.researched and "Production" in trait.exclude_tags:
                                    $ trait_tags = ""
                                    if trait.exclude_tags:
                                        $ trait_tags = " - "
                                        for a_tag in trait.exclude_tags:
                                            $ trait_tags += "[[" + a_tag + "]"
                                    $ trait_allowed = True
                                    python: # Check to see if the trait is excluded by any of the traits currently in the serum. A long looped segment only to deal with lists of tags, which are unlikely.
                                        for checking_trait in starting_serum.traits:
                                            for tag in trait.exclude_tags:
                                                for checking_tag in checking_trait.exclude_tags:
                                                    if tag == checking_tag:
                                                        trait_allowed = False
                                    $ side_effect_chance = trait.get_effective_side_effect_chance()
                                    if side_effect_chance >= 10000: #If it's a massively high side effect chance assume it's a special trait and it's just guarnateed.
                                        $ side_effect_chance_string = "Always Guaranteed"
                                    else:
                                        $ side_effect_chance_string = str(side_effect_chance) + "%"
                                    $ trait_side_effects = "\nMastery Level: " + str(trait.mastery_level) + " | Side Effect Chance: " + side_effect_chance_string
                                    textbutton trait.name + trait_tags + trait_side_effects action [Hide("trait_tooltip"),Function(starting_serum.add_trait,trait)] sensitive trait_allowed style "textbutton_style" text_style "textbutton_text_style" hovered Show("trait_tooltip",None,trait,0.315,0.57) unhovered Hide("trait_tooltip") xsize 520

                            null height 30
                            text "Add Serum Traits" style "menu_text_style" size 25 xanchor 0.5 xalign 0.5 xsize 530
                            for trait in sorted(sorted(list_of_traits, key = lambda trait: trait.exclude_tags, reverse = True), key=lambda trait: trait.tier, reverse = True): # Sort traits by exclude tags (So all production traits are grouped, for example), then by tier (so the highest tier production tag ends up at the top
                                if trait not in starting_serum.traits and trait.researched and "Production" not in trait.exclude_tags:
                                    $ trait_tags = ""
                                    if trait.exclude_tags:
                                        $ trait_tags = " - "
                                        for a_tag in trait.exclude_tags:
                                            $ trait_tags += "[[" + a_tag + "]"
                                    $ trait_allowed = True
                                    python: # Check to see if the trait is excluded by any of the traits currently in the serum. A long looped segment only to deal with lists of tags, which are unlikely.
                                        for checking_trait in starting_serum.traits:
                                            for tag in trait.exclude_tags:
                                                for checking_tag in checking_trait.exclude_tags:
                                                    if tag == checking_tag:
                                                        trait_allowed = False
                                    $ side_effect_chance = trait.get_effective_side_effect_chance()
                                    if side_effect_chance >= 10000: #If it's a massively high side effect chance assume it's a special trait and it's just guarnateed.
                                        $ side_effect_chance_string = "Always Guaranteed"
                                    else:
                                        $ side_effect_chance_string = str(side_effect_chance) + "%"
                                    $ trait_side_effects = "\nMastery Level: " + str(trait.mastery_level) + " | Side Effect Chance: " + side_effect_chance_string
                                    textbutton trait.name + trait_tags + trait_side_effects action [Hide("trait_tooltip"),Function(starting_serum.add_trait,trait)] sensitive trait_allowed style "textbutton_style" text_style "textbutton_text_style" hovered Show("trait_tooltip",None,trait,0.315,0.57) unhovered Hide("trait_tooltip") xsize 530

        frame:
            background "#888888"
            ysize 800
            vbox:
                xsize 550
                text "Remove a trait" style "menu_text_style" size 25 xanchor 0.5 xalign 0.5
                viewport:
                    xsize 550
                    ysize 480
                    scrollbars "vertical"
                    mousewheel True
                    frame:
                        xsize 550
                        background None
                        vbox:
                            for trait in starting_serum.traits:
                                $ trait_tags = ""
                                if trait.exclude_tags:
                                    $ trait_tags = " - "
                                    for a_tag in trait.exclude_tags:
                                        $ trait_tags += "[[" + a_tag + "]"
                                $ side_effect_chance = trait.get_effective_side_effect_chance()
                                if side_effect_chance >= 10000: #If it's a massively high side effect chance assume it's a special trait and it's just guarnateed.
                                    $ side_effect_chance_string = "Always Guaranteed"
                                else:
                                    $ side_effect_chance_string =  str(side_effect_chance) + "%"
                                $ trait_side_effects = "\nMastery Level: " + str(trait.mastery_level) + " | Side Effect Chance: " + side_effect_chance_string
                                textbutton trait.name + trait_tags + trait_side_effects action[Hide("trait_tooltip"), Function(starting_serum.remove_trait,trait)] style "textbutton_style" text_style "textbutton_text_style" hovered Show("trait_tooltip",None,trait,0.635,0.57) unhovered Hide("trait_tooltip") xsize 550

        frame:
            background "#888888"
            ysize 800
            vbox:
                xsize 550
                text "Current Serum Statistics:" style "menu_text_style" size 25 xanchor 0.5 xalign 0.5
                if effective_traits > starting_serum.slots:
                    text "Trait Slots: " + str(effective_traits) +"/[starting_serum.slots]" style "menu_text_style" color "#DD0000" xanchor 0.5 xalign 0.5
                else:
                    text "Trait Slots: " + str(effective_traits) +"/[starting_serum.slots]" style "menu_text_style" xanchor 0.5 xalign 0.5
                hbox:
                    xanchor 0.5
                    xalign 0.5
                    spacing 10
                    xsize 550
                    for num in __builtin__.range(__builtin__.max(starting_serum.slots,effective_traits)):
                        if num < effective_traits and num < starting_serum.slots:
                            add "Serum_Slot_Full.png" xanchor 0.5 xalign 0.5
                        elif num < effective_traits and num >= starting_serum.slots:
                            add "Serum_Slot_Incorrect.png" xanchor 0.5 xalign 0.5
                        else:
                            add "Serum_Slot_Empty.png" xanchor 0.5 xalign 0.5
                grid 2 3 xanchor 0.5 xalign 0.5:
                    spacing 10
                    text "Research Required: [starting_serum.research_needed]" style "menu_text_style"
                    text "Production Cost: [starting_serum.production_cost]" style "menu_text_style"
                    text "Value: $[starting_serum.value]" style "menu_text_style"
                    $ calculated_profit = (starting_serum.value*mc.business.batch_size)-starting_serum.production_cost
                    if calculated_profit > 0:
                        text "Expected Profit:{color=#98fb98} $[calculated_profit]{/color}" style "menu_text_style"
                    else:
                        $ calculated_profit = 0 - calculated_profit
                        text "Expected Profit:{color=#ff0000} -$[calculated_profit]{/color}" style "menu_text_style"
                    text "Duration: [starting_serum.duration] Turns" style "menu_text_style"
                    null #Placeholder to keep the grid aligned

                text "Serum Effects:" style "menu_text_style" size 25 xanchor 0.5 xalign 0.5

                viewport:
                    xsize 550
                    scrollbars "vertical"
                    mousewheel True
                    frame:
                        xsize 550
                        background None
                        vbox:
                            for trait in starting_serum.traits:
                                text trait.name style "menu_text_style"
                                text "    "  + trait.positive_slug style "menu_text_style" color "#98fb98"
                                text "    "  + trait.build_negative_slug() style "menu_text_style" color "#ff0000"

    frame:
        background "#888888"
        xsize 250
        xanchor 0.5
        xalign 0.5
        yalign 0.9
        vbox:
            xanchor 0.5
            xalign 0.5
            textbutton "Create Design":
                action Return(starting_serum) sensitive (starting_serum.slots >= effective_traits and len(starting_serum.traits) and starting_serum.has_tag("Production")) > 0
                style "textbutton_style"
                text_style "textbutton_text_style"
                xanchor 0.5
                xalign 0.5
                xsize 230

            textbutton "Reject Design" action Return("None") style "textbutton_style" text_style "textbutton_text_style" xanchor 0.5 xalign 0.5 xsize 230

    imagebutton:
        auto "/tutorial_images/restart_tutorial_%s.png"
        xsize 54
        ysize 54
        yanchor 1.0
        xalign 0.0
        yalign 1.0
        action Function(mc.business.reset_tutorial,"design_tutorial")

    $ design_tutorial_length = 5 #The number of  tutorial screens we have.
    if mc.business.event_triggers_dict["design_tutorial"] > 0 and mc.business.event_triggers_dict["design_tutorial"] <= design_tutorial_length: #We use negative numbers to symbolize the tutorial not being enabled
        imagebutton:
            auto
            sensitive True
            xsize 1920
            ysize 1080
            idle "/tutorial_images/design_tutorial_"+__builtin__.str(mc.business.event_triggers_dict["design_tutorial"])+".png"
            hover "/tutorial_images/design_tutorial_"+__builtin__.str(mc.business.event_triggers_dict["design_tutorial"])+".png"
            action Function(mc.business.advance_tutorial,"design_tutorial")


screen review_designs_screen():
    add "Science_Menu_Background.png"
    default selected_serum = None
    vbox:
        text "Serum Designs:" style "menu_text_style" size 30
        grid 2 len(mc.business.serum_designs):
            for serum_design in mc.business.serum_designs:
                $ serum_name = serum_design.name
                if serum_design.researched:
                    $ serum_name += " - Research Finished"
                else:
                    $ serum_name += " - " + str(serum_design.current_research) + "/" + str(serum_design.research_needed) + " Research Required"

                if serum_design == selected_serum:
                    textbutton serum_name:
                        action [SetScreenVariable("selected_serum", None), Hide("serum_tooltip")] style "textbutton_style" text_style "textbutton_text_style" background "#888888"

                else:
                    textbutton serum_name:
                        action SetScreenVariable("selected_serum",serum_design) hovered [SetScreenVariable("selected_serum", None), Show("serum_tooltip",None,serum_design)] unhovered Hide("serum_tooltip") style "textbutton_style" text_style "textbutton_text_style"

                textbutton "Scrap Design" action Function(mc.business.remove_serum_design,serum_design) style "textbutton_style" text_style "textbutton_text_style"

    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action Return()
        textbutton "Return" align [0.5,0.5] style "return_button_style" text_style "return_button_style"


screen serum_tooltip(the_serum, set_x_align = 0.9, set_y_align = 0.1):
    zorder 105 #Serum tooltips are a high order so they may be properly layered onto others when needed to show extra info.
    frame:
        background "#888888"

        xalign set_x_align
        yalign set_y_align
        yanchor 0.0
        viewport:
            xsize 540
            ymaximum 800
            scrollbars "vertical"
            mousewheel True
            vbox:
                text "[the_serum.name]" style "menu_text_style" xanchor 0.5 xalign 0.5 size 26
                grid 2 3 xanchor 0.5 xalign 0.5:
                    spacing 10
                    text "Research Required: [the_serum.research_needed]" style "menu_text_style"
                    text "Production Cost: [the_serum.production_cost]" style "menu_text_style"
                    text "Value: $[the_serum.value]" style "menu_text_style"
                    $ calculated_profit = (the_serum.value*mc.business.batch_size)-the_serum.production_cost
                    if calculated_profit > 0:
                        text "Expected Profit:{color=#98fb98} $[calculated_profit]{/color}" style "menu_text_style"
                    else:
                        $ calculated_profit = 0 - calculated_profit
                        text "Expected Profit:{color=#ff0000} -$[calculated_profit]{/color}" style "menu_text_style"

                    text "Duration: [the_serum.duration] Turns" style "menu_text_style"
                    null

                for trait in the_serum.traits:
                    text trait.name style "menu_text_style"
                    text "    "  + trait.positive_slug style "menu_text_style" color "#98fb98"
                    text "    "  + trait.negative_slug style "menu_text_style" color "#ff0000"
                if the_serum.side_effects:
                    for side_effect in the_serum.side_effects:
                        text side_effect.name style "menu_text_style"
                        text "    "  + side_effect.negative_slug style "menu_text_style" color "#ff0000"


screen trait_tooltip(the_trait,given_xalign=0.9,given_yalign=0.1):
    frame:
        background "#888888"

        xalign given_xalign
        yalign given_yalign
        xanchor 1.0
        yanchor 0.0
        vbox:
            xsize 500
            text the_trait.name style "menu_text_style" xalign 0.5 xanchor 0.5
            text the_trait.positive_slug style "menu_text_style" size 14 color "#98fb98" xalign 0.5 xanchor 0.5
            text the_trait.build_negative_slug() style "menu_text_style" size 14 color "#ff0000" xalign 0.5 xanchor 0.5
            text the_trait.desc style "menu_text_style" xalign 0.5 xanchor 0.5

screen trait_list_tooltip(the_traits, y_height = 0.1):
    hbox:
        spacing 50
        xalign 0.5
        yalign y_height
        xanchor 0.0
        for trait in the_traits:
            frame: #TODO: Functionally identical to trait Figure out how to put this into a separate screen or displayable.
                background "#888888"
                xalign 0.0
                yalign 0.0
                xanchor 1.0
                yanchor 0.0
                vbox:
                    xsize 500
                    text trait.name style "menu_text_style" xalign 0.5 xanchor 0.5
                    text trait.positive_slug style "menu_text_style" size 14 color "#98fb98" xalign 0.5 xanchor 0.5
                    text trait.build_negative_slug() style "menu_text_style" size 14 color "#ff0000" xalign 0.5 xanchor 0.5
                    text trait.desc style "menu_text_style" xalign 0.5 xanchor 0.5


screen serum_trade_ui(inventory_1,inventory_2,name_1="Player",name_2="Business"): #Lets you trade serums back and forth between two different inventories. Inventory 1 is assumed to be the players.
    modal True
    add "Science_Menu_Background.png"
    frame:
        background "#888888"
        xalign 0.5
        xanchor 0.5
        yalign 0.1
        ysize 800
        vbox:
            yalign 0.0
            spacing 20
            text "Trade Serums Between Inventories." style "menu_text_style" size 25 xalign 0.5 xanchor 0.5
            for serum in set(inventory_1.get_serum_type_list()) | set(inventory_2.get_serum_type_list()): #Gets a unique entry for each serum design that shows up in either list. Doesn't duplicate if it's in both.
                # has a few things. 1) name of serum design. 2) count of first inventory, 3) arrows for transfering, 4) count of second inventory.
                frame:
                    background "#777777"
                    xalign 0.5
                    xanchor 0.5
                    yalign 0.0
                    yanchor 0.0
                    vbox:
                        xalign 0.5
                        xanchor 0.5
                        xsize 600

                        hbox:
                            textbutton serum.name + ": " style "textbutton_style" text_style "menu_text_style" action NullAction() hovered Show("serum_tooltip",None,serum) unhovered Hide("serum_tooltip") #displays the name of this particular serum
                            null width 10
                            text name_1 + "\nhas: " + str(inventory_1.get_serum_count(serum)) style "menu_text_style"#The players current inventory count. 0 if there is nothing in their inventory
                            textbutton "|<" action [Function(inventory_1.change_serum,serum,inventory_2.get_serum_count(serum)),Function(inventory_2.change_serum,serum,-inventory_2.get_serum_count(serum))] sensitive (inventory_2.get_serum_count(serum) > 0) style "textbutton_style" text_style "textbutton_text_style"
                            textbutton "<<" action [Function(inventory_1.change_serum,serum,5),Function(inventory_2.change_serum,serum,-5)] sensitive (inventory_2.get_serum_count(serum) > 4) style "textbutton_style" text_style "textbutton_text_style"
                            textbutton "<" action [Function(inventory_1.change_serum,serum,1),Function(inventory_2.change_serum,serum,-1)] sensitive (inventory_2.get_serum_count(serum) > 0) style "textbutton_style" text_style "textbutton_text_style"
                            #When pressed, moves 1 serum from the business inventory to the player. Not active if the business has nothing in it.
                            null width 10
                            textbutton ">" action [Function(inventory_2.change_serum,serum,1),Function(inventory_1.change_serum,serum,-1)] sensitive (inventory_1.get_serum_count(serum) > 0) style "textbutton_style" text_style "textbutton_text_style"
                            textbutton ">>" action [Function(inventory_2.change_serum,serum,5),Function(inventory_1.change_serum,serum,-5)] sensitive (inventory_1.get_serum_count(serum) > 4) style "textbutton_style" text_style "textbutton_text_style"
                            textbutton ">|" action [Function(inventory_2.change_serum,serum,inventory_1.get_serum_count(serum)),Function(inventory_1.change_serum,serum,-inventory_1.get_serum_count(serum))] sensitive (inventory_1.get_serum_count(serum) > 0) style "textbutton_style" text_style "textbutton_text_style"
                            text name_2 + "\nhas: " + str(inventory_2.get_serum_count(serum)) style "menu_text_style"


    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action Return()
        textbutton "Return" align [0.5,0.5] text_style "return_button_style"


screen serum_select_ui: #How you select serum and trait research
    add "Science_Menu_Background.png"
    vbox:
        xalign 0.1
        yalign 0.4
        frame:
            background "#888888"
            xsize 1000
            if not mc.business.active_research_design == None:
                text "Current Research: [mc.business.active_research_design.name] " + str(int(mc.business.active_research_design.current_research)) + "/[mc.business.active_research_design.research_needed])" style "menu_text_style" size 25 xanchor 0.5 xalign 0.5
            else:
                text "Current Research: None!" style "menu_text_style" size 25 xanchor 0.5 xalign 0.5

        null height 20

        frame:
            background "#888888"
            xsize 1000
            ysize 900
            hbox:
                viewport:
                    xsize 320
                    ysize 800
                    scrollbars "vertical"
                    mousewheel True
                    vbox:
                        xsize 320
                        spacing 0
                        text "Research New Traits" style "menu_text_style" size 20 xanchor 0.5 xalign 0.5
                        for trait in sorted(sorted(list_of_traits, key = lambda trait: trait.exclude_tags, reverse = True), key=lambda trait: trait.tier, reverse = True):
                            if not trait.researched and trait.has_required():
                                $ trait_tags = ""
                                if trait.exclude_tags:
                                    $ trait_tags = "\nExcludes Other: "
                                    for a_tag in trait.exclude_tags:
                                        $ trait_tags += "[[" + a_tag + "]"

                                if trait.research_needed > 10000: #Assume very high values are impossible #TODO: Just make this a boolean we can toggle on each trait.
                                    $ research_needed_string = "Research Impossible"
                                else:
                                    $ research_needed_string = "(" +str(trait.current_research)+"/"+ str(trait.research_needed) + ")"
                                $ trait_title = trait.name + " " + research_needed_string  + trait_tags
                                textbutton trait_title:
                                    text_xalign 0.5
                                    text_text_align 0.5
                                    text_size 14
                                    action [Hide("trait_tooltip"),Return(trait)] style "textbutton_style"
                                    text_style "textbutton_text_style"
                                    hovered Show("trait_tooltip",None,trait)
                                    unhovered Hide("trait_tooltip")
                                    xsize 300

                viewport:
                    xsize 320
                    ysize 800
                    scrollbars "vertical"
                    mousewheel True
                    vbox:
                        xsize 320
                        text "Master Existing Traits:" style "menu_text_style" size 20 xanchor 0.5 xalign 0.5

                        for trait in sorted(sorted(list_of_traits, key = lambda trait: trait.exclude_tags, reverse = True), key=lambda trait: trait.tier, reverse = True):
                            if trait.researched:
                                $ trait_tags = ""
                                if trait.exclude_tags:
                                    $ trait_tags = "\nExcludes Other: "
                                    for a_tag in trait.exclude_tags:
                                        $ trait_tags += "[[" + a_tag + "]"

                                if trait.research_needed > 10000: #Assume very high values are impossible #TODO: Just make this a boolean we can toggle on each trait.
                                    $ research_needed_string = "Research Impossible"
                                else:
                                    $ research_needed_string = "(" +str(trait.current_research)+"/"+ str(trait.research_needed) + ")"

                                $ side_effect_chance = trait.get_effective_side_effect_chance()
                                if side_effect_chance >= 10000: #If it's a massively high side effect chance assume it's a special trait and it's just guarnateed.
                                    $ side_effect_chance_string = "Always Guaranteed"
                                else:
                                    $ side_effect_chance_string = str(side_effect_chance) + "%"
                                $ trait_title = trait.name + " " + research_needed_string + trait_tags + "\nMastery Level: " + str(trait.mastery_level) + "\nSide Effect Chance: " + side_effect_chance_string
                                textbutton trait_title:
                                    text_xalign 0.5
                                    text_text_align 0.5
                                    text_size 14
                                    action [Hide("trait_tooltip"),Return(trait)] style "textbutton_style"
                                    text_style "textbutton_text_style"
                                    hovered Show("trait_tooltip",None,trait)
                                    unhovered Hide("trait_tooltip")
                                    xsize 300


                viewport:
                    xsize 320
                    ysize 800
                    scrollbars "vertical"
                    mousewheel True
                    vbox:
                        xsize 320
                        text "Research New Designs:" style "menu_text_style" size 20 xanchor 0.5 xalign 0.5
                        for serum in mc.business.serum_designs:
                            if not serum.researched:
                                textbutton "[serum.name] ([serum.current_research]/[serum.research_needed])":
                                    text_xalign 0.5
                                    text_text_align 0.5
                                    text_size 14
                                    action [Hide("serum_tooltip"),Return(serum)] style "textbutton_style"
                                    text_style "textbutton_text_style"
                                    hovered Show("serum_tooltip",None,serum)
                                    unhovered Hide("serum_tooltip")
                                    xsize 300

            textbutton "Do not change research." action Return("None") style "textbutton_style" text_style "textbutton_text_style" yalign 0.995 xanchor 0.5 xalign 0.5

    imagebutton:
        auto "/tutorial_images/restart_tutorial_%s.png"
        xsize 54
        ysize 54
        yanchor 1.0
        xalign 0.0
        yalign 1.0
        action Function(mc.business.reset_tutorial,"research_tutorial")

    $ research_tutorial_length = 5 #The number of  tutorial screens we have.
    if mc.business.event_triggers_dict["research_tutorial"] > 0 and mc.business.event_triggers_dict["research_tutorial"] <= research_tutorial_length: #We use negative numbers to symbolize the tutorial not being enabled
        imagebutton:
            auto
            sensitive True
            xsize 1920
            ysize 1080
            idle "/tutorial_images/research_tutorial_"+__builtin__.str(mc.business.event_triggers_dict["research_tutorial"])+".png"
            hover "/tutorial_images/research_tutorial_"+__builtin__.str(mc.business.event_triggers_dict["research_tutorial"])+".png"
            action Function(mc.business.advance_tutorial,"research_tutorial")

screen serum_production_select_ui:
    add "Science_Menu_Background.png"
    default line_selected = None
    default production_remaining = 100
    python:
        production_remaining = 100
        for key in mc.business.serum_production_array:
            production_remaining -= mc.business.serum_production_array[key][1] # How much of the 100% capability are we using?

    vbox:
        xalign 0.04
        yalign 0.04
        xsize 600
        yanchor 0.0
        frame:
            background "#999999"
            xsize 510
            text "Production Lines" style "menu_text_style" size 30 xalign 0.5
        frame:
            background "#999999"
            xsize 510
            text "Capacity Remaining: [production_remaining]%" style "menu_text_style"
        spacing 20
        for count in range(1,mc.business.production_lines+1): #For the non-programmers we index our lines to 1 through production_lines.
            frame:
                background "#999999"
                vbox:
                    $ name_string = ""
                    if count in mc.business.serum_production_array:
                        $ name_string = "Production Line " + str(count) + "\nCurrently Producing: " + mc.business.serum_production_array[count][0].name
                    else:
                        $ name_string = "Production Line " + str(count) + "\nCurrently Producing: Nothing"

                    $ button_background = "#000080"
                    if line_selected == count:
                        $ button_background = "#666666"

                    if count in mc.business.serum_production_array:
                        $ the_serum = mc.business.serum_production_array[count][0]
                        textbutton name_string action [SetScreenVariable("line_selected",count),Hide("serum_tooltip")] style "textbutton_style" text_style "textbutton_text_style" hovered Show("serum_tooltip",None,the_serum,0.94,0.072) unhovered Hide("serum_tooltip") background button_background xsize 500
                    else:
                        textbutton name_string action SetScreenVariable("line_selected",count) style "textbutton_style" text_style "textbutton_text_style" background button_background xsize 500

                    null height 20
                    hbox:
                        ysize 40
                        xsize 500
                        text "Production Weight: " style "menu_text_style" xalign 0.0
                        if count in mc.business.serum_production_array:
                            textbutton "-10%" action Function(mc.business.change_line_weight,count,-10) style "textbutton_style" text_style "textbutton_text_style" yanchor 0.25 tooltip "Work done by production employees will be split between active lines based on production weight."
                            text str(mc.business.serum_production_array[count][1]) + "%" style "menu_text_style"
                            textbutton "+10%" action Function(mc.business.change_line_weight,count,10) style "textbutton_style" text_style "textbutton_text_style" yanchor 0.25 tooltip "Work done by production employees will be split between active lines based on production weight."
                        else:
                            textbutton "-10%" action NullAction style "textbutton_style" text_style "textbutton_text_style" sensitive False yanchor 0.25 tooltip "Work done by production employees will be split between active lines based on production weight."
                            text "0%" style "menu_text_style"
                            textbutton "+10%" action NullAction style "textbutton_style" text_style "textbutton_text_style" sensitive False yanchor 0.25 tooltip "Work done by production employees will be split between active lines based on production weight."

                    hbox:
                        ysize 40
                        xsize 500
                        text "Auto-sell Threshold: " style "menu_text_style"
                        if count in mc.business.serum_production_array:
                            textbutton "-1" action Function(mc.business.change_line_autosell,count,-1) style "textbutton_style" text_style "textbutton_text_style" yanchor 0.25 tooltip "Doses of serum above the auto-sell threshold will automatically be flagged for sale and moved to the marketing department."
                            if mc.business.serum_production_array[count][3] < 0:
                                text "None" style "menu_text_style"
                            else:
                                text str(mc.business.serum_production_array[count][3]) style "menu_text_style"
                            textbutton "+1" action Function(mc.business.change_line_autosell,count,1) style "textbutton_style" text_style "textbutton_text_style"  yanchor 0.25 tooltip "Doses of serum above the auto-sell threshold will automatically be flagged for sale and moved to the marketing department."
                        else:
                            textbutton "-1" action NullAction style "textbutton_style" text_style "textbutton_text_style" sensitive False yanchor 0.25 tooltip "Doses of serum above the auto-sell threshold will automatically be flagged for sale and moved to the marketing department."
                            text "None" style "menu_text_style"
                            textbutton "+1" action NullAction style "textbutton_style" text_style "textbutton_text_style" sensitive False yanchor 0.25 tooltip "Doses of serum above the auto-sell threshold will automatically be flagged for sale and moved to the marketing department."

    if line_selected:
        frame:
            yanchor 0.0
            background "#999999"
            xalign 0.5
            yalign 0.04
            xsize 600
            vbox:
                text "Choose Production for Line [line_selected]" style "menu_text_style" size 30
                if len(mc.business.serum_designs) == 0:
                    frame:
                        xfill True
                        background "#000080"
                        text "No designs researched! Create and research a design in the R&D department first!" style "textbutton_text_style"
                else:
                    for a_serum in mc.business.serum_designs:
                        if a_serum.researched:
                            textbutton a_serum.name action [Hide("serum_tooltip"), Function(mc.business.change_production,a_serum,line_selected), SetScreenVariable("line_selected",None)] hovered Show("serum_tooltip",None,a_serum,0.94,0.072) unhovered Hide("serum_tooltip") style "textbutton_style" text_style "textbutton_text_style"

    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action Return()
        textbutton "Return" align [0.5,0.5] text_style "return_button_style"

    imagebutton:
        auto "/tutorial_images/restart_tutorial_%s.png"
        xsize 54
        ysize 54
        yanchor 1.0
        xalign 0.0
        yalign 1.0
        action Function(mc.business.reset_tutorial,"production_tutorial")


    $ production_tutorial_length = 5 #The number of  tutorial screens we have.
    if mc.business.event_triggers_dict["production_tutorial"] > 0 and mc.business.event_triggers_dict["production_tutorial"] <= production_tutorial_length: #We use negative numbers to symbolize the tutorial not being enabled
        imagebutton:
            auto
            sensitive True
            xsize 1920
            ysize 1080
            idle "/tutorial_images/production_tutorial_"+__builtin__.str(mc.business.event_triggers_dict["production_tutorial"])+".png"
            hover "/tutorial_images/production_tutorial_"+__builtin__.str(mc.business.event_triggers_dict["production_tutorial"])+".png"
            action Function(mc.business.advance_tutorial,"production_tutorial")

screen serum_inventory_select_ui(the_inventory): #Used to let the player select a serum from an inventory.
    add "Science_Menu_Background.png"
    modal True
    frame:
        background "#888888"
        xsize 400
        ysize 1000
        xalign 0.05
        yalign 0.05
        anchor (0.0,0.0)
        vbox:
            spacing 10
            default selected_serum = None
            text "Serum Available" size 22 style "menu_text_style"
            for serum in the_inventory.serums_held:
                button:
                    background "#1a45a1aa"
                    xsize 380
                    ysize 80
                    action [Hide("serum_tooltip"),Return(serum[0])]
                    hovered Show("serum_tooltip",None,serum[0])
                    #unhovered Hide("serum_tooltip")
                    text serum[0].name + " - " + str(serum[1]) + " Doses" style "menu_text_style" size 18 xalign 0.5 xanchor 0.5 yalign 0.5 yanchor 0.5

    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action [Hide("serum_tooltip"), Return("None")]
        textbutton "Return" align [0.5,0.5] text_style "return_button_style"

#LIKELY NOT NEEDED
init -2 python:
    def colour_changed_r(new_value):
        if not new_value:
            new_value = 0

        try:
            new_value = float(new_value)
        except ValueError:
            new_value = 0

        if float(new_value) < 0:
            new_value = 0
        elif float(new_value) > 1:
            new_value = 1.0
        cs = renpy.current_screen()

        cs.scope["current_r"] = __builtin__.round(float(new_value),2)
        renpy.restart_interaction()

    def colour_changed_g(new_value):
        if not new_value:
            new_value = 0

        try:
            new_value = float(new_value)
        except ValueError:
            new_value = 0

        if float(new_value) < 0:
            new_value = 0
        elif float(new_value) > 1:
            new_value = 1.0
        cs = renpy.current_screen()

        cs.scope["current_g"] = __builtin__.round(float(new_value),2)
        renpy.restart_interaction()

    def colour_changed_b(new_value):
        if not new_value:
            new_value = 0

        try:
            new_value = float(new_value)
        except ValueError:
            new_value = 0

        if float(new_value) < 0:
            new_value = 0
        elif float(new_value) > 1:
            new_value = 1.0

        cs = renpy.current_screen()

        cs.scope["current_b"] = __builtin__.round(float(new_value),2)
        renpy.restart_interaction()

    def update_colour_palette(palette_index, new_r,new_g,new_b,new_a):
        persistent.colour_palette[palette_index] = [new_r,new_g,new_b,new_a]
        renpy.save_persistent()


screen outfit_creator(starting_outfit, outfit_type = "full", slut_limit = None): ##Pass a completely blank outfit instance for a new outfit, or an already existing instance to load an old one.\
    add "Paper_Background.png"
    modal True
    zorder 100
    default catagory_selected = "Panties"

    default demo_outfit = starting_outfit.get_copy()

    if outfit_type == "under":
        $ valid_layers = [0,1]
    elif outfit_type == "over":
        $ valid_layers = [2,3]
    else:
        $ valid_layers = [0,1,2,3]

    $ valid_catagories = ["Panties", "Bras", "Pants", "Skirts", "Dresses", "Shirts", "Socks", "Shoes", "Facial", "Rings", "Bracelets", "Neckwear"] #Holds the valid list of catagories strings to be shown at the top.

    $ catagories_mapping = {
        "Panties": [panties_list, Outfit.can_add_lower, Outfit.add_lower],  #Maps each catagory to the function it should use to determine if it is valid and how it should be added to the outfit.
        "Bras": [bra_list, Outfit.can_add_upper, Outfit.add_upper],
        "Pants": [pants_list, Outfit.can_add_lower, Outfit.add_lower],
        "Skirts": [skirts_list, Outfit.can_add_lower, Outfit.add_lower],
        "Dresses": [dress_list, Outfit.can_add_dress, Outfit.add_dress],
        "Shirts": [shirts_list, Outfit.can_add_upper, Outfit.add_upper],
        "Socks": [socks_list, Outfit.can_add_feet, Outfit.add_feet],
        "Shoes": [shoes_list, Outfit.can_add_feet, Outfit.add_feet],
        "Facial": [earings_list, Outfit.can_add_accessory, Outfit.add_accessory],
        "Rings": [rings_list, Outfit.can_add_accessory, Outfit.add_accessory],
        "Bracelets": [bracelet_list, Outfit.can_add_accessory, Outfit.add_accessory],
        "Neckwear": [neckwear_list, Outfit.can_add_accessory, Outfit.add_accessory]}

    default bar_select = 0 # 0 is nothing selected, 1 is red, 2 is green, 3 is blue, and 4 is alpha

    default selected_colour = "colour" #If secondary we are alterning the patern colour. When changed it updates the colour of the clothing item. Current values are "colour" and "colour_pattern"
    default current_r = 1.0
    default current_g = 1.0
    default current_b = 1.0
    default current_a = 1.0

    default hide_underwear = False
    default hide_base = False
    default hide_overwear = False

    default selected_clothing = None
    # $ current_colour = [1.0,1.0,1.0,1.0] #This is the colour we will apply to all of the clothing

    #Each catagory below has a click to enable button. If it's false, we don't show anything for it.
    #TODO: refactor this outfit creator to remove as much duplication as possible.

    hbox: #The main divider between the new item adder and the current outfit view.
        xpos 15
        yalign 0.5
        yanchor 0.5
        spacing 15
        frame:
            background "#aaaaaa"
            padding (20,20)
            xysize (880, 1015)
            hbox:
                spacing 15
                vbox: #Catagories select on far left
                    spacing 15
                    for catagory in valid_catagories:
                        textbutton catagory:
                            style "textbutton_style"
                            text_style "textbutton_text_style"
                            if catagory == catagory_selected:
                                background "#4f7ad6"
                                hover_background "#4f7ad6"
                            else:
                                background "#1a45a1"
                                hover_background "#3a65c1"
                            text_align(0.5,0.5)
                            text_anchor(0.5,0.5)
                            xysize (220, 60)
                            action [SetScreenVariable("catagory_selected",catagory), SetScreenVariable("selected_clothing", None), SetScreenVariable("selected_colour", "colour")] #Set the clothing to None when you change catagories to avoid breaking the clothing add function assignments
                vbox:
                    spacing 15
                    viewport:
                        ysize 480
                        xminimum 605
                        scrollbars "vertical"
                        mousewheel True
                        frame:
                            xsize 620
                            yminimum 480
                            background "#888888"
                            vbox:
                                #THIS IS WHERE ITEM CHOICES ARE SHOWN
                                if catagory_selected in catagories_mapping:
                                    $ valid_check = catagories_mapping[catagory_selected][1]
                                    $ apply_method = catagories_mapping[catagory_selected][2]
                                    $ cloth_list_length = len(catagories_mapping[catagory_selected][0])
                                    $ sorted_list = sorted(catagories_mapping[catagory_selected][0], key = lambda x: x.layer)
                                    $ sorted_list.sort(key = lambda x: x.slut_value)
                                    for cloth in sorted_list:
                                        $ is_sensitive = valid_check(starting_outfit, cloth) and cloth.layer in valid_layers
                                        if cloth.has_extension and cloth.has_extension.layer not in valid_layers:
                                            $ is_sensitive = False
                                        $ cloth_name = cloth.name.title()
                                        $ cloth_info = cloth.generate_stat_slug()

                                        frame:
                                            xsize 580
                                            ysize 50
                                            background "#00000000"
                                            textbutton cloth.name.title():
                                                xalign 0.0
                                                ysize 50
                                                style "textbutton_style"
                                                text_style "textbutton_text_style"
                                                if valid_check(starting_outfit, cloth):
                                                    background "#1a45a1"
                                                    hover_background "#3a65c1"
                                                else:
                                                    background "#444444"
                                                    hover_background "#444444"
                                                insensitive_background "#444444"
                                                xfill True
                                                sensitive is_sensitive
                                                action [SetScreenVariable("selected_clothing", cloth), SetScreenVariable("selected_colour", "colour")]
                                                hovered Function(apply_method, demo_outfit, cloth)
                                                unhovered Function(demo_outfit.remove_clothing, cloth)
                                            text cloth_info:
                                                style "textbutton_text_style"
                                                xalign 0.95
                                                yalign 1.0
                                                text_align 1.0

                    frame:
                        #THIS IS WHERE SELECTED ITEM OPTIONS ARE SHOWN
                        xysize (605, 480)
                        background "#888888"
                        vbox:
                            spacing 10
                            if selected_clothing is not None:
                                text selected_clothing.name + ", " + selected_clothing.generate_stat_slug() style "textbutton_text_style"
                                if __builtin__.type(selected_clothing) is Clothing: #Only clothing items have patterns, facial accessories do not (currently).
                                    hbox:
                                        spacing 5
                                        for pattern in selected_clothing.supported_patterns:
                                            textbutton pattern:
                                                style "textbutton_style"
                                                text_style "textbutton_text_style"
                                                if selected_clothing.pattern == selected_clothing.supported_patterns[pattern]:
                                                    background "#4f7ad6"
                                                    hover_background "#4f7ad6"
                                                else:
                                                    background "#1a45a1"
                                                    hover_background "#3a65c1"
                                                xfill False
                                                xsize 120
                                                text_xalign 0.5
                                                text_xanchor 0.5
                                                text_size 12
                                                sensitive True
                                                action SetField(selected_clothing,"pattern",selected_clothing.supported_patterns[pattern])

                                hbox:
                                    spacing -5 #We will manually handle spacing so we can have our colour predictor frames
                                    textbutton "Primary Colour":
                                        style "textbutton_style"
                                        text_style "textbutton_text_style"
                                        text_size 12
                                        xsize 120
                                        if selected_colour == "colour":
                                            background "#4f7ad6"
                                            hover_background "#4f7ad6"
                                        else:
                                            background "#1a45a1"
                                            hover_background "#3a65c1"
                                        sensitive True
                                        if selected_colour == "colour_pattern":
                                            action [SetField(selected_clothing,"colour_pattern",[current_r,current_g,current_b,current_a]), SetScreenVariable("selected_colour","colour"), SetScreenVariable("current_r",selected_clothing.colour[0]), SetScreenVariable("current_g",selected_clothing.colour[1]), SetScreenVariable("current_b",selected_clothing.colour[2]), SetScreenVariable("current_a",selected_clothing.colour[3])]
                                        else:
                                            action NullAction()

                                    frame:
                                        if selected_colour == "colour":
                                            background Color(rgb=(current_r,current_g,current_b,current_a))
                                        else:
                                            background Color(rgb=(selected_clothing.colour[0], selected_clothing.colour[1], selected_clothing.colour[2]))
                                        xysize (45,45)
                                        yanchor 0.5
                                        yalign 0.5

                                    if __builtin__.type(selected_clothing) is Clothing and selected_clothing.pattern is not None:
                                        null width 15
                                        textbutton "Pattern Colour":
                                            style "textbutton_style"
                                            text_style "textbutton_text_style"
                                            text_size 12
                                            xsize 120
                                            if selected_colour == "colour_pattern":
                                                background "#4f7ad6"
                                                hover_background "#4f7ad6"
                                            else:
                                                background "#1a45a1"
                                                hover_background "#3a65c1"
                                            sensitive True
                                            if selected_colour == "colour":
                                                action [SetField(selected_clothing,"colour",[current_r,current_g,current_b,current_a]), SetScreenVariable("selected_colour","colour_pattern"), SetScreenVariable("current_r",selected_clothing.colour_pattern[0]), SetScreenVariable("current_g",selected_clothing.colour_pattern[1]), SetScreenVariable("current_b",selected_clothing.colour_pattern[2]), SetScreenVariable("current_a",selected_clothing.colour_pattern[3])]
                                            else:
                                                action NullAction()
                                        frame:
                                            if selected_colour == "colour_pattern":
                                                background Color(rgb=(current_r,current_g,current_b,current_a))
                                            else:
                                                background Color(rgb=(selected_clothing.colour_pattern[0], selected_clothing.colour_pattern[1], selected_clothing.colour_pattern[2]))
                                            xysize (45,45)
                                            yanchor 0.5
                                            yalign 0.5

                                hbox:
                                    spacing 10
                                    vbox:
                                        text "Red" style "textbutton_text_style"
                                        hbox:
                                            if bar_select == 1:
                                                frame:
                                                    input default current_r length 4 changed colour_changed_r allow ".0123456789" style "menu_text_style"
                                                    xsize 70
                                                    ysize 50
                                            else:
                                                button:
                                                    background "#888888"
                                                    action SetScreenVariable("bar_select",1)
                                                    text "%.2f" % current_r style "menu_text_style"
                                                    xsize 70
                                                    ysize 50

                                            bar value ScreenVariableValue("current_r", 1.0) xsize 120 ysize 45 style style.slider unhovered SetScreenVariable("current_r",__builtin__.round(current_r,2))
                                    vbox:
                                        text "Green" style "textbutton_text_style"
                                        hbox:
                                            if bar_select == 2:
                                                frame:
                                                    input default current_g length 4 changed colour_changed_g allow ".0123456789" style "menu_text_style"
                                                    xsize 70
                                                    ysize 50
                                            else:
                                                button:
                                                    background "#888888"
                                                    action SetScreenVariable("bar_select",2)
                                                    text "%.2f" % current_g style "menu_text_style"
                                                    xsize 70
                                                    ysize 50

                                            bar value ScreenVariableValue("current_g", 1.0) xsize 120 ysize 45 style style.slider unhovered SetScreenVariable("current_g",__builtin__.round(current_g,2))
                                    vbox:
                                        text "Blue" style "textbutton_text_style"
                                        hbox:
                                            if bar_select == 3:
                                                frame:
                                                    input default current_b length 4 changed colour_changed_b allow ".0123456789" style "menu_text_style"
                                                    xsize 70
                                                    ysize 50
                                            else:
                                                button:
                                                    background "#888888"
                                                    action SetScreenVariable("bar_select",3)
                                                    text "%.2f" % current_b style "menu_text_style"
                                                    xsize 70
                                                    ysize 50

                                            bar value ScreenVariableValue("current_b", 1.0) xsize 120 ysize 45 style style.slider unhovered SetScreenVariable("current_b",__builtin__.round(current_b,2))

                                text "Transparency: " style "menu_text_style"
                                hbox:
                                    spacing 5
                                    for trans in ['1.0', '0.95', '0.9', '0.8', '0.75', '0.66', '0.5', '0.33', '0.25']:
                                        $ trans_name = str(int(float(trans)*100)) + "%"
                                        button:
                                            if current_a == float(trans):
                                                background "#4f7ad6"
                                            else:
                                                background "#1a45a1"
                                            text trans_name style "menu_text_style" xalign 0.5 xanchor 0.5 yalign 0.5 yanchor 0.5
                                            xysize (60, 40)
                                            action SetScreenVariable("current_a", float(trans))

                                hbox:
                                    spacing 5
                                    xalign 0.5
                                    xanchor 0.5
                                    for count, a_colour in __builtin__.enumerate(persistent.colour_palette):
                                        frame:
                                            background "#aaaaaa"
                                            button:
                                                background Color(rgb=(a_colour[0], a_colour[1], a_colour[2]))
                                                xysize (40,40)
                                                sensitive True
                                                action [SetScreenVariable("current_r", a_colour[0]), SetScreenVariable("current_g", a_colour[1]), SetScreenVariable("current_b", a_colour[2]), SetScreenVariable("current_a", a_colour[3])]
                                                alternate Function(update_colour_palette, count, current_r, current_g, current_b, current_a)



                        #TODO: Change this "Add" butotn to "Remove" when you're selecting something that is arleady part of the outfit.
                        if selected_clothing:
                            textbutton "Add to Outfit":
                                style "textbutton_style"
                                text_style "textbutton_text_style"
                                background "#1a45a1"
                                hover_background "#3a65c1"
                                xalign 0.5
                                yalign 1.0
                                xanchor 0.5
                                yanchor 1.0
                                sensitive valid_check(starting_outfit, selected_clothing)
                                action [SetField(selected_clothing, selected_colour,[current_r,current_g,current_b,current_a]), Function(apply_method, starting_outfit, selected_clothing)]
                                hovered [SetField(selected_clothing, selected_colour,[current_r,current_g,current_b,current_a]), Function(apply_method, demo_outfit, selected_clothing)]
                                unhovered Function(demo_outfit.remove_clothing, selected_clothing)




            # vbox: #Items selector
            #     #W/ item customixing window at bottom
            #
        vbox:
            spacing 15
            frame:
                xysize (440, 500)
                background "#aaaaaa"
                padding (20,20)
                vbox:
                    spacing 15
                    text "Current Items" style "textbutton_text_style"
                    frame:
                        xfill True
                        yfill True
                        background "#888888"
                        viewport:
                            ysize 500
                            xminimum 440
                            scrollbars "vertical"
                            mousewheel True
                            vbox:
                                spacing 5
                                for cloth in starting_outfit.upper_body + starting_outfit.lower_body + starting_outfit.feet + starting_outfit.accessories:
                                    if not cloth.is_extension: #Don't list extensions for removal.
                                        button:
                                            background Color(rgb = (cloth.colour[0], cloth.colour[1], cloth.colour[2]))
                                            xysize (380, 40)
                                            action [Function(starting_outfit.remove_clothing, cloth),Function(demo_outfit.remove_clothing, cloth)]
                                            xalign 0.5
                                            yalign 0.0
                                            text cloth.name xalign 0.5 xanchor 0.5 yalign 0.5 yanchor 0.5 style "outfit_style"

            frame:
                background "#aaaaaa"
                xysize (440, 500)
                padding (20,20)
                vbox:
                    yalign 0.0
                    text "Outfit Stats" style "menu_text_style" size 20

                    if outfit_type == "full":
                        text "Sluttiness (Full Outfit) : " + str(demo_outfit.slut_requirement) + "{image=gui/heart/red_heart.png}"style "menu_text_style"

                    if outfit_type == "under":
                        if demo_outfit.is_suitable_underwear_set():
                            text "Sluttiness (As Underwear): " + str(demo_outfit.get_underwear_slut_score()) + "{image=gui/heart/red_heart.png}" style "menu_text_style"
                        else:
                            text "Sluttiness (As Underwear): Invalid" style "menu_text_style"

                    elif outfit_type == "over":
                        if demo_outfit.is_suitable_overwear_set():
                            text "Sluttiness (As Overwear): " + str(demo_outfit.get_overwear_slut_score()) + "{image=gui/heart/red_heart.png}" style "menu_text_style"
                        else:
                            text "Sluttiness (As Overwear): Invalid" style "menu_text_style"
                    text "Tits Visible: " + str(demo_outfit.tits_visible()) style "menu_text_style" #TODO: Show what effects these are having on the outfit.
                    text "Tits Usable: " + str(demo_outfit.tits_available()) style "menu_text_style"
                    text "Wearing a Bra: " + str(demo_outfit.wearing_bra()) style "menu_text_style"
                    text "Bra Covered: " + str(demo_outfit.bra_covered()) style "menu_text_style"
                    text "Pussy Visible: " + str(demo_outfit.vagina_visible()) style "menu_text_style"
                    text "Pussy Usable: " + str(demo_outfit.vagina_available()) style "menu_text_style"
                    text "Wearing Panties: " + str(demo_outfit.wearing_panties()) style "menu_text_style"
                    text "Panties Covered: " + str(demo_outfit.panties_covered()) style "menu_text_style"

                    hbox:
                        yalign 1.0
                        xalign 0.5
                        xanchor 0.5
                        spacing 50
                        $ save_button_name = "Save Outfit"
                        if slut_limit is not None:
                            $ save_button_name += "\nLimit: " + str(slut_limit) + "{image=gui/heart/red_heart.png}"
                        $ slut_to_use = starting_outfit.slut_requirement
                        if outfit_type == "under":
                            $ slut_to_use = starting_outfit.get_underwear_slut_score()
                        elif outfit_type == "over":
                            $ slut_to_use = starting_outfit.get_overwear_slut_score()

                        textbutton save_button_name:
                            action Return(starting_outfit.get_copy())
                            style "textbutton_style"
                            text_style "textbutton_text_style" text_text_align 0.5 text_xalign 0.5 xysize (155,80)
                            sensitive slut_limit is None or slut_to_use <= slut_limit
                        textbutton "Abandon Design" action Return("Not_New") style "textbutton_style" text_style "textbutton_text_style" text_text_align 0.5 text_xalign 0.5 xysize (185,80)

        frame:
            background "#aaaaaa"
            xsize 180
            vbox:
                style_prefix "check"
                label "Show Layers" text_style "menu_text_style" text_size 22
                textbutton "Underwear" action ToggleScreenVariable("hide_underwear", False, True) text_size 20
                textbutton "Clothing" action ToggleScreenVariable("hide_base", False, True) text_size 20
                textbutton "Overwear" action ToggleScreenVariable("hide_overwear", False, True) text_size 20

    fixed: #TODO: Move this to it's own screen so it can be shown anywhere
        pos (1450,0)
        add mannequin_average
        # TODO: Add radio buttons to show or hide layers
        $ hide_list = []
        if hide_underwear:
            $ hide_list.append(1)
        if hide_base:
            $ hide_list.append(2)
        if hide_overwear:
            $ hide_list.append(3)
        for cloth in demo_outfit.generate_draw_list(None,"stand3", hide_layers = hide_list):
            add cloth

    imagebutton:
        auto "/tutorial_images/restart_tutorial_%s.png"
        xsize 54
        ysize 54
        yanchor 1.0
        xanchor 1.0
        xalign 1.0
        yalign 1.0
        action Function(mc.business.reset_tutorial,"outfit_tutorial")


    $ outfit_tutorial_length = 8 #The number of  tutorial screens we have.
    if mc.business.event_triggers_dict["outfit_tutorial"] > 0 and mc.business.event_triggers_dict["outfit_tutorial"] <= outfit_tutorial_length: #We use negative numbers to symbolize the tutorial not being enabled
        imagebutton:
            auto
            sensitive True
            xsize 1920
            ysize 1080
            idle "/tutorial_images/outfit_tutorial_"+__builtin__.str(mc.business.event_triggers_dict["outfit_tutorial"])+".png"
            hover "/tutorial_images/outfit_tutorial_"+__builtin__.str(mc.business.event_triggers_dict["outfit_tutorial"])+".png"
            action Function(mc.business.advance_tutorial,"outfit_tutorial")

style outfit_description_style is textbutton_text_style:
    size 14

screen outfit_delete_manager(the_wardrobe): ##Allows removal of outfits from players saved outfits.
    add "Paper_Background.png"
    modal True
    zorder 100
    default preview_outfit = None
    hbox:
        spacing 20
        xalign 0.1
        yalign 0.1
        frame:
            background "#888888"
            xsize 450
            ysize 750
            viewport:
                scrollbars "vertical"
                xsize 450
                ysize 750
                mousewheel True
                vbox:
                    text "Full Outfits" style "menu_text_style" size 30
                    for outfit in the_wardrobe.get_outfit_list():
                        textbutton "Delete "+outfit.name+ "\n(Sluttiness " +str(outfit.slut_requirement) +")" action Function(the_wardrobe.remove_outfit,outfit) hovered SetScreenVariable("preview_outfit", outfit.get_copy()) unhovered SetScreenVariable("preview_outfit", None) style "textbutton_style" text_style "outfit_description_style" xsize 210

        frame:
            background "#888888"
            xsize 450
            ysize 750
            viewport:
                scrollbars "vertical"
                xsize 450
                ysize 750
                mousewheel True
                vbox:
                    text "Overwear Sets" style "menu_text_style" size 30
                    for outfit in the_wardrobe.get_overwear_sets_list():
                        textbutton "Delete "+outfit.name+ "\n(Sluttiness " +str(outfit.get_overwear_slut_score()) +")" action Function(the_wardrobe.remove_outfit,outfit) hovered SetScreenVariable("preview_outfit", outfit.get_copy()) unhovered SetScreenVariable("preview_outfit", None) style "textbutton_style" text_style "outfit_description_style" xsize 210

        frame:
            background "#888888"
            xsize 450
            ysize 750
            viewport:
                scrollbars "vertical"
                xsize 450
                ysize 750
                mousewheel True
                vbox:
                    text "Underwear Sets" style "menu_text_style" size 30
                    for outfit in the_wardrobe.get_underwear_sets_list():
                        textbutton "Delete "+outfit.name+ "\n(Sluttiness " +str(outfit.get_underwear_slut_score()) +")" action Function(the_wardrobe.remove_outfit,outfit) hovered SetScreenVariable("preview_outfit", outfit.get_copy()) unhovered SetScreenVariable("preview_outfit", None) style "textbutton_style" text_style "outfit_description_style" xsize 210


    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action Return("No Return")
        textbutton "Return" align [0.5,0.5] text_style "return_button_style"

    fixed:
        pos (1450,0)
        add mannequin_average
        if preview_outfit:
            for cloth in preview_outfit.generate_draw_list(None,"stand3"):
                add cloth

screen outfit_select_manager(slut_limit = 999, show_outfits = True, show_overwear = True, show_underwear = True, main_selectable = True, show_make_new = True, show_export = True, show_modify = True, show_duplicate = True, show_delete = True):
    #If sluttiness_limit is passed, you cannot exit the creator until the proposed outfit has a sluttiness below it (or you create nothing).
    add "Paper_Background.png"
    modal True
    zorder 100
    default preview_outfit = None

    $ outfit_info_array = []
    ## ["Catagory name", is_catagory_enabled, "return value when new is made", slut score calculation field/function, "export field type", add_outfit_to_wardrobe_function] ##
    $ outfit_info_array.append([show_outfits, "Full Outfit", "new_full", Outfit.get_slut_requirement , "FullSets", Wardrobe.add_outfit, Wardrobe.get_outfit_list])
    $ outfit_info_array.append([show_overwear, "Overwear Set", "new_over", Outfit.get_overwear_slut_score, "OverwearSets",  Wardrobe.add_overwear_set, Wardrobe.get_overwear_sets_list])
    $ outfit_info_array.append([show_underwear, "Underwear Set", "new_under", Outfit.get_underwear_slut_score, "UnderwearSets", Wardrobe.add_underwear_set, Wardrobe.get_underwear_sets_list])

    hbox:
        spacing 20
        xalign 0.1
        yalign 0.1
        for catagory_info in outfit_info_array:
            if catagory_info[0]:
                frame:
                    background "#888888"
                    xsize 450
                    ysize 850
                    viewport:
                        scrollbars "vertical"
                        xsize 450
                        ysize 850
                        mousewheel True
                        vbox:
                            spacing -10
                            text catagory_info[1] + "s" style "menu_text_style" size 30 #Add an s to make it plural so we can reuse the field in the new button. Yep, I'm that clever-lazy.
                            null height 10
                            if show_make_new:
                                textbutton "Create New " + catagory_info[1]:
                                    action Return(catagory_info[2])
                                    sensitive True
                                    style "textbutton_style"
                                    text_style "outfit_description_style"
                                    xsize 450

                                null height 35

                            for outfit in catagory_info[6](mc.designed_wardrobe):
                                textbutton outfit.name + " (Sluttiness " +str(catagory_info[3](outfit)) +")":
                                    action Return(["select",outfit.get_copy()])
                                    sensitive (catagory_info[3](outfit) <= slut_limit) and main_selectable
                                    hovered SetScreenVariable("preview_outfit", outfit.get_copy())
                                    unhovered SetScreenVariable("preview_outfit", None)
                                    style "textbutton_style"
                                    text_style "outfit_description_style"
                                    tooltip "Pick this outfit."
                                    xsize 450

                                if show_export or show_modify or show_duplicate or show_delete:
                                    hbox:
                                        spacing 0
                                        xsize 450
                                        if show_export:
                                            default exported = []
                                            textbutton "Export":
                                                action [Function(exported.append,outfit), Function(log_outfit, outfit, outfit_class = catagory_info[4], wardrobe_name = "Exported_Wardrobe"), Function(renpy.notify, "Outfit exported to Exported_Wardrobe.xml")]
                                                sensitive outfit not in exported
                                                hovered SetScreenVariable("preview_outfit", outfit.get_copy())
                                                unhovered SetScreenVariable("preview_outfit", None)
                                                style "textbutton_style"
                                                text_style "outfit_description_style"
                                                tooltip "Export this outfit. The export will be added as an xml section in game/wardrobes/Exported_Wardrobe.xml."
                                                xsize 100

                                        if show_modify:
                                            textbutton "Modify":
                                                action Return(["modify",outfit]) #If we are modifying an outfit just return it. outfit management loop will find which catagory it is in.
                                                sensitive (catagory_info[3](outfit) <= slut_limit)
                                                hovered SetScreenVariable("preview_outfit", outfit.get_copy())
                                                unhovered SetScreenVariable("preview_outfit", None)
                                                style "textbutton_style"
                                                text_style "outfit_description_style"
                                                tooltip "Modify this outfit."
                                                xsize 100

                                        if show_duplicate:
                                            $ the_copied_outfit = outfit.get_copy() #We make a copy to add to the wardrobe if this is selected. Otherwise continues same as "Modify"
                                            textbutton "Duplicate":
                                                action [Function(catagory_info[5], mc.designed_wardrobe, the_copied_outfit), Return(["duplicate",the_copied_outfit])]
                                                #sensitive (catagory_info[3](outfit) <= slut_limit)
                                                hovered SetScreenVariable("preview_outfit", outfit.get_copy())
                                                unhovered SetScreenVariable("preview_outfit", None)
                                                style "textbutton_style"
                                                text_style "outfit_description_style"
                                                tooltip "Duplicate this outfit and edit the copy, leaving the original as it is."
                                                xsize 100

                                        if show_delete:
                                            textbutton "Delete":
                                                action Function(mc.designed_wardrobe.remove_outfit, outfit)
                                                #sensitive (catagory_info[3](outfit) <= slut_limit)
                                                hovered SetScreenVariable("preview_outfit", outfit.get_copy())
                                                unhovered SetScreenVariable("preview_outfit", None)
                                                style "textbutton_style"
                                                text_style "outfit_description_style"
                                                tooltip "Remove this outfit from your wardrobe. This cannot be undone!"
                                                xsize 100

                                    null height 20

                                null height 25

        if slut_limit != 999:
            frame:
                background "#888888"
                text "Slut Limit: " + str(slut_limit) + "{image=gui/heart/red_heart.png}" style "textbutton_text_style" text_align 0.0
    frame:
        background None
        anchor [0.5,0.5]
        align [0.39,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action Return("No Return")
        textbutton "Return" align [0.5,0.5] text_style "return_button_style"

    fixed:
        pos (1450,0)
        add mannequin_average
        if preview_outfit:
            for cloth in preview_outfit.generate_draw_list(None,"stand3"):
                add cloth

screen girl_outfit_select_manager(the_wardrobe, show_sets = False): ##Brings up a list of outfits currently in a girls wardrobe.
    add "Paper_Background.png"
    modal True
    zorder 100
    default preview_outfit = None

    hbox:
        xalign 0.1
        yalign 0.1
        spacing 20
        frame:
            background "#888888"
            xsize 450
            ysize 750
            viewport:
                scrollbars "vertical"
                xsize 450
                ysize 750
                mousewheel True
                vbox:
                    text "Full Outfits" style "menu_text_style" size 30
                    for outfit in the_wardrobe.get_outfit_list():
                        textbutton "Select "+outfit.name+ "\n(Sluttiness " +str(outfit.slut_requirement) +")" action Return(outfit) hovered SetScreenVariable("preview_outfit", outfit.get_copy()) unhovered SetScreenVariable("preview_outfit", None) style "textbutton_style" text_style "outfit_description_style" xsize 210

        if show_sets:
            frame:
                background "#888888"
                xsize 450
                ysize 750
                viewport:
                    scrollbars "vertical"
                    xsize 450
                    ysize 750
                    mousewheel True
                    vbox:
                        text "Overwear Sets" style "menu_text_style" size 30
                        for outfit in the_wardrobe.get_overwear_sets_list():
                            textbutton "Select "+outfit.name+ "\n(Sluttiness " +str(outfit.get_overwear_slut_score()) +")" action Return(outfit) hovered SetScreenVariable("preview_outfit", outfit.get_copy()) unhovered SetScreenVariable("preview_outfit", None) style "textbutton_style" text_style "outfit_description_style" xsize 210

            frame:
                background "#888888"
                xsize 450
                ysize 750
                viewport:
                    scrollbars "vertical"
                    xsize 450
                    ysize 750
                    mousewheel True
                    vbox:
                        text "Underwear Sets" style "menu_text_style" size 30
                        for outfit in the_wardrobe.get_underwear_sets_list():
                            textbutton "Select "+outfit.name+ "\n(Sluttiness " +str(outfit.get_underwear_slut_score()) +")" action Return(outfit) hovered SetScreenVariable("preview_outfit", outfit.get_copy()) unhovered SetScreenVariable("preview_outfit", None) style "textbutton_style" text_style "outfit_description_style" xsize 210

    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action Return("None")
        textbutton "Return" align [0.5,0.5] text_style "return_button_style"

    fixed:
        pos (1450,0)
        add mannequin_average
        if preview_outfit:
            for cloth in preview_outfit.generate_draw_list(None,"stand3"):
                add cloth

screen map_manager():
    add "Paper_Background.png"
    modal True
    zorder 100

    $ x_size_percent = 0.07
    $ y_size_percent = 0.145

    for place in list_of_places: #Draw the text buttons over the background
        if place.visible:
            $ hex_x = x_size_percent * place.map_pos[0]
            $ hex_y = y_size_percent * place.map_pos[1]
            if place.map_pos[0] % 2 == 1:
                $ hex_y += y_size_percent/2
            if not place == mc.location:
                frame:
                    background None
                    xysize [171,150]
                    anchor [0.0,0.0]
                    align (hex_x,hex_y)
                    imagebutton:
                        anchor [0.5,0.5]
                        auto "gui/LR2_Hex_Button_%s.png"
                        focus_mask "gui/LR2_Hex_Button_idle.png"
                        action Function(mc.change_location,place)
                        sensitive place.accessable #TODO: replace once we want limited travel again with: place in mc.location.connections
                    text place.formalName + "\n(" + str(len(place.people)) + ")" anchor [0.5,0.5] style "map_text_style"

            else:
                frame:
                    background None
                    xysize [171,150]
                    anchor [0.0,0.0]
                    align (hex_x,hex_y)
                    imagebutton:
                        anchor [0.5,0.5]
                        idle "gui/LR2_Hex_Button_Alt_idle.png"
                        focus_mask "gui/LR2_Hex_Button_Alt_idle.png"
                        action Function(mc.change_location,place)
                        sensitive False
                    text place.formalName + "\n(" + str(len(place.people)) + ")" anchor [0.5,0.5] style "map_text_style"

        ##TODO: add a sub map to housing_map_manager() so we can go to people's homes

    $ xy_pos = [7,4]
    $ hex_x = x_size_percent * xy_pos[0]
    $ hex_y = y_size_percent * xy_pos[1]
    if xy_pos[0] % 2 == 1:
        $ hex_y += y_size_percent/2

    if mc.location in mc.known_home_locations:
        frame:
            background None
            xysize [171,150]
            anchor [0.0,0.0]
            align (hex_x,hex_y)
            imagebutton:
                anchor [0.5,0.5]
                idle "gui/LR2_Hex_Button_Alt_idle.png"
                focus_mask "gui/LR2_Hex_Button_Alt_idle.png"
                action Show("housing_map_manager")
                sensitive len(mc.known_home_locations) > 0
            text "Visit Someone..." anchor [0.5,0.5] style "map_text_style"
    else:
        frame:
            background None
            xysize [171,150]
            anchor [0.0,0.0]
            align (hex_x, hex_y)
            imagebutton:
                anchor [0.5,0.5]
                auto "gui/LR2_Hex_Button_%s.png"
                focus_mask "gui/LR2_Hex_Button_idle.png"
                action Show("housing_map_manager")
                sensitive len(mc.known_home_locations) > 0
            text "Visit Someone..." anchor [0.5,0.5] style "map_text_style"

    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action Return(mc.location)
        textbutton "Return" align [0.5,0.5] text_style "return_button_style"

screen housing_map_manager():
    modal True
    zorder 101
    add "Paper_Background.png"

    $ x_pos = 0
    $ y_pos = 0
    $ max_places_per_row = 5
    $ x_offset_per_place = 0.145
    $ y_offset_per_row = 0.07
    for place in mc.known_home_locations:
        if not place == mc.location and not place.hide_in_known_house_map:
            frame:
                background None
                xysize [171,150]
                anchor [0.0,0.0]
                align [0.2+(x_offset_per_place*x_pos),0.4+(y_offset_per_row*y_pos)]
                imagebutton:
                    anchor [0.5,0.5]
                    auto "gui/LR2_Hex_Button_%s.png"
                    focus_mask "gui/LR2_Hex_Button_idle.png"
                    action Function(mc.change_location,place)
                    sensitive place.accessable
                text place.formalName + "\n(" + str(len(place.people)) + ")" anchor [0.5,0.5] style "map_text_style"

        else:
            frame:
                background None
                xysize [171,150]
                anchor [0.0,0.0]
                align [0.1+(x_offset_per_place*x_pos),0.5+(y_offset_per_row*y_pos)]
                imagebutton:
                    anchor [0.5,0.5]
                    idle "gui/LR2_Hex_Button_Alt_idle.png"
                    focus_mask "gui/LR2_Hex_Button_Alt_idle.png"
                    action Function(mc.change_location,place)
                    sensitive False
                text place.formalName + "\n(" + str(len(place.people)) + ")" anchor [0.5,0.5] style "map_text_style"
        $ x_pos += 1
        if x_pos >= max_places_per_row + 0.5:
            $ x_pos += 0.5
            $ x_pos += -max_places_per_row
            $ y_pos += 1

    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action [Hide("housing_map_manager"), Return(mc.location)]
        textbutton "Return" align [0.5,0.5] text_style "return_button_style"


init -2 python:
    def purchase_policy(the_policy):
        the_policy.buy_policy()
        if not the_policy.toggleable or the_policy.is_toggleable(): #Note: is_toggleable() checks to see if a toggleable policy has pre-reqs met to toggle, while toggleable flags a policy to turn on when bought then stay on.
            the_policy.apply_policy()

    def toggle_policy(the_policy):
        if the_policy in mc.business.active_policy_list:
            the_policy.remove_policy()
        else:
            the_policy.apply_policy()


init -2 screen policy_selection_screen_v2():
    add "Paper_Background.png"
    modal True
    zorder 100
    $ tooltip = GetTooltip()
    $ catagories = [["Uniform Policies",uniform_policies_list], ["Recruitment Policies",recruitment_policies_list], ["Serum Policies",serum_policies_list], ["Organisation Policies",organisation_policies_list]]
    default selected_catagory = catagories[0] #Default to the first in our catagories list
    default selected_policy = None #If not None this will have it's info displayed on the right section of the bottom pane
    #TODO: Side bar showing current and max Complience, once the Complience system is added.

    vbox:
        xalign 0.5
        xanchor 0.5
        yanchor 0.0
        yalign 0.05
        spacing 20
        frame: #Top frame holding the policy catagories that we have.
            xsize 1320
            ysize 140
            background "#aaaaaa"
            text "Funds: $[mc.business.funds]":
                xalign 1.0
                xanchor 1.0
                yanchor 0.0
                style "textbutton_text_style"
                size 18
            vbox:
                text "Policy Catagories" style "menu_text_style" size 26 yalign 0.5 yanchor 0.5 xalign 0.5 xanchor 0.5
                xalign 0.5
                xanchor 0.5
                hbox:
                    spacing 25
                    xalign 0.5
                    xanchor 0.5
                    for catagory in catagories:
                        textbutton catagory[0]:
                            xsize 300
                            ysize 80
                            action SetScreenVariable("selected_catagory", catagory)
                            sensitive selected_catagory != catagory
                            style "textbutton_style"
                            text_style "textbutton_text_style"
                            background "#000080"
                            hover_background "#1a45a1"
                            insensitive_background "#222222"

        frame:
            xsize 1320
            ysize 650
            background "#aaaaaa"
            xpadding 20
            ypadding 20
            hbox: #Container for the policy select and policy info screens.
                xanchor 0.5
                xalign 0.5
                yanchor 0.5
                yalign 0.5
                xsize 1300
                ysize 600
                spacing 20
                xfill True
                frame: #Container for policy select
                    xsize 500
                    background "#888888"
                    viewport:
                        mousewheel True
                        scrollbars "vertical"
                        vbox: # Contains list for policy select
                            spacing 0
                            for policy in selected_catagory[1]:
                                $ policy_name = policy.name + " - "
                                if policy.is_active(): #Display owned and active policies
                                    $ policy_name += "Active"
                                elif policy.is_owned():
                                    $ policy_name += "Disabled"
                                else:
                                    if policy.cost <= mc.business.funds:
                                        $ policy_name += "{color=20a020}$" + str(policy.cost) + "{/color}"
                                    else:
                                        $ policy_name += "{color=902020}$" + str(policy.cost) + "{/color}"

                                    if not (policy.requirement() and (policy.cost <= mc.business.funds)):
                                        $ policy_name = "{color=999999}" + policy_name + "{/color}"
                                textbutton policy_name:
                                    xalign 0.5
                                    xanchor 0.5
                                    #xsize 500
                                    xfill True
                                    action SetScreenVariable("selected_policy", policy)
                                    style "textbutton_style"
                                    text_style "textbutton_text_style"
                                    text_size 16
                                    if policy.is_owned():
                                        background "#59853f"
                                        hover_background "#a9d59f"
                                        #insensitive_background "#305012"
                                        insensitive_background "#222222"
                                    else:
                                        if policy.requirement() and (policy.cost <= mc.business.funds):
                                            background "#000080"
                                        else:
                                            background "#000040"
                                        hover_background "#1a45a1"
                                        insensitive_background "#222222"
                                    sensitive selected_policy != policy

                frame: #Container for the seleected policy info.
                    background "#888888"
                    xsize 780
                    xpadding 40
                    ypadding 10
                    if selected_policy is not None:
                        viewport:
                            mousewheel True
                            scrollbars "vertical"
                            xalign 0.5
                            xanchor 0.5
                            ysize 500

                            vbox: # Contains title, description, and buy/toggle button for policy
                                xalign 0.5
                                xanchor 0.5
                                xfill True

                                text selected_policy.name:
                                    xalign 0.5
                                    xanchor 0.5
                                    yanchor 0.0
                                    text_align 0.5
                                    size 32
                                    style "textbutton_text_style"

                                null height 30

                                text selected_policy.desc:
                                    xalign 0.5
                                    xanchor 0.5
                                    yanchor 0.0
                                    text_align 0.5
                                    size 16
                                    style "textbutton_text_style"
                                    justify True

                        if selected_policy.is_owned():
                            $ the_button_name = ""
                            if selected_policy.toggleable:
                                if selected_policy.is_active():
                                    $ the_button_name = "Disable Policy"
                                else:
                                    $ the_button_name = "Enable Policy"

                                if not selected_policy.is_toggleable():
                                    if selected_policy.is_active():
                                        $ the_button_name += "\n{size=12}{color=#800000}Cannot be disabled, needed for:\n"
                                        $ blocking_policies = [a_policy for a_policy in selected_policy.depender_policies if a_policy.is_active()]
                                        for requirement in blocking_policies:
                                            $ the_button_name += requirement.name
                                            if requirement is not blocking_policies[-1]:
                                                $ the_button_name += "\n" #Format the list with a comma if not at the end of the list.
                                        $ the_button_name += "{/color}{/size}"


                                    else:
                                        $ the_button_name += "\n{size=12}{color=#800000}Requires Active:\n"
                                        $ blocking_policies = [a_policy for a_policy in selected_policy.dependant_policies if not a_policy.is_active()]
                                        for requirement in blocking_policies:
                                            $ the_button_name += requirement.name
                                            if requirement is not blocking_policies[-1]:
                                                $ the_botton_name += "\n" #Format the list with a comma if not at the end of the list.
                                        $ the_button_name += "{/color}{/size}"
                            else: #Note: Non-toggleable policies that are owned should _always_ be active.
                                $ the_button_name = "Policy Active"

                            textbutton the_button_name:
                                xalign 0.5
                                xanchor 0.5
                                yalign 1.0
                                yanchor 1.0
                                xsize 300
                                action Function(toggle_policy, selected_policy)
                                style "textbutton_style"
                                text_style "textbutton_text_style"
                                background "#000080"
                                hover_background "#1a45a1"
                                insensitive_background "#222222"
                                sensitive selected_policy.is_toggleable()
                                text_xalign 0.5
                                text_xanchor 0.5
                        else: #We want to purchase it
                            textbutton "Purchase: $[selected_policy.cost]":
                                xalign 0.5
                                xanchor 0.5
                                yalign 1.0
                                yanchor 1.0
                                xsize 300
                                action Function(purchase_policy, selected_policy)
                                style "textbutton_style"
                                text_style "textbutton_text_style"
                                background "#000080"
                                hover_background "#1a45a1"
                                insensitive_background "#222222"
                                sensitive selected_policy.requirement() and (selected_policy.cost <= mc.business.funds)
                                text_xalign 0.5
                                text_xanchor 0.5

    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action Return()
        textbutton "Return" align [0.5,0.5] text_style "return_button_style"

    imagebutton:
        auto "/tutorial_images/restart_tutorial_%s.png"
        xsize 54
        ysize 54
        yanchor 1.0
        xalign 0.0
        yalign 1.0
        action Function(mc.business.reset_tutorial,"policy_tutorial")

    $ policy_tutorial_length = 4 #The number of  tutorial screens we have.
    if mc.business.event_triggers_dict["policy_tutorial"] > 0 and mc.business.event_triggers_dict["policy_tutorial"] <= policy_tutorial_length: #We use negative numbers to symbolize the tutorial not being enabled
        imagebutton:
            auto
            sensitive True
            xsize 1920
            ysize 1080
            idle "/tutorial_images/policy_tutorial_"+__builtin__.str(mc.business.event_triggers_dict["policy_tutorial"])+".png"
            hover "/tutorial_images/policy_tutorial_"+__builtin__.str(mc.business.event_triggers_dict["policy_tutorial"])+".png"
            action Function(mc.business.advance_tutorial,"policy_tutorial")


init -2 screen policy_selection_screen():
    add "Paper_Background.png"
    modal True
    zorder 100
    $ tooltip = GetTooltip()
    $ catagories = [["Uniform Policies",uniform_policies_list], ["Recruitment Policies",recruitment_policies_list], ["Serum Policies",serum_policies_list], ["Organisation Policies",organisation_policies_list]]
    default selected_catagory = catagories[0] #Default to the first in our catagories list
    vbox:
        xalign 0.5
        yalign 0.15
        spacing 30
        frame: #Top frame holding the policy catagories that we have.
            xsize 1320
            ysize 140
            background "#1a45a1aa"
            vbox:
                text "Policy Catagories" style "menu_text_style" size 26 yalign 0.5 yanchor 0.5 xalign 0.5 xanchor 0.5
                hbox:
                    spacing 35
                    xalign 0.5
                    xanchor 0.5
                    for catagory in catagories:
                        textbutton catagory[0]:
                            xsize 300
                            ysize 80
                            action SetScreenVariable("selected_catagory", catagory)
                            sensitive selected_catagory != catagory
                            style "textbutton_style"
                            text_style "textbutton_text_style"

        frame: #Holds the list of business policies. Needs to be scrollable.
            xsize 1320
            ysize 650
            background "#1a45a1aa"
            viewport:
                mousewheel True
                scrollbars "vertical"
                xsize 800
                ysize 650
                vbox:
                    spacing 10
                    for policy in selected_catagory[1]:
                        if policy.is_owned():
                            textbutton "$" + str(policy.cost) + " - " + policy.name:
                                tooltip policy.desc
                                action NullAction()
                                style "textbutton_style"
                                text_style "textbutton_text_style"
                                background "#59853f"
                                hover_background "#78b156"
                                sensitive True
                                xsize 800
                                ysize 100
                        else:
                            if policy.requirement() and (policy.cost < mc.business.funds or policy.cost == mc.business.funds):
                                textbutton "$" + str(policy.cost) + " - " + policy.name:
                                    tooltip policy.desc
                                    style "textbutton_style"
                                    text_style "textbutton_text_style"
                                    action Function(purchase_policy,policy)
                                    sensitive policy.requirement() and (policy.cost < mc.business.funds or policy.cost == mc.business.funds)
                                    xsize 800
                                    ysize 100
                            else:
                                textbutton "$" + str(policy.cost) + " - " + policy.name:
                                    tooltip policy.desc
                                    style "textbutton_style"
                                    text_style "textbutton_text_style"
                                    background "#666666"
                                    action NullAction()
                                    sensitive True
                                    xsize 800
                                    ysize 100


    if tooltip:
        frame:
            background "#1a45a1aa"
            anchor [1.0,0.0]
            align [0.84,0.2]
            xsize 500
            text tooltip style "menu_text_style"

    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action Return()
        textbutton "Return" align [0.5,0.5] text_style "return_button_style"

    imagebutton:
        auto "/tutorial_images/restart_tutorial_%s.png"
        xsize 54
        ysize 54
        yanchor 1.0
        xalign 0.0
        yalign 1.0
        action Function(mc.business.reset_tutorial,"policy_tutorial")

    $ policy_tutorial_length = 4 #The number of  tutorial screens we have.
    if mc.business.event_triggers_dict["policy_tutorial"] > 0 and mc.business.event_triggers_dict["policy_tutorial"] <= policy_tutorial_length: #We use negative numbers to symbolize the tutorial not being enabled
        imagebutton:
            auto
            sensitive True
            xsize 1920
            ysize 1080
            idle "/tutorial_images/policy_tutorial_"+__builtin__.str(mc.business.event_triggers_dict["policy_tutorial"])+".png"
            hover "/tutorial_images/policy_tutorial_"+__builtin__.str(mc.business.event_triggers_dict["policy_tutorial"])+".png"
            action Function(mc.business.advance_tutorial,"policy_tutorial")


init -2 style return_button_style:
    text_align 0.5
    size 30
    italic True
    bold True
    color "#dddddd"
    outlines [(2,"#222222",0,0)]

init -2 style map_text_style:
    text_align 0.5
    size 14
    italic True
    bold True
    color "#dddddd"
    outlines [(2,"#222222",0,0)]

init -2 style map_frame_style:
    background "#094691"

init -2 style map_frame_blue_style:
    background "#5fa7ff"

init -2 style map_frame_grey_style:
    background "#222222"

init -2 python:
    def greyout_transform(d):
        return AlphaBlend(Solid("#fff"), d, Solid("#000"), True)

init -2 style digital_text is text:
    font "Autobusbold-1ynL.ttf"
    color "#19e9f7"
    outlines [(2,"#222222",0,0)]
    yanchor 0.5
    yalign 0.5

init -2 style text_message_style is say_dialogue:
    font "Autobusbold-1ynL.ttf"
    color "#19e9f7"
    outlines [(2,"#222222",0,0)]
    #TODO: MIght need to decide on Size too

init -2 style general_dialogue_style is say_dialogue:
    outlines [(2,"#222222",0,0)]


transform float_up:
    subpixel True #Experimental, might have performance impact.
    xalign 0.92
    yalign 1.0
    alpha 1.0
    ease 1.0 yalign 0.4
    easeout 2.0 alpha 0.0

style float_text:
    size 30
    italic True
    bold True
    outlines [(2,"#222222",0,0)]

style float_text_pink is float_text:
    color "#FFB6C1"

style float_text_red is float_text:
    color "B22222"

style float_text_grey is float_text:
    color "696969"

style float_text_green is float_text:
    color "228B22"

style float_text_yellow is float_text:
    color "D2691E"

style float_text_blue is float_text:
    color "483D8B"

# screen float_up_screen (text_array, style_array): #text_array is a list of the text to be displayed on each line, style_array is the list of corisponding styles to be used for that text.
#     vbox at float_up:
#         xanchor 0.5
#         for index, update_text in enumerate(text_array):
#             text update_text style style_array[index]
#     timer 3.0 action Hide("float_up_screen") #Hide this screen after 3 seconds, so it can be called again by something else.

label start:
    scene bg paper_menu_background with fade
    "Lab Rats 2 contains adult content. If you are not over 18 or your country's equivalent age you should not view this content."
    menu:
        "I am over 18.":
            "Excellent, let's continue then."

        "I am not over 18.":
            $renpy.full_restart()

    "Vren" "v0.38.1 represents an early iteration of Lab Rats 2. Expect to run into limited content, unexplained features, and unbalanced game mechanics."
    "Vren" "Would you like to view the FAQ?"
    menu:
        "View the FAQ.":
            call faq_loop from _call_faq_loop
        "Get on with the game!":
            "You can access the FAQ from your bedroom at any time."

    "Vren" "Lab Rats 2 contains content related to impregnation and pregnancy. These settings may be changed in the menu at any time."
    menu:
        "No pregnancy content.\n{size=16}Girls never become pregnant. Most pregnancy content hidden.{/size}":
            $ persistent.pregnancy_pref = 0

        "Predictable pregnancy content.\n{size=16}Birth control is 100%% effective. Girls always default to taking birth control.{/size}":
            $ persistent.pregnancy_pref = 1

        "Realistic pregnancy content.\n{size=16}Birth control is not 100%% effective. Girls may not be taking birth control.{/size}":
            $ persistent.pregnancy_pref = 2

    $ renpy.block_rollback()
    call screen character_create_screen()
    $ return_arrays = _return #These are the stat, skill, and sex arrays returned from the character creator.
    call create_test_variables(store.name,store.b_name,store.l_name,return_arrays[0],return_arrays[1],return_arrays[2]) from _call_create_test_variables ##Moving some of this to an init block (init 1specifically) would let this play better with updates in the future.
    $ renpy.block_rollback()
    menu:
        "Play introduction and tutorial.":
            call tutorial_start from _call_tutorial_start

        "Skip introduction and tutorial.":
            $ mc.business.event_triggers_dict["Tutorial_Section"] = False
    jump normal_start

label tutorial_start:
    menu:
        "I have played Lab Rats 1 Before.":
            "It has been a year since the end of your summer job at the university lab."



        "I am new to Lab Rats.":
            "A year ago you were a chemical engineering student, getting ready to graduate soon and looking for something to do over the summer."
            "You ended up with a summer job on campus as a lab assistant working with a two person team."
            "Your lab director, Nora, and her long time lab assistant Stephanie were investigating the properties of a new lab created molecule."
            "It didn't take long before you discovered it could be used to deliver mind altering agents. You spent the summer creating doses of \"serum\" in secret."
            "It has been a year since the end of your summer job at the university lab."

    "Your experimentation with the inhibition removing serum was fun, but in the end the effects were temporary."
    "The end of the summer also meant the end of your access to the serum making supplies."
    "Little by litle the women slid back into into their previous lives."

    scene
    $ bedroom.show_background()

    "Four months ago you graduated from university with a degree in chemical engineering."
    "Since then you have been living at home and sending out resumes. You have had several interviews, but no job offers yet."
    "Today you have have an interview with a small pharmacutical company. You've gotten up early and dressed in your finest suit."
    $ hall.show_background()
    "You head for the front door, eager to get to your interview early."
    mom.char "[mom.mc_title], are you leaving already?"
    "[mom.possessive_title]'s voice comes from the kitchen, along with the smell of breakfast."
    mc.name "Yeah, I want make sure I make it on time."
    mom.char "You haven't had any breakfast yet. You should eat, I'll drive you if you're running late."
    "The smell of cooked toast and frying eggs wins you over and you head to the kitchen."
    $ kitchen.show_background()
    $ mom.draw_person(emotion = "happy", position = "back_peek")
    "[mom.possessive_title] is at the stove and looks back at you when you come into the room."
    mom.char "The food's almost ready. Just take a seat and I'll make you a plate."
    mc.name "Thanks Mom, I didn't realize how hungry I was. Nerves, I guess."
    mom.char "Don't worry, I'm sure they'll love you."
    "She turns back and focuses her attention on her cooking. A few minutes later she presents you with a plate."
    $ mom.draw_person(emotion = "happy")
    mom.char "Here you go sweetheart. You look very sharp in your suit, by the way. My little boy is all grown up."
    "You eat quickly, keeping a sharp eye on the time. When you're done you stand up and move to the front door again."
    mc.name "Okay, I've got to go if I'm going to catch my bus. I'll talk to you later and let you know how it goes."
    mom.char "Wait."
    "Mom follows you to the front door. She straightens your tie and brushes some lint off of your shoulder."
    mom.char "Oh, I should have ironed this for you."
    mc.name "It's fine, Mom. Really."
    mom.char "I know, I know, I'll stop fussing. Good luck sweety."
    "She wraps her arms around you and gives you a tight hug. You hug her back then hurry out the door."
    $ clear_scene()
    $ downtown.show_background()
    "It takes an hour on public transit then a short walk to find the building. It's a small single level office attached to a slightly larger warehouse style building."
    "You pull on the door handle. It thunks loudly - locked. You try the other one and get the same result."
    mc.name "Hello?"
    "You pull on the locked door again, then take a step back and look around for another enterance you might have missed. You don't see any."
    "You get your phone out and call the contact number you were given a few days earlier. It goes immediately to a generic voice mail system."
    "With nothing left to do you give up and turn around. Suddenly there's a click and the front door to the office swings open."
    "Janitor" "Hey, who's making all that noise?"
    "A middle aged man is standing at the door wearing grey-brown overalls. He's holding a stack of papers in one hand and a tape gun in the other."
    mc.name "That was me. I'm suppose to be here for a job interview, do you know where I should be going?"
    "Janitor" "Well I think you're shit out of luck then. They went belly up yesterday. This place belongs to the bank now."
    mc.name "What? That can't be right, I was talking to them less than a week ago."
    "Janitor" "Here, take a look for yourself."
    "The man, who you assume is a janitor of some sort, hands you one of the sheets of paper he's holding."
    "It features a picture of the building along with an address matching the one you were given and a large \"FORECLOSED\" label along the top."
    "The janitor turns around and holds a page up to the front door, then sticks it in place with tape around all four edges."
    "Janitor" "They must have been neck deep in dept, if that makes you feel better about not working for 'em."
    "Janitor" "They left all their science stuff behind; must've been worth less than the debt they're ditching."
    mc.name "So everything's still in there?"
    "Janitor" "Seems like it. Bank doesn't know where to sell it and didn't want me to warehouse it, so it goes with the property."
    "You look back at the foreclosure notice and read until you see the listing price."
    "The rent on the unit is expensive, but an order of magnitude less than what you would have expected a fully stocked lab to be worth."
    mc.name "Would you mind if I take a quick look around? I promise I won't be long."
    "The janitor gives you a stern look, judging your character, then nods and opens the door."
    "Janitor" "I'm just about done tidying this place up so the bank can sell it. If you can be in and out in five minutes you can look around."
    mc.name "Thank you, I'll be quick."
    "You step inside the building and take a walk around."
    "The main office building contains a small lab, much like the one you worked at while you were in university, suitable for research and development tasks."
    "The connected warehouse space has a basic chemical production line installed. The machines are all off-brand but seem functional."
    "At the back of the building is a loading dock for shipping and recieving materials."
    "While you're exploring you hear the janitor yell from across the building."
    "Janitor" "I need to be heading off. Are ya done in there?"
    mc.name "Yeah, I'm done. Thanks again."
    "The janitor locks the door when you leave. You get on a bus heading home and do some research on the way."
    "You look up the price of some of the pieces of equipment you saw and confirm your suspicion. The bank has no idea how valuable the property really is."
    scene
    $ renpy.with_statement(fade)
    $ kitchen.show_background()
    "Three days later..."
    $ mom.draw_person(position = "sitting")
    "[mom.title] looks over the paperwork you've laid out. Property cost, equipment value, and potential earnings are all listed."
    mom.char "And you've checked all the numbers?"
    mc.name "Three times."
    mom.char "It's just... this is a lot of money [mom.mc_title]. I would need to take a second morgage out on the house."
    mc.name "And I'll be able to pay for that. This is the chance of a life time Mom."
    mom.char "What was it you said you were going to make again?"
    mc.name "When I was working at the lab last summer we developed some prototype chemical carriers. I think they have huge commercial potential."
    mc.name "And there's no regulation around them yet, because they're so new. I can start production and be selling them tomorrow."
    "[mom.possessive_title] leans back in her chair and pinches the brow of her nose."
    mom.char "Okay, you've convinced me. I'll get in touch with the bank and put a loan on the house."
    "You jump up and throw your arms around [mom.possessive_title]. She laughs and hugs you back."

    lily.char "What's going on?"
    $ lily.draw_person()
    "[lily.possessive_title] steps into the doorway and looks at you both."
    $ mom.draw_person(position = "sitting")
    mom.char "Your brother is starting a business. I'm his first +investor."
    $ lily.draw_person(emotion = "happy")
    lily.char "Is that what you've been excited about the last couple days? What're you actually making?"
    mc.name "I'll have to tell you more about it later Lily, I've got some calls to make. Thanks Mom, you're the best!"
    $ clear_scene()
    "You leave [mom.possessive_title] and sister in the kitchen to talk retreat to your room for some privacy."

    $ bedroom.show_background()
    "You can manage the machinery of the lab, but you're going to need help refining the serum design from last year."
    "You pick up your phone and call [stephanie.title]."
    stephanie.char "Hello?"
    mc.name "Stephanie, this is [mc.name]."
    stephanie.char "[stephanie.mc_title]! Good to hear from you, what's up?"
    mc.name "I'd like to talk to you about a business offer. Any chance we could meet somewhere?"
    stephanie.char "Ooh, a business offer. How mysterious. I'm almost done here at the lab, if you buy me a drink you've got a deal."
    mc.name "Done. Where's convenient for you?"
    "Stephanie sends you the address of a bar close to the university."
    scene
    $ bar_location.show_background()
    "It takes you an hour to get your pitch prepared and to get over to the bar."
    "When you arrive [stephanie.title] is sitting at the bar with a drink already. She smiles and raises her glass."
    $ stephanie.draw_person(position = "sitting", emotion = "happy")
    stephanie.char "Hey [stephanie.mc_title], it's great to see you!"
    "She she stands and gives you a hug."
    stephanie.char "That was a crazy summer we had together. It seems like such a blur now, but I had a lot of fun."
    mc.name "Me too, that's actually part of what I want to talk to you about."
    "You order a drink for yourself and sit down."
    "You lay out your idea to [stephanie.title]: the commercial production and distribution of the experimental serum."
    stephanie.char "Well that's... Fuck, it's bold, I'll say that. And you need me to handle the R&D side of the business."
    mc.name "Right. Production processes are my bread and butter, but I need your help to figure out what we're actually making."
    "Stephanie finishes off her drink and flags down the bartender for another."
    stephanie.char "I would need to quit my job at the lab, and there's no guarantee that this even goes anywhere."
    mc.name "Correct."
    stephanie.char "Do have any clients?"
    mc.name "Not yet. It's hard to have clients without a product."
    "Stephanie gets her drink and sips it thoughtfully."
    mc.name "The pay won't be great either, but I can promise..."
    stephanie.char "I'm in."
    mc.name "I... what?"
    stephanie.char "I'm in. The old lab just doesn't feel the same since you left. I've been looking for something new in my life, something to shake things up."
    stephanie.char "I think this is it."
    "She raises her drink and smiles a huge smile."
    stephanie.char "A toast: To us, and stupid risks!"
    mc.name "To us!"
    "You clink glasses together and drink."
    stephanie.char "Ah... Okay, so I've got some thoughts already..."
    "Stephanie grabs a napkin and starts doodling on it. You spend the rest of the night with her, drinking and talking until you have to say goodbye."
    $ clear_scene()
    "A week later [mom.possessive_title] has a new morgage on the house and purchases the lab in your name."
    "You are the sole shareholder of your own company and [stephanie.title] is first, and so far only, employee. She takes her position as your head researcher."
    $ mc.business.event_triggers_dict["Tutorial_Section"] = True
    #$ mc.can_skip_time = False
    python: #To begin the tutorial we limit where people can travel!
        for place in list_of_places:
            place.accessable = False
    $ lobby.accessable = True
    return

label normal_start:
    ## For now, this ensures reloadin the game doesn't reset any of the variables.
    $ renpy.scene()
    show screen tooltip_screen
    show screen phone_hud_ui
    show screen business_ui
    show screen goal_hud_ui
    show screen main_ui
    $ bedroom.show_background()
    "It's Monday, and the first day of operation for your new business!"
    "[stephanie.title] said she would meet you at your new office for a tour."

    #Add Stepyhanie to our business and flag her with a special role.
    $ mc.business.add_employee_research(stephanie)
    $ mc.business.r_div.add_person(stephanie) #Lets make sure we actually put her somewhere
    $ mc.business.r_div.move_person(stephanie,lobby)
    $ stephanie.set_work(mc.business.r_div)
    $ mc.business.head_researcher = stephanie
    $ stephanie.special_role = [steph_role, employee_role, head_researcher]

    #call examine_room(mc.location) from _call_examine_room
    #TODO: movement overlay tutorial thing.
    jump game_loop

label faq_loop:
    menu:
        "Gameplay Basics.":
            menu:
                "Making Serum.":
                    "Vren" "Making serum in your lab is the most important task for success in Lab Rats 2. You begin the game with a fully equipt lab."
                    "Vren" "The first step to make a serum is to design it in your lab. The most basic serum design can be made without any additions, but most will be made by adding serum traits."
                    "Vren" "Serum traits modify the effects of a serum. The effects can be simple - increasing duration or Suggestion increase - or it may be much more complicated."
                    "Vren" "Each serum design has a limited number of trait slots. The number of slots can be increased by using more advanced serum production techniques."
                    "Vren" "Once you have decided on the traits you wish to include in your serum you will have to spend time in the lab researching it."
                    "Vren " "Place the design in the research queue and spend a few hours working in the lab."
                    "Vren" "More complicated serums will take more time to research. Once the serum is completely researched it can be produced by your production division."
                    "Vren" "Move to your production division and slot the new design into the current production queue."
                    "Vren" "Before you can produce the serum you will need raw supplies."
                    "Vren" "One unit of supply is needed for every production point the serum requires. You can order supply from your main office."
                    "Vren" "Once you have supplies you can spend time in your production lab. Serum is made in batches - unlocking larger batches will let you make more serum with the same amount of supply."
                    "Vren" "You can kepp this serum for personal use or you can head to the main office and mark it for sale."
                    "Vren" "Once a serum is marked for sale you can spend time in your marketing division to find a buyer."
                    "Vren" "Your research and development lab can also spend time researching new traits for serum instead of producing new serum designs."

                "Hiring Staff.":
                    "Vren" "While you can do all the necessary tasks for your company yourself, that isn't how you're going to make it big. Hiring employees will let you spend you grow your business and pull in more and more money."
                    "Vren" "To hire someone, head over to your main office. From there you can request a trio of resumes to choose from, for a small cost. The stats of the three candidates will be chosen, and you can choose who to hire."
                    "Vren" "The three primary stats - Charisma, Intelligence, and Focus - are the most important traits for a character. Each affects the jobs in your company differently."
                    "Vren" "Charisma is the primary stat for marketing and human resources, as well as being a secondary stat for purchasing supplies."
                    "Vren" "Intelligence is the primary stat for research, as well as a secondary stat for human resources and production."
                    "Vren" "Focus is the primary stat for supply procurement and production, as well as a secondary stat for research."
                    "Vren" "Each character will also have an expected salary, to be paid each day. Higher stats will result in a more expensive employee, so consider hiring specialists rather than generalists."
                    "Vren" "Your staff will come into work each morning and perform their appropriate tasks, freeing up your time for other pursuits..."

                "Corrupting People.":
                    "Vren" "You may be wondering what you can do with all this serum you produce. The main use of serum is to increase the Suggestibility statistic of another character."
                    "Vren" "While a character has a Suggestibility value of 0 nothing you do will have a long lasting effect on their personality. Suggestibility above 0 will allow you to slowly corrupt them."
                    "Vren" "Each girl has a Core Sluttiness value. This is the level of sluttiness they think is appropriate without any external influence. Core sluttiness looks like this: {image=gui/heart/gold_heart.png}"
                    "Vren" "They also have a Temporary Sluttiness value, which fluctuates up and down based on recent events. Temporary sluttiness looks like this: {image=gui/heart/red_heart.png}"
                    "Vren" "A girls Temporary Sluttiness will decrease if it is higher than her Core Sluttiness. If Suggestibility is higher than 0 there is a chance for the Temporary sluttiness to turn into Core sluttiness."
                    "Vren" "Suggesibility has another use. It will increase the cap for Temporary sluttiness. Temporary sluttiness looks like this: {image=gui/heart/grey_heart.png}"
                    "Vren" "Interacting with a girl is the most direct way to change their Obedience or Sluttiness. There may also be random events that change their scores."
                    "Vren" "Most actions have a minimum Temporary sluttiness rquirement before they can be attempted and a maximum Temporary sluttiness they will have an effect on."
                    "Vren" "Having sex with a girl is nessesary to increase her sluttiness to the highest levels. Higher arousal will make a girl more willing to strip down or have sex."
                    "Vren" "If you are able to make a girl cum she will immediately start to turn Temporary sluttiness into core sluttiness."
                    "Vren" "As a girls Sluttiness increases she will be more willing to wear revealing clothing or have sex with you."
                    "Vren" "As her Obedience increase she will be more deferential. She may be willing to have sex simply because you ask, even if she is not normally slutty enough."

                "Leveling Up.":
                    "Vren" "There are three main catagories of experience: Stats, Work Skills, and Sex Skills."
                    "Vren" "For each of these catagories you will have a goal assigned. When that goal is completed you will recieve one point to spend on any of the scores in that catagory."
                    "Vren" "Once per day you may also scrap a goal that is overly difficult or not possible to complete yet."
                    "Vren" "When you complete a goal future goals in that catagory will increase in difficulty. Spend your early points wisely!"
                    "Vren" "Some goals are only checked at the end of the day or end of a turn, so if you have a goal that should be completed but is not giving you the option try advancing time."

        "Development Questions.":
            menu:
                "Will there be more character poses?":
                    "Vren" "Absolutely! The current standing poses proved that the rendering workflow for the game is valid, which means I will be able to introduce character poses for different sex positions."
                    "Vren" "Most sex positions have character poses associated with them and new poses will be rendered with each update."

                "Will there be animation?":
                    "Vren" "No, there will not be full animation in the game. There may be small sprite based animations added later, but this will require more experimentation by me before I can commit to it."

                "Why are their holes in some pieces of clothing?":
                    "Vren" "Some character positions cause portions of the character model to poke out of their clothing when I am rendering them."
                    "Vren" "I will be adjusting my render settings and rerendering any clothing items that need it as we go forward."

        "Done.":
            return
    call faq_loop from _call_faq_loop_1
    return

label check_inventory_loop:
    call screen show_serum_inventory(mc.inventory)
    return

label check_business_inventory_loop:
    call screen show_serum_inventory(mc.business.inventory,[mc.business.sale_inventory],["Production Inventory","Waiting to Ship"])
    return

init -2 python:
    def indent(elem, level=0):
        i = "\n" + level*"    "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "    "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def log_outfit(the_outfit, outfit_class = "FullSets", wardrobe_name = "Exported_Wardrobe"):
        file_path = os.path.abspath(os.path.join(config.basedir, "game"))
        file_path = os.path.join(file_path,"wardrobes")
        file_name = os.path.join(file_path, wardrobe_name + ".xml")

        if not os.path.isfile(file_name): #We assume if the file exists that it is well formed. Otherwise we will create it and guarantee it is well formed.
            #Note: if the file is changed (by inserting extra outfits, for example) exporting outfits may crash due to malformed xml, but we do not overwrite the file.
            missing_file = open(file_name,"w+")
            starting_element = ET.Element("Wardrobe",{"name":wardrobe_name})
            starting_tree = ET.ElementTree(starting_element)
            ET.SubElement(starting_element,"FullSets")
            ET.SubElement(starting_element,"UnderwearSets")
            ET.SubElement(starting_element,"OverwearSets")

            indent(starting_element)
            starting_tree.write(file_name,encoding="UTF-8")


        wardrobe_tree = ET.parse(file_name)
        tree_root = wardrobe_tree.getroot()
        outfit_root = tree_root.find(outfit_class)

        outfit_element = ET.SubElement(outfit_root,"Outfit",{"name":the_outfit.name})
        upper_element = ET.SubElement(outfit_element, "UpperBody")
        lower_element = ET.SubElement(outfit_element, "LowerBody")
        feet_element = ET.SubElement(outfit_element, "Feet")
        accessory_element = ET.SubElement(outfit_element, "Accessories")


        for cloth in the_outfit.upper_body:
            item_dict = build_item_dict(cloth)
            if not cloth.is_extension:
                ET.SubElement(upper_element,"Item", item_dict)
        for cloth in the_outfit.lower_body:
            item_dict = build_item_dict(cloth)
            if not cloth.is_extension:
                ET.SubElement(lower_element,"Item", item_dict)
        for cloth in the_outfit.feet:
            item_dict = build_item_dict(cloth)
            if not cloth.is_extension:
                ET.SubElement(feet_element,"Item", item_dict)
        for cloth in the_outfit.accessories:
            item_dict = build_item_dict(cloth)
            if not cloth.is_extension:
                ET.SubElement(accessory_element,"Item", item_dict)


        indent(tree_root)
        wardrobe_tree.write(file_name,encoding="UTF-8")

    def build_item_dict(cloth):
        item_dict = {"name":cloth.proper_name,"red":str(cloth.colour[0]),"green":str(cloth.colour[1]),"blue":str(cloth.colour[2]),"alpha":str(cloth.colour[3])}
        if __builtin__.type(cloth) is Clothing and cloth.pattern is not None:
            item_dict.update({"pattern":cloth.pattern, "pred":str(cloth.colour_pattern[0]), "pgreen":str(cloth.colour_pattern[1]), "pblue":str(cloth.colour_pattern[2]), "palpha":str(cloth.colour_pattern[3])})
        return item_dict

    def log_wardrobe(the_wardrobe, file_name):

        for outfit in the_wardrobe.outfits:
            log_outfit(outfit, outfit_class = "FullSets", wardrobe_name = file_name)

        for outfit in the_wardrobe.underwear_sets:
            log_outfit(outfit, outfit_class = "UnderwearSets", wardrobe_name = file_name)

        for outfit in the_wardrobe.overwear_sets:
            log_outfit(outfit, outfit_class = "OverwearSets", wardrobe_name = file_name)


label outfit_master_manager(*args, **kwargs): #New outfit manager that centralizes exporting, modifying, duplicating, and deleting.
    call screen outfit_select_manager(*args, **kwargs)

    if _return == "No Return":
        return None #We're done and want to leave.

    $ outfit_type = None
    $ outfit = None
    $ slut_limit = kwargs.get("slut_limit", None)
    if _return == "new_full":
        $ outfit_type = "full"
        call screen outfit_creator(Outfit("New Outfit"), outfit_type = outfit_type, slut_limit = slut_limit)
        $ outfit = _return

    elif _return == "new_over":
        $ outfit_type = "over"
        call screen outfit_creator(Outfit("New Overwear Set"), outfit_type = outfit_type, slut_limit = slut_limit)
        $ outfit = _return

    elif _return == "new_under":
        $ outfit_type = "under"
        call screen outfit_creator(Outfit("New Underwear Set"), outfit_type = outfit_type, slut_limit = slut_limit)
        $ outfit = _return


    elif isinstance(_return, list):
        #If we are returning an outfit we should be in one of the three sets (if not: panic!)
        $ command = _return[0]
        $ outfit = _return[1]

        if command == "select":
            return outfit

        elif outfit in mc.designed_wardrobe.outfits:
            $ outfit_type = "full"

        elif outfit in mc.designed_wardrobe.overwear_sets:
            $ outfit_type = "over"

        elif outfit in mc.designed_wardrobe.underwear_sets:
            $ outfit_type = "under"

        else:
            "We couldn't find it anywhere! PANIC!"

        $ mc.designed_wardrobe.remove_outfit(outfit) # Remove it so we can re-add it later. Note that "dupicate" has already copied an outfit and added it so we can re-use this code.

        call screen outfit_creator(outfit, outfit_type = outfit_type, slut_limit = slut_limit)
        $ outfit = _return

    if not outfit == "Not_New":
        $ new_outfit_name = renpy.input("Please name this outfit.", default = outfit.name)
        while new_outfit_name == "":
            $ new_outfit_name = renpy.input("Please enter a non-empty name.", default = outfit.name)


        $ mc.save_design(outfit, new_outfit_name, outfit_type)

    call outfit_master_manager(*args, **kwargs) from _call_outfit_master_manager #Loop around until the player decides they want to leave.
    return _return

label wardrobe_import(): #TODO: Figure out where we want to put this. Might be interesting to embed this at the clothing store as a location option.
    $ list_of_xml_files = []
    # Build a list of all possible files inside of the imports file.
    python:
        file_path = os.path.abspath(os.path.join(config.basedir, "game"))
        file_path = os.path.join(file_path,"wardrobes")
        file_path = os.path.join(file_path,"imports")
        for file_name in os.listdir(file_path):
            if file_name[-4:] == ".xml":
                list_of_xml_files.append((file_name, file_name))

    if not list_of_xml_files:
        "No files found. Place wardrobe XML files inside of games/wardrobes/imports to make them available for importing."
        return

    $ list_of_xml_files.append(("None","None")) #Provide a way to cancel
    "Select a wardrobe file to import:"

    $ chosen_filename = renpy.display_menu(list_of_xml_files) #Get the player to choose a list
    if chosen_filename is "None":
        return

    $ the_wardrobe = wardrobe_from_xml(chosen_filename[:-4], in_import = True)
    $ mc.designed_wardrobe = mc.designed_wardrobe.merge_wardrobes(the_wardrobe, keep_primary_name = True)


    # Some file cleanup so they don't exist in memory for the rest of the game.
    $ list_of_xml_files = []
    $ the_wardrobe = None

    "Wardrobe imported."
    return


label game_loop(): ##THIS IS THE IMPORTANT SECTION WHERE YOU DECIDE WHAT ACTIONS YOU TAKE

    $ people_list = []

    $ people_list.extend(mc.location.people)

    $ actions_list = []




    $ actions_list.append(["Check your phone.", "Phone"])
    $ actions_list.extend(mc.location.get_valid_actions())

    $ people_list.sort(key = sort_display_list, reverse = True)
    $ actions_list.sort(key = sort_display_list, reverse = True)

    $ actions_list.insert(0,["Go somewhere else.", "Travel"])
    if time_of_day == 4:
        if sleep_action not in mc.location.actions: #If they're in a location they can sleep we shouldn't show this because they can just sleep here.
            $ actions_list.insert(0, ["Go home and sleep.{image=gui/heart/Time_Advance.png}{image=gui/heart/Time_Advance.png} (tooltip)It's late. Go home and sleep.", "Wait"])
    else:
        $ actions_list.insert(0, ["Wait here\n{image=gui/heart/Time_Advance.png}, +10 Extra {image=gui/extra_images/energy_token.png} (tooltip)Kill some time and wait around. Recovers more energy than working.", "Wait"])
    $ actions_list.insert(0,"Do Something")
    $ people_list.insert(0,"Talk to Someone")


    call screen main_choice_display([people_list,actions_list])

    $ picked_option = _return
    if isinstance(picked_option, Person):
        $ picked_option.draw_person()
        $ enabled_talk_events = []
        python:
            for possible_talk_event in picked_option.on_talk_event_list:
                if possible_talk_event.is_action_enabled(picked_option):
                    enabled_talk_events.append(possible_talk_event)
        if enabled_talk_events:
            #If there are any events we want to trigger it happens instead of talking to the person. If we want it to lead into talk_person we can call that separately. Only one event per interaction.
            $ talk_action = get_random_from_list(enabled_talk_events)
            $ talk_action.call_action(picked_option)
            if talk_action in picked_option.on_talk_event_list: #This shouldn't come up much, but it an event is double removed this helps us fail gracefully.
                $ picked_option.on_talk_event_list.remove(talk_action)


        else:
            if picked_option.title is None:
                "You decide to approach the stranger and introduce yourself."
            else:
                "You approach [picked_option.title] and chat for a little bit."
                $ picked_option.call_dialogue("greetings")

            if picked_option.has_taboo(["underwear_nudity","bare_tits", "bare_pussy"]) and picked_option.judge_outfit(picked_option.outfit, -30): #If she's in anything close to slutty she's self-concious enough to coment on it.
                if picked_option.outfit.vagina_visible() and picked_option.has_taboo("bare_pussy") and picked_option.outfit.tits_visible() and picked_option.has_taboo("bare_tits"):
                    "[picked_option.title] doesn't say anything about it, but seems unconfortable being naked in front of you."
                    "As you talk she seems to become more comfortable with her own nudity, even if she isn't thrilled by it."

                if picked_option.outfit.vagina_visible() and picked_option.has_taboo("bare_pussy"):
                    "[picked_option.title] doesn't say anything about it, but angles her body to try and conceal her bare pussy from you."
                    "As you talk she seems to become more comfortable, even if she isn't thrilled about it."

                elif picked_option.outfit.tits_visible() and picked_option.has_taboo("bare_tits"):
                    "[picked_option.title] doesn't say anything about it, but brings her arms up to try and conceal her tits."
                    if picked_option.has_large_tits():
                        "Her large chest isn't easy to hide, and she quickly realises it's hopeless."
                    else:
                        "As you talk she seems to become more comfortable, and eventaully lets her arms drop again."

                elif ((picked_option.outfit.wearing_panties() and not picked_option.outfit.panties_covered()) or (picked_option.outfit.wearing_bra() and not picked_option.outfit.bra_covered())) and picked_option.has_taboo("underwear_nudity"):
                    "[picked_option.title] doesn't say anything about it, but she tries to cover up her underwear with her hands."
                    "As you talk she seems to become more comfortable, and eventually she lets her arms drop to her sides."

                $ picked_option.update_outfit_taboos()
            call talk_person(picked_option) from _call_talk_person

    elif isinstance(picked_option, Action):
        $ picked_option.call_action()


    elif picked_option == "Travel":
        call screen map_manager
        $ new_location = _return
        call change_location(new_location) from _call_change_location #_return is the location returned from the map manager.
        if new_location.people: #There are people in the room, let's see if there are any room events
            $ enabled_room_events = []
            python: #Scan through all the people and...
                for a_person in new_location.people:
                    for possible_room_event in a_person.on_room_enter_event_list:
                        if possible_room_event.is_action_enabled(a_person): #See what events the are enabled...
                            enabled_room_events.append([a_person, possible_room_event]) #Then keep track of the person so we know who to remove it from if it triggers.

            if enabled_room_events: #If there are room events to take care of run those right now.
                $ picked_event = get_random_from_list(enabled_room_events)
                $ picked_event[0].on_room_enter_event_list.remove(picked_event[1]) #Remove the event from their list since we will be running it.
                $ picked_event[1].call_action(picked_event[0]) #Run the action with the person as an extra argument.

            elif new_location in [mc.business.m_div, mc.business.p_div, mc.business.r_div, mc.business.s_div, mc.business.h_div]: #There are no room events, so generate a quick room greeting from an employee if one is around.
                $ possible_greetings = []
                python:
                    for a_person in new_location.people:
                        if mc.business.get_employee_title(a_person) != "None":
                            possible_greetings.append(a_person)
                $ the_greeter = get_random_from_list(possible_greetings)
                if the_greeter:
                    $ the_greeter.draw_person()
                    $ the_greeter.call_dialogue("work_enter_greeting")
                    $ clear_scene()

    elif picked_option == "Phone":
        call browse_internet() from _call_browse_internet

    elif picked_option == "Wait":
        if time_of_day == 4:
            $ mc.change_location(bedroom)
        else:
            $ mc.change_energy(10) #Extra 10 energy gain if you spend your time waiting around
        call advance_time from _call_advance_time_15
        $ mc.location.show_background() #Redraw the background in case it has changed due to the new time.

    jump game_loop



label change_location(the_place):
    $ renpy.scene()
    $ the_place.show_background()
    if the_place.trigger_tutorial and the_place.tutorial_label is not None and mc.business.event_triggers_dict.get("Tutorial_Section",False):
        $ the_place.trigger_tutorial = False
        $ renpy.call(the_place.tutorial_label)

    return

label talk_person(the_person):
    $ mc.having_text_conversation = None #Just in case some event hasn't properly reset this.
    # $ the_person.draw_person() #Removed v0.28.1, this was often called when no character change was required. Character draw should be handled by events that lead into this label if required.
    if the_person.title is None:
        call person_introduction(the_person) from _call_person_introduction #If their title is none we assume it is because we have never met them before. We have a special introduction scene for new people.
        #Once that's done we continue to talk to the person.




    $ small_talk_action = Action("Make small talk.\n-15 {image=gui/extra_images/energy_token.png}", requirement = small_talk_requirement, effect = "small_talk_person", args=the_person, requirement_args=the_person,
        menu_tooltip = "A pleasant chat about your likes and dislikes. A good way to get to know someone and the first step to building a lasting relationship. Provides a chance to study the effects of active serum traits and raise their mastery level.")
    $ compliment_action = Action("Compliment her.\n-15 {image=gui/extra_images/energy_token.png}", requirement = compliment_requirement, effect = "compliment_person", args=the_person, requirement_args=the_person,
        menu_tooltip = "Lay the charm on thick and heavy. A great way to build a relationship, and every girl is happy to recieve a compliment! Provides a chance to study the effects of active serum traits and raise their mastery level.")
    $ flirt_action = Action("Flirt with her.\n-15 {image=gui/extra_images/energy_token.png}", requirement = flirt_requirement, effect = "flirt_person", args=the_person, requirement_args=the_person,
        menu_tooltip = "A conversation filled with innuendo and double entendre. Both improves your relationship with a girl and helps make her a little bit sluttier. Provides a chance to study the effects of active serum traits and raise their mastery level.")
    $ date_action = Action("Ask her on a date.", requirement = date_option_requirement, effect = "date_person", args=the_person, requirement_args=the_person,
        menu_tooltip = "Ask her out on a date. The more you impress her the closer you'll grow. Play your cards right and you might end up back at her place.")
    $ make_girlfriend_action = Action("Ask her to be your girlfriend.", requirement = ask_girlfriend_requirement, effect = "ask_be_girlfriend_label", args = the_person, requirement_args = the_person,
        menu_tooltip = "Ask her to start an official, steady relationship and be your girlfriend.", priority = 10)
    $ bc_talk_action = Action("Talk about her birth control.", requirement = bc_talk_requirement, effect = "bc_talk_label", args = the_person, requirement_args = the_person,
        menu_tooltip = "Talk to her about her use of birth control. Ask her to start or stop taking it, or just check what she's currently doing.")
    $ chat_list = [small_talk_action, compliment_action, flirt_action, date_action, make_girlfriend_action, bc_talk_action]

    $ grope_action = Action("Grope her.\n-5 {image=gui/extra_images/energy_token.png}", requirement = grope_requirement, effect = "grope_person", args = the_person, requirement_args = the_person,
        menu_tooltip = "Be \"friendly\" and see how far she is willing to let you take things. May make her more comfortable with physical contact, but at the cost of her opinion of you.")

    $ command_action = Action("Give her a command.", requirement = command_requirement, effect = "command_person", args = the_person, requirement_args = the_person,
        menu_tooltip = "Leverage her obedience and command her to do something.")

    $ specific_action_list = ["Say goodbye.", command_action, grope_action]

    python:
        special_role_actions = []
        roles_that_need_people_args = []
        for role in the_person.special_role:
            for act in role.actions:
                special_role_actions.append([act,the_person]) #They're a list of actions and their extra arg so that gets passed through properly.
                roles_that_need_people_args.append(act) #All role actions need to be passed the specific person, so we keep a list of these actions here and check it below.

        for act in mc.main_character_actions: #The main character has a "role" that lets us add special actions as well.
            special_role_actions.append([act,the_person])
            roles_that_need_people_args.append(act)

        chat_list.sort(key = sort_display_list, reverse = True)
        chat_list.insert(0,"Chat with her")

        specific_action_list.sort(key = sort_display_list, reverse = True)
        specific_action_list.insert(0,"Do something specific")

        special_role_actions.sort(key = sort_display_list, reverse = True)
        special_role_actions.insert(0,"Special Actions")

    call screen main_choice_display([chat_list, specific_action_list, special_role_actions])

    if isinstance(_return, Action):
        $ starting_time_of_day = time_of_day
        if _return in roles_that_need_people_args:
            $ _return.call_action(the_person)
        else:
            $ _return.call_action()

        if the_person in mc.location.people and time_of_day == starting_time_of_day:
            call talk_person(the_person) from _call_talk_person_1 #If we're in the same place and time hasn't advanced keep talking to them until we stop talking on purpose.

    $ clear_scene()
    return


label examine_room(the_room):
    python:
        renpy.say("","You are at [the_room.name].") #Where are we right now?

        people_here = the_room.people #Format the names of people in the room with you so it looks nice.
        if len(people_here) == 0:
            room_names = "There's nobody else in the room with you."
        elif len(people_here) == 1:
            room_names = "The only other person in the room with you is "
            room_names += people_here[0].name
            room_names += "."
        elif len(people_here) == 2:
            room_names = "Inside the room you see "
            room_names += people_here[0].name
            room_names += " and "
            room_names += people_here[1].name
            room_names += "."
        elif len(people_here) >2 and len(people_here) < 6:
            room_names = "Inside the room you see "
            for person in people_here[0:len(people_here)-2]:
                room_names += person.name
                room_names += ", "
            last_person = people_here[len(people_here)-1].name
            room_names += "and "
            room_names += last_person
            room_names += " among other people."
        else:
            room_names = "The room is filled with people."

        renpy.say("",room_names) ##This is the actual print statement!!

        connections_here = the_room.connections # Now we format the output for the connections so that it is readable.
        if len(connections_here) == 0:
            connect_names = "There are no exits from here. You're trapped!" #Shouldn't ever happen, hopefully."
        elif len(connections_here) == 1:
            connect_names = "From here your only option is to head to "
            connect_names += connections_here[0].name
            connect_names += "."
        elif len(connections_here) == 2:
            connect_names = "From here you can head to either "
            connect_names += connections_here[0].name
            connect_names += " or "
            connect_names += connections_here[1].name
            connect_names += "."
        else:
            connect_names = "From here you can go to "
            for place in connections_here[0:len(connections_here)-1]:
                connect_names += place.name
                connect_names += ", "
            last_place = connections_here[len(connections_here)-1].name
            connect_names += "and "
            connect_names += last_place
            connect_names += "."
        renpy.say("",connect_names) ##This is the actual print statement!!

    "That's all there is to see nearby."

    return

label examine_person(the_person):
    #Take a close look and figure out their physical attributes (tit size, ass size?, hair colour, hair style)

    python:
        string = "She has " + the_person.skin + " coloured skin, along with " + the_person.hair_colour[0] + " coloured hair and pretty " + the_person.eyes[0] + " coloured eyes. She stands " + height_to_string(the_person.height) + " tall."
        renpy.say("",string)

        outfit_top = the_person.outfit.get_upper_visible()
        outfit_bottom = the_person.outfit.get_lower_visible()
        string = ""

        if len(outfit_top) == 0: ##ie. is naked
            string += "She's wearing nothing at all on top, with her nice " + the_person.tits + " sized tits on display for you."
        elif len(outfit_top) == 1:
            string += "She's wearing a " + outfit_top[0].name + " with her nice " + the_person.tits + " sized tits underneath."
        elif len(outfit_top) == 2:
            string += "She's wearing a " + outfit_top[1].name + " with a " + outfit_top[0].name + " underneath. Her tits look like they're " + the_person.tits + "'s."
        elif len(outfit_top) == 3:
            string += "She's wearing a " + outfit_top[2].name + " with a " + outfit_top[1].name + " and " + outfit_top[0].name + " underneath. Her tits look like they're " + the_person.tits + "'s."
        renpy.say("",string)

        string = ""
        if len(outfit_bottom) == 0: #naked
            string += "Her legs are completely bare, and you have a clear view of her pussy."
        elif len(outfit_bottom) == 1:
            string += "She's also wearing " + outfit_bottom[0].name + " below."
            if not outfit_bottom[0].hide_below:
                string += " You can see her pussy underneath."
        elif len(outfit_bottom) == 2:
            string += "She's also wearing " + outfit_bottom[0].name + " below, with " + outfit_bottom[1].name +  " visible below."
            if not outfit_bottom[1].hide_below:
                string += " You can see her pussy underneath."
        renpy.say("",string)
        title = mc.business.get_employee_title(the_person)
        if title == "Researcher":
            renpy.say("", the_person.title + " currently works in your research department.")
        elif title == "Marketing":
            renpy.say("", the_person.title + " currently works in your marketing department.")
        elif title == "Supply":
            renpy.say("", the_person.title + " currently works in your supply procurement department.")
        elif title == "Production":
            renpy.say("", the_person.title + " currently works in your production department.")
        elif title == "Human Resources":
            renpy.say("", the_person.title + " currently works in your human resources department.")
        else:
            renpy.say("", the_person.title + " does not currently work for you.")

    return

label give_serum(the_person):
    call screen serum_inventory_select_ui(mc.inventory)
    if not _return == "None":
        $ the_serum = _return
        "You decide to give [the_person.title] a dose of [the_serum.name]."
        $ mc.inventory.change_serum(the_serum,-1)
        $ the_person.give_serum(copy.copy(the_serum)) #use a copy rather than the main class, so we can modify and delete the effects without changing anything else.
        return the_serum
    else:
        "You decide not to give [the_person.title] anything."
        return False

label sleep_action_description: #REMEMBER TO UPDATE THE SLEEP QUICK BUTTON ON THE MAIN UI, IT DOES NOT TOUCH THIS FUNCTION IN ANY WAY!
    "You go to bed after a hard days work."
    call advance_time from _call_advance_time
    return

label faq_action_description:
    call faq_loop from _call_faq_loop_2
    return

label hr_work_action_description:
    $ mc.business.player_hr()
    call advance_time from _call_advance_time_1
    return

label research_work_action_description:
    $ mc.business.player_research()
    call advance_time from _call_advance_time_2
    return

label supplies_work_action_description:
    $ mc.business.player_buy_supplies()
    call advance_time from _call_advance_time_3
    return

label market_work_action_description:
    $ mc.business.player_market()
    call advance_time from _call_advance_time_4

    return

label production_work_action_description:
    $ mc.business.player_production()
    call advance_time from _call_advance_time_5
    return

label interview_action_description:
    $ count = 3 #Num of people to generate, by default is 3. Changed with some policies
    if recruitment_batch_three_policy.is_active():
        $ count = 10
    elif recruitment_batch_two_policy.is_active():
        $ count = 6
    elif recruitment_batch_one_policy.is_active():
        $ count = 4

    $ interview_cost = 50
    "Bringing in [count] people for an interview will cost $[interview_cost]. Do you want to spend time interviewing potential employees?"
    menu:
        "Yes, I'll pay the cost. -$[interview_cost]":
            $ mc.business.funds += -interview_cost
            $ clear_scene()
            $ renpy.free_memory() #Try and free available memory
            python: #Build our list of candidates with our proper recruitment requirements
                candidates = []

                for x in range(0,count+1): #NOTE: count is given +1 because the screen tries to pre-calculate the result of button presses. This leads to index out-of-bounds, unless we pad it with an extra character (who will not be reached).
                    candidates.append(make_person())

                reveal_count = 0
                reveal_sex = False
                if recruitment_knowledge_one_policy.is_active():
                    reveal_count += 2
                if recruitment_knowledge_two_policy.is_active():
                    reveal_count += 2
                if recruitment_knowledge_three_policy.is_active():
                    reveal_count += 1
                    reveal_sex = True
                if recruitment_knowledge_four_policy.is_active():
                    reveal_count += 1
                for a_candidate in candidates:
                    for x in __builtin__.range(0,reveal_count): #Reveal all of their opinions based on our policies.
                        a_candidate.discover_opinion(a_candidate.get_random_opinion(include_known = False, include_sexy = reveal_sex),add_to_log = False) #Get a random opinion and reveal it.
            call hire_select_process(candidates) from _call_hire_select_process
            $ candidates = [] #Prevent it from using up extra memory
            $ renpy.free_memory() #Try and force a clean up of unused memory.

            if not _return == "None":
                $ new_person = _return
                $ new_person.generate_home() #Generate them a home location so they have somewhere to go at night.
                call hire_someone(new_person, add_to_location = True) from _call_hire_someone #
                $ new_person.set_title(get_random_title(new_person))
                $ new_person.set_possessive_title(get_random_possessive_title(new_person))
                $ new_person.set_mc_title(get_random_player_title(new_person))
            else:
                "You decide against hiring anyone new for now."
            call advance_time from _call_advance_time_6
        "Nevermind.":
            pass
    return

label hire_select_process(candidates):
    hide screen main_ui #NOTE: We have to hide all of these screens because we are using a fake (aka. non-screen) background for this. We're doing that so we can use the normal draw_person call for them.
    hide screen phone_hud_ui
    hide screen business_ui
    hide screen goal_hud_ui
    $ show_candidate(candidates[0]) #Show the first candidate, updates are taken care of by actions within the screen.
    show bg paper_menu_background #Show a paper background for this scene.
    $ count = __builtin__.len(candidates)-1
    call screen interview_ui(candidates,count)
    $ renpy.scene()
    show screen phone_hud_ui
    show screen business_ui
    show screen goal_hud_ui
    show screen main_ui
    $ clear_scene()
    $ mc.location.show_background()

    return _return


label hire_someone(new_person, add_to_location = False): # Breaks out some of the functionality of hiring someone into an independent lable.
    python:
        new_person.event_triggers_dict["employed_since"] = day
        mc.business.listener_system.fire_event("new_hire", the_person = new_person)
        new_person.add_role(employee_role)
        for other_employee in mc.business.get_employee_list():
            town_relationships.begin_relationship(new_person, other_employee) #They are introduced to everyone at work, with a starting value of "Acquaintance"

    "You complete the nessesary paperwork and hire [_return.name]. What division do you assign them to?"
    menu:
        "Research and Development.":
            $ mc.business.add_employee_research(new_person)
            $ new_person.set_work(mc.business.r_div)
            if add_to_location:
                $ mc.business.r_div.add_person(new_person)

        "Production.":
            $ mc.business.add_employee_production(new_person)
            $ new_person.set_work(mc.business.p_div)
            if add_to_location:
                $ mc.business.p_div.add_person(new_person)

        "Supply Procurement.":
            $ mc.business.add_employee_supply(new_person)
            $ new_person.set_work(mc.business.s_div)
            if add_to_location:
                $ mc.business.s_div.add_person(new_person)

        "Marketing.":
            $ mc.business.add_employee_marketing(new_person)
            $ new_person.set_work(mc.business.m_div)
            if add_to_location:
                $ mc.business.m_div.add_person(new_person)

        "Human Resources.":
            $ mc.business.add_employee_hr(new_person)
            $ new_person.set_work(mc.business.h_div)
            if add_to_location:
                $ mc.business.h_div.add_person(new_person)




    return

label serum_design_action_description:
    $counter = len(list_of_traits)
    hide screen main_ui
    hide screen phone_hud_ui
    hide screen business_ui
    call screen serum_design_ui(SerumDesign(),[]) #This will return the final serum design, or None if the player backs out.
    $ my_return_serum = _return

    show screen phone_hud_ui
    show screen business_ui
    show screen main_ui
    if not my_return_serum == "None":
        $ name = renpy.input("Please give this serum design a name.")
        $ my_return_serum.name = name
        $ mc.business.add_serum_design(my_return_serum)
        $ mc.business.listener_system.fire_event("new_serum", the_serum = my_return_serum)
        call advance_time from _call_advance_time_7
    else:
        "You decide not to spend any time designing a new serum type."
    return

label research_select_action_description:
    hide screen main_ui
    hide screen phone_hud_ui
    hide screen business_ui
    call screen serum_select_ui
    show screen phone_hud_ui
    show screen business_ui
    show screen main_ui
    if not _return == "None":
        $mc.business.set_serum_research(_return)
        "You change your research to [_return.name]."
    else:
        "You decide to leave your labs current research topic as it is."
    return

label production_select_action_description: #TODO: Change this to allow you to select which line of serum you are changing!
    hide screen main_ui
    hide screen phone_hud_ui
    hide screen business_ui
    call screen serum_production_select_ui
    show screen phone_hud_ui
    show screen business_ui
    show screen main_ui
    return

label trade_serum_action_description:
    "You step into the stock room to check what you currently have produced."
    hide screen main_ui
    hide screen phone_hud_ui
    hide screen business_ui
    $ renpy.block_rollback()
    call screen serum_trade_ui(mc.inventory,mc.business.inventory)
    $ renpy.block_rollback()
    show screen phone_hud_ui
    show screen business_ui
    show screen main_ui
    return

label sell_serum_action_description:
    "You look through your stock of serum, marking some to be sold by your marketing team."
    hide screen main_ui
    hide screen phone_hud_ui
    hide screen business_ui
    $ renpy.block_rollback()
    call screen serum_trade_ui(mc.business.inventory,mc.business.sale_inventory,"Production Stockpile","Sales Stockpile")
    $ renpy.block_rollback()

    show screen phone_hud_ui
    show screen business_ui
    show screen main_ui
    return

label review_designs_action_description:
    hide screen main_ui
    hide screen phone_hud_ui
    hide screen business_ui
    $ renpy.block_rollback() #Block rollback to prevent any strange issues with references being lost.
    call screen review_designs_screen()
    $ renpy.block_rollback()

    show screen phone_hud_ui
    show screen business_ui
    show screen main_ui
    return


label pick_supply_goal_action_description:
    $ amount = renpy.input("How many units of serum supply would you like your supply procurement team to keep stocked?")
    $ amount = amount.strip()

    while not amount.isdigit():
        $ amount = renpy.input("Please put in an integer value.")

    $ amount = int(amount)
    $ mc.business.supply_goal = amount
    if amount <= 0:
        "You tell your team to keep [amount] units of serum supply stocked. They question your sanity, but otherwise continue with their work. Perhaps you should use a positive number."
    else:
        "You tell your team to keep [amount] units of serum supply stocked."

    return

label policy_purchase_description:
    call screen policy_selection_screen_v2() #policy_selection_screen
    return

label head_researcher_select_description:
    call screen employee_overview(white_list = mc.business.research_team, person_select = True)
    $ new_head = _return
    $ mc.business.head_researcher = new_head
    $ new_head.add_role(head_researcher)
    return

label pick_company_model_description:
    call screen employee_overview(person_select = True)
    $ new_model = _return
    if new_model is not None:
        $ mc.business.company_model = new_model
        $ new_model.add_role(company_model_role)
    return

label set_uniform_description:
    #First, establish the maximums the uniform can reach.
    $ slut_limit, underwear_limit, limited_to_top = mc.business.get_uniform_limits() #Function generates all uniform related limits to keep them consistent between events and active/deavtive policies.


    #Some quick holding variables to store the options picked.
    $ selected_div = None
    $ uniform_mode = None
    $ uniform_type = None
    menu:
        "Add a complete outfit." if not limited_to_top:
            $ uniform_mode = "full"

        "Add a complete outfit.\n{size=22}Requires: Reduced Coverage Corporate Uniforms{/size} (disabled)" if limited_to_top:
            pass

        "Add an overwear set.":
            $ uniform_mode = "over"

        "Add an underwear set." if not limited_to_top:
            $ uniform_mode = "under"

        "Add an underwear set.\n{size=22}Requires: Reduced Coverage Corporate Uniforms{/size} (disabled)" if limited_to_top:
            pass

        "Remove a uniform or set.":
            $ uniform_mode = "delete"


    menu:
        "Company Wide Uniforms.\n{size=22}Can be worn by everyone.{/size}": #Get the wardrobe we are going to be modifying.
            $ selected_div = mc.business.all_uniform

        "R&D Uniforms.":
            $ selected_div = mc.business.r_uniform

        "Production Uniforms.":
            $ selected_div = mc.business.p_uniform

        "Supply Procurement Uniforms.":
            $ selected_div = mc.business.s_uniform

        "Marketing Uniforms.":
            $ selected_div = mc.business.m_uniform

        "Human Resources Uniforms.":
            $ selected_div = mc.business.h_uniform

    if uniform_mode == "delete":
        call screen outfit_delete_manager(selected_div) #Calls the wardrobe screen and lets teh player delete whatever they want.

    else:
        if uniform_mode == "full":
            call outfit_master_manager(slut_limit = slut_limit) from _call_outfit_master_manager_3
            $ new_outfit = _return
            if new_outfit is None:
                return


            $ mc.business.listener_system.fire_event("add_uniform", the_outfit = new_outfit, the_type = "full")
            $ selected_div.add_outfit(new_outfit.get_copy())

        elif uniform_mode == "under":
            call outfit_master_manager(slut_limit = underwear_limit, show_outfits = False, show_underwear = True, show_overwear = False) from _call_outfit_master_manager_4
            $ new_outfit = _return
            if new_outfit is None:
                return

            $ mc.business.listener_system.fire_event("add_uniform", the_outfit = new_outfit, the_type = "under")
            $ selected_div.add_underwear_set(new_outfit.get_copy())

        else: #uniform_mode == "over":
            call outfit_master_manager(slut_limit = slut_limit, show_outfits = False, show_underwear = False, show_overwear = True) from _call_outfit_master_manager_5
            $ new_outfit = _return
            if new_outfit is None:
                return

            $ mc.business.listener_system.fire_event("add_uniform", the_outfit = new_outfit, the_type = "over")
            $ selected_div.add_overwear_set(new_outfit.get_copy())


    return

label set_serum_description: #TODO: Add a special screen for all of this instead of doing it through menus
    "Which divisions would you like to set a daily serum for?"
    $ selected_div = None
    $ selected_serum = None

    menu:
        "All.":
            $ selected_div = "All"

        "Research and Development.":
            $ selected_div = "R"

        "Production.":
            $ selected_div = "P"

        "Supply Procurement.":
            $ selected_div = "S"

        "Marketing.":
            $ selected_div = "M"

        "Human Resources.":
            $ selected_div = "H"

    menu:
        "Pick a new serum.":
            call screen serum_inventory_select_ui(mc.business.inventory)
            $ selected_serum = _return

        "Clear existing serum.":
            $ selected_serum = None

    if selected_serum == "None": #IF we didn't select an actual serum, just return and don't chagne anything.
        return

    if selected_div == "All":
        $ mc.business.m_serum = selected_serum
        $ mc.business.p_serum = selected_serum
        $ mc.business.r_serum = selected_serum
        $ mc.business.s_serum = selected_serum
        $ mc.business.h_serum = selected_serum

    elif selected_div == "R":
        $ mc.business.r_serum = selected_serum

    elif selected_div == "P":
        $ mc.business.p_serum = selected_serum

    elif selected_div == "S":
        $ mc.business.s_serum = selected_serum

    elif selected_div == "M":
        $ mc.business.m_serum = selected_serum

    elif selected_div == "H":
        $ mc.business.h_serum = selected_serum

    return

label advance_time:
    # 1) Turns are processed _before_ the time is advanced.
    # 1a) crises are processed if they are triggered.
    # 2) Time is advanced, day is advanced if required.
    # 3) People go to their next intended location.
    # Then: Add research crisis when serum is finished, requiring additional input from the player and giving the chance to test a serum on the R&D staff.

    #$mc.can_skip_time = False #Ensure the player cannot skip time during crises.

    $ mandatory_advance_time = False #If a crisis returns an "Advance Time" value once this turn is finished processing it will process ANOTHER turn, so a crisis can require a turn to pass.

    python:
        people_to_process = [] #This is a master list of turns of need to process, stored as tuples [character,location]. Used to avoid modifying a list while we iterate over it, and to avoid repeat movements.
        for place in list_of_places:
            for people in place.people:
                people_to_process.append([people,place])

    python:
        for (people,place) in people_to_process: #Run the results of people spending their turn in their current location.
            people.run_turn()

        mc.business.run_turn()
        mc.run_turn()


    #We make sure that all mandatory crises are run here. Mandatory crises always trigger as soon as they are able, possibly with multiple crises triggering in a single turn.
    $ count = 0
    $ max = len(mc.business.mandatory_crises_list)
    $ clear_list = []
    while count < max: #We need to keep this in a renpy loop, because a return call will always return to the end of an entire python block.
        $crisis = mc.business.mandatory_crises_list[count]
        if crisis.is_action_enabled():
            $ crisis.call_action()
            if _return == "Advance Time":
                $ mandatory_advance_time = True
            $ clear_scene()
            $ clear_list.append(crisis)
        $ count += 1
    $ mc.location.show_background()
    python: #Needs to be a different python block, otherwise the rest of the block is not called when the action returns.
        for crisis in clear_list:
            mc.business.mandatory_crises_list.remove(crisis) #Clean up the list.


    #Once mandatory crises are managed we may or may not run a random crisis to keep things interesting.
    if renpy.random.randint(0,100) < 10: #ie. run a crisis 10% of the time.
        python:
            possible_crisis_list = []
            for crisis in crisis_list:
                if crisis[0].is_action_enabled(): #Get the first element of the weighted tuple, the action.
                    possible_crisis_list.append(crisis) #Build a list of valid crises from ones that pass their requirement.

        $ the_crisis = get_random_from_weighted_list(possible_crisis_list)
        if the_crisis:
            $ the_crisis.call_action()
            if _return == "Advance Time":
                $ mandatory_advance_time = True

    $ clear_scene()
    $ renpy.scene()
    $ mc.location.show_background()
    show screen business_ui

    if time_of_day == 4: ##First, determine if we're going into the next chunk of time. If we are, advance the day and run all of the end of day code.
        python:
            for (people,place) in people_to_process:
                people.run_day()

        $ mc.run_day()
        $ mc.business.run_day()

        $ time_of_day = 0
        $ day += 1

        if mc.business.funds < 0:
            $ mc.business.bankrupt_days += 1
            if mc.business.bankrupt_days == mc.business.max_bankrupt_days:
                $ renpy.say("","With no funds to pay your creditors you are forced to close your business and auction off all of your materials at a fraction of their value. Your story ends here.")
                $ renpy.full_restart()
            else:
                $ days_remaining = mc.business.max_bankrupt_days-mc.business.bankrupt_days
                $ renpy.say("","Warning! Your company is losing money and unable to pay salaries or purchase necessary supplies!")
                $ renpy.say("","You have [days_remaining] days to restore yourself to positive funds or the bank will reclaim the business!")
        else:
            $ mc.business.bankrupt_days = 0

        call screen end_of_day_update() # We have to keep this outside of a python block, because the renpy.call_screen function does not properly fade out the text bar.
        $ mc.business.clear_messages()

        #Now we run mandatory morning crises. Nearly identical to normal crises, but these always trigger at the start of the day (ie when you wake up and before you have control of your character.)
        $ count = 0
        $ max = len(mc.business.mandatory_morning_crises_list)
        $ clear_list = []
        while count < max: #We need to keep this in a renpy loop, because a return call will always return to the end of an entire python block.
            $crisis = mc.business.mandatory_morning_crises_list[count]
            if crisis.is_action_enabled():
                $ crisis.call_action()
                if _return == "Advance Time":
                    $ mandatory_advance_time = True
                $ clear_scene()
                $ clear_list.append(crisis)
            $ count += 1
        $ mc.location.show_background()
        python: #Needs to be a different python block, otherwise the rest of the block is not called when the action returns.
            for crisis in clear_list:
                mc.business.mandatory_morning_crises_list.remove(crisis) #Clean up the list.


        if renpy.random.randint(0,100) < 15: # We run morning crises 5% of all mornings
            python:
                possible_morning_crises = []
                for crisis in morning_crisis_list:
                    if crisis[0].is_action_enabled(): #Get the first element of the weighted tuple, the action.
                        possible_morning_crises.append(crisis) #Build a list of valid crises from ones that pass their requirement.
            $ the_morning_crisis = get_random_from_weighted_list(possible_morning_crises)
            if the_morning_crisis:
                $ the_morning_crisis.call_action()
                if _return == "Advance Time":
                    $ mandatory_advance_time = True

        $ renpy.free_memory()

    else:
        $ time_of_day += 1 ##Otherwise, just run the end of day code.

    python:
        for (people,place) in people_to_process: #Now move everyone to where the should be in the next time chunk. That may be home, work, etc.
            people.run_move(place)

            if people.title is not None: #We don't assign events to people we haven't met.
                if renpy.random.randint(0,100) < 15: #Only assign one to 15% of people, to cut down on the number of people we're checking.
                    possible_crisis_list = []
                    for crisis in limited_time_event_pool:
                        if crisis[0].is_action_enabled(people): #Get the first element of the weighted tuple, the action.
                            possible_crisis_list.append(crisis) #Build a list of valid crises from ones that pass their requirement.

                    the_crisis = get_random_from_weighted_list(possible_crisis_list, return_everything = True)
                    if the_crisis is not None:
                        limited_time_event = Limited_Time_Action(the_crisis[0], the_crisis[0].event_duration) #Wraps the action so that we can have an instanced duration counter and add/remove it easily.\
                        #renpy.notify("Created event: " + the_crisis[0].name + " for " + people.name)
                        if the_crisis[2] == "on_talk":
                            people.on_talk_event_list.append(limited_time_event)

                        elif the_crisis[2] == "on_enter":
                            people.on_room_enter_event_list.append(limited_time_event)

    $ mc.business.run_move() # In each phase it runs people->MC->Business. Policy effects are run as part of the business, and so can overwrite/alter things an employee has done (like wear their uniform)


    $ mc.location.show_background()
    if mandatory_advance_time: #If a crisis has told us to advance time after it we do so.
        call advance_time from _call_advance_time_28

    $ people_to_process = [] #Clears the memory used here.
    return


label create_test_variables(character_name,business_name,last_name,stat_array,skill_array,_sex_array,max_num_of_random=4): #Gets all of the variables ready. TODO: Move some of this stuff to an init block?

    $ list_of_traits = [] #List of serum traits that can be used. Established here so they play nice with rollback, saving, etc.
    $ list_of_nora_traits = []
    $ list_of_side_effects = [] #List of special serum traits that are reserved for bad results.

    call instantiate_serum_traits() from _call_instantiate_serum_traits #Creates all of the default LR2 serum traits. TODO: Create a mod loading list that has labels that can be externally added and called here.
    call instantiate_side_effect_traits() from _call_instantiate_side_effect_traits

    python:

        list_of_places = [] #By having this in an init block it may be set to null each time the game is reloaded, because the initialization stuff below is only called once.

        ##Actions##
        hr_work_action = Action("Organize your business.\n{image=gui/heart/Time_Advance.png}",hr_work_action_requirement,"hr_work_action_description",
            menu_tooltip = "Raise business efficency, which drops over time based on how many employees the business has.\n+3*Charisma + 2*Skill + 1*Intelligence + 5 Efficency.")
        research_work_action = Action("Research in the lab.\n{image=gui/heart/Time_Advance.png}",research_work_action_requirement,"research_work_action_description",
            menu_tooltip = "Contribute research points towards the currently selected project.\n+3*Intelligence + 2*Skill + 1*Focus + 10 Research Points.")
        supplies_work_action = Action("Order Supplies.\n{image=gui/heart/Time_Advance.png}",supplies_work_action_requirement,"supplies_work_action_description",
            menu_tooltip = "Purchase serum supply at the cost of $1 per unit of supplies. When producing serum every production point requires one unit of serum.\n+3*Focus + 2*Skill + 1*Charisma + 10 Serum Supply.")
        market_work_action = Action("Sell Prepared Serums.\n{image=gui/heart/Time_Advance.png}",market_work_action_requirement,"market_work_action_description",
            menu_tooltip = "Sell serums that have been marked for sale. Mark serum manually from your office or set an autosell threshold in production.\n3*Charisma + 2*Skill + 1*Focus + 5 Serum Doses Sold.")
        production_work_action = Action("Produce serum.\n{image=gui/heart/Time_Advance.png}",production_work_action_requirement,"production_work_action_description",
            menu_tooltip = "Produce serum from raw materials. Each production point of serum requires one unit if supply, which can be purchased from your office.\n+3*Focus + 2*Skill + 1*Intelligence + 10 Production Points.")

        interview_action = Action("Hire someone new.\n{image=gui/heart/Time_Advance.png}", interview_action_requirement,"interview_action_description",
            menu_tooltip = "Look through the resumes of several candidates. More information about a candidate can be revealed by purchasing new business policies.")
        design_serum_action = Action("Create a new serum design.\n{image=gui/heart/Time_Advance.png}", serum_design_action_requirement,"serum_design_action_description",
            menu_tooltip = "Combine serum traits to create a new design. Once a design has been created it must be researched before it can be put into production.")
        pick_research_action = Action("Assign Research Project.", research_select_action_requirement,"research_select_action_description",
            menu_tooltip = "Pick the next research topic for your R&D division. Serum designs must be researched before they can be put into production.")
        pick_production_action = Action("Set production settings.", production_select_action_requirement,"production_select_action_description",
            menu_tooltip = "Decide what serum designs are being produced. Production is divided between multiple factory lines, and auto sell thresholds can be set to automatically flag serum for sale.")
        pick_supply_goal_action = Action("Set the amount of supply you would like to maintain.", pick_supply_goal_action_requirement,"pick_supply_goal_action_description",
            menu_tooltip = "Set a maximum amount of serum you and your staff will attempt to purchase.")
        policy_purhase_action = Action("Manage business policies.", policy_purchase_requirement,"policy_purchase_description",
            menu_tooltip = "New business policies changes the way your company runs and expands your control over it. Once purchased business policies are always active.")
        set_head_researcher_action = Action("Select a Head Researcher.", head_researcher_select_requirement, "head_researcher_select_description",
            menu_tooltip = "Pick a member of your R&D staff to be your head researcher. A head resercher with a high intelligence score will increase the amount of research produced by the entire division.")

        trade_serum_action = Action("Access production stockpile.", trade_serum_action_requirement, "trade_serum_action_description",
            menu_tooltip = "Move serum to and from your personal inventory. You can only use serum you are carrying with you.")
        sell_serum_action = Action("Mark serum to be sold.", sell_serum_action_requirement, "sell_serum_action_description",
            menu_tooltip = "Decide what serum should be available for sale. It can then be sold from the marketing division. Setting an autosell threshold in the production department can do this automatically.")
        review_designs_action = Action("Review serum designs.", review_designs_action_requirement, "review_designs_action_description",
            menu_tooltip = "Shows all existing serum designs and allows you to delete any you no longer desire.")

        set_company_model_action = Action("Pick a company model.", pick_company_model_requirement, "pick_company_model_description",
            menu_tooltip = "Pick one your employees to be your company model. You can run ad campaigns with your model, increasing the value of every dose of serum sold.")

        sleep_action = Action("Go to sleep for the night.\n{image=gui/heart/Time_Advance.png}{image=gui/heart/Time_Advance.png}",sleep_action_requirement,"sleep_action_description",
            menu_tooltip = "Go to sleep and advance time to the next day. Night time counts as three time chunks when calculating serum durations.", priority = 20)
        faq_action = Action("Check the FAQ.",faq_action_requirement,"faq_action_description",
            menu_tooltip = "Answers to frequently asked questions about Lab Rats 2.")

        downtown_search_action = Action("Wander the streets.\n{image=gui/heart/Time_Advance.png}", downtown_search_requirement, "downtown_search_label",
            menu_tooltip = "Spend time exploring the city and seeing what interesting locations it has to offer.")


        strip_club_show_action = Action("Watch a show.", stripclub_show_requirement, "stripclub_dance",
            menu_tooltip = "Take a seat and wait for the next girl to come out on stage.")

        mom_office_person_request_action = Action("Approach the receptionist.", mom_office_person_request_requirement, "mom_office_person_request",
            menu_tooltip = "The receptionist might be able to help you, if you're looking for someone.")


        import_wardrobe_action = Action("Import a wardrobe file.", faq_action_requirement, "wardrobe_import",
            menu_tooltip = "Select and import a wardrobe file, adding all outfits to your current wardrobe.")


        test_action = Action("This is a test.", faq_action_requirement, "faq_action_description")



        ##Roles##
    call instantiate_roles() from _call_instantiate_roles #Broken out as a renpy statement instead of using the python equivalent because returning from a label might skip to the end of the whole pyton statement.
    python:
        ##Actions unlocked by policies##
        set_uniform_action = Action("Manage Employee Uniforms.",set_uniform_requirement,"set_uniform_description")
        set_serum_action = Action("Set Daily Serum Doses.",set_serum_requirement,"set_serum_description")

        ##PC's Home##
        hall = Room("main hall","Home",[],standard_house_backgrounds[:],[],[],[],False,[3,3], lighting_conditions = standard_indoor_lighting)
        bedroom = Room("your bedroom", "Your Bedroom",[],standard_bedroom_backgrounds[:],[],[],[sleep_action,faq_action],False,[3,2], lighting_conditions = standard_indoor_lighting)
        lily_bedroom = Room("Lily's bedroom", "Lily's Bedroom",[],standard_bedroom_backgrounds[:],[],[],[],False,[2,3], lighting_conditions = standard_indoor_lighting)
        mom_bedroom = Room("your mom's bedroom", "Mom's Bedroom",[], standard_bedroom_backgrounds[:],[],[],[],False,[2,4], lighting_conditions = standard_indoor_lighting)
        kitchen = Room("kitchen", "Kitchen",[],standard_kitchen_backgrounds[:],[],[],[],False,[3,4], lighting_conditions = standard_indoor_lighting)

        home_bathroom = Room("bathroom", "Bathroom", [], home_bathroom_background, [], [], [], False, [0,0], visible = False) #Note: Only used by special events. Not connected to the main map


        ##PC's Work##
        lobby = Room(business_name + " lobby",business_name + " Lobby",[],standard_office_backgrounds[:],[],[],[],False,[11,3], tutorial_label = "lobby_tutorial_intro", lighting_conditions = standard_indoor_lighting)
        office = Room("main office","Main Office",[],standard_office_backgrounds[:],[],[],[policy_purhase_action,hr_work_action,supplies_work_action,interview_action,sell_serum_action,pick_supply_goal_action,set_uniform_action,set_serum_action],False,[11,2], tutorial_label = "office_tutorial_intro", lighting_conditions = standard_indoor_lighting)
        m_division = Room("marketing division","Marketing Division",[],standard_office_backgrounds[:],[],[],[market_work_action,set_company_model_action],False,[12,3], tutorial_label = "marketing_tutorial_intro", lighting_conditions = standard_indoor_lighting)
        rd_division = Room("R&D division","R&D Division",[],lab_background,[],[],[research_work_action,design_serum_action,pick_research_action,review_designs_action,set_head_researcher_action],False,[12,4], tutorial_label = "research_tutorial_intro", lighting_conditions = standard_indoor_lighting)
        p_division = Room("Production division", "Production Division",[],standard_office_backgrounds[:],[],[],[production_work_action,pick_production_action,trade_serum_action],False,[11,4], tutorial_label = "production_tutorial_intro", lighting_conditions = standard_indoor_lighting)


        ##Connects all Locations##
        downtown = Room("downtown","Downtown",[],standard_downtown_backgrounds[:],[],[],[downtown_search_action],True,[6,4], lighting_conditions = standard_outdoor_lighting)

        ##A mall, for buying things##
        mall = Room("mall","Mall",[],standard_mall_backgrounds[:],[],[],[],True,[8,2], lighting_conditions = standard_indoor_lighting)
        gym = Room("gym","Gym",[],standard_mall_backgrounds[:],[],[],[],True,[7,1], lighting_conditions = standard_indoor_lighting)
        home_store = Room("home improvement store","Home Improvement Store",[],standard_mall_backgrounds[:],[],[],[],True,[8,1], lighting_conditions = standard_indoor_lighting)
        sex_store = Room("sex store","Sex Store",[],standard_mall_backgrounds[:],[],[],[],True,[9,2], lighting_conditions = standard_indoor_lighting)
        clothing_store = Room("clothing store","Clothing Store",[],standard_mall_backgrounds[:],[],[],[import_wardrobe_action],True,[8,3], lighting_conditions = standard_indoor_lighting)
        office_store = Room("office supply store","Office Supply Store",[],standard_mall_backgrounds[:],[],[],[],True,[9,1], lighting_conditions = standard_indoor_lighting)


        ##Other Locations##
        aunt_apartment = Room("Rebecca's Apartment", "Rebecca's Apartment", [], standard_house_backgrounds[:], [], [], [], False, [4, 2], None, False, lighting_conditions = standard_indoor_lighting)
        aunt_bedroom = Room("Rebecca's bedroom", "Rebecca's Bedroom", [], standard_bedroom_backgrounds[:], [], [], [], False, [3, 1], None, False, lighting_conditions = standard_indoor_lighting)
        cousin_bedroom = Room("Gabrielle's bedroom", "Gabrielle's Bedroom", [], standard_bedroom_backgrounds[:], [], [], [], False, [4,1], None, False, lighting_conditions = standard_indoor_lighting)

        university = Room("university Campus", "University Campus", [], standard_campus_backgrounds[:], [], [], [], False, [9,5], None, False, standard_outdoor_lighting)

        strip_club_owner = get_random_male_name()
        strip_club = Room(strip_club_owner + "'s Gentlemen's Club", strip_club_owner + "'s Gentlemen's Club", [], stripclub_background, [], [], [strip_club_show_action], False, [6,5], None, False, lighting_conditions = standard_club_lighting)

        mom_office_name = get_random_male_name() + " and " + get_random_male_name() + " Ltd."

        mom_office_lobby = Room(mom_office_name + " Lobby", mom_office_name + " Lobby", [], standard_office_backgrounds[:], [], [], [mom_office_person_request_action], False, [5,4], lighting_conditions = standard_indoor_lighting)
        mom_offices = Room(mom_office_name + " Offices", mom_office_name + " Offices", [], standard_office_backgrounds[:], [], [], [], False, [5,5], visible = False, lighting_conditions = standard_indoor_lighting)


        bar_location = Room("Bar", "Bar", [], standard_bar_backgrounds[:], [], [], [], False, [10,10], visible = False, lighting_conditions = standard_indoor_lighting)

        ##PC starts in his bedroom##
        main_business = Business(business_name, m_division, p_division, rd_division, office, office)
        mc = MainCharacter(bedroom,character_name,last_name,main_business,stat_array,skill_array,_sex_array)



        town_relationships = RelationshipArray() #Singleton class used to track relationships. Remvoes need for recursive character references (which messes with Ren'py's saving methods)
        mc.generate_goals()

        generate_premade_list() # Creates the list with all the premade characters for the game in it. Without this we both break the policies call in create_random_person, and regenerate the premade list on each restart.

        ##Keep a list of all the places##
        list_of_places.append(bedroom)
        list_of_places.append(lily_bedroom)
        list_of_places.append(mom_bedroom)
        list_of_places.append(kitchen)
        list_of_places.append(hall)

        list_of_places.append(lobby)
        list_of_places.append(office)
        list_of_places.append(rd_division)
        list_of_places.append(p_division)
        list_of_places.append(m_division)

        list_of_places.append(downtown)

        list_of_places.append(office_store)
        list_of_places.append(clothing_store)
        list_of_places.append(sex_store)
        list_of_places.append(home_store)
        list_of_places.append(gym)
        list_of_places.append(mall)

        list_of_places.append(aunt_apartment)
        list_of_places.append(aunt_bedroom)
        list_of_places.append(cousin_bedroom)
        list_of_places.append(university)
        list_of_places.append(strip_club)

        list_of_places.append(mom_office_lobby)
        list_of_places.append(mom_offices)

        for room in [bedroom, lily_bedroom, mom_bedroom, aunt_bedroom, cousin_bedroom]:
            room.add_object(make_wall())
            room.add_object(make_floor())
            room.add_object(make_bed())
            room.add_object(make_window())

        home_bathroom.add_object(make_wall())
        home_bathroom.add_object(Object("shower door", ["Lean"], sluttiness_modifier = 5, obedience_modifier = 5))
        home_bathroom.add_object(make_floor())

        kitchen.add_object(make_wall())
        kitchen.add_object(make_floor())
        kitchen.add_object(make_chair())
        kitchen.add_object(make_table())

        hall.add_object(make_wall())
        hall.add_object(make_floor())

        lobby.add_object(make_wall())
        lobby.add_object(make_floor())
        lobby.add_object(make_chair())
        lobby.add_object(make_desk())
        lobby.add_object(make_window())

        office.add_object(make_wall())
        office.add_object(make_floor())
        office.add_object(make_chair())
        office.add_object(make_desk())
        office.add_object(make_window())

        mom_office_lobby.add_object(make_wall())
        mom_office_lobby.add_object(make_floor())
        mom_office_lobby.add_object(make_chair())
        mom_office_lobby.add_object(make_desk())
        mom_office_lobby.add_object(make_window())

        mom_offices.add_object(make_wall())
        mom_offices.add_object(make_floor())
        mom_offices.add_object(make_chair())
        mom_offices.add_object(make_desk())
        mom_offices.add_object(make_window())

        rd_division.add_object(make_wall())
        rd_division.add_object(make_floor())
        rd_division.add_object(make_chair())
        rd_division.add_object(make_desk())

        m_division.add_object(make_wall())
        m_division.add_object(make_floor())
        m_division.add_object(make_chair())
        m_division.add_object(make_desk())

        p_division.add_object(make_wall())
        p_division.add_object(make_floor())
        p_division.add_object(make_chair())
        p_division.add_object(make_desk())

        downtown.add_object(make_floor())

        university.add_object(make_grass())

        office_store.add_object(make_wall())
        office_store.add_object(make_floor())
        office_store.add_object(make_chair())

        clothing_store.add_object(make_wall())
        clothing_store.add_object(make_floor())

        sex_store.add_object(make_wall())
        sex_store.add_object(make_floor())

        home_store.add_object(make_wall())
        home_store.add_object(make_floor())
        home_store.add_object(make_chair())

        mall.add_object(make_wall())
        mall.add_object(make_floor())

        gym.add_object(make_wall())
        gym.add_object(make_floor())

        aunt_apartment.add_object(make_wall())
        aunt_apartment.add_object(make_floor())
        aunt_apartment.add_object(make_couch())
        aunt_apartment.add_object(make_table())
        aunt_apartment.add_object(make_chair())

        strip_club.add_object(make_wall())
        strip_club.add_object(make_floor())
        strip_club.add_object(make_table())
        strip_club.add_object(make_chair())
        strip_club.add_object(make_stage())

        for place in list_of_places:
            if place.public:
                if not max_num_of_random == 0:
                    random_count = renpy.random.randint(1,max_num_of_random)
                else:
                    random_count = 0;
                for x in range(0,random_count):
                    the_person = create_random_person()
                    the_person.generate_home()
                    place.add_person(the_person) #We are using create_random_person instead of make_person because we want premade character bodies to be hirable instead of being eaten up by towns-folk.

        stripclub_strippers = []
        stripclub_wardrobe = wardrobe_from_xml("Stripper_Wardrobe")
        for i in __builtin__.range(0,4):
            a_girl = create_random_person(start_sluttiness = renpy.random.randint(15,30))
            a_girl.generate_home()
            a_girl.set_schedule(strip_club, times = [3,4])
            stripclub_strippers.append(a_girl)
            strip_club.add_person(a_girl)

        business_wardrobe = wardrobe_from_xml("Business_Wardrobe") #Used in some of Mom's events when we need a business-ish outfit


        ##Global Variable Initialization##
        day = 0 ## Game starts on day 0.
        time_of_day = 0 ## 0 = Early morning, 1 = Morning, 2 = Afternoon, 3 = Evening, 4 = Night

    return
