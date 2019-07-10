from z3 import *
import math

# Solvable test state
state = [6,3,5,1,0,7,8,2,4]

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
def isFinalState(state):
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
    return simplify(Or(case1,case2))


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
    return simplify(Or(case1,case2))

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
    return simplify(Or(case1,case2))

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
    return simplify(Or(case1,case2))

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
        tmp = Or(tmp, case1 , case2, case3)
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
        tmp = Or(tmp, case1 , case2, case3)
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
        tmp = Or(tmp, case1 , case2, case3)
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
        # case1 equals shifting the empty tile down
        case2 = switchTiles(state1, state2, (i+1)*dim, (i+2)*dim)
        # case1 equals shifting the empty tile to the right
        case3 = switchTiles(state1, state2, (i+1)*dim, (i+1)*dim+1)
        tmp = Or(tmp, case1 , case2, case3)
    return simplify(tmp)

# generates possible Transitions from state1 to state2 for tiles filling the middle of a given puzzle
def fillerTransitions(state1, state2):
    print("TODO")

def switchTiles(state1, state2, pos1, pos2):
    tmp = And((state1[pos1] == state2[pos2]),(state1[pos2] == state2[pos1]))
    for i in range(len(state1)):
        if i != pos1 and i != pos2:
            tmp = And(tmp, state1[i] == state2[i])
    return tmp


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
