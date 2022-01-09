init -2 python:
    class Policy(renpy.store.object): # An upgrade that can be purchased by the character for their business.
        def __init__(self, name, desc, requirement, cost, toggleable = False,
            on_buy_function = None, extra_arguments = None, on_apply_function = None, on_remove_function = None, on_turn_function = None, on_move_function = None, on_day_function = None, dependant_policies = None):

            self.name = name #A short name for the policy.
            self.desc = desc #A text description of the policy.
            self.requirement = requirement #a function that is run to see if the PC can purchase this policy.
            self.cost = cost #Cost in dollars.

            self.toggleable = toggleable #If True this policy can be toggled on and off. Otherwise, it is set "active" when bought and can never be deactivated.


            if extra_arguments is None:
                self.extra_arguments = {}
            else:
                self.extra_arguments = extra_arguments #A dictionary of extra values that can be used by the various on_buy, on_apply, etc. functions

            self.on_buy_function = on_buy_function #A function to be called when purchased
            self.on_apply_function = on_apply_function
            self.on_remove_function = on_remove_function
            self.on_turn_function = on_turn_function #These functions are applied to anyone with the Employee role. Policies that affect people with specific sub-roles
            self.on_move_function = on_move_function
            self.on_day_function = on_day_function

            if dependant_policies is None:
                self.dependant_policies = []
            elif isinstance(dependant_policies, Policy):
                self.dependant_policies = [dependant_policies] #If we hand a single item wrap it in a list for iteration purposes
            else:
                self.dependant_policies = dependant_policies # Otherwise we have a list already.

            self.depender_policies = [] #These policies depend _on_ us, and are declared when other policies are defined. If they are on, we cannot toggle off.
            for policy in self.dependant_policies:
                policy.depender_policies.append(self) #Esentially builds a two way linked list of policies while allowing us to only define the requirements from the base up. Also conveniently stops dependency cycles from forming.


        def __cmp__(self,other): #
            if type(other) is Policy:
                if self.name == other.name and self.desc == other.desc and self.cost == other.cost:
                    return 0
                else:
                    if self.__hash__() < other.__hash__(): #Use hash values to break ties.
                        return -1
                    else:
                        return 1

            else:
                if self.__hash__() < other.__hash__(): #Use hash values to break ties.
                    return -1
                else:
                    return 1

        def __hash__(self):
            return hash((self.name,self.desc,self.cost))

        def is_owned(self):
            if self in mc.business.policy_list:
                return True
            else:
                return False

        def is_active(self):
            if self in mc.business.active_policy_list:
                return True
            else:
                return False

        def is_toggleable(self):
            return_toggle = True
            if self.is_owned and self.toggleable: #If a policy is supposed to be toggleable:
                if self in mc.business.active_policy_list: # We are currently active, so we are only disable-able if all of the dependers are off.
                    for policy in self.depender_policies:
                        if policy.is_active(): #If any of the policies that rely on this are active we cannot toggle off.
                            return_toggle = False

                else: # We are owned but not active. We can only be toggled if every policy in our dependant list is active
                    for policy in self.dependant_policies:
                        if not policy.is_active():
                            return_toggle = False

            else:
                return_toggle = False

            return return_toggle

        def buy_policy(self, ignore_cost = False):
            mc.business.policy_list.append(self)
            if not ignore_cost:
                mc.business.change_funds(-self.cost)
            if self.on_buy_function is not None:
                self.on_buy_function(**self.extra_arguments)

        def apply_policy(self):
            mc.business.active_policy_list.append(self)
            if self.on_apply_function is not None:
                self.on_apply_function(**self.extra_arguments)
            return

        def remove_policy(self):
            if self in mc.business.active_policy_list:
                mc.business.active_policy_list.remove(self)
                if self.on_remove_function is not None:
                    self.on_remove_function(**self.extra_arguments)
            return

        def on_turn(self):
            if self.on_turn_function is not None:
                self.on_turn_function(**self.extra_arguments)
            return

        def on_move(self):
            if self.on_move_function is not None:
                self.on_move_function(**self.extra_arguments)
            return

        def on_day(self):
            if self.on_day_function is not None:
                self.on_day_function(**self.extra_arguments)
            return
