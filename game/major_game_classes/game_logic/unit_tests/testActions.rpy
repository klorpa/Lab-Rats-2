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
