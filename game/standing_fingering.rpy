init:
    python:
        standing_finger = Position("Fingering",25,50, "walking_away" ,"Stand","None","Foreplay",15,4,[],
        "intro_standing_finger",
        ["scene_standing_finger_1","scene_standing_finger_2"],
        "outro_standing_finger",
        "transition_default_standing_finger",
        "strip_standing_finger", "strip_ask_standing_finger",
        "orgasm_standing_finger",
        verb = "finger",
        opinion_tags = ["being fingered"])
        #list_of_positions.append(standing_finger) #Only reachable by massaging her first.

init 1:
    python:
        standing_finger.link_positions(standing_grope,"transition_standing_fingering_standing_grope")

label intro_standing_finger(the_girl, the_location, the_object, the_round):
    "You stand behind [the_girl.title] and put yoru arms around her, pulling her close against you."
    if the_girl.outfit.vagina_available():
        "You don't waste any time pushing your hand between her legs, teasing her cute, exposed pussy with your fingers."
        "She moans quietly as you slide two fingers inside of her wet hole."
    else:
        $ the_item = the_girl.outfit.get_lower_top_layer()
        if the_item:
            "You don't waste any time pushing your hand between her legs, sliding it under her [the_item.name] to reach her pussy."
            "You run a finger over it, teasing it first."
            "She moans quietly as you slide two fingers into her wet hole."
        else:
            "She moans quietly as you slide two fingers inside of her wet hole."
    return

label scene_standing_finger_1(the_girl, the_location, the_object, the_round):
    if the_girl.has_large_tits():
        if the_girl.outfit.tits_available():
            "You reach your free hand up to [the_girl.title]'s bare tits and cup one, massaging it while you finger her."

        else:
            "You reach your free hand up to [the_girl.title]'s tits and squeeze one through her clothing, enjoying its size and weight."
    else:
        if the_girl.outfit.tits_available():
            "You paw at [the_girl.possessive_title]'s small tits with your free hand, running your thumb over one of her nipples as you continue to finger her."
            "Her body responds, the nipple hardening as you play with it."
        else:
            "You paw at [the_girl.possessive_title]'s small tits through her clothing with your free hand."
            "You can feel her body respond, her nipple hardening enough that you can feel it through the fabric."
    return


label scene_standing_finger_2(the_girl, the_location, the_object, the_round):
    "You slide your fingers in and out of her pussy, stroking the inside of that soft tunnel."
    "Each movement draws moans of pleasure from [the_girl.possessive_title], who presses herself against you."
    if the_girl.arousal > 50:
        if the_girl.outfit.vagina_available():
            "Her pussy is dripping wet now, dripping juices down her thighs."
        else:
            $ the_item = the_girl.outfit.get_lower_top_layer()
            if the_item:
                "Her pussy is dripping wet now, her juices leaving a faint wet spot on her [the_item.name]."
    else:
        if the_girl.outfit.vagina_available():
            "She places one of her own hands over yours, encouraging you to speed up."
            the_girl.char "Just like that... Ah..."
        else:
            $ the_item = the_girl.outfit.get_lower_top_layer()
            if the_item:
                "You look over her shoulder and watch as your fingers move under her [the_item.name], timed to her soft moans of pleasure."
    return

label outro_standing_finger(the_girl, the_location, the_object, the_round):
    if the_girl.arousal >= 100:
        "Feeling [the_girl.title] cum around your fingers pushes you over the edge. You feel your cock spasm in your underwear as a wave of pleasure washes over you."
        "It takes both of you a moment to recover from your orgasms."
    else:
        "Feeling [the_girl.title]'s hot, tight pussy squeezing your fingers is enough to push you that little bit further, past the point of no return."
        "You grasp her tightly with your free hand as you cum, shoving your fingers deep into her cunt and making her gasp in suprise."
        "When you've recovered you recover you slide them out."
        the_girl.char "Did you just... Cum?"
        mc.name "Yeah."
        "She grinds her butt back into your crotch."
        the_girl.char "Aww, I thought I was going to get there first. Oh well."
    return


label transition_standing_fingering_standing_grope(the_girl, the_location, the_object, the_round):
    "You give her a few wet pussy a few more strokes, then pull your fingers out and drag them along her stomach."
    if the_girl.sluttiness >= 60:
        "She moans and takes hold of your hand, bringing it up to her mouth. She slides your fingers, fresh from her cunt, into her mouth."
        "Her tongue wraps around them as she sucks gently on your fingers. She works her hips, grinding your erection against her ass."
    else:
        "She moans and works her hips back against you, grinding your ereciton against her ass."
    return

label transition_default_standing_finger(the_girl, the_location, the_object, the_round):
    "You gather [the_girl.title] up in your arms, cradling her from behind. You reach a hand between her legs, sliding it down to her pussy."
    "You don't waste any time sliding two fingers into her warm, wet pussy."
    return

label strip_standing_finger(the_girl, the_clothing, the_location, the_object, the_round):
    the_girl.char "Your hands feel amazing... Oh my god..."
    $ the_girl.draw_animated_removal(the_clothing, position = standing_finger.position_tag)
    "She strips off her [the_clothing.name] while you're fingering her, moaning the whole time."
    return

label strip_ask_standing_finger(the_girl, the_clothing, the_location, the_object, the_round):
    the_girl.char "Everything feels so tight, I want to take it all off... Do you mind?"
    "[the_girl.possessive_title] grabs onto her [the_clothing.name], waiting for you to tell her what to do."
    menu:
        "Let her strip.":
            mc.name "Take it off. Strip for me."
            $ the_girl.draw_animated_removal(the_clothing, position = standing_finger.position_tag)
            "[the_girl.possessive_title] takes off her [the_clothing.name] and drops it to the side while you pump your fingers in and out of her cunt."

        "Leave it on.":
            mc.name "No, I like how you look with it on."
            if the_girl.sluttiness < 80:
                the_girl.char "Do you think I look sexy in it?"
            else:
                the_girl.char "Don't you think I would look better wearing your cum? That would be so fitting for your dirty little slut, wouldn't it?"
    $ standing_finger.redraw_scene(the_girl)
    return

label orgasm_standing_finger(the_girl, the_location, the_object, the_round):
    the_girl.char "Oh god... Right there! Right there! Ahhhhh!"
    "Her whole body tenses up and she leans back into you. A shiver runs through her body as she climaxes."
    $ the_girl.call_dialogue("climax_responses_foreplay")
    "She quivers with pleasure for a few seconds before her whole body relaxes."
    the_girl.char "Ah... Keep going..."
    return
