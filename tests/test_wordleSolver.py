import logging

import pytest
from wordleBot.wordleSolver import WordNotFoundError, WordleSolver
from wordleBot.functions import read as read_wordlist

import pandas as pd

from wordle import Wordle
            
###########################################################
#                         TESTS                           #
###########################################################



def test_oneWordle():
    word = "games"
    wordle = Wordle(word)
    
    wordleSolver = WordleSolver(len(word), "en")
    
    for _ in range(20):
        guess = wordleSolver.nextWord()
        feedback = wordle.check(guess)
        if wordleSolver.calculate(feedback):
            assert guess == word
            return None
    else:
        raise RuntimeError("Should found wort already, after 20 trys still no word.")



class TestCompleteWordlist:




    @pytest.mark.slow
    def test_completeWordlist(self):    
        wordLength = 5
        wordlist: list[str] = list(read_wordlist("./wordlist/wordlist.txt", wordLength).values)
        wordlistLength = len(wordlist)
        
        wordleSolver = WordleSolver(wordLength, "en")
        failures = []
        for word_i, word in zip(range(wordlistLength), wordlist):
            try:
                for i in range(20):
                    wordle = Wordle(word)
                    guess = wordleSolver.nextWord()
                    feedback = wordle.check(guess)
                    if wordleSolver.calculate(feedback):
                        if  guess == word:
                            logging.info(f"({word_i}/{wordlistLength}) Needed {i} guesses to find {word !r}.")
                        else:
                            failures.append(f"({word_i}/{wordlistLength}) FAILED: Word {word !r}: Thought {guess !r} is right.")
                        break
                else:
                    raise RuntimeError("Should found wort already, after 20 trys still no word.")
                wordleSolver.reset()
            except WordNotFoundError as err:
                failures.append(f"({word_i}/{wordlistLength}) FAILED: Word {word !r}: {err}")
        assert not failures