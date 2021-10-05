from os import access, R_OK
from os.path import exists, isfile, dirname
from typing import Tuple

import numpy


class ReadError(Exception):
    def __init__(self, msg: str):
        self.__msg = msg

    def __str__(self) -> str:
        return self.__msg


def _safe_parse_str(s: str) -> float:
    try:
        return float(s)
    except ValueError:
        raise ReadError(f"Expected input measure to be float number, got {s}")


def read_data(input_file: str) -> Tuple[numpy.ndarray, numpy.ndarray]:
    xs, ys = [], []
    with open(input_file) as f:
        for line in f:
            # Parse next line in file
            try:
                x, y = line.split()
            except ValueError:
                raise ReadError(f"Expected two values separated with space in each line, got {line}")

            # Safe parsing each measurement
            xs.append(_safe_parse_str(x))
            ys.append(_safe_parse_str(y))

    xs = numpy.array(xs)
    ys = numpy.array(ys)
    sorted_idx = numpy.argsort(xs)
    return xs[sorted_idx], ys[sorted_idx]


def save_result(diff: int, error: int, conjugation: int, output_file: str):
    with open(output_file, "w") as f:
        f.write(f"{diff} {error} {conjugation}\n")


def validate_input_path(input_path: str) -> bool:
    if not exists(input_path):
        raise FileExistsError(f"Input file does not exist: {input_path}")
    if not isfile(input_path):
        raise FileExistsError("Passed input file is not a valid file")
    if not access(input_path, R_OK):
        raise FileExistsError("Input file is not readable")
    return True


def validate_output_path(output_path: str) -> bool:
    parent = dirname(output_path)
    if not exists(parent):
        raise FileExistsError(f"Folder for output file is not exist ({parent})")
    if not isfile(output_path):
        raise FileExistsError("Passed output file is not a valid file")
    return True
