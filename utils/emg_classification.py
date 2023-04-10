import glob
import os
import re

import numpy as np
import pandas as pd
from scipy import integrate
from sklearn import linear_model, metrics


def numerical_sort(value: str) -> list:
    """
    Sorts a given string containing numerical values in ascending order
    """
    numbers = re.compile(r"(\d+)")
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


def cumulative_iemg(data: np.ndarray) -> np.ndarray:
    """
    Calculates cumulative values of iEMG
    """
    return np.abs(integrate.cumtrapz(np.abs(data), initial=0))


def get_score(x: np.ndarray, y: np.ndarray) -> float:
    model = linear_model.LinearRegression()
    model.fit(x, y)
    prediction = model.predict(x)
    return metrics.r2_score(y, prediction)


def is_consistent(data: np.ndarray) -> bool:
    """
    Returns true/false depending on whether the signal segment is consistent
    """
    x = np.arange(len(data)).reshape(-1, 1)
    y = cumulative_iemg(data)
    return get_score(x, y) >= 0.99


def classify_signals(source_path: str) -> None:
    """
    Loads and classifies signal chunks
    """
    signals = sorted(glob.glob(os.path.join(source_path, "*/")))
    for signal in signals:
        signal_chunks = sorted(
            glob.glob(os.path.join(signal, "*.txt")), key=numerical_sort
        )
        for signal_chunk in signal_chunks:
            signal_ = pd.read_csv(signal_chunk, delimiter=" ")
            needle = np.asarray(signal_["needle"])
            surface = np.asarray(signal_["surface"])
            if not (is_consistent(needle) or is_consistent(surface)):
                only_name = os.path.splitext(signal_chunk)[0]
                os.rename(signal_chunk, f"{only_name}x.txt")


if __name__ == "__main__":
    classify_signals("./segmented_signals")
