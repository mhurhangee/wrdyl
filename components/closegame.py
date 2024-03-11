#Imports from textual
from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static

#Import of ascii title art
from components.letters import e, x, i, t, qm

#Close game? screen
class CloseGame(Screen):

    #Binding to go back, without starting a new game
    BINDINGS = [('space', 'pop_screen', 'Return to game')]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        #ASCII title
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
            #Message to display
            Static('Press [b]SPACE[/b] to return. \n [i]OR[/i] \n Press [b]Ctrl+R[/b] for a new game \n [i]OR[/i] \n Press [b]Ctrl+C[/b] to exit the game and return to the terminal.', classes='welcome'),
			#Padding
            Static('  ', classes='welcome')
        )