from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static

from components.letters import e, x, i, t, qm

class CloseGame(Screen):

    BINDINGS = [('space', 'pop_screen', 'Return to game')]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Vertical(
            Static('  ', classes='welcome'),
            Horizontal(
                Static(e, classes='column', id='w'),
                Static(x, classes='column', id='r'),
                Static(i, classes='column', id='d'),
                Static(t, classes='column', id='y'),
                Static(qm, classes='column', id='l'),
                classes='welcome'
            ),
            Static('Press [b]SPACE[/b] to return to the game \n \n [i]OR[/i] \n \n Press Ctrl+R for a new game \n \n [i]OR[/i] \n \n Press [b]Ctrl+C[/b] to exit the game and return to the terminal.', classes='welcome'),
			Static('  ', classes='welcome')
        )