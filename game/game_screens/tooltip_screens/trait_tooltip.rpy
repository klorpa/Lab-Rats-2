screen trait_tooltip(the_trait, given_align = (0.0,0.0), given_anchor = (0.0,0.0)):
    frame:
        background "#888888"
        align given_align
        anchor given_anchor
        vbox:
            xsize 500
            text the_trait.name style "menu_text_style" xalign 0.5 xanchor 0.5
            text the_trait.positive_slug style "menu_text_style" size 14 color "#98fb98" xalign 0.5 xanchor 0.5
            text the_trait.build_negative_slug() style "menu_text_style" size 14 color "#ff0000" xalign 0.5 xanchor 0.5
            text the_trait.desc style "menu_text_style" xalign 0.5 xanchor 0.5

screen trait_list_tooltip(the_traits, given_align = (0.0,0.0), given_anchor = (0.0,0.0)): #TODO: Update this to match parameters handed to trait tooltip. Used when you need to display a list of traits all together.
    hbox:
        spacing 50
        align given_align
        anchor given_anchor
        for trait in the_traits:
            use trait_tooltip(trait)
