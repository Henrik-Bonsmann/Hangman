"""
    A simple game of hangman built as an exercise for the WBS Coding School "Data Science" boot camp in September 2022.
    Created by Henrik Bonsmann and Yeeun Bae.
"""

#from IPython.display import clear_output
# english_words_alpha_set contains no punctuation
from english_words import english_words_alpha_set
import random
import sys
import os
import argparse
import ast

def cls():
    """
    Clears the console for neater output.
    """
    os.system('cls' if os.name=='nt' else 'clear')

def get_gallow(n_mistakes, difficulty):
  """
  Construct ASCII art depending on health levels.

  mistakes -- The number of wrong guesses so far (int)

  return -- String depicting gallows ASCII art for the current gamestate
  """
  gallow = ""
  
  # Lookup table for different difficulties. 
  # Length needs to be equal to maxHealth.
  # Always end at 11 for the man to hang!
  if difficulty == 'easy':
    state = [0,1,2,3,4,5,6,7,8,9,10,11]
  elif difficulty == 'medium':
    state = [1,2,4,6,7,8,9,10,11]
  elif difficulty == 'hard':
    state = [4,6,7,8,9,10,11]

  if state[n_mistakes] == 0:
    gallow = r"""     
          
           
             
           
          
     
............. 
"""
  elif state[n_mistakes] == 1:
    gallow = r"""     
          
           
             
           
          
 ____________    
/            \  
"""
  elif state[n_mistakes] ==  2:
    gallow = r"""     
          
   |        
   |          
   |        
   |       
 __|_________    
/            \  
"""
  elif state[n_mistakes] == 3:
    gallow = r"""     
          
   |/        
   |          
   |        
   |       
 __|_________    
/            \  
"""
  elif state[n_mistakes] == 4:
    gallow = r"""     
    _____      
   |/        
   |          
   |        
   |       
 __|_________    
/            \  
"""
  elif state[n_mistakes] == 5:
    gallow = r"""     
    _____      
   |/    |     
   |          
   |        
   |        
 __|_________    
/            \ 
"""
  elif state[n_mistakes] == 6:
    gallow = r"""     
    _____      
   |/    |     
   |     O     
   |       
   |        
 __|_________    
/            \ 
"""
  elif state[n_mistakes] == 7:
    gallow = r"""     
    _____      
   |/    |     
   |     O     
   |     |    
   |        
 __|_________    
/            \ 
"""
  elif state[n_mistakes] == 8:
    gallow = r"""     
    _____      
   |/    |     
   |     O     
   |    /|    
   |         
 __|_________    
/            \ 
"""
  elif state[n_mistakes] == 9:
    gallow = r"""     
    _____      
   |/    |     
   |     O     
   |    /|\    
   |         
 __|_________    
/            \ 
"""
  elif state[n_mistakes] == 10:
    gallow = r"""     
    _____      
   |/    |     
   |     O     
   |    /|\    
   |    /     
 __|_________    
/            \ 
"""
  elif state[n_mistakes] == 11:
    gallow = r"""     
    _____      
   |/    |     
   |     O     
   |    /|\    
   |    / \    
 __|_________    
/            \ 
"""
  else:
    # If you ever get here, you didn't set up the difficulty correctly!
    gallow = "ERROR!"
  return gallow


def show_output(progress, mistakes, difficulty):
  """ 
  Shows a nice graphical output of the gamestate.

  progress -- The List of unknown / known letters in the solution (list)
  mistakes --  Wrongly guessed characters (list)
  """

  cls()
  gallow = get_gallow(len(mistakes), difficulty)

  print(gallow, '\n', " ".join(mistakes), '\n  \n', " ".join(progress))
  
  
def show_progress(letter, word, progress):
  """
  Apply the guessed letter if it was a correct guess and show the 
  progress of word guessing.

  """

  # Show the progress of user's guess (for unknown spelling: '_')
  

  # Interate over the entire word so that the result will show all the same 
  #  letters will be shown once the letter is given as a guess
  if letter in word:
    correct = True
  else:
    correct = False

  for i in range(0, len(word)):
    if letter == word[i]:
      progress[i] = letter
  
  return progress, correct


def clean_input(user_in, mistakes):
  """
  Catches input errors and returns a standardized character.

  user_in -- user generated input (string)
  mistakes -- Wrongly guessed characters (list)

  return -- Char or False on error   
  """

  # All the numbers of the alphabet!
  letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
             'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
  
  if user_in == "":
    print("No input detected.\n")
    char= False
  elif len(user_in) > 1:
    print("Only input a single letter!\n")
    char= False
  else:
    char = user_in.upper()
    if not (char in letters):
      # Restricts alphabetical special characters that would pass .isalpha()
      print("Don't input special characters!\n")
      char =  False
    elif char in mistakes:
      print(f"You already guessed {char}!")
      char = False
  return char


def get_char(mistakes):
  """
  Requests user input until valid. 

  mistakes -- wrongly guessed characters (list)

  return -- the next guess (char)
  """
  user_in = ''
  char = False
  while not char:
    user_in = input("Please guess a letter: \n")
    char = clean_input(user_in, mistakes)
  return char


def makeOutput(solution):
  """
  Construct an output of placeholder "_" the length of the solution

  solution -- The word to guess (str)

  return -- a list of len(solution) filled with '_' (list)
  """
  output = []
  for i in range(len(solution)):
    output.append('_')
  return output


def scrabbleIndex(word):
  """
  Scores the difficulty of a hangman word based on scrabble points. Points for each unique letter are added up and divided by the total number of characters in the word.

  word -- The word to score (str)

  return -- the scrabbleIndex (float)

  """

  #Adjusted Scrabble scores. 'A' and 'E' have been reduced to 0 points.
  points = {\
      'A': 0,
      'B': 3,
      'C': 3,
      'D': 2,
      'E': 0,
      'F': 4,
      'G': 2,
      'H': 4,
      'I': 1,
      'J': 8,
      'K': 5,
      'L': 1,
      'M': 3,
      'N': 1,
      'O': 1,
      'P': 3,
      'Q': 10,
      'R': 1,
      'S': 1,
      'T': 1,
      'U': 1,
      'V': 4,
      'W': 4,
      'X': 8,
      'Y': 4,
      'Z': 10
  }
  score = 0

  # Use set() to only check unique values
  for letter in set(word):
    score += points[letter]

  score /= len(word)
  
  return score

def determineBounds(difficulty):
  """
  Checks game option and adjusts scrabbleIndex boundaries accordingly. 
  Outputs informative errors if necessary.

  difficulty -- directly usable values or predetermined setting (list(2), str)
                'none': no restrictions
                'easy': use only words with a scrabbleIndex <= 1
                'hard': use only words with a scrabbleIndex >= 1

  """

  if type(difficulty) == list:
    if len(difficulty) ==2:
      if difficulty[0]<difficulty[1]:
        bound = difficulty
      else:
        raise ValueError("word_difficulty lower bound must be smaller than \
                          upper bound.")
    else: 
      raise ValueError("word_difficulty list must contain exactly \
                        one lower and one upper bound.")
  
  elif type(difficulty) != str:
    raise ValueError('word_difficulty must be of type (list) or (str).') 
  
  elif difficulty.lower() == 'none':
    bound = [0,11]
  elif difficulty.lower() == 'easy':
    bound = [0,1]
  elif difficulty.lower() == 'hard':
    bound = [1,11]
  else:
    raise ValueError("Choose preset word_difficulty from: \
                      'none', 'easy', 'hard'")
  return(bound)


# convert the word set into a list to make it indexable
words = list(english_words_alpha_set) 

def getWord(difficulty = 'none'):
  """
  Returns a random english word from the english_words package 
  within appropriate scrabbleIndex values

  difficulty -- directly usable values or predetermined setting (list(2), str)
                'none': no restrictions
                'easy': use only words with a scrabbleIndex <= 1
                'hard': use only words with a scrabbleIndex >= 1
  """
  
  # Highest possible scrabble index is 10.
  bound = determineBounds(difficulty)

  # Ensures entry into the while loop
  score = bound[1]+1
  word = ''

  while score <= bound[0] or score >= bound[1]:
    word = words[random.randint(0, len(words))].upper()
    score = scrabbleIndex(word)
  return word


def health_state(difficulty):
  # This will depend on the difficulty level.
  # The easier the game is, the more chances the user gets.
  if difficulty.lower() == 'easy':
    health = 11
  elif difficulty.lower() == 'medium':
    health = 8
  else:
    health = 6
  return health


def checkSolution(word):
  """
  Checks if a provided word is valid for a game of hangman.

  word -- the word to evaluate (str)

  return -- whether the word is valid (bool)
  """

  # All the numbers of the alphabet!
  letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
             'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

  check = True

  for char in word:
    # Alphabetical special characters are not valid
    if char not in letters:
      check = False
      break
  return check

def hangman(game_difficulty = 'easy', word_difficulty = 'easy', word = ''):
  """
  Play a game of Hangman!

  game_difficulty -- determines the maximum number of mistakes (str)
                      'easy':   11
                      'medium':  8
                      'hard':    6
  word_difficulty -- Sets a predetermined range for valid scrabble_index values,
                     or provide custom ones (str, list(2))
                      'none': pick from all words
                      'easy': pick from words with a scrabble index <=1
                      'hard': pick from words with a scrabble index >=1 
  word            -- set a custom word for someone else to solve (str)
  """

  guess = ''
  mistakes = []
  solution = ''
  
  max_health = health_state(game_difficulty)

  if len(word):
    if checkSolution(word.upper()):
      solution = word.upper()
    else:
      input("The provided word was not valid, \
             generating a random english word.")
      solution = getWord(word_difficulty)
  else:
    solution = getWord(word_difficulty)

  progress = makeOutput(solution)

  # Print game screen before start to set up game area and
  # show number of letters
  show_output(progress, mistakes, game_difficulty)

  # Core game loop: Ask for a letter, then show where it goes in the word or
  #                draw part of the Hangman
  # Repeat until you run out of tries or you guessed the word correctly.
  while(len(mistakes) < max_health) and ('_' in progress):
    guess = get_char(mistakes)
    progress, correct = show_progress(guess, solution, progress)
    if not correct:
        mistakes.append(guess)
    show_output(progress, mistakes, game_difficulty)

  if '_' not in progress:
    print("\n You won! You saved the man.")
  elif len(mistakes) >= max_health:
    print(f"\n You lost. Sorry. \n The word was {solution}.")
  print(f"\n This word's scrabbleIndex was {round(scrabbleIndex(solution),2)}.")
  
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Play a game of Hangman")
    parser.add_argument("--game_difficulty", help="Game difficulty: 'easy', 'medium' or 'hard ", nargs='?', default='easy')
    parser.add_argument("--word_difficulty", help= "Word difficulty: Scrabble Index Bounds or 'none','easy', 'hard'", nargs='?', default='easy')
    parser.add_argument("--word", help="Provide a custom word", nargs='?', default = '')
    args = parser.parse_args()
    try:
        args.word_difficulty = ast.literal_eval(args.word_difficulty)
    except:
        pass
    
    hangman(args.game_difficulty, args.word_difficulty, args.word)