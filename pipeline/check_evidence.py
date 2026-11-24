"""Machine check: does each evidence URL load, and is the cited snippet really on the page?
usage: check_evidence.py <pass dir>  -> data/evidence_<pass>.json"""
import json,sys,glob,re,html,pathlib
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0,str(pathlib.Path(__file__).parent))
from fetch import fetch
d=sys.argv[1].rstrip("/");name=pathlib.Path(d).name
recs=[r for f in sorted(glob.glob(d+"/cat*.json")) for r in json.load(open(f))]
def norm(s):
    s=s.replace("\\u003c","<").replace("\\u003e",">").replace('\\"','"').replace("\\n"," ")
    s=html.unescape(html.unescape(s)); s=re.sub(r"<[^>]+>"," ",s)
    return re.sub(r"[^a-z0-9一-鿿]+"," ",s.lower()).strip()
def chk(x):
    r,e=x;u=e.get("url") or "";m=e.get("match") or ""
    if not u.startswith("http"): st="bad_url"
    else:
        s,b,f=fetch(u)
        if s!=200: st="http_%s"%s
        elif not m: st="no_snippet"
        else:
            n=norm(b); st="match" if norm(m) in n or norm(m).replace(" ","") in n.replace(" ","") else "snippet_not_found"
    return dict(id=r["id"],app=r["app"],field=e.get("field"),url=u,status=st)
with ThreadPoolExecutor(12) as ex: out=list(ex.map(chk,[(r,e) for r in recs for e in r["evidence"]]))
json.dump(out,open(f"data/evidence_{name}.json","w"),indent=1)
from collections import Counter
print(len(recs),"records",len(out),"evidence",Counter(o["status"] for o in out))
