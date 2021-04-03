label wardrobe_import():
    $ list_of_xml_files = []
    # Build a list of all possible files inside of the imports file.
    python:
        file_path = os.path.abspath(os.path.join(config.basedir, "game"))
        file_path = os.path.join(file_path,"wardrobes")
        file_path = os.path.join(file_path,"imports")
        for file_name in os.listdir(file_path):
            if file_name[-4:] == ".xml":
                list_of_xml_files.append((file_name, file_name))

    if not list_of_xml_files:
        "No files found. Place wardrobe XML files inside of games/wardrobes/imports to make them available for importing."
        return

    $ list_of_xml_files.append(("None","None")) #Provide a way to cancel
    "Select a wardrobe file to import:"

    $ chosen_filename = renpy.display_menu(list_of_xml_files) #Get the player to choose a list
    if chosen_filename is "None":
        return

    $ the_wardrobe = wardrobe_from_xml(chosen_filename[:-4], in_import = True)
    $ mc.designed_wardrobe = mc.designed_wardrobe.merge_wardrobes(the_wardrobe, keep_primary_name = True)


    # Some file cleanup so they don't exist in memory for the rest of the game.
    $ list_of_xml_files = []
    $ the_wardrobe = None

    "Wardrobe imported."
    return
