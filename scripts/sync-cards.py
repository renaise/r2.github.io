#!/usr/bin/env python3
"""Rewrite each card's <span class="d"> from that project's hook in #cs-data.

The card text is baked into the markup so the grid reads with JS off, which
means it is a second copy of the hook and drifts silently: a hook pass once
landed in every panel and in none of the cards, and the cards are the surface
people actually read first. Run this after any hook edit. --check exits
non-zero when the two disagree, so it can refuse rather than report.
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
page = ROOT / "index.html"
src = page.read_text()

data = json.loads(
    re.search(r'id="cs-data">(.*?)</script>', src, re.S).group(1).replace("<\\/", "</")
)

ESC = {"&": "&amp;", "<": "&lt;", ">": "&gt;"}
def esc(t): return "".join(ESC.get(c, c) for c in t)

stale, out = [], src
for slug, rec in data.items():
    hook = rec.get("hook")
    if not hook:
        continue
    # the card anchor, then its description span: the first .d after the slug
    anchor = re.search(r'data-slug="%s"' % re.escape(slug), out)
    if not anchor:
        print("  %s: no card, left alone" % slug); continue
    m = re.compile(r'<span class="d">(.*?)</span>', re.S).search(out, anchor.end())
    if not m:
        print("  %s: card has no description span" % slug); continue
    if m.group(1) == esc(hook):
        continue
    stale.append(slug)
    out = out[:m.start(1)] + esc(hook) + out[m.end(1):]

if "--check" in sys.argv:
    print("cards out of sync: " + (", ".join(stale) if stale else "none"))
    sys.exit(1 if stale else 0)

if stale:
    page.write_text(out)
    for s in stale:
        print("  %s: card rewritten from the hook" % s)
else:
    print("  all cards already match their hooks")
