init 0 python:
    close_strip_dancing = StripteasePosition(name = "Close Strip Dancing",
        slut_requirement = 20,
        is_close = True,
        allows_touching = True, allows_jerking = True, allows_turning = True,
        position_towards_pose = "stand4", position_away_pose = "walking_away",
        girl_energy_cost = 12, guy_arousal_gain = 17,
        intro_label = "strip_close_dancing_intro",
        transition_label = "strip_close_dancing_transition",
        turn_towards_label = "strip_close_dancing_turn_towards",
        turn_away_label = "strip_close_dancing_turn_away",
        towards_labels = ["strip_close_dancing_towards_1", "strip_close_dancing_towards_2"],
        away_labels = ["strip_close_dancing_away_1"],
        climax_label = "strip_close_dancing_climax")

    list_of_strip_positions.append(close_strip_dancing)

init 1 python:
    strip_dancing.leads_to.append([close_strip_dancing, "Call her closer."])

#TODO: Similar to the dancing ones, but emphasise the fact that she's right in front of you "tits in your face. Wags her ass in your face, ect".
#TODO: Then if you're touching her you get options to spank her, squeeze her tits, caress her face, ect.

label strip_close_dancing_intro(the_person, guy_state, for_pay = False):
    "[the_person.possessive_title] stands right in front of you, her body nearly on top of yours."
    "She places her hands on her hips and sways them sensually back and forth sensually, keeping time to imagined music."
    if guy_state == "touching":
        "You reach out and place your hands on her thighs, feeling the shape of the body as she moves."
    elif guy_state == "jerking":
        "You stroke yourself and enjoy the way her body looks in motion."
    return

label strip_close_dancing_transition(the_person, guy_state, for_pay = False):
    "[the_person.possessive_title] dances her way closer to you, stopping within arms reach."
    if guy_state == "touching":
        pass
    elif guy_state == "jerking":
        pass
    return

label strip_close_dancing_turn_towards(the_person, guy_state, for_pay = False):
    "[the_person.title] turns to face you, keeping herself close to you."
    if guy_state == "touching":
        if the_person.outfit.tits_available():
            if the_person.has_large_tits():
                "You reach up her torso and fondle her tits as she presents them. Their soft, warm weight feels satisfying in your hands."
            else:
                "You reach up her torso and fondle her chest as she presents it to you."
        else:
            $ the_item = the_person.outfit.get_upper_top_layer()
            "You reach up her torso and grope at her tits underneath her [the_item.display_name]."
    elif guy_state == "jerking":
        if the_person.outfit.tits_visible():
            if the_person.has_large_tits():
                "You gaze at her tits as they bounce and jiggle with the motion, jerking off at the same time."
            else:
                "You gaze at her cute little tits as she presents them for you to look at, jerking off at the same time."
        else:
            "You jerk off at the same time, enjoying all the way she moves for you."
    return

label strip_close_dancing_turn_away(the_person, guy_state, for_pay = False):
    "[the_person.title] spins herself around and lifts her arms into the air."
    if the_person.outfit.vagina_visible():
        "She wiggles her hips, jiggling her ass for you to watch."
    else:
        $ the_item = the_person.outfit.get_lower_top_layer()
        "She shakes her hips, showing off the shape of her butt under her [the_item.display_name]."

    if guy_state == "touching":
        if the_person.outfit.vagina_available():
            "You feel the shapely curves of her ass and hips, caressing her as she dances."
        else:
            $ the_item = the_person.outfit.get_lower_top_layer()
            "You feel the shapely curves of her ass and hips underneath her [the_item.display_name]."

    elif guy_state == "jerking":
        pass #No special dialogue
    return

label strip_close_dancing_towards_1(the_person, guy_state, for_pay = False):
    if the_person.has_large_tits():
        "[the_person.title] shifts her hips and holds her hands behind her head, letting her large tits bounce and jiggle for you."
    else:
        "[the_person.title] moves her body side to side for you while you watch."

    if guy_state == "touching":
        if the_person.outfit.tits_available():
            if the_person.has_large_tits():
                "You grab her tits and juggle them in your hands."
            else:
                "You grab her chest and fondle her tits."
        else:
            $ the_item = the_person.outfit.get_upper_top_layer()
            "You feel up her chest, grabbing at her tits through her [the_item.display_name]."
    elif guy_state == "jerking":
        "You stroke your hard shaft. She's close enough that the tip of your cock is nearly brushing against her."
    return

label strip_close_dancing_towards_2(the_person, guy_state, for_pay = False):
    if the_person.has_large_tits():
        "[the_person.possessive_title] cups her tits and squeezes them together as she dances."
    else:
        "[the_person.possessive_title] dances for your enjoyment, swaying her body to imagined music."

    if guy_state == "touching":
        "You feel up her hips and her chest as she moves in front of you."
    elif guy_state == "jerking":
        "You jerk off while you watch her move."
    return

label strip_close_dancing_away_1(the_person, guy_state, for_pay = False):
    "[the_person.title] holds her arms in front of you and bends forward, giving you a close look at her ass."
    if the_person.outfit.vagina_visible():
        "She shakes her hips and jiggles that butt for your enjoyment.."
    else:
        $ the_item = the_person.outfit.get_lower_top_layer()
        "She shakes her hips and jiggles her ass. You wonder what it would look like without her [the_item.display_name] in the way."

    if guy_state == "touching":
        "You feel up the curves of her thighs, her ass, and her hips."
        "Her body is warm under your hands, and you want to feel even more of it."

    elif guy_state == "jerking":
        "You stroke your shaft faster, unconciously keeping time with the rhythm of [the_person.title]'s hips."
        "She's so close that, with just a little movement, you can tap the end of your cock onto her body."

    return

label strip_close_dancing_climax(the_person, guy_state, for_pay = False):
    "[the_person.possessive_title] is breathing heavily. She presses herself against your body suddenly."
    the_person "Oh my... Ah...!"
    if guy_state == "touching":
        "She squeals and locks her knees together, climaxing from your gentle caresses."
    elif guy_state == "jerking":
        "She squeals and locks her knees together, climaxing while you jerk off next to her."
    else:
        "She squeals and locks her knees together, climaxing just from you watching her."
    $ the_person.run_orgasm(trance_chance_modifier = the_person.get_opinion_score("public sex") + the_person.get_opinion_score("masturbating"), reset_arousal = False)
    "You feel a shiver run through her body. You hold onto her, in case she's about to collapse completely."
    "After a long moment her shoulders slump. She takes long, deep breaths to try and regain control of herself."
    "When she has caught her breath she gives you a weak smile and stands back up under her own strength."
    return
