# CS412 HW2 Question4
def buildIndexTable(datacube, partitions):
    # partition cube, store indics to stack
    parIndices = []
    cellNum = len(datacube)
    dimension = len(datacube[0])
    size = dimension/partitions
    temp = dimension
    while temp >= size:
        temp = temp - size
        parIndices.append(temp)
    parIndices[-1] = 0
    # iterate each shell
    tableList = []
    while len(parIndices) > 0:
        start = parIndices.pop()
        end = parIndices[-1] if len(parIndices) > 0 else dimension
        # attibute, TID list
        indexTable = {}
        for r in range(cellNum):
            for c in range(start, end):
                if datacube[r][c] in indexTable:
                    indexTable[datacube[r][c]].append(r)
                else:
                    indexTable[datacube[r][c]] = [r]
        tableList.append(indexTable)
    return

def main():
    tables = [1, 2, 3]
    for i in range(3):
        t = {i: i}
        tables.append(t)
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