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

def reverse(data):
	for index in range(len(data)-1, -1, -1):
		yield data[index]

class Connect4(Game):
	def __init__(self, player1, player2, be_quiet = False):
		super(self.__class__, self).__init__(player1, player2, be_quiet)
		self.matrix = matrix_lib.init_grid(STANDARD_C4_WIDTH,STANDARD_C4_HEIGHT,' ')
		self.height = [0,0,0,0,0,0,0]
		self.rows = STANDARD_C4_HEIGHT
		self.cols = STANDARD_C4_WIDTH
		
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

	def make_new_instance(self):
		return Connect4(player.Player(), player.Player())
				
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
	state_split = re.split(';', game_state)
	turn = int(state_split[-1])
	x_s_turn = (turn % 2) == 0
	grid = state_split[:-1]
	cols = len(grid[0])
	temp_l=[]
	for lst in grid:
		temp_l = temp_l + [x for x in lst]
	x_quad = wordops_lib.snake_search('XXXX',temp_l,cols,True)
	print "x_quad = %i" % (x_quad)
	o_quad = wordops_lib.snake_search('OOOO',temp_l,cols,True)
	print "o_quad = %i" % (o_quad)
	x_triple = wordops_lib.snake_search('XXX ',temp_l,cols,True)
	print "x_triple = %i" % (x_triple)
	o_triple = wordops_lib.snake_search('OOO ',temp_l,cols,True)
	print "o_triple = %i" % (o_triple)
	if x_quad:
		value = 100
	if o_quad:
		value = -100
	if x_triple:
		if x_s_turn:
			value = 100
		else:
			value = 50
	if o_triple:
		if not x_s_turn:
			value = -100
		else:
			value = -50
	print "value = %i" % (value)
	return value


g = Connect4(player.Human(), player.Human())
g.play()

num_games = 10000

win_counts = [0,0,0]
for x in range(num_games):
	g = Connect4(player.RandomAI(), player.RandomAI(),True)
	w = g.play()
	win_counts[w] += 1

print win_counts
for w in win_counts:
	print str(w) + "/" + str(num_games) + " : " + str(w/float(num_games))
print
