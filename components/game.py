from textual.screen import Screen
from textual.app import ComposeResult, Binding, App
from textual.containers import Horizontal, Vertical, Center, Middle, Grid
from textual.widgets import Header, Footer, Static, Input, Button

from components.randomword import random_word
from components.letters import p, l, a, y, exc
from components.renderstring import RenderString
from components.champ import Champ

class Game(Screen):

    #BINDINGS = [
    #    Binding('ctrl+x', 'champ_screen', 'Champ', show=False)
    #    ]

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
            "\n\n█ █ █ █ █\n\n█ █ █ █ █\n\n█ █ █ █ █\n\n█ █ █ █ █\n\n█ █ █ █ █\n\n█ █ █ █ █\n\n", classes = 'guesses'
            ), classes = 'play_grid'
        )
        yield Center(
            Input(placeholder="guess", classes='input')
        )