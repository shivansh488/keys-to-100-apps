"""curl-based fetch with an on-disk cache so reruns are cheap and evidence is reproducible."""
import subprocess,hashlib,pathlib,json,os,threading
C=pathlib.Path("cache");C.mkdir(exist_ok=True)
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36"
def fetch(u,force=False):
    k=C/(hashlib.sha1(u.encode()).hexdigest()+".json")
    if k.exists() and not force:
        try: d=json.loads(k.read_text());return d["s"],d["b"],d["f"]
        except ValueError: pass   # torn cache file, refetch
    try:
        p=subprocess.run(["curl","-sL","--compressed","-m","25","-A",UA,"-w","\n@@%{http_code}@@%{url_effective}","--",u],capture_output=True,timeout=40)
        o=p.stdout.decode("utf8","replace");b,_,m=o.rpartition("\n@@");s,_,f=m.partition("@@")
        s=int(s or 0)
    except Exception: s,b,f=0,"",u
    t=k.with_suffix(f".{os.getpid()}.{threading.get_ident()}.tmp");t.write_text(json.dumps(dict(u=u,s=s,b=b[:1500000],f=f)));os.replace(t,k)  # atomic
    return s,b[:1500000],f
