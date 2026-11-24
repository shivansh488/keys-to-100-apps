"""pass 2 + logged supervisor overrides -> data/final.json and data/patterns.json"""
import json,glob
from collections import Counter,defaultdict
R={r["id"]:r for f in glob.glob("data/pass2/*.json") for r in json.load(open(f))}
A={a["id"]:a for a in json.load(open("data/apps.json"))};M=json.load(open("data/composio_match.json"))
OV=[(91,dict(access="self_serve_trial",mcp="none_found",mcp_url="",access_notes="Enterprise API: 14-day trial, then paid, minimum 15 licences. (A separate consumer preview API is free and has an MCP server.)"),"Brief's hint names the Gemini Enterprise API; pass 2 had answered for the consumer preview."),
(40,dict(mcp="community"),"Pass 2 notes say community servers exist; label should be community."),
(18,dict(main_blocker="none"),"Trial carries the API, so paid plan is a later cost rather than a build blocker."),
(38,dict(mcp="none_found"),"Vendor page opened in browser says the server is announced and not launched yet.")]
log=[]
for i,ch,why in OV:
    for k,v in ch.items(): log.append(dict(id=i,app=R[i]["app"],field=k,frm=R[i].get(k),to=v,why=why));R[i][k]=v
out=[]
for i in sorted(R):
    r=dict(R[i]);r["category"]=A[i]["category"];r["hint"]=A[i]["hint"];r["composio"]=M[str(i)]["slugs"];r["composio_toolkits"]=M[str(i)].get("toolkits",{})
    c=r.get("confidence") or {};r["min_conf"]=min([c.get(k,0.5) for k in("auth","access","api","mcp")]);out.append(r)
json.dump(out,open("data/final.json","w"),indent=1,ensure_ascii=False);json.dump(log,open("data/overrides.json","w"),indent=1,ensure_ascii=False)
G={"self_serve_free":"free","self_serve_trial":"trial","paid_plan":"paid","admin_or_app_approval":"approval","partner_or_sales":"sales","no_api":"none"}
P={}
P["n"]=len(out)
for k in("access","mcp","verdict","main_blocker","prod_gate","api_breadth"): P[k]=Counter(r[k] for r in out)
st=lambda r:{"static" if x in("api_key","token") else x for x in r["auth"]}
P["auth_any"]=Counter(x for r in out for x in set(r["auth"]));P["auth_static"]=sum("static" in st(r) for r in out);P["auth_oauth"]=sum("oauth2" in r["auth"] for r in out)
P["auth_both"]=sum("oauth2" in r["auth"] and "static" in st(r) for r in out);P["oauth_only"]=[r["app"] for r in out if st(r)=={"oauth2"}];P["static_no_oauth"]=sum("static" in st(r) and "oauth2" not in r["auth"] for r in out)
P["cat"]={c:dict(Counter(G[r["access"]] for r in out if r["category"]==c),oauth=sum("oauth2" in r["auth"] for r in out if r["category"]==c),static=sum("static" in st(r) for r in out if r["category"]==c),build=sum(r["verdict"]=="build_now" for r in out if r["category"]==c),second=sum(r["prod_gate"] in("app_review","partner_program","security_review") for r in out if r["category"]==c),mcp=sum(r["mcp"]=="official" for r in out if r["category"]==c)) for c in dict.fromkeys(r["category"] for r in out)}
ss=[r for r in out if r["access"].startswith("self")]
P["self_serve"]=len(ss);P["ss_second_gate"]=sum(r["prod_gate"] in("app_review","partner_program","security_review") for r in ss);P["ss_unknown"]=sum(r["prod_gate"]=="unknown" for r in ss)
for v in("build_now","build_with_caveat","needs_outreach"): P["list_"+v]=[(r["app"],r["access"],r["prod_gate"],r["main_blocker"],bool(r["composio"])) for r in out if r["verdict"]==v and (v!="build_now")]
P["gap_build_now"]=[(r["app"],r["access"],r["auth"],r["prod_gate"],r["mcp"],r["min_conf"]) for r in out if r["verdict"]=="build_now" and not r["composio"]]
P["gap_other"]=[(r["app"],r["verdict"],r["main_blocker"]) for r in out if r["verdict"]!="build_now" and not r["composio"]]
P["mcp_prod_gated"]=[r["app"] for r in out if r["mcp"]=="official" and r["verdict"]!="build_now"]
P["mcp_none"]=[(r["app"],r["mcp"]) for r in out if r["mcp"]!="official"]
P["openapi"]=sum(r.get("openapi_public") is True for r in out)
P["low_conf"]=[(r["app"],r["min_conf"]) for r in out if r["min_conf"]<.6]
json.dump(P,open("data/patterns.json","w"),indent=1)
for k,v in P.items(): print(k,":",dict(v) if isinstance(v,Counter) else v)
