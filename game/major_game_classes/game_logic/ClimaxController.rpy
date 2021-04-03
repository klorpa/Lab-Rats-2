init -2 python:
    #TODO: These climax types might have to be Action based at some point if we want to add requirements to them.
    class ClimaxController(renpy.store.object): #A class that allows for the easy formatting and menu display of sex climax options.
        climax_type_dict = {
            "masturbation":0.5,
            "air":0.75, #ie a girl gets you off somehow, but you cum into open air/the floor/yourself
            "body":1.0, #Generic bodyshot. Stomach or ass, normally.
            "face":1.25, #Onto her face, but not explicitly her mouth
            "tits":1.25, #You already know what these are.
            "mouth":1.5, #Cum into her mouth explicitly. Bonus for her swallowing?
            "pussy":2.0, #Creampie. Knocked down to 1.5x if you're wearing a condom.
            "anal":2.0, #Butt-pie? Does this have some sexy name I don't know about?
            "throat":2.0 #Throatpie. Down the hatch!
            }

        def __init__(self, *args): #Each argument provided should be a list of "display_name" and the climax type that should be associated with that climax
            self.selected_climax_type = None #Set when the player selects a return value, let's us call run_climax() at the correct moment later.
            self.climax_options = args

        def get_climax_multiplier(self, type, with_novelty = False):
            multiplier = ClimaxController.climax_type_dict[type]
            if type == "pussy" and mc.condom:
                multiplier += -0.5

            return multiplier

        def show_climax_menu(self): #NOTE: We show the menu even when we don't intend to give more than one option. More player interaction + more information display.
            display_list = []
            for climax_option in self.climax_options:
                display_name = climax_option[0]
                climax_type = climax_option[1]
                display_name += "{size=20}{color=#29B6F6}\n"
                display_name += "x{multiplier:.2f} Clarity Produced".format(multiplier = self.get_climax_multiplier(climax_type))
                display_name += "{/color}{/size}"
                display_name += " (tooltip)All Locked Clarity is released when you climax. How much Clarity is produced varies depending on how you cum, and it's possible to have a multiplier greater than 1!"
                display_list.append([display_name,climax_option])

            self.selected_climax_type = renpy.display_menu(display_list, screen = "choice")
            return self.selected_climax_type[0]

        def do_clarity_release(self, the_person = None):
            if the_person:
                multiplier = self.get_climax_multiplier(self.selected_climax_type[1])
                mc.convert_locked_clarity(multiplier, with_novelty = the_person.novelty)
                the_person.change_novelty(-2)
            else:
                multiplier = self.get_climax_multiplier(self.selected_climax_type[1])
                mc.convert_locked_clarity(multiplier, with_novelty = mc.masturbation_novelty)
                mc.masturbation_novelty += -2
                if mc.masturbation_novelty < 50:
                    mc.masturbation_novelty = 50
