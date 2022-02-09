# init -1 python:
#     def get_appropriate_normal_job(the_person):
#
#         return #TODO: Look through the existing jobs and figure out which one the person should have.

label instantiate_jobs():
    $ list_of_jobs = [] # Random characters will be given a job from this list.
    python:
        unemployed_job = Job("Unemployed", unemployed_role, work_days = [], work_times = [])

        # Your business Roles #TODO: Add the ability to give girls new titles for their job.
        # -> alternatively, have different _jobs_ within the divisions you can assign girls too.
        # -> "Mary, Job: Professional Cumdump" has a good ring to it.
        # -> Add some sort of job title progression?
        hr_job = Job("Personnel Manager", employee_role, job_location = mc.business.h_div, hire_function = setup_employee_stats)
        market_job = Job("Sales Representative",  employee_role, job_location = mc.business.m_div, hire_function = setup_employee_stats)
        rd_job = Job("R&D Scientist", employee_role, job_location = mc.business.r_div, hire_function = setup_employee_stats)
        supply_job = Job("Logistics Manager", employee_role, job_location = mc.business.s_div, hire_function = setup_employee_stats)
        production_job = Job("Production Line Worker", employee_role, job_location = mc.business.p_div, hire_function = setup_employee_stats)

        # Jobs with existing effects #TODO Some of these should leave new roles (ex-stripper, etc.) when you hire someone.
        mom_associate_job = Job("Business Associate", mom_associate_role, job_location = mom_offices, work_times = [1,2])
        mom_secretary_job = Job("Personal Secretary", mom_secretary_role, job_location = mom_offices, work_times = [1,2])

        aunt_unemployed_job = Job("Unemployed", critical_job_role, work_days = [], work_times = [])

        influencer_job = Job("Influencer", critical_job_role)


        steph_lab_assistant = Job("Lab Assistant", critical_job_role, job_location = university) #Job for Steph to technically have at the start of the game so her job title is set correctly.
        nora_professor_job = Job("Professor", critical_job_role, job_location = university)

        alexia_barista_job = Job("Barista", critical_job_role, job_location = downtown)

        emily_student_job = Job("Tutee", student_role, job_location = university, work_times = [1,2])
        sister_student_job = Job("Student", sister_student_role, job_location = university, work_times = [1,2])
        student_job = Job("Student", generic_student_role, job_location = university, work_times = [1,2]) #Note that this is different from Emily's Student role, which is really a "tutee" role.

        city_rep_job = Job("City Administartor", city_rep_role, job_location = city_hall, work_days = [0,1,2,3,4,5,6], work_times = [0,1,2,3,4]) #ie. hide her in the private City Hall location for most of the time.

        stripper_job = Job("Stripper", stripper_role, job_location = strip_club, work_days = [0,1,2,3,4,5,6], work_times = [3,4], hire_function = stripper_hire, quit_function = stripper_replace)
        prostitute_job = Job("Prostitute", prostitute_role, job_location = downtown, work_days = [0,1,2,3,4,5,6], work_times = [3,4])

        # Random city roles, with no speciifc stuff related to them.
        secretary_job = Job("Secretary", unimportant_job_role, job_location = mom_office_lobby)

        barista_job = Job("Barista", unimportant_job_role, job_location = mall)

        clothing_cashier_job = Job("Cashier", unimportant_job_role, job_location = clothing_store)
        sex_cashier_job = Job("Cashier", unimportant_job_role, job_location = sex_store)
        electronics_cashier_job = Job("Cashier", unimportant_job_role, job_location = electronics_store)
        supply_cashier_job = Job("Cashier", unimportant_job_role, job_location = office_store)
        home_improvement_cashier_job = Job("Cashier", unimportant_job_role, job_location = home_store)

        nurse_job = Job("Nurse", unimportant_job_role, job_location = downtown)
        gym_instructor_job = Job("Gym Instructor", unimportant_job_role, job_location = gym)
        office_worker_job = Job("Office Worker", unimportant_job_role, job_location = downtown)


        list_of_jobs.append(barista_job)

        list_of_jobs.append(clothing_cashier_job)
        list_of_jobs.append(sex_cashier_job)
        list_of_jobs.append(electronics_cashier_job)
        list_of_jobs.append(supply_cashier_job)
        list_of_jobs.append(home_improvement_cashier_job)

        list_of_jobs.append(nurse_job)
        list_of_jobs.append(gym_instructor_job)
        list_of_jobs.append(office_worker_job)


    return
