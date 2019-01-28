import logging
import os
import shutil
import time
from collections import OrderedDict

import map2ckan
import od2ckan
import odtw
import config

LOGGING_FILE = 'ipgod-od2ckan.log'
logging.basicConfig(filename=LOGGING_FILE,
                    level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(filename)s_%(lineno)d  : %(message)s')
logger = logging.getLogger('root')


def showCaculate(dict_by_count):
    ## shot dict_by_count result
    # show the 0 & 1 case
    if 0 in dict_by_count:
        print("[{}: {}]".format(0, dict_by_count.pop(0)))

    if 1 in dict_by_count:
        print("[{}: {}]".format(1, dict_by_count.pop(1)))

    # show the other case
    sort_list = list(OrderedDict(sorted(dict_by_count.items())).items())
    sum_list = sum(dict_by_count.values())
    print("[Start] dataset summary :total {} \n (res,count)= {}".format(sum_list,sort_list))
    logger.info("[Start] dataset summary :total {} \n (res,count)= {}".format(sum_list,sort_list))
    # print(len(dict))


def countFile(root):

    dict_by_count = {}
    dict_by_dspath = {}
    dict_by_onlymeta = {}
    dict_by_nomesg = {}
    # ds_count =0
    for dataset_name in os.listdir(root):
        # ds_count += 1
        # dataset full path
        dataset_path = os.path.join(root, dataset_name)

        # count the resources of dataset
        rs_count = 0
        for _ in os.listdir(dataset_path):
            rs_count += 1

        ## import ckan by conditions :
        if rs_count == 0:
            dict_by_nomesg[dataset_path] = rs_count
        elif rs_count == 1:
            dict_by_onlymeta[dataset_path] = rs_count
        else:
            # update the workable dataset
            dict_by_dspath[dataset_path] = rs_count

        ## caculate by count
        if rs_count in dict_by_count:
            dict_by_count[rs_count] += 1
        else:
            dict_by_count[rs_count] = 1

    showCaculate(dict_by_count)
    return (dict_by_dspath, dict_by_onlymeta, dict_by_nomesg)



def commitCkan(dsp):

    odtwod = odtw.od()
    root_path = dsp
    (root, dataset) = os.path.split(dsp)
    dataset_full_path = os.path.join(root_path, dataset + ".json")
    data = odtwod.read(dataset_full_path)

    ckmap = map2ckan.mapod2ckan()
    package = ckmap.map(data)
    od_data_path = os.path.dirname(os.path.realpath(dataset_full_path))
    package['basepath'] = od_data_path
    put2ckan = od2ckan.import2ckan()
    print("package={}".format(package))
    res = put2ckan.commit(package)
    logger.info("[finish] %s" % res)


if __name__ == "__main__":

    ##
    #if os.path.isdir("./done/ok") is False:
    #    os.makedirs("./done/ok")
    #    os.makedirs("./done/0")
    #    os.makedirs("./done/1")
    #    os.makedirs("./done/failed")
    #root = "./data/"
    root = config.ROOT_PATH
    (ok_dataset, meta_dataset, nosg_dataset) = countFile(root)




    ## produce normal dataset
    for ds in list(ok_dataset.keys()):
        # commitCkan(ds, odtw)
        try:
            commitCkan(ds)
            #shutil.move(ds, "./done/ok")
            shutil.move(ds, config.DONE_PATH+"/ok")
            logger.info("[ok] import dataset : {}".format(ds))
        except Exception as ex:
            print(ex)
            logger.error("[fail] import dataset {} error: {}".format(ds,ex))
            shutil.move(ds, config.DONE_PATH+"/failed")

    ## produce only meta dataset
    for ds in list(meta_dataset.keys()):
        # commitCkan(ds, odtw)
        try:
            commitCkan(ds)
            #shutil.move(ds, "./done/1")
            shutil.move(ds, config.DONE_PATH+"/1")
            logger.info("[1] import meta : {}".format(ds))
        except Exception as ex:
            logger.error("[fail] import meta {} failed: {}".format(ds,ex))
            #shutil.move(ds, "./done/failed")
            shutil.move(ds, config.DONE_PATH+"/failed")

    ## produce empty dataset
    for ds in list(nosg_dataset.keys()):
        #shutil.move(ds, "./done/0")
        shutil.move(ds, config.DONE_PATH+"/0")
        logger.error("[0] empty: {}".format(ds))

