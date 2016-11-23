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
		
	def make_new_instance(self):
		return Checkers(player.Player(), player.Player())
		
	def opg(self):
		for y in reverse(range(self.rows)):
			str1 = str(y) + '|'
			for x in range(self.cols):
				str1 = str1 + str(self.matrix[y][x])
			print str1 + '|'
		print '-----------'
		print ' |abcdefgh|'
		
	def check_winner(self):
		has_x = False
		has_o = False
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
				self.winner = 0
		if has_x and not has_o:
			self.winner = 1
		if has_o and not has_x:
			self.winner = 2
		return self.winner
	

		
	def __str__(self):
		value = ''
		for row in self.matrix:
			str1 = ''
			for x in row:
				str1 += str(x)
			value += str1 + ';'
		return value + str(self.turn)
		
	def load_state_from_string(self, state):
		grid1 = re.split(';', state)
		self.turn = int(grid1[-1])
		grid2 = grid1[:-1]
		self.rows = len(grid2)
		self.cols = len(grid2[0])
		self.matrix = [[str(x) for x in row] for row in grid2]
		
		self.check_winner()
		
	def get_child_states(self):
		root = str(self)
		moves = self.get_child_moves()
		states = []
		for mv in moves:
			indices = self.parse_move(move)
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

	#need to do this still	
	def get_child_moves(self):
		pass	
		
	#need to finish this
	def parse_move(self, move):
		let2num = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
		value = []
		moves = re.split('-', move)
		for sq in moves:	#still needs to add in-between squares
			row = int(sq[1])
			col = let2num[sq[0]]
			value += [(row,col)]
		return value
#		returns a list of tuples of indices [(y,x)]
#		that includes every square it technically moved to
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
				print + str(self.get_player_num()) + ", enter a valid checkers move"
			move = self.current_player().choose_move(self)
			if human and move in self.escapes:
				self.handle_escape(move)
			if str(move) in possible_moves:
				indices = self.parse_move(move)
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
		self.check_winner()
				
				
if __name__ == "__main__":
	g = Checkers(player.Human(), player.Human())
	g.opg()
	
	
	
