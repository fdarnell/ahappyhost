#!/usr/bin/env python3
"""Static site generator for ahappyhost.com.

Every page shares one header/nav/footer defined here, so chrome can never
drift between pages. Run `python3 scripts/build.py` from the repo root after
editing; it rewrites the HTML files in place.
"""
import hashlib
import json
import os
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://www.ahappyhost.com"

CFG = json.loads((ROOT / "site.config.json").read_text())


def asset_hash(relpath):
    """Short content hash so cache-busted URLs change whenever the file does."""
    return hashlib.md5((ROOT / relpath).read_bytes()).hexdigest()[:10]


CSS_V = asset_hash("css/style.css")
JS_V = asset_hash("js/main.js")
PHONE = CFG["phone"]
PHONE_TEL = CFG["phone_tel"]
EMAIL = CFG["email"]

# ---------------------------------------------------------------- SVG icons
ICONS = {
    "facebook": '<svg viewBox="0 0 24 24" fill="#1877F2" aria-hidden="true"><path d="M24 12.07C24 5.4 18.63 0 12 0S0 5.4 0 12.07c0 6.02 4.39 11.02 10.13 11.93v-8.44H7.08v-3.49h3.05V9.41c0-3.02 1.79-4.7 4.53-4.7 1.31 0 2.68.24 2.68.24v2.97h-1.51c-1.49 0-1.96.93-1.96 1.89v2.26h3.33l-.53 3.49h-2.8V24C19.61 23.09 24 18.09 24 12.07z"/></svg>',
    "tiktok": '<svg viewBox="0 0 24 24" fill="#000" aria-hidden="true"><path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.9 2.9 0 1 1-2.31-2.84v-3.5a6.37 6.37 0 1 0 5.76 6.34V8.69a8.18 8.18 0 0 0 4.77 1.52V6.75a4.85 4.85 0 0 1-1-.06z"/></svg>',
    "instagram": '<svg viewBox="0 0 24 24" fill="#E4405F" aria-hidden="true"><path d="M12 2.16c3.2 0 3.58.01 4.85.07 3.25.15 4.77 1.69 4.92 4.92.06 1.27.07 1.65.07 4.85 0 3.2-.01 3.58-.07 4.85-.15 3.23-1.66 4.77-4.92 4.92-1.27.06-1.64.07-4.85.07-3.2 0-3.58-.01-4.85-.07-3.26-.15-4.77-1.7-4.92-4.92-.06-1.27-.07-1.64-.07-4.85 0-3.2.01-3.58.07-4.85C2.38 3.92 3.9 2.38 7.15 2.23 8.42 2.18 8.8 2.16 12 2.16zM12 0C8.74 0 8.33.01 7.05.07 2.7.27.27 2.69.07 7.05.01 8.33 0 8.74 0 12s.01 3.67.07 4.95c.2 4.36 2.62 6.78 6.98 6.98 1.28.06 1.69.07 4.95.07s3.67-.01 4.95-.07c4.35-.2 6.78-2.62 6.98-6.98.06-1.28.07-1.69.07-4.95s-.01-3.67-.07-4.95C23.73 2.7 21.31.27 16.95.07 15.67.01 15.26 0 12 0zm0 5.84A6.16 6.16 0 1 0 18.16 12 6.16 6.16 0 0 0 12 5.84zm0 10.15A3.99 3.99 0 1 1 16 12a3.99 3.99 0 0 1-4 3.99zm6.41-11.85a1.44 1.44 0 1 0 1.43 1.44 1.44 1.44 0 0 0-1.43-1.44z"/></svg>',
    "youtube": '<svg viewBox="0 0 24 24" fill="#FF0000" aria-hidden="true"><path d="M23.5 6.19a3.02 3.02 0 0 0-2.12-2.14C19.5 3.55 12 3.55 12 3.55s-7.5 0-9.38.5A3.02 3.02 0 0 0 .5 6.19 31.6 31.6 0 0 0 0 12a31.6 31.6 0 0 0 .5 5.81 3.02 3.02 0 0 0 2.12 2.14c1.88.5 9.38.5 9.38.5s7.5 0 9.38-.5a3.02 3.02 0 0 0 2.12-2.14A31.6 31.6 0 0 0 24 12a31.6 31.6 0 0 0-.5-5.81zM9.55 15.57V8.43L15.82 12z"/></svg>',
    "google": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#4285F4" d="M23.49 12.27c0-.79-.07-1.54-.19-2.27H12v4.51h6.47a5.57 5.57 0 0 1-2.4 3.58v3h3.86c2.26-2.09 3.56-5.17 3.56-8.82z"/><path fill="#34A853" d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.86-3c-1.08.72-2.45 1.16-4.07 1.16-3.13 0-5.78-2.11-6.73-4.96H1.29v3.09A11.99 11.99 0 0 0 12 24z"/><path fill="#FBBC05" d="M5.27 14.29A7.12 7.12 0 0 1 4.89 12c0-.8.14-1.57.38-2.29V6.62H1.29a11.99 11.99 0 0 0 0 10.76z"/><path fill="#EA4335" d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.31 0 3.26 2.69 1.29 6.62l3.98 3.09C6.22 6.86 8.87 4.75 12 4.75z"/></svg>',
    "chevron": '<svg class="nav-caret" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>',
    "burger": '<svg viewBox="0 0 24 24" fill="none" stroke="#000" stroke-width="2.4" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="#000" stroke-width="2.6" aria-hidden="true"><path d="M3 13l6 7L21 4"/></svg>',
    "check_w": '<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.6" aria-hidden="true"><path d="M3 13l6 7L21 4"/></svg>',
    "search": '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="#000" stroke-width="1.8" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5L21 21"/></svg>',
    "garland": '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="#000" stroke-width="1.6" aria-hidden="true"><path d="M2 5c5 6 15 6 20 0"/><path d="M6 8.2l-1 3 2.6-.9zM12 9.6l-.9 3 2.5-1zM18 8.2l1 3-2.6-.9z" fill="#000" stroke="none"/><circle cx="4" cy="6.5" r="1.1" fill="#000" stroke="none"/><circle cx="20" cy="6.5" r="1.1" fill="#000" stroke="none"/></svg>',
    "bed": '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="#000" stroke-width="1.8" aria-hidden="true"><path d="M3 7v11M3 14h18v4M3 11h18v3"/><circle cx="7" cy="9.5" r="1.6"/><path d="M10 11V9.2c0-.7.5-1.2 1.2-1.2H19c1.1 0 2 .9 2 2v1"/></svg>',
    "tools": '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="#000" stroke-width="1.8" aria-hidden="true"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.2L3 17.8V21h3.2l6.3-6.3a4 4 0 0 0 5.2-5.4l-2.6 2.6-2.1-.6-.6-2.1z"/></svg>',
    "envelope": '<svg viewBox="0 0 24 24" fill="none" stroke="#000" stroke-width="1.7" aria-hidden="true"><rect x="2.5" y="5" width="19" height="14" rx="2"/><path d="M3 6.5l9 6.5 9-6.5"/></svg>',
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="#000" stroke-width="1.7" aria-hidden="true"><path d="M5 3h4l1.6 4.5L8 9.6a13 13 0 0 0 6.4 6.4l2.1-2.6L21 15v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="#000" stroke-width="1.7" aria-hidden="true"><path d="M12 21s7-6.1 7-11a7 7 0 1 0-14 0c0 4.9 7 11 7 11z"/><circle cx="12" cy="10" r="2.6"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="#000" stroke-width="1.6" aria-hidden="true"><path d="M12 2l8 3v6c0 5.2-3.4 9.3-8 11-4.6-1.7-8-5.8-8-11V5z"/><path d="M8.5 12l2.4 2.4 4.6-4.8"/></svg>',
    "circlecheck": '<svg viewBox="0 0 24 24" fill="none" stroke="#000" stroke-width="1.6" aria-hidden="true"><circle cx="12" cy="12" r="9.5"/><path d="M8 12.5l2.6 2.6L16.5 9"/></svg>',
    "handshake": '<svg viewBox="0 0 24 24" fill="none" stroke="#000" stroke-width="1.5" aria-hidden="true"><path d="M4 7l4-2 4 2 4-2 4 2v7l-4 4-4-3-4 3-4-4z"/><path d="M12 7v7"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="#000" stroke-width="1.6" aria-hidden="true"><circle cx="12" cy="12" r="9.5"/><path d="M12 6.5V12l4 2.5"/></svg>',
}

SERVICES = [
    ("cabinsetup", "Cabin Setup"),
    ("rental-inspections", "Rental Inspections"),
    ("seasonal-decorating", "Seasonal Decorating"),
    ("photo-staging", "Photo Staging"),
    ("handyman-services", "Handyman Services"),
    ("a-happy-guest", "A Happy Guest"),
]

SOCIALS = [
    ("Facebook", CFG["social"]["facebook"], "facebook", "#1877F2"),
    ("TikTok", CFG["social"]["tiktok"], "tiktok", "#000000"),
    ("Instagram", CFG["social"]["instagram"], "instagram", "#E4405F"),
    ("YouTube", CFG["social"]["youtube"], "youtube", "#FF0000"),
    ("Google", CFG["social"]["google"], "google", "#4285F4"),
]

FOOTER_SOCIAL_GLYPHS = {
    "facebook": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.5 21v-7h2.4l.4-3h-2.8V9.1c0-.9.3-1.5 1.6-1.5h1.3V4.9c-.3 0-1.1-.1-2.1-.1-2.1 0-3.6 1.3-3.6 3.7V11H8.3v3h2.4v7z"/></svg>',
    "tiktok": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.7 7.3a4 4 0 0 1-2.9-3.3V3.4h-2.6v10.3a2.2 2.2 0 1 1-1.7-2.14V8.9a4.8 4.8 0 1 0 4.3 4.77V9.4a6.2 6.2 0 0 0 3.6 1.15V7.9a3.7 3.7 0 0 1-.7-.06z"/></svg>',
    "instagram": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4.3c2.5 0 2.8 0 3.8.06 2.5.11 3.7 1.3 3.8 3.8.05 1 .06 1.3.06 3.8s-.01 2.8-.06 3.8c-.11 2.5-1.3 3.7-3.8 3.8-1 .05-1.3.06-3.8.06s-2.8-.01-3.8-.06c-2.5-.11-3.7-1.3-3.8-3.8-.05-1-.06-1.3-.06-3.8s.01-2.8.06-3.8c.11-2.5 1.3-3.7 3.8-3.8 1-.05 1.3-.06 3.8-.06zm0 3.4a4.3 4.3 0 1 0 0 8.6 4.3 4.3 0 0 0 0-8.6zm0 7.1a2.8 2.8 0 1 1 0-5.6 2.8 2.8 0 0 1 0 5.6zm4.5-8.3a1 1 0 1 0 1 1 1 1 0 0 0-1-1z"/></svg>',
    "youtube": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M19.7 7.6a2 2 0 0 0-1.4-1.4C17 5.8 12 5.8 12 5.8s-5 0-6.3.4A2 2 0 0 0 4.3 7.6 21 21 0 0 0 4 12a21 21 0 0 0 .3 4.4 2 2 0 0 0 1.4 1.4c1.3.4 6.3.4 6.3.4s5 0 6.3-.4a2 2 0 0 0 1.4-1.4A21 21 0 0 0 20 12a21 21 0 0 0-.3-4.4zM10.4 14.4V9.6l4.2 2.4z"/></svg>',
    "google": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21.6 12.2c0-.7-.06-1.4-.18-2H12v3.9h5.4a4.6 4.6 0 0 1-2 3v2.5h3.2c1.9-1.75 3-4.3 3-7.4zM12 22c2.7 0 5-.9 6.6-2.4l-3.2-2.5c-.9.6-2 1-3.4 1-2.6 0-4.8-1.8-5.6-4.1H3.1v2.6A10 10 0 0 0 12 22zM6.4 14a6 6 0 0 1 0-3.8V7.6H3.1a10 10 0 0 0 0 8.9zM12 6a5.4 5.4 0 0 1 3.8 1.5L18.7 4.7A9.6 9.6 0 0 0 12 2a10 10 0 0 0-8.9 5.5l3.3 2.6C7.2 7.8 9.4 6 12 6z"/></svg>',
}


def head(title, desc, path, jsonld_extra=""):
    canonical = SITE + path
    biz = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": SITE + "/#business",
        "name": "A Happy Host, LLC",
        "description": "Short-term rental concierge services in Sevierville, Pigeon Forge, and Gatlinburg, TN: cabin setup, rental inspections, seasonal decorating, photo staging, handyman services, and guest experiences.",
        "url": SITE + "/",
        "telephone": "+1-865-314-7564",
        "email": EMAIL,
        "image": SITE + "/images/logo-photo.jpg",
        "logo": SITE + "/images/logo-a-happy-host.png",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "902 McMakin Way",
            "addressLocality": "Pigeon Forge",
            "addressRegion": "TN",
            "postalCode": "37863",
            "addressCountry": "US",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": 35.802524, "longitude": -83.5228981},
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "opens": "09:00", "closes": "17:00",
        }],
        "areaServed": [
            {"@type": "City", "name": "Sevierville"},
            {"@type": "City", "name": "Pigeon Forge"},
            {"@type": "City", "name": "Gatlinburg"},
            {"@type": "AdministrativeArea", "name": "Sevier County, TN"},
        ],
        "sameAs": [s[1] for s in SOCIALS[:4]],
    }
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<!-- TODO: paste Google Search Console verification meta tag here -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="A Happy Host">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}/og-image.png">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/fonts/InterTight-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/SourceSans3-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/css/style.css?v={CSS_V}">
<script type="application/ld+json">{json.dumps(biz, separators=(",", ":"))}</script>
{jsonld_extra}<script src="/js/main.js?v={JS_V}" defer></script>
</head>
<body>
"""


def breadcrumbs(items):
    """items: list of (name, path). Home is implicit first."""
    lst = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}]
    for i, (name, path) in enumerate(items, start=2):
        entry = {"@type": "ListItem", "position": i, "name": name}
        if path:
            entry["item"] = SITE + path
        lst.append(entry)
    data = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": lst}
    return f'<script type="application/ld+json">{json.dumps(data, separators=(",", ":"))}</script>\n'


def service_jsonld(name, path, desc):
    data = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": name,
        "serviceType": name,
        "description": desc,
        "url": SITE + path,
        "provider": {"@id": SITE + "/#business"},
        "areaServed": ["Sevierville TN", "Pigeon Forge TN", "Gatlinburg TN"],
    }
    return f'<script type="application/ld+json">{json.dumps(data, separators=(",", ":"))}</script>\n'


def header(active=""):
    social = "\n".join(
        f'<a href="{url}" aria-label="A Happy Host on {name}" rel="noopener" target="_blank">{ICONS[icon]}</a>'
        for name, url, icon, _ in SOCIALS
    )
    dd = "\n".join(f'<a href="/{slug}">{label}</a>' for slug, label in SERVICES)

    def cur(p):
        return ' aria-current="page"' if active == p else ""

    return f"""<header class="topbar">
  <div class="container topbar-grid">
    <p class="topbar-phone"><a href="tel:{PHONE_TEL}">{PHONE}</a></p>
    <a class="topbar-logo" href="/" aria-label="A Happy Host home">
      <img src="/images/logo-a-happy-host.png" alt="A Happy Host Rental Concierge logo" width="111" height="111">
    </a>
    <div class="topbar-social">
{social}
    </div>
    <button class="nav-toggle" aria-expanded="false" aria-controls="mainmenu" aria-label="Open menu">{ICONS["burger"]}</button>
  </div>
</header>
<nav class="mainnav" aria-label="Main">
  <div class="mainnav-inner" id="mainmenu">
    <a href="/"{cur("home")}>Home</a>
    <a href="/about"{cur("about")}>About</a>
    <a href="/contact"{cur("contact")}>Contact</a>
    <div class="nav-item">
      <a href="/cabinsetup" aria-haspopup="true">Services{ICONS["chevron"]}</a>
      <div class="dropdown">
{dd}
      </div>
    </div>
  </div>
</nav>
"""


def footer():
    svc = "\n".join(f'<li><a href="/{slug}">{label}</a></li>' for slug, label in SERVICES)
    soc = "\n".join(
        f'<a href="{url}" style="background:{color}" aria-label="A Happy Host on {name}" rel="noopener" target="_blank">{FOOTER_SOCIAL_GLYPHS[icon]}</a>'
        for name, url, icon, color in SOCIALS
    )
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <img src="/images/logo-a-happy-host.png" alt="A Happy Host Rental Concierge logo" width="140" height="140" loading="lazy">
        <p class="footer-guest">
          <img src="/images/logo-a-happy-guest.png" alt="A Happy Guest logo" width="58" height="56" loading="lazy">
          <a href="/a-happy-guest">Click here if you're a guest at a rental!</a>
        </p>
      </div>
      <nav aria-label="Footer">
        <h3>Navigation</h3>
        <ul class="footer-links">
          <li><a href="/">Home</a></li>
          <li><a href="/about">About</a></li>
          <li><a href="/contact">Contact</a></li>
          <li><a href="/accessibility">Accessibility</a></li>
          <li><a href="/tos">TOS</a></li>
          <li><a href="/sitemap.xml">Sitemap</a></li>
        </ul>
      </nav>
      <nav aria-label="Services">
        <h3>Services</h3>
        <ul class="footer-links">
{svc}
        </ul>
      </nav>
      <div>
        <h3>Business Hours</h3>
        <div class="hours-row"><span class="hours-label">Mon - Fri</span><span>9:00 am - 5:00 pm</span></div>
        <div class="hours-row"><span class="hours-label">Sat - Sun</span><span>Closed</span></div>
        <div class="hours-row"><span class="hours-label">Emergencies:</span><span>Open 24/7</span></div>
        <div class="hours-row"><span class="hours-label">Phone:</span><span><a href="tel:{PHONE_TEL}">{PHONE}</a></span></div>
        <p style="margin-top:10px"><a href="/contact">Click here for department emails</a></p>
      </div>
      <div class="footer-connect">
        <p>Let&rsquo;s stay connected! Like, follow, and subscribe to see our latest projects, helpful tips, and behind-the-scenes updates.</p>
        <div class="footer-social">
{soc}
        </div>
      </div>
    </div>
  </div>
  <div class="footer-bottom">
    <div class="container footer-bottom-grid">
      <address style="font-style:normal">&copy; 2026 All Rights Reserved | A Happy Host, LLC &middot; 902 McMakin Way, Pigeon Forge, TN 37863 &middot; <a href="tel:{PHONE_TEL}">{PHONE}</a></address>
      <p>Please Report Errors to the <a href="mailto:{EMAIL}">Webmaster</a></p>
    </div>
  </div>
</footer>
<script defer src="/_vercel/insights/script.js"></script>
</body>
</html>
"""


def cta_band(learn_href="/about", contact_label="Contact"):
    return f"""<div class="choose-actions">
        <a class="btn btn-aqua" href="/contact#GetStarted">{contact_label}</a>
        <a class="btn btn-outline" href="{learn_href}">Learn more</a>
      </div>"""


PAGES = {}

# =============================================================== HOME
PAGES["index.html"] = dict(
    title="#1 Services for Rentals | A Happy Host | 865-314-7564",
    desc="We offer expert concierge services for rental property owners and guests in Sevierville, Pigeon Forge & Gatlinburg. Enhance your rental experience today!",
    path="/",
    active="home",
    jsonld="",
    body=f"""<main>
  <section class="hero-home" style="background-image:linear-gradient(rgba(0,0,0,.28),rgba(0,0,0,.28)),url('/images/hero-home.jpg')">
    <div class="hero-home-head">
      <a class="site-link" href="#welcome">A Happy Host</a>
      <h1>Concierge Services</h1>
    </div>
    <div class="hero-strip">
      <div class="container hero-strip-grid">
        <div>
          <a class="btn btn-dark" href="/contact#GetStarted">Contact Us</a>
          <p>When you need a team to call on, we are the place to go. With a strategically located office, we are staffed and ready to take on your projects. From decorating to installations we have the resources your short term rental needs to get the highest ROI possible and save you time.</p>
        </div>
        <div class="hero-stat"><h2>15+</h2><p>qualified workers</p></div>
        <div class="hero-stat"><h2>20+</h2><p>Contractor Relationships</p></div>
        <div class="hero-stat"><h2>5 Stars</h2><p>Average Rating</p></div>
      </div>
    </div>
  </section>

  <section class="section welcome center" id="welcome">
    <div class="container">
      <h2 class="label-h">We're glad you're here.</h2>
      <p>Welcome to A Happy Host, the #1 concierge company for Sevierville, Gatlinburg, Pigeon Forge and surrounding. We are your go to concierge service located in the heart of the Smoky Mountains. We are here to enhance your rental experience, providing personalized attention and top-notch service to ensure your property and guests receive world class care. Our dedicated team is here to provide you with unparalleled support and assistance. From <a href="/seasonal-decorating">seasonal decorating</a> to <a href="/handyman-services">handyman services</a> we are here to assist with local resources for taking care of your needs. Our dedicated team is committed to making your concierge experience stress-free and delightful. As locals with a passion for hospitality, we strive to offer exceptional care and expertise to make sure your guests' visit to the Smokies is unforgettable. Let us be your team for all your rental property needs!</p>
    </div>
  </section>

  <section aria-label="Our services">
    <div class="service-cards">
      <a class="service-card" href="/photo-staging" style="background-image:url('/images/card-photo-staging.jpg')">
        <h3>Photo Staging</h3>
        <p>Let the guest see themselves in your home before they even arrive.</p>
      </a>
      <a class="service-card" href="/rental-inspections" style="background-image:url('/images/card-rental-inspections.jpg')">
        <h3>Rental Inspections</h3>
        <p>Self Managing? Get a monthly inspection for less than one night's refund to your guest.</p>
      </a>
      <a class="service-card" href="/seasonal-decorating" style="background-image:url('/images/card-seasonal-decorating.jpg')">
        <h3>Seasonal Decorating</h3>
        <p>Where creativity meets expertise to elevate your property's appeal throughout the year.</p>
      </a>
      <a class="service-card" href="/cabinsetup" style="background-image:url('/images/card-cabin-setup.jpg')">
        <h3>Cabin Setup</h3>
        <p>Take your rental from empty to ready in less than a week.</p>
      </a>
      <a class="service-card" href="/handyman-services" style="background-image:url('/images/card-handyman.jpg')">
        <h3>Handyman Services</h3>
        <p>There's always something...and we always have someone for the job.</p>
      </a>
      <a class="service-card" href="/a-happy-guest" style="background-image:url('/images/card-happy-guest.jpg')">
        <h3>A Happy Guest</h3>
        <p>Are you a guest staying at a rental? Click to see all the special arrangments we can make for you!</p>
      </a>
    </div>
  </section>

  <section class="section checklist">
    <div class="container">
      <p class="checklist-sub">All Your Rental Needs Solved in One Place</p>
      <h2 class="label-h">Your checklist is our priority.</h2>
      <div class="checklist-grid">
        <div class="check-card">
          {ICONS["search"]}
          <p><a href="/rental-inspections">Inspections</a> - Keep a small matter from getting worse. Get a professional inspection on your rental.</p>
          <p class="check-done">{ICONS["check"]} CHECK!</p>
        </div>
        <div class="check-card">
          {ICONS["garland"]}
          <p><a href="/seasonal-decorating">Decorating</a> - No matter the occasion, we have the perfect team to prepare a space for you.</p>
          <p class="check-done">{ICONS["check"]} CHECK!</p>
        </div>
        <div class="check-card">
          {ICONS["bed"]}
          <p><a href="/cabinsetup">Setup and Staging</a> - We have the experience and resources to make an empty room perfect.</p>
          <p class="check-done">{ICONS["check"]} CHECK!</p>
        </div>
        <div class="check-card">
          {ICONS["tools"]}
          <p><a href="/handyman-services">Handyman Services</a> - No matter the task, we can pair you with the perfect servicer.</p>
          <p class="check-done">{ICONS["check"]} CHECK!</p>
        </div>
      </div>
    </div>
  </section>

  <section class="band band-photo" style="background-image:url('/images/checklist-bg.jpg')">
    <div class="container about-band-grid">
      <img src="/images/guest-occasions.jpg" alt="A Happy Guest welcome treats under a cloche with sparkling water at a rental cabin" loading="lazy" width="768" height="853">
      <div class="about-card">
        <h2 class="label-h">About us</h2>
        <div class="about-card-grid">
          <div><h3>Qualified Team</h3><p>Our team is made up of dedicated professionals who take pride in their work.</p></div>
          <div><h3>Our Mission</h3><p>To give our valued clients the freedom to live their best lives.</p></div>
          <div><h3>Outstanding Support</h3><p>Your satisfaction is our priority, and we go beyond to ensure you have a seamless, stress-free experience.</p></div>
          <div><h3>Same Day Availability</h3><p>We offer many services that are ready to go within a day's heads notice.</p></div>
        </div>
        <a class="btn btn-outline" href="/about">Learn more</a>
      </div>
    </div>
  </section>

  <section class="band band-gray">
    <div class="container">
      <h2 class="label-h">Happy Clients</h2>
      <p class="reviews-intro">We&rsquo;re proud to have earned glowing reviews from clients who love the quality and care we bring to every occasion. Our reviews reflect the trust and confidence our clients place in us.</p>
      <div class="review-grid">
        <article class="review-card">
          <h3>Pinchas Ostreicher</h3>
          <img src="/images/five-stars.png" alt="Five star rating" loading="lazy" width="294" height="50">
          <p>If I could give A Happy Host more than 5 stars, I absolutely would! Amy and Ricky Shaver, along with their exceptional team, have been an absolute blessing to my business...</p>
        </article>
        <article class="review-card">
          <h3>Amanda Daigle</h3>
          <img src="/images/five-stars.png" alt="Five star rating" loading="lazy" width="294" height="50">
          <p>A Happy Host has been an absolute lifesaver on numerous occasions as I run my short-term rental in Gatlinburg from a distance!&nbsp; Their service is always top-notch...</p>
        </article>
        <article class="review-card">
          <h3>Andrew Kensmoe</h3>
          <img src="/images/five-stars.png" alt="Five star rating" loading="lazy" width="294" height="50">
          <p>The team goes above and beyond to help us with our cabins.&nbsp; For things like maintenance, holiday decor, new cabin setup, or even a charcuterie board they are top notch.</p>
        </article>
      </div>
      <a class="reviews-more" href="{CFG["social"]["google"]}" rel="noopener" target="_blank">Click to see more reviews!</a>
      <img class="reviews-stars" src="/images/five-stars.png" alt="5 stars representing a five star company and their 5 star performance" loading="lazy" width="294" height="50">
    </div>
  </section>

  <section class="band band-gray" style="padding-top:0">
    <div class="container work-grid">
      <div>
        <h2 class="label-h">Lets get to work.</h2>
        <p>Are you tired of juggling all the tasks that come with owning rental properties? Let our expert concierge team take the weight off your shoulders! Our comprehensive range of services is tailored to make your property ownership experience a breeze. From setting up your <a href="/cabinsetup">cabins</a> with a touch of elegance to carrying out meticulous <a href="/rental-inspections">rental inspections</a>, we've got you covered every step of the way. Picture your properties adorned with stunning <a href="/seasonal-decorating">seasonal decorations</a> and expertly <a href="/photo-staging">staged</a> to attract top-tier tenants. Need a reliable <a href="/handyman-services">handyman</a> for those occasional fixes? Look no further! Experience the convenience and peace of mind that comes with choosing our concierge services.</p>
        <a class="btn btn-aqua" href="/contact#GetStarted">Get in touch</a>
        <p class="work-outro">Contact us today and let's elevate your rental property management to a whole new level!</p>
      </div>
      <img src="/images/home-work-gift.jpg" alt="Guest welcome gift box wrapped with a teal ribbon by A Happy Host" loading="lazy" width="768" height="1024">
    </div>
  </section>
</main>
""",
)

# =============================================================== ABOUT
PAGES["about.html"] = dict(
    title="#1 Concierge Service for Rentals | A Happy Host | About Us",
    desc="Need expert concierge services? Whatever your needs, we can help! Family-owned rental concierge in the Great Smoky Mountains.",
    path="/about",
    active="about",
    jsonld=breadcrumbs([("About Us", "/about")]),
    body=f"""<main>
  <section class="hero-split">
    <div class="hero-split-text">
      <h1>We Live &amp; Breathe Service</h1>
      <p class="eyebrow">Our Love for Serving Our Clients</p>
      <p><strong>A Happy Host, LLC</strong> is a family-owned rental concierge business located in the Great Smoky Mountains. We are dedicated to helping homeowners manage their investments from a distance. Have a rental in Sevierville, Pigeon Forge, or Gatlinburg? We are the right team for you. Reach out now and see how we can help you manage your rental property!</p>
    </div>
    <div class="hero-split-img" style="background-image:url('/images/about-hero-owners.jpg')" role="img" aria-label="Amy and Ricky Shaver, owners of A Happy Host"></div>
  </section>

  <section class="band band-aqua features-band">
    <div class="container features-grid">
      <div class="feature-item">{ICONS["shield"]}<h3>Trusted by 700+<br>STR Clients</h3></div>
      <div class="feature-item">{ICONS["circlecheck"]}<h3>Friendly &amp;<br>Professional</h3></div>
      <div class="feature-item">{ICONS["handshake"]}<h3>Premium Support Services</h3></div>
      <div class="feature-item">{ICONS["clock"]}<h3>On Time,<br>Every Time</h3></div>
    </div>
  </section>

  <section class="band band-photo why-band" style="background-image:url('/images/about-why-bg.jpg')">
    <div class="container">
      <h2>Why Choose Us?</h2>
      <div class="why-grid">
        <p class="why-item">{ICONS["check_w"]} Years of professional experience</p>
        <p class="why-item">{ICONS["check_w"]} Team of people who love their job</p>
        <p class="why-item">{ICONS["check_w"]} Friendly service and competitive rates</p>
        <p class="why-item">{ICONS["check_w"]} Excellent reviews and satisfied clients</p>
      </div>
    </div>
  </section>

  <section class="section" style="background:#fff">
    <div class="container excerpt-grid">
      <div>
        <h2 class="label-h center">A Brief Excerpt</h2>
        <p>Hi! We're the Shavers! In 2021, COVID changed everything for our family. On September 2, 2021 our family was diagnosed with COVID19. Little did we know our lives would soon change. Rick became very ill with COVID pneumonia and would be home bound for months dependent on home 02. This illness cost him his corporate job and nearly his life. We lost so much income that we were forced to look for new careers. Through a literal dream, A Happy Host, LLC was born.</p>
        <p>Hi, I am Amy. A little background, I purchased my first STR in 2005 at 25 years old. It was a project with my late father. There was little STR Support in 2005, this leaving me to learn the basics of STR's to myself. Through decades of experience we are now able to help STR owners thrive and their guests make the best memories in the Smokies!</p>
      </div>
      <img src="/images/about-excerpt.png" alt="Guest enjoying popcorn in a cabin home theater prepared by A Happy Host" loading="lazy" width="768" height="1152">
    </div>
  </section>

  <section class="band band-gray">
    <div class="container cta-strip">
      <img src="/images/about-office-doors.jpg" alt="A Happy Host office entrance in Pigeon Forge, Tennessee" loading="lazy" width="768" height="1024">
      <div>
        <h2>Ready to let us serve your property?</h2>
        <p>Head on over to our <a href="/contact">contact page</a> and let's get started!</p>
        <a class="btn btn-gray" href="/contact#GetStarted">Contact Us</a>
      </div>
    </div>
  </section>
</main>
""",
)

# =============================================================== CONTACT
PAGES["contact.html"] = dict(
    title="#1 Concierge Service for Rentals | A Happy Host | Contact",
    desc="Get expert help managing your rental property. Call 865-314-7564 or visit us at 902 McMakin Way, Pigeon Forge, TN.",
    path="/contact",
    active="contact",
    jsonld=breadcrumbs([("Contact", "/contact")]),
    body=f"""<main>
  <section class="hero-split">
    <div class="hero-split-text">
      <h1>Get In Touch</h1>
      <p class="eyebrow">We Are Ready to Hear From You</p>
      <p>In all occasions of communication, we are excited to get together. You are welcome to come by our office at 902 McMakin Way, Pigeon Forge, TN. You can also give us a call, email us, or fill out the form below and someone will give you a call.</p>
      <p>Talk to you soon!</p>
      <p><a href="mailto:{EMAIL}"><strong>{EMAIL}</strong></a></p>
      <p><a href="tel:{PHONE_TEL}"><strong>{PHONE}</strong></a></p>
    </div>
    <div class="hero-split-img" style="background-image:url('/images/contact-hero.jpg')" role="img" aria-label="A Happy Host Rental Concierge logo on the office window"></div>
  </section>

  <section class="section" id="GetStarted" style="background:#fff">
    <div class="container form-section-grid">
      <div>
        <h2 class="label-h">Get Started Now</h2>
        <p>Ready to have a better, more impactful rental experience? Setting up an account is quick and easy. Our team is ready to take your call.</p>
        <p style="margin-top:16px">Your new and improved rental support program is a form away!</p>
      </div>
      <form class="contact-form" action="#" method="post" novalidate>
        <h2 class="visually-hidden" style="position:absolute;left:-9999px">Contact Us</h2>
        <label for="f-name">Full Name</label>
        <input id="f-name" name="name" type="text" autocomplete="name" required placeholder="Enter your full name">
        <label for="f-email">Email</label>
        <input id="f-email" name="email" type="email" autocomplete="email" required placeholder="Enter your email">
        <label for="f-phone">Phone Number</label>
        <input id="f-phone" name="phone" type="tel" autocomplete="tel" placeholder="+123">
        <label for="f-message">Message</label>
        <textarea id="f-message" name="message" required placeholder="Tell us a bit about your needs"></textarea>
        <button class="btn btn-dark" type="submit">Submit</button>
        <p class="form-status ok" role="status">Thank you for contacting us. We will get back to you as soon as possible.</p>
        <p class="form-status err" role="alert">Oops, there was an error sending your message. Please try again later.</p>
      </form>
    </div>
    <div class="container">
      <p class="form-note">*By providing your phone number, you agree to receive SMS messages from A Happy Host. Message frequency varies. Message &amp; data rates may apply. Reply STOP to opt out. See our <a href="/tos">terms of service (TOS)</a> for details.</p>
    </div>
  </section>

  <section class="section">
    <div class="container contact-cards">
      <div class="contact-card">
        {ICONS["envelope"]}
        <h3>Email Contact</h3>
        <p>General Inquiries<br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
        <p>Inspections<br><a href="mailto:inspections@ahappyhostgsm.com">inspections@ahappyhostgsm.com</a></p>
        <p>Concierge Services<br><a href="mailto:concierge@ahappyhostgsm.com">concierge@ahappyhostgsm.com</a></p>
        <p>Seasonal Decorating<br><a href="mailto:decor@ahappyhostgsm.com">decor@ahappyhostgsm.com</a></p>
      </div>
      <div class="contact-card">
        {ICONS["phone"]}
        <h3>Phone</h3>
        <p>Office <a href="tel:{PHONE_TEL}">{PHONE}</a></p>
      </div>
      <div class="contact-card">
        {ICONS["pin"]}
        <h3>Office</h3>
        <address style="font-style:normal">902 McMakin Way, Pigeon Forge, TN 37863</address>
      </div>
    </div>
  </section>
</main>
""",
)


def service_page(slug, h1, hero_img, hero_paras, intro_eyebrow, intro_html, rows, extra="", choose=None, hero_btn="btn-dark"):
    """Build the shared service-page layout."""
    hero_p = "\n".join(f"<p>{p}</p>" for p in hero_paras)
    rows_html = ""
    for i, (title, paras, img, alt) in enumerate(rows):
        flip = " flip" if i % 2 else ""
        ptxt = "\n".join(f"<p>{p}</p>" for p in paras)
        rows_html += f"""
  <div class="feature-row{flip}">
    <img class="photo" src="{img}" alt="{alt}" loading="lazy" width="1150" height="480">
    <div class="feature-card">
      <h3>{title}</h3>
      {ptxt}
    </div>
  </div>"""
    choose_html = ""
    if choose:
        choose_html = f"""
  <section class="section">
    <div class="container choose-grid">
      <img src="{choose["img"]}" alt="{choose["alt"]}" loading="lazy" width="768" height="520">
      <div>
        <h2 class="{choose.get("hclass", "big-h")} center">{choose["title"]}</h2>
        {choose["html"]}
        {cta_band()}
      </div>
    </div>
  </section>"""
    return f"""<main>
  <section class="hero-service" style="background-image:linear-gradient(rgba(0,0,0,.30),rgba(0,0,0,.30)),url('{hero_img}')">
    <div class="container">
      <h1>{h1}</h1>
      <div class="hero-panel">
{hero_p}
      </div>
      <a class="btn {hero_btn}" href="/contact#GetStarted">Contact</a>
    </div>
  </section>

  <section class="section svc-intro">
    <div class="container">
      <p class="eyebrow">{intro_eyebrow}</p>
      {intro_html}
      <a class="btn btn-outline" href="/about">About Us</a>
    </div>
  </section>

  <section class="band band-gray" style="padding-bottom:70px">
{rows_html}
  </section>
{extra}{choose_html}
</main>
"""


# =============================================================== CABIN SETUP
PAGES["cabinsetup.html"] = dict(
    title="Best Cabin Setup Services | A Happy Host",
    desc="Enhance your rental with our expert cabin setup services in Sevier County, TN. Contact us to create inviting spaces for your guests today!",
    path="/cabinsetup",
    active="services",
    jsonld=breadcrumbs([("Services", None), ("Cabin Setup", "/cabinsetup")])
    + service_jsonld("Cabin Setup", "/cabinsetup", "Complete short-term rental cabin setup: furniture, bedding, supplies, and amenities arranged before guest arrival."),
    body=service_page(
        "cabinsetup",
        "Cabin Setup",
        "/images/card-cabin-setup.jpg",
        [
            "Get advice from a local professional. We know what lasts, where to get it, and what to think about before its too late!",
            "From arranging furniture to curating decorative elements, we pay close attention to every detail to create a cohesive and inviting ambiance that sets your rental cabins apart from the competition. Our focus on functionality ensures that the setup not only looks aesthetically pleasing but also enhances the efficiency and comfort of the space for guests.",
        ],
        "Cabin Setup",
        """<p>Our cabin setup service is not just about arranging furniture and setting up amenities &ndash; it's about unlocking a world of comfort, style, and convenience that transforms your rental property into a welcoming retreat. At our rental concierge service, A Happy Host, we understand that the little details make a big difference in how you experience your vacation, and that's why our cabin setup service is designed with care and expertise.</p>
      <p>From arranging furniture to curating decorative elements, we pay close attention to every detail to create a cohesive and inviting ambiance that sets your rental cabins apart from the competition. Our focus on functionality ensures that the setup not only looks aesthetically pleasing but also enhances the efficiency and comfort of the space for guests.</p>""",
        [
            (
                "We Get It.",
                [
                    "We recognize that each guest has unique preferences and requirements when it comes to their cabin setup. Whether it's a family seeking a cozy space for quality time together, a couple looking for a romantic escape, or a solo traveler in search of tranquility, our team customizes the setup to suit the individual needs. We take the time to understand preferences and specifications, ensuring that your cabin reflects the needed style and enhances the overall Gatlinburg, Pigeon Forge or Sevierville experience.",
                ],
                "/images/cabin-divider.jpg",
                "Cozy staged bedding and pillows in a Smoky Mountain rental cabin",
            ),
            (
                "No Detail Overlooked",
                [
                    "When you choose our cabin setup service, you can rest assured that every aspect of your rental property will be immaculately prepared before the guest arrival. From arranging furniture to setting up bedding, stocking essential supplies, and ensuring all amenities are in place, we leave no detail overlooked. Our meticulous approach to cabin setup guarantees that everything is in perfect order, allowing you to step into a welcoming and well-prepared space from the moment of arrival.",
                ],
                "/images/cabin-photo.jpg",
                "Dining table styled with dishes and greenery during a cabin setup",
            ),
        ],
        extra="""
  <div class="carousel" aria-label="Cabin setup photo gallery">
    <div class="carousel-track">
      <img src="/images/carousel-9428.jpg" alt="Staged living area in a Smoky Mountain cabin" loading="lazy" width="1150" height="560">
      <img src="/images/carousel-9427.jpg" alt="Cozy seating arranged during a cabin setup" loading="lazy" width="1150" height="560">
      <img src="/images/carousel-9419.jpg" alt="Finished cabin setup with decor accents" loading="lazy" width="1150" height="560">
    </div>
    <div class="carousel-dots" role="tablist"></div>
  </div>""",
        choose=dict(
            img="/images/contact-hero.jpg",
            alt="A Happy Host Rental Concierge window decal at the Pigeon Forge office",
            title="When You Choose Us.",
            hclass="label-h",
            html="""<p class="text-center"><strong>Experience and reliability are what set us apart from the others.</strong></p>
        <p>When you choose our cabin setup service, you're choosing Sevier County's premier provider of tailored, personalized, and top-quality cabin setup services. We take pride in our attention to detail, our commitment to excellence, and our dedication to ensuring that your rental property is a welcoming and inviting space that meets your needs and exceeds your expectations.</p>
        <p>Trust us to transform your cabin into a sanctuary of comfort and style, where the guests can relax, unwind, and create cherished memories in the heart of the Smoky Mountains.</p>""",
        ),
    ),
)

# =============================================================== RENTAL INSPECTIONS
PAGES["rental-inspections.html"] = dict(
    title="Professional Rental Inspections | A Happy Host",
    desc="Ensure your rental property is guest-ready with our inspection service in Sevierville, Pigeon Forge & Gatlinburg. Contact us for expert assistance today!",
    path="/rental-inspections",
    active="services",
    jsonld=breadcrumbs([("Services", None), ("Rental Inspections", "/rental-inspections")])
    + service_jsonld("Rental Inspections", "/rental-inspections", "Detailed walkthrough inspections of short-term rentals covering plumbing, electrical, appliances, HVAC, and structural components."),
    body=service_page(
        "rental-inspections",
        "Rental Inspections",
        "/images/inspections-hero.jpg",
        [
            "This service is geared toward your peace of mind and the guest leaving a 5-star review.",
            "Our dedication to customer satisfaction drives us to go above and beyond to deliver outstanding results. We understand that the success of a rental property hinges on its presentation and marketability, and our Rental Staging Concierge service is designed to maximize the property's potential and attract quality tenants.",
        ],
        "Rental Inspections",
        f"""<p><strong>Maintain those 5-star reviews!</strong></p>
      <p>As part of our comprehensive rental concierge services, our rental inspection service is designed to provide property owners with peace of mind and assurance that their rental units are well-maintained and ready for guests. We understand the importance of maintaining the integrity and quality of your property while ensuring a positive experience for your visitors. Our rental inspection process is tailored to identify any potential issues or maintenance requirements, allowing you to address them promptly and maintain the property's value and excitement for your guests.</p>
      <p><a href="/contact#GetStarted">Contact us</a> now to get started.</p>""",
        [
            (
                "Inspection Process",
                [
                    "Our rental inspection service involves a detailed walkthrough of the property, both inside and out. We carefully assess the condition of key areas such as plumbing, electrical systems, appliances, HVAC units, and structural components. By conducting a thorough examination, we aim to identify any maintenance issues or safety concerns that need attention before guests arrive. Our experienced team is trained to spot both minor and major issues to ensure your property is in top shape for your guests.",
                ],
                "/images/card-rental-inspections.jpg",
                "Two inspectors performing a walkthrough inspection at a rental home",
            ),
            (
                "Preventative Measures",
                [
                    "One of the primary goals of our rental inspections is to prevent small problems from escalating into costly repairs. By proactively addressing maintenance needs identified during the inspection, we help you avoid unexpected issues that could disrupt your guests' stay or lead to negative reviews. From addressing minor leaks to changing air filters and conducting routine maintenance tasks, our preventive measures are designed to keep your rental property in optimal condition.",
                ],
                "/images/handyman-photo2.png",
                "Technician performing preventative maintenance with a drill",
            ),
        ],
        extra=f"""
  <section class="section">
    <div class="container infographic-grid">
      <figure>
        <img src="/images/inspections-diagram.png" alt="Why do I need inspections? Diagram of inspection areas: electrical assessment, safety checks, plumbing check, kitchen audit, tech check, hot tub analysis, happy guests, overall cleanliness, and real time photos" loading="lazy" width="900" height="1100">
        <a class="btn btn-gray" href="/downloads/inspection-diagram.jpg" download>Download Diagram</a>
      </figure>
      <figure>
        <img src="/images/inspections-form.png" alt="Why do I need inspections? Explanation of how monthly preventative inspections protect your investment, ensure 5-star reviews, and offer cost-effective peace of mind" loading="lazy" width="900" height="1100">
        <a class="btn btn-gray" href="/downloads/inspection-form.jpg" download>Download Form</a>
      </figure>
    </div>
  </section>""",
        choose=dict(
            img="/images/staging-difference.jpg",
            alt="Coffee and pastry styled on a cabin table after an inspection visit",
            title="Expert Guidance",
            hclass="label-h",
            html="""<p>In addition to identifying maintenance needs, our rental inspection service offers expert guidance and recommendations for optimizing the guest experience. We provide insights on potential upgrades, renovations, or enhancements that could add value to your property and attract more renters. Whether it's suggesting energy-efficient appliances, modernizing interior decor, or <a href="/seasonal-decorating">enhancing outdoor amenities</a>, our team offers tailored recommendations to help you elevate your property to meet the expectations of today's rental market.</p>
        <p><strong>Want more 5-star reviews?</strong> Give us a call now to get started!</p>""",
        ),
        hero_btn="btn-aqua",
    ),
)

# =============================================================== SEASONAL DECORATING
PAGES["seasonal-decorating.html"] = dict(
    title="Beautiful Seasonal Decorating | A Happy Host",
    desc="Elevate your rental with seasonal decor tailored to your vision in Gatlinburg, Pigeon Forge & Sevierville. Contact us for a consultation today!",
    path="/seasonal-decorating",
    active="services",
    jsonld=breadcrumbs([("Services", None), ("Seasonal Decorating", "/seasonal-decorating")])
    + service_jsonld("Seasonal Decorating", "/seasonal-decorating", "Year-round seasonal decorating for short-term rentals, from winter wonderlands to fall themes, including storage of decorations."),
    body=service_page(
        "seasonal-decorating",
        "Seasonal Decorating",
        "/images/seasonal-hero.jpg",
        [
            "No more worrying about storing your decorations! We have the perfect seasonal decor to give your rental that special touch of excitement for every time of year.",
            "Our process begins with a personalized consultation where we delve into your unique vision, property style, and seasonal goals. We listen attentively to your preferences, ensuring that the seasonal decor reflects your taste and aligns with the ambiance you wish to cultivate for your tenants and guests.",
        ],
        "Seasonal Decorating",
        """<p>Seasonal decorating transforms rental properties into captivating spaces that offer guests unforgettable experiences. At our concierge service based in Gatlinburg, Pigeon Forge, and Sevierville, we specialize in concierge services regarding seasonal decorating, where creativity meets expertise to elevate your property's appeal all year long.</p>
      <p><a href="/contact#GetStarted">Contact A Happy Host</a> to book your decorating soon!</p>""",
        [
            (
                "Personalized Magic",
                [
                    "At A Happy Host, we understand that every guest experience begins with the welcoming ambiance of your rental property. Our seasonal decorating service is thoughtfully curated to reflect unique tastes, preferences, and requests, ensuring that your space radiates warmth and charm. Whether you desire a cozy winter wonderland, a colorful spring oasis, a vibrant summer retreat, or a rustic fall haven, we specialize in tailoring our decorations to suit the season and your distinctive aesthetic.",
                ],
                "/images/seasonal-photo.jpg",
                "Fall arrangement with leather pumpkin and florals styled in a rental living room",
            ),
            (
                "No Detail Overlooked",
                [
                    "Our team meticulously selects high-quality decor pieces that harmonize with your property's aesthetic and create a welcoming atmosphere that resonates with each season's spirit. Whether you envision a cozy autumn theme with warm hues and rustic accents or a festive winter wonderland brimming with holiday cheer, we bring your ideas to life with precision and creativity.",
                ],
                "/images/card-seasonal-decorating.jpg",
                "Christmas tree and holiday decorations installed at a rental cabin fireplace",
            ),
        ],
        choose=dict(
            img="/images/seasonal-owners.jpg",
            alt="The owners of A Happy Host outside in the Smoky Mountains",
            title="When You Choose Us.",
            hclass="label-h",
            html="""<p>Our dedication to excellence extends to our customer service approach in seasonal decorating. We keep open lines of communication throughout the process, ensuring that you are informed and involved as much as you would like. From initial concept development to final installation, we prioritize transparency, collaboration, and responsiveness to ensure a seamless and enjoyable experience for our clients.</p>
        <p>In conclusion, our seasonal decorating services offer property owners a hassle-free and transformative way to enhance their rental properties year-round. Let us bring creativity, expertise, and a touch of seasonal magic to your properties, creating inviting spaces that delight guests and leave a lasting impression on guests.</p>""",
        ),
    ),
)

# =============================================================== PHOTO STAGING
PAGES["photo-staging.html"] = dict(
    title="Professional Photo Staging Services | A Happy Host",
    desc="Boost your rental's appeal with expert photo staging in the Smoky Mountains. Attract guests & enhance your listing today!",
    path="/photo-staging",
    active="services",
    jsonld=breadcrumbs([("Services", None), ("Photo Staging", "/photo-staging")])
    + service_jsonld("Photo Staging", "/photo-staging", "Professional photo staging for short-term rental listings: furniture arrangement, decor, and lighting optimized for captivating listing photos."),
    body=service_page(
        "photo-staging",
        "Photo Staging",
        "/images/staging-hero.jpg",
        [
            "In today's competitive rental market, having stunning photos that showcase your property's best features is essential for attracting guests and standing out from the crowd. Whether you are a new property owner looking to launch your rental business or a seasoned host looking to refresh your listing's visual appeal, our photo staging service is the perfect solution to elevate your property's online presence and increase its booking potential.",
        ],
        "Photo Staging",
        """<p>As the premier provider of concierge services for rental property owners in our area, we are proud to offer our specialized service for photo staging tailored for short-term rentals. We understand the importance of having high-quality photos that showcase your property in the best possible light, and our expert team is here to help you present your rental space in an attractive and inviting way.</p>""",
        [
            (
                "Stand Out.",
                [
                    "Effective photo staging is a critical component of your rental property listing. When guests are browsing through various options online, the first impression they get from your property's photos can make all the difference in catching their interest and ultimately leading to a booking. Our photo staging service focuses on highlighting the key features and unique selling points of your rental property to make it stand out among the competition.",
                ],
                "/images/card-photo-staging.jpg",
                "Staged cabin living room with mounted TV and styled sofa ready for listing photos",
            ),
            (
                "Your property shines.",
                [
                    "Our experienced team of staging professionals has a keen eye for detail and an understanding of what makes a property appealing to potential renters. We will be glad to work closely with you to understand your property's unique charm and style, and then carefully stage each room to create inviting and captivating photographs that will attract guests and set your property apart. From arranging furniture and decor to optimizing lighting and framing shots, we take care of every aspect of the photo staging process to ensure that your property shines.",
                ],
                "/images/guest-chef-table.jpg",
                "Table place setting staged with dishware and linens for listing photos",
            ),
        ],
        extra="""
  <div class="carousel" aria-label="Photo staging gallery">
    <div class="carousel-track">
      <img src="/images/carousel-9428.jpg" alt="Staged living space in a Smoky Mountain rental" loading="lazy" width="1150" height="560">
      <img src="/images/carousel-9427.jpg" alt="Dining area staged for photos at a rental cabin" loading="lazy" width="1150" height="560">
      <img src="/images/card-cabin-setup.jpg" alt="Sectional sofa and coffee table staged in a cabin living room" loading="lazy" width="1150" height="560">
      <img src="/images/carousel-9419.jpg" alt="Bedroom staged with layered bedding for listing photos" loading="lazy" width="1150" height="560">
      <img src="/images/carousel-9398.jpg" alt="Cozy seating nook staged at a rental property" loading="lazy" width="1150" height="560">
      <img src="/images/carousel-9396.jpg" alt="Kitchen staged with props for rental listing photos" loading="lazy" width="1150" height="560">
      <img src="/images/cabin-divider.jpg" alt="Outdoor deck staged with furniture and drinks" loading="lazy" width="1150" height="560">
    </div>
    <div class="carousel-dots" role="tablist"></div>
  </div>""",
        choose=dict(
            img="/images/staging-difference.jpg",
            alt="Styled coffee and pastry vignette showing staging details",
            title="The Difference.",
            hclass="label-h",
            html="""<p>Contact us today to learn more about our photo staging service and how we can help you create captivating images that will drive bookings and maximize your rental property's potential. Trust the experts at our concierge service to showcase your property in its best light and make a lasting impression on potential guests.</p>""",
        ),
    ),
)

# =============================================================== HANDYMAN SERVICES
PAGES["handyman-services.html"] = dict(
    title="Experienced Handyman Services | A Happy Host",
    desc="Get reliable handyman services for your rental property in Sevier County, TN. Contact us for efficient repairs & maintenance today!",
    path="/handyman-services",
    active="services",
    jsonld=breadcrumbs([("Services", None), ("Handyman Services", "/handyman-services")])
    + service_jsonld("Handyman Services", "/handyman-services", "Concierge handyman services for rental property owners: scheduled repairs and maintenance completed on time by skilled craftsmen."),
    body=service_page(
        "handyman-services",
        "Handyman Services",
        "/images/card-handyman.jpg",
        [
            "Our team will schedule convenient service appointments at times that suit you best. Whether it's a quick repair or a more extensive project, our handymen arrive punctually and fully equipped to handle the task at hand. We pride ourselves on our efficient service delivery, completing projects on time and with meticulous attention to detail.",
        ],
        "Handyman Services",
        f"""<p>We understand that property maintenance can be a time-consuming and often stressful aspect of rental property ownership. That's why we tailor our concierge handyman services around alleviating these burdens by providing a specialized and professional handyman service tailored to meet the unique needs of property owners.</p>
      <p>Call or <a href="/contact#GetStarted">contact us</a> to schedule your service now! <a href="tel:{PHONE_TEL}"><strong>{PHONE}</strong></a></p>""",
        [
            (
                "Our Commitment.",
                [
                    "When you choose our handyman concierge services, you can expect a seamless and hassle-free customer experience from start to finish. Our commitment to exceptional service extends beyond just completing the necessary repairs; we strive to make the entire maintenance process as stress-free as possible for you.",
                    "From the moment you schedule an appointment with us, you can trust that your property is in capable hands. Our handymen arrive on time, ready to work, and prioritize completing repairs efficiently without compromising on quality. We value your time and aim to minimize disruptions to your rental schedule by ensuring that repairs are completed promptly and to your satisfaction.",
                ],
                "/images/handyman-photo1.png",
                "Handyman working on kitchen cabinets at a rental property",
            ),
            (
                "Professionalism.",
                [
                    "Our dedication to professionalism and excellence is evident in the quality of work we outsource. We take pride in our craftsmen and their attention to detail, ensuring that all repairs are completed to the highest standards. Their commitment to you extends to the materials and tools they use, ensuring that your property receives lasting and durable repairs.",
                ],
                "/images/handyman-photo2.png",
                "Craftsman driving a screw with a cordless drill during a repair",
            ),
        ],
        extra="""
  <div class="divider-photo" style="background-image:url('/images/handyman-divider.png')" role="img" aria-label="Tools and hardware arranged around a red house with a heart"></div>""",
        choose=dict(
            img="/images/handyman-divider.png",
            alt="Wrenches, hammer, and hardware arranged around a red house with a heart cutout",
            title="We Go Beyond.",
            html="""<p>Our Sevier County based Handyman Services go beyond just fixing maintenance issues &ndash; we offer a comprehensive and reliable solution for property owners seeking peace of mind and exceptional service. With our specialized approach, skilled team, and commitment to customer satisfaction, we are your trusted partner in maintaining the value and appeal of your rental properties.</p>
        <p>Contact us today to experience the difference our concierge handyman services can make for your property maintenance needs.</p>""",
        ),
    ),
)

# =============================================================== A HAPPY GUEST
PAGES["a-happy-guest.html"] = dict(
    title="Guest Concierge Services for Rentals | A Happy Host",
    desc="Enhance your vacation with personalized concierge services in the Smoky Mountains. Contact A Happy Host for in-home chefs & event planning!",
    path="/a-happy-guest",
    active="services",
    jsonld=breadcrumbs([("Services", None), ("A Happy Guest", "/a-happy-guest")])
    + service_jsonld("A Happy Guest — Guest Concierge Services", "/a-happy-guest", "Vacation guest concierge services: proposals, in-home chefs, special occasions, and custom experiences at Smoky Mountain rentals."),
    body=service_page(
        "a-happy-guest",
        "A Happy Guest!",
        "/images/guest-hero-boards.png",
        [
            "Are you looking for the perfect getaway? If so, our Happy Guest Services are for you. From an in-home chef to special birthday or proposal events, we specialize in providing you, your friends, and your family with the most unforgettable vacation. Whatever it is, we have a huge range of services geared toward making your trip absolutely unforgettable.",
        ],
        "A Happy Guest",
        """<p>We believe that your Smoky Mountain vacation experience should be the best it can be. That's why we provide a warm and personalized touch for every service you request. From customized messages to personalized recommendations on local attractions and dining options, we strive to make you feel right at home from the moment they arrive to your vacation rental. Our goal is to help you create a memorable experience that will last a lifetime.</p>
      <p><strong>Check out some examples of our premier services below!</strong></p>""",
        [
            (
                "Proposals.",
                [
                    "Ready to pop the question? We love to plan, prepare, and assist in helping you craft that special moment. Whether its in a cabin or on top of a mountain, we can connect you with the best photographer and go ahead of you to your special location to prepare for your arrival.",
                    'Craft the perfect proposal with our proposal experience services! Call now at <a href="tel:+18653147564"><strong>865-314-7564</strong></a>',
                ],
                "/images/guest-proposals.jpg",
                "Proposal setup at a cabin with a Will You Marry Me banner, rose petals, and balloons",
            ),
            (
                "Chef Services.",
                [
                    "From large parties to just a couple people, we have the experience for you. Always going out to eat on vacation because you don't want to cook? What if you could dine in without cooking?",
                    "<strong>Let us book the right cook for you so you don't have to!</strong>",
                ],
                "/images/guest-chef-table.jpg",
                "Elegant dinner place setting prepared for an in-cabin chef experience",
            ),
            (
                "Special Occasions.",
                [
                    "From birthday parties to sports teams we have the balloons, confetti, and delicious treats to help you SAVE time and HAVE a great time. We would love to get information about your occasion and come up with exciting ways to improve the experience at your rental location.",
                    '<a href="/contact#GetStarted"><strong>Contact A Happy Host</strong></a> now to get started!',
                ],
                "/images/guest-occasions.jpg",
                "Welcome treats under a glass cloche with sparkling water and an A Happy Guest card",
            ),
            (
                "Everything Else.",
                [
                    "Do you have a special occasion, event, vacation dreams, or casual needs that you believe we could help improve or make easier on you? That's what A Happy Guest is all about! It's our goal to take your trip from just a regular vacation to an unforgettable version of that trip you never thought was possible! In short, if you have a vacation dream, we have a way to make it come true.",
                ],
                "/images/guest-collage-celebrate.jpg",
                "Collage of A Happy Guest celebrations: birthdays, proposals, and party setups",
            ),
        ],
        choose=dict(
            img="/images/guest-gumballs.jpg",
            alt="Candy machines filled with colorful gumballs at a rental cabin",
            title="We Go Beyond.",
            html="""<p>In conclusion, at A Happy Host, we love to make A Happy Guest. Designed to elevate your experience at your rental in Pigeon Forge, Gatlinburg, Sevierville, and the Smoky Mountains! With a focus on personalization, support, local expertise, and special requests, we are dedicated to helping you create exceptional and memorable experiences. Let us provide you with a seamless and enjoyable stay by maximizing your rental potential.</p>
        <p>Contact a concierge now to see how we can take you trip to the next level.</p>""",
        ),
    ),
)

# =============================================================== ACCESSIBILITY
PAGES["accessibility.html"] = dict(
    title="Accessibility Statement | A Happy Host | 865-314-7564",
    desc="A Happy Host, LLC strives to ensure its services are accessible to people with disabilities. Read our accessibility statement.",
    path="/accessibility",
    active="",
    jsonld=breadcrumbs([("Accessibility", "/accessibility")]),
    body=f"""<main class="section legal">
  <div class="container narrow">
    <h1>A Happy Host, LLC Accessibility Statement</h1>
    <p class="date">Updated: January 2025.</p>
    <h2>General:</h2>
    <p>A Happy Host, LLC strives to ensure that its services are accessible to people with disabilities. A Happy Host, LLC has invested a significant amount of resources to help ensure that its website is made easier to use and more accessible for people with disabilities, with the strong belief that every person has the right to live with dignity, equality, comfort and independence.</p>
    <h2>Accessibility on ahappyhost.com:</h2>
    <p>ahappyhost.com is built with semantic HTML, keyboard-navigable menus, descriptive alternative text, and sufficient color contrast to improve its compliance with the Web Content Accessibility Guidelines (WCAG 2.1).</p>
    <h2>Disclaimer:</h2>
    <p>A Happy Host, LLC continues its efforts to constantly improve the accessibility of its site and services in the belief that it is our collective moral obligation to allow seamless, accessible and unhindered use also for those of us with disabilities.</p>
    <p>Despite our efforts to make all pages and content on ahappyhost.com fully accessible, some content may not have yet been fully adapted to the strictest accessibility standards. This may be a result of not having found or identified the most appropriate technological solution.</p>
    <h2>Here For You:</h2>
    <p>If you are experiencing difficulty with any content on ahappyhost.com or require assistance with any part of our site, please contact us during normal business hours as detailed below and we will be happy to assist.</p>
    <h2>Contact Us</h2>
    <p>If you wish to report an accessibility issue, have any questions or need assistance, please contact A Happy Host, LLC Customer Support as follows:</p>
    <p>Phone: <a href="tel:{PHONE_TEL}">+1 (865) 314-7564</a><br>Email: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
  </div>
</main>
""",
)

# =============================================================== TOS
PAGES["tos.html"] = dict(
    title="Terms of Service | A Happy Host | 865-314-7564",
    desc="Terms of Service for ahappyhost.com, operated by A Happy Host, LLC, including our SMS messaging terms.",
    path="/tos",
    active="",
    jsonld=breadcrumbs([("Terms of Service", "/tos")]),
    body=f"""<main class="section legal">
  <div class="container narrow">
    <h1>A Happy Host, LLC Terms of Service</h1>
    <p class="date">Effective date: January 2025</p>
    <p>These Terms of Service ("Terms") govern your use of ahappyhost.com (the "Website"), operated by A Happy Host, LLC ("we", "us", or "our").</p>
    <h2>1. Acceptance of Terms</h2>
    <p>By accessing our Website, you agree to be bound by these Terms. If you disagree with any part of the terms, then you may not access the Website.</p>
    <h2>2. Intellectual Property</h2>
    <p>The Website and its original content, features, and functionality are and will remain the exclusive property of A Happy Host, LLC. The Website is protected by copyright, trademark, and other laws of both the United States and foreign countries.</p>
    <h2>3. User Conduct</h2>
    <p>You agree not to use the Website in any way that is harmful, illegal, obscene, threatening, harassing, defamatory, or otherwise objectionable.</p>
    <h2>4. Limitation of Liability</h2>
    <p>In no event shall A Happy Host, LLC be liable for any indirect, incidental, special, consequential or punitive damages, including without limitation, loss of profits, data, use, goodwill, or other intangible losses, resulting from your access to or use of or inability to access or use the Website.</p>
    <h2>5. Changes to These Terms</h2>
    <p>We reserve the right, at our sole discretion, to modify or replace these Terms at any time. By continuing to access or use our Website after those revisions become effective, you agree to be bound by the revised terms.</p>
    <h2>6. Termination</h2>
    <p>We may terminate or suspend your access to the Website immediately, without prior notice or liability, for any reason whatsoever, including without limitation if you breach the Terms.</p>
    <h2>7. Messaging/SMS Terms:</h2>
    <p>SMS messages may be used for scheduling, updates, and promotions. To stop receiving messages, text &ldquo;STOP&rdquo; to the shortcode. To resume, sign up as initially.</p>
    <p>For assistance, reply with &ldquo;HELP&rdquo; or contact <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
    <p>Message and data rates may apply. Frequency varies. Contact your wireless provider for details about your text or data plan.</p>
    <h2>8. Contact Us</h2>
    <p>If you have any questions about these Terms, please contact us at: <a href="tel:{PHONE_TEL}">{PHONE}</a></p>
  </div>
</main>
""",
)

# =============================================================== 404
PAGES["404.html"] = dict(
    title="Page Not Found | A Happy Host",
    desc="The page you are looking for could not be found. Explore A Happy Host's rental concierge services.",
    path="/404",
    active="",
    jsonld="",
    body=f"""<main class="section center">
  <div class="container narrow">
    <h1 class="big-h" style="text-decoration:none">Page not found</h1>
    <p>Sorry, we couldn't find that page. It may have moved, or the link may be out of date.</p>
    <p style="margin-top:20px">Head back to the <a href="/">home page</a>, browse our <a href="/cabinsetup">services</a>, or give us a call at <a href="tel:{PHONE_TEL}"><strong>{PHONE}</strong></a>.</p>
    <p style="margin-top:30px"><a class="btn btn-aqua" href="/">Back to Home</a></p>
  </div>
</main>
""",
)


def build():
    titles, descs = set(), set()
    for fname, page in PAGES.items():
        if page["path"] != "/404":
            assert page["title"] not in titles, f"duplicate title: {page['title']}"
            assert page["desc"] not in descs, f"duplicate description: {fname}"
            titles.add(page["title"])
            descs.add(page["desc"])
        html = (
            head(page["title"], page["desc"], page["path"], page["jsonld"])
            + header(page["active"])
            + page["body"]
            + footer()
        )
        (ROOT / fname).write_text(html)
        print(f"wrote {fname} ({len(html)} bytes)")

    # sitemap.xml
    urls = [p["path"] for p in PAGES.values() if p["path"] != "/404"]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        loc = SITE + ("" if u == "/" else u) + ("/" if u == "/" else "")
        sm.append(f"  <url><loc>{SITE + u if u != '/' else SITE + '/'}</loc></url>")
    sm.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sm) + "\n")
    print("wrote sitemap.xml")


if __name__ == "__main__":
    os.chdir(ROOT)
    build()
