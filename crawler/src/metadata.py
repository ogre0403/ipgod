import const
import json
import requests
import logging
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

LOGGING_FILE = 'ipgod.log'
logging.basicConfig(#filename=LOGGING_FILE,
                    level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(filename)s_%(lineno)d  : %(message)s')
logger = logging.getLogger('root')

class Metadata(object):
    
    def getMetaData(dataid):
        """
        Given dataset id, find out all download link
        return all available opendata matadata object
        """
        
        r = requests.get(const.METADATA_URL_PREFIX + dataid)
        x = json.loads(r.text)
        
        if x.get("success") == False:
            return []
        
        Metadata.getLogFile(x, dataid)
        # print(dataid)
        
        result = []
        
        for element in x["result"]["distribution"]:
            obj = Metadata(element)
            result.append(obj)
        
        #result.append(x["result"]["organization"])
        
        return result
    
    
    def __init__(self, x):
        
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
        
        if URLType == 0, URL is downloadURL. else if URLType is 1, URL is accessURL
        """
        if not hasattr(self, 'downloadURL') and hasattr(self, 'accessURL'):
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
                        
            abspath = const.DOWNLOAD_PATH+"/"+dir_name
            
            
            response = requests.get(URL,stream=True,verify=False)
            # TODO: Save download status in postgreSQL DB
            # postgreSQL schema
            # dataset-id(resourceID), download-timestamp, download-status
            
            self.downloadStatusCode = response.status_code
            if self.downloadStatusCode/100 >= 4:
                return False
            
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
            
            file_name = abspath + name +"." + fileType.strip(";\"")
            
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
        #DONE: Just save the JSON object
        # Just save the JSON object as a json file which is entitled by datasetID
        # eg. A59000000N-000229.json
      
        # get log file name
        datasetID = dataid
        
        name = datasetID
        name = name.replace("/","").rstrip()
        
        # get directory name
        dir_name = datasetID.rstrip()
        
        path = const.DOWNLOAD_PATH + "/"
        dir_name = path + dir_name
        logger.info("Create a directory. Directory path: "+dir_name)
        # create a organization directory in current path
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        
        # abspath will be the log file's path
        # abspath = os.path.abspath(dir_name)+"\\"+name+"\\"
        
        # get log file absolute path
        file_name = dir_name + "/" + name + ".json"
        
        # open a file IO stream and write result
        f = open(file_name, "w", encoding = "UTF-8")
        x_dump = json.dumps(x, indent = 4)
        f.write(x_dump)
