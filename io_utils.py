from typing import Tuple

import numpy


def read_data(input_file: str) -> Tuple[numpy.ndarray, numpy.ndarray]:
    xs, ys = [], []
    with open(input_file) as f:
        for line in f:
            x, y = line.split()
            xs.append(float(x))
            ys.append(float(y))
    xs = numpy.array(xs)
    ys = numpy.array(ys)
    sorted_idx = numpy.argsort(xs)
    return xs[sorted_idx], ys[sorted_idx]


def save_result(diff: int, error: int, conjugation: int, output_file: str):
    with open(output_file, "w") as f:
        f.write(f"{diff} {error} {conjugation}\n")
