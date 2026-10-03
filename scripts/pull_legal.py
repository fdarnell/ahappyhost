#!/usr/bin/env python3
"""Regenerate scripts/legal_pages.py from the live Duda site.

The legal and policy pages are the client's own documents, so they are read
off the live site rather than retyped.

Two things this gets right that a naive scrape does not:

  * <a> and <span> are INLINE. An earlier version treated them as blocks, so
    "Email: services@ahappyhostgsm.com" came through as "Email:" — the address
    lives in a nested anchor. Every legal page lost its contact email that way.
  * Chrome (header/footer) is stripped only from the LEADING and TRAILING runs,
    never from the middle. The company email and phone legitimately appear in
    the body of these documents, and filtering by "appears on every page" ate
    them.

    python3 scripts/pull_legal.py
"""
import html as H
import json
import pathlib
import re
import urllib.request

from bs4 import BeautifulSoup

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://www.ahappyhost.com"
BLOCK = ("h1", "h2", "h3", "h4", "h5", "p", "li", "td", "div")

PAGES = {
    "handbook": "/handbook",
    "nda-non-compete": "/nda/non-compete",
    "terms-and-condition": "/terms-and-condition",
    "privacy-policy": "/privacy-policy",
    "service-rate-update-2025": "/service-rate-update-2025",
}
CHROME_REF = "/about"

META = {
    "handbook": ("Company Handbook &amp; Policies | A Happy Host",
                 "A Happy Host, LLC company handbook and policies for team members and contractors.", "/handbook"),
    "nda-non-compete": ("NDA &amp; Non-Compete | A Happy Host",
                        "Non-Disclosure Agreement and Non-Compete for A Happy Host, LLC.", "/nda/non-compete"),
    "terms-and-condition": ("Terms and Conditions | A Happy Host",
                            "Terms and Conditions and Service Agreement for A Happy Host, LLC rental concierge services.", "/terms-and-condition"),
    "privacy-policy": ("Privacy Policy | A Happy Host",
                       "How A Happy Host, LLC collects, uses and protects your personal information.", "/privacy-policy"),
    "service-rate-update-2025": ("Service Rate Update 2025 | A Happy Host",
                                 "A Happy Host, LLC service rate update effective October 15, 2025.", "/service-rate-update-2025"),
}


def fetch(path):
    req = urllib.request.Request(SITE + path, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=45).read().decode("utf-8", "ignore")


def blocks(html):
    soup = BeautifulSoup(html, "lxml")
    for t in soup(["script", "style", "noscript", "svg", "iframe", "img"]):
        t.decompose()
    out = []
    for el in soup.find_all(BLOCK):
        if el.find(BLOCK):
            continue
        text = re.sub(r"\s+", " ", el.get_text(" ", strip=True)).replace("​", "").replace("﻿", "").strip()
        if len(text) < 3:
            continue
        tag = el.name if el.name in ("h1", "h2", "h3", "h4", "h5", "li") else "p"
        if out and out[-1][1] == text:
            continue
        out.append((tag, text))
    return out


def is_heading(tag, t):
    if tag in ("h1", "h2", "h3", "h4", "h5"):
        return True
    if len(t) > 90:
        return False
    return bool(re.match(r"^\d+\.\s+\S", t) or re.match(r"^(SECTION|ARTICLE)\b", t, re.I)
                or (t.isupper() and 4 <= len(t) <= 80))


def render(bl):
    out, in_list, first = [], False, True
    for tag, t in bl:
        esc = H.escape(t, quote=False)
        if tag == "li":
            if not in_list:
                out.append("    <ul>")
                in_list = True
            out.append(f"      <li>{esc}</li>")
            continue
        if in_list:
            out.append("    </ul>")
            in_list = False
        if first:
            out.append(f"    <h1>{esc}</h1>")
            first = False
        elif is_heading(tag, t):
            out.append(f"    <h2>{esc}</h2>")
        else:
            out.append(f"    <p>{esc}</p>")
    if in_list:
        out.append("    </ul>")
    return "\n".join(out)


# Header/footer text that is not part of a document even when it survives the
# cross-page chrome test. Without this the body started at "Contact Us" and the
# real title ("Privacy Policy - A Happy Host LLC") was demoted to a paragraph.
EDGE_NOISE = re.compile(
    r"^(contact us|get in touch|home|about|services|sitemap|accessibility|tos|menu|"
    r"happy guest|a happy guest|business hours|navigation|"
    r"mon ?- ?fri.*|sat ?- ?sun.*|emergencies.*|phone:.*|"
    r"click here if you.*|let.s stay connected.*|please report errors.*|"
    r"all rights reserved.*|\u00a9.*|865[-. ]?314[-. ]?7564|[\w.+-]+@[\w.-]+)$",
    re.I)


def trim_edges(bl):
    """Drop header/footer noise from the start and end, never from the middle."""
    i, j = 0, len(bl)
    while i < j and EDGE_NOISE.match(bl[i][1].strip()):
        i += 1
    while j > i and EDGE_NOISE.match(bl[j - 1][1].strip()):
        j -= 1
    return bl[i:j]


raw = {slug: blocks(fetch(path)) for slug, path in PAGES.items()}
raw["_ref"] = blocks(fetch(CHROME_REF))

counts = {}
for bl in raw.values():
    for _, t in set(bl):
        counts[t] = counts.get(t, 0) + 1
chrome = {t for t, n in counts.items() if n == len(raw)}

parts = ['''"""Legal and policy pages, transcribed from the live Duda site.

Generated by scripts/pull_legal.py — do not hand-edit. Content is verbatim;
only the markup is the rebuild's own.
"""

LEGAL_PAGES = {}
''']
report = {}
for slug, bl in raw.items():
    if slug == "_ref":
        continue
    idx = [i for i, (_, t) in enumerate(bl) if t not in chrome]
    lo, hi = min(idx), max(idx)
    body_blocks = trim_edges(bl[lo:hi + 1])   # keep chrome strings INSIDE the body, drop edge noise
    title, desc, path = META[slug]
    parts.append(f'''
LEGAL_PAGES["{slug}"] = dict(
    title="{title}",
    desc="{desc}",
    path="{path}",
    body="""<main class="legal">
  <section class="legal-body">
    <div class="container">
{render(body_blocks)}
    </div>
  </section>
</main>""",
)
''')
    report[slug] = len(body_blocks)

(ROOT / "scripts" / "legal_pages.py").write_text("".join(parts))
(ROOT / "_research" / "live-legal-pages.json").write_text(
    json.dumps({k: v for k, v in raw.items() if k != "_ref"}, indent=1))
for slug, n in report.items():
    print(f"  {slug:<26} {n:>4} blocks")
print("wrote scripts/legal_pages.py")
