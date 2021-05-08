init 0 python:
    def test_personality_titles(the_person):
        return ["Tester"]

    def test_personality_possessive_titles(the_person):
        return ["Your tester"]

    def test_personality_mc_titles(the_person):
        return ["Master tester"]

    class TestPersonality(unittest.TestCase):
        # def setUp(self):
        #     pass

        def test_init(self):
            test_personality = Personality("test_personality", "relaxed")

            self.assertIsInstance(test_personality, Personality)


        def test_generate_opinion(self):
            test_personality = Personality("test_personality", "relaxed", common_likes = ["the colour black", "work uniforms"], common_dislikes = ["Fridays", "flirting"])
            opinion = test_personality.generate_default_opinion()
            opinion_topic = opinion[0]
            opinion_strength = opinion[1][0]
            opinion_known = opinion[1][1]

            self.assertIn(opinion_topic, opinions_list)
            self.assertTrue(opinion_strength == -2 or opinion_strength == -1 or opinion_strength == 1 or opinion_strength == 2)
            self.assertFalse(opinion_known)

        def test_generate_sexy_opinion(self):
            test_personality = Personality("test_personality", "relaxed", common_sexy_likes = ["drinking cum", "being submissive"], common_sexy_dislikes = ["giving handjobs", "showing her tits"])
            opinion = test_personality.generate_default_sexy_opinion()
            opinion_topic = opinion[0]
            opinion_strength = opinion[1][0]
            opinion_known = opinion[1][1]

            self.assertIn(opinion_topic, sexy_opinions_list)
            self.assertTrue(opinion_strength == -2 or opinion_strength == -1 or opinion_strength == 1 or opinion_strength == 2)
            self.assertFalse(opinion_known)

        def test_get_titles(self):
            test_personality = Personality("test_personality", "relaxed")
            test_person = create_random_person()

            self.assertEqual(test_personality.get_personality_titles(test_person), test_person.name)
            self.assertEqual(test_personality.get_personality_possessive_titles(test_person), test_person.name)
            self.assertEqual(test_personality.get_personality_player_titles(test_person), mc.name)

            test_personality = Personality("test_personality", "wild", titles_function = test_personality_titles, possessive_titles_function = test_personality_possessive_titles, player_titles_function = test_personality_mc_titles)

            self.assertNotEqual(test_personality.get_personality_titles(test_person), test_person.name)
            self.assertNotEqual(test_personality.get_personality_possessive_titles(test_person), test_person.name)
            self.assertNotEqual(test_personality.get_personality_player_titles(test_person), mc.name)
            self.assertEqual(test_personality.get_personality_titles(test_person), ["Tester"])
            self.assertEqual(test_personality.get_personality_possessive_titles(test_person), ["Your tester"])
            self.assertEqual(test_personality.get_personality_player_titles(test_person), ["Master tester"])
