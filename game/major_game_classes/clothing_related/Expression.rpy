init -2 python:
    class Expression(renpy.store.object):
        def __init__(self,name,skin_colour,facial_style, colour = None):
            self.name = name
            self.skin_colour = skin_colour
            self.facial_style = facial_style #The style of face the person has, currently creatively named "Face_1", "Face_2", "Face_3", etc..
            self.emotion_set = ["default","happy","sad","angry","orgasm"]
            self.positions_set = ["stand2","stand3","stand4","stand5","walking_away","kissing","missionary","blowjob","against_wall","back_peek","sitting","kneeling1","standing_doggy","cowgirl"] #The set of images we are going to draw emotions for. These are positions that look towards the camera
            self.special_modifiers = {"kissing":["kissing"]} #Special modifiers that are sometimes applied to expressions, but not always. ie. for blowjobs that may be either in normal crouching mode or blowjob mode.
            self.ignore_position_set = ["doggy","walking_away","standing_doggy"] #The set of positions that we are not going to draw emotions for. These look away from the camera TODO: This should reference the Position class somehow.
            self.position_dict = {}
            for position in self.positions_set: #All positions support the blowjob special modifier now.
                if position in self.special_modifiers.keys():
                    self.special_modifiers[position].extend(["blowjob"])
                else:
                    self.special_modifiers[position] = ["blowjob"]

            for position in self.positions_set+self.ignore_position_set:
                self.position_dict[position] = {}

            for position in self.positions_set:
                for emotion in self.emotion_set:
                    self.position_dict[position][emotion] = emotion + "_" + facial_style + "_" + position + "_" + skin_colour + ".png"

            for position in self.ignore_position_set: #Positions that ignore emotions always use the "default" emotion for the back of the head.
                for emotion in self.emotion_set:
                    self.position_dict[position][emotion] = "default" + "_" + facial_style + "_" + position + "_" + skin_colour + ".png" ##An empty image to be drawn when we don't want to draw any emotion, because the character's face is turned away.

            for position, modifiers in self.special_modifiers.iteritems(): #Position is the key of our special modifers dict, get all the positions with a special modifier assigned.
                for modifier in modifiers: #If that position has multiple special modifers we want to add them all.
                    for emotion in self.emotion_set:
                        modified_emotion = emotion + "_" + modifier
                        self.position_dict[position][modified_emotion] = modified_emotion + "_" + facial_style + "_" + position + "_" + skin_colour + ".png"#Add a new emotion titled "<emotion>_<modifier>", for example "sad_blowjob".


            if not colour:
                self.colour = [1,1,1,1]
            else:
                self.colour = colour


        def generate_emotion_displayable(self,position,emotion, special_modifier = None, eye_colour = None, lighting = None):

            if not position in self.positions_set+self.ignore_position_set:
                position = "stand3"
            if not emotion in self.emotion_set:
                emotion = "default" #Get our default emotion to show if we get an incorrect one.
            elif special_modifier is not None and special_modifier in self.special_modifiers:
                emotion = emotion + "_" + special_modifier

            if lighting is None:
                lighting = [1,1,1]

            if eye_colour is None:
                eye_colour = [0.8,0.8,0.8,1] #grey by default.

            # if renpy.mobile or test_zip: #On mobile platforms we use .zip files to hold all of the individual images to bypass the andorid file limit. This results in significantly slower animation (for reasons currently unknown), but android douesn't animate anyways.

            base_name = self.position_dict[position][emotion]
            base_image = VrenZipImage(position, base_name)

            mask_name = self.position_dict[position][emotion].replace("_" + self.skin_colour,"_Pattern_1")
            mask_image = VrenZipImage(position, mask_name)



            inverted_mask_image = im.MatrixColor(mask_image, [1,0,0,0,0, 0,1,0,0,0, 0,0,1,0,0, 0,0,0,-1,1])
            #mask_image = im.MatrixColor(mask_image, [1,0,0,0,0, 0,1,0,0,0, 0,0,1,0,0, 0,0,0,1,0]) #Does this even do anything??? #TODO: Check that this does something. (Might have been used to ensure image values were capped properly)

            colour_pattern_matrix = im.matrix.tint(eye_colour[0], eye_colour[1], eye_colour[2]) * im.matrix.tint(*lighting)
            shader_pattern_image = im.MatrixColor(base_image, colour_pattern_matrix)

            skin_colour_matrix = im.matrix.tint(self.colour[0], self.colour[1], self.colour[2]) * im.matrix.tint(*lighting)

            base_image = im.MatrixColor(base_image, skin_colour_matrix) #To support the lighting of the room we also retint it here.
            final_image = AlphaBlend(mask_image, base_image, shader_pattern_image, alpha=False)

            return final_image

        def generate_raw_image(self, position, emotion, special_modifier = None): #Returns the raw ZipFileImage or Image, instead of the displayable (used for generating region masks)
            if not position in self.positions_set+self.ignore_position_set:
                position = "stand3"
            if not emotion in self.emotion_set:
                emotion = "default" #Get our default emotion to show if we get an incorrect one.
            elif special_modifier is not None and special_modifier in self.special_modifiers:
                emotion = emotion + "_" + special_modifier

            base_name = self.position_dict[position][emotion]
            base_image = VrenZipImage(position, base_name)

            return base_image
