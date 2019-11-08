class Node:
    def __init__(self,data,gScore,hScore):
        self.data = data
        self.gScore = gScore
        self.hScore = hScore

    def generateChildren(self):
        emptyTileIndex = self.data.index(0)



    def move(self,index, direction):
        if(index+direction >= 0 and index+direction <= 9):
            tmpState = self.data.copy()
            tmpState.insert(index,tmpState[index+direction])
            tmpState.remove(0)
            tmpState.remove(index+direction)
            tmpState.insert(index+direction, 0)
            return tmpState
        else:
            return null


tmpNode = Node([1,2,3,4,5,6,7,8,0],0,0)
tmpNode2 = Node(tmpNode.move(8, -3),0,0)
print(tmpNode.data)
print(tmpNode2.data)
