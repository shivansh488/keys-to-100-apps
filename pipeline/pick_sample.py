"""Stratified random gold sample: 2 apps per category, fixed seed, drawn before any LLM pass ran."""
import json,random
r=random.Random(20261124);A=json.load(open("data/apps.json"));out=[]
for c in dict.fromkeys(a["category"] for a in A): out+=sorted(a["id"] for a in r.sample([a for a in A if a["category"]==c],2))
json.dump(out,open("data/gold_ids.json","w"));print([(i,A[i-1]["app"]) for i in out])
