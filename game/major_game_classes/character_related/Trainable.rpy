init -2 python:
    class Trainable(renpy.store.object):
        def __init__(self, short_name, on_train_label, display_name = None, base_cost = 100, unlocked_function = None, extra_args = None, doubling_amount = 2.0, training_tag = None):
            self.short_name = short_name #A short word to be used for lists and logs, but not nessesarily for display. Should be unique.
            self.on_train_label = on_train_label #A Ren'py label that is called with the person as an argument (as well as any extra args) when this is bought.
            #on_train_effect should encapsulate all effects except for paying the Clarity cost.

            if display_name is None: #display_name is a long form name used for buttons.
                self.display_name = self.short_name
            else:
                self.display_name = display_name

            self.base_cost = base_cost #Starting clarity cost before she has been trained in this before.

            self.unlocked_function = unlocked_function #A python function called to check if this trainable should be displayed. It will be passed the person and any extra args.

            if extra_args is None: #Extra arguments passed through to the train label and the unlocked function to make it easier to reuse the same base functionality.
                self.extra_args = []
            elif isinstance(extra_args,list):
                self.extra_args = extra_args
            else:
                self.extra_args = [extra_args]

            self.doubling_amount = doubling_amount*1.0 #The cost of training this thing doubles every time it has been trained doubling_amount already.

            if training_tag is None: #Training tag is used to record how often a similar thing has been trained and increase all of their costs together.
                self.training_tag = self.short_name
            else:
                self.training_tag = training_tag


        def get_full_name(self, the_person): #If an unlock function returns a string that is shown here as the reason.
            clarity_string = str(self.get_cost(the_person)) + " Clarity"
            if mc.free_clarity < self.get_cost(the_person):
                clarity_string = "{color=#ff0000}" + clarity_string + "{/color}"



            return_string = self.display_name + " - " + clarity_string
            if self.unlocked_function is not None:
                unlock_return = self.unlocked_function(the_person, *self.extra_args)
                if isinstance(unlock_return, basestring):
                    return_string += "\n{color=#ff0000}Requires: " + unlock_return + "{/color}"

            return return_string

        def get_cost(self, the_person):
            base_modified_cost = self.base_cost * (2**(the_person.training_log[self.training_tag]/self.doubling_amount))
            trance_modifier = 2.0
            if the_person.has_exact_role(heavy_trance_role):
                trance_modifier = 1.0
            elif the_person.has_exact_role(very_heavy_trance_role):
                trance_modifier = 0.5

            return int(base_modified_cost*trance_modifier)

        def is_shown(self, the_person):
            if self.unlocked_function is None:
                return True
            else:
                if self.unlocked_function(the_person, *self.extra_args):
                    return True
                else:
                    return False

        def is_unlocked(self, the_person):
            if self.unlocked_function is None: #No requirement means it's always enabled
                pass

            #Otherwise check it's requirement.
            else:
                unlock_function_return = self.unlocked_function(the_person, *self.extra_args)
                if isinstance(unlock_function_return, basestring):
                    return False
                elif unlock_function_return == False:
                    return False
                else:
                    pass

            if mc.free_clarity >= self.get_cost(the_person):
                return True
            else:
                return False
