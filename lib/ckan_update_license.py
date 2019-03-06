from ckanapi import RemoteCKAN
import time

if __name__ == "__main__" :
    
    scidm = RemoteCKAN('http://ipgod.nchc.org.tw', apikey='02285f49-a9a7-4809-a42c-a568547511ec')
    
    data_list = scidm.call_action('package_list', {})
    len(data_list)
    
    for dataset_id in data_list :
        ## get dataset detail as dict
        dataset_detail_dict = scidm.call_action('package_show', {'id':dataset_id})
        ## udpate the license_title
        dataset_detail_dict['license_title']='政府資料開放授權條款-第1版'
        dataset_detail_dict['license_id']='Open-Government-Data'
    
        ## update the licenseURL in extras
        check_license_title_existed = False
        for i in dataset_detail_dict["extras"] :
            if i["key"] == "cost":
                i["value"] = "免費"
            if i["key"] == "licenseURL":
                i["value"] = "https://data.gov.tw/license"
            if i["key"] == "license_title":
                check_license_title_existed =True
    
        ## add license_title if not existed
        if check_license_title_existed is False:
            dataset_detail_dict["extras"].append({"key":"license_title", "value":"政府資料開放授權條款－第1版"})
    
        ## update
        time.sleep( 5 )
        try :
            scidm.call_action('package_update', dataset_detail_dict)
        except Exception as ex:
            print("error={}".format(ex))
