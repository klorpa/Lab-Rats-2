init -1:
    define house_background = Image("Home_Background.png")
    define house_background_dark = Image("Home_Background_Dark.png")

    define apartment_background = Image("Apartment_Lobby.png")

    define bedroom_background = Image("Bedroom_1.png")
    define bedroom_background_dark = Image("Bedroom_1_Dark.png")

    define home_bathroom_background = Image("Home_Bathroom_Background.png")

    define kitchen_background = Image("Kitchen_1.png")
    define kitchen_background_dark = Image("Kitchen_Dark.png")

    define mall_background = Image("Mall_Background.png")
    define mall_background_dark = Image("Mall_Background_Dark.png")

    define lab_background = Image("Lab_Background.png")

    define office_background = Image("Office_Background.png")
    define office_background_dark = Image("Office_Background_Dark.png")

    define outside_background = Image("Outside_Background.png")
    define outside_background_dark = Image("Outside_Background_Dark.png")

    define bar_background = Image("Bar_Background.png")
    define stripclub_background = Image("Club_Background.png")

    define campus_background = Image("Campus.png")
    define campus_background_dark = Image("Campus_dark.png")

    define restaraunt_background = Image("Restaraunt_Background.png")

    define theater_background = Image("Theater_Background.png")

    define bathroom_background = Image("Bathroom_Background.png")

    image bg science_menu_background = Image("Science_Menu_Background.png")
    image bg paper_menu_background = Image("Paper_Background.png")

    python: #Some standard background progressions we can use throughout the game. Generally should be copied (use the [:] slice operator to copy the list)
        standard_bedroom_backgrounds = [bedroom_background_dark, bedroom_background, bedroom_background, bedroom_background, bedroom_background_dark]
        standard_house_backgrounds = [house_background_dark, house_background, house_background, house_background, house_background_dark]
        standard_kitchen_backgrounds = [kitchen_background_dark, kitchen_background, kitchen_background, kitchen_background, kitchen_background_dark]
        standard_downtown_backgrounds = [outside_background_dark, outside_background, outside_background, outside_background, outside_background_dark]
        standard_mall_backgrounds = [mall_background_dark, mall_background, mall_background, mall_background, mall_background_dark]
        standard_office_backgrounds = [office_background_dark, office_background, office_background, office_background, office_background_dark]
        standard_campus_backgrounds = [campus_background_dark, campus_background, campus_background, campus_background, campus_background_dark]

        standard_bar_backgrounds = [bar_background, bar_background, bar_background, bar_background, bar_background]

        #lighting_format = [[r,g,b],[r,g,b],[r,g,b],[r,g,b],[r,g,b]]
        standard_indoor_lighting = [[0.91,0.91,0.95],[0.98,0.98,0.98],[0.98,0.98,0.98],[0.98,0.98,0.98],[0.91,0.91,0.95]]
        standard_outdoor_lighting = [[0.7,0.7,0.8],[1,1,1],[1,1,1],[1,1,1],[0.7,0.7,0.8]]
        standard_club_lighting = [[0.8,0.8,0.9], [0.8,0.8,0.9], [0.8,0.8,0.9], [0.8,0.8,0.9], [0.8,0.8,0.9]]

        dark_lighting = [[0.4,0.4,0.55],[0.4,0.4,0.55],[0.4,0.4,0.55],[0.4,0.4,0.55],[0.4,0.4,0.55]]
