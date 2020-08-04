#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mcimage
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

import argparse
import json
import os
from typing import Tuple

import numpy as np
from PIL import Image, UnidentifiedImageError

from color import ColorProcessor, ColorCache

MAP_SIZE = 128
MAP_OFFSET = 64
BASE_HEIGHT = 1
COMMANDS_PER_FUNCTION = 65536
COMMAND_BLOCK_POS = (-75, 80, -64)
VIEWING_PLATFORM_RADIUS = 5

SETBLOCK_TEMPLATE = "setblock {} {} {} minecraft:{} replace\n"
FILL_TEMPLATE = "fill {} {} {} {} {} {} minecraft:{}\n"


def parse_args() -> Tuple[argparse.ArgumentParser, argparse.Namespace]:
    parser = argparse.ArgumentParser(
        prog="mcimage",
        description="Generates a function file to place blocks in Minecraft for pixel art",
    )
    parser.add_argument(
        "-d",
        metavar="dir",
        dest="datapack_dir",
        help="Directory to place generated datapacks",
        default=os.path.join(os.path.dirname(__file__), "datapacks"),
    )
    parser.add_argument(
        "-n",
        metavar="name",
        dest="datapack_name",
        help="Name of datapack to export, which contains the function file",
        default="mcimage",
    )
    parser.add_argument(
        "--ns",
        metavar="namespace",
        dest="namespace",
        help="Namespace of the function. Defaults to be being derived from filename",
    )
    parser.add_argument(
        "--size",
        metavar="size",
        help="Size of image to scale to, 1 for 128x128 (default), 2 for 256x256",
        choices=(1, 2),
        default=1,
        type=int,
    )
    parser.add_argument("filename")

    args = parser.parse_args()
    return parser, args


class MCImage:
    def __init__(
        self,
        filename: str,
        size: str,
        dp_name: str,
        dp_dir: str,
        parser: argparse.ArgumentParser,
    ):
        self.filename = filename
        self.dp_name = dp_name
        self.dp_dir = dp_dir
        self.parser = parser
        self._image_size = MAP_SIZE * size

    def _normalize_columns(self):
        """
        Normalizes the height of blocks in the column
        such that the lowest block is at the zero level
        """
        print("Normalizing height in each column... ", end="")
        for x in range(self._image_size):
            min_y = min(
                self.blocks[z][x][1]
                for z in range(-1, self._image_size)
                if self.blocks[z][x][0] != "stone"
            )
            for z in range(-1, self._image_size):
                self.blocks[z][x] = (self.blocks[z][x][0], self.blocks[z][x][1] - min_y)

        print("done")

    def _block_off_water(self):
        """
        Blocks off water blocks on their surrounding sides to prevent it
        from spilling over other blocks
        """
        print("Blocking off any water blocks...")
        self._water_blockers = set()
        for z in range(1, len(self.blocks)):
            for x in range(len(self.blocks[z])):
                block_id, y = self.blocks[z][x]
                if block_id == "water":
                    for dx, dz in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                        if (
                            (0 <= x + dx < len(self.blocks[z]))
                            and (0 <= z + dz < len(self.blocks))
                            and self.blocks[z + dz][x + dx][1] < y
                        ):
                            self._water_blockers.add((x + dx, y, z + dz - 1))

    def _process_image(self):
        """
        Scales and processes the image to an array of pixels
        """
        print("Processing image...")
        self._open_image()
        print(f"Size of image is {self.im.size}")

        not_square = False
        if self.im.size[0] != self.im.size[1]:
            print("Image size is not square")
            print("Image will be cropped to largest centered square possible")
            square_width = min(self.im.size)
            not_square = True
            x, y = ((c - square_width) / 2 for c in self.im.size)

        print(f"Scaling to {2 * (self._image_size,)}")
        self.im = self.im.resize(
            2 * (self._image_size,),
            resample=Image.LANCZOS,
            box=(x, y, x + square_width, y + square_width) if not_square else None,
            reducing_gap=3.0,
        )
        self.pixels = np.array(self.im)

    def _determine_blocks(self):
        # Process pixels into blocks and coordinates
        self.blocks = [[("stone", -1) for x in range(self._image_size)]]
        with ColorCache() as cache:
            for z in range(self._image_size):
                print(f"Determining blocks... row {z+1}/{self._image_size}", end="\r")
                row = []
                for x in range(self._image_size):
                    pixel_color = tuple(self.pixels[z][x])
                    block_id, height_diff = ColorProcessor.get_block(pixel_color, cache)
                    block = (block_id, self.blocks[z][x][1] + height_diff)
                    row += [block]
                self.blocks += [row]
            print()

    def _process_pixels(self):
        self._determine_blocks()
        self._normalize_columns()
        self._block_off_water()

    def _prepare_commands(self) -> str:
        """
        Prepares commands from the given blocks
        """
        print("Preparing commands... ", end="")

        self._commands = ["tell @p Placing blocks, please be patient...\n"]
        for z in range(-1, self._image_size):
            for x in range(self._image_size):
                block_id, y = self.blocks[z + 1][x]
                self._commands.append(
                    SETBLOCK_TEMPLATE.format(
                        x - MAP_OFFSET, y + BASE_HEIGHT, z - MAP_OFFSET, block_id,
                    )
                )
                self._commands.append(
                    FILL_TEMPLATE.format(
                        x - MAP_OFFSET,
                        y + BASE_HEIGHT + 1,
                        z - MAP_OFFSET,
                        x - MAP_OFFSET,
                        255,
                        z - MAP_OFFSET,
                        "air",
                    )
                )

        for x, y, z in self._water_blockers:
            self._commands.append(
                SETBLOCK_TEMPLATE.format(
                    x - MAP_OFFSET, y + BASE_HEIGHT, z - MAP_OFFSET, "glass",
                )
            )

        print("done")

    def _export_datapack(self):
        """
        Exports a datapack with the function text

        The function is saved in a datapack under ``name``.

        The function to draw the image is namespaced under ``namespace``
        """

        def get_adjusted_coords(base_coords, coords_diff):
            return (c + diff for c, diff in zip(base_coords, coords_diff))

        namespace = self._namespace_from_filename(self.filename)

        print("Exporting commands to datapack... ")
        datapack_dir = os.path.join(self.dp_dir, self.dp_name)
        functions_dir = os.path.join(datapack_dir, "data", namespace, "functions")

        os.makedirs(functions_dir, exist_ok=True)
        with open(os.path.join(datapack_dir, "pack.mcmeta"), "w") as f:
            metadata = {
                "pack": {
                    "pack_format": 5,
                    "description": "Draw images in Minecraft with map pixel art",
                }
            }
            json.dump(metadata, f)

        for n, commands in enumerate(
            self._commands[i : i + COMMANDS_PER_FUNCTION]
            for i in range(0, len(self._commands), COMMANDS_PER_FUNCTION)
        ):
            with open(os.path.join(functions_dir, f"draw_{n}.mcfunction"), "w") as f:
                f.write("".join(commands))
        with open(os.path.join(functions_dir, "setup.mcfunction"), "w") as f:
            f.write(
                FILL_TEMPLATE.format(
                    *COMMAND_BLOCK_POS,
                    *get_adjusted_coords(COMMAND_BLOCK_POS, (-1, 5, 0)),
                    "air",
                )
            )
            for i in range(n + 1):
                block_id = "chain_command_block" if i else "command_block"
                block_state = "[facing=up]"
                block_entity_data = (
                    f"{{Command: 'function {namespace}:draw_{i}'"
                    + (", auto: 1" if i else "")
                    + "}"
                )
                f.write(
                    SETBLOCK_TEMPLATE.format(
                        *get_adjusted_coords(COMMAND_BLOCK_POS, (0, i, 0)),
                        f"{block_id}{block_state}{block_entity_data}",
                    )
                )
                if not i:
                    f.write(
                        SETBLOCK_TEMPLATE.format(
                            *get_adjusted_coords(COMMAND_BLOCK_POS, (-1, 0, i)),
                            "stone_button[face=wall, facing=west]",
                        )
                    )
            f.write(
                FILL_TEMPLATE.format(
                    *get_adjusted_coords(
                        COMMAND_BLOCK_POS,
                        (VIEWING_PLATFORM_RADIUS, -1, VIEWING_PLATFORM_RADIUS),
                    ),
                    *get_adjusted_coords(
                        COMMAND_BLOCK_POS,
                        (-VIEWING_PLATFORM_RADIUS, -1, -VIEWING_PLATFORM_RADIUS),
                    ),
                    "glass",
                )
                + (
                    "gamemode creative @s\n"
                    "tp @s {} {} {} -90 0\n".format(
                        *get_adjusted_coords(COMMAND_BLOCK_POS, (-3, 0, 0))
                    )
                )
            )

        print(f"Datapack exported as directory {datapack_dir}")
        print(f"Setup function is called {namespace}:setup")

    @staticmethod
    def _namespace_from_filename(filename: str):
        """
        Generates a namespace from a filename

        Namespace is the filename, stripped of extension, lowercased
        and all non-alphanumeric characters replaced with underscores
        """
        namespace = "".join(
            c.lower() if c.isalnum() else "_"
            for c in os.path.basename(filename).rsplit(".", maxsplit=1)[0]
        )

        return namespace

    def _open_image(self):
        try:
            self.im = Image.open(self.filename).convert("RGB")
        except UnidentifiedImageError:
            self.parser.error(f"{self.filename} is not an image file")
        except FileNotFoundError:
            self.parser.error(f"{self.filename} was not found")

    def process(self):
        self._process_image()
        self._process_pixels()
        self._prepare_commands()
        self._export_datapack()


def main():
    parser, args = parse_args()
    mcimage = MCImage(
        args.filename, args.size, args.datapack_name, args.datapack_dir, parser
    )
    mcimage.process()


if __name__ == "__main__":
    main()
