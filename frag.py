# CS412 HW2 Question4
import sys
from sets import Set

def buildIndexTable(datacube, partitions):
    # topological order of dimension
    order = []
    for i in range(len(datacube[0])):
        order.append(datacube[0][i][0])
    # partition cube, store indics to stack
    parIndices = []
    cellNum = len(datacube)
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
        cuboids = []
        for r in range(cellNum):
            for c in range(start, end):
                t = datacube[r][c]
                if t in cuboids:
                    index = cuboids.index(t)
                    indexTable[index][1].append(r)
                else:
                    cuboids.append(t)
                    indexTable.append([[t], [r]])
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
    cuboids = []
    for i in range(len(indexTable)):
        c1 = indexTable[i][0]
        c1Idx = indexTable[i][1]
        for j in range(i+1, len(indexTable)):
            c2 = indexTable[j][0]
            c2Idx = indexTable[j][1]
            newIdx = Set(c1Idx) & Set(c2Idx)
            if len(newIdx) > 0:
                newCuboid = Set(c1 + c2)
                # sort dimension by order
                def dimensionCmp(d1, d2):
                    i1 = order.index(d1[0][0])
                    i2 = order.index(d2[0][0])
                    if i1 != i2:
                        return i1-i2
                    else:
                        return int(d1[0][1]) - int(d2[0][1])
                newCuboid = sorted(newCuboid, cmp=dimensionCmp)
                t = tuple(newCuboid)
                if t not in cuboids:
                    newtable.append([newCuboid,newIdx])
                    cuboids.append(t)
    computeCuboids(newtable, order)

def printCuboids(indexTable, order):
    # sort cuboids
    def cuboidCmp(cube1, cube2):
        # determine cube order
        c1 = cube1[0]
        c2 = cube2[0]
        for i in range(len(c1)):
            i1 = order.index(c1[i][0])
            i2 = order.index(c2[i][0])
            if i1 != i2:
                return i1-i2
        # determine cell order
        for i in range(len(c1)):
            if int(c1[i][1]) != int(c2[i][1]):
                return int(c1[i][1]) - int(c2[i][1])
    cuboids = sorted(indexTable, cmp=cuboidCmp)
    # print sorted cuboids
    for i in range(len(cuboids)):
        s = ' '.join(cuboids[i][0])+' : '+str(len(cuboids[i][1]))
        print s

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

if __name__ == "__main__":
   main()