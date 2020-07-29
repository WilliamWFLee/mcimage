#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

from PIL import Image, UnidentifiedImageError


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


def main():
    parser = get_arg_parser()
    filename = get_filename(parser)
    try:
        im = Image.open(filename)
    except UnidentifiedImageError:
        parser.error(f"{filename} is not an image file")


main()
