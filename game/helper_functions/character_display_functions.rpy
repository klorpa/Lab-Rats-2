init -1 python:
    def clear_scene(specific_layers = None): # Clears the current scene of characters.
        global draw_layers
        if specific_layers is not None and not isinstance(specific_layers, list):
            specific_layers = [specific_layers] #Allows for passing lists or single names.

        for a_layer in draw_layers:
            if specific_layers is None or a_layer in specific_layers:
                renpy.scene(a_layer)

    def can_use_animation(): #Checks key properties to determine if we can or cannot use animation (mainly rendering type and config option
        if renpy.mobile: #Unfortunately no animation support for mobile devices.
            return False

        if not renpy.display.draw.info["renderer"] == "gl2": #Software rendering does not support the screen capture technique we use, so we can only use static images for it. (also it runs painfully slow, so it needs everything it can get).
            return False

        if not persistent.vren_animation:
            return False

        return True

    def add_draw_layer(layer_name): #Sets up a character draw layer under the name of "layer name". This can be used to draw multiple characters on the screen at once.
        global draw_layers

        if layer_name not in draw_layers:
            draw_layers.append(layer_name)
            renpy.add_layer(layer_name, above = "master")
            config.menu_clear_layers.append(layer_name)
            config.context_clear_layers.append(layer_name)
