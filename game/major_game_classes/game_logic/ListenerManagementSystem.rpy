init -2 python:
    class ListenerManagementSystem(renpy.store.object): #Used to manage listeners in objects. Contains functiosn for enrolling and removing triggers as well as firing notices to those triggers.
        def __init__(self):
            self.event_dict = {} #THis dictionary uses strings as keys (the trigger that is called) and each key holds a list of goals. When an event is triggered each listener enrolled to the key recieves a notice (the on_trigger_funciton is called)

        def enroll_goal(self, trigger_name, the_goal):
            if trigger_name in self.event_dict:
                self.event_dict[trigger_name].append(the_goal) #Add the goal to the list.

            else: #The trigger_name is not in our dict, we need to add it then add the goal to it.
                self.event_dict[trigger_name] = [the_goal]

        def fire_event(self, trigger_name, **kwargs):
            if trigger_name in self.event_dict: #Make sure we have the key first before we go grabbing lists.
                completed_goals = [] #We store completed goals in a seperate list to let us flag things for removal without
                for goal in self.event_dict[trigger_name]:
                    if goal.call_trigger(**kwargs): #on_trigger returns true if the goal is finished and we can stop letting it know.
                        completed_goals.append(goal)
                for goal in completed_goals:
                    goal.complete_goal()
                    self.event_dict[trigger_name].remove(goal) #Remove all completed goals, they are no longer important.
