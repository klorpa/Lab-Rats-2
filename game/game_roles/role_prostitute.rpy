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

label prostitute_hire_offer(the_person):
    mc.name "Have you ever thought about a different career?"
    mc.name "My company could really use talented people like you."
    "She laughs and shakes her head."
    the_person "I don't think you really mean that."
    mc.name "I do, and you wouldn't have to be walking the streets just to make ends meet."
    if the_person.get_opinion_score(["vaginal sex", "anal sex", "public sex", "giving blowjobs", "skimpy outfits"]) > 1 and the_person.effective_sluttiness >= 40:
        # She enjoys fucking people too much to quit.
        the_person "That's sweet of you to say, but I don't just do it for the money."
        the_person "Truth is, I kind of like it. I get paid to get fucked, what's not to like?"
        "She shakes her head in a final refusal."
        the_person "So thanks, but no thanks."

    else:
        the_person "Really? Well... Okay, tell me about it."
        call stranger_hire_result(the_person)
        if _return:
            mc.name "Then it's settled. I'll see you at work."
            the_person "I suppose I'm going to need a more professional wardrobe now."
            mc.name "That might surprise you, actually..."
        else:
            mc.name "I'm really sorry [the_person.title], but I just don't think we have any positions available that suit your skills right now."
            the_person "I knew it was too good to be true."
            mc.name "Hey, chin up. If we have an opening to fill you'll be my first thought."
    return
