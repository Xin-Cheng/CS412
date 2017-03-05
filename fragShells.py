# CS412 HW2 Question4
from sets import Set

def buildIndexTable(datacube, partitions):
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
    # debug
    for i in range(1):
        computeCuboids(tableList[i])
    return      

def computeCuboids(indexTable):
    if len(indexTable) == 0:
        return
    newtable = {}
    cuboids = indexTable.keys()
    for i in range(len(cuboids)):
        for j in range(i+1, len(cuboids)):
            s = Set(cuboids[i] + cuboids[j])
            newCuboid = tuple(s)
            tid = indexTable[cuboids[i]] & indexTable[cuboids[j]]
            if len(tid) > 0 and (not (newCuboid in newtable)):
                newtable[newCuboid] = tid
    computeCuboids(newtable)
    

def main():
    datacube = [
        ['a1', 'b2', 'c1', 'd1', 'e1'],
        ['a1', 'b2', 'c1', 'd2', 'e1'],
        ['a1', 'b2', 'c1', 'd1', 'e2'],
        ['a2', 'b1', 'c1', 'd1', 'e2'],
        ['a2', 'b1', 'c1', 'd1', 'e3']
    ]
    partitions = 2
    order = []
    for i in range(len(datacube[0])):
        order.append(datacube[0][i][0])
    buildIndexTable(datacube, partitions)

if __name__ == "__main__":
   main()