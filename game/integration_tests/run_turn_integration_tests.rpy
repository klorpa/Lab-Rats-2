init 1 python:
    integration_test_labels.append("run_world_turn_integration_test")

label run_world_turn_integration_test():
    "Testing advancing time."
    call advance_time()
    "..."
    call advance_time()
    "..."
    call advance_time()
    "..."
    call advance_time()
    "..."
    call advance_time()

    menu:
        "Tests successful.":
            return True

        "Tests failed.":
            return False
