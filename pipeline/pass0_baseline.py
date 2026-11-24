"""Pass 0: keyless rule-based baseline. Crawl hint URL + a few likely doc links, regex the fields.
Deliberately simple: it is the floor the LLM passes are measured against."""
import json,re,html,pathlib,sys
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin,urlparse
sys.path.insert(0,str(pathlib.Path(__file__).parent))
from fetch import fetch
apps=json.load(open("data/apps.json"))
LINK=re.compile(r'(?i)(authenticat|/auth\b|/api\b|developer|api-reference|getting-started|pricing)')
def strip(h):
    h=re.sub(r'(?is)<(script|style|svg)\b.*?</\1>',' ',h)
    return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',h)))
def run(a):
    root="https://"+a["hint"]; st,body,final=fetch(root); pages={final or root:strip(body)}
    links=[]
    for m in re.findall(r'href="([^"#]+)"',body):
        u=urljoin(final or root,m)
        if LINK.search(u) and urlparse(u).scheme.startswith("http") and u not in links: links.append(u)
    for u in links[:5]:
        s,b,f=fetch(u)
        if s==200: pages[f or u]=strip(b)
    t=" ".join(pages.values())
    auth=[]
    if re.search(r'(?i)oauth',t): auth.append("oauth2")
    if re.search(r'(?i)\bapi[ -]?key|api token|access token|personal access',t): auth.append("static_key")
    if re.search(r'(?i)basic auth|http basic',t): auth.append("basic")
    if re.search(r'(?i)contact (our )?sales|request (a )?demo|book a demo|become a partner',t) and not re.search(r'(?i)free trial|start (for )?free|sign up free|get started free|free plan',t): acc="partner_or_sales"
    elif re.search(r'(?i)free trial',t): acc="self_serve_trial"
    elif re.search(r'(?i)start (for )?free|free plan|free tier|sign up',t): acc="self_serve_free"
    else: acc="unknown"
    mcp="official" if re.search(r'(?i)\bMCP\b|model context protocol',t) else "none_found"
    api=[x for x,p in(("rest",r'(?i)\brest(ful)?\b'),("graphql",r'(?i)graphql')) if re.search(p,t)]
    verdict="build_now" if auth and acc.startswith("self") else ("needs_outreach" if acc=="partner_or_sales" else "build_with_caveat" if auth else "not_buildable")
    return dict(id=a["id"],app=a["app"],auth=auth or ["unknown"],access=acc,api_types=api,mcp=mcp,verdict=verdict,pages=list(pages),http=st)
with ThreadPoolExecutor(12) as ex: res=list(ex.map(run,apps))
pathlib.Path("data/pass0.json").write_text(json.dumps(res,indent=1))
from collections import Counter
for k in("access","mcp","verdict"): print(k,Counter(r[k] for r in res))
print("auth",Counter(x for r in res for x in r["auth"]),"seed page failed:",[r["app"] for r in res if r["http"]!=200])
