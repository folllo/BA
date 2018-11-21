from math import sqrt

testPuzzle3x3 = 	[1,2,3,
		4,6,5,
		7,8,0]

testPuzzle4x4 = [1,2,3,4,
	  			5,6,7,8,
	  			15,0,11,12,
	  			13,14,9,10]

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
	if dim%2 == 1:
		#print("The puzzles Dimension is Odd")
		if(numberOfInversions%2==0):
			return True
		else:
			return False
	else:
		if(int(puzzle.index(0)/4)%2)==1:
			#print("The puzzles dimension is even and its blank is in an odd row")
			if(numberOfInversions%2==0):
				return True
			else:
				return False

		else:
			#print("The puzzles dimension is even and its blank is in an even row")
			if(numberOfInversions%2==1):
				return True
			else:
				return False




