import pathlib
import string
import pandas as pd
import numpy as np
from imports import import_wordlist
from functions import sort_py_percentage

path = pathlib.Path("./wordlist/wordlist.txt")
# path = pathlib.Path("./wordlist/wordlist-german.txt")

wl = import_wordlist.read(path)

# Only use words of len 5
wl = wl[wl.str.len() == 5]
wl: pd.Series = wl.reset_index(drop=True).squeeze()

# Sort the list by percentage
best_word_list = sort_py_percentage(wl)
best_word_list = best_word_list * 100

print(best_word_list.head(10))