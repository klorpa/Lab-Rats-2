init 0 python:
    def test_policy_requirement():
        return True

    class TestPolicy(unittest.TestCase):
        def setUp(self):
            mc.business.policy_list = [] #Makes sure we don't have policies left in this list from a previous test.

        def test_init(self):
            test_policy = Policy("Test Policy", "This is a test description", test_policy_requirement, 100)
            self.assertIsInstance(test_policy, Policy)

        def test_policy_purchase(self):
            test_policy = Policy("Test Policy", "This is a test description", test_policy_requirement, 100)
            start_cash = mc.business.funds

            test_policy.buy_policy()
            self.assertEqual(start_cash - test_policy.cost, mc.business.funds)
            self.assertTrue(test_policy in mc.business.policy_list)

        def test_policy_toggle(self):
            test_policy = Policy("Test Policy", "This is a test description", test_policy_requirement, 100, toggleable = True)

            test_policy.buy_policy()
            self.assertNotIn(test_policy, mc.business.active_policy_list)

            toggle_policy(test_policy)
            self.assertIn(test_policy, mc.business.active_policy_list)

            toggle_policy(test_policy)
            self.assertNotIn(test_policy, mc.business.active_policy_list)

            self.assertIn(test_policy, mc.business.policy_list)
