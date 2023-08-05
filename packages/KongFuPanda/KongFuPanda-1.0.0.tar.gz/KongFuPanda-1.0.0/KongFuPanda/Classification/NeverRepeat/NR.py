from collections import Counter


def nr(str):
    dictCount = Counter(str)  # 第一步计数
    listSort = sorted(dictCount.items(), key=lambda d: d[1], reverse=True)  # 第二步排序
    dictSout = dict(listSort)  # 第三步
    listNr = []
    listNP = []
    dictSoutKey2 = sum(list(dictSout.values()), list(dictSout.values())[1]) - list(dictSout.values())[0]

    for j in range(list(dictSout.values())[0]):
        for i in range(dictSout.__len__()):
            if list(dictSout.values())[i] > 0:
                if sum(list(dictSout.values())[1:]) == 0 and list(dictSout.keys())[i] is listNr[dictSoutKey2 - 1]:
                    count = 1
                    for k in range(listNr.__len__() - 1):
                        if list(dictSout.keys())[i] is listNr[k] or list(dictSout.keys())[i] is listNr[k + 1]:
                            count += 1
                            if count >= listNr.__len__():
                                listNP += list(dictSout.keys())[i]
                                break
                        else:
                            # listNr[k:k + 1] = list(dictSout.keys())[i]
                            listNr.insert(k + 1, list(dictSout.keys())[i])
                            break
                else:
                    listNr += list(dictSout.keys())[i]
                    dictSout[list(dictSout.keys())[i]] = list(dictSout.values())[i] - 1
                if listNr.__len__() - 1 >= dictSoutKey2:
                    dictSoutKey2 += 1

            else:
                listNr += ''

    print("原序列 \n", str)
    print("最优可排序列\n", listNr)
    print("存在不可重排序列元素：", listNP)
    return listNr, listNP


if __name__ == '__main__':
    s = ['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'b', 'c', 'b', 'c', 'b', 'c',
         'b', 'c', 'a', 'a', 'a', 'a', 'b', 'c', 'b', 'c', 'b', 'c',
         'b', 'c']
    nr(s)
