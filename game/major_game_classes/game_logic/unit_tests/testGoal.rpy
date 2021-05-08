init 0 python:
    def test_goal_true(the_goal, difficulty):
        return True

    def test_goal_on_trigger(the_goal, variable):
        return not variable

    class TestClimaxController(unittest.TestCase):
        def test_init(self):
            test_goal = Goal("test goal", "This is a test goal!", "player_flirt", "MC", test_goal_true, test_goal_on_trigger)

            self.assertIsInstance(test_goal, Goal)

        def test_check_valid(self):
            test_goal = Goal("test goal", "This is a test goal!", "player_flirt", "MC", test_goal_true, test_goal_on_trigger)

            self.assertTrue(test_goal.check_valid(1))

        def test_trigger(self):
            test_goal = Goal("test goal", "This is a test goal!", "player_flirt", "MC", test_goal_true, test_goal_on_trigger)

            self.assertTrue(test_goal.call_trigger(variable = False))
            self.assertFalse(test_goal.call_trigger(variable = True))

    #TODO: Include a test suite for ListenerManagementSystem here, since it is tied tightly into the goal system
