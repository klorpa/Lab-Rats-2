## Stores all of the information about positions a girl might be in during a strip tease.
init -2 python:
    class StripteasePosition(renpy.store.object):
        def __init__(self, name,
            is_close = False,
            allows_touching = False, allows_jerking = True, allows_turning = True,
            slut_requirement = 0,
            position_towards_pose = "stand2", position_away_pose = "back_peek",
            girl_energy_cost = 5,
            girl_arousal_gain = 0,
            guy_energy_cost = 0,
            guy_arousal_gain = 0,
            intro_label = None,
            transition_label = None,
            turn_towards_label = None,
            turn_away_label = None,
            towards_labels = None,
            away_labels = None,
            climax_label = None):

            self.name = name
            self.is_close = is_close

            self.allows_touching = allows_touching
            self.allows_jerking = allows_jerking
            self.allows_turning = allows_turning

            self.slut_requirement = slut_requirement

            self.intro_label = intro_label
            self.transition_label = transition_label
            self.turn_towards_label = turn_towards_label
            self.turn_away_label = turn_away_label
            self.towards_labels = towards_labels
            self.away_labels = away_labels
            self.climax_label = climax_label

            self.position_towards_pose = position_towards_pose
            self.position_away_pose = position_away_pose

            self.girl_energy_cost = girl_energy_cost
            self.girl_arousal_gain = girl_arousal_gain

            self.guy_energy_cost = guy_energy_cost
            self.guy_arousal_gain = guy_arousal_gain


            self.leads_to = [] #Other positions should add a tuple of (position, command discription) to this list.

        #TODO: Decide what other thigns we need here.

        def call_intro(self, the_person, guy_state, for_pay):
            renpy.call(self.intro_label, the_person,  guy_state, for_pay)

        def call_transition(self, the_person, guy_state, for_pay):
            renpy.call(self.transition_label, the_person, guy_state, for_pay)

        def call_description(self, the_person, direction, guy_state, for_pay):
            if direction == "towards":
                renpy.call(get_random_from_list(self.towards_labels), the_person, guy_state, for_pay)
            else:
                renpy.call(get_random_from_list(self.away_labels), the_person, guy_state, for_pay)

        def call_turn_description(self, the_person, new_direction, guy_state, for_pay):
            if new_direction == "towards":
                renpy.call(self.turn_towards_label, the_person, guy_state, for_pay)
            else:
                renpy.call(self.turn_away_label, the_person, guy_state, for_pay)

        def call_climax(self, the_person, guy_state, for_pay):
            renpy.call(self.climax_label, the_person, guy_state, for_pay)

        def call_pose(self, the_person, direction):
            if direction == "away":
                the_person.draw_person(self.position_away_pose)
            else:
                the_person.draw_person(self.position_towards_pose)

        def has_acceptable_transition(self, the_person):
            for other in self.leads_to:
                if other[0].slut_requirement < the_person.effective_sluttiness():
                    return True

            return False
        # def call_outro(self, guy_state, for_pay):
        #     renpy.call(self.outro_label)

        # def call_strip(self, guy_state, the_clothing, for_pay):
        #     renpy.call(self.strip_label, guy_state, the_clothing, for_pay)






# Intro - what we describe when we _start_ in that position_name
# Transition - what we describe when we transition into that state (maybe from one we already know)
# Watching state - A few different descriptions of you just watching her.
# Touching state - If she's close enough to touch, a few different descriptions of you touching her.
# Jerking state - If you have your cock out a few different descriptions of you jerking off.
# Outro state for her - You made her cum by touching her, or just by looking at her.
# Outro state for you - She made you cum (maybe while jerking off)
# Strip state - She takes off a piece of clothing (maybe for money).
