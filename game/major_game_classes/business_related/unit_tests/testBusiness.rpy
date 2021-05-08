init 0 python:
    class TestBusiness(unittest.TestCase):
        def setUp(self):
            test_room = Room("Test Room")
            new_business = Business("Test Business", test_room, test_room, test_room, test_room, test_room)

            self.test_business = new_business

        def test_existance(self):
            self.assertIsInstance(mc.business, Business)

        def test_init(self):
            self.assertIsInstance(self.test_business, Business) #Business exists, no crashes during init

            self.assertEqual(self.test_business.get_employee_count(),0) #Properly contains no people at start.

        def test_hire_employee(self):
            total_count = 0
            self.assertEqual(self.test_business.get_employee_count(), 0)

            for job_department_add in [Business.add_employee_research, Business.add_employee_production, Business.add_employee_marketing, Business.add_employee_supply, Business.add_employee_hr]:
                self.assertEqual(self.test_business.get_employee_count(),total_count)

                test_person = create_random_person()
                job_department_add(self.test_business, test_person)

                self.assertEqual(self.test_business.get_employee_count(),total_count + 1)
                self.assertTrue(test_person in self.test_business.get_employee_list())
                self.assertTrue(test_person.has_role(employee_role))
                total_count += 1

        def test_fire_employee(self):
            self.assertEqual(self.test_business.get_employee_count(), 0)

            test_person = create_random_person()
            self.test_business.add_employee_research(test_person)
            self.assertEqual(self.test_business.get_employee_count(), 1)
            self.assertTrue(test_person.has_role(employee_role))

            self.test_business.remove_employee(test_person)
            self.assertEqual(self.test_business.get_employee_count(), 0)
            self.assertFalse(test_person.has_role(employee_role))
