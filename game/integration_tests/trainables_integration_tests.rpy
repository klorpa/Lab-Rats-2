init 1 python:
    integration_test_labels.append("run_basic_trainables_integration_tests")

label run_basic_trainables_integration_tests():
    $ the_person = mom
    $ the_person.draw_person()
    $ the_person.run_orgasm(force_trance = True)
    $ mc.add_clarity(8000)
    $ renpy.notify("Do nothing, end training early")
    call trance_train_label(the_person)
    menu:
        "Successfully ended without training.":
            pass

        "Test failed.":
            return False

    $ renpy.notify("Purchase stat increase.")

    call trance_train_label(the_person)
    menu:
        "Succesfully bought stat increase.":
            pass

        "Test failed.":
            return False

    $ renpy.notify("Add a new opinion.")
    call trance_train_label(the_person)
    menu:
        "Opinion added.":
            pass

        "Test failed.":
            return False

    $ renpy.notify("Strenthen opinion.")
    call trance_train_label(the_person)
    menu:
        "Opinion strengthened.":
            pass

        "Test failed.":
            return False

    return True
