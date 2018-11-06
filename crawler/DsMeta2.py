import hashlib
import json
import logging
import os
import random
import string

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

import ResMeta2
import config



requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
logger = logging.getLogger(__name__)


class DatasetMeta(object):
    def genResId(self, x):
        if x['result']['identifier'] and x['result']['distribution'] :
            datasetid = x['result']['identifier']
            for i in x['result']['distribution']:
                if 'format' in i and 'downloadURL' in i:
                    format = i['format']
                    dURL = i['downloadURL']
                    md5 = hashlib.md5()
                    md5.update(str(dURL+ format).encode("utf-8"))
                    resourceID = md5.hexdigest()[0:5]
                else:
                    resourceID = ''.join(
                        random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=5))

                i['resourceID'] = datasetid + "_" +resourceID
            return x
        else:
            return x
    def setJsonFile(self, x, dataid):
        """
        This function will create a directory and a log file which under former directory.
        A directory file will be named by the owner name while is the key "organization"'s value in json
        A log file will be named by file title in json
         Just save the JSON object as a json file which is entitled by datasetID
         eg. A59000000N-000229.json
        """
        # x will be the json full format of that dataset
        # get log file name
        datasetID = dataid

        name = datasetID
        name = name.replace("/", "").rstrip()

        # get directory name
        dir_name = datasetID.rstrip()

        path = config.DOWNLOAD_PATH + "/"
        dir_name = path + dir_name
        logger.info("Create a directory. Directory path: " + dir_name)
        # create a organization directory in current path
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        # abspath will be the log file's path
        # abspath = os.path.abspath(dir_name)+"\\"+name+"\\"

        # get log file absolute path
        file_name = dir_name + "/" + name + ".json"

        # generate the resource id
        x = self.genResId(x)
        # ensure_ascii = False, display Chinese char
        x_dump = json.dumps(x, indent=4, ensure_ascii=False)



        # open a file IO stream and write result
        f = open(file_name, "w", encoding="UTF-8")
        try:
            f.write(x_dump)
        finally:
            f.close()
        return x


    def getResList(self,dataid):
        """
        Given dataset id, find out all download link
        return all available opendata matadata object
        """
        logger.info("Get Resource ID of dataid = " + dataid)
        ## get dataset metadata from server
        r = requests.get(config.METADATA_URL_PREFIX + dataid,  timeout=config.request_timeout )
        try:
            json_raw = json.loads(r.text)
            if json_raw.get("success") == False:
                return []
        except:
            logging.exception(dataid + "Json load error !!")
            return []



        ## store json file,
        ## x = dataset json, dataid = datasetid
        ## reload the jsonfile as structure
        json_with_resid = self.setJsonFile(json_raw, dataid)


        ## produce resource working list
        res_working_list = []

        if json_with_resid["result"]["distribution"] != None:
            for element in json_with_resid["result"]["distribution"]:

                res_meta = ResMeta2.ResourceMeta(element, dataid)
                ## dump metadata as json file and generate resource_id

                ## generate data in result queue
                res_working_list.append(res_meta)
        else:
            # Some data set has no resource field in JSON format
            # eg. http://data.gov.tw/api/v1/rest/dataset/315260000M-000014
            logger.warn("dataid = " + dataid + " has no distribution field")
        return res_working_list



