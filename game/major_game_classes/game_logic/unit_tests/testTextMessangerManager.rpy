init 0 python:
    class TestTextMessageManager(unittest.TestCase):
        def test_init(self):
            test_manager = TextMessageManager()

            self.assertIsInstance(test_manager, TextMessageManager)

        def test_register_number(self):
            test_manager = TextMessageManager()
            test_person = create_random_person()

            self.assertNotIn(test_person, test_manager.message_history.keys())

            test_manager.register_number(test_person)

            self.assertIn(test_person, test_manager.message_history.keys())

        def test_add_message(self):
            test_manager = TextMessageManager()
            test_person = create_random_person()

            self.assertNotIn(test_person, test_manager.message_history.keys())
            self.assertFalse(test_manager.get_message_list(test_person))

            test_message = renpy.character.HistoryEntry()
            test_message.who = test_person.title
            test_message.what = "This is a test"
            test_manager.add_message(test_person, test_message)

            self.assertIn(test_person, test_manager.message_history.keys())
            self.assertTrue(test_manager.get_message_list(test_person))
            self.assertEqual(test_manager.get_message_list(test_person)[-1].who, test_person.title)

            test_message = renpy.character.HistoryEntry()
            test_message.who = mc.name
            test_message.what = "MC response"
            test_manager.add_message(test_person, test_message)

            self.assertEqual(test_manager.get_message_list(test_person)[-1].who, mc.name)

        def test_add_non_convo_mesages(self):
            test_manager = TextMessageManager()
            test_person = create_random_person()

            self.assertNotIn(test_person, test_manager.message_history.keys())
            self.assertFalse(test_manager.get_message_list(test_person))

            test_manager.add_non_convo_message(test_person, "This is a test")

            self.assertIn(test_person, test_manager.message_history.keys())
            self.assertTrue(test_manager.get_message_list(test_person))
            self.assertEqual(test_manager.get_message_list(test_person)[-1].who, test_person.title)

            test_manager.add_non_convo_message(test_person, "MC response", as_mc = True)

            self.assertEqual(test_manager.get_message_list(test_person)[-1].who, mc.name)

        def test_add_system_message(self):
            test_manager = TextMessageManager()
            test_person = create_random_person()

            self.assertNotIn(test_person, test_manager.message_history.keys())
            self.assertFalse(test_manager.get_message_list(test_person))

            test_manager.add_system_message(test_person, "Test system message")

            self.assertIn(test_person, test_manager.message_history.keys())
            self.assertTrue(test_manager.get_message_list(test_person))
            self.assertEqual(test_manager.get_message_list(test_person)[-1].who, None)
            self.assertEqual(test_manager.get_message_list(test_person)[-1].what, "Test system message")

        def test_has_person_list(self):
            test_manager = TextMessageManager()
            test_person = create_random_person()
            other_person = create_random_person()

            self.assertFalse(test_manager.get_person_list())

            test_manager.register_number(test_person)

            self.assertIn(test_person, test_manager.get_person_list())
            self.assertNotIn(other_person, test_manager.get_person_list())

        def test_has_number(self):
            test_manager = TextMessageManager()
            test_person = create_random_person()
            other_person = create_random_person()

            self.assertFalse(test_manager.has_number(test_person))
            self.assertFalse(test_manager.has_number(other_person))

            test_manager.register_number(test_person)

            self.assertTrue(test_manager.has_number(test_person))
            self.assertFalse(test_manager.has_number(other_person))
