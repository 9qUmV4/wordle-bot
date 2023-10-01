# Wordle bot

This is a small script which aimes to half automate the game wordle.
We hacked it toghether in the lunch break, so don't expect anything. 

To get started run:
```
python3 -m build
python3 -m wordleBot
```

Help page:
```
python3 -m wordleBot --help
```

## Game Links
Links to some wordle games: 
[Wordle - The New York Times](https://www.nytimes.com/games/wordle/index.html)
[Wordle Game - Play Unlimited](https://wordlegame.org/)
[Wordle Archive - Play Older and Next Games](https://wordle-play.com/wordle-archive)

## Development cheat sheet
And to edit source code and test it:
```
pip install -e . 
```
  
The english word list we used is [this](https://www-personal.umich.edu/~jlawler/wordlist.html) and the german wordlist [this](https://gist.github.com/MarvinJWendt/2f4f4154b8ae218600eb091a5706b5f4)

## Improvements
- [ ] Downvote words with duplicate letters, because words like "sissy" get a good probability, but are bad to get new information.
- [ ] Imput checking: If feedback on duplicate letter is ambiguis (e.g. gray and yellow)