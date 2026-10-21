from pathlib import Path
root=Path("site") if Path("site/index.html").exists() else Path(".")
is_mesh=Path("site/index.html").exists()
prefix="/mesh-italia/" if is_mesh else "/heartagram-italia/"
domain="www.mesh-band.it" if is_mesh else "www.heartagram-italia.it"
legacy="https://salvatoresinatra0001-ux.github.io"+prefix
updated=0
for path in root.rglob("*"):
 if not path.is_file() or path.suffix.lower() not in {".html",".css",".js",".xml",".json",".txt"}:continue
 before=path.read_text("utf8",errors="replace")
 after=before.replace(legacy,"https://"+domain+"/").replace(prefix,"/")
 if before!=after:path.write_text(after,encoding="utf8");updated+=1
if is_mesh:
 (root/"_redirects").write_text("# Legacy routes\n/musica/fallen-angel/ /v2/musica/fallen-angel/ 301\n/mesh-italia/* /:splat 301\n",encoding="utf8")
 css=root/"assets/site.css"
 style=css.read_text("utf8")
 tag="/* MESH 2.2 editorial polish */"
 if tag not in style:
  css.write_text(style+"\n"+tag+"\nhtml{scroll-padding-top:90px}.release-notice{border-block:1px solid #5e514c}.release-grid img,.media-lead img{height:auto}a:focus-visible,button:focus-visible{outline:3px solid currentColor;outline-offset:4px}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto!important}*{transition:none!important;animation:none!important}}\n",encoding="utf8")
else:
 toml=Path("netlify.toml")
 if toml.exists():
  original=toml.read_text("utf8")
  updated_toml=original.replace("status = 200","status = 301")
  if updated_toml!=original:toml.write_text(updated_toml,encoding="utf8")
print("Normalized",updated,"files for",domain)
