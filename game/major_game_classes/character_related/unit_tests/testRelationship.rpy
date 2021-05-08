init 0 python:
    class TestRelationship(unittest.TestCase):
        # def setUp(self):

        def test_relationship_init(self):
            test_person_a = create_random_person()
            test_person_b = create_random_person()
            test_relationship = Relationship(test_person_a, test_person_b, "testers")

            self.assertIsInstance(test_relationship, Relationship)
            self.assertIs(test_relationship.get_other_person(test_person_b), test_person_a)
            self.assertIs(test_relationship.get_other_person(test_person_a), test_person_b)
            self.assertEqual(test_relationship.get_type(), "testers")

        def test_relationship_array_init(self):
            test_relationship_array = RelationshipArray()

            self.assertIsInstance(test_relationship_array, RelationshipArray)
            self.assertFalse(test_relationship_array.relationships)

        def test_relationship_array_relationships(self):
            test_relationship_array = RelationshipArray()
            test_person_a = create_random_person()
            test_person_b = create_random_person()
            test_person_c = create_random_person()
            test_person_d = create_random_person()
            test_relationship_array.update_relationship(test_person_a, test_person_b, "testers")
            test_relationship_array.update_relationship(test_person_c, test_person_d, "forwards", "backwards")

            self.assertIsNone(test_relationship_array.get_relationship(test_person_a, test_person_a))
            self.assertIsInstance(test_relationship_array.get_relationship(test_person_a, test_person_b), Relationship)
            self.assertIsInstance(test_relationship_array.get_relationship(test_person_b, test_person_a), Relationship)
            self.assertIs(test_relationship_array.get_relationship(test_person_a, test_person_b), test_relationship_array.get_relationship(test_person_b, test_person_a))
            self.assertIsNone(test_relationship_array.get_relationship(test_person_a, test_person_c))
            self.assertEqual(test_relationship_array.get_relationship_type(test_person_c, test_person_d), "forwards")
            self.assertEqual(test_relationship_array.get_relationship_type(test_person_d, test_person_c), "backwards")

        def test_relationship_changes(self):
            test_relationship_array = RelationshipArray()
            test_person_a = create_random_person()
            test_person_b = create_random_person()

            test_relationship_array.begin_relationship(test_person_b, test_person_a)

            self.assertIsInstance(test_relationship_array.get_relationship(test_person_b, test_person_a), Relationship)
            self.assertEqual(test_relationship_array.get_relationship_type(test_person_b, test_person_a), "Acquaintance")

            test_relationship_array.improve_relationship(test_person_b, test_person_a)

            self.assertIsInstance(test_relationship_array.get_relationship(test_person_b, test_person_a), Relationship)
            self.assertEqual(test_relationship_array.get_relationship_type(test_person_b, test_person_a), "Friend")

            test_relationship_array.worsen_relationship(test_person_b, test_person_a)
            test_relationship_array.worsen_relationship(test_person_b, test_person_a)

            self.assertIsInstance(test_relationship_array.get_relationship(test_person_b, test_person_a), Relationship)
            self.assertEqual(test_relationship_array.get_relationship_type(test_person_b, test_person_a), "Rival")

            test_relationship_array.worsen_relationship(test_person_b, test_person_a)
            test_relationship_array.worsen_relationship(test_person_b, test_person_a)

            self.assertIsInstance(test_relationship_array.get_relationship(test_person_b, test_person_a), Relationship)
            self.assertEqual(test_relationship_array.get_relationship_type(test_person_b, test_person_a), "Nemesis")
