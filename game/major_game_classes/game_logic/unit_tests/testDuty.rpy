init 0 python:
    def testduty_test_function(test_person):
        test_person.event_triggers_dict["testduty_test_variable"] = True

    class TestDuty(unittest.TestCase):
        def test_init(self):
            new_duty = Duty("Test duty",
                "A duty set up for unit testing!")

            self.assertIsInstance(new_duty, Duty)

        def test_has_duty(self):
            new_duty = Duty("Test duty",
                "A duty set up for unit testing!")

            test_person = create_random_person()

            self.assertEqual(test_person.duties, [])
            self.assertNotIn(new_duty, test_person.duties)

            test_person.add_duty(new_duty)
            self.assertIn(new_duty, test_person.duties)

            new_duty_2 = Duty("Test duty 2",
                "Another duty set up for unit testing!")

            self.assertNotIn(new_duty_2, test_person.duties)

        def test_add_remove_duty(self):
            new_duty = Duty("Test duty",
                "A duty set up for unit testing!")

            new_duty_2 = Duty("Test duty 2",
                "Another duty set up for unit testing!")

            test_person = create_random_person()
            self.assertFalse(test_person.has_duty(new_duty))

            test_person.add_duty(new_duty)
            self.assertTrue(test_person.has_duty(new_duty))
            self.assertFalse(test_person.has_duty(new_duty_2))

            test_person.add_duty(new_duty_2)
            self.assertTrue(test_person.has_duty(new_duty))
            self.assertTrue(test_person.has_duty(new_duty_2))

            test_person.remove_duty(new_duty)
            self.assertFalse(test_person.has_duty(new_duty))
            self.assertTrue(test_person.has_duty(new_duty_2))

        def test_on_change_functions(self):
            new_duty = Duty("Test duty",
                "A duty set up for testing the various on_@ functions!",
                on_turn_function = testduty_test_function,
                on_move_function = testduty_test_function,
                on_day_function = testduty_test_function,
                on_apply_function = testduty_test_function,
                on_remove_function = testduty_test_function)

            test_person = create_random_person()
            test_person.add_duty(new_duty)

            self.assertTrue(test_person.has_duty(new_duty))
            self.assertTrue(callable(new_duty.on_turn_function))
            self.assertTrue(callable(new_duty.on_move_function))
            self.assertTrue(callable(new_duty.on_day_function))
            self.assertTrue(callable(new_duty.on_apply_function))
            self.assertTrue(callable(new_duty.on_remove_function))

            test_person.event_triggers_dict["testduty_test_variable"] = False
            new_duty.on_turn(test_person)
            self.assertTrue(test_person.event_triggers_dict.get("testduty_test_variable", False))

            test_person.event_triggers_dict["testduty_test_variable"] = False
            new_duty.on_move(test_person)
            self.assertTrue(test_person.event_triggers_dict.get("testduty_test_variable", False))

            test_person.event_triggers_dict["testduty_test_variable"] = False
            new_duty.on_day(test_person)
            self.assertTrue(test_person.event_triggers_dict.get("testduty_test_variable", False))

            test_person.event_triggers_dict["testduty_test_variable"] = False
            new_duty.on_apply(test_person)
            self.assertTrue(test_person.event_triggers_dict.get("testduty_test_variable", False))

            test_person.event_triggers_dict["testduty_test_variable"] = False
            new_duty.on_remove(test_person)
            self.assertTrue(test_person.event_triggers_dict.get("testduty_test_variable", False))
