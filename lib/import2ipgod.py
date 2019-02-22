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

def force_recover_move( src_dataset_dir , dst_dir ):
    try :
        shutil.move(src_dataset_dir, dst_dir)
    except Exception as ex:
        for src_dir, dirs, files in os.walk(src_dataset_dir):
            dataset_name = os.path.basename(src_dataset_dir)
            dst_dataset_dir = os.path.join(dst_dir, dataset_name)
            if not os.path.exists(dst_dataset_dir):
                os.makedirs(dst_dataset_dir)
            for file_ in files:
                src_file = os.path.join(src_dir, file_)
                dst_file = os.path.join(dst_dataset_dir, file_)
                if os.path.exists(dst_file):
                    # in case of the src and dst are the same file
                    if os.path.samefile(src_file, dst_file):
                        continue
                    os.remove(dst_file)
                shutil.move(src_file, dst_dataset_dir)
        shutil.rmtree(src_dataset_dir)

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

def produce_empty_dataset(empty_dataset_list, empty_dir_path):
    empty_target_path = os.path.join(config.DONE_PATH + "/" + empty_dir_path)
    for ds_dir_path in list(empty_dataset_list.keys()):
        force_recover_move(ds_dir_path, empty_target_path)
        logger.error("[0] empty: {}".format(ds_dir_path))
    return (empty_dataset_list.__len__(), 0)

def produce_dataset(dataset_path_list, done_flag):
    success_count = 0
    failed_count = 0
    for dataset_path in list(dataset_path_list.keys()):
        try:
            commit_ckan(dataset_path)
            ds_dst_dir_path = config.DONE_PATH + "/" + done_flag
            force_recover_move(dataset_path, ds_dst_dir_path)
            success_count += 1
            logger.info("[{}] import dataset : {}".format(done_flag, dataset_path))
        except Exception as ex:
            failed_count += 1
            traceback.print_exc()
            logger.exception("[fail] import dataset {} error: {}".format(dataset_path, ex))
            ds_failed_dir_path = config.DONE_PATH + "/failed"
            force_recover_move(dataset_path, ds_failed_dir_path)

    return (success_count, failed_count)


if __name__ == "__main__":

    root = config.ROOT_PATH
    (ds_count, ok_dataset, meta_dataset, nosg_dataset) = count_file(root)

    ## produce normal dataset
    (ok_count , ok_failed_count) = produce_dataset( ok_dataset , "ok")

    ## produce only meta dataset
    (meta_count , meta_failed_count) = produce_dataset( meta_dataset, "1")

    ## produce empty dataset
    (empty_count, _ ) = produce_empty_dataset( nosg_dataset, "0" )

    ## finalize the report of the downloaad thread
    # report  total / add normal_success / normal_fail  /  title_success / title_fail / empty
    logger.info(
        "[Report] total {},  normal_dataset = {}, meta dataset = {}"
            .format(ds_count, ok_count , meta_count))
    logger.error(
        "[Report] total {},  normal_failed = {}, meta failed =  {} , empty = {} "
            .format(ds_count, ok_failed_count, meta_failed_count , empty_count ))