init -2 python:
    def offer_to_hire_requirement(the_person):
        if the_person.love < 10:
            return False
        elif the_person.has_role(employee_role):
            return False
        elif the_person.love < 20:
            return "Requires: 20 Love"
        elif mc.business.get_employee_count() >= mc.business.max_employee_count:
            return "At employee limit."
        else:
            return True #NOTE: This doesn't guarantee they'll accept, just that you get past the generalised first stop.
        return

    def setup_employee_stats(the_person): #Centeralised funtion for setting up employee stuff when you hire them
        the_person.event_triggers_dict["employed_since"] = day
        mc.business.listener_system.fire_event("new_hire", the_person = the_person)
        for other_employee in mc.business.get_employee_list():
            town_relationships.begin_relationship(the_person, other_employee) #They are introduced to everyone at work, with a starting value of "Acquaintance"

    def stripper_hire(the_person):
        stripclub_strippers.append(the_person)

    def stripper_replace(the_person): # on_quit function called for strippers to make sure there's always somewone working at the club. Also removes them from the list of dancers
        #Note: Gabrielle is a special case and is manually added back into the list after she quits.
        # stripclub_strippers = []
        # stripclub_wardrobe = wardrobe_from_xml("Stripper_Wardrobe")
        # for i in __builtin__.range(0,4):
        a_girl = create_random_person(start_sluttiness = renpy.random.randint(15,30), job = stripper_job)
        a_girl.generate_home()
        a_girl.set_schedule(strip_club, the_times = [3,4]) #NOTE: This might not be required eventually, but for now it makes sure girls are at the club after hours, and not during the morning.
        a_girl.home.add_person(a_girl)

        if the_person in stripclub_strippers:
            stripclub_strippers.remove(the_person)



label stranger_hire_result(the_person): #Check to see if you want to hire someone.
    $ the_person.salary = the_person.calculate_base_salary()
    call hire_select_process([the_person,make_person()]) #Padded with extra random person to prevent hiring crash
    if isinstance(_return, Person):
        call hire_someone(the_person)
        $ the_person.draw_person()
        return True
    else:
        $ the_person.draw_person()
        return False

    return False
