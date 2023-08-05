import operator
from math import *


class Tree:
    '''
    计算熵值
    '''

    def calcShannonEnt(self, dataSet):
        numEntries = len(dataSet)
        labelCounts = {}
        for featVec in dataSet:  # the the number of unique elements and their occurance
            currentLabel = featVec[-1]
            if currentLabel not in labelCounts.keys(): labelCounts[currentLabel] = 0
            labelCounts[currentLabel] += 1
        shannonEnt = 0.0
        for key in labelCounts:
            prob = float(labelCounts[key]) / numEntries
            shannonEnt -= prob * log(prob, 2)  # log base 2
        return shannonEnt

    '''
    重新划分数据集
    '''

    def dataSetSplit(self, dataSet, index, value):
        retDataSet = []
        for featVec in dataSet:
            if featVec[index] == value:
                reducedFeatVec = featVec[:index]
                reducedFeatVec.extend(featVec[index + 1:])
                retDataSet.append(reducedFeatVec)
        return retDataSet

    '''
    选择一个最优的特征进行规划
    '''

    def chooseBestFeatureToSplit(self, dataSet):
        numFeatures = len(dataSet[0]) - 1  # the last column is used for the labels
        baseEntropy = self.calcShannonEnt(dataSet)
        bestInfoGain = 0.0;
        bestFeature = -1
        for i in range(numFeatures):  # iterate over all the features
            featList = [example[i] for example in dataSet]  # create a list of all the examples of this feature
            uniqueVals = set(featList)  # get a set of unique values
            newEntropy = 0.0
            for value in uniqueVals:
                subDataSet = self.dataSetSplit(dataSet, i, value)
                prob = len(subDataSet) / float(len(dataSet))
                newEntropy += prob * self.calcShannonEnt(subDataSet)
            infoGain = baseEntropy - newEntropy  # calculate the info gain; ie reduction in entropy
            if (infoGain > bestInfoGain):  # compare this to the best gain so far
                bestInfoGain = infoGain  # if better than current best, set to best
                bestFeature = i
        return bestFeature  # returns an integer

    def majorityCnt(self, classList):
        classCount = {}
        for vote in classList:
            if vote not in classCount.keys(): classCount[vote] = 0
            classCount[vote] += 1
        sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
        return sortedClassCount[0][0]

    '''
    创建一颗树
    '''

    def createTree(self, dataSet, labels):
        classList = [example[-1] for example in dataSet]
        if classList.count(classList[0]) == len(classList):
            return classList[0]  # stop splitting when all of the classes are equal
        if len(dataSet[0]) == 1:  # stop splitting when there are no more features in dataSet
            return self.majorityCnt(classList)
        bestFeat = self.chooseBestFeatureToSplit(dataSet)
        bestFeatLabel = labels[bestFeat]
        myTree = {bestFeatLabel: {}}
        del (labels[bestFeat])
        featValues = [example[bestFeat] for example in dataSet]
        uniqueVals = set(featValues)
        for value in uniqueVals:
            subLabels = labels[:]  # copy all of labels, so trees don't mess up existing labels
            myTree[bestFeatLabel][value] = self.createTree(self.dataSetSplit(dataSet, bestFeat, value), subLabels)
        return myTree

    '''
    分类器
    '''

    def classify(self, inputTree, featLabels, testVec):
        firstStr = inputTree.keys()[0]
        secondDict = inputTree[firstStr]
        featIndex = featLabels.index(firstStr)
        key = testVec[featIndex]
        valueOfFeat = secondDict[key]
        if isinstance(valueOfFeat, dict):
            classLabel = self.classify(valueOfFeat, featLabels, testVec)
        else:
            classLabel = valueOfFeat
        return classLabel

    '''
    存储树
    '''

    def storeTree(self, inputTree, fileName):
        import pickle
        fw = open(fileName, "w")
        pickle.dump(inputTree, fw)
        fw.close()

    '''
    加载树
    '''

    def grabTree(self, fileName):
        import pickle
        fr = open(fileName)
        return pickle.load(fr)
