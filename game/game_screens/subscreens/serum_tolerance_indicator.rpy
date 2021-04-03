screen serum_tolerance_indicator(the_person): #Produces a hoverable textbutton that contains the current serum count vs current serum tolerance
    textbutton "Serum Tolerance: " + str(len(the_person.serum_effects)) + "/" + str(the_person.serum_tolerance):
        style "textbutton_style"
        text_style "textbutton_text_style"
        tooltip "Being under the effects of too many serums at once can have negative side effects, lowering Sluttiness, Obedience, and Happiness."
        action NullAction()
        sensitive True
        if len(the_person.serum_effects) > the_person.serum_tolerance:
            text_color "#FF0000"
