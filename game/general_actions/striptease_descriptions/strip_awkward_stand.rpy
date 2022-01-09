init 0 python:
    strip_awkward_stand = StripteasePosition(name = "Awkward_stand",
        girl_energy_cost = 8, guy_arousal_gain = 8,
        intro_label = "strip_awkward_stand_intro",
        transition_label = "strip_awkward_transition",
        turn_towards_label = "strip_awkward_stand_turn_towards",
        turn_away_label = "strip_awkward_stand_turn_away",
        towards_labels = ["strip_awkward_stand_towards_1", "strip_awkward_stand_towards_2"],
        away_labels = ["strip_awkward_stand_away_1"],
        climax_label = "strip_awkward_stand_climax")

    list_of_strip_positions.append(strip_awkward_stand)


label strip_awkward_stand_intro(the_person, guy_state, for_pay = False):
    "[the_person.possessive_title] stands in front of you, doing her best to avoid making eye contact."
    "She's obviously unsure about what to do."
    mc.name "Don't just stand there. Move a little."
    if the_person.has_large_tits():
        "[the_person.title] shifts her weight from side to side while you watch her. The small movements still make her big tits jiggle around."
    else:
        "[the_person.title] shifts her weight from side to side while you watch her."
    return

label strip_awkward_transition(the_person, guy_state, for_pay = False):
    "[the_person.title] stands a few feet in front of you. She seems uncomfortable with all of the attention and doesn't know what to do."
    if guy_state == "jerking":
        "That doesn't dissuade you, and you keep rubbing your cock in front of her."
    return

label strip_awkward_stand_turn_away(the_person, guy_state, for_pay = False):
    $ the_person.draw_person(position = "back_peek")
    "She turns around and peeks at you over her shoulder, unsure what to do now."
    return

label strip_awkward_stand_turn_towards(the_person, guy_state, for_pay = False):
    $ the_person.draw_person()
    "She turns back to face you, still unsure what to do."
    return

label strip_awkward_stand_towards_1(the_person, guy_state, for_pay = False):
    "You get a good look at [the_person.title] while she stands in front of you, even if she's not sure what to do with herself."
    "She gazes around the room, looking for something to do other than make eye contact."
    if guy_state == "jerking":
        "You jerk yourself off while staring at [the_person.title]."
        "She blushes and covers her eyes with a hand."
        the_person "Oh my god..."
    return

label strip_awkward_stand_towards_2(the_person, guy_state, for_pay = False):
    if the_person.outfit.tits_visible():
        "[the_person.possessive_title] wiggles her shoulders half-heartedly."
        if the_person.has_large_tits():
            "Luckily, her big tits make up for her lack of enthusiasm, jiggling around with every movement."
    else:
        "[the_person.possessive_title] wiggles her shoulders half-heartedly."
        $ the_item = the_person.outfit.get_upper_top_layer()
        if the_person.has_large_tits():
            "Unfortunately, her [the_item.display_name] is able to keep her tits from doing much jiggling."
        else:
            "Unfortuantely there isn't much for her to shake. Any interesting movement is hidden underneath her [the_item.display_name]."

    if guy_state == "jerking":
        if the_person.outfit.tits_visible():
            "You ogle her bare tits and jerk yourself off, imagining what else you could do with them..."
        else:
            "You keep jerking yourself off, imagining what her bare tits would look like."
    return

label strip_awkward_stand_away_1(the_person, guy_state, for_pay = False):
    "[the_person.title] takes a breath and gathers her courage."
    the_person "Do you... like my butt?"
    "She bends forward a tiny bit, a tame attempt to emphasise her curves."
    if the_person.outfit.vagina_visible():
        "She runs a hand over her bare ass while you check her out."
    else:
        $ the_item = the_person.outfit.get_lower_top_layer()
        "She runs a hand over her [the_item.display_name], then gives herself the worlds lightest spank."
    mc.name "Looking good [the_person.title]."

    if guy_state == "jerking":
        "You enjoy the view and stroke your cock some more."
        "[the_person.possessive_title] stares at your cock for a moment, then pulls her eyes away."
    return

label strip_awkward_stand_climax(the_person, guy_state, for_pay = False): #TODO: Link this with some personality dialogue
    "[the_person.possessive_title] looks away from you, panting loudly."
    the_person "Don't... don't look at me! I'm going to... Ah!"
    "She squeals and locks her knees together as she climaxes."
    $ the_person.run_orgasm(trance_chance_modifier = the_person.get_opinion_score("public sex") + the_person.get_opinion_score("masturbating"), reset_arousal = False)
    "Her thighs quiver with effort for a few seconds, then relax as the orgasm passes."
    "Her shoulders slump and she takes long, deep breaths to try and regain control of herself."
    return

label strip_awkward_stand_outro(the_person, guy_state, for_pay = False): #TODO: Decide if we want to let you resist/force cumming
    #TODO: Maybe we only want to let you cum if you're jerking off for simplicities sake.
    if guy_state == "watching" or guy_state == "touching":
        "Just watching [the_person.title] pose for your enjoyment is enough to push you that little bit further."
        $ climax_controller = ClimaxController(["Cum your pants.","air"])
        $ the_choice = climax_controller.show_climax_menu()
        "You grunt and shut your eyes as your cock pumps it's load into your underwear."
        $ climax_controller.do_clarity_release(the_person)
        the_person "[the_person.mc_title]? What's wrong?"
        mc.name "Nothing. Nothing at all."

    elif guy_state = "jerking":
        "Her performance may not be very inspired, but jerking off while [the_person.possessive_title] poses is still plenty of stimulation."
        "You feel your climax crest the point of no return and you speed up, stroking yourself faster still."
        the_person "Oh my god, are you about to..."
        $ climax_controller = ClimaxController(["Cum on the floor", "air"])
        $ the_choice = climax_controller.show_climax_menu()
        "You grunt and fire your load off, pulsing it out in an arc as she watches."
        $ climax_controller.do_clarity_release(the_person)
        the_person "...Cum..."
    return
#
# label strip_awkward_stand_strip(the_person, the_clothing, guy_state, for_pay = False): #TODO: Maybe this should be generalised
#     #TODO: She takes off the piece of clothing handed over.
#     $ test_outfit = the_person.outfit.get_copy()
#     $ test_outfit.remove_clothing(the_clothing)
#
#     $ taboo_break = False
#     if test_outfit.vagina_visible() and the_person.has_taboo("bare_pussy"):
#         $ taboo_break = "bare_pussy"
#     elif test_outfit.tits_visible() and the_person.has_taboo("bare_tits"):
#         $ taboo_break = "bare_tits"
#     elif test_outfit.underwear_visible() and the_person.has_taboo("underwear_nudity"):
#         $ taboo_break = "underwear_nudity"
#
#     if taboo_break:
#         $ the_person.call_dialogue(taboo_break + "_taboo_break", the_clothing = the_clothing)
#         $ the_person.break_taboo(taboo_break)
#
#     $ generalised_strip_description(the_person, the_clothing)

    # if for_pay:
    #     "You hold up some cash, reminding [the_person.title] what she's working for."
    #
    #     #TODO: Remind hr that that you're paying while she strips
    #
    # else:
    #     #TODO: She'll do it for free because she thinks it's fun.
    # return
