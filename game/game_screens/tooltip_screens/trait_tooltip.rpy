screen trait_tooltip(the_trait, given_align = (0.0,0.0), given_anchor = (0.0,0.0)):
    frame:
        background "#888888"
        align given_align
        anchor given_anchor
        vbox:
            xsize 500
            text the_trait.name style "menu_text_style" xalign 0.5 xanchor 0.5
            use aspect_grid(the_trait)

            if isinstance(the_trait, SerumTraitBlueprint):
                text "Customisable Trait" style "menu_text_style" size 16 color "#9898fb" xalign 0.5 xanchor 0.5
            if the_trait.exclude_tags:
                $ conflict_string = "Exclusive Tags: "
                for exclude_tag in the_trait.exclude_tags:
                    $ conflict_string += exclude_tag
                    if not exclude_tag == the_trait.exclude_tags[-1]:
                        $ conflict_string += ", "

                text conflict_string style "menu_text_style" size 14 color "#9898fb" xalign 0.5 xanchor 0.5
            if the_trait.positive_slug:
                text the_trait.positive_slug style "menu_text_style" size 14 color "#98fb98" xalign 0.5 xanchor 0.5
            if the_trait.build_negative_slug():
                text the_trait.build_negative_slug() style "menu_text_style" size 14 color "#ff0000" xalign 0.5 xanchor 0.5

            text the_trait.desc style "menu_text_style" xalign 0.5 xanchor 0.5
            transclude

screen trait_list_tooltip(the_traits, given_align = (0.0,0.0), given_anchor = (0.0,0.0)): #TODO: Update this to match parameters handed to trait tooltip. Used when you need to display a list of traits all together.
    hbox:
        spacing 50
        align given_align
        anchor given_anchor
        for trait in the_traits:
            use trait_tooltip(trait)

        transclude
         #If you hand the serum tooltip a child it's added to the vBox

screen trait_details(the_trait, given_xanchor = 0.5, given_xalign = 0.5):
    frame:
        background "#444444"
        xfill True
        yfill False
        vbox:
            text the_trait.name style "menu_text_style"
            use aspect_grid(the_trait, given_xanchor, given_xalign)
            if the_trait.positive_slug:
                text "    "  + the_trait.positive_slug style "menu_text_style" color "#98fb98"
            if the_trait.negative_slug:
                text "    "  + the_trait.negative_slug style "menu_text_style" color "#ff0000"

screen aspect_grid(the_thing, given_xanchor = 0.5, given_xalign = 0.5): #Note: This can be given either a trait or a serum, since both have aspect info.
    grid 7 1:
        xanchor given_xanchor
        xalign given_xalign
        if the_thing.tier > mc.business.max_serum_tier:
            text "Tier: {color=#fb6868}" + str(the_thing.tier) + "{/color}" style "menu_text_style" size 14
        else:
            text "Tier: " + str(the_thing.tier) style "menu_text_style" size 14
        text "Men: " + str(the_thing.mental_aspect) style "menu_text_style" size 14 color "#0049d8"
        text "Phy: " + str(the_thing.physical_aspect) style "menu_text_style" size 14 color "#00AA00"
        text "Sex: " + str(the_thing.sexual_aspect) style "menu_text_style" size 14 color "#FFC0CB"
        text "Med: " + str(the_thing.medical_aspect) style "menu_text_style" size 14 color "#FFFFFF"
        text "Flw: " + str(the_thing.flaws_aspect) style "menu_text_style" size 14 color "#BBBBBB"
        text "Attn: " + str(the_thing.attention) style "menu_text_style" size 14 color "#FF6249"

screen contract_aspect_grid(the_thing):
    $ non_zero_aspects = 0
    if the_thing.mental_aspect > 0:
        $ non_zero_aspects += 1
    if the_thing.physical_aspect > 0:
        $ non_zero_aspects += 1
    if the_thing.sexual_aspect > 0:
        $ non_zero_aspects += 1
    if the_thing.medical_aspect > 0:
        $ non_zero_aspects += 1

    hbox:
        text "Doses Required: " + str(the_thing.amount_desired) style "menu_text_style" size 14 color "#4444AA"
        text "Payout: $" + str(the_thing.price_per_dose*the_thing.amount_desired) style "menu_text_style" size 14 color "#85bb65"

        if the_thing.contract_started:
            text "Deliver in: " + str(the_thing.contract_length - the_thing.time_elapsed) + " days" style "menu_text_style" size 14 color "#BBBBBB"
        else:
            text "Deliver in: "+ str(the_thing.contract_length) + " days" style "menu_text_style" size 14 color "#BBBBBB"


    grid non_zero_aspects+2 1:
        if the_thing.mental_aspect > 0:
            text "Men: >=" + str(the_thing.mental_aspect) style "menu_text_style" size 14 color "#0049d8"
        if the_thing.physical_aspect > 0:
            text "Phy: >=" + str(the_thing.physical_aspect) style "menu_text_style" size 14 color "#00AA00"
        if the_thing.sexual_aspect > 0:
            text "Sex: >=" + str(the_thing.sexual_aspect) style "menu_text_style" size 14 color "#FFC0CB"
        if the_thing.medical_aspect > 0:
            text "Med: >=" + str(the_thing.medical_aspect) style "menu_text_style" size 14 color "#FFFFFF"
        text "Flw: <=" + str(the_thing.flaws_aspect) style "menu_text_style" size 14 color "#BBBBBB"
        text "Attn: <=" + str(the_thing.attention) style "menu_text_style" size 14 color "#FF6249"
