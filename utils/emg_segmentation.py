import glob
import math
import os

import numpy as np
import pandas as pd


def get_segments(data: np.ndarray, segment_size: int = 3000) -> tuple:
    """
    Splits data into segments of equal size
    """
    n = int((math.floor(len(data) / 100000) * 100000) / segment_size)
    data = data[0 : segment_size * n]
    data_segments = data.reshape(n, segment_size)
    residuum = data[segment_size * n + 1 : -1]
    return data_segments, n, residuum


def segment_signals(source_path: str, destination_path: str, segment_size: int) -> None:
    """
    Loads signals and saves them as segments
    """
    filenames = glob.glob(os.path.join(source_path, "*.txt"))
    n = len(filenames)

    if not os.path.exists(destination_path):
        os.mkdir(destination_path)

    for f in filenames:
        data = pd.read_csv(f, delimiter=" ")
        needle = np.asarray(data["needle"])
        surface = np.asarray(data["surface"])

        needle_segments, n, _ = get_segments(data=needle, segment_size=segment_size)
        surface_segments, n, _ = get_segments(data=surface, segment_size=segment_size)

        signal_name = os.path.splitext(f)[0][-5:]
        dir_path = os.path.join(destination_path, signal_name)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        for i in range(n):
            column_names = ["needle", "surface"]
            segment_ = pd.DataFrame(columns=column_names)
            segment_["needle"] = needle_segments[i]
            segment_["surface"] = surface_segments[i]
            segment_.to_csv(
                os.path.join(destination_path, dir_path[-5:], f"{str(i + 1)}.txt"),
                sep=" ",
                index=False,
            )


if __name__ == "__main__":
    segment_signals("./signals", "./segmented_signals", 30000)
