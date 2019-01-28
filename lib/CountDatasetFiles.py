import os
from collections import OrderedDict

def count_file(root):
    for dirname in os.listdir(root):
        dirpath = os.path.join(root,dirname)

        filecount = 0
        for _ in os.listdir(dirpath):
            filecount += 1
        dict[dirpath] = filecount
        if filecount in icount:
            icount[filecount] += 1
        else :
            icount[filecount] = 1

    if 0 in icount :
        print( "[{}: {}]".format(0,icount.pop(0)))
    if 1 in icount :
        print( "[{}: {}]".format(1,icount.pop(1)))


    sort_dict = OrderedDict(sorted(icount.items()))
    print(sort_dict)

    print(len(dict))

if __name__ == "__main__" :
    icount = {}
    dict = {}
    root = "./data/"
    count_file(root)
