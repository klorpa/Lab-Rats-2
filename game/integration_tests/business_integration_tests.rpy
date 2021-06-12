init 1 python:
    integration_test_labels.append("basic_business_tests")
    integration_test_labels.append("hiring_integration_test")
    integration_test_labels.append("business_research_integration_tests")
    integration_test_labels.append("business_set_uniforms_integration_test")

label basic_business_tests(): #TODO:we can probably automate these tests (or build unit tests for the specific business actions)
    "Testing basic business job functionality."
    $ mc.business.team_effectiveness = 75
    "Starting with HR. Effectiveness set to 75 and should rise."
    call hr_work_action_description
    menu:
        "Team Efficiency rose.":
            pass

        "Test failed.":
            return False

    $ test_trait = SerumTrait("Test Trait", "This is a test trait")
    $ mc.business.set_serum_research(test_trait)
    "Now checking research work. Setting research to fake trait. Should either rise or finish being researched."
    call research_work_action_description
    menu:
        "Research proceeded.":
            pass

        "Test failed.":
            return False

    $ mc.business.supply_count = 0
    "Testing supply procurement. Setting supplies to 0, should rise after purchase."
    call supplies_work_action_description
    menu:
        "Supplies purchased, cash paid.":
            pass

        "Test failed.":
            return False


    $ test_serum = SerumDesign()
    $ test_serum.name = "Integration Test Desgin"
    $ test_serum.add_trait(primitive_serum_prod)
    $ test_serum.add_trait(basic_med_app)
    $ mc.business.sale_inventory.change_serum(test_serum, 5)
    "Testing marketing work. Giving company inventory several doses of serum. Funds should rise after sales."
    call market_work_action_description
    menu:
        "Funds increased, doses gone.":
            pass

        "Test failed.":
            return False

    $ mc.business.clear_production()
    $ mc.business.change_production(test_serum, 0)
    $ mc.int += 100
    $ mc.business.supply_count += 1000
    "Testing production work. Should convert materials into serum production."
    call production_work_action_description
    $ mc.int += -100
    menu:
        "Supplies spent, doses created.":
            pass

        "Test failed.":
            return False
    return True

label hiring_integration_test():
    "Testing screen based business activities."
    "Starting by hiring employee. Hire new employee."
    call interview_action_description

    menu:
        "Employee hired and placed correctly.":
            pass

        "Test failed.":
            return False

    "Reject all potential candidates."
    call interview_action_description

    menu:
        "Successfully exited interview UI.":
            pass

        "Test failed.":
            return False
    return True

label business_research_integration_tests():
    "Testing research selection. Select, unlock, and begin researching new topic."
    $ mc.add_clarity(500)
    call research_select_action_description

    menu:
        "Research changed successfully.":
            pass

        "Test failed.":
            return False


    $ basic_med_app.unlock_trait(pay_clarity = False)
    $ basic_med_app.unlocked = True

    $ simple_aphrodesiac.unlock_trait(pay_clarity = False)
    $ simple_aphrodesiac.unlocked = True
    "Testing serum design. Design a new serum."

    call serum_design_action_description

    "Now begin researching the serum design."
    call research_select_action_description

    menu:
        "Serum begun research properly.":
            pass

        "Test failed.":
            return False

    return True

label business_set_production_integration_test():
    "Testing production setting ability. Giving you new serum design."
    $ test_serum = SerumDesign()
    $ test_serum.name = "Integration Test Design"
    $ test_serum.add_trait(primitive_serum_prod)
    $ test_serum.add_trait(simple_aphrodesiac)
    $ test_serum.unlocked = True
    $ test_serum.researched = True
    $ mc.business.serum_designs.append(test_serum)
    "Set production to new serum design."
    call production_select_action_description
    menu:
        "Production set successfully.":
            pass

        "Test failed.":
            return False
    $ mc.business.supply_count = 1000
    $ mc.int += 50

    "Now running production to produce serum."
    call production_work_action_description
    menu:
        "Doses of serum design produced.":
            pass

        "Test failed.":
            return False

    "Now set an autosell threshold for the trait."
    call production_select_action_description
    "Producing more serum..."
    call production_work_action_description
    menu:
        "Doses of serum made, moved to sales.":
            pass

        "Test failed.":
            return False
    $ mc.int += -50
    return True

label business_set_uniforms_integration_test():
    "Testing uniform creation. Create overwear uniform for full company."
    $ strict_uniform_policy.buy_policy(ignore_cost = True)
    $ strict_uniform_policy.apply_policy()
    call set_uniform_description
    $ test_person = create_random_person()
    $ mc.business.add_employee_research(test_person)
    $ test_person.wear_uniform()
    $ test_person.draw_person()
    menu:
        "Overwear uniform properly applied.":
            pass

        "Test failed.":
            return False

    "Testing uniform removal."
    call set_uniform_description
    $ test_person.planned_uniform = None #Clear planned uniform so she replans
    $ test_person.wear_uniform()
    $ test_person.draw_person()
    menu:
        "Uniform properly cleared.":
            pass

        "Test failed.":
            return False

    "Create full outfit for company."
    $ strict_uniform_policy.buy_policy(ignore_cost = True)
    $ strict_uniform_policy.apply_policy()
    $ relaxed_uniform_policy.buy_policy(ignore_cost = True)
    $ relaxed_uniform_policy.apply_policy()
    $ casual_uniform_policy.buy_policy(ignore_cost = True)
    $ casual_uniform_policy.apply_policy()
    $ reduced_coverage_uniform_policy.buy_policy(ignore_cost = True)
    $ reduced_coverage_uniform_policy.apply_policy()
    call set_uniform_description
    $ test_person.wear_uniform()
    $ test_person.draw_person()
    menu:
        "Uniform applied properly.":
            pass

        "Test failed.":
            return False

    $ mc.business.remove_employee(test_person)
    return True
