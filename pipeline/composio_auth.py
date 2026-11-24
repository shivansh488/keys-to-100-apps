"""Cross-source check: auth schemes + managed OAuth + tool counts from Composio's public toolkit pages."""
import json,re,sys,pathlib
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0,"pipeline")
from fetch import fetch
M=json.load(open("data/composio_match.json"))
def one(s):
    st,b,_=fetch(f"https://docs.composio.dev/toolkits/{s}.md")
    if st!=200:return s,None
    a=re.search(r"\*\*Auth:\*\*\s*(.+)",b);m=re.search(r"managed OAuth available\?\*\*\s*(.+)",b)
    t=re.search(r"\*\*Tools?:?\*\*:?\s*(\d+)",b) 
    return s,dict(auth=[x.strip() for x in a.group(1).split(",")] if a else [],managed=m.group(1).strip() if m else None,tools=int(t.group(1)) if t else len(re.findall(r"(?m)^\s*(?:\||###|-)\s*`?[A-Z0-9]+_[A-Z0-9_]+",b)))
sl=sorted({s for v in M.values() for s in v["slugs"]})
with ThreadPoolExecutor(8) as ex: D=dict(ex.map(one,sl))
for v in M.values(): v["toolkits"]={s:D[s] for s in v["slugs"] if D[s]}
json.dump(M,open("data/composio_match.json","w"),indent=1)
from collections import Counter
print(len(sl),sum(d is None for d in D.values()),Counter(x for d in D.values() if d for x in d["auth"]),Counter(d["managed"] for d in D.values() if d))
