init 0 python:
    class TestJob(unittest.TestCase):
        def test_init(self):
            test_job = Job("Test Job")
            self.assertIsInstance(test_job, Job)

        def test_job_location(self):
            test_location = Room("Test Room")
            test_job = Job("Test Job", job_location = test_location)

            self.assertIsInstance(test_job.job_location, Room)
            self.assertEqual(test_job.job_location, test_location)

        def test_job_location_schedule(self):
            test_location = Room("Test Room")
            test_job = Job("Test Job", job_location = test_location, work_days = [0,1,2,3,4,5,6], work_times = [0,1,2,3,4])

            self.assertEqual(test_job.job_location, test_location)
            self.assertEqual(test_job.schedule.get_destination(2,2),test_location)


        def test_job_location_no_schedule(self):
            test_location = Room("Test Room")
            test_job = Job("Test Job", job_location = test_location, work_days = [0,1,2,3,4,5,6], work_times = [0,4])


            # test_job.schedule.print_schedule()
            # location = test_job.schedule.get_destination(2,2)
            # print(location.name)

            self.assertEqual(test_job.job_location, test_location)
            self.assertNotEqual(test_job.schedule.get_destination(2,2),test_location)
            self.assertIsNone(test_job.schedule.get_destination(2,2))
