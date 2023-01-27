# Hangman
Hangman game for the WBS Coding School "Data Science" bootcamp.

Created by Henrik Bonsmann and Yeeun Bae, September 2022.

## IPython Notebook
Originally, this project was constructed in google colab. `The_Hangman_Challenge.ipynb` is a copy of that notebook and useable with google colab. Execute all cells from top to bottom. The last cell is set up to let you play a default game. See below for options.

## .py file
Compilation of the notebook to use as a self-contained python file. Install the package specified in the `requirements.txt` before executing. The file can be run directly from a python console and supports all the parameters of the game function as positional and keyword arguments.

## Hangman options
The `hangman()` function is set up to work with default values for a quick and easy game, but can be modified further with arguments:

1. `game_difficulty` sets up the number of mistakes that can be made until the game is lost:
    - `easy` (default): 11 mistakes maximum
    - `medium`: 8 mistakes maximum
    - `hard`: 6 mistakes maximum
    
2. `word_difficulty`: Chooses a random english word based on a calculated "ScrabbleScore".
    - `none`: Choose from all words
    - `easy` (default): Choose a word with a ScrabbleScore below 1
    - `hard`: Choose a word with a ScrabbleScore above 1
    - Additionally, a list of floats can be provided to be used as a range of ScrabbleScores for the choosen word. `[.2,.8]` will choose a random word with a ScrabbleScore of between 0.2 and 0.8.
    
3. `word` provide a custom word for someone else to solve.
    The string needs to consist of alphabetical characters common to the english alphabet. Special characters of any sort are not allowed!
    
### The ScrabbleScore
To calculate the difficulty of guessing a certain word, this game calculates a ScrabbleScore. All *unique* characters in a word are scored based on their value in the word-laying game "Scrabble" - with the exception of "E" and "A" which are so common that they are assigned a score of 0. The score is summed up and divided by the total number of letters in the word. Thus shorter words and words including rarer letters are deemed more difficult to guess.
