#!/bin/python
# -*- coding: utf-8 -*-
import logging
import psycopg2
import time
import datetime
import ConfigParser

LOGGING_FILE = 'ipgod-od2ckan.log'
logging.basicConfig(filename=LOGGING_FILE,
                    level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(filename)s_%(lineno)d  : %(message)s')
logger = logging.getLogger('root') 

config = ConfigParser.ConfigParser()
config.read('config.ini')
class ipgoddb():
    def __init__(self):
        self.conn = 0
	db = config.get('db', 'database')
	user = config.get('db', 'user')
	server = config.get('db', 'host')
	password = config.get('db', 'password')

        try:
            self.conn = psycopg2.connect("dbname=%s user=%s host=%s password=%s" % (db, user, server, password))
        except:
            logger.warn("connect db error")
        self.cur = self.conn.cursor()

    def get_pkgs(self):
        try:
            #self.cur.execute("SELECT package_name, status, datetime from import where  datetime > CURRENT_TIMESTAMP - INTERVAL '6000 secs' and status=200")
            self.cur.execute("SELECT package_name, file_id from ckan_download  where status=200 and processed=FALSE")
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
            self.cur.execute("UPDATE ckan_download SET processed=TRUE where package_name like %s and file_id like %s", (package, fileid))
            self.conn.commit()
        except:
            logger.warn("import done error")

    def exist(self, package, fileid):
	print package
        self.cur.execute("SELECT COUNT(*) from import where package_name like %s and file_id = %s", (package, fileid))
	count_pkg = self.cur.fetchall()
	pkg_c = count_pkg[0][0]
        return pkg_c

    def import_pkg(self, package, fileid, status):
        pkg_c = self.exist(package, fileid)
	if pkg_c > 0:
	    logger.warn("package %s and resource %s exist" % (package, fileid))
	else:
	    try:
		ct = datetime.datetime.now()
		self.cur.execute("INSERT INTO import (package_name, file_id, status, datetime) VALUES (%s, %s, %s, %s)", (package, fileid, status, ct))
		self.conn.commit()
	    except:
		logger.warn("import db error")

    def get_status(self, package, fileid):
        
        pkg_c = self.exist(package, fileid)
        if pkg_c > 0:
            self.cur.execute("SELECT status from import where package_name like %s and file_id = %s", (package, fileid))
            count_status = self.cur.fetchall()
            status = count_status[0][0]
        else:
            status = 0
        print status
        return status


    def update_pkg(self, package, fileid, status):
        try:
            self.cur.execute("UPDATE import SET status=%s where package_name like %s and file_id = %s", (status, package, fileid))
            self.conn.commit()
        except:
            logger.warn("update error")

    def log_package(self, package, fileid, log):
        try:
            self.cur.execute("UPDATE import SET comment=%s where package_name like %s, and = like %s", (log, package, fileid))
            self.conn.commit()
        except:
            logger.warn("log comment error")

    def remove_pkg(self, package, fileid):
        try:
            self.cur.execute("DELETE from import  where package_name like %s and file_id = %s", package, fileid)
            self.conn.commit()
        except:
            logger.warn("remove error")
