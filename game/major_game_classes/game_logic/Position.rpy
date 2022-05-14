init -2 python:
    class Position(renpy.store.object):
        def __init__(self,name,slut_requirement,slut_cap,requires_hard, requires_large_tits,
            position_tag,requires_location,requires_clothing,skill_tag,
            girl_arousal,girl_energy,guy_arousal,guy_energy,connections,
            intro,scenes,outro,transition_default,
            strip_description, strip_ask_description,
            orgasm_description,
            taboo_break_description,
            verb = "fuck", verbing = None, opinion_tags = None, record_class = None,
            default_animation = None, modifier_animations = None,
            associated_taboo = None):


            self.name = name
            self.slut_requirement = slut_requirement #The required slut score of the girl. Obedience will help fill the gap if possible, at a happiness penalty. Value from 0 (almost always possible) to ~100
            self.slut_cap = slut_cap #The maximum sluttiness that this position will have an effect on.
            self.requires_hard = requires_hard
            self.requires_large_tits = requires_large_tits

            self.girl_arousal = girl_arousal # The base arousal the girl receives from this position.
            self.girl_energy = girl_energy # The amount of energy the girl spends on this position.

            self.guy_arousal = guy_arousal # The base arousal the guy receives from this position.
            self.guy_energy = guy_energy # The base energy the guy spends on this position.

            self.position_tag = position_tag # The tag used to get the correct position image set.
            self.requires_location = requires_location # A tag that must match an object to have sex on it (eg. "lean", which needs something like a wall to lean against)
            self.requires_clothing = requires_clothing # A tag that notes what (lack of) clothing requirements the position has. Vaginal requires access to her vagina, tits her tits.
            self.skill_tag = skill_tag #The skill that will provide a bonus to this position.
            self.opinion_tags = opinion_tags #The opinion that will be checked each round.
            self.connections = connections
            self.intro = intro
            self.taboo_break_description = taboo_break_description #Called instead of the intro/transition when you break a taboo with someone. Should include call to personality taboo specific dialogue.
            self.scenes = scenes
            self.outro = outro
            self.transition_default = transition_default #TODO: add transitions that go between related positions but with different objects. Things like standing sex into fucking her against a window.
            self.transitions = []
            self.strip_description = strip_description
            self.strip_ask_description = strip_ask_description
            self.orgasm_description = orgasm_description
            self.verb = verb #A verb used to describe the position. "Fuck" is default, and mostly used for sex positions or blowjobs etc. Kiss, Fool around, etc. are also possibilities.
            if verbing is None: #The verb used as "Go back to [verbing] her.". Added specifically to support things like grope/groping, which have different spellings depending.
                self.verbing = verb + "ing"
            else:
                self.verbing = verbing
            self.record_class = record_class #A key to Person.sex_record[] that is updated once (and only once!) per sexual encounter if this position is picked.

            self.current_modifier = None #We will update this if the posisiion has a special modifier that shoudl be applied, like blowjob.

            if default_animation is None:
                self.default_animation = idle_wiggle_animation
            else:
                self.default_animation = default_animation #If not None this is used to animate the character if nothing else is specifically handed over.

            if modifier_animations is None: #If an animation exists for a special modifier it is used instead of the default one.
                self.modifier_animations = {}
            else:
                self.modifier_animations = modifier_animations

            self.associated_taboo = associated_taboo #What taboo tag, if any, is associated with this position. Until broken a taboo makes a position harder to select, but the taboo is broken once it is done once.
            # Current sex related taboo are:
            # kissing, touching_body, touching_penis, touching_vagina, sucking_cock, licking_pussy, vaginal_sex, anal_sex
            # And as a special case for vaginal sex: condomless_sex

        def link_positions(self,other,transition_label): #This is a one way link!
            self.connections.append(other)
            self.transitions.append([other,transition_label])

        def link_positions_two_way(self,other,transition_label_1,transition_label_2): #Link it both ways. Great for adding a modded position without modifying other positions.
            self.link_positions(other,transition_label_1)
            other.link_positions(self,transition_label_2)

        def call_intro(self, the_person, the_location, the_object):
            renpy.call(self.intro,the_person, the_location, the_object)

        def call_taboo_break(self, the_person, the_location, the_object):
            renpy.call(self.taboo_break_description, the_person, the_location, the_object)

        def call_scene(self, the_person, the_location, the_object):
            random_scene = renpy.random.randint(0,len(self.scenes)-1)
            renpy.call(self.scenes[random_scene],the_person, the_location, the_object)

        def call_outro(self, the_person, the_location, the_object):
            renpy.call(self.outro,the_person, the_location, the_object)

        def call_transition(self, the_position, the_person, the_location, the_object):
            if the_position is None:
                transition_scene = self.transition_default #If we don't care what position we started in we can call the transition "in reverse" by setting the position to None and using our own default.
            else:
                transition_scene = the_position.transition_default
                for position_tuple in self.transitions:
                    if position_tuple[0] == the_position: ##Does the position match the one we are looking for?
                        transition_scene = position_tuple[1] ##If so, set it's label as the one we are going to change to.
            renpy.call(transition_scene, the_person, the_location, the_object)

        def call_strip(self, the_person, the_clothing, the_location, the_object):
            renpy.call(self.strip_description, the_person, the_clothing, the_location, the_object)

        def call_strip_ask(self, the_person, the_clothing, the_location, the_object):
            renpy.call(self.strip_ask_description, the_person, the_clothing, the_location, the_object)

        def call_orgasm(self, the_person, the_location, the_object):
            renpy.call(self.orgasm_description, the_person, the_location, the_object)

        def check_clothing(self, the_person):
            if self.requires_clothing == "Vagina":
                return the_person.outfit.vagina_available()
            elif self.requires_clothing == "Tits":
                return the_person.outfit.tits_available()
            else:
                return True ##If you don't have one of the requirements listed above just let it happen.

        def calculate_arousal_modified_speed(self, the_person):
            male_energy_fraction = (1.0*self.guy_energy) / (self.guy_energy+self.girl_energy)  # Animation strength is divided based on who is spending more energy (ie. girls giving blowjobs speed up as they get horny, not you).
            male_animation_effect = male_energy_fraction * (mc.arousal/mc.max_arousal)  # Being closer to max arousal increases the speed of the animation.

            female_energy_fraction = (1.0*self.girl_energy) / (self.guy_energy+self.girl_energy)
            female_animation_effect = female_energy_fraction * (1.0*the_person.arousal/the_person.max_arousal)

            the_animation_speed = 0.5 + (0.5 * (male_animation_effect + female_animation_effect)) #Scales the animation strength from 50% to 100%, increasing as each party gets more aroused.

            return the_animation_speed

        def redraw_scene(self, the_person, emotion = None): #redraws the scene, call this when something is modified.
            the_animation_speed = self.calculate_arousal_modified_speed(the_person)

            if self.current_modifier in self.modifier_animations:
                position_animation = self.modifier_animations[self.current_modifier]
            else:
                position_animation = self.default_animation

            the_person.draw_person(self.position_tag, emotion = emotion, special_modifier = self.current_modifier, the_animation = position_animation, animation_effect_strength = the_animation_speed)

        def her_position_willingness_check(self, the_person, ignore_taboo = False): #Checks if the given girl would/can pick this position. A mirror of the main character's options.
            possible = True

            position_taboo = self.associated_taboo
            if ignore_taboo:
                position_taboo = None

            final_slut_requirement = self.slut_requirement
            final_slut_cap = self.slut_cap
            if self.skill_tag == "Anal" and the_person.has_family_taboo():
                final_slut_requirement += -10 #It's easier to convince a family member to have anal sex, since it's not "real" incest or something.
                final_slut_cap += -10
            elif self.skill_tag == "Vaginal" and the_person.has_family_taboo():
                final_slut_requirement += 10 #It's harder to convince a family member to have vaginal sex
                final_slut_cap += 10


            if final_slut_requirement > the_person.effective_sluttiness(position_taboo):
                possible = False # Too slutty for her.
            elif not self.check_clothing(the_person):
                possible = False # Clothing is in the way.
            elif mc.energy < self.guy_energy or the_person.energy < self.girl_energy:
                possible = False # One of them is too tired.
            elif self.requires_hard and mc.recently_orgasmed:
                possible = False # The mc has cum recently and isn't hard.
            elif self.requires_large_tits and not the_person.has_large_tits():
                possible = False # You need large tits for this and she doesn't have it.

            return possible

        def build_position_willingness_string(self, the_person, ignore_taboo = False): #Generates a string for this position that includes a tooltip and coloured willingness for the person given.
            willingness_string = ""
            tooltip_string = ""

            # girl_expected_arousal = str(int(self.girl_arousal * (1 + 0.1 * mc.sex_skills[self.skill_tag]))) #Estimate what they'll gain based on both of your skills to make the predictions as accurate as possible.
            # guy_expected_arousal = str(int(self.guy_arousal * (1 + 0.1 * the_person.sex_skills[self.skill_tag])))

            # energy_string = build_energy_string(the_person)
            # arousal_string = build_arousal_string(the_person)

            disable = False

            position_taboo = self.associated_taboo
            if ignore_taboo:
                position_taboo = None

            taboo_break_string = ""
            if the_person.has_taboo(position_taboo):
                taboo_break_string = " {image=gui/extra_images/taboo_break_token.png} "

            final_slut_requirement = self.slut_requirement
            final_slut_cap = self.slut_cap
            if self.skill_tag == "Anal" and the_person.has_family_taboo():
                final_slut_requirement += -10 #It's easier to convince a family member to have anal sex, since it's not "real" incest or something.
                final_slut_cap += -10
            elif self.skill_tag == "Vaginal" and the_person.has_family_taboo():
                final_slut_requirement += 10 #It's harder to convince a family member to have vaginal sex
                final_slut_cap += 10

            if the_person.effective_sluttiness(position_taboo) > final_slut_cap:
                if the_person.arousal > final_slut_cap:
                    willingness_string = "{color=#6b6b6b}Boring{/color}" #No sluttiness gain AND half arousal gain
                    tooltip_string = " (tooltip)This position is too boring to interest her when she is this horny. No sluttiness increase and her arousal gain is halved."
                else:
                    willingness_string = "{color=#3C3CFF}Comfortable{/color}" #No sluttiness
                    tooltip_string = " (tooltip)This position is too tame for her tastes. No sluttiness increase, but it may still be a good way to get warmed up and ready for other positions."
            elif the_person.effective_sluttiness(position_taboo) >= final_slut_requirement:
                willingness_string = "{color=#3DFF3D}Exciting{/color}" #Normal sluttiness gain
                tooltip_string = " (tooltip)This position pushes the boundry of what she is comfortable with. Increases temporary sluttiness, which may become permanent over time or with serum application."
            elif the_person.effective_sluttiness(position_taboo) + the_person.obedience-100 >= final_slut_requirement:
                willingness_string = "{color=#FFFF3D}Likely Willing if Commanded{/color}"
                tooltip_string = " (tooltip)This position is beyond what she would normally consider. She is obedient enough to do it if she is commanded, at the cost of some happiness."
            else:
                willingness_string = "{color=#FF3D3D}Likely Too Slutty{/color}"
                tooltip_string = " (tooltip)This position is so far beyond what she considers appropriate that she would never dream of it."

            if the_person.has_taboo(position_taboo):
                tooltip_string +="\nSuccessfully selecting this position will break a taboo, making it easier to convince " + the_person.title + " to do it and similar acts in the future."


            if not self.check_clothing(the_person):
                disable = True
                willingness_string += "\nObstructed by clothing"
            elif mc.recently_orgasmed and self.requires_hard:
                disable = True
                willingness_string += "\nRecently orgasmed"
            elif mc.energy < self.guy_energy and the_person.energy < self.girl_energy:
                disable = True
                willingness_string += "\nYou're both too tired"
            elif mc.energy < self.guy_energy:
                disable = True
                willingness_string += "\nYou're too tired"
            elif the_person.energy < self.girl_energy:
                disable = True
                willingness_string += "\nShe's too tired"
            #else:

            if disable:
                return taboo_break_string + self.name + taboo_break_string + "\n{size=22}"+ willingness_string + "{/size}" + " (disabled)" #Don't show the arousal and energy string if it's disabled to prevent overrun
            else:
                return taboo_break_string + self.name + taboo_break_string  + "\n{size=22}" + willingness_string + "\n" + self.build_energy_arousal_line(the_person) + "{/size}" + tooltip_string

        def calculate_energy_cost(self, the_person): # Calculates this positions's true energy cost based on the skill of the participants.
            base_energy = 0
            if isinstance(the_person, Person):
                base_energy = self.girl_energy
            else:
                base_energy = self.guy_energy
            return __builtin__.int(base_energy * (1 - (0.05*the_person.sex_skills[self.skill_tag])))

        def build_energy_string(self, the_person):
            return "{color=#3C3CFF}" + str(self.calculate_energy_cost(mc)) + "{/color}/{color=#F0A8C0}" + str(self.calculate_energy_cost(the_person)) + "{/color} {image=gui/extra_images/energy_token.png}"

        def build_arousal_string(self, the_person):
            girl_expected_arousal = str(int(self.girl_arousal * (1 + 0.1 * mc.sex_skills[self.skill_tag]))) #Estimate what they'll gain based on both of your skills to make the predictions as accurate as possible.
            guy_expected_arousal = str(int(self.guy_arousal * (1 + 0.1 * the_person.sex_skills[self.skill_tag])))
            return "{color=#3C3CFF}" + guy_expected_arousal + "{/color}/{color=#F0A8C0}" + girl_expected_arousal + "{/color} {image=gui/extra_images/arousal_token.png}"

        def build_energy_arousal_line(self, the_person):
            return "{size=22}" + self.build_energy_string(the_person) + " | " + self.build_arousal_string(the_person) + "{/size}"
