init 0 python:
    class TestGroupDisplayManager(unittest.TestCase):
        def test_init(self):
            test_person_1 = create_random_person()
            test_person_2 = create_random_person()
            test_person_3 = create_random_person()
            test_group = GroupDisplayManager([test_person_1, test_person_2, test_person_3], test_person_2)

            self.assertIsInstance(test_group, GroupDisplayManager)

        def test_add_person(self):
            test_person_1 = create_random_person()
            test_person_2 = create_random_person()
            test_person_3 = create_random_person()
            test_group = GroupDisplayManager([test_person_1, test_person_2], test_person_2)

            self.assertNotIn(test_person_3, test_group.group_of_people)

            test_group.add_person(test_person_3)

            self.assertIn(test_person_3, test_group.group_of_people)
            self.assertIs(test_person_2, test_group.primary_speaker)

            test_person_4 = create_random_person()
            test_group.add_person(test_person_4, make_primary = True)

            self.assertIn(test_person_4, test_group.group_of_people)
            self.assertIs(test_person_4, test_group.primary_speaker)

        def test_remove_person(self):
            test_person_1 = create_random_person()
            test_person_2 = create_random_person()
            test_person_3 = create_random_person()
            test_group = GroupDisplayManager([test_person_1, test_person_2, test_person_3], test_person_2)

            self.assertIn(test_person_2, test_group.group_of_people)

            test_group.remove_person(test_person_2, new_primary = test_person_1)

            self.assertNotIn(test_person_2, test_group.group_of_people)
            self.assertIn(test_person_1, test_group.group_of_people)
            self.assertIs(test_person_1, test_group.primary_speaker)

            test_group.remove_person(test_person_1)

            self.assertNotIn(test_person_1, test_group.group_of_people)
            self.assertIsNone(test_group.primary_speaker)

        def test_set_primary(self):
            test_person_1 = create_random_person()
            test_person_2 = create_random_person()
            test_person_3 = create_random_person()
            test_group = GroupDisplayManager([test_person_1, test_person_2, test_person_3])

            self.assertIs(test_group.primary_speaker, test_person_1)

            test_group.set_primary(test_person_3)

            self.assertIs(test_group.primary_speaker, test_person_3)

            test_group.set_primary(test_person_2)

            self.assertIs(test_group.primary_speaker, test_person_2)
