screen show_serum_inventory(the_inventory, extra_inventories = [],inventory_names = []): #You can now pass extra inventories, as well as names for all of the inventories you are passing. Returns nothing, but is used to view inventories.
    add "Science_Menu_Background.png"

    hbox:
        $ count = 0
        spacing 40
        xalign 0.05
        yalign 0.2
        for an_inventory in [the_inventory] + extra_inventories:
            frame:
                background "#888888"
                xsize 600
                viewport:
                    xsize 610
                    ysize 800
                    xalign 0.05
                    yalign 0.05
                    scrollbars "vertical"
                    mousewheel True
                    vbox:
                        xalign 0.02
                        yalign 0.02
                        if len(inventory_names) > 0 and count < len(inventory_names):
                            text inventory_names[count] style "menu_text_style" size 25
                        else:
                            text "Serums in Inventory" style "menu_text_style" size 25

                        default selected_serum = None
                        for design in sorted(an_inventory.serums_held, key=lambda a_serum: a_serum[0].name):
                            use serum_design_menu_item(design[0], name_addition = ": " + str(design[1]) + " Doses")
                $ count += 1

    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action Return()
        textbutton "Return" align [0.5,0.5] style "return_button_style" text_style "return_button_style"
