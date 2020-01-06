"""
Use this script to draw the annotated landmarks on the image. This makes it easy to check if your annotations look fine.

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
  - /__images_with_landmarks
     - 1.png
     - 2.png
"""


from pathlib import  Path
import json

from PIL import Image, ImageDraw

import config


IMAGE_DIR = Path(config.IMAGE_DIR)
ANNOTATION_DIR = Path(config.ANNOTATION_DIR)
ANNOTATED_IMAGES_DIR = ANNOTATION_DIR / "__images_with_landmarks"


def load_annotations(image_name):
    annotations = (ANNOTATION_DIR / image_name).glob("*.json")
    annotations = {a.name.replace(".json", ""): json.loads(a.read_text()) for a in annotations}
    return annotations


def index_images():
    images = list(IMAGE_DIR.glob("*.png")) + list(IMAGE_DIR.glob("*.jpg"))
    return sorted(images)


def draw_landmark(image_draw, annotation):
    radius = 3

    if annotation["status"] == "occluded/missing":
        return

    coordinates = annotation["coordinates"]
    x, y = coordinates["x"], coordinates["y"]
    image_draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(255, 0, 0, 0))


def draw_all_landmarks(image_name, annotations):
    image = Image.open(str(IMAGE_DIR / image_name))
    draw = ImageDraw.Draw(image)

    for name, data in annotations.items():
        draw_landmark(draw, data)

    image.save(str(ANNOTATED_IMAGES_DIR / image_name))


def main():
    ANNOTATED_IMAGES_DIR.mkdir(exist_ok=True, parents=False)
    print("Writing images with landmarks to {}".format(ANNOTATED_IMAGES_DIR))

    for image in index_images():
        print(image)
        annotations = load_annotations(image.name)
        draw_all_landmarks(image.name, annotations)

main()
