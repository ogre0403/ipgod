import os
import json
import json
import logging
import requests
import config

def count_file(root):
    for dirname in os.listdir(root):
        dirpath = os.path.join(root,dirname)

        filecount = 0
        for _ in os.listdir(dirpath):
            filecount += 1
        dict[dirpath] = filecount


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

def queryByRequest(http_str):

    r = requests.get(http_str, timeout=config.request_timeout)
    dataset_id = json.loads(r.text)['result']
    return dataset_id


if __name__ == "__main__" :
    #    calculate non process dataset
    json_path = "./list/dataid_list_2017.json"
    datasets_dir = "./data"
    ## case 1 : compare dataid_list.json to dir existed
    # src1 = jsonReadDataset(json_path)
    # src2 = listFromDir(datasets_dir)
    ## case 2 : compare online dataset to dataid_list
    src1 = queryByRequest("https://data.gov.tw/api/v1/rest/dataset") #https://data.gov.tw/api/v1/rest/dataset
    src2 = jsonReadDataset(json_path)
    non_process_dataset = findExclusiveOr(src1,src2)
    #store2json(non_process_dataset,json_path)
    print("[Report] alldataset ={}, existed ={}, remain= {}".
          format(len(src1),len(src2),len(non_process_dataset)))
    


