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

            self.assertTrue(test_outfit.has_clothing(jeans))
            self.assertTrue(test_outfit.has_clothing(tshirt))
            self.assertFalse(test_outfit.has_clothing(heart_pasties))

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

            test_outfit.remove_clothing_list([bra, tshirt])

            self.assertFalse(test_outfit.has_clothing(bra))
            self.assertFalse(test_outfit.has_clothing(tshirt))
            self.assertTrue(test_outfit.has_clothing(jeans))
