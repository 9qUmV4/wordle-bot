import pandas as pd
import pathlib
from functions import sort_py_percentage
from imports import import_wordlist


class Wordle():
    
    def __init__(self) -> None:

        self.path = pathlib.Path("./wordlist/wordlist.txt")
        # self.path = pathlib.Path("./wordlist/wordlist-german.txt")

        self.wl = import_wordlist.read(self.path, 5)

        self.letter = []

        self.exclude = ""
        self.exclude_y = [[], [], [], [], []]
        self.include_l = ""

        self.guesses = 0

        self.pattern = r""
        self.HiLtI:pd.Series

        self.bestWord = "cares"

        self.question = "What's the result? (\"-\" for grey; \"y\" for yellow; \"g\" for green): "

    def nextWord(self):
        if(self.guesses == 0):
            print("1. Word: ", self.bestWord)
            self.inp = input(self.question)

        elif(self.guesses <= 5):
            self.bestWord = self.getWord()

            print(self.guesses, ". Word: ", self.bestWord)
            self.inp = input(self.question)
        
        self.letter = []
            
        for i in range(len(self.inp)):

            self.letter.append("")

            if(self.inp[i] == "-"):
                self.exclude += self.bestWord[i]
                self.letter[i] = self.exclude + self.exclude_y[i]
                self.letter[i] = "[^" + self.letter[i] + "]"

            elif(self.inp[i] == "y"):
                self.include_l += self.inp[i]
                self.exclude_y[i] = self.inp[i]

            elif(self.inp[i] == "g"):
                self.letter[i] = self.inp[i]

            else:
                print("HS")

        print(self.letter)

        self.pattern()

        self.guesses += 1

    def getWord(self, wl_hit):
        self.wl_sort = sort_py_percentage(wl_hit)

    def pattern(self):
        self.pattern = r"^{0[0]}{0[1]}{0[2]}{0[3]}{0[4]}$".format(self.letter)
        # print(self.pattern)

        self.HiLtI = self.wl[self.wl.str.match(self.pattern)]
        self.HiLtI: pd.Series = self.HiLtI.reset_index(drop=True).squeeze()
