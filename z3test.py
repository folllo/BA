from z3 import *
import math

# Solvable test state
state = [6,3,5,1,0,7,8,2,4]

testState = [ Int("x_1_%s" % (i)) for i in range(9)]

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
def topLeftTransitions(state1, state2):
    print("TODO")

# generates possible Transitions from state1 to state2 for the top right corner of a given puzzle
def topRightTransitions(state1, state2):
    print("TODO")

# generates possible Transitions from state1 to state2 for the bottom left corner of a given puzzle
def bottomLeftTransitions(state1, state2):
    print("TODO")

# generates possible Transitions from state1 to state2 for the bottom right corner of a given puzzle
def bottomRightTransitions(state1, state2):
    print("TODO")

# generates possible Transitions from state1 to state2 for the top row of a given puzzle
def topRowTransitions(state1, state2):
    print("TODO")

# generates possible Transitions from state1 to state2 for the right row of a given puzzle
def rightRowTransitions(state1, state2):
    print("TODO")

# generates possible Transitions from state1 to state2 for the bottom row of a given puzzle
def bottomRowTransitions(state1, state2):
    print("TODO")

# generates possible Transitions from state1 to state2 for the left row of a given puzzle
def leftRowTransitions(state1, state2):
    print("TODO")

# generates possible Transitions from state1 to state2 for tiles filling the middle of a given puzzle
def fillerTransitions(state1, state2):
    print("TODO")


# testPrints
#print(stateToZ3State(state, 0))
#printStateMatrix(generateStateMatrix(9, 20))
#print(isState(testState))
#print(isFinalState(testState))

print(isStateMatrix(generateStateMatrix(9,10)))
# print(int(math.sqrt(9)))
