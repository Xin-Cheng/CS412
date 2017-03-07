# CS412 HW2 Question4
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
        # attibute, TID list
        indexTable = {}
        for r in range(cellNum):
            for c in range(start, end):
                t = (datacube[r][c],)
                if t in indexTable:
                    indexTable[t].add(r)
                else:
                    indexTable[t] = Set([r])
        tableList.append(indexTable)
    # compute cuboids
    for i in range(len(tableList)):
        computeCuboids(tableList[i], order)
    return      

def computeCuboids(indexTable, order):
    if len(indexTable) == 0:
        return
    printCuboids(indexTable, order)
    newtable = {}
    cuboids = indexTable.keys()
    for i in range(len(cuboids)):
        for j in range(i+1, len(cuboids)):
            s = Set(cuboids[i] + cuboids[j])
            newCuboid = tuple(s)
            tid = indexTable[cuboids[i]] & indexTable[cuboids[j]]
            if len(tid) > 0 and (not (newCuboid in newtable)):
                newtable[newCuboid] = tid
    computeCuboids(newtable, order)

def printCuboids(indexTable, order):
    # sort dimension in cuboid
    def dimensionCmp(c1, c2):
        i1 = order.index(c1[0])
        i2 = order.index(c2[0])
        if i1 != i2:
            return i1-i2
        else:
            return int(c1[1]) - int(c2[1])
    for key, value in indexTable.iteritems():
        oldkey = key
        newkey = tuple(sorted(key, cmp=dimensionCmp))
        indexTable[newkey] = indexTable.pop(oldkey)
    # sort cuboids
    cuboids = []
    for key, value in indexTable.iteritems():
        cuboids.append(key + (len(value),))
    def cuboidCmp(c1, c2):
        # determine cube order
        for i in range(len(c1) - 1):
            i1 = order.index(c1[i][0])
            i2 = order.index(c2[i][0])
            if i1 != i2:
                return i1-i2
        # determine cell order
        for i in range(len(c1) - 1):
            if int(c1[i][1]) != int(c2[i][1]):
                return int(c1[i][1]) - int(c2[i][1])
    cuboids = sorted(cuboids, cmp=cuboidCmp)
    # print sorted cuboids 
    # print cuboids
    length = len(cuboids[0])
    for i in range(len(cuboids)):
        print ' '.join(cuboids[i][:length-1]), ':', cuboids[i][length-1]

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
    i = "finish"

if __name__ == "__main__":
   main()