"""Cross-source check: do our auth answers cover the auth scheme Composio actually ships for that app?
Coarse: oauth2 present? static credential present?"""
import json,glob,sys
M=json.load(open("data/composio_match.json"));out={}
for P in ("pass0","pass1","pass2"):
    R=json.load(open("data/pass0.json")) if P=="pass0" else [r for f in sorted(glob.glob(f"data/{P}/cat*.json")) for r in json.load(open(f))]
    n=ok=0;miss=[]
    for r in R:
        tk={s:t for s,t in M[str(r["id"])].get("toolkits",{}).items() if not s.endswith("_mcp")}
        if not tk: continue
        c=set()
        for t in tk.values():
            for a in t["auth"]: c.add("oauth2" if "OAUTH" in a else "static")
        o={"oauth2" if a=="oauth2" else "none" if a=="none" else "static" if a!="unknown" else "unknown" for a in r["auth"]}
        n+=1
        if c<=o: ok+=1
        else: miss.append((r["id"],r["app"],sorted(c),r["auth"]))
    out[P]=dict(n=n,ok=ok,miss=miss);print(P,ok,n)
for m in out["pass2"]["miss"]: print("  ",m)
json.dump(out,open("data/cross_composio.json","w"),indent=1)
