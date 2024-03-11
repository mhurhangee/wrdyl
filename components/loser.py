#Imports from textual
from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, Center, VerticalScroll
from textual.widgets import Header, Footer, Static

#Local imports, including ASCII title art
from components.letters import l, o, s, e, r1
from components.renderstring import RenderString

#Losing screen
class Loser(Screen):
    #Constructor class with the random word and it's definition.
    def __init__(self, wrdyl_word: str = 'Hello', wrdyl_def: str = 'World!', play_grid: str = 'Fail') -> None:
        super().__init__()
        self.wrdyl_word = wrdyl_word
        self.wrdyl_def = wrdyl_def
        self.game_display = ''
        #turning list of play_grid into a string
        for i in range(len(play_grid)):
            self.game_display += '\n' + str(play_grid[i]) + '\n'

    #Display ...
    def compose(self) -> ComposeResult:
        r = RenderString()
        render_word = r.render(f"{self.wrdyl_word}")
        render_def = r.render(f"{self.wrdyl_def}")
        #...header and footer
        yield Header()
        yield Footer()
        #...title
        yield Vertical(
            Vertical (
                Horizontal(
                    Static(l, classes='column', id='w'),
                    Static(o, classes='column', id='r'),
                    Static(s, classes='column', id='d'),
                    Static(e, classes='column', id='y'),
                    Static(r1, classes='column', id='l'),
                    classes='welcome'
                )
            ),
            Center(Static(
                f"{self.game_display}", classes = 'guesses'
                ), classes = 'play_grid'
            ),
            Vertical(
                #...losing message
                Static(f"Unlucky [i]LOSER[/i]! You failed to guess [b][white on bright_red]{render_word}[/b][/]. \n \n Press [b]Ctrl+R[/b] to play again. \n \n{render_def}", classes='welcome')
            )
        )