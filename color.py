#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import colorsys
import os
import pickle
from typing import List, Sequence, Tuple

Color = Sequence[int]

COLORS = {
    "grass_block": ((89, 125, 39), (109, 153, 48), (127, 178, 56),),
    "sandstone": ((174, 164, 115), (213, 201, 140), (247, 233, 163),),
    "mushroom_stem": ((140, 140, 140), (171, 171, 171), (199, 199, 199)),
    "redstone_block": ((180, 0, 0), (220, 0, 0), (255, 0, 0)),
    "ice": ((112, 112, 180), (138, 138, 220), (160, 160, 255)),
    "iron_block": ((117, 117, 117), (144, 144, 144), (167, 167, 167)),
    "oak_leaves": ((0, 87, 0), (0, 106, 0), (0, 124, 0)),
    "white_wool": ((180, 180, 180), (220, 220, 220), (255, 255, 255)),
    "clay": ((115, 118, 129), (141, 144, 158), (164, 168, 184)),
    "dirt": ((106, 76, 54), (130, 94, 66), (151, 109, 77)),
    "cobblestone": ((79, 79, 79), (96, 96, 96), (112, 112, 112)),
    "water": ((45, 45, 180), (55, 55, 220), (64, 64, 255)),
    "oak_log": ((100, 84, 50), (123, 102, 62), (143, 119, 72)),
    "quartz_block": ((180, 177, 172), (220, 217, 211), (255, 252, 245)),
    "orange_wool": ((152, 89, 36), (186, 109, 44), (216, 127, 51)),
    "magenta_wool": ((125, 53, 152), (153, 65, 186), (178, 76, 216)),
    "light_blue_wool": ((72, 108, 152), (88, 132, 186), (102, 153, 216)),
    "yellow_wool": ((161, 161, 36), (197, 197, 44), (229, 229, 51)),
    "lime_wool": ((89, 144, 17), (109, 176, 21), (127, 204, 25)),
    "pink_wool": ((170, 89, 116), (208, 109, 142), (242, 127, 165)),
    "gray_wool": ((53, 53, 53), (65, 65, 65), (76, 76, 76)),
    "light_gray_wool": ((108, 108, 108), (132, 132, 132), (153, 153, 153)),
    "cyan_wool": ((53, 89, 108), (65, 109, 132), (76, 127, 153)),
    "purple_wool": ((89, 44, 125), (109, 54, 153), (127, 63, 178)),
    "blue_wool": ((36, 53, 125), (44, 65, 153), (51, 76, 178)),
    "brown_wool": ((72, 53, 36), (88, 65, 44), (102, 76, 51)),
    "green_wool": ((72, 89, 36), (88, 109, 44), (102, 127, 51)),
    "red_wool": ((108, 36, 36), (132, 44, 44), (153, 51, 51)),
    "black_wool": ((17, 17, 17), (21, 21, 21), (25, 25, 25)),
    "gold_block": ((176, 168, 54), (215, 205, 66), (250, 238, 77)),
    "diamond_block": ((64, 153, 150), (79, 188, 183), (92, 219, 213)),
    "lapis_block": ((52, 90, 180), (63, 110, 220), (74, 128, 255)),
    "emerald_block": ((0, 153, 40), (0, 187, 0), (0, 217, 58)),
    "spruce_log": ((91, 60, 34), (111, 74, 42), (129, 86, 49)),
    "netherrack": ((79, 1, 0), (96, 1, 0), (112, 2, 0)),
    "white_terracotta": ((147, 124, 113), (180, 152, 138), (209, 177, 161)),
    "orange_terracotta": ((112, 57, 25), (137, 70, 31), (159, 82, 36)),
    "magenta_terracotta": ((105, 61, 76), (128, 75, 93), (149, 87, 108)),
    "light_blue_terracotta": ((79, 76, 97), (96, 93, 119), (112, 108, 138)),
    "yellow_terracotta": ((131, 93, 25), (160, 114, 31), (186, 133, 36)),
    "lime_terracotta": ((72, 82, 37), (88, 100, 45), (103, 117, 53)),
    "pink_terracotta": ((112, 54, 55), (128, 66, 67), (160, 77, 78)),
    "gray_terracotta": ((40, 28, 24), (49, 35, 30), (57, 41, 35)),
    "light_gray_terracotta": ((95, 75, 69), (116, 92, 84), (135, 107, 98)),
    "cyan_terracotta": ((61, 64, 64), (75, 79, 79), (87, 92, 92)),
    "purple_terracotta": ((86, 51, 62), (105, 62, 75), (122, 73, 88)),
    "blue_terracotta": ((53, 43, 64), (65, 53, 79), (76, 62, 92)),
    "brown_terracotta": ((53, 35, 32), (65, 43, 30), (76, 50, 35)),
    "green_terracotta": ((53, 57, 29), (65, 70, 36), (76, 82, 42)),
    "red_terracotta": ((100, 42, 32), (122, 51, 39), (142, 60, 46)),
    "black_terracotta": ((26, 15, 11), (31, 18, 13), (37, 22, 16)),
}

HSV_WEIGHTS = {"hue": 0.47, "sat": 0.29, "val": 0.24}

# Maps RGB color to most suitable block and height difference
COLOR_CACHE = {}

print("Looking for color cache... ")
if os.path.exists("color.cache"):
    print("Color cache found, loading... ", end="")
    with open("color.cache", "rb") as f:
        COLOR_CACHE.update(pickle.load(f))
    print("done.")
else:
    print("Color cache wasn't found, image processing may take longer")
    print("Color mappings found will be saved for future use")


def get_distance(target_color: Color, compare_color: Color) -> float:
    """
    Gets the distance of one color from the other.

    Both colors are a tuple of three integers, each a component of RGB, 0 to 255.

    Colors are converted to HSV using colorsys, and their distance is calculated
    as the square root of a weighted sum of the differences
    of the squares of each color component
    """
    target_hsv = colorsys.rgb_to_hsv(*[v / 255 for v in target_color])
    compare_hsv = colorsys.rgb_to_hsv(*[v / 255 for v in compare_color])

    hue_diff = HSV_WEIGHTS["hue"] * (compare_hsv[0] - target_hsv[0]) ** 2
    sat_diff = HSV_WEIGHTS["sat"] * (compare_hsv[1] - target_hsv[1]) ** 2
    val_diff = HSV_WEIGHTS["val"] * (compare_hsv[2] - target_hsv[2]) ** 2

    return sum((hue_diff * sum(target_color), sat_diff, val_diff))


def get_block(color: Color) -> Tuple[str, int]:
    if color in COLOR_CACHE:
        return COLOR_CACHE[color]
    closest_block_id = None
    height_diff = None
    closest_distance = None
    for block_id, colors in COLORS.items():
        for n, c in enumerate(colors):
            distance = get_distance(c, color)
            if closest_block_id is None or distance < closest_distance:
                closest_block_id = block_id
                height_diff = n - 1
                closest_distance = distance

    COLOR_CACHE[color] = (closest_block_id, height_diff)
    return (closest_block_id, height_diff)


def process_pixels(pixels: Sequence[Sequence[int]]) -> List[List[Tuple[str, int]]]:
    image_size = len(pixels)
    # Process pixels into blocks and coordinates
    blocks = [[("stone", 0) for x in range(image_size)]]
    for z in range(image_size):
        print(f"Determining blocks... row {z+1}/{image_size}", end="\r")
        row = []
        for x in range(image_size):
            pixel_color = tuple(pixels[z][x])
            block_id, height_diff = get_block(pixel_color)
            block = (block_id, blocks[z][x][1] + height_diff)
            row += [block]
        blocks += [row]

    print()
    save_cache()

    return blocks


def save_cache():
    print("Saving color cache... ", end="")
    with open("color.cache", "wb") as f:
        pickle.dump(COLOR_CACHE, f)
    print("done")
