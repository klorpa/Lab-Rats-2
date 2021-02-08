#Contains all of the events related to the humiliating office work role, given by one of the punishment options.

init -2 python:
    def employee_humiliating_work_on_turn(the_person):
        if mc.business.is_open_for_business():
            mc.business.change_team_effectiveness(-2) #Worse for team efficency


    def employee_humiliating_work_on_day(the_person):
        if mc.business.is_open_for_business():
            the_person.change_obedience(2)
            the_person.change_happiness(-5)

    def employee_humiliating_work_remove_requirement(the_person, trigger_day):
        if day >= trigger_day:
            return True
        return False

    def employee_humiliating_work_report_requirement(the_person):
        if not mc.business.is_open_for_business():
            return False
        elif not mc.is_at_work():
            return False
        return True

label employee_humiliating_work_remove_label(the_person):
    python:
        if employee_humiliating_work_role in the_person.special_role:
            the_person.remove_role(employee_humiliating_work_role)

        if employee_role in the_person.special_role: #She may have quit/been fired since then.
            humiliating_work_report_action = Action("Humiliating work report crisis", employee_humiliating_work_report_requirement, "employee_humiliating_work_report_label", args = the_person, requirement_args = the_person)
            mc.business.mandatory_crises_list.append(humiliating_work_report_action)

    return

label employee_humiliating_work_report_label(the_person):
    if employee_role not in the_person.special_role: #She's already been fired, just finish.
        return

    $ the_person.draw_person()
    "[the_person.title] catches your attention while you are working."
    the_person "Do you have a moment [the_person.title]?"
    mc.name "Sure, what do you need?"
    the_person "I wanted to let you know that I've finished my week of punishment."
    menu:
        "Tell me about it.":
            mc.name "Good. Tell me about it."
            the_person "It was terrible, [the_person.mc_title]. The bathrooms are disgusting, and things get dirty the moment I finish cleaning them!"
            the_person "I never want to have to do that again, it felt so demeaning!"
            mc.name "What about your other work? Any performace issues to report?"
            the_person "I tried my best, but there was just so much to do every day. I'm sorry, but I haven't been able to keep up."
            menu:
                "Punish her for unfinished work.":
                    mc.name "Well that's simply not acceptable. We'll have to talk about this later. Understood?"
                    $ the_person.add_infraction(Infraction.underperformance_factory())

                "Let her go.":
                    mc.name "I hope you've learned something from the experience. Don't let this happen again."

        "Let her go.":
            mc.name "Good. Don't let this happen again."

    "She nods and steps away."
    $ clear_scene()
    return
