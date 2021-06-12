init 0 python:
    class TestOutfit(unittest.TestCase):
        def test_init(self):
            test_outfit = Outfit("test outfit")

            self.assertIsInstance(test_outfit, Outfit)

        def test_copy(self):
            test_outfit = Outfit("test outfit")
            test_outfit.add_upper(bra.get_copy())
            test_outfit.add_upper(tshirt.get_copy())
            test_outfit.add_lower(jeans.get_copy())
            test_outfit.add_lower(panties.get_copy())
            test_outfit.add_feet(heels.get_copy())
            test_outfit.add_accessory(sunglasses.get_copy())
            other_outfit = test_outfit.get_copy()

            self.assertIsNot(test_outfit, other_outfit)

        def test_add_clothing(self):
            test_outfit = Outfit("test outfit")
            test_outfit.add_upper(bra.get_copy())
            test_outfit.add_upper(tshirt.get_copy())
            test_outfit.add_lower(jeans.get_copy())
            test_outfit.add_lower(panties.get_copy())
            test_outfit.add_feet(heels.get_copy())
            test_outfit.add_accessory(sunglasses.get_copy())

            self.assertIn(bra, test_outfit.upper_body)
            self.assertIn(tshirt, test_outfit.upper_body)
            self.assertIn(jeans, test_outfit.lower_body)
            self.assertIn(panties, test_outfit.lower_body)
            self.assertIn(heels, test_outfit.feet)
            self.assertIn(sunglasses, test_outfit.accessories)

        def test_get_draw_list(self):
            test_person = create_random_person()
            test_outfit = Outfit("test outfit")
            test_outfit.add_upper(bra.get_copy())
            test_outfit.add_upper(tshirt.get_copy())
            test_outfit.add_lower(jeans.get_copy())
            test_outfit.add_lower(panties.get_copy())
            test_outfit.add_feet(heels.get_copy())
            test_outfit.add_accessory(sunglasses.get_copy())

            draw_list = test_outfit.generate_draw_list(test_person, "stand2")
            for draw_item in draw_list:
                self.assertIsInstance(draw_item, renpy.display.core.Displayable)

        def test_add_clothing(self):
            test_outfit = Outfit("test outfit")

            self.assertTrue(test_outfit.can_add_upper(tshirt))

            test_outfit.add_upper(tshirt.get_copy())

            self.assertFalse(test_outfit.can_add_upper(tshirt))

            test_outfit.add_upper(tshirt.get_copy())

            self.assertTrue(test_outfit.can_add_upper(bra))

            test_outfit.add_upper(bra.get_copy())

            self.assertTrue(test_outfit.can_add_lower(jeans))

            test_outfit.add_lower(jeans.get_copy())

            self.assertFalse(test_outfit.can_add_lower(jeans))

            test_outfit.add_lower(panties.get_copy())

            self.assertTrue(test_outfit.can_add_feet(heels.get_copy()))

            test_outfit.add_feet(heels.get_copy())

            self.assertTrue(test_outfit.can_add_accessory(sunglasses.get_copy()))

            test_outfit.add_accessory(sunglasses.get_copy())

            self.assertTrue(test_outfit.can_add_accessory(chandelier_earings.get_copy()))

            test_outfit.add_accessory(chandelier_earings.get_copy())

            self.assertFalse(test_outfit.can_add_accessory(chandelier_earings.get_copy()))

        def test_has_clothing(self):
            test_outfit = Outfit("test outfit")
            test_outfit.add_upper(bra.get_copy())
            test_outfit.add_upper(tshirt.get_copy())
            test_outfit.add_lower(jeans.get_copy())
            test_outfit.add_accessory(sunglasses.get_copy())

            self.assertTrue(test_outfit.has_clothing(jeans))
            self.assertTrue(test_outfit.has_clothing(tshirt))
            self.assertFalse(test_outfit.has_clothing(heart_pasties))
            self.assertTrue(test_outfit.has_clothing(sunglasses))

        def test_remove_clothing(self):
            test_person = create_random_person()
            test_outfit = Outfit("test outfit")
            test_outfit.add_upper(bra.get_copy())
            test_outfit.add_upper(tshirt.get_copy())
            test_outfit.add_lower(jeans.get_copy())
            test_outfit.add_lower(panties.get_copy())
            test_outfit.add_feet(heels.get_copy())
            test_outfit.add_accessory(sunglasses.get_copy())

            self.assertTrue(test_outfit.has_clothing(jeans))

            test_outfit.remove_clothing(jeans)

            self.assertFalse(test_outfit.has_clothing(jeans))
            self.assertTrue(test_outfit.has_clothing(panties))

            test_outfit.remove_clothing(panties)

            self.assertFalse(test_outfit.has_clothing(panties))

        def test_remove_clothing_list(self):
            test_outfit = Outfit("test outfit")
            test_outfit.add_upper(bra.get_copy())
            test_outfit.add_upper(tshirt.get_copy())
            test_outfit.add_lower(jeans.get_copy())
            test_outfit.add_lower(panties.get_copy())
            test_outfit.add_feet(heels.get_copy())
            test_outfit.add_accessory(sunglasses.get_copy())

            self.assertTrue(test_outfit.has_clothing(bra))
            self.assertTrue(test_outfit.has_clothing(tshirt))
            self.assertTrue(test_outfit.has_clothing(jeans))
            self.assertTrue(test_outfit.has_clothing(sunglasses))

            test_outfit.remove_clothing_list([bra, tshirt])

            self.assertFalse(test_outfit.has_clothing(bra))
            self.assertFalse(test_outfit.has_clothing(tshirt))
            self.assertTrue(test_outfit.has_clothing(jeans))

        def test_add_repeated_accessories(self):
            test_outfit = Outfit("test outfit")
            test_outfit.add_accessory(sunglasses.get_copy())

            self.assertTrue(test_outfit.has_clothing(sunglasses))
            self.assertTrue(test_outfit.can_add_accessory(lipstick))

            test_outfit.add_accessory(lipstick.get_copy())

            self.assertTrue(test_outfit.has_clothing(lipstick))
            self.assertFalse(test_outfit.can_add_accessory(lipstick))

            lipstick_count = 0
            for item in test_outfit.accessories:
                if item.is_similar(lipstick):
                    lipstick_count += 1
            self.assertEqual(lipstick_count, 1)

            test_outfit.add_accessory(lipstick.get_copy())

            lipstick_count = 0
            for item in test_outfit.accessories:
                if item.is_similar(lipstick):
                    lipstick_count += 1
            self.assertEqual(lipstick_count, 1)



    class TestOutfitStrip(unittest.TestCase):
        def setUp(self):
            test_outfit = Outfit("test outfit")
            test_outfit.add_upper(bra.get_copy())
            test_outfit.add_upper(tshirt.get_copy())
            test_outfit.add_lower(jeans.get_copy())
            test_outfit.add_lower(panties.get_copy())
            test_outfit.add_feet(heels.get_copy())
            test_outfit.add_accessory(sunglasses.get_copy())
            self.test_outfit = test_outfit

            test_person = create_random_person()
            test_person.apply_outfit(self.test_outfit)
            self.test_person = test_person

        def test_get_full_strip_list(self):
            strip_list = self.test_person.outfit.get_full_strip_list(strip_accessories = True)
            item_list = self.test_person.outfit.generate_clothing_list()
            for item in strip_list:
                self.assertIn(item, item_list)
            for item in item_list:
                self.assertIn(item, strip_list)

            strip_list = self.test_person.outfit.get_full_strip_list(strip_accessories = False)
            for item in strip_list:
                self.assertIn(item, item_list)
            self.assertNotIn(sunglasses, strip_list)

            strip_list = self.test_person.outfit.get_full_strip_list(strip_feet = False)
            for item in strip_list:
                self.assertIn(item, item_list)
            self.assertNotIn(heels, strip_list)

        def test_get_underwear_strip_list(self):
            strip_list = self.test_person.outfit.get_underwear_strip_list()

            self.assertIn(tshirt, strip_list)
            self.assertIn(jeans, strip_list)
            self.assertNotIn(bra, strip_list)
            self.assertNotIn(panties, strip_list)
            self.assertNotIn(heels, strip_list)

        def test_get_tit_strip_list(self):
            strip_list = self.test_person.outfit.get_tit_strip_list()

            self.assertIn(tshirt, strip_list)
            self.assertIn(bra, strip_list)
            self.assertNotIn(jeans, strip_list)
            self.assertNotIn(heels, strip_list)

        def test_get_vagina_strip_list(self):
            strip_list = self.test_person.outfit.get_vagina_strip_list()

            self.assertIn(jeans, strip_list)
            self.assertIn(panties, strip_list)
            self.assertNotIn(tshirt, strip_list)
            self.assertNotIn(bra, strip_list)
            self.assertNotIn(heels, strip_list)

        def test_get_half_off_to_tits_list(self):
            strip_list = self.test_person.outfit.get_half_off_to_tits_list()

            self.assertIn(tshirt, strip_list)
            self.assertIsNot(bra, strip_list)
            self.assertNotIn(jeans, strip_list)
            self.assertNotIn(heels, strip_list)

        def test_get_half_off_to_vagina(self):
            strip_list = self.test_person.outfit.get_half_off_to_vagina_list()

            self.assertIn(jeans, strip_list)
            self.assertIn(panties, strip_list)
            self.assertNotIn(tshirt, strip_list)
            self.assertNotIn(heels, strip_list)

        def test_strip_to_underwear(self):
            self.assertTrue(self.test_person.outfit.bra_covered())
            self.assertTrue(self.test_person.outfit.panties_covered())
            self.assertFalse(self.test_person.outfit.vagina_available())
            self.assertFalse(self.test_person.outfit.tits_available())

            self.test_person.outfit.strip_to_underwear()

            self.assertFalse(self.test_person.outfit.bra_covered())
            self.assertFalse(self.test_person.outfit.panties_covered())
            self.assertFalse(self.test_person.outfit.vagina_available())
            self.assertFalse(self.test_person.outfit.tits_available())

        def test_strip_to_tits(self):
            self.assertTrue(self.test_person.outfit.bra_covered())
            self.assertTrue(self.test_person.outfit.panties_covered())
            self.assertFalse(self.test_person.outfit.vagina_available())
            self.assertFalse(self.test_person.outfit.tits_available())

            self.test_person.outfit.strip_to_tits()

            self.assertTrue(self.test_person.outfit.tits_available())
            self.assertFalse(self.test_person.outfit.vagina_available())
            self.assertTrue(self.test_person.outfit.panties_covered())

        def test_strip_to_vagina(self):
            self.assertTrue(self.test_person.outfit.bra_covered())
            self.assertTrue(self.test_person.outfit.panties_covered())
            self.assertFalse(self.test_person.outfit.vagina_available())
            self.assertFalse(self.test_person.outfit.tits_available())

            self.test_person.outfit.strip_to_vagina()

            self.assertFalse(self.test_person.outfit.tits_available())
            self.assertTrue(self.test_person.outfit.vagina_available())
            self.assertTrue(self.test_person.outfit.bra_covered())
