init 0 python:
    class TestSerumDesign(unittest.TestCase):
        def test_init(self):
            test_serum_design = SerumDesign()

            self.assertIsInstance(test_serum_design, SerumDesign)

        def test_add_trait(self):
            test_serum_design = SerumDesign()

            self.assertFalse(test_serum_design.traits)
            self.assertFalse(test_serum_design.side_effects)

            test_serum_design.add_trait(primitive_serum_prod)

            self.assertIn(primitive_serum_prod, test_serum_design.traits)
            self.assertFalse(test_serum_design.side_effects)

            test_serum_design.add_trait(bad_reputation, is_side_effect = True)

            self.assertIn(bad_reputation, test_serum_design.side_effects)

        def test_refused_add(self):
            test_serum_design = SerumDesign()
            test_serum_design.add_trait(primitive_serum_prod)

            self.assertIn(primitive_serum_prod, test_serum_design.traits)

            test_serum_design.add_trait(primitive_serum_prod)

            self.assertIn(primitive_serum_prod, test_serum_design.traits)

            test_serum_design.remove_trait(primitive_serum_prod)

            self.assertFalse(test_serum_design.traits)

        def test_remove_trait(self):
            test_serum_design = SerumDesign()
            test_serum_design.add_trait(primitive_serum_prod)

            self.assertIn(primitive_serum_prod, test_serum_design.traits)

            test_serum_design.remove_trait(primitive_serum_prod)

            self.assertFalse(test_serum_design.traits)

        def test_is_same_design(self):
            test_serum_design = SerumDesign()
            test_serum_design.add_trait(primitive_serum_prod)
            other_serum_design = SerumDesign()

            self.assertFalse(test_serum_design.is_same_design(other_serum_design))
            self.assertFalse(other_serum_design.is_same_design(test_serum_design))

            other_serum_design.add_trait(primitive_serum_prod)

            self.assertTrue(test_serum_design.is_same_design(other_serum_design))
            self.assertTrue(other_serum_design.is_same_design(test_serum_design))

            test_serum_design.remove_trait(primitive_serum_prod)

            self.assertFalse(test_serum_design.is_same_design(other_serum_design))
            self.assertFalse(other_serum_design.is_same_design(test_serum_design))

        def test_is_same_design_side_effect(self):
            test_serum_design = SerumDesign()
            test_serum_design.add_trait(primitive_serum_prod)
            other_serum_design = SerumDesign()
            other_serum_design.add_trait(primitive_serum_prod)

            self.assertTrue(test_serum_design.is_same_design(other_serum_design))
            self.assertTrue(other_serum_design.is_same_design(test_serum_design))

            test_serum_design.add_trait(bad_reputation, is_side_effect = True)

            self.assertFalse(test_serum_design.is_same_design(other_serum_design))
            self.assertFalse(other_serum_design.is_same_design(test_serum_design))

            other_serum_design.add_trait(bad_reputation, is_side_effect = True)

            self.assertTrue(test_serum_design.is_same_design(other_serum_design))
            self.assertTrue(other_serum_design.is_same_design(test_serum_design))

            test_serum_design.remove_trait(bad_reputation)
            test_serum_design.add_trait(bad_reputation)

            self.assertFalse(test_serum_design.is_same_design(other_serum_design))
            self.assertFalse(other_serum_design.is_same_design(test_serum_design))

        def test_has_tag(self):
            test_serum_design = SerumDesign()

            self.assertFalse(test_serum_design.has_tag("Production"))

            test_serum_design.add_trait(primitive_serum_prod)

            self.assertTrue(test_serum_design.has_tag("Production"))
            self.assertFalse(test_serum_design.has_tag("Suggest"))

            test_serum_design.add_trait(suggestion_drugs_trait)

            self.assertTrue(test_serum_design.has_tag("Suggest"))

        def test_duration_counter(self):
            test_serum_design = SerumDesign()
            test_serum_design.add_trait(primitive_serum_prod)

            self.assertEqual(test_serum_design.duration, 3)
            self.assertEqual(test_serum_design.duration_counter, 0)

            self.assertFalse(test_serum_design.duration_expired())

            test_person = create_random_person()

            test_serum_design.run_on_turn(test_person)

            self.assertFalse(test_serum_design.duration_expired())
            self.assertEqual(test_serum_design.duration_counter, 1)

            test_serum_design.run_on_turn(test_person)
            test_serum_design.run_on_turn(test_person)

            self.assertTrue(test_serum_design.duration_expired())

            test_serum_design.run_on_turn(test_person)

            self.assertTrue(test_serum_design.duration_expired())

        def test_add_research(self):
            test_serum_design = SerumDesign()
            test_serum_design.add_trait(primitive_serum_prod)

            self.assertEqual(test_serum_design.current_research, 0)
            self.assertFalse(test_serum_design.researched)

            test_serum_design.add_research(1)

            self.assertFalse(test_serum_design.researched)

            test_serum_design.add_research(1000)

            self.assertTrue(test_serum_design.researched)

        def test_unlock(self):
            test_serum_design = SerumDesign()
            test_serum_design.add_trait(primitive_serum_prod)

            self.assertFalse(test_serum_design.unlocked)

            serum_cost = primitive_serum_prod.clarity_added
            mc.add_clarity(3*serum_cost, add_to_log = False)
            starting_clarity = mc.free_clarity
            test_serum_design.unlock_design()

            self.assertTrue(test_serum_design.unlocked)
            self.assertEqual(mc.free_clarity, starting_clarity - serum_cost)

            test_serum_design = SerumDesign()
            test_serum_design.add_trait(primitive_serum_prod)

            self.assertFalse(test_serum_design.unlocked)

            start_clarity = mc.free_clarity
            test_serum_design.unlock_design(pay_clarity = False)

            self.assertTrue(test_serum_design.unlocked)
            self.assertEqual(mc.free_clarity, start_clarity)
