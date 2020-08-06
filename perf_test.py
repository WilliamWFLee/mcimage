#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import timeit


def main():
    results = timeit.repeat(
        stmt="[color.ColorProcessor.get_block(c, color.ColorCache()) for c in colors]",
        setup=(
            "import random; import color; "
            "colors = [tuple(random.randrange(256) for _ in range(3)) for _ in range(10000)]"
        ),
        repeat=5,
        number=10,
    )
    print("Average for 10 loops, best of 5:", sum(results) / 5)


main()
