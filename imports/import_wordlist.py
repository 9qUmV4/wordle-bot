from operator import length_hint
from typing import Union
import pathlib
import pandas as pd

def read(path: Union[str, pathlib.Path], length: int) -> pd.Series:

    if isinstance(path, str):
        path = pathlib.Path(path)
    if not isinstance(path, pathlib.Path):
        raise TypeError("Must be string or pathlib.Path.")

    if not isinstance(length, int):
        raise TypeError("Length must be an integer.")
    if not length > 0:
        raise ValueError("Lenght must be greater than zero.")
    
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
