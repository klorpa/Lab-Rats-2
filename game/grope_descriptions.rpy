## Holds all of the labels for groping someone to seduce them. Each returns True or False depending on if the character was rejected or not.

label grope_shoulder(the_person):
    # TODO: Make all of this dialogue/reaction personality based.
    "You put your hand on [the_person.title]'s shoulder as you make small talk."
    if the_person.effective_sluttiness("touching_body") < 5:
        #Failure, and you've pissed her off in the process.
        "She shoots you a cold look and takes a step back."
        $ the_person.change_love(-1)
        the_person.char "I'm sorry, I'd prefer if you didn't touch me without permission."
        return False

    else:
        if the_person.effective_sluttiness("touching_body") < 10: #This branch is both a warning to the player not to push things too far and the way they increase sluttiness.
            "She glances uncertainly at your hand, but you give her a warm smile and prompt her to continue the conversation."
            "Once you have her talking again you start to gently massage her shoulder."
            "[the_person.possessive_title] seems uncomfortable but doesn't leave immediately."
            $ the_person.change_love(-1)
            $ the_person.change_slut_temp(2)
        else:
            "[the_person.possessive_title] doesn't seem to mind at all as you start to gently massage her shoulder."

        menu:
            "Move your hand to her waist.":
                return True
            "Stop touching her.":
                return False

label grope_waist(the_person):
    "You give her shoulder a final squeeze, then slide your hand down her back until it's resting on her waist."
    if the_person.effective_sluttiness("touching_body") < 10:
        "[the_person.title] shifts and tries to move away from you."
        the_person.char "Sorry, but could you... Move your hand? I'm just not comfortable with this."
        $ the_person.change_love(-1)
        mc.name "Of course, no problem."
        return False

    else:
        if the_person.effective_sluttiness("touching_body") < 15:
            the_person.char "I... Uh..."
            "You squeeze her hip and smile."
            mc.name "Is something wrong?"
            "She hesitates for a moment, then shakes her head."
            the_person.char "Uh, no. Nothing's wrong [the_person.mc_title]."
            $ the_person.change_slut_temp(2)
            $ the_person.change_love(-1)
            # Uncomfortable

        else:
            #Comfortable
            "[the_person.title] keeps talking as if nothing is wrong. She even smiles when you squeeze her soft hip."

        menu:
            "Slide your hand onto her ass.":
                return True

            "Stop touching her.":
                return False

label grope_ass(the_person):
    if the_person.has_taboo("touching_body"):
        "Feeling bold, you step a little bit closer and slide your hand around behind [the_person.title]."
    else:
        "Feeling a little aroused, you step closer to [the_person.title] and slide your hand behind her."

    if the_person.effective_sluttiness("touching_body") < 15:
        "She yelps and steps towards you as your hand moves onto her ass."
        the_person.char "[the_person.mc_title]! Could you please not just grab my ass when we're talking?!"
        $ the_person.change_love(-1)
        mc.name "Of course, I'm so sorry [the_person.title]. It won't happen again."
        the_person.char "Okay then. Thank you."
        return False

    else:
        if the_person.effective_sluttiness("touching_body") < 20:
            "[the_person.title] squirms a little bit as you run your hand over her ass, trying to move away without making a scene."
            the_person.char "Uh... [the_person.mc_title]. Do you mind?"
            mc.name "Is something wrong?"
            "You grab a handful of her ass and squeeze, making her yelp quietly."
            the_person.char "Ah! You're hand is on my..."
            $ the_person.change_arousal(5)
            $ the_person.change_slut_temp(2)
            $ the_person.change_love(-1)
            "You squeeze again, and this time she just takes a deep breath."
            the_person.char "Never... Never mind. Sorry, what were we talking about?"
            "She seems uncomfortable, but doesn't actively try and stop you from massaging her butt."
        else:
            "As you run your hand over her ass you feel [the_person.title] instinctively press her hips back against it."
            "You grab a handful and squeeze, making her close her eyes and sigh happily."
            $ the_person.change_arousal(5 + mc.sex_skills["Foreplay"])
            mc.name "Is everything okay?"
            the_person.char "Uh, yeah... Everything is fine. Sorry, what was I saying?"
            "She starts talking again, unbothered by your butt massage."

        menu:
            "Grope her tits.":
                return True

            "Stop touching her.":
                return False


label grope_tits(the_person):
    if the_person.has_large_tits():
        "You keep one hand on [the_person.title]'s ass and bring the other up to her big tits. You cup one and massage it gently."
    else:
        "You keep one hand on [the_person.title]'s ass and bring the other up to her tits. You place your hand over one and massage it gently."
    if the_person.effective_sluttiness("touching_body") < 20:
        #Refuses.
        the_person.char "Hey!"
        "She slaps your hand away and glares at you."
        $ the_person.change_love(-1)
        the_person.char "I'm trying to talk to you, could you focus please?"
        mc.name "Right, sorry about that."
        return False

    else:
        if the_person.effective_sluttiness("touching_body") < 25:
            #Uncomfortable
            the_person.char "Oh, I..."
            $ the_person.change_love(-1)
            "[the_person.title] seems unsure of what to do. You smile and prompt her."
            mc.name "Don't mind me, what were you saying?"
            the_person.char "Right, I um... Sorry, I'm having a little trouble concentrating with you..."
            if the_person.outfit.tits_visible():
                "She trails off awkwardly. You can see her nipples hardening in response to your touch."
            else:
                $ the_item = the_person.outfit.get_upper_top_layer()
                "She trails off awkwardly. You feel her nipple harden as you touch her, hidden somewhere beneath her [the_item.display_name]."
            $ the_person.change_arousal(5 + mc.sex_skills["Foreplay"])
            $ the_person.change_slut_temp(2)
            mc.name "That's okay, I don't mind. Take your time."
            "She still seems nervous, but takes a deep breath and tries her best to continue holding up her side of the conversation."
            "You think about going even furthur, but [the_person.possessive_title] seems to be on the edge of what she would tolerate."
            "You satisfy yourself with grabbing her ass and massaging her tits while you talk."
            return False #If she's uncomfortable at this level you can't enter the sex system (ie. you need 35+ sluttiness OR need to have broken the touching body taboo some other way).

        else:
            #Comfortable
            if the_person.has_taboo("touching_body"):
                $ the_person.call_dialogue("touching_body_taboo_break")
                $ the_person.break_taboo("touching_body")
            else:
                the_person.char "Oh... Oh [the_person.mc_title]..."
                "She closes her eyes and takes a deep breath."
                $ the_person.change_arousal(5 + mc.sex_skills["Foreplay"])
                the_person.char "Sorry, you're making it really hard to concentrate right now."
            menu:
                "Keep going.":
                    mc.name "We can keep talking later, I think there's something more important to take care of."
                    if the_person.effective_sluttiness() < 40:
                        "She nods and steps closer to you, pressing her body against yours eagerly."
                        "You slide behind her, cradling a breast in one hand and rubbing her inner thigh with your other."
                    else:
                        "You step closer to [the_person.title]. She seems nervous, but lets you step behind her and wrap your arms around her."
                        "You cradle a breast in one hand and slide your other down between her legs to caress her inner thing."
                    return True #Note: If this returns True it leads into the generic sex system starting with a standing massage position.

                "Stop touching her.":
                    return False
