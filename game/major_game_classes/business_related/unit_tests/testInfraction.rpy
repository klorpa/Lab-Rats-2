init 0 python:
    class TestInfraction(unittest.TestCase):
        # def setUp(self):
        #     pass
        def test_init(self):
            test_infraction = Infraction("Test Infraction", "This is a test infraction.", 3, 7)
            self.assertIsInstance(test_infraction, Infraction)


        def test_factories(self): #Checks that all current factories are properly handing over an Infraction when called.
            test_infraction = Infraction.bureaucratic_mistake_factory()
            self.assertIsInstance(test_infraction, Infraction)

            test_infraction = Infraction.underperformance_factory()
            self.assertIsInstance(test_infraction, Infraction)

            test_infraction = Infraction.careless_accident_factory()
            self.assertIsInstance(test_infraction, Infraction)

            test_infraction = Infraction.office_disturbance_factory()
            self.assertIsInstance(test_infraction, Infraction)

            test_infraction = Infraction.out_of_uniform_factory()
            self.assertIsInstance(test_infraction, Infraction)

            test_infraction = Infraction.disobedience_factory()
            self.assertIsInstance(test_infraction, Infraction)

            test_infraction = Infraction.inappropriate_behaviour_factory()
            self.assertIsInstance(test_infraction, Infraction)
