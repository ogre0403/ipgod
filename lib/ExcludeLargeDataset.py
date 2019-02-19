import os
from collections import OrderedDict
import shutil


def exclude_file(root,limit_num):
    dict_count_sum = {}
    dict_ds_count = {}
    dict_largeds_count={}
    large_dir_path = "./done/large"
    # dataset count from root
    for dataset_name in os.listdir(root):
        dataset_path = os.path.join(root,dataset_name)

        filecount = 0
        # resource count from dataset dir
        for _ in os.listdir(dataset_path):
            filecount += 1

        # produce the large file if filecount exceed limit
        if filecount > limit_num :
            shutil.move(dataset_path, large_dir_path)
            dict_largeds_count[dataset_name]=filecount

        # add dict_ds_count{"path" : "count"}
        dict_ds_count[dataset_path] = filecount

        # add dict_count_sum{"filecount": "summation"}
        if filecount in dict_count_sum:
            dict_count_sum[filecount] += 1
        else :
            dict_count_sum[filecount] = 1

    if 0 in dict_count_sum :
        print( "[{}: {}]".format(0,dict_count_sum.pop(0)))
    if 1 in dict_count_sum :
        print( "[{}: {}]".format(1,dict_count_sum.pop(1)))

    sort_dict = OrderedDict(sorted(dict_count_sum.items()))
    print(sort_dict)
    print(len(dict_ds_count))

    print("[finish] moved list: {}".format(dict_largeds_count))


if __name__ == "__main__" :
    resource_threshold = 30
    root = "./data/"
    exclude_file(root,resource_threshold)
