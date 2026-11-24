"""Build site/index.html (static HTML, works without JS) + site/data.json + site/data.csv from data/*."""
import json,html,csv,pathlib,glob
from collections import Counter
e=html.escape;J=lambda p:json.load(open(p))
F=J("data/final.json");P=J("data/patterns.json");S=J("data/scores.json");H=J("data/holdout.json");X=J("data/cross_composio.json");G=J("data/gold/gold.json")
E1=Counter(x["status"]=="match" for x in J("data/evidence_pass1.json"));E2=Counter(x["status"]=="match" for x in J("data/evidence_pass2.json"));OV=J("data/overrides.json")
hc=list(csv.DictReader(open("data/human_checks.csv")));done=sum(x["status"]=="done" for x in hc)
AC={"self_serve_free":("free","Free"),"self_serve_trial":("trial","Trial"),"paid_plan":("paid","Paid plan"),"admin_or_app_approval":("appr","Vendor approval"),"partner_or_sales":("sales","Sales or partner"),"no_api":("none","No remote API")}
VD={"build_now":("go","Build now"),"build_with_caveat":("mid","Caveat"),"needs_outreach":("stop","Outreach"),"not_buildable":("stop","Not buildable")}
GT={"none":"","app_review":"App review","partner_program":"Partner program","security_review":"Security review","unknown":"Not settled","paid_plan":"Paid plan"}
AU={"oauth2":"OAuth2","api_key":"API key","token":"Token","basic":"Basic","other":"Other","none":"None"}
BL={"none":"","paid_plan":"Paid plan","app_review":"App review","partner_or_sales":"Sales or partner gate","no_public_api":"No public API","local_only":"Runs locally only","docs_gated":"Docs gated","narrow_api":"Narrow API","other":"Other"}
pct=lambda a,b:f"{100*a/b:.1f}".rstrip("0").rstrip(".")+"%"
# slim export
slim=[{k:r.get(k) for k in("id","app","category","one_liner","auth","auth_notes","access","access_notes","prod_gate","api_types","api_breadth","openapi_public","mcp","mcp_url","mcp_notes","verdict","main_blocker","blocker_notes","min_conf","needs_browser","unresolved")}|{"composio_toolkits":r["composio"],"evidence":[{"field":x["field"],"url":x["url"]} for x in r["evidence"]]} for r in F]
pathlib.Path("site").mkdir(exist_ok=True);json.dump(slim,open("site/data.json","w"),indent=0,ensure_ascii=False)
with open("site/data.csv","w",newline="") as f:
    w=csv.writer(f);w.writerow(["id","app","category","one_liner","auth","access","prod_gate","api_types","api_breadth","mcp","verdict","main_blocker","in_composio","evidence"])
    for r in slim: w.writerow([r["id"],r["app"],r["category"],r["one_liner"],"|".join(r["auth"]),r["access"],r["prod_gate"],"|".join(r["api_types"]),r["api_breadth"],r["mcp"],r["verdict"],r["main_blocker"],bool(r["composio_toolkits"])," ".join(x["url"] for x in r["evidence"])])
# chart
def bar(c):
    d=P["cat"][c];seg=""
    for k,(cl,lab) in (("free",AC["self_serve_free"]),("trial",AC["self_serve_trial"]),("paid",AC["paid_plan"]),("approval",AC["admin_or_app_approval"]),("sales",AC["partner_or_sales"]),("none",AC["no_api"])):
        n=d.get(k,0)
        if n: seg+=f'<span class="seg s-{cl}" style="flex:{n}" title="{lab}: {n} of 10"><b>{n}</b></span>'
    return f'<div class="barrow"><span class="barlab">{e(c)}</span><span class="bar" role="img" aria-label="{e(c)}: '+", ".join(f"{d.get(k,0)} {k}" for k in("free","trial","paid","approval","sales","none") if d.get(k))+f'">{seg}</span></div>'
cats=sorted(P["cat"],key=lambda c:-(P["cat"][c].get("free",0)+P["cat"][c].get("trial",0)+P["cat"][c].get("free",0)/100))
bars="".join(bar(c) for c in cats)
leg="".join(f'<span><i class="dot s-{cl}"></i>{lab}</span>' for cl,lab in AC.values())
# rows
rows=""
for r in F:
    ac=AC[r["access"]];vd=VD[r["verdict"]];ev={}
    for x in r["evidence"]: ev.setdefault(x["field"],x["url"])
    links=" ".join(f'<a href="{e(ev[k])}">{k}</a>' for k in("auth","access","api","mcp") if k in ev)
    api="/".join(t.upper() if t!="graphql" else "GraphQL" for t in r["api_types"] if t in("rest","graphql","soap","grpc","sdk","cli","none"))
    mc={"official":"Official","community":"Community","none_found":"None found"}[r["mcp"]];mc=f'<a href="{e(r["mcp_url"])}">{mc}</a>' if (r["mcp_url"] or "").startswith("http") and r["mcp"]=="official" else mc
    unk='<span class="tag warn" title="At least one answer below 60% confidence">low confidence</span>' if r["min_conf"]<.6 else ""
    note=r["access_notes"] or "";bn=r["blocker_notes"] if r["main_blocker"]!="none" else ""
    rows+=f'''<tr data-c="{e(r["category"])}" data-a="{ac[0]}" data-v="{vd[0]}" data-m="{r["mcp"]}" data-k="{"in" if r["composio"] else "gap"}" data-u="{" ".join(r["auth"])}"><td class="num">{r["id"]}</td><th scope="row">{e(r["app"])}{unk}<small>{e(r["one_liner"])}</small></th><td><span class="v v-{vd[0]}">{vd[1]}</span><small>{e(BL[r["main_blocker"]])}</small></td><td><i class="dot s-{ac[0]}"></i>{ac[1]}<small>{e(note)}</small></td><td>{"".join(f'<span class="tag">{AU[a]}</span>' for a in r["auth"])}</td><td>{e(GT.get(r["prod_gate"],r["prod_gate"]))or "None"}</td><td>{api}<small>{r["api_breadth"]}{", OpenAPI" if r["openapi_public"] else ""}</small></td><td>{mc}</td><td>{"Yes" if r["composio"] else "<b>No</b>"}</td><td class="ev">{links}</td></tr>'''
def lst(items,f): return "".join(f"<li>{f(x)}</li>" for x in items)
by={r["app"]:r for r in F}
gap=lst(P["gap_build_now"],lambda x:f'<b>{e(x[0])}</b> <span>{", ".join(AU[a] for a in x[2] if a!="other")}, {AC[x[1]][1].lower()}</span>')
cav=lst(P["list_build_with_caveat"],lambda x:f'<b>{e(x[0])}</b> <span>{BL[x[3]].lower()}</span>')
out=lst(P["list_needs_outreach"],lambda x:f'<b>{e(x[0])}</b> <span>{BL[x[3]].lower()}</span>')
# scores
tot=lambda p:(S[p]["correct"],S[p]["claims"]);T=[("Pass 0","Keyless rules crawl",*tot("pass0"),H["scores"]["pass0"],X["pass0"]),("Pass 1","Research agents",*tot("pass1"),H["scores"]["pass1"],X["pass1"]),("Pass 2","Adversarial verifiers",*tot("pass2"),H["scores"]["pass2"],X["pass2"])]
acc="".join(f'<tr><th scope="row">{a}<small>{b}</small></th><td><span class="meter"><i style="width:{100*c/d:.1f}%"></i></span><b>{pct(c,d)}</b><small>{c} of {d}</small></td><td><b>{pct(h["ok"],h["n"])}</b><small>{h["ok"]} of {h["n"]}</small></td><td><b>{pct(x["ok"],x["n"])}</b><small>{x["ok"]} of {x["n"]}</small></td></tr>' for a,b,c,d,h,x in T)
fld="".join(f'<tr><th scope="row">{n}</th>'+"".join(f'<td>{S[p]["by_field"][k]}/20</td>' for p in("pass0","pass1","pass2"))+"</tr>" for k,n in(("auth","Auth"),("access","Access gate"),("mcp","MCP"),("verdict","Verdict")))
why={("Zendesk","mcp"):"Fixed. Vendor FAQ shows an early-access MCP server since 10 Nov 2026.",("Vonage","auth"):"Still counted wrong. Agent said Basic plus JWT; gold wants the key and secret listed as a static key.",("LinkedIn Ads","verdict"):"Fixed by a clearer rule: vendor approval means outreach.",("Pinterest","verdict"):"Fixed by the same rule.",("Pinterest","mcp"):"The gold label was wrong. The vendor page says the server has not launched. Final data says none found.",("Ecwid","mcp"):"Fixed. A docs-search MCP does not act on the product.",("MrScraper","auth"):"Still counted wrong. Agent also listed x402 pay-per-call as other.",("MrScraper","access"):"Fixed. Pricing FAQ says a 7-day, card-required trial. Another vendor page disagrees.",("Clay","access"):"Fixed. Docs say the API is on every plan, including free. Pricing FAQ still disagrees.",("Clay","verdict"):"Fixed with the access change."}
miss="".join(f'<tr><th scope="row">{e(x["app"])}</th><td>{k}</td><td>{e(", ".join(x[k]["got"]) if isinstance(x[k]["got"],list) else x[k]["got"])}</td><td>{e(why.get((x["app"],k),""))}</td></tr>' for x in S["pass1"]["rows"] for k in("auth","access","mcp","verdict") if not x[k]["ok"])
hits="".join(f'<tr><th scope="row">{e(x["app"])}</th>'+"".join(f'<td class="{"ok" if x[k]["ok"] else "no"}">{"Hit" if x[k]["ok"] else "Miss"}</td>' for k in("auth","access","mcp","verdict"))+f'<td class="ev">'+" ".join(f'<a href="{e(u)}">{i+1}</a>' for i,u in enumerate(G[str(x["id"])]["urls"]))+"</td></tr>" for x in S["pass2"]["rows"])
hcr="".join(f'<li><b>{e(x["app"])}</b> {e(x["question"])} <a href="{e(x["open_this"])}">open</a></li>' for x in hc)
ovr="".join(f'<li><b>{e(o["app"])}</b>, {e(o["field"])}: {e(o["why"])}</li>' for o in OV if o["field"]!="access_notes" and o["field"]!="mcp_url")
co=''.join(f'<option value="{e(c)}">{e(c)}</option>' for c in P["cat"])
tpl=open("pipeline/page_template.html").read()
for k,v in dict(BARS=bars,LEG=leg,ROWS=rows,GAP=gap,CAV=cav,OUT=out,ACC=acc,FLD=fld,MISS=miss,HITS=hits,HC=hcr,HCN=f"{done} of {len(hc)}",OVR=ovr,CATS=co,NB=str(P["verdict"]["build_now"]),NC=str(P["verdict"]["build_with_caveat"]),NO=str(P["verdict"]["needs_outreach"]),SS=str(P["self_serve"]),FREE=str(P["access"]["self_serve_free"]),TRIAL=str(P["access"]["self_serve_trial"]),SG=str(P["ss_second_gate"]),SU=str(P["ss_unknown"]),OAU=str(P["auth_oauth"]),STA=str(P["auth_static"]),BOTH=str(P["auth_both"]),OONLY=str(len(P["oauth_only"])),SNO=str(P["static_no_oauth"]),MCP=str(P["mcp"]["official"]),MCPG=str(len(P["mcp_prod_gated"])),NG=str(len(P["gap_build_now"])),NGT=str(len(P["gap_build_now"])+len(P["gap_other"])),EV1=f'{E1[True]} of {sum(E1.values())}',EV2=f'{E2[True]} of {sum(E2.values())}',UNR=str(sum(bool(r["unresolved"]) for r in F)),SETT=str(H["settled"])).items(): tpl=tpl.replace("{{"+k+"}}",v)
assert "{{" not in tpl, tpl[tpl.index("{{"):][:40]
open("site/index.html","w").write(tpl);print(len(tpl))
# standalone copy for GitHub Pages: same content in a full HTML document
import shutil
pathlib.Path("docs").mkdir(exist_ok=True)
head,body=tpl.split("</style>",1)
open("docs/index.html","w").write('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<style>img{max-width:100%}[hidden]{display:none!important}</style>\n'+head+"</style>\n</head>\n<body>"+body+"</body>\n</html>\n")
for f in("data.json","data.csv"): shutil.copy("site/"+f,"docs/"+f)
pathlib.Path("docs/.nojekyll").touch()
