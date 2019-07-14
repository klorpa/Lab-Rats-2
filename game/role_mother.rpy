init -2 python:
    #MOM ACTION REQUIREMENTS
    def mom_weekly_pay_requirement(the_person):
        if time_of_day == 4 and day%7 == 4: #It is the end of the day on friday
            return True
        return False

    def mom_offer_make_dinner_requirement(the_person):
        if time_of_day == 3:
            return True
        return False

### MOM ACTION LABELS ###

label mom_weekly_pay_label(the_person):
    $ renpy.show(bedroom.name,what=bedroom.background_image)
    "You're getting ready for bed when [the_person.possessive_title] calls from downstairs."
    the_person.char "[the_person.mc_title], could we talk for a moment?"
    mc.name "Sure, down in a second."
    $ renpy.show(kitchen.name,what=kitchen.background_image)
    $ the_person.draw_person(position = "sitting")
    "[the_person.title] is sitting at the kitchen table, a collection of bills laid out in front of her."

    if the_person.sluttiness < 20:
        the_person.char "This new morgage on the house is really stressing our finances. It would really help if you could chip in."
        menu:
            "Give her nothing.":
                mc.name "Sorry Mom, I'm just not turning a profit right now. Hopefully we will be soon though. I'll help out as sooon as I can."
                $ the_person.change_happiness(-5)
                $ the_person.change_love(-1)
                $ the_person.draw_person(position = "sitting", emotion = "sad")
                the_person.char "Okay swetheart, I understand. I'll talk with Lily and let her know that we have to cut back on non essentials."

            "Help out.\n{size=22}-$100{/size}" if mc.business.funds >= 100:
                "You pull out your wallet and count out some cash."
                $ mc.business.funds += -100
                mc.name "Here you go Mom, I hope this helps."
                $ the_person.change_happiness(5)
                $ the_person.change_love(3)
                $ the_person.draw_person(position = "sitting", emotion = "happy")
                the_person.char "Every little bit does [the_person.mc_title]. Thank you so much."
                "She gives you a hug and turns her attention back to the bills."

            "Help out.\n{size=22}-$100{/size} (disabled)" if mc.business.funds < 100:
                pass

    else: #TODO: have an even higher level
    #elif the_person.sluttiness < 60:
        if mc.business.event_triggers_dict.get("Mom_Payment_Level",0) >= 1: #We've been through this song and dance already.
            the_person.char "The budget is still really tight [the_person.mc_title], so I was wondering if you wanted to buy any sort of favour from me?"

        else:
            the_person.char "Our budget is really stretched thin right now, and it would be a huge relief if you could help out."
            the_person.char "I wouldn't feel right about just taking your hard earned money though, so I was hoping we could make a deal..."
            mc.name "What sort of deal Mom?"
            the_person.char "Remember last summer, and you paid me for some... personal favours?"
            "She blushes and looks away for a second before regaining her composure."
            the_person.char "Maybe we could start doing that again... I know I shouldn't even bring it up."
            mc.name "No Mom, you're doing it for the good of the family, right? I think it's a great idea."
            $ the_person.change_slut_temp(2)
            $ the_person.change_happiness(5)
            $ the_person.change_love(2)
            the_person.char "Of course, it's the best thing for all of us. What would you like to do?"
            $ mc.business.event_triggers_dict["Mom_Payment_Level"] = 1


        menu:
            "Have strip for you. -$100" if mc.business.funds >= 100:
                if mc.business.event_triggers_dict.get("Mom_Strip",0) >= 1:
                    mc.name "I want you to show off yourself off to me, how does that sound?"
                    the_person.char "Fair is fair, but I'll need a little extra if you want to see anything... inappropriate."
                    $ mc.business.funds += -100
                    "You hand over the cash and sit back while [the_person.possessive_title] entertains you."
                else:
                    $ mc.business.event_triggers_dict["Mom_Strip"] = 1
                    mc.name "I'd like to see a little more of you Mom, how about I pay you to give me a little strip tease."
                    the_person.char "Oh my god, I've raised such a dirty boy. How about I pose for you a bit, and if you want to see more you can contribute a little extra."
                    mc.name "Sounds like a good deal Mom."
                    $ mc.business.funds += -100
                    "You hand over the cash and sit back while [the_person.possessive_title] entertains you."

                call pay_strip_scene(the_person) from _call_pay_strip_scene_2

            "Have strip for you. -$100 (disabled)" if mc.business.funds <100:
                pass

            "Have her test some serum. -$100" if mc.business.funds >= 100:
                if mc.business.event_triggers_dict.get("Mom_Serum_Test",0) >= 1:
                    mc.name "I've got some more serum I'd like you to test Mom."
                    call give_serum(the_person) from _call_give_serum_10
                    if _return:
                        $ mc.business.funds += -100
                        "You hand the serum to [the_person.possessive_title], followed by the cash."
                        the_person.char "Okay, so that's all for now?"
                        mc.name "That's all. I'll just be keeping an eye on you in the future, but you don't need to worry about that."
                        the_person.char "Well thank you [the_person.mc_title], this money will really make a difference. I'm so proud of you!"
                    else:
                        mc.name "Actually, I don't have anything right now. Maybe next wek though, okay?"
                        the_person.char "Okay [the_person.mc_title], thanks for at least thinking about it."
                else:
                    $ mc.business.event_triggers_dict["Mom_Serum_Test"] = 1
                    mc.name "I have something you could help me with Mom."
                    the_person.char "What is it [the_person.mc_title]? I'll do whatever I can for you."
                    mc.name "We have a little bit of a research bottleneck at work. I have something I'd like you to test for me."
                    the_person.char "Oh, okay. If it helps I can be your for hire test subject!"
                    mc.name "Excellent, let me just see if I have anything with me right now..."
                    call give_serum(the_person) from _call_give_serum_11
                    if _return:
                        $ mc.business.funds += -100
                        "You hand the serum to [the_person.possessive_title], followed by the cash."
                        the_person.char "Okay, so that's all for now?"
                        mc.name "That's all. I'll just be keeping an eye on you in the future, but you don't need to worry about that."
                        the_person.char "Well thank you [the_person.mc_title], this money will really make a difference. I'm so proud of you!"
                    else:
                        mc.name "Actually, I don't have anything right now. Maybe next wek though, okay?"
                        the_person.char "Okay [the_person.mc_title], thanks for at least thinking about it."


            "Nothing this week.":
                mc.name "Sorry Mom, but I'm tight on cash right now as well. Maybe next week, okay?"
                "[the_person.possessive_title] nods and turns back to her bills."
                the_person.char "I understand [the_person.mc_title]. Now don't let me keep you, I'm sure you were up to something important."
                pass

            #TODO: pay her to fuck you.
            #TODO: pay her to change her wardrobe
            #TODO: pay her to do somehting with Lily.
            #TODO: have Lily start a cam show to make cash, then bring your Mom into it.


    $ mom_weekly_pay_action = Action("mom weekly pay", mom_weekly_pay_requirement, "mom_weekly_pay_label", args=mom, requirement_args =[mom])
    $ mc.business.mandatory_crises_list.append(mom_weekly_pay_action)
    return

label mom_offer_make_dinner_label(the_person):
    #TODO you offer to make dinner. It takes up time, but you can slip serum to your mom and sister.
    mc.name "You've been working youself so hard lately Mom, how about you let me make dinner tonight?"
    the_person.char "Oh [the_person.mc_title], that's such a sweet thing for you to offer!"
    $ the_person.change_happiness(5)
    $ the_person.change_obedience(-1)
    $ the_person.change_love(2)
    "[the_person.possessive_title] gives you a hug."
    the_person.char "Do you know where everything is?"
    mc.name "Yeah, I think I can take care of it."
    the_person.char "Well thank you, you're always such a help around here!"
    $ renpy.scene("Active")
    $ renpy.show(kitchen.name,what=kitchen.background_image)
    "You head to the kitchen and get to work. The cooking isn't hard, but it takes up most of your evening."
    "As you're plating out dinner you have a perfect opportunity to give your mother or sister some serum in secret."
    menu:
        "Add serum to Mom's food.":
            call give_serum(mom) from _call_give_serum_8

        "Leave Mom's food alone.":
            pass

    menu:
        "Add serum to [lily.name]'s food.":
            call give_serum(lily) from _call_give_serum_9

        "Leave [lily.name]'s food alone.":
            pass

    "You bring the food out and have a nice family dinner together."
    call advance_time from _call_advance_time_10
    return
