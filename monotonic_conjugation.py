from argparse import ArgumentParser

import numpy
from scipy.stats import rankdata

from io_utils import read_data, save_result, validate_input_path, validate_output_path, ReadError


def float_to_int(num: float) -> int:
    return int(round(num))


def main(input_path: str, output_path: str):
    try:
        validate_input_path(input_path)
    except FileExistsError as err:
        print(err)
        return
    try:
        validate_output_path(output_path)
    except FileExistsError as err:
        print(err)
        return

    try:
        xs, ys = read_data(input_path)
    except ReadError as err:
        print(err)
        return

    n = len(xs)
    if n < 9:
        print("Monotonic conjugation check works correctly only for more than 9 measures.")
        return

    # scipy's rankdata returns ranks from min to max, therefore manually invert them
    ranks = rankdata(ys, method="average")
    ranks = -(ranks - numpy.max(ranks) - 1)

    p = float_to_int(n / 3)
    r1 = ranks[:p].sum()
    r2 = ranks[-p:].sum()

    diff = r1 - r2
    error = (n + 0.5) * numpy.sqrt(p / 6)
    conjugation = diff / (p * (n - p))

    save_result(float_to_int(diff), float_to_int(error), round(conjugation, 2), output_path)


if __name__ == "__main__":
    __arg_parser = ArgumentParser(description="Script for calculating monotonic conjugation")
    __arg_parser.add_argument("--input", type=str, default="data/in.txt", help="Path to file with input data")
    __arg_parser.add_argument("--output", type=str, default="data/out.txt", help="Path to output file")

    __args = __arg_parser.parse_args()
    main(__args.input, __args.output)
