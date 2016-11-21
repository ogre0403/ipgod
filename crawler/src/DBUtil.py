from pg import DB
import const
import config


def createConnection():
    """
    Create PostgreSQL connection with configured db/port/user/password
    :return: PostgreSQL connection to const.DB_DATABASE
    """
    conn = DB(dbname=const.DB_DATABASE,
              host=config.db_ip,
              port=config.db_port,
              user=config.db_user,
              passwd=config.db_password)
    return conn


def getLastUpdateEpoch(conn):
    # TODO
    """
    Find out last update timestamp from PostgreSQL
    :param conn: previous created PostgreSQL connection
    :return: Last update timestamp
    """
    conn.query()

    return -1


def closeConnection(conn):
    """
    Close PostgreSQL connection
    :param conn: previous created PostgreSQL connection
    """
    conn.close()

