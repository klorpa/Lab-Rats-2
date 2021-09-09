init -2 python:
    class SerumTraitBlueprint(SerumTrait): #A Serum Trait Blueprint is a trait that describes a general class of similar actions - like changing hair colour.
        # Unlike a normal trait, when it is "unlocked" it instead brings up a UI to design a new trait, which is added to a business specific list and set as the research instead.
        def __init__(self, unlock_label = None, *args, **kwargs):
            super(SerumTraitBlueprint, self).__init__(*args, **kwargs)
            self.unlock_label = unlock_label #Unlock label should take a copy trait (ie. a proper SerumTrait) and fill any needed traits for effects_dict.

            #Record the actual traits so we can have an acualised design.
            self.given_args = args
            self.given_kwargs = kwargs

        def unlock_trait(self, pay_clarity = True):
            if pay_clarity:
                mc.spend_clarity(self.clarity_cost)

            copy_trait = SerumTrait(*self.given_args, **self.given_kwargs) #TODO We want some way to back out of this creation process.
            mc.business.blueprinted_traits.append(copy_trait)
            copy_trait.unlock_trait(pay_clarity = False)
            if self.unlock_label: #If the unlock_trait removes itself from the blueprinted_traits list we don't name it - it was canceled because some input was invalid.
                renpy.call_in_new_context("name_blueprint_trait", copy_trait, self.unlock_label) #NOTE: This calls in a new context, so it should properly return.

            return copy_trait
