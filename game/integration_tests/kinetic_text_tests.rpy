init 1 python:
    integration_test_labels.append("kinetic_text_test")


label kinetic_text_test():
    $ the_person = mom
    $ phrase ="cum, cock!, dick, pussy, fuck, pRegNanT, knocked up! knock me up, preg me, oh my GOD!"
    "Testing text normally:"
    $ renpy.say(mom, phrase)
    "Now testing with high arousal. All text should animate and have trance desauturation."
    $ mom.add_role(heavy_trance_role)
    $ mom.arousal = 100
    $ renpy.say(mom, phrase)
    $ mom.arousal = 0
    $ mom.remove_role(heavy_trance_role)
    menu:
        "Tests successful.":
            return True

        "Tests failed.":
            return False
