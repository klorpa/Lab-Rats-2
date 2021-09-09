init -2 python:
    class Role(renpy.store.object): #Roles are assigned to special people. They have a list of actions that can be taken when you talk to the person and acts as a flag for special dialogue options.
        def __init__(self, role_name, actions = None, hidden = False, on_turn = None, on_move = None, on_day = None, role_dates = None, looks_like = None, role_trainables = None, internet_actions = None):
            self.role_name = role_name
            if actions is None:
                self.actions = []
            elif isinstance(actions, list):
                self.actions = actions # A list of actions that can be taken. These actions are shown when you talk to a person with this role if their requirement is met.
            else:
                self.actions = [actions]

            if internet_actions is None:
                self.internet_actions = []
            elif isinstance(internet_actions, list):
                self.internet_actions = internet_actions
            else:
                self.internet_actions = [internet_actions]

            # At some point we may want a seperate list of role actions that are available when you text someone.
            self.hidden = hidden #A hidden role is not shown on the "Roles" list
            self.on_turn = on_turn #A function that is run each turn on every person with this Role.
            self.on_move = on_move #A function that is run each move phase on every person with this Role.
            self.on_day = on_day

            if role_dates is None:
                self.role_dates = [] # A role date is an action that should be added to the list of date triggers.
            elif isinstance(role_dates, list):
                self.role_dates = role_dates
            else:
                self.role_dates = [role_dates]

            self.linked_roles = [] #A list of other roles. If this role is removed, all linked roles are removed as well.
            if looks_like is None:
                self.looks_like = [] #A list of other roles. when has_role() is used this role is treated as any of the roles in looks_like for comparison purposes. NOTE: Does not inherit actual role actions.
            elif isinstance(looks_like, list):
                self.looks_like = looks_like
            else:
                self.looks_like = [looks_like]

            if role_trainables is None: #Trainable entries added when a girl is in a trance.
                self.role_trainables = []
            elif isinstance(role_trainables, list):
                self.role_trainables = role_trainables
            else:
                self.role_trainables = [role_trainables]

        def __cmp__(self,other):
            matches = True
            if not self.role_name == other.role_name:
                matches = False

            for an_action in self.actions:
                if not an_action in other.actions:
                    matches = False
                    break

            for an_action in other.actions:
                if not an_action in self.actions:
                    matches = False
                    break

            if not self.on_turn == other.on_turn:
                matches = False

            if not self.on_move == other.on_move:
                matches = False

            if not self.on_day == other.on_day:
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

        def run_turn(self, the_person):
            if self.on_turn is not None:
                self.on_turn(the_person)

        def run_move(self, the_person):
            if self.on_move is not None:
                self.on_move(the_person)

        def run_day(self, the_person):
            if self.on_day is not None:
                self.on_day(the_person)

        def link_role(self, the_role):
            if the_role not in self.linked_roles:
                self.linked_roles.append(the_role)

        def check_looks_like(self, the_role):
            for lookalike in self.looks_like:
                if the_role == lookalike:
                    return True
                return lookalike.check_looks_like(the_role)
            return False
