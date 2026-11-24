"""Match the 100 apps to Composio's public toolkit catalogue (docs.composio.dev sitemap)."""
import json,re
S=set(open("data/composio_slugs.txt").read().split());A=json.load(open("data/apps.json"))
n=lambda s:re.sub(r"[^a-z0-9]","",s.lower())
N={}
for s in S:N.setdefault(n(s),[]).append(s)
alias={"Lark (Larksuite)":["lark","larksuite","lark_suite"],"Threads (Meta)":["threads","meta_threads"],"Meta Ads":["metaads","meta_ads","facebook_ads"],"GoHighLevel":["gohighlevel","highlevel"],"Magento (Adobe Commerce)":["magento","adobe_commerce"],"Salesforce Commerce Cloud":["salesforce_commerce_cloud","commerce_cloud"],"Amazon Selling Partner":["amazon_selling_partner","amazon_sp_api","amazon_seller"],"WhatsApp Business":["whatsapp"],"YouTube Transcript":["transcriptapi","youtube_transcript"],"Monday.com":["monday"],"Waterfall.io":["waterfall"],"Telegram":["telegram"],"Binance":["binance"],"Google Ads":["googleads"],"Coda":["coda"],"Neo4j":["neo4j"],"MongoDB Atlas":["mongodb_atlas","mongodb"],"QuickBooks":["quickbooks"],"Otter AI":["otter_ai","otter"],"Bright Data":["brightdata"],"SE Ranking":["se_ranking","seranking"],"Help Scout":["helpscout","help_scout"],"Copper":["copper"],"Front":["front","frontapp"],"Devin":["devin"],"Pylon":["pylon"],"Plain":["plain"],"Close":["close"],"Zoho CRM":["zoho"]}
out={}
for a in A:
    c=[a["app"]]+alias.get(a["app"],[])
    hit=sorted({s for x in c for s in N.get(n(x),[])+N.get(n(x)+"mcp",[])})
    near=sorted(s for s in S if n(a["app"].split(" (")[0])[:6] in n(s))[:6] if not hit else []
    out[a["id"]]=dict(slugs=hit)
    if not hit: print(a["id"],a["app"],near)
json.dump(out,open("data/composio_match.json","w"),indent=1);print("covered",sum(bool(v["slugs"]) for v in out.values()))
