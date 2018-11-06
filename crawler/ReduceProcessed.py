import os
import json


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

    print(dict)
    print(icount)


def findExclusiveOr(src1, src2):
    list_exclu = []
    list_exclu = list(set(src1) - set(src2))
    return list_exclu


def jsonReadDataset(directory):
    with open(directory,"r") as f:
        dataid = json.load(f)
    return dataid


def listFromDir(directory):
    list_dir = []
    for dirname in os.listdir(directory):
        list_dir.append(dirname)
    return list_dir


def store2json(non_process_dataset, json_file):
    import datetime
    now = datetime.datetime.now()
    datetime = "{}{:02}{:02}_{:02}{:02}".format(now.year, now.month, now.day, now.hour, now.minute, now.second)
    json_backup_name = json_file +datetime
    print(json_backup_name)
    os.rename(json_file,json_backup_name)
    with open(json_file, 'w') as outfile:
        json.dump(non_process_dataset, outfile)


if __name__ == "__main__" :
    #    calculate non process dataset
    json_path = "./list/dataid_list.json"
    datasets_dir = "./data"
    src1 = jsonReadDataset(json_path)
    src2 = listFromDir(datasets_dir)
    non_process_dataset = findExclusiveOr(src1,src2)
    store2json(non_process_dataset,json_path)
    print("[Report] alldataset ={}, existed ={}, remain= {}".
          format(len(src1),len(src2),len(non_process_dataset)))
    


