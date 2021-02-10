import argparse

from label_img.visualisation import create_visualisation


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i",
        "--images_folder",
        default="../EAF/VOC2021/JPEGImages",
        help="path to existing folder where the images are ( can be styled or not ), default is ../EAF/VOC2021/JPEGImages/",
    )
    parser.add_argument(
        "-a",
        "--annotations_folder",
        default="../EAF/VOC2021/Annotations",
        help="path to existing folder where the corresponding annotations are ( can be styled or not ), default is ../EAF/VOC2021/JPEGImages/",
    )
    parser.add_argument(
        "-o",
        "--output_folder",
        default="../EAF/visualisation",
        help="path to existing folder where annotated images will be put, default is ../EAF/visualisation/",
    )
    args = parser.parse_args()

    IMAGE_FOLDER = args.images_folder
    ANNOT_FOLDER = args.annotations_folder
    OUTPUT_FOLDER = args.output_folder

    create_visualisation(IMAGE_FOLDER, ANNOT_FOLDER, OUTPUT_FOLDER)
