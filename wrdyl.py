from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Static
from textual.screen import Screen

from components.welcome import Welcome
from components.help import Help
from components.closegame import CloseGame
from components.letters import w, r, d, y, l

class Game(Screen):

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Vertical(
            Static('[b](Welcome to)', classes='welcome'),
            Horizontal(
                Static(w, classes='column'),
                Static(r, classes='column'),
                Static(d, classes='column'),
                Static(y, classes='column'),
                Static(l, classes='column'),
                classes='welcome'
            ),
            Static('Enter letters to play', classes='welcome')
        )

class Wrdyl(App):

	CSS_PATH = 'wrdyl.tcss'

	SCREENS = {
		'help_screen': Help(),
		'welcome': Welcome(),
		'close_game': CloseGame(),
		'game_screen': Game()
	}

	BINDINGS = [
		('space', 'game_screen', 'Play game'),
		('question_mark', 'help_screen', 'Help'),
		('ctrl+x', 'close_game_screen', 'Close Game'),
		('ctrl+d', 'toggle_dark', 'Dark/Light Mode')
	]

	TITLE = 'WRDYL: A python clone of Wordle for your terminal'

	def on_mount(self) -> None:
		self.push_screen(Welcome())

	def action_toggle_dark(self) -> None:
		self.dark = not self.dark

	def action_help_screen(self) -> None:
		self.push_screen(Help())

	def action_close_game_screen(self) -> None:
		self.push_screen(CloseGame())

	def action_game_screen(self) -> None:
		self.push_screen(Game())

if __name__ == '__main__':
	Wrdyl().run()
