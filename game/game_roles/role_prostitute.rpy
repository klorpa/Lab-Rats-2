init -1 python:
    def prostitute_requirement(the_person):
        if not mc.business.has_funds(200):
            "Not enough cash"
        elif the_person.sexed_count >= 1:
            "She's worn out. Maybe later."
        else:
            return True

label prostitute_label(the_person):
    mc.name "[the_person.title], I'm looking for a friend to spend some time with. Are you available?"
    the_person "If you're paying I am."
    $ mc.business.change_funds(-200)
    $ the_person.change_obedience(1)

    $ the_person.add_situational_obedience("prostitute", 40, "I'm being paid for this, I should do whatever he wants me to do.")
    call fuck_person(the_person, private = True, ignore_taboo = True) from _call_fuck_person_23 #She's a prostitute, she doesn't care about normal taboos
    $ the_report = _return

    $ the_person.clear_situational_obedience("prostitute")
    if the_report.get("girl orgasms", 0) > 0:
        "It takes [the_person.title] a few moments to catch her breath."
        the_person "Maybe I should be paying you... Whew!"
    $ the_person.review_outfit()

    the_person "That was fun, I hope you had a good time [the_person.mc_title]."
    "She gives you a quick peck on the cheek."
    $ clear_scene()
    return
