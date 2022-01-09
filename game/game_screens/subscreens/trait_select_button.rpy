screen trait_select_button(the_trait, is_enabled = True, the_action = VrenNullAction, tooltip_anchor = (0.5,0.57), tooltip_align = (0.5,0.0)):
    $ trait_tags = ""
    # if the_trait.exclude_tags:
    #     $ trait_tags = " - "
    #     for a_tag in the_trait.exclude_tags:
    #         $ trait_tags += "[[" + a_tag + "]"

    $ aspect_tags = "\n{size=14}"
    if the_trait.tier > mc.business.max_serum_tier:
        $ aspect_tags += "Tier: {color=#98fb98}" + str(the_trait.tier) + "{/color}"
    else:
        $ aspect_tags += "Tier:" + str(the_trait.tier)

    $ aspect_tags += "{color=#0049d8} Men: " + str(the_trait.mental_aspect) + "{/color}"
    $ aspect_tags += "{color=#00AA00} Phy: " + str(the_trait.physical_aspect) + "{/color}"
    $ aspect_tags += "{color=#FFC0CB} Sex: " + str(the_trait.sexual_aspect) + "{/color}"
    $ aspect_tags += "{color=#FFFFFF} Med: " + str(the_trait.medical_aspect) + "{/color}"
    $ aspect_tags += "{color=#BBBBBB} Flw: " + str(the_trait.flaws_aspect) + "{/color}"
    $ aspect_tags += "{color=#FF6249} Attn: " + str(the_trait.attention) + "{/color}"
    $ aspect_tags += "{/size}"

    # $ side_effect_chance = the_trait.get_effective_side_effect_chance()
    # if side_effect_chance >= 10000: #If it's a massively high side effect chance assume it's a special trait and it's just guarnateed.
    #     $ side_effect_chance_string = "Always Guaranteed"
    # else:
    #     $ side_effect_chance_string = str(side_effect_chance) + "%"
    # $ trait_side_effects = "\nMastery Level: " + str(the_trait.mastery_level) + " | Side Effect Chance: " + side_effect_chance_string
    textbutton the_trait.name + aspect_tags:
        action [Hide("trait_tooltip"),the_action]
        sensitive is_enabled
        style "textbutton_style"
        text_style "textbutton_text_style"
        hovered Show("trait_tooltip",None, the_trait, tooltip_anchor, tooltip_align)
        unhovered Hide("trait_tooltip")
        xsize 530
        text_align 0.0
