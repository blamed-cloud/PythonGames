#!/usr/bin/env python
#connect4.py
###USAGE### connect4.py
import random
import re
from AISuite.game import Game as Game
import AISuite.player as player
from AISuite.alphabeta import UPPER_BOUND, LOWER_BOUND, shallowest_first

class Pig(Game):
	def __init__(self, player1, player2, be_quiet = False, show_game = False):
		super(self.__class__, self).__init__(player1, player2, be_quiet)
		self.show_board = show_game
		self.scores = [0.0,0,0]
			
	def get_child_states(self):
		root = str(self)
		self.scores[self.get_player_num()] += int(self.scores[0])
		self.scores[0] = 0.0
		self.turn += 1
		hold_state = str(self)
		self.load_state_from_string(root)
		#gives expected value of rolling the die:
		self.scores[0] = (5.0 * self.scores[0] + 20.0) / 6.0
		roll_state = str(self)
		self.load_state_from_string(root)
		return [hold_state, roll_state]
		
	def get_child_moves(self):
		return ['Hold', 'Roll']
	
	def do_turn(self):
		human = self.is_human_turn()
		if not self.quiet:
			print "Turn " + str(self.turn)
		finished_playing = False
		possible_moves = self.get_child_moves()
		while not finished_playing:
			if human or self.show_board:
				self.opg()
				print "Player" + str(self.get_player_num()) + ", enter a valid move from " + str(possible_moves)
			move = self.current_player().choose_move(self)
			if human and move in self.escapes:
				self.handle_escape(move)
			if str(move) in possible_moves + ['h','H','r','R','hold','roll']:
				if 'h' in move or 'H' in move:
					self.scores[self.get_player_num()] += int(self.scores[0])
					self.scores[0] = 0.0
					self.turn += 1
					finished_playing = True
				else:
					roll = random.choice([1,2,3,4,5,6])
					if roll == 1:
						self.scores[0] = 0.0
						self.turn += 1
						finished_playing = True
					else:
						self.scores[0] += roll
			else:
				if human:
					print 'That wasn\'t a valid move.'
					self.opg()
		self.check_winner()
		

	def make_new_instance(self):
		return Pig(player.Player(), player.Player())

	def __str__(self):
		return str(self.scores[0]) + ';' + str(self.scores[1]) + ';' + str(self.scores[2]) + ';' + str(self.turn)
		
	def load_state_from_string(self, state):
		split = state.split(';')
		for x in range(3):
			try:
				self.scores[x] = int(split[x])
			except:
				self.scores[x] = float(split[x])
		self.turn = int(split[3])
		self.check_winner()
		
	def opg(self):
		print "Player1's score:    " + str(self.scores[1])
		print "Player2's score:    " + str(self.scores[2])
		print "it is currently player" + str(self.get_player_num()) + "'s turn."
		print "current turn score: " + str(self.scores[0])
		print
		
	def check_winner(self):
		if self.scores[1] >= 100:
			self.winner = 1
		elif self.scores[2] >= 100:
			self.winner = 2
		else:
			self.winner = -1
		return self.winner
		
	
def pig_heuristic(game_state):
	value = 0
	split = game_state.split(';')
	
	#check if the game is over
	if int(split[1]) == 100:
		return UPPER_BOUND
	elif int(split[2]) == 100:
		return LOWER_BOUND
		
	m = 1
	if int(split[-1]) % 2 == 1:
		m = -1
	
	value = int(split[1]) - int(split[2]) + m*int((5.0 * float(split[0]) + 20.0) / 6.0)
	
	#respect the bounds
	if value >= UPPER_BOUND:
		value = UPPER_BOUND-1
	elif value <= LOWER_BOUND:
		value = LOWER_BOUND+1
	
	return value
	
#p = Pig(player.Human(), player.Human())
#p.play()
