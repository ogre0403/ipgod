import queue
import logging
import datetime
import requests
import json
import os
import types
import urllib.request
from pip._vendor.pyparsing import empty
from idlelib.ReplaceDialog import replace

class test():
    def __init_():
        print("class: test, initialized")

def main():
    
    logging.basicConfig(level=logging.NOTSET,
                    format = "%(asctime)s [%(levelname)s] %(filename)s_%(lineno)d  : %(message)s"
                    #filename="test_log.txt"
                    )
            
    log = logging.getLogger("root")
    log.info("this is a test info")
    log.warning("this is a test warning")
    log.debug("this is a test debug")
    
    #url = "http://140.120.15.162/home/test.html";
    url = "http://data.gov.tw/api/v1/rest/dataset/382000000A-000136"
    url_modi = "http://data.gov.tw/api/v1/rest/dataset?modified=2016-10-18%2020:23:12"
    
    r = requests.get(url)
    x = json.loads(r.text)
    
    # log.debug("json:\n %s",x)
    # log.info("result: %s",x['result'])
    
    x_dump = json.dumps(x, sort_keys=True, indent=4)
    
    for majorkey, obj in x.items():
        #print(majorkey, type(obj))
        if type(obj) is dict:
            for k, v in obj.items():
                #print("%s: %s" %(k,v))
                if k == "organization":
                    dir_name = obj[k]
                if k == "title":
                    name = obj[k]
        
    
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    abspath = os.path.abspath(dir_name)+"\\"
    file_name = abspath + name + ".txt"
    #print(file_name)
    f = open(file_name, "w", encoding = "UTF-8")
    
    #for clz, val in x.items():
        #print(clz, val)
    print(x["result"]["distribution"][0]["format"])
    print(x["result"]["distribution"][1]["format"])
    
    for k, v in x["result"].items():
        # print(k,type(v))
        if type(v) is list:
            f.write("%-25s: \n" %(k))
            for j in v:
                if type(j) is dict:
                    for distribution_key, distribution_value in j.items():
                        if distribution_key == "downloadURL" and distribution_value is not empty:
                            download_url = distribution_value
                        ''' to get the download file type
                        if distribution_key == "format" and distribution_value is not empty and j.get("downloadURL") is not None:
                            download_name = "."+distribution_value
                        '''
                        f.write("%30s: %s\n"%(distribution_key, distribution_value))
                else:
                    f.write("%30s\n"%(j))
        else:
            f.write("%-25s: %s\n" %(k,v))
    download_name = abspath + name + ".zip"
    # print(x["result"]["organization"])
    
    download_url = "http://www.ntbt.gov.tw/etwmain/download?sid=14f2a5235f3000006a40f74a70267f48"
    #download_url="http://data.gcis.nat.gov.tw/od/file?oid=01905E71-28D8-49ED-88CD-F3100F9DE5F2"
    #download file
    response = requests.get(download_url,stream=True)
    r = requests.head(download_url)
    print(download_url)
    
    fileType = response.headers.get("content-type","zip")
    file_name = response.headers.get("Content-Disposition")
    #file_name = file_name[file_name.find("filename")+len("filename="):len(file_name)]
    #file_name = file_name[file_name.rfind("."):len(file_name)]
    
    print(file_name.rstrip("\""))
    
    if ";" in fileType:
        fileType = fileType[fileType.index("/")+1:fileType.index(";")]
    else:
        fileType = fileType[fileType.index("/")+1:len(fileType)]

    if fileType == "octet-stream":
        fileType = "zip"
    
    print(fileType)
    
    with open(download_name, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024): 
            if chunk:
                f.write(chunk)
    #response = urllib.request.urlopen(download_url)
    #urllib.request.urlretrieve(download_url, download_name)
    
if __name__ == "__main__":
    for handler in logging.root.handlers:
        handler.addFilter(logging.Filter("root"))
    main()
