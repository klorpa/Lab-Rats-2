#Contains all of the events related to the office busywork role, given by one of the punishment options.

init -2 python:
    def employee_busywork_on_turn(the_person):
        if mc.business.is_open_for_business():
            mc.business.change_team_effectiveness(-1) #She's slightly worse for efficency because she's not focusing

    def employee_busywork_on_day(the_person):
        if mc.business.is_open_for_business():
            the_person.change_obedience(1)

    def employee_busywork_remove_requirement(the_person, trigger_day):
        if day >= trigger_day:
            return True
        return False

    def employee_busywork_report_requirement(the_person):
        if not mc.business.is_open_for_business():
            return False
        elif not mc.is_at_work():
            return False
        return True

label employee_busywork_remove_label(the_person):
    python:
        if employee_busywork_role in the_person.special_role:
            the_person.remove_role(employee_busywork_role)

        if employee_role in the_person.special_role: #She may have quit/been fired since then.
            busywork_report_action = Action("Busywork report crisis", employee_busywork_report_requirement, "employee_busywork_report_label", args = the_person, requirement_args = the_person)
            mc.business.mandatory_crises_list.append(busywork_report_action)

    return

label employee_busywork_report_label(the_person):
    # The person tells you about their week being the office bitch.
    if employee_role not in the_person.special_role:
        return
    $ the_person.draw_person()
    "[the_person.title] catches your attention while you are working."
    the_person "Do you have a moment [the_person.title]?"
    mc.name "Sure, what do you need?"
    the_person "I wanted to let you know that I've finished my week of punishment."
    menu:
        "Tell me about it.":
            mc.name "Good. Tell me about it."
            the_person "I've been doing coffee runs for the office every day, which people seemed to appreciate."
            the_person "Someone told a client I was the office secretary and gave them my phone number. I've been answering calls all week, every hour of the day."
            the_person "The hardest part was getting my normal work done. I tried to stay on top of it, but it's been piling up."
            menu:
                "Punish her for unfinished work.":
                    mc.name "I've noticed that you have been leaving unfinished work."
                    $ the_person.add_infraction(Infraction.underperformance_factory())
                    mc.name "That will be a separate disciplinary problem to resolve later. Don't let this happen again, understood?"

                "Let her go.":
                    mc.name "I hope you've learned something from the experience. Don't let this happen again."

        "Let her go.":
            mc.name "Good. Don't let this happen again."
    "She nods and steps away."
    $ clear_scene()
    return
