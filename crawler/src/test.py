import json
import requests

URL = "http://data.gov.tw/api/v1/rest/dataset/345000000G-000001"

r = requests.get(URL, stream=True,verify=False,headers={'Connection':'close'});

x = json.loads(r.text)

print(x['success'])