#!/usr/bin/env python
#connect4.py
###USAGE### connect4.py
import re
import AISuite.PythonLibraries.matrix_lib as matrix_lib
from AISuite.game import Game as Game
import AISuite.player as player
from AISuite.alphabeta import UPPER_BOUND, LOWER_BOUND, shallowest_first

BOARD_SIZE = 8

def reverse(data):
	for index in range(len(data)-1,-1,-1):
		yield data[index]

class Othello(Game):
	escapes = [":w", ":q", ":wq", ":r", ":m"]
	
	def __init__(self, player1, player2, be_quiet = False, show_game = False):
		super(self.__class__, self).__init__(player1, player2, be_quiet)
		self.matrix = matrix_lib.init_grid(BOARD_SIZE, BOARD_SIZE, ' ')
		self.matrix[3][3] = 'X'
		self.matrix[3][4] = 'O'
		self.matrix[4][3] = 'O'
		self.matrix[4][4] = 'X'
		self.rows = BOARD_SIZE
		self.cols = BOARD_SIZE
		self.show_board = show_game
		
	def make_new_instance(self):
		return Othello(player.Player(), player.Player())
	
	def handle_escape(self, code):
		if code == ":w":
			print "UnemplementedError: saving"
		elif code == ":wq":
			print "UnemplementedError: saving"
			raise SystemExit
		elif code == ":q":
			raise SystemExit
		elif code == ":r":
			pass
		elif code == ":m":
			print self.get_child_moves()
		
	def opg(self):
		moves = self.get_child_moves()
		for y in reverse(range(self.rows)):
			str1 = str(y)
			for x in range(self.cols):
				if self.sq2string(y,x) in moves:
					icon = '.'
				else:
					icon = str(self.matrix[y][x])
				str1 = str1 + '|' + icon
			print str1 + '|'
		print '------------------'
		print ' |a|b|c|d|e|f|g|h|'
		
	def get_player_icon(self, p_num = -1):
		icons = [' ', 'X', 'O']
		if p_num == -1:
			p_num = self.get_player_num()
		return icons[p_num]
		
	def check_winner(self):
		has_x = False
		has_o = False
		has_blank = False
		num_x = 0
		num_o = 0
		for row in self.matrix:
			for item in row:
				if item == 'X':
					has_x = True
					num_x += 1
				if item == 'O':
					has_o = True
					num_o += 1
				if item == ' ':
					has_blank = True
		if has_x and has_o and has_blank:
			if self.get_child_moves() == []:
				if num_x > num_o:
					self.winner = 1
				elif num_x < num_o:
					self.winner = 2
				elif num_x == num_o:
					self.winner = 0
		if has_x and not has_o:
			self.winner = 1
		if has_o and not has_x:
			self.winner = 2
		if not has_blank:
			if num_x > num_o:
				self.winner = 1
			elif num_x < num_o:
				self.winner = 2
			elif num_x == num_o:
				self.winner = 0
		return self.winner
		
	def __str__(self):
		value = ''
		for row in self.matrix:
			str1 = ''
			for x in row:
				str1 += str(x)
			value += str1 + ';'
		return value + str(self.turn) + ';' + str(self.winner)
		
	def load_state_from_string(self, state):
		grid1 = re.split(';', state)
		self.winner = int(grid1[-1])
		self.turn = int(grid1[-2])
		grid2 = grid1[:-2]
		self.rows = len(grid2)
		self.cols = len(grid2[0])
		self.matrix = [[str(x) for x in row] for row in grid2]
	
	def sq2string(self, y, x):
		num2let = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}
		return num2let[x] + str(y)
		
	def get_child_moves(self):
		moves = []
		for y in range(self.rows):
			for x in range(self.cols):
				if self.matrix[y][x] == ' ':
					sq = self.sq2string(y,x)
					indices = self.parse_move(sq)
					if len(indices) > 1:
						moves += [sq]
		return moves
	
	#returns a list of squares that get changed to the current player's token	
	def parse_move(self, move):
		let2num = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
		row = int(move[1])
		col = let2num[move[0]]
		indices = [(row,col)]
		lines = []
		line_strs = []
		for y in [-1,0,1]:
			for x in [-1,0,1]:
				if [y,x] != [0,0]:
					line = self.get_line(row,col,[y,x])
					lines += [line]
					line_strs += [''.join([self.matrix[item[0]][item[1]] for item in line])]
		icon = self.get_player_icon()
		for k in range(len(lines)):
			string = line_strs[k]
			if icon in string:
				i = 0
				if ' ' in string:
					if string.index(icon) < string.index(' '):
						i = string.index(icon)
				else:
					i = string.index(icon)
				for x in range(i):
					indices += [lines[k][x]]
		return indices
						
			
	def get_line(self,y,x,dr, include_base = False):
		indices = []
		if include_base:
			indices += [(y,x)]
		y1 = y + dr[0]
		x1 = x + dr[1]
		while y1 in range(self.rows) and x1 in range(self.cols):
			indices += [(y1,x1)]
			y1 += dr[0]
			x1 += dr[1]
		return indices
	
	def get_child_states(self):
		root = str(self)
		moves = self.get_child_moves()
		states = []
		for mv in moves:
			indices = self.parse_move(mv)
			token = self.get_player_icon()
			for pos in indices:
				self.matrix[pos[0]][pos[1]] = token
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
		possible_moves = self.get_child_moves()
		while not finished_playing:
			if human:
				print "Player" + str(self.get_player_num()) + ", enter a valid othello move"
			move = self.current_player().choose_move(self)
			if human and move in self.escapes:
				self.handle_escape(move)
			if str(move) in possible_moves:
				indices = self.parse_move(move)
				token = self.get_player_icon()
				for pos in indices:
					self.matrix[pos[0]][pos[1]] = token
				self.turn += 1
				finished_playing = True
			else:
				if human:
					print 'That wasn\'t a valid move.'
					print 'valid moves look like: a3 or c5'
					self.opg()
		self.check_winner()
	
def value_of_square(y,x, size = BOARD_SIZE):
	value = 1
	if y == 0 or y == size - 1:
		value += 3
	if x == 0 or x == size - 1:
		value += 3
	return value	
		
def othello_heuristic(game_state):
	value = 0
	#manipulate game_state into usable data
	state_split = re.split(';', game_state)
	winner = int(state_split[-1])
	turn = int(state_split[-2])
	x_s_turn = (turn % 2) == 0
	grid = state_split[:-2]
	matrix = [[x for x in y] for y in grid]
	cols = len(matrix[0])
	rows = len(matrix)	
	#check if the game is over
	if winner == 1:
		return UPPER_BOUND
	elif winner == 2:
		return LOWER_BOUND
	elif winner == 0:
		return 0
	#do some calculations that probably take too long
	value_dict = {'X':1, 'O':-1}
	for y in range(len(matrix)):
		for x in range(len(matrix[y])):
			token = matrix[y][x]
			if token in value_dict:
				value += value_dict[token]*value_of_square(y,x)
				
	#respect the bounds
	if value >= UPPER_BOUND:
		value = UPPER_BOUND-1
	elif value <= LOWER_BOUND:
		value = LOWER_BOUND+1
	
	return value	
		
if __name__ == "__main__":
	
#	g = Othello(player.Human(),player.Human())
#	g.play()
	
	#some random games
#	num_games_random = 100
#	win_counts_random = [0,0,0]
#	for x in range(num_games_random):
#		g = Othello(player.RandomAI(),player.RandomAI(),True)
#		w = g.play()
#		win_counts_random[w] += 1
#		if w == 0:
#			g.opg()
#	print win_counts_random
#	for w in win_counts_random:
#		print str(w) + "/" + str(num_games_random) + " : " + str(w/float(num_games_random))
#	print
	
	#some AI games
	num_games = 5
	win_counts = [0,0,0]
	for x in range(num_games):
		print "Beginning game %i" % (x)
		ai1 = player.AI_ABPruning(othello_heuristic, depth_lim = 5)
		ai1.set_child_selector(shallowest_first)
		ai2 = player.AI_ABPruning(othello_heuristic, depth_lim = 5)
		ai2.set_child_selector(shallowest_first)
		g = Othello(ai1,ai2,False, True)
		w = g.play()
		win_counts[w] += 1

	print win_counts
	for w in win_counts:
		print str(w) + "/" + str(num_games) + " : " + str(w/float(num_games))
	print


