import sys
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
            if not isinstance(transactions[i][s], list):
                if s == last and transactions[i][s][-1] == '.':
                    transactions[i][s] = transactions[i][s][:-1]
                if transactions[i][s] in stopwords:
                    transactions[i].remove(transactions[i][s])
            else:
                if s == last and transactions[i][s][-1][-1] == '.':
                    transactions[i][s][-1] = transactions[i][s][-1][:-1]
                for item in transactions[i][s]:
                    if item in stopwords:
                        transactions[i][s].remove(item)
        print transactions[i]

def main():
    transactions = []
    stopwords = ["a", "an", "are", "as", "at", "by", "be", "for", "from", "has", "he", "in", "is", "it", "its", "of", "on", "that", "the", "to", "was", "were", "will", "with"]
    min_sup = input()
    for line in sys.stdin.readlines():  
        transactions.append(line.lower().split())
    clean(transactions, stopwords)
    

if __name__ == "__main__":
    main()