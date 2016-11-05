#!/bin/python
# -*- coding: utf-8 -*-
import logging
import psycopg2
import time
import datetime

LOGGING_FILE = 'ipgod-od2ckan.log'
logging.basicConfig(filename=LOGGING_FILE,
                    level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(filename)s_%(lineno)d  : %(message)s')
logger = logging.getLogger('root') 

class ipgoddb():
    def __init__(self):
        self.conn = 0
        try:
            self.conn = psycopg2.connect("dbname='ipgod' user='thomas' host='localhost' password='nchcnchc'")
        except:
            logger.warn("connect db error")
        self.cur = self.conn.cursor()

    def get_pkgs(self):
        try:
            #self.cur.execute("SELECT package_name, status, datetime from import where  datetime > CURRENT_TIMESTAMP - INTERVAL '6000 secs' and status=200")
            self.cur.execute("SELECT package_name, fileid from ckan_download  where status=200 and processed=FALSE")
        except:
            logger.warn("select error")
        pkgs = []
        rows = self.cur.fetchall()
        for row in rows:
	    pkg = row[0].rstrip()
            pkgs.append(pkg)
        return pkgs

    def import_done(self, package, fileid):
        try:
            self.cur.execute("UPDATE ckan_download SET processed=TRUE where package_name like %s and fileid like %s", (package, fileid))
            self.conn.commit()
        except:
            logger.warn("import done error")


    def import_pkg(self, package, status):
        #self.cur.execute("SELECT COUNT(*) from import where package_name like %s", (package,))
	#count_pkg = self.cur.fetchall()
	#pkg_c = count_pkg[0][0]
	pkg_c = 0
	if pkg_c > 0:
	    logger.warn("package %s exist") % package
	else:
	    try:
		ct = datetime.datetime.now()
		self.cur.execute("INSERT INTO import (package_name, status, datetime) VALUES (%s, %s, %s)", (package, status, ct))
		self.conn.commit()
	    except:
		logger.warn("import db error")


    def update_pkg(self, package, status):
        try:
            self.cur.execute("UPDATE import SET status=%s where package_name like %s", (status, package))
            self.conn.commit()
        except:
            logger.warn("update error")

    def log_package(self, package, log):
        try:
            self.cur.execute("UPDATE import SET comment=%s where package_name like %s", (log, package))
            self.conn.commit()
        except:
            logger.warn("log comment error")

    def remove_pkg(self, package):
        try:
            self.cur.execute("DELETE from import  where package_name like %s", package)
            self.conn.commit()
        except:
            logger.warn("remove error")
