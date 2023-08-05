def seg(s):
    s2 = s[0]
    for e in s[1:]:
        if e == s2[-1]:
            s2 += e
        else:
            s2 += '/'
            s2 += e

    print(s)
    print(s2)


def seg2():
    s2 = []
    s = ['a', 'a', 'b', 'b', 'v', 'v', 'c', 'c', 'a', 's']
    for e in enumerate(s):
        s2.append(e)
    s3 = s2[0]
    for ind, e in enumerate(s2[1:]):
        if e == s3[-1]:
            s3 += e
        else:
            # s3 += '/'
            s3 += e

    print(s)
    print(s3)


if __name__ == '__main__':
    seg2()
