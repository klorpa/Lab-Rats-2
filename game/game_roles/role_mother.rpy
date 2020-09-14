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

    def mom_work_promotion_one_requirement(the_person):
        if the_person.love < 15:
            return False
        elif the_person.sluttiness < 15:
            return False
        elif the_person.obedience < 100:
            return False
        return True

    def mom_work_prmotion_one_before_requirement(start_day):
        if day < start_day:
            return False
        elif mc.business.is_weekend(): #TODO: we really need to stop using the buisness to define what the weekend is.
            return False #No interview on the weekend
        else:
            return True

    def mom_work_promotion_one_report_requirement(the_person, start_day):
        if time_of_day <= 2 and day == start_day:
            return False #Too early in the day for the interview to have happened
        else:
            return True

    def mom_work_promotion_two_intro_requirement(start_day):
        if day < start_day:
            return False
        elif time_of_day != 4:
            return False
        else:
            return True

    def mom_work_promotion_two_prep_requirement(the_person):
        if not the_person.event_triggers_dict.get("mom_work_promotion_two_prep_enabled", False):
            return False #Not visible if not enabled
        elif time_of_day < 3:
            return "Too early to prepare."
        else:
            return True

    def mom_work_promotion_two_requirement(start_day):
        if day < start_day:
            return False
        elif mc.business.is_weekend():
            return False
        else:
            return True

    def mom_work_promotion_two_report_requirement(the_person):
        if the_person in kitchen.people or the_person in mom_bedroom.people: #Only talk about this at home
            return True
        return False

### MOM ACTION LABELS ###

label mom_weekly_pay_label(the_person):
    #todo: at some point demand to take over the house, adds extra "house rules" options
    $ bedroom.show_background()
    "You're getting ready for bed when [the_person.possessive_title] calls from downstairs."
    the_person.char "[the_person.mc_title], could we talk for a moment?"
    mc.name "Sure, down in a second."
    $ kitchen.show_background()
    $ the_person.draw_person(position = "sitting")
    "[the_person.title] is sitting at the kitchen table, a collection of bills laid out in front of her."

    if the_person.effective_sluttiness() < 20:
        the_person.char "This new morgage on the house is really stressing our finances. It would really help if you could chip in."
        call mom_low_sluttiness_weekly_pay(the_person) from _call_mom_low_sluttiness_weekly_pay #The menu is separated out to make looping easier.
    else:
        if mc.business.event_triggers_dict.get("Mom_Payment_Level",0) >= 1: #We've been through this song and dance already.
            if the_person.event_triggers_dict.get("Mom_forced_off_bc", False):
                if the_person.on_birth_control:
                    the_person.char "The budget is still really tight [the_person.mc_title], so I was wondering if you wanted to buy any sort of favour from me?"
                    $ the_person.event_triggers_dict["Mom_forced_off_bc"] = False
                else:
                    the_person.char "The budget is still really tight [the_person.mc_title]. I was hoping you could help out, for a favour, of course."
                    the_person.char "I haven't taken my birth control all week. If you're able to pay me I won't start again."
                    menu:
                        "Keep her off her birth control. -$150" if mc.business.funds >= 150:
                            mc.name "I think we can keep this deal going."
                            "You pull out the cash and hand it over. She places them alongside the bills."
                            $ mc.business.funds += -150
                            the_person.char "Thank you so much. Is there anything else I could do for a little more help?"

                        "Keep her off her birth control. -$150 (disabled)" if mc.business.funds < 150:
                            pass

                        "Let her start taking her birth control.":
                            mc.name "I'm sorry, the budget at work has been a little tight lately."
                            the_person.char "I understand. Is there anything else I can do for then?"
                            call manage_bc(the_person, start = True) from _call_manage_bc
                            $ the_person.event_triggers_dict["Mom_forced_off_bc"] = False
            else:
                the_person.char "The budget is still really tight [the_person.mc_title], so I was wondering if you wanted to buy any sort of favour from me?"

            if lily.event_triggers_dict.get("sister_instathot_special_pictures_recent", False) and not lily.event_triggers_dict.get("sister_instathot_mom_knows", False): #She sold special pictures this week and Mom doesn't know about them yet.
                call mom_weekly_pay_lily_question(the_person) from _call_mom_weekly_pay_lily_question
                $ lily.event_triggers_dict["sister_instathot_special_pictures_recent"] = False


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
        call mom_high_sluttiness_weekly_pay(the_person) from _call_mom_high_sluttiness_weekly_pay


    $ mom_weekly_pay_action = Action("mom weekly pay", mom_weekly_pay_requirement, "mom_weekly_pay_label", args=mom, requirement_args =[mom]) # Reload the event for next week.
    $ mc.business.mandatory_crises_list.append(mom_weekly_pay_action)
    return

label mom_low_sluttiness_weekly_pay(the_person):
    menu:
        "Give her nothing.":
            mc.name "Sorry Mom, I'm just not turning a profit right now. Hopefully we will be soon though. I'll help out as soon as I can."
            $ the_person.change_happiness(-5)
            $ the_person.change_love(-1)
            $ the_person.draw_person(position = "sitting", emotion = "sad")
            the_person.char "Okay swetheart, I understand. I'll talk with Lily and let her know that we have to cut back on non essentials."

        "Help out.\n{size=22}-$100{/size}" if mc.business.funds >= 100:
            "You pull out your wallet and count out some cash, but hesitate before you hand it over."
            $ mc.business.funds += -100
            menu:
                "Ask for a kiss.":
                    mc.name "I'd like a kiss for it though."
                    if the_person.has_taboo("kissing"):
                        the_person.char "A kiss?"
                        mc.name "For being such a good son."
                        the_person.char "Oh, well that's easy then."
                        "[the_person.possessive_title] stands up and leans in to give you a kiss on the cheek."
                        mc.name "On the lips, [the_person.mc_title]. Please?"
                        the_person.char "You've always been so affectionate. Not like other boys at all, you know. Fine."
                        $ kissing.call_taboo_break(the_person, None, None) #We can reuse the kissing taboo break scene for improved dialogue and description.
                        "After a moment she pulls back and looks away from you, blushing."
                        $ the_person.break_taboo("kissing")
                    else:
                        the_person.char "Okay, come here."
                        if the_person.effective_sluttiness("kissing") > 15:
                            "You lean down to kiss her as she's sitting. [the_person.possessive_title] puts a hand on the back of your head and pulls you against her as your lips meet."
                            "Her mouth opens slightly, letting your tongues meet as she makes out with you."
                            $ the_person.change_arousal(5 + mc.sex_skills["Foreplay"])
                            "It might be your imagination, but you think you might even hear her moan."
                            "When you finally break the kiss she fixes her hair and smiles proudly at you."
                        else:
                            "You lean down to kiss her. She lets you press your lips against hers, and even returns the gentle kiss after a moment of hesitation."
                            "When you finally break the kiss she looks away from you, blushing with embarrassment."

                    $ the_person.change_slut_temp(2)
                    the_person.char "There, have I earned my reward?"
                    "You hold out the cash for her and she takes it."
                    the_person.char "Thank you so much, every little bit helps."

                "Make her say please.":
                    mc.name "What are the magic words?"
                    the_person.char "Abracadabra?"
                    mc.name "No, the words we say when we want help?"
                    the_person.char "Oooh, I see what you're getting at. I've drilled it into you and now I'm getting a taste of my own medicine."
                    "She smiles and rolls her eyes playfully."
                    the_person.char "May I {i}please{/i} have some help with the bills?"
                    mc.name "I'm not sure if you mean it..."
                    the_person.char "Pretty please, [the_person.mc_title]?"
                    $ the_person.change_obedience(2)
                    "You hold out the cash and she takes it."
                    mc.name "And..."
                    the_person.char "Thank you [the_person.mc_title], you're very kind."
            $ the_person.change_happiness(5)
            $ the_person.change_love(3)
            $ the_person.draw_person(position = "sitting", emotion = "happy")
            "She gives you a hug and turns her attention back to organising the bills."

        "Help out.\n{size=22}-$100{/size} (disabled)" if mc.business.funds < 100:
            pass
    return

label mom_high_sluttiness_weekly_pay(the_person):
    menu:
        "Strip for me. -$100" if mc.business.funds >= 100:
            if mc.business.event_triggers_dict.get("Mom_Strip", 0) >= 1:
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

        "Strip for me. -$100 (disabled)" if mc.business.funds <100:
            pass

        "Test some serum. -$100" if mc.business.funds >= 100:
            if mc.business.event_triggers_dict.get("Mom_Serum_Test",0) >= 1:
                mc.name "I've got some more serum I'd like you to test Mom."
                call give_serum(the_person) from _call_give_serum_10
                if _return:
                    $ mc.business.funds += -100
                    "You hand the serum to [the_person.possessive_title], followed by the cash."
                    the_person.char "Okay, so that's all for now?"
                    mc.name "That's all. I'll just be keeping an eye on you in the future, but you don't need to worry about that."
                    the_person.char "Well thank you sweetheart, this money will really make a difference. I'm so proud of you!"
                else:
                    mc.name "Actually, I don't have anything right now. Maybe next wek though, okay?"
                    the_person.char "Okay sweetheart, thanks for at least thinking about it."
            else:
                $ mc.business.event_triggers_dict["Mom_Serum_Test"] = 1
                mc.name "I have something you could help me with Mom."
                the_person.char "What is it sweetheart? I'll do whatever I can for you."
                mc.name "We have a little bit of a research bottleneck at work. I have something I'd like you to test for me."
                the_person.char "Oh, okay. If it helps I can be your for hire test subject!"
                mc.name "Excellent, let me just see if I have anything with me right now..."
                call give_serum(the_person) from _call_give_serum_11
                if _return:
                    $ mc.business.funds += -100
                    "You hand the serum to [the_person.possessive_title], followed by the cash."
                    the_person.char "Okay, so that's all for now?"
                    mc.name "That's all. I'll just be keeping an eye on you in the future, but you don't need to worry about that."
                    the_person.char "Well thank you sweetheart, this money will really make a difference. I'm so proud of you!"
                else:
                    mc.name "Actually, I don't have anything right now. Maybe next wek though, okay?"
                    the_person.char "Okay sweetheart, thanks for at least thinking about it."

        # "I want to make some changes around here." if the_person.obedience >= 120:
        #     #TODO: Requires obedience, but unlocks a bunch of other options, like having your Mom bring you breakfast every morning, not wearing anything at home, etc.
        #     mc.name "Now that I'm the man of the house, I want to make some changes around the house."
        #     the_person.char "What sorts of changes?"
        #     call mom_make_house_changes(the_person)
        #
        # "I want to make some changes around here.\nRequires: 120 Obedience (disabled)" if the_person.obedience < 120:
        #     pass


        #TODO: "I want to breed Lily" option, once you've got Mom at high sluttiness, obedience, and Love. She gives you the go-ahead to knock up your sister.

        "Suck me off. -$300" if mc.business.funds >= 300 and the_person.effective_sluttiness("sucking_cock") >= 30:
            mc.name "Alright, I'll pay you to give me a blowjob."
            if (not the_person.has_taboo("sucking_cock")) or the_person.effective_sluttiness("sucking_cock") >= 60:
                the_person.char "If that's what you need."
                "You pull out your wallet and count out her cash while [the_person.possessive_title] gets onto her knees in front of you."
                $ mc.business.funds += -300
                $ the_person.draw_person(position = "blowjob")
                the_person.char "Remember, not a word to anyone else though. Okay>"
                mc.name "Of course, this is just between you and me."
                $ the_person.break_taboo("sucking_cock")

            else:
                the_person.char "What? I mean... I could never do that! How could you even say that?"
                "You pull out your wallet and count out the cash while you talk."
                mc.name "Sure you could. It's just me and you here, nobody would ever need to know."
                mc.name "Besides, it's for the family, right? This is just another way to help everyone out. Myself included, I've been real stressed at work lately."
                $ mc.business.funds += -300
                "You lay the cash down on the table. [the_person.possessive_title] hesitates, then meekly reaches for the money."
                the_person.char "Not a word to anyone, or I'll kick you out of the house."
                mc.name "Of course [the_person.title], don't you trust your own son?"
                $ the_person.draw_person(position = "blowjob")
                "She sighs and kneels down in front of you. You unzip your pants and pull your cock out for your mother."
                mc.name "Don't worry, it won't bite."
                the_person.char "This isn't my exactly my first blowjob sweety, I'm not worried."
                $ the_person.break_taboo("sucking_cock")

            "With that she opens her mouth and slides the tip of your hard cock inside. Her tongue swirls around the tip, sending a jolt of pleasure up your spine."
            $the_person.add_situational_obedience("deal", 20, "I'm doing this for the family")
            call fuck_person(the_person, private = True, start_position = blowjob, skip_intro = True, position_locked = True) from _call_fuck_person_33
            $ the_person.clear_situational_obedience("deal")
            $ the_report = _return
            if the_report.get("girl orgasms", 0) > 0:
                "You pull up your pants while [the_person.possessive_title] is on her knees panting, trying to get her breath back."
                mc.name "I didn't know you were going to enjoy that so much. Maybe you should be paying me next time."
                the_person.char "Ah... I hope we can come to some sort of deal... Ah... In the future..."
            else:
                "You pull your pants up while [the_person.possessive_title] gets off of her kness and cleans herself up."
            $ the_person.review_outfit()
            $ the_person.change_obedience(4)

        "Suck me off. -$300 (disabled)" if mc.business.funds < 300 and the_person.effective_sluttiness("sucking_cock") >= 30:
            pass

        "Stop your birth control. -$150" if mc.business.funds >= 150 and the_person.effective_sluttiness() >= 30 and persistent.pregnancy_pref > 0 and not the_person.event_triggers_dict.get("Mom_forced_off_bc", False):
            mc.name "I have something I'd like you to do. I want you to stop taking your birth control."
            if the_person.on_birth_control:
                if the_person.has_taboo("vaginal_sex"):
                    the_person.char "[the_person.mc_title], why would you want that? I hope you aren't thinking about something inappropriate between us!"
                else:
                    the_person.char "[the_person.mc_title], why would you want that? It's already so wrong every time we're together!"
                mc.name "I just think it would be a good way to remind you about what's important."
                "She seems like she's about to say more, but she stops when you pull out your money."
                the_person.char "How about... I stop for the week. If you don't want me to take it you'll have to pay me every week."
                mc.name "Okay, let's test it out for this week and see how you do."
                "You hand over the money to her and she tucks it away quickly."
                $ mc.business.funds += -150
                the_person.char "One moment."
                "[the_person.possessive_title] leaves the room, but returns quickly. She hands you a small blister pack labeled with each day of the week."
                the_person.char "Here are my pills for the week, so you know I'm not lying. I've already taken one for today, but starting tomorrow I won't have any."
                mc.name "Thank you [the_person.title]."
                $ the_person.event_triggers_dict["Mom_forced_off_bc"] = True
                call manage_bc(the_person, start = False) from _call_manage_bc_1
            else:
                the_person.char "I'm sorry, I can't take your money for that [the_person.mc_title]."
                mc.name "Sure you can [the_person.title], it's..."
                "[the_person.possessive_title] shakes her head and interupts you."
                the_person.char "No, I mean I can't take your money because I'm not taking any birth control right now."
                if the_person.has_taboo("vaginal_sex"):
                    the_person.char "It's been a while since I needed it, so I don't bother."
                else:
                    the_person.char "I know I should, but... I just haven't bothered talking to my doctor."
                the_person.char "Is there something else you would like?"
                call mom_high_sluttiness_weekly_pay(the_person) from _call_mom_high_sluttiness_weekly_pay_1


        "Stop your birth control. -$150 (disabled)" if mc.business.funds < 150 and the_person.effective_sluttiness() >= 30 and persistent.pregnancy_pref > 0  and not the_person.event_triggers_dict.get("Mom_forced_off_bc", False):
            pass


        "Nothing this week.":
            mc.name "Sorry Mom, but I'm tight on cash right now as well. Maybe next week, okay?"
            "[the_person.possessive_title] nods and turns back to her bills."
            the_person.char "I understand sweetheart. Now don't let me keep you, I'm sure you were up to something important."
            pass

        #TODO: pay her to fuck you.
        #TODO: pay her to change her wardrobe
        #TODO: pay her to do somehting with Lily.
        #TODO: have Lily start a cam show to make cash, then bring your Mom into it.



    return

label mom_post_sex_confront(the_person):
    #TODO: She talks to you after the first time you seduce her somehow and talks about how "it was wrong... we can't do that!"

    return

label mom_make_house_changes(the_person):
    # A list of house rules to put into place.
    # TODO: This entire event. Make each one a linked action so that requirements work properly.

    #TODO: Just display a bunch of action options os that the requirements are propertly formatted for all of these.

    # menu:
    #     "I want breakfast delivered to me every morning." if mc.business.event_triggers_dict.get("mom_home_breakfast", false): #Bonus energy recovery. #TODO: Figure out how this works with other random events.
    #
    #
    #     "I want breakfast delivered to me every morning. (disabled)" if not mc.business.event_triggers_dict.get("mom_home_breakfast", false):
    #         pass
    #
    #     "I want my breakfast delivered to me naked." if mc.business.event_triggers_dict.get("mom_home_breakfast", true) and the_person.obedience >= 140 and
    #
    #     "You are going to be naked when you deliver my breakfast.": #Once you're having breakfast delivered
    #         pass
    #
    #     "You are going to service me when you deliver my breakfast.":
    #         pass
    #
    #     "I want you to start wearing more comfortable clothes around the house.": #Sets minimum sluttiness for Mom's outfits
    #         pass
    #
    #     "You are only allowed to wear your underwear when you're at home.":
    #         pass
    #
    #     "You can't wear anything that would keep your tits and pussy from me.":
    #         pass
    #
    #     # TODO: The disipline options are only available after Lily's started her insta-pic account and is posting stuff and you turn her in. If Mom is too slutty she says she doesn't care.
    #     # TODO: Add other "bad" things you can use as leverage against Lily.
    #     "I want to be in charge of Lily's discipline.": #Only after she's done somethign "bad", let's you punish her somehow, or just unlocks other things in this menu?
    #         # The whole Lily section might be better broken out into her role. with this as the enabling action. Definitely one of the paths to breaking them both and having your incest harem.
    #         pass
    #
    #     "Lily is only allowed to be in her underwear while at home.":
    #         pass
    #
    #     "Lily can't wear anything that would keep her tits or pussy from me.":
    #         pass
    #
    #     "Never mind.":
    #         call mom_high_sluttiness_weekly_pay(the_person) #Go back and pick something else.

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
    $ clear_scene()
    $ kitchen.show_background()
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

label mom_serve_breakfast_request(the_person):
    #TODO: You ask her to make you breakfast every morning as your helping-with-the-bills request
    mc.name "I want breakfast brought to me every morning. I'm usually so busy with work I don't have any time to do it myself."
    the_person.char "Okay [the_person.mc_title], if you're able to help out every week with the bills I can do that."
    the_person.char "I'll have to get up early to get it made before work, but I'll do it for you. Maybe [lily.title] can help me."
    # TODO: She wants some extra money from you every week she keeps doing this.
    # TODO: Hook this up to actually do something.
    #TODO: If she's slutty enough to move onto the nude_serve level she has a chance of showing up in her underwear.
    return

label mom_nude_serve_breakfast_request(the_person): # TODO: Hook this up
    mc.name "When you bring me breakfast in the morning I want you to bring it to me naked."
    if the_person.effective_sluttiness() < 60: #She has some reservations about it
        the_person.char "What! [the_person.mc_title], I couldn't..."
        mc.name "Come on [the_person.title], it's nice to start my day off with a little eye candy. I've seen you naked before."
        the_person.char "When you were younger, sure, but you're so much older now."
        mc.name "Well you wanted to know what I wanted in exchange for my help. There it is."
        "She thinks about it for a long time, then nods."
        the_person.char "Fine, if you're going to be paying for it I'll go along with it. I want you to know I think it's silly though."
    else: #She's already really slutty and that's not a big deal
        the_person.char "Okay, if that's what you'd like [the_person.mc_title]."

    return

label mom_breakfast_with_service_request(the_person): # TODO: Hook this up. as a reward
    mc.name "When you bring me breakfast I want you to give me some entertainment as well."
    the_person.char "I'm already naked when I come in, what more do you want [the_person.mc_title]?"
    mc.name "I wake up with morning wood a lot, I want you to use your tits and mouth to take care of that for me."
    if the_person.effective_sluttiness() < 80:
        the_person.char "Oh my god, do you really mean..."
        if the_person.sex_record.get("Blowjobs",0) > 0 or the_person.sex_record.get("Tit Fucks") > 0:
            mc.name "Sure, why not? We've done it before."
            the_person.char "Maybe, but... Do you really want to be doing that every morning?"
            mc.name "Just something quick to blow off some steam. Come on, I love you Mom, don't you love me?"
        else:
            mc.name "Sure, why not? I love you and I want to feel close to you every day. Don't you love me Mom?"
        "You watch as her heart melts. She nods and hugs you."
        the_person.char "Of course I love you [the_person.mc_title]. Okay, I'll do this for you as long as you're helping out with the bills."
    else:
        the_person.char "Of course, I should have thought about that [the_person.mc_title]."
        the_person.char "As long as you're helping with the bills I'll make sure your morning wood is always taken care of."


    return

label mom_work_promotion_one(the_person): #Mom is up for a promotion and asks you for help. You can tell her to get it on her merits (She doesn't) or to dress up for it.
    # Triggered when Mom has 15 sluttiness, 15 Love, and at least 100 Obedience
    $ the_person.draw_person()
    the_person.char "Hi [the_person.mc_title]. It's nice to see you, I'm feeling a little stressed right now."
    mc.name "Is everything okay?"
    the_person.char "Oh, everything is fine. It's actually good news! A promotion is up for grabs at the office, and I'm on the short list."
    mc.name "Hey, congratulations! I'm proud of you [the_person.title]."
    the_person.char "Thank you. I'm just... I'm nervous I'm not going to get it. There's a lot of competition and..."
    "She shrugs and shakes her head."
    the_person.char "Well, never mind what else."
    mc.name "What? You can tell me [the_person.title], I'm here for you."
    "She smiles warmly at you."
    the_person.char "You're so sweet. I'm just worried that I'm the only woman up for the promotion. The senior positions seem like a boys-only club."
    "You nod and think for a moment."
    menu:
        "Take advantage of your womanly charms.":
            mc.name "Well they've made this easy for you then. You've got something none of those men have [the_person.title]."
            the_person.char "What do you mean?"
            mc.name "If you're the only woman then you're the only person who can bring a womans perspective, and a womans charm."
            the_person.char "That is one way of looking at... Wait, what do you mean a \"womans charm\", exactly?"
            the_person.char "I hope you aren't suggesting I do anything unethical."
            mc.name "No, of course not. I'm just pointing out that your looks alone can catch their attention."
            mc.name "Once you have their attention your technical skills will shine through."
            the_person.char "That does make sense... Okay, you're right [the_person.mc_title]."
            the_person.char "Would you help me pick out my interview outfit? You can tell me how a man thinks about it."
            $ the_person.change_slut_temp(2)
            menu:
                "Help her pick out an outfit.":
                    mc.name "Sure thing [the_person.title]. Come on, let's go see what we can find in your closet."
                    the_person.char "Thank you sweetheart. You're such a good boy, helping me out like this."
                    $ mom_bedroom.show_background()
                    "You follow her to her bedroom and start digging around in her wardrobe."
                    call mom_work_promotion_outfit_create(the_person) from _call_mom_work_promotion_outfit_create

                "Let her pick out her own outfit.":
                    mc.name "Sorry [the_person.title], but I don't have the time right now."
                    the_person.char "Of course, you're a busy boy these days. I'm sure I can figure something out myself."

            "She puts her hands on your shoulders and gives you a quick kiss on the cheek."
            the_person.char "Thank you for your support [the_person.mc_title]. I'll let you know how things go!"
            the_person.char "There are two rounds of interviews, hopefully this will get me through to the next round."
            $ the_person.event_triggers_dict["mom_work_promotion_outfit_slutty"] = True #Even if you don't make something special for her she'll try and pick something slutty for herself.

        "You've earned this.":
            mc.name "You don't need to worry [the_person.title]. I know how skilled and dedicated you are, I'm sure your bosses will see it too."
            mc.name "They won't have any choice but to give you the promotion."
            the_person.char "Thank you for your confidence [the_person.mc_title]. There are two interview stages, I'm just hoping to get through to the next round."

    $ mom_work_promotion_one_before_crisis = Action("mom work promotion one before", mom_work_prmotion_one_before_requirement, "mom_work_promotion_one_before", args = the_person, requirement_args = renpy.random.randint(day+3, day+8))
    $ mc.business.mandatory_morning_crises_list.append(mom_work_promotion_one_before_crisis)

    # Leads to a line of events where she basically sleeps her way to a better job.
    # Could we have an alternative line where you find her boss and either A) Sleep with her or B) Fuck his wife?


    $ clear_scene()
    return

label mom_work_promotion_outfit_create(the_person):
    call outfit_master_manager(slut_limit = the_person.sluttiness + 15, show_overwear = False, show_underwear = False) from _call_outfit_master_manager_6
    $ interview_outfit = _return
    if interview_outfit:
        $ acceptable = False
        "You lay the outfit out on [the_person.possessive_title]'s bed."
        mc.name "Let's see how you look in this."
        the_person.char "Okay, just give me one moment..."
        "[the_person.title] starts to strip down."
        $ strip_choice = the_person.outfit.remove_random_any(top_layer_first = True, do_not_remove = True)
        while strip_choice is not None:
            $ the_person.draw_animated_removal(strip_choice)
            "You watch as [the_person.possessive_title] take off her [strip_choice.display_name]."
            $ strip_choice = the_person.outfit.remove_random_any(top_layer_first = True, do_not_remove = True)

        if the_person.update_outfit_taboos():
            "As she gets naked she tries to cover herself up with her hands, turning her body away from you."
            the_person.char "You don't mind me being... naked, do you [the_person.mc_title]?"
            mc.name "No, not at all [the_person.title]. It'll help us finish this faster."
            the_person.char "Right, of course. It's nice for us to be comfortable together, no matter what."
            "She smiles and starts to put on your outfit."
        else:
            "Once she's stripped naked she starts to put on your outfit."

        $ the_person.apply_outfit(interview_outfit)
        $ the_person.draw_person()

        if interview_outfit.vagina_visible():
            the_person.char "I couldn't wear this [the_person.mc_title], I'm not even covered!"
            the_person.char "You've had your fun, now let's be serious about this, okay?"

        elif interview_outfit.tits_visible():
            the_person.char "I couldn't wear this [the_person.mc_title], my breasts are..."
            mc.name "Maybe that'll get you the promotion!"
            "She rolls her eyes."
            the_person.char "I don't think the office dress code will ever be that formal."
            the_person.char "You've had your fun, now let's be serious about this, okay?"

        elif the_person.judge_outfit(interview_outfit): # It's not really pushing the limit
            $ acceptable = True
            the_person.char "Ooh, this is nice [the_person.mc_title]."
            $ the_person.draw_person(position = "back_peek")
            the_person.char "Does it look good from the back?"
            mc.name "It looks great [the_person.possessive_title]."
            $ the_person.draw_person()
            the_person.char "Do you think it's going far enough though? I mean, if the point is to catch some attention."
            the_person.char "It's nice, it just feels a little... boring? Do you think this is what I should wear?"

        else: #It's pushing the limit, but she'll wear it.
            $ acceptable = True
            the_person.char "Ooh, this could work."
            mc.name "Give me a spin, let me see it from behind."
            $ the_person.draw_person(position = "back_peek")
            the_person.char "Well? How does my butt look?"
            mc.name "It looks great [the_person.title]. I think you'll have the full attention of the room."
            "She laughs and gives her hips a wiggle, then turns around and blushes."
            $ the_person.draw_person()
            the_person.char "Sorry, I got a little carried away. It's certainly a bold outfit..."
            the_person.char "Do you think it's appropriate for an interview? I don't want to get in trouble."
            mc.name "You have everything covered that needs covering, it's just a bit of fun self-expression."
            mc.name "I'm sure all the men in the room will appreciate having something nice to look at while you tell them all about your qualifications."
            the_person.char "I suppose it's worth a try... Well, do you think this should be my outfit?"


        menu:
            "Go with it." if acceptable:
                mc.name "I think we've nailed it. You're going to get this promotion [the_person.title]."
                $ the_person.event_triggers_dict["mom_work_promotion_outfit"] = interview_outfit
                $ the_person.wardrobe.add_outfit(interview_outfit.get_copy()) #Add it to her wardrobe so she'll wear it after too.

            "Try something else." if acceptable:
                mc.name "Let's try something else before we commit. You've only got one shot at this, we want to get it right."
                call mom_work_promotion_outfit_create(the_person) from _call_mom_work_promotion_outfit_create_1

            "Try something else." if not acceptable:
                mc.name "Okay, let's try something different and see how it looks."
                call mom_work_promotion_outfit_create(the_person) from _call_mom_work_promotion_outfit_create_2

            "Out of ideas.":
                mc.name "Sorry [the_person.title], but I'm all out of ideas."
                the_person.char "That's okay, you've given me something to think about. I'm sure I can put something together now."

    else:
        mc.name "Sorry [the_person.title], but I don't really know what you should wear."
        the_person.char "That's fine [the_person.mc_title], I'm sure I can figure out something to wear by myself."

    return

label mom_work_promotion_one_before(the_person): # She tells you in the morning that she's going to her interview.
    # If she doesn't have an interview outfit picked she picks one here too.

    "There's a knock on your door shortly after you wake up."
    the_person.char "[the_person.mc_title], it's me. Do you mind if I come in?"
    mc.name "Come in [the_person.title]."
    $ interview_outfit = the_person.event_triggers_dict.get("mom_work_promotion_outfit", None)
    if interview_outfit is None:
        if the_person.event_triggers_dict.get("mom_work_promotion_outfit_slutty", False):
            $ interview_outfit = business_wardrobe.get_outfit_with_name("business_slutty")
            $ the_person.event_triggers_dict["mom_work_promotion_outfit"] = interview_outfit.get_copy()

        else:
            $ interview_outfit = business_wardrobe.get_outfit_with_name("business_conservative")
            $ the_person.event_triggers_dict["mom_work_promotion_outfit"] = interview_outfit.get_copy()

    $ the_person.planned_outfit = interview_outfit
    $ the_person.apply_outfit(interview_outfit)
    $ the_person.draw_person()
    the_person.char "I've got my first interview for my promotion today, so I'm heading to the office early."
    the_person.char "How do I look? Is it okay?"
    "She gives you a quick turn left and right."
    mc.name "You look great [the_person.title], you're going to blow them away."
    the_person.char "Aw, thank you [the_person.mc_title]. Come on, give me a kiss for good luck"
    if the_person.effective_sluttiness("kissing") > 30:
        "[the_person.possessive_title] steps close to you and leans towards you."
        "You kiss her on the lips. She closes her eyes and kisses you back, mainting it for a few long seconds before stepping back."
    else:
        "She leans in and turns her head, letting you give her a peck on the cheek."

    mc.name "Good luck [the_person.title]."
    the_person.char "I'll let you know how it goes when I see you later today. Have a good time at work."
    "She steps out of your room, blowing you a kiss as she closes the door behind her."
    $ clear_scene()
    $ mom_bedroom.move_person(the_person, downtown)
    $ mom_work_promotion_one_report_crisis = Action("mom work promotion one report", mom_work_promotion_one_report_requirement, "mom_work_promotion_one_report", requirement_args = day)
    $ the_person.on_room_enter_event_list.append(mom_work_promotion_one_report_crisis)
    return

label mom_work_promotion_one_report(the_person): # She tells you how her interview went.
    if the_person.event_triggers_dict.get("mom_work_promotion_outfit_slutty", False):
        $ the_person.draw_person(emotion = "happy")
        $ the_person.change_happiness(20, add_to_log = False)
        the_person.char "Oh, hi [the_person.mc_title]. I've got good news! My interview went really well!"
        mc.name "That's great news!"
        the_person.char "I think you were right about my outfit. I was getting comments on it all day!"
        the_person.char "The interview board seems very receptive to my points about bringing a womans viewpoint onto the team, too!"
        "She gives you a tight hug."
        $ the_person.change_love(3)
        the_person.char "Thank you for all of the help and encouragement. You're such a sweetheart."
        mc.name "I'm just happy to see you happy [the_person.title]."
        the_person.char "The next stage of interviews is next week. I'm having a one-on-one lunch with the man who would be my boss."
        the_person.char "I'll worry about that later though, right now I'm just going to have a drink and be happy!"
        # She was using her slutty outfit, things went well
    else:
        $ the_person.draw_person()
        the_person.char "Oh, hi [the_person.mc_title]."
        mc.name "Hey [the_person.title]. Did you have your interview today?"
        the_person.char "I did. It went... Fine, I suppose."
        the_person.char "I made it through to the second round, but there are a lot of other good candidates. I shouldn't get my hopes up."
        mc.name "Don't count yourself out so early. You just need to find a way to stand out in a crowd."
        the_person.char "Maybe you're right. At least I made it through the first round, so I can celebrate that!"
        mc.name "That's the spirit."
        "She gives you a quick hug and kiss on the cheek."
        the_person.char "Thank you for your support [the_person.mc_title]."
        # She was using a conservative outfit, it went poorly

    $ clear_scene()
    $ mom_work_promotion_two_intro_crisis = Action("mom work promotion two intro crisis", mom_work_promotion_two_intro_requirement, "mom_work_promotion_two_intro", args = the_person, requirement_args = renpy.random.randint(day+2, day+4))
    $ mc.business.mandatory_crises_list.append(mom_work_promotion_two_intro_crisis)
    return

label mom_work_promotion_two_intro(the_person): # She asks you to help her prepare for her one-on-one interview.
    "There's a soft knock at your door as you are getting ready for bed."
    the_person.char "It's me, can I come in?"
    mc.name "Come on on [the_person.title]."
    $ the_person.draw_person()
    "[the_person.possessive_title] opens the door and leans in."
    the_person.char "Sorry to bother you, I know you probably want to get to bed after a long day."
    mc.name "Don't worry about it. What's up?"
    the_person.char "My second interview for my promotion is coming up soon, and I was hoping you could help me prepare when you've got time."
    the_person.char "I understand if you're busy, but if you can make time to help your mother out I would appreciate it."
    the_person.char "Just come talk to me if you've got some free time, okay?"
    mc.name "Okay, I will [the_person.title]."
    the_person.char "Thank you [the_person.mc_title]. Sweet dreams."
    "She blows you a kiss and closes the door."
    $ clear_scene()
    $ the_person.event_triggers_dict["mom_work_promotion_two_prep_enabled"] = True

    $ mom_work_promotion_two_crisis = Action("mom_work_promotion_two_crisis", mom_work_promotion_two_requirement, "mom_work_promotion_two", args = the_person, requirement_args = renpy.random.randint(day+6,day+9))
    $ mc.business.mandatory_morning_crises_list.append(mom_work_promotion_two_crisis)
    return

label mom_work_promotion_two_prep(the_person):
    $ the_person.event_triggers_dict["mom_work_promotion_two_prep_enabled"] = False #Disable the action so it can only be taken once.
    mc.name "I've got some spare time, do you want some help getting ready for your interview?"
    $ the_person.draw_person(emotion = "happy")
    if the_person in the_person.home.people: # in her bedroom already
        the_person.char "That would be so helpful, thank you sweetheart."
        $ the_person.draw_person(position = "sitting")
        "She sits down on the side of her bed and motions for you to do the same."
    else:
        the_person.char "That would be so helpful, thank you sweetheart. Let's go to my bedroom, so we don't bother your sister."
        $ mom_bedroom.show_background()
        $ the_person.draw_person(position = "sitting")
        "You follow her to her room. She sits down on the side of her bed and motions for you to do the same."

    the_person.char "Okay, um... So I have some notes about topics I want to discuss, and..."
    mc.name "Wait, before we start you should get into your interview outfit."
    "She nods."
    the_person.char "That's a good idea. The way you dress can say a lot about you."
    the_person.char "Just one second while I get changed..."
    $ the_person.draw_person(position = "walking_away")
    "[the_person.possessive_title] stands up and turns towards her wardrobe as she starts stripping down."

    $ next_item = the_person.outfit.remove_random_any(top_layer_first = True, do_not_remove = True)
    while next_item:
        $ the_person.draw_animated_removal(next_item)
        "..."
        $ next_item = the_person.outfit.remove_random_any(top_layer_first = True, do_not_remove = True)

    $ interview_uniform = the_person.event_triggers_dict.get("mom_work_promotion_outfit", None)
    "Once she's naked she starts to dig around in her wardrobe."
    the_person.char "Now let's see, where did I hang it up..."

    if the_person.event_triggers_dict.get("mom_work_promotion_outfit_slutty", False):
        "She pulls a hanger out of the wardrobe."
        the_person.char "Ah, here it is."
        $ interview_uniform = the_person.event_triggers_dict.get("mom_work_promotion_outfit")
        "[the_person.title] slides the outfit on, then turns around to you and smiles."
        $ the_person.apply_outfit(interview_uniform)
        $ the_person.draw_person(emotion = "happy")
        the_person.char "Does it still look good?"
        mc.name "It looks great [the_person.title]. I can't take my eyes off of you."

    else:
        # She was dressed conservatively.

        mc.name "[the_person.title], were you planning to wear the same outfit?"
        $ the_person.draw_person(position = "back_peek")
        the_person.char "I was. Why?"
        menu:
            "Suggest something sexier.":
                mc.name "It was a little... severe. If this is a one-on-one you want something a little more friend and eye-catching."
                mc.name "Something that will show off your womanly assets."
                the_person.char "Do you think so? I suppose I did have trouble in the first round holding their attention..."
                the_person.char "Okay, let me try putting on something more... revealing. One moment."
                "She turns back to her wardrobe and digs around. She pulls out a few pieces of clothing and put them on the bed."
                the_person.char "Let's try this..."
                $ interview_uniform = business_wardrobe.get_outfit_with_name("business_slutty")
                $ the_person.event_triggers_dict["mom_work_promotion_outfit_slutty"] = True
                $ the_person.apply_outfit(interview_uniform)
                "[the_person.title] slides on her new outfit in front of you."
                $ the_person.draw_person(emotion = "happy")
                the_person.char "What do you think about this? It's a little bolder, but I don't think I would get in any trouble for wearing it."
                mc.name "I think it's a big improvement. I can't take my eyes off of you now."

            "That outfit is fine.":
                mc.name "No reason, I was just curious."
                "She smiles and turns back to the wardrobe. After a moment she pulls out a hanger with the outfit on it."
                $ interview_uniform = the_person.event_triggers_dict.get("mom_work_promotion_outfit") # This is guaranteed to exist by the step 1 before event.
                $ the_person.apply_outfit(interview_uniform)
                "She slides the outfit on in front of you."
                $ the_person.draw_person(emotion = "happy")
                the_person.char "There, now I'm feeling professional."

    $ the_person.draw_person(position = "sitting")
    "[the_person.possessive_title] sits back down on the bed and crosses her legs."

    mc.name "Now let's talk about your attitude. You're going to want to show your potential boss that you're a good fit."
    the_person.char "Oh, just thinking about this is making me nervous. How do you think I should act?"
    menu:
        "Be slutty.": #She gets promoted to be her bosses "secretary"
            mc.name "You need to grab his attention, and you can rely on men to think with their dicks."
            the_person.char "Uh, what do you mean [the_person.mc_title]."
            mc.name "You need to get him excited, [the_person.title]. He's way more likely to enjoy your time together if he's turned on."
            "She nods, but seems unsure."
            the_person.char "I don't need to actually... do anything with him, right?"
            mc.name "No, of course not. You've got a great figure though, so make sure to keep your ti... breasts out front."
            "[the_person.possessive_title] puffs out her chest a little bit."
            the_person.char "Like this?"
            mc.name "That's a good start. Maybe try touching his thigh while you're talking. Just a gentle stroke."
            "She reaches out and rubs your thigh, maintaining eye contact with you."
            the_person.char "Is that about right? Oh, I guess it is!"
            "[the_person.title] pulls her hand back as it brushes against your hardening cock."
            mc.name "Sorry [the_person.title], that's just a natural reaction. Let's practice one other thing you can try."
            the_person.char "Alright, what is it?"
            mc.name "If you think you're losing him try dropping a fork, and then get on your knees to get it."
            mc.name "Let him get a good look at your butt when he thinks you won't notice."
            the_person.char "What if he doesn't look?"
            mc.name "Trust me, he'll look. Give it a try, we can roleplay it a little bit."
            "[the_person.possessive_title] takes a pen from her bed stand and drops it on the floor in front of her."
            the_person.char "Oops. One moment..."
            $ the_person.draw_person(position = "doggy")
            "She gets off the bed and onto her knees, reaching slowly for the pen."
            menu:
                "Slap her ass.":
                    "You sit forward and slap your hand across [the_person.possessive_title]'s butt. She gasps and stands up"
                    $ the_person.draw_person()
                    the_person.char "[the_person.title], try and take this seriously."
                    mc.name "I am being serious. If something like this happens you need to be ready."
                    the_person.char "You mean my boss might..."
                    mc.name "I don't think he would be bold enough, but if he does it means our plan is working."
                    mc.name "You have to make him feel comfortable after, like everyone is having fun."
                    the_person.char "Right..."
                    mc.name "Come on, let's try it again. This time just get the pen and laugh it off."
                    $ the_person.draw_person(position = "doggy")
                    "She nods and gets back onto her knees, making an obvious show of reaching for her dropped pen."
                    the_person.char "Let me just get this..."
                    "You give her ass a solid slap, setting it jiggling for a moment. [the_person.title] gasps, but grabs the pen before standing up."
                    $ the_person.draw_person(emotion = "happy")
                    the_person.char "Haha! Save it for later, we've got business to talk about right now..."
                    "She sits back down next to you and puts the end of the pen on her lips, almost sucking on it."
                    the_person.char "How was that? I think I really got it."
                    "You reposition to make your growing erection more comfortable."
                    mc.name "Yeah, I think you got it too [the_person.title]. He won't be able to say no to you if you can do something like that."

                "Just watch.":
                    "You enjoy the view as she stretches forward and retrieves the pen."
                    $ the_person.draw_person(position = "sitting")
                    "She stands up, brushes off her knees, and sits back down on the bed beside you."
                    the_person.char "How was that? Did I do that right?"
                    mc.name "It was great [the_person.title]."
                    "She smiles and nods."
                    the_person.char "Okay, I think I can do all of that. Once I have his attention I can make sure to talk about all my qualifications."
                    mc.name "Yeah, I'm sure he'll want to hear about that too."

            "[the_person.possessive_title] gives you a warm hug."
            the_person.char "Thank you for the help [the_person.mc_title]. I couldn't have done this without you."
            mc.name "It was my pleasure [the_person.title]. Let me know how it goes, okay?"
            $ the_person.event_triggers_dict["mom_work_promotion_two_tactic"] = "slutty"


        "Be friendly.": #She gets promoted to be her bosses "secretary" if she's dressed sluttily
            mc.name "You need to be friendly with him. Catch his attention and try and make a connection right away."
            the_person.char "Okay, but how do I do that?"
            mc.name "Start by being physical with him. Kiss him on the cheek when you meet, touch his arm when you talk, lean close to him when you can."
            mc.name "If he tries to make any jokes be sure to laugh, even if they aren't funny. Let's give all of that a try now."
            "[the_person.title] nods, and you both stand up."
            $ the_person.draw_person()
            the_person.char "Okay, let's see. Ah... Hello sir, good to see you again."
            mc.name "Mrs.[the_person.last_name], it's good to see you too."
            "You hold out your hand to shake hers. She takes it, then steps forward and gives you a quick hug."
            "She follows it up with a quick peck on the cheek, then motions to the bed."
            the_person.char "Shall we sit down and talk?"
            mc.name "That's perfect [the_person.title]. Keep that up for the whole interview and I think you'll do well."
            the_person.char "Thank you sweetheart, I'm going to do my best."
            "She pulls you into a real hug for a few seconds."
            mc.name "Let me know how it goes, okay?"
            $ the_person.event_triggers_dict["mom_work_promotion_two_tactic"] = "friendly"

        "Be professional.": #She doesn't get any sort of promotion
            mc.name "Keep it professional. Focus on your qualifications and your training."
            "She nods."
            the_person.char "Okay, I think I can do that. I have some notes written down for things I want to tell him about."
            mc.name "Good, let's go through that list now."
            "[the_person.possessive_title] grabs a note pad from her bed stand and starts reading through it."
            "You help her organise her notes and prepare for the interview."
            the_person.char "I think I'm ready, now I just have to wait and try not to worry too much."
            the_person.char "Thank you for the help sweetheart."
            "She leans over and gives you a hug, followed by a kiss on the cheek."
            mc.name "No problem [the_person.title]. Let me know how it goes, okay?"
            $ the_person.event_triggers_dict["mom_work_promotion_two_tactic"] = "professional"


    the_person.char "I'll tell you as soon as I find out."
    $ clear_scene()
    $ mc.location.show_background()
    return

label mom_work_promotion_two(the_person): # Based on what you tell her to do the promotion offer can turn out different ways.
    $ the_person.event_triggers_dict["mom_work_promotion_two_prep_enabled"] = False #Too late to prep if you haven't yet.
    if the_person.event_triggers_dict.get("mom_work_promotion_two_tactic", "none") == "slutty":
        $ the_person.event_triggers_dict["mom_work_secretary_promotion"] = True
    elif the_person.event_triggers_dict.get("mom_work_promotion_two_tactic", "none") == "friendly" and the_person.event_triggers_dict.get("mom_work_promotion_outfit_slutty", False):
        $ the_person.event_triggers_dict["mom_work_secretary_promotion"] = True
    else:
        $ the_person.event_triggers_dict["mom_work_secretary_promotion"] = False

    $ mom_work_promotion_two_report_crisis = Action("mom work promotion two report", mom_work_promotion_two_report_requirement, "mom_work_promotion_two_report")
    $ the_person.on_room_enter_event_list.append(mom_work_promotion_two_report_crisis)
    return

label mom_work_promotion_two_report(the_person): #TODO: Hook this up as an on_room or maybe a mandatory event
    if the_person.event_triggers_dict.get("mom_work_secretary_promotion", False): #Promotion, setting her up to be turned into the office slut.
        $ the_person.change_happiness(20, add_to_log = False)
        $ the_person.draw_person(emotion = "happy")
        "[the_person.title] gives you a bright smile and hurries over to you as soon as she sees you."
        the_person.char "[the_person.mc_title], I have some good news!"
        mc.name "Let me guess. You got your promtion?"
        the_person.char "Kind of. I had a fantastic interview with my superior and I think we really made a connection."
        the_person.char "He told me that the committee had already made their pick, so there wasn't really any chance I was going to get hte promotion."
        the_person.char "But he did tell me that there was a position in his department as his personal technical assistant."
        the_person.char "He offered me the job right there! It's not much of a pay raise, but the hours are more flexible and the work should be easier."
        mc.name "That's fantastic [the_person.title]. I knew it would all work out."
        if the_person.event_triggers_dict.get("mom_work_promotion_two_tactic", "none") == "friendly":
            the_person.char "You were right about being friendly. He said he was really excited for us to be working together."
            the_person.char "I almost think he gave me the job just to spend more time with me."

        elif the_person.event_triggers_dict.get("mom_work_promotion_outfit_slutty", False):
            the_person.char "You were right about being a little flirty with him. He had his eyes all over me the entire time."
            the_person.char "I almost think he gave me the job just so he could spend more time looking at me."

        "[the_person.possessive_title] gives you a tight hug."
        the_person.char "Thank you so much for all of your help sweetheart. You're the best son in the whole world."
        "You hug her back. When she steps away she's still smiling ear to ear."

    else: #No promotion
        $ the_person.change_happiness(-20, add_to_log = False)
        $ the_person.draw_person(emotion = "sad")
        "[the_person.title] gives you a half-hearted smile when she sees you enter the room."
        the_person.char "Oh, hi [the_person.mc_title]..."
        mc.name "Hey [the_person.title]. Is something wrong?"
        the_person.char "I had my second round interview today, and I was told I'm not getting the position."
        mc.name "Oh, I'm sorry."
        "You give [the_person.possessive_title] a gentle hug."
        the_person.char "Thank you. I'll be okay."
        mc.name "I know you will [the_person.title]. They're idiots for not believing in you."
        "She let's you hold her for a few moments, then she steps back and smiles. It seems a little more sincere this time."

    $ clear_scene()
    return

label mom_weekly_pay_lily_question(the_person):
    if the_person.event_triggers_dict.get("mom_instathot_questioned", False):
        the_person.char "Before we talk about that, do can I ask you a question?"
        mc.name "Sure, what do you want to know?"
        the_person.char "Well, it's your sister again. She had more money to help with the bills, but she still won't tell me where it's from."
        the_person.char "I know I said I wouldn't pry, but the only times she leaves the house is to go to class."
        the_person.char "I just really want to be sure she's not in some sort of trouble."
    else:
        the_person.char "Oh, before we talk about that I'm hoping you can answer something for me."
        mc.name "Okay, what do you need to know?"
        the_person.char "Your sister was very strange just now. She actually offered to help with the bills."
        the_person.char "She wouldn't tell me where she's getting this money though."
        the_person.char "I respect her privacy, but I want to make sure she isn't getting into any trouble."
        $ the_person.event_triggers_dict["mom_instathot_questioned"] = True

    menu:
        "Cover for [lily.title].":
            if the_person.event_triggers_dict.get("mom_instathot_questioned", False):
                mc.name "She's working on campus, so I guess she's working between classes."
                the_person.char "I just wish she would trust me."
                mc.name "I'm sure she'll tell you eventually, but you don't need to worry about her."
                the_person.char "I hope she does. Thank you [the_person.mc_title]."

            else:
                mc.name "Uh... No, she isn't getting into any trouble. I think she's just got a job on campus."
                the_person.char "Really? Why wouldn't she tell me about that, I'm so proud of her!"
                mc.name "I don't know, maybe she didn't want you to think she's doing it just because we need money."
                the_person.char "Well, I'll let her tell me when she's ready. I'm just happy to know it's nothing to worry about."

        "Tell her about Insta-pic.":
            mc.name "Well, I think she's picked up a part time job."
            the_person.char "Oh, why haven't I heard about this?"
            mc.name "It's not exactly a traditional job. She's been putting picture up on Insta-pic."
            the_person.char "Insta-pic? Isn't that an internet thing? I don't understand."
            mc.name "[lily.title] puts up pictures showing off clothing, and Insta-pic pays her for the ad traffic she generates."
            the_person.char "So it's like modeling, but she can do it from home?"
            mc.name "I guess so, yeah. She's just worried that you wouldn't approve."
            the_person.char "Why wouldn't I? Models can be very successful. And there are no photographers or agents to take advantage of her."
            the_person.char "I'm going to tell her how proud I am of her. Maybe she'll even let her Mom take a few photos with her."
            "She laughs and shrugs."
            the_person.char "Never mind, nobody's interested in looking at someone old like me."
            mc.name "You should absolutely ask [lily.title] to take some pictures with you. I think you'd be surprised."
            the_person.char "Aww, you're too sweet."
            $ lily.event_triggers_dict["sister_instathot_mom_knows"] = True
            $ sister_instapic_discover_crisis = Action("sister insta mom reveal", sister_instapic_discover_requirement, "sister_instathot_mom_discover", args = lily, requirement_args = lily)
            $ mc.business.mandatory_crises_list.append(sister_instapic_discover_crisis)
    return

label mom_stress_relief_offer(the_person): #TODO: Write and hook this up.

    return
