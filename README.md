# ipgod

### Create database and table
```SQL
CREATE TABLE ckan_download (
	resource_id CHAR(21) PRIMARY KEY,
	download_time TIMESTAMP WITH TIME ZONE,
	status SMALLINT
);
```

### Install required modules first.
```bash
$ pip install schedule
$ pip install requests
$ pip install PyGreSQL
```

###Change configuration in config.py
```python
FetchHistory=True # start a thread to get history data since last update

db_ip = "localhost"         # IP of Database which having download status 
db_port=5432                # Port of Database which having download status 
db_user="ckan_default"      # username of Database which having download status 
db_password="ckan_passwd"   # password of Database which having download status
 
DOWNLOAD_PATH = 'D:/dataset' # Where to place download open data resource
```


