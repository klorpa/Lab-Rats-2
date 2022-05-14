label set_duties_controller(the_person): # UI only builds a list of duties we plan to add/remove, we don't change anything until those lists are finalized
    call screen set_duties_screen(the_person) # Avoids running on_apply and on_remove code repeatedly, possibly resulting in incorrect variable resets
    $ duties_to_add = _return[0]
    $ duties_to_remove = _return[1]
    $ duties_updated = False
    python:
        for a_duty in duties_to_add:
            the_person.add_duty(a_duty)
            duties_updated = True
        for a_duty in duties_to_remove:
            the_person.remove_duty(a_duty)
            duties_updated = True
    return duties_updated # Only reset the duties counter if something was actually changed.


screen set_duties_screen(the_person, allow_changing_duties = True, show_available_duties = True, hide_on_exit = False):
    modal True
    zorder 120
    add "Paper_Background.png"
    $ available_duties = []
    default add_duties = []
    default remove_duties = []
    python:
        for a_duty in the_person.job.available_duties:
            if a_duty.check_requirement(the_person) is not False:
                available_duties.append(a_duty)
    default selected_duty = None
    python:
        for a_duty in the_person.duties + add_duties:
            if a_duty in available_duties:
                available_duties.remove(a_duty) # Remove current duties from the available list.

    vbox:
        yalign 0.05
        xanchor 0.5
        xalign 0.5
        use girl_title_header(the_person, 1750, 120)
        spacing 20
        hbox:
            xanchor 0.5
            xalign 0.5
            spacing 20
            if show_available_duties:
                frame:
                    background "#1a45a1aa"
                    xsize 500
                    ysize 700
                    xanchor 0.5
                    xalign 0.5
                    vbox:
                        text "Available Duties" style "menu_text_style" size 22
                        # viewport: #TODO: Add viewports when we have enough duties set to justify it
                        #     mousewheel True
                        #     scrollbars "vertical"
                        for a_duty in available_duties:
                            textbutton a_duty.duty_name:
                                style "textbutton_style" text_style "textbutton_text_style"
                                action SetScreenVariable("selected_duty", a_duty)
                                sensitive True
                                if not a_duty is selected_duty:
                                    background "#000080"

                                else:
                                    background "#000040"

                                hover_background "#1a45a1"
                                insensitive_background "#222222"

            frame:
                background "#1a45a1aa"
                xsize 500
                ysize 700
                xanchor 0.5
                xalign 0.5
                vbox:
                    $ the_person.duties_title = "Current Duties (" + str(len(the_person.duties)+len(add_duties)) + "/" + str(the_person.work_experience) + ")"
                    text the_person.duties_title style "menu_text_style" size 22
                    # viewport:
                    #     mousewheel True
                    #     scrollbars "vertical"
                    vbox:
                        for a_duty in the_person.duties + add_duties:
                            textbutton a_duty.duty_name:
                                style "textbutton_style" text_style "textbutton_text_style"

                                action SetScreenVariable("selected_duty", a_duty)
                                sensitive True
                                if not a_duty is selected_duty:
                                    background "#000080"

                                else:
                                    background "#000040"
                                hover_background "#1a45a1"
                                insensitive_background "#222222"
            frame:
                background "#1a45a1aa"
                xsize 500
                ysize 700
                xanchor 0.5
                xalign 0.5
                vbox:
                    xanchor 0.5
                    xalign 0.5
                    if selected_duty is not None:
                        use duty_tooltip(selected_duty):
                            if allow_changing_duties: #Hide the button so we can use this as a display.
                                if selected_duty in the_person.duties + add_duties:
                                    if selected_duty in the_person.job.mandatory_duties:
                                        textbutton "Locked - Mandatory Duty":
                                            style "textbutton_style"
                                            text_style "textbutton_text_style"
                                            xanchor 0.5
                                            xalign 0.5
                                            action NullAction()
                                            sensitive False
                                            insensitive_background "#222222"
                                    else:
                                        textbutton "Remove Duty":
                                            style "textbutton_style"
                                            text_style "textbutton_text_style"
                                            xanchor 0.5
                                            xalign 0.5
                                            if selected_duty in add_duties:
                                                action RemoveFromSet(add_duties, selected_duty)
                                            else:
                                                action AddToSet(remove_duties, selected_duty)
                                            background "#000080"
                                            hover_background "#1a45a1"
                                            insensitive_background "#222222"

                                else:
                                    $ button_name = "Add Duty"
                                    $ button_sensitive = selected_duty.check_requirement(the_person)
                                    if button_sensitive is True:
                                        if len(the_person.duties) + len(add_duties) >= the_person.work_experience:
                                            $ button_sensitive = "Max Duties Reached"
                                    if isinstance(button_sensitive, basestring):
                                        $ button_name += " - " + button_sensitive
                                    textbutton button_name:
                                        style "textbutton_style"
                                        text_style "textbutton_text_style"
                                        sensitive button_sensitive is True  #NOTE: button_sensitive can be a string, so we do direct comparison.
                                        xanchor 0.5
                                        xalign 0.5
                                        if selected_duty in remove_duties:
                                            action RemoveFromSet(remove_duties, selected_duty)
                                        else:
                                            action AddToSet(add_duties, selected_duty)
                                        action Function(the_person.add_duty, selected_duty)
                                        background "#000080"
                                        hover_background "#1a45a1"
                                        insensitive_background "#222222"

    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            if hide_on_exit: #Use this when you want ot show this screen from another. Note that you cannot change duties if just hiding/showing. (TODO: Try using run_in_new_context to call the duties_manager label)
                action Hide("set_duties_screen")
            else:
                action Return([add_duties, remove_duties])
        textbutton "Return" align [0.5,0.5] style "return_button_style" text_style "return_button_style"
