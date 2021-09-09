init -1 python:
    def get_obedience_plaintext(obedience_amount):
        obedience_string = "ERROR - Please Tell Vren!"
        if obedience_amount < 50: #49 or less
            obedience_string = "Completely Wild"

        elif obedience_amount < 70: #50 to 69
            obedience_string = "Disobedient"

        elif obedience_amount < 95: #70 to 94
            obedience_string = "Free Spirited"

        elif obedience_amount < 105: #95 to 104
            obedience_string = "Respectful"

        elif obedience_amount < 130: #105 to 129
            obedience_string = "Loyal"

        elif obedience_amount < 150: #130 to 149
            obedience_string = "Docile"

        else: #150 or more
            obedience_string = "Subservient"

        return obedience_string

    def format_titles(the_person):
        person_title = the_person.title
        if person_title is None:
            person_title = "???"
        return_title = "{color=" + the_person.char.who_args["color"] + "}" + "{font=" + the_person.char.what_args["font"] + "}" + person_title + "{/font}{/color}"
        return return_title

    def opinion_score_to_string(the_score): #Takes an opinion score and puts it into a plain string.
        if the_score == -2:
            return "hates"

        elif the_score == -1:
            return "dislikes"

        elif the_score == 0:
            return "has no opinion on"

        elif the_score == 1:
            return "likes"

        else: #the_score == 2:
            return "loves"

    def SO_relationship_to_title(relationship_string): #Takes a character relationship (Girlfriend, Fiancée, Married) and returns the male equivalent
        if relationship_string == "Girlfriend":
            return "boyfriend"
        elif relationship_string == "Fiancée":
            return "fiancé"
        elif relationship_string == "Married":
            return "husband"
        else:
            return "ERROR - relationship incorrectly defined"

    def girl_relationship_to_title(relationship_string):
        if relationship_string == "Girlfriend":
            return "girlfriend"
        elif relationship_string == "Fiancée":
            return "fiancée"
        elif relationship_string == "Married":
            return "wife"
        else:
            return "ERROR - relationship incorrectly defined"

    def height_to_string(the_height): #Height is a value between 0.9 and 1.0 which corisponds to 5' 0" and 5' 10"
        rounded_height = __builtin__.round(the_height,2) #Round height to 2 decimal points.
        if rounded_height >= 1.00:
            return "5' 10\""
        elif rounded_height == 0.99:
            return "5' 9\""
        elif rounded_height == 0.98:
            return "5' 8\""
        elif rounded_height == 0.97:
            return "5' 7\""
        elif rounded_height == 0.96:
            return "5' 6\""
        elif rounded_height == 0.95:
            return "5' 5\""
        elif rounded_height == 0.94:
            return "5' 4\""
        elif rounded_height == 0.93:
            return "5' 3\""
        elif rounded_height == 0.92:
            return "5' 2\""
        elif rounded_height == 0.91:
            return "5' 1\""
        elif rounded_height <= 0.90:
            return "5' 0\""
        else:
            return "Problem, height not found in chart."


    def remove_punctuation(the_text):
        #TODO: might need to cast unicode to string/aski
        return re.sub("[.,!;\"']", "", the_text)
        # tbl = dict.fromkeys(i for i in xrange(sys.maxunicode)
        #   if unicodedata.category(unichr(i)).startswith('P'))
        # return text.translate(tbl)
