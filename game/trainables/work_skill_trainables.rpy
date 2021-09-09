init -2 python:
    def train_work_requirement(the_person):
        if the_person.has_role(employee_role):
            return True
        else:
            return False

label train_hr_label(the_person):
    mc.name "Let's talk about your HR work."
    "[the_person.possessive_title] nods passively and listens to you."
    mc.name "I think you could make some improvements. Our employees are, after all, our most valuable resource..."
    $ the_person.change_hr_skill(1)
    "You take advantage of [the_person.title]'s malleable and impress upon her the need to improve her skill."
    return

label train_market_label(the_person):
    mc.name "Let's talk about your marketing skills."
    "[the_person.possessive_title] nods passively and listens to you."
    mc.name "I think you could make some improvements. We can't succeed without the best and brightest out there selling our product..."
    $ the_person.change_market_skill(1)
    "You take advantage of [the_person.title]'s malleable and impress upon her the need to improve her skill."
    return

label train_research_label(the_person):
    mc.name "Let's talk about your research work."
    "[the_person.possessive_title] nods passively and listens to you."
    mc.name "I think you could make some improvements. In this business we need to be at the cutting edge of R&D..."
    $ the_person.change_research_skill(1)
    "You take advantage of [the_person.title]'s malleable and impress upon her the need to improve her skill."
    return

label train_production_label(the_person):
    mc.name "Let's talk about your work on the production room floor."
    "[the_person.possessive_title] nods passively and listens to you."
    mc.name "I think you could make some improvements. Let's go over the fundamentals..."
    $ the_person.change_production_skill(1)
    "You take advantage of [the_person.title]'s malleable and impress upon her the need to improve her skill."
    return

label train_supply_label(the_person):
    mc.name "Let's talk about your work securing supplies for our work."
    "[the_person.possessive_title] nods passively and listens to you."
    mc.name "I think you could make some improvements. Without supply our company couldn't do anything at all..."
    $ the_person.change_supply_skill(1)
    "You take advantage of [the_person.title]'s malleable and impress upon her the need to improve her skill."
    return
