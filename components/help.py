#Imports from textual
from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static

#Import ascii title art
from components.letters import h, e, l, p, exc


#Help screen
class Help(Screen):

    #Binding to return to game
    BINDINGS = [('space', 'pop_screen', 'Close Help')]

    #Display ...
    def compose(self) -> ComposeResult:
        #...header and footer
        yield Header()
        yield Footer()
        yield Vertical(
            #...top padding
            Static('  ', classes='welcome'),
            #...title
            Horizontal(
                Static(h, classes='column', id='w'),
                Static(e, classes='column', id='r'),
                Static(l, classes='column', id='d'),
                Static(p, classes='column', id='y'),
                Static(exc, classes='column', id='l'),
                classes='welcome'
            ),
            #...help message
            Static('[b]How To Play[/b]\n\nGuess the Wordle in 6 tries.\n\nEach guess must be a valid 5-letter word.\n\nThe color of the tiles will change to show how close your guess was to the word.\n\n Press [b]SPACE[/b] to return.', classes='welcome'),
			#...padding
            Static('  ', classes='welcome')
        )