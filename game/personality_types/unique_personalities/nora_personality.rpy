### PERSONALITY CHARACTERISTICS ###
init 1300:
    python:
        def nora_titles(the_person):
            valid_titles = [the_person.name]
            return valid_titles

        def nora_possessive_titles(the_person):
            valid_titles = [the_person.name]
            valid_titles.append("Your old boss")
            return valid_titles

        def nora_player_titles(the_person):
            valid_titles = [mc.name]
            return valid_titles

        nora_personality = Personality("nora", default_prefix = "reserved",
        common_likes = ["pants", "working", "research work", "classical"],
        common_sexy_likes = ["vaginal sex", "skimpy uniforms", "lingerie", "masturbating"],
        common_dislikes = ["heavy metal", "HR work", "marketing work", "sports"],
        common_sexy_dislikes = ["not wearing anything", "not wearing underwear", "being submissive", "creampies"],
        titles_function = nora_titles, possessive_titles_function = nora_possessive_titles, player_titles_function = nora_player_titles,
        insta_chance = 0, dikdok_chance = 0)
