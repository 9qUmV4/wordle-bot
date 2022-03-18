import pandas as pd

wl: pd.Series = pd.read_table("./wordlist/wordlist-german.txt").squeeze()
wl: pd.Series = wl.str.lower()

for k, r in {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"}.items():
    wl = wl.str.replace(k, r)
    
wl5 = wl[wl.str.len() == 5]

exclude = [r"'", r"-", r"/", r"\(", r"\)", r"\x03", r"\x07", r"\x08", r"\.", r"ø", r"å", r"é", r"á", r"ó", r"ç", r"è", r"ê", r"ë", r"ñ", r"ô", r"í", r"à"]
for e in exclude:
    wl5 = wl5[~wl5.str.contains(e)]

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


for i in range(len(c)):
    print(len(c[i]))

k = [[], [], [], [], []]

for i in range(len(c)):
    k[i] = list(c[i].keys())

for i in range(len(k)):
    k[i].sort()

print(k[0])
print(k[1])
print(k[2])
print(k[3])
print(k[4])