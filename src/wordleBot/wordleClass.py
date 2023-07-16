import logging
import re
import sys
from pathlib import Path

import pandas as pd

from functions import sort_py_percentage
from imports import import_wordlist


class WordleSolver:
    def __init__(self, length: int = 5, language: str | None = None) -> None:
        """Create a solver for one wordle

        Args:
            length (int, optional): Lenght of word. Defaults to 5.
            language (str | None, optional): Select the language of the wordle (en-english, de-german). Defaults to asking the user.
        """
        
        # Select language
        while language not in ("en", "de"):
            language = input(
                "Select the language of the Wordle game (de - deutsch, en - english): "
            ).strip().lower()

        if language == "en":
            self.path = Path("./wordlist/wordlist.txt")
        elif language == "de":
            self.path = Path("./wordlist/wordlist-german.txt")

        # Check lenght of word
        if not isinstance(length, int):
            raise TypeError("Length must be an integer.")
        if not length > 0:
            raise ValueError("Length must be greater than zero.")
        self.wordLength: int = length

        # Read in wordlist as all possible words
        self.possibleWords: pd.Series = import_wordlist.read(
            self.path, 
            self.wordLength
        )

        # Current guess of word
        self.currentGuess: str = ""

        # Counter of guesses
        self.guessCounter: int = 0

        # List of strings of letters not allowed on the respective position.
        # One string per letter position
        self.excludedLetters: list[str] = ["" for _ in range(self.wordLength)]

        # string of letters must be part of searched word but have a unknown position
        self.includedLetters: str = ""
        
        # list of letters which are set (green). None means still open letter position
        self.greenFlag: list[str] = [None for _ in range(self.wordLength)]


    def nextWord(self) -> None:
        self.guessCounter += 1
        
        # Calculate the percetages for each word
        sorted_wordlist = self.calculatePossibility(self.possibleWords)

        for use_word in range(len(sorted_wordlist)):
            # Guess the currently best word
            self.currentGuess = sorted_wordlist.iat[use_word]

            # Print the current guess
            logging.debug(f"Current word guess: {self.currentGuess}")
            print(self.guessCounter, "Word:", self.currentGuess)

            # Get user feedback for the current guess
            user_feedback = self.getUserFeedback()
            match user_feedback:
                case "q":
                    logging.info("User quit program")
                    sys.exit(0)
                case "n" | "next":
                    pass # Loop again
                case _:
                    break
        
        # And analyse it
        self.analyzeInput(user_feedback)

        self.updatePossibleWords()


    def calculatePossibility(self, wordList: pd.Series) -> pd.Series:
        """Capsules sort_by_percentages.
        Calculates for each word the possibility it is the right one. Returns a sorted list from best to worst

        Args:
            wl_hit (pd.Series): List of words to sort

        Returns:
            pd.Series: Sorted list with percentages as index and words as values, sorted from best to worst
        """
        return sort_py_percentage(wordList)
    
    
    def getUserFeedback(self) -> str:
        """Gets user feedback for the current guessed word

        Returns:
            str: Checked user feedback
        """
        while True:
            user_input = input( # TODO Add q for quit
                'What\'s the result? ("-" for grey; "y" for yellow; "g" for green)\n'
                + 'Use "q" to quit and "n" or "next" if word is unknown.           :'
            ).lower().strip()
            
            # Check if lenght of input the same then lenght of search word
            # and if only chars from the set -yg got used.
            if re.fullmatch(fr"[-yg]{{{self.wordLength}}}|q|n|next", user_input):
                return user_input
            

    def analyzeInput(self, feedback: str) -> tuple:
        """Analyses the user feedback on current guessed word

        Args:
            feedback (str): Feedback for the current guessed word
        """
        if not re.fullmatch(fr"[-yg]{{{self.wordLength}}}", feedback):
            raise ValueError("Not a valid feedback")

        if feedback == "ggggg":
            print("Found word in" + str(self.guessCounter) + " trys!")
            sys.exit(0)
            
        # Clear self.includedLetters because we will populate it again
        self.includedLetters = ""

        for i, fb, letter in zip(range(self.wordLength), feedback, self.currentGuess):
            match fb:
                case "-":   # Letter not in word
                    for i_ex in range(self.wordLength): 
                        if letter not in self.excludedLetters[i_ex]:
                            self.excludedLetters[i_ex] += letter
                case "y":   # Letter in word, but wrong position
                    # If letter is not already in excluded letters
                    if letter not in self.excludedLetters[i]:
                        self.excludedLetters[i] += letter
                    self.includedLetters += letter
                case "g":   # Letter correct
                    self.greenFlag[i] = letter
                    # TODO del? self.includedLetters.replace(letter, "", 1) # Remove letter from included letters
                case _ as capture:
                    raise ValueError(f"This is a bug, please report! Captured the following: {repr(capture)}")
                
        logging.info(f"greenFlag: {self.greenFlag}")
        logging.info(f"includedLetters: {self.includedLetters}")
        logging.info(f"excludedLetters: {self.excludedLetters}")
                

    def updatePossibleWords(self) -> None:
        """Update the list of possible words based on greenFlag, excludedLetter and includedLetter
        """
        # mask words containing must have letters
        reg_patter_included = f"^.*{'.*'.join(sorted(self.includedLetters))}.*$"
        logging.debug(f"reg_patter_included: {reg_patter_included}")
        sortedWordList = self.possibleWords.apply(func=lambda s: "".join(sorted(s))) # TODO Calculate on creation, not here
        b_required = sortedWordList.str.fullmatch(reg_patter_included)
        
        # mask words matching fixed letters and not including forbidden letters
        reg_patter = "^"
        for flag, excl in zip(self.greenFlag, self.excludedLetters):
            if flag:    # If letter is known, use it
                reg_patter += flag
            elif not excl:  # no forbidden letters, except everything
                reg_patter += "."
            else:       # add forbidden letters
                reg_patter += f"[^{excl}]"
        reg_patter += "$"
        logging.info(f"Regex pattern: {reg_patter !r}")
        
        b_pos = self.possibleWords.str.fullmatch(reg_patter)
        
        self.possibleWords = self.possibleWords[b_required & b_pos].reset_index(drop=True).squeeze()
