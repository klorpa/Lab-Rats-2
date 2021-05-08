init 1 python:
    integration_test_labels.append("run_sex_system_integration_test")
    integration_test_labels.append("run_complex_sex_integraiton_test")


label run_sex_system_integration_test():
    "Testing sex system. Let's meet our happy contestant."
    "Run encounters until you cannot take any other actions."
    $ test_person = create_random_person()
    $ test_person.set_title("Tester")
    $ test_room = Room()
    $ test_room.add_person(test_person)
    $ mc.change_location(test_room)
    $ test_person.draw_person()

    "Starting sex with empty room, no Sluttiness."
    call fuck_person(test_person)
    menu:
        "Positions properly limited by Sluttiness.":
            pass

        "Test failed.":
            return False
    $ mc.change_energy(100)
    $ test_person.change_energy(100)
    $ test_person.change_slut_temp(100)
    $ test_person.change_slut_core(100)
    "Starting sex with empty room, high Sluttiness."
    call fuck_person(test_person)
    menu:
        "Positions properly limited by clothing, objects.":
            pass

        "Test failed.":
            return False

    $ mc.change_energy(100)
    $ test_person.change_energy(100)
    $ test_room.add_object(make_bed())
    "Starting sex in room with bed."
    call fuck_person(test_person)
    menu:
        "Positions properly enabled by objects.":
            pass

        "Test failed.":
            return False

    $ mc.change_energy(100)
    $ test_person.change_energy(100)
    $ test_person.change_slut_core(-100)
    $ test_person.change_slut_temp(-100)
    $ test_person.change_obedience(100)

    "Starting sex in room with high obedience, no Sluttiness."
    call fuck_person(test_person)
    menu:
        "Positions and stripping properly enabled by Obedience.":
            pass

        "Test failed.":
            return False

    $ mc.change_energy(100)
    $ test_person.change_energy(100)
    $ test_person.change_slut_core(50)
    $ test_person.change_slut_temp(50)
    $ other_person = create_random_person()
    $ other_person.set_title("Watcher")
    $ test_room.add_person(other_person)

    "Adding new person to room for public sex check."

    call fuck_person(test_person, private = False)
    menu:
        "Public sex responses properly triggered.":
            pass

        "Test failed.":
            return False

    $ mc.change_energy(100)
    $ test_person.change_energy(100)

    "Setting sex position to private this time."
    call fuck_person(test_person, private = True)
    menu:
        "Public sex responses not triggered.":
            pass

        "Test failed.":
            return False


    $ mc.change_location(bedroom)
    return True

label run_complex_sex_integraiton_test():
    "Testing complex sex options."
    "Run encounters until you do not have any options left."
    $ test_person = create_random_person()
    $ test_person.set_title("Tester")
    $ test_person.draw_person()
    $ test_room = Room()
    $ test_room.add_object(make_floor())
    $ test_room.add_object(make_bed())
    $ test_room.add_object(make_chair())
    $ test_room.add_object(make_desk())
    $ mc.change_location(test_room)

    "Starting encounter with forced position but without supporting Sluttiness."
    call fuck_person(test_person, start_position = blowjob)
    menu:
        "Girl immediately wanted to change position.":
            pass

        "Test failed.":
            return False

    $ mc.change_energy(100)
    $ test_person.change_energy(100)

    "Let's get her a little more comfortable and willing."
    $ test_person.change_slut_temp(100)
    $ test_person.change_slut_core(100)
    $ test_person.change_obedience(100)
    $ test_person.apply_outfit(Outfit("Nude"))
    $ test_person.draw_person()

    "Starting encounter with forced missionary, skipped intro."
    call fuck_person(test_person, start_position = missionary, skip_intro = True)
    menu:
        "Started in missionary, no intro.":
            pass

        "Test failed.":
            return False

    $ mc.change_energy(100)
    $ test_person.change_energy(100)
    "Starting encounter with girl in charge."
    call fuck_person(test_person, girl_in_charge = True)
    menu:
        "Girl was in charge.":
            pass

        "Test failed.":
            return False

    $ mc.change_energy(100)
    $ test_person.change_energy(100)
    "Starting encounter with forced, locked position."
    call fuck_person(test_person, start_position = skull_fuck, position_locked = True)
    menu:
        "Unable to change position.":
            pass

        "Test failed.":
            return False

    $ mc.change_energy(100)
    $ test_person.change_energy(100)
    "Starting encounter with forced missionary, no condom ask."
    call fuck_person(test_person, start_position = missionary, skip_condom = True)
    menu:
        "No condom asked for.":
            pass

        "Test failed.":
            return False

    $ mc.change_location(bedroom)
    return True
