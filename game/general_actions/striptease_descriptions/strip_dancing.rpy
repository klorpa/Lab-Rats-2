init 0 python:
    strip_dancing = StripteasePosition(name = "Strip_Dancing",
        slut_requirement = 10,
        position_towards_pose = "stand3", position_away_pose = "back_peek",
        girl_energy_cost = 12, guy_arousal_gain = 15,
        intro_label = "strip_dancing_intro",
        transition_label = "strip_dancing_transition",
        turn_towards_label = "strip_awkward_stand_turn_towards",
        turn_away_label = "strip_dancing_turn_away",
        towards_labels = ["strip_dancing_towards_1", "strip_dancing_towards_2"],
        away_labels = ["strip_dancing_away_1"],
        climax_label = "strip_dancing_climax")

    list_of_strip_positions.append(strip_dancing)

init 1 python:
    strip_awkward_stand.leads_to.append([strip_dancing, "Tell her to dance."])

label strip_dancing_intro(the_person, guy_state, for_pay = False):
    "[the_person.possessive_title] takes up a position a few feet in front of you."
    "She sets her feet a shoulders width apart and starts to move, shifting her shoulders and hips to imagined music."
    return

label strip_dancing_transition(the_person, guy_state, for_pay = False):
    "[the_person.possessive_title] starts to get a little more comfortable."
    "After warming up for a little bit she starts to move her body."
    "She sways her hips and shoulders from side to side in time with imagined music, giving you a more dynamic view of her body."
    return

label strip_dancing_turn_towards(the_person, guy_state, for_pay = False):
    $ the_person.draw_person()
    "She gives her ass a few more shakes, then turns back to you and runs her hand down her hips."
    return

label strip_dancing_turn_away(the_person, guy_state, for_pay = False):
    "She swings her hips a few times, then lets the movement carry her in a half-circle."
    $ the_person.draw_person(position = "back_peek")
    "She looks at you over her shoulder, giving you a wink and a smile."
    return

label strip_dancing_towards_1(the_person, guy_state, for_pay = False):
    if the_person.has_large_tits():
        "[the_person.title] moves her body side to side for you, letting her large tits bounce and jiggle while you watch."
    else:
        "[the_person.title] moves her body side to side for you while you watch."

    if guy_state == "jerking":
        "You stroke your cock slowly as she dances in front of you."
    return

label strip_dancing_towards_2(the_person, guy_state, for_pay = False):
    if the_person.has_large_tits():
        if the_person.outfit.tits_visible():
            "She cups her big tits in her hands and jiggles them playfully."
        else:
            $ the_item = the_person.outfit.get_upper_top_layer()
            "She rolls her shoulders, emphasising her big tits hidden underneath her [the_item.display_name]."
    else:
        if the_person.outfit.tits_visible():
            "She plants her hands on her tits and rubs them playfully."
        else:
            "She runs her hands over her chest, emphasisng her breasts."

    if guy_state == "jerking":
        "Your cock responds, twitching with excitement in your hand. You keep stroking yourself and enjoy the show."
    return

label strip_dancing_away_1(the_person, guy_state, for_pay = False):
    "[the_person.title] lifts her hands above her body, giving you a good look at her ass."
    if the_person.outfit.vagina_visible():
        "She shakes her hips and jiggles her ass for you."
    else:
        $ the_item = the_person.outfit.get_lower_top_layer()
        "She shakes her hips and jiggles her ass. You wonder what it would look like without her [the_item.display_name] in the way."

    if guy_state == "jerking":
        "You can't help but be turned on by the view. You stroke your shaft faster, unconciously keeping time with the rhythm of [the_person.title]'s hips."
    return

label strip_dancing_climax(the_person, guy_state, for_pay = False):
    "[the_person.possessive_title]'s dancing speeds up and takes on a frantic, almost jerky quality."
    the_person "Oh my... Ah...!"
    "She squeals and locks her knees together, climaxing just from you watching her."
    $ the_person.run_orgasm(trance_chance_modifier = the_person.get_opinion_score("public sex") + the_person.get_opinion_score("masturbating"), reset_arousal = False)
    "Her thighs quiver with effort for a few seconds, then relax as the orgasm passes."
    "Her shoulders slump and she takes long, deep breaths to try and regain control of herself."
    "When she has caught her breath she gives you a weak smile and wiggles her hips, starting to dance for you again."
    return
