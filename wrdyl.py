#Imports from textual for the app
from textual.app import App, Binding
from textual.widgets import  Input

#Local imports of classes used to generate different screens of the game.
#I.e. the welcome splash screen, help screen, confirming closing the game screen, winning and losing screens.
from components.welcome import Welcome
from components.help import Help
from components.closegame import CloseGame
from components.game import Game
from components.champ import Champ
from components.loser import Loser

#Function to retrieve a random word from an API and it's definition from a dictionary API
from components.randomword import random_word

#Main and parent App class for the textual application. All other classes and functions are called from the Wrdyl app.
class Wrdyl(App):

	#CSS style sheet in textual format
	CSS_PATH = 'wrdyl.tcss'

	#Pre-installing the main screens of the app.
	SCREENS = {
		'help_screen': Help(),
		'welcome_screen': Welcome(),
		'close_game': CloseGame(),
		'game_screen': Game()
	}

	#Defining the key bindings used to play and navigate the app.
	BINDINGS = [
		Binding('ctrl+w', 'welcome_screen', 'Back to the start', show=True, priority=True),
		Binding('ctrl+r', 'game_screen', 'Play game', show=True, priority=True),
		Binding('ctrl+d', 'help_screen', 'Help', show=True, priority=True),
		Binding('ctrl+y', 'close_game_screen', 'Close Game', show=True, priority=True)#,
		#Binding('ctrl+l', 'toggle_dark', 'Dark/Light Mode', show=True, priority=True),
	]

	#Title of the app displayed in the header.
	TITLE = 'WRDYL: A python clone of Wordle for your terminal'

	#Shows the Welcome screen on the App being loaded.
	def on_mount(self) -> None:
		self.push_screen(Welcome())

	#Show the help screen when the key binding to help_screen is pressed (ctrl+d)
	def action_help_screen(self) -> None:
		self.push_screen(Help())

	#Show the close game? screen when the key binding to close_game_screen is pressed (ctrl+y)
	def action_close_game_screen(self) -> None:
		self.push_screen(CloseGame())
	
	#Show the welcome screen when the key binding to welcome_screen is pressed (ctrl+w)
	def action_welcome_screen(self) -> None:
		self.push_screen(Welcome())

	#Initialise play grid variable that is used to display the blocks and letters for the game,
		#guesses which is used to track which turn the player is on (and which row on the play grid to edit) and
		# list of previous guesses
	play_grid = ''
	guesses = 0
	previous_words = []
	
	#Show a new game screen when the key binding to game_screen is pressed (ctrl+r). Is used to start
		#a new game, generate a new random word and fresh interface.
	def action_game_screen(self) -> None:
		
		#Get a random word and its definition from the APIs
		self.wrdyl_word, self.wrdyl_def = random_word()

		#check if a game screen for the random word exists. The game_screens are called game_screen_<random_word>_<no. of guess>.
			#Thereby each screen is unique and avoids their names clashing.  Popping and uninstalling the screen would be preferable 
			#to avoid making more and more screens. However, uninstall feature of textual appears to be bugged/not working as intended. 
		if not self.is_screen_installed(f'game_screen_{self.wrdyl_word}_0'):

			#Reset the variables for the new game.
			self.guesses = 0
			self.previous_words = []
			self.play_grid = ['███ ███ ███ ███ ███' for i in range(6)]

			#Initialise and install game screen for this games random word
			game = Game(self.wrdyl_word, self.play_grid)
			self.install_screen(game, f'game_screen_{self.wrdyl_word}_0')

			#Install winning and losing screens to be called later if need.
			self.install_screen(Champ(self.wrdyl_word, self.wrdyl_def), f'champ_screen_{self.wrdyl_word}')
			self.install_screen(Loser(self.wrdyl_word, self.wrdyl_def), f'loser_screen_{self.wrdyl_word}')

			#Display game screen
			self.push_screen(f'game_screen_{self.wrdyl_word}_0')

	#Function used in logic of colouring the letters. It finds all the instances of the a character in a string
			#and reutns as a list of indexes
	def find_all_indexes(self, string, char) -> list:
		indexes = []
		try:
			index = string.index(char)
			while True:
				indexes.append(index)
				index = string.index(char, index + 1)
		except ValueError:
			pass
		return indexes
	
	#Called whenever a user submits a guess by hitting enter. Logic used to assess guesses and update play grid.
	def on_input_submitted(self, event: Input.Submitted) -> None:

		#Assess if input is valid (length==5, in dictionary API, only A to Z and not already guessed)
			#If valid continue, otherwise display notification saying it is not valid.
		if event.validation_result.is_valid and event.value not in self.previous_words:
			#track number of guesses and previous guesses  
			self.guesses += 1
			self.previous_words.append(event.value)

			#for readbility set the player guess and random word to new variables and as UPPERCASE
			player_wrdyl = event.value.upper()
			random_wrdyl = self.wrdyl_word.upper()

			#Matching swapped variables are used in the logic to determine matches betweem the player's word and the random word.
				#The matching_swapped variables are editted as matches are found to prevent a two letters of the player's word matching
				#against a single letter in random word. Thus, providing a more accurate not misleading coloured output.
			matching_swapped_player_word =  player_wrdyl
			matching_swapped_wordle_word = random_wrdyl
			
			#Initialise coloured output to replace the row in the play grid
			coloured_output = ''

			#Find the direct matches i.e. the H in HELLO and HATCH. but not the H, L and O in HELLO and LOATH. Marked as green in game.	
				#For each character in the random word, check if the character matches the corresponding character in the player guess.
				#If so, swap the letter out for $ or £, respectively to prevent additional matches later and to provide coloured output.
				#Also, add to correct letter index
			for index, char in enumerate(random_wrdyl):
				if char ==  player_wrdyl[index]:
					matching_swapped_player_word = matching_swapped_player_word[:index] + '£' + matching_swapped_player_word[index+1:]
					matching_swapped_wordle_word = matching_swapped_wordle_word[:index] + '$' + matching_swapped_wordle_word[index+1:]

			#Form sets of unique characters for each word (not including the direct matches) and find their intersection
				#That way, we know if there are any common letters to mark as yellow. I.e. the H, L and O in HELLO AND SLOTH.
				#The H in HELLO and HATCH would not appear as swapped for £ and $ respectively.
			wordle_set = set(matching_swapped_wordle_word)
			player_set = set(matching_swapped_player_word)
			common_set = wordle_set & player_set

			#Initialise dictionaries to store common letters from both words as the key and their frequency as the value
			common_dictionary_wordle_count = {}
			common_dictionary_player_count = {}

			#Check if common set has any members, i.e. check there are common letters.
				#For example, none in HELLO and HATCH and three in HELLO AND SLOTH
			if len(common_set) != 0:
				#store common letters for random and player words as the key and their frequency as the value
				for letter in common_set:
					common_dictionary_wordle_count[letter] = matching_swapped_wordle_word.count(letter)
					common_dictionary_player_count[letter] = matching_swapped_player_word.count(letter)

				#Used to store which common letters to swap out. In case of the L in HELLO and SLOTH,
					#we only want to swap (i.e. colour yellow) the first L in HELLO as only one L in SLOTH. 
				commons_letter_index = [[] for i in range(len(common_dictionary_player_count))]

				#For each common letter, if the frequency of the letter is less or equal in the player word, find all the indexes in 
				 #the random word. For example, if player word SLOTH and random word HELLO, for L we find all the indexes of L in SLOTH
				i = 0 
				for key in common_dictionary_player_count.keys():
					commons_letter_index[i] = commons_letter_index[i] + self.find_all_indexes(matching_swapped_player_word,key)
					while len(commons_letter_index[i]) > common_dictionary_wordle_count[key]:
						commons_letter_index[i].pop()
					i += 1
				
				common_letters_list = []
				[common_letters_list.extend(row) for row in commons_letter_index]

				for index in common_letters_list:
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

		#If the input submitted by the user isn't valid display a notification informing the user of why.
		elif event.value.upper() == "WRDYL" :
			self.notify(f"It's the name of the game.", title="WRDYL!", severity="information", timeout=5)
		elif event.value in self.previous_words:
			self.notify(f"Already guessed [i]{event.value.upper()}[/] before. Please enter a unique word", title="Already guessed!", severity="warning", timeout=5)
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

#Run the app
if __name__ == '__main__':
	app = Wrdyl()
	app.run()