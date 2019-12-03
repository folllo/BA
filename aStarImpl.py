from numpy import sqrt

class Node:
    def __init__(self,data,parent,gScore,hScore):
        self.data = data
        self.size = int(sqrt(len(data)))
        self.parent = parent
        self.gScore = gScore
        self.fScore = hScore

    def generateChildren(self):
        emptyTileIndex = self.data.index(0)
        # -self.size=up, self.size=down, -1=left, 1=right
        directions = [-self.size,self.size,-1,1]
        children = []
        for direction in directions:
            child = self.move(emptyTileIndex, direction)
            if child is not None:
                children.append(Node(child,self,self.gScore+1,0))
        return children


    def move(self,index, direction):
        if(index+direction >= 0 and index+direction <= 8):
            if(direction == 1 and index%self.size == 2):
                return None
            elif(direction == -1 and index%self.size == 0):
                return None
            else:
                tmpState = self.data.copy()
                self.swapListItems(tmpState, index, index+direction)
                return tmpState
        else:
            return None

    def swapListItems(self, list, pos1, pos2):
        list[pos1], list[pos2] = list[pos2], list[pos1]



class Puzzle:
    def __init__(self,start,goal):
        self.start = start
        self.goal = goal
        self.open = []
        self.closed = []

    def hScore(self, node):
        score = 0;
        for i in range(0,len(self.goal.data)):
                if self.goal.data[i] != node.data[i] and node.data[i] != 0:
                    score += 1
        return score

    def fScore(self, node):
        node.fScore = self.hScore(node)+node.gScore

    def solve(self):
        self.open += self.start.generateChildren()
        for i in self.open:
            self.fScore(i)
        self.open.sort(key=lambda x: x.fScore, reverse=False)
        current = self.open.pop(0)
        self.closed.append(current.data)

        while(current.data != self.goal.data):
            tmp = []
            tmp += current.generateChildren()
            for i in tmp:
                if self.closed.count(i.data) < 1:
                    self.fScore(i)
                    self.open.append(i)
            self.open.sort(key=lambda x: x.fScore, reverse=False)
            current = self.open.pop(0)
            self.closed.append(current.data)

        #     self.printPuzzleState(current.data)
        #     print("  |  ")
        #     print("  |  ")
        #     print("  V  ")
        # self.printPuzzleState(current.data)
        # print("---------------------")
        # print(self.start.data)
        # print("---------------------")
        solution = []
        while(current.parent != None):
            solution.append(current.data)
            # self.printPuzzleState(current.data)
            # print("  ^  ")
            # print("  |  ")
            # print("  |  ")
            current = current.parent
        # self.printPuzzleState(self.start.data)
        solution.append(current.data)
        return solution

    def printPuzzleState(self, state):
        size = int(sqrt(len(state)))
        for i in range(0,size):
                print(state[i*size], state[i*size+1], state[i*size+2])
