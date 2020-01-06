"""
Use this script to merge the individual annotation files into one file per image.

If before running the script you have:

annotations/
  - 1.png/
     - eye_left.json
     - eye_right.json
  - 2.png/
     - eye_left.json
     - eye_right.json

After running the script you will have a new folder in annotations:

annotations/
  - 1.png /
     - eye_left.json
     - eye_right.json
  - 2.png /
     - eye_left.json
     - eye_right.json
  - /__annotations_merged
     - 1.png.json
     - 2.png.json
"""

from pathlib import Path
import json

import config

IMAGE_DIR = Path(config.IMAGE_DIR)
ANNOTATION_DIR = Path(config.ANNOTATION_DIR)
MERGED_ANNOTATIONS_DIR = ANNOTATION_DIR / "__annotations_merged"


def index_images():
    images = list(IMAGE_DIR.glob("*.png")) + list(IMAGE_DIR.glob("*.jpg"))
    return sorted(images)


def load_annotations(image_name):
    annotations = (ANNOTATION_DIR / image_name).glob("*.json")
    annotations = {a.name.replace(".json", ""): json.loads(a.read_text()) for a in annotations}
    return annotations


def main():
    MERGED_ANNOTATIONS_DIR.mkdir(exist_ok=True, parents=False)
    print("Writing images with landmarks to {}".format(MERGED_ANNOTATIONS_DIR))

    for image in index_images():
        print(image)
        merged_annotations = load_annotations(image.name)

        merged_file = MERGED_ANNOTATIONS_DIR / (image.name + ".json")
        merged_file.write_text(json.dumps(merged_annotations, indent=4))


main()
