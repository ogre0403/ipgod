import logging

import requests

from requests.packages.urllib3.exceptions import InsecureRequestWarning

import config

#logging.getLogger("requests").setLevel(logging.WARNING)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
logger = logging.getLogger(__name__)


class ResourceMeta(object):


    def __init__(self, x, dataid):

        self.datasetID = dataid

        # eg. resourceID = A59000000N-000229-001
        #     datasetID = A59000000N-000229
        self.resourceDescription = x.get('resourceDescription')
        self.format = x.get('format', "NA")
        if self.format == "NA":
            logger.warn("No format")
        self.resourceModified = x.get('resourceModified')
        if 'resourceID' in x:
            self.resourceID = x['resourceID']  # empty at this moment
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

        if self.resourceID:
            name = self.resourceID
        else:
            self.resourceID = self.datasetID + "_" + "{:0>5}".format(num)  ## need change, because thomas need the hash
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

        response = requests.get(URL, timeout=config.request_timeout , stream=True, verify=False)
        logger.info("download:" + URL)
        try:
            with open(file_name, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
            return True
        except:
            logger.error("ERROR:" + URL)
            return False
