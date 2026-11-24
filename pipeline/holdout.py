"""Holdout labels read by the supervising agent in a live browser AFTER pass 2 finished, without opening pass 2 records for
these apps (agent summary reports mentioning Podio, Gladly, Aircall, systeme.io, Coda, Ramp and Devin had been seen).
None = could not be settled from primary pages in this check; excluded from the score, never guessed."""
import json,sys
sys.path.insert(0,"pipeline");import score
F="self_serve_free";S="static"
L={6:dict(auth=(["oauth2"],["basic",S,"other"]),mcp=["official"],urls=["https://developers.podio.com/authentication","https://www.progress.com/podio/documentation/using-podio/podio-mcp-server"]),
20:dict(auth=([],["basic",S]),access=["partner_or_sales"],verdict=["needs_outreach"],urls=["https://developer.gladly.com/rest/"]),
29:dict(auth=(["basic","oauth2"],[S]),urls=["https://developers.aircall.io/api-references"]),
37:dict(auth=([S],[]),access=[F],mcp=["official"],verdict=["build_now"],urls=["https://developer.systeme.io/reference/api","https://systeme.io/pricing","https://systeme.io/mcp"]),
45:dict(auth=([S,"oauth2"],["other"]),mcp=["none_found","community"],urls=["https://developer.adobe.com/commerce/webapi/get-started/authentication/"]),
57:dict(access=[F,"self_serve_trial"],mcp=["official"],verdict=["build_now"],urls=["https://brightdata.com/ai/mcp-server"]),
63:dict(auth=(["oauth2",S],[]),mcp=["official"],urls=["https://docs.netlify.com/api-and-cli-guides/api-guides/get-started-with-api/"]),
78:dict(auth=([S],["oauth2"]),access=[F],verdict=["build_now"],urls=["https://coda.io/developers/apis/v1"]),
89:dict(auth=(["oauth2"],["basic"]),mcp=["official"],urls=["https://docs.ramp.com/developer-api/v1/authorization"]),
96:dict(urls=["https://docs.devin.ai/api-reference/overview"])}
assert sorted(L)==sorted(json.load(open("data/holdout_ids.json")))
res={}
for P in("pass0","pass1","pass2"):
    R=score.load(P);n=ok=0;miss=[]
    for i,g in L.items():
        for k in("auth","access","mcp","verdict"):
            if k not in g: continue
            n+=1;r=R[i]
            if k=="auth":
                a=score.st(r["auth"]);m,y=map(set,g["auth"]);good=m<=a and a<=m|y and a!=set()
            else: good=r[k] in g[k]
            ok+=good
            if not good: miss.append((r["app"],k,r[k],g[k]))
    res[P]=dict(n=n,ok=ok,miss=miss);print(P,ok,n,miss if P!="pass0" else "")
json.dump(dict(scores=res,labels={str(k):v for k,v in L.items()},settled=res["pass2"]["n"],possible=40),open("data/holdout.json","w"),indent=1)
