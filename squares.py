#!/usr/bin/env python
#squares.py
###USAGE### squares.py
from AISuite.game import Game as Game
import AISuite.player as player
from AISuite.alphabeta import UPPER_BOUND, LOWER_BOUND, shallowest_first

class Square(object):
	reverse_side = {"UP": "DOWN", "RIGHT": "LEFT", "DOWN": "UP", "LEFT": "RIGHT"}
	vert_or_horiz = {"UP": "_", "RIGHT": "|", "DOWN": "_", "LEFT": "|"}
	
	def __init__(self):
		self.side = {"UP": 0, "RIGHT": 0, "DOWN": 0, "LEFT": 0}
		self.primary = {"UP": True, "RIGHT": True, "DOWN": True, "LEFT": True}
		self.links = {}
		self.filled = False
		self.fill_tag = " "
		
	def check_full(self, player_tag):
		if (not self.filled) and (self.side["UP"] != 0) and (self.side["RIGHT"] != 0) and (self.side["DOWN"] != 0) and (self.side["LEFT"] != 0):
			self.filled = True
			self.fill_tag = player_tag
		return self.filled
		
	def is_full(self):
		return self.filled
		
	def is_side_used(self, direction):
		return self.side[direction] != 0
		
	def is_side_primary(self, side):
		return self.primary[side]
		
	def get_tag(self):
		return self.fill_tag
		
	def num_filled_sides(self):
		return sum(self.side.values())
		
	def link_side(self, other, direction, primary_side = True):
		if direction not in self.links:
			self.links[direction] = other
			self.primary[direction] = primary_side
			other.link_side(self,Square.reverse_side[direction], not primary_side)
			
	def is_side_empty(self, direction):
		return self.side[direction] == 0
		
	def fill_side(self, direction, player_tag):
		filled = self.filled
		if self.side[direction] == 0:
			self.side[direction] = 1
			filled = self.check_full(player_tag)
			if direction in self.links:
				self.links[direction].fill_side(Square.reverse_side[direction], player_tag)
				filled = filled or self.links[direction].is_full()
		return filled
		
	def empty_side(self, direction):
		self.filled = False
		self.fill_tag = " "
		if self.side[direction] != 0:
			self.side[direction] = 0
			if direction in self.links:
				self.links[direction].empty_side(Square.reverse_side[direction])
				
	def primary_print_str(self, direction):
		value = ""
		if self.primary[direction]:
			if self.side[direction] != 0:
				value = Square.vert_or_horiz[direction]
			else:
				value = " "
		return value
		
class Squares(Game):
	def __init__(self, player1, player2, be_quiet = False, show_game = False, n_rows = 3, n_cols = 4):
		super(self.__class__, self).__init__(player1, player2, be_quiet)
		self.grid = []
		# create empty squares
		for y in range(n_rows):
			row = []
			for x in range(n_cols):
				row += [Square()]
			self.grid += [row]
		# perform linking
		#### consider implimeting back-linking ####
		for y in range(n_rows):
			for x in range(n_cols):
				if x != n_cols - 1:
					self.grid[y][x].link_side(self.grid[y][x+1],"RIGHT")
				if y != n_rows - 1:
					self.grid[y][x].link_side(self.grid[y+1][x],"DOWN")
		self.sides = ["UP","RIGHT","DOWN","LEFT"]
		self.thinking = False
		self.show_board = show_game
		self.rows = n_rows
		self.cols = n_cols

	def __str__(self):
		value = ''
		for row in self.grid:
			str1 = ''
			for sq in row:
				box_str = ''
				for s in self.sides:
					if sq.is_side_used(s):
						box_str += s[0]
					else:
						box_str += ' '
				str1 += box_str + str(sq.get_tag()) + ','
			str1 = str1[:-1] #remove trailing comma
			value += str1 + ';'
		value += str(self.turn) + ';' + str(self.winner)
		return value
		
	def load_state_from_string(self, state):
		new_state = state.split(';')
		self.winner = int(new_state[-1])
		self.turn = int(new_state[-2])
		sq_data = new_state[:-2]
		data = [x.split(',') for x in sq_data]
		for y in range(self.rows):
			for x in range(self.cols):
				str1 = data[y][x]
				tag = str1[-1]
				str1 = str1[:-1]
				for s in self.sides:
					if s[0] in str1:
						self.grid[y][x].fill_side(s,tag)
					else:
						self.grid[y][x].empty_side(s)
		
	def get_child_states(self):
		root = str(self)
		moves = self.get_child_moves()
		states = []
		for mv in moves:
			for x in mv.split(','):
				self.update_state(*self.move_str2list(x))
			self.check_winner()
			self.turn += 1
			states += [str(self)]
			self.load_state_from_string(root)
		return states
		
	def get_child_moves(self):
		moves = []
		for y in range(self.rows):
			for x in range(self.cols):
				for s in self.sides:
					if self.grid[y][x].is_side_primary(s):
						if not self.grid[y][x].is_side_used(s):
							mv_str = str(y) + '-' + str(x) + s[0]
							full = self.update_state(y,x,s)
							if full and self.check_winner() == -1:
								new_moves = self.get_child_moves()
								for mv in new_moves:
									moves += [mv_str + ',' + mv]
							else:
								moves += [mv_str]
							self.grid[y][x].empty_side(s)
		return moves
		
	def update_state(self, row, col, side):
		fill = False
		if self.is_valid_sq_pos([row,col]):
			if not self.grid[row][col].is_side_used(side):
				fill = self.grid[row][col].fill_side(side, self.get_player_num())
		return fill
		
	def move_str2list(self, mv):
		row = mv.split('-')[0]
		col = mv[:-1].split('-')[1]
		side = None
		for s in self.sides:
			if mv[-1] in s:
				side = s
				break
		return [int(row),int(col),side]			

	def do_turn(self):
		human = self.is_human_turn()
		if human or self.show_board:
			self.opg()
		mv = ''
		finished_playing = False
		while not finished_playing:
			if human:
				print "Player" + str(self.get_player_num()) + " it is your turn."
				print "please give a valid move."
				print "a valid move looks like r-cS"
				print "where r is the row number (0-indexed)"
				print "c is the column number (0-indexed)"
				print "and S is one of U/D/L/R, for the side of the square."
			mv = self.current_player().choose_move(self)
			if human and mv in self.escapes:
				self.handle_escape(mv)
			else:
				for x in mv.split(','):
					tup = self.move_str2list(x)
					if tup[2] != None:
						full = self.update_state(*tup)
						if full and self.check_winner() == -1:
							if human:
								self.opg()
								print "You filled a square, so go again."
						else:
							finished_playing = True
							break
		self.turn += 1
		self.thinking = False
			

	def make_new_instance(self):
		return Squares(player.Player(), player.Player(), n_rows = self.rows, n_cols = self.cols)
				
	def opg(self):
		for y in range(self.rows):
			top_row = ' '*len(str(y))
			middle_row = str(y)
			bottom_row = ' '*len(str(y))
			for x in range(self.cols):
				sq = self.grid[y][x]
				top_row += "." + sq.primary_print_str("UP")
				middle_row += sq.primary_print_str("LEFT") + str(sq.get_tag()) + sq.primary_print_str("RIGHT")
				bottom_row += "." + sq.primary_print_str("DOWN")
			top_row += "."
			bottom_row += "."
			if len(top_row) >= 2*self.cols + 1:
				print top_row
			print middle_row
			if len(bottom_row) >= 2*self.cols + 1:
				print bottom_row
		print "="*max(len(top_row), len(middle_row), len(bottom_row))
				
	def is_valid_sq_pos(self, sq):
		return (sq[0] in range(self.rows)) and (sq[1] in range(self.cols))
		
	def check_winner(self):
		win = [0,0,0]
		for y in range(self.rows):
			for x in range(self.cols):
				tag = self.grid[y][x].get_tag()
				if tag == " ":
					self.winner = -1
					return -1
				elif str(tag) == "1":
					win[1] += 1
				elif str(tag) == "2":
					win[2] += 1
		if win[1] > win[2]:
			self.winner = 1
		elif win[1] == win[2]:
			self.winner = 0
		elif win[2] > win[1]:
			self.winner = 2
		return self.winner


def squares_heuristic(game_state):
	value = 0
	#manipulate game_state into usable data
	state_split = game_state.split(';')
	winner = int(state_split[-1])
	turn = int(state_split[-2])
	matrix = [x.split(',') for x in state_split[:-2]]
	#check if the game is over
	if winner == 1:
		return UPPER_BOUND
	elif winner == 2:
		return LOWER_BOUND
	elif winner == 0:
		return 0
	#do some calculations that probably take too long
	for row in matrix:
		for sq in row:
			if sq[-1] == "1":
				value += 1
			elif sq[-1] == "2":
				value -= 1
	#respect the bounds
	if value >= UPPER_BOUND:
		value = UPPER_BOUND-1
	elif value <= LOWER_BOUND:
		value = LOWER_BOUND+1
	
	return value
	
if __name__ == "__main__":	

	option = "heuristic_test"
	filename = "sq_game_data_d2.txt"
	num_games = 0
	win_counts = [0,0,0]	
	
	if option == "functionality_test":
		num_games = 1000
		for x in range(num_games):
			g = Squares(player.RandomAI(),player.RandomAI(),True, n_rows = 5, n_cols = 5)
			w = g.play()
			win_counts[w] += 1
			if x % 10 == 0:
				print x
	
	if option == "simulate_all":	
		filename = "sq_game_data_all.txt"
		num_games = 10000
		FILE = open(filename, 'a')
		for x in range(num_games):
			g = Squares(player.RandomAI(),player.RandomAI(),True)
			w = g.play()
			g.record_history_to_file(FILE)
			if x % 100 == 0:
				print x
			win_counts[w] += 1
		FILE.close()

	elif option == "simulate_end":
		filename = "sq_game_data.txt"
		num_games = 50000
		FILE = open(filename, 'a')
		for x in range(num_games):
			g = Squares(player.RandomAI(),player.RandomAI(),True)
			w = g.play()
			FILE.write(str(g) + '~' + str(w) + '\n')
			if x % 100 == 0:
				print x
			win_counts[w] += 1
		FILE.close()
	
	elif option == "simulate_d2_end":
		filename = "sq_game_data_d2.txt"
		num_games = 1000
		FILE = open(filename, 'a')
		for x in range(num_games):
			ai1 = player.AI_ABPruning(squares_heuristic, depth_lim = 2)
			ai1.set_child_selector(shallowest_first)
			ai2 = player.AI_ABPruning(squares_heuristic, depth_lim = 2)
			ai2.set_child_selector(shallowest_first)
			g = Squares(ai1,ai2,True)
			w = g.play()
			FILE.write(str(g) + '~' + str(w) + '\n')
			if x % 10 == 0:
				print x
			win_counts[w] += 1
		FILE.close()
	
	elif option == "human_2p":		
		g = Squares(player.Human(), player.Human())
		g.play()
		
	elif option == "human_1pX":
		ai = player.AI_ABPruning(squares_heuristic, depth_lim = 5)
		ai.set_child_selector(shallowest_first)
		g = Squares(player.Human(), ai)
		g.play()
		
	elif option == "human_1pO":
		ai = player.AI_ABPruning(squares_heuristic, depth_lim = 5)
		ai.set_child_selector(shallowest_first)
		g = Squares(ai, player.Human())
		g.play()
		
#	elif option == "recorder_test":
#		rec = recorder.Recorder(filename, BOARD_SIZE**2, BOARD_SIZE**2, ['X','O',' '])
#		num_games = 5
#		for x in range(num_games):
#			print "Beginning game %i" % (x)
#			ai1 = player.AI_ABPruning(rec.recorder_heuristic, depth_lim = 4)
#			ai1.set_child_selector(shallowest_first)
#			g = Fractoe(ai1, player.RandomAI(), False, True)
#			w = g.play()
#			win_counts[w] += 1

	elif option == "heuristic_test":
		num_games = 5
		for x in range(num_games):
			print "Beginning game %i" % (x)
			ai1 = player.AI_ABPruning(squares_heuristic, depth_lim = 2)
			ai1.set_child_selector(shallowest_first)
			ai2 = player.AI_ABPruning(squares_heuristic, depth_lim = 2)
			ai2.set_child_selector(shallowest_first)
			g = Squares(ai1,ai2,False, True)
			w = g.play()
			win_counts[w] += 1
		
#	elif option == "vs_mode":
#		rec = recorder.Recorder(filename, BOARD_SIZE**2, BOARD_SIZE**2, ['X','O',' '])
#		num_games = 5
#		for x in range(num_games):
#			print "Beginning game %i" % (x)
#			ai1 = player.AI_ABPruning(rec.recorder_heuristic, depth_lim = 5)
#			ai1.set_child_selector(shallowest_first)
#			ai2 = player.AI_ABPruning(fractoe_heuristic, depth_lim = 3)
#			ai2.set_child_selector(shallowest_first)
#			g = Fractoe(ai1,ai2,False, True)
#			w = g.play()
#			win_counts[w] += 1
	print win_counts
	for w in win_counts:
		print str(w) + "/" + str(num_games) + " : " + str(w/float(num_games))
	print

