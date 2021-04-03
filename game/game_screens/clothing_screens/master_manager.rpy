#Not technically a screen, but critical for managing proper access to all of the other screens.
label outfit_master_manager(*args, **kwargs): #New outfit manager that centralizes exporting, modifying, duplicating, and deleting. Call this and pass any args/kwargs that would normally be passed to outfit_creator.
    call screen outfit_select_manager(*args, **kwargs)

    if _return == "No Return":
        return None #We're done and want to leave.

    $ outfit_type = None
    $ outfit = None
    $ slut_limit = kwargs.get("slut_limit", None)
    if _return == "new_full":
        $ outfit_type = "full"
        call screen outfit_creator(Outfit("New Outfit"), outfit_type = outfit_type, slut_limit = slut_limit)
        $ outfit = _return

    elif _return == "new_over":
        $ outfit_type = "over"
        call screen outfit_creator(Outfit("New Overwear Set"), outfit_type = outfit_type, slut_limit = slut_limit)
        $ outfit = _return

    elif _return == "new_under":
        $ outfit_type = "under"
        call screen outfit_creator(Outfit("New Underwear Set"), outfit_type = outfit_type, slut_limit = slut_limit)
        $ outfit = _return


    elif isinstance(_return, list):
        #If we are returning an outfit we should be in one of the three sets (if not: panic!)
        $ command = _return[0]
        $ outfit = _return[1]

        if command == "select":
            return outfit

        elif outfit in mc.designed_wardrobe.outfits:
            $ outfit_type = "full"

        elif outfit in mc.designed_wardrobe.overwear_sets:
            $ outfit_type = "over"

        elif outfit in mc.designed_wardrobe.underwear_sets:
            $ outfit_type = "under"

        else:
            "We couldn't find it anywhere! PANIC!"

        $ mc.designed_wardrobe.remove_outfit(outfit) # Remove it so we can re-add it later. Note that "dupicate" has already copied an outfit and added it so we can re-use this code.

        call screen outfit_creator(outfit, outfit_type = outfit_type, slut_limit = slut_limit)
        $ outfit = _return

    if not outfit == "Not_New":
        $ new_outfit_name = renpy.input("Please name this outfit.", default = outfit.name)
        while new_outfit_name == "":
            $ new_outfit_name = renpy.input("Please enter a non-empty name.", default = outfit.name)


        $ mc.save_design(outfit, new_outfit_name, outfit_type)

    call outfit_master_manager(*args, **kwargs) from _call_outfit_master_manager #Loop around until the player decides they want to leave.
    return _return
