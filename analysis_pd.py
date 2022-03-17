import pandas as pd

wl: pd.Series = pd.read_table("./wordlist/wordlist-german.txt").squeeze()
wl: pd.Series = wl.str.lower()

for k, r in {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"}.items():
    wl = wl.str.replace(k, r)

wl = wl[wl.str.len() == 5]

exclude = list((r"'", r"-", r"/", r"\(", r"\)", r"\x03", r"\x07", r"\x08", r"\.", r"ø", r"å", r"é", r"á", r"ó", r"ç", r"è", r"ê", r"ë", r"ñ", r"ô", r"í", r"à"))
for e in exclude:
    wl = wl[~wl.str.contains(e)]

wl: pd.Series = wl.reset_index(drop=True).squeeze()

print(wl)
