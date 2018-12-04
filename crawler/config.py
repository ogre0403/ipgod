# control launch crawler.fatchList() or not
FetchHistory = False

# if crawler.fatchList() = True, fetch dataset from History_Time to now
History_Time = "2018-10-18 11:30:00"

# the url of data_gov to query UPDATED dataset list
MODIFIED_URL_PREFIX = 'http://data.gov.tw/api/v1/rest/dataset?modified='

# the url of data_gov to query dataset information
METADATA_URL_PREFIX = 'http://data.gov.tw/api/v1/rest/dataset/'

# the DIR path where data download
DOWNLOAD_PATH = './data'

# the File path where dataset list indicate, if FetchHistory = False, program will only fetch dataset in this file
LIST_PATH = './list/dataid_list.json'

# the number of downloader threads
downloader_num = 1

# log config file to setup python logging
logging_configure_file = "logging.ini"

# set request timeout limit ( not download time)(in second)
request_timeout = 120

# take a rest for ckan (in second)
timesleep_add_organization = 1
timesleep_add_dataset = 1
timesleep_add_resource = 0.5


## [od2ckan]
ckanurl="http://ipgod.nchc.org.tw"
ckan_key="02285f49-a9a7-4809-a42c-a568547511ec"
root_path="./data"
#root_path="/home/thomas/data_download/"

## deprecated,  Database and table name
# DB_DATABASE = "ipgod"
# DB_TABLE = "ckan_download"
# db_ip = "localhost"
# db_port = 5432
# db_user = "ckan_default"
# db_password = "ckan_passwd"

## deprecated
#update_interval_sec = 60

## deprecated, to control non-stoppable downloader to download
#download_interval_sec = 6

## deprecated ,
#fetcher_num = 1