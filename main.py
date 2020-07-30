#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
from typing import Sequence, Tuple

import numpy as np
from PIL import Image, UnidentifiedImageError

from color import process_pixels

IMAGE_SIZE = 128
MAP_OFFSET = 64

SETBLOCK_TEMPLATE = "setblock {x} {y} {z} {block_id}\n"
FILL_TEMPLATE = "fill {x1} {y1} {z1} {x2} {y2} {z2} {block_id}\n"


def get_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mcimage",
        description="Generates a function file to place blocks in Minecraft for pixel art",
    )
    parser.add_argument("filename")
    return parser


def get_filename(parser: argparse.ArgumentParser) -> str:
    args = parser.parse_args()
    return args.filename


def normalize_columns(blocks):
    """
    Normalizes the height of blocks in the column
    such that the lowest block is at the zero level
    """
    print("Normalizing height in each column...")
    for x in range(IMAGE_SIZE):
        min_y = min(blocks[z][x][1] for z in range(-1, IMAGE_SIZE))
        for z in range(-1, IMAGE_SIZE):
            blocks[z][x] = (blocks[z][x][0], blocks[z][x][1] - min_y)


def process_image(im: Image.Image):
    """
    Scales and processes the image to an array of pixels
    """
    print("Scaling image...")
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
                y=y,
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
        for y in range(256)
    )
    text = f"{air_fill_commands}{block_commands}"

    print("done")
    return text


def process_image_to_commands(im: Image.Image) -> str:
    """
    Processes an image opened in Pillow to commands
    """
    pixels = process_image(im)
    blocks = process_pixels(pixels)
    text = prepare_commands(blocks)

    return text


def export_datapack(text: str, img_filename: str):
    """
    Exports a datapack which the function text

    The function is saved in a datapack called mcimage.

    The function to draw the image is namespaced under the image filename,
    lowercased and all non-alphanumeric characters replaced with underscores
    """
    namespace = "".join(
        c.lower() if c.isalnum() else "_"
        for c in img_filename.rsplit(".", maxsplit=1)[0]
    )
    datapack_dir = os.path.join("datapacks", "mcimage")
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
        f.write(text)


def main():
    parser = get_arg_parser()
    filename = get_filename(parser)
    try:
        im = Image.open(filename)
    except UnidentifiedImageError:
        parser.error(f"{filename} is not an image file")

    function_text = process_image_to_commands(im)
    export_datapack(function_text, filename)


if __name__ == "__main__":
    main()
