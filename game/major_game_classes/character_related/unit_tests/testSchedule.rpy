init 0 python:
    class TestSchedule(unittest.TestCase):
        def test_init(self):
            test_daily_schedule = DailySchedule()
            test_schedule = Schedule()

            self.assertIsInstance(test_daily_schedule, DailySchedule)
            self.assertIsInstance(test_schedule, Schedule)


        def test_daily_schedule_default_values(self):
            test_daily_schedule = DailySchedule()

            self.assertIsInstance(test_daily_schedule, DailySchedule)
            for c in range(0,5):
                self.assertIsNone(test_daily_schedule.day_plan[c])

        def test_schedule_default_values(self):
            test_schedule = Schedule()

            self.assertIsInstance(test_schedule, Schedule)
            for d in range(0,7):
                for t in range(0,4):
                    self.assertIsNone(test_schedule.schedule[d].day_plan[t])

        def test_daily_set_schedule(self):
            test_daily_schedule = DailySchedule()
            test_room = Room("Test Room")

            test_daily_schedule.set_schedule(test_room, [0,1,2])

            for c in range(0,3):
                self.assertEqual(test_daily_schedule.day_plan[c], test_room)

            for c in range(3,5):
                self.assertEqual(test_daily_schedule.day_plan[c], None)

        def test_set_schedule(self):
            test_schedule = Schedule()
            test_room = Room("Test Room")

            test_schedule.set_schedule(test_room, the_days = [0,1,2,3,4,5,6], the_times = [0,1,2])

            for d in range(0,5):
                for t in range(0,3):
                    self.assertIs(test_schedule.schedule[d].day_plan[t], test_room)

            for d in range(5,7):
                for t in range(3,5):
                    self.assertIsNone(test_schedule.schedule[d].day_plan[t])

            # test_schedule.print_schedule()

        def test_daily_get_schedule(self):
            test_daily_schedule = DailySchedule()
            test_room = Room("Test Room")

            test_daily_schedule.set_schedule(test_room, [0,1,2])

            for c in range(0,3):
                self.assertEqual(test_daily_schedule.day_plan[c], test_daily_schedule.get_destination(c))

            for c in range(3,5):
                self.assertEqual(test_daily_schedule.day_plan[c], test_daily_schedule.get_destination(c))


        def test_get_destination(self):
            test_schedule = Schedule()
            test_room = Room("Test Room")

            test_schedule.set_schedule(test_room, the_days = [0,1,2,3,4,5,6], the_times = [0,1,2])

            for d in range(0,7):
                for t in range(0,5):
                    self.assertEqual(test_schedule.get_destination(specified_day = d, specified_time = t), test_schedule.schedule[d].day_plan[t])
