from math import sqrt
from random import shuffle
from aStarImpl import *
import numpy as np
import time

FINAL_STATE_3X3 = [1,2,3,4,5,6,7,8,0]
FINAL_STATE_4X4 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]
FINAL_STATE_5X5 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,0]

# Generates X random NPuzzle instances
def generateXNPuzzles(x, dimension):
	puzzles = []
	for x in range(0, x):
		puzzles.append(generateNpuzzle(dimension))

	return puzzles

# Generates a NPuzzle instance for the given dimension
def generateNpuzzle(dimension):
	if(dimension == 3):
		state = FINAL_STATE_3X3.copy()
	elif(dimension == 4):
		state = FINAL_STATE_4X4.copy()
	elif(dimension == 5):
		state = FINAL_STATE_5X5.copy()

	shuffle(state)
	while(not validatePuzzle(state)):
		shuffle(state)
	return state

def calcInversions(puzzle):
	invCount = 0
	arrLen = len(puzzle)
	for x in range(arrLen):
		for y in range(x+1,arrLen):
			if puzzle[x] != 0 and puzzle[y] != 0 and puzzle[x]>puzzle[y]:
				invCount += 1
	return invCount

# Checks if a puzzle configuration is valid
def validatePuzzle(puzzle):
	dim = int(sqrt(len(puzzle)))
	numberOfInversions = calcInversions(puzzle)
	#True if the dimension of the puzzle is odd and the number of inversions is even.
	if dim%2 == 1:
		if(numberOfInversions%2==0):
			return True
		else:
			return False
	#True if dimension of the puzzle is even, the blank tile is on an odd row counted from the bottom and the number of inversions is even.
	else:
		if(int(puzzle.index(0)/4)%2)==1:
			if(numberOfInversions%2==0):
				return True
			else:
				return False
		#True if dimension of the puzzle is even, the blank tile is on an even row counted from the bottom and the number of inversions is odd.
		else:
			if(numberOfInversions%2==1):
				return True
			else:
				return False

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

def convertOneDimArrayToNDimArray(array):
	return np.reshape(array, (-1, int(sqrt(len(array)))))


file = open("aStarTimes.txt", "w")
file2 = open("nPuzzleInstances.txt", "w")

states = generateXNPuzzles(1000, 3)
times = []
totalTime = 0
goalNode = Node([1,2,3,4,5,6,7,8,0], None,0,0)
i = 0
for state in states:
	i-=-1
	file2.write(str(state))
	file2.write("\n")
	startNode = Node(state, None, 0,0)
	puz = Puzzle(startNode, goalNode)
	startTime = time.time()
	sol = puz.solve()
	elapsedTime = time.time()-startTime
	totalTime+=elapsedTime
	print(str(i) + ": " + str(elapsedTime))
	file.write(str(elapsedTime))
	file.write("\n")
	times.append(elapsedTime)

file.close()
file2.close()
print("toalTime: ", totalTime)
# print(FINAL_STATE_3X3)
# B = convertOneDimArrayToNDimArray([6,3,5,1,0,7,8,2,4])
# print(B)

# npuzzles = generateXNPuzzles(1000,3)
#
# for puzzle in npuzzles:
# 	printPuzzle(puzzle)
