#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import timeit

"""
Performance tests for the get_block method

Compares where the target color is a numpy array of length 3, dtype=np.uint8,
and where the target color is 3-tuple of int.
"""

REPEAT = 5
NUMBER = 1000


def main():
    for (stmt, setup) in (
        (
            "color.ColorProcessor.get_block(c, color.ColorCache())",
            "import random; import color; c = tuple(random.randrange(256) for _ in range(3))",
        ),
        (
            "color.ColorProcessor.get_block(tuple(c), color.ColorCache())",
            "import random; import color; import numpy as np; c = np.array([random.randrange(256) for _ in range(3)], dtype=np.uint8)",
        ),
    ):
        results = timeit.repeat(stmt=stmt, setup=setup, repeat=REPEAT, number=NUMBER,)
        print(
            f"Average for {NUMBER} loops, best of {REPEAT}:", sum(results) / 5,
        )


main()
