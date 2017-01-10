#!/usr/bin/env python
#tictactoe.py
from AISuite.PythonLibraries.prgm_lib import bcolors

class Tictactoe:
	def __init__(self):
		self.grid = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
		self.winner = " "

	def load(self, board_state):
		for num in range(9): 
			col = num % 3
			row = (num - (num % 3))/3
			self.grid[row][col] = board_state[num]
		self.winner = " "
		self.check_for_winner()
		
	def __str__(self):
		value = ""
		for row in range(3):
			for col in range(3):
				value += self.grid[row][col]
		return value
		
	def __repr__(self):
		return self.__str__()
		
	def set_square(self,row,col,player):
		self.grid[row][col] = player
		self.check_for_winner()
		
	def get_square(self,row,col):
		return self.grid[row][col]
		
	def get_row(self,row, special = [-1]): #color the special token
		string = ' '
		for y in range(len(self.grid)):
			if y not in special:
				string += self.grid[row][y] + " | "
			else:
				string += self.colored(self.grid[row][y]) + " | "

		return string[:-2]
		
	def colored(self,token):
		value = token
		if token == "X":
			value = bcolors.BLUE + token + bcolors.ENDC
		elif token == "O":
			value = bcolors.RED + token + bcolors.ENDC
		return value
		
	def check_for_winner(self):
		for x in range(len(self.grid)):
			if self.grid[x][0] == self.grid[x][1] == self.grid[x][2] != " ":
				self.winner = self.grid[x][0]
			if self.grid[0][x] == self.grid[1][x] == self.grid[2][x] != " ":
				self.winner = self.grid[0][x]
		if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] != " ":
			self.winner = self.grid[1][1]
		if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] != " ":
			self.winner = self.grid[1][1]
		if self.winner == " ":
			if self.is_full():
				self.winner = "C"
		return self.winner

	def is_full(self):
		full = True
		for row in range(3):
			for col in range(3):
				if self.grid[row][col] == " ":
					full = False
		return full

	def is_finished(self):
		return self.winner != " "

	def get_winner(self):
		value = -1
		if self.winner == "X":
			value = 1
		elif self.winner == "O":
			value = 2
		elif self.winner == "C":
			value = 0
		return value	
	
	def opg(self):
		for x in range(len(self.grid)):
			string = ' '
			for y in range(len(self.grid[x])):
				string += self.grid[x][y] + " | "
			print string[:-2]
			string2 = ''
			if x != 2:
				for var in range(len(string)-2):
					string2 += "-"
				print string2
	


