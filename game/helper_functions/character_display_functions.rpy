init -1 python:
    def clear_scene(specific_layers = None): # Clears the current scene of characters.
        global draw_layers
        if specific_layers is not None and not isinstance(specific_layers, list):
            specific_layers = [specific_layers] #Allows for passing lists or single names.

        for a_layer in draw_layers:
            if specific_layers is None or a_layer in specific_layers:
                global_draw_number[a_layer] += 1
                renpy.scene(a_layer)

    def can_use_animation(): #Checks key properties to determine if we can or cannot use animation (mainly rendering type and config option
        if renpy.mobile: #Unfortunately no animation support for mobile devices.
            return False

        if renpy.display.draw.info["renderer"] == "sw": #Software rendering does not support the screen capture technique we use, so we can only use static images for it. (also it runs painfully slow, so it needs everything it can get).
            return False

        if not persistent.vren_animation:
            return False

        return True

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

                    the_render = prepared_animation_render[draw_layer].get(the_person.character_number, None)
                    if the_render is not None:
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
