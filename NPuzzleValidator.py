from math import sqrt

def calcInversions(puzzle):
	invCount = 0
	arrLen = len(puzzle)
	for x in range(arrLen):
		for y in range(x+1,arrLen):
			if puzzle[x] != 0 and puzzle[y] != 0 and puzzle[x]>puzzle[y]:
				invCount += 1
	return invCount


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




