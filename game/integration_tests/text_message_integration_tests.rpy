init 1 python:
    integration_test_labels.append("run_text_message_integration_tests")

label run_text_message_integration_tests():
    $ the_person = mom
    $ other_person = lily
    "Testing text messaging system. Testing with [the_person.title]."
    the_person "Hello, this should be a normal test!"
    $ mc.start_text_convo(the_person)
    the_person "And this should be shown on the phone."
    "This narration should be shown as normal."
    $ mc.phone.add_system_message(the_person, "This is a system message.")
    $ mc.pause_text_convo()
    other_person "This dialogue with [other_person.title] should display as normal."
    $ mc.resume_text_convo()
    the_person "And this should be back on the phone."
    menu:
        "All tests completed.":
            pass

        "Test failed.":
            $ mc.end_text_convo()
            return False

    $ mc.end_text_convo()
    return True
