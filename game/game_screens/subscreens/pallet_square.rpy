screen pallet_square(current_r, current_g, current_b, current_a, colour_list, count):

    $ background_colour = "#aaaaaa"
    button:
        yanchor 0.5
        yalign 0.5
        background background_colour
        action [SetScreenVariable("current_r", colour_list[0]), SetScreenVariable("current_g", colour_list[1]), SetScreenVariable("current_b", colour_list[2]), SetScreenVariable("current_a", colour_list[3])]
        alternate Function(update_colour_palette, count, current_r, current_g, current_b, current_a)
        sensitive True
        use colour_square(colour_list, background_colour = background_colour)

screen colour_square(colour_list, background_colour = "#aaaaaa", square_size_x = 30, square_size_y = 30):

    frame:
        yanchor 0.5
        yalign 0.5
        background Color(rgb=(colour_list[0], colour_list[1], colour_list[2]))
        frame: #semi-hack to produce a border of full alpha colour, makes it easier to see the relative transparency of something.
            xpadding 0
            ypadding 0
            background background_colour
            frame:
                background Color(rgb=(colour_list[0], colour_list[1], colour_list[2]), alpha = colour_list[3])
                xysize (square_size_x, square_size_y)
