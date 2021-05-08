init 1 python:
    integration_test_labels.append("give_serum_integration_test")

label give_serum_integration_test():
    "Testing ability to give serum to girl. Giving you doses of premade serum"
    $ test_serum = SerumDesign()
    $ test_serum.name = "Integration Test Design"
    $ test_serum.add_trait(primitive_serum_prod)
    $ test_serum.add_trait(simple_aphrodesiac)
    $ mc.inventory.change_serum(test_serum, 1)

    $ test_person = create_random_person()
    $ test_person.draw_person()
    "Give serum to girl. Sluttiness should increase."
    call give_serum(test_person)

    menu:
        "Serum given, effects added.":
            pass

        "Test failed.":
            return False

    return True
