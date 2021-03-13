init -2 python:
    #MOM ACTION REQUIREMENTS
    def mom_weekly_pay_requirement(the_person):
        if day%7 == 5: #It is the end of the day on friday
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

    def mom_work_promotion_one_before_requirement(start_day):
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

    def mom_date_intercept_requirement(the_person, the_date):
        if the_person is the_date:
            return False
        if not person_at_home(the_person):
            return False
        elif the_person.energy < 80:
            return False
        elif not mc_at_home():
            return False
        elif the_person.love < 10:
            return False
        else:
            return True

    def mom_office_person_request_requirement():
        if time_of_day >= 4 or time_of_day == 0:
            return False
        elif mc.business.is_weekend():
            return False
        return True

    def mom_work_secretary_replacement_intro_requirement(the_person, the_day):
        if day < the_day:
            return False
        elif mc.location.get_person_count() > 1:
            return False
        elif the_person.effective_sluttiness() < 30 or the_person.obedience < 100 or the_person.love < 10:
            return False
        else:
            return True

    def mom_work_secretary_replacement_bigger_tits_reintro_requirement(the_person):
        if not the_person.event_triggers_dict.get("mom_work_tit_options_reintro", False):
            return False
        if the_person.event_triggers_dict.get("mom_office_slutty_level", 0) != 1:
            return False
        elif the_person.event_triggers_dict.get("mom_replacement_approach", "seduce") != "tits":
            return False
        elif mc.location.get_person_count() > 1:
            return "Not while other people are around."
        else:
            return True

    def mom_work_secretary_replacement_report_requirement(the_person, the_day):
        if day < the_day:
            return False
        elif time_of_day < 2:
            return False
        elif mc.location.get_person_count() > 1:
            return False # She doesn't want to talk about it
        elif (the_person.event_triggers_dict.get("mom_replacement_approach_waiting_for_tits", False) and rank_tits(the_person.tits) <= rank_tits(the_person.event_triggers_dict.get("mom_replacement_approach_waiting_for_tits", False))):
            return False
        else:
            return True

    def mom_got_boobjob_requirement(start_day):
        if day < start_day:
            return False
        return True


### MOM ACTION LABELS ###

label mom_weekly_pay_label(the_person):
    #todo: at some point demand to take over the house, adds extra "house rules" options
    $ bedroom.show_background()
    "You're just getting out of bed when [the_person.possessive_title] calls from downstairs."
    the_person "[the_person.mc_title], could we talk for a moment?"
    mc.name "Sure, down in a second."
    $ kitchen.show_background()
    $ the_person.draw_person(position = "sitting")
    "[the_person.title] is sitting at the kitchen table, a collection of bills laid out in front of her."

    if the_person.effective_sluttiness() < 20:
        the_person "This new morgage on the house is really stressing our finances. It would really help if you could chip in."
        call mom_low_sluttiness_weekly_pay(the_person) from _call_mom_low_sluttiness_weekly_pay #The menu is separated out to make looping easier.
    else:
        if mc.business.event_triggers_dict.get("Mom_Payment_Level",0) >= 1: #We've been through this song and dance already.
            if the_person.event_triggers_dict.get("Mom_forced_off_bc", False):
                if the_person.on_birth_control:
                    the_person "The budget is still really tight [the_person.mc_title], so I was wondering if you wanted to buy any sort of favour from me?"
                    $ the_person.event_triggers_dict["Mom_forced_off_bc"] = False
                else:
                    the_person "The budget is still really tight [the_person.mc_title]. I was hoping you could help out, for a favour, of course."
                    the_person "I haven't taken my birth control all week. If you're able to pay me I won't start again."
                    menu:
                        "Keep her off her birth control. -$150" if mc.business.funds >= 150:
                            mc.name "I think we can keep this deal going."
                            "You pull out the cash and hand it over. She places them alongside the bills."
                            $ mc.business.funds += -150
                            the_person "Thank you so much. Is there anything else I could do for a little more help?"

                        "Keep her off her birth control. -$150 (disabled)" if mc.business.funds < 150:
                            pass

                        "Let her start taking her birth control.":
                            mc.name "I'm sorry, the budget at work has been a little tight lately."
                            the_person "I understand. Is there anything else I can do for then?"
                            call manage_bc(the_person, start = True) from _call_manage_bc
                            $ the_person.event_triggers_dict["Mom_forced_off_bc"] = False
            else:
                the_person "The budget is still really tight [the_person.mc_title], so I was wondering if you wanted to buy any sort of favour from me?"

            if lily.event_triggers_dict.get("sister_instathot_special_pictures_recent", False) and not lily.event_triggers_dict.get("sister_instathot_mom_knows", False): #She sold special pictures this week and Mom doesn't know about them yet.
                call mom_weekly_pay_lily_question(the_person) from _call_mom_weekly_pay_lily_question
                $ lily.event_triggers_dict["sister_instathot_special_pictures_recent"] = False


        else:
            the_person "Our budget is really stretched thin right now, and it would be a huge relief if you could help out."
            the_person "I wouldn't feel right about just taking your hard earned money though, so I was hoping we could make a deal..."
            mc.name "What sort of deal Mom?"
            the_person "Remember last summer, and you paid me for some... personal favours?"
            "She blushes and looks away for a second before regaining her composure."
            the_person "Maybe we could start doing that again... I know I shouldn't even bring it up."
            mc.name "No Mom, you're doing it for the good of the family, right? I think it's a great idea."
            $ the_person.change_slut_temp(2)
            $ the_person.change_happiness(5)
            $ the_person.change_love(2)
            the_person "Of course, it's the best thing for all of us. What would you like to do?"
            $ mc.business.event_triggers_dict["Mom_Payment_Level"] = 1
        call mom_high_sluttiness_weekly_pay(the_person) from _call_mom_high_sluttiness_weekly_pay


    $ mom_weekly_pay_action = Action("mom weekly pay", mom_weekly_pay_requirement, "mom_weekly_pay_label", args=mom, requirement_args =[mom]) # Reload the event for next week.
    $ mc.business.mandatory_morning_crises_list.append(mom_weekly_pay_action)
    return

label mom_low_sluttiness_weekly_pay(the_person):
    menu:
        "Give her nothing.":
            mc.name "Sorry Mom, I'm just not turning a profit right now. Hopefully we will be soon though. I'll help out as soon as I can."
            $ the_person.change_happiness(-5)
            $ the_person.change_love(-1)
            $ the_person.draw_person(position = "sitting", emotion = "sad")
            the_person "Okay swetheart, I understand. I'll talk with Lily and let her know that we have to cut back on non essentials."

        "Help out.\n{size=22}-$100{/size}" if mc.business.funds >= 100:
            "You pull out your wallet and count out some cash, but hesitate before you hand it over."
            $ mc.business.funds += -100
            menu:
                "Ask for a kiss.":
                    mc.name "I'd like a kiss for it though."
                    if the_person.has_taboo("kissing"):
                        the_person "A kiss?"
                        mc.name "For being such a good son."
                        the_person "Oh, well that's easy then."
                        "[the_person.possessive_title] stands up and leans in to give you a kiss on the cheek."
                        mc.name "On the lips, [the_person.title]. Please?"
                        the_person "You've always been so affectionate. Not like other boys at all, you know. Fine."
                        $ kissing.call_taboo_break(the_person, None, None) #We can reuse the kissing taboo break scene for improved dialogue and description.
                        "After a moment she pulls back and looks away from you, blushing."
                        $ the_person.break_taboo("kissing")
                    else:
                        the_person "Okay, come here."
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
                    the_person "There, have I earned my reward?"
                    "You hold out the cash for her and she takes it."
                    the_person "Thank you so much, every little bit helps."

                "Make her say please.":
                    mc.name "What are the magic words?"
                    the_person "Abracadabra?"
                    mc.name "No, the words we say when we want help?"
                    the_person "Oooh, I see what you're getting at. I've drilled it into you and now I'm getting a taste of my own medicine."
                    "She smiles and rolls her eyes playfully."
                    the_person "May I {i}please{/i} have some help with the bills?"
                    mc.name "I'm not sure if you mean it..."
                    the_person "Pretty please, [the_person.mc_title]?"
                    $ the_person.change_obedience(2)
                    "You hold out the cash and she takes it."
                    mc.name "And..."
                    the_person "Thank you [the_person.mc_title], you're very kind."
            $ the_person.change_happiness(5)
            $ the_person.change_love(3)
            $ the_person.draw_person(position = "sitting", emotion = "happy")
            "She gives you a hug and turns her attention back to organising the bills."

        "Help out.\n{size=22}-$100{/size} (disabled)" if mc.business.funds < 100:
            pass
    return

label mom_high_sluttiness_weekly_pay(the_person): #TODO: Change all of these over to use Actions instead of just being a menu.
    menu:
        "Strip for me. -$100" if mc.business.funds >= 100:
            if mc.business.event_triggers_dict.get("Mom_Strip", 0) >= 1:
                mc.name "I want you to show off yourself off to me, how does that sound?"
                the_person "Fair is fair, but I'll need a little extra if you want to see anything... inappropriate."
                $ mc.business.funds += -100
                "You hand over the cash and sit back while [the_person.possessive_title] entertains you."
            else:
                $ mc.business.event_triggers_dict["Mom_Strip"] = 1
                mc.name "I'd like to see a little more of you Mom, how about I pay you to give me a little strip tease."
                the_person "Oh my god, I've raised such a dirty boy. How about I pose for you a bit, and if you want to see more you can contribute a little extra."
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
                    the_person "Okay, so that's all for now?"
                    mc.name "That's all. I'll just be keeping an eye on you in the future, but you don't need to worry about that."
                    the_person "Well thank you sweetheart, this money will really make a difference. I'm so proud of you!"
                else:
                    mc.name "Actually, I don't have anything right now. Maybe next wek though, okay?"
                    the_person "Okay sweetheart, thanks for at least thinking about it."
            else:
                $ mc.business.event_triggers_dict["Mom_Serum_Test"] = 1
                mc.name "I have something you could help me with Mom."
                the_person "What is it sweetheart? I'll do whatever I can for you."
                mc.name "We have a little bit of a research bottleneck at work. I have something I'd like you to test for me."
                the_person "Oh, okay. If it helps I can be your for hire test subject!"
                mc.name "Excellent, let me just see if I have anything with me right now..."
                call give_serum(the_person) from _call_give_serum_11
                if _return:
                    $ mc.business.funds += -100
                    "You hand the serum to [the_person.possessive_title], followed by the cash."
                    the_person "Okay, so that's all for now?"
                    mc.name "That's all. I'll just be keeping an eye on you in the future, but you don't need to worry about that."
                    the_person "Well thank you sweetheart, this money will really make a difference. I'm so proud of you!"
                else:
                    mc.name "Actually, I don't have anything right now. Maybe next wek though, okay?"
                    the_person "Okay sweetheart, thanks for at least thinking about it."

        # "I want to make some changes around here." if the_person.obedience >= 120:
        #     #TODO: Requires obedience, but unlocks a bunch of other options, like having your Mom bring you breakfast every morning, not wearing anything at home, etc.
        #     mc.name "Now that I'm the man of the house, I want to make some changes around the house."
        #     the_person "What sorts of changes?"
        #     call mom_make_house_changes(the_person)
        #
        # "I want to make some changes around here.\nRequires: 120 Obedience (disabled)" if the_person.obedience < 120:
        #     pass


        #TODO: "I want to breed Lily" option, once you've got Mom at high sluttiness, obedience, and Love. She gives you the go-ahead to knock up your sister.

        "Suck me off. -$300" if mc.business.funds >= 300 and the_person.effective_sluttiness("sucking_cock") >= 30:
            mc.name "Alright, I'll pay you to give me a blowjob."
            if (not the_person.has_taboo("sucking_cock")) or the_person.effective_sluttiness("sucking_cock") >= 60:
                the_person "If that's what you need."
                "You pull out your wallet and count out her cash while [the_person.possessive_title] gets onto her knees in front of you."
                $ mc.business.funds += -300
                $ the_person.draw_person(position = "blowjob")
                the_person "Remember, not a word to anyone else though. Okay?"
                mc.name "Of course, this is just between you and me."
                $ the_person.break_taboo("sucking_cock")

            else:
                the_person "What? I mean... I could never do that! How could you even say that?"
                "You pull out your wallet and count out the cash while you talk."
                mc.name "Sure you could. It's just me and you here, nobody would ever need to know."
                mc.name "Besides, it's for the family, right? This is just another way to help everyone out. Myself included, I've been real stressed at work lately."
                $ mc.business.funds += -300
                "You lay the cash down on the table. [the_person.possessive_title] hesitates, then meekly reaches for the money."
                the_person "Not a word to anyone, or I'll kick you out of the house."
                mc.name "Of course [the_person.title], don't you trust your own son?"
                $ the_person.draw_person(position = "blowjob")
                "She sighs and kneels down in front of you. You unzip your pants and pull your cock out for your mother."
                mc.name "Don't worry, it won't bite."
                the_person "This isn't my exactly my first blowjob sweety, I'm not worried."
                $ the_person.break_taboo("sucking_cock")

            "With that she opens her mouth and slides the tip of your hard cock inside. Her tongue swirls around the tip, sending a jolt of pleasure up your spine."
            $the_person.add_situational_obedience("deal", 20, "I'm doing this for the family")
            call fuck_person(the_person, private = True, start_position = blowjob, skip_intro = True, position_locked = True) from _call_fuck_person_33
            $ the_person.clear_situational_obedience("deal")
            $ the_report = _return
            if the_report.get("girl orgasms", 0) > 0:
                "You pull up your pants while [the_person.possessive_title] is on her knees panting, trying to get her breath back."
                mc.name "I didn't know you were going to enjoy that so much. Maybe you should be paying me next time."
                the_person "Ah... I hope we can come to some sort of deal... Ah... In the future..."
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
                    the_person "[the_person.mc_title], why would you want that? I hope you aren't thinking about something inappropriate between us!"
                else:
                    the_person "[the_person.mc_title], why would you want that? It's already so wrong every time we're together!"
                mc.name "I just think it would be a good way to remind you about what's important."
                "She seems like she's about to say more, but she stops when you pull out your money."
                the_person "How about... I stop for the week. If you don't want me to take it you'll have to pay me every week."
                mc.name "Okay, let's test it out for this week and see how you do."
                "You hand over the money to her and she tucks it away quickly."
                $ mc.business.funds += -150
                the_person "One moment."
                "[the_person.possessive_title] leaves the room, but returns quickly. She hands you a small blister pack labeled with each day of the week."
                the_person "Here are my pills for the week, so you know I'm not lying. I've already taken one for today, but starting tomorrow I won't have any."
                mc.name "Thank you [the_person.title]."
                $ the_person.event_triggers_dict["Mom_forced_off_bc"] = True
                call manage_bc(the_person, start = False) from _call_manage_bc_1
            else:
                the_person "I'm sorry, I can't take your money for that [the_person.mc_title]."
                mc.name "Sure you can [the_person.title], it's..."
                "[the_person.possessive_title] shakes her head and interupts you."
                the_person "No, I mean I can't take your money because I'm not taking any birth control right now."
                if the_person.has_taboo("vaginal_sex"):
                    the_person "It's been a while since I needed it, so I don't bother."
                else:
                    the_person "I know I should, but... I just haven't bothered talking to my doctor."
                $ the_person.update_birth_control_knowledge()
                the_person "Is there something else you would like?"
                call mom_high_sluttiness_weekly_pay(the_person) from _call_mom_high_sluttiness_weekly_pay_1


        "Stop your birth control. -$150 (disabled)" if mc.business.funds < 150 and the_person.effective_sluttiness() >= 30 and persistent.pregnancy_pref > 0  and not the_person.event_triggers_dict.get("Mom_forced_off_bc", False):
            pass

        #TODO: Enable this and tie it into Lily's new Instapic story chunk
        # "Let [lily.title] get a boob job. -$500" if mc.business.funds >= 200 and lily.event_triggers_dict.get("insta_boobjob_wanted", False): #TODO: Implement this!
        #     mc.name "This will be some easy money for you. I want you to let [lily.title] have some cosmetic surgery done."
        #     mc.name "I'll pay you $500 if you just tell her you're okay with it. You don't need to do anythin else."
        #     the_person "Cosmetic surgery? What does she want to have changed? She's a beautiful young woman!"
        #     menu:
        #         "She wants breast implants.":
        #             mc.name "She wants to have breast implants put in."
        #
        #             pass
        #
        #         "She wants bigger tits.":
        #             mc.name "She's tired of her tiny tits and she wants some bigger ones."
        #             pass

        "Nothing this week.":
            mc.name "Sorry Mom, but I'm tight on cash right now as well. Maybe next week, okay?"
            "[the_person.possessive_title] nods and turns back to her bills."
            the_person "I understand sweetheart. Now don't let me keep you, I'm sure you were up to something important."
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
    #     # TODO: The disipline options are only available after Lily's started her InstaPic account and is posting stuff and you turn her in. If Mom is too slutty she says she doesn't care.
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
    the_person "Oh [the_person.mc_title], that's such a sweet thing for you to offer!"
    $ the_person.change_happiness(5)
    $ the_person.change_obedience(-1)
    $ the_person.change_love(2)
    "[the_person.possessive_title] gives you a hug."
    the_person "Do you know where everything is?"
    mc.name "Yeah, I think I can take care of it."
    the_person "Well thank you, you're always such a help around here!"
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

    if hall.has_person(aunt):
        menu:
            "Add serum to [aunt.name]'s food.":
                call give_serum(aunt) from _call_give_serum_32

            "Leave [aunt.name]'s food alone.":
                pass

    if hall.has_person(cousin) or lily_bedroom.has_person(cousin):
        menu:
            "Add serum to [cousin.name]'s food.":
                call give_serum(cousin) from _call_give_serum_33

            "Leave [cousin.name]'s food alone.":
                pass

    "You bring the food out and have a nice family dinner together."
    call advance_time from _call_advance_time_10
    return

label mom_serve_breakfast_request(the_person):
    #TODO: You ask her to make you breakfast every morning as your helping-with-the-bills request
    mc.name "I want breakfast brought to me every morning. I'm usually so busy with work I don't have any time to do it myself."
    the_person "Okay [the_person.mc_title], if you're able to help out every week with the bills I can do that."
    the_person "I'll have to get up early to get it made before work, but I'll do it for you. Maybe [lily.title] can help me."
    # TODO: She wants some extra money from you every week she keeps doing this.
    # TODO: Hook this up to actually do something.
    #TODO: If she's slutty enough to move onto the nude_serve level she has a chance of showing up in her underwear.
    return

label mom_nude_serve_breakfast_request(the_person): # TODO: Hook this up
    mc.name "When you bring me breakfast in the morning I want you to bring it to me naked."
    if the_person.effective_sluttiness() < 60: #She has some reservations about it
        the_person "What! [the_person.mc_title], I couldn't..."
        mc.name "Come on [the_person.title], it's nice to start my day off with a little eye candy. I've seen you naked before."
        the_person "When you were younger, sure, but you're so much older now."
        mc.name "Well you wanted to know what I wanted in exchange for my help. There it is."
        "She thinks about it for a long time, then nods."
        the_person "Fine, if you're going to be paying for it I'll go along with it. I want you to know I think it's silly though."
    else: #She's already really slutty and that's not a big deal
        the_person "Okay, if that's what you'd like [the_person.mc_title]."

    return

label mom_breakfast_with_service_request(the_person): # TODO: Hook this up. as a reward
    mc.name "When you bring me breakfast I want you to give me some entertainment as well."
    the_person "I'm already naked when I come in, what more do you want [the_person.mc_title]?"
    mc.name "I wake up with morning wood a lot, I want you to use your tits and mouth to take care of that for me."
    if the_person.effective_sluttiness() < 80:
        the_person "Oh my god, do you really mean..."
        if the_person.sex_record.get("Blowjobs",0) > 0 or the_person.sex_record.get("Tit Fucks") > 0:
            mc.name "Sure, why not? We've done it before."
            the_person "Maybe, but... Do you really want to be doing that every morning?"
            mc.name "Just something quick to blow off some steam. Come on, I love you Mom, don't you love me?"
        else:
            mc.name "Sure, why not? I love you and I want to feel close to you every day. Don't you love me Mom?"
        "You watch as her heart melts. She nods and hugs you."
        the_person "Of course I love you [the_person.mc_title]. Okay, I'll do this for you as long as you're helping out with the bills."
    else:
        the_person "Of course, I should have thought about that [the_person.mc_title]."
        the_person "As long as you're helping with the bills I'll make sure your morning wood is always taken care of."


    return

label mom_work_promotion_one(the_person): #Mom is up for a promotion and asks you for help. You can tell her to get it on her merits (She doesn't) or to dress up for it.
    # Triggered when Mom has 15 sluttiness, 15 Love, and at least 100 Obedience
    $ the_person.draw_person()
    the_person "Hi [the_person.mc_title]. It's nice to see you, I'm feeling a little stressed right now."
    mc.name "Is everything okay?"
    the_person "Oh, everything is fine. It's actually good news! A promotion is up for grabs at the office, and I'm on the short list."
    mc.name "Hey, congratulations! I'm proud of you [the_person.title]."
    the_person "Thank you. I'm just... I'm nervous I'm not going to get it. There's a lot of competition and..."
    "She shrugs and shakes her head."
    the_person "Well, never mind what else."
    mc.name "What? You can tell me [the_person.title], I'm here for you."
    "She smiles warmly at you."
    the_person "You're so sweet. I'm just worried that I'm the only woman up for the promotion. The senior positions seem like a boys-only club."
    "You nod and think for a moment."
    menu:
        "Take advantage of your womanly charms.":
            mc.name "Well they've made this easy for you then. You've got something none of those men have [the_person.title]."
            the_person "What do you mean?"
            mc.name "If you're the only woman then you're the only person who can bring a womans perspective, and a womans charm."
            the_person "That is one way of looking at... Wait, what do you mean a \"womans charm\", exactly?"
            the_person "I hope you aren't suggesting I do anything unethical."
            mc.name "No, of course not. I'm just pointing out that your looks alone can catch their attention."
            mc.name "Once you have their attention your technical skills will shine through."
            the_person "That does make sense... Okay, you're right [the_person.mc_title]."
            the_person "Would you help me pick out my interview outfit? You can tell me how a man thinks about it."
            $ the_person.change_slut_temp(2)
            menu:
                "Help her pick out an outfit.":
                    mc.name "Sure thing [the_person.title]. Come on, let's go see what we can find in your closet."
                    the_person "Thank you sweetheart. You're such a good boy, helping me out like this."
                    $ mom_bedroom.show_background()
                    "You follow her to her bedroom and start digging around in her wardrobe."
                    call mom_work_promotion_outfit_create(the_person) from _call_mom_work_promotion_outfit_create

                "Let her pick out her own outfit.":
                    mc.name "Sorry [the_person.title], but I don't have the time right now."
                    the_person "Of course, you're a busy boy these days. I'm sure I can figure something out myself."

            "She puts her hands on your shoulders and gives you a quick kiss on the cheek."
            the_person "Thank you for your support [the_person.mc_title]. I'll let you know how things go!"
            the_person "There are two rounds of interviews, hopefully this will get me through to the next round."
            $ the_person.event_triggers_dict["mom_work_promotion_outfit_slutty"] = True #Even if you don't make something special for her she'll try and pick something slutty for herself.

        "You've earned this.":
            mc.name "You don't need to worry [the_person.title]. I know how skilled and dedicated you are, I'm sure your bosses will see it too."
            mc.name "They won't have any choice but to give you the promotion."
            the_person "Thank you for your confidence [the_person.mc_title]. There are two interview stages, I'm just hoping to get through to the next round."

    $ mom_work_promotion_one_before_crisis = Action("mom work promotion one before", mom_work_promotion_one_before_requirement, "mom_work_promotion_one_before", args = the_person, requirement_args = renpy.random.randint(day+3, day+8))
    $ mc.business.mandatory_morning_crises_list.append(mom_work_promotion_one_before_crisis)
    $ the_person.apply_outfit() # If you've been trying out an outfit she changes back into it.
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
        the_person "Okay, just give me one moment..."
        "[the_person.title] starts to strip down."
        $ strip_list = the_person.outfit.get_full_strip_list()
        $ generalised_strip_description(the_person, strip_list)

        if the_person.update_outfit_taboos():
            "As she gets naked she tries to cover herself up with her hands, turning her body away from you."
            the_person "You don't mind me being... naked, do you [the_person.mc_title]?"
            mc.name "No, not at all [the_person.title]. It'll help us finish this faster."
            the_person "Right, of course. It's nice for us to be comfortable together, no matter what."
            "She smiles and starts to put on your outfit."
        else:
            "Once she's stripped naked she starts to put on your outfit."

        $ the_person.apply_outfit(interview_outfit)
        $ the_person.draw_person()

        if interview_outfit.vagina_visible():
            the_person "I couldn't wear this [the_person.mc_title], I'm not even covered!"
            the_person "You've had your fun, now let's be serious about this, okay?"

        elif interview_outfit.tits_visible():
            the_person "I couldn't wear this [the_person.mc_title], my breasts are..."
            mc.name "Maybe that'll get you the promotion!"
            "She rolls her eyes."
            the_person "I don't think the office dress code will ever be that formal."
            the_person "You've had your fun, now let's be serious about this, okay?"

        elif the_person.judge_outfit(interview_outfit): # It's not really pushing the limit
            $ acceptable = True
            the_person "Ooh, this is nice [the_person.mc_title]."
            $ the_person.draw_person(position = "back_peek")
            the_person "Does it look good from the back?"
            mc.name "It looks great [the_person.possessive_title]."
            $ the_person.draw_person()
            the_person "Do you think it's going far enough though? I mean, if the point is to catch some attention."
            the_person "It's nice, it just feels a little... boring? Do you think this is what I should wear?"

        else: #It's pushing the limit, but she'll wear it.
            $ acceptable = True
            the_person "Ooh, this could work."
            mc.name "Give me a spin, let me see it from behind."
            $ the_person.draw_person(position = "back_peek")
            the_person "Well? How does my butt look?"
            mc.name "It looks great [the_person.title]. I think you'll have the full attention of the room."
            "She laughs and gives her hips a wiggle, then turns around and blushes."
            $ the_person.draw_person()
            the_person "Sorry, I got a little carried away. It's certainly a bold outfit..."
            the_person "Do you think it's appropriate for an interview? I don't want to get in trouble."
            mc.name "You have everything covered that needs covering, it's just a bit of fun self-expression."
            mc.name "I'm sure all the men in the room will appreciate having something nice to look at while you tell them all about your qualifications."
            the_person "I suppose it's worth a try... Well, do you think this should be my outfit?"


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
                the_person "That's okay, you've given me something to think about. I'm sure I can put something together now."

    else:
        mc.name "Sorry [the_person.title], but I don't really know what you should wear."
        the_person "That's fine [the_person.mc_title], I'm sure I can figure out something to wear by myself."

    return

label mom_work_promotion_one_before(the_person): # She tells you in the morning that she's going to her interview.
    # If she doesn't have an interview outfit picked she picks one here too.

    "There's a knock on your door shortly after you wake up."
    the_person "[the_person.mc_title], it's me. Do you mind if I come in?"
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
    the_person "I've got my first interview for my promotion today, so I'm heading to the office early."
    the_person "How do I look? Is it okay?"
    "She gives you a quick turn left and right."
    mc.name "You look great [the_person.title], you're going to blow them away."
    the_person "Aw, thank you [the_person.mc_title]. Come on, give me a kiss for good luck"
    if the_person.effective_sluttiness("kissing") > 30:
        "[the_person.possessive_title] steps close to you and leans towards you."
        "You kiss her on the lips. She closes her eyes and kisses you back, mainting it for a few long seconds before stepping back."
    else:
        "She leans in and turns her head, letting you give her a peck on the cheek."

    mc.name "Good luck [the_person.title]."
    the_person "I'll let you know how it goes when I see you later today. Have a good time at work."
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
        the_person "Oh, hi [the_person.mc_title]. I've got good news! My interview went really well!"
        mc.name "That's great news!"
        the_person "I think you were right about my outfit. I was getting comments on it all day!"
        the_person "The interview board seems very receptive to my points about bringing a womans viewpoint onto the team, too!"
        "She gives you a tight hug."
        $ the_person.change_love(3)
        the_person "Thank you for all of the help and encouragement. You're such a sweetheart."
        mc.name "I'm just happy to see you happy [the_person.title]."
        the_person "The next stage of interviews is next week. I'm having a one-on-one lunch with the man who would be my boss."
        the_person "I'll worry about that later though, right now I'm just going to have a drink and be happy!"
        # She was using her slutty outfit, things went well
    else:
        $ the_person.draw_person()
        the_person "Oh, hi [the_person.mc_title]."
        mc.name "Hey [the_person.title]. Did you have your interview today?"
        the_person "I did. It went... Fine, I suppose."
        the_person "I made it through to the second round, but there are a lot of other good candidates. I shouldn't get my hopes up."
        mc.name "Don't count yourself out so early. You just need to find a way to stand out in a crowd."
        the_person "Maybe you're right. At least I made it through the first round, so I can celebrate that!"
        mc.name "That's the spirit."
        "She gives you a quick hug and kiss on the cheek."
        the_person "Thank you for your support [the_person.mc_title]."
        # She was using a conservative outfit, it went poorly

    $ clear_scene()
    $ mom_work_promotion_two_intro_crisis = Action("mom work promotion two intro crisis", mom_work_promotion_two_intro_requirement, "mom_work_promotion_two_intro", args = the_person, requirement_args = renpy.random.randint(day+2, day+4))
    $ mc.business.mandatory_crises_list.append(mom_work_promotion_two_intro_crisis)
    return

label mom_work_promotion_two_intro(the_person): # She asks you to help her prepare for her one-on-one interview.
    "There's a soft knock at your door as you are getting ready for bed."
    the_person "It's me, can I come in?"
    mc.name "Come on on [the_person.title]."
    $ the_person.draw_person()
    "[the_person.possessive_title] opens the door and leans in."
    the_person "Sorry to bother you, I know you probably want to get to bed after a long day."
    mc.name "Don't worry about it. What's up?"
    the_person "My second interview for my promotion is coming up soon, and I was hoping you could help me prepare when you've got time."
    the_person "I understand if you're busy, but if you can make time to help your mother out I would appreciate it."
    the_person "Just come talk to me if you've got some free time, okay?"
    mc.name "Okay, I will [the_person.title]."
    the_person "Thank you [the_person.mc_title]. Sweet dreams."
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
        the_person "That would be so helpful, thank you sweetheart."
        $ the_person.draw_person(position = "sitting")
        "She sits down on the side of her bed and motions for you to do the same."
    else:
        the_person "That would be so helpful, thank you sweetheart. Let's go to my bedroom, so we don't bother your sister."
        $ mom_bedroom.show_background()
        $ the_person.draw_person(position = "sitting")
        "You follow her to her room. She sits down on the side of her bed and motions for you to do the same."

    the_person "Okay, um... So I have some notes about topics I want to discuss, and..."
    mc.name "Wait, before we start you should get into your interview outfit."
    "She nods."
    the_person "That's a good idea. The way you dress can say a lot about you."
    the_person "Just one second while I get changed..."
    $ the_person.draw_person(position = "walking_away")
    "[the_person.possessive_title] stands up and turns towards her wardrobe as she starts stripping down."

    $ strip_list = the_person.outfit.get_full_strip_list()
    $ generalised_strip_description(the_person, strip_list, position = "walking_away")

    $ interview_uniform = the_person.event_triggers_dict.get("mom_work_promotion_outfit", None)
    "Once she's naked she starts to dig around in her wardrobe."
    the_person "Now let's see, where did I hang it up..."

    if the_person.event_triggers_dict.get("mom_work_promotion_outfit_slutty", False):
        "She pulls a hanger out of the wardrobe."
        the_person "Ah, here it is."
        $ interview_uniform = the_person.event_triggers_dict.get("mom_work_promotion_outfit")
        "[the_person.title] slides the outfit on, then turns around to you and smiles."
        $ the_person.apply_outfit(interview_uniform)
        $ the_person.draw_person(emotion = "happy")
        the_person "Does it still look good?"
        mc.name "It looks great [the_person.title]. I can't take my eyes off of you."

    else:
        # She was dressed conservatively.

        mc.name "[the_person.title], were you planning to wear the same outfit?"
        $ the_person.draw_person(position = "back_peek")
        the_person "I was. Why?"
        menu:
            "Suggest something sexier.":
                mc.name "It was a little... severe. If this is a one-on-one you want something a little more friend and eye-catching."
                mc.name "Something that will show off your womanly assets."
                the_person "Do you think so? I suppose I did have trouble in the first round holding their attention..."
                the_person "Okay, let me try putting on something more... revealing. One moment."
                "She turns back to her wardrobe and digs around. She pulls out a few pieces of clothing and put them on the bed."
                the_person "Let's try this..."
                $ interview_uniform = business_wardrobe.get_outfit_with_name("business_slutty")
                $ the_person.event_triggers_dict["mom_work_promotion_outfit_slutty"] = True
                $ the_person.apply_outfit(interview_uniform)
                "[the_person.title] slides on her new outfit in front of you."
                $ the_person.draw_person(emotion = "happy")
                the_person "What do you think about this? It's a little bolder, but I don't think I would get in any trouble for wearing it."
                mc.name "I think it's a big improvement. I can't take my eyes off of you now."

            "That outfit is fine.":
                mc.name "No reason, I was just curious."
                "She smiles and turns back to the wardrobe. After a moment she pulls out a hanger with the outfit on it."
                $ interview_uniform = the_person.event_triggers_dict.get("mom_work_promotion_outfit") # This is guaranteed to exist by the step 1 before event.
                $ the_person.apply_outfit(interview_uniform)
                "She slides the outfit on in front of you."
                $ the_person.draw_person(emotion = "happy")
                the_person "There, now I'm feeling professional."

    $ the_person.draw_person(position = "sitting")
    "[the_person.possessive_title] sits back down on the bed and crosses her legs."

    mc.name "Now let's talk about your attitude. You're going to want to show your potential boss that you're a good fit."
    the_person "Oh, just thinking about this is making me nervous. How do you think I should act?"
    menu:
        "Be slutty.": #She gets promoted to be her bosses "secretary"
            mc.name "You need to grab his attention, and you can rely on men to think with their dicks."
            the_person "Uh, what do you mean [the_person.mc_title]."
            mc.name "You need to get him excited, [the_person.title]. He's way more likely to enjoy your time together if he's turned on."
            "She nods, but seems unsure."
            the_person "I don't need to actually... do anything with him, right?"
            mc.name "No, of course not. You've got a great figure though, so make sure to keep your ti... breasts out front."
            "[the_person.possessive_title] puffs out her chest a little bit."
            the_person "Like this?"
            mc.name "That's a good start. Maybe try touching his thigh while you're talking. Just a gentle stroke."
            "She reaches out and rubs your thigh, maintaining eye contact with you."
            the_person "Is that about right? Oh, I guess it is!"
            "[the_person.title] pulls her hand back as it brushes against your hardening cock."
            mc.name "Sorry [the_person.title], that's just a natural reaction. Let's practice one other thing you can try."
            the_person "Alright, what is it?"
            mc.name "If you think you're losing him try dropping a fork, and then get on your knees to get it."
            mc.name "Let him get a good look at your butt when he thinks you won't notice."
            the_person "What if he doesn't look?"
            mc.name "Trust me, he'll look. Give it a try, we can roleplay it a little bit."
            "[the_person.possessive_title] takes a pen from her bed stand and drops it on the floor in front of her."
            the_person "Oops. One moment..."
            $ the_person.draw_person(position = "doggy")
            "She gets off the bed and onto her knees, reaching slowly for the pen."
            menu:
                "Slap her ass.":
                    "You sit forward and slap your hand across [the_person.possessive_title]'s butt. She gasps and turns around on the floor."
                    $ the_person.draw_person(position = "kneeling1")
                    the_person "[the_person.mc_title], try and take this seriously."
                    mc.name "I am being serious. If something like this happens you need to be ready."
                    the_person "You mean my boss might..."
                    mc.name "I don't think he would be bold enough, but if he does it means our plan is working."
                    mc.name "You have to make him feel comfortable after, like everyone is having fun."
                    the_person "Right..."
                    mc.name "Come on, let's try it again. This time just get the pen and laugh it off."
                    $ the_person.draw_person(position = "doggy")
                    "She nods and gets back onto her knees, making an obvious show of reaching for her dropped pen."
                    the_person "Let me just get this..."
                    "You give her ass a solid slap, setting it jiggling for a moment. [the_person.title] gasps, but grabs the pen before standing up."
                    $ the_person.draw_person(emotion = "happy")
                    the_person "Haha! Save it for later, we've got business to talk about right now..."
                    "She sits back down next to you and puts the end of the pen on her lips, almost sucking on it."
                    the_person "How was that? I think I really got it."
                    "You reposition to make your growing erection more comfortable."
                    mc.name "Yeah, I think you got it too [the_person.title]. He won't be able to say no to you if you can do something like that."

                "Just watch.":
                    "You enjoy the view as she stretches forward and retrieves the pen."
                    $ the_person.draw_person(position = "sitting")
                    "She stands up, brushes off her knees, and sits back down on the bed beside you."
                    the_person "How was that? Did I do that right?"
                    mc.name "It was great [the_person.title]."
                    "She smiles and nods."
                    the_person "Okay, I think I can do all of that. Once I have his attention I can make sure to talk about all my qualifications."
                    mc.name "Yeah, I'm sure he'll want to hear about that too."

            "[the_person.possessive_title] gives you a warm hug."
            the_person "Thank you for the help [the_person.mc_title]. I couldn't have done this without you."
            mc.name "It was my pleasure [the_person.title]. Let me know how it goes, okay?"
            $ the_person.event_triggers_dict["mom_work_promotion_two_tactic"] = "slutty"


        "Be friendly.": #She gets promoted to be her bosses "secretary" if she's dressed sluttily
            mc.name "You need to be friendly with him. Catch his attention and try and make a connection right away."
            the_person "Okay, but how do I do that?"
            mc.name "Start by being physical with him. Kiss him on the cheek when you meet, touch his arm when you talk, lean close to him when you can."
            mc.name "If he tries to make any jokes be sure to laugh, even if they aren't funny. Let's give all of that a try now."
            "[the_person.title] nods, and you both stand up."
            $ the_person.draw_person()
            the_person "Okay, let's see. Ah... Hello sir, good to see you again."
            mc.name "Mrs.[the_person.last_name], it's good to see you too."
            "You hold out your hand to shake hers. She takes it, then steps forward and gives you a quick hug."
            "She follows it up with a quick peck on the cheek, then motions to the bed."
            the_person "Shall we sit down and talk?"
            mc.name "That's perfect [the_person.title]. Keep that up for the whole interview and I think you'll do well."
            the_person "Thank you sweetheart, I'm going to do my best."
            "She pulls you into a real hug for a few seconds."
            mc.name "Let me know how it goes, okay?"
            $ the_person.event_triggers_dict["mom_work_promotion_two_tactic"] = "friendly"

        "Be professional.": #She doesn't get any sort of promotion
            mc.name "Keep it professional. Focus on your qualifications and your training."
            "She nods."
            the_person "Okay, I think I can do that. I have some notes written down for things I want to tell him about."
            mc.name "Good, let's go through that list now."
            "[the_person.possessive_title] grabs a note pad from her bed stand and starts reading through it."
            "You help her organise her notes and prepare for the interview."
            the_person "I think I'm ready, now I just have to wait and try not to worry too much."
            the_person "Thank you for the help sweetheart."
            "She leans over and gives you a hug, followed by a kiss on the cheek."
            mc.name "No problem [the_person.title]. Let me know how it goes, okay?"
            $ the_person.event_triggers_dict["mom_work_promotion_two_tactic"] = "professional"


    the_person "I'll tell you as soon as I find out."
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
        the_person "[the_person.mc_title], I have some good news!"
        mc.name "Let me guess. You got your promotion?"
        the_person "Kind of. I had a fantastic interview with my superior and I think we really made a connection."
        the_person "He told me that the committee had already made their pick, so there wasn't really any chance I was going to get the promotion."
        the_person "But he did tell me that there was a position in his department as his personal technical assistant."
        the_person "He offered me the job right there! It's not much of a pay raise, but the hours are more flexible and the work should be easier."
        mc.name "That's fantastic [the_person.title]. I knew it would all work out."
        if the_person.event_triggers_dict.get("mom_work_promotion_two_tactic", "none") == "friendly":
            the_person "You were right about being friendly. He said he was really excited for us to be working together."
            the_person "I almost think he gave me the job just to spend more time with me."

        elif the_person.event_triggers_dict.get("mom_work_promotion_outfit_slutty", False):
            the_person "You were right about being a little flirty with him. He had his eyes all over me the entire time."
            $ the_person.change_slut_temp(2) # She gets a little sluttier after using her looks to get promoted.
            the_person "I almost think he gave me the job just so he could spend more time looking at me."

        "[the_person.possessive_title] gives you a tight hug."
        the_person "Thank you so much for all of your help sweetheart. You're the best son in the whole world."
        "You hug her back. When she steps away she's still smiling ear to ear."
        $ the_person.event_triggers_dict["mom_office_slutty_level"] = 1
        $ the_person.event_triggers_dict["mom_boss_name"] = get_random_male_name()
        $ the_person.event_triggers_dict["mom_boss_last_name"] = get_random_last_name()

        $ mom_work_secretary_replacement = Action("Mom work secretary replacement", mom_work_secretary_replacement_intro_requirement, "mom_work_secretary_replacement_intro", requirement_args = [day + 7])
        $ the_person.on_talk_event_list.append(mom_work_secretary_replacement)

    else: #No promotion
        $ the_person.change_happiness(-20, add_to_log = False)
        $ the_person.draw_person(emotion = "sad")
        "[the_person.title] gives you a half-hearted smile when she sees you enter the room."
        the_person "Oh, hi [the_person.mc_title]..."
        mc.name "Hey [the_person.title]. Is something wrong?"
        the_person "I had my second round interview today, and I was told I'm not getting the position."
        mc.name "Oh, I'm sorry."
        "You give [the_person.possessive_title] a gentle hug."
        the_person "Thank you. I'll be okay."
        mc.name "I know you will [the_person.title]. They're idiots for not believing in you."
        "She let's you hold her for a few moments, then she steps back and smiles. It seems a little more sincere this time."

    $ clear_scene()
    return

label mom_work_slutty_report(the_person):
    #TODO: Called on_talk occasionally where she tells you what it's like at work with her new promotion. Exact actions depend on her outfit, Sluttiness, and how "office_slutty" she's decided to be.
    if not the_person.event_triggers_dict.get("mom_work_secretary_promotion", False):
        return # Only trigger when she's been promoted, just double check that's true.

    $ the_person.draw_person()
    "[the_person.possessive_title] smiles as you."
    the_person "Hi [the_person.mc_title], it's good to see you. It was an interesting day at work, I'm glad to be home."
    menu:
        "Ask about her day.":
            mc.name "Promotion keeping you busy?"
            $ slut_level = the_person.event_triggers_dict.get("mom_office_slutty_level", 0)
            $ random_result = renpy.random.randint(0,3)
            if slut_level == 1: #Just took her promotion and was asked to be a little slutty
                if random_result == 0: # A) Catches her boss watching her as she's collecting some documents.
                    the_person "There's a lot to learn, but my new boss seems keen to help."
                    the_person "Very keen, sometimes... I think he spent most of the day staring at my butt while I was sorting documents."
                    the_person "Oh well, there's no harm if he's just looking."
                elif random_result == 1: # B) Boss gropes her ass while they're talking about a report.
                    the_person "It is, but I'm getting the hang of it. My boss, on the other hand..."
                    the_person "He's a little handsy with me, if you know what I mean. Today I was walking him through a report and..."
                    the_person "Well, he put his hand on my butt while we were talking."
                    the_person "I didn't say anything, obviously. I know that's part of the reason he hired me, it's just a little suprising."
                    the_person "Oh well, there's no harm in it."
                elif random_result == 2: # C) She overhears some rumours in the office of her being even _sluttier_ than she is.
                    the_person "It is. I'm having a hard time fitting in with the department."
                    the_person "Today I overheard some talk at the water cooler that the boss was fucking me, and that's why I got the promotion."
                    the_person "Oh well, it's just a silly office rumour."
                else: # D) "Accidentally" drops something and has to bend over to pick it up, sticking her ass in her bosses face.
                    the_person "It is, but I'm enjoying myself. My boss does a great job keeping everything friendly and casual."
                    the_person "I overheard my boss talking on the phone with a friend. He mentioned my butt and said I was looking fantastic."
                    the_person "So when I went in to give him the end of day report I \"accidentally\" dropped it and had to pick it up in front of him."
                    the_person "He sure got a good look of my butt then! He was smiling for the rest of the day!"

            elif slut_level == 2: # If she's at the blowjob phase
                if random_result == 0: # E) Gives her boss a blowjob when he was unhappy with his lunch order
                    the_person "My boss certainly is! He's so moody these days, one moment he's sealing a big deal and laughing, the next he's having a breakdown."
                    the_person "Today I brought him his lunch during a phone meeting. I guess I got something wrong, because he started complaining."
                    if the_person.effective_sluttiness("sucking_cock") > the_person.love: #She doesn't care about you enough to hide what she's doing #TODO: This should also consider if she's in a comitted relationship with you
                        the_person "But I wasn't going to be having any of that! I closed the door, got down on my knees, and unzipped his pants."
                        the_person "He finished up with that phone call so fast! That wasn't the only thing that finished quickly..."
                        the_person "He wasn't complaining about his food after that, but I hope he doesn't start expecting that all the time!"
                    else:
                        the_person "But I wasn't going to have any of that! I closed the door, got down in front of him, and... Ehm..."
                        "She stops and blushes, looking away from you."
                        the_person "Sorry, maybe I shouldn't be talking about this with you. I made sure he was happy, that's all."

                elif random_result == 1: # F) Shows her tits to Boss while he was talking about hiring "someone younger"
                    the_person "It is, but not how I expected! I caught my boss today looking at resumes!"
                    the_person "He said it was for an clerk position, but I think he might have been looking people to replace me."
                    the_person "It was certainly all younger women he was looking at. I had to nip that in the bud!"
                    the_person "When I had a chance I got the girls out..."
                    "She puffs out her chest and wiggles her shoulders, emphasising her tits  with a jiggle."
                    the_person "... to remind him why he keeps me around. I think that set him straight!"

                elif random_result == 2: # G) Showed her tits to help secure a big deal for her boss.
                    the_person "It is, but I feel like I'm making a difference for the office."
                    the_person "My boss had a meeting with a big rival today, apparently things were tense between them."
                    the_person "He had me get some drinks for the two of them. The other guy made a comment about my breasts as I was coming back in."
                    the_person "He looked like he was going to faint when he noticed me! Well, I wanted to help so I told them it wasn't any problem and got my tits out."
                    the_person "I gave them a good look, and we all had a good laugh about it. When I left they were talking business again and they sounded like old friends!"
                    the_person "They made a deal later that day, and my boss said it was all because of me!"
                    the_person "I would have never done that when I was younger, but now I'm seeing all the different ways I can help out the team."

                else: # H) Got felt up by a business associate during a meeting.
                    the_person "Oh, it's not so bad. Most of the time I just stand around and hand out reports at meetings."
                    the_person "Today was more interesting than most. I was sat beside one of the junior assistants, and this one couldn't keep his hands to himself."
                    the_person "All meeting he was brushing his hand against my thigh, touching my arm when I handed him stuff, that sort of thing."
                    the_person "He seemed so nervous, like I was going to bite his hand off!"
                    the_person "I couldn't let the poor kid worry like that, so I took his hand under the desk and put it between my legs."
                    the_person "The look on his face! He felt me up a little, but I don't think he thought he'd get that far."
                    the_person "I told him later that I didn't mind, but he'd get in trouble if he tried that with any of the other office girls."
                    the_person "He seemed to learn his lesson, and it made the meeting much more interesting!"

        "Talk about something else.":
            pass #ie just talk to her normally

    #TODO: More levels as her story advances, especially if you don't blackmail her boss.
    call talk_person(the_person) from _call_talk_person_21
    return

label mom_work_secretary_replacement_intro(the_person): #TODO: Set up as an on_talk added by her "promotion", triggers some time after she's recieved her promotion (if she has been, maybe a way to re-trigger the event?).
    #TODO: Event where Mom is worried that her boss is going to hire a new secretary and replace her.
    the_person "Oh, hi [the_person.mc_title]. Say, can I have your opinion on something?"
    mc.name "Sure [the_person.title], what is it?"
    the_person "It's about my boss. I've been happy with my new role in the company, and I think he has been too, but..."
    the_person "Well, he's a man with a wandering eye, and I know part of the reason he hired me for the job was beause of my \"womanly charm\"."
    the_person "Today I recieved a call from a woman asking for more information about an interview. I told her I didn't know anything, but something felt wrong." #NOTE: Make sure this event triggers at the end of a work day, not the start, and only on week days
    the_person "I did some snooping, and nobody knows what position that interview would have been for. I think he's trying to replace me!"
    the_person "You had such good instincts last time, I was hoping you would know what I should do now."
    the_person "I don't want to be replaced, but I don't know what I can do about it!"
    menu:
        "Seduce your boss.":
            $ the_person.event_triggers_dict["mom_replacement_approach"] = "seduce"
            mc.name "I think the answer here is pretty clear."
            the_person "You do? It is?"
            mc.name "Well, yeah [the_person.title]. Your boss hired you with certain expectations, and you aren't living up to them."
            mc.name "If you want to keep your job, you're going to have to start putting out."
            the_person "Do you mean I should have sex with him? [the_person.mc_title], I couldn't do that! I'm not a prostitute!"
            mc.name "You don't nessesarily need to start fucking him, but I'm sure there are other things you could do that would convince him to keep you around."
            mc.name "If you give him a blowjob every now and then I'm positive he'll stop trying to replace you."
            the_person "I... I shouldn't do that though..."
            mc.name "Then just show him your tits [the_person.title]. You're going to have to do something if you don't want to get replaced by someone younger and hotter!"
            "She frowns, but after a moment of thought nods in agreement."
            the_person "You're right, of course. I knew what he wanted the moment we went on that lunch date..."
            the_person "Fine, I'll do what I have to do... I just hope I'm able to convince him."
            menu:
                "You need to practice.":
                    mc.name "You should practice first. You might only have one chance."
                    the_person "That's a good idea, would you... be able to help me?"
                    mc.name "Of course [the_person.title], I'm always here to help."
                    menu:
                        "Give me a blowjob.":
                            $ the_person.event_triggers_dict["mom_replacement_seduce_practice"] = "blowjob"
                            "You unzip your pants and start to pull it down."
                            mc.name "Are you ready?"
                            $ taboo_path = False
                            if the_person.has_taboo("sucking_cock"): #Taboo break stuff
                                the_person "[the_person.mc_title], what are you doing? I thought I was just going to show him my breasts!"
                                mc.name "Maybe that would work, but are you willing to take the risk?"
                                mc.name "If you're going to do I think you need to commit."
                                the_person "But I can't practice... That... with you!"
                                mc.name "Who else would you go to? Is there anyone you trust more than me?"
                                "You pull your pants down low enough that your hard cock springs free. [the_person.possessive_title] looks at it, momentarily transfixed."
                                the_person "I... I shouldn't... We shouldn't be intimite like that..."
                                mc.name "This isn't about intimacy [the_person.title], it's about keeping your job."
                                mc.name "Just relax and pretend I'm not your son."
                                "You take her hand and bring it to your cock. She brushes her fingers over it as she considers."
                                "After a long moment she makes her decision and wraps her fingers around your shaft."
                                the_person "Alright, I trust you [the_person.mc_title]. This is just so I can practice though."
                                $ the_person.draw_person(position = "blowjob")
                                "She sinks to her knees in front of you, glances around quickly to make sure you are still alone, and then leans in."
                                "[the_person.possessive_title] kisses the tip experimentally, then parts her lips and begins to suck it."
                                $ taboo_path = True
                            else: #
                                $ the_person.draw_person(position = "blowjob")
                                "She nods and sinks to her knees."
                                the_person "Thank you for your help [the_person.mc_title]."
                                "You respond by letting your hard cock spring free and bouncing it onto her face."
                                "She kisses the tip experimentally, then parts her lips and slips it inside to suck on it."

                            call fuck_person(the_person, private = True, start_position = blowjob, skip_intro = True, position_locked = True) from _call_fuck_person_107
                            $ the_report = _return

                            if the_report.get("guy orgasms") > 0:
                                the_person "Well... I think that was a success."
                                mc.name "That was great [the_person.title]. Do that for your boss and I don't think you'll have any problems."

                            else:
                                the_person "I'm sorry, I just can't keep going [the_person.mc_title]."
                                mc.name "You'll get there [the_person.title], you just need some more practice."

                            if taboo_path:
                                the_person "I'm... glad I was able to try that with you first [the_person.title]."
                                the_person "It might not be right, but I feel safe with you. It was even kind of fun."
                                the_person "Not that we should be doing that very often, of course!"

                            else:
                                pass

                            "[the_person.possessive_title] stands up and takes a moment to tidy herself up."
                            $ the_person.outfit.restore_all_clothing()
                            $ the_person.review_outfit()
                            $ the_person.draw_person()


                        "Show me your tits.":
                            mc.name "Well then get, what are you waiting for?"
                            the_person "Right, okay then."
                            $ strip_list = the_person.outfit.get_tit_strip_list()
                            $ half_off_instead = False
                            if the_person.outfit.can_half_off_to_tits():
                                $ strip_list = the_person.outfit.get_half_off_to_tits_list()
                                $ half_off_instead = True

                            $ generalised_strip_description(the_person, strip_list, half_off_instead = half_off_instead)
                            the_person "Well, there you are..."
                            "[the_person.possessive_title] stands awkwardly in front of you, unsure of what else to do."
                            mc.name "You can't just stand there if you want to convince him, [the_person.title]."
                            menu:
                                "Shake them for me.":
                                    mc.name "Shake them around for me. You want to show off how nice they are!"
                                    the_person "Right, right..."
                                    $ the_person.draw_person(the_animation = tit_bob, animation_effect_strength = 0.3)
                                    "[the_person.possessive_title] shakes her shoulders, bouncing her tits up and down for you."
                                    mc.name "That's better. Now pretend I'm your boss. What are you going to say to me?"
                                    the_person "Oh... [the_person.mc_title], do you like my breasts? Are they... big enough for you?"
                                    mc.name "More enthusiasm."
                                    the_person "Uh... Okay, I'm just so happy to be showing you my breasts [the_person.mc_title]. I hope you like them."
                                    mc.name "Jiggle them more, and don't call them \"breasts\". Call them something sexier, like tits."
                                    $ the_person.draw_person(the_animation = tit_bob, animation_effect_strength = 0.7)
                                    "[the_person.possessive_title] puts her back into it, jiggling her tits up and down, then side to side."
                                    the_person "Mmm, do I look sexy [the_person.mc_title]? I hope you like looking at my big MILF tits!"
                                    the_person "I bet they'd look even better with your... cock between them!"
                                    mc.name "That's it! Now you've got it!"
                                    $ the_person.draw_person(the_animation = tit_bob, animation_effect_strength = 0.15)
                                    "She slows down her tit bouncing, a little out of breath from the effort."
                                    the_person "Was that good? I didn't take it too far?"
                                    mc.name "No, that's perfect! I liked it, I'm sure he will too."
                                    the_person "I just hope I can keep my job. If I can do that I'll be happy. Do you think this will work?"

                                "Titfuck me." if the_person.has_large_tits():
                                    $ the_person.event_triggers_dict["mom_replacement_seduce_practice"] = "blowjob"
                                    "You pull down your pants, and your hard cock springs free of your underwear."
                                    mc.name "You need to practice putting those to use. Show him they're more than just eye candy."
                                    the_person "Do you think I'll need to?"
                                    "You shrug."
                                    mc.name "Better to be prepared, right?"
                                    "She nods and gets onto her knees in front of you. She collects her tits up in her hands and presses them on either side of your cock."
                                    the_person "How does that feel?"
                                    "[the_person.possessive_title] gives your shaft a few slow strokes with her tits. They feel warm and soft wrapped around you."
                                    mc.name "It feels great [the_person.title], keep doing that."
                                    call fuck_person(the_person, start_position = tit_fuck, private = True, skip_intro = True, position_locked = True) from _call_fuck_person_108
                                    $ the_report = _return
                                    $ the_person.draw_person()
                                    if the_report.get("guy orgasms") > 0:
                                        the_person "Well... What do you think? Do you think this will work?"

                                    else:
                                        the_person "I'm sorry, I just can't keep going [the_person.mc_title]."
                                        mc.name "You'll get there [the_person.title], you just need some more practice."
                                        the_person "I hope so... Do you think this will work?"


                            menu:
                                "Get bigger tits.":
                                    mc.name "Well, there's one more thing you could do..."
                                    the_person "What is it? What do you think I should do?"
                                    call mom_work_secretary_replacement_intro_bigger_tits(the_person) from _call_mom_work_secretary_replacement_intro_bigger_tits
                                    $ the_person.event_triggers_dict["mom_replacement_approach_waiting_for_tits"] = the_person.tits

                                "You'll be fine.":
                                    mc.name "Yeah, I think it'll work [the_person.title]. Just be confident and remember that you have what he wants."
                            "[the_person.title] takes a moment to tidy themselves up."
                            $ the_person.outfit.restore_all_clothing()
                            $ the_person.review_outfit()
                            $ the_person.draw_person()
                            the_person "Thank you for the help [the_person.mc_title]."


                "You'll do fine.":
                    mc.name "You'll be fine [the_person.title], I think you're going to find that you're a natural."

            $ work_seduce = Action("mom_work_secretary_replacement_seduction_report", mom_work_secretary_replacement_report_requirement, "mom_work_secretary_replacement_report", requirement_args = [day+1])
            $ the_person.on_talk_event_list.append(work_seduce)


        "Get bigger tits." if the_person.tits != "FF" and not the_person.event_triggers_dict.get("getting boobjob", False):
            mc.name "Well, I have an idea..."
            the_person "I knew you would! Tell me, what do you think I should do?"
            mc.name "Your boss hired you for this job because he likes how you look, so you should give him some more to look at."
            call mom_work_secretary_replacement_intro_bigger_tits(the_person) from _call_mom_work_secretary_replacement_intro_bigger_tits_1
            $ the_person.event_triggers_dict["mom_replacement_approach"] = "tits"
            $ the_person.event_triggers_dict["mom_replacement_approach_waiting_for_tits"] = the_person.tits
            $ work_seduce = Action("mom_work_secretary_replacement_seduction_report", mom_work_secretary_replacement_report_requirement, "mom_work_secretary_replacement_report", requirement_args = [day+1])
            $ the_person.on_talk_event_list.append(work_seduce)

        "I'll take care of it.": #Same as do nothing, but gives some dialogue to point you in the right direction.
            mc.name "[the_person.title], you don't need to worry. I'm going to take care of it."
            the_person "What are you going to do?"
            mc.name "I'll try and get in touch with your boss and have a conversation with him. I'll tell him how much this position means to you."
            mc.name "I'm sure I'll be able to work out some sort of deal with him."
            "[the_person.possessive_title] smiles and pulls you into a hug."
            the_person "Oh, thank you [the_person.mc_title]. I knew you would be able to help somehow."
            mc.name "No problem [the_person.title]. You just relax and leave it to me."
            "She gives you one last squeeze, then lets you go."
            $ the_person.event_triggers_dict["mom_promotion_boss_phase_one"] = True
            #TODO: An action where you come back and tell her she has no choice but to seduce him/get larger tits when talking to him fails

        "Do nothing.":  #Do nothing, and imply she's on her own to figure this out.
            mc.name "That's a tough situation [the_person.title], but I don't think there's much you can do."
            mc.name "Just keep doing your best, I'm sure your dedication and enthusiasm will convince him."
            the_person "I hope you're right..." #If she doesn't do anything the quest fizzles out (For now, at least)
            $ the_person.event_triggers_dict["mom_promotion_boss_phase_one"] = True

    call talk_person(the_person) from _call_talk_person_22
    return

label mom_work_secretary_replacement_intro_bigger_tits(the_person): #Breakout for telling her she needs to get bigger tits and for setting up related actions/events
    mc.name "Plastic surgery has come a long way, and breast implants can look almost exactly like the real things."
    the_person "You think I need to get... fake boobs?"
    if the_person.has_large_tits():
        "She puts an arm under her breasts and lifts them up for emphasis."
        the_person "You don't think these are big enough?"
        mc.name "They're nice, but most men agree that bigger is always better."
    else:
        "She looks down at her chest and nods."
        the_person "I suppose they could be larger..."
    mc.name "It's not just about the size, it'll show him just how committed you are to the position."
    "[the_person.possessive_title] thinks about it for a long moment, then nods."
    the_person "I think I could do that, but... Where would I get the money for the procedure?"
    the_person "We're having trouble getting by as it is!"
    call mom_work_secretary_replacement_bigger_tits_options(the_person) from _call_mom_work_secretary_replacement_bigger_tits_options
    return

label mom_work_secretary_replacement_bigger_tits_reintro(the_person):
    if the_person.event_triggers_dict.get("mom_promotion_boss_phase_one_failed_intro", False):
        $ the_person.event_triggers_dict["mom_promotion_boss_phase_one_failed_intro"] = False
        $ the_person.event_triggers_dict["mom_replacement_approach"] = "tits"
        mc.name "I talked to your boss [the_person.title]."
        the_person "You did? Well, what did he say? I was probably just being paranoid, right?"
        mc.name "No, you weren't. He's looking for a replacement."
        the_person "He is? Oh no [the_person.mc_title], what am I going to do!"
        mc.name "Well, I think I have an idea..."
        the_person "Well, what is it?"
        mc.name "You need to make sure he wants to keep you around, even if it's just to look at you."
        call mom_work_secretary_replacement_intro_bigger_tits(the_person) from _call_mom_work_secretary_replacement_intro_bigger_tits_2

    else:
        mc.name "Are you still looking for a way to convince your boss to keep you around?"
        "[the_person.title] nods."
        mc.name "I think larger breasts are the way to go."
        the_person "But we don't have much spare money right now [the_person.mc_title], how would I afford it?"
        call mom_work_secretary_replacement_bigger_tits_options(the_person) from _call_mom_work_secretary_replacement_bigger_tits_options_1
    call talk_person(the_person) from _call_talk_person_23
    return

label mom_work_secretary_replacement_bigger_tits_options(the_person):
    menu:
        "I'll pay.\n-$7000" if mc.business.funds >= 7000: #NOTE: Requirements not needed, you can come back and pay in a few days.
            mc.name "I'll pay for it [the_person.title]."
            the_person "I can't let you do that for me [the_person.mc_title]! It would be so expensive!"
            mc.name "Don't worry about the cost, business is good right now and i want to give back a little."
            mc.name "Just let me do this for you, okay?"
            "She smiles happily and hugs you, holding you tight against her chest."
            the_person "Thank you [the_person.mc_title]. What would I do without you?"
            mc.name "Happy to help [the_person.title]."
            $ the_person.event_triggers_dict["mom_work_tit_options_reintro"] = False
            $ mc.business.funds += -7000

            $ the_person.event_triggers_dict["getting boobjob"] = True #Reset the flag so you can ask her to get _another_ boobjob.
            $ got_boobjob_action = Action("Mom Got Boobjob", mom_got_boobjob_requirement, "mom_got_boobjob_label", args = the_person, requirement_args = day + renpy.random.randint(3,6))
            $ mc.business.mandatory_crises_list.append(got_boobjob_action)

        "I'll pay.\n{color=#FF0000}Requires: $7000 (disabled)" if mc.business.funds < 7000:
            pass

        "Give her some serum." if mc.inventory.get_any_serum_count() > 0: #Note: The seduce event has already been added and is watching her breast size, so if it goes up she'll trigger it right away
            mc.name "Lucky for you my company is working on an experimental treatment that could help with this."
            mc.name "No surgery needed, no extra cost, and they'll be identical to the real thing."
            the_person "You can do that? That sounds like magic!"
            mc.name "Not magic, I'm just putting that university degree you helped me get to work."
            the_person "Okay, so what do I have to do?"
            menu:
                "Give her a dose of serum.":
                    call give_serum(the_person) from _call_give_serum_34
                    if _return:
                        "You just have to drink this."
                        "She drinks down the vial of serum quickly, then looks down at her chest."
                        mc.name "It's going to take some time, but you should see results soon."
                    else:
                        mc.name "You'll just have to drink a small amount of a special serum. I need to pick some up from the office first though."
                        the_person "I understand. Come and see me as soon as you have it, okay?"

                "Give it to her later.":
                    mc.name "You'll just have to drink a small amount of a special serum. I need to pick some up from the office first though."
                    the_person "I understand. Come and see me as soon as you have it, okay?"

            "She nods happily and pulls you into a hug, holding you against her chest."
            the_person "Thank you [the_person.mc_title]. What would I do without you?"
            mc.name "Happy to help [the_person.title]."
            $ the_person.event_triggers_dict["mom_work_tit_options_reintro"] = True

        "Give her some serum.{color=#FF0000}\nRequires: Serum Dose (disabled)"if mc.inventory.get_any_serum_count() <= 0:
            pass

        "Make her pay." if the_person.love >= 30 and the_person.obedience >= 130:
            mc.name "And we're going to have even more trouble if you lose your job!"
            mc.name "You're just going to have to find the cash somewhere. There must be something you can do, right?"
            the_person "Well... I have some money set aside for [lily.title]'s university tuiton next year..."
            mc.name "You'll be able to replace it soon enough, as long you don't get fired."
            "[the_person.possessive_title] scowls and thinks for a long moment. Finally she sighs and nods."
            the_person "Okay, I'll do it [the_person.mc_title]. You're right, it's important."
            $ the_person.event_triggers_dict["mom_work_tit_options_reintro"] = False
            $ the_person.event_triggers_dict["getting boobjob"] = True #Reset the flag so you can ask her to get _another_ boobjob.
            $ got_boobjob_action = Action("Mom Got Boobjob", mom_got_boobjob_requirement, "mom_got_boobjob_label", args = the_person, requirement_args = day + renpy.random.randint(3,6))
            $ mc.business.mandatory_crises_list.append(got_boobjob_action)
            pass

        "Make her pay.\n{color=#FF0000}Requires: 30 Love, 130 Obedience (disabled)" if the_person.love < 30 or the_person.obedience < 130:
            pass

        "I don't know.":
            mc.name "That's tough [the_person.title], I don't know what to do about that."
            "She frowns and nods."
            the_person "I'll think about it, okay? If you have any thoughts on what I can do let me know."
            $ the_person.event_triggers_dict["mom_work_tit_options_reintro"] = True
    return

label mom_work_secretary_replacement_report(the_person):
    $ the_solution = the_person.event_triggers_dict.get("mom_replacement_approach", "seduce")
    $ the_person.change_happiness(20, add_to_log = False)
    $ the_person.event_triggers_dict["mom_work_tit_options_reintro"] = False #No more reintro for this event
    "[the_person.possessive_title] is smiling happily when you step close to her."
    mc.name "You look happy [the_person.title]. Did you get some good news?"
    if the_solution == "seduce": #She seduced him and gave him a blowjob/titfuck.
        the_person "I did! I had a talk with my boss, just like you suggested, and..."
        "She trails off and shrugs."
        mc.name "And? What happend?"
        the_person "And I... convinced him that he should keep me around. He promised he would stop looking for a new secretary."
        menu:
            "Congradulate her.":
                mc.name "Hey, that's great! Good job [the_person.title], I knew you could do it."
                the_person "Thank you [the_person.mc_title]. It's a huge weight off of my shoulders, that's for sure."
                the_person "Now, did you want to talk about something?"

            "Ask how she did it.":
                mc.name "That's great! So, how did you do it?"
                the_person "Well, I... Are you sure you want me to tell you this? Oh, I guess it's not a big deal."
                the_person "I asked to have a discussion with him in his office during lunch today."
                the_person "He wasn't happy about having his lunch interrupted, but he seemed much more interested when I took my top off."
                mc.name "Mmhm? Go on."
                the_person "Once I had his attention I told him I knew he was looking for my replacement. He asked me what I was going to do about it."
                "She blushes a little and shrugs innocently."
                if the_person.event_triggers_dict.get("mom_replacement_seduce_practice", "titfuck") == "titfuck":
                    the_person "So I got onto my knees and used my breasts to... pleasure him, just like we practiced."
                elif the_person.event_triggers_dict.get("mom_replacement_seduce_practice", "titfuck") == "blowjob":
                    the_person "So I got onto my knees and used my mouth to... pleasure him, just like we practiced."
                else:
                    the_person "So I got onto my knees and used my mouth to... pleasure him."
                the_person "When he, um... {i}finished{/i}, he said I didn't have to worry about my job as long as I could keep up with my duties."
                the_person "Thank you for your help [the_person.mc_title], I don't think I would have had the courage to do this if it wasn't for you."
                mc.name "My pleasure [the_person.title], I'm just happy that you're doing what you enjoy."
                "She smiles and gives you a quick hug."
                the_person "Now, did you want to talk to me about something?"

    elif the_solution == "tits":
        the_person "I did! My boss noticed my... improvements as soon as I came into work today."
        the_person "When I brought him his lunch order he asked me why I got them."
        "She smiles and laughs, almost a giggle."
        the_person "I told him I got them for him, and he nearly fell out of his chair!"
        the_person "He wanted to see them, so I gave him a quick peek. I don't think I have anything to worry about now."
        the_person "Thank you [the_person.mc_title], your advice was perfect!"
        mc.name "My pleasure [the_person.title], I'm just happy to know you're doing what you love."
        the_person "I'm sure you don't mind that your mommy has even bigger tits now, either."
        if the_person.get_opinion_score("showing her tits") > 0:
            the_person "Would you like it if I got them even bigger? I'm really thinking about it now."
        "She puts an arm under her breasts and bounces them up and down."
        the_person "Anyways, did you have something you wanted to talk to me about?"

    else:
        pass #Shouldn't be possible

    $ the_person.event_triggers_dict["mom_office_slutty_level"] = 2
    call talk_person(the_person) from _call_talk_person_24
    return



label mom_weekly_pay_lily_question(the_person):
    if the_person.event_triggers_dict.get("mom_instathot_questioned", False):
        the_person "Before we talk about that, do can I ask you a question?"
        mc.name "Sure, what do you want to know?"
        the_person "Well, it's your sister again. She had more money to help with the bills, but she still won't tell me where it's from."
        the_person "I know I said I wouldn't pry, but the only times she leaves the house is to go to class."
        the_person "I just really want to be sure she's not in some sort of trouble."
    else:
        the_person "Oh, before we talk about that I'm hoping you can answer something for me."
        mc.name "Okay, what do you need to know?"
        the_person "Your sister was very strange just now. She actually offered to help with the bills."
        the_person "She wouldn't tell me where she's getting this money though."
        the_person "I respect her privacy, but I want to make sure she isn't getting into any trouble."
        $ the_person.event_triggers_dict["mom_instathot_questioned"] = True

    menu:
        "Cover for [lily.title].":
            if the_person.event_triggers_dict.get("mom_instathot_questioned", False):
                mc.name "She's working on campus, so I guess she's working between classes."
                the_person "I just wish she would trust me."
                mc.name "I'm sure she'll tell you eventually, but you don't need to worry about her."
                the_person "I hope she does. Thank you [the_person.mc_title]."

            else:
                mc.name "Uh... No, she isn't getting into any trouble. I think she's just got a job on campus."
                the_person "Really? Why wouldn't she tell me about that, I'm so proud of her!"
                mc.name "I don't know, maybe she didn't want you to think she's doing it just because we need money."
                the_person "Well, I'll let her tell me when she's ready. I'm just happy to know it's nothing to worry about."

        "Tell her about InstaPic.":
            mc.name "Well, I think she's picked up a part time job."
            the_person "Oh, why haven't I heard about this?"
            mc.name "It's not exactly a traditional job. She's been putting picture up on InstaPic."
            the_person "InstaPic? Isn't that an internet thing? I don't understand."
            mc.name "[lily.title] puts up pictures showing off clothing, and InstaPic pays her for the ad traffic she generates."
            the_person "So it's like modeling, but she can do it from home?"
            mc.name "I guess so, yeah. She's just worried that you wouldn't approve."
            the_person "Why wouldn't I? Models can be very successful. And there are no photographers or agents to take advantage of her."
            the_person "I'm going to tell her how proud I am of her. Maybe she'll even let her Mom take a few photos with her."
            "She laughs and shrugs."
            the_person "Never mind, nobody's interested in looking at someone old like me."
            mc.name "You should absolutely ask [lily.title] to take some pictures with you. I think you'd be surprised."
            the_person "Aww, you're too sweet."
            $ lily.event_triggers_dict["sister_instathot_mom_knows"] = True
            $ sister_instapic_discover_crisis = Action("sister insta mom reveal", sister_instapic_discover_requirement, "sister_instathot_mom_discover", args = lily, requirement_args = lily)
            $ mc.business.mandatory_crises_list.append(sister_instapic_discover_crisis)
    return

label mom_stress_relief_offer(the_person): #TODO: Write and hook this up.
    #TODO: Mom sees that you're "stressed" - maybe triggered by going to work too many days in a row without doing something else - and offers to help "relieve" you.
    #TODO: What she offers to do depends on her sluttiness.
    return

label mom_date_intercept(the_mom, the_date): #TODO: Add some relationship awareness to Mom so she can coment on you dating multiple girls, ect.
    #Triggers when you've got a date planned with a girl, but Mom has high Love.
    #TODO: Write a Mom specific movie date. Maybe mirror the LR1 event and have Lily join in sometimes.

    "You're getting ready for your date with [the_date.title] when you hear a knock at your door."
    the_mom "Knock knock. Are you in there [the_mom.mc_title]?"
    mc.name "Yeah, come on in [the_mom.title]."
    $ the_mom.draw_person()
    "[the_mom.possessive_title] steps into your room and closes the door behind her."
    the_mom "Oh, you're looking very handsome tonight. Is there some special occasion?"
    if the_date.has_role(girlfriend_role):
        mc.name "I'm taking [the_date.title] on a date tonight."
    else:
        mc.name "I'm going out on a date tonight."

    if the_mom.love > 70 and the_mom.effective_sluttiness() > 60: #High slut, she offers to fuck you (with slut bonus) if you stay at home
        if the_mom.get_opinion_score("not wearing anything") > 0 or the_mom.get_opinion_score("lingerie") < 0:
            the_mom "You are? Oh [the_mom.mc_title]..."
            $ strip_list = the_mom.outfit.get_full_strip_list()
            if strip_list:
                $ first_item = strip_list[0]
                $ the_mom.draw_animated_removal(first_item)
                "[the_mom.possessive_title] grabs her [first_item.display_name] and pulls it off."
                $ strip_list.remove(first_item)
            else:
                "[the_mom.possessive_title] spreads her legs, displaying her naked body for you."

            mc.name "[the_mom.title], what are you doing?"
            the_mom "Convincing you to stay home tonight."
            $ generalised_strip_description(the_mom, strip_list)

        else:
            the_mom "You are? I... Don't go anywhere, okay? I'll be right back."
            $ clear_scene()
            "Before you can ask her any questions she's hurried out of your room."
            "You shrug and go back to preparing for your date. A few short minutes later [the_mom.possessive_title] steps back into your room."
            $ the_mom.apply_outfit(lingerie_wardrobe.get_random_appropriate_outfit(the_mom.sluttiness + 20, 0 + (the_mom.sluttiness/2), guarantee_output = True), update_taboo = True)
            $ the_mom.draw_person()
            the_mom "[the_mom.mc_title], are you still sure you want to go out and see some other girl?"
            mc.name "[the_mom.title], what are you doing?"
            the_mom "Convincing you to stay home tonight."

        the_mom "What are you expecting this girl to do for you that I can't? You know nobody will ever love you like your mother."
        the_mom "You're a man now, which means you have different needs, but I still want to be the one to take care of you."
        "She steps close to you and cups your crotch, rubbing your already-hard cock through your pants."
        the_mom "Let me take care of you. Stay home tonight."
        menu:
            "Cancel your date with [the_date.title].":
                mc.name "[the_mom.title]... You know you're the most important woman in my life. I'll call [the_date.title] and cancel."
                $ the_mom.change_happiness(10)
                $ the_mom.change_love(2)
                $ the_mom.change_slut_temp(2)
                "[the_mom.possessive_title]'s face lights up."
                the_mom "Thank you [the_mom.mc_title], you're making the right decision. We're going to have such a wonderful time togther."
                mc.name "Just give me a moment, okay? She's probably not going to be happy about this."
                $ skip_intro = False
                $ start_position = None
                $ skip_condom = False
                if the_mom.get_opinion_score("giving blowjobs") > the_mom.get_opinion_score("vaginal_sex") or the_mom.effective_sluttiness("vaginal_sex") < 70:
                    $ the_mom.draw_person(position = "kneeling1")
                    "[the_mom.possessive_title] drops to her knees in front of you."
                    the_mom "I'll be quiet. Go ahead, I'm going to get you warmed up and show you just how thankful I am!"
                    "You get your phone out while [the_mom.title] pulls down your pants. Your hard cock bounces against her face when it springs free of your underwear."
                    the_mom "Oh! Sorry, sorry..."
                    "You call [the_date.title] as [the_mom.possessive_title] starts to lick at your shaft."
                    $ the_mom.draw_person(position = "blowjob", special_modifier = "blowjob", the_animation = blowjob_bob, animation_effect_strength = 0.3)
                    the_date "Hello?"
                    mc.name "Hey [the_date.title], it's [the_date.mc_title]."
                    the_date "Hey [the_date.mc_title], I was just about to head out the door. Is everything okay?"
                    mc.name "Well, I hate to tell you this so late, but..."
                    "[the_mom.possessive_title] looks up at you from her knees, your cock bulging out one cheek."
                    mc.name "Something important has come up, and it needs to be taken care of. I won't be able to go out tonight."
                    $ the_mom.change_love(4)
                    $ the_mom.change_slut_temp(3)
                    "[the_mom.title]'s eyes light up, and she bobs her head up and down on your shaft happily. You have to stiffle a moan."
                    the_date "Oh no, is everyone okay?"
                    $ the_date.change_happiness(-20)
                    $ the_date.change_love(-3)
                    "[the_date.possessive_title]'s disappointment is clear, even over the phone."
                    mc.name "It's a family situation, I'm sorry that I can't say any more."
                    "[the_mom.possessive_title] sucks gently on the tip of your cock."
                    the_date "Okay, well... I hope you get that resolved. Let's try and reschedule, okay?"
                    mc.name "Yeah, I'll be in touch. Thanks for understanding [the_date.title]. Bye."
                    the_date "Bye..."
                    "[the_mom.possessive_title] pulls off your cock, smiling happily."
                    the_mom "Thank you [the_mom.mc_title]. I'm the only woman you'll ever need in your life."
                    "With that she slides you back into her warm, wet mouth and continues to suck you off."
                    $ skip_intro = True
                    $ start_position = blowjob

                else:
                    the_mom "I'll just be over here, ready for you..."
                    "[the_mom.title] climbs onto your bed, face down and ass up, while she waits for you."
                    mc.name "Hey [the_date.title], it's [the_date.mc_title]."
                    the_date "Hey [the_date.mc_title], I was just about to head out the door. Is everything okay?"
                    if not the_mom.outfit.vagina_available():
                        $ strip_list = the_mom.outfit.get_half_off_to_vagina_list()
                        if strip_list:
                            $ generalised_strip_description(the_mom, strip_list, position = "doggy", half_off_instead = True)
                        else:
                            $ strip_list = the_mom.outfit.get_full_strip_list()
                            $ generalised_strip_description(the_mom, strip_list, position = "doggy")
                    "You're distracted as [the_mom.possessive_title] reaches back and jiggles her butt for you."
                    the_date "[the_date.mc_title]? Are you there?"
                    mc.name "Uh, yeah. Sorry, I hate to tell you this so late, but something important has come out."
                    mc.name "I'm not going to be able to make it for our date tonight."
                    the_date "Oh no, is everyone okay?"
                    $ the_date.change_happiness(-20)
                    $ the_date.change_love(-3)
                    "[the_mom.title] grabs one ass cheek and pulls it to the side, giving you a clear view of her pretty pink pussy."
                    menu:
                        "Fuck [the_mom.title]'s pussy right away.":
                            "You unzip your pants and step clsoer to [the_mom.possessive_title]."
                            mc.name "It's my Mom, she really needs me close right now."
                            "You grab [the_mom.title]'s hips with your free hand and hold her steady as you slide your cock into her wet pussy. You fuck her slowly while you talk."
                            $ the_mom.draw_person(position = "doggy", the_animation = blowjob_bob, animation_effect_strength = 0.3)
                            mc.name "I can't really say any more than that right now. I'm sorry."
                            the_date "I understand, I hope everything works out. Let's try and resechedule some time soon, okay?"
                            "[the_mom.possessive_title] grabs one of your pillows to muffle her moans with."
                            mc.name "Yeah, I'll be in touch. Thanks for understanding [the_date.title]. Bye."
                            the_date "Bye..."
                            if the_mom.has_taboo("condomless_sex"):
                                the_mom "[the_mom.mc_title], did you put on a condom?"
                                mc.name "Nope. [the_date.title] doesn't like condoms."
                                the_mom "Then... I'll give you everything she could give you! I don't care if you fuck my pussy unprotected [the_mom.mc_title]!"
                                $ the_mom.break_taboo("condomless_sex")
                            else:
                                "As soon as you put your phone down [the_mom.title] starts to moans loudly."
                                the_mom "Oh [the_mom.mc_title], that feels amazing!"
                            $ skip_intro = True
                            $ start_position = doggy
                            $ skip_condom = True


                        "Wait until you're off the phone.":
                            "You place a hand on [the_mom.possessive_title]'s butt and squeeze it idly as you talk."
                            mc.name "It's my Mom, she really needs me close right now."
                            mc.name "I can't really say any more than that right now. I'm sorry."
                            the_date "I understand, I hope everything works out. Let's try and resechedule some time soon, okay?"
                            "[the_mom.possessive_title] puts a hand between her legs and starts to massage her clit while you're talking."
                            mc.name "Yeah, I'll be in touch. Thanks for understanding [the_date.title]. Bye."
                            the_date "Bye..."


                $ the_mom.add_situational_slut("Eager", 10, "I'll show that skank how a {i}real{/i} woman should treat him!")
                call fuck_person(the_mom, private = True, skip_intro = skip_intro, start_position = start_position, skip_condom = skip_condom) from _call_fuck_person_36
                $ report = _return
                $ the_mom.clear_situational_slut("Eager")
                if the_report.get("guy orgasms", 0) > 0:
                    the_mom "Ah... Well, wasn't that better than anything that girl would have done?"
                    mc.name "That was great [the_mom.title]."
                    $ the_mom.change_happiness(10)
                    the_mom "Anything for my special man."
                else:
                    the_mom "I'm sorry [the_mom.mc_title], I just don't have the energy I use to have..."
                    mc.name "It's okay [the_mom.title], maybe later we can finish this up."
                    $ the_mom.change_happiness(-5)
                    the_mom "I'll do my best. For my special man I'll try anything at all."

                the_mom "Now, would you like to watch some TV with me? I'll get us some snacks, we can spend the whole night together."
                mc.name "Sounds good [the_mom.title]."
                $ the_mom.change_love(1 + mc.charisma)
                "You spend the rest of the evening with [the_mom.possessive_title], sitting on the couch, watching TV, and chatting."
                #TODO: Add a proper Mom date that this leads into

            "Tell her no.":
                mc.name "Sorry [the_mom.title], but I just can't cancel my plans this suddenly."
                mc.name "I need to get going."
                if the_mom.love > 80:
                    "You hurry to the door, but [the_mom.possessive_title] grabs your arm."
                    the_mom "Wait! How about about just a quicky? You can tell her you're running late."
                    the_mom "I want to take all of your cum, so she doesn't get any. Can you give me that, at least?"
                    menu:
                        "Fuck [the_mom.title] before your date.":
                            "You sigh, then nod."
                            mc.name "Fine, but we need to make it quick."
                            $ the_mom.change_love(1)
                            $ the_mom.change_slut_temp(1)
                            "She nods happly."
                            $ the_mom.add_situational_slut("Eager", 20, "I need to drain those balls before that skank touches him!")
                            call fuck_person(the_mom, private = True) from _call_fuck_person_40
                            $ report = _return
                            $ the_mom.clear_situational_slut("Eager")
                            if the_report.get("guy orgasms", 0) > 0:
                                the_mom "Mmm, that was great [the_mom.mc_title]. Whatever happens I'll always be the first woman you come to, right?"
                                mc.name "Of course [the_mom.title]."
                                $ the_mom.change_happiness(5)
                            else:
                                the_mom "I'm sorry [the_mom.mc_title], I just don't have the energy I use to have..."
                                mc.name "It's okay [the_mom.title], maybe later we can finish this up."
                                the_mom "Maybe you do need this other girl... You should find someone who can take care of you properly."
                                $ the_mom.change_happiness(-5)

                            "You're interupted by a phone call. It's [the_date.title]."
                            mc.name "Hey [the_date.title]..."
                            the_date "[the_date.mc_title], are you on your way?"
                            mc.name "I'm just heading out the door. Something important came up, but it's taken care of. Family related."
                            $ the_date.change_happiness(-5)
                            $ the_date.change_love(-1)
                            the_date "Okay, well I'm waiting here."
                            mc.name "I'm on my way, I won't be long."
                            "You hang up and stuff your cock back into your pants."
                            the_mom "Have a good date [the_mom.mc_title]. Give me a kiss before you go."
                            "You kiss [the_mom.possessive_title], then hurry out of your room."

                        "Tell her no again.":
                            mc.name "I don't have time [the_mom.title]. I'm sorry, but I really need to go."
                            mc.name "We can spend time together later, okay?"
                            $ the_mom.change_happiness(-10)
                            $ the_mom.change_love(-2)
                            $ clear_scene()
                            "You hurry out of the room, leaving [the_mom.possessive_title] behind."
                else:
                    "You hurry out of the room, leaving [the_mom.possessive_title] behind."
                    $ the_mom.change_happiness(-10)
                    $ the_mom.change_love(-2)
                    $ clear_scene()

                return False

    elif the_mom.love > 50 and the_mom.effective_sluttiness("sucking_cock") > 40 and the_mom.get_opinion_score("giving blowjobs") >= 0: #TODO: Moderate sluttiness. She tries to convince you to stay home by offering sex (default sex system entry)
        the_mom "Oh, you are? I was hoping you would spend some time at home, I barely see you these days."
        mc.name "Sorry, but I've already made these plans. Maybe some other time, okay?"
        the_mom "[the_mom.mc_title], you aren't seeing this girl just for... physical reasons, are you?"
        mc.name "What? Why?"
        the_mom "Well, A boy your age can sometimes be thinking with his penis instead of his head."
        "She steps closer to you and puts a hand to your crotch. It twitches in response, quickly growing hard."
        the_mom "I don't want you out getting in trouble with girls if all you really need is some physical relief."
        the_mom "If you decide to stay home, maybe I can... take care of this for you?"
        mc.name "[the_mom.title], [the_date.title] won't be happy with me if I cancel last minute."
        $ the_mom.draw_person(position = "kneeling1")
        "[the_mom.possessive_title] gets onto her knees in front of you, face level with the large bulge in your pants."
        if the_mom.has_taboo("sucking_cock"):
            the_mom "Please [the_mom.mc_title]? You were probably hoping to get a blowjob from her, right? Well..."
            "She hesitates, as if she needs to be extra sure she means what she's about to say."
            the_mom "I could do that too! You wouldn't need to worry about dressing up, or paying for dinner, or even leaving the house."
            the_mom "Just stay home and I'll take better care of you than any whatever skank is trying to get her hands on you!"
        else:
            the_mom "Please [the_mom.mc_title]? If you stay you don't need to worry about dressing up or paying for dinner."
            the_mom "I'll give you a nice blowjob, then when you're finished we can watch some TV and relax."
            the_mom "Doesn't that sound so much nicer than trying to impress some skank you just met? You've known me your whole life already."

        menu:
            "Cancel your date with [the_date.title].":
                "[the_mom.possessive_title] cups your crotch and massages it gently while you think about it."
                mc.name "Fine, but she's really not going to be happy about this."
                the_mom "Don't worry about her, I'm the only woman you need in your life right now. You can worry about finding a wife when you're older."
                mc.name "Just... Give me a minute to call her, okay?"
                if the_mom.get_opinion_score("giving blowjobs") > 0 and the_mom.effective_sluttiness("sucking_cock") >= 50:
                    the_mom "I can be quiet. Go ahead, I'll just get started..."
                    "You get your phone out while [the_mom.title] pulls down your pants. Your hard cock bounces against her face when it springs free of your underwear."
                    the_mom "Oh! Sorry, sorry..."
                    "You call [the_date.title] as [the_mom.possessive_title] starts to lick at your shaft."
                    $ the_mom.draw_person(position = "blowjob", special_modifier = "blowjob", the_animation = blowjob_bob, animation_effect_strength = 0.3)
                    the_date "Hello?"
                    mc.name "Hey [the_date.title], it's [the_date.mc_title]."
                    the_date "Hey [the_date.mc_title], I was just about to head out the door. Is everything okay?"
                    mc.name "Well, I hate to tell you this so late, but..."
                    "[the_mom.possessive_title] looks up at you from her knees, your cock bulging out one cheek."
                    mc.name "Something important has come up, and it needs to be taken care of. I won't be able to go out tonight."
                    $ the_mom.change_love(4)
                    $ the_mom.change_slut_temp(3)
                    "[the_mom.title]'s eyes light up, and she bobs her head up and down on your shaft happily. You have to stiffle a moan."
                    the_date "Oh no, is everyone okay?"
                    $ the_date.change_happiness(-20)
                    $ the_date.change_love(-3)
                    "[the_date.possessive_title]'s disappointment is clear, even over the phone."
                    mc.name "It's a family situation, I'm sorry that I can't say any more."
                    "[the_mom.possessive_title] sucks gently on the tip of your cock."
                    the_date "Okay, well... I hope you get that resolved. Let's try and reschedule, okay?"
                    mc.name "Yeah, I'll be in touch. Thanks for understanding [the_date.title]. Bye."
                    the_date "Bye..."
                    "[the_mom.possessive_title] pulls off your cock, smiling happily."
                    the_mom "Thank you [the_mom.mc_title]. Now, should I keep going?"
                    "She starts to suck you off again before you even respond."

                else:
                    "[the_mom.title] nods and waits, still on her knees, while you get your phone out and call [the_date.title]."
                    the_date "Hello?"
                    mc.name "Hey [the_date.title], it's [the_date.mc_title]."
                    the_date "Hey [the_date.mc_title], I was just about to head out the door. Is everything okay?"
                    mc.name "Well, I hate to tell you this so late, but..."
                    mc.name "Something important has come up, and it needs to be taken care of. I won't be able to go out tonight."
                    "[the_mom.possessive_title]'s eyes light up, and she smiles happily at you."
                    $ the_mom.change_love(3)
                    $ the_mom.change_slut_temp(2)
                    the_date "Oh no, is everyone okay?"
                    $ the_date.change_happiness(-20)
                    $ the_date.change_love(-3)
                    "[the_date.possessive_title]'s disappointment is clear, even over the phone."
                    mc.name "It's a family situation, I'm sorry that I can't say any more."
                    the_date "Okay, well... I hope you get that resolved. Let's try and reschedule, okay?"
                    mc.name "Yeah, I'll be in touch. Thanks for understanding [the_date.title]. Bye."
                    the_date "Bye..."
                    the_mom "Thank you [the_mom.mc_title]. Now, should I take care of this?"
                    "She unzips your pants and pulls them down. Your hard cock springs free, bouncing in front of her face."
                    the_mom "Oh!"
                    if the_mom.break_taboo("sucking_cock"):
                        the_mom "It looks so much bigger when it's right in your face..."
                        "She takes a deep breath."
                        the_mom "It's fine, I can do this. Anything to make my [the_mom.mc_title] feel special and want to spend more time with me."
                    "She gives it an experimental kiss, then slips her lips over the tip."


                if not the_mom.outfit.vagina_visible() or not the_mom.outfit.tits_visible():
                    menu:
                        "Order her to strip." if the_mom.obedience >= 140:
                            mc.name "You should be dressed for the occassion first. Strip."
                            the_mom "Of course, right away [the_mom.mc_title]."
                            $ the_mom.draw_person()
                            "She stands up to get undressed."
                            $ remove_shoes = False
                            $ feet_ordered = the_mom.outfit.get_feet_ordered()
                            if feet_ordered:
                                $ top_feet = feet_ordered[-1]
                                the_mom "Do you want me to keep my [top_feet.display_name] on?"
                                menu:
                                    "Strip it all off.":
                                        mc.name "Take it all off, I don't want you to be wearing anything."
                                        the_mom "Yes [the_mc.title]. I'll get completely naked for you."
                                        $ remove_shoes = True

                                    "Leave them on.":
                                        mc.name "You can leave them on."

                            call naked_strip_description(the_mom, remove_shoes = remove_shoes) from _call_naked_strip_description_1
                            the_mom "There, now you can properly enjoy the view. Shall I get to it, then?"
                            mc.name "Go ahead."

                        "Order her to strip.\n{size=16}{color=#FF0000}Requires: 140 Obedience{/color}{/size} (disabled)" if the_mom.obedience < 140:
                            pass

                        "Enjoy your blowjob.":
                            pass

                $ the_mom.draw_person(position = "blowjob", special_modifier = "blowjob", the_animation = blowjob_bob, animation_effect_strength = 0.3)
                "You rest a hand on the top of [the_mom.possessive_title]'s head as she starts to suck on your cock. She starts slowly, but quickly picks up speed and confidence."
                mc.name "That feels great [the_mom.title]."
                "She pops off your cock for a moment and smiles up at you."
                the_mom "See? You don't need any other women in your life. I'll take care of you [the_mom.mc_title], just like I always have."
                "With that she slides you back into her mouth."
                call fuck_person(the_mom, start_position = blowjob, skip_intro = True, girl_in_charge = True, position_locked = True) from _call_fuck_person_99
                $ the_report = _return
                if the_report.get("guy orgasms", 0) > 0:
                    the_mom "Ah... Well, wasn't that better than anything that girl would have done?"
                    mc.name "That was great [the_mom.title]."
                    $ the_mom.change_happiness(10)
                    the_mom "Anything for my special man."
                else:
                    the_mom "I'm sorry [the_mom.mc_title], I just don't have the energy I use to have..."
                    mc.name "It's okay [the_mom.title], maybe later we can finish this up."
                    $ the_mom.change_happiness(-5)
                    the_mom "I'll do my best. For my special man I'll try anything at all."
                the_mom "Now, would you like to watch some TV with me? I'll get us some snacks, we can spend the whole night together."
                mc.name "Sounds good [the_mom.title]."
                $ the_mom.change_love(1 + mc.charisma)
                "You spend the rest of the evening with [the_mom.possessive_title], sitting on the couch, watching TV, and chatting."
                return True


            "Tell her no.":
                mc.name "I can't do that [the_mom.title]! I'm sorry, but I really do have to get going."
                "You leave her on her knees and hurry out of your room."
                $ the_mom.change_happiness(-5)
                $ the_mom.change_love(-1)
                return False


    elif the_mom.love > 30 and the_mom.effective_sluttiness("touching_penis") > 15 and the_mom.get_opinion_score("giving handjobs") >= 0:
        the_mom "That's nice, I'm sure you'll show her a wonderful time."
        the_mom "This girl, I assume you're interested in her... physically?"
        mc.name "I suppose so, why?"
        $ the_mom.draw_person(position = "sitting")
        "[the_mom.possessive_title] sits down on your bed and pats the spot beside her. You sit down with her to talk."
        the_mom "Well, for young men like yourself it's easy to get distracted by a girls looks."
        the_mom "It's not your fault, your hormones just take over and suddenly all you can look at are her butt and breasts!"
        mc.name "[the_mom.title], I think I'll be fine."
        "She places her hand on your upper thigh and gives it a gentle squeeze."
        the_mom "I want you to find a girl that's really right for you emotionally, not just some bimbo with nice tits."
        the_mom "The easiest way to be sure is to flush out all of those hormones first, so you can see her with a clear head."
        if the_mom.has_taboo("touching_penis"):
            the_mom "I was thinking... Well, if you wanted me to, I could, umm..."
            "[the_mom.possessive_title] blushes and looks away, struggling to finish her sentence."
            mc.name "What is it [the_mom.title]?"
            the_mom "I can help you deal with all of those hormones, if you'd like."
            the_mom "I've got a bit of experience, I can... give you a handjob?"
        else:
            the_mom "Let me help you. I'll give you a quick handjob before you go, so you aren't thinking with your penis all night."
            the_mom "You'll feel better, and I promise she'll notice how much more respectful you are."

        menu:
            "Let her \"help\" you.":
                if the_mom.has_taboo("touching_penis"):
                    mc.name "That sounds like a really good idea [the_mom.title]."
                    "She breathes a sigh of relief."
                    the_mom "Okay, well then... You just stand up and I'll take care of you."
                    the_mom "Nothing sexual here, of course. I'm just doing my motherly duty trying to help you."
                    mc.name "Of course [the_mom.title], of course."
                else:
                    mc.name "That sounds like a good idea [the_mom.title]."
                    "She smiles happily."
                    the_mom "Good, you just stand up and I'll take care of you."
                    the_mom "It's my job as your mother to do things like this, after all. I think it's more common than people say, really."

                $ the_mom.draw_person()
                "You and [the_mom.possessive_title] both stand up. She reaches down for your pants and unzips them."
                "She pulls them down, gasping softly when your hard cock springs out of your underwear."
                if the_mom.has_taboo("touching_penis"):
                    the_mom "Oh... This is just to help you, okay? There's nothing wrong with it, it's just because I love you..."
                else:
                    the_mom "Oh, you really do need this [the_mom.mc_title]. I'll take care of this for you, leave it to mommy."
                "She wraps her fingers gently around your shaft and gives it a few experimental strokes."
                if not the_mom.outfit.tits_visible() and (the_mom.effective_sluttiness(["underwear_nudity","bare_tits"]) > 25 or the_mom.get_opinion_score("showing her tits") > 0):
                    if the_mom.has_taboo(["underwear_nudity","bare_tits"]):
                        the_mom "This would probably be faster if you had some more... stimulation, right?"
                        the_mom "Let me take my breasts out... It's just to speed this along, there's nothing wrong about it."
                    else:
                        the_mom "Of course, you probably want to see mommy's tits. Let me get those out for you to look at."
                    "She lets go of your cock and steps back."
                    if the_mom.outfit.can_half_off_to_tits():
                        $ strip_list = the_mom.outfit.get_half_off_to_tits_list()
                        $ generalised_strip_description(the_mom, strip_list, half_off_instead = True)
                    else:
                        $ strip_list = the_mom.outfit.get_tit_strip_list()
                        $ generalised_strip_description(the_mom, strip_list)
                    the_mom "There, now you have something to oggle while I get you off."
                    if not the_mom.outfit.vagina_visible():
                        menu:
                            "Order her to strip completely." if the_mom.obedience >= 140:
                                mc.name "That's not enough for me. Get naked for me [the_mom.title]."
                                if the_person.has_taboo("bare_pussy"):
                                    the_mom "[the_mom.mc_title], I can't... I shouldn't do that."
                                    mc.name "Come on, I need to get off, and I need to see you naked to do that."
                                    mc.name "You're already jerking me off, it's not a big deal seeing you naked while you do it."
                                    mc.name "I'm going to be late if you keep stalling. Hurry up and get naked!"
                                    $ the_mom.change_obedience(5 + the_mom.get_opinion_score("being submissive"))
                                    "She takes a deep breath and starts to strip down."
                                else:
                                    $ the_mom.change_obedience(1 + the_mom.get_opinion_score("being submissive"))
                                    the_mom "Of course [the_mom.mc_title]. Whatever you need me to do to make you cum I'll do it."
                                $ remove_shoes = False
                                $ feet_ordered = the_mom.outfit.get_feet_ordered()
                                if feet_ordered:
                                    $ top_feet = feet_ordered[-1]
                                    the_mom "Do you want me to keep my [top_feet.display_name] on?"
                                    menu:
                                        "Strip it all off.":
                                            mc.name "Take it all off, I don't want you to be wearing anything."
                                            $ remove_shoes = True

                                        "Leave them on.":
                                            mc.name "You can leave them on."


                                call naked_strip_description(the_mom, remove_shoes = remove_shoes) from _call_naked_strip_description_2
                                if the_mom.break_taboo("bare_pussy"):
                                    the_mom "There. I guess this isn't so strange, really. Now, where were we..."
                                else:
                                    the_mom "There you go [the_mom.mc_title], now enjoy my naked body while I stroke you off."

                            "Order her to strip completely.\n{size=16}{color=#FF0000}Requires: 140 Obedience{/color}{/size} (disabled)" if the_mom.obedience < 140:
                                pass

                            "Oggle her tits.":
                                pass
                    "She wraps her fingers around your shaft again and starts to stroke it."

                else:
                    pass

                the_mom "You've got a date to keep, so cum quickly, okay?"
                call fuck_person(the_mom, start_position = handjob, skip_intro = True, girl_in_charge = True, position_locked = True) from _call_fuck_person_100
                $ the_report = _return
                if the_report.get("guy orgasms", 0) > 0:
                    the_mom "There we go [the_mom.mc_title], all taken care of. Now I don't have to worry about you getting into trouble while you're out."
                    "She gives you a happy smile."
                    $ the_mom.change_slut_temp(2)
                    $ the_mom.change_love(2)
                    the_mom "Now go on, you've got a date to keep. Have fun out there, okay?"
                    mc.name "Thanks [the_mom.title], I will."
                    "You stuff your cock back in your pants and get ready to leave."
                    the_mom "Wait, one last thing..."
                    "She hurries over to you and kisses you, deeply and passionately."
                    the_mom "Mmm... Remember, Mommy loves you and will always be here for you."
                    mc.name "I love you too [the_mom.title]. See you later."

                else:
                    the_mom "I'm sorry [the_mom.mc_title], I just don't have the energy to finish you off. I need more practice I guess."
                    "She seems rather disapointed in herself."
                    $ the_mom.change_slut_temp(1)
                    mc.name "We can work on that. Thanks for trying [the_mom.title], it was still nice."
                    "[the_mom.possessive_title] gives you a weak smile."
                    the_mom "Go on, you've got a date to keep. Have fun out there."
                $ the_mom.break_taboo("touching_penis")
                $ the_mom.update_outfit_taboos()
                $ the_mom.apply_outfit()
                "You hurry out of the house to meet [the_date.title]."
                $ clear_scene()
                return False

            "Tell her no.":
                mc.name "Sorry [the_mom.title], but I'm going to pass."
                if the_mom.has_taboo("touching_penis"):
                    the_mom "Of course! It's not right, I'm your mother and I shouldn't... How could I even suggest that!"
                    mc.name "Relax, it's fine. I don't think it's a bad idea, but I might need my energy for later tonight."
                    the_mom "Oh, I... Oh [the_mom.mc_title], please promise me you'll be safe, at the very least."
                    mc.name "I will [the_mom.title], I promise."
                    $ the_mom.change_slut_temp(2)
                    the_mom "Well, if that's what you're planning... Be sure to show her a good time. Don't be selfish, girls don't like that."
                    mc.name "Okay [the_mom.title], I'll do that."
                else:
                    mc.name "Depending on how the date goes I might need all my energy for later tonight."
                    the_mom "Oh [the_mom.mc_title], well..."
                    $ the_mom.change_slut_temp(1)
                    the_mom "In that case, be sure to show her a good time. Don't be selfish, girls don't like that."
                    mc.name "Noted, thanks [the_mom.title]."
                $ the_mom.draw_person()
                "She stands up and moves to the door."
                the_mom "Don't be out too late, I worry when I don't know where you are. Love you sweetheart."
                mc.name "Love you too [the_mom.title]."
                $ clear_scene()
                return False

    else:
        the_mom "That's nice, I'm sure you'll have a wonderful time together."
        the_mom "Don't stay out too late, and make sure you use protection if you two are going to..."
        "She blushes and shrugs."
        the_mom "You know."
        mc.name "Relax [the_mom.title], I'm not a little kid."
        the_mom "I know. Oh lord, do I know. You've grown up into such a fine man, I just... hate to think of you leaving."
        the_mom "Come here, I need a hug."
        "[the_mom.possessive_title] pulls you into her arms. She rests her head on your shoulder while you hold her."
        "You're silent for a few moments, then she steps back and holds you at arms length."
        $ the_mom.change_love(1)
        the_mom "I love you sweetheart. Have a good night."
        mc.name "I love you too [the_mom.title]. I'll see you later."
        $ clear_scene()
        return False #Returns False if the date was not intercepted.
    return False

label mom_office_person_request():
    $ the_person = mc.business.event_triggers_dict.get("mom_office_secretary", None)
    if the_person is None:
        $ the_person = create_random_person()
        $ mc.business.event_triggers_dict["mom_office_secretary"] = the_person
    #TODO: Give her a specific outfit, so she's always dressed appropriately

    $ the_person.draw_person(position = "sitting")
    "You walk up to the reception desk. The receptionist looks up at you."
    the_person "Hello, can I help you? Do you have an appointment?"
    $ ask_for_actions = ["Ask for someone"]
    $ other_actions = ["Other", "Leave"]

    $ ask_for_actions.append(mom)

    if mom.event_triggers_dict.get("mom_promotion_boss_phase_one", False) and mom.event_triggers_dict.get("mom_replacement_approach", None) is None:
        $ ask_for_actions.append([mom.title + "'s Boss","Boss"])

    call screen main_choice_display([ask_for_actions, other_actions], draw_person_previews = False, draw_hearts_for_people = False)
    if _return == "Leave":
        mc.name "Sorry to bother you."
        $ clear_scene()
    elif _return == "Boss":
        call mom_promotion_boss_phase_one(the_person) from _call_mom_promotion_boss_phase_one

    else:
        mc.name "I'm here to see Miss.[mc.last_name]. Can you let her know I'm here?"
        the_person "Of course, one moment."
        "The receptionist picks up her phone and calls someone. After a brief quiet conversation she hangs up."
        if mom_offices.has_person(mom):
            the_person "She's coming down right now to meet you."
            "After a brief wait [mom.title] steps out of the elevator banks and smiles happily at you."
            $ mom_offices.move_person(mom,mom_office_lobby)
            $ clear_scene()
            $ mom.draw_person() #TODO: Make sure she's wearing her work uniform.
            mom "Hi [mom.mc_title], did you need me for something?"
            call talk_person(mom) from _call_talk_person_25

        else:
            the_person "I'm sorry, but she doesn't seem to be in the building at the moment."
            mc.name "Right, okay. Sorry to bother you."
    return

label mom_promotion_boss_phase_one(the_secretary):
    $ mom.event_triggers_dict["mom_promotion_boss_phase_one"] = False
    $ mom.event_triggers_dict["mom_promotion_boss_phase_one_failed_intro"] = True #Triggers the reintro where you tell her she'll need to figure out another way
    $ mom.event_triggers_dict["mom_work_tit_options_reintro"] = True
    $ mom.event_triggers_dict["mom_replacement_approach"] = "tits"

    $ boss_name = mom.event_triggers_dict.get("mom_boss_name", "Vren")
    $ mom_boss_last_name = mom.event_triggers_dict.get("mom_boss_last_name", "Games")
    $ mom_boss_quick_name = "Mr."+mom_boss_last_name
    mc.name "I don't, but I was hoping to set one up. I need to speak to Mr.[mom_boss_last_name]."
    "She nods and turns to her computer briefly, typing something in before turning back to you."
    the_secretary "Okay, and who should I say is trying to reach him?"
    menu:
        "Reference your business.":
            $ business_name = mc.business.name
            mc.name "Mr.[mc.last_name]. I'm here representing [business_name]. I have work I need to discuss with him."

        "Reference [mom.title].":
            $ mom_last_name = mom.create_formatted_title(mom.last_name)
            mc.name "Mr.[mc.last_name]. I'm the son of [mom_last_name], there's a family matter I need to discuss with him."

        "Pretend you're here for a job.":
            mc.name "Mr.[mc.last_name]. I'm a recent graduate and I've heard he's hiring."
            mc.name "Just tell him I'm here for the position he's been advertising."

    "She types on her computer again."
    the_secretary "Understood. I'll need to check that he's in. Take a seat in the lobby and I'll get back to you in a moment."
    $ clear_scene()
    "She motions to a wing of seats in an alcove to your side. You walk over and sit down across from a young woman."

    $ the_wife = create_random_person(last_name = mom_boss_last_name, age = 42)
    $ the_daughter = the_wife.generate_daughter(force_live_at_home = True)
    $ the_daughter.set_schedule(mom_office_lobby, [3])
    $ the_daughter.set_schedule(university, [1,2])

    $ mom.event_triggers_dict["mom_boss_wife"] = the_wife
    $ mom.event_triggers_dict["mom_boss_daughter"] = the_daughter


    $ the_daughter.draw_person(position = "sitting")

    "You pick up a magazine from a coffee table and flip through it idly."
    the_daughter "Um, excuse me?"
    "You glance up. It's the young woman across from you talking."
    the_daughter "I just overheard, you're here to talk to [mom_boss_quick_name]?"
    mc.name "Yeah, I am."
    the_daughter "Sorry, this probably seems really strange. I'm his daughter, he's suppose to be meeting me..."
    "She checks her phone and sighs."
    the_daughter "Well, half an hour ago, actually. If, um... If you talk to him, could you let him know I'm down here?"
    the_daughter "Sorry, I know you're probably really important and I shouldn't be bothering you!"
    mc.name "No, it's fine. I'll let him know, if I'm able to see him."
    "She thanks you and sits back down. A few moments later the secretary at the front desk calls you over."
    $ the_secretary.draw_person(position = "sitting")
    the_secretary "Mr.[mc.last_name]? [mom_boss_quick_name] has five minutes to meet with you. Sixth floor, on your right."
    mc.name "Thank you."
    "You stand up and turn to the young woman in the waiting room."
    $ the_daughter.draw_person(position = "sitting")
    mc.name "I'll let your dad know. I'm sure he'll be down right after our meeting."
    "She smiles meekly and waves as you head off to the bank of lobby elevators."
    $ clear_scene()
    "You take an elevator up to the sixth floor and follow the signage to [mom_boss_quick_name]'s office."
    "The door is open as you walk up, so you knock and peek your head in."
    mom_boss_quick_name "Come on in. I don't have much time, so let's make this quick, okay?"
    "You move inside the office and nudge the door closed. [mom_boss_quick_name] is older than you expected, slightly overweight with a two hundred dollar buzz cut."
    mc.name "That suits me just fine. I need to talk to you about one of your employees."
    mc.name "Miss.[mc.last_name] works for you as your technical assistant. I think you've given her that position because you expect something from her."
    "[mom_boss_quick_name] cocks an eyebrow, taking you seriously for the first time."
    mom_boss_quick_name "Are you her lawyer, or something? You look a little young for this kid. What was your name again?"
    mc.name "[mc.name] [mc.last_name]. Ring any bells?"
    mom_boss_quick_name "[mc.last_name]... Wait, you aren't... Shit, so you're that kid she's always talking about."
    mc.name "Yeah, I'm that kid."
    mom_boss_quick_name "Well listen kid, I don't know what you want to hear. I haven't done anything wrong, it's all just business."
    mom_boss_quick_name "So what are you here for?"
    menu:
        "I want to help you.":
            mc.name "I want to help."
            mom_boss_quick_name "I... What? Help with what? This is is a wierd way to ask for a job, kid."
            mc.name "Not with your work, I want to help you with my Mom."
            mc.name "I know you hired her because she's a good looking woman, but I bet you want to do more than just look at her."
            mom_boss_quick_name "Jesus kid, it sounds like you actually want me to fuck your mom. Why the hell would you want that?"
            mc.name "You don't need to know why, but I think we could work together."
            "He thinks for a moment, one arm planted on his desk. After a moment he chuckles and shakes his head."
            mom_boss_quick_name "This is too wierd for me. I don't know what your game is, and I don't like not knowing."
            mom_boss_quick_name "Maybe I'll take your old lady for a ride - I'd like to see those tits jiggling, that's for sure."
            mom_boss_quick_name "But I don't want to be part of whatever wierd sex thing you're setting me up for. No way."


        "I want you to back off.":
            mc.name "I want you to back off. I don't want you using her job as a way to manipulate her."
            mom_boss_quick_name "So that's it, huh? Worried your mom is going to have to fuck her way up the corporate ladder?"
            mom_boss_quick_name "Frankly kid, you don't have much leverage here. I haven't done anything, and even if I had..."
            mom_boss_quick_name "Well, it ain't illegal to chase a little tail. What are you going to do to convince me?"
            menu:
                "I'll get you someone else.":
                    mc.name "If all you want is a pretty girl to fuck around the office I can find you someone else."
                    mom_boss_quick_name "You can, huh? And how are you going to do that, exactly?"
                    mc.name "Let's just say I have a way with women."
                    "He shakes his head and scoffs."
                    mom_boss_quick_name "Yeah, I'm sure you do kid. Alright, I think I've entertained this long enough."

                "I'll pay you.":
                    mc.name "I can pay you."
                    mom_boss_quick_name "You want to pay me so I'll keep paying your mom? You didn't do very well in business class, did ya kid."
                    mc.name "She likes the job, I have the cash. I just want you to stay away from her."
                    "He shakes his head and scoffs."
                    mom_boss_quick_name "I'm not for sale. I've got enough money to buy whatever I want."
                    mom_boss_quick_name "Alright, I think I've entertained this long enough."

            mc.name "I..."
            "He shakes his head and walks towards the door of the office, motioning for you to leave."
            mom_boss_quick_name "I thought Miss.[mc.last_name] was just a stuffy house wife, but now you've got me interested."
            mom_boss_quick_name "I'm going to keep her around, and see if I can get that ass bouncing on my dick."
            mom_boss_quick_name "You obviously think it might happen, or you wouldn't be here."
            mc.name "Listen, I can..."
            mom_boss_quick_name "No, you can't. Scram kid, before I call security. I've got a board meeting to get to."

    mc.name "Don't you have to meet your daughter?"
    "He glares at you."
    mom_boss_quick_name "What? What do you... Oh fuck, what day is it?"
    "He groans and paces around the room. After a moment he looks at you again, looking more concerned now."
    mom_boss_quick_name "Why do you know about that? You stay away from her, do you understand?"
    mc.name "Hey, I'm just passing the message along. It sounds like she's been waiting in the lobby for a {i}long{/i} time."
    mom_boss_quick_name "Get out. I don't have time for this!"
    "You decide to cut your losses and back out of the room as [mom_boss_quick_name] grabs for the phone on his desk."
    mom_boss_quick_name "... Yeah... Is she... For how long?..."
    "You return to the elevators and take one back to the lobby, unsure of what to do next."
    "When they open the young woman from earlier is standing at the front desk, sobbing quietly while the secretary tries to calm her."
    $ the_group = GroupDisplayManager([the_secretary, the_daughter])
    $ the_group.draw_person(the_daughter, emotion = "sad")
    $ the_group.draw_person(the_secretary)
    $ the_daughter.change_happiness(-30)
    the_secretary "... okay sweetheart. I'm sure he's on his way, it'll probably be a super quick meeting..."
    $ the_group.draw_person(the_daughter, emotion = "sad")
    the_daughter "Maybe... Can I just sit here?"
    "She glances at you as you step out of the elevator."
    menu:
        "Comfort her.":
            "You join the two girls at the front desk."
            mc.name "I, uh... let him know, but I guess you've heard from him."
            "She nods, fresh tears obvious on her cheeks."
            the_daughter "I'm just going to wait here. He won't be long, right?"
            mc.name "I... wouldn't bet on that. My meeting with him didn't go much better, if that helps."
            mc.name "Would you like to go for a walk, maybe get a drink. I think I could use one."
            the_daughter "But what if he comes looking for me?"
            mc.name "We'll stay close by, if he calls you'll be back in five minutes. I bet you've waited a lot longer than that for him, right?"
            "She nods again, wiping her face with the palms of her hands."
            the_daughter "Sorry, I'm a mess."
            mc.name "Don't worry about it, some days are just like that."
            "The secretary leans back in her chair, looking obviously relieved to have someone take care of this burden."
            $ clear_scene()
            $ the_daughter.draw_person()
            $ the_daughter.change_happiness(5)
            mc.name "I don't think I got your name, by the way."
            "She gives you a weak smile."
            $ title_choice = get_random_title(the_daughter)
            $ formatted_title = the_daughter.create_formatted_title(title_choice)
            the_daughter "I'm [formatted_title]. Nice to meet you. Well, not that nice, but you know..."
            $ the_daughter.set_title(title_choice)
            #$ the_daughter.set_possessive_title(get_random_possessive_title(the_daughter))
            $ the_daughter.set_possessive_title(mom_boss_quick_name + "'s daughter")
            "She looks at you expectantly, waiting for your name in return."
            call person_introduction(the_daughter, girl_introduction = False) from _call_person_introduction_5
            mc.name "Come on, let's go find a drink. Know anywhere good around here?"
            "[the_daughter.possessive_title] shakes her head meekly."
            mc.name "I'm sure we'll find something. I'm not feeling too picky..."
            $ the_daughter.change_love(10)
            $ bar_location.show_background()
            $ the_daughter.draw_person()
            "After a quick search on your phone and a brief walk the two of you are sitting in a small hole in the wall bar."
            $ the_daughter.change_happiness(10)
            "You order drinks and sit down. Soon enough you have [the_daughter.title] talking and smiling,clearly happier than she was before."
            call date_conversation(the_daughter) from _call_date_conversation
            the_daughter "Hey, so uh... Thanks for doing this for me. I was a mess back there."
            mc.name "I just took a pretty girl out for drinks, I'm not exactly a super hero."
            the_daughter "Well it meant a lot to me. So maybe... we could do this again some time?"
            mc.name "That sounds like a..."
            "You're interupted by her phone buzzing. She glances at it and sighs."
            the_daughter "That's him, I need to get going. Here, let me give you my number."
            mc.name "On one condition."
            the_daughter "What would that be?"
            mc.name "Don't tell your dad about me. I don't think he's particularly fond of me at the moment."
            the_daughter "Did something happen at your meeting? You know what, I don't need to know."
            the_daughter "I won't say a word. Just promise you'll call, okay?"
            mc.name "Deal."
            "You hand her your phone, and she keys in her number. She hands it back with a smile."
            the_daughter "See you around [the_daughter.mc_title]."
            mc.name "See you soon [the_daughter.title]."
            $ clear_scene()
            "She hurries out of the bar. You take a few minutes to finish your drink, then out as well."



            pass #TODO: Decide what else we might want to have as part of this storyline in this update.
            # Key part is that you've met his daughter.
            # Maybe just a simple event if you start dating her where you talk to him, and he promises to back off as long as you don't "break her heart."
            # Also meet her mom at some point. Maybe if you do that you can threaten to tell her, and that blackmail has the same effect.

        "Leave.":
            "You try and avoid her gaze as you walk awkwardly past."
            mc.name "I, uh... let him know. Have a good day."
            "You hurry out of the building and back onto the city street."
            $ clear_scene()


    #TODO: Your conversation with him


    #TODO: Add an introduction for his daughter so you can set her title for you
    #TODO: YOu go up to talk to him.
    #TODO: Either you decide to do nothing, provide him with a sluttier girl to work as his proper assistant, or decide to blackmail him.


    #TODO
    $ mc.change_location(downtown) #Make sure we move you downtown

    call advance_time() from _call_advance_time_33 #All of that took some time, so let's advance it a little bit.
    return

label mom_got_boobjob_label(the_person):
    call got_boobjob(the_person) from _call_got_boobjob_2
    return
