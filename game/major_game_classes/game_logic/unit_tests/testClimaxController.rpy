init 0 python:
    class TestClimaxController(unittest.TestCase):
        def test_init(self):
            test_controller = ClimaxController(["Face","face"],["Tits","tits"])

            self.assertIsInstance(test_controller, ClimaxController)

        def test_get_climax_multiplier(self):
            test_controller = ClimaxController(["Face","face"],["Tits","tits"],["Pussy","pussy"],["Body","body"])
            mc.condom = False

            self.assertEqual(test_controller.get_climax_multiplier("face"), 1.25)
            self.assertEqual(test_controller.get_climax_multiplier("tits"), 1.25)
            self.assertEqual(test_controller.get_climax_multiplier("body"), 1.0)
            self.assertEqual(test_controller.get_climax_multiplier("pussy"), 2.0)

            mc.condom = True

            self.assertEqual(test_controller.get_climax_multiplier("pussy"), 1.5)

        def test_show_menu(self):
            test_controller = ClimaxController(["Face","face"],["Tits","tits"],["Pussy","pussy"],["Body","body"])

            test_controller.show_climax_menu() #TODO: See what this actually does.

            self.assertTrue(True) #TODO: WRite proper check when we know what happens with this test.

        def test_do_clarity_release(self):
            test_person = create_random_person()
            test_controller = ClimaxController(["Face","face"],["Tits","tits"],["Pussy","pussy"],["Body","body"])
            test_controller.set_climax_type("body")
            mc.locked_clarity = 0
            mc.free_clarity = 0
            mc.masturbation_novelty = 100
            mc.change_locked_clarity(100, add_to_log = False)
            test_controller.do_clarity_release(test_person)

            self.assertEqual(mc.locked_clarity, 0)
            self.assertEqual(mc.free_clarity, 100)
            self.assertEqual(test_person.novelty, 95)

            mc.free_clarity = 0
            mc.change_locked_clarity(200, add_to_log = False)
            test_controller.do_clarity_release(test_person)

            self.assertEqual(mc.locked_clarity, 0)
            self.assertEqual(mc.free_clarity, 190)
            self.assertEqual(test_person.novelty, 90)

            mc.free_clarity = 0
            mc.change_locked_clarity(100, add_to_log = False)
            test_controller.set_climax_type("masturbation")
            test_controller.do_clarity_release()

            self.assertEqual(mc.locked_clarity, 0)
            self.assertEqual(mc.free_clarity, 50)
            self.assertEqual(mc.masturbation_novelty, 95)
            self.assertEqual(test_person.novelty, 90)
