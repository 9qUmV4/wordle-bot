import pandas as pd

wl: pd.Series = pd.read_table("./wordlist/wordlist.txt").squeeze()

wl5 = wl[wl.str.len() == 5]
wl5 = wl5[~wl5.str.contains(r"'")]
wl5 = wl5[~wl5.str.contains(r"-")]
wl5 = wl5[~wl5.str.contains(r"/")]
wl5 = wl5[~wl5.str.contains(r"\(")]
wl5 = wl5[~wl5.str.contains(r"\)")]
wl5: pd.Series = wl5.reset_index(drop=True).squeeze()

c = [{}, {}, {}, {}, {}]


for i in range(len(wl5)):
#for i in range(5):
    for j in range(5):
        if((wl5[i][j] in c[j])):
            c[j][wl5[i][j]] += 1
        else:
            c[j][wl5[i][j]] = 1


for i in range(5):
    for j in c[i].keys():
        c[i][j] /= len(wl5)
        c[i][j] *= 100

prob = 0
for i in c[0].keys():
    prob += c[0][i]

words = {}
for i in range(len(wl5)):
    words[wl5[i]] = 0
    for j in range(5):
        words[wl5[i]] += c[j][wl5[i][j]]

biggest = {"": 0}
big  = ""

h = 0

for i in words.keys():
    if(words[i] > biggest[list(biggest.keys())[0]]):
        biggest[list(biggest.keys())[0]] = words[i]
        big = list(words.keys())[h]
    h += 1

print(biggest)
print(big)
