init 0 python:
    class TestClothing(unittest.TestCase):
        def setUp(self):
            self.test_clothing = Clothing("Tshirt", 2, True, True, "Tshirt", True, False, 1, whiteness_adjustment = 0.35, supported_patterns = {"Striped":"Pattern_2","Text":"Pattern_3"}, display_name = "shirt",
                can_be_half_off = True, half_off_regions = [breast_region, stomach_region, pelvis_region], half_off_ignore_regions = [upper_arm_region], half_off_gives_access = True, half_off_reveals = True,
                constrain_regions = [torso_region, upper_arm_region, stomach_region])

        def test_copy(self):
            other_clothing = self.test_clothing.get_copy()

            self.assertEqual(other_clothing, self.test_clothing)
            self.assertIsNot(other_clothing, self.test_clothing)

        def test_drawable(self):
            self.assertIsInstance(self.test_clothing.generate_item_displayable("standard_body", "DD", "stand2"), renpy.display.core.Displayable)


    class testExpression(unittest.TestCase):
        def setUp(self):
            self.test_expression = Expression("Test Expression", "white", "Face_2")

        def test_drawable(self):
            self.assertIsInstance(self.test_expression.generate_emotion_displayable("stand2", "happy"), renpy.display.core.Displayable)

    class testFacial_Accessories(unittest.TestCase):
        def setUp(self):
            self.test_accessory = Facial_Accessory("Modern Glasses", 2, False, False, "Modern_Glasses", False, False, 0, display_name = "earings")

        def test_drawable(self):
            self.assertIsInstance(self.test_accessory.generate_item_displayable("stand2", "Face_2", "happy"), renpy.display.core.Displayable)
