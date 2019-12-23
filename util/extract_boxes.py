import numpy as np
import argparse
import os
import cv2

from .bounding_boxes import get_bounding_boxes

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", default="assets/images/bounding_boxes.png")
    parser.add_argument("--output", default="assets/bounding_boxes.txt")

    args = parser.parse_args()

    overlay = cv2.imread(args.image, cv2.IMREAD_UNCHANGED)
    overlay = cv2.cvtColor(overlay, cv2.COLOR_BGRA2RGB)

    with open(args.output, "w") as file:
        write_boxes(file, "characters", overlay, (255, 0, 0))
        write_boxes(file, "bonuses", overlay, (0, 255, 0))
        write_boxes(file, "values", overlay, (0, 0, 255))
    
def write_boxes(file, name, image, colour):
    file.write(f"#begin {name.upper()}\n")
    boxes = get_bounding_boxes(image, colour)
    for box in boxes:
        file.write(f"{' '.join(map(str, box))}\n")
    file.write(f"#end\n")

if __name__ == '__main__':
    main()