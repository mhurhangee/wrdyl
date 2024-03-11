#Imports from textual
from textual.screen import Screen
from textual.app import ComposeResult, Binding
from textual.containers import Horizontal, Vertical, Center
from textual.widgets import Header, Footer, Static, Input
from textual.validation import Length, Function

#Import to check if word is in dictionary
import httpx

#Import of title ASCII art
from components.letters import p, l, a, y, exc

#Game screen for playing the game
class Game(Screen):

    #constructor for collecting input of random word and play grid and their instance variables
    def __init__(
            self, 
            wrdyl_word: str = "Hello", 
            play_grid: list = ['fail']
            ) -> None:
        super().__init__()
        #instance variables
        self.wrdyl_word = wrdyl_word
        self.game_display = ''
        #turning list of play_grid into a string
        for i in range(len(play_grid)):
            self.game_display += '\n' + str(play_grid[i]) + '\n'

    
    #Display ...
    def compose(self) -> ComposeResult:
        #...header and footer
        yield Header()
        yield Footer()
        #...title
        yield Vertical(
            Horizontal(
                Static(p, classes='column', id='w'),
                Static(l, classes='column', id='r'),
                Static(a, classes='column', id='d'),
                Static(y, classes='column', id='y'),
                Static(exc, classes='column', id='l'),
                classes='welcome'
            )
        )
        #...play grid
        yield Center(Static(
            f"{self.game_display}", classes = 'guesses'
            ), classes = 'play_grid'
        )
        #...box for receiving guesses from player
        yield Center(
            Input(
                placeholder="WRDYL", #placeholder text within the input prior to user input
                validators=[ #functions used to validate the input and return a result used in Wrdyl class
                    Length(5,5),
                    Function(is_alpha, False),
                    Function(is_in_dictionary, False)
                            ], 
                classes='input' 
                )
        )
        #...padding
        yield Static('  ', classes='welcome')

#function to validate input by determining if string is a letter a to z       
def is_alpha(value: str) -> bool:
    if value.isalpha():
        return True
    else:
        return None

#function to validate input by determining if word in is the dictionary
def is_in_dictionary(value: str) -> bool:
    if len(value) > 3:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{value}"

        with httpx.Client() as client:
            response = client.get(url)
            try:
                results = response.json()
                    
            except Exception:
                results= 'XXXXX'
        
        if results == 'XXXXX' or isinstance(results, dict):
            return False
        elif isinstance(results, list):
            return True