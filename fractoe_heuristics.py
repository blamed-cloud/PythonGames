#!/usr/bin/env python
#heuristics.py
import re
from AISuite.alphabeta import UPPER_BOUND, LOWER_BOUND

def list_product(thing):
	product = 1
	for x in thing:
		product *= x
	return product
	
def tictactoe_string_to_numbers(tic_state):
	player_map = {"X":1, " ":0, "O":-1}
	grid = []
	for j in range(3):
		row = []
		for k in range(3):
			row.append(player_map[tic_state[3*j+k]])
		grid.append(row)
	return grid

def is_board_won(state, board):
	board_str = re.split(";", state)[board]
	grid = tictactoe_string_to_numbers(board_str)
	grid_x = [[grid[j][k]+1 for k in range(3)] for j in range(3)]
	grid_o = [[abs(grid[j][k]-1) for k in range(3)] for j in range(3)]
	moves = max(tictactoe_moves_to_win(grid_x),tictactoe_moves_to_win(grid_o))
	return (moves == 8)

def tictactoe_moves_to_win(grid):	
	products_rows = [list_product(row) for row in grid]
	products_cols = [list_product([grid[row][col] for row in range(3)]) for col in range(3)]
	main_diag = grid[0][0] * grid[1][1] * grid[2][2]
	off_diag = grid[2][0] * grid[1][1] * grid[0][2]
	value = max(products_rows + products_cols + [main_diag] + [off_diag])
	return value
	
def jank_log2(num):
	power = 0
	while 2 ** power < num:
		power += 1
	return power 
	
def count_won_boards(moves_grid):
	value = 0
	for x in range(3):
		for y in range(3):
			if moves_grid[x][y]==8:
				value += 1
	return value
			
def game_length(game_state):
	turns = int(re.split(";", game_state)[-2])	#returns the number of turns of the game.
	if turns % 2 == 0:
		turns = turns * -1
	return turns
			
def is_volatile(game_state):
	value = False
	board_list = re.split(";", game_state)
	turn = int(board_list[-2])
	current_board = int(board_list[-1])
	board_list = board_list[:-2]
	if current_board == -1:
		value = True
	else:
		grid = tictactoe_string_to_numbers(board_list[current_board])
		if turn % 2 == 1:	# X player
			grid = [[grid[j][k]+1 for k in range(3)] for j in range(3)]
		else:			# O player
			grid = [[abs(grid[j][k]-1) for k in range(3)] for j in range(3)]
		moves = tictactoe_moves_to_win(grid)
		if moves == 4:
			value = True
	return value
			
def fractoe_heuristic(game_state):
	value = 0
	board_list = re.split(";", game_state)[:-2]
	big_grid_x = []
	big_grid_o = []
	for x in range(3):
		row_x = []
		row_o = []
		for y in range(3):
			grid = tictactoe_string_to_numbers(board_list[3*x + y])
			grid_x = [[grid[j][k]+1 for k in range(3)] for j in range(3)]
			grid_o = [[abs(grid[j][k]-1) for k in range(3)] for j in range(3)]
			row_x += [tictactoe_moves_to_win(grid_x)]
			row_o += [tictactoe_moves_to_win(grid_o)]
		big_grid_x += [row_x]
		big_grid_o += [row_o]
	won_boards_x = count_won_boards(big_grid_x)
	won_boards_o = count_won_boards(big_grid_o)
	board_offset = 5*(won_boards_x - won_boards_o)
	moves_till_x_wins = tictactoe_moves_to_win(big_grid_x)
	moves_till_o_wins = tictactoe_moves_to_win(big_grid_o)
	if moves_till_x_wins != 0:
		moves_x = 9 - jank_log2(moves_till_x_wins)
	else:
		moves_x = -1
	if moves_till_o_wins != 0:
		moves_o = 9 - jank_log2(moves_till_o_wins)
	else:
		moves_o = -1
	if moves_x == 0:
		value = UPPER_BOUND
	elif moves_o == 0:
		value = LOWER_BOUND
	elif moves_x == -1 and moves_o == -1:
		value = 0
	elif moves_x == -1 and moves_o != -1:
		value = LOWER_BOUND / 2 + moves_o + board_offset
	elif moves_x != -1 and moves_o == -1:
		value = UPPER_BOUND / 2 - moves_x + board_offset
	elif moves_x != -1 and moves_o != -1:
		value = moves_o - moves_x + board_offset
	return value

