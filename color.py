#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mcimage.color
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

import hashlib
import os
import pickle
from typing import Sequence, Tuple

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


class ColorCache:
    """
    A class for mapping RGB color tuples to most appropriate blocks and elevations
    """

    _CACHE_FILENAME = os.path.join(os.path.dirname(__file__), "color.cache")

    def __init__(self, cache_dict=None):
        self.cache_dict = {} if cache_dict is None else cache_dict
        self._cache_hash = None
        self._changed = False

    @classmethod
    def _get_file_hash(cls):
        if os.path.exists(cls._CACHE_FILENAME):
            md5 = hashlib.md5()
            with open(cls._CACHE_FILENAME, "rb") as f:
                for line in f:
                    md5.update(line)
            return md5.hexdigest()

    def _update_cache(self):
        # Loads color cache, and updates to cache_dict
        if os.path.exists(self._CACHE_FILENAME):
            with open(self._CACHE_FILENAME, "rb") as f:
                self.cache_dict.update(pickle.load(f))
                self._cache_hash = self._get_file_hash()

    def open(self):
        """
        Opens the color cache from file
        """
        print("Loading color mappings from file...")
        self._update_cache()

    def save(self):
        """
        Updates and saves the cache to file
        """
        if not self._changed:
            print("Mappings were not changed, so no save required")
            return
        print("Saving color mappings, please wait...")
        if self._get_file_hash() != self._cache_hash:
            self._update_cache()
        with open(f"{self._CACHE_FILENAME}-journal", "wb") as f:
            pickle.dump(self.cache_dict, f)
            f.flush()
            os.fsync(f.fileno())

        os.rename(f"{self._CACHE_FILENAME}-journal", self._CACHE_FILENAME)

    def find(self, color: Color) -> Tuple[str, int]:
        """
        Finds corresponding block/elevation difference in cache

        Returns None is not found
        """
        return self.cache_dict[color] if color in self.cache_dict else None

    def add(self, color: Color, block_id: str, height_diff: int, replace: bool = True):
        """
        Adds a new color to the cache

        If replace is True, then the given color in cache is replaced if it exists,
        else a ValueError is raised.
        """
        if not isinstance(color, tuple):
            raise TypeError(
                f"Color must be of type 'tuple', got {type(color).__name__!r}"
            )
        if len(color) != 3:
            raise ValueError(f"Color must be of length 3, got {len(color)}")

        if not replace and color in self.cache_dict:
            raise ValueError("Mapping for color {color} already exists")
        self.cache_dict[color] = (block_id, height_diff)
        self._changed = True

    def copy(self):
        """
        Returns a copy of the cache object
        """
        return type(self)(self.cache_dict)

    def merge(self, *others):
        """
        Merges other cache objects with this cache object
        """
        for other in others:
            self.cache_dict.update(other.cache_dict)
        self._changed = True

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()

    def __iter__(self):
        return iter(self.cache_dict)

    def __contains__(self, key):
        return key in self.cache_dict

    def __setitem__(self, key, value):
        self.add(key, *value)

    def __getitem__(self, key):
        color = self.find(key)
        if color is None:
            raise KeyError(color)
        return color


class ColorProcessor:
    @staticmethod
    def get_distance(target_color: Color, compare_color: Color) -> float:
        """
        Gets the distance of one color from the other.

        Both colors are a tuple of three integers, each a component of RGB, 0 to 255.

        Their distance is calculated as the square root of the sum of the differences
        of the squares of each color component
        """

        return sum((v2 - v1) ** 2 for v1, v2 in zip(target_color, compare_color))

    @classmethod
    def get_block(cls, color: Color, cache: ColorCache) -> Tuple[str, int]:
        if color in cache:
            return cache[color]
        closest_block_id = None
        height_diff = None
        closest_distance = None
        for block_id, colors in COLORS.items():
            for n, c in enumerate(colors):
                distance = cls.get_distance(color, c)
                if closest_block_id is None or distance < closest_distance:
                    closest_block_id = block_id
                    height_diff = n - 1
                    closest_distance = distance
                    if closest_distance == 0:
                        break
            else:
                continue
            break

        cache[color] = (closest_block_id, height_diff)
        return (closest_block_id, height_diff)
