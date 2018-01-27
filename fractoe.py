#!/usr/bin/env python
#fractoe.py
from AISuite.game import Game as Game
import AISuite.player as player
from AISuite.alphabeta import UPPER_BOUND, LOWER_BOUND, shallowest_first
import AISuite.recorder as recorder
import AISuite.PythonLibraries.prgm_lib as prgm_lib
import fractoe_tictactoe as tictactoe
Tictactoe = tictactoe.Tictactoe
from fractoe_heuristics import fractoe_heuristic

BOARD_SIZE = 3

def coor_split(num):
	col = num % BOARD_SIZE
	row = (num - col) / BOARD_SIZE
	return [row,col]
	
def coor_splice(row,col):
	return row*BOARD_SIZE + col

class Fractoe(Game):
	def __init__(self, player1, player2, be_quiet = False, show_game = False):
		super(self.__class__, self).__init__(player1, player2, be_quiet)
		self.grid = [[Tictactoe(), Tictactoe(), Tictactoe()], [Tictactoe(), Tictactoe(), Tictactoe()], [Tictactoe(), Tictactoe(), Tictactoe()]]
		self.rows = BOARD_SIZE
		self.cols = BOARD_SIZE
		self.show_board = show_game
		self.current_box = -1
		self.current_row = -1
		self.current_col = -1
		self.thinking = False
		self.boards_won = [-1,-1,-1,-1,-1,-1,-1,-1,-1]
		self.player_token = [" ","X","O"]
		self.last_moves = [ [[-1,-1],[-1,-1]], [[-1,-1], [-1,-1]] ]
		
	def load_state_from_string(self, state_string):
		class_data = state_string.split(";")
		self.boards_won = [-1,-1,-1,-1,-1,-1,-1,-1,-1]
		for num in range(9):
			col = num % 3
			row = (num - (num % 3))/3
			self.grid[row][col].load(class_data[num])
			self.boards_won[num] = self.grid[row][col].get_winner()
		self.turn = int(class_data[9])
		self.current_box = int(class_data[10])
		if self.current_box != -1:
			x = self.current_box
			self.current_col = x % 3
			self.current_row = (x - (x % 3))/3
		else:
			self.current_row = -1
			self.current_col = -1
		self.check_for_winner()

	def __str__(self):
		value = ""
		for row in range(3):
			for col in range(3):
				value += str(self.grid[row][col]) + ';'
		value += str(self.turn) + ';'
		value += str(self.current_box)
		return value
	
	@staticmethod
	def parse_state(game_state):
		split_list = game_state.split(';')
		split_list = split_list[:-2] + split_list[-1]
		return ';'.join(split_list)

	def get_child_states(self):
		root = str(self)
		moves = self.get_child_moves()
		states = []
		for m in moves:
			self.current_box = int(str(m)[0])
			self.current_col = self.current_box % 3
			self.current_row = (self.current_box - self.current_col)/3
			num = int(str(m)[1])
			self.try_placing_square(num)
			self.turn += 1
			states += [str(self)]
			self.load_state_from_string(root)
		return states
		
	def get_child_moves(self):
		children = []
		if self.current_box == -1:
			for box in range(9):
				if self.boards_won[box] == -1:
					for x in range(9):
						out_c = box % 3
						out_r = (box - out_c)/3
						in_c = x % 3
						in_r = (x - in_c)/3
						if self.grid[out_r][out_c].get_square(in_r,in_c) == " ":
							children += [str(box) + str(x)]
		else:
			for x in range(9):
					out_c = self.current_box % 3
					out_r = (self.current_box - out_c)/3
					in_c = x % 3
					in_r = (x - in_c)/3
					if self.grid[out_r][out_c].get_square(in_r,in_c) == " ":
						children += [str(self.current_box) + str(x)]
		return children

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
				if self.current_box != -1:
					print "Current board is " + str(self.current_box)
					self.grid[self.current_row][self.current_col].opg()
				print "Player" + str(self.get_player_num()) + ", it is your turn to play."
				print "Please enter a valid move string."
				print "a valid move string is two numbers, such as 34"
				print "this indicates the 4-th square on the 3-rd board (both 0-indexed)"
			move = self.current_player().choose_move(self)
			if human and move in self.escapes:
				self.handle_escape(move)
			elif str(move) in valid_moves:
				self.current_box = int(str(move)[0])
				self.current_col = self.current_box % 3
				self.current_row = (self.current_box - self.current_col)/3
				num = int(str(move)[1])
				inner_col = num % 3
				inner_row = (num - (num % 3))/3				
				turn_descriptor = [[self.current_row,self.current_col], [inner_row, inner_col]]
				self.try_placing_square(num)
				self.turn += 1
				finished_playing = True
				self.thinking = False
				self.last_moves[self.get_player_num()-1] = turn_descriptor
			else:
				if human:
					print 'That wasn\'t a valid move.'
					print 'Valid moves look like: 08 or 27'
					self.opg()
		self.check_winner()

	def make_new_instance(self):
		return Fractoe(player.Player(), player.Player())

	def opg(self):
		prgm_lib.cls(100)
		for x in range(len(self.grid)):
			size = 0
			string0 = ''
			for z in range(3):
				string1 = ''
				string2 = ''
				for y in range(len(self.grid[x])):
					special = self.get_last_moves_in(x,y,z)
					string3 = self.grid[x][y].get_row(z,special)
					for var in range(len(string3) - 9 * len(special)):
						string2 += "-"
					string1 += string3 + " || "
					string2 += " || "
				print string1[:-4]
				if z != 2:
					print string2[:-4]
				size = len(string2)-4
			for var in range(size):
				string0 += "="
			if x != 2:
				print string0
		print
		
	def check_for_winner(self):
		for x in range(3):
			if self.boards_won[3*x] == self.boards_won[3*x+1] == self.boards_won[3*x+2] > 0:
				self.winner = self.boards_won[3*x]
			if self.boards_won[x] == self.boards_won[x+3] == self.boards_won[x+6] > 0:
				self.winner = self.boards_won[x]
		if self.boards_won[0] == self.boards_won[4] == self.boards_won[8] > 0:
			self.winner = self.boards_won[4]
		if self.boards_won[2] == self.boards_won[4] == self.boards_won[6] > 0:
			self.winner = self.boards_won[4]
		if self.winner == -1 and self.check_full():
			self.winner = 0
		return self.winner
		
	def check_full(self):
		full = True
		for x in self.boards_won:
			if x == -1:
				full = False
		return full
		
	def is_board_won(self, board):
		return self.boards_won[board]
		
	def get_current_box(self):
		return self.current_box
		
	def get_board_string(self,row,col):
		return str(self.grid[row][col])
		
	def get_last_moves_in(self,x,y,z):
		special = []
		if self.last_moves[0][0][0] == x and self.last_moves[0][0][1] == y and self.last_moves[0][1][0] == z:
			special += [self.last_moves[0][1][1]]
		if self.last_moves[1][0][0] == x and self.last_moves[1][0][1] == y and self.last_moves[1][1][0] == z:
			special += [self.last_moves[1][1][1]]
		return special
		
	def try_placing_square(self, num):
		inner_col = num % 3
		inner_row = (num - (num % 3))/3
		value = False
		if self.grid[self.current_row][self.current_col].get_square(inner_row,inner_col) == " ":
			token = self.player_token[self.get_player_num()]
			self.grid[self.current_row][self.current_col].set_square(inner_row,inner_col,token)
			if self.grid[self.current_row][self.current_col].is_finished():
				box_winner = self.grid[self.current_row][self.current_col].get_winner()
				self.boards_won[self.current_box] = box_winner
				self.check_for_winner()
			if not self.grid[inner_row][inner_col].is_finished():
				self.current_box = num
				self.current_row = inner_row
				self.current_col = inner_col
			else:
				self.current_box = -1
				self.current_row = -1
				self.current_col = -1
			value = True
		return value
		
		
		
if __name__ == "__main__":	

	option = "simulate_d2_end"
	filename = "fr_game_data_d2.txt"
	num_games = 0
	win_counts = [0,0,0]	
	
	if option == "simulate_all":	
		filename = "fr_game_data_all.txt"
		num_games = 10000
		FILE = open(filename, 'a')
		for x in range(num_games):
			g = Fractoe(player.RandomAI(),player.RandomAI(),True)
			w = g.play()
			g.record_history_to_file(FILE)
			if x % 100 == 0:
				print x
			win_counts[w] += 1
		FILE.close()

	elif option == "simulate_end":
		filename = "fr_game_data.txt"
		num_games = 50000
		FILE = open(filename, 'a')
		for x in range(num_games):
			g = Fractoe(player.RandomAI(),player.RandomAI(),True)
			w = g.play()
			FILE.write(str(g) + '~' + str(w) + '\n')
			if x % 100 == 0:
				print x
			win_counts[w] += 1
		FILE.close()
	
	elif option == "simulate_d2_end":
		filename = "fr_game_data_d2.txt"
		num_games = 1000
		FILE = open(filename, 'a')
		for x in range(num_games):
			ai1 = player.AI_ABPruning(fractoe_heuristic, depth_lim = 2)
			ai1.set_child_selector(shallowest_first)
			ai2 = player.AI_ABPruning(fractoe_heuristic, depth_lim = 2)
			ai2.set_child_selector(shallowest_first)
			g = Fractoe(ai1,ai2,True)
			w = g.play()
			FILE.write(str(g) + '~' + str(w) + '\n')
			if x % 10 == 0:
				print x
			win_counts[w] += 1
		FILE.close()
	
	elif option == "human_2p":		
		g = Fractoe(player.Human(), player.Human())
		g.play()
		
	elif option == "human_1pX":
		ai = player.AI_ABPruning(fractoe_heuristic, depth_lim = 5)
		ai.set_child_selector(shallowest_first)
		g = Fractoe(player.Human(), ai)
		g.play()
		
	elif option == "human_1pO":
		ai = player.AI_ABPruning(fractoe_heuristic, depth_lim = 5)
		ai.set_child_selector(shallowest_first)
		g = Fractoe(ai, player.Human())
		g.play()
		
	elif option == "recorder_test":
		rec = recorder.Recorder(filename, BOARD_SIZE**2, BOARD_SIZE**2, ['X','O',' '])
		num_games = 5
		for x in range(num_games):
			print "Beginning game %i" % (x)
			ai1 = player.AI_ABPruning(rec.recorder_heuristic, depth_lim = 4)
			ai1.set_child_selector(shallowest_first)
			g = Fractoe(ai1, player.RandomAI(), False, True)
			w = g.play()
			win_counts[w] += 1

	elif option == "heuristic_test":
		num_games = 5
		for x in range(num_games):
			print "Beginning game %i" % (x)
			ai1 = player.AI_ABPruning(fractoe_heuristic, depth_lim = 2)
			ai1.set_child_selector(shallowest_first)
			ai2 = player.AI_ABPruning(fractoe_heuristic, depth_lim = 2)
			ai2.set_child_selector(shallowest_first)
			g = Fractoe(ai1,ai2,False, True)
			w = g.play()
			win_counts[w] += 1
		
	elif option == "vs_mode":
		rec = recorder.Recorder(filename, BOARD_SIZE**2, BOARD_SIZE**2, ['X','O',' '])
		num_games = 5
		for x in range(num_games):
			print "Beginning game %i" % (x)
			ai1 = player.AI_ABPruning(rec.recorder_heuristic, depth_lim = 5)
			ai1.set_child_selector(shallowest_first)
			ai2 = player.AI_ABPruning(fractoe_heuristic, depth_lim = 3)
			ai2.set_child_selector(shallowest_first)
			g = Fractoe(ai1,ai2,False, True)
			w = g.play()
			win_counts[w] += 1
	print win_counts
	for w in win_counts:
		print str(w) + "/" + str(num_games) + " : " + str(w/float(num_games))
	print

