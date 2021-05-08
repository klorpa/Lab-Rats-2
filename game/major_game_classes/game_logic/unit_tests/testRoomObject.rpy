init 0 python:
    class TestRoomObject(unittest.TestCase):
        def test_init(self):
            test_object = Object("test object", [])

            self.assertIsInstance(test_object, Object)

        def test_has_traits(self):
            test_object = Object("test object", [])

            self.assertFalse(test_object.has_trait("stand"))
            self.assertFalse(test_object.has_trait("kneel"))

            test_object = Object("test object", ["stand", "lay"])

            self.assertTrue(test_object.has_trait("stand"))
            self.assertFalse(test_object.has_trait("kneel"))
