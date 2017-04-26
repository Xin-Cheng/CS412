from sys import stdin
from math import log
from sets import Set

def split(dataset, size, header):
    label = dataset[len(header) - 1]
    entr = 0
    for c in label.values():
        pr = float(c)/size
        entr += -pr*log(pr, 2)
    col = len(dataset) - 1
    info = [0]*col
    info_gains = [entr]*col
    split_info = [0]*col
    for i in range(col):
        group = dataset[i]
        for g in group.values():
            p = float(len(g))/size
            split_info[i] += -p*log(p, 2)
            entro = entropy(g)
            info[i] += p*entro
        info_gains[i] -= info[i]
        split_info[i] = info_gains[i]/split_info[i]
    print header[info_gains.index(max(info_gains))]
    print header[split_info.index(max(split_info))]

def entropy(labels):
    lbs = set(labels)
    entro = 0
    for l in lbs:
        pr = float(labels.count(l))/len(labels)
        entro += -pr*log(pr, 2)
    return entro

def main():
    size = input() - 1
    header = stdin.readline().split(',')
    col = len(header) - 1
    dataset = [{} for x in range(col + 1)]
    for line in stdin.readlines():
        l = line.rstrip().split(',')
        label = l[-1]
        if label in dataset[col]:
            dataset[col][label] += 1
        else:
            dataset[col][label] = 1
        for i in range(col):
            if l[i] in dataset[i]:
                dataset[i][l[i]].append(label)
            else:
                dataset[i][l[i]] = [label]
    split(dataset, size, header)
    
if __name__ == "__main__":
    main()