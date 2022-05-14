#Contains LR2 specific styles and transforms that are used elsewhere, rather inconsistently.
init 0:
    transform scale_person(height_factor = 1):
        zoom (height_factor*0.8)  #This is the scale factor for height, with the tallest unmodified by serum girl being 0.8 and the shortest being 0.72

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

    style textbutton_style: ##The generic style used for text button backgrounds. TODO: Replace this with a pretty background image instead of a flat colour.
        padding [5,5]
        margin [5,5]
        background "#000080"
        insensitive_background "#222222"
        hover_background "#aaaaaa"

    style textbutton_text_style: ##The generic style used for the text within buttons
        size 20
        italic True
        bold True
        color "#dddddd"
        outlines [(2,"#222222",0,0)]
        text_align 0.5

    style menu_text_style:
        size 18
        italic True
        bold True
        color "#dddddd"
        outlines [(2,"#222222",0,0)]
        text_align 0.5

    style outfit_style: ##The text style used for text inside of the outfit manager.
        size 16
        italic True
        color "#dddddd"
        outlines [(1,"#666666",0,0)]
        insensitive_color "#222222"
        hover_color "#ffffff"

    style outfit_description_style is textbutton_text_style:
        size 14

    style return_button_style:
        text_align 0.5
        size 30
        italic True
        bold True
        color "#dddddd"
        outlines [(2,"#222222",0,0)]

    style map_text_style:
        text_align 0.5
        size 14
        italic True
        bold True
        color "#dddddd"
        outlines [(2,"#222222",0,0)]

    style map_frame_style:
        background "#094691"

    style map_frame_blue_style:
        background "#5fa7ff"

    style map_frame_grey_style:
        background "#222222"

    style digital_text is text:
        font "fonts/Autobusbold-1ynL.ttf"
        color "#19e9f7"
        outlines [(2,"#222222",0,0)]
        yanchor 0.5
        yalign 0.5

    style text_message_style is say_dialogue:
        font "fonts/Autobusbold-1ynL.ttf"
        color "#19e9f7"
        outlines [(2,"#222222",0,0)]
        #TODO: MIght need to decide on Size too

    style general_dialogue_style is say_dialogue:
        outlines [(2,"#222222",0,0)]

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
