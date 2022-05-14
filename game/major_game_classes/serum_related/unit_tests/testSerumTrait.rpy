init 0 python:
    def test_trait_on_apply(the_person, the_serum, add_to_log = False):
        the_serum.effects_dict["on_apply"] = True

    def test_trait_on_remove(the_person, the_serum, add_to_log = False):
        the_serum.effects_dict["on_remove"] = True

    def test_trait_on_turn(the_person, the_serum, add_to_log = False):
        the_serum.effects_dict["on_turn"] = True

    def test_trait_on_move(the_person, the_serum, add_to_log = False):
        the_serum.effects_dict["on_move"] = True

    def test_trait_on_day(the_person, the_serum, add_to_log = False):
        the_serum.effects_dict["on_day"] = True

    class TestSerumTrait(unittest.TestCase):
        def setUp(self):
            self.test_serum_trait = SerumTrait("Test trait", "This is a test trait")

            self.complex_test_serum_trait = SerumTrait("Complex trait", "This is a complex trait",
                positive_slug = "Positive slug", negative_slug = "Negative slug",
                research_added = 40, slots_added = 1, production_added = 20,
                base_side_effect_chance = 20, clarity_added = 20,
                on_apply = test_trait_on_apply,
                on_remove = test_trait_on_remove,
                on_turn = test_trait_on_turn,
                on_move = test_trait_on_move,
                on_day = test_trait_on_day,
                requires = None,
                tier = 0,
                start_researched = False,
                research_needed = 100,
                exclude_tags = None,
                is_side_effect = False,
                clarity_cost = 50,
                start_unlocked = False)

        def test_init(self):
            self.assertIsInstance(self.test_serum_trait, SerumTrait)
            self.assertIsInstance(self.complex_test_serum_trait, SerumTrait)

        def test_run_ons(self):
            test_person = create_random_person()
            test_serum = SerumDesign()
            test_serum.effects_dict["unit tester"] = self
            self.complex_test_serum_trait.run_on_apply(test_person, test_serum)
            self.complex_test_serum_trait.run_on_remove(test_person, test_serum)
            self.complex_test_serum_trait.run_on_turn(test_person, test_serum)
            self.complex_test_serum_trait.run_on_move(test_person, test_serum)
            self.complex_test_serum_trait.run_on_day(test_person, test_serum)

            self.assertTrue(test_serum.effects_dict.get("on_apply",False))
            self.assertTrue(test_serum.effects_dict.get("on_remove",False))
            self.assertTrue(test_serum.effects_dict.get("on_turn",False))
            self.assertTrue(test_serum.effects_dict.get("on_move",False))
            self.assertTrue(test_serum.effects_dict.get("on_day",False))


        def test_add_research(self):
            self.assertFalse(self.complex_test_serum_trait.researched)
            self.assertEqual(self.complex_test_serum_trait.current_research, 0)

            self.complex_test_serum_trait.add_research(50)

            self.assertFalse(self.complex_test_serum_trait.researched)
            self.assertEqual(self.complex_test_serum_trait.current_research, 50)

            self.complex_test_serum_trait.add_research(60)

            self.assertTrue(self.complex_test_serum_trait.researched)
            self.assertEqual(self.complex_test_serum_trait.current_research, 10)
            self.assertEqual(self.complex_test_serum_trait.mastery_level, 1)

            self.complex_test_serum_trait.add_research(100)

            self.assertEqual(self.complex_test_serum_trait.current_research, 10)
            self.assertEqual(self.complex_test_serum_trait.mastery_level, 1.5)

            self.complex_test_serum_trait.add_research(240)
            self.assertEqual(self.complex_test_serum_trait.current_research, 50)
            self.assertEqual(self.complex_test_serum_trait.mastery_level, 2.5)


        def test_unlock(self):
            self.assertFalse(self.test_serum_trait.unlocked)
            self.assertFalse(self.complex_test_serum_trait.unlocked)

            mc.add_clarity(200, add_to_log = False)
            start_clarity = mc.free_clarity
            self.test_serum_trait.unlock_trait()

            self.assertTrue(self.test_serum_trait.unlocked)
            self.assertEqual(mc.free_clarity, start_clarity - self.test_serum_trait.clarity_cost)

            start_clarity = mc.free_clarity

            self.complex_test_serum_trait.unlock_trait(pay_clarity = False)

            self.assertTrue(self.complex_test_serum_trait.unlocked)
            self.assertEqual(mc.free_clarity, start_clarity)

        def test_required(self):
            test_trait_one = SerumTrait("Base trait", "First trait that will be required")
            test_trait_two = SerumTrait("Requiring trait", "Second trait that requries the first", requires = test_trait_one)
            test_trait_three = SerumTrait("High tier trait", "Requires higher tier research, but nothing else", tier = 1)

            mc.business.research_tier = 0

            self.assertTrue(test_trait_one.has_required())
            self.assertFalse(test_trait_two.has_required())
            self.assertFalse(test_trait_three.has_required())

            test_trait_one.add_research(200)

            self.assertTrue(test_trait_one.researched)

            self.assertTrue(test_trait_one.has_required())
            self.assertTrue(test_trait_two.has_required())
            self.assertFalse(test_trait_three.has_required())

            mc.business.research_tier = 1

            self.assertTrue(test_trait_one.has_required())
            self.assertTrue(test_trait_two.has_required())
            self.assertTrue(test_trait_three.has_required())

        def test_is_similar(self):
            test_trait_one = SerumTrait("Test Trait", "Trait 1")
            test_trait_two = SerumTrait("Different Trait", "Trait 2")
            test_trait_three = SerumTrait("Test Trait", "Trait 1")

            self.assertFalse(test_trait_one.is_similar(test_trait_two))
            self.assertFalse(test_trait_two.is_similar(test_trait_one))

            self.assertFalse(test_trait_two.is_similar(test_trait_one))
            self.assertFalse(test_trait_two.is_similar(test_trait_three))

            self.assertTrue(test_trait_one.is_similar(test_trait_three))
            self.assertTrue(test_trait_three.is_similar(test_trait_one))

            test_trait_one.physical_aspect = 10
            self.assertFalse(test_trait_one.is_similar(test_trait_three))

            test_trait_three.physical_aspect = 10
            self.assertTrue(test_trait_three.is_similar(test_trait_one))
