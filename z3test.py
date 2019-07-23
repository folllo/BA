from z3 import *
import math
import time
import re

# Solvable test state
state = [6,3,5,1,0,7,8,2,4]
finalState = [1,2,3,4,5,6,7,8,0]

testState = [ Int("x_1_%s" % (i)) for i in range(9)]
testState_2 = [ Int("x_2_%s" % (i)) for i in range(9)]
testState4x4 = [ Int("x_1_%s" % (i)) for i in range(16) ]
testState4x4_2 = [ Int("x_2_%s" % (i)) for i in range(16) ]

s = Solver()

# generates a matrix of z3 states e.g. "x_1_0", ..., "x_1_9" with the number of states equal to the number of steps wanted
def generateStateMatrix(stateSize, numOfSteps):
 return [[ Int("x_%s_%s" % (i+1, j)) for j in range(stateSize)] for i in range(numOfSteps)]

# utility function to prettyprint a state Matrix
def printStateMatrix(stateMatrix):
    for val in stateMatrix:
        print(val)

# Converts a python State array into a z3 state array with the format "x_index_0", ... , "x_index_len(state)"
def stateToZ3State(state, index):
    z3State = [ Int("x_%s_%s" % (index, i)) for i in range(9)]
    tmp = True;
    for i in range(len(z3State)):
        tmp = And(tmp,(z3State[i] == state[i]))
    return simplify(tmp)

# Validates if a state has Distinct values and Values are >= 0
def isState(state):
    tmp = Distinct(state);
    for val in state:
        tmp = And(tmp, (val >= 0))
    return simplify(tmp)

# Validates if a State is the final State
def isFinalStateFormula(state):
    tmp = True
    for i in range(len(state)-1):
        tmp = And(tmp, (state[i] == i+1))
    return simplify(And(tmp, state[len(state)-1] == 0))

# generates isState formula for a given stateMatrix
def isStateMatrix(stateMatrix):
    tmp = True;
    for val in stateMatrix:
        tmp = And(tmp, isState(val))
    return simplify(tmp)

# generates possible Transitions from state1 to state2 for the top left corner of a given puzzle
#
#   |x|_|_|
#   |_|_|_|     x = empty tile
#   |_|_|_|
#
def topLeftTransitions(state1, state2, dim):
    # case1 equals shifting the empty tile to the right
    case1 = switchTiles(state1, state2, 0, 1)
    # case2 equals shifting the empty tile down
    case2 = switchTiles(state1, state2, 0, dim)
    return simplify(And(Or(case1,case2), (state1[0] == 0)))


# generates possible Transitions from state1 to state2 for the top right corner of a given puzzle
#
#   |_|_|x|
#   |_|_|_|     x = empty tile
#   |_|_|_|
#
def topRightTransitions(state1, state2, dim):
    # case1 equals shifting the empty tile to the left
    case1 = switchTiles(state1, state2, dim-1, dim-2)
    # case2 equals shifting the empty tile down
    case2 = switchTiles(state1, state2, dim-1, 2*dim-1)
    return simplify(And(Or(case1,case2), (state1[dim-1] == 0)))

# generates possible Transitions from state1 to state2 for the bottom left corner of a given puzzle
#
#   |_|_|_|
#   |_|_|_|     x = empty tile
#   |x|_|_|
#
def bottomLeftTransitions(state1, state2, dim):
    # case1 equals shifting the empty tile to the right
    case1 = switchTiles(state1, state2, dim*(dim-1), dim*(dim-1)+1)
    # case2 equals shifting the empty tile up
    case2 = switchTiles(state1, state2, dim*(dim-1), dim*(dim-2))
    return simplify(And(Or(case1,case2),(state1[dim*(dim-1)] == 0)))

# generates possible Transitions from state1 to state2 for the bottom right corner of a given puzzle
#
#   |_|_|_|
#   |_|_|_|     x = empty tile
#   |_|_|x|
#
def bottomRightTransitions(state1, state2, dim):
    # case1 equals shifting the empty tile to the left
    case1 = switchTiles(state1, state2, dim*dim-1, dim*dim-2)
    # case2 equals shifting the empty tile up
    case2 = switchTiles(state1, state2, dim*dim-1, dim*(dim-1)-1)
    return simplify(And(Or(case1,case2), (state1[dim*dim-1] == 0)))

# generates possible Transitions from state1 to state2 for the top row of a given puzzle
#
#   |_|x|x|_|
#   |_|_|_|_|     x = possible empty tile positions
#   |_|_|_|_|
#   |_|_|_|_|
#
def topRowTransitions(state1, state2, dim):
    tmp = False
    for i in range(dim-2):
        # case1 equals shifting the empty tile to the left
        case1 = switchTiles(state1, state2, i+1, i)
        # case1 equals shifting the empty tile to the right
        case2 = switchTiles(state1, state2, i+1, i+2)
        # case1 equals shifting the empty tile down
        case3 = switchTiles(state1, state2, i+1, i+dim+1)
        tmp = And(Or(tmp, case1 , case2, case3), (state1[i+1] == 0))
    return simplify(tmp)

# generates possible Transitions from state1 to state2 for the right column of a given puzzle
#
#   |_|_|_|_|
#   |_|_|_|x|     x = possible empty tile positions
#   |_|_|_|x|
#   |_|_|_|_|
#
def rightColumnTransitions(state1, state2, dim):
    tmp = False
    for i in range(dim-2):
        # case1 equals shifting the empty tile up
        case1 = switchTiles(state1, state2, (i+2)*dim-1, (i+1)*dim-1)
        # case1 equals shifting the empty tile down
        case2 = switchTiles(state1, state2, (i+2)*dim-1, (i+3)*dim-1)
        # case1 equals shifting the empty tile to the left
        case3 = switchTiles(state1, state2, (i+2)*dim-1, (i+2)*dim-2)
        tmp = And(Or(tmp, case1 , case2, case3), (state1[(i+2)*dim-1] == 0))
    return simplify(tmp)

# generates possible Transitions from state1 to state2 for the bottom row of a given puzzle
#
#   |_|_|_|_|
#   |_|_|_|_|     x = possible empty tile positions
#   |_|_|_|_|
#   |_|x|x|_|
#
def bottomRowTransitions(state1, state2, dim):
    tmp = False
    for i in range(dim-2):
        # case1 equals shifting the empty tile to the right
        case1 = switchTiles(state1, state2, dim*(dim-1)+i+1, dim*(dim-1)+i+2)
        # case1 equals shifting the empty tile to the left
        case2 = switchTiles(state1, state2, dim*(dim-1)+i+1, dim*(dim-1)+i)
        # case1 equals shifting the empty tile up
        case3 = switchTiles(state1, state2, dim*(dim-1)+i+1, dim*(dim-2)+i+1)
        tmp = And(Or(tmp, case1 , case2, case3), (state1[dim*(dim-1)+i+1] == 0))
    return simplify(tmp)

# generates possible Transitions from state1 to state2 for the left column of a given puzzle
#
#   |_|_|_|_|
#   |x|_|_|_|     x = possible empty tile positions
#   |x|_|_|_|
#   |_|_|_|_|
#

def leftColumnTransitions(state1, state2, dim):
    tmp = False
    for i in range(dim-2):
        # case1 equals shifting the empty tile up
        case1 = switchTiles(state1, state2, (i+1)*dim, i*dim)
        # case2 equals shifting the empty tile down
        case2 = switchTiles(state1, state2, (i+1)*dim, (i+2)*dim)
        # case3 equals shifting the empty tile to the right
        case3 = switchTiles(state1, state2, (i+1)*dim, (i+1)*dim+1)
        tmp = And(Or(tmp, case1 , case2, case3), (state1[(i+1)*dim] == 0))
    return simplify(tmp)

# generates possible Transitions from state1 to state2 for tiles filling the middle of a given puzzle
#
#   |_|_|_|_|
#   |_|x|x|_|     x = possible empty tile positions
#   |_|x|x|_|
#   |_|_|_|_|
#
def fillerTransitions(state1, state2, dim):
    tmp = False
    for i in range(1,dim-1):
        for j in range(1, dim-1):
            # case1 equals shifting the empty tile up
            case1 = switchTiles(state1, state2, j+dim*i, j+dim*(i-1));
            # case2 equals shifting the empty tile to the right
            case2 = switchTiles(state1, state2, j+dim*i, j+dim*i+1);
            # case3 equals shifting the empty tile down
            case3 = switchTiles(state1, state2, j+dim*i, j+dim*(i+1));
            # case4 equals shifting the empty tile to the left
            case4 = switchTiles(state1, state2, j+dim*i, j+dim*i-1);
            tmp = And(Or(tmp, case1, case2, case3, case4), (state1[j+dim*i] == 0))
    return simplify(tmp)

def switchTiles(state1, state2, pos1, pos2):
    tmp = And((state1[pos1] == state2[pos2]),(state1[pos2] == state2[pos1]));
    for i in range(len(state1)):
        if i != pos1 and i != pos2:
            tmp = And(tmp, state1[i] == state2[i])
    return tmp

def isEqualState(state1, state2):
    tmp = True
    for i in range(len(state)):
        tmp = And(tmp, (state1[i] == state2[i]))
    return simplify(tmp)

# combines all transition functions to get one big formula
def combineTransitions(state1, state2, dim):
    cornerTransitions = Or(topLeftTransitions(state1, state2, dim), topRightTransitions(state1, state2, dim), bottomLeftTransitions(state1, state2, dim), bottomRightTransitions(state1, state2, dim))
    sideTransitions = Or(topRowTransitions(state1, state2, dim), rightColumnTransitions(state1, state2, dim), bottomRowTransitions(state1, state2, dim), leftColumnTransitions(state1, state2, dim))
    return simplify(Or(cornerTransitions, sideTransitions, fillerTransitions(state1, state2, dim)))

def getFormula(startingstate, steps):
    dim = int(math.sqrt(len(startingstate)))
    stateMatrix = generateStateMatrix(dim*dim, steps+1);
    tmp = stateToZ3State(startingstate, 1)
    tmp2 = False;
    for i in range(steps):
        tmp = And(tmp,combineTransitions(stateMatrix[i], stateMatrix[i+1], dim), isState(stateMatrix[i]))
        tmp2 = Or(tmp2, isFinalStateFormula(stateMatrix[i]))
        if(i > 0):
            tmp = And(tmp, tmp2, Not(isEqualState(stateMatrix[i-1], stateMatrix[i+1]))) # Check if last two steps cancle eachother out. (Moving the empty tile back and forth)


    return simplify(tmp)


def groupSolutionStates(solutionList, dim):
    tmp = [[ 0 for j in range(dim*dim)] for i in range(int(len(solutionList)/(dim*dim)))]
    for i in range(len(solutionList)):
        indeces = parseVar(str(solutionList[i]))
        tmp[indeces[0]-1][indeces[1]] = solutionList[solutionList[i]].as_long()
    return tmp

# utility function to extract the indeces from a variable name
def parseVar(var):
    return [int(s) for s in re.findall(r'\d+', var)]

# -------------------------------------------------------- testPrints --------------------------------------------------------
#print(stateToZ3State(state, 0))
#printStateMatrix(generateStateMatrix(9, 20))
#print(isState(testState))
#print(isFinalState(testState))

#print(isStateMatrix(generateStateMatrix(9,10)))

dim = int(math.sqrt(len(testState)))
# print(topLeftTransitions(testState, testState_2, dim))
# print(topRightTransitions(testState, testState_2, dim))
# print(bottomLeftTransitions(testState, testState_2, dim))
# print(bottomRightTransitions(testState, testState_2, dim))
# print(topRowTransitions(testState4x4, testState4x4_2, 4))
# print(rightColumnTransitions(testState4x4, testState4x4_2, 4))
# print(leftColumnTransitions(testState4x4, testState4x4_2, 4))
# print(bottomRowTransitions(testState4x4, testState4x4_2, 4))
# print(fillerTransitions(testState4x4, testState4x4_2, 4))
# print(fillerTransitions(testState, testState_2, 3))
# s.add(And(stateToZ3State(state,1),isState(testState), isState(testState_2), fillerTransitions(testState, testState_2, 3)))
# print(s.check())
# print(s.model())
start = time.time()
s.add(getFormula(state, 200));
end = time.time()
print("Building the formula took " + str(end-start) + " seconds")
print("Calculating solution...")
start = time.time()
print(s.check())
solution = s.model()
end = time.time()
print("Checking for a solution took " + str(end-start) + " seconds")
x = groupSolutionStates(solution, 3)
printStateMatrix(x)
print(len(x))
print(x.index(finalState))
