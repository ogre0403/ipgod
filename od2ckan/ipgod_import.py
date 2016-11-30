import psycopg2
from datetime import datetime

class ipgoddb():
    def __init__(self)
        try:  
            self.conn = psycopg2.connect("dbname='ipgod' user='thomas' host='localhost' password='okok7480'")
            self.cur = conn.cursor()
        except:
            print "connect db error"

    def get_pkgs(self):
        try:  
            self.cur.execute("SELECT package_name, status, datetime from import where  datetime > CURRENT_TIMESTAMP - INTERVAL '60 secs' and status == 0")
            rows = self.cur.fetchall()
        except:
            print "select error"
        pkgs = []
        for row in rows:
                pkgs.append(row['package_name'])
        return pkgs

    def update_pkg(self, package, status):
        try:  
            self.cur.execute("UPDATE import SET status = %s where package_name = %s", (statue, package))
            self.conn.commit()
        except:
            print "update error"

    def log_package(self, package, log):
        try:  
            self.cur.execute("UPDATE import SET comment = %s where package_name = %s", (log, package))
            self.conn.commit()
        except:
            print "log comment error"

    def remove_pkgs(self):
        try:  
            self.cur.execute("DELETE from import  where package_name = %s", package)
            self.conn.commit()
        except:
            print "remove error"


class importd():
