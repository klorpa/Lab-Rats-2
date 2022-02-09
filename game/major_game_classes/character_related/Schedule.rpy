init -2 python:
    class DailySchedule(renpy.store.object):
        def __init__(self, early_morning_location = None, morning_location = None, afternoon_location = None, evening_location = None, night_location = None):
            self.day_plan = {}
            if early_morning_location is not None:
                self.day_plan[0] = early_morning_location
            else:
                self.day_plan[0] = None

            if morning_location is not None:
                self.day_plan[1] = morning_location
            else:
                self.day_plan[1] = None

            if afternoon_location is not None:
                self.day_plan[2] = afternoon_location
            else:
                self.day_plan[2] = None

            if evening_location is not None:
                self.day_plan[3] = evening_location
            else:
                self.day_plan[3] = None

            if night_location is not None:
                self.day_plan[4] = night_location
            else:
                self.day_plan[4] = None

        def get_destination(self, specified_time = None):
            if specified_time is None:
                specified_time = time_of_day
            return self.day_plan[specified_time]

        def get_copy(self): #Returns a new DailySchedule
            return_schedule = DailySchedule(self.day_plan[0], self.day_plan[1], self.day_plan[2], self.day_plan[3], self.day_plan[4])
            return return_schedule

        def set_schedule(self, the_place, the_times):
            if isinstance(the_times, list):
                for a_time in the_times: #If it's a list distribute out a bunch of single time calls.
                    self.set_schedule(the_place, a_time)
                return

            self.day_plan[the_times] = the_place

    class Schedule(renpy.store.object):
        def __init__(self,
            monday_schedule = None, tuesday_schedule = None, wednesday_schedule = None, thursday_schedule = None, friday_schedule = None,
            saturday_schedule = None, sunday_schedule = None):

            self.schedule = {} # Dict of DailySchedule

            if monday_schedule is not None:
                self.schedule[0] = monday_schedule
            else:
                self.schedule[0] = DailySchedule()
            if tuesday_schedule is not None:
                self.schedule[1] = tuesday_schedule
            else:
                self.schedule[1] = DailySchedule()
            if wednesday_schedule is not None:
                self.schedule[2] = wednesday_schedule
            else:
                self.schedule[2] = DailySchedule()
            if thursday_schedule is not None:
                self.schedule[3] = thursday_schedule
            else:
                self.schedule[3] = DailySchedule()
            if friday_schedule is not None:
                self.schedule[4] = friday_schedule
            else:
                self.schedule[4] = DailySchedule()

            if saturday_schedule is not None:
                self.schedule[5] = saturday_schedule
            else:
                self.schedule[5] = DailySchedule()
            if sunday_schedule is not None:
                self.schedule[6] = sunday_schedule
            else:
                self.schedule[6] = DailySchedule()

        def get_destination(self, specified_day = None, specified_time = None):
            if specified_day is None:
                specified_day = day%7
            else:
                specified_day = specified_day%7

            if specified_time is None:
                specified_time = time_of_day

            return self.schedule[specified_day].get_destination(specified_time)

        def get_next_destination(self):
            check_time = time_of_day + 1
            check_day = day
            if check_time > 4:
                check_day = day+1
                check_time = 0

            return self.get_destination(check_day, check_time)

        def get_copy(self): #Returns a proper copy of the schedule that has unique DailySchedule references (but referenced Locations)
            new_schedule = Schedule(
                monday_schedule = self.schedule[0].get_copy(),
                tuesday_schedule = self.schedule[1].get_copy(),
                wednesday_schedule = self.schedule[2].get_copy(),
                thursday_schedule = self.schedule[3].get_copy(),
                friday_schedule = self.schedule[4].get_copy(),
                saturday_schedule = self.schedule[5].get_copy(),
                sunday_schedule = self.schedule[6].get_copy())

            return new_schedule

        def set_schedule(self, the_place, the_days = None, the_times = None):
            if the_days is None:
                the_days = [0,1,2,3,4,5,6]
            if the_times is None:
                the_times = [0,1,2,3,4]
            if isinstance(the_days, list):
                for a_day in the_days:
                    self.set_schedule(the_place, a_day, the_times)
                return

            self.schedule[the_days].set_schedule(the_place, the_times) #Get the daily schedule for that day and set the location appropraitely

        def print_schedule(self):
            for day_number in range(0, 7):
                day_message = str(day_number) + " || "
                for time_number in range(0,5):
                    location = self.get_destination(specified_day = day_number, specified_time = time_number)
                    if isinstance(location, Room):
                        day_message += location.name + " | "
                    else:
                        day_message += "None | "
                print(day_message)
