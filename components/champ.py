#Imports from textual
from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, Center
from textual.widgets import Header, Footer, Static

#Local imports, including ASCII title art
from components.letters import c, h, a, m, p
from components.renderstring import RenderString

#Winning screen
class Champ(Screen):

    #Constructor class with the random word and it's definition.
    def __init__(self, wrdyl_word: str = "Hello", wrdyl_def: str = "World!", play_grid: str = 'Fail') -> None:
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
        # ...title art
        yield Vertical(
            Vertical(
                Horizontal(
                    Static(c, classes='column', id='w'),
                    Static(h, classes='column', id='r'),
                    Static(a, classes='column', id='d'),
                    Static(m, classes='column', id='y'),
                    Static(p, classes='column', id='l'),
                    classes='welcome'
                )
            ),
            Center(Static(f"{self.game_display}", classes = 'guesses'), classes = 'play_grid' ),
            Vertical(
                #...Winners message
                Static(f"Well done [i]CHAMP[/i]! You guessed [b][white on bright_green]{render_word}[/][/b]. \n \n Press [b]Ctrl+R[/b] to play [b]Wrdyl[/b] again! \n \n {render_def}", classes='welcome'),
                #...Padding
                Static('  ', classes='welcome')
            )
        )