init:
    python:
        cunnilingus = Position(name = "Cunnilingus", slut_requirement = 40, slut_cap = 60, requires_hard = False, requires_large_tits = False,
            position_tag = "missionary", requires_location = "Sit", requires_clothing = "Vagina", skill_tag = "Oral",
            girl_arousal = 15, girl_energy = 3,
            guy_arousal = 3, guy_energy = 15,
            connections = [],
            intro = "intro_cunnilingus",
            scenes = ["scene_cunnilingus_1","scene_cunnilingus_2"],
            outro = "outro_cunnilingus",
            transition_default = "transition_default_cunnilingus",
            strip_description = "strip_cunnilingus", strip_ask_description = "strip_ask_cunnilingus",
            orgasm_description = "orgasm_cunnilingus",
            taboo_break_description = "taboo_break_cunnilingus",
            verb = "lick",
            opinion_tags = ["getting head"], record_class = "Cunnilingus",
            associated_taboo = "licking_pussy")

        list_of_positions.append(cunnilingus)

# init 1:
#     python:
#         cunnilingus.link_positions(other, "transition_label") #If there are transitions they go here

label intro_cunnilingus(the_girl, the_location, the_object):
    mc.name "Sit down for me [the_girl.title]."
    "You motion to the [the_object.name]. She nods and sits down in front of you."
    $ cunnilingus.redraw_scene(the_girl) #Draw her sitting down.
    "Get down in front of her and place your hands on her knees, guiding them open."
    "She spreads your legs for you, giving you access to her cute pussy."
    "You lean forward and run your tongue along her slit. She moans softly as soon as you make contact."
    the_girl.char "Oh [the_girl.mc_title]..."
    return

label taboo_break_cunnilingus(the_girl, the_location, the_object):
    "You take [the_girl.title] by the hand and guide her towards the [the_object.name]."
    $ cunnilingus.redraw_scene(the_girl)
    "She follows your direction, sitting down in front of you."
    the_girl.char "What are you doing?"
    "You get down in front of her, place your hands on her knees, and encourage her to spread her legs for you."
    $ the_girl.call_dialogue(cunnilingus.associated_taboo+"_taboo_break")
    "She lets you spread her legs, giving you a clear view of her vagina."
    "You slide forward and bring your head even closer. [the_girl.possessive_title] takes a sharp breath and turns her head to the side."
    "You bring one hand up to her pussy and spread it open to reveal the tender pink inside."
    "With her thighs pressed against your shoulders you can feel every tremble and shiver of anticipation in her body."
    the_girl.char "Come on, do it!"
    "You run your tongue along the length of her slit, tasting her sweet juices."
    the_girl.char "Oh my god!"
    return

label scene_cunnilingus_1(the_girl, the_location, the_object):
    "You lick at [the_girl.possessive_title]'s delicate pussy, spreading her lips and sending your tongue inside."
    "She shivers with each touch, obviously enjoying the feeling."
    if the_person.arousal > 40:
        "Her pussy is dripping wet, filling your mouth with the taste of her juices."
    $ the_girl.call_dialogue("sex_responses_oral")
    return

label scene_cunnilingus_2(the_girl, the_location, the_object):
    "You flick your tongue over [the_girl.possessive_title]'s clit. She gasps and grabs at your shoulders."
    $ the_girl.call_dialogue("sex_responses_oral")
    "You tease the sensitive nub with your tongue, then suck on it gently."
    "She runs her fingers through your hair and sighs, reclining on the [the_object.name]."
    return

label outro_cunnilingus(the_girl, the_location, the_object): #With low arousal gain this is unlikely to come up much
    "The taste of [the_girl.possessive_title]'s pussy, the sound of her moans, and the subtle twitches of her body drive you crazy."
    "You touch yourself, stroking your hard cock between your legs while you pleasure her."
    "Finally you've gone too far, pushing yourself to climax."
    "You pull your head back and grunt, jerking your cock and blasting out a load of cum onto the floor in front of [the_girl.title]."
    the_girl.char "Oh my god... That's so hot!"
    return


label transition_default_cunnilingus(the_girl, the_location, the_object):
    "You get down on your knees in front of [the_girl.title] and push her legs open. She leans back and lets you spread them."
    "You move in and lick her pussy, tasting her sweet juices and making her twitch from the sudden pleasure."
    "She places a hand on the top of your head and moans."
    return

label strip_cunnilingus(the_girl, the_clothing, the_location, the_object):
    $ the_girl.call_dialogue("sex_strip")
    $ the_girl.draw_animated_removal(the_clothing, position = cunnilingus.position_tag)
    "[the_girl.possessive_title] strips off her [the_clothing.name] while you're eating her out, throwing it to the side."
    return

label strip_ask_cunnilingus(the_girl, the_clothing, the_location, the_object):
    the_girl.char "[the_girl.mc_title], I'm like to take off my [the_clothing.name] if you don't mind."
    menu:
        "Let her strip.":
            "You look up from between her legs and nod."
            mc.name "Take it off for me."
            $ the_girl.draw_animated_removal(the_clothing, position = cunnilingus.position_tag)
            "She strips out of her [the_clothing.name] and throws it to the side while you move back in and lick at her cunt."


        "Leave it on.":
            "You look up from between her legs and shake your head."
            mc.name "No, I like how you look with it on."
            the_girl.char "Yeah? Do I look sexy in it? Mmmm..."
    return

label orgasm_cunnilingus(the_girl, the_location, the_object):
    "You notice [the_girl.possessive_title]'s moans becoming louder, and her legs twitching more noticeably on either side of you."
    "You speed up your efforts, doing your best to drive her towards her orgasm. She moans and begins to writhe under your skilled tongue."
    $ the_girl.call_dialogue("climax_responses_oral")
    "All at once the tension in her body is unleashed in a series of violent tremors. Her legs wrap around you for a moment, pulling you against her."
    "The moment passes and she relaxes. For a moment all she can do is look down at you and pant."
    return
