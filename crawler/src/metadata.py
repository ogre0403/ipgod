import const
import json
import requests
import logging


LOGGING_FILE = 'ipgod.log'
logging.basicConfig(#filename=LOGGING_FILE,
                    level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(filename)s_%(lineno)d  : %(message)s')
logger = logging.getLogger('root')


class Metadata(object):

    @staticmethod
    def getMetaData(dataid):
        """
        Given dataset id, find out all download link
        return all available opendata matadata object
        """
        r = requests.get(const.METADATA_URL_PREFIX + dataid)
        x = json.loads(r.text)
        result = []
        for element in x['result']['distribution']:
            obj = Metadata(element)
            result.append(obj)
        return result

    def __init__(self, json ):
        self.resourceID = json['resourceID']

        # eg. resourceID = A59000000N-000229-001
        #     datasetID = A59000000N-000229
        self.datasetID = self.resourceID[:-4]
        self.resourceDescription = json['resourceDescription']
        self.format = json['format']
        self.resourceModified = json['resourceModified']

        # Some data has no downloadURL field
        if 'downloadURL' in json:
            self.downloadURL = json['downloadURL']

        self.metadataSourceOfData = json['metadataSourceOfData']
        self.characterSetCode = json['characterSetCode']


    def download(self):
        # TODO: implement resource download logic
        """
        Download data via self.downloadURL field
        return True if download complete, False if download fail
        """
        if not hasattr(self, 'downloadURL'):
            logger.warn(self.resourceID + " NO download URL")
            return False
        else:
            logger.info("download from " + self.downloadURL)
            return True

    def getDataSetID(self):
        return self.datasetID

    def getResourceID(self):
        return self.resourceID

    def getResourceDescription(self):
        return self.resourceDescription

    def getFormat(self):
        return self.format

    def getResourceModified(self):
        return self.resourceModified

    def getDownloadURL(self):
        return self.downloadURL

    def getMetadataSourceOfData(self):
        return self.metadataSourceOfData

    def getCharacterSetCode(self):
        return self.characterSetCode





