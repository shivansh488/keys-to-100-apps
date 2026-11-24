"""Second sample, drawn after pass 2 with a new seed, excluding the gold apps: 1 per category."""
import json,random
A=json.load(open("data/apps.json"));g=set(json.load(open("data/gold_ids.json")));r=random.Random(777)
out=[r.choice([a["id"] for a in A if a["category"]==c and a["id"] not in g]) for c in dict.fromkeys(a["category"] for a in A)]
json.dump(out,open("data/holdout_ids.json","w"));print([(i,A[i-1]["app"],A[i-1]["hint"]) for i in out])
