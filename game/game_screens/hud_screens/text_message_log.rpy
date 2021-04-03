screen text_message_log(the_person, newest_who = None, newest_what = None):
    fixed:
        xanchor 0.5
        xalign 0.5
        frame:
            background Frame("LR2_Phone_Text.png", 0,0,0,0)
            xanchor 0.5
            xalign 0.5
            yanchor 1.0
            yalign 1.0
            xsize 740
            ysize 940

        viewport: #The display for the text, which can be scrolled up and down.
            xalign 0.5 #X position on the screen
            yalign 0.905 #Y position of the top of the phone
            xanchor 0.5
            yanchor 1.0
            mousewheel True
            scrollbars "vertical"
            xsize 660
            ysize 690
            yinitial 1.0
            vbox:
                box_reverse False
                xanchor 0.5
                xalign 0.5
                spacing 10
                yanchor 1.0
                yalign 1.0


                $ display_who = ""
                $ display_what = ""
                $ who_align = 0.0
                $ what_align = 1.0
                $ history_list = mc.phone.get_message_list(the_person)
                $ display_list = []
                for item in history_list:
                    $ display_tuple = [item.who, item.what]
                    $ display_list.append(display_tuple)

                if newest_what is not None:
                    $ display_list.append([newest_who, newest_what])


                for history_item in display_list:
                    $ log_who = history_item[0]
                    $ log_what = history_item[1]

                    frame: #TODO: Add support for system messages (ie. in-phone narration)
                        padding (15,15)
                        if log_who == mc.name:
                            background Frame("LR2_Text_Bubble.png", 26, 6, 26, 6)
                        elif log_who is None:
                            background Frame("LR2_Text_Bubble_System.png", 26, 6, 26, 6)
                        else:
                            background Frame("LR2_Text_Bubble_Girl.png", 26, 6, 26, 6)

                        hbox:
                            xsize 600
                            if log_who == mc.name:
                                box_reverse True
                                $ display_who = mc.name
                                $ display_what = log_what
                                $ who_align = 1.0
                                $ what_align = 0.0
                            elif log_who is None:
                                $ what_align = 0.5
                                $ display_what = log_what
                            else:
                                box_reverse False
                                $ display_who = mc.having_text_conversation.create_formatted_title(log_who)
                                $ display_what = log_what
                                $ who_align = 0.0
                                $ what_align = 1.0

                            if log_who is not None:
                                text display_who xsize 75 text_align who_align xalign who_align yalign 0.0 yanchor 0.0 size 22 style "digital_text"
                            text display_what text_align what_align xalign what_align yalign 0.0 yanchor 0.0 xsize 570 xfill True style "digital_text"
