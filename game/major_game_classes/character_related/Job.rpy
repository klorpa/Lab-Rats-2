init -2 python:
    class Job(renpy.store.object): # A job is just a title displayed on the screen and a name that is displayed. A person can only have one job at a time (if it's not a full time job it's just a Role).
        def __init__(self, job_title, job_role = None, job_location = None, hire_function = None, quit_function = None, work_days = None, work_times = None):
            self.job_title = job_title # The string that is displayed on the hud
            if job_role is None:
                self.job_role = unimportant_job_role
            else:
                self.job_role = job_role # The role that is added when an NPC has this job, removed when they quit this job.

            self.job_location = job_location # If job location is None than the character is allowed in to spend their job time in any of the public spaces.


            self.hire_function = hire_function # Called when a role is give to a character. Should take a Person as a parameter.
            self.quit_function = quit_function #Function called when a character quits this job. Should take a Person as a parameter

            if work_days is None:
                work_days = [0,1,2,3,4]
            if work_times is None:
                work_times = [1,2,3]
            self.schedule = Schedule()
            self.schedule.set_schedule(job_location, work_days, work_times)

        def __cmp__(self, other):
            matches = True
            if not self.job_title == other.job_title:
                matches = False
            elif not self.job_role == other.job_role:
                matches = False
            elif not self.hire_function == other.hire_function:
                matches = False
            elif not self.quit_function == other.quit_function:
                matches = False

            if matches:
                return 0
            else:
                if self.__hash__() < other.__hash__(): #Use hash values to break ties.
                    return -1
                else:
                    return 1
