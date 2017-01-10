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
				
	def primary_print_str(self, direction):
		value = ""
		if self.primary[direction]:
			if self.side[direction] != 0:
				value = Square.vert_or_horiz[direction]
			else:
				value = " "
		return value
		
def Squares(Game):
	def __init__(self, player1, player2, be_quiet = False, show_game = False, n_rows = 4, n_cols = 5):
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
					if sq.is_side_filled(s):
						box_str += s[0]
					else:
						box_str += ' '
				str1 += box_str + ','
		
	def load_state_from_string(self, state):
		pass
		
	def get_child_states(self):
		root = str(self)
		moves = self.get_child_moves()
		states = []
		for mv in moves:
			#update game-state
			states += [str(self)]
			self.load_state_from_string(root)
		
	def get_child_moves(self):
		moves = []
		for y in range(self.rows):
			for x in range(self.cols):
				for s in self.sides:
					if self.grid[y][x].is_side_primary(s)
						if not self.grid[y][x].is_side_used(s):
							moves += [str(y) + '-' + str(x) + s[0]]
		return moves
						

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
			mv = self.current_player().choose_square(self)
			if human and mv in self.escapes:
				self.handle_escape(sq)
			else:
				row = mv.split('-')[0]
				col = mv[:-1].split('-')[1]
				side = None
				for s in self.sides:
					if mv[-1] in s:
						side = s
						break
				col = mv[:-1].split('-')[1]
				if side != None:
					if self.is_valid_sq_pos([row,col]):
						if not self.grid[row][col].is_side_used(side):
							full = self.grid[row][col].fill_side(direction, self.get_player_num())
							if full:
								if self.check_winner() == -1:
									if human:
										self.opg()
										print "You filled a square, so go again."
								else:
									finished_playing = True
							else:
								finished_playing = True
		self.turn += 1
		self.thinking = False
			

	def make_new_instance(self):
		return Squares(player.Player(), player.Player(), n_rows = self.rows, n_cols = self.cols)
				
	def opg(self):
		for y in range(self.rows):
			top_row = "\t"
			middle_row = str(y) + "\t"
			bottom_row = "\t"
			for x in range(self.cols):
				sq = self.grid[y][x]
				top_row += "." + sq.primary_print_str("UP")
				middle_row += sq.primary_print_str("LEFT") + str(sq.get_tag()) + sq.primary_print_str("RIGHT")
				bottom_row += "." + sq.primary_print_str("DOWN")
			top_row += "."
			bottom_row += "."
			if len(top_row) == 2*self.cols + 1:
				print top_row
			print middle_row
			if len(bottom_row) == 2*self.cols + 1:
				print bottom_row
		print "="*(2*self.cols + 1)
				
	def is_valid_sq_pos(self, sq):
		return (sq[0] in range(self.rows)) and (sq[1] in range(self.cols))
		
	def check_winner(self):
		win = [0,0,0]
		for y in range(self.rows):
			for x in range(self.cols):
				tag = self.grid[y][x].get_tag()
				if tag == " ":
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
		
	
