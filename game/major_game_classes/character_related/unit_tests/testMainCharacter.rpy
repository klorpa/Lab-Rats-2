init 0 python:
    class TestMainCharacter(unittest.TestCase):
        # def setUp(self):
        #     pass

        def test_init(self):
            test_location = Room("New MC test location")
            test_business = Business("Test Business", test_location, test_location, test_location, test_location, test_location)
            new_main_character = MainCharacter(test_location, "Test", "Character", test_business, [0,0,0], [0,0,0,0,0], [0,0,0,0])

            self.assertIsInstance(new_main_character, MainCharacter)

        def test_change_location(self):
            current_location = mc.location
            test_location = Room("New MC location")
            mc.change_location(test_location)

            self.assertIs(mc.location, test_location)

            mc.change_location(current_location)

            self.assertIsNot(mc.location, test_location)
            self.assertIs(mc.location, current_location)

        def test_change_location_malformed(self):
            starting_location = mc.location

            self.assertIsInstance(starting_location, Room)

            mc.change_location("This is not a location")

            self.assertIs(mc.location, starting_location)

            test_location = Room("New MC location")

            mc.change_location(test_location)

            self.assertIsNot(mc.location, starting_location)
            self.assertIs(mc.location, test_location)

            mc.change_location(starting_location)

        def test_add_arousal(self):
            start_arousal = mc.arousal
            mc.change_arousal(20)

            self.assertEqual(mc.arousal, start_arousal + 20)

        def test_arousal_floor(self):
            mc.arousal = 0
            mc.change_arousal(-50)

            self.assertEqual(mc.arousal, 0)

        def test_arousal_subtraction(self):
            start_arousal = mc.arousal
            mc.change_arousal(50)
            self.assertEqual(mc.arousal, start_arousal + 50)

            mc.change_arousal(-25)
            self.assertEqual(mc.arousal, start_arousal + 25)

        def test_change_energy(self):
            mc.energy = mc.max_energy
            start_energy = mc.energy
            mc.change_energy(-50, add_to_log = False)

            self.assertEqual(mc.energy, start_energy - 50)

            mc.change_energy(20, add_to_log = False)
            self.assertEqual(mc.energy, start_energy - 30)

        def test_energy_floor(self):
            mc.energy = 0
            mc.change_energy(-50, add_to_log = False)

            self.assertEqual(mc.energy, 0)

        def test_energy_ceiling(self):
            mc.energy = mc.max_energy
            mc.change_energy(50, add_to_log = False)

            self.assertEqual(mc.energy, mc.max_energy)

        def test_change_masturbation_novelty(self):
            mc.masturbation_novelty = 75
            mc.change_masturbation_novelty(20, add_to_log = False)

            self.assertEqual(mc.masturbation_novelty, 95)

            mc.change_masturbation_novelty(20, add_to_log = False)

            self.assertEqual(mc.masturbation_novelty, 100)

            mc.change_masturbation_novelty(-20, add_to_log = False)

            self.assertEqual(mc.masturbation_novelty, 80)

            mc.change_masturbation_novelty(-100, add_to_log = False)

            self.assertEqual(mc.masturbation_novelty, 50)

        def test_change_locked_clarity(self):
            start_clarity = mc.locked_clarity
            mc.change_locked_clarity(50, add_to_log = False)

            self.assertEqual(mc.locked_clarity, start_clarity + 50)
            mc.change_locked_clarity(-20, add_to_log = False)

            self.assertEqual(mc.locked_clarity, start_clarity + 30)

        def test_release_clarity(self):
            mc.locked_clarity = 100
            mc.free_clarity = 0
            mc.convert_locked_clarity(conversion_multiplier = 1.0, with_novelty = False, add_to_log = False)

            self.assertEqual(mc.free_clarity, 100)

        def test_release_clarity_conversion(self):
            mc.locked_clarity = 100
            mc.free_clarity = 0

            mc.convert_locked_clarity(conversion_multiplier = 0.7, with_novelty = False, add_to_log = False)

            self.assertEqual(mc.free_clarity, 70)

        def test_release_clarity_novelty(self):
            mc.locked_clarity = 100
            mc.free_clarity = 0

            mc.convert_locked_clarity(with_novelty = 0.6, add_to_log = False)

            self.assertTrue(mc.free_clarity, 60)

        def test_spend_clarity(self):
            mc.free_clarity = 300

            mc.spend_clarity(50, add_to_log = False)

            self.assertTrue(mc.free_clarity, 250)

        def test_free_add_clarity(self):
            mc.free_clarity = 100

            mc.add_clarity(100, add_to_log = False)

            self.assertTrue(mc.free_clarity, 200)

        def test_improve_stats(self):
            test_location = Room("New MC test location")
            test_business = Business("Test Business", test_location, test_location, test_location, test_location, test_location)
            new_main_character = MainCharacter(test_location, "Test", "Character", test_business, [0,0,0], [0,0,0,0,0], [0,0,0,0])
            new_main_character.free_stat_points = 20

            new_main_character.improve_stat("int",1)
            new_main_character.improve_stat("cha",2)
            new_main_character.improve_stat("foc",3)

            self.assertEqual(new_main_character.int, 1)
            self.assertEqual(new_main_character.charisma, 2)
            self.assertEqual(new_main_character.focus, 3)
            self.assertEqual(new_main_character.free_stat_points, 14)

        def test_improve_work_skills(self):
            test_location = Room("New MC test location")
            test_business = Business("Test Business", test_location, test_location, test_location, test_location, test_location)
            new_main_character = MainCharacter(test_location, "Test", "Character", test_business, [0,0,0], [0,0,0,0,0], [0,0,0,0])
            new_main_character.free_work_points = 20

            new_main_character.improve_work_skill("hr",1)
            new_main_character.improve_work_skill("market",2)
            new_main_character.improve_work_skill("research",3)
            new_main_character.improve_work_skill("production",4)
            new_main_character.improve_work_skill("supply",5)

            self.assertEqual(new_main_character.hr_skill,1)
            self.assertEqual(new_main_character.market_skill,2)
            self.assertEqual(new_main_character.research_skill,3)
            self.assertEqual(new_main_character.production_skill,4)
            self.assertEqual(new_main_character.supply_skill,5)
            self.assertEqual(new_main_character.free_work_points, 5)

        def test_improve_sex_skills(self):
            test_location = Room("New MC test location")
            test_business = Business("Test Business", test_location, test_location, test_location, test_location, test_location)
            new_main_character = MainCharacter(test_location, "Test", "Character", test_business, [0,0,0], [0,0,0,0,0], [0,0,0,0])

            new_main_character.free_sex_points += 20
            new_main_character.improve_sex_skill("Foreplay",1)
            new_main_character.improve_sex_skill("Oral",2)
            new_main_character.improve_sex_skill("Vaginal",3)
            new_main_character.improve_sex_skill("Anal",4)

            self.assertEqual(new_main_character.sex_skills["Foreplay"],1)
            self.assertEqual(new_main_character.sex_skills["Oral"],2)
            self.assertEqual(new_main_character.sex_skills["Vaginal"],3)
            self.assertEqual(new_main_character.sex_skills["Anal"],4)

            old_energy = new_main_character.max_energy
            new_main_character.improve_sex_skill("stam",2)

            self.assertEqual(new_main_character.max_energy, old_energy + 40)
            self.assertEqual(new_main_character.free_sex_points, 8)

        def test_start_end_text_convo(self):
            test_location = Room("New MC test location")
            test_business = Business("Test Business", test_location, test_location, test_location, test_location, test_location)
            new_main_character = MainCharacter(test_location, "Test", "Character", test_business, [0,0,0], [0,0,0,0,0], [0,0,0,0])
            new_person = create_random_person()

            self.assertFalse(new_main_character.phone.has_number(new_person))
            new_main_character.start_text_convo(new_person)

            self.assertTrue(new_main_character.phone.has_number(new_person))
            self.assertIs(new_main_character.having_text_conversation, new_person)
            self.assertFalse(new_main_character.text_conversation_paused)

            new_main_character.end_text_convo()
            self.assertIsNone(new_main_character.having_text_conversation)
            self.assertFalse(new_main_character.text_conversation_paused)
