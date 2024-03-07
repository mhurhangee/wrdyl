from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static
from components.letters import w, r, d, y, l



class Welcome(Screen):

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Vertical(
            Static('  ', classes='welcome'),
            Horizontal(
                Static(w, classes='column', id='w'),
                Static(r, classes='column', id='r'),
                Static(d, classes='column', id='d'),
                Static(y, classes='column', id='y'),
                Static(l, classes='column', id='l'),
                classes='welcome'
            ),
            Static('Welcome to [b]WRDYL[/b]: [i]A python clone of Wordle for your terminal.[/i] \n\n\n Press [b]SPACE[/b] to play the game', classes='welcome'),
			Static('  ', classes='welcome'),
            id = 'welcome_page'
        )