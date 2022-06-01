import pandas as pd
import pathlib
from functions import sort_py_percentage
from imports import import_wordlist


class Wordle:
    def __init__(self, length: int = 5) -> None:

        lang = input(
            "Select the language of the Wordle game (de - deutsch, en- english): "
        )
        if lang == "en":
            self.path = pathlib.Path("./wordlist/wordlist.txt")
        elif lang == "de":
            self.path = pathlib.Path("./wordlist/wordlist-german.txt")
        else:
            print(
                "This language is currently not in our database or you used a wrong letter. \n Please try again by restarting the code"
            )
            exit()

        if not isinstance(length, int):
            raise TypeError("Length must be an integer.")
        if not length > 0:
            raise ValueError("Length must be greater than zero.")

        self.wordlength = length

        self.sorted_wordlist: pd.Series | None = None
        self.possible_wordlist: pd.Series = import_wordlist.read(
            self.path, self.wordlength
        )

        self.pattern = r""
        self.bestWord = ""

        self.question = (
            'What\'s the result? ("-" for grey; "y" for yellow; "g" for green): '
        )

        self.guesses = 0

        self.exclude_y = [[], [], [], [], []]
        self.exclude = ""

        self.greenFlag = [False for i in range(self.wordlength)]

    def nextWord(self) -> None:

        if self.guesses <= 5:

            self.sorted_wordlist = self.getBestWords(self.possible_wordlist)
            self.bestWord = self.sorted_wordlist.index[0]

            print(self.guesses + 1, ". Word: ", self.bestWord)
            inp = input(self.question).lower().strip()
            if not len(inp) == self.wordlength:
                exit("This is not a valid input.")

            self.letter, self.greenFlag = self.analyzeInput(inp)

            print(self.letter)

            self.pattern()

            self.guesses += 1

    def getBestWords(self, wl_hit: pd.Series) -> pd.Series:

        return sort_py_percentage(wl_hit)

    def analyzeInput(self, inp: str) -> tuple:

        if inp == "ggggg":
            exit("ggwp eZ in " + str(self.guesses + 1) + " trys")

        else:
            letter = [[], [], [], [], []]
            bestWord = self.bestWord
            exclude_y = self.exclude_y
            include_l = ""
            greenFlag = self.greenFlag

            count = 0

            for i in inp:
                letter[count].append("")

                if i == "-":
                    self.exclude += bestWord[count]
                    letter[count] = self.exclude + exclude_y[count]

                elif i == "y":
                    include_l += inp[count]
                    exclude_y[count] = inp[count]

                elif i == "g":
                    letter[count] = inp[count]
                    greenFlag[count] = True

                else:
                    exit("This is not a valid input")

                count += 1

            return letter, greenFlag

    def pattern(self) -> None:
        
        for l in self.include_l:
            wl: pd.Series = wl[wl.str.contains(l)]

        for i in range(len(self.letter)):
            self.letter[i] = (
                "[^" + self.letter[i] + "]"
            )  # TODO inline if statement: expression_if_true if condition else expression_if_false
            # self.letter[i] = "[^" + self.letter[i] + "]" if self.greenFlag == False else "[" + self.letter[i] + "]"
        self.pattern = r"^{0[0]}{0[1]}{0[2]}{0[3]}{0[4]}$".format(self.letter)
        print(self.pattern)

        self.possible_wordlist = self.possible_wordlist[
            self.possible_wordlist.str.match(self.pattern)
        ]
        self.possible_wordlist: pd.Series = self.possible_wordlist.reset_index(
            drop=True
        ).squeeze()
