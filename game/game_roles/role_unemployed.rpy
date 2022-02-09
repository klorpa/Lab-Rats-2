init -2 python:
    pass

label unemployed_offer_hire(the_person):
    mc.name "Hey [the_person.title], are you interested in a job?"
    the_person "Right now? Yeah, I am! I, uh... Don't suppose you're hiring, are you?"
    menu:
        "Offer her full pay.":
            mc.name "I am. Let's see if we have a position you might fit..."
            call unemployed_offer_accept(the_person)

        "Offer her half pay.":
            mc.name "I am. The position is more of an internship, so the pay isn't great..."
            the_person "Something is better than nothing! I'm sure I'll be first in line for a promotion, right?"
            mc.name "Sure, yeah... Let's see if we have a position that you might fit into..."
            $ the_person.salary_modifier = 0.5
            call unemployed_offer_accept(the_person)
    return

label unimportant_job_offer_hire(the_person):
    mc.name "Hey [the_person.title], are you interested in a change of scenery?"
    mc.name "My company is hiring, and I think you might be a fanstic fit."
    "She thinks about it for a moment."
    the_person "Well... Sure, I'll consider it!"
    call stranger_hire_result(the_person)
    if _return:
        mc.name "Well then we have a deal. Glad to have you aboard [the_person.title]!"
        the_person "Thank you [the_person.mc_title]! I'll have to let my boss know, I guess."
    else:
        mc.name "I don't think we have any roles that fit your skill set at the moment unfortunately."
        "She seems a little disappointed, but gets over it quickly."
        the_person "Oh, alright then."
    return

label unemployed_offer_accept(the_person):
    call stranger_hire_result(the_person)
    if _return:
        mc.name "Well then we have a deal. Glad to have you aboard [the_person.title]!"
        the_person "Thank you so much [the_person.mc_title], I won't let you down!"
    else:
        mc.name "I don't think we have any roles that fit your skill set at the moment unfortunately."
        "[the_person.possessive_title] frowns."
        the_person "I understand. Thank you for thinking about it anyways."
    return
