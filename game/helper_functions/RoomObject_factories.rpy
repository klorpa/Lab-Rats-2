init -1 python:
    def make_wall(): #Helper functions for creating instances of commonly used objects.
        the_wall = Object("wall",["Lean"], sluttiness_modifier = 0, obedience_modifier = 0) #0/5
        return the_wall

    def make_door():
        the_door = Object("door", ["Lean"], sluttiness_modifier = 0, obedience_modifier = 0)
        return the_door

    def make_window():
        the_window = Object("window",["Lean"], sluttiness_modifier = 0, obedience_modifier = 0) #-5/5
        return the_window

    def make_chair():
        the_chair = Object("chair",["Sit","Low"], sluttiness_modifier = 0, obedience_modifier = 0)
        return the_chair

    def make_desk():
        the_desk = Object("desk",["Sit","Lay","Low"], sluttiness_modifier = 0, obedience_modifier = 0)
        return the_desk

    def make_table():
        the_table = Object("table",["Sit","Lay","Low"], sluttiness_modifier = 0, obedience_modifier = 0)
        return the_table

    def make_bed():
        the_bed = Object("bed",["Sit","Lay","Low"], sluttiness_modifier = 0, obedience_modifier = 0) #10/10
        return the_bed

    def make_couch():
        the_couch = Object("couch",["Sit","Lay","Low"], sluttiness_modifier = 0, obedience_modifier = 0) #5/-5
        return the_couch

    def make_floor():
        the_floor = Object("floor",["Lay","Kneel"], sluttiness_modifier = 0, obedience_modifier = 0) #-10/-10
        return the_floor

    def make_grass():
        the_grass = Object("grass",["Lay","Kneel"], sluttiness_modifier = 0, obedience_modifier = 0) #-5/-10
        return the_grass

    def make_stage():
        the_stage = Object("stripclub stage",["Lay","Sit"], sluttiness_modifier = 0, obedience_modifier = 0) #5/-5
        return the_stage
