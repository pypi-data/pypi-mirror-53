from numpy import *

from KongFuPanda.Classification import Bytes

byte = Bytes()


def loadDataSet():
    postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                   ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                   ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                   ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                   ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                   ['quit', 'worthless', 'dog', 'stupid']]
    classVec = [0, 1, 0, 1, 0, 1]  # 1 is 词性偏负面, 0 词性偏正面
    return postingList, classVec


def createVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)


def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0] * len(vocabList)

    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print("the word: %s is not in my Vocabulary!" % word)
    return returnVec


def trainNB0(trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory) / float(numTrainDocs)
    p0Num = zeros(numWords);
    p1Num = zeros(numWords)  # change to ones()
    p0Denom = 0.0;
    p1Denom = 0.0  # change to 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]  # 侮辱性的
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]  # 非侮辱性的
            p0Denom += sum(trainMatrix[i])
    p1Vect = p1Num / p1Denom  # change to log()
    p0Vect = p0Num / p0Denom  # change to log()
    return p0Vect, p1Vect, pAbusive


def nativeTest():
    listPosts, listClasses = loadDataSet()
    list = createVocabList(listPosts)
    trainMat = []
    for postDoc in listPosts:
        trainMat.append(setOfWords2Vec(list, postDoc))
    p0V, p1V, pAb = trainNB0(trainMat, listClasses)


def testingNB():
    listOPosts, listClasses = loadDataSet()
    myVocabList = createVocabList(listOPosts)
    trainMat = []
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
    p0V, p1V, pAb = trainNB0(array(trainMat), array(listClasses))
    testEntry = ['stupid', 'my', 'dalmation']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print(testEntry, 'classified as: ', byte.classifyNB(thisDoc, p0V, p1V, pAb))
    testEntry = ['stupid']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print(testEntry, 'classified as: ', byte.classifyNB(thisDoc, p0V, p1V, pAb))


if __name__ == '__main__':
    # nativeTest()
    testingNB()
