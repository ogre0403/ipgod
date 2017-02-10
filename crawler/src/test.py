import DBUtil
from pg import DB

conn = DBUtil.createConnection()

q = "SELECT COUNT(*) from resource_metadata WHERE package_name = '1' AND resource_id = '2' AND url = '3' AND format = '4'"

res = conn.query(q)
print(DBUtil.isDatasetEmpty(conn) )