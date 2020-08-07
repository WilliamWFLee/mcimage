#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mcimage.color

MIT License

Copyright (c) 2020 William Lee

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE
"""

from typing import Sequence, Tuple

Color = Sequence[int]

COLORS = {
    (0, 87, 0): ("oak_leaves", -1),
    (0, 106, 0): ("oak_leaves", 0),
    (0, 124, 0): ("oak_leaves", 1),
    (0, 153, 40): ("emerald_block", -1),
    (0, 187, 0): ("emerald_block", 0),
    (0, 217, 58): ("emerald_block", 1),
    (17, 17, 17): ("black_wool", -1),
    (21, 21, 21): ("black_wool", 0),
    (25, 25, 25): ("black_wool", 1),
    (26, 15, 11): ("black_terracotta", -1),
    (31, 18, 13): ("black_terracotta", 0),
    (36, 53, 125): ("blue_wool", -1),
    (37, 22, 16): ("black_terracotta", 1),
    (40, 28, 24): ("gray_terracotta", -1),
    (44, 65, 153): ("blue_wool", 0),
    (45, 45, 180): ("water", -1),
    (49, 35, 30): ("gray_terracotta", 0),
    (51, 76, 178): ("blue_wool", 1),
    (52, 90, 180): ("lapis_block", -1),
    (53, 35, 32): ("brown_terracotta", -1),
    (53, 43, 64): ("blue_terracotta", -1),
    (53, 53, 53): ("gray_wool", -1),
    (53, 57, 29): ("green_terracotta", -1),
    (53, 89, 108): ("cyan_wool", -1),
    (55, 55, 220): ("water", 0),
    (57, 41, 35): ("gray_terracotta", 1),
    (61, 64, 64): ("cyan_terracotta", -1),
    (63, 110, 220): ("lapis_block", 0),
    (64, 64, 255): ("water", 1),
    (64, 153, 150): ("diamond_block", -1),
    (65, 43, 30): ("brown_terracotta", 0),
    (65, 53, 79): ("blue_terracotta", 0),
    (65, 65, 65): ("gray_wool", 0),
    (65, 70, 36): ("green_terracotta", 0),
    (65, 109, 132): ("cyan_wool", 0),
    (72, 53, 36): ("brown_wool", -1),
    (72, 82, 37): ("lime_terracotta", -1),
    (72, 89, 36): ("green_wool", -1),
    (72, 108, 152): ("light_blue_wool", -1),
    (74, 128, 255): ("lapis_block", 1),
    (75, 79, 79): ("cyan_terracotta", 0),
    (76, 50, 35): ("brown_terracotta", 1),
    (76, 62, 92): ("blue_terracotta", 1),
    (76, 76, 76): ("gray_wool", 1),
    (76, 82, 42): ("green_terracotta", 1),
    (76, 127, 153): ("cyan_wool", 1),
    (79, 1, 0): ("netherrack", -1),
    (79, 76, 97): ("light_blue_terracotta", -1),
    (79, 79, 79): ("cobblestone", -1),
    (79, 188, 183): ("diamond_block", 0),
    (86, 51, 62): ("purple_terracotta", -1),
    (87, 92, 92): ("cyan_terracotta", 1),
    (88, 65, 44): ("brown_wool", 0),
    (88, 100, 45): ("lime_terracotta", 0),
    (88, 109, 44): ("green_wool", 0),
    (88, 132, 186): ("light_blue_wool", 0),
    (89, 44, 125): ("purple_wool", -1),
    (89, 125, 39): ("grass_block", -1),
    (89, 144, 17): ("lime_wool", -1),
    (91, 60, 34): ("spruce_log", -1),
    (92, 219, 213): ("diamond_block", 1),
    (95, 75, 69): ("light_gray_terracotta", -1),
    (96, 1, 0): ("netherrack", 0),
    (96, 93, 119): ("light_blue_terracotta", 0),
    (96, 96, 96): ("cobblestone", 0),
    (100, 42, 32): ("red_terracotta", -1),
    (100, 84, 50): ("oak_log", -1),
    (102, 76, 51): ("brown_wool", 1),
    (102, 127, 51): ("green_wool", 1),
    (102, 153, 216): ("light_blue_wool", 1),
    (103, 117, 53): ("lime_terracotta", 1),
    (105, 61, 76): ("magenta_terracotta", -1),
    (105, 62, 75): ("purple_terracotta", 0),
    (106, 76, 54): ("dirt", -1),
    (108, 36, 36): ("red_wool", -1),
    (108, 108, 108): ("light_gray_wool", -1),
    (109, 54, 153): ("purple_wool", 0),
    (109, 153, 48): ("grass_block", 0),
    (109, 176, 21): ("lime_wool", 0),
    (111, 74, 42): ("spruce_log", 0),
    (112, 2, 0): ("netherrack", 1),
    (112, 54, 55): ("pink_terracotta", -1),
    (112, 57, 25): ("orange_terracotta", -1),
    (112, 108, 138): ("light_blue_terracotta", 1),
    (112, 112, 112): ("cobblestone", 1),
    (112, 112, 180): ("ice", -1),
    (115, 118, 129): ("clay", -1),
    (116, 92, 84): ("light_gray_terracotta", 0),
    (117, 117, 117): ("iron_block", -1),
    (122, 51, 39): ("red_terracotta", 0),
    (122, 73, 88): ("purple_terracotta", 1),
    (123, 102, 62): ("oak_log", 0),
    (125, 53, 152): ("magenta_wool", -1),
    (127, 63, 178): ("purple_wool", 1),
    (127, 178, 56): ("grass_block", 1),
    (127, 204, 25): ("lime_wool", 1),
    (128, 66, 67): ("pink_terracotta", 0),
    (128, 75, 93): ("magenta_terracotta", 0),
    (129, 86, 49): ("spruce_log", 1),
    (130, 94, 66): ("dirt", 0),
    (131, 93, 25): ("yellow_terracotta", -1),
    (132, 44, 44): ("red_wool", 0),
    (132, 132, 132): ("light_gray_wool", 0),
    (135, 107, 98): ("light_gray_terracotta", 1),
    (137, 70, 31): ("orange_terracotta", 0),
    (138, 138, 220): ("ice", 0),
    (140, 140, 140): ("mushroom_stem", -1),
    (141, 144, 158): ("clay", 0),
    (142, 60, 46): ("red_terracotta", 1),
    (143, 119, 72): ("oak_log", 1),
    (144, 144, 144): ("iron_block", 0),
    (147, 124, 113): ("white_terracotta", -1),
    (149, 87, 108): ("magenta_terracotta", 1),
    (151, 109, 77): ("dirt", 1),
    (152, 89, 36): ("orange_wool", -1),
    (153, 51, 51): ("red_wool", 1),
    (153, 65, 186): ("magenta_wool", 0),
    (153, 153, 153): ("light_gray_wool", 1),
    (159, 82, 36): ("orange_terracotta", 1),
    (160, 77, 78): ("pink_terracotta", 1),
    (160, 114, 31): ("yellow_terracotta", 0),
    (160, 160, 255): ("ice", 1),
    (161, 161, 36): ("yellow_wool", -1),
    (164, 168, 184): ("clay", 1),
    (167, 167, 167): ("iron_block", 1),
    (170, 89, 116): ("pink_wool", -1),
    (171, 171, 171): ("mushroom_stem", 0),
    (174, 164, 115): ("sandstone", -1),
    (176, 168, 54): ("gold_block", -1),
    (178, 76, 216): ("magenta_wool", 1),
    (180, 0, 0): ("redstone_block", -1),
    (180, 152, 138): ("white_terracotta", 0),
    (180, 177, 172): ("quartz_block", -1),
    (180, 180, 180): ("white_wool", -1),
    (186, 109, 44): ("orange_wool", 0),
    (186, 133, 36): ("yellow_terracotta", 1),
    (197, 197, 44): ("yellow_wool", 0),
    (199, 199, 199): ("mushroom_stem", 1),
    (208, 109, 142): ("pink_wool", 0),
    (209, 177, 161): ("white_terracotta", 1),
    (213, 201, 140): ("sandstone", 0),
    (215, 205, 66): ("gold_block", 0),
    (216, 127, 51): ("orange_wool", 1),
    (220, 0, 0): ("redstone_block", 0),
    (220, 217, 211): ("quartz_block", 0),
    (220, 220, 220): ("white_wool", 0),
    (229, 229, 51): ("yellow_wool", 1),
    (242, 127, 165): ("pink_wool", 1),
    (247, 233, 163): ("sandstone", 1),
    (250, 238, 77): ("gold_block", 1),
    (255, 0, 0): ("redstone_block", 1),
    (255, 252, 245): ("quartz_block", 1),
    (255, 255, 255): ("white_wool", 1),
}


class ColorProcessor:
    @staticmethod
    def get_distance(target_color: Color, compare_color: Color) -> float:
        """
        Gets the distance of one color from the other.

        Both colors are a tuple of three integers, each a component of RGB, 0 to 255.

        Their distance is calculated as the sum of the differences
        of the squares of each color component
        """

        return sum(abs(v2 - v1) ** 2 for v1, v2 in zip(target_color, compare_color))

    @classmethod
    def get_block(cls, color: Color) -> Tuple[str, int]:
        """
        Gets the closest block to the given colour
        """
        closest_block = None
        closest_distance = None
        for c, block in COLORS.items():
            distance = cls.get_distance(color, c)
            if closest_block is None or distance < closest_distance:
                closest_block = block
                closest_distance = distance
                if closest_distance == 0:
                    break

        return closest_block
