init -1 python:
    def indent(elem, level=0):
        i = "\n" + level*"    "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "    "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def log_outfit(the_outfit, outfit_class = "FullSets", wardrobe_name = "Exported_Wardrobe"):
        file_path = os.path.abspath(os.path.join(config.basedir, "game"))
        file_path = os.path.join(file_path,"wardrobes")
        file_name = os.path.join(file_path, wardrobe_name + ".xml")

        if not os.path.isfile(file_name): #We assume if the file exists that it is well formed. Otherwise we will create it and guarantee it is well formed.
            #Note: if the file is changed (by inserting extra outfits, for example) exporting outfits may crash due to malformed xml, but we do not overwrite the file.
            missing_file = open(file_name,"w+")
            starting_element = ET.Element("Wardrobe",{"name":wardrobe_name})
            starting_tree = ET.ElementTree(starting_element)
            ET.SubElement(starting_element,"FullSets")
            ET.SubElement(starting_element,"UnderwearSets")
            ET.SubElement(starting_element,"OverwearSets")

            indent(starting_element)
            starting_tree.write(file_name,encoding="UTF-8")


        wardrobe_tree = ET.parse(file_name)
        tree_root = wardrobe_tree.getroot()
        outfit_root = tree_root.find(outfit_class)

        outfit_element = ET.SubElement(outfit_root,"Outfit",{"name":the_outfit.name})
        upper_element = ET.SubElement(outfit_element, "UpperBody")
        lower_element = ET.SubElement(outfit_element, "LowerBody")
        feet_element = ET.SubElement(outfit_element, "Feet")
        accessory_element = ET.SubElement(outfit_element, "Accessories")


        for cloth in the_outfit.upper_body:
            item_dict = build_item_dict(cloth)
            if not cloth.is_extension:
                ET.SubElement(upper_element,"Item", item_dict)
        for cloth in the_outfit.lower_body:
            item_dict = build_item_dict(cloth)
            if not cloth.is_extension:
                ET.SubElement(lower_element,"Item", item_dict)
        for cloth in the_outfit.feet:
            item_dict = build_item_dict(cloth)
            if not cloth.is_extension:
                ET.SubElement(feet_element,"Item", item_dict)
        for cloth in the_outfit.accessories:
            item_dict = build_item_dict(cloth)
            if not cloth.is_extension:
                ET.SubElement(accessory_element,"Item", item_dict)


        indent(tree_root)
        wardrobe_tree.write(file_name,encoding="UTF-8")

    def build_item_dict(cloth):
        item_dict = {"name":cloth.proper_name,"red":str(cloth.colour[0]),"green":str(cloth.colour[1]),"blue":str(cloth.colour[2]),"alpha":str(cloth.colour[3])}
        if __builtin__.type(cloth) is Clothing and cloth.pattern is not None:
            item_dict.update({"pattern":cloth.pattern, "pred":str(cloth.colour_pattern[0]), "pgreen":str(cloth.colour_pattern[1]), "pblue":str(cloth.colour_pattern[2]), "palpha":str(cloth.colour_pattern[3])})
        return item_dict

    def log_wardrobe(the_wardrobe, file_name):

        for outfit in the_wardrobe.outfits:
            log_outfit(outfit, outfit_class = "FullSets", wardrobe_name = file_name)

        for outfit in the_wardrobe.underwear_sets:
            log_outfit(outfit, outfit_class = "UnderwearSets", wardrobe_name = file_name)

        for outfit in the_wardrobe.overwear_sets:
            log_outfit(outfit, outfit_class = "OverwearSets", wardrobe_name = file_name)
