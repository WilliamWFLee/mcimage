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
from typing import Sequence, Tuple

import numpy as np
from PIL import Image, UnidentifiedImageError

from color import process_pixels

IMAGE_SIZE = 128
MAP_OFFSET = 64
BASE_HEIGHT = 10

SETBLOCK_TEMPLATE = "setblock {x} {y} {z} {block_id}\n"
FILL_TEMPLATE = "fill {x1} {y1} {z1} {x2} {y2} {z2} {block_id}\n"


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
    parser.add_argument("filename")

    args = parser.parse_args()
    return parser, args


def normalize_columns(blocks):
    """
    Normalizes the height of blocks in the column
    such that the lowest block is at the zero level
    """
    print("Normalizing height in each column... ", end="")
    for x in range(IMAGE_SIZE):
        min_y = min(blocks[z][x][1] for z in range(-1, IMAGE_SIZE))
        for z in range(-1, IMAGE_SIZE):
            blocks[z][x] = (blocks[z][x][0], blocks[z][x][1] - min_y)

    print("done")


def process_image(im: Image.Image):
    """
    Scales and processes the image to an array of pixels
    """
    print("Processing image...")
    print(f"Size of image is {im.size}")
    if im.size[0] != im.size[1]:
        print("Image size is not square")
        print("Image will be cropped to largest centered square possible")
        square_width = min(im.size)
        x, y = ((c - square_width) / 2 for c in im.size)
        im = im.crop((x, y, x + square_width, y + square_width))

    print(f"Scaling to {2 * (IMAGE_SIZE,)}")
    im.thumbnail(2 * (IMAGE_SIZE,))

    return np.array(im)


def prepare_commands(blocks: Sequence[Sequence[Tuple[str, int]]]) -> str:
    """
    Prepares commands from the given blocks
    """
    print("Preparing commands... ", end="")
    image_size = len(blocks[0])
    block_commands = ""
    for z in range(-1, image_size):
        for x in range(image_size):
            block_id, y = blocks[z + 1][x]
            block_commands += SETBLOCK_TEMPLATE.format(
                x=x - MAP_OFFSET,
                y=y + BASE_HEIGHT,
                z=z - MAP_OFFSET,
                block_id=f"minecraft:{block_id}",
            )

    air_fill_commands = "".join(
        FILL_TEMPLATE.format(
            x1=-MAP_OFFSET,
            y1=y,
            z1=-MAP_OFFSET - 1,
            x2=image_size - MAP_OFFSET - 1,
            y2=y,
            z2=image_size - MAP_OFFSET - 1,
            block_id="minecraft:air",
        )
        for y in range(BASE_HEIGHT, 256)
    )
    text = f"gamemode creative @s\ntp @s 0 150 0\n{air_fill_commands}{block_commands}"

    print("done")
    return text


def process_image_to_commands(im: Image.Image) -> str:
    """
    Processes an image opened in Pillow to commands
    """
    pixels = process_image(im)
    blocks = process_pixels(pixels)
    normalize_columns(blocks)
    text = prepare_commands(blocks)

    return text


def export_datapack(commands: str, name: str, directory: str, namespace: str):
    """
    Exports a datapack which the function text

    The function is saved in a datapack under ``name``.

    The function to draw the image is namespaced under ``namespace``
    """

    print("Exporting commands to datapack... ", end="")
    datapack_dir = os.path.join(directory, name)
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

    with open(os.path.join(functions_dir, "draw.mcfunction"), "w") as f:
        f.write(commands)
    print("done")
    print(f"Datapack exported as directory {datapack_dir}")
    print(f"Function name will be {namespace}:draw")


def namespace_from_filename(img_filename: str):
    """
    Generates a namespace from a filename

    Namespace is the filename, stripped of extension, lowercased
    and all non-alphanumeric characters replaced with underscores
    """
    namespace = "".join(
        c.lower() if c.isalnum() else "_"
        for c in os.path.basename(img_filename).rsplit(".", maxsplit=1)[0]
    )

    return namespace


def main():
    parser, args = parse_args()
    try:
        im = Image.open(args.filename).convert("RGB")
    except UnidentifiedImageError:
        parser.error(f"{args.filename} is not an image file")
    except FileNotFoundError:
        parser.error(f"{args.filename} was not found")

    commands = process_image_to_commands(im)
    export_datapack(
        commands,
        args.datapack_name,
        args.datapack_dir,
        namespace_from_filename(args.filename),
    )


if __name__ == "__main__":
    main()
