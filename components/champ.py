from textual.screen import Screen
from textual.app import ComposeResult, Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static

from components.letters import c, h, a, m, p
from components.renderstring import RenderString

class Champ(Screen):

    BINDINGS = [('space', 'pop_screen', 'Pop')]
#		('ctrl+w', 'welcome_screen', 'Back to the start'),
#		('ctrl+r', 'game_screen', 'Play game'),
#		('ctrl+d', 'help_screen', 'Help'),
#		('ctrl+y', 'close_game_screen', 'Close Game'),
#		('ctrl+l', 'toggle_dark', 'Dark/Light Mode'),
#		#('ctrl+r', 'pop_screen', 'Pop'),
#		Binding('ctrl+x', 'champ_screen', 'Champ', show=False),
#		Binding('ctrl+z', 'loser_screen', 'Loser', show=False)
 #       ]

    def __init__(self, wrdyl_word: str = "Hello", wrdyl_def: str = "World!") -> None:
        super().__init__()
        self.wrdyl_word = wrdyl_word
        self.wrdyl_def = wrdyl_def

    def compose(self) -> ComposeResult:
        r = RenderString()
        render_word = r.render(f"{self.wrdyl_word}")
        render_def = r.render(f"{self.wrdyl_def}")
        yield Header()
        yield Footer()
        yield Vertical(
            Horizontal(
                Static(c, classes='column', id='w'),
                Static(h, classes='column', id='r'),
                Static(a, classes='column', id='d'),
                Static(m, classes='column', id='y'),
                Static(p, classes='column', id='l'),
                classes='welcome'
            ),
            Static(f"Well done [b]CHAMP[/b]. You guessed [b]{render_word}[/b]. \n \n {render_def}", classes='welcome')
        )