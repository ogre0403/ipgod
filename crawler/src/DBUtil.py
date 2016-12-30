from pg import DB
import const
import config
import logging

q_string1_template = "select max(download_time at time zone 'Asia/Taipei') as last from {} "
q_string2_template = "INSERT INTO {} VALUES ( '{}', '{}',TIMESTAMP '{}' at time zone 'Asia/Taipei', {}, False, False)"


logger = logging.getLogger(__name__)

def createConnection():
    """
    Create PostgreSQL connection with configured db/port/user/password
    :return: PostgreSQL connection to const.DB_DATABASE
    """
    try:
        conn = DB(dbname=const.DB_DATABASE,
                  host=config.db_ip,
                  port=config.db_port,
                  user=config.db_user,
                  passwd=config.db_password)
        return conn
    except Exception as e:
        logging.exception("Create DB connection error!!")


def getLastUpdateEpoch(conn):
    """
    Find out last update timestamp from PostgreSQL with format 2016-11-21 12:00:02
    :param conn: previous created PostgreSQL connection
    :return: Last update timestamp or None
    """
    qs = q_string1_template.format(const.DB_TABLE)
    try:
        q = conn.query(qs)
        """
        To aviod empty DB
        """
        if q.namedresult()[0].last is None:
            return "NA"
        else:
            return q.namedresult()[0].last.strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        logging.exception("Query DB for last fetch error!!")


def insertDownloadResult(conn, package_name, file_id, timeStr, status):
    """
    Write download result status into database.
    :param conn: PostgreSQL connection
    :param resource_id: String, with format A59000000N-000229, which has fixed length 17
    :param file_id: String, with format 002, which has fixed length 3
    :param timeStr: String, with 2016-11-22 12:10:00 format
    :param status: small int
    :return:
    """
    qs = q_string2_template.format(const.DB_TABLE, package_name, file_id, timeStr, status)
    try:
        conn.query(qs)
    except Exception as e:
        logging.exception("Insert new record error !!")

def closeConnection(conn):
    """
    Close PostgreSQL connection
    :param conn: previous created PostgreSQL connection
    """
    try:
        conn.close()
    except Exception as e:
        logging.exception("Close DB connection error!!")
