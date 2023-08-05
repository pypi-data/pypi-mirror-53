from KongFuPanda.Classification import Tree

tree = Tree()


def createDataSet():
    dataSet = [
        [1, 1, 'yes'],
        [1, 1, 'yes'],
        [1, 0, 'no'],
        [0, 1, 'no'],
        [0, 1, 'no']
    ]
    labels = ['no surfacing', 'flippers']
    # change to discrete values
    return dataSet, labels


def baseTest():
    global tree
    dataSet, labels = createDataSet()
    ent = tree.calcShannonEnt(dataSet)
    list = tree.dataSetSplit(dataSet, 1, 0)
    list = tree.chooseBestFeatureToSplit(dataSet)
    tree = tree.createTree(dataSet, labels)
    print(tree)


if __name__ == '__main__':
    baseTest()
