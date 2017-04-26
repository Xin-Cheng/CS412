from sys import stdin
from math import log

def split(dataset, size, header):
    label = len(dataset[0]) - 1
    prs = probability(dataset, label)
    entr = entropy(prs)
    info_gains = []
    gain_ratio = []
    for i in range(label):
        infogain, splitinfo = info_gain(dataset, i, entr)
        info_gains.append(infogain)
        gain_ratio.append(infogain/splitinfo)
    print header[info_gains.index(max(info_gains))]
    print header[gain_ratio.index(max(gain_ratio))]

def info_gain(dataset, idx, all_info):
    size = len(dataset)
    label = len(dataset[0]) - 1
    groups = []
    features = {}
    for i in range(size):
        if dataset[i][idx] in features:
            features[dataset[i][idx]][1] += 1
            groups[features[dataset[i][idx]][0]].append(dataset[i])
        else:
            features[dataset[i][idx]] = [len(groups), 1]
            groups.append([dataset[i]])
    ens = []
    prs = []
    for i in range(len(groups)):
        pr = probability(groups[i], label)
        ens.append(entropy(pr))
        prs.append(float(len(groups[i]))/size)
    info = 0
    splitinfo = 0
    for i in range(len(prs)):
        info += prs[i]*ens[i]
        splitinfo += prs[i]*log(prs[i], 2)
    return all_info - info, -splitinfo

def probability(group, idx):
    lables = {}
    size = len(group)
    for t in group:
        if t[idx] in lables:
            lables[t[idx]] += 1
        else:
            lables[t[idx]] = 1
    counts = lables.values()
    prs = []
    for c in counts:
        prs.append(float(c)/size)
    return prs

# calculate entropy
def entropy(probability):
    ent = 0
    for p in probability:
        ent += p*log(p, 2)
    return -ent

def main():
    size = input() - 1
    header = stdin.readline().split(',')
    dataset = []
    for line in stdin.readlines():
        dataset.append(line.rstrip().split(','))
    split(dataset, size, header)
    
if __name__ == "__main__":
    main()