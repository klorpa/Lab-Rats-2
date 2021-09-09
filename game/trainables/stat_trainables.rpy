init -2 python:
    pass #Requirements go here

label train_slut_label(the_person):
    if the_person.sluttiness < 20:
        mc.name "You need to be more open to new experiences and new sensations. Don't be affraid to open up to people about how you feel."

    elif the_person.sluttiness < 40:
        mc.name "You really need to cut loose a little more. You're so stuffy and uptight."
        mc.name "It wouldn't kill you to show a some skin now and then, you know?"

    elif the_person.sluttiness < 60:
        mc.name "You would have more fun if you stopped worrying about what people think of you and just did whatever you want."
        mc.name "Get naked, have sex, whatever. It's all just so much fun."

    elif the_person.sluttiness < 80:
        mc.name "You should give in to your desires, you'll have more fun if you do."
        mc.name "You know you want to get naked and get fucked, so why are you holding back?"

    else:
        mc.name "You should just accept you're a huge slut. But it's fun being a slut, isn't it?"
        mc.name "Life is simple when you've got a cock in front of you, so just forget about doing anything else."

    "[the_person.possessive_title] nods her head passively, her orgasm-trance making her easier to manipulate."
    the_person "Do you think so? I'm not so sure..."
    mc.name "I'm very sure. Let's talk about it some more, I'm sure I can convince you..."
    "You spend time talking to [the_person.title], carefully moulding her personality while she is in this suggestible state."
    $ the_person.change_slut(5)
    "When you're done she's happily agreeing with you that she should be \"just a little bit\" sluttier."
    return

label train_obedience_label(the_person):
    if the_person.obedience < 100:
        mc.name "Did you know you are absolutely terrible at following orders. It's one of the worst parts of your personality."
        mc.name "You need to shut up and listen some times. It's for your own good."
    elif the_person.obedience < 120:
        mc.name "You need to get better at taking instructions. You can be difficult to work with, and nobody likes that."
        mc.name "If you just did what other people told you to do people would like you more."

    elif the_person.obedience < 140:
        mc.name "You like it when other people tell you what to do, right? It's so much easier than thinking for yourself."
        mc.name "From now on you should always make sure to do what other people tell you to do."

    else:
        mc.name "Life is so much easier when all you have to do is listen to commands and follow them."
        mc.name "You should stop trying to think for yourself at all. Your job is to serve and make other people happy."

    the_person "Do you think so? I'm not sure that's what I want..."
    "She objects weakly, but her climax induced trance has made her very easy to manipulate."
    mc.name "I'm absolutely sure this is what you need to do. Let's talk about it, I'm sure I can convince you..."
    $ the_person.change_obedience(5)
    "When you're done she's realised that you're right, and she should think less and follow instructions more."
    return

label train_love_label(the_person):
    if the_person.love < 0:
        mc.name "I think our relationship got off on the wrong foot. You really should give me another chance."
    elif the_person.love < 25:
        mc.name "I really feel a connection with you [the_person.title], don't you agree?"
    elif the_person.love < 50:
        mc.name "Don't you feel nice when we're together [the_person.title]?"
        mc.name "I really feel a connection, and I'm pretty sure you feel it too."
    elif the_person.love < 75:
        mc.name "This connection between us, it feels so natural. You feel it too, right?"
        mc.name "We need to see where this goes, love like this can't be denied!"
    else:
        mc.name "I can't stay away from you [the_person.title]."
        mc.name "I know you feel it too, we were meant for each other!"

    "[the_person.possessive_title] doesn't seem entirely convinced, but her mind is too addled to argue."
    mc.name "Let's just spend some time together, I'm sure you'll feel the same way soon..."
    $ the_person.change_love(5)
    "When you're done she's warmed significantly to you, mostly thanks to the orgasm-trance you put her in."
    return

label train_suggest_label(the_person):
    mc.name "How are you feeling right now [the_person.title]?"
    the_person "Hmm? Fine, I guess. Why?"
    "Her glassy eyes and neutral smile betray the orgasm-trance you put her in."
    mc.name "Nothing, you just looked like you're having a good day. You like feeling like this, right?"
    "She nods passively, her mouldable mind absorbing your words."
    mc.name "You should try and capture this feeling more often. Let me give you some advice..."
    $ the_person.change_suggest(2)
    "You spend some time weakening [the_person.possessive_title]'s defenses against slipping into a trance when she cums."
    return

label train_charisma_label(the_person):
    mc.name "You should spend some time and work on your people skills [the_person.title]."
    "She listens and nods passively."
    the_person "Do you think so? What do you think I need to change?"
    mc.name "Well, I've got some ideas. Let me tell you..."
    $ the_person.change_cha(1)
    "You explain to [the_person.possessive_title] how best to make friends and influence people."
    return

label train_intelligence_label(the_person):
    mc.name "You need to try and smarten up [the_person.title]. Go back to school, take lessons on line, whatever."
    "She listens and nods passively."
    the_person "Do you think so? I don't even know where to start."
    mc.name "Well, I've got some ideas. Let me tell you..."
    $ the_person.change_int(1)
    "You explain to [the_person.possessive_title] how she should get smarter."
    return

label train_focus_label(the_person):
    mc.name "You need to be a more focused person [the_person.title]."
    "She listens and nods passively."
    the_person "Do you think so? How do I get better at that?"
    mc.name "Well, let me give you some ideas..."
    $ the_person.change_focus(1)
    "You make use of [the_person.possessive_title]'s mouldable state to strengthen her mental willpower."
    return
