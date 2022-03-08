from xml.etree.ElementInclude import include
import pandas as pd

wl: pd.Series = pd.read_table("./wordlist/wordlist.txt").squeeze()

wl5 = wl[wl.str.len() == 5]
wl5 = wl5[~wl5.str.contains(r"-")]
wl5 = wl5[~wl5.str.contains(r"\(")]
wl5 = wl5[~wl5.str.contains(r"\)")]
wl5: pd.Series = wl5.reset_index(drop=True).squeeze()

letter = []

exclude = "tkahdfrnp"
include_l = "ae"

include_l = list(include_l)
for l in include_l:
    wl5: pd.Series = wl5[wl5.str.contains(l)]

letter.append(  exclude + ""  )
letter.append(  exclude + ""  )
letter.append(  exclude + "ae"  )
letter.append(  exclude + ""  )
letter.append(  exclude + "e"  )

for i in range(len(letter)):
    letter[i] = "[^" + letter[i] + "]"

# letter[0] = "s"
letter[1] = "e"
# letter[2] = "o"
letter[3] = "a"
letter[4] = "l"


pattern = r"^{0[0]}{0[1]}{0[2]}{0[3]}{0[4]}$".format(letter)
print(pattern)

HiLtI = wl5[wl5.str.match(pattern)]
HiLtI: pd.Series = HiLtI.reset_index(drop=True).squeeze()

print(HiLtI.head(50))

