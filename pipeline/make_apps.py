"""Writes data/apps.json: the 100 apps exactly as listed in the brief."""
import json, pathlib
CATS=["CRM and Sales","Support and Helpdesk","Communications and Messaging","Marketing, Ads, Email and Social","Ecommerce","Data, SEO and Scraping","Developer, Infra and Data platforms","Productivity and Project Management","Finance and Fintech","AI, Research and Media-native"]
RAW="""Salesforce|salesforce.com;HubSpot|hubspot.com;Pipedrive|pipedrive.com;Attio|attio.com;Twenty|twenty.com;Podio|podio.com;Zoho CRM|zoho.com/crm;Close|close.com;Copper|copper.com;DealCloud|api.docs.dealcloud.com
Zendesk|zendesk.com;Intercom|intercom.com;Freshdesk|freshdesk.com;Front|front.com;Pylon|usepylon.com;LiveAgent|liveagent.com;Plain|plain.com;Help Scout|helpscout.com;Gorgias|gorgias.com;Gladly|gladly.com
Slack|slack.com;Twilio|twilio.com;Zoho Cliq|zoho.com/cliq;Lark (Larksuite)|open.larksuite.com;Pumble|pumble.com;Discord|discord.com;Telegram|core.telegram.org;WhatsApp Business|developers.facebook.com/docs/whatsapp;Aircall|aircall.io;Vonage|developer.vonage.com
Google Ads|developers.google.com/google-ads;Meta Ads|developers.facebook.com/docs/marketing-apis;LinkedIn Ads|learn.microsoft.com/linkedin/marketing;GoHighLevel|highlevel.stoplight.io;Mailchimp|mailchimp.com/developer;Klaviyo|developers.klaviyo.com;systeme.io|systeme.io;Pinterest|developers.pinterest.com;Threads (Meta)|developers.facebook.com/docs/threads;SendGrid|sendgrid.com
Shopify|shopify.dev;WooCommerce|woocommerce.com/document/woocommerce-rest-api;BigCommerce|developer.bigcommerce.com;Salesforce Commerce Cloud|developer.salesforce.com/docs/commerce;Magento (Adobe Commerce)|developer.adobe.com/commerce;Squarespace|developers.squarespace.com;Ecwid|api-docs.ecwid.com;Gumroad|gumroad.com/api;Amazon Selling Partner|developer-docs.amazon.com/sp-api;fanbasis|fanbasis.com
DataForSEO|docs.dataforseo.com;SE Ranking|seranking.com/api;Ahrefs|ahrefs.com/api;MrScraper|docs.mrscraper.com;Apify|docs.apify.com;Firecrawl|firecrawl.dev;Bright Data|brightdata.com;Sherlock|github.com/sherlock-project/sherlock;Waterfall.io|waterfall.io;Clay|clay.com
GitHub|docs.github.com/rest;Vercel|vercel.com/docs/rest-api;Netlify|docs.netlify.com/api;Cloudflare|developers.cloudflare.com/api;Supabase|supabase.com/docs;Neo4j|neo4j.com/docs/api;Snowflake|docs.snowflake.com;MongoDB Atlas|mongodb.com/docs/atlas/api;Datadog|docs.datadoghq.com/api;Sentry|docs.sentry.io/api
Notion|developers.notion.com;Airtable|airtable.com/developers;Linear|developers.linear.app;Jira|developer.atlassian.com;Asana|developers.asana.com;Monday.com|developer.monday.com;ClickUp|clickup.com/api;Coda|coda.io/developers;Smartsheet|smartsheet.com/developers;Harvest|help.getharvest.com/api-v2
Stripe|stripe.com/docs/api;Plaid|plaid.com/docs;Binance|binance-docs.github.io;Paygent Connect|paygent.com;iPayX|ipayx.ai/docs;QuickBooks|developer.intuit.com;Xero|developer.xero.com;Brex|developer.brex.com;Ramp|docs.ramp.com;PitchBook|pitchbook.com
NotebookLM|cloud.google.com/gemini;Otter AI|help.otter.ai;Fathom|fathom.video;Consensus|consensus.app;Reducto|reducto.ai;Devin|docs.devin.ai;higgsfield|higgsfield.ai/cli;Mermaid CLI|github.com/mermaid-js/mermaid-cli;YouTube Transcript|transcriptapi.com;Grain|grain.com"""
out=[];n=0
for c,l in zip(CATS,RAW.split("\n")):
    for p in l.split(";"):
        n+=1;a,h=p.split("|");out.append(dict(id=n,app=a,hint=h,category=c))
assert n==100
pathlib.Path("data/apps.json").write_text(json.dumps(out,indent=1))
