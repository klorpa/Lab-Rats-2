### PERSONALITY CHARACTERISTICS ###
init 1300:
    python:
        def stephanie_titles(the_person):
            valid_titles = [the_person.name]
            if the_person.love > 10:
                valid_titles.append("Steph")
            return valid_titles

        def stephanie_possessive_titles(the_person):
            return "Your friend"
        def stephanie_player_titles(the_person):
            return mc.name
        stephanie_personality = Personality("stephanie", default_prefix = "wild",
        common_likes = ["pants", "research work", "Fridays", "makeup", "the colour red"],
        common_sexy_likes = ["giving blowjobs", "drinking cum","cheating on men"],
        common_dislikes = ["Mondays", "HR work", "marketing work", "conservative outfits"],
        common_sexy_dislikes = ["anal sex", "being submissive"],
        titles_function = stephanie_titles, possessive_titles_function = stephanie_possessive_titles, player_titles_function = stephanie_player_titles,
        insta_chance = 40, dikdok_chance = 20)

### DIALOGUE ###
label stephanie_greetings(the_person):
    if the_person.love < 0:
        the_person "Ugh... What do you need? Can we make this quick?"
    elif the_person.happiness < 90:
        the_person "Hey, hope you're having a better day than me. What's up?"
    else:
        if the_person.obedience > 130:
            if the_person.sluttiness > 60:
                the_person "Good to see you [the_person.mc_title], I hope you're here to see me about something fun."
            else:
                the_person "Good to see you [the_person.mc_title], how can I help?"
        else:
            if the_person.sluttiness > 60:
                the_person "Hey [the_person.mc_title], are you here for business or pleasure?"
                "[the_person.title] smiles playfully."
            else:
                "Hey [the_person.mc_title], what's up?"
    return

label stephanie_cum_face(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 60:
            the_person "Mmm, that feels nice. I bet it would feel even nicer in my mouth next time, [the_person.mc_title]."
        else:
            the_person "There we go, all taken care of. You can cum in my mouth next time if you want, it would make cleaning up a lot faster."
    else:
        if the_person.sluttiness > 80:
            the_person "Aww, you should shoot it into my mouth next time. I love how your hot cum tastes."
            "[the_person.title] runs a finger through a puddle of your cum and then licks it clean, winking at you while she does."
        else:
            the_person "Oh man, you really got me covered, didn't you. I wish you would just cum in my mouth so I don't have to worry about getting cleaned up."
    return

label stephanie_cum_mouth(the_person):
    if the_person.obedience > 130:
        if the_person.sluttiness > 60:
            the_person "Oh god, you taste so good. Thank you for the treat [the_person.mc_title]."
        else:
            the_person "Mmm, thank you [the_person.mc_title]."
    else:
        if the_person.sluttiness > 80:
            the_person "Mmm, your cum tastes so great [the_person.mc_title], are you sure there isn't any more of it for me?"
            "[the_person.title] licks her lips and sighs happily."
        else:
            "[the_person.title] licks her lips and smiles at you."
            the_person "Mmm, that was nice."
    return

# label stephanie_cum_vagina(the_person):
#     #TODO
#     return
#
# label stephanie_cum_anal(the_person):
#     #TODO
#     return

label stephanie_improved_serum_unlock(the_person):
    mc.name "[the_person.title], now that you've had some time in the lab there's something I wanted to talk to you about."
    the_person "Okay, how can I help?"
    mc.name "All of our research and development up until this point has been based on the limited notes you and I have from our days at the lab. I wanted to ask if you think there's more we could be doing."
    "[the_person.title] smiles mischieviously."
    the_person "I've got an idea then, I'm sure it's something you'll like."
    mc.name "What's your plan?"
    the_person "All of the testing that I've been doing so far focuses on not getting people killed, which is important, but I really need to know more about what subjective effects there are."
    the_person "I want to take a dose of serum myself and have you record the effects. You can ask me a few questions, gauge how much it affects me."
    mc.name "Do you think that's a good idea?"
    the_person "[nora.title] would never let me do it, but that's why I work for you now and not for her. Come on [the_person.mc_title], this is chance to do real, proper science!"
    return

label stephanie_sex_strip(the_person):
    if the_person.sluttiness < 20:
        if the_person.arousal < 50:
            the_person "Ugh I've started to dress like [nora.title]. Let me take some of this off."
        else:
            the_person "Is it getting warm in here? I need to take something off."

    elif the_person.sluttiness < 60:
        if the_person.arousal < 50:
            the_person "You saw more of me back at the lab, I think I can lose a little more clothing, don't you?"
        else:
            the_person "One second, let me take some of this off for you. Feel free to watch."

    else:
        if the_person.arousal < 50:
            the_person "Ugh, fuck this stupid outfit. I hope you don't mind if I take it off."
        else:
            the_person "Wait, I need to take this off, I want to feel you against me."

    return
