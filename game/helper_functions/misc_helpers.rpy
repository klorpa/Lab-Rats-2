init -1 python:
    def sort_display_list(the_item): #Function to use when sorting lists of actions (and potentially people or strings)
        extra_args = None
        if isinstance(the_item, list): #If it's a list it's actually an item of some sort with extra args. Break those out and continue.
            extra_args = the_item[1]
            the_item = the_item[0]

        if isinstance(the_item, Action):
            if the_item.is_action_enabled(extra_args):
                return the_item.priority
            else:
                return the_item.priority - 1000 #Apply a ranking penalty to disabled items. They will appear in priority order but below enabled events (Unless something has a massive priority).

        elif isinstance(the_item, Person):
            return the_item.core_sluttiness #Order people by sluttiness? Love? Something else?

        else:
            return 0

    def get_coloured_arrow(direction):
        if direction < 0:
            return "{image=gui/heart/Red_Down.png}"

        elif direction > 0:
            return "{image=gui/heart/Green_Up.png}"

        else:
            return "{image=gui/heart/Grey_Steady.png}"
