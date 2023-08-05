import time

from numpy import *

from KongFuPanda.Classification.KNN import KNN

'''
加载数据
'''

knn = KNN.knn()


def create_dataset_Test():
    dataSet = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['好', '好', '不好', '不好']
    inX = [int(n) for n in input().split(',')]
    k = 4
    print(inX)
    cc = knn.classify(inX, dataSet, labels, k)
    print(cc)


def appointmentTest(k):
    hoRatio = 0.50  # hold out 10%
    datingDataMat, datingLabels = knn.getFile('Appointment.txt')  # load data setfrom file
    normMat, ranges, minVals = knn.autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m * hoRatio)
    errorCount = 0.0
    str = time.strftime('%Y%m%d', time.localtime())
    filename = "appointment_" + str + ".log"

    fo = open(filename, "a+", encoding='utf-8')

    for i in range(numTestVecs):
        classifierResult = knn.classify(normMat[i, :], normMat[numTestVecs:m, :], datingLabels[numTestVecs:m], k)
        str = "the classifier came back with: %d, the real answer is: %d" % (classifierResult, datingLabels[i])
        # print(str)
        fo.write(str + "\n")
        if (classifierResult != datingLabels[i]): errorCount += 1.0
    str = "the total error rate is: %f" % (errorCount / float(numTestVecs))
    print(str)
    fo.write(str + "\n")
    str = "the total test count is: %d ，the total error count is: %d" % (numTestVecs, errorCount)
    print(str)
    fo.write(str + "\n")
    fo.close()
    return errorCount, k


if __name__ == '__main__':
    # create_dataset_Test()
    list = []
    string = time.strftime('%Y%m%d', time.localtime())
    filename = "appointment_knn_" + string + ".log"

    fo = open(filename, "w", encoding='utf-8')

    for k in range(1, 21):
        list.append(appointmentTest(k))

    min = min(list)
    fo.write("\n".join(str(e) for e in list))
    print(min)
