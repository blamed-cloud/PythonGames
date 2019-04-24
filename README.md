# PythonGames

This repository is a collection of game engines, complete with heuristic functions, of various two-player games. It is primarily intended to test the functionality of my AISuite library, as well as to satisfy a personal interest with heursitic functions and board games.

## List of Games
* Checkers
* Connect4
* Fractoe
* Othello
* Pig (in testing)
* Squares (AKA dots and boxes)

## main.py

The primary way to use this library is to call the main.py program, which exists to play the various games. The rest of this readme will essentially be a rundown of the command-line arguments to main.py. The third line of the main.py file gives a rough run-down of the command line arguments expected by the program, which will be expanded on here. Note that [...] denotes an optional argument, <...> denotes a required argument, <'...'> denotes a required argument that must be equal to whatever is inside the quotes, and <'...'/.../'...'> denotes a choice of required exact-strings, and | denotes the choice of modes.

There are two main modes that main.py can run in: option mode or user-specified mode.

### Option Mode

This mode is currently used for collecting game data for use with the recorder functionality. This is primarily done with the -m flag.

#### [-m <'simulate_all'/'simulate_end'/'simulate_d2_end'/'rand_tests_first'/'rand_tests_second'>]

The mode flag; also can be --mode instead of -m. 

##### -m simulate_all

The option to run in a mode were several games are played with RandomAI, and the entire game is saved to the log file.

##### -m simulate_end

Similar to simulate_all, except only the end of the game is recorded (the game_state when the game is over).

##### -m simulate_d2_end

Similar to simulate_end, except instead of RandomAI, the games are played by AI_ABPruning ai with a depth limit of 2.

##### -m rand_tests_first

Used to test the RandomAI against the Random_TreeAI where Random_TreeAI goes first.

##### -m rand_tests_second

Used to test the RandomAI against the Random_TreeAI where Random_TreeAI goes second.

#### [-n \<numgames>]

The numgames flag; also can be --numgames instead of -n. here <numgames> is an integer corresponding to how many games you want to play.

E.G. -n 10

#### [-g <'Fractoe'/'Connect4'/'Checkers'/'Othello'/'Squares'/'Pig'>]

The game flag; also can be --game instead of -g. The -g is followed by the name of the game you want to play, and must be exactly equal to one of the above choices (case sensitive). Levenshtein-style error-correction update may be coming eventually.

### User-Specified Mode

This mode is for playing the game, either with humans or AI's.

#### [-n \<numgames>]

The numgames flag; also can be --numgames instead of -n. here <numgames> is an integer corresponding to how many games you want to play.

E.G. -n 10

#### [-g <'Fractoe'/'Connect4'/'Checkers'/'Othello'/'Squares'/'Pig'>]

The game flag; also can be --game instead of -g. The -g is followed by the name of the game you want to play, and must be exactly equal to one of the above choices (case sensitive). Levenshtein-style error-correction update may be coming eventually.

#### [-f \<filename>]

The filename flag; can also be --filename instead of -f. The -f is followed by the name of the file you want to read from if you are using the recorder-heuristic.

#### [-h \<num_humans>]

The humans flag; can also be --humans instead of -h. The -h is followed by an integer (usually 1 or 2) corresponding to the number of humans playing in this game.

#### [-D \<depth_lim_x>]

The DepthlimX flag; can also be --DepthlimX instead of -D. The -D is followed by an integer (usually between 2 and 5) corresponding to the depth limit for the X (first) player.

#### [-d \<depth_lim_o>]

The depthlimO flag; can also be --depthlimO instead of -d. The -d is followed by an integer (usually between 2 and 5) corresponding to the depth limit for the O (second) player.

#### [-A <'random'/'randomTree'/'heuristic'/'recorder'/'mcts'>]

The AitypeX flag; can also be --AitypeX instead of -A.

##### -A random

This specifies that the AI for the X player should be RandomAI.

##### -A randomTree

This specifies that the AI for the X player should be Random_TreeAI.

##### -A heuristic

This specifies that the AI for the X player should be AI_ABPruning, using the written heuristic.

##### -A recorder

This specifies that the AI for the X player should be AI_ABPruning, using the recorder heuristic.

##### -A mcts

This specifies that the AI for the X player should be MCTS_Player, using monte carlo tree search.

#### [-a <'random'/'randomTree'/'heuristic'/'recorder'/'mcts'>]

The aitypeO flag; can also be --aitypeO instead of -a. This flag is essentially the same as the -A flag except it is to specify the second player's AI.

#### [-t <time>]

The time flag; can also be --time instead of -t. This flag is used to set the maximum turn time for the MCTS_Player class.

#### [-s]

The show flag; can also be --show instead of -s. The presence of this flag tells the game to show the game board when it is not a humans turn.

#### [-q]

The quiet flag; can also be --quiet instead of -q. The presence of this flag supresses any output of the game.

#### [-x]

The xhuman flag; can also be --xhuman instead of -x. The presence of this flag ensures that the human will be the first player if there is only one human.

#### [-o]

The ohuman flag; can also be --ohuman instead of -o. The presence of this flag ensures that the human will be the second player if there is only one human.
