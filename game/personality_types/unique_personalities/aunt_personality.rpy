### PERSONALITY CHARACTERISTICS ###
init 1300:
    python:
        def aunt_titles(the_person):
            valid_titles = []
            valid_titles.append(the_person.name)
            valid_titles.append("Aunt " + the_person.name)
            if the_person.love > 20:
                valid_titles.append("Auntie")
            return valid_titles

        def aunt_possessive_titles(the_person):
            valid_possessive_titles = []
            valid_possessive_titles.append(the_person.name)
            valid_possessive_titles.append("Your aunt")

            if the_person.love > 20:
                valid_possessive_titles.append("Your loving aunt")


            if the_person.love > 40 and the_person.sluttiness > 60:
                valid_possessive_titles.append("Your personal MILF")

            if the_person.sluttiness > 100:
                valid_possessive_titles.append("Your cock hungry aunt")
                valid_possessive_titles.append("Your cumdump aunt")

            return valid_possessive_titles

        def aunt_player_titles(the_person):
            valid_player_titles = []
            valid_player_titles.append(mc.name)

            if the_person.love > 20:
                valid_player_titles.append("Sweetheart")
                valid_player_titles.append("Sweety")
            return valid_player_titles

        aunt_personality = Personality("aunt", default_prefix = "wild",
            common_likes = ["small talk", "the colour pink", "makeup", "flirting"],
            common_sexy_likes = ["lingerie", "skimpy outfits", "taking control"],
            common_dislikes = ["working", "hiking", "conservative outfits"],
            common_sexy_dislikes = ["public sex", "masturbating", "being fingered", "cheating on men"],
            titles_function = aunt_titles, possessive_titles_function = aunt_possessive_titles, player_titles_function = aunt_player_titles)

label aunt_sex_beg_finish(the_person):
    "Wait, I really need this [the_person.mc_title]! You're making me feel like a real women, please don't stop! Please!"
    return

## Taboo break dialogue ##
# label aunt_kissing_taboo_break(the_person):
#
#     return
#
# label aunt_touching_body_taboo_break(the_person):
#
#     return
#
# label aunt_touching_penis_taboo_break(the_person):
#
#     return
#
# label aunt_touching_vagina_taboo_break(the_person):
#
#     return
#
# label aunt_sucking_cock_taboo_break(the_person):
#
#     return
#
# label aunt_licking_pussy_taboo_break(the_person):
#
#     return
#
# label aunt_vaginal_sex_taboo_break(the_person):
#
#     return
#
# label aunt_anal_sex_taboo_break(the_person):
#
#     return
#
# label aunt_condomless_sex_taboo_break(the_person):
#
#     return
#
# label aunt_underwear_nudity_taboo_break(the_person, the_clothing):
#
#     return
#
# label aunt_bare_tits_taboo_break(the_person, the_clothing):
#
#     return
#
# label aunt_bare_pussy_taboo_break(the_person, the_clothing):
#
#     return
#
# label aunt_facial_cum_taboo_break(the_person):
#
#     return
#
# label aunt_mouth_cum_taboo_break(the_person):
#
#     return
#
# label aunt_body_cum_taboo_break(the_person):
#
#     return
#
# label aunt_creampie_taboo_break(the_person):
#
#     return
#
# label aunt_anal_creampie_taboo_break(the_person):
#
#     return
