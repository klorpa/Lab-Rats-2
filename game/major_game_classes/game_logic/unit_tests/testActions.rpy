init 0 python:
    def action_test_requirement_true():
        return True

    def action_test_requirement_false():
        return False

    def action_test_requirement_variable(variable):
        return not variable

    class TestAction(unittest.TestCase):
        def test_init(self):
            test_action = Action("Test action", action_test_requirement_true, "action_test_true")

            self.assertIsInstance(test_action, Action)

        def test_compare(self):
            test_action = Action("Test action", action_test_requirement_true, "action_test_true")
            other_action = Action("Test action", action_test_requirement_true, "action_test_true")

            self.assertEqual(test_action, other_action)

            other_action = Action("Test action", action_test_requirement_false, "action_test_true")

            self.assertNotEqual(test_action, other_action)

        def test_check_requirement(self):
            test_action = Action("Test action", action_test_requirement_variable, "action_test_true")

            self.assertTrue(test_action.check_requirement(False))
            self.assertFalse(test_action.check_requirement(True))
            self.assertTrue(test_action.is_action_enabled(False))
            self.assertFalse(test_action.is_action_enabled(True))

            test_action = Action("Test action", action_test_requirement_variable, "action_test_true", requirement_args = True)

            self.assertFalse(test_action.check_requirement())
            self.assertFalse(test_action.is_action_enabled())

            test_action = Action("Test action", action_test_requirement_variable, "action_test_true", requirement_args = False)

            self.assertTrue(test_action.check_requirement())
            self.assertTrue(test_action.is_action_enabled())

        def test_work_crisis_helper_functions(self):
            mc.change_location(downtown)

            day = 0 #Set the time of day so we can be sure we should be open
            global time_of_day
            time_of_day = 3

            person_one = create_random_person()
            person_two = create_random_person()

            person_one.generate_home()
            person_two.generate_home()

            self.assertIsInstance(person_one.home, Room)
            self.assertIsInstance(person_two.home, Room)

            lobby.add_person(person_one) #Need to avoid putting them downtown, because they might actually work there
            lobby.add_person(person_two)

            self.assertFalse(person_at_home(person_one))
            self.assertFalse(person_at_work(person_one))

            self.assertFalse(in_research_with_other())
            self.assertFalse(in_production_with_other())
            self.assertFalse(anyone_else_in_office())

            mc.business.add_employee_research(person_one)
            lobby.move_person(person_one, rd_division)

            self.assertFalse(person_at_home(person_one))
            self.assertTrue(person_at_work(person_one))

            mc.business.add_employee_production(person_two)
            lobby.move_person(person_two, p_division)

            self.assertFalse(anyone_else_in_office())

            mc.change_location(rd_division)
            self.assertTrue(in_research_with_other())
            self.assertTrue(in_production_with_other())

            mc.change_location(p_division)
            self.assertTrue(in_research_with_other())
            self.assertTrue(in_production_with_other())

            self.assertTrue(anyone_else_in_office())

            mc.business.remove_employee(person_one)
            mc.business.remove_employee(person_two)

            self.assertTrue(person_one.home.has_person(person_one))
            self.assertFalse(person_at_work(person_one))

        def test_home_crisis_helper_functions(self):
            day = 0 #Set the time of day so we can be sure we should be open
            global time_of_day
            time_of_day = 3

            mc.change_location(downtown)
            self.assertFalse(mc_at_work())
            self.assertFalse(mc_at_home())

            mc.change_location(rd_division)
            self.assertTrue(mc_at_work())
            self.assertFalse(mc_at_home())

            mc.change_location(bedroom)
            self.assertFalse(mc_at_work())
            self.assertTrue(mc_at_home())

        # def test_action_call(self): #TODO: Implement a label testing framework as well.
        #     test_action = Action("Test action", action_test_requirement_true, "action_test_true")
        #
        #     self.assertTrue(test_action.call_action())
        #
        #     test_action = Action("Test action", action_test_requirement_true, "action_test_false")
        #
        #     self.assertFalse(test_action.call_action())
        #
        #     test_action = Action("Test action", action_test_requirement_true, "action_test_variable")
        #
        #     self.assertTrue(test_action.call_action(False))
        #     self.assertFalse(test_action.call_action(True))
        #
        #     test_action = Action("Test action", action_test_requirement_true, "action_test_variable", args = True)
        #
        #     self.assertFalse(test_action.call_action())
        #
        #     test_action = Action("Test action", action_test_requirement_true, "action_test_variable", args = False)
        #
        #     self.assertTrue(test_action.call_action())

label action_test_true():
    "Test"
    return True

label action_test_false():
    "Test"
    return False

label action_test_variable(variable):
    "Test"
    return not variable
