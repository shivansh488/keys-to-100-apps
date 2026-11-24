"""Gold labels for the 20 sampled apps. Read in a live browser by the supervising agent (NOT a human)
before opening data/pass1. auth: 'must' = methods that must be present, 'may' = allowed extras (static = api_key/token).
access/mcp/verdict: list, first is the answer, rest are alternates accepted because the docs or schema are ambiguous."""
import json
S="static";G={}
def g(i,must,may,access,mcp,verdict,urls,note=""): G[i]=dict(must=must,may=may,access=access,mcp=mcp,verdict=verdict,urls=urls,note=note)
F,T,P,A="self_serve_free","self_serve_trial","paid_plan","admin_or_app_approval"
B,C,O,N="build_now","build_with_caveat","needs_outreach","not_buildable"
off=["official"];non=["none_found","community"]
g(1,["oauth2"],["other"],[F],off,[B],["https://developer.salesforce.com/docs/platform/api-rest/guide/intro-oauth-and-connected-apps.html","https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/hosted-mcp-servers-overview.html"],"Developer Edition signup page rendered blank in the browser; free tier not re-confirmed, so access here is the weakest label.")
g(3,["oauth2",S],[],[F],off,[B],["https://pipedrive.readme.io/docs/core-api-concepts-authentication","https://pipedrive.readme.io/docs/developer-sandbox-account","https://www.pipedrive.com/en/features/mcp-server"])
g(11,["oauth2"],[],[T],off,[B],["https://developer.zendesk.com/api-reference/introduction/security-and-auth/","https://developer.zendesk.com/documentation/api-basics/getting-started/getting-a-trial-or-sponsored-account-for-development/","https://support.zendesk.com/hc/en-us/articles/11458059060250-Zendesk-Bridge-FAQ-EAP"],"API tokens are now marked deprecated. MCP server is early access by enrolment (from 2026-11-10), known from search text; the support page itself was behind a sign-in.")
g(13,[S],["basic","oauth2"],[T,F],off,[B],["https://developers.freshdesk.com/api/","https://www.freshworks.com/freshdesk/pricing/","https://support.freshdesk.com/support/solutions/articles/50000012670"],"Pricing page only describes a 14-day trial; a legacy free plan could not be ruled out.")
g(28,[S],["oauth2"],[F],off,[B,C],["https://developers.facebook.com/documentation/business-messaging/whatsapp/get-started","https://developers.facebook.com/blog/post/2026/09/15/whatsapp-business-messaging-mcp-ai-agent/"],"MCP is for setup/testing, gradual rollout.")
g(30,[S,"other"],["basic","oauth2"],[T,F],off,[B],["https://developer.vonage.com/en/getting-started/concepts/authentication","https://developer.vonage.com/en/mcp-server/overview"],"JWT is 'other'. Free account confirmed; whether credit-limited was not.")
g(33,["oauth2"],[],[A],non,[O],["https://learn.microsoft.com/en-us/linkedin/marketing/increasing-access","https://learn.microsoft.com/en-us/linkedin/shared/authentication/authentication"])
g(38,["oauth2"],[S,"other"],[A],off,[O],["https://developers.pinterest.com/docs/getting-started/connect-app/","https://developers.pinterest.com/docs/key-concepts/access-tiers/","https://developers.pinterest.com/about-pinterest-mcp/"])
g(47,[S,"oauth2"],[],[P],non,[C],["https://docs.ecwid.com/llms-full.txt"],"Only stores on paid plans get API; free dev upgrade by email. Docs-search MCP is not a product MCP.")
g(48,["oauth2"],[S],[F],off,[B],["https://gumroad.com/api","https://gumroad.com/mcp"])
g(54,[S],[],[T],off,[B],["https://docs.mrscraper.com/docs/getting-started/mcp-server","https://mrscraper.com/pricing"],"7-day / 1,000-token trial, card required.")
g(60,[S],["oauth2"],[F],off,[B],["https://developers.clay.com/public-api/authentication.md","https://university.clay.com/docs/clay-api-cli"],"Public API is now on all plans incl. free: contradicts older 'Enterprise only' lore.")
g(61,["oauth2",S],["other","basic"],[F],off,[B],["https://docs.github.com/en/rest/authentication/authenticating-to-the-rest-api"])
g(62,[S],["oauth2","other"],[F],off,[B],["https://vercel.com/docs/rest-api","https://vercel.com/docs/agent-resources/vercel-mcp"])
g(79,[S,"oauth2"],[],[P,T],off,[C],["https://developers.smartsheet.com/api/smartsheet/introduction","https://developers.smartsheet.com/ai-mcp/smartsheet/mcp-server","https://www.smartsheet.com/pricing"],"API needs Business+; 30-day trial exists, whether it carries API not testable without sign-up.")
g(80,[S,"oauth2"],[],[F],off,[B],["https://help.getharvest.com/api-v2/authentication-api/authentication/authentication/","https://www.getharvest.com/pricing","https://support.getharvest.com/hc/en-us/articles/46293697226381-Harvest-MCP"])
g(81,[S],["basic","oauth2","other"],[F],off,[B],["https://docs.stripe.com/api/authentication","https://docs.stripe.com/mcp"])
g(83,[S,"other"],["oauth2"],[F],off,[B],["https://developers.binance.com/en/docs/products/spot/rest-api","https://testnet.binance.vision/","https://developers.binance.com/en/docs/agent-native/mcp-server"])
g(95,[S],[],[T],off,[B],["https://docs.reducto.ai/quickstart","https://reducto.ai/pricing","https://docs.reducto.ai/mcp-server/index.md"],"$150 one-off free usage = credit-limited trial under our schema.")
g(98,["none"],[],["no_api",F],non,[C,N],["https://github.com/mermaid-js/mermaid-cli"],"Local CLI; wrapping is realistic.")
assert sorted(G)==sorted(json.load(open("data/gold_ids.json")))
json.dump({str(k):v for k,v in G.items()},open("data/gold/gold.json","w"),indent=1);print(len(G))
