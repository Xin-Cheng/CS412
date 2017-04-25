import pandas as pd
import numpy as np
from sys import stdin

def split(dataset, size):
    header = list(dataset)
    label = header[-1]
    ent = entropy(dataset, label)
    features = header[0:len(header)-1]
    # find split feature
    information = np.zeros(len(header) - 1)
    split_information = np.zeros(len(header) - 1)
    for i in range(len(features)):
        info, split_info = info_gain(dataset, label, features[i])
        information[i] = info
        split_information[i] = split_info
    # choose the feature with lowest infomation as current tree node
    gain = ent - information
    print features[np.argmax(gain)]
    gain_ratio = gain/split_information
    print features[np.argmax(gain_ratio)]

def info_gain(dataset, label, feature):
    size = dataset.shape[0]
    # calculate the probability of each distinct value of this feature
    groups = dataset.groupby(feature)
    counts = groups.size().reset_index(name='count')
    group_probability = np.array(counts['count'], dtype=float)/size
    log_pr = np.log2(group_probability)
    # calculate entropy of each distinct value
    distinct_names = dataset[feature].unique()
    eps = np.zeros(len(distinct_names))
    for i in range(len(distinct_names)):
        eps[i] = entropy(groups.get_group(distinct_names[i]), label)
    info = np.dot(group_probability, eps)
    split_info = -np.dot(group_probability, log_pr)
    return info, split_info

# calculate entropy
def entropy(group, label):
    size = group.shape[0]
    groups = group.groupby(label).size().reset_index(name='count')
    counts = np.array(groups['count'], dtype=float)
    probabilities = counts/size
    log_probabilities = -np.log2(probabilities)
    ent = np.dot(probabilities, log_probabilities)
    return ent

def main():
    size = input() - 1
    header = stdin.readline().split(',')
    dataset = pd.DataFrame([], columns=header)
    itr = 0
    for line in stdin.readlines():
        dataset.loc[itr] = line.split(',')
        itr += 1
    split(dataset, size)
    
if __name__ == "__main__":
    main()
