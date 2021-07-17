init 1 python:
    integration_test_labels.append("outfit_design_integration_test")

label outfit_design_integration_test():
    "Running outfit design test. Design an outfit."
    call outfit_master_manager(show_underwear = False, show_overwear = False)
    "Now design an overwear set."
    call outfit_master_manager(show_outfits = False, show_overwear = True, show_underwear = False)
    "Now design an underwear set."
    call outfit_master_manager(show_outfits = False, show_overwear = False, show_underwear = True)

    menu:
        "All outfits designed successfully.":
            pass

        "Test failed.":
            return False

    "Now select an outfit."
    $ test_person = create_random_person()
    call outfit_master_manager(show_make_new = False, show_export = False, show_modify = False, show_duplicate = False, show_delete = False)
    $ the_outfit = _return
    if the_outfit is None or not isinstance(the_outfit, Outfit):
        "Outfit incorrectly returned. Test failed."
        return False
    "Testing outfit on person."
    $ test_person.draw_person()
    "Now changing her into new outfit."
    $ test_person.apply_outfit(the_outfit)
    $ test_person.draw_person()
    menu:
        "Outfit successfully worn.":
            pass

        "Test failed.":
            return False

    "Now test deleting all of those outfits."
    call outfit_master_manager(show_make_new = False, show_export = False, show_modify = False, show_duplicate = False)
    "Redrawing test girl to ensure nothing has changed with her reference."
    $ test_person.draw_person()
    menu:
        "Outfits removed, girl still dressed.":
            pass

        "Test failed.":
            return False

    return True
