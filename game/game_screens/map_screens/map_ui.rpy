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
