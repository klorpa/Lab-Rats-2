init:
    python:
        standing_grope = Position(name = "Groping", slut_requirement = 0, slut_cap = 30, requires_hard = False, requires_large_tits = False,
            position_tag = "walking_away" , requires_location = "Stand", requires_clothing = "None", skill_tag = "Foreplay",
            girl_arousal = 10, girl_energy = 5,
            guy_arousal = 5, guy_energy = 15,
            connections = [],
            intro = "intro_standing_grope",
            scenes = ["scene_standing_grope_1","scene_standing_grope_2","scene_standing_grope_3"],
            outro = "outro_standing_grope",
            transition_default = "transition_default_standing_grope",
            strip_description = "strip_standing_grope", strip_ask_description = "strip_ask_standing_grope",
            orgasm_description = "orgasm_standing_grope",
            taboo_break_description = "taboo_break_standing_grope",
            verb = "grope", verbing = "groping",
            opinion_tags = None,
            associated_taboo = "touching_body")

        list_of_positions.append(standing_grope)

init 1:
    python:
        standing_grope.link_positions(standing_finger,"transition_standing_grope_standing_fingering")

label intro_standing_grope(the_girl, the_location, the_object):

    "You stand behind [the_girl.title] and put your arms around her, pulling her close against you."
    "You reach one hand down, running across her stomach and towards her waist and the other up towards her tits."
    if the_girl.has_large_tits():
        "She sighs and leans into you cup one of her tits and heft it up, massaging it gently."
        "Your other hand slides between her legs, bruishing against her inner thighs and caressing her pussy."
    else:
        "She sighs and leans into you as your hand slides between her legs, brushing her thighs and petting her pussy."
    return

label taboo_break_standing_grope(the_girl, the_location, the_object):
    "You put your hands on [the_girl.title]'s arms, rubbing them gently."
    the_girl.char "Oh..."
    "Next, you slide your hands down her body, over the curves of her torso onto her hips."
    "You take a small step forward and slide your hands behind [the_girl.possessive_title] and onto her ass."
    $ the_girl.call_dialogue(standing_grope.associated_taboo+"_taboo_break")
    if the_girl.has_large_tits():
        "You step behind [the_girl.title], putting one arm across her torso and cupping one of her juicy tits."
    else:
        "You step behind [the_girl.title], putting one arm across her torso and cupping one of her tits."
    "Your other hand slides lower, over her hips again and down to her inner thigh. She sighs happily and leans against you."
    return

label scene_standing_grope_1(the_girl, the_location, the_object):
    if the_girl.has_large_tits():
        if the_girl.outfit.tits_available():
            "You squeeze and massage [the_girl.possessive_title]'s bare tits. They're soft, warm, and heavy in your hand."

        else:
            "You squeeze and massage [the_girl.possessive_title]'s tits. They're pleasantly soft and heavy underneath her clothing."
    else:
        if the_girl.outfit.tits_available():
            "You paw at [the_girl.possessive_title]'s small tits, cupping one in your hand and running a thumb over her nipple."
            "Her body responds, her nipple hardening as you play with it."
        else:
            "You paw at [the_girl.possessive_title]'s small tits over her clothing."
            "You can feel her body respond, her nipples hardening enough that you can feel them through the fabric."
    return


label scene_standing_grope_2(the_girl, the_location, the_object):
    if the_girl.outfit.vagina_available():
        "[the_girl.title] spreads her legs for you, giving you space between them to slide your hand down."
        "She moans softly when you run a finger over her warm, wet, slit."
        the_girl.char "Oh... Don't tease me like that..."
    else:
        $ the_item = the_girl.outfit.get_lower_top_layer()
        "[the_girl.title] spreads her legs for you, and you rub her crotch through her [the_item.name]."
        the_girl.char "Mmm..."
    return

label scene_standing_grope_3(the_girl, the_location, the_object):
    if the_girl.outfit.vagina_available():
        "[the_girl.title] presses her hips back against you, grinding her bare ass rubbing against your crotch."
        the_girl.char "Mmm, I can feel your erection. That's so fucking hot..."
    else:
        "[the_girl.title] presses her hips back against you, grinding her ass against your crotch."
    return

label outro_standing_grope(the_girl, the_location, the_object):
    if the_girl.arousal >= 100:
        "Hearing [the_girl.title] cum in your arms pushes you over the edge. You feel your cock spasm in your underwear as a wave of pleasure washes over you."
        "It takes both of you a moment to recover from your orgasms."
    else:
        "Feeling [the_girl.title]'s body under your hands is enough to push you that little bit further, past the point of no return."
        "You grasp her tightly as you cum, pumping your load out into your pants."
        the_girl.char "Did you just... Cum?"
        mc.name "Yeah."
        "She grinds her butt back into your crotch."
        the_girl.char "Mmm, good to hear."
    return

# label transition_standing_grope_blowjob(the_girl, the_location, the_object):
#
#     return

#TODO: Add a "finger" position that is reachable from here.

label transition_standing_grope_standing_fingering(the_girl, the_location, the_object):
    if the_girl.outfit.vagina_available():
        "You pet [the_girl.title]'s pussy, then slide two fingers inside of it. She gasps as they slip inside."
    else:
        $ the_item = the_girl.outfit.get_lower_top_layer()
        if the_item:
            "You slide a hand under her [the_item.name], bringing your hand right to her pussy."
            "She gasps as you tease it with two fingers, then slip them inside of the wet hole."
        else:
            "You pet [the_girl.title]'s pussy, then slide two fingers inside of it. She gasps as they slip inside."
    the_girl.char "Oh [the_girl.mc_title]... Ah..."
    return

label transition_default_standing_grope(the_girl, the_location, the_object):
    "You gather [the_girl.title] up in your arms, cradling her from behind. You reach one hand down between her legs, and the other up to cup her breasts."
    "She leans her weight against you in response."
    return

label strip_standing_grope(the_girl, the_clothing, the_location, the_object):
    the_girl.char "Your hands feel amazing... Oh my god..."
    $ the_girl.draw_animated_removal(the_clothing, position = standing_grope.position_tag)
    "She strips off her [the_clothing.name] while you're feeling her up."
    return

label strip_ask_standing_grope(the_girl, the_clothing, the_location, the_object):
    the_girl.char "I want to feel you touch me everywhere... Can I talk off my [the_clothing.name] for you?"
    menu:
        "Let her strip.":
            mc.name "Take it off for me."
            $ the_girl.draw_animated_removal(the_clothing, position = standing_grope.position_tag)
            "You watch while [the_girl.possessive_title] takes off her [the_clothing.name] and drops it to the side."

        "Leave it on.":
            mc.name "No, I like how you look with it on."
            if the_girl.sluttiness < 80:
                the_girl.char "Do you think I look sexy in it?"
            else:
                the_girl.char "Don't you think I would look better wearing your cum? That would be so fitting for your dirty little slut, wouldn't it?"
    $ standing_grope.redraw_scene(the_girl)
    return

label orgasm_standing_grope(the_girl, the_location, the_object):
    "You feel [the_girl.possessive_title] tense up in your arms as you explore her body."
    $ the_girl.call_dialogue("climax_responses_foreplay")
    "She quivers with pleasure for a few seconds before her whole body relaxes."
    the_girl.char "Ah... Keep going... I might be able to cum again!"
    return
