init -2 python:
    class GroupDisplayManager(renpy.store.object):
        default_shift_amount = 0.15
        adjust_per_person = 0.05
        def __init__(self, group_of_people, primary_speaker = None):
            self.group_of_people = group_of_people #First person in the list is drawn on the left size, with new people being added to the right
            if primary_speaker is not None and primary_speaker in self.group_of_people:
                self.primary_speaker = primary_speaker
            else:
                self.primary_speaker = group_of_people[0]

            self.last_draw_commands = {} # Tracks the list of arguments for the last draw_person or draw_animated_removal called for a person, sorted by character_number. Allows for characters to be redrawn when they are moved behind a new primary.

        def add_person(self, the_person, make_primary = False): #Add a person to the character list. Doesn't provoke a redraw automatically.
            if the_person not in self.group_of_people:
                self.group_of_people.append(the_person)

            if make_primary:
                self.primary_speaker = the_person

        def remove_person(self, the_person, new_primary = None): #Remove the_person from the list of people being drawn. Does not redraw (call redraw_group for that)
            if the_person in self.group_of_people:
                self.group_of_people.remove(the_person)
                if the_person is self.primary_speaker:
                    self.primary_speaker = None
                if the_person.character_number in self.last_draw_commands:
                    del self.last_draw_commands[the_person.character_number]

            if new_primary is not None:
                self.set_primary(the_person)

        def set_primary(self, the_person): #Note: Does not redraw #TODO: maybe it should?
            if the_person in self.group_of_people:
                self.primary_speaker = the_person

        def pick_arbitrary_primary(self): #Picks a new primary if none exists (because they have left, for example). Usually not needed, events should manage who is primary themselves.
            if len(self.group_of_people) > 0: #If there's nobody in the group by definition there is no primary.
                self.set_primary(get_random_from_list(self.group_of_people))

        # NOTE: It is most convenient to pass everything through as a key word argument, to avoid issues with normally defaulted arguments inside of draw_person or draw_animated_removal eating them as the wrong argument.
        def draw_person(self, the_person, make_primary = True, *args, **kwargs): #Seperate accessor methods to maintain consistency between group and single draws, while keeping all similar code in one place.
            self.last_draw_commands[the_person.character_number] = [args, kwargs]
            self.do_draw(the_person, Person.draw_person, make_primary, *args, **kwargs)

        def draw_animated_removal(self, the_person, make_primary = True, *args, **kwargs): #Removal draws need to have some arguments removed so we can redraw the character without redrawing the clothing removal
            # Remove animated_removal specific arguments so we can store a "draw_person" compatable set of arguments

            last_args = [] #Note: We are assuming all parameter are passed through as key words
            last_kwargs = kwargs.copy() #Note this is a shallow copy, so no copies of clothing items, ect are being made.
            if "half_off_instead" in last_kwargs:
                del last_kwargs["half_off_instead"] #Technically this could also be provided inside of args, but in practice that is a massive number of items to specify.
            if "the_clothing" in last_kwargs:
                del last_kwargs["the_clothing"]

            self.last_draw_commands[the_person.character_number] = [last_args, last_kwargs]
            self.do_draw(the_person, Person.draw_animated_removal, make_primary, *args, **kwargs)

        def draw_group(self, *args, **kwargs): #Draws every member in the group. Parameters passed are applied to everyone in the group. Draw one person at a time if you need that level of control.
            clear_scene() #We can assume we are clearing the scene if we are drawing a group.
            for group_member in self.group_of_people:
                self.draw_person(group_member, False, *args, **kwargs)

        def redraw_person(self, the_person, make_primary = True): # Draws the_person using the last recorded set of draw commands. Useful to redraw people as primary speaker change but their position does not.
            the_args, the_kwargs = self.last_draw_commands.get(the_person.character_number, [[],{}]) #If we have drawn them before reuse those parameters.
            self.draw_person(the_person, make_primary, *the_args, **the_kwargs)


        def redraw_group(self): #Attemps to redraw everyone in the group using hte last known set of draw commands. Useful when you add in a new person or someone's spacing changes
            clear_scene()
            for group_member in self.group_of_people:
                self.redraw_person(group_member, make_primary = False)

        def do_draw(self, the_person, the_draw_method, make_primary = True, *args, **kwargs): # Holds all of the similar code for all group based drawing methods (ie. passes through all information, keeping what is needed to redraw a character)
            #TODO: have the positioning account for different position widths.
            if self.primary_speaker is None: #Ensure there is always technically a primary, even if one was just removed.
                self.pick_arbitrary_primary()

            if make_primary and the_person is not self.primary_speaker: #We're replacing the primary speaker, so we need to redraw them into the background
                old_primary = self.primary_speaker
                self.set_primary(the_person)
                last_args, last_kwargs = self.last_draw_commands.get(old_primary.character_number, [[],{}]) #Get the last arguments provided.
                #last_kwargs["display_zorder"] = None #Ensures their z-position is reset and drawn properly #TODO: This is going to fuck with manually set z-levels, but we don't have a good way of dealing with that.
                self.draw_person(old_primary, make_primary = False, *last_args, **last_kwargs) #Redraw the character in their previous state, but now in the background.

            character_index = self.group_of_people.index(the_person)
            primary_index = self.group_of_people.index(self.primary_speaker)



            if len(self.group_of_people) > 1:
                posible_shift_amount = GroupDisplayManager.default_shift_amount + (GroupDisplayManager.adjust_per_person*len(self.group_of_people))
                shift_amount = 1.0 - (posible_shift_amount/(len(self.group_of_people)-1))*(character_index+1/len(self.group_of_people))
            else:
                shift_amount = 1.0

            scale_amount = 1.0
            if character_index != primary_index: #Scale down everyone who isn't the primary
                scale_amount = 0.8


            z_level = -abs(character_index - primary_index)
            # When drawing a character they are only animated if they are one of the 2 closest people to the primary speaker.
            # Note that they _stay_ animated even if the primary changes; It is almost identical to just redraw the entire group for most groups of size 5 or so.
            if primary_index == 0 or primary_index == len(self.group_of_people): #Side position primary, only animate them and 2 slots away
                if z_level < -2:
                    kwargs["the_animation"] = no_animation
            else: #Some middle psoition primary
                if z_level < -1: # Only animate characters on either side from the primary speaker.
                    kwargs["the_animation"] = no_animation

            if kwargs.get("display_transform", None) is None: # If the event specifies a specific display transform let it override (and trust the event to handle multi-person display somehow), otherwise, apply a position shift
                kwargs["display_transform"] = position_shift(shift_amount, scale_amount)

            if kwargs.get("display_zorder", None) is None:
                kwargs["display_zorder"] = z_level

            if kwargs.get("wipe_scene", None) is None:
                kwargs["wipe_scene"] = False #Don't clear the scene of other characters, we need them to remain so the whole group can be drawn/redrawn.

            the_draw_method(the_person, *args, **kwargs)
