import sys
from sets import Set
import operator
def clean(transactions, stopwords):
    for i in range(len(transactions)):
        # group joined words
        while 'and' in transactions[i]:
            joined_words = []
            and_idx = transactions[i].index('and')
            if and_idx != len(transactions[i]) - 1:
                joined_words.append(transactions[i][and_idx+1])
                transactions[i].remove(transactions[i][and_idx+1])
            if and_idx != 0:
                joined_words.insert(0, transactions[i][and_idx-1])
                transactions[i].remove(transactions[i][and_idx-1])
            idx = and_idx - 2
            while idx >= 0 and transactions[i][idx][-1] == ',':
                joined_words.insert(0, transactions[i][idx][:-1])
                transactions[i].remove(transactions[i][idx])
                idx -= 1
            if len(joined_words) > 0:
                transactions[i][transactions[i].index('and')] = joined_words
        # remove stop words
        last = len(transactions[i]) - 1
        for s in range(last, -1, -1):
            if not isinstance(transactions[i][s], list) and transactions[i][s] in stopwords:
                transactions[i].remove(transactions[i][s])
            elif isinstance(transactions[i][s], list):
                for item in transactions[i][s]:
                    if item in stopwords:
                        transactions[i][s].remove(item)
    return transactions

def contains(transaction, item):
    for i in range(len(transaction)):
        if (isinstance(transaction[i], list) and item in transaction[i]) or item == transaction[i]:
            return i
    return -1

def findDistincItem(dataset):
    distinctWords = []
    for transaction in dataset:
        for item in transaction:
            if isinstance(item, list):
                distinctWords += item
            else:
                distinctWords.append(item)
    return list(Set(distinctWords))

def prune(singleItems, database, minSup):
    count = [0]*len(singleItems)
    frequents = []
    for i in range(len(singleItems)):
        for transaction in database:
            if contains(transaction, singleItems[i]) != -1:
                count[i] += 1
    for i in range(len(singleItems)):
        if (count[i] >= minSup):
            frequents.append([count[i], singleItems[i]])  
    return frequents
    
def prefixSpan(prefix, projectedDB, patterns, minSup):
    singleItems = findDistincItem(projectedDB)
    frequentItems = prune(singleItems, projectedDB, minSup)
    for freq in frequentItems:
        if len(prefix) == 0:
            newPrefix = list(freq)
        else:
            newPrefix = list(prefix) + [freq[1]]
        if newPrefix[0] > freq[0]:
            newPrefix[0] = freq[0]
        patterns.append(newPrefix)
        newDB = []
        for transaction in projectedDB:
            idx = contains(transaction, freq[1])
            if idx != -1:
                newDB.append(transaction[idx:])
                if isinstance(newDB[-1][0], list):
                    idx = newDB[-1][0].index(freq[1])
                    newDB[-1][0] = newDB[-1][0][idx+1:]
                    if not newDB[-1][0]:
                        newDB[-1].pop(0)
                    else:
                        newDB[-1][0][0] = '_' + newDB[-1][0][0]
                else:
                    newDB[-1].pop(0)
        prefixSpan(newPrefix, newDB, patterns, minSup)

def output(patterns, minSup):
    maxLen = 0
    for pattern in patterns:
        if len(pattern) > maxLen:
            maxLen = len(pattern)
    longestPatterns = []
    for pattern in patterns:
        if (len(pattern) == maxLen):
            longestPatterns.append(pattern)
    longestTuples = []
    for lp in longestPatterns:
        for i in range(len(lp)):
            if lp[i][0] == '_':
                lp[i] = lp[i][1:]
        strPattern = ' '.join(lp)
        if strPattern not in longestTuples:
            longestTuples.append(strPattern)            
    cdd = 0

def main():
    transactions = []
    stopwords = ["a", "an", "are", "as", "at", "by", "be", "for", "from", "has", "he", "in", "is", "it", "its", "of", "on", "that", "the", "to", "was", "were", "will", "with"]
    minSup = input()
    for line in sys.stdin.readlines():
        l = line.lower().split()
        if l[-1][-1] == '.':
            l[-1] = l[-1][:-1]
        transactions.append(l)
    transactions = clean(transactions, stopwords)
    prefix = []
    projectedDB = transactions
    patterns = []
    prefixSpan(prefix, projectedDB, patterns, minSup)
    output(patterns, minSup)
    cdd = 1
    
if __name__ == "__main__":
    main()