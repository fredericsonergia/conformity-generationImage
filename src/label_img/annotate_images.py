from Save_xml import Save_Xml


def create_annotation_file(shapes, filename, image_path, annot_path):
    path = annot_path + filename + ".xml"
    saver = Save_Xml()
    saver.savePascalVocFormat(path, shapes, image_path)
