import json
import logging
import requests
import config
from ckanapi import RemoteCKAN
import numpy as np

logger = logging.getLogger(__name__)


class FetcherList():
    dataid = None

    def writeId2Datalist(self,dataid):
        ## load json file only as dataid
        try:
            with open(config.LIST_PATH, 'w') as outfile:
                json.dump(dataid, outfile)
        except:
            return False
    def processHistory(self):
        latestTime = config.History_Time
        r = requests.get(config.MODIFIED_URL_PREFIX + latestTime,  timeout=config.request_timeout )
        x = json.loads(r.text)
        dataid = x['result']
        return self.writeId2Datalist(dataid)


    def findExclusiveOr(self, src1, src2):
        list_exclu = []
        src1 = np.char.lower(src1)
        src2 = np.char.lower(src2)
        list_exclu = list(set(src1) - set(src2))
        return list_exclu

    def processExclude(self):
        ## ipgod_list
        # ipgod = RemoteCKAN('http://ipgod.nchc.org.tw', apikey='02285f49-a9a7-4809-a42c-a568547511ec')
        ipgod = RemoteCKAN(config.ckanurl, apikey=config.ckan_key)
        ipgod_list = ipgod.call_action('package_list', {})
        ## datagov_list
        r = requests.get("https://data.gov.tw/api/v1/rest/dataset")
        x = json.loads(r.text)
        datagov_list = x["result"]
        non_process_dataset = self.findExclusiveOr(datagov_list, ipgod_list)
        return self.writeId2Datalist(non_process_dataset)


if __name__ == "__main__":
    # using python logging in multiple modules
    # Ref: http://stackoverflow.com/questions/15727420/using-python-logging-in-multiple-modules

    # fl = FetcherList()
    # if fl.processHistory() :
    #     print("Ok")
    # else:
    #     print("Failed")
    historyFetcher = FetcherList()
    if config.Fetch_Mode == 0 :
        pass
    elif config.Fetch_Mode == 1:
        ## history mode
        historyFetcher.processHistory()
    elif config.Fetch_Mode == 2:
        ## diff mode
        historyFetcher.processExclude()
    else:
        pass
