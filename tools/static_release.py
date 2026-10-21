#!/usr/bin/env python3
"""Static-site QA and offline export, Python standard library only."""
import argparse, html.parser, json, pathlib, re, shutil, zipfile
from urllib.parse import urlsplit, unquote
P=pathlib.Path
class Links(html.parser.HTMLParser):
 def __init__(self): super().__init__();self.refs=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  for a in ("href","src","poster"):
   if d.get(a):self.refs.append((tag,a,d[a]))
def target(root,source,url):
 u=urlsplit(url)
 if u.scheme or u.netloc or url.startswith(("#","data:","mailto:","tel:","javascript:")):return None
 path=unquote(u.path)
 if not path:return None
 f=(root/path.lstrip("/") if path.startswith("/") else source.parent/path)
 if path.endswith("/"):f=f/"index.html"
 elif not f.suffix:f=f/"index.html"
 return f.resolve()
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--root",required=True);ap.add_argument("--name",required=True);a=ap.parse_args()
 root=P(a.root).resolve();out=P("dist");out.mkdir(exist_ok=True)
 pages=list(root.rglob("*.html"));broken=[];images=[];refs=0
 for page in pages:
  p=Links();p.feed(page.read_text(encoding="utf-8",errors="replace"))
  for tag,attr,url in p.refs:
   refs+=1;t=target(root,page,url)
   if t and (not t.is_relative_to(root) or not t.is_file()):broken.append({"page":str(page.relative_to(root)),"url":url})
 for f in root.rglob("*"):
  if f.suffix.lower() in (".jpg",".jpeg",".png",".webp",".svg",".gif"):images.append(str(f.relative_to(root)))
 report={"site":a.name,"html_pages":len(pages),"image_assets":len(images),"links_inspected":refs,"missing_internal_targets":broken,"notes":["External URLs, license provenance, JS runtime, and photographic resolution require separate verification."]}
 (out/(a.name+"-qa-report.json")).write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
 def pack(name,offline):
  with zipfile.ZipFile(out/name,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
   for f in root.rglob("*"):
    if not f.is_file():continue
    rel=f.relative_to(root);data=f.read_bytes()
    if offline and f.suffix.lower() in (".html",".css"):
     txt=data.decode("utf-8",errors="replace")
     depth=len(rel.parts)-1
     prefix="../"*depth or "./"
     # Rewrite site-root paths to page-relative paths for file:// viewing.
     txt=re.sub(r'(?P<q>["\x27])/(?!(?:/))(?P<path>[^"\x27?#]*)(?P<tail>[?#][^"\x27]*)?(?P=q)',lambda m:m.group("q")+prefix+(m.group("path") or "index.html")+(m.group("tail") or "")+m.group("q"),txt)
     if f.suffix.lower()==".css":txt=re.sub(r'url\((["\x27]?)/([^)]*?)\1\)',lambda m:"url("+m.group(1)+prefix+m.group(2)+m.group(1)+")",txt)
     data=txt.encode()
    z.writestr(str(rel),data)
 pack(a.name+"-PREVIEW.zip",False);pack(a.name+"-FINALE-OFFLINE.zip",True)
 print(json.dumps({"pages":len(pages),"images":len(images),"broken":len(broken)}))
 if broken:print("WARN: missing internal links; see QA report")
if __name__=="__main__":main()
