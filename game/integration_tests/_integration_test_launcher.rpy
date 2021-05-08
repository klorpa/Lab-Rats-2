init -1 python:
    def integration_test_dev_requirement():
        if config.developer:
            return True
        else:
            return False

init 0 python:
    integration_test_labels = [] # You can add your own integration test labels to this list to have them run. Make sure they are added in init step 1 or later!


label run_integration_tests():
    "Reminder: \">\" will enable fast skipping. Integration tests may have side effects in main game."

    menu:
        "Run all integration tests.":
            $ test_results = {}
            $ has_failure = False

            $ test_count = 0
            while test_count < len(integration_test_labels): #Needs to be done in Ren'py to prevent first integration test from returning for the full stack.
                $ integration_test = integration_test_labels[test_count]
                $ renpy.call(integration_test)
                if not _return:
                    $ has_failure = True
                $ log_message("TEST " + integration_test + " : " + str(_return))
                $ test_count += 1



            if has_failure:
                "Integration test failure. See log file for details."

            else:
                "Integration tests successful."

        "Run specific integraiton test.":
            python:
                choices = []
                for integration_test in integration_test_labels:
                    choices.append([integration_test, integration_test])

                test_choice = renpy.display_menu(choices)
                renpy.call(test_choice) #TODO: Also wrap this up to catch exceptions.
            $ log_message("TEST " + test_choice + " : " + str(_return))

            if not _return:
                "Integration test failure. See log file for details."

            else:
                "Integration tests successful."

    #TODO: Things to integration test:
    # 12) chat actions
    # Set daily serum doses
