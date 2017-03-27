import sys
from sets import Set

# check if a transaction contains an itemset
def contains_set(transaction, item):
    for i in range(len(item) - 1):
        if item[i + 1] not in transaction:
            return False
    return True

def contains_pattern(pattern_set, pattern):
    if len(pattern_set) == 0:
        return False
    for i in range(len(pattern_set)):
        str1 = "".join(pattern_set[i][1:])
        str2 = "".join(pattern[1:])
        if str1 == str2:
            return True
    return False

# merge two itemset
def merge_set(s1, s2):
    s = set(s1 + s2)
    s = sorted(list(s))
    return s

# self join
def self_join(new_set):
    itemset = []
    if len(new_set) <= 1:
        return itemset
    for i in range(len(new_set)):
        for j in range(i + 1, len(new_set)):
            s = [ 0 ] + merge_set(new_set[i][1:] , new_set[j][1:])
            if not contains_pattern(itemset, s):
                itemset.append(s)
    return itemset

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

def is_close(freq_set, index, pattern):
    for i in range(index + 1, len(freq_set)):
        if len(freq_set[i]) > len(pattern) and contains_set(freq_set[i][1:], pattern) and freq_set[i][0] == pattern[0]:
            return False
    return True

def is_max(freq_set, index, pattern):
    for i in range(index + 1, len(freq_set)):
        if len(freq_set[i]) > len(pattern) and contains_set(freq_set[i][1:], pattern):
            return False
    return True

def CLOSET(freq_set):
    close_set = []
    for i in range(len(freq_set)):
        if is_close(freq_set, i, freq_set[i]):
            close_set.append(freq_set[i])
    return  close_set         

def MaxMiner(freq_set):
    max_set = []
    for i in range(len(freq_set)):
        if is_max(freq_set, i, freq_set[i]):
            max_set.append(freq_set[i])
    return  max_set 

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
    print("")

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
    close_set = CLOSET(freq_set)
    print_patterns(close_set)
    max_set = MaxMiner(freq_set)
    print_patterns(max_set)

if __name__ == "__main__":
   main()