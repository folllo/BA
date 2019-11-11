from random import shuffle
from math import sqrt
from NPuzzleValidator import *
import time
import os

RUNNING=1

FINAL_STATE_4X4 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]

FINAL_STATE_3X3 = [1,2,3,4,5,6,7,8,0]

FINAL_STATE_5X5 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,0]

#prints the puzzle in a readable way
def printPuzzle(puzzle):
	dim = int(sqrt(len(puzzle)))
	tmp=0
	for x in puzzle:
		print("[", x, end="]", sep=' 'if x<10 else'')
		tmp+=1
		if tmp%dim==0:
			print('')
	print('')
# takes a puzzle and returns a shuffled puzzle
def shufflePuzzle(puzzle):
	shuffle(puzzle)

# returns the current index of the blank tile
def findBlankTile(puzzle):
	return(puzzle.index(0))

# switches the position of the blank tile with the one above it
def moveUp(puzzle):
	dim = int(sqrt(len(puzzle)))
	pos_pre_move = findBlankTile(puzzle)
	pos_post_move = pos_pre_move-dim
	if(pos_post_move>=0):
		tmp = puzzle[pos_post_move]
		puzzle[pos_post_move] = 0
		puzzle[pos_pre_move] = tmp
	else:
		print("Invalid Move")

# switches the position of the blank tile with the one below it
def moveDown(puzzle):
	dim = int(sqrt(len(puzzle)))
	pos_pre_move = findBlankTile(puzzle)
	pos_post_move = pos_pre_move+dim
	if(pos_post_move<=len(puzzle)-1):
		tmp = puzzle[pos_post_move]
		puzzle[pos_post_move] = 0
		puzzle[pos_pre_move] = tmp
	else:
		print("Invalid Move")

# switches the position of the blank tile with the one on its right
def moveRight(puzzle):
	dim = int(sqrt(len(puzzle)))
	pos_pre_move = findBlankTile(puzzle)
	pos_post_move = pos_pre_move+1
	if((pos_pre_move)%dim != dim-1):
		tmp = puzzle[pos_post_move]
		puzzle[pos_post_move] = 0
		puzzle[pos_pre_move] = tmp
	else:
		print("Invalid Move")

# switches the position of the blank tile with the one on its left
def moveLeft(puzzle):
	dim = int(sqrt(len(puzzle)))
	pos_pre_move = findBlankTile(puzzle)
	pos_post_move = pos_pre_move-1
	if((pos_pre_move)%dim != 0):
		tmp = puzzle[pos_post_move]
		puzzle[pos_post_move] = 0
		puzzle[pos_pre_move] = tmp
	else:
		print("Invalid Move")

print("----------------------------0 marks the blank Tile----------------------------------")
print("----------------------use w,a,s,d to move the blank tile----------------------------")
print("Enter a dimension(3,4,5): ")
x = input()
if(x == "3"):
	fin = FINAL_STATE_3X3.copy()
	state = FINAL_STATE_3X3.copy()
elif(x == "4"):
	fin = FINAL_STATE_4X4.copy()
	state = FINAL_STATE_4X4.copy()
elif(x == "5"):
	fin = FINAL_STATE_5X5.copy()
	state = FINAL_STATE_5X5.copy()

shufflePuzzle(state)
while(not validatePuzzle(state)):
	shufflePuzzle(state)
os.system('clear')
printPuzzle(state)
start = time.time()
move_count = 0
while(RUNNING):

	x = input()

	if(x == 'w'):
		moveUp(state)
	elif(x == 's'):
		moveDown(state)
	elif(x == 'a'):
			moveLeft(state)
	elif(x == 'd'):
			moveRight(state)
	os.system('clear')
	printPuzzle(state)
	move_count += 1
	if(state == fin):
		print("FINISHED")
		RUNNING = 0
		end = time.time()
		print("Finished in ", end-start, " Seconds within ", move_count, " moves")
