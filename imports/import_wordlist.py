from typing import Union
import pathlib
import pandas as pd
import numpy as np

def read(path: Union[str, pathlib.Path], length) -> pd.DataFrame:

    if isinstance(path, str):
        path = pathlib.Path(path)
    if not isinstance(path, pathlib.Path):
        raise TypeError("Must be string or pathlib.Path")
    
    # Read in the file as a Series
    wl: pd.Series = pd.read_table(path, dtype=str).squeeze()

    # Lower all strings and drop NaN values
    wl = wl.str.lower()
    wl.dropna(inplace=True)

    # Replace German umlauts
    for k, r in {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"}.items():
        wl = wl.str.replace(k, r)

    # Exclude special characters, that can't be typed
    exclude = [r"'", r"-", r"/", r"\(", r"\)", r"\x03", r"\x07", r"\x08", r"\.", r"ø", r"å", r"é", r"á", r"ó", r"ç", r"è", r"ê", r"ë", r"ñ", r"ô", r"í", r"à"]
    for e in exclude:
        wl = wl[~wl.str.contains(e)]

    # Only use words of len length
    wl = wl[wl.str.len() == length]
    wl: pd.Series = wl.reset_index(drop=True).squeeze()

    return wl
