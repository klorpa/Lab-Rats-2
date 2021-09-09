init -2 python:
    def train_learn_opinion_requirement(the_person):
        if the_person.has_unknown_opinions():
            return True
        else:
            return "Unknown Opinions"

    def train_strengthen_opinion_requirement(the_person):
        if the_person.get_opinion_topics_list(include_unknown = False, include_hate = False, include_love = False):
            return True
        else:
            return "Known Moderate Opinion"

    def train_weaken_opinion_requirement(the_person):
        if the_person.get_opinion_topics_list(include_unknown = False):
            return True
        else:
            return "Known Opinion"



label train_learn_opinion_label(the_person):
    mc.name "Let's talk about you, what do you have strong feelings about?"
    the_person "Me? Oh, I don't know..."
    menu:
        "Tell me a normal opinion." if the_person.has_unknown_opinions(sexy_opinions = False):
            mc.name "Really, tell me anything at all."
            $ sexy_opinion = False

        "Tell me a sexy opinion." if the_person.has_unknown_opinions(normal_opinions = False):
            mc.name "Really, I promise I won't tell anyone else. You must have something interesting to share."
            $ sexy_opinion = True

    "You keep prompting [the_person.possessive_title] to share more information."

    if sexy_opinion:
        $ revealed_opinion = the_person.get_random_opinion(include_known = False, include_normal = False)

    else:
        $ revealed_opinion = the_person.get_random_opinion(include_known = False)

    if revealed_opinion:
        $ the_person.discover_opinion(revealed_opinion)
        "She can't resist for long. You listen as she tells you her opinion about [revealed_opinion]."
        if sexy_opinion:
            the_person "I hope that wasn't too personal to share..."
            mc.name "No, that's exactly what I wanted to know about. Thank you [the_person.title]."
        else:
            the_person "I hope that's what you wanted to hear about..."
            mc.name "It was perfect, thank you [the_person.title]."
    else:
        "[the_person.title] seems happy to share her opinions with you after some prompting."
        "Unfortunately, she doesn't have anything to tell you that you don't already know."
        return False
    return

label train_strengthen_opinion_label(the_person): #TODO: Only have this enabled if she has a known moderate opinion
    mc.name "I want to talk to you about something."
    the_person "Okay, what do you want to talk about?"
    python:
        opinion_list = the_person.get_opinion_topics_list(include_unknown = False, include_hate = False, include_love = False)
        show_list = []
        for topic in opinion_list:
            if the_person.get_opinion_score(topic) < 0:
                show_list.append(("Dislikes " + topic, topic))
            else:
                show_list.append(("Likes " + topic, topic))

        show_list.append(["Never Mind","Never Mind"])

    $ player_choice = renpy.display_menu(show_list)
    if not player_choice == "Never Mind":
        mc.name "I think you have the right idea, but you could take it even further..."
        "[the_person.possessive_title] listens attentively as you talk to her."
        $ the_person.strengthen_opinion(player_choice)
        "After a while you feel confident you have strengthened her opinion."
    else:
        mc.name "On second thought, never mind."
        "She shrugs, completely unbothered."
        return False
    return

label train_weaken_opinion_label(the_person): #TODO; Only have this enabled if you know of an opinion
    mc.name "I want to talk to you about something."
    the_person "Okay, what do you want to talk about?"
    python:
        opinion_list = the_person.get_opinion_topics_list(include_unknown = False)
        show_list = []
        for topic in opinion_list:
            if the_person.get_opinion_score(topic) == -2:
                show_list.append(("Hates " + topic, topic))
            elif the_person.get_opinion_score(topic) == -1:
                show_list.append(("Dislikes " + topic, topic))
            elif the_person.get_opinion_score(topic) == -1:
                show_list.append(("Likes " + topic, topic))
            else:
                show_list.append(("Loves " + topic, topic))

        show_list.append(["Never Mind","Never Mind"])

    $ player_choice = renpy.display_menu(show_list)
    if not player_choice == "Never Mind":
        mc.name "You've got it all wrong, you need to think about this some more."
        mc.name "Here, let me explain it to you..."
        "[the_person.possessive_title] listens attentively while you mould her opinions of [player_choice]."
        $ the_person.weaken_opnion(player_choice)
        "When you're finished you feel confident that you have weakened her opinion."
    else:
        mc.name "On second thought, never mind."
        "She shrugs, completely unbothered."
        return False
    return

label train_new_opinion_label(the_person, sexy_list = False):
    mc.name "I want to talk to you about something."
    the_person "Okay, what do you want to talk about?"
    if sexy_list:
        $ opinion_train_options = sexy_opinions_list[:]
    else:
        $ opinion_train_options = opinions_list[:]
    python:
        for known_opinion in the_person.get_opinion_topics_list(include_unknown = False, include_sexy = False):
            if known_opinion in opinion_train_options:
                opinion_train_options.remove(known_opinion) #Remove opinions we already know about.


    $ display_list = []
    python:
        for opinion in opinion_train_options:
            display_list.append((opinion,opinion))
    $ display_list.append(("Never Mind","Never Mind"))
    $ player_choice = renpy.display_menu(display_list)
    if not player_choice == "Never Mind":
        mc.name "Let's talk about [player_choice]."
        if the_person.get_opinion_score(player_choice) == 0:
            "[the_person.possessive_title] nods and listens attentively as you explain to her what her opinion should be."
            menu:
                "Create a positive opinion of [player_choice].":
                    $ the_person.create_opinion(player_choice)


                "Create a negative opinion of [player_choice].":
                    $ the_person.create_opinion(player_choice, start_positive = False)
            "It takes some time, but after a long conversation you feel confident you've put a strong opinion in [the_person.title]'s mind."

        else:
            the_person "[player_choice]? Yeah, I have some thoughts about that..."
            $ the_person.discover_opinion(player_choice)
            "It quickly becomes clear that [the_person.possessive_title] already has an opinion about [player_choice]."
            "You'll need a different approach if you want to change an opinion she has already formed."
            return False


    else:
        mc.name "On second thought, never mind."
        "She shrugs, completely unbothered."
        return False
    return
