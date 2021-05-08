init 0 python:
    class TestRoom(unittest.TestCase):
        def test_init(self):
            test_room = Room("test room")

            self.assertIsInstance(test_room, Room)

        def test_add_object(self):
            test_room = Room("test room")
            test_object = Object("test object", "stand")
            test_room.add_object(test_object)

            self.assertIn(test_object, test_room.objects)
            self.assertTrue(test_room.has_object_with_trait("stand"))
            self.assertIn(test_object, test_room.objects_with_trait("stand"))
            self.assertIs(test_object, test_room.get_object_with_name("test object"))

        def test_manipulate_person(self):
            test_room = Room("test room")
            test_person = create_random_person()

            self.assertNotIn(test_person, test_room.get_person_list())
            self.assertEqual(test_room.get_person_count(), 0)

            test_room.add_person(test_person)

            self.assertIn(test_person, test_room.get_person_list())
            self.assertEqual(test_room.get_person_count(), 1)

            other_person = create_random_person()
            test_room.add_person(other_person)

            self.assertIn(other_person, test_room.get_person_list())
            self.assertEqual(test_room.get_person_count(), 2)

            test_room.remove_person(test_person)

            self.assertNotIn(test_person, test_room.get_person_list())
            self.assertIn(other_person, test_room.get_person_list())
            self.assertEqual(test_room.get_person_count(), 1)

            other_room = Room("other room")

            test_room.move_person(test_person, other_room)
            self.assertNotIn(test_person, test_room.get_person_list())
            self.assertNotIn(test_person, other_room.get_person_list())

            test_room.move_person(other_person, other_room)
            self.assertNotIn(other_person, test_room.get_person_list())
            self.assertIn(other_person, other_room.get_person_list())
