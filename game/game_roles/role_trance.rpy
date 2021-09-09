### All of the actions for when a girl is in some level of trance. ###
init -2 python:
    def trance_on_turn(the_person):
        the_person.event_triggers_dict["trance_training_available"] = True
        if renpy.random.randint(0, 100) >= the_person.suggestibility:
            if the_person.has_exact_role(very_heavy_trance_role):
                the_person.remove_role(very_heavy_trance_role)
                the_person.add_role(heavy_trance_role)
            elif the_person.has_exact_role(heavy_trance_role):
                the_person.remove_role(heavy_trance_role)
                the_person.add_role(trance_role)
            else:
                the_person.remove_role(trance_role)

    def trance_on_day(the_person):
        # Run 2 extra instances of the on turn to match the standard decay rate of serums.
        trance_on_turn(the_person)
        trance_on_turn(the_person)


    def trance_train_requirement(the_person):
        if not the_person.event_triggers_dict.get("trance_training_available", True):
            return "Trained too recently."
        else:
            return True

label trance_train_label(the_person):
    if the_person.has_exact_role(trance_role):
        "It's subtle, but you can tell from [the_person.possessive_title]'s unfocused gaze that she's still in her post-orgasm trance."

    elif the_person.has_exact_role(heavy_trance_role):
        "It's obvious from [the_person.possessive_title]'s unfocused gaze and relaxed posture that she's still deep in a post-orgasm trance."

    else:
        "[the_person.possessive_title]'s eyes are unfocused, her mouth slightly slack."
        "It's painfully obvious that thoughts are somewhere else entirely, and that makes her open to all types of influences."
    mc.name "[the_person.title], I want you to listen closely to me, okay? This is going to be very important."
    #TODO: Different reactions depending on Obedience, same result but she's on auto pilot
    the_person "Yeah, sure..."
    call do_training(the_person)
    return
