init 0 python:
    class TestWardrobe(unittest.TestCase):
        def test_init(self):
            test_wardrobe = Wardrobe("Test wardrobe")

            self.assertIsInstance(test_wardrobe, Wardrobe)

        def test_add_outfits(self):
            test_wardrobe = Wardrobe("Test wardrobe")
            test_outfit = Outfit("Test outfit")
            test_outfit.add_upper(bra.get_copy())
            test_outfit.add_upper(tshirt.get_copy())
            test_outfit.add_lower(jeans.get_copy())
            test_outfit.add_lower(panties.get_copy())
            test_outfit.add_feet(heels.get_copy())
            test_outfit.add_accessory(sunglasses.get_copy())

            self.assertFalse(test_wardrobe.outfits)
            self.assertFalse(test_wardrobe.underwear_sets)
            self.assertFalse(test_wardrobe.overwear_sets)

            test_wardrobe.add_outfit(test_outfit)

            self.assertIn(test_outfit, test_wardrobe.outfits)

            test_underwear = Outfit("Test underwear")
            test_underwear.add_upper(bra.get_copy())
            test_underwear.add_lower(panties.get_copy())
            test_wardrobe.add_underwear_set(test_underwear)

            self.assertIn(test_underwear, test_wardrobe.underwear_sets)

            test_overwear = Outfit("Test overwear")
            test_overwear.add_upper(tshirt.get_copy())
            test_overwear.add_lower(jeans.get_copy())
            test_overwear.add_feet(heels.get_copy())
            test_wardrobe.add_overwear_set(test_overwear)

            self.assertIn(test_overwear, test_wardrobe.overwear_sets)

        def test_remove_outfits(self):
            test_wardrobe = Wardrobe("Test wardrobe")
            test_outfit = Outfit("Test outfit")
            test_underwear = Outfit("Test underwear")
            test_overwear = Outfit("Test overwear")
            test_wardrobe.add_outfit(test_outfit)
            test_wardrobe.add_underwear_set(test_underwear)
            test_wardrobe.add_overwear_set(test_overwear)

            self.assertIn(test_outfit, test_wardrobe.outfits)

            test_wardrobe.remove_outfit(test_outfit)

            self.assertNotIn(test_outfit, test_wardrobe.outfits)

            test_wardrobe.remove_outfit(test_underwear)
            test_wardrobe.remove_outfit(test_overwear)

            self.assertNotIn(test_underwear, test_wardrobe.underwear_sets)
            self.assertNotIn(test_overwear, test_wardrobe.overwear_sets)
