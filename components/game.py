from textual.screen import Screen
from textual.app import ComposeResult, Binding, App
from textual.containers import Horizontal, Vertical, Center, Middle, Grid, Container
from textual.widgets import Header, Footer, Static, Input, Button
from textual.validation import Length, Validator, Function, ValidationResult

import httpx

from components.randomword import random_word
from components.letters import p, l, a, y, exc
from components.renderstring import RenderString
from components.champ import Champ

class Game(Screen):

    #BINDINGS = [
    #    Binding('ctrl+x', 'champ_screen', 'Champ', show=False)
    #    ]
    def __init__(
            self, 
            wrdyl_word: str = "Hello", 
            #wrdyl_def: str = "World!",
            play_grid: str = '\n\n█ █ █ █ █\n\n█ █ █ █ █\n\n█ █ █ █ █\n\n█ █ █ █ █\n\n█ █ █ █ █\n\n█ █ █ █ █\n\n'
            ) -> None:
        super().__init__()
        self.wrdyl_word = wrdyl_word
        self.play_grid = play_grid
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        #if event.value == self.wrdyl_word:
        self.play_grid = 'Hello'
    


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
            f"{self.play_grid}", classes = 'guesses'
            ), classes = 'play_grid'
        )
        yield Center(
            Input(
                placeholder="guess",
                validators=[
                    Length(5,5),
                    Function(is_alpha, False),
                    Function(is_in_dictionary, False)
                            ], 
                classes='input'
                )
        )
    


    
def is_alpha(value: str) -> bool:
    if value.isalpha():
        return True
    else:
        return False

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