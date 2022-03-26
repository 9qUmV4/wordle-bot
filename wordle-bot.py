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

exclude = "a"
include_l = ""

include_l = list(include_l)
for l in include_l:
    wl: pd.Series = wl[wl.str.contains(l)]

letter.append(  exclude + ""  )
letter.append(  exclude + ""  )
letter.append(  exclude + ""  )
letter.append(  exclude + ""  )
letter.append(  exclude + ""  )

for i in range(len(letter)):
    letter[i] = "[^" + letter[i] + "]"

# letter[0] = ""
# letter[1] = ""
# letter[2] = ""
# letter[3] = ""
# letter[4] = ""


pattern = r"^{0[0]}{0[1]}{0[2]}{0[3]}{0[4]}$".format(letter)
print(pattern)

HiLtI = wl[wl.str.match(pattern)]
HiLtI: pd.Series = HiLtI.reset_index(drop=True).squeeze()

print(HiLtI.head(50))
print("Hits:", len(HiLtI))

