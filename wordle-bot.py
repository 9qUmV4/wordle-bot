import pandas as pd
from functions import sort_py_percentage
from imports import import_wordlist


wl = import_wordlist.read("./wordlist/wordlist.txt")

letter = []

exclude = ""
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

print(HiLtI)
print(sort_py_percentage(HiLtI))
print("Hits:", len(HiLtI))
