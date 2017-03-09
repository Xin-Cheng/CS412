# CS412 HW2 Question4
import sys
from sets import Set

class Cuboid:
    name = ''
    cell = []
    TIDs = []
    def __init__(self, cell, TIDs, order):
        self.cell = cell
        self.TIDs = TIDs
        if len(self.cell) > 1:
            self.sort(order)
        self.name = ''.join(self.cell)
    def sort(self, order):
        # sort dimension by order
        def dimensionCmp(d1, d2):
            if order.index(d1[0]) != order.index(d2[0]):
                return order.index(d1[0]) - order.index(d2[0])
            else:
                return int(d1[1]) - int(d2[1])
        self.cell = sorted(self.cell, cmp = dimensionCmp)

def cuboidJoin(first, second, order):
    cell = list(Set(first.cell) | Set(second.cell))
    tids = list(Set(first.TIDs) & Set(second.TIDs))
    return Cuboid(cell, tids, order)

def contains(cuboidlist, cuboid):
    for i in range(len(cuboidlist)):
        if cuboid.name == cuboidlist[i].name:
            return i
    return -1

def buildIndexTable(datacube, partitions):
    # topological order of dimension
    order = []
    for i in range(len(datacube[0])):
        order.append(datacube[0][i][0])
    # partition cube, store indics to stack
    parIndices = []
    dimension = len(datacube[0])
    temp = dimension
    size = partitions
    while temp > 0:
        temp -= temp/size
        size -= 1
        parIndices.append(temp)
    # iterate each shell
    tableList = []
    while len(parIndices) > 0:
        start = parIndices.pop()
        end = parIndices[-1] if len(parIndices) > 0 else dimension
        # index table: attribut + TID list
        indexTable = []
        for r in range(dimension):
            for c in range(start, end):
                cube = Cuboid([datacube[r][c]], [r], order)
                cont = contains(indexTable, cube)
                if cont == -1:
                    indexTable.append(cube)
                else:
                    indexTable[cont].TIDs.append(r)
        tableList.append(indexTable)
    # compute cuboids
    for i in range(len(tableList)):
        computeCuboids(tableList[i], order)
        print

def computeCuboids(indexTable, order):
    if len(indexTable) == 0:
        return
    printCuboids(indexTable, order)
    newtable = []
    for i in range(len(indexTable)):
        for j in range(i+1, len(indexTable)):
            cube = cuboidJoin(indexTable[i], indexTable[j], order)
            if len(cube.TIDs) > 0:
                if contains(newtable, cube) == -1:
                    newtable.append(cube)
    computeCuboids(newtable, order)

def printCuboids(indexTable, order):
    # sort cuboids
    def cuboidCmp(cube1, cube2):
        # determine cube order
        for i in range(len(cube1.cell)):
            if order.index(cube1.cell[i][0]) != order.index(cube2.cell[i][0]):
                return order.index(cube1.cell[i][0]) - order.index(cube2.cell[i][0])
        # determine cell order
        for i in range(len(cube1.cell)):
            if int(cube1.cell[i][1]) != int(cube2.cell[i][1]):
                return int(cube1.cell[i][1]) - int(cube2.cell[i][1])
    cuboids = sorted(indexTable, cmp = cuboidCmp)
    # print sorted cuboids
    for i in range(len(cuboids)):
        print ' '.join(cuboids[i].cell)+' : '+str(len(cuboids[i].TIDs))

def main():
    datacube = [
        ['a1', 'b2', 'c1', 'd1', 'e1'],
        ['a1', 'b2', 'c1', 'd2', 'e1'],
        ['a1', 'b2', 'c1', 'd1', 'e2'],
        ['a2', 'b1', 'c1', 'd1', 'e2'],
        ['a2', 'b1', 'c1', 'd1', 'e3']
    ]
    partitions = 2
    buildIndexTable(datacube, partitions)
    i = 'finish'

if __name__ == "__main__":
   main()