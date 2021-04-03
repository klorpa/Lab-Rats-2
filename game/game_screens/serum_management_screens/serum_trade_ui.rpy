screen serum_trade_ui(inventory_1,inventory_2,name_1="Player",name_2="Business"): #Lets you trade serums back and forth between two different inventories. Inventory 1 is assumed to be the players.
    modal True
    add "Science_Menu_Background.png"
    frame:
        background "#888888"
        xalign 0.5
        xanchor 0.5
        yalign 0.1
        ysize 800
        vbox:
            yalign 0.0
            spacing 20
            text "Trade Serums Between Inventories." style "menu_text_style" size 25 xalign 0.5 xanchor 0.5
            for serum in set(inventory_1.get_serum_type_list()) | set(inventory_2.get_serum_type_list()): #Gets a unique entry for each serum design that shows up in either list. Doesn't duplicate if it's in both.
                # has a few things. 1) name of serum design. 2) count of first inventory, 3) arrows for transfering, 4) count of second inventory.
                frame:
                    background "#777777"
                    xalign 0.5
                    xanchor 0.5
                    yalign 0.0
                    yanchor 0.0
                    vbox:
                        xalign 0.5
                        xanchor 0.5
                        xsize 600

                        hbox:
                            textbutton serum.name + ": " style "textbutton_style" text_style "menu_text_style" action NullAction() hovered Show("serum_tooltip",None,serum, given_align = (0.02,0.02)) unhovered Hide("serum_tooltip") #displays the name of this particular serum
                            null width 10
                            text name_1 + "\nhas: " + str(inventory_1.get_serum_count(serum)) style "menu_text_style"#The players current inventory count. 0 if there is nothing in their inventory
                            textbutton "|<" action [Function(inventory_1.change_serum,serum,inventory_2.get_serum_count(serum)),Function(inventory_2.change_serum,serum,-inventory_2.get_serum_count(serum))] sensitive (inventory_2.get_serum_count(serum) > 0) style "textbutton_style" text_style "textbutton_text_style"
                            textbutton "<<" action [Function(inventory_1.change_serum,serum,5),Function(inventory_2.change_serum,serum,-5)] sensitive (inventory_2.get_serum_count(serum) > 4) style "textbutton_style" text_style "textbutton_text_style"
                            textbutton "<" action [Function(inventory_1.change_serum,serum,1),Function(inventory_2.change_serum,serum,-1)] sensitive (inventory_2.get_serum_count(serum) > 0) style "textbutton_style" text_style "textbutton_text_style"
                            #When pressed, moves 1 serum from the business inventory to the player. Not active if the business has nothing in it.
                            null width 10
                            textbutton ">" action [Function(inventory_2.change_serum,serum,1),Function(inventory_1.change_serum,serum,-1)] sensitive (inventory_1.get_serum_count(serum) > 0) style "textbutton_style" text_style "textbutton_text_style"
                            textbutton ">>" action [Function(inventory_2.change_serum,serum,5),Function(inventory_1.change_serum,serum,-5)] sensitive (inventory_1.get_serum_count(serum) > 4) style "textbutton_style" text_style "textbutton_text_style"
                            textbutton ">|" action [Function(inventory_2.change_serum,serum,inventory_1.get_serum_count(serum)),Function(inventory_1.change_serum,serum,-inventory_1.get_serum_count(serum))] sensitive (inventory_1.get_serum_count(serum) > 0) style "textbutton_style" text_style "textbutton_text_style"
                            text name_2 + "\nhas: " + str(inventory_2.get_serum_count(serum)) style "menu_text_style"


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
        textbutton "Return" align [0.5,0.5] text_style "return_button_style"
