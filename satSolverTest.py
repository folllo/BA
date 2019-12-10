from solver import *
import numpy as np

puzzleInstances = []
file = open("nPuzzleInstances.txt")
for line in file:
	tmp = line.rstrip()
	tmp = tmp.replace("[", '').replace("]", '')
	tmp = tmp.split(",")
	numArray = []	
	for num in tmp:
		num = int(num.rstrip())
		numArray.append(num)

	puzzleInstances.append(numArray)

file.close()



file2 = open("satTimes.txt", "w")
times = []
totalTime = 0
i=0

for state in puzzleInstances:
	i-=-1
	startTime = time.time()
	solveNPuzzle(puzzleInstances[0], 31)	
	elapsedTime = time.time()-startTime
	totalTime+=elapsedTime
	print(str(i) + ": " + str(elapsedTime))
	file2.write(str(elapsedTime))
	file2.write("\n")
	times.append(elapsedTime)

file2.close()
print("toalTime: ", totalTime)
