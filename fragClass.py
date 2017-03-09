class Cuboid:
    cell = []
    TIDs = []
    def __init__(self, cell, TIDs, order):
        self.cell = cell
        self.sort(order)
        self.TIDs = TIDs
    def sort(self, order):
        # sort dimension by order
        def dimensionCmp(d1, d2):
            i1 = order.index(d1[0])
            i2 = order.index(d2[0])
            if i1 != i2:
                return i1-i2
            else:
                return int(d1[0][1]) - int(d2[0][1])
        self.cell = sorted(self.cell, cmp = dimensionCmp)

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
    cube = Cuboid(['b2', 'a1'], [1, 2], order)
    tableList = []
    for i in range(len(datacube)):
        for j in range(len(datacube)):
            attr = [datacube[i][j]]
            tid = [i]
            cube = Cuboid(attr, tid)
            tableList.append(cube)
    tableList[1].TIDs.append(222)
    i = 0

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