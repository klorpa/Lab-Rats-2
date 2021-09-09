screen girl_title_header(the_person, x_size, y_size, include_details_button = False):
    frame:
        xsize x_size
        ysize y_size
        xalign 0.5
        background "#1a45a1aa"

        if include_details_button:
            textbutton "Show Details":
                style "textbutton_style"
                text_style "textbutton_text_style"
                action Show("person_info_detailed", None, the_person)
                xanchor 1.0
                xalign 0.95
                yanchor 0.5
                yalign 0.5

        vbox:
            xalign 0.5 xanchor 0.5
            text "[the_person.name] [the_person.last_name]" style "menu_text_style" size 30 xalign 0.5 yalign 0.5 yanchor 0.5 color the_person.char.who_args["color"] font the_person.char.what_args["font"]
            if not mc.business.get_employee_title(the_person) == "None":
                text "Position: " + mc.business.get_employee_title(the_person) + " ($[the_person.salary]/day)" style "menu_text_style" xalign 0.5 yalign 0.5 yanchor 0.5

            $ visible_roles = []
            $ role_string = "Special Roles: "
            python:
                for role in the_person.special_role:
                    if not role.hidden:
                        visible_roles.append(role.role_name)

                if visible_roles:
                    role_string += visible_roles[0]
                    for role in visible_roles[1::]: #Slicing off the first manually let's us use commas correctly.
                        role_string += ", " + role
            if visible_roles:
                text role_string style "menu_text_style" xalign 0.5 yalign 0.5 yanchor 0.5
