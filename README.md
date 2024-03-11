# WRDYL
A python clone of Wordle for your terminal.

## Motivation

After coding a rudimentary version of Wordle in Python, I checked it against a number of Wordle tutorials written in python to assess my own outcome.

However, I noticed two I thought they were all lacking two major things. 

1. The visual appeal of the original Wordle. 
2. Functionality *actually* matching wordle

Regarding point 2, in the tutorials, they used the `in` keyword or the intersection of `set_A & set_B` to detect if there were common letters in each word at different places. Whilst this does highlight the letters, it leads to an error in the functionality.

For example, if the Wordle word is **SLOTH** and the player guesses **HELLO**, then using `in` or `set_A & set_B` would highlight the **H** and **O** in **HELLO** correctly. However, both the **L**'s in **HELLO** would also be highlighted yellow, when it should only be the first.  Otherwise, it misleads the player into thinking two L's are in the Wordle. This has been solved in **Wrdyl**.

## How to play
- Install (installation section TBD) and run `__init__.py` in your terminal.
- Press Ctrl+r to begin a new game (the key bindings are shown in the blue footer on the terminal screen)
- Try and guess the Wrdyl using the clues.
- A green background indicates that the letter is in the correct place, yellow indicates its in the word but incorrect place and no background indicates that its not in the word.
-  Only five letter words that are in the dictionary will be accepted.
- You have six attempts to guess the word. Good luck!

# To Do
- Add a display of letters already guessed.
- Add a hint button.
- Add the ability to change settings.
- Test logic on letters with defined test cases.
- Keep track of current score and/or streak and display.
- Store highscores in a .txt file 
- Create requirements.txt or poetry file and make installation section in README.md
- Add issues of key bindings and screen uninstallation.
- Render word necessary in losing and winning screen.