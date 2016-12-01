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

class Checkers(Game):
	escapes = [":w", ":q", ":wq", ":r", ":m"]
	
	def __init__(self, player1, player2, be_quiet = False, show_game = False):
		super(self.__class__, self).__init__(player1, player2, be_quiet)
		self.matrix = matrix_lib.init_grid(BOARD_SIZE, BOARD_SIZE, ' ')
		for y in range(len(self.matrix)):
			for x in range(len(self.matrix[y])):
				if (x + y) % 2 == 0:
					if y < 3:
						self.matrix[y][x] = 'x'
					if y > 4:
						self.matrix[y][x] = 'o'
		self.upgrade_row = {'o':0, 'x':BOARD_SIZE-1, 'X':-1, 'O':-1}
		self.upgrade_to = {'x':'X','o':'O'}
		self.rows = BOARD_SIZE
		self.cols = BOARD_SIZE
		self.show_board = show_game
		self.moves_since_capture = 0
		
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
		
	def make_new_instance(self):
		return Checkers(player.Player(), player.Player())
		
	def opg(self):
		for y in reverse(range(self.rows)):
			str1 = str(y)
			for x in range(self.cols):
				str1 = str1 + '|' + str(self.matrix[y][x])
			print str1 + '|'
		print '------------------'
		print ' |a|b|c|d|e|f|g|h|'
		
	def get_player_icons(self, p_num = -1):
		icons = [(' '), ('x', 'X'), ('o', 'O')]
		if p_num == -1:
			p_num = self.get_player_num()
		return icons[p_num]
		
	def check_winner(self):
		has_x = False
		has_o = False
		if self.moves_since_capture == 50:
			self.winner = 0
			return 0
		for row in self.matrix:
			for item in row:
				if item == 'x' or item == 'X':
					has_x = True
				if item == 'o' or item == 'O':
					has_o = True
			if has_x and has_o:
				break
		if has_x and has_o:
			if self.get_child_moves() == []:
				self.winner = (self.turn + 1 % 2) + 1 
		if has_x and not has_o:
			self.winner = 1
		if has_o and not has_x:
			self.winner = 2
		return self.winner
		
	def load_state_from_string(self, state):
		grid1 = re.split(';', state)
		self.moves_since_capture = int(grid1[-1])
		self.winner = int(grid1[-2])
		self.turn = int(grid1[-3])
		grid2 = grid1[:-3]
		self.rows = len(grid2)
		self.cols = len(grid2[0])
		self.matrix = [[str(x) for x in row] for row in grid2]
		
	def get_child_states(self):
		root = str(self)
		moves = self.get_child_moves()
		states = []
		for mv in moves:
			indices = self.parse_move(mv)
			if len(indices) == 2:
				self.moves_since_capture += 1
			else:
				self.moves_since_capture = 0
			start = indices[0]
			last = indices[-1]
			indices = indices[:-1]
			token = self.matrix[start[0]][start[1]]
			for pos in indices:
				self.matrix[pos[0]][pos[1]] = ' '
			if last[0] == self.upgrade_row[token]:
				token = self.upgrade_to[token]
			self.matrix[last[0]][last[1]] = token
			self.turn += 1
			states += [str(self)]
			self.load_state_from_string(root)
		return states	

	def get_adj_moves(self, y, x, dist = 1, icon = ' '):
		full_y = [-1*dist, dist]
		dir_dict = {' ':full_y, 'X':full_y, 'O':full_y, 'x':[dist], 'o':[-1*dist]}
		list_x = [-1*dist, dist]
		moves = []
		for off_y in dir_dict[icon]:
			for off_x in list_x:
				moves += [(y + off_y, x + off_x)]
		final_moves = []
		for m in moves:
			if m[0] in range(self.rows) and m[1] in range(self.cols):
				final_moves += [m]
		return final_moves
		
	def sq2string(self, y, x):
		num2let = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}
		return num2let[x] + str(y)

	def get_captures(self,y,x,token, invalid_sq = []):
		captures = []
		base = self.sq2string(y,x)
		away_2 = self.get_adj_moves(y,x,2,token)
		away_1 = self.get_adj_moves(y,x,1,token)
		for move in away_2:
			if self.matrix[move[0]][move[1]] == ' ':
				new_away_1 = self.get_adj_moves(move[0],move[1],1)
				for cap in away_1:
					if cap in new_away_1 and cap not in invalid_sq:
						enemy = self.matrix[cap[0]][cap[1]]
						if enemy != ' ' and enemy.upper() != token.upper():
							new_sq = self.sq2string(move[0],move[1])
							new_invalid_sq = invalid_sq + [cap]
							captures += [base + '-' + new_sq]
							new_caps = self.get_captures(move[0],move[1],token,new_invalid_sq)
							new_caps1 = [base + '-' + x for x in new_caps]
							captures += new_caps1
		return captures		

	#currently, if a piece would promote, that ends it's turn.	
	def get_child_moves(self):
		icons = self.get_player_icons()
		moves = []
		for y in range(self.rows):
			for x in range(self.cols):
				icon = self.matrix[y][x]
				if icon in icons:
					base = self.sq2string(y,x)
					for m in self.get_adj_moves(y,x,1,icon):
						if self.matrix[m[0]][m[1]] == ' ':
							mv = self.sq2string(m[0],m[1])
							moves += [base + '-' + mv]
					self.matrix[y][x] = ' '	#this avoids the edge case where a king-piece moves back to it's square.
					moves += self.get_captures(y,x,icon)
					self.matrix[y][x] = icon
		return moves		

	def get_in_between_sq(self,base,move):
		away_1_base = self.get_adj_moves(base[0],base[1],1)
		away_1_move = self.get_adj_moves(move[0],move[1],1)
		for m in away_1_base:
			if m in away_1_move:
				return m

	def parse_move(self, move):
		let2num = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
		value = []
		moves = re.split('-', move)
		for sq in moves:
			row = int(sq[1])
			col = let2num[sq[0]]
			value += [(row,col)]
		sq_list = []
		for x in range(len(value)-1):
			base = value[x]
			next = value[x+1]
			sq_list += [base]
			if next in self.get_adj_moves(base[0],base[1],2):
				sq_list += [self.get_in_between_sq(base,next)]
		sq_list += [value[-1]]
		return sq_list
#		returns a list of tuples of indices [(y,x)]
#		that includes every square it technically moved to, in order
#		even squares of opponents pieces it hopped over.
		
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
				print "Player" + str(self.get_player_num()) + ", enter a valid checkers move"
			move = self.current_player().choose_move(self)
			if human and move in self.escapes:
				self.handle_escape(move)
			if str(move) in possible_moves:
				indices = self.parse_move(move)
				if len(indices) == 2:
					self.moves_since_capture += 1
				else:
					self.moves_since_capture = 0
				start = indices[0]
				last = indices[-1]
				indices = indices[:-1]
				token = self.matrix[start[0]][start[1]]
				for pos in indices:
					self.matrix[pos[0]][pos[1]] = ' '
				if last[0] == self.upgrade_row[token]:
					token = self.upgrade_to[token]
				self.matrix[last[0]][last[1]] = token
				self.turn += 1
				finished_playing = True
			else:
				if human:
					print 'That wasn\'t a valid move.'
					print 'valid moves look like: a3-b4 or a3-c5-a7'
					self.opg()
		self.check_winner()

	def __str__(self):
		value = ''
		for row in self.matrix:
			str1 = ''
			for x in row:
				str1 += str(x)
			value += str1 + ';'
		return value + str(self.turn) + ';' + str(self.winner) + ';' + str(self.moves_since_capture)
		
	
def checkers_heuristic(game_state):
	value = 0
	#manipulate game_state into usable data
	state_split = re.split(';', game_state)
	draw50 = int(state_split[-1])
	winner = int(state_split[-2])
	turn = int(state_split[-3])
	x_s_turn = (turn % 2) == 0
	grid = state_split[:-3]
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
	VALUE_X = lambda y: 10
	VALUE_O = lambda y: -VALUE_X(y)
	value_x = lambda y: y+1
	value_o = lambda y: 8-y
	value_dict = {'X':VALUE_X, 'O':VALUE_O, 'x':value_x, 'o':value_o}
	for y in range(len(matrix)):
		for x in range(len(matrix[y])):
			token = matrix[y][x]
			if token in value_dict:
				value += value_dict[token](y)
	#give the game a more draw-ish value the closer it is to the 50-move limit
	if value > 0:
		value = max(0,value - draw50)
	elif value < 0:
		value = min(0, value + draw50)			
	
	#respect the bounds
	if value >= UPPER_BOUND:
		value = UPPER_BOUND-1
	elif value <= LOWER_BOUND:
		value = LOWER_BOUND+1
	
	return value
				
if __name__ == "__main__":
	
	#some random games
#	num_games_random = 100
#	win_counts_random = [0,0,0]
#	for x in range(num_games_random):
#		g = Checkers(player.RandomAI(),player.RandomAI(),True)
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
		ai1 = player.AI_ABPruning(checkers_heuristic, depth_lim = 5)
		ai1.set_child_selector(shallowest_first)
		ai2 = player.AI_ABPruning(checkers_heuristic, depth_lim = 5)
		ai2.set_child_selector(shallowest_first)
		g = Checkers(ai1,ai2,False, True)
		w = g.play()
		win_counts[w] += 1

	print win_counts
	for w in win_counts:
		print str(w) + "/" + str(num_games) + " : " + str(w/float(num_games))
	print	
	
