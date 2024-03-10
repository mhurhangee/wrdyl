from typing import Coroutine
from textual.app import App, ComposeResult, RenderResult, Binding
from textual.containers import Container, Horizontal, Vertical
from textual.events import Key
from textual.widgets import Header, Footer, Static, Input
from textual.screen import Screen
from textual.widget import Widget
from textual.validation import ValidationResult

import httpx

from colorama import Back

import time

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
		Binding('ctrl+w', 'welcome_screen', 'Back to the start', show=True, priority=True),
		Binding('ctrl+r', 'game_screen', 'Play game', show=True, priority=True),
		Binding('ctrl+d', 'help_screen', 'Help', show=True, priority=True),
		Binding('ctrl+y', 'close_game_screen', 'Close Game', show=True, priority=True),
		Binding('ctrl+l', 'toggle_dark', 'Dark/Light Mode', show=True, priority=True),
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

	play_grid = ['███ ███ ███ ███ ███' for i in range(6)]
	#'\n\n█ █ █ █ █\n\n█ █ █ █ █\n\n█ █ █ █ █\n\n█ █ █ █ █\n\n█ █ █ █ █\n\n█ █ █ █ █\n\n'
	
	def action_game_screen(self) -> None:
		self.wrdyl_word, self.wrdyl_def = random_word()

		if not self.is_screen_installed(f'game_screen_{self.wrdyl_word}_0'):
			self.guesses = 0
			self.previous_words = []
			self.play_grid = ['███ ███ ███ ███ ███' for i in range(6)]
			game = Game(self.wrdyl_word, self.play_grid)
			self.install_screen(game, f'game_screen_{self.wrdyl_word}_0')
			self.install_screen(Champ(self.wrdyl_word, self.wrdyl_def), f'champ_screen_{self.wrdyl_word}')
			self.install_screen(Loser(self.wrdyl_word, self.wrdyl_def), f'loser_screen_{self.wrdyl_word}')
			self.push_screen(f'game_screen_{self.wrdyl_word}_0')

	
	def action_champ_screen(self) -> None:
		self.pop_screen()
		self.push_screen(f'champ_screen_{self.wrdyl_word}')
	
	def action_loser_screen(self) -> None:
		self.push_screen(f'loser_screen_{self.wrdyl_word}')

	def find_all_indexes(self, string, char):
		indexes = []
		try:
			index = string.index(char)
			while True:
				indexes.append(index)
				index = string.index(char, index + 1)
		except ValueError:
			pass
		return indexes
	
	guesses = 0
	previous_words = []

	def on_input_submitted(self, event: Input.Submitted) -> None:
		if event.validation_result.is_valid and event.value not in self.previous_words: 
			self.guesses += 1
			self.previous_words.append(event.value)

			player_wrdyl = event.value.upper()
			random_wrdyl = self.wrdyl_word.upper()

			matching_swapped_player_word =  player_wrdyl
			matching_swapped_wordle_word = random_wrdyl
			coloured_output = ''

			correct_letter_index = []
			for index, char in enumerate(random_wrdyl):
				if char ==  player_wrdyl[index]:
					correct_letter_index.append(index)
					matching_swapped_player_word = matching_swapped_player_word[:index] + '£' + matching_swapped_player_word[index+1:] #(SKIN£) or K££££
					matching_swapped_wordle_word = matching_swapped_wordle_word[:index] + '$' + matching_swapped_wordle_word[index+1:]

			wordle_set = set(matching_swapped_wordle_word)
			player_set = set(matching_swapped_player_word)

			common_set = wordle_set & player_set
			common_dictionary_wordle_count = {}
			common_dictionary_player_count = {}

			if len(common_set) != 0:
				for letter in common_set:
					common_dictionary_wordle_count[letter] = matching_swapped_wordle_word.count(letter)
					common_dictionary_player_count[letter] = matching_swapped_player_word.count(letter)

				commons_letter_index = []
				
				for key in common_dictionary_player_count.keys():
					if common_dictionary_player_count[key] <= common_dictionary_wordle_count[key]:
						commons_letter_index = commons_letter_index + self.find_all_indexes(matching_swapped_player_word,key)
#if count in player word is greater than count in wordle word
					else:
						commons_letter_index = commons_letter_index + self.find_all_indexes(matching_swapped_player_word,key)
						while len(commons_letter_index) > common_dictionary_wordle_count[key]:
							commons_letter_index.pop()
            
				for index in commons_letter_index:
					matching_swapped_player_word = matching_swapped_player_word[:index] + '@' + matching_swapped_player_word[index+1:]
                    
			for i in range(len(random_wrdyl)):
				if matching_swapped_player_word[i] == '£':
					coloured_output += '[b][white on bright_green]' +  ' ' + player_wrdyl[i]+ ' ' + '[/][/] '
				elif matching_swapped_player_word[i] == '@':
					coloured_output += '[b][white on bright_yellow]' +  ' ' + player_wrdyl[i]+ ' ' +  '[/][/] '
				else:
					coloured_output += '[b][white]'  +  ' ' + player_wrdyl[i]+ ' ' + '[/][/] '


			self.play_grid[self.guesses-1] = "~ " + coloured_output + "~"
				
			game = Game(self.wrdyl_word, self.play_grid)
			self.install_screen(game, f'game_screen_{self.wrdyl_word}_{self.guesses}')
			self.push_screen(f'game_screen_{self.wrdyl_word}_{self.guesses}')

			if matching_swapped_player_word == '£££££':
				#time.sleep(6)
				self.push_screen(f'champ_screen_{self.wrdyl_word}')
				self.notify("WINNER WINNER CHICKEN DINNER", title="WRDYL", severity="information", timeout=5)
			elif self.guesses == 6:
				#time.sleep(6)
				self.push_screen(f'loser_screen_{self.wrdyl_word}')
				self.notify(f" Read a book.", title="Pathetic", severity="information", timeout=5)

		elif event.value.upper() == "WRDYL" :
			self.notify(f"It's the name of the game.", title="WRDYL!", severity="information", timeout=5)
		elif event.value in self.previous_words:
			self.notify(f"Already guessed {event.value} before. Please enter a unique word", title="Already guessed!", severity="warning", timeout=5)
		elif not event.value.isalpha():
			self.notify(f"Your guess can only contain the letters A to Z.", title="Weird characters!", severity="error", timeout=5)
		elif not event.validation_result.is_valid and len(event.value) < 5:
			self.notify(f"Your guess is too short. Please enter a five letter word.", title="Too short", severity="information", timeout=5)
		elif not event.validation_result.is_valid and len(event.value) > 5:
			self.notify(f"Your guess is too long. Please enter a five letter word.", title="Too long", severity="warning", timeout=5)
		elif not event.validation_result.is_valid:
			self.notify(f"Your guess {event.value} is not in our dictionary. Please try another word.", title="Not in dictionary", severity="information", timeout=5)
		else:
			pass

		


if __name__ == '__main__':
	app = Wrdyl()
	app.run()