# Contains functions that receive a Person, String and return a modified String based.
#NOTE: None of this is currently used
init -3 python:
    def test_modifier(Person, what): #Note: we need to make sure we properly preserve text mark ups.
        return what + " | it worked! |"


    def gagged_speach(Person, what):
        #TODO: We need to make sure we strip the text of notational stuff before we start modifying it (and then add it in after).
        modified_response = what #TODO: We still need to work on stripping out the existing modifiers and preserving them somehow.
        #Gagged characters can't make plosive sounds. Now I only wish english was written with proper phonetics!

        for plosive in ["th", "ch", "ca", "p", "b", "t", "d", "k", "g", "x"]:
            if len(plosive) == 1:
                modified_response = modified_response.replace(plosive, ">>") #This approach defines some special characters taht will mess things up if theyre included, we should probably avoid that
                modified_response = modified_response.replace(plosive.capitalize(), "^^") #Catches plosives at the start of a sentence or in a proper noun
            else:
                modified_response = modified_response.replace(plosive, ">>>") #This approach defines some special characters taht will mess things up if theyre included, we should probably avoid that
                modified_response = modified_response.replace(plosive.capitalize(), "^>>")

        split_list = modified_response.split()
        return_response = ""
        for word in split_list: #We need to be able to scan forwards and backwards in the list.
            for count, letter in enumerate(word):
                if letter == ">":
                    return_response += gagged_speach_get_letter(word, count).lower()

                elif letter == "^":
                    return_response += gagged_speach_get_letter(word, count).upper()

                else:
                    return_response += letter

            if word == split_list[-1]:
                pass
            else:
                return_response += " "

        return return_response

    def gagged_speach_get_letter(word, position):
        print("Trying: " + word + " at position " + str(position))
        for scan_position in range(position, -1, -1):
            if word[scan_position].isalpha():
                return word[scan_position]

        for scan_position in range(position, len(word)-1):
            if word[scan_position].isalpha():
                return word[scan_position]

        return "ugh"



        #TOOD: Scan left of position until we hit a non-special character and return that.
        #TODO: If we don't run into anything, scan right until we hit a non-special character and return that.
        #TODO: If neither of those work replace it with "ugh"

    # "What can I do?"
    # "Whaa aaan I ooo?"
    # "Whaaa aaan I ooo?"
    # "What the fuck"
    # "Whaaa eeee "
    # "What ugh fuck


    # NOTE: This partial work is no longer needed thanks to the awesome tag library I was able to find.
    # def aroused_text_wiggle(tag, argument, contents):
    #     return_value = []
    #     for kind, text in contents:
    #         if kind == renpy.TEXT_TEXT:
    #             for i in range(0, len(text)):
    #                 letter = text[i]
    #                 variation = renpy.random.Random(i + ord(letter)) * 6.28 #Offsets the time of each letter by up to 1 rotation (2*pi), but keeps it consistent based on position and letter, so it only varies with time going forward.
    #                 amount = argument * sin(time.time() + variation)
    #                 rv.append(aroused_text_wiggle_transform(letter, amount, kind)))
    #         else:
    #             rv.append((kind, text))
    #
    #     return return_value
    #     # Argument is the displacement of the text allowed in pixels.
    #
    #
    # def text_move_transform(s, amount, kind): #Moves the text the amount pixels up (negative is down).
    #     text_return = []
    #     text_return.append(renpy.TEXT_TAG, "
    #     return text_return
