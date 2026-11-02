import re, sys, os, html
import yaml, markdown
R=sys.argv[1]; OUT=sys.argv[2]
cfg=yaml.load(open(f'{R}/mkdocs.yml'), Loader=yaml.BaseLoader) if False else None
# nav order (hand-mirrored from mkdocs.yml)
nav=[("Start here",[("index.md","Start here"),("demo-2026-10-22.md","MVP demo, Oct 22")]),
 ("Setup, step by step",[(f"setup/{f}",t) for f,t in [
  ("01-build-data.md","1. Build and publish the data"),("02-views.md","2. Source and views"),
  ("03-web-map.md","3. Build the web map"),("04-popups.md","4. Set up pop-ups"),
  ("05-field-maps-form.md","5. Field Maps form"),("06-survey123.md","6. Survey123 form"),
  ("07-test.md","7. Test before the pilot"),("08-pilot.md","8. Run the staff pilot")]]),
 ("Reference",[("reference/schema.md","Schema and field reasons"),("reference/app-comparison.md","Field Maps vs Survey123"),
  ("reference/task-cards.md","Pilot task cards"),("reference/offline-basemap.md","Offline basemap"),("reference/esri-docs.md","Esri 11.5 docs"),("reference/troubleshooting.md","Troubleshooting"),("downloads.md","Downloads")])]
def pid(path): return re.sub(r'[^a-z0-9]+','-',path.replace('.md','').split('/')[-1].lower()).strip('-')
pages=[p for _,g in nav for p in g]
secs=[]
for path,title in pages:
    src=open(f'{R}/docs/{path}').read()
    src=re.sub(r'```mermaid\n(.*?)```', lambda m:'<pre class="mermaid">'+html.escape(m.group(1))+'</pre>', src, flags=re.S)
    md=markdown.Markdown(extensions=['tables','fenced_code','toc','attr_list','pymdownx.tasklist','pymdownx.superfences'],
        extension_configs={'toc':{'slugify':lambda v,s: pid(path)+'--'+markdown.extensions.toc.slugify(v,'-')}})
    body=md.convert(src)
    base=os.path.dirname(path)
    def fix(m):
        href=m.group(1)
        if href.startswith('http'): return f'href="{href}" target="_blank" rel="noopener"'
        target, _, anchor = href.partition('#')
        if not target: return f'href="#{pid(path)}--{anchor}"'
        full=os.path.normpath(os.path.join(base,target))
        if full.startswith('kit/'): return f'class="kitfile" data-kit="{full}" title="Download {os.path.basename(full)}" href="#{pid("downloads.md")}"'
        return f'href="#{pid(full)}--{anchor}"' if anchor else f'href="#{pid(full)}"'
    body=re.sub(r'href="([^"]+)"', fix, body)
    secs.append((path,title,body))
navhtml=''.join(f'<p class="navgrp">{g}</p><ul>'+''.join(f'<li><a href="#{pid(p)}">{html.escape(t)}</a></li>' for p,t in items)+'</ul>' for g,items in nav)
sel=''.join(f'<option value="{pid(p)}">{html.escape(t)}</option>' for p,t in pages)
content=''.join(f'<section class="page" id="{pid(p)}">{b}</section>' for p,t,b in secs)
# Embed kit files the viewer can save (downloads capability allowlist; .py ships in the zip)
import base64, json
KIT_EXT=('.xlsx','.csv','.zip','.txt','.json','.md')
kit={}
for dp,_,fs in os.walk(f'{R}/docs/kit'):
    for fn in fs:
        if fn.lower().endswith(KIT_EXT):
            full=os.path.relpath(os.path.join(dp,fn), f'{R}/docs')
            kit[full]=base64.b64encode(open(os.path.join(dp,fn),'rb').read()).decode()
content+='<script type="application/json" id="kitdata">'+json.dumps(kit)+'</script>'
tpl=open(sys.argv[3]).read()
open(OUT,'w').write(tpl.replace('%%NAV%%',navhtml).replace('%%SELECT%%',sel).replace('%%CONTENT%%',content))
