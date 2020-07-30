#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os

import numpy as np
from PIL import Image, UnidentifiedImageError

from color import get_block

MC_NAMESPACE_ID = "minecraft"

IMAGE_SIZE = 128
MAP_OFFSET = 64


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


def process_image(im: Image.Image) -> str:
    print("Scaling image...")
    im.thumbnail(2 * (IMAGE_SIZE,))
    image_array = np.array(im)

    # Process pixels into blocks and coordinates
    blocks = [[("stone", 0) for x in range(IMAGE_SIZE)]]
    # Cache for blocks, maps color tuple to block ID and height difference
    block_cache = {}
    for z in range(IMAGE_SIZE):
        print(
            f"Determining best blocks to use... row {z+1} out of {IMAGE_SIZE}", end="\r"
        )
        row = []
        for x in range(IMAGE_SIZE):
            pixel_color = tuple(image_array[z][x])
            if pixel_color in block_cache:
                block_id, height_diff = block_cache[pixel_color]
            else:
                block_id, height_diff = get_block(pixel_color)
                block_cache[pixel_color] = (block_id, height_diff)
            block = (block_id, blocks[z][x][1] + height_diff)
            row += [block]
        blocks += [row]
    print()

    # Normalises each column, so that the lowest block in that column is at zero
    print("Normalizing height in each column...")
    for x in range(IMAGE_SIZE):
        min_y = min(blocks[z][x][1] for z in range(-1, IMAGE_SIZE))
        for z in range(-1, IMAGE_SIZE):
            blocks[z][x] = (blocks[z][x][0], blocks[z][x][1] - min_y)

    print("Preparing commands...")
    block_commands = ""
    for z in range(-1, IMAGE_SIZE):
        for x in range(IMAGE_SIZE):
            block_id, y = blocks[z + 1][x]
            block_commands += (
                f"setblock {x - MAP_OFFSET} {y} {z - MAP_OFFSET} "
                f"{MC_NAMESPACE_ID}:{block_id}\n"
            )

    air_fill_commands = "\n".join(
        (
            f"fill {-MAP_OFFSET} {y} {-MAP_OFFSET-1} {IMAGE_SIZE - MAP_OFFSET - 1} "
            f"{y} {IMAGE_SIZE - MAP_OFFSET - 1} minecraft:air"
        )
        for y in range(256)
    )
    text = f"{air_fill_commands}\n{block_commands}"

    return text


def export_datapack(text: str, img_filename: str):
    datapack_name = "".join(
        c if c.isalnum() else "_" for c in img_filename.rsplit(".", maxsplit=1)[0]
    ).lower()
    datapack_dir = os.path.join("datapacks", datapack_name)
    functions_dir = os.path.join(datapack_dir, "data", datapack_name, "functions")

    os.makedirs(functions_dir, exist_ok=True)
    with open(os.path.join(datapack_dir, "pack.mcmeta"), "w") as f:
        metadata = {
            "pack": {
                "pack_format": 5,
                "description": f"Draws {img_filename} using Minecraft blocks. Made with mcimage",
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

    function_text = process_image(im)
    export_datapack(function_text, filename)


if __name__ == "__main__":
    main()
