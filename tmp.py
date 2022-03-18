import string
from traceback import print_tb
from xmlrpc.client import FastParser
import pandas as pd
import numpy as np

wl: pd.Series = pd.read_table("./wordlist/wordlist.txt").squeeze()

wl = wl.str.lower()
for k, r in {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"}.items():
    wl = wl.str.replace(k, r)
wl = wl[wl.str.len() == 5]
wl = wl[~wl.str.contains(r"-")]
wl = wl[~wl.str.contains(r"\(")]
wl = wl[~wl.str.contains(r"\)")]
wl: pd.Series = wl.reset_index(drop=True).squeeze()


dt = wl.str.split("", expand=True)
dt: pd.DataFrame = dt.drop(columns=[0, 6])
dt.columns = range(dt.columns.size)

dt_c = pd.DataFrame(data=np.nan, index=list(string.ascii_lowercase), columns=range(5))

for c in string.ascii_lowercase:
    dt_tmp: pd.DataFrame = (dt == c).replace({False: 0, True: 1})
    dt_c.loc[c, :] = dt_tmp.sum(axis="index", skipna=True)

dt_cn = (dt_c / len(wl)) * 100

print(dt_cn)

for col in range(len(dt.columns)):
    dt.iloc[: col] = 


dt_p = 