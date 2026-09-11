#!/usr/bin/env python3
"""Rewrite the /work/<slug>/ pages from the case study payload in index.html.

There are two surfaces for one project: the panel, which every visitor with JS
sees, and the standalone page, which is the no-JS fallback the card still points
at. They carried two different vocabularies and two different versions of the
same prose, and drifted apart the moment one was edited. This regenerates the
page from `#cs-data`, so the panel is the single source and the page can be
re-synced and diffed rather than remembered.

    python3 scripts/sync-work-pages.py [--check]

--check exits non-zero if any page is out of date, without writing.
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SECTIONS = [("problem", "Problem"), ("process", "Process"),
            ("solution", "Solution"), ("impact", "Impact")]

def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def payload():
    s = (ROOT / "index.html").read_text()
    raw = re.search(r'id="cs-data">(.*?)</script>', s, re.S).group(1)
    return json.loads(raw.replace("<\\/", "</"))

def render(rec):
    out = []
    for key, label in SECTIONS:
        body = rec.get(key)
        if not body:
            continue
        paras = "\n".join(f"        <p>{esc(p.strip())}</p>"
                          for p in body.split("\n") if p.strip())
        out.append(f'    <section>\n      <div class="lbl">{label}</div>\n'
                   f'      <div class="body">\n{paras}\n      </div>\n    </section>')
    # A project with no four-part text keeps whatever the page already had.
    return "\n\n".join(out) if out else None

def main():
    check = "--check" in sys.argv
    data, stale = payload(), []
    for page in sorted((ROOT / "work").glob("*/index.html")):
        slug = page.parent.name
        rec = data.get(slug)
        if not rec:
            print(f"  {slug}: not in the payload, left alone"); continue
        block = render(rec)
        if block is None:
            print(f"  {slug}: no four-part text, left alone"); continue
        src = page.read_text()
        new = re.sub(r'    <section>.*</section>', block, src, count=1, flags=re.S)
        if new == src:
            print(f"  {slug}: already in sync")
        elif check:
            stale.append(slug); print(f"  {slug}: OUT OF DATE")
        else:
            page.write_text(new); print(f"  {slug}: rewritten from the payload")
    if check and stale:
        sys.exit(1)

main()
