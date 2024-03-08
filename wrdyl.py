from typing import Coroutine
from textual.app import App, ComposeResult, RenderResult, Binding
from textual.containers import Container, Horizontal, Vertical
from textual.events import Key
from textual.widgets import Header, Footer, Static
from textual.screen import Screen
from textual.widget import Widget

import httpx

from components.welcome import Welcome
from components.help import Help
from components.closegame import CloseGame
from components.game import Game
from components.champ import Champ
from components.loser import Loser
from components.randomword import random_word

class Wrdyl(App):

	CSS_PATH = 'wrdyl.tcss'

	SCREENS = {
		'help_screen': Help(),
		'welcome_screen': Welcome(),
		'close_game': CloseGame(),
		'game_screen': Game()
	}

	BINDINGS = [
		('ctrl+w', 'welcome_screen', 'Back to the start'),
		('ctrl+r', 'game_screen', 'Play game'),
		('ctrl+d', 'help_screen', 'Help'),
		('ctrl+y', 'close_game_screen', 'Close Game'),
		('ctrl+l', 'toggle_dark', 'Dark/Light Mode'),
		#('ctrl+r', 'pop_screen', 'Pop'),
		Binding('ctrl+x', 'champ_screen', 'Champ', show=False),
		Binding('ctrl+z', 'loser_screen', 'Loser', show=False)
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
	
	def action_welcome_screen(self) -> None:
		self.push_screen(Welcome())
	
	def action_game_screen(self) -> None:
		self.wrdyl_word, self.wrdyl_def = random_word()

		
		if not self.is_screen_installed(f'game_screen_{self.wrdyl_word}_0'):
			self.install_screen(Game(), f'game_screen_{self.wrdyl_word}_0')
			self.install_screen(Champ(self.wrdyl_word, self.wrdyl_def), f'champ_screen_{self.wrdyl_word}')
			self.install_screen(Loser(self.wrdyl_word, self.wrdyl_def), f'loser_screen_{self.wrdyl_word}')
			self.push_screen(f'game_screen_{self.wrdyl_word}_0')
	
	def action_champ_screen(self) -> None:
		self.pop_screen()
		self.push_screen(f'champ_screen_{self.wrdyl_word}')
	
	def action_loser_screen(self) -> None:
		self.push_screen(f'loser_screen_{self.wrdyl_word}')

if __name__ == '__main__':
	app = Wrdyl()
	app.run()
