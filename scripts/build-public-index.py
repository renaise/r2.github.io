#!/usr/bin/env python3
"""Generate human- and agent-readable case study pages from the public portfolio."""
from html import escape
from pathlib import Path
import json
import re
import sys
from xml.sax.saxutils import escape as xml_escape

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://renaise.com"
# Review additions here first. Keep gated and unpublished projects out even if
# someone adds them to the homepage data.
SLUGS = (
    "idler", "osmosis", "soot", "flora", "maestro", "aputure",
    "depictions-of-original-sin", "biota", "studio-artifice", "lighthouse",
    "the-artifact-index", "artifice-brand", "artifactory", "cinebox", "vamos",
    "fielder", "moshpit", "codex-foundry", "mythra", "rememe",
)
SECTIONS = ("problem", "process", "solution", "impact")

def esc(value):
    return escape(str(value), quote=True)

def page(title, path, description, body):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · Renaise Kim</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{SITE}{path}">
<link rel="stylesheet" href="/work/read.css">
</head>
<body>
<nav aria-label="Portfolio"><a href="/">Renaise</a> / <a href="/work/">Public work</a></nav>
<main>
{body}
</main>
</body>
</html>
'''

def case_study(slug, record):
    title = record["name"]
    claim = record.get("title", "")
    path = f"/work/{slug}/"
    facts = "".join(f"<dt>{label}</dt><dd>{esc(record[k])}</dd>"
                    for k, label in (("role", "Role"), ("year", "Year"), ("medium", "Medium"))
                    if record.get(k))
    intro = f"<p>{esc(record['hook'])}</p>" if record.get("hook") else ""
    body = []
    for field in SECTIONS:
        paragraphs = "".join(f"<p>{esc(p.strip())}</p>"
                             for p in record.get(field, "").splitlines() if p.strip())
        if paragraphs:
            body.append(f"<section><h2>{field.title()}</h2>{paragraphs}</section>")
    heading = f"<p>{esc(claim)}</p>" if claim and claim != title else ""
    summary = record.get("hook") or claim or title
    return page(title, path, summary, f'''<article>
<header><h1>{esc(title)}</h1>{heading}</header>
<dl>{facts}</dl>
{intro}
{chr(10).join(body)}
<p><a href="/{slug}/">View {esc(title)} in the interactive portfolio</a></p>
</article>''')

src = (ROOT/"index.html").read_text()
records = json.loads(re.search(r'id="cs-data">(.*?)</script>', src, re.S)[1])
for slug in SLUGS:
    assert not (records[slug].keys() & {"locked", "unlock", "embed"}), slug

outputs = {}
links = []
llms = ["# Renaise Kim", "", "> Selected public portfolio work by Renaise Kim, designer and curator.", "",
        "[Public work index](https://renaise.com/work/) · [Interactive portfolio](https://renaise.com/)", "", "## Public case studies", ""]
for slug in SLUGS:
    record = records[slug]
    path = f"/work/{slug}/"
    title, claim = record["name"], record.get("title", "")
    # Preserve the existing rich SOOT reading page; it is synced separately.
    if slug != "soot":
        outputs[path.lstrip("/")+"index.html"] = case_study(slug, record)
    links.append(f'<li><a href="{path}">{esc(title)}</a>'
                 f'<span>{esc(claim)} · {esc(record["role"])}</span></li>')
    llms.append(f"- [{title}]({SITE}{path}): {claim}. Role: {record['role']}.")
outputs["work/index.html"] = page("Public work", "/work/", "Public case studies by Renaise Kim.",
    "<h1>Public work</h1><p>Case studies by Renaise Kim, designer and curator.</p><ul>"
    + "\n".join(links) + "</ul>")
outputs["llms.txt"] = "\n".join(llms)+"\n"
outputs["sitemap.xml"] = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(
    f"  <url><loc>{xml_escape(SITE+path)}</loc></url>" for path in ("/","/work/",*(f"/work/{s}/" for s in SLUGS))) + "\n</urlset>\n"

check = "--check" in sys.argv
stale = []
for name, content in outputs.items():
    path = ROOT / name
    if check:
        if not path.is_file() or path.read_text() != content:
            stale.append(name)
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
if stale:
    print("Out of date:", ", ".join(stale)); sys.exit(1)
