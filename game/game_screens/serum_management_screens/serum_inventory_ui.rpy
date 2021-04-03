screen show_serum_inventory(the_inventory, extra_inventories = [],inventory_names = []): #You can now pass extra inventories, as well as names for all of the inventories you are passing. Returns nothing, but is used to view inventories.
    add "Science_Menu_Background.png"
    hbox:
        $ count = 0
        xalign 0.05
        yalign 0.05
        spacing 40
        for an_inventory in [the_inventory] + extra_inventories:
            frame:
                background "#888888"
                xsize 400
                vbox:
                    xalign 0.02
                    yalign 0.02
                    if len(inventory_names) > 0 and count < len(inventory_names):
                        text inventory_names[count] style "menu_text_style" size 25
                    else:
                        text "Serums in Inventory" style "menu_text_style" size 25

                    default selected_serum = None
                    for design in an_inventory.serums_held:
                        if design == selected_serum:
                            textbutton design[0].name + ": " + str(design[1]) + " Doses":
                                style "textbutton_style" text_style "textbutton_text_style"
                                action [SetScreenVariable("selected_serum", None), Hide("serum_tooltip")]
                                sensitive True
                                #hovered Show("serum_tooltip",None,design[0])
                                background "#666666"
                        else:
                            textbutton design[0].name + ": " + str(design[1]) + " Doses":
                                style "textbutton_style" text_style "textbutton_text_style"
                                action SetScreenVariable("selected_serum", design)
                                sensitive True
                                hovered [SetScreenVariable("selected_serum", None), Show("serum_tooltip", None, design[0], given_anchor = (1.0,0.0), given_align = (0.95,0.05))]
                                unhovered Hide("serum_tooltip")
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
