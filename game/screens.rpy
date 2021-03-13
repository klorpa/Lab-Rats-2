################################################################################
## Initialization
################################################################################

init offset = -1


################################################################################
## Styles
################################################################################

style default:
    font gui.default_font
    size gui.text_size
    color gui.text_color

style input is prompt_text:
    outlines [(3,"#222222",0,0)]

style hyperlink_text:
    color gui.accent_color
    hover_color gui.hover_color
    hover_underline True


style gui_text:
    font gui.interface_font
    color gui.interface_text_color
    size gui.interface_text_size
    yanchor 0.0


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.button_text_properties("button")
    yalign 0.5


style label_text is gui_text:
    color gui.accent_color
    size gui.label_text_size

style prompt_text is gui_text:
    color gui.text_color
    size gui.interface_text_size


style bar:
    ysize gui.bar_size
    left_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    unscrollable "hide"
    xsize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    ysize gui.slider_size
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/slider/horizontal_[prefix_]thumb.png"

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"


style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)



################################################################################
## In-game screens
################################################################################


## Say screen ##################################################################
##
## The say screen is used to display dialogue to the player. It takes two
## parameters, who and what, which are the name of the speaking character and
## the text to be displayed, respectively. (The who parameter can be None if no
## name is given.)
##
## This screen must create a text displayable with id "what", as Ren'Py uses
## this to manage text display. It can also create displayables with id "who"
## and id "window" to apply style properties.
##
## https://www.renpy.org/doc/html/screen_special.html#say

screen say(who, what, vren_test = None):
    $ show_phone = False #If True the phone is shown. If having a text conversation with "who" then that message is displayed on the phone. The say window has priority on displaying dialogue.
    $ show_say_window = True #If True the say window is shown. If also showing the phone this will be on top, and is for narration or dialogue with other characters.

    if hasattr(store,"mc"):
        if mc.having_text_conversation is not None:
            $ show_phone = True
            if who is None: #Narration is always shown in the normal say window
                $ show_say_window = True
            elif mc.text_conversation_paused: #And dialogue can be shown as normal by setting this to True
                $ show_say_window = True
            else: #Otherwise we're talking via text, don't show the menu.
                $ show_say_window = False



        #     if show_phone and mc.override_phone:
        #         $ show_say_window
        #
        # if mc.hide_say_window:
        #     $ show_say_window = False
        #     $ show_phone = mc.having_text_conversation is not None


    if show_phone:
        if show_say_window:
            use text_message_log(mc.having_text_conversation) #We're displaying narration or non-texting dialogue, so just display the history
        else:
            use text_message_log(mc.having_text_conversation, who, what) #Pass it the current message to display it

        window: #NOTE: This whole section is invisible, but is needed to satisfy Ren'py's need to have something with the "what" id.
            at transform:
                alpha 0.0
            xalign 2.5 #Just shove it all off the screen, in case it renders not-invisible at some point
            id "window"
            background None
            text what id "what"
            if who is not None:
                window:
                    text who id "who"

    if show_say_window:
        style_prefix "say"
        window:
            id "window"
            if vren_test is not None:
                text vren_test id "what"
            else:
                text what id "what"

            if who is not None:
                window:
                    style "namebox"
                    text who id "who"

        # If there's a side image, display it above the text. Do not display
        # on the phone variant - there's no room.
        if not renpy.variant("small"):
            add SideImage() xalign 0.0 yalign 1.0

style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label


style window:
    xalign 0.55
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Image("gui/textbox.png", xalign=0.55, yalign=1.0)

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style say_label:
    color gui.accent_color
    font gui.name_font
    size gui.name_text_size
    xalign gui.name_xalign
    yalign 0.5
    outlines [(2,"#222222",0,0)]

style say_dialogue:
    xpos gui.text_xpos
    xanchor gui.text_xalign
    xsize gui.text_width
    ypos gui.text_ypos
    first_indent 50
    outlines [(2,"#222222",0,0)]

    text_align gui.text_xalign
    layout ("subtitle" if gui.text_xalign else "tex")


## Input screen ################################################################
##
## This screen is used to display renpy.input. The prompt parameter is used to
## pass a text prompt in.
##
## This screen must create an input displayable with id "input" to accept the
## various input parameters.
##
## http://www.renpy.org/doc/html/screen_special.html#input

screen input(prompt):
    style_prefix "input"

    window:

        vbox:
            xpos gui.text_xpos
            xanchor gui.text_xalign
            ypos gui.text_ypos

            text prompt style "input_prompt"
            input id "input"


style input_prompt is default

style input_prompt:
    xmaximum gui.text_width
    xalign gui.text_xalign
    text_align gui.text_xalign
    outlines [(2,"#222222",0,0)]

style input:
    xmaximum gui.text_width
    xalign gui.text_xalign
    text_align gui.text_xalign

## Choice screen ###############################################################
##
## This screen is used to display the in-game choices presented by the menu
## statement. The one parameter, items, is a list of objects, each with caption
## and action fields.
##
## http://www.renpy.org/doc/html/screen_special.html#choice

init -2 python:
    def call_formated_action_choice(the_actions):
    #This formats a list of text and actions properly so the Choice screen will display everything the way we want.
    # This is handing a list of actions OR simple strings. Actions will be tested to determine which state they pass to the choice screen. Strings are passed directly.
    # The answer from the choice screen is returned.
        valid_actions_list = [] #A list of tuples, the tag to be shown and the thing to be returned.
        for act in the_actions:
            if isinstance(act, basestring):
                valid_actions_list.append([act,act]) #If it's just a string it is it's own return value.
            else: #It's either an action or a list of [action, extra_args].
                extra_args = []
                if isinstance(act, list):
                    extra_args = act[1] #second part of list, which is itself a list of extra parameters.
                    act = act[0] #rename it so the rest works properly.

                display_name = ""
                display = False
                if act.is_action_enabled(extra_args):
                    display_name = act.name
                    display = True
                elif act.is_disabled_slug_shown(extra_args):
                    display_name = act.get_disabled_slug_name(extra_args)
                    display = True

                if act.menu_tooltip:
                    display_name += " (tooltip)" + act.menu_tooltip

                if display:
                    valid_actions_list.append([display_name, act]) #Return value shouldn't matter, since it should be disabled.

        act_choice = renpy.display_menu(valid_actions_list,True,"Choice")
        return act_choice #We've shown the screen and the player picked something. return that to them.

screen main_choice_display(elements_list, draw_hearts_for_people = True, draw_person_previews = True, person_preview_args = None): #Elements_list is a list of lists, with each internal list recieving an individual column
    #The first element in a column should be the title, either text or a displayable. After that it should be a tuple of (displayable/text, return_value).
    #[["Title",["Item",Return] ]]


    hbox:
        spacing 10
        xalign 0.518
        yalign 0.2
        xanchor 0.5
        yanchor 0.0
        for count in __builtin__.range(len(elements_list)):
            frame:
                background "gui/LR2_Main_Choice_Box.png"
                xsize 380
                ysize 700
                $ title_element = elements_list[count][0]
                if isinstance(title_element, basestring):
                    text title_element xalign 0.5 ypos 45 anchor (0.5,0.5) size 26 style "menu_text_style" xsize 200
                else:
                    add title_element xalign 0.5 ypos 45 anchor (0.5,0.5)


                $ column_elements = elements_list[count][1:]
                viewport id title_element:
                    #scrollbars "vertical" #But if we aren't on a PC we need to make sure the player can scroll since they won't have a mouse wheel.

                    mousewheel True
                    xalign 0.5
                    xanchor 0.5
                    yanchor 0.0

                    ypos 99
                    xsize 360
                    ysize 588
                    vbox:
                        for item in column_elements:

                            #Key values we want to know about to display our text button.
                            $ title = ""
                            $ return_value = None

                            $ hovered_list = []
                            $ unhovered_list = []
                            $ the_tooltip = None
                            $ extra_args = None

                            $ display = True
                            $ is_sensitive = True

                            if isinstance(item,list): #It's a title/return value pair. Show the title, return the value.
                                if isinstance(item[0], Action): #It's an action with extra arguments.
                                    $ extra_args = item[1]
                                    $ item = item[0] #Rename item so that this is caught by the action section below.

                                else: #It's (probably) a title/return string pair. Show the title, return the value
                                    $ title = item[0]
                                    $ return_value = item[1]

                            if isinstance(item,Person): #It's a person. Format it for a person list.
                                $ title = format_titles(item)
                                $ return_value = item

                                if draw_hearts_for_people:
                                    $ title += "\n"
                                    $ title += get_heart_image_list(item)

                                if person_preview_args is None:
                                    $ person_preview_args = {}

                                if draw_person_previews:
                                    $ person_displayable = item.build_person_displayable(lighting = mc.location.get_lighting_conditions(), **person_preview_args)
                                    #$ hovered_list.append(Function(item.draw_person, **person_preview_args))
                                    $ hovered_list.append(Function(renpy.show, item.name, at_list=[character_right, scale_person(item.height)],layer="solo",what=person_displayable,tag=item.name))
                                    $ unhovered_list.append(Function(clear_scene))

                            if isinstance(item,Action):
                                $ title = ""
                                $ return_value = item
                                $ display = False #Default display state for an action is to hide it unless it is enabled or has a disabled slug
                                if item.is_action_enabled(extra_args):
                                    $ title = item.name
                                    $ display = True

                                elif item.is_disabled_slug_shown(extra_args):
                                    $ title = item.get_disabled_slug_name(extra_args)
                                    $ display = True

                                if item.menu_tooltip:
                                    $ the_tooltip = item.menu_tooltip

                            if isinstance(item,basestring): #It's just text. Display the text and return the text.
                                $ title = item
                                $ return_value = item

                            if " (tooltip)" in title:
                                $ the_tooltip = title.split(" (tooltip)",1)[1]
                                $ title = title.replace(" (tooltip)" + the_tooltip,"")

                            if " (disabled)" in title:
                                $ title = title.replace(" (disabled)", "")
                                $ is_sensitive = False

                            if display: #If we haven't encountered any reason to completely hide the item we display it now.
                                textbutton title:
                                    xsize 360
                                    ysize 100
                                    xalign 0.5
                                    yalign 0.0
                                    xanchor 0.5
                                    yanchor 0.0
                                    style "textbutton_style"
                                    text_style "textbutton_text_style"
                                    text_align (0.5,0.5)
                                    hovered hovered_list
                                    unhovered unhovered_list
                                    action Return(return_value)
                                    tooltip the_tooltip
                                    sensitive is_sensitive

                vbar:
                    value YScrollValue(title_element)
                    xalign 0.99
                    yalign 0.99
                    ysize 585

screen person_choice(people, draw_hearts = False, person_prefix = None, person_suffix = None, show_person_preview = True, person_preview_args = None):
    style_prefix "choice"
    #We want to have 2 vboxes, seperated so that they are staggered as they go down.
    #if len(items) > 10: #TODO: see if we can have the viewport all the time but only show it as scrollable when there are enough items in it, to simplify this section.

    viewport:
        scrollbars "vertical"
        mousewheel True
        child_size (1920,400+125*(len(people)//2))
        vbox:
            xalign 0.34
            yalign 0.5
            null height 400
            for i in people[0::2]:
                #Check if " (tooltip)" in i.caption, and if it is remove it and everything after it and add it as a tooltip

                if isinstance(i, Person):
                    $ her_title = format_titles(i)
                    if person_prefix:
                        $ her_title = person_prefix + " " + her_title
                    if person_suffix:
                        $ her_title += " " + person_suffix

                    if draw_hearts: #If we want to draw sluttiness hearts under someone add them to the image list now
                        $ her_title += "\n"
                        $ her_title += get_heart_image_list(i)

                    if person_preview_args is None:
                        $ person_preview_args = {}

                    $ person_displayable = i.build_person_displayable(lighting = mc.location.get_lighting_conditions(), **person_preview_args)
                    textbutton her_title:
                        action [Function(renpy.scene, "front_1"), Return(i)]
                        if show_person_preview:
                            hovered Function(renpy.show, i.name, at_list=[character_right, scale_person(i.height)],layer="front_1",what=person_displayable,tag=i.name)
                            unhovered Function(renpy.scene,"front_1")
                else:
                    textbutton i action Return(i)

        vbox:
            xalign 0.67
            yalign 0.5
            null height 400
            if len(people)%2 == 0:
                null height 125 #Add an empty list element to keep the alignment correct if there are an even number of elements in both lists.
            for j in people[1::2]:
                if isinstance(j, Person):
                    $ her_title = format_titles(j)
                    if person_prefix:
                        $ her_title = person_prefix + " " + her_title
                    if person_suffix:
                        $ her_title += " " + person_suffix
                    if draw_hearts: #If we want to draw sluttiness hearts under someone add them to the image list now
                        $ her_title += "\n"
                        $ her_title += get_heart_image_list(j)

                    if person_preview_args is None:
                        $ person_preview_args = {}

                    $ person_displayable = j.build_person_displayable(lighting = mc.location.get_lighting_conditions(), **person_preview_args)
                    textbutton her_title:
                        action [Function(renpy.scene, "front_1"), Return(j)]
                        if show_person_preview:
                            hovered Function(renpy.show, j.name, at_list=[character_right, scale_person(j.height)],layer="front_1",what=person_displayable,tag=j.name)
                            unhovered Function(renpy.scene,"front_1")
                else:
                    textbutton j action Return(j)



screen choice(items):
    style_prefix "choice"
    #We want to have 2 vboxes, seperated so that they are staggered as they go down.
    #if len(items) > 10: #TODO: see if we can have the viewport all the time but only show it as scrollable when there are enough items in it, to simplify this sectio.
    #TODO Check if the MC is present
    $ show_phone = False
    if hasattr(store,"mc"):
        if mc.having_text_conversation and not mc.text_conversation_paused:
            $ show_phone = True

    if show_phone: #Underlays the phone display.
        use text_message_log(mc.having_text_conversation)

    viewport:
        scrollbars "vertical"
        mousewheel True
        child_size (1920,125*len(items)//2)
        yalign 0.5
        yanchor 0.5
        vbox:
            xalign 0.34
            yalign 0.5
            null height 490
            for i in items[0::2]:
                #Check if " (tooltip)" in i.caption, and if it is remove it and everything after it and add it as a tooltip
                $ the_tooltip = ""
                if isinstance(i.action, Person):
                    $ the_tooltip = "This is a person!"

                if " (tooltip)" in i.caption:
                    $ the_tooltip = i.caption.split(" (tooltip)",1)[1]
                if " (disabled)" in i.caption:
                    textbutton i.caption.replace(" (disabled)", "").replace(" (tooltip)" + the_tooltip,"") sensitive False tooltip the_tooltip #Replace the full tooltip bit with nothing.
                else:
                    textbutton i.caption.replace(" (tooltip)" + the_tooltip,"") action i.action tooltip the_tooltip

        vbox:
            xalign 0.67
            yalign 0.5
            null height 490
            if len(items)%2 == 0:
                null height 125 #Add an empty list element to keep the alignment correct if there are an even number of elements in both lists.
            for j in items[1::2]:
                $ the_tooltip = ""
                if " (tooltip)" in j.caption:
                    $ the_tooltip = j.caption.split(" (tooltip)",1)[1]

                if " (disabled)" in j.caption:
                    textbutton j.caption.replace(" (disabled)", "").replace(" (tooltip)" + the_tooltip,"") sensitive False tooltip the_tooltip
                else:
                    textbutton j.caption.replace(" (tooltip)" + the_tooltip,"") action j.action tooltip the_tooltip



## When this is true, menu captions will be spoken by the narrator. When false,
## menu captions will be displayed as empty buttons.
define config.narrator_menu = True


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 500
    yanchor 0.5
    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")

style choice_button_text is default:
    properties gui.button_text_properties("choice_button")
    outlines [(2,"#222222",0,0)]
    ysize 500
    yalign 0.5


## Quick Menu screen ###########################################################
##
## The quick menu is displayed in-game to provide easy access to the out-of-game
## menus.

screen quick_menu():

    # Ensure this appears on top of other screens.
    zorder 100

    # Add an in-game quick menu.
    hbox:
        style_prefix "quick"

        xalign 0.5
        yalign 1.0

        textbutton _("Back") action Rollback()
        textbutton _("History") action ShowMenu('history')
        textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
        textbutton _("Auto") action Preference("auto-forward", "toggle")
        textbutton _("Save") action ShowMenu('save')
        textbutton _("Q.Save") action QuickSave()
        textbutton _("Q.Load") action QuickLoad()
        textbutton _("Prefs") action ShowMenu('preferences')


## This code ensures that the quick_menu screen is displayed in-game, whenever
## the player has not explicitly hidden the interface.
init python:
    config.overlay_screens.append("quick_menu")


style quick_button is default
style quick_button_text is button_text

style quick_button:
    properties gui.button_properties("quick_button")

style quick_button_text:
    properties gui.button_text_properties("quick_button")


################################################################################
# Main and Game Menu Screens
################################################################################

## Navigation screen ###########################################################
##
## This screen is included in the main and game menus, and provides navigation
## to other menus, and to start the game.

screen navigation():
    if main_menu: # This is used if we are on the main menu at the start of the game.
        add "images/LR2_Title.png"
        frame: #Central main menu button
            background None
            xsize 600
            ysize 188
            anchor (0.5,0.5)
            align (0.5,0.535)
            imagebutton:
                action Start()
                auto "gui/button/main_choice_%s_background.png"
                focus_mask "gui/button/main_choice_idle_background.png"
            text "New Game" align (0.5,0.5) xanchor 0.5 style "menu_text_style" size 50

        frame: #Bottom Left Patreon button
            background None
            xsize 600
            ysize 188
            anchor (0.5,0.5)
            align (0.223,0.627)
            imagebutton:
                action [SetVariable("main_menu",False),ShowMenu("about")]
                auto "gui/button/main_choice_%s_background.png"
                focus_mask "gui/button/main_choice_idle_background.png"
            text "About" align (0.5,0.5) xanchor 0.5 style "menu_text_style" size 50

        frame: #Bottom Right about button
            background None
            xsize 600
            ysize 188
            anchor (0.5,0.5)
            align (0.777,0.627)
            imagebutton:
                action OpenURL("https://www.patreon.com/vrengames")
                auto "gui/button/main_choice_%s_background.png"
                focus_mask "gui/button/main_choice_idle_background.png"
            image "Patreon_Link_Image_idle.png" align (0.5,0.5) anchor(0.5,0.5)

        frame: #Load top left button
            background None
            xsize 600
            ysize 188
            anchor (0.5,0.5)
            align (0.223,0.442)
            imagebutton:
                action [SetVariable("main_menu",False),ShowMenu("load")]
                auto "gui/button/main_choice_%s_background.png"
                focus_mask "gui/button/main_choice_idle_background.png"
            text "Load Game" align (0.5,0.5) xanchor 0.5 style "menu_text_style" size 50

        frame: #Preferences top right button
            background None
            xsize 600
            ysize 188
            anchor (0.5,0.5)
            align (0.777,0.442)
            imagebutton:
                action [SetVariable("main_menu",False),ShowMenu("preferences")]
                auto "gui/button/main_choice_%s_background.png"
                focus_mask "gui/button/main_choice_idle_background.png"
            text "Preferences" align (0.5,0.5) xanchor 0.5 style "menu_text_style" size 50

        frame: #Quit middle buttom button
            background None
            xsize 600
            ysize 188
            anchor (0.5,0.5)
            align (0.5,0.72)
            imagebutton:
                action Quit(confirm=True)
                auto "gui/button/main_choice_%s_background.png"
                focus_mask "gui/button/main_choice_idle_background.png"
            text "Quit" align (0.5,0.5) xanchor 0.5 style "menu_text_style" size 50


    else: # This is the in game save/load section
        vbox:
            style_prefix "navigation"

            xpos gui.navigation_xpos
            yalign 0.5

            spacing gui.navigation_spacing

            textbutton _("History") action ShowMenu("history")

            textbutton _("Save") action ShowMenu("save")

            textbutton _("Load") action ShowMenu("load")

            textbutton _("Preferences") action ShowMenu("preferences")

            textbutton _("Main Menu") action [ShowMenu("main_menu"),SetVariable("main_menu",True),MainMenu(confirm=False)] sensitive True

            textbutton _("About") action ShowMenu("about")

            if renpy.variant("pc"):

                ## The quit button is banned on iOS and unnecessary on Android.
                textbutton _("Quit") action Quit(confirm=not main_menu)

            imagebutton auto "Patreon_Link_Image_%s.png" action OpenURL("https://www.patreon.com/user?u=4548070") xpos 0.1 ypos 0.5


style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")

style navigation_button_text:
    properties gui.button_text_properties("navigation_button")


## Main Menu screen ############################################################
##
## Used to display the main menu when Ren'Py starts.
##
## http://www.renpy.org/doc/html/screen_special.html#main-menu

screen main_menu():

    # This ensures that any other menu screen is replaced.
    tag menu

    style_prefix "main_menu"

    add gui.main_menu_background

    # This empty frame darkens the main menu.
    frame:
        pass

    ## The use statement includes another screen inside this one. The actual
    ## contents of the main menu are in the navigation screen.
    use navigation

    if gui.show_name:

        vbox:
            text "[config.name!t]":
                style "main_menu_title"

            text "[config.version]":
                style "main_menu_version"


style main_menu_frame is empty
style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_version is main_menu_text

#style main_menu_frame:
#    xsize 420
#    yfill True

#    background "images/LR2_Title.png"

style main_menu_vbox:
    xalign 1.0
    xoffset -30
    xmaximum 1200
    yalign 1.0
    yoffset -30

style main_menu_text:
    xalign 1.0

    layout "subtitle"
    text_align 1.0
    color gui.accent_color

style main_menu_title:
    size gui.title_text_size


## Game Menu screen ############################################################
##
## This lays out the basic common structure of a game menu screen. It's called
## with the screen title, and displays the background, title, and navigation.
##
## The scroll parameter can be None, or one of "viewport" or "vpgrid". When this
## screen is intended to be used with one or more children, which are
## transcluded (placed) inside it.

screen game_menu(title, scroll=None):

    # Add the backgrounds.
    if main_menu:
        add gui.main_menu_background
    else:
        add gui.game_menu_background

    style_prefix "game_menu"

    frame:
        style "game_menu_outer_frame"

        hbox:

            # Reserve space for the navigation section.
            frame:
                style "game_menu_navigation_frame"

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:
                        scrollbars "vertical"
                        mousewheel True
                        draggable True

                        side_yfill True

                        vbox:
                            transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial 1.0

                        scrollbars "vertical"
                        mousewheel True
                        draggable True

                        side_yfill True

                        transclude

                else:

                    transclude

    use navigation

    textbutton _("Return"):
        style "return_button"

        action Return()

    label title

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    bottom_padding 45
    top_padding 180

    background "images/LR2_Title.png"

style game_menu_navigation_frame:
    xsize 420
    yfill True

style game_menu_content_frame:
    left_margin 60
    right_margin 30
    top_margin 15

style game_menu_viewport:
    xsize 1380

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 15

style game_menu_label:
    xpos 75
    ysize 180

style game_menu_label_text:
    size gui.title_text_size
    color gui.accent_color
    yalign 0.5

style return_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset -45


## About screen ################################################################
##
## This screen gives credit and copyright information about the game and Ren'Py.
##
## There's nothing special about this screen, and hence it also serves as an
## example of how to make a custom screen.

screen about():

    tag menu

    ## This use statement includes the game_menu screen inside this one. The
    ## vbox child is then included inside the viewport inside the game_menu
    ## screen.
    use game_menu(_("About"), scroll="viewport"):

        style_prefix "about"

        vbox:

            label "[config.name!t]"
            text _("Version [config.version!t]\n")

            ## gui.about is usually set in options.rpy.
            if gui.about:
                text "[gui.about!t]\n"

            text _("Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]")


## This is redefined in options.rpy to add text to the about screen.
define gui.about = ""


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size


## Load and Save screens #######################################################
##
## These screens are responsible for letting the player save the game and load
## it again. Since they share nearly everything in common, both are implemented
## in terms of a third screen, file_slots.
##
## https://www.renpy.org/doc/html/screen_special.html#save
## https://www.renpy.org/doc/html/screen_special.html#load

screen save():

    tag menu

    use file_slots(_("Save"))


screen load():

    tag menu

    use file_slots(_("Load"))


screen file_slots(title):

    default page_name_value = FilePageNameInputValue()

    use game_menu(title):

        fixed:

            ## This ensures the input will get the enter event before any of the
            ## buttons do.
            order_reverse True

            # The page name, which can be edited by clicking on a button.
            button:
                style "page_label"

                key_events True
                xalign 0.5
                action page_name_value.Toggle()

                input:
                    style "page_label_text"
                    value page_name_value

            ## The grid of file slots.
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"

                xalign 0.5
                yalign 0.5

                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    button:
                        action FileAction(slot)

                        has vbox

                        add FileScreenshot(slot) xalign 0.5

                        text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                            style "slot_time_text"

                        text FileSaveName(slot):
                            style "slot_name_text"

                        key "save_delete" action FileDelete(slot)

            ## Buttons to access other pages.
            hbox:
                style_prefix "page"

                xalign 0.5
                yalign 1.0

                spacing gui.page_spacing

                textbutton _("<") action FilePagePrevious()

                textbutton _("{#auto_page}A") action FilePage("auto")

                textbutton _("{#quick_page}Q") action FilePage("quick")

                # range(1, 10) gives the numbers from 1 to 9.
                for page in range(1, 10):
                    textbutton "[page]" action FilePage(page)

                textbutton _(">") action FilePageNext()


style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text

style page_label:
    yalign 0.05
    xpadding 75
    ypadding 5

style page_label_text:
    text_align 0.5
    layout "subtitle"
    hover_color gui.hover_color

style page_button:
    properties gui.button_properties("page_button")

style page_button_text:
    properties gui.button_text_properties("page_button")

style slot_button:
    properties gui.button_properties("slot_button")

style slot_button_text:
    properties gui.button_text_properties("slot_button")


## Preferences screen ##########################################################
##
## The preferences screen allows the player to configure the game to better suit
## themselves.
##
## https://www.renpy.org/doc/html/screen_special.html#preferences

screen preferences():

    tag menu

    if renpy.mobile:
        $ cols = 2
    else:
        $ cols = 4

    use game_menu(_("Preferences"), scroll="viewport"):

        vbox:

            hbox:
                box_wrap True

                if renpy.variant("pc"):

                    vbox:
                        style_prefix "radio"
                        label _("Display")
                        textbutton _("Window") action Preference("display", "window")
                        textbutton _("Fullscreen") action Preference("display", "fullscreen")

                vbox:
                    style_prefix "radio"
                    label _("Rollback Side")
                    textbutton _("Disable") action Preference("rollback side", "disable")
                    textbutton _("Left") action Preference("rollback side", "left")
                    textbutton _("Right") action Preference("rollback side", "right")

                vbox:
                    style_prefix "check"
                    label _("Skip")
                    textbutton _("Unseen Text") action Preference("skip", "toggle")
                    textbutton _("After Choices") action Preference("after choices", "toggle")
                    textbutton _("Transitions") action InvertSelected(Preference("transitions", "toggle"))

                vbox:
                    style_prefix "radio"
                    label "Pregnancy Settings"
                    textbutton "Disabled" action SetField(persistent, "pregnancy_pref", 0)
                    textbutton "Predictable" action SetField(persistent, "pregnancy_pref", 1)
                    textbutton "Realistic" action SetField(persistent, "pregnancy_pref", 2)

                if not renpy.mobile: #Animations are always disabled on mobile.
                    vbox:
                        style_prefix "radio"
                        label "Animation"
                        textbutton "Enable" action SetField(persistent, "vren_animation", True)
                        textbutton "Disable" action SetField(persistent, "vren_animation", False)

                    # vbox:
                    #     style_prefix "radio"
                    #     label "Animation Scaling"
                    #     textbutton "1.0" action SetField(persistent, "vren_mac_scale", 1.0)
                    #     textbutton "2.0" action SetField(persistent, "vren_mac_scale", 2.0)

                ## Additional vboxes of type "radio_pref" or "check_pref" can be
                ## added here, to add additional creator-defined preferences.

            null height (4 * gui.pref_spacing)

            hbox:
                style_prefix "slider"
                box_wrap True

                vbox:

                    label _("Text Speed")

                    bar value Preference("text speed")

                    label _("Auto-Forward Time")

                    bar value Preference("auto-forward time")

                vbox:

                    if config.has_music:
                        label _("Music Volume")

                        hbox:
                            bar value Preference("music volume")

                    if config.has_sound:

                        label _("Sound Volume")

                        hbox:
                            bar value Preference("sound volume")

                            if config.sample_sound:
                                textbutton _("Test") action Play("sound", config.sample_sound)


                    if config.has_voice:
                        label _("Voice Volume")

                        hbox:
                            bar value Preference("voice volume")

                            if config.sample_voice:
                                textbutton _("Test") action Play("voice", config.sample_voice)

                    if config.has_music or config.has_sound or config.has_voice:
                        null height gui.pref_spacing

                        textbutton _("Mute All"):
                            action Preference("all mute", "toggle")
                            style "mute_all_button"


style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_label is pref_label
style slider_label_text is pref_label_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_pref_vbox is pref_vbox

style mute_all_button is check_button
style mute_all_button_text is check_button_text

style pref_label:
    top_margin gui.pref_spacing
    bottom_margin 3

style pref_label_text:
    yalign 1.0

style pref_vbox:
    xsize 338

style radio_vbox:
    spacing gui.pref_button_spacing

style radio_button:
    properties gui.button_properties("radio_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style radio_button_text:
    properties gui.button_text_properties("radio_button")

style check_vbox:
    spacing gui.pref_button_spacing

style check_button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style check_button_text:
    properties gui.button_text_properties("check_button")

style slider_slider:
    xsize 525

style slider_button:
    properties gui.button_properties("slider_button")
    yalign 0.5
    left_margin 15

style slider_button_text:
    properties gui.button_text_properties("slider_button")

style slider_vbox:
    xsize 675


## History screen ##############################################################
##
## This is a screen that displays the dialogue history to the player. While
## there isn't anything special about this screen, it does have to access the
## dialogue history stored in _history_list.
##
## https://www.renpy.org/doc/html/history.html

screen history():

    tag menu

    ## Avoid predicting this screen, as it can be very large.
    predict False

    use game_menu(_("History"), scroll=("vpgrid" if gui.history_height else "viewport")):

        style_prefix "history"

        for h in _history_list:

            window:

                ## This lays things out properly if history_height is None.
                has fixed:
                    yfit True

                if h.who:

                    label h.who:
                        style "history_name"

                        ## Take the color of the who text from the Character, if
                        ## set.
                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                text h.what

        if not _history_list:
            label _("The dialogue history is empty.")


style history_window is empty

style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_text is gui_text

style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize gui.history_height

style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text:
    min_width gui.history_name_width
    text_align gui.history_name_xalign
    size 28

style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    text_align gui.history_text_xalign
    size 24
    layout ("subtitle" if gui.history_text_xalign else "tex")

style history_label:
    xfill True

style history_label_text:
    xalign 0.5


## Help screen #################################################################
##
## A screen that gives information about key and mouse bindings. It uses other
## screens (keyboard_help, mouse_help, and gamepad_help) to display the actual
## help.

screen help(): #VREN: This isn't used anywhere, I'm sure people can figure this out themselves.

    tag menu

    default device = "keyboard"

    use game_menu(_("Help"), scroll="viewport"):

        style_prefix "help"

        vbox:
            spacing 23

            hbox:

                textbutton _("Keyboard") action SetScreenVariable("device", "keyboard")
                textbutton _("Mouse") action SetScreenVariable("device", "mouse")

                if GamepadExists():
                    textbutton _("Gamepad") action SetScreenVariable("device", "gamepad")

            if device == "keyboard":
                use keyboard_help
            elif device == "mouse":
                use mouse_help
            elif device == "gamepad":
                use gamepad_help


screen keyboard_help():

    hbox:
        label _("Enter")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Space")
        text _("Advances dialogue without selecting choices.")

    hbox:
        label _("Arrow Keys")
        text _("Navigate the interface.")

    hbox:
        label _("Escape")
        text _("Accesses the game menu.")

    hbox:
        label _("Ctrl")
        text _("Skips dialogue while held down.")

    hbox:
        label _("Tab")
        text _("Toggles dialogue skipping.")

    hbox:
        label _("Page Up")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Page Down")
        text _("Rolls forward to later dialogue.")

    hbox:
        label "H"
        text _("Hides the user interface.")

    hbox:
        label "S"
        text _("Takes a screenshot.")

    hbox:
        label "V"
        text _("Toggles assistive {a=https://www.renpy.org/l/voicing}self-voicing{/a}.")


screen mouse_help():

    hbox:
        label _("Left Click")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Middle Click")
        text _("Hides the user interface.")

    hbox:
        label _("Right Click")
        text _("Accesses the game menu.")

    hbox:
        label _("Mouse Wheel Up\nClick Rollback Side")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Mouse Wheel Down")
        text _("Rolls forward to later dialogue.")


screen gamepad_help():

    hbox:
        label _("Right Trigger\nA/Bottom Button")
        text _("Advance dialogue and activates the interface.")

    hbox:
        label ("Left Trigger\nLeft Shoulder")
        text _("Roll back to earlier dialogue.")

    hbox:
        label _("Right Shoulder")
        text _("Roll forward to later dialogue.")

    hbox:
        label _("D-Pad, Sticks")
        text _("Navigate the interface.")

    hbox:
        label _("Start, Guide")
        text _("Access the game menu.")

    hbox:
        label _("Y/Top Button")
        text _("Hides the user interface.")

    textbutton _("Calibrate") action GamepadCalibrate()


style help_button is gui_button
style help_button_text is gui_button_text
style help_label is gui_label
style help_label_text is gui_label_text
style help_text is gui_text

style help_button:
    properties gui.button_properties("help_button")
    xmargin 12

style help_button_text:
    properties gui.button_text_properties("help_button")

style help_label:
    xsize 375
    right_padding 30

style help_label_text:
    size gui.text_size
    xalign 1.0
    text_align 1.0



################################################################################
## Additional screens
################################################################################


## Confirm screen ##############################################################
##
## The confirm screen is called when Ren'Py wants to ask the player a yes or no
## question.
##
## http://www.renpy.org/doc/html/screen_special.html#confirm

screen confirm(message, yes_action, no_action):

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 45

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 150

                textbutton _("Yes") action yes_action
                textbutton _("No") action no_action

    ## Right-click and escape answer "no".
    key "game_menu" action no_action


style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background Frame([ "gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style confirm_prompt_text:
    text_align 0.5
    layout "subtitle"

style confirm_button:
    properties gui.button_properties("confirm_button")

style confirm_button_text:
    properties gui.button_text_properties("confirm_button")


## Skip indicator screen #######################################################
##
## The skip_indicator screen is displayed to indicate that skipping is in
## progress.
##
## https://www.renpy.org/doc/html/screen_special.html#skip-indicator

screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        hbox:
            spacing 9

            text _("Skipping")

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"


## This transform is used to blink the arrows one after another.
transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size

style skip_triangle:
    # We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE
    # glyph in it.
    font "DejaVuSans.ttf"


## Notify screen ###############################################################
##
## The notify screen is used to show the player a message. (For example, when
## the game is quicksaved or a screenshot has been taken.)
##
## https://www.renpy.org/doc/html/screen_special.html#notify-screen

screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text message

    timer 3.25 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos

    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

style notify_text:
    size gui.notify_text_size


## NVL screen ##################################################################
##
## This screen is used for NVL-mode dialogue and menus.
##
## http://www.renpy.org/doc/html/screen_special.html#nvl


screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox:
            spacing gui.nvl_spacing

        ## Displays dialogue in either a vpgrid or the vbox.
        if gui.nvl_height:

            vpgrid:
                cols 1
                yinitial 1.0

                use nvl_dialogue(dialogue)

        else:

            use nvl_dialogue(dialogue)

        ## Displays the menu, if given. The menu may be displayed incorrectly if
        ## config.narrator_menu is set to True, as it is above.
        for i in items:

            textbutton i.caption:
                action i.action
                style "nvl_button"

    add SideImage() xalign 0.0 yalign 1.0


screen nvl_dialogue(dialogue):

    for d in dialogue:

        window:
            id d.window_id

            fixed:
                yfit gui.nvl_height is None

                if d.who is not None:

                    text d.who:
                        id d.who_id

                text d.what:
                    id d.what_id


## This controls the maximum number of NVL-mode entries that can be displayed at
## once.
define config.nvl_list_length = 6

style nvl_window is default
style nvl_entry is default

style nvl_label is say_label
style nvl_dialogue is say_dialogue

style nvl_button is button
style nvl_button_text is button_text

style nvl_window:
    xfill True
    yfill True

    background "gui/nvl.png"
    padding gui.nvl_borders.padding

style nvl_entry:
    xfill True
    ysize gui.nvl_height

style nvl_label:
    xpos gui.nvl_name_xpos
    xanchor gui.nvl_name_xalign
    ypos gui.nvl_name_ypos
    yanchor 0.0
    xsize gui.nvl_name_width
    min_width gui.nvl_name_width
    text_align gui.nvl_name_xalign

style nvl_dialogue:
    xpos gui.nvl_text_xpos
    xanchor gui.nvl_text_xalign
    ypos gui.nvl_text_ypos
    xsize gui.nvl_text_width
    min_width gui.nvl_text_width
    text_align gui.nvl_text_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_thought:
    xpos gui.nvl_thought_xpos
    xanchor gui.nvl_thought_xalign
    ypos gui.nvl_thought_ypos
    xsize gui.nvl_thought_width
    min_width gui.nvl_thought_width
    text_align gui.nvl_thought_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_button:
    properties gui.button_properties("nvl_button")
    xpos gui.nvl_button_xpos
    xanchor gui.nvl_button_xalign

style nvl_button_text:
    properties gui.button_text_properties("nvl_button")



################################################################################
## Mobile Variants
################################################################################

style pref_vbox:
    variant "medium"
    xsize 675

## Since a mouse may not be present, we replace the quick menu with a version
## that uses fewer and bigger buttons that are easier to touch.
screen quick_menu():
    variant "touch"

    zorder 100

    hbox:
        style_prefix "quick"

        xalign 0.5
        yalign 1.0

        textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
        textbutton _("Menu") action ShowMenu()
        textbutton _("Auto") action Preference("auto-forward", "toggle")


style window:
    variant "small"
    background "gui/phone/textbox.png"

style nvl_window:
    variant "small"
    background "gui/phone/nvl.png"

style main_menu_frame:
    variant "small"
    background "gui/phone/overlay/main_menu.png"

style game_menu_outer_frame:
    variant "small"
    background "gui/phone/overlay/game_menu.png"

style game_menu_navigation_frame:
    variant "small"
    xsize 510

style game_menu_content_frame:
    variant "small"
    top_margin 0

style pref_vbox:
    variant "small"
    xsize 600

style slider_pref_vbox:
    variant "small"
    xsize None

style slider_pref_slider:
    variant "small"
    xsize 900
