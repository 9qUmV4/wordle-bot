

###########################################################
#                        WORDLE                           #
###########################################################
import sys


class Wordle():
    def __init__(self, word: str) -> None:
        self.word = word.lower()
        self.counter = 0
        
    def check(self, guess: str) -> str:
        self.counter += 1
        
        feedback = ["" for _ in range(len(self.word))]
        availableLetters = self.word
        # Green / Exact match
        for i, w, g in zip(range(len(self.word)), self.word, guess):
            if w == g:
                feedback[i] = "g"
                availableLetters = availableLetters.replace(w, "", 1)
                
        for i, w, g in zip(range(len(self.word)), self.word, guess):
            if feedback[i] == "": # Not green
                if g in availableLetters: # Yellow
                    feedback[i] = "y"
                    availableLetters = availableLetters.replace(g, "", 1)
                else: # Gray
                    feedback[i] = "-"
                    
        return "".join(feedback)
    
    
    
if __name__ == "__main__":
    word = input("Solution word: ").strip().lower()
    wordle = Wordle(word)
    try:
        while True:
            guess = input("Guess? :")
            feedback = wordle.check(guess)
            print(f"Feedback on guess {guess}: {feedback !r}")
            if feedback == len(word) * "g":
                break
    except KeyboardInterrupt:
        sys.exit(0)
    sys.exit(0)