#!/usr/bin/env python
#connect4.py
###USAGE### connect4.py
import PythonLibraries.wordops_lib as wordops_lib
import PythonLibraries.prgm_lib as prgm_lib
import re
import PythonLibraries.matrix_lib as matrix_lib
from AISuite.game import Game as Game
import AISuite.player as player

STANDARD_C4_HEIGHT = 6
STANDARD_C4_WIDTH = 7

class Connect4(Game):
	def __init__(self, player1, player2, be_quiet = False):
		super(Connect4, self).__init__(player1, player2, be_quiet)
		self.matrix = matrix_lib.init_grid(STANDARD_C4_WIDTH,STANDARD_C4_HEIGHT,' ')
		self.height = [0,0,0,0,0,0,0]
		self.rows = STANDARD_C4_HEIGHT
		self.cols = STANDARD_C4_WIDTH
		
	def opg(self):
		for y in range(self.rows):
			str1='| '
			for x in range(self.cols):
				str1=str1+str(matrix[y][x]) + ' | '
			print str1
			print '-----------------------------'
		print '  0   1   2   3   4   5   6'

	def check_winner(self):
		temp_l=[]
		for lst in matrix:
			temp_l=temp_l + lst
		p1w=wordops_lib.snake_search('XXXX',temp_l,self.cols,True,True)
		p2w=wordops_lib.snake_search('OOOO',temp_l,self.cols,True,True)
		if p1w:
			self.winner = 1
		if p2w:
			self.winner = 2
		return self.winner		

	def make_new_instance(self):
		return Connect4(player.Player(), player.Player())
				
	def get_child_moves(self):
		return [x for x in range(self.cols) if self.height[x] < self.rows]
	
	def __str__(self):
		value = ''
		for y in matrix:
			str1 = ''
			for x in matrix[y]:
				str1 += str(x)
			value += str1 + ';'
		return value + str(self.turn)

	def load_state_from_string(self, state):
		grid1 = re.split(';', state)
		self.turn = int(grid1[-1])
		grid2 = grid1[:-1]
		self.matrix = [[str(x) for x in y] for y in grid2]
		self.calculate_height()
		
	def calculate_height(self):
		for x in range(self.cols):
			self.height[x]=min([y for y in range(self.rows) if matrix[y][x]==' '])
			
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
			states += str(self)
			self.load_state_from_string(root)
		return states
		
	def do_turn(self):
		human = self.is_human_turn()
		if human:
			self.opg()
		col = -1
		finished_playing = False
		possible_moves = [str(x) for x in self.get_child_moves()]
		while not finished_playing:
			if human:
				print "Enter a number between 0 and " + str(self.cols) + " to play in that column."
			sq = self.current_player().choose_square(self)
			if sq in self.escapes:
				self.handle_escape(sq)
			if sq in possible_moves:
				self.matrix[self.height[int(sq)]][int(sq)] = self.get_player_icon(self.get_player_num())
				self.height[int(sq)] += 1
				self.turn += 1
				finished_playing = True
			else:
				if human:
					print 'Either that column is full or that wasn\'t a valid column'
		self.check_winner()
		


g = Connect4(player.Human(), player.RandomAI())
g.play()
