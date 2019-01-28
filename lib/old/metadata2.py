import config
import const
import json
import requests
import os, io
# import DBUtil
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import logging
import urllib.request
import hashlib

logging.getLogger("requests").setLevel(logging.WARNING)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
logger = logging.getLogger(__name__)


class Metadata2(object):
    def gen_res_id(self, x):
        if x['result']['identifier'] and x['result']['distribution'] :
            datasetid = x['result']['identifier']
            for i in x['result']['distribution']:
                format = i['format']
                dURL = i['downloadURL']
                md5 = hashlib.md5()
                md5.update(str(dURL+ format).encode("utf-8"))
                resourceID = md5.hexdigest()[0:5]
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
        x = self.gen_res_id(x)
        # ensure_ascii = False, display Chinese char
        x_dump = json.dumps(x, indent=4, ensure_ascii=False)



        # open a file IO stream and write result
        f = open(file_name, "w", encoding="UTF-8")
        try:
            f.write(x_dump)
        finally:
            f.close()


    def getMetaData(dataid):
        """
        Given dataset id, find out all download link
        return all available opendata matadata object
        """
        logger.info("Get Resource ID of dataid = " + dataid)
        ## get dataset metadata from server
        r = requests.get(const.METADATA_URL_PREFIX + dataid)
        try:
            x = json.loads(r.text)
            if x.get("success") == False:
                return []
        except:
            logging.exception(dataid + "Json load error !!")
            return []

        result = []

        if x["result"]["distribution"] != None:
            for element in x["result"]["distribution"]:

                obj = Metadata2(element, dataid)
                ## dump metadata as json file and generate resource_id
                obj.setJsonFile(x, dataid)  ## set json file
                ## generate data in result queue
                result.append(obj)
        else:
            # Some data set has no resource field in JSON format
            # eg. http://data.gov.tw/api/v1/rest/dataset/315260000M-000014
            logger.warn("dataid = " + dataid + " has no distribution field")
        return result

    def __init__(self, x, dataid):

        self.datasetID = dataid
        self.resourceID = ""  # empty at this moment
        # eg. resourceID = A59000000N-000229-001
        #     datasetID = A59000000N-000229
        self.resourceDescription = x.get('resourceDescription')
        self.format = x.get('format', "NA")
        if self.format == "NA":
            logger.warn("No format")
        self.resourceModified = x.get('resourceModified')

        # Some data has no downloadURL field
        if 'downloadURL' in x:
            self.downloadURL = x['downloadURL']
        if 'accessURL' in x:
            self.accessURL = x['accessURL']

        self.metadataSourceOfData = x['metadataSourceOfData']
        self.characterSetCode = x['characterSetCode']

    # https://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py

    def download(self, num):
        """
        Download data via self.downloadURL field
        return True if download complete, False if download fail
        """
        if not hasattr(self, 'downloadURL') and not hasattr(self, 'accessURL'):
            logger.warn(self.datasetID + " NO download URL and NO access URL")
            return False
        if hasattr(self, 'downloadURL'):
            URL = self.downloadURL
        elif hasattr(self, 'accessURL'):
            URL = self.accessURL
        else:
            return False

        ## waue : there is no resource id
        # if not hasattr(self, 'resourceID') :

        if self.resourceID :
            name = self.resourceID
        else :
            self.resourceID = self.datasetID + "_" + str(num)  ## need change, because thomas need the hash
            name = self.resourceID
        # try:
        #     self.resourceID = self.datasetID + "_" + str(num)  ## need change, because thomas need the hash
        #     name = self.resourceID
        # except:
        #     self.resourceID = self.datasetID
        #     name = self.datasetID


        dir_name = self.datasetID + "/"
        abspath = config.DOWNLOAD_PATH + "/" + dir_name

        # to avoid the bad connection

        # Download the file from `url` and save it locally under `file_name`:
        if self.format is not "NA":
            file_name = abspath + name + "." + self.format.strip(";\"").lower()
        else:
            # Ensuring the file type is correct from url and request header.
            if "zip" in URL.lower():
                fileTypeFromURL = "zip"
            elif "csv" in URL.lower():
                fileTypeFromURL = "csv"
            elif "xml" in URL.lower():
                fileTypeFromURL = "xml"
            elif "txt" in URL.lower():
                fileTypeFromURL = "txt"
            else:
                fileTypeFromURL = "NA"

        response = requests.get(URL, stream=True, verify=False)
        logger.info("download:" + URL)
        try:
            with open(file_name, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
        except:
            logger.error("ERROR" + URL)
            return False

        # if status code != 200 will return false
        # if self.downloadStatusCode != 200:
        #    return False

        # self.checkHeader(response, fileTypeFromURL)

        return True
