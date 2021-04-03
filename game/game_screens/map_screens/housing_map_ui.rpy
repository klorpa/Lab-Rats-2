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
