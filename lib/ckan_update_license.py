from ckanapi import RemoteCKAN
import time
import logging.config

LOGGING_FILE = '../../log/update_license.log'

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(filename)s_%(lineno)d  : %(message)s',
                    handlers = [logging.FileHandler(LOGGING_FILE, 'a', 'utf-8')])

logger = logging.getLogger('root')
ipgod = RemoteCKAN('http://ipgod.nchc.org.tw', apikey='02285f49-a9a7-4809-a42c-a568547511ec')



# result_tuple = (total_count, success_count, failed_count)
result_dict = {
    "total_count": 0,
    "success_count" : 0,
    "failed_count" : 0,
}

def amend_licenseTitle_licenseURL(dataset_detail_dict):
    ## update the licenseURL in extras
    check_license_title_existed = False
    for i in dataset_detail_dict["extras"]:
        if i["key"] == "cost":
            i["value"] = "免費"
        if i["key"] == "licenseURL":
            i["value"] = "https://data.gov.tw/license"
        if i["key"] == "license_title":
            check_license_title_existed = True

    ## add license_title if not existed
    if check_license_title_existed is False:
        dataset_detail_dict["extras"].append({"key": "license_title", "value": "政府資料開放授權條款－第1版"})

    return dataset_detail_dict

# def call_ckanapi_updating_ckan(dataset_detail_dict, result_tuple):
def call_ckanapi_updating_ckan(dataset_detail_dict):
    try:
        ipgod.call_action('package_update', dataset_detail_dict)
        #ipgod.call_action('package_create', dataset_detail_dict)
        result_dict["success_count"] += 1
        logger.info("[success] id ={} ".format(dataset_id))
        return result_dict

    except Exception as ex:
        result_dict["failed_count"] +=1
        print("error={}".format(ex))
        logger.error("[error] id ={} error = {} ".format(dataset_id, ex))
        return result_dict

# def update_license_info(dataset_id, result_tuple):
def update_license_info(dataset_id):
    ## get dataset detail as dict
    dataset_detail_dict = ipgod.call_action('package_show', {'id': dataset_id})
    ## udpate the license_title
    dataset_detail_dict['license_title'] = '政府資料開放授權條款-第1版'
    dataset_detail_dict['license_id'] = 'Open-Government-Data'
    ## update extra info
    dataset_detail_dict = amend_licenseTitle_licenseURL(dataset_detail_dict)

    ## update to ckan
    time.sleep(3)
    return call_ckanapi_updating_ckan(dataset_detail_dict)

if __name__ == "__main__" :
    #data_list=[ '054c130d-c887-4486-8183-b2f53d9e5fb4', '05d07aca-dee8-43d5-a596-cc0da1a71c8f']
    data_list = ipgod.call_action('package_list', {})

    result_dict["total_count"] = len(data_list)

    logger.info("[init] dataset length= {}".format(result_dict["total_count"]))
    for dataset_id in data_list:
        result_dict = update_license_info(dataset_id)

    logger.info("[report] total ={}, success={}, failed={} "
                .format(result_dict["total_count"], result_dict["success_count"],result_dict["failed_count"]))

