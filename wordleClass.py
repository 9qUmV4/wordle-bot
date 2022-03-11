import pandas as pd

class Wordle():
    
    def __init__(self) -> None:

        self.wl: pd.Series = pd.read_table("./wordlist/wordlist.txt").squeeze()

        self.wl5 = self.wl[self.wl.str.len() == 5]
        self.wl5 = self.wl5[~self.wl5.str.contains(r"\(")]
        self.wl5 = self.wl5[~self.wl5.str.contains(r"\)")]
        self.wl5 = self.wl5[~self.wl5.str.contains(r"-")]

        self.wl5: pd.Series = self.wl5.reset_index(drop=True).squeeze()

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
