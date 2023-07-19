# Some Speedtest

import pandas as pd
import pytest
from wordleBot.functions import read as read_wordlist, sort_by_percentage
from wordleBot.wordleSolver import WordleSolver

@pytest.mark.speed
class TestSpeed:
    wordLength = 5
    wordlist = read_wordlist("./wordlist/wordlist.txt", wordLength)
    wordlistLength = len(wordlist)
    
    def test_calculation_of_wordlist(self):
        swl = sort_by_percentage(self.wordlist)
        assert len(swl) == self.wordlistLength