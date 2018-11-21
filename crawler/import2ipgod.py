import logging
import os
import shutil
import time
from collections import OrderedDict

import map2ckan
import od2ckan
import odtw

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
    sort_dict = OrderedDict(sorted(dict_by_count.items()))
    print(sort_dict)
    # print(len(dict))


def countFile(root):
    dict_by_count = {}
    dict_by_dspath = {}
    dict_by_onlymeta = {}
    dict_by_nomesg = {}
    for dataset_name in os.listdir(root):
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


def commitCkan(dsp, odtw):
    root_path = dsp
    (root, dataset) = os.path.split(dsp)
    dataset_full_path = os.path.join(root_path, dataset + ".json")
    data = odtw.read(dataset_full_path)

    ckmap = map2ckan.mapod2ckan()
    package = ckmap.map(data)
    # print package
    od_data_path = os.path.dirname(os.path.realpath(dataset_full_path))
    package['basepath'] = od_data_path
    put2ckan = od2ckan.import2ckan()
    res = put2ckan.commit(package)
    logger.info("[finish] %s" % res)


if __name__ == "__main__":

    ##
    if os.path.isdir("./done/ok") is False:
        os.makedirs("./done/ok")
        os.makedirs("./done/0")
        os.makedirs("./done/1")
        os.makedirs("./done/failed")

    root = "./data/"
    (ok_dataset, meta_dataset, nosg_dataset) = countFile(root)

    odtw = odtw.od()
    ## produce normal dataset
    for ds in list(ok_dataset.keys()):
        # commitCkan(ds, odtw)
        try:
            commitCkan(ds, odtw)
            time.sleep(1)
            shutil.move(ds, "./done/ok")
            logger.info("[ok] import dataset : {}".format(ds))
        except:
            logger.error("[fail] import dataset error: {}".format(ds))
            shutil.move(ds, "./done/failed")

    ## produce only meta dataset
    for ds in list(meta_dataset.keys()):
        # commitCkan(ds, odtw)
        try:
            commitCkan(ds, odtw)
            time.sleep(0.5)
            shutil.move(ds, "./done/1")
            logger.info("[1] import meta : {}".format(ds))
        except:
            logger.error("[fail] import meta failed: {}".format(ds))
            shutil.move(ds, "./done/failed")

    ## produce empty dataset
    for ds in list(nosg_dataset.keys()):
        shutil.move(ds, "./done/0")
        logger.error("[0] empty: {}".format(ds))
