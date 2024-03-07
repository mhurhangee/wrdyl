from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static

from components.letters import h, e, l, p, exc



class Help(Screen):

    BINDINGS = [('question_mark', 'pop_screen', 'Close Help')]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Vertical(
            Static('  ', classes='welcome'),
            Horizontal(
                Static(h, classes='column', id='w'),
                Static(e, classes='column', id='r'),
                Static(l, classes='column', id='d'),
                Static(p, classes='column', id='y'),
                Static(exc, classes='column', id='l'),
                classes='welcome'
            ),
            Static('[b]How To Play[/b]\n\nGuess the Wordle in 6 tries.\n\nEach guess must be a valid 5-letter word.\n\nThe color of the tiles will change to show how close your guess was to the word.', classes='welcome'),
			Static('  ', classes='welcome')
        )