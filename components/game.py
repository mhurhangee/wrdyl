from textual.screen import Screen
from textual.app import ComposeResult, Binding, App
from textual.containers import Horizontal, Vertical, Center, Middle, Grid, Container
from textual.widgets import Header, Footer, Static, Input, Button
from textual.validation import Length, Validator, Function, ValidationResult

from colorama import Back

import httpx

from components.randomword import random_word
from components.letters import p, l, a, y, exc
from components.renderstring import RenderString
from components.champ import Champ

class Game(Screen):

    BINDINGS = [
        Binding('ctrl+w', 'welcome_screen', 'Back to the start', show=True, priority=True),
        Binding('ctrl+r', 'game_screen', 'Play game', show=True, priority=True),
        Binding('ctrl+d', 'help_screen', 'Help', show=True, priority=True),
        Binding('ctrl+y', 'close_game_screen', 'Close Game', show=True, priority=True),
        Binding('ctrl+l', 'toggle_dark', 'Dark/Light Mode', show=True, priority=True),
		#('ctrl+r', 'pop_screen', 'Pop'),
        Binding('ctrl+x', 'champ_screen', 'Champ', show=False),
        Binding('ctrl+z', 'loser_screen', 'Loser', show=False)
    ]
 
    def __init__(
            self, 
            wrdyl_word: str = "Hello", 
            #wrdyl_def: str = "World!",
            play_grid: list = ['fail']
            ) -> None:
        super().__init__()
        self.wrdyl_word = wrdyl_word
        self.game_display = ''
        for i in range(len(play_grid)):
            self.game_display += '\n' + str(play_grid[i]) + '\n'

    

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
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

        #r = RenderString()
        #render = r.render(f"{wrdyl_word} and {wrdyl_definition}")
        
        yield Center(Static(
            f"{self.game_display}", classes = 'guesses'
            ), classes = 'play_grid'
        )
        yield Center(
            Input(
                placeholder="WRDYL",
                validators=[
                    Length(5,5),
                    Function(is_alpha, False),
                    Function(is_in_dictionary, False)
                            ], 
                classes='input'
                )
        )
        yield Static('  ', classes='welcome')
       
def is_alpha(value: str) -> bool:
    if value.isalpha():
        return True
    else:
        return None

def is_in_dictionary(value: str) -> bool:
        if len(value) == 5:
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
        else:
            return False