import pandas as pd

class Wordle():
    
    def __init__(self) -> None:

        self.wl: pd.Series = pd.read_table("./wordlist/wordlist-german.txt").squeeze()
        self.wl: pd.Series = self.wl.str.lower()


        for k, r in {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"}.items():
            self.wl = self.wl.str.replace(k, r)

        self.wl = self.wl[self.wl.str.len() == 5]

        exclude = [r"'", r"-", r"/", r"\(", r"\)", r"\x03", r"\x07", r"\x08", r"\.", r"ø", r"å", r"é", r"á", r"ó", r"ç", r"è", r"ê", r"ë", r"ñ", r"ô", r"í", r"à"]
        for e in exclude:
            self.wl = self.wl[~self.wl.str.contains(e)]
        
        self.wl: pd.Series = self.wl.reset_index(drop=True).squeeze()

        self.letter = []

        self.exclude = ""
        self.include_l = ""

        self.guesses = 0

        self.bestWord = "cares"

        self.question = "What's the result? (\"-\" for grey; \"y\" for yellow; \"g\" for green)"

    def nextWord(self):
        if(self.guesses == 0):
            print("1. Word: ", self.bestWord)
            self.inp = input(self.question)
        elif(self.guesses <= 5):
            self.bestWord = self.getWord()

            print(self.guesses, ". Word: ", self.bestWord)
            self.inp = input(self.question)

        for i in range(5):
            if(self.inp[i] == "-"):
                # print("-")
                self.exclude += self.inp[i]
            elif(self.inp[i] == "y"):
                # print("y") 
                self.include_l += self.inp[i]
            elif(self.inp[i] == "g"):
                print("g")
            else:
                print("HS")


        self.guesses += 1

    def getWord(self):
        pass
