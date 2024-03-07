from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Static
from textual.screen import Screen

from components.welcome import Welcome
from components.letters import w, r, d, y, l

class Help(Screen):

	BINDINGS = [('ctrl+h', 'pop_screen', 'Close Help')]

	def compose(self) -> ComposeResult:
		yield Horizontal(
			Static(w, classes='title_letters'),
			Static(r, classes='title_letters'),
			Static(d, classes='title_letters'),
			Static(y, classes='title_letters'),
			Static(l, classes='title_letters')
		)
		yield Static('Help Message', id='help_message')

class CloseGame(Screen):

	BINDINGS = [('ctrl+x', 'pop_screen', 'Close Help')]

	def compose(self) -> ComposeResult:
		yield Horizontal(
			Static(w, classes='title_letters'),
			Static(r, classes='title_letters'),
			Static(d, classes='title_letters'),
			Static(y, classes='title_letters'),
			Static(l, classes='title_letters')
		)
		yield Static('To close game press Ctrl + C', id='close_game_message')
		yield Static('Or press SPACE BAR to go back', id='close_game_message2')

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
            Static('Enter letters to play', classes='welcome'),
            id = 'welcome_page'
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
		('ctrl+d', 'toggle_dark', 'Dark/Light Mode'),
		('ctrl+h', 'help_screen', 'Help Screen'),
		('ctrl+x', 'close_game_screen', 'Close Game'),
		('space', 'game_screen', 'Play game')
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
