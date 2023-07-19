import logging
import re
from pathlib import Path

import pandas as pd

from .functions import sort_by_percentage, read as read_wordlist

__all__ = [
    "WordNotFoundError",
    "WordleSolver",
]

class WordNotFoundError(Exception):
    """Word not found: Out of words or no words availible
    """
    pass


class WordleSolver:
    """Solver for wordle
    """
    def __init__(self, length: int = 5, language: str | None = None, highlightsAllDuplicates: bool = False) -> None:
        """Create a solver

        Args:
            length (int, optional): Lenght of word. Defaults to 5.
            language (str | None, optional): Select the language of the wordle (en-english, de-german). Defaults to asking the user.
        """
        
        # Check language and set path of wordlist accordingly
        if not isinstance(language, str):
            TypeError("Languange must be a string")
        if language not in ["en", "de"]:
            ValueError("Language must be 'en' or 'de'")

        if language == "en":
            self._path = Path("./wordlist/wordlist.txt")
        elif language == "de":
            self._path = Path("./wordlist/wordlist-german.txt")

        # Check lenght of word
        if not isinstance(length, int):
            raise TypeError("Length must be an integer.")
        if not length > 0:
            raise ValueError("Length must be greater than zero.")
        self._wordLength: int = length
        
        # Check and store highlightsAllDupicates
        if not isinstance(highlightsAllDuplicates, bool):
            raise TypeError("Param highlightsAllDuplicates must be a bool")
        self._highlightsAllDuplicates = highlightsAllDuplicates
        
        # Compile Regex Pattern to speed up solving
        self._regex_feedback_check = re.compile(fr"[-yg]{{{self.wordLength}}}")

        # Read in wordlist
        self._wordlist: pd.Series = self._calculatePossibility(read_wordlist(
            self.path, 
            self.wordLength
        ))
        
        # Calculate a lookup table for letters sorted by alphabet
        self._lookup_sorted_words = self._wordlist.apply(func=lambda s: "".join(sorted(s)))
        
        # And reset
        self.reset()
        return None


    def reset(self) -> None:
        """Reset to get ready to solve next wordle.
        """
        # Populate possibleWords with the wordlist
        self._possibleWords: pd.Series = self._wordlist.copy(deep=True)

        # Current guess of word
        self._currentGuess: str = ""
        
        # Index of current guessed word in self._possibleWords
        self._currentGuessIndex: int = -1

        # Counter of guesses
        self._roundCounter: int = 1

        # List of strings of letters not allowed on the respective position.
        # One string per letter position
        self._excludedLetters: list[str] = ["" for _ in range(self.wordLength)]

        # string of letters must be part of searched word but have a unknown position
        self._includedLetters: str = ""
        
        # list of letters which are set (green). None means still open letter position
        self._greenFlag: list[str] = [None for _ in range(self.wordLength)]   
        return None


    @property
    def path(self) -> Path:
        """Path to used wordlist. Readonly

        Returns:
            Path: Path to used wordlist
        """
        return self._path
    

    @property
    def wordLength(self) -> int:
        """Length of the searched word. Readonly

        Returns:
            int: Length of the searched word
        """
        return self._wordLength
    
    
    @property
    def possibleWords(self) -> list[str]:
        """Returns a list of all possible words sorted from highest to lowest propability.
        If you only want the next best word, use nextWord(). This will iterrate over all 
        possible words.

        Returns:
            list[str]: List containing all possible words
        """
        return list(self._possibleWords.values)
    
    
    @property
    def lenght(self) -> int:
        """Returns the current amount of possible words.
        More performant than len(wordleSolver.possibleWords)

        Returns:
            int: Amount of possible words
        """
        return len(self._possibleWords)
    
    
    @property
    def guessIndex(self) -> int:
        """Index of guess in possibleWords

        Returns:
            int: Index of guess
        """
        return self._currentGuessIndex
    
    
    @property
    def guess(self) -> str:
        """Current guess

        Returns:
            str: Last word returned from nextWord()
        """
        
    @property
    def round(self) -> int:
        """The current round. Increases if calculate() is called.

        Returns:
            int: current round
        """
        self._roundCounter
        

    def nextWord(self) -> str:
        """Get the next best word to use. 
        This iterrates over all possible words sorted from highest to lowest propability.
        
        Raises:
            WordNotFoundError: If no more word is avilable, raises a WordNotFoundError().
        
        Returns:
            str: Next best word to use
        """
        self._currentGuessIndex += 1
        try:
            self._currentGuess: str = str(self._possibleWords.iat[self._currentGuessIndex])
            logging.debug(f"Current word guess: {self._currentGuess !r}")
            return self._currentGuess
        except IndexError:
            logging.error("Reached end of list of possible words")
            raise WordNotFoundError
            

           # logging.critical("Out of words. Did you make a typing misstake? If not, its a bug. Please Report.")
           # print("Out of words. Did you make a typing misstake? If not, its a bug. Please Report.")
           # sys.exit(1)

    
    def calculate(self, feedback: str, *, wordOverride: str | None = None) -> bool:
        """Calculates the new possible word based on provided feedback.
        This will recalculate possible words based on the feedback for 
        the last word returned by nextWord().

        Args:
            feedback (str): Feedback must be a string with lenght of wordLenght. Use
                            - "g" for green/correct letter,
                            - "y" for yellow/letter in word, but wrong position and
                            - "-" for gray/letter not in word.
                            Example "g-yg-" means first and fourth letter are correct, 
                            third letter is not in this position and second and five 
                            letter are not in word.
            wordOverride (str | None): Override the word for which the feedback applies. 
                                       Must be one in wordleSolver.possibleWords. 
                          
        Raises:
            IndexError: Raised if wordOverride is not in wordleSolver.possibleWords
            RuntimeError: Raised if calculate() without wordOverride is called before 
                          nextWord() since init or last calculate() 

        Returns:
            bool: Returns True if wordle is finished (feedback only contains g) else False.
        """
        
        # Check feedback
        if not isinstance(feedback, str):
            raise TypeError("feedback must be a str")
        if not re.fullmatch(self._regex_feedback_check, feedback):
            raise ValueError("Not a valid feedback")
        
        # Check wordOverride
        if wordOverride is None:
            if self._currentGuessIndex == -1: # nextWord not called since last calculate()
                raise RuntimeError("You must call nextWord() before calculate() without wordOverride")
            word = self._currentGuess
        else:
            if not isinstance(wordOverride, str):
                raise TypeError("wordOverride must be a str")
            if wordOverride not in self._possibleWords:
                raise IndexError("wordOverride is not in wordleSolver.possibleWords")
            word = wordOverride
        
        # If wordle got found, return True
        if feedback == "ggggg":
            return True
            
        
        # The logic to use for one or multible of one letter (*/_=placeholder/empty):
        # | Word  | NYTimes               | Wordle Archive                 |
        # |       |                       | (highlightsAllDuplicates=True) |
        # |-------|-----------------------|--------------------------------|
        # |       | inc     ex      flag  | inc     ex      flag           |
        # | g**** | x       _____   x____ | x       _____   x____          |
        # | *y*** | x       _x___   _____ | x       _x___   _____          |
        # | **-** |         xxxxx   _____ |         xxxxx   _____          |
        # | gy*** | xx      _x___   x____ | x       _x___   x____          |
        # | g*-** | x       _xxxx   x____ |         ERROR                  |
        # | *y-** | x       _xx__   _____ |         ERROR                  |
        # | gy-** | xx      _xx__   x____ |         ERROR                  |
        # | g***g | xx      _____   x___x | xx      _____   x___x          |
        # | *y**y | xx      _x__x   _____ | x       _x__x   _____          |
        # | **-*- |         xxxxx   _____ |         xxxxx   _____          |
            
        addToIncludedLetters = ""
        yellowLetters = "" # All yellow reported letter in this round
            
        for i, fb, letter in sorted(zip(range(self.wordLength), feedback, word), key=lambda x: {"g": 0, "y": 1, "-": 2}[x[1]]):
            match fb:
                case "g":   # Letter correct
                    self._greenFlag[i] = letter
                    addToIncludedLetters += letter
                case "y":   # Letter in word, but wrong position
                    addToIncludedLetters += letter
                    # If letter is not already in excluded letters
                    if letter not in self._excludedLetters[i]:
                        self._excludedLetters[i] += letter
                    yellowLetters += letter
                case "-":   # Letter less or not in word
                    if letter in yellowLetters:
                        self._excludedLetters[i] += letter # Letter is not on this position
                    elif letter in self._greenFlag: # Other occurents of letter is green
                        for i_ex in range(self.wordLength):
                            if letter != self._greenFlag[i_ex] and (letter not in self._excludedLetters[i_ex]):
                                self._excludedLetters[i_ex] += letter
                    else: # Letter is not in word
                        for i_ex in range(self.wordLength):
                            if letter not in self._excludedLetters[i_ex]:
                                self._excludedLetters[i_ex] += letter
                case _ as capture:
                    raise ValueError(f"This is a bug, please report! Captured the following: {capture !r}")        
        
        # Add to include letters to included letters
        addToIncludedLetters_woDup = "".join(set(addToIncludedLetters)) # Remove dupicates
        if self._highlightsAllDuplicates:
            # If flag is set, drop duplicates
            addToIncludedLetters = addToIncludedLetters_woDup
        for l in addToIncludedLetters_woDup:
            self._includedLetters = self._includedLetters.replace(l, "")
            self._includedLetters += l * addToIncludedLetters.count(l)
        
        # Update round counter
        self._roundCounter += 1
        
        # Reset index of current guess
        self._currentGuessIndex = -1
        
        logging.info(f"greenFlag: {self._greenFlag}")
        logging.info(f"includedLetters: {self._includedLetters}")
        logging.info(f"excludedLetters: {self._excludedLetters}")
        
        # Updated possible words
        self._updatePossibleWords()
        
        if len(self._possibleWords) == 0:
            logging.critical("Word list of lenght 0. No word found! Probably a Bug")
            raise WordNotFoundError("Word list of lenght 0. No word found! Probably a Bug")
        
        self._possibleWords = self._calculatePossibility(self._possibleWords)
        
        return False 
                

    def _updatePossibleWords(self) -> None:
        """Update the list of possible words based on greenFlag, excludedLetter and includedLetter
        """
        # mask words containing must have letters
        reg_patter_included = f"^.*{'.*'.join(sorted(self._includedLetters))}.*$"
        logging.debug(f"reg_patter_included: {reg_patter_included}")
        b_required = self._lookup_sorted_words.loc[self._possibleWords.index].str.fullmatch(reg_patter_included)
        
        # mask words matching fixed letters and not including forbidden letters
        reg_patter = "^"
        for flag, excl in zip(self._greenFlag, self._excludedLetters):
            if flag:    # If letter is known, use it
                reg_patter += flag
            elif not excl:  # no forbidden letters, except everything
                reg_patter += "."
            else:       # add forbidden letters
                reg_patter += f"[^{excl}]"
        reg_patter += "$"
        logging.info(f"Regex pattern: {reg_patter !r}")
        
        b_pos = self._possibleWords.str.fullmatch(reg_patter)
        
        self._possibleWords = self._possibleWords[b_required & b_pos]


    def _calculatePossibility(self, wordList: pd.Series) -> pd.Series:
        """Capsules sort_by_percentages.
        Calculates for each word the possibility it is the right one. Returns a sorted list from best to worst

        Args:
            wl_hit (pd.Series): List of words to sort

        Returns:
            pd.Series: Sorted list with percentages as index and words as values, sorted from best to worst
        """
        return sort_by_percentage(wordList)