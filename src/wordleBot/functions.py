import logging
import pathlib
import string
import sys
from typing import Union

import numpy as np
import pandas as pd


def sort_by_percentage(wl: pd.Series) -> pd.Series:
    """Takes a pd.Series list containing words and returns them sorted by percentage. 
    Returns a pd.Series with the percentage in the Index and word as value"""
    # Check if dataframe is empty
    
    if isinstance(wl, str):
        return pd.Series(data=[wl,], index=[1, ])
    # Split up string into single chars
    dt = wl.str.split("", expand=True).iloc[:,1:-1]
    
    
    dt_c = dt.apply(pd.value_counts, normalize=True, sort=False)
    dt_percentage = dt.replace(dt_c).sum("columns") / 5
    
    df_sorted = pd.concat({"word": wl, "percentage": dt_percentage}, axis=1).sort_values("percentage", ascending=False)
    return df_sorted["word"]


def read(path: Union[str, pathlib.Path], length: int) -> pd.Series:
    """Imports the list with all words

    Args:
        path (Union[str, pathlib.Path]): Path to wordlist
        length (int): Lenght of words to keep, must be lenght of wordle

    Raises:
        TypeError: Raised if filepath is not string nor Path
        TypeError: Raised if wordle lenght is not an integer
        ValueError: Raised if leanght is 0 or lower

    Returns:
        pd.Series: Wordlist as pd.Series
    """

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
    wl.dropna(inplace=True)
    wl = wl.str.lower()

    # Replace German umlauts
    for k, r in {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"}.items():
    # TODO no for loop
        wl = wl.str.replace(k, r)

    # Exclude special characters, use only [a-z]
    wl = wl[wl.str.fullmatch("^[a-z]+$")]

    # Only use words of len length
    wl = wl[wl.str.len() == length]
    wl: pd.Series = wl.reset_index(drop=True).squeeze()

    return wl
