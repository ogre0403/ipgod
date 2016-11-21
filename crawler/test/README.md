# PostgreSQL Docker Environment for Testing DBUtil.py
ref: https://docs.docker.com/engine/examples/postgresql_service/

### Build PostgreSQL Docker image

```bash
$ cd test
$ docker build -t eg_postgresql .
```

### Launch PostgreSQL server and client docker container

```bash
# Start server container
$ docker run --rm -P --name pg_test eg_postgresql

# Start clinet container
$ docker run --rm -t -i --link pg_test:pg eg_postgresql bash
postgres@7ef98b1b7243:/$ psql -h $PG_PORT_5432_TCP_ADDR -p $PG_PORT_5432_TCP_PORT -d ckan_default -U ckan_default -W
Password for user ckan_default: <ckan_passwd>
```


### Create testing ckan_download Table and insert testing data 

```SQL
--- Make Testing Table 
CREATE TABLE ckan_download (
	resource_id CHAR(21) PRIMARY KEY,
	download_time TIMESTAMP WITH TIME ZONE,
	status SMALLINT
);

--- Insert Testing data with linux timestamp
INSERT INTO ckan_download VALUES ('A59000000N-000229-001',　TIMESTAMP 'epoch' + 1479700800 * INTERVAL '1 second', 200);
INSERT INTO ckan_download VALUES ('A59000000N-000229-002',　TIMESTAMP 'epoch' + 1479700801 * INTERVAL '1 second', 404);
INSERT INTO ckan_download VALUES ('A59000000N-000229-003',　TIMESTAMP 'epoch' + 1479700802 * INTERVAL '1 second', 405);

--- Select data and convert download_time to UTC+8(i.e. Asia/Taipei) time zone. 
SELECT resource_id, download_time at time zone 'Asia/Taipei' , status  FROM ckan_download;
```

