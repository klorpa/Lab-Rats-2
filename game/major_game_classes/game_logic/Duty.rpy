## A duty is similar to a Role, but it's mechanics are controlled by the business.
# -> Duties are given to employees of the MC's business, capped at that employees seniority level.
# -> Seniority levels are 1(intern, green employee), 2 (standard employee), 3(senior employee, department head).
# -> Duties are checked to add role actions/dates/interactions in the same way as roles.
init -2 python:
    class Duty(renpy.store.object):
        def __init__(self, duty_name, duty_description, actions = None,
            on_turn_function = None, internet_actions = None,
            requirement_function = None, on_move_function = None, on_day_function = None, on_apply_function = None, on_remove_function = None,
            duty_trainables = None, only_at_work = True):

            #TODO: Have a "smalltalk" label that can be called whenever you talk to a girl, she'll talk to you about her recent duties and what that entails.
            #TODO: Have an "on enterance" label that can be called instead of the generic greetings when you enter the room so it can tie into their active duties.

            self.duty_name = duty_name  #A short slug that can be shown in a menu, UI, etc.
            self.duty_description = duty_description # A paragraph to describe what this duty is, both flavour and effect
            if actions is None:
                self.actions = []
            elif isinstance(actions, list):
                self.actions = actions
            else:
                self.actions = [actions]

            self.requirement_function = requirement_function

            self.on_turn_function = on_turn_function
            self.on_move_function = on_move_function
            self.on_day_function = on_day_function

            self.on_apply_function = on_apply_function
            self.on_remove_function = on_remove_function

            self.only_at_work = only_at_work # Only run on_turn, on_move only when the employee is at work. Only run on_day when the employee went to work that day.

            if duty_trainables is None:
                self.duty_trainables = []
            elif isinstance(duty_trainables, list):
                self.duty_trainables = duty_trainables
            else:
                self.duty_trainables = [duty_trainables]

            if duty_trainables is None:
                self.duty_trainables = []
            elif isinstance(duty_trainables, list):
                self.duty_trainables = duty_trainables
            else:
                self.duty_trainables = [duty_trainables]

            if internet_actions is None:
                self.internet_actions = []
            elif isinstance(internet_actions, list):
                self.internet_actions = internet_actions
            else:
                self.internet_actions = [internet_actions]

        def __cmp__(self, other):
            matches = True
            if other is None:
                return 0
            elif not isinstance(other, Duty):
                return 0

            if not self.duty_name == other.duty_name:
                matches = False

            for an_action in self.actions:
                if not an_action in other.actions:
                    matches = False
                    break

            for an_action in other.actions:
                if not an_action in self.actions:
                    matches = False
                    break

            if not self.on_turn_function == other.on_turn_function:
                matches = False

            if not self.on_move_function == other.on_move_function:
                matches = False

            if not self.on_day_function == other.on_day_function:
                matches = False

            if not self.on_apply_function == other.on_apply_function:
                matches = False

            if not self.on_remove_function == other.on_remove_function:
                matches = False

            if matches:
                return 0
            else:
                if other is None:
                    return 1
                elif self.__hash__() < other.__hash__(): #Use hash values to break ties.
                    return -1
                else:
                    return 1

        def check_requirement(self, the_person):
            if self.requirement_function is not None:
                return self.requirement_function(the_person)
            return True


        def on_turn(self, the_person):
            if self.on_turn_function:
                self.on_turn_function(the_person)

        def on_move(self, the_person):
            if self.on_move_function:
                self.on_move_function(the_person)

        def on_day(self, the_person):
            if self.on_day_function:
                self.on_day_function(the_person)

        def on_apply(self, the_person):
            if self.on_apply_function:
                self.on_apply_function(the_person)

        def on_remove(self, the_person):
            if self.on_remove_function:
                self.on_remove_function(the_person)
