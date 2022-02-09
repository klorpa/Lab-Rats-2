#Contains all of the role events and actions related to the main Mom storyline.

init -2 python:
    def mom_on_day(the_person):
        # Set up taboo break revisits if taboos have been broken.
        if the_person.has_broken_taboo(["touching_body","kissing","bare_pussy","bare_tits","touching_vagina"]) and not the_person.event_triggers_dict.get("kissing_revisit_complete", False): #Checks if they have all of these taboos or not.
            if the_person.has_role(mom_girlfriend_role):
                the_person.event_triggers_dict["kissing_revisit_complete"] = True
            else:
                broken_taboos = the_person.event_triggers_dict.get("kissing_revisit_restore_taboos",[]) #Note: this will result in duplicates sometimes.
                if the_person.has_broken_taboo("bare_tits"):
                    broken_taboos.append("bare_tits")
                if the_person.has_broken_taboo("bare_pussy"):
                    broken_taboos.append("bare_pussy")
                if the_person.has_broken_taboo("kissing"):
                    broken_taboos.append("kissing")
                if the_person.has_broken_taboo("touching_body"):
                    broken_taboos.append("touching_body")
                if the_person.has_broken_taboo("touching_vagina"):
                    broken_taboos.append("touching_vagina")

                taboo_revisit_event = Action("mom kissing taboo revisit", mom_kissing_taboo_revisit_requirement, "mom_kissing_taboo_break_revisit")
                if not the_person.has_queued_event(taboo_revisit_event):
                    the_person.event_triggers_dict["kissing_revisit_count"] = the_person.event_triggers_dict.get("kissing_revisit_count",0) + 1
                    the_person.on_room_enter_event_list.append(taboo_revisit_event)
                    for a_taboo in broken_taboos:
                        the_person.restore_taboo(a_taboo, add_to_log = False)
                the_person.event_triggers_dict["kissing_revisit_restore_taboos"] = broken_taboos

        if the_person.has_broken_taboo(["sucking_cock", "licking_pussy"]) and not the_person.event_triggers_dict.get("oral_revisit_complete", False):
            if the_person.has_role(mom_girlfriend_role):
                the_person.event_triggers_dict["oral_revisit_complete"] = True
            else:
                broken_taboos = the_person.event_triggers_dict.get("oral_revisit_restore_taboos",[])
                if the_person.has_broken_taboo("sucking_cock"):
                    broken_taboos.append("sucking_cock")
                if the_person.has_broken_taboo("licking_pussy"):
                    broken_taboos.append("licking_pussy")
                taboo_revisit_event = Action("mom oral taboo revisit", mom_oral_taboo_revisit_requirement, "mom_oral_taboo_break_revisit")
                if not the_person.has_queued_event(taboo_revisit_event):
                    for a_taboo in broken_taboos:
                        the_person.restore_taboo(a_taboo, add_to_log = False)
                    the_person.event_triggers_dict["oral_revisit_count"] = the_person.event_triggers_dict.get("oral_revisit_count", 0) + 1
                    the_person.on_room_enter_event_list.append(taboo_revisit_event)
                the_person.event_triggers_dict["oral_revisit_restore_taboos"] = broken_taboos

        if the_person.has_broken_taboo("anal_sex") and not the_person.event_triggers_dict.get("anal_revisit_complete", False):
            if the_person.has_role(mom_girlfriend_role):
                the_person.event_triggers_dict["anal_revisit_complete"] = True
            else:
                taboo_revisit_event = Action("mom anal taboo revisit", mom_anal_taboo_revisit_requirement, "mom_anal_taboo_break_revisit")
                if not the_person.has_queued_event(taboo_revisit_event):
                    the_person.restore_taboo("anal_sex", add_to_log = False)
                    the_person.event_triggers_dict["anal_revisit_count"] = the_person.event_triggers_dict.get("anal_revisit_count", 0) + 1
                    the_person.on_room_enter_event_list.append(taboo_revisit_event)

        if the_person.has_broken_taboo("vaginal_sex") and not the_person.event_triggers_dict.get("vaginal_revisit_complete", False):
            if the_person.has_role(mom_girlfriend_role):
                the_person.event_triggers_dict["vaginal_revisit_complete"] = True
            else:
                taboo_revisit_event = Action("mom vaginal taboo revisit", mom_vaginal_taboo_revisit_requirement, "mom_vaginal_taboo_break_revisit")
                if not the_person.has_queued_event(taboo_revisit_event):
                    the_person.restore_taboo("vaginal_sex", add_to_log = False)
                    the_person.event_triggers_dict["vaginal_revisit_count"] = the_person.event_triggers_dict.get("vaginal_revisit_count", 0) + 1
                    the_person.on_room_enter_event_list.append(taboo_revisit_event)


        return

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
        the_person "This new mortgage on the house is really stressing our finances. It would really help if you could chip in."
        call mom_low_sluttiness_weekly_pay(the_person) from _call_mom_low_sluttiness_weekly_pay #The menu is separated out to make looping easier.
    else:
        if mc.business.event_triggers_dict.get("Mom_Payment_Level",0) >= 1: #We've been through this song and dance already.
            if the_person.event_triggers_dict.get("Mom_forced_off_bc", False):
                if the_person.on_birth_control:
                    $ mc.change_locked_clarity(10)
                    the_person "The budget is still really tight [the_person.mc_title], so I was wondering if you wanted to buy some sort of favour from me?"
                    $ the_person.event_triggers_dict["Mom_forced_off_bc"] = False
                else:
                    the_person "The budget is still really tight [the_person.mc_title]. I was hoping you could help out, for a favour, of course."
                    $ mc.change_locked_clarity(10)
                    the_person "I haven't taken my birth control all week. If you're able to pay me I won't start again."
                    menu:
                        "Keep her off her birth control. -$150" if mc.business.has_funds(150):
                            mc.name "I think we can keep this deal going."
                            "You pull out the cash and hand it over. She places them alongside the bills."
                            $ mc.business.change_funds(-150)
                            the_person "Thank you so much. Is there anything else I could do for a little more help?"

                        "Keep her off her birth control. -$150 (disabled)" if not mc.business.has_funds(150):
                            pass

                        "Let her start taking her birth control.":
                            mc.name "I'm sorry, the budget at work has been a little tight lately."
                            the_person "I understand. Is there anything else I can do for then?"
                            call manage_bc(the_person, start = True) from _call_manage_bc
                            $ the_person.event_triggers_dict["Mom_forced_off_bc"] = False
            else:
                $ mc.change_locked_clarity(10)
                the_person "The budget is still really tight [the_person.mc_title], so I was wondering if you wanted to buy any sort of favour from me?"

            if lily.event_triggers_dict.get("sister_instathot_special_pictures_recent", False) and not lily.event_triggers_dict.get("sister_instathot_mom_knows", False): #She sold special pictures this week and Mom doesn't know about them yet.
                call mom_weekly_pay_lily_question(the_person) from _call_mom_weekly_pay_lily_question
                $ lily.event_triggers_dict["sister_instathot_special_pictures_recent"] = False


        else:
            the_person "Our budget is really stretched thin right now, and it would be a huge relief if you could help out."
            the_person "I wouldn't feel right about just taking your hard earned money though, so I was hoping we could make a deal..."
            mc.name "What sort of deal Mom?"
            $ mc.change_locked_clarity(5)
            the_person "Remember last summer, and you paid me for some... personal favours?"
            "Of course you remember all of the naughty things you convinced her to do last year."
            "Her memory of it seems much foggier, probably as a result of all the serum you exposed her to."
            "[the_person.title] blushes and looks away for a second before regaining her composure."
            $ mc.change_locked_clarity(10)
            the_person "Maybe we could start doing that again... I know I shouldn't even bring it up."
            mc.name "No [the_person.title], you're doing it for the good of the family, right? I think it's a great idea."
            $ the_person.change_slut(2, 30)
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
            the_person "Okay sweetheart, I understand. I'll talk with Lily and let her know that we have to cut back on non essentials."

        "Help out.\n{size=22}-$100{/size}" if mc.business.has_funds(100):
            "You pull out your wallet and count out some cash, but hesitate before you hand it over."
            $ mc.business.change_funds(-100)
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
                        $ mc.change_locked_clarity(10)
                        "After a moment she pulls back and looks away from you, blushing."
                        $ the_person.break_taboo("kissing")
                    else:
                        the_person "Okay, come here."
                        if the_person.effective_sluttiness("kissing") > 15:
                            "You lean down to kiss her as she's sitting. [the_person.possessive_title] puts a hand on the back of your head and pulls you against her as your lips meet."
                            "Her mouth opens slightly, letting your tongues meet as she makes out with you."
                            $ the_person.change_arousal(5 + mc.sex_skills["Foreplay"])
                            "It might be your imagination, but you think you might even hear her moan."
                            $ mc.change_locked_clarity(10)
                            "When you finally break the kiss she fixes her hair and smiles proudly at you."
                        else:
                            "You lean down to kiss her. She lets you press your lips against hers, and even returns the gentle kiss after a moment of hesitation."
                            $ mc.change_locked_clarity(10)
                            "When you finally break the kiss she looks away from you, blushing with embarrassment."

                    $ the_person.change_slut(2, 30)
                    the_person "There, have I earned my reward?"
                    "You hold out the cash for her and she takes it."
                    the_person "Thank you so much, every little bit helps."

                "Make her say please.":
                    mc.name "What are the magic words?"
                    the_person "Abracadabra?"
                    mc.name "No, the words we say when we want help?"
                    the_person "Oooh, I see what you're getting at. I've drilled it into you and now I'm getting a taste of my own medicine."
                    "She smiles and rolls her eyes playfully."
                    $ mc.change_locked_clarity(5)
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

        "Help out.\n{size=22}-$100{/size} (disabled)" if not mc.business.has_funds(100):
            pass
    return

label mom_high_sluttiness_weekly_pay(the_person): #TODO: Change all of these over to use Actions instead of just being a menu.
    menu:
        "Strip for me. -$100" if mc.business.has_funds(100):
            if mc.business.event_triggers_dict.get("Mom_Strip", 0) >= 1:
                mc.name "I want you to show off yourself off to me, how does that sound?"
                the_person "Fair is fair, but I'll need a little extra if you want to see anything... inappropriate."
                $ mc.business.change_funds(-100)
                $ the_person.change_obedience(1)
                "You hand over the cash and sit back while [the_person.possessive_title] entertains you."
            else:
                $ mc.business.event_triggers_dict["Mom_Strip"] = 1
                mc.name "I'd like to see a little more of you Mom, how about I pay you to give me a little strip tease."
                the_person "Oh my god, I've raised such a dirty boy. How about I pose for you a bit, and if you want to see more you can contribute a little extra."
                mc.name "Sounds like a good deal Mom."
                $ mc.business.change_funds(-100)
                $ the_person.change_obedience(1)
                "You hand over the cash and sit back while [the_person.possessive_title] entertains you."

            call strip_tease(the_person, for_pay = True)


        "Strip for me. -$100 (disabled)" if not mc.business.has_funds(100):
            pass

        "Test some serum. -$100" if mc.business.has_funds(100):
            if mc.business.event_triggers_dict.get("Mom_Serum_Test",0) >= 1:
                mc.name "I've got some more serum I'd like you to test Mom."
                call give_serum(the_person) from _call_give_serum_10
                if _return:
                    $ mc.business.change_funds(-100)
                    "You hand the serum to [the_person.possessive_title], followed by the cash."
                    the_person "Okay, so that's all for now?"
                    mc.name "That's all. I'll just be keeping an eye on you in the future, but you don't need to worry about that."
                    the_person "Well thank you sweetheart, this money will really make a difference. I'm so proud of you!"
                else:
                    mc.name "Actually, I don't have anything right now. Maybe next week though, okay?"
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
                    $ mc.business.change_funds(-100)
                    "You hand the serum to [the_person.possessive_title], followed by the cash."
                    the_person "Okay, so that's all for now?"
                    mc.name "That's all. I'll just be keeping an eye on you in the future, but you don't need to worry about that."
                    the_person "Well thank you sweetheart, this money will really make a difference. I'm so proud of you!"
                else:
                    mc.name "Actually, I don't have anything right now. Maybe next week though, okay?"
                    the_person "Okay sweetheart, thanks for at least thinking about it."

        "Test some serum. -$100 (disabled)" if not mc.business.has_funds(100):
            pass

        # "I want to make some changes around here." if the_person.obedience >= 120:
        #     #TODO: Requires obedience, but unlocks a bunch of other options, like having your Mom bring you breakfast every morning, not wearing anything at home, etc.
        #     mc.name "Now that I'm the man of the house, I want to make some changes around the house."
        #     the_person "What sorts of changes?"
        #     call mom_make_house_changes(the_person)
        #
        # "I want to make some changes around here.\nRequires: 120 Obedience (disabled)" if the_person.obedience < 120:
        #     pass


        #TODO: "I want to breed Lily" option, once you've got Mom at high sluttiness, obedience, and Love. She gives you the go-ahead to knock up your sister.

        "Suck me off. -$300" if mc.business.has_funds(300) and the_person.effective_sluttiness("sucking_cock") >= 30:
            mc.name "Alright, I'll pay you to give me a blowjob."
            if (not the_person.has_taboo("sucking_cock")) or the_person.effective_sluttiness("sucking_cock") >= 60:
                the_person "If that's what you need."
                $ mc.change_locked_clarity(10)
                "You pull out your wallet and count out her cash while [the_person.possessive_title] gets onto her knees in front of you."
                $ mc.business.change_funds(-300)
                $ the_person.draw_person(position = "blowjob")
                the_person "Remember, not a word to anyone else though. Okay?"
                mc.name "Of course, this is just between you and me."
                $ the_person.break_taboo("sucking_cock")

            else:
                the_person "What? I mean... I could never do that! How could you even say that?"
                "You pull out your wallet and count out the cash while you talk."
                mc.name "Sure you could. It's just me and you here, nobody would ever need to know."
                mc.name "Besides, it's for the family, right? This is just another way to help everyone out. Myself included, I've been real stressed at work lately."
                $ mc.business.change_funds(-300)
                "You lay the cash down on the table. [the_person.possessive_title] hesitates, then meekly reaches for the money."
                the_person "Not a word to anyone, or I'll kick you out of the house."
                mc.name "Of course [the_person.title], don't you trust your own son?"
                $ the_person.draw_person(position = "blowjob")
                $ mc.change_locked_clarity(10)
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
                "You pull your pants up while [the_person.possessive_title] gets off of her knees and cleans herself up."
            $ the_person.review_outfit()
            $ the_person.change_obedience(4)

        "Suck me off. -$300 (disabled)" if not mc.business.has_funds(300) and the_person.effective_sluttiness("sucking_cock") >= 30:
            pass

        "Stop your birth control. -$150" if mc.business.has_funds(150) and the_person.effective_sluttiness() >= 30 and persistent.pregnancy_pref > 0 and not the_person.event_triggers_dict.get("Mom_forced_off_bc", False):
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
                $ mc.business.change_funds(-150)
                the_person "One moment."
                "[the_person.possessive_title] leaves the room, but returns quickly. She hands you a small blister pack labeled with each day of the week."
                the_person "Here are my pills for the week, so you know I'm not lying. I've already taken one for today, but starting tomorrow I won't have any."
                mc.name "Thank you [the_person.title]."
                $ the_person.event_triggers_dict["Mom_forced_off_bc"] = True
                call manage_bc(the_person, start = False) from _call_manage_bc_1
            else:
                the_person "I'm sorry, I can't take your money for that [the_person.mc_title]."
                mc.name "Sure you can [the_person.title], it's..."
                "[the_person.possessive_title] shakes her head and interrupts you."
                the_person "No, I mean I can't take your money because I'm not taking any birth control right now."
                if the_person.has_taboo("vaginal_sex"):
                    the_person "It's been a while since I needed it, so I don't bother."
                else:
                    the_person "I know I should, but... I just haven't bothered talking to my doctor."
                $ the_person.update_birth_control_knowledge()
                the_person "Is there something else you would like?"
                call mom_high_sluttiness_weekly_pay(the_person) from _call_mom_high_sluttiness_weekly_pay_1


        "Stop your birth control. -$150 (disabled)" if not mc.business.has_funds(150) and the_person.effective_sluttiness() >= 30 and persistent.pregnancy_pref > 0  and not the_person.event_triggers_dict.get("Mom_forced_off_bc", False):
            pass

        #TODO: Enable this and tie it into Lily's new Instapic story chunk
        # "Let [lily.title] get a boob job. -$500" if mc.business.has_funds(200) and lily.event_triggers_dict.get("insta_boobjob_wanted", False): #TODO: Implement this!
        #     mc.name "This will be some easy money for you. I want you to let [lily.title] have some cosmetic surgery done."
        #     mc.name "I'll pay you $500 if you just tell her you're okay with it. You don't need to do anything else."
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
        #TODO: pay her to do something with Lily.
        #TODO: have Lily start a cam show to make cash, then bring your Mom into it.



    return

label mom_post_sex_confront(the_person):
    #TODO: She talks to you after the first time you seduce her somehow and talks about how "it was wrong... we can't do that!"

    return

label mom_make_house_changes(the_person):
    # A list of house rules to put into place.
    # TODO: This entire event. Make each one a linked action so that requirements work properly.

    #TODO: Just display a bunch of action options os that the requirements are properly formatted for all of these.

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
    #     # TODO: The discipline options are only available after Lily's started her InstaPic account and is posting stuff and you turn her in. If Mom is too slutty she says she doesn't care.
    #     # TODO: Add other "bad" things you can use as leverage against Lily.
    #     "I want to be in charge of Lily's discipline.": #Only after she's done something "bad", let's you punish her somehow, or just unlocks other things in this menu?
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

label mom_offer_make_dinner_label(the_person): #you offer to make dinner. It takes up time, but you can slip serum to your mom and sister.
    mc.name "You've been working yourself so hard lately Mom, how about you let me make dinner tonight?"
    the_person "Oh [the_person.mc_title], that's such a sweet thing for you to offer!"
    $ the_person.change_happiness(5)
    $ the_person.change_obedience(-1)
    $ the_person.change_love(2)

    the_person "Do you know where everything is?"
    mc.name "Yeah, I think I can take care of it."
    the_person "Well thank you, you're always such a help around here!"
    if the_person.love < 20 and the_person.effective_sluttiness() < 10:
        $ mc.change_locked_clarity(5)
        "[the_person.possessive_title] gives you a quick hug."
    elif the_person.love < 40 and the_person.effective_sluttiness() < 30:
        $ mc.change_locked_clarity(10)
        "[the_person.possessive_title] gives you a hug, then a quick kiss on the lips."
    else:
        $ mc.change_locked_clarity(10)
        "[the_person.possessive_title] gives you a hug, then kisses you on the lips."
        the_person "It's so nice having a man around the house again..."
        "She leans her head happily on your shoulder for a moment."
        menu:
            "Hold her gently.":
                "You just hold [the_person.title] in your arms for a few moments."
                $ the_person.change_love(1)
                "After a little while she sighs and steps back."
                the_person "I should get out of your way."

            "Slap her ass.":
                "You reach around [the_person.possessive_title] and give her ass a quick slap."
                if the_person.outfit.vagina_visible():
                    "The strike makes a satisfying smack and sets her butt jiggling for a few moments."
                    $ mc.change_locked_clarity(20)
                    "You give her bare ass a few more taps before letting her step back."
                else:
                    $ mc.change_locked_clarity(10)
                    "The strike makes a satisfying smack and sets her butt jiggling for a few moments."
                the_person "Oh!"
                mc.name "Come on [the_person.title], I've got dinner to cook. Run along, or I'll find some way to put you to work."


    the_person "Let me know if you need anything."
    $ clear_scene()
    $ kitchen.show_background()
    "You get to work. The cooking isn't hard, but it takes up most of your evening."
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

label mom_date_intercept(the_mom, the_date): #TODO: Add some relationship awareness to Mom so she can comment on you dating multiple girls, etc.
    #Triggers when you've got a date planned with a girl, but Mom has high Love.
    #TODO: Write a Mom specific movie date. Maybe mirror the LR1 event and have Lily join in sometimes.

    "You're getting ready for your date with [the_date.title] when you hear a knock at your door."
    the_mom "Knock knock. Are you in there [the_mom.mc_title]?"
    mc.name "Yeah, come on in [the_mom.title]."
    $ the_mom.draw_person()
    "[the_mom.possessive_title] steps into your room and closes the door behind her."
    the_mom "Oh, you're looking very handsome tonight. Is there some special occasion?"
    if the_date.has_role(girlfriend_role) and (not the_date.has_role(sister_girlfriend_role) or the_date.event_triggers_dict.get("sister_girlfriend_mom_knows",False)):
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
            $ mc.change_locked_clarity(10)
            the_mom "Convincing you to stay home tonight."
            $ generalised_strip_description(the_mom, strip_list)
            $ mc.change_locked_clarity(20)

        else:
            the_mom "You are? I... Don't go anywhere, okay? I'll be right back."
            $ clear_scene()
            "Before you can ask her any questions she's hurried out of your room."
            "You shrug and go back to preparing for your date. A few short minutes later [the_mom.possessive_title] steps back into your room."
            $ the_mom.apply_outfit(lingerie_wardrobe.get_random_appropriate_outfit(the_mom.sluttiness + 20, 0 + (the_mom.sluttiness/2), guarantee_output = True), update_taboo = True)
            $ the_mom.draw_person()
            $ mc.change_locked_clarity(30)
            the_mom "[the_mom.mc_title], are you still sure you want to go out and see some other girl?"
            mc.name "[the_mom.title], what are you doing?"
            the_mom "Convincing you to stay home tonight."

        the_mom "What are you expecting this girl to do for you that I can't? You know nobody will ever love you like your mother."
        the_mom "You're a man now, which means you have different needs, but I still want to be the one to take care of you."
        $ mc.change_locked_clarity(20)
        "She steps close to you and cups your crotch, rubbing your already-hard cock through your pants."
        the_mom "Let me take care of you. Stay home tonight."
        menu:
            "Cancel your date with [the_date.title].":
                mc.name "[the_mom.title]... You know you're the most important woman in my life. I'll call [the_date.title] and cancel."
                $ the_mom.change_happiness(10)
                $ the_mom.change_love(2)
                $ the_mom.change_slut(1, 70)
                "[the_mom.possessive_title]'s face lights up."
                the_mom "Thank you [the_mom.mc_title], you're making the right decision. We're going to have such a wonderful time together."
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
                    $ mc.change_locked_clarity(20)
                    "You call [the_date.title] as [the_mom.possessive_title] starts to lick at your shaft."
                    $ the_mom.draw_person(position = "blowjob", special_modifier = "blowjob", the_animation = blowjob_bob, animation_effect_strength = 0.3)
                    the_date "Hello?"
                    mc.name "Hey [the_date.title], it's [the_date.mc_title]."
                    the_date "Hey [the_date.mc_title], I was just about to head out the door. Is everything okay?"
                    mc.name "Well, I hate to tell you this so late, but..."
                    $ mc.change_locked_clarity(30)
                    "[the_mom.possessive_title] looks up at you from her knees, your cock bulging out one cheek."
                    mc.name "Something important has come up, and it needs to be taken care of. I won't be able to go out tonight."
                    $ the_mom.change_love(4)
                    $ the_mom.change_slut(1, 70)
                    $ mc.change_locked_clarity(30)
                    "[the_mom.title]'s eyes light up, and she bobs her head up and down on your shaft happily. You have to stifle a moan."
                    the_date "Oh no, is everyone okay?"
                    $ the_date.change_happiness(-20)
                    $ the_date.change_love(-3)
                    "[the_date.possessive_title]'s disappointment is clear, even over the phone."
                    mc.name "It's a family situation, I'm sorry that I can't say any more."
                    $ mc.change_locked_clarity(20)
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
                    $ the_mom.draw_person(position = "doggy")
                    $ mc.change_locked_clarity(20)
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
                        $ mc.change_locked_clarity(40)
                    "You're distracted as [the_mom.possessive_title] reaches back and jiggles her butt for you."
                    the_date "[the_date.mc_title]? Are you there?"
                    mc.name "Uh, yeah. Sorry, I hate to tell you this so late, but something important has come out."
                    mc.name "I'm not going to be able to make it for our date tonight."
                    the_date "Oh no, is everyone okay?"
                    $ the_date.change_happiness(-20)
                    $ the_date.change_love(-3)
                    $ mc.change_locked_clarity(30)
                    "[the_mom.title] grabs one ass cheek and pulls it to the side, giving you a clear view of her pretty pink pussy."
                    menu:
                        "Fuck [the_mom.title]'s pussy right away.":
                            "You unzip your pants and step closer to [the_mom.possessive_title]."
                            mc.name "It's my Mom, she really needs me close right now."
                            $ mc.change_locked_clarity(40)
                            "You grab [the_mom.title]'s hips with your free hand and hold her steady as you slide your cock into her wet pussy. You fuck her slowly while you talk."
                            $ the_mom.draw_person(position = "doggy", the_animation = blowjob_bob, animation_effect_strength = 0.3)
                            mc.name "I can't really say any more than that right now. I'm sorry."
                            the_date "I understand, I hope everything works out. Let's try and reschedule some time soon, okay?"
                            $ mc.change_locked_clarity(30)
                            "[the_mom.possessive_title] grabs one of your pillows to muffle her moans with."
                            mc.name "Yeah, I'll be in touch. Thanks for understanding [the_date.title]. Bye."
                            the_date "Bye..."
                            if the_mom.has_taboo("condomless_sex") or the_mom.wants_condom():
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
                            the_date "I understand, I hope everything works out. Let's try and reschedule some time soon, okay?"
                            $ mc.change_locked_clarity(30)
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
                return True

            "Tell her no.":
                mc.name "Sorry [the_mom.title], but I just can't cancel my plans this suddenly."
                mc.name "I need to get going."
                if the_mom.love > 80:
                    "You hurry to the door, but [the_mom.possessive_title] grabs your arm."
                    $ mc.change_locked_clarity(10)
                    the_mom "Wait! How about about just a quicky? You can tell her you're running late."
                    the_mom "I want to take all of your cum, so she doesn't get any. Can you give me that, at least?"
                    menu:
                        "Fuck [the_mom.title] before your date.":
                            "You sigh, then nod."
                            mc.name "Fine, but we need to make it quick."
                            $ the_mom.change_love(1)
                            $ the_mom.change_slut(1, 80)
                            "She nods happily."
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

                            "You're interrupted by a phone call. It's [the_date.title]."
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
        $ mc.change_locked_clarity(10)
        "She steps closer to you and puts a hand to your crotch. It twitches in response, quickly growing hard."
        the_mom "I don't want you out getting in trouble with girls if all you really need is some physical relief."
        the_mom "If you decide to stay home, maybe I can... take care of this for you?"
        mc.name "[the_mom.title], [the_date.title] won't be happy with me if I cancel last minute."
        $ the_mom.draw_person(position = "kneeling1")
        "[the_mom.possessive_title] gets onto her knees in front of you, face level with the large bulge in your pants."
        if the_mom.has_taboo("sucking_cock"):
            the_mom "Please [the_mom.mc_title]? You were probably hoping to get a blowjob from her, right? Well..."
            "She hesitates, as if she needs to be extra sure she means what she's about to say."
            $ mc.change_locked_clarity(20)
            the_mom "I could do that too! You wouldn't need to worry about dressing up, or paying for dinner, or even leaving the house."
            the_mom "Just stay home and I'll take better care of you than any whatever skank is trying to get her hands on you!"
        else:
            the_mom "Please [the_mom.mc_title]? If you stay you don't need to worry about dressing up or paying for dinner."
            $ mc.change_locked_clarity(20)
            the_mom "I'll give you a nice blowjob, then when you're finished we can watch some TV and relax."
            the_mom "Doesn't that sound so much nicer than trying to impress some skank you just met? You've known me your whole life already."

        menu:
            "Cancel your date with [the_date.title].":
                $ mc.change_locked_clarity(20)
                "[the_mom.possessive_title] cups your crotch and massages it gently while you think about it."
                mc.name "Fine, but she's really not going to be happy about this."
                the_mom "Don't worry about her, I'm the only woman you need in your life right now. You can worry about finding a wife when you're older."
                mc.name "Just... Give me a minute to call her, okay?"
                if the_mom.get_opinion_score("giving blowjobs") > 0 and the_mom.effective_sluttiness("sucking_cock") >= 50:
                    the_mom "I can be quiet. Go ahead, I'll just get started..."
                    $ mc.change_locked_clarity(10)
                    "You get your phone out while [the_mom.title] pulls down your pants. Your hard cock bounces against her face when it springs free of your underwear."
                    the_mom "Oh! Sorry, sorry..."
                    $ mc.change_locked_clarity(20)
                    "You call [the_date.title] as [the_mom.possessive_title] starts to lick at your shaft."
                    $ the_mom.draw_person(position = "blowjob", special_modifier = "blowjob", the_animation = blowjob_bob, animation_effect_strength = 0.3)
                    the_date "Hello?"
                    mc.name "Hey [the_date.title], it's [the_date.mc_title]."
                    the_date "Hey [the_date.mc_title], I was just about to head out the door. Is everything okay?"
                    mc.name "Well, I hate to tell you this so late, but..."
                    $ mc.change_locked_clarity(20)
                    "[the_mom.possessive_title] looks up at you from her knees, your cock bulging out one cheek."
                    mc.name "Something important has come up, and it needs to be taken care of. I won't be able to go out tonight."
                    $ the_mom.change_love(4)
                    $ the_mom.change_slut(1, 70)
                    $ mc.change_locked_clarity(20)
                    "[the_mom.title]'s eyes light up, and she bobs her head up and down on your shaft happily. You have to stifle a moan."
                    the_date "Oh no, is everyone okay?"
                    $ the_date.change_happiness(-20)
                    $ the_date.change_love(-3)
                    "[the_date.possessive_title]'s disappointment is clear, even over the phone."
                    mc.name "It's a family situation, I'm sorry that I can't say any more."
                    "[the_mom.possessive_title] sucks gently on the tip of your cock."
                    the_date "Okay, well... I hope you get that resolved. Let's try and reschedule, okay?"
                    mc.name "Yeah, I'll be in touch. Thanks for understanding [the_date.title]. Bye."
                    the_date "Bye..."
                    $ mc.change_locked_clarity(20)
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
                    $ the_mom.change_slut(1, 70)
                    the_date "Oh no, is everyone okay?"
                    $ the_date.change_happiness(-20)
                    $ the_date.change_love(-3)
                    "[the_date.possessive_title]'s disappointment is clear, even over the phone."
                    mc.name "It's a family situation, I'm sorry that I can't say any more."
                    the_date "Okay, well... I hope you get that resolved. Let's try and reschedule, okay?"
                    mc.name "Yeah, I'll be in touch. Thanks for understanding [the_date.title]. Bye."
                    the_date "Bye..."
                    the_mom "Thank you [the_mom.mc_title]. Now, should I take care of this?"
                    $ mc.change_locked_clarity(10)
                    "She unzips your pants and pulls them down. Your hard cock springs free, bouncing in front of her face."
                    the_mom "Oh!"
                    if the_mom.break_taboo("sucking_cock"):
                        $ mc.change_locked_clarity(20)
                        the_mom "It looks so much bigger when it's right in your face..."
                        "She takes a deep breath."
                        the_mom "It's fine, I can do this. Anything to make my [the_mom.mc_title] feel special and want to spend more time with me."
                    "She gives it an experimental kiss, then slips her lips over the tip."


                if not the_mom.outfit.vagina_visible() or not the_mom.outfit.tits_visible():
                    menu:
                        "Order her to strip." if the_mom.obedience >= 140:
                            mc.name "You should be dressed for the occasion first. Strip."
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
                            $ mc.change_locked_clarity(30)
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
                $ mc.change_locked_clarity(20)
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
            $ mc.change_locked_clarity(10)
            the_mom "I've got a bit of experience, I can... give you a handjob?"
        else:
            $ mc.change_locked_clarity(10)
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
                $ mc.change_locked_clarity(10)
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
                    $ mc.change_locked_clarity(20)
                    the_mom "There, now you have something to ogle while I get you off."
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
                                $ mc.change_locked_clarity(20)
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
                    $ the_mom.change_slut(2, 80)
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
                    "She seems rather disappointed in herself."
                    $ the_mom.change_slut(1, 60)
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
                    $ the_mom.change_slut(1, 50)
                    the_mom "Well, if that's what you're planning... Be sure to show her a good time. Don't be selfish, girls don't like that."
                    mc.name "Okay [the_mom.title], I'll do that."
                else:
                    mc.name "Depending on how the date goes I might need all my energy for later tonight."
                    the_mom "Oh [the_mom.mc_title], well..."
                    $ the_mom.change_slut(1, 60)
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
        $ the_person = create_random_person(job = secretary_job)
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


init -1 python:
    def mom_found_serums_requirement(start_day):
        if day < start_day:
            return False

        return True

label mom_found_serums(): #TODO: Triggers a couple of days after the start of the game
    # Triggers in the morning (so you have a chance to interact with her after dosing her)
    $ the_person = mom

    $ blue_serum = SerumDesign()
    $ blue_serum.name = "Blue Serum"
    $ blue_serum.add_trait(primitive_serum_prod)
    $ blue_serum.add_trait(high_capacity_design)
    $ blue_serum.add_trait(high_con_drugs)
    $ blue_serum.add_trait(simple_aphrodesiac)

    $ red_serum = SerumDesign()
    $ red_serum.name = "Red Serum"
    $ red_serum.add_trait(improved_serum_prod)
    $ red_serum.add_trait(high_capacity_design)
    $ red_serum.add_trait(aphrodisiac)
    $ red_serum.add_trait(off_label_drugs)
    $ red_serum.add_trait(large_obedience_enhancer)

    $ purple_serum = SerumDesign()
    $ purple_serum.name = "Purple Serum"
    $ purple_serum.add_trait(improved_serum_prod)
    $ purple_serum.add_trait(off_label_drugs)
    $ purple_serum.add_trait(improved_duration_trait)

    "There's a knock on your door."
    $ the_person.draw_person()
    the_person "[the_person.mc_title], can I come in?"
    mc.name "Sure [the_person.title]."
    "[the_person.possessive_title] opens up your bedroom door. She's holding a dusty cardboard box."
    the_person "I was doing some tidying in the attic and found this. It has your name on it..."
    "She turns the other side to face you. \"[mc.name] - Serum Reserve DO NOT TOUCH\"."
    menu:
        "Snatch the box from her.":
            "You step close and grab at the box."
            mc.name "I can take that!"
            "She laughs and steps away, mistaking your worry for play."
            the_person "Oh? Hiding something away in here? Something you don't want your mother to see?"
            the_person "Am I about to find a stack of dirty magazines?"
            "She opens up the top of the box and looks inside."

        "Ask calmly for it.":
            mc.name "Oh, that. I can take that from you."
            "You step close and motion to take the box from her, but she holds onto it for a moment and opens the top of the box."

    the_person "What is all of this, anyways? A whole lot of glass..."
    mc.name "It's some... stuff from the university lab."
    the_person "[the_person.mc_title], were you stealing?"
    "You were."
    mc.name "No, of course not! It's stuff I... made. I didn't know it was still around. Can I have the box now?"
    "She pulls out one of the glass vials inside and holds it up to the light. It's a light blue"
    the_person "Is this the stuff you're making in your lab now?"
    mc.name "Sort of, yeah."
    the_person "Hmm... What does it do?"
    menu:
        "You should try it and find out.":
            mc.name "Drink it and find out. It's not harmful."
            the_person "Really? It's not a drug, is it?"
            mc.name "Everything's a drug, [the_person.title]. It won't get you high, if that's what you're asking."
            "She considers it, then shrugs and uncorks the top of the vial."
            the_person "I have to admit I am a little curious..."
            $ the_person.give_serum(blue_serum)
            "[the_person.possessive_title] drinks down the liquid and drops the empty vial back into the box."
            the_person "Well? Now what?"
            mc.name "You probably won't feel anything. The effects are subtle."
            the_person "But it's good for me?"
            mc.name "Yes [the_person.title], it's good for you."
            "She smiles happily and hands you the box full of old serum doses."


        "Nothing, really.":
            mc.name "Nothing, really. But it quite delicate, so if I could just have those..."
            the_person "Right, sorry."
            "She puts the vial back and hands the box to you."

    the_person "Now I'll get out of your way. Have a good day!"
    $ clear_scene()

    "She closes the door behind her, leaving you alone with your spoils. You had forgotten you stashed these away as an emergency reserve."
    "You dig through the box. Some vials are empty - maybe you used them, or they were never full to begin with."
    $ mc.inventory.change_serum(blue_serum, 6)
    $ mc.log_event("Found 6 doses of Blue Serum!", "float_text_blue")
    "You find a number of blue serum doses. Back in university they did a wonderful job of making girls slutty and influenceable."
    "Best to save them for when you have a specific boundary to push though, because they don't last very long."

    "You dig a little deeper. There are a few specialised doses of serum in here too."
    $ mc.inventory.change_serum(red_serum, 3)
    $ mc.log_event("Found 3 doses of Red Serum!", "float_text_blue")
    "Red serum. It was stronger than your Blue design, making girls slutty and obedient on the spot."
    "It was also particularly likely to make a girl suggestible after she climaxed."

    $ mc.inventory.change_serum(purple_serum, 3)
    $ mc.log_event("Found 3 doses of Purple Serum!", "float_text_blue")
    "And some Purple serum. It's a gentler, longer duration serum."
    "It didn't make girls any sluttier directly, but it gave you a lot of time to try and make them cum."
    "If you did you could usually put some very fun ideas in their heads."
    "Useful when you have the time and opportunity to focus on one girl in particular."


    "Of course you could always sell these doses at the office. Sometime soon you'll be able to recreate them and more anyways."
    "But maybe it's a good idea to hold onto them, in case you find any interesting opportunities to apply them."

    return
