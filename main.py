#!/usr/bin/env python
#main.py
###USAGE### main.py [-m <'simulate_all'/'simulate_end'/'simulate_d2_end'/'rand_tests_first'/'rand_tests_second'>] [-n <numgames>] [-g <'Fractoe'/'Connect4'/'Checkers'/'Othello'/'Squares'/'Pig'/'Pentago'>] | [-n <numgames>] [-f <filename>] [-h <num_humans>] [-g <'Fractoe'/'Connect4'/'Checkers'/'Othello'/'Squares'/'Pig'/'Pentago'>] [-D <depth_lim_x>] [-d <depth_lim_o>] [-A <'random'/'randomTree'/'heuristic'/'recorder'/'mcts'>] [-a <'random'/'randomTree'/'heuristic'/'recorder'/'mcts'>] [-t <time>] [-s] [-q] [-x] [-o] ; sms=N ; $#=0-13
import AISuite.PythonLibraries.prgm_lib as prgm_lib
import sys
import AISuite.player as player
import AISuite.recorder as recorder
import random
from fractoe import Fractoe
from fractoe_heuristics import fractoe_heuristic
from pentago import Pentago, pentago_heuristic
from checkers import Checkers, checkers_heuristic
from connect4 import Connect4, connect4_heuristic
from othello import Othello, othello_heuristic
from squares import Squares, squares_heuristic
from pig import Pig, pig_heuristic
from AISuite.alphabeta import shallowest_first

re_mk = prgm_lib.flag_re_mk

arg_dict = {}
arg_dict[re_mk('mode')] = 1
arg_dict[re_mk('numgames')] = 1
arg_dict[re_mk('file')] = 1
arg_dict[re_mk('humans')] = 1
arg_dict[re_mk('game')] = 1
arg_dict[re_mk('DepthlimX')] = 1
arg_dict[re_mk('depthlimO')] = 1
arg_dict[re_mk('AitypeX')] = 1
arg_dict[re_mk('aitypeO')] = 1
arg_dict[re_mk('time')] = 1
arg_dict[re_mk('show')] = 0
arg_dict[re_mk('quiet')] = 0
arg_dict[re_mk('xhuman')] = 0
arg_dict[re_mk('ohuman')] = 0

flag_argc = [1,1,1,1,1,1,1,1,1,1,0,0,0,0]
flags = [re_mk('mode'), re_mk('numgames'), re_mk('file'), re_mk('humans'), re_mk('game'), re_mk('DepthlimX'), re_mk('depthlimO'), re_mk('AitypeX'), re_mk('aitypeO'), re_mk('time'), re_mk('show'), re_mk('quiet'), re_mk('xhuman'), re_mk('ohuman')]

o_args = prgm_lib.arg_flag_ordering(sys.argv, flag_argc, flags)

option = "None"
num_games = 1
filename = "default"
humans = 0
game = "Fractoe"
depth_x = 4
depth_o = 4
ai_x = "random"
ai_o = "random"
time = 30
show = False
quiet = False
xhuman = False
ohuman = False

if str(o_args[0]) != "None":
	option = str(o_args[0])

if str(o_args[1]) != "None":
	num_games = int(o_args[1])

if str(o_args[2]) != "None":
	filename = str(o_args[2])

if str(o_args[3]) != "None":
	humans = int(o_args[3])

if str(o_args[4]) != "None":
	game = str(o_args[4])

if str(o_args[5]) != "None":
	depth_x = int(o_args[5])

if str(o_args[6]) != "None":
	depth_o = int(o_args[6])

if str(o_args[7]) != "None":
	ai_x = str(o_args[7])

if str(o_args[8]) != "None":
	ai_o = str(o_args[8])
	print ai_o

if str(o_args[9]) != "None":
	time = int(o_args[9])

if str(o_args[10]) != "None":
	show = True

if str(o_args[11]) != "None":
	quiet = True

if str(o_args[12]) != "None":
	xhuman = True

if str(o_args[13]) != "None":
	ohuman = True

can_recorder = True
G = Fractoe
heuristic = fractoe_heuristic
tiles = ['X', 'O', ' ']
rec_board_height = 9
rec_board_height = 9
prefix = "fr_"
if game == "Fractoe":
	pass
elif game == "Connect4":
	G = Connect4
	heuristic = connect4_heuristic
	from connect4 import STANDARD_C4_HEIGHT as rec_board_height
	from connect4 import STANDARD_C4_WIDTH as rec_board_width
	prefix = "c4_"
elif game == "Checkers":
	G = Checkers
	heuristic = checkers_heuristic
	from checkers import BOARD_SIZE as rec_board_height
	rec_board_width = rec_board_height
	tiles = ['X', 'x', 'O', 'o', ' ']
	prefix = "ch_"
elif game == "Othello":
	G = Othello
	heuristic = othello_heuristic
	from othello import BOARD_SIZE as rec_board_height
	rec_board_width = rec_board_height
	prefix = "ot_"
elif game == "Squares":
	G = Squares
	heuristic = squares_heuristic
	prefix = "sq_"
	can_recorder = False
elif game == "Pig":
	G = Pig
	heuristic = pig_heuristic
	prefix = "pg_"
	can_recorder = False
elif game == "Pentago":
	G = Pentago
	heuristic = pentago_heuristic
	from pentago import BOARD_SIZE as rec_board_height
	rec_board_width = rec_board_height
	prefix = "pt_"

if filename == "default":
	filename = prefix + "game_data.txt"

player1 = player.RandomAI()
player2 = player.RandomAI()
rec = None

if not can_recorder and (ai_x == "recorder" or ai_o == "recorder"):
	print "Sorry, the game you chose is not set up to allow recorder ai."
	raise SystemExit

if ai_x == "random":
	pass
elif ai_x == "randomTree":
	player1 = player.Random_TreeAI(depth_lim = depth_x)
elif ai_x == "heuristic":
	player1 = player.AI_ABPruning(heuristic, depth_lim = depth_x)
#	player1.set_child_selector(shallowest_first, shallowest_first.sel)
elif ai_x == "recorder":
	rec = recorder.Recorder(filename, rec_board_height, rec_board_width, tiles)
	player1 = player.AI_ABPruning(rec.recorder_heuristic, depth_lim = depth_x)
#	player1.set_child_selector(shallowest_first)
elif ai_x == "mcts":
	player1 = player.MCTS_Player(turnTime = time)

if ai_o == "random":
	pass
elif ai_o == "randomTree":
	player2 = player.Random_TreeAI(depth_lim = depth_o)
elif ai_o == "heuristic":
	player2 = player.AI_ABPruning(heuristic, depth_lim = depth_o)
#	player2.set_child_selector(shallowest_first)
elif ai_o == "recorder":
	if rec == None:
		rec = recorder.Recorder(filename, rec_board_height, rec_board_width, tiles)
	player2 = player.AI_ABPruning(rec.recorder_heuristic, depth_lim = depth_o)
#	player2.set_child_selector(shallowest_first)
elif ai_o == "mcts":
	player2 = player.MCTS_Player(turnTime = time)

if humans == 1:
	if xhuman:
		player1 = player.Human()
	else:
		if ohuman:
			player2 = player.Human()
		else:
			choice = random.choice(["X","O"])
			if choice == "X":
				player1 = player.Human()
			else:
				player2 = player.Human()
elif humans == 2:
	player1 = player.Human()
	player2 = player.Human()

win_counts = [0,0,0]
total_turns = 0

if option == "simulate_all":
	filename = prefix + "game_data_all.txt"
	FILE = open(filename, 'a')
	for x in range(num_games):
		g = G(player.RandomAI(),player.RandomAI(),True)
		w = g.play()
		g.record_history_to_file(FILE)
		if x % 100 == 0:
			print x
		win_counts[w] += 1
		total_turns += g.get_turn()
	FILE.close()
elif option == "simulate_end":
	filename = prefix + "game_data.txt"
	FILE = open(filename, 'a')
	for x in range(num_games):
		g = G(player.RandomAI(),player.RandomAI(),True)
		w = g.play()
		FILE.write(str(g) + '~' + str(w) + '\n')
		if x % 100 == 0:
			print x
		win_counts[w] += 1
		total_turns += g.get_turn()
	FILE.close()
elif option == "simulate_d2_end":
	filename = prefix + "game_data_d2.txt"
	FILE = open(filename, 'a')
	for x in range(num_games):
		ai1 = player.AI_ABPruning(heuristic, depth_lim = 2)
		ai1.set_child_selector(shallowest_first)
		ai2 = player.AI_ABPruning(heuristic, depth_lim = 2)
		ai2.set_child_selector(shallowest_first)
		g = G(ai1,ai2,True)
		w = g.play()
		FILE.write(str(g) + '~' + str(w) + '\n')
		if x % 10 == 0:
			print x
		win_counts[w] += 1
		total_turns += g.get_turn()
	FILE.close()
elif option == "rand_tests_first":
	print "Testing Random tree going first against random"
	for x in range(num_games):
		print "Beginning game %i" % (x)
		ai1 = player.Random_TreeAI(depth_x)
		ai2 = player.RandomAI()
		g = G(ai1, ai2, quiet, show)
		w = g.play()
		win_counts[w] += 1
		total_turns += g.get_turn()
elif option == "rand_tests_second":
	print "Testing Random tree going second against random"
	for x in range(num_games):
		print "Beginning game %i" % (x)
		ai1 = player.Random_TreeAI(depth_o)
		ai2 = player.RandomAI()
		g = G(ai2, ai1, quiet, show)
		w = g.play()
		win_counts[w] += 1
		total_turns += g.get_turn()
else:
	for x in range(num_games):
		if not quiet:
			print "Beginning game %i" % (x)
		g = G(player1,player2, quiet, show)
		w = g.play()
		player1.reset()
		player2.reset()
		win_counts[w] += 1
		total_turns += g.get_turn()

print win_counts
for w in win_counts:
	print str(w) + "/" + str(num_games) + " : " + str(w/float(num_games))
print
print "Total # turns: " + str(total_turns)
print "Avg # turns:   " + str(total_turns/float(num_games))
print
