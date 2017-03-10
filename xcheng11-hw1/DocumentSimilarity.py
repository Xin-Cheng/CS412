# CS412 HW1 Question4 xcheng11
import sys
import os
import math
import numpy
from sklearn.decomposition import PCA as skPCA

# split the file by line and then split each line by space
def parseFile(path):
    docList = []
    with open(path) as file:
        for line in file:
            docList.append(line.split())
    return docList

# construct a vector containing unique words; word as key, idf as value
def constructVector(docList):
    wordDic = {}
    numDoc = len(docList)
    for d in range(numDoc):
        doc = docList[d]
        for w in range(len(doc)):
            if not wordDic.has_key(doc[w]):
                wordDic[doc[w]] = 1
            elif w == doc.index(doc[w]):
                wordDic[doc[w]] += 1
    # Calculate idf(t) for each word
    for key, value in wordDic.iteritems():
        wordDic[key] = math.log(float(numDoc)/value)   
    return wordDic

# based on the word dictionary, convert each document to |V| dimension vector d
def convertDocument(docList, wordDic):
    numDoc = len(docList)
    vecList = []
    for d in range(numDoc):
        vec = []
        doc = docList[d]
        numItem = len(doc)
        for key in wordDic:
            # calculate tf for each word
            tf = float(doc.count(key))/numItem
            vec.append(tf*wordDic[key])
        vecList.append(vec)
    return vecList

# calculate Manhattan Distance
def manhattanDistance(documents):
    queryDoc = documents[len(documents)-1]
    maDistance = []
    for i in range(len(documents)):
        val = numpy.sum(numpy.absolute(numpy.subtract(documents[i], queryDoc)))
        maDistance.append(round(val, 3))
    return maDistance

# calculate Euclidean Distance
def euclideanDistance(documents):
    queryDoc = documents[len(documents)-1]
    euDistance = []
    for i in range(len(documents)):
        sub = numpy.subtract(documents[i], queryDoc)
        val = math.sqrt(numpy.dot(sub, sub))
        euDistance.append(round(val, 3))
    return euDistance

# calculate Spremum Distance
def supremumDistance(documents):
    queryDoc = documents[len(documents)-1]
    suDistance = []
    for i in range(len(documents)):
        val = max(numpy.absolute(numpy.subtract(documents[i], queryDoc)))       
        suDistance.append(round(val, 3))
    return suDistance

# calculate Cosine similarity
def cosinSimilarity(documents):
    queryDoc = documents[len(documents)-1]
    cosDistance = []
    for i in range(len(documents)):
        val = 1 - numpy.dot(queryDoc, documents[i])/(math.sqrt(numpy.dot(queryDoc, queryDoc))*math.sqrt(numpy.dot(documents[i], documents[i])))
        cosDistance.append(round(val, 3))
    return cosDistance

# calulate Euclidean Distance after project the document using PCA
def PCA(documents):
    pca = skPCA(n_components=2)
    projDocuments = pca.fit_transform(documents)
    pcaDistance = euclideanDistance(projDocuments)
    return pcaDistance

# find the five minimum distances in a given array
def fiveMin(arr):
    minVal = {}
    for i in range(5):
        minVal[i] = "inf"
    for j in range(len(arr)):
        mx = max(minVal, key = minVal.get)
        if arr[j] < minVal[mx]:
            minVal.pop(mx)
            minVal[j] = arr[j]
    # Sort five minimum values
    minVal = sorted([(value,key) for (key,value) in minVal.items()])
    for m in range(len(minVal)):
        print(minVal[m][1]+1),
    print

def main(argv):
    # check command line options
    if len(argv) > 0:
        path = os.path.abspath(argv[0])
    else:
        path = 'corpus.txt'
    if not os.path.exists(path):
        print("Couldn't find file: " + path)
        sys.exit()
    docList = parseFile(path)
    wordDic = constructVector(docList)
    print(len(wordDic))
    documents = convertDocument(docList, wordDic)
    fiveMin(manhattanDistance(documents))
    fiveMin(euclideanDistance(documents))
    fiveMin(supremumDistance(documents))
    fiveMin(cosinSimilarity(documents))
    fiveMin(PCA(documents))

if __name__ == "__main__":
   main(sys.argv[1:])