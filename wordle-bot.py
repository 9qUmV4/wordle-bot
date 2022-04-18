import pandas as pd
from functions import sort_py_percentage
from imports import import_wordlist


wl = import_wordlist.read("./wordlist/wordlist.txt", 5)

print(wl)

letter = []

exclude = "y"
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
# letter[1] = "o"
# letter[2] = "o"
# letter[3] = "e"
# letter[4] = "s"

# TODO escape regex chars
pattern = r"^{0[0]}{0[1]}{0[2]}{0[3]}{0[4]}$".format(letter)
print(pattern)

HiLtI = wl[wl.str.match(pattern)]
HiLtI: pd.Series = HiLtI.reset_index(drop=True).squeeze()

if isinstance(HiLtI, str):
    print("The only word:", HiLtI)
else:
    print("Hits:", len(HiLtI))
    print(sort_py_percentage(HiLtI))
