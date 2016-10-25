import const
import json
import requests
import logging
import os

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
        
        Metadata.getLogFile(x)
        
        result = []
        
        for element in x["result"]["distribution"]:
            obj = Metadata(element, x["result"]["organization"], x["result"]["title"])
            result.append(obj)
        
        #result.append(x["result"]["organization"])
       
        return result
    
    
    def __init__(self, json, organization, title):
        
        self.title = title.replace("/","").rstrip()
        self.organization = organization
        self.resourceID = json.get('resourceID')
        # eg. resourceID = A59000000N-000229-001
        #     datasetID = A59000000N-000229
        self.datasetID = self.resourceID[:-4]
        self.resourceDescription = json.get('resourceDescription')
        self.format = json.get('format',"NA")
        if self.format == "NA":
            logger.warn("No format")
        self.resourceModified = json.get('resourceModified')

        # Some data has no downloadURL field
        if 'downloadURL' in json:
            self.downloadURL = json['downloadURL']
            
        self.metadataSourceOfData = json['metadataSourceOfData']
        self.characterSetCode = json['characterSetCode']
        
        
    def getDataID(self):
        return self.dataid
    
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
            
            name = self.resourceID.replace("/","")
            dir_name = self.organization+"\\"+self.title
            
            abspath = os.path.abspath(dir_name)+"\\"
            
            
            response = requests.get(self.downloadURL,stream=True)
            
            
            if "zip" in self.downloadURL:
                fileType = "zip"
                print(self.downloadURL)
            elif "csv" in self.downloadURL:
                fileType = "csv"
            elif "xml" in self.downloadURL:
                fileType = "xml"
            elif "txt" in self.downloadURL:
                fileType = "txt"
            elif "Content-Disposition" in response.headers:
                fileType = response.headers.get("Content-Disposition")
                fileType = fileType[fileType.rfind(".")+1:len(fileType)].rstrip("\"")
            else:
                fileType = response.headers.get("content-type","NA")
                if fileType != "NA":
                    if ";" in fileType:
                        fileType = fileType[fileType.index("/")+1:fileType.index(";")]
                    else:
                        fileType = fileType[fileType.index("/")+1:len(fileType)]
                        
                    if fileType == "octet-stream":
                        fileType = "zip"
                else:
                    fileType = self.format
                    
                    

            file_name = abspath + name+"." + fileType
            print(file_name)
            with open(file_name, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024): 
                    if chunk:
                        f.write(chunk)
            
            return True
    
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
    
    def getLogFile(x):
        name = x["result"]["title"].replace("/","").rstrip()
        dir_name = x["result"]["organization"].rstrip()
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        if not os.path.exists(dir_name+"\\"+name):
            os.makedirs(dir_name+"\\"+name)
        abspath = os.path.abspath(dir_name)+"\\"+name+"\\"
        file_name = abspath + name + ".txt"
        
        # print(file_name)
        
        f = open(file_name, "w", encoding = "UTF-8")
        
        for k, v in x["result"].items():
            # print(k,type(v))
            if type(v) is list:
                f.write("%-25s: \n" %(k))
                for j in v:
                    if type(j) is dict:
                        for distribution_key, distribution_value in j.items():
                            if distribution_key == "downloadURL" and len(distribution_value) > 0:
                                download_url = distribution_value
                            # to get the download file type
                            if distribution_key == "format" and len(distribution_value) > 0 and j.get("downloadURL") is not None:
                                download_type = "."+distribution_value
                            
                            f.write("%30s: %s\n"%(distribution_key, distribution_value))
                    else:
                        f.write("%30s\n"%(j))
            else:
                f.write("%-25s: %s\n" %(k,v))
        
