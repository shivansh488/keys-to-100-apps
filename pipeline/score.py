"""Score every available pass against the locked gold sample. auth static = api_key or token."""
import json,glob,os,sys
G=json.load(open("data/gold/gold.json"))
def load(p):
    if p=="pass0":
        return {r["id"]:dict(r,auth=["api_key" if a=="static_key" else a for a in r["auth"]]) for r in json.load(open("data/pass0.json"))}
    return {r["id"]:r for f in sorted(glob.glob(f"data/{p}/cat*.json")) for r in json.load(open(f))}
def st(a): return {"static" if x in("api_key","token") else x for x in a}
def judge(r,g):
    a=st(r["auth"]); must,may=set(g["must"]),set(g["may"])
    return dict(auth=must<=a and a<=must|may,access=r["access"] in g["access"],mcp=r["mcp"] in g["mcp"],verdict=r["verdict"] in g["verdict"])
if __name__=="__main__":
    out={}
    for p in ("pass0","pass1","pass2"):
        R=load(p)
        if not R: continue
        rows=[]
        for i,g in G.items():
            r=R.get(int(i))
            if not r: continue
            j=judge(r,g); rows.append(dict(id=int(i),app=r["app"],**{k:dict(ok=j[k],got=r[k]) for k in j}))
        tot={k:sum(x[k]["ok"] for x in rows) for k in("auth","access","mcp","verdict")}
        out[p]=dict(n=len(rows),by_field=tot,correct=sum(tot.values()),claims=4*len(rows),rows=rows)
        print(p,len(rows),tot,f"{sum(tot.values())}/{4*len(rows)} = {sum(tot.values())/(4*len(rows)):.1%}")
        for x in rows:
            for k in tot:
                if not x[k]["ok"]: print("   MISS",x["app"],k,"got",x[k]["got"],"gold",G[str(x["id"])]["must" if k=="auth" else k])
    json.dump(out,open("data/scores.json","w"),indent=1)
