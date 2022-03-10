import pandas as pd

wl: pd.Series = pd.read_table("./wordlist/wordlist-german.txt").squeeze()

wl: pd.Series = wl.str.lower()
for k, r in {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"}.items():
    wl = wl.str.replace(k, r)
wl = wl[wl.str.len() == 5]
wl = wl[~wl.str.contains(r"-")]
wl = wl[~wl.str.contains(r"\(")]
wl = wl[~wl.str.contains(r"\)")]
wl: pd.Series = wl.reset_index(drop=True).squeeze()

letter = []

exclude = "fotzamhd"
include_l = "re"

include_l = list(include_l)
for l in include_l:
    wl: pd.Series = wl[wl.str.contains(l)]

letter.append(  exclude + ""  )
letter.append(  exclude + "r"  )
letter.append(  exclude + ""  )
letter.append(  exclude + "e"  )
letter.append(  exclude + ""  )

for i in range(len(letter)):
    letter[i] = "[^" + letter[i] + "]"

# letter[0] = "s"
letter[1] = "e"
letter[2] = "r"
# letter[3] = "s"
letter[4] = "e"


pattern = r"^{0[0]}{0[1]}{0[2]}{0[3]}{0[4]}$".format(letter)
print(pattern)

HiLtI = wl[wl.str.match(pattern)]
HiLtI: pd.Series = HiLtI.reset_index(drop=True).squeeze()

print(HiLtI.head(50))
print("Hits:", len(HiLtI))

