init -2 python:
    class Object(renpy.store.object): #Contains a list of traits for the object which decides how it can be used. #TODO: We need to rename this, this is just asking for a major namespace collision
        def __init__(self,name,traits,sluttiness_modifier = 0, obedience_modifier = 0):
            self.traits = traits
            self.name = name
            self.sluttiness_modifier = sluttiness_modifier #Changes a girls sluttiness when this object is used in a sex scene
            self.obedience_modifier = obedience_modifier #Changes a girls obedience when this object is used in a sex scene.

        def has_trait(self,the_trait):
            for trait in self.traits:
                if trait == the_trait:
                    return True
            return False

        def get_formatted_name(self):
            if not (self.sluttiness_modifier == 0 and self.obedience_modifier == 0):
                the_string = self.name + "\n{size=22}"
                if self.sluttiness_modifier != 0 or self.obedience_modifier != 0:
                    the_string += "Temporary Modifiers\n"

                if self.sluttiness_modifier < 0:
                    the_string += str(self.sluttiness_modifier) + " Sluttiness"
                    if not self.obedience_modifier == 0:
                        the_string += ", "
                if self.sluttiness_modifier > 0:
                    the_string += "+" + str(self.sluttiness_modifier) + " Sluttiness"
                    if not self.obedience_modifier == 0:
                        the_string += ", "

                if self.obedience_modifier < 0:
                    the_string += str(self.obedience_modifier) + " Obedience"

                if self.obedience_modifier >0:
                    the_string += "+" + str(self.obedience_modifier) + " Obedience"

                the_string += "{/size} (tooltip)The object you have sex on influences how enthusiastic and obedient a girl will be."
                return the_string
            else:
                return self.name
