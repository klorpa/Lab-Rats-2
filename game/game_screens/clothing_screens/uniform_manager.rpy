# Provides a list of clothing items inside of the uniform wardrobe
# Each uniform has a couple of key pieces of information that is also stored with it (Extend Wardrobe?)
# First, it lists if it should be an overwear, underwear, or full uniform. The same outfit can be flagged for any or all of them, if valid.
# Second, it lists what departments the outfit should be worn for. Could be All, some combination of specific departments, or None.

# We also need a button that takes us to the outfit select manager. From here you can select an outfit to add to the uniform wardrobe.
# init -2 python: #TODO See if we even need anything likethese funcitons
#     def uniform_manager_set_underwear(the_uniform):
#         the_uniform.underwear_flag = not the_uniform.underwear_flag
#
#     def uniform_manager_set_overwear(the_uniform):
#         the_uniform.overwear_flag = not the_uniform.overwear_flag
#
#     def uniform_manager_set_full(the_uniform):
#         the_uniform.full_outfit_flag = not the_uniform.full_outfit_flag
#
#     def uniform_manager_set_research(the_uniform):
#         the_uniform.research_flag = not the_uniform.research_flag
#
#     def uniform_manager_set_prod(the_uniform):
#         the_uniform.production_flag = not the_uniform.production_flag
#
#     def uniform_manager_set_supply(the_uniform):
#         the_uniform.supply_flag = not the_uniform.supply_flag
#
#     def uniform_manager_set_market(the_uniform):
#         the_uniform.marketing_flag = not the_uniform.marketing_flag
#
#     def uniform_manager_set_hr(the_uniform):
#         the_uniform.hr_flag = not the_uniform.hr_flag

screen uniform_manager():
    add "Paper_Background.png"
    default preview_outfit = None
    modal True
    $ slide_amount = 120 #Easier modification for where the headers sit.

    vbox:
        spacing 10
        hbox:
            null width 425 + slide_amount
            text "Uniform Style" style "menu_text_style" size 30
            null width 400
            text "Used By"  style "menu_text_style" size 30

        null height -25
        hbox:
            spacing 60

            #text "Name" style "menu_text_style" size 30
            null width 315 + slide_amount

            text "Full" style "menu_text_style" size 25 xsize 50 #TODO: Make these textbuttons so we can have tooltips
            text "Over" style "menu_text_style" size 25 xsize 50
            text "Under" style "menu_text_style" size 25  xsize 50

            null# width 50

            text "Market" style "menu_text_style" size 25 xsize 50
            text "R&D" style "menu_text_style" size 25 xsize 50
            text "Prod" style "menu_text_style" size 25 xsize 50
            text "Supply" style "menu_text_style" size 25 xsize 50
            text "HR" style "menu_text_style" size 25 xsize 50
        viewport:
            xalign 0.05
            yalign 0.05
            scrollbars "vertical"
            ysize 750
            mousewheel True
            vbox:
                for a_uniform in mc.business.business_uniforms:
                    use uniform_entry(a_uniform)

        textbutton "Add Uniform":
            style "textbutton_style"
            text_style "textbutton_text_style"
            action Return("Add")

    use mannequin_display(preview_outfit)

    frame:
        background None
        anchor [0.5,0.5]
        align [0.39,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action [mc.business.update_uniform_wardrobes(), Return(None)]
        textbutton "Return" align [0.5,0.5] text_style "return_button_style"

screen uniform_entry(given_uniform):
    frame:
        background "#888888"
        hbox:
            spacing 80
            hbox:
                spacing 10
                textbutton given_uniform.outfit.name:
                    xsize 250
                    yanchor 0.5
                    yalign 0.5
                    sensitive True
                    hovered SetScreenVariable("preview_outfit", given_uniform.outfit)
                    unhovered SetScreenVariable("preview_outfit", None)
                    action NullAction()
                    style "textbutton_style"
                    text_style "textbutton_text_style"
                textbutton "Remove":
                    xsize 150
                    text_xanchor 0.5
                    text_xalign 0.5
                    yanchor 0.5
                    yalign 0.5
                    sensitive True
                    hovered SetScreenVariable("preview_outfit", given_uniform.outfit)
                    unhovered SetScreenVariable("preview_outfit", None)
                    action [SetScreenVariable("preview_outfit", None), RemoveFromSet(mc.business.business_uniforms, given_uniform)]
                    style "textbutton_style"
                    text_style "textbutton_text_style"
                    background "#800000"
                    hover_background "#b00000"
            #null
            use uniform_button(state = given_uniform.full_outfit_flag, is_sensitive = given_uniform.can_toggle_full_outfit_state(), toggle_function = given_uniform.set_full_outfit_flag)
            use uniform_button(state = given_uniform.overwear_flag, is_sensitive = given_uniform.can_toggle_overwear_state(), toggle_function = given_uniform.set_overwear_flag)
            use uniform_button(state = given_uniform.underwear_flag, is_sensitive = given_uniform.can_toggle_underwear_state(), toggle_function = given_uniform.set_underwear_flag)

            null #Spacing purposes
            use uniform_button(state = given_uniform.marketing_flag, is_sensitive = True, toggle_function = given_uniform.set_marketing_flag)
            use uniform_button(state = given_uniform.research_flag, is_sensitive = True, toggle_function = given_uniform.set_research_flag)
            use uniform_button(state = given_uniform.production_flag, is_sensitive = True, toggle_function = given_uniform.set_production_flag)
            use uniform_button(state = given_uniform.supply_flag, is_sensitive = True, toggle_function = given_uniform.set_supply_flag)
            use uniform_button(state = given_uniform.hr_flag, is_sensitive = True, toggle_function = given_uniform.set_hr_flag)

screen uniform_button(state, is_sensitive, toggle_function):
    $ button_colour = "#666666"
    $ hovered_button_colour = "#aaaaaa"

    if is_sensitive:
        if state:
            $ button_colour = "#449044"
            $ hovered_button_colour = "#66a066"

    else:
        $ button_colour = "#222222"
        #$ hovered_button_colour = "#888888"

    button:
        background button_colour
        hover_background hovered_button_colour
        sensitive is_sensitive
        action Function(toggle_function, not state)
        xsize 50 ysize 40
        yanchor 0.5 yalign 0.5
