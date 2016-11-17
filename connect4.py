#!/usr/bin/env python
#connect4.py
###USAGE### connect4.py
import PythonLibraries.wordops_lib as wordops_lib
import PythonLibraries.prgm_lib as prgm_lib
import re
import PythonLibraries.matrix_lib as matrix_lib
from AISuite.game import Game as Game
import AISuite.player as player
from AISuite.alphabeta import UPPER_BOUND, LOWER_BOUND

STANDARD_C4_HEIGHT = 6
STANDARD_C4_WIDTH = 7

def reverse(data):
	for index in range(len(data)-1, -1, -1):
		yield data[index]

class Connect4(Game):
	def __init__(self, player1, player2, be_quiet = False, show_game = False):
		super(self.__class__, self).__init__(player1, player2, be_quiet)
		self.matrix = matrix_lib.init_grid(STANDARD_C4_WIDTH,STANDARD_C4_HEIGHT,' ')
		self.height = [0,0,0,0,0,0,0]
		self.rows = STANDARD_C4_HEIGHT
		self.cols = STANDARD_C4_WIDTH
		self.show_board = show_game
		
	def make_new_instance(self):
		return Connect4(player.Player(), player.Player())
		
	def handle_escape(self, code):
		if code == ":w":
			print "UnemplementedError: saving"
		elif code == ":wq":
			print "UnemplementedError: saving"
			raise SystemExit
		elif code == ":q":
			raise SystemExit
		elif code == ":r":
			connect4_heuristic(str(self))
		
	def opg(self):
		for y in reverse(range(self.rows)):
			str1='| '
			for x in range(self.cols):
				str1=str1+str(self.matrix[y][x]) + ' | '
			print str1
			print '-----------------------------'
		print '  0   1   2   3   4   5   6'

	def check_winner(self):
		temp_l=[]
		for lst in self.matrix:
			temp_l=temp_l + lst
		p1w=wordops_lib.snake_search('XXXX',temp_l,self.cols,True,True)
		p2w=wordops_lib.snake_search('OOOO',temp_l,self.cols,True,True)
		if p1w:
			self.winner = 1
		if p2w:
			self.winner = 2
		if min(self.height) == self.rows:
			self.winner = 0
		return self.winner
				
	def get_child_moves(self):
		return [x for x in range(self.cols) if self.height[x] < self.rows]
	
	def __str__(self):
		value = ''
		for y in self.matrix:
			str1 = ''
			for x in y:
				str1 += str(x)
			value += str1 + ';'
		return value + str(self.turn)

	def load_state_from_string(self, state):
		grid1 = re.split(';', state)
		self.turn = int(grid1[-1])
		grid2 = grid1[:-1]
		self.rows = len(grid2)
		self.cols = len(grid2[0])
		self.matrix = [[str(x) for x in y] for y in grid2]

		self.calculate_height()
		self.check_winner()
		
	def calculate_height(self):
		self.height = [0,0,0,0,0,0,0]
		for x in range(self.cols):
			self.height[x]=min([y for y in range(self.rows) if self.matrix[y][x]==' '] + [self.rows])
			
	def get_player_icon(self, p_num):
		icons = [' ', 'X', 'O']
		return icons[self.get_player_num()]
				
	def get_child_states(self):
		root = str(self)
		moves = self.get_child_moves()
		states = []
		for col in moves:
			self.matrix[self.height[col]][col] = self.get_player_icon(self.get_player_num())
			self.height[col] += 1
			self.turn += 1
			states += [str(self)]
			self.load_state_from_string(root)
		return states
		
	def do_turn(self):
		human = self.is_human_turn()
		if human or self.show_board:
			self.opg()
		col = -1
		if not self.quiet:
			print "Turn " + str(self.turn)
		finished_playing = False
		possible_moves = [str(x) for x in self.get_child_moves()]
		while not finished_playing:
			if human:
				print "Player" + str(self.get_player_num()) + ", enter a number between 0 and " + str(self.cols) + " to play in that column."
			sq = self.current_player().choose_move(self)
			if sq in self.escapes:
				self.handle_escape(sq)
			if str(sq) in possible_moves:
				self.matrix[self.height[int(sq)]][int(sq)] = self.get_player_icon(self.get_player_num())
				self.height[int(sq)] += 1
				self.turn += 1
				finished_playing = True
			else:
				if human:
					print 'Either that column is full or that wasn\'t a valid column'
		self.check_winner()
		

def connect4_heuristic(game_state):
	value = 0
	#manipulate game_state into usable data
	state_split = re.split(';', game_state)
	turn = int(state_split[-1])
	x_s_turn = (turn % 2) == 0
	grid = state_split[:-1]
	cols = len(grid[0])
	temp_l=[]
	for lst in grid:
		temp_l = temp_l + [x for x in lst]
		
	#check if the game is over
	x_quad = wordops_lib.snake_search('XXXX',temp_l,cols,True)
	if x_quad:
		return UPPER_BOUND
	o_quad = wordops_lib.snake_search('OOOO',temp_l,cols,True)
	if o_quad:
		return LOWER_BOUND
	
	#do some calculations that probably take too long	
	weights_x = {" XXX ": 8, "XXX ": 6, "OXXX ": 4, "X XX": 4, " XX  ": 2, "XX  ": 1, "OXX  ": 1, " XX O": 1}
	weights_o = {" OOO ": -8, "OOO ": -6, "XOOO ": -4, "O OO": -4, " OO  ": -2, "OO  ": -1, "XOO  ": -1, " OO X": -1}
	for string in weights_x:
		value += wordops_lib.snake_search(string,temp_l,cols,True)*weights_x[string]
	for string in weights_o:
		value += wordops_lib.snake_search(string,temp_l,cols,True)*weights_o[string]
	
	#slight bonus for being your turn. may consider removing this
	if x_s_turn:
		value += 5
	else:
		value += -5
	
	#respect the bounds
	if value >= UPPER_BOUND:
		value = UPPER_BOUND-1
	elif value <= LOWER_BOUND:
		value = LOWER_BOUND+1
	
	return value

if __name__ == "__main__":
	#g = Connect4(player.Human(), player.Human())
	#g.play()

	num_games = 5

	win_counts = [0,0,0]
	for x in range(num_games):
		print "Beginning game %i" % (x)
		g = Connect4(player.AI_ABPruning(connect4_heuristic, depth_lim = 4),player.RandomAI(),False, True)
		w = g.play()
		win_counts[w] += 1

	print win_counts
	for w in win_counts:
		print str(w) + "/" + str(num_games) + " : " + str(w/float(num_games))
	print	
