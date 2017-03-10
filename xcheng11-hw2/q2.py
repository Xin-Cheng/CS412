from itertools import chain, combinations
from pprint import pprint

cells = [
['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'a10'],
['b1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'a10'],
['c1', 'c2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'a10'],
['d1', 'd2', 'd3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'a10']
    ]

cells1 = [
['a1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10'],
['d1', 'b2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10'],
['d1', 'd2', 'c3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10']
    ]


def Question2():
    def powerset(s):
        return chain.from_iterable(combinations(s, r) for r in range(0, len(s)+1))

    new_set = dict()
    for cell in cells1:
        list1 = list(powerset(cell))
        for key in list1:
            if key not in new_set:
                new_set[key] = 0
            new_set[key] += 1

    # aggregate cells
    print len(new_set) - len(cells1)
    # verify iceberg condition
    count = 0
    for key in sorted(new_set.keys()):
        if new_set[key] >= 2:
            count += 1

    print count
    i = 1

Question2()