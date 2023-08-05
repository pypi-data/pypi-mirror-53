tree = Tree()

def lense():
    fw = open("lenses.txt")
    lenses = [inst.strip().split("\t") for inst in fw.readlines()]
    lensesLabels = ['age', 'prescript', 'astigmtic', 'tearRate']
    lensesTree = tree.createTree(lenses, lensesLabels)
    print(lensesTree)

if __name__ == '__main__':
    lense()