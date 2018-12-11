##################################
# 15110 Principles of Computing  #
# PA9: Mancala                   #                  
# Fall 2015                      #
##################################


# ~ Imports ~ #
import tkinter 
from tkinter import Canvas
from random import randint, seed
from time import sleep


# ~ Global Variables ~ #

BOARD_WIDTH = 360
BOARD_HEIGHT = 720
BOARD_MARGIN = 30

HOUSE_WIDTH = 135
HOUSE_HEIGHT = 60
STORE_WIDTH = 300
STORE_HEIGHT = 90
X_MARGIN = 30
Y_MARGIN = 15
HOUSE_PADDING = 10
STORE_PADDING = 15
X_COUNT_MARGIN = 15
Y_COUNT_MARGIN = 30

PEBBLE_RADIUS = 10

PLAY_MESSAGE = """
###########################
# ~ Let's play Mancala! ~ #
###########################
"""

WINDOW = tkinter.Tk()
CANVAS = Canvas(WINDOW, width=BOARD_WIDTH, height=BOARD_HEIGHT)
CANVAS.pack()

# ~ Tkinter custom circle function ~ #
def _create_circle(self, x, y, r, **kwargs):
	return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

tkinter.Canvas.create_circle = _create_circle


#########
# MODEL #
#########

# Creates a list representing a new board at the start of the game.
# @return {list} Represents the start state of the board 
def new_board(): 
	board = []
	start_pebble_count = 4
	start_store_count = 0
	for right_house in range(6):
		board.append(start_pebble_count)
	board.append(start_store_count) # Add player1 store at index 6
	for left_house in range(6):
		board.append(start_pebble_count)
	board.append(start_store_count) # Add player0 store at index 13
	return board

# Returns the moves available to the given player according to the state of
# the board. A player can only choose a house on his side of the board which
# is not empty. 
# @param board {list} Represents pebbles in each pit on board
# @param player {int} Player, can either be 0 or 1
# @return {list} Pits available for the player to pick 
def get_available_moves(board, player):
	if (player == 0): player_pits = [0, 1, 2, 10, 11, 12]
	else: player_pits = [3, 4, 5, 7, 8, 9]
	available_moves = []
	for pit in player_pits: 
		# Check that pit is not currently empty
		if (board[pit] != 0): 
			available_moves.append(pit)
	return available_moves

# Returns True if pit is a house on the player's side of the board.
# @param player {int} Player, can either be 0 or 1
# @param pit {int} Pit index to evaluate
# @return {bool} True if pit is a house on player's side of the board
def is_plyr_house(player, pit):
	if (player == 1):
		if ((3 <= pit <= 5) or (7 <= pit <= 9)):
			return True
	else:
		if ((0 <= pit <= 2) or (10 <= pit <= 12)):
			return True
	return False

# Returns False if there are no pebbles in any of the houses on the player's 
# side of the board 
# @param board {list} Mancala board model
# @param player {int} Player, can only be 0 or 1
# @return {bool} False if player has no valid move to make
def has_move(board, player):
	if (player == 0): board = board[0:3] + board[10:13]
	else: board = board[3:6] + board[7:10]
	# Loop through elements in board representing number of pebbles in each pit
	for pebbles in board: 
		# If a pit with pebbles in it is found, return True immediately
		if (pebbles != 0): 
			return True
	print("Player {} cannot move because there are no pebbles on the player's side of the board".format(player))
	return False

# Returns True if the match has ended.
# @param board {list} Board model
# @return {bool} True if match has ended
def is_end_match(board):
	for pit in range(len(board)): 
		# If the pit is a store, ignore it
		if ((pit == 6) or (pit == 13)): 
			continue
		else: 
			house = board[pit]
			if (house != 0): # Check if the house has pebbles in it
				return False
	return True

# Returns True if finished game ended in a win, False if ended in a tie
# @param board {list} Board model
# @return {bool} True if match has ended in a win
def is_win(board):
	# Assume that end_match() is True
	store0 = board[13]
	store1 = board[6]
	if (store1 > store0): 
		print("Congratulations! Player1 wins!")
		return True
	elif (store0 > store1): 
		print("Congratulations! Player0 wins!")
		return True
	else: 
		print("Great game. It's a tie!")
		return False


########
# VIEW #
########

# PROVIDED IN STARTER
# Returns drawing bounds of given pit.
# @param {int} Pit index
# @return {list} Drawing bounds of pit as [left, top, right, bottom]
def get_pit_coors(pit):
	# If pit is in right column
	# CALCULATE PIT DIMENSIONS FROM BOTTOM UP
	if (0 <= pit <= 5):
		# Left side of right column
		left = BOARD_MARGIN + HOUSE_WIDTH + X_MARGIN
		right = left + HOUSE_WIDTH
		# Bottom edge of player0 side of board, i.e. the bottom edge of the 
		# houses at the bottom of the board
		side0_baseline = BOARD_HEIGHT - (BOARD_MARGIN + STORE_HEIGHT + Y_MARGIN)
		# If pit is in bottom half (side0) of board
		if (pit <= 2): # (pits 0-2)
			bottom = side0_baseline - (HOUSE_HEIGHT * pit) - (Y_MARGIN * pit)
			top = bottom - HOUSE_HEIGHT
		# If pit is in top half (side1) of board
		else: # (pits 3-5)
			# Subtract extra Y_MARGIN to previous calculation 
			bottom = (side0_baseline - Y_MARGIN) - (HOUSE_HEIGHT * pit) - (Y_MARGIN * pit)
			top = bottom - HOUSE_HEIGHT
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
	# If pit is in left column
	# CALCULATE PIT DIMENSIONS FROM TOP DOWN
	elif (7 <= pit <= 12):
		left = BOARD_MARGIN
		right = left + HOUSE_WIDTH
		# Top edge of player1 side of board
		side1_topline = BOARD_MARGIN + STORE_HEIGHT + Y_MARGIN
		# If pit is in top half (side1) of board
		if (pit <= 9): # (pits 7-9)
			pit -= 7 # Normalize to start at 0
			top = side1_topline + (HOUSE_HEIGHT * pit) + (Y_MARGIN * pit)
			bottom = top + HOUSE_HEIGHT
		else: # (pits 10-12)
			pit -= 7 # Normalize to start at 0
			# Add extra Y_MARGIN to previous calculation
			top = (side1_topline + Y_MARGIN) + (HOUSE_HEIGHT * pit) + (Y_MARGIN * pit)
			bottom = top + HOUSE_HEIGHT
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
	# Pit is a store
	else: 
		left = BOARD_MARGIN
		right = left + STORE_WIDTH
		if (pit == 6): # Player1 store (top of board)
			top = BOARD_MARGIN
			bottom = top + STORE_HEIGHT 
		else: # Player0 store (bottom of board)
			bottom = BOARD_HEIGHT - BOARD_MARGIN
			top = bottom - STORE_HEIGHT
	return [left, top, right, bottom]
	# return {'left': left, 'top': top, 'right': right, 'bottom': bottom}

# Returns random drawing center coordinates of a pebble placed within bounds of 
# given pit.
# @param {int} Pit index
# @return {list} Random center coordinates as [center_x, center_y]
def get_pebble_coors(pit):
	pit_coors = get_pit_coors(pit) 
	# Establish bounds for x coordinate
	left_center_bound = pit_coors[0] + HOUSE_PADDING + PEBBLE_RADIUS 
	right_center_bound = pit_coors[2] - HOUSE_PADDING - PEBBLE_RADIUS
	center_x = randint(left_center_bound, right_center_bound)
	# Establish bounds for y coordinate
	top_center_bound = pit_coors[1] + HOUSE_PADDING + PEBBLE_RADIUS
	bottom_center_bound = pit_coors[3] - HOUSE_PADDING - PEBBLE_RADIUS
	center_y = randint(top_center_bound, bottom_center_bound)   
	return [center_x, center_y]


# Draws the entire board display based on the model.
# @param {list} Board model
# @param {int} Player, can only be 0 or 1
# return {None}
def display_board(board, player):
	CANVAS.delete(tkinter.ALL)
	# Draw board body
	draw_board_body(player)
	# Draw all store and house pits 
	draw_all_pits(board)
	# Draw pebble counts for each pit
	# Draw pebbles in each pit
	for pit in range(len(board)):
		draw_pebble_count(board, pit)
		seed(pit)
		pebble_count = board[pit]
		for pebble in range(pebble_count):
			pebble_coors = get_pebble_coors(pit)
			draw_pebble(pebble_coors[0], pebble_coors[1])
	sleep(0.3)
	WINDOW.update()

def draw_board_body(player):
	(width0, width1) = (0, 0)
	# if (player == 1): width1 = 4
	# if (player == 0): width0 = 4
	CANVAS.create_rectangle(4, 4, BOARD_WIDTH, BOARD_WIDTH, fill='#8A5C2E', outline='DarkRed', width=width1)
	CANVAS.create_rectangle(4, BOARD_WIDTH, BOARD_WIDTH, BOARD_HEIGHT, fill='#996633', outline='DarkRed', width=width0)

def draw_all_pits(board): 
	for pit in range(len(board)):
		pit_coors = get_pit_coors(pit) # List: [left, top, right, bottom]
		if ((pit == 6) or (pit == 13)): padding = STORE_PADDING
		else: padding = HOUSE_PADDING
		(left, top) = (pit_coors[0], pit_coors[1])
		(right, bottom) = (pit_coors[2], pit_coors[3])
		draw_pit(left, top, right, bottom, padding)

# GRAPHICAL ELEMENT DRAW FUNCTIONS      
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Draw one pit.
# @params left, top, right, bottom {int} Dimensions of pit
# @param padding {int} Width of pit padding (HOUSE_PADDING or STORE_PADDING)
# @return {None}
def draw_pit(left, top, right, bottom, padding): 
	CANVAS.create_rectangle(left, top, right, bottom, fill='#634321', width=0)
	CANVAS.create_line(left, top, left+padding, top+padding, fill='#4F361A')
	CANVAS.create_line(right, bottom, right-padding, bottom-padding, fill='#4F361A')
	CANVAS.create_line(right, top, right-padding, top+padding, fill='#4F361A')
	CANVAS.create_line(left, bottom, left+padding, bottom-padding, fill='#4F361A')
	CANVAS.create_rectangle(left, top, right, bottom, fill=None, outline='#966C43')
	CANVAS.create_rectangle(left+padding, top+padding, right-padding, bottom-padding, fill='#704B25', outline='#4F361A')

# Draw one pebble.
# @params center_x, center_y {int} Center coordinates for pebble
# return {None}
def draw_pebble(center_x, center_y):
	CANVAS.create_circle(center_x, center_y, PEBBLE_RADIUS, fill='#A01F1F', outline='DarkRed')
	CANVAS.create_circle(center_x, center_y, PEBBLE_RADIUS, fill='FireBrick', width=0)
	CANVAS.create_circle(center_x+4, center_y-4, 1.5, fill='GhostWhite', width=0)

# Draw one pebble count for pit next to pit on board.
# @param board {list} Board model
# @param pit {pit} Pit for which to draw count
# return {None}
def draw_pebble_count(board, pit):
	pit_coors = get_pit_coors(pit)
	(left, top) = (pit_coors[0], pit_coors[1])
	(right, bottom) = (pit_coors[2], pit_coors[3])
	if (pit < 7): # Pits in the right column have pebble counts drawn on right
				  # of pit
		x = right + X_COUNT_MARGIN
		y = top + Y_COUNT_MARGIN
	else: # Pits in left column have pebble counts drawn on left of pit
		x = left - X_COUNT_MARGIN
		y = top + Y_COUNT_MARGIN
	count = str(board[pit])
	CANVAS.create_text(x, y, text=count, anchor="center")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# END GRAPHICAL ELEMENT DRAW FUNCTIONS 


##############
# CONTROLLER #
##############

# TODO: Replace with click pick_pit()
def pick_pit(board, player):
	while True: 
		print("-----It is player " + str(player) + "'s turn.-----")
		valid_pits = get_available_moves(board, player)
		pit = input("Pick a pit number {} to sow pebbles: ".format(valid_pits))
		if (pit == "quit"):
			break
		else: 
			try: pit = int(pit)
			except:
				print("Please provide a valid integer.")
				continue
		if (not is_plyr_house(player, pit)):
			print("Input is not a valid pit. Pick a pit {}.".format(valid_pits))
		elif (board[pit] == 0):
			print("There are no pebbles in the pit that you have chosen. Please pick a valid pit.")
		else: 
			break
	return pit

# Given a valid pit, distribute the pebbles in pit one at a time to subsequent 
# pits taking into account the player, meaning that the function should skip 
# the opponent's store. 
# @param pit {int} Pit from which pebbles are distributed
# @param board {list} Board model 
# @param player {int} Player (0 or 1)
# @param ai_opt {bool} True if AI is on 
# @return {pit} Last pit to receive a pebble
def distr_pebbles(pit, board, player, ai_opt): 
	# Get pebbles in current pit and remove from curent pit
	pebbles = board[pit]
	board[pit] = 0
	# Get next pit to start dropping pebbles in
	next_pit = (pit + 1) % 14
	while pebbles > 0:
		pit = next_pit
		if (pit == 6):
			# This store belongs to current player, add a pebble to the store
			if (player == 1): 
				board[pit] += 1 
				pebbles -= 1
			else: next_pit = (pit + 1) % 14 # Skip this store
		elif (pit == 13): 
			if (player == 0): 
				board[pit] += 1
				pebbles -= 1
			else: next_pit = (pit + 1) % 14
		else: # Next pit is a house 
			board[pit] += 1
			pebbles -= 1
		next_pit = (pit + 1) % 14
		if (not ai_opt): 
			display_board(board, player)
	# Return the last pit to receive a pebble
	return pit

# Runs a turn for one player move.
# @param pit {int} Pit index at which to start turn (i.e. start by distributing)
#                   pebbles from this pit
# @param board {list} Board model at the start of the turn
# @param player {int} Player, can only be 0 or 1
# @param ai_opt {bool} True if AI is on for the current game
# @return {list} Board model at the end of the turn
def run_turn(pit, board, player, ai_opt):
	new_board = board[:] # Deepcopy of board
	next_pit = distr_pebbles(pit, new_board, player, ai_opt)
	# If the last pit already has pebbles in it then pick up all pebbles from 
	# that pit and continue distributing
	while ((new_board[next_pit] > 1) and (next_pit != 6) and (next_pit != 13)):
		pebbles = new_board[next_pit]
		next_pit = distr_pebbles(next_pit, new_board, player, ai_opt)
	# If next pit doesn't have any pebbles in it or is one of the stores
	return new_board

# Switches current player to opponent if opponent has move to make and returns
# new current player. 
# @param board {list} Board model
# @param player {int} Original player
# @return {int} New current player (0 or 1)
def switch_plyr(board, player):
	# Check if opponent has a move to make 
	opponent = (player + 1) % 2
	if has_move(board, opponent): 
		player = opponent
	return player

# PROVIDED IN STARTER
# Quits the game by printing feedback to user and destroying Tkinter window.
# @return {None}
def quit_game():
	print("Goodbye!")
	try: WINDOW.destroy() 
	except: return None
################################################################################
################################################################################

####################################
# Minimax: Artificial Intelligence #
####################################

def min_move_list(board): #for humans
    move_list = []
    for i in range(0, 3):
        if board[i] != 0:
            move_list.append(i)
    for i in range(10, 13):
        if board[i] != 0:
            move_list.append(i)
    return move_list

def max_move_list(board): #for ai
    move_list = []
    for i in range(3, 6):
        if board[i] != 0:
            move_list.append(i)
    for i in range(7, 10):
        if board[i] != 0:
            move_list.append(i)
    return move_list

def minimax(depth, player, board):
    # print("The player number is {}".format(player))
    # print("The depth of the tree is {}".format(depth))
    if depth > 5 or is_end_match(board):
        # print("The match ended with the result, {}".format((board[6] - board[13], None)))
        return (board[6] - board[13], None) #no next move since match ended
    if player == 1: #AI = maximizing player = 1
        bestValue = (-48, None) #min num of pebble difference
        # print("The max moves possible is {}".format(max_move_list(board)))
        max_moves = max_move_list(board)
        if max_moves == []:
            val = minimax(depth + 1, 0, board)
            if val[0] > bestValue[0]:
                bestValue = (val[0], None)
        for move in max_move_list(board): #for every possible move of AI
            val = minimax(depth + 1, 0, run_turn(move, board, 1, True))
            if val[0] > bestValue[0]:
                bestValue = (val[0], move)
        return bestValue
    else:
        bestValue = (48, None) #max num of pebble difference
        # print("The min moves possible is {}".format(min_move_list(board)))
        min_moves = min_move_list(board)
        if min_moves == []:
            val = minimax(depth + 1, 1, board)
            if val[0] < bestValue[0]:
                bestValue = (val[0], None)
        for move in min_moves: #for every possible move of human
            val = minimax(depth + 1, 1, run_turn(move, board, 0, True))
            if val[0] < bestValue[0]:
                bestValue = (val[0], move)
        return bestValue

def run_with_ai(board):
    player = 0
    while not is_end_match(board):
        if player == 0:
            move = pick_pit(board, player)
            if move == 'quit':
                break
            else:
                board = run_turn(move, board, player, False)
        elif player == 1:
            print("-----It is now the computer's turn-----")
            move = minimax(0, 1, board)[1]
            if move: #if there's a next move
                print("The computer has chosen pit number {}".format(move))
                board = run_turn(move, board, player, False)
        player = switch_plyr(board, player)
        display_board(board, player)
    if is_end_match(board):
        is_win(board)
        ans = input("Press enter to continue or type 'quit' to quit: ")
        if ans == 'quit':
            quit_game()
            return None
        else:
            run_game(True)
    else:
        quit_game()
        return None

################################################################################
################################################################################

# Starts and runs game until player quits. 
# @param ai_opt {bool} True if AI is on for this game, False for two player game
# @return {None}

def run_game(ai_opt):
	board = new_board()
	print(PLAY_MESSAGE)
	player = 0
	display_board(board, player)
	if (ai_opt): 
		run_with_ai(board)
	else: 
		while (not is_end_match(board)):
			pit = pick_pit(board, player)
			if (pit == "quit"):
				quit_game()
				return None
			else: 
				board = run_turn(pit, board, player, ai_opt) # TODO: ai_opt?
			player = switch_plyr(board, player)
			display_board(board, player)
	return None		


#######################################################################################
#######################################################################################

run_game(True)
