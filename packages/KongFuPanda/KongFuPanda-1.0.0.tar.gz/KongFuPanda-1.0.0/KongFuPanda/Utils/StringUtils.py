class StringUtils:
    def strCount(self, str):
        List = [1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4]
        a = {}
        for i in List:
            if List.count(i) > 1:
                a[i] = List.count(i)
        print(a)


def strCount():
    List = ['a', 'a', 'b', 'b', 'v', 'v', 'c', 'c', 'a', 's']
    a = {}
    for i in List:
        if List.count(i) > 1:
            a[i] = List.count(i)
    val = a.items()
    print(a.values())


if __name__ == '__main__':
    strCount()