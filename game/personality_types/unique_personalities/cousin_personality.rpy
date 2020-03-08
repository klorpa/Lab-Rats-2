### PERSONALITY CHARACTERISTICS ###
init 1300:
    python:
        def cousin_titles(the_person):
            valid_titles = []
            valid_titles.append(the_person.name)
            if the_person.love > 20:
                valid_titles.append("Cuz")

            if the_person.love < -30:
                valid_titles.append("Hellspawn")
            return valid_titles

        def cousin_possessive_titles(the_person):
            valid_possessive_titles = []
            valid_possessive_titles.append(the_person.name)
            valid_possessive_titles.append("Your cousin")
            if the_person.love > 20:
                valid_possessive_titles.append("Your cuz")

            if the_person.love < -30:
                valid_possessive_titles.append("Your bitchy cousin")

            if the_person.sluttiness > 40:
                valid_possessive_titles.append("Your cock-goth cousin")

            return valid_possessive_titles

        def cousin_player_titles(the_person):
            valid_player_titles = []
            valid_player_titles.append(mc.name)
            if the_person.love < -20:
                valid_player_titles.append("Asshat")
                valid_player_titles.append("Dickwad")
                valid_player_titles.append("Dick-for-brains")

            if the_person.love > 20:
                valid_player_titles.append("Cuz")

            if the_person.love < 0 and the_person.sluttiness > 40:
                valid_player_titles.append("Dildo")

                if the_person.obedience < 20:
                    valid_player_titles.append("Cock slave")
                    valid_player_titles.append("Slave")
            return valid_player_titles

        cousin_personality = Personality("cousin", default_prefix = "introvert",
            common_likes = ["the colour black","heavy metal","punk","makeup","skimpy outfits"],
            common_sexy_likes = ["lingerie","masturbating","taking control","getting head"],
            common_dislikes = ["small talk","flirting","working"],
            common_sexy_dislikes = ["kissing", "giving blowjobs", "bareback sex"],
            titles_function = cousin_titles, possessive_titles_function = cousin_possessive_titles, player_titles_function = cousin_player_titles)

### DIALOGUE ###
## Taboo break dialogue ##
# label cousin_kissing_taboo_break(the_person):
#
#     return
#
# label cousin_touching_body_taboo_break(the_person):
#
#     return
#
# label cousin_touching_penis_taboo_break(the_person):
#
#     return
#
# label cousin_touching_vagina_taboo_break(the_person):
#
#     return
#
# label cousin_sucking_cock_taboo_break(the_person):
#
#     return
#
# label cousin_licking_pussy_taboo_break(the_person):
#
#     return
#
# label cousin_vaginal_sex_taboo_break(the_person):
#
#     return
#
# label cousin_anal_sex_taboo_break(the_person):
#
#     return
#
# label cousin_condomless_sex_taboo_break(the_person):
#
#     return
#
# label cousin_underwear_nudity_taboo_break(the_person, the_clothing):
#
#     return
#
# label cousin_bare_tits_taboo_break(the_person, the_clothing):
#
#     return
#
# label cousin_bare_pussy_taboo_break(the_person, the_clothing):
#
#     return
#
# label cousin_facial_cum_taboo_break(the_person):
#
#     return
#
# label cousin_mouth_cum_taboo_break(the_person):
#
#     return
#
# label cousin_body_cum_taboo_break(the_person):
#
#     return
#
# label cousin_creampie_taboo_break(the_person):
#
#     return
#
# label cousin_anal_creampie_taboo_break(the_person):
#
#     return
