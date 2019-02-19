import logging
import os
import shutil
import time
import traceback
from collections import OrderedDict
import CountDatasetFiles
import map2ckan
import od2ckan
import odtw
import config
import logging.config

# LOGGING_FILE = 'ipgod-od2ckan.log'
# logging.basicConfig(filename=LOGGING_FILE,
#                     level=logging.INFO,
#                     format='%(asctime)s [%(levelname)s] %(filename)s_%(lineno)d  : %(message)s')
# logger = logging.getLogger('root')
logger = logging.getLogger(__name__)
logging.config.fileConfig(config.import_logging_configure_file,
                          defaults=None,
                          disable_existing_loggers=False)




def count_file(root):
    #TODO  : test the function
    CountDatasetFiles.count_file(root)
#    dict_by_count = {}
    dict_by_dspath = {}
    dict_by_onlymeta = {}
    dict_by_nomesg = {}
    ds_count =0
    for dataset_name in os.listdir(root):
        ds_count += 1
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
    return (ds_count, dict_by_dspath, dict_by_onlymeta, dict_by_nomesg)



def commit_ckan(dsp):

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

def produce_dataset(target_dataset, destination, empty = False):
    if empty is True :
        for ds in list(target_dataset.keys()):
            shutil.move(ds, config.DONE_PATH+"/" + destination)
            logger.error("[0] empty: {}".format(ds))
        return (target_dataset.__len__(), 0)

    success_count = 0
    failed_count = 0
    for ds in list(target_dataset.keys()):
        try:
            commit_ckan(ds)
            shutil.move(ds, config.DONE_PATH + "/" + destination)
            success_count += 1
            logger.info("[{}] import dataset : {}".format(destination, ds))

        except Exception as ex:
            failed_count += 1
            traceback.print_exc()
            logger.exception("[fail] import dataset {} error: {}".format(ds, ex))
            shutil.move(ds, config.DONE_PATH + "/failed")

    return (success_count, failed_count)


if __name__ == "__main__":

    root = config.ROOT_PATH
    (ds_count, ok_dataset, meta_dataset, nosg_dataset) = count_file(root)

    ## produce normal dataset
    (ok_count , ok_failed_count) = produce_dataset( ok_dataset , "ok")

    ## produce only meta dataset
    (meta_count , meta_failed_count) = produce_dataset( meta_dataset, "1")

    ## produce empty dataset
    (empty_count, _ ) = produce_dataset( nosg_dataset, "0" , empty= True)

    ## finalize the report of the downloaad thread
    # report  total / add normal_success / normal_fail  /  title_success / title_fail / empty
    logger.info(
        "[Report] total {},  normal_dataset = {}, meta dataset = {}"
            .format(ds_count, ok_count , meta_count))
    logger.error(
        "[Report] total {},  normal_failed = {}, meta failed =  {} , empty = {} "
            .format(ds_count, ok_failed_count, meta_failed_count , empty_count ))