init 1 python:
    integration_test_labels.append("draw_person_integration_test")
    integration_test_labels.append("draw_group_integration_test")

label draw_person_integration_test():
    "Drawing integration test."
    $ test_person = create_random_person()
    $ other_person = create_random_person()

    "Drawing person one."
    $ test_person.draw_person()

    "Drawing person two."
    $ other_person.draw_person()

    "Drawing with specific positions."
    $ test_person.draw_person(position = "stand3")
    "..."
    $ test_person.draw_person(position = "kneeling1")
    "..."
    $ other_person.draw_person(position = "walking_away")
    "..."
    $ other_person.draw_person(position = "standing_doggy")

    "Drawing with specific emotions"
    $ test_person.draw_person(emotion = "happy")
    "..."
    $ test_person.draw_person(emotion = "sad")
    "..."
    $ test_person.draw_person(emotion = "angry")

    "Drawing with special modifiers"
    $ other_person.draw_person(position = "kissing")
    "..."
    $ other_person.draw_person(position = "kissing", special_modifier = "kissing")
    "..."
    $ test_person.draw_person(position = "blowjob")
    "..."
    $ test_person.draw_person(position = "blowjob", special_modifier = "blowjob")


    "Drawing animated clothing removal"
    $ strip_item = test_person.outfit.remove_random_any(top_layer_first = True, exclude_feet = True, do_not_remove = True)
    $ test_person.draw_animated_removal(strip_item)

    "Drawing animated clothing removal with position"
    $ strip_item = test_person.outfit.remove_random_any(top_layer_first = True, exclude_feet = True, do_not_remove = True)
    $ test_person.draw_animated_removal(strip_item, position = "back_peek")

    menu:
        "Tests successful.":
            return True

        "Tests failed.":
            return False

label draw_group_integration_test():
    $ test_person = create_random_person()
    $ other_person = create_random_person()
    $ third_person = create_random_person()

    $ the_group = GroupDisplayManager()
    $ the_group.add_person(test_person)
    $ the_group.draw_group()
    "Drawing group with one person."

    $ the_group.add_person(other_person)
    $ the_group.draw_group()
    "Drawing group with two people."

    $ the_group.add_person(third_person)
    $ the_group.draw_group()
    "Drawing group with three people."

    $ the_group.draw_group(position = "walking_away")
    "Drawing group in position."

    $ the_group.draw_group(emotion = "orgasm")
    "Drawing group with emotion."

    $ the_group.draw_group()
    $ the_group.draw_person(test_person, position = "doggy")
    "Drawing group with single person in position."

    $ the_group.draw_person(third_person, position = "walking_away", make_primary = False)
    "Drawing single person without changing primary."

    $ strip_item = test_person.outfit.remove_random_any(top_layer_first = True, exclude_feet = True, do_not_remove = True)
    $ the_group.draw_animated_removal(test_person, position = "stand2", the_clothing = strip_item)
    "Drawing single person animated clothing removal."

    $ the_group.remove_person(test_person)
    $ the_group.draw_group()
    "Drawing group after primary removal."

    menu:
        "Tests successful.":
            return True

        "Tests failed.":
            return False
