import psycopg2
import sys
import const
import logging

logging.basicConfig(#filename=LOGGING_FILE,
                    level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(filename)s_%(lineno)d  : %(message)s')
logger = logging.getLogger('root')

class PostgresSQL():
    def __init__(self,host, dbname, user, password):
        #Define our connection string
        conn_string = "host='"+host+"' dbname='"+dbname+"' user='"+user+"' password='"+password+"'"
     
        # print the connection string we will use to connect
        logger.info("Connecting to database\n    ->%s" % (conn_string))
     
        # get a connection, if a connect cannot be made an exception will be raised here
        conn = psycopg2.connect(conn_string)
        conn.commit()
        # conn.cursor will return a cursor object, you can use this cursor to perform queries
        self.cursor = conn.cursor()
        
        logger.info("Connected!")
        
    
    def insertData(self,resourceID, statusCode):
        self.cursor.execute("INSERT INTO public."+ const.table+" (resourceid, downloadstatuscode) VALUES ('"+resourceID+"',"+ str(statusCode)+");COMMIT;")
        
        self.cursor.execute("SELECT * FROM public."+const.table )
        
        self.rows  = self.cursor.fetchall()
        
    def printData(self):
        for element in self.rows:
            logger.info(element)
        
    
def main():
    x = PostgresSQL(const.host, const.dbname, const.user, const.password)
    x.insertData("TEST45678", 404)
    x.printData()
    
if __name__ == "__main__":
    
    main()