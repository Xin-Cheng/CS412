import sys
from sets import Set

# check if a transaction contains an itemset
def contains_set(transaction, item):
    for i in range(len(item) - 1):
        if item[i + 1] not in transaction:
            return False
    return True

def apriori(dataset, itemset, min_sup, freq_set):
    # count item
    for i in range(len(itemset)):
        for t in range(len(dataset)):
            if contains_set(dataset[t], itemset[i]):
                itemset[i][0] += 1
    new_set = []
    for i in range(len(itemset)):
        if itemset[i][0] >= min_sup:
            new_set.append(itemset[i])
            freq_set.append(itemset[i])
    print("apriori")

def main():
    dataset = []
    items = []
    min_sup = input()
    for line in sys.stdin.readlines():  
        l = line.split()
        dataset.append(l)
        items += l
    items = list(set(items))
    items.sort()
    itemset = []
    for i in range(len(items)):
        s = []
        s.extend([0, items[i]])
        itemset.append(s)
    freq_set = []
    apriori(dataset, itemset, min_sup, freq_set)
    print ("finish")

if __name__ == "__main__":
   main()