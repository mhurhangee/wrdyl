from textual.screen import Screen
from textual.app import ComposeResult, Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static

from components.letters import l, o, s, e, r1
from components.renderstring import RenderString

class Loser(Screen):

    BINDINGS = [
        Binding('space', 'pop_screen', 'Return to game')
        ]

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
                Static(l, classes='column', id='w'),
                Static(o, classes='column', id='r'),
                Static(s, classes='column', id='d'),
                Static(e, classes='column', id='y'),
                Static(r1, classes='column', id='l'),
                classes='welcome'
            ),
            Static(f"Unlucky [b]LOSER[/b]. You failed to guess [b]{render_word}[/b]. \n \n {render_def}", classes='welcome')
        )