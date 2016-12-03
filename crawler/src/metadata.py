import config
import const
import json
import requests
import logging
import os
import DBUtil
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

LOGGING_FILE = 'ipgod.log'
logging.basicConfig(#filename=LOGGING_FILE,
                    level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(filename)s_%(lineno)d  : %(message)s')
logger = logging.getLogger('root')


class Metadata(object):

    def getMetaData(dataid, timeStr):
        """
        Given dataset id, find out all download link
        return all available opendata matadata object
        """

        r = requests.get(const.METADATA_URL_PREFIX + dataid)
        x = json.loads(r.text)

        if x.get("success") == False:
            return []

        Metadata.getLogFile(x, dataid)
        result = []

        for element in x["result"]["distribution"]:
            obj = Metadata(element, timeStr)
            result.append(obj)
        return result

    def __init__(self, x, timeStr):
        self.timeStr = timeStr
        self.resourceID = x.get('resourceID')
        # eg. resourceID = A59000000N-000229-001
        #     datasetID = A59000000N-000229
        self.datasetID = self.resourceID[:-4]
        self.resourceDescription = x.get('resourceDescription')
        self.format = x.get('format',"NA")
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

    def getDataID(self):
        return self.dataid

    def download(self):
        """
        Download data via self.downloadURL field
        return True if download complete, False if download fail
        """
        if not hasattr(self, 'downloadURL') and not hasattr(self, 'accessURL'):
            logger.warn(self.resourceID + " NO download URL and NO access URL")
            return False
        else:
            if hasattr(self, 'downloadURL'):
                URL = self.downloadURL
            elif hasattr(self, 'accessURL'):
                URL = self.accessURL
            logger.info("download from " + URL)

            name = self.resourceID.replace("/","")
            dir_name = self.datasetID+"/"

            abspath = config.DOWNLOAD_PATH+"/"+dir_name
            
            # to avoid the bad connection
            response = requests.get(URL,stream=True,verify=False,headers={'Connection':'close'})
            
            self.downloadStatusCode = response.status_code

            
            
            # Save download status in postgreSQL DB
            conn = DBUtil.createConnection()
            
            DBUtil.insertDownloadResult(conn, self.resourceID[:-4], self.resourceID[-3:], self.timeStr, self.downloadStatusCode)
            DBUtil.closeConnection(conn)
            
            # if status code != 200 will return false
            if self.downloadStatusCode != 200:
                return False
            
            # use file type from json file's information
            if self.format is not "NA":
                file_name = abspath + name +"." + self.format.strip(";\"").lower()
            else:
                # TODO: ONLY support these 4 format?
                # following resource URL can not be download
                #  http://data.moi.gov.tw/MoiOD/System/DownloadFile.aspx?DATA=9DE2F2C7-F8C3-4D59-A3E7-D08E413C07E5
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

                if "Content-Disposition" in response.headers:
                    fileTypeFromContentDesposition = response.headers.get("Content-Disposition")
                    fileTypeFromContentDesposition = fileTypeFromContentDesposition[fileTypeFromContentDesposition.rfind(".")+1:len(fileTypeFromContentDesposition)].rstrip("\"")
                else:
                    fileTypeFromContentDesposition = "NA"

                if "content-type" in response.headers:
                    fileTypeFromContentType = response.headers.get("content-type","NA")

                    if ";" in fileTypeFromContentType:
                        fileTypeFromContentType = fileTypeFromContentType[fileTypeFromContentType.index("/")+1:fileTypeFromContentType.index(";")]
                    else:
                        fileTypeFromContentType = fileTypeFromContentType[fileTypeFromContentType.index("/")+1:len(fileTypeFromContentType)]

                    if fileTypeFromContentType == "octet-stream" or fileTypeFromContentType == "x-zip":
                        fileTypeFromContentType = "zip"
                else:
                    fileTypeFromContentType = "NA"

                fileTypeFromFormat = self.format

                if fileTypeFromURL != "NA":
                    fileType = fileTypeFromURL
                elif fileTypeFromContentDesposition != "NA":
                    fileType = fileTypeFromContentDesposition
                elif fileTypeFromContentType != "NA":
                    fileType = fileTypeFromContentType
                elif fileTypeFromFormat != "NA":
                    fileType = fileTypeFromFormat
                
            
            with open(file_name, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            logger.info("Download completed. File path: "+file_name)

            return True

    def getDownloadStatusCode(self):
        return self.downloadStatusCode

    def getOrganization(self):
        return self.organization

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

    def getLogFile(x, dataid):
        """
        This function will create a directory and a log file which under former directory.
        A directory file will be named by the owner name while is the key "organization"'s value in json
        A log file will be named by file title in json
         Just save the JSON object as a json file which is entitled by datasetID
         eg. A59000000N-000229.json
        """
        # get log file name
        datasetID = dataid

        name = datasetID
        name = name.replace("/","").rstrip()

        # get directory name
        dir_name = datasetID.rstrip()

        path = config.DOWNLOAD_PATH + "/"
        dir_name = path + dir_name
        logger.info("Create a directory. Directory path: "+dir_name)
        # create a organization directory in current path
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        # abspath will be the log file's path
        # abspath = os.path.abspath(dir_name)+"\\"+name+"\\"

        # get log file absolute path
        file_name = dir_name + "/" + name + ".json"

        # ensure_ascii = False, display Chinese char
        x_dump = json.dumps(x, indent=4, ensure_ascii=False)

        # open a file IO stream and write result
        f = open(file_name, "w", encoding = "UTF-8")
        try:
            f.write(x_dump)
        finally:
            f.close()
