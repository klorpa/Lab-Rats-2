init -2 python:
    def train_foreplay_requirement(the_person):
        if the_person.has_taboo("touching_body"):
            return "Broken Touching Taboo"
        else:
            return True

    def train_oral_requirement(the_person):
        if the_person.has_taboo("sucking_cock"):
            return "Broken Blowjob Taboo"
        else:
            return True

    def train_vaginal_requirement(the_person):
        if the_person.has_taboo("vaginal_sex"):
            return "Broken Sex Taboo"
        else:
            return True

    def train_anal_requirement(the_person):
        if the_person.has_taboo("anal_sex"):
            return "Broken Anal Taboo"
        else:
            return True

label train_foreplay_label(the_person): #TODO: All of these should require you have broken the correct taboo.
    mc.name "I want to talk about your personal skills."
    "[the_person.possessive_title] listens attentively."
    mc.name "Your foreplay could use some work. Here, let me show you some examples."
    "You pull out your phone and bring up a collection of porn clips of girls giving strip teases, handjobs, and making out."
    the_person "Oh, I see..."
    $ the_person.change_sex_skill("Foreplay", 1)
    "You keep [the_person.title]'s attention fixed on the screen until you think the lesson has sunk into her suggestible mind."
    return

label train_oral_label(the_person):
    mc.name "I want to talk to you about your oral skills. You really need to work on it."
    "[the_person.possessive_title] nods passively."
    mc.name "Here, let me show you some girls who really know what they're doing..."
    "You pull out your phone and bring up a collection of porn clips showing blowjobs and some choice face fucks."
    the_person "Oh... Do you really think I could do that?"
    mc.name "It's just a matter of practice. You'll get rid of that gag reflex in no time..."
    $ the_person.change_sex_skill("Oral", 1)
    "You keep [the_person.title]'s attention fixed on the screen until you think the lesson has sunk into her suggestible mind."
    return

label train_vaginal_label(the_person):
    mc.name "I need to talk to you about your bedroom skills. They need some work."
    "[the_person.possessive_title] nods passively and listens."
    mc.name "You need to do more than just lie there like a wet fish. And a few keggles wouldn't hurt, too."
    mc.name "Here, I've got some homework for you to look at. Let's take a look."
    "You pull out your phone and bring up a collection of porn clips showing girls getting fucked in a wide range of angles and intensities."
    "She watches without saying anything, eyes fixed on the videos."
    $ the_person.change_sex_skill("Vaginal", 1)
    "You keep feeding her more porn until you think the lesson has sunk into her suggestible mind."
    return

label train_anal_label(the_person):
    mc.name "Let's talk about anal. You have a lot you need to learn if you're going to be impressing anyone."
    "[the_person.possessive_title] nods passively."
    mc.name "Here, I've got some examples of what you should be able to do. Let's take a look and I'll tell you waht to do..."
    "You pull out your phone and bring up a collection of porn clips, each one showing a girl getting happily railed in the ass."
    "[the_person.title] watches without saying anything, her attention grabbed completely by the videos."
    $ the_person.change_sex_skill("Anal", 1)
    "You keep feeding her more porn until you think the lesson has sunk into her suggestible mind."
    return
