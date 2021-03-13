# All of the event stuff for the gym bunny role. When you work out in the gym (A TODO thing) she appears.

label gymbunny_intro_1(the_person):
    "You push for one more rep, then set the bar and sit up to catch your breath."
    $ the_person.draw_person()
    the_person "Hey, good work there. You're getting better at that."
    "A woman walking past your bench slows down and smiles at you."
    "You've seen her around the gym before, and clearly she's seen you too."
    mc.name "Thanks. It's getting easier."
    the_person "Keep it up. I expect to see you around here again, alright?"
    $ the_person.draw_person(position = "walking_away")
    "She gives you a brief smile, then turns and walks away before you can get her name."

    return

label gymbunny_intro_2(the_person):
    #TODO: You work out again, and this time she comes and helps you finish a rep that was slightly too hard
    #TODO: Scolds you for not having a spotter, then offers to do that whenver she's there
    #TODO: Do Character intros
    return

label gymbunny_intro_3(the_person):
    #TODO: Called the first time she spots for you. After she A) compliments your progress and B) says she'd like to share her workout plan.
    return

#After intro_3 you can work out with her every day. At first she takes charge, leaving you with opportunities for things like a stretching massage, serum dose, ect.
#TODO: Maybe your Aunt can be a gym bunny in the future too?

#TODO: Options to give her serum as a "workout enhancer"
#TODO: Event series where you work out with her and have some sort of "workout plan" (that involves a lot of sex)
