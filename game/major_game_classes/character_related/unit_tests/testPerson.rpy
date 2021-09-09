init 0 python:
    class TestPerson(unittest.TestCase):
        # def setUp(self):
        #     pass

        def test_init(self):
            test_person = create_random_person()

            self.assertIsInstance(test_person, Person)

        def test_global_character_advance(self):
            current_global_number = Person.global_character_number

            test_person = create_random_person()

            self.assertEqual(test_person.character_number, current_global_number)
            self.assertEqual(Person.global_character_number, current_global_number+1)

        def test_displayable_build(self):
            test_person = create_random_person()
            test_displayable = test_person.build_person_displayable()

            self.assertIsInstance(test_displayable, renpy.display.core.Displayable)


        def test_change_suggest(self):
            test_person = create_random_person()
            test_person.suggestibility = 0
            start_suggest = test_person.suggestibility
            test_person.change_suggest(20)

            self.assertEqual(test_person.suggestibility, start_suggest+20)

            test_person.change_suggest(-50)

            self.assertEqual(test_person.suggestibility, start_suggest-30)

        def test_change_suggest_effect(self):
            test_person = create_random_person()
            start_suggest = test_person.suggestibility
            test_person.add_suggest_effect(20, add_to_log = False)

            self.assertEqual(test_person.suggestibility, start_suggest + 20)

            test_person.add_suggest_effect(10, add_to_log = False)

            self.assertEqual(test_person.suggestibility, start_suggest + 20)

            test_person.add_suggest_effect(30, add_to_log = False)

            self.assertEqual(test_person.suggestibility, start_suggest + 30)

            test_person.remove_suggest_effect(20)
            test_person.remove_suggest_effect(30)

            self.assertEqual(test_person.suggestibility, start_suggest + 10)

            test_person.remove_suggest_effect(-10)

            self.assertEqual(test_person.suggestibility, start_suggest + 10)

            test_person.remove_suggest_effect(10)

            self.assertEqual(test_person.suggestibility, start_suggest)

        def test_change_happiness(self):
            test_person = create_random_person()
            start_happinesss = test_person.happiness
            test_person.change_happiness(40, add_to_log = False)

            self.assertEqual(test_person.happiness, start_happinesss + 40)

            test_person.change_happiness(-20, add_to_log = False)

            self.assertEqual(test_person.happiness, start_happinesss + 20)

            test_person.change_happiness(-200, add_to_log = False)

            self.assertEqual(test_person.happiness, 0)

        def test_change_love(self):
            test_person = create_random_person()
            test_person.love = 0
            test_person.change_love(7, add_to_log = False)

            self.assertEqual(test_person.love, 7)

            test_person.change_love(40, max_modified_to = 20, add_to_log = False)

            self.assertEqual(test_person.love, 20)

            test_person.change_love(40, add_to_log = False)

            self.assertEqual(test_person.love, 60)

            test_person.change_love(-80, add_to_log = False)

            self.assertEqual(test_person.love, -20)

            test_person.change_love(-300, add_to_log = False)

            self.assertEqual(test_person.love, -100)

            test_person.change_love(300, add_to_log = False)

            self.assertEqual(test_person.love, 100)

        def test_change_slut_temp(self):
            test_person = create_random_person()
            start_sluttiness = test_person.sluttiness
            test_person.change_slut(20, add_to_log = False)

            self.assertEqual(test_person.sluttiness, start_sluttiness + 20)

            test_person.change_slut(-20, add_to_log = False)

            self.assertEqual(test_person.sluttiness, start_sluttiness)

            test_person.change_slut(-100, add_to_log = False)

            self.assertEqual(test_person.sluttiness, start_sluttiness - 100)

        def test_change_slut_capped(self):
            test_person = create_random_person()
            start_sluttiness = test_person.sluttiness
            test_person.change_slut(20, add_to_log = False)

            self.assertEqual(test_person.sluttiness, start_sluttiness + 20)

            test_person.change_slut(20, start_sluttiness+20, add_to_log = False)

            self.assertEqual(test_person.sluttiness, start_sluttiness + 20)

            test_person.change_slut(20, start_sluttiness+30, add_to_log = False)

            self.assertEqual(test_person.sluttiness, start_sluttiness + 30)

        def test_change_slut_over_cap(self):
            test_person = create_random_person()
            start_sluttiness = test_person.sluttiness
            test_person.change_slut(60, add_to_log = False)

            self.assertEqual(test_person.sluttiness, start_sluttiness + 60)

            test_person.change_slut(50, 20, add_to_log = False)

            self.assertEqual(test_person.sluttiness, start_sluttiness + 60)

            test_person.change_slut(-100, 50, add_to_log = False)

            self.assertEqual(test_person.sluttiness, 50)


        def test_changee_obedience(self):
            test_person = create_random_person()
            start_obedience = test_person.obedience
            test_person.change_obedience(10, add_to_log = False)

            self.assertEqual(test_person.obedience, start_obedience + 10)

            test_person.change_obedience(-15, add_to_log = False)

            self.assertEqual(test_person.obedience, start_obedience - 5)

            test_person.change_obedience(205, add_to_log = False)

            self.assertEqual(test_person.obedience, start_obedience + 200)

            test_person.change_obedience(-500, add_to_log = False)

            self.assertEqual(test_person.obedience, 0)

        def test_situational_slut(self):
            test_person = create_random_person()
            start_sluttiness = test_person.sluttiness
            test_person.add_situational_slut("testing", 20, "This is a test modifier")

            self.assertEqual(test_person.sluttiness, start_sluttiness )
            self.assertEqual(test_person.effective_sluttiness(), start_sluttiness + 20)

            test_person.add_situational_slut("testing", 10, "Another test modifier")

            self.assertEqual(test_person.effective_sluttiness(), start_sluttiness + 10)

            test_person.add_situational_slut("different test", 15, "Test test")

            self.assertEqual(test_person.effective_sluttiness(), start_sluttiness + 25)

            test_person.clear_situational_slut("testing")
            test_person.clear_situational_slut("different test")

            self.assertEqual(test_person.effective_sluttiness(), start_sluttiness)

            test_person.add_situational_slut("neg test", -15)

            self.assertEqual(test_person.effective_sluttiness(), start_sluttiness - 15)

        def test_situational_obedience(self):
            test_person = create_random_person()
            start_obedience = test_person.obedience
            test_person.add_situational_obedience("testing", 10, "Test")

            self.assertEqual(test_person.obedience, start_obedience + 10)

            test_person.add_situational_obedience("testing", -15)

            self.assertEqual(test_person.obedience, start_obedience - 15)

            test_person.add_situational_obedience("another test", 16)

            self.assertEqual(test_person.obedience, start_obedience + 1)

            test_person.clear_situational_obedience("testing")
            test_person.clear_situational_obedience("another test")

            self.assertEqual(test_person.obedience, start_obedience)

        def test_change_stats(self):
            test_person = create_random_person()
            test_person.charisma = 0
            test_person.int = 0
            test_person.focus = 0

            self.assertEqual(test_person.charisma_debt, 0)
            self.assertEqual(test_person.int_debt, 0)
            self.assertEqual(test_person.focus_debt, 0)

            test_person.change_cha(1, add_to_log = False)
            test_person.change_int(2, add_to_log = False)
            test_person.change_focus(3, add_to_log = False)

            self.assertEqual(test_person.charisma, 1)
            self.assertEqual(test_person.int, 2)
            self.assertEqual(test_person.focus, 3)
            self.assertEqual(test_person.charisma_debt, 0)
            self.assertEqual(test_person.int_debt, 0)
            self.assertEqual(test_person.focus_debt, 0)

            test_person.change_cha(-3, add_to_log = False)
            test_person.change_int(-5, add_to_log = False)
            test_person.change_focus(-10, add_to_log = False)

            self.assertEqual(test_person.charisma, 0)
            self.assertEqual(test_person.int, 0)
            self.assertEqual(test_person.focus, 0)
            self.assertEqual(test_person.charisma_debt, -2)
            self.assertEqual(test_person.int_debt, -3)
            self.assertEqual(test_person.focus_debt, -7) ##

            test_person.change_cha(15, add_to_log = False)
            test_person.change_int(20, add_to_log = False)
            test_person.change_focus(25, add_to_log = False)

            self.assertEqual(test_person.charisma, 13)
            self.assertEqual(test_person.int, 17)
            self.assertEqual(test_person.focus, 18)
            self.assertEqual(test_person.charisma_debt, 0)
            self.assertEqual(test_person.int_debt, 0)
            self.assertEqual(test_person.focus_debt, 0)

        def test_change_sex_skill(self):
            test_person = create_random_person()
            starting_foreplay = test_person.sex_skills["Foreplay"]
            starting_oral = test_person.sex_skills["Oral"]
            starting_vaginal = test_person.sex_skills["Vaginal"]
            starting_anal = test_person.sex_skills["Anal"]

            test_person.change_sex_skill("Foreplay", 1, add_to_log = False)

            self.assertEqual(test_person.sex_skills["Foreplay"], starting_foreplay + 1)

            test_person.change_sex_skill("Oral", 2, add_to_log = False)

            self.assertEqual(test_person.sex_skills["Oral"], starting_oral + 2)

            test_person.change_sex_skill("Vaginal", 3, add_to_log = False)

            self.assertEqual(test_person.sex_skills["Vaginal"], starting_vaginal + 3)

            test_person.change_sex_skill("Anal", 4, add_to_log = False)

            self.assertEqual(test_person.sex_skills["Anal"], starting_anal + 4)

            test_person.change_sex_skill("Foreplay", 20, add_to_log = False)

            self.assertEqual(test_person.sex_skills["Foreplay"], starting_foreplay + 21)

            test_person.change_sex_skill("Anal", -1000, add_to_log = False)

            self.assertEqual(test_person.sex_skills["Anal"], 0)

        def test_change_arousal(self):
            test_person = create_random_person()
            test_person.change_arousal(20, add_to_log = False)

            self.assertEqual(test_person.arousal, 20)

            test_person.change_arousal(-10, add_to_log = False)

            self.assertEqual(test_person.arousal, 10)

            test_person.change_arousal(-23, add_to_log = False)

            self.assertEqual(test_person.arousal, 0)

            test_person.change_arousal(1000, add_to_log = False)

            self.assertEqual(test_person.arousal, 1000)

            test_person.reset_arousal()

            self.assertEqual(test_person.arousal, 0)

        def test_change_max_arousal(self):
            test_person = create_random_person()
            start_max_arousal = test_person.max_arousal

            test_person.change_max_arousal(20, add_to_log = False)

            self.assertEqual(test_person.max_arousal, start_max_arousal + 20)

            test_person.change_max_arousal(-40, add_to_log = False)

            self.assertEqual(test_person.max_arousal, start_max_arousal - 20)

            test_person.change_max_arousal(-1000, add_to_log = False)

            self.assertEqual(test_person.max_arousal, 20)

            test_person.change_max_arousal(1000, add_to_log = False)

            self.assertEqual(test_person.max_arousal, 1020)
            self.assertEqual(test_person.arousal, 0)

        def test_change_novelty(self):
            test_person = create_random_person()
            start_novelty = test_person.novelty

            self.assertEqual(start_novelty, 100)

            test_person.change_novelty(-20, add_to_log = False)

            self.assertEqual(test_person.novelty, start_novelty - 20)

            test_person.change_novelty(10, add_to_log = False)

            self.assertEqual(test_person.novelty, start_novelty - 10)

            test_person.change_novelty(-120, add_to_log = False)

            self.assertEqual(test_person.novelty, 0)

            test_person.change_novelty(200, add_to_log = False)

            self.assertEqual(test_person.novelty, 100)

        def test_change_energy(self):
            test_person = create_random_person()
            start_energy = test_person.energy
            test_person.change_energy(-40, add_to_log = False)

            self.assertEqual(test_person.energy, start_energy - 40)

            test_person.change_energy(20, add_to_log = False)

            self.assertEqual(test_person.energy, start_energy - 20)

            test_person.change_energy(-200, add_to_log = False)

            self.assertEqual(test_person.energy, 0)

            test_person.change_energy(200, add_to_log = False)

            self.assertEqual(test_person.energy, test_person.max_energy)

        def test_change_max_energy(self):
            test_person = create_random_person()
            start_max = test_person.max_energy
            test_person.change_max_energy(-20, add_to_log = False)

            self.assertEqual(test_person.max_energy, start_max - 20)
            self.assertEqual(test_person.energy, test_person.max_energy)

            test_person.change_energy(-40, add_to_log = False)
            test_person.change_max_energy(-20, add_to_log = False)

            self.assertEqual(test_person.max_energy, start_max - 40)
            self.assertEqual(test_person.energy, test_person.max_energy - 20)

            test_person.change_max_energy(-100, add_to_log = False)

            self.assertTrue(test_person.max_energy < 0)

        def test_wearing_uniform(self):
            test_person = create_random_person()
            return_value = test_person.is_wearing_uniform()

            self.assertIsNotNone(return_value)
            self.assertFalse(return_value)

        def test_should_wear_uniform(self):
            test_person = create_random_person()
            return_value = test_person.should_wear_uniform()

            self.assertIsNotNone(return_value)
            self.assertFalse(return_value)

        def test_job_happiness(self):
            test_person = create_random_person()
            return_value = test_person.get_job_happiness_score()

            self.assertIsInstance(return_value, __builtin__.int)

        def test_get_no_condom_threshold(self):
            test_person = create_random_person()
            return_value = test_person.get_no_condom_threshold()

            self.assertIsInstance(return_value, __builtin__.int)

        def test_wants_condom(self):
            test_person = create_random_person()
            return_value = test_person.wants_condom()

            self.assertTrue(return_value) #NOTE: this assumes girls with ~0 sluttiness will always want a condom.

        def test_is_family(self):
            test_person = create_random_person()

            self.assertFalse(test_person.is_family())

            self.assertTrue(mom.is_family())

        def test_has_large_tits(self):
            test_person = create_random_person()
            test_person.tits = "AA"

            self.assertFalse(test_person.has_large_tits())

            test_person.tits = "FF"

            self.assertTrue(test_person.has_large_tits())

        def test_wants_creampie(self):
            test_person = create_random_person()

            self.assertFalse(test_person.wants_creampie()) #NOTE: This assuems girls with ~0 sluttiness will never want a creampie

        def test_days_from_ideal_fertility(self):
            test_person = create_random_person()
            distance = test_person.days_from_ideal_fertility()

            self.assertTrue(distance <= 15)
            self.assertTrue(distance >= 0)

        def test_fertility_cycle_string(self):
            test_person = create_random_person()

            self.assertIsInstance(test_person.fertility_cycle_string(), basestring)

        def test_update_birth_control_knowledge(self):
            test_person = create_random_person()
            test_person.on_birth_control = False
            test_person.update_birth_control_knowledge()

            self.assertFalse(test_person.event_triggers_dict.get("birth_control_status", True))
            test_person.on_birth_control = True
            self.assertFalse(test_person.event_triggers_dict.get("birth_control_status", True))

            test_person.update_birth_control_knowledge()
            self.assertTrue(test_person.event_triggers_dict.get("birth_control_status", False))

            test_person.update_birth_control_knowledge(force_known_state = False)
            self.assertFalse(test_person.event_triggers_dict.get("birth_control_status", True))

            self.assertEqual(test_person.event_triggers_dict.get("birth_control_known_day", -1), day)

            test_person.update_birth_control_knowledge(force_known_day = day + 2)
            self.assertEqual(test_person.event_triggers_dict.get("birth_control_known_day", -1), day+2)

        def test_effective_sluttiness(self):
            test_person = create_random_person()

            self.assertIsInstance(test_person.effective_sluttiness(), __builtin__.int)
            self.assertIsInstance(test_person.effective_sluttiness("kissing"), __builtin__.int)

            self.assertTrue(test_person.effective_sluttiness() > test_person.effective_sluttiness("kissing"))

        def test_calculate_base_salary(self):
            test_person = create_random_person()

            self.assertIsInstance(test_person.calculate_base_salary(), __builtin__.int)

        def test_set_schedule(self):
            test_person = create_random_person()
            test_room = Room("Schedule test location")
            test_person.set_schedule(test_room, times = [0,1])

            self.assertIs(test_person.schedule[0][1], test_room)
            self.assertIs(test_person.schedule[3][0], test_room)

            other_test_room = Room("Other schedule test room")
            test_person.set_schedule(other_test_room, days = [2,4], times = [0])

            self.assertIs(test_person.schedule[2][0], other_test_room)
            self.assertIs(test_person.schedule[4][0], other_test_room)
            self.assertIs(test_person.schedule[4][1], test_room)
            self.assertIs(test_person.schedule[3][0], test_room)

        def test_set_work(self):
            test_person = create_random_person()
            test_room = Room("Schedule test location")
            test_person.set_work(test_room)

            self.assertIs(test_person.schedule[0][1], test_room)
            self.assertIs(test_person.schedule[4][1], test_room)
            self.assertIsNot(test_person.schedule[3][4], test_room)
            self.assertIsNot(test_person.schedule[2][0], test_room)
            self.assertIsNot(test_person.schedule[6][1], test_room)

            test_person.set_work(None)
            self.assertIsNone(test_person.schedule[0][1])
            self.assertIsNone(test_person.schedule[4][1])

            other_test_room = Room("Other schedule test location")
            test_person.set_work(other_test_room, work_days = [5,6], work_times = [0,3])

            self.assertIs(test_person.schedule[5][0], other_test_room)
            self.assertIs(test_person.schedule[6][3], other_test_room)
            self.assertIsNot(test_person.schedule[2][2], other_test_room)
            self.assertIsNot(test_person.schedule[5][1], other_test_room)

        def test_get_destination(self):
            test_person = create_random_person()

            self.assertIsNone(test_person.get_destination())

            test_home_location = Room("Test home location")
            test_work_location = Room("Test location")
            test_person.set_schedule(test_home_location, times = [0,1,2,3,4])
            test_person.set_work(test_work_location)

            self.assertIsInstance(test_person.get_destination(), Room)
            self.assertIs(test_person.get_destination(specified_day = 4, specified_time = 2), test_work_location)
            self.assertIs(test_person.get_destination(specified_day = 4, specified_time = 4), test_home_location)
            self.assertIs(test_person.get_destination(specified_day = 4+7, specified_time = 2), test_work_location)
            self.assertIs(test_person.get_destination(specified_day = 4+14, specified_time = 4), test_home_location)

        def test_role_manipulation(self):
            test_person = create_random_person()
            test_role = Role("Test role")
            test_person.add_role(test_role)

            self.assertIn(test_role, test_person.special_role)
            self.assertTrue(test_person.has_role(test_role))

            test_person.remove_role(test_role)

            self.assertNotIn(test_role, test_person.special_role)
            self.assertFalse(test_person.has_role(test_role))

            test_person.add_role(test_role)

            self.assertIs(test_person.get_role_reference(test_role), test_role)
            self.assertIs(test_person.get_role_reference_by_name("Test role"), test_role)

        def test_lookalike_role_manipulation(self):
            test_person = create_random_person()
            test_role = Role("Test role")
            lookalike_role = Role("Lookalike role", looks_like = test_role)

            test_person.add_role(test_role)

            self.assertTrue(test_person.has_role(test_role))
            self.assertFalse(test_person.has_role(lookalike_role))

            test_person.remove_role(test_role)
            test_person.add_role(lookalike_role)

            self.assertTrue(test_person.has_role(test_role))
            self.assertTrue(test_person.has_role(lookalike_role))
            self.assertFalse(test_person.has_exact_role(test_role))
            self.assertTrue(test_person.has_exact_role(lookalike_role))

            test_person.remove_role(lookalike_role)

            self.assertFalse(test_person.has_role(test_role))
            self.assertFalse(test_person.has_role(lookalike_role))

        def test_layered_lookalike_roles(self):
            role_1 = Role("Role_1")
            role_2 = Role("Role_2", looks_like = role_1)
            role_3 = Role("Role_3", looks_like = role_2)

            test_person = create_random_person()
            test_person.add_role(role_1)

            self.assertTrue(test_person.has_role(role_1))
            self.assertFalse(test_person.has_role(role_2))
            self.assertFalse(test_person.has_role(role_3))

            test_person.remove_role(role_1)
            test_person.add_role(role_2)

            self.assertTrue(test_person.has_role(role_1))
            self.assertTrue(test_person.has_role(role_2))
            self.assertFalse(test_person.has_role(role_3))

            test_person.remove_role(role_2)
            test_person.add_role(role_3)

            self.assertTrue(test_person.has_role(role_1))
            self.assertTrue(test_person.has_role(role_2))
            self.assertTrue(test_person.has_role(role_3))

        def test_infraction_manipulation(self):
            test_person = create_random_person()

            test_infraction = Infraction.careless_accident_factory()
            test_person.add_infraction(test_infraction, add_to_log = False)

            self.assertNotIn(test_infraction, test_person.infractions)

            test_person.add_infraction(test_infraction, add_to_log = False, require_policy = False)

            self.assertIn(test_infraction, test_person.infractions)

            test_person.remove_infraction(test_infraction)

            self.assertNotIn(test_infraction, test_person.infractions)

        def test_break_taboo(self):
            test_person = create_random_person()

            self.assertTrue(test_person.has_taboo("kissing"))
            self.assertTrue(test_person.has_taboo("underwear_nudity"))

            self.assertTrue(test_person.break_taboo("kissing"))

            self.assertFalse(test_person.has_taboo("kissing"))
            self.assertTrue(test_person.has_taboo("underwear_nudity"))
            self.assertFalse(test_person.break_taboo("kissing"))

        def test_get_opinion(self):
            test_person = create_random_person()
            test_person.opinions["Test Normal"] = [1,False]
            test_person.sexy_opinions["Test Sexy"] = [2,False]

            self.assertTrue(test_person.has_unknown_opinions())

            while test_person.has_unknown_opinions(sexy_opinions = False):
                test_person.discover_opinion(test_person.get_random_opinion(include_known = False, include_sexy = False))

            self.assertTrue(test_person.has_unknown_opinions())
            self.assertFalse(test_person.has_unknown_opinions(sexy_opinions = False))

            while test_person.has_unknown_opinions():
                test_person.discover_opinion(test_person.get_random_opinion(include_known = False, include_sexy = True))

            self.assertFalse(test_person.has_unknown_opinions())
            self.assertFalse(test_person.has_unknown_opinions(sexy_opinions = False))
            self.assertFalse(test_person.has_unknown_opinions(normal_opinions = False))

        def test_opinion_manipulation(self):
            test_person = create_random_person()
            while not test_person.get_opinion_score("being fingered") == 0:
                test_person = create_random_person() #Guarantee they don't have this opinion.

            self.assertEqual(test_person.get_opinion_score("being fingered"), 0)

            test_person.create_opinion("being fingered")

            self.assertEqual(test_person.get_opinion_score("being fingered"), 1)

            test_person.strengthen_opinion("being fingered")

            self.assertEqual(test_person.get_opinion_score("being fingered"), 2)

            test_person.strengthen_opinion("being fingered")

            self.assertEqual(test_person.get_opinion_score("being fingered"), 2)

            test_person.weaken_opnion("being fingered")

            self.assertEqual(test_person.get_opinion_score("being fingered"), 1)

            test_person.weaken_opnion("being fingered")

            self.assertEqual(test_person.get_opinion_score("being fingered"), 0)

            test_person.weaken_opnion("being fingered")

            self.assertEqual(test_person.get_opinion_score("being fingered"), 0)

            test_person.create_opinion("being fingered", start_positive = False)

            self.assertEqual(test_person.get_opinion_score("being fingered"), -1)

            test_person.strengthen_opinion("being fingered")

            self.assertEqual(test_person.get_opinion_score("being fingered"), -2)

            test_person.strengthen_opinion("being fingered")

            self.assertEqual(test_person.get_opinion_score("being fingered"), -2)

            test_person.weaken_opnion("being fingered")
            test_person.weaken_opnion("being fingered")

            self.assertEqual(test_person.get_opinion_score("being fingered"), 0)

        def test_trance_proc(self):
            test_person = create_random_person()

            self.assertFalse(test_person.has_role(trance_role))

            test_person.run_orgasm(show_dialogue = False, trance_chance_modifier = -10, add_to_log = False)

            self.assertFalse(test_person.has_role(trance_role))

            test_person.run_orgasm(show_dialogue = False, trance_chance_modifier = 200, add_to_log = False)

            self.assertTrue(test_person.has_exact_role(trance_role))

            test_person.run_orgasm(show_dialogue = False, force_trance = True, add_to_log = False)

            self.assertTrue(test_person.has_exact_role(heavy_trance_role))

            test_person.run_turn()

            self.assertTrue(test_person.has_exact_role(trance_role))

            test_person.run_turn()

            self.assertFalse(test_person.has_role(trance_role))
