#!/usr/bin/env python
#fractoe.py
from AISuite.game import Game as Game
import AISuite.player as player
from AISuite.alphabeta import UPPER_BOUND, LOWER_BOUND, shallowest_first
import AISuite.recorder as recorder
import AISuite.PythonLibraries.prgm_lib as prgm_lib
import fractoe_tictactoe as tictactoe
Tictactoe = tictactoe.Tictactoe
import AISuite.PythonLibraries.wordops_lib as wordops_lib

BOARD_SIZE = 2

def coor_split(num, size = BOARD_SIZE):
	col = num % size
	row = (num - col) / size
	return [row,col]

def coor_splice(row,col, size = BOARD_SIZE):
	return row*size + col

class Pentago(Game):
	def __init__(self, player1, player2, be_quiet = False, show_game = False):
		super(self.__class__, self).__init__(player1, player2, be_quiet)
		self.grid = [[Tictactoe(), Tictactoe()],[Tictactoe(),Tictactoe()]]
		self.rows = BOARD_SIZE
		self.cols = BOARD_SIZE
		self.show_board = show_game
		self.thinking = False
		self.player_token = [" ","X","O"]
		#self.last_moves = [ [[-1,-1],[-1,-1]], [[-1,-1], [-1,-1]] ]
		
		
	def __str__(self):
		value = ""
		for row in range(BOARD_SIZE):
			for col in range(BOARD_SIZE):
				value += str(self.grid[row][col]) + ";"
		value += str(self.turn)
		return value
		
	@staticmethod
	def parse_state(game_state):
		split_list = game_state.split(';')
		split_list = split_list[:-1]
		return ';'.join(split_list)
	
	def get_child_states(self):
		root = str(self)
		moves = self.get_child_moves()
		states = []
		for m in moves:
			self.update_from_move(m)
			states += [str(self)]
			self.load_state_from_string(root)
		return states
		
	
	def get_child_moves(self):
		children = []
		for x in range(len(self.grid)):
			for y in range(len(self.grid[x])):
				for j in range(3):		#3 because tictactoe
					for k in range(3):	#as above
						if self.grid[x][y].get_square(j,k) == " ":
							m_str = str(coor_splice(x,y)) + str(coor_splice(j,k,3))
							for t in ['A','C']:
								for b in range(BOARD_SIZE * BOARD_SIZE):
									children += [m_str + t + str(b)]
		return children
	
	
	def update_from_move(self, move):
		b1 = int(move[0])
		[x,y] = coor_split(b1)
		sq = int(move[1])
		[j,k] = coor_split(sq,3)
		rotation = move[2]
		rotation_b = int(move[3])
		[z,w] = coor_split(rotation_b)
		token = self.player_token[self.get_player_num()]
		
		self.grid[x][y].set_square(j,k, token)
		self.grid[z][w].rotate(rotation)
		self.turn += 1
		
		
	def do_turn(self):
		human = self.is_human_turn()
		if human or self.show_board:
			self.opg()
		if not human:
			if not self.quiet and not self.thinking:
				print "Player" + str(self.get_player_num()) + " (the computer) is thinking..."
				self.thinking = True
		finished_playing = False
		valid_moves = self.get_child_moves()
		while not finished_playing:
			if human:
				print "Player" + str(self.get_player_num()) + ", it is your turn to play."
				print "Please enter a valid move string."
				print "a valid move string is two numbers a letter and a number, such as 18C2 or 18A2"
				print "this indicates the 8-th square on the 1-st board (both 0-indexed)"
				print "followed by a clockwise or anti-clockwise rotation of the second board."
			move = self.current_player().choose_move(self)
			if human and move in self.escapes:
				self.handle_escape(move)
			elif move.upper() in valid_moves:
				self.update_from_move(move.upper())
				finished_playing = True
				self.thinking = False
			else:
				if human:
					print "That wasn\'t a valid move."
					print "valid moves look like: [0-3][0-8][AC][0-3]"
					self.opg()
		self.check_winner()
	
	
	def make_new_instance(self):
		return Pentago(player.Player(), player.Player())
		
	
	def load_state_from_string(self, state_string):
		class_data = state_string.split(";")
		boards = BOARD_SIZE * BOARD_SIZE
		for num in range(boards):
			col = num % BOARD_SIZE
			row = (num - col) / BOARD_SIZE
			self.grid[row][col].load(class_data[num])
		self.turn = int(class_data[-1])
		self.check_winner()
		
	
	def opg(self):
		prgm_lib.cls(100)
		for x in range(len(self.grid)):
			size = 0
			string0 = ''
			for z in range(3):	#3 because tictactoe
				string1 = ''
				string2 = ''
				for y in range(len(self.grid[x])):
					string3 = self.grid[x][y].get_row(z)
					for var in range(len(string3)):
						string2 += "-"
					string1 += string3 + "|"
					string2 += "|"
				print string1[:-1]
				if z != 2:
					print string2[:-1]
				size = len(string2)-1
			for var in range(size):
				string0 += "="
			if x != 2:
				print string0
		print
		
	
	def check_winner(self):
		temp_l = []
		for x in range(len(self.grid)):
			for z in range(3):
				string0 = ''
				for y in range(len(self.grid[x])):
					string0 += str(self.grid[x][y])[z*3:(z+1)*3]
				temp_l += [l for l in string0]
			
		p1w = wordops_lib.snake_search('XXXXX',temp_l, 6,True,True)
		p2w = wordops_lib.snake_search('OOOOO',temp_l, 6,True,True)
		if p1w and p2w:
			self.winner = 0
		else:
			if p1w:
				self.winner = 1
			elif p2w:
				self.winner = 2
			elif self.check_full():
				self.winner = 0
		return self.winner
		
	
	def check_full(self):
		full = True
		for x in range(len(self.grid)):
			for y in range(len(self.grid[x])):
				if not self.grid[x][y].is_full():
					full = False
		return full
		
	
def pentago_heuristic(game_string):
	state_l = game_string.split(";")
	turn = state_l[-1]
	state_l = state_l[:-1]
	board_lists = [[let for let in x] for x in state_l]
	x_val = 0
	o_val = 0
	
	for board in board_lists:
		x_val += wordops_lib.snake_search("XX",board,3,True)*2
		x_val += wordops_lib.snake_search("XXX",board,3,True)*3
		o_val += wordops_lib.snake_search("OO",board,3,True)*2
		o_val += wordops_lib.snake_search("OOO",board,3,True)*3
		
	value = x_val - o_val
	
	#respect the bounds
	if value >= UPPER_BOUND:
		value = UPPER_BOUND-1
	elif value <= LOWER_BOUND:
		value = LOWER_BOUND+1	
		
	return x_val - o_val
	
	
if __name__ == "__main__":

	g = Pentago(player.Human(), player.RandomAI())
	g.play()	
