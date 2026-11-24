import json,sys;sys.path.insert(0,"pipeline")
from fetch import fetch
for x in json.load(open("data/evidence_pass2.json")):
    if x["status"].startswith("http_0"): print(fetch(x["url"],force=True)[0],x["url"])
