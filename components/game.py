from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, Center, Middle, Grid
from textual.widgets import Header, Footer, Static, Input, Button

from components.randomword import random_word
from components.letters import p, l, a, y, exc
from components.renderstring import RenderString

class Game(Screen):

    #BINDINGS = [('space', 'pop_screen', 'Return to game')]

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

        wrdyl_word, wrdyl_definition = random_word()

        r = RenderString()
        render = r.render(f"{wrdyl_word} and {wrdyl_definition}")
        
        yield Center(Static(
            f"{render}\n\n█ █ █ █ █\n\n█ █ █ █ █\n\n█ █ █ █ █\n\n█ █ █ █ █\n\n█ █ █ █ █\n\n█ █ █ █ █\n\n", classes = 'guesses'
            ), classes = 'play_grid'
        )
        yield Center(
            Input(placeholder="guess", classes='input')
        )
        
