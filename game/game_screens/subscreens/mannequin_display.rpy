screen mannequin_display(the_outfit = None):
    fixed:
        pos (1450,0)
        add mannequin_average
        if the_outfit is not None:
            for cloth in the_outfit.generate_draw_list(None,"stand3"):
                add cloth
