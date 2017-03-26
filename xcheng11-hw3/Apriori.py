import sys
from sets import Set

# check if a transaction contains an itemset
def contains_set(transaction, item):
    for i in range(len(item) - 1):
        if item[i + 1] not in transaction:
            return False
    return True

# self join
def self_join(new_set):
    if len(new_set) <= 1:
        return new_set
    itemset = []
    for i in range(len(new_set)):
        for j in range(i + 1, len(new_set)):
            s = [ 0 ] + new_set[i][1:] + new_set[j][1:]
            itemset.append(s)
    return itemset

# print result
def print_patterns(freq_set):
    def setCmp(s1, s2):
        if s1[0] != s2[0]:
            return s2[0] - s1[0]
        else:
            str1 = " ".join(s1[1:])
            str2 = " ".join(s2[1:])
            if str1 < str2:
                return -1
            else:
                return 1
    ordered_set = sorted(freq_set, cmp = setCmp)
    for i in range(len(ordered_set)):
        print ("{0} [{1}]").format(ordered_set[i][0], " ".join(ordered_set[i][1:]))
    print ("finish")

def apriori(dataset, itemset, min_sup, freq_set):
    if (len(itemset) == 0):
        return
    # count item
    for i in range(len(itemset)):
        for t in range(len(dataset)):
            if contains_set(dataset[t], itemset[i]):
                itemset[i][0] += 1
    new_set = []
    # prune
    for i in range(len(itemset)):
        if itemset[i][0] >= min_sup:   
            freq_set.append(itemset[i])
            new_set.append(itemset[i])
    new_itemset = self_join(new_set)
    apriori(dataset, new_itemset, min_sup, freq_set)

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
    print_patterns(freq_set)
    print ("finish")

if __name__ == "__main__":
   main()