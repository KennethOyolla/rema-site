#!/usr/bin/env python3
"""Assembles the static site: pages/*.html + shared head, header, form and footer -> dist/.
Each page starts with a comment block of settings:  <!-- title: ... | desc: ... | nav: home -->"""
import re, shutil, pathlib

ROOT = pathlib.Path(__file__).parent
PAGES, DIST = ROOT / "pages", ROOT / "dist"
SITE = "https://remasolutions.co.ke"
APP = "https://rema.blue-flame.co.ke"

NAV = [("how-it-works", "How it works"), ("dashboards", "Dashboards"), ("who-its-for", "Who it's for"), ("pricing", "Pricing & trial")]

def head(title, desc, slug):
    url = SITE + ("/" if slug == "index" else f"/{slug}")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/og.png">
<meta name="theme-color" content="#3570B3">
<link rel="icon" href="/assets/favicon.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,500..800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>"""

def header(active):
    links = "".join(
        f'<a href="/{s}"{" aria-current=\"page\"" if s == active else ""}>{t}</a>' for s, t in NAV)
    return f"""
<header class="top"><div class="wrap">
  <a class="brand" href="/" aria-label="ReMA home"><img src="/assets/rema-logo.png" alt="ReMA" width="75" height="26"></a>
  <button class="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button>
  <nav class="nav" id="nav">{links}<a href="{APP}">Sign in</a><a class="btn btn-primary" href="/#demo">Request a demo</a></nav>
</div></header>
<main>"""

FORM = """
<form class="form-card lead" id="demo-form" action="https://crm.zoho.com/crm/WebToLeadForm" method="POST" accept-charset="UTF-8">
  <h3>Request a demo or a trial</h3>
  <p class="small">We reply within one working day. A trial runs for a month with your own stores, people and products.</p>
  <!-- Zoho CRM web-to-lead: "ReMA website - demo request" form, Leads module -->
  <input type="hidden" name="xnQsjsdp" value="9aad8c7cb23f4581bc1624213b738ac5ae00454a7760c5b3bfab7f8f3a858a4f">
  <input type="hidden" name="zc_gad" id="zc_gad" value="">
  <input type="hidden" name="xmIwtLD" value="d7d06d270f5b81d1eb01a5636e758c38903132f8d242ba5df0a6c97153a1d6e153c3f10ae821fdfba1cab472ff9bb1ad">
  <input type="hidden" name="actionType" value="TGVhZHM=">
  <input type="hidden" name="returnURL" value="https://remasolutions.co.ke/thanks">
  <input type="hidden" name="Lead Source" value="Website">
  <input type="hidden" name="LEADCF17" value="ReMA">
  <input type="hidden" name="Description" value="">
  <div style="position:absolute;left:-9999px" aria-hidden="true"><input type="text" name="aG9uZXlwb3Q" tabindex="-1" autocomplete="off" value=""></div>
  <div class="fields">
    <label>Your name<input name="Last Name" maxlength="80" autocomplete="name" required></label>
    <label>Company<input name="Company" maxlength="200" autocomplete="organization" required></label>
    <label>Phone or WhatsApp<input name="Mobile" type="tel" maxlength="30" autocomplete="tel" required></label>
    <label>Work e-mail<input name="Email" type="email" maxlength="100" autocomplete="email"></label>
    <label>Country<select name="Country"><option>Kenya</option><option>Uganda</option><option>Tanzania</option><option>Rwanda</option><option>Other</option></select></label>
    <label>You are a<select name="LEADCF27"><option>Merchandising agency</option><option value="Manufacturer/brand owner">Manufacturer / brand owner</option><option>Distributor</option><option>Field sales team</option><option>Other</option></select></label>
    <div class="full"><span class="small" style="font-weight:600;color:var(--ink-2)">People in the field</span>
      <div class="radio-row" style="margin-top:6px">
        <label><input type="radio" name="LEADCF28" value="1-10">1–10</label>
        <label><input type="radio" name="LEADCF28" value="11-30" checked>11–30</label>
        <label><input type="radio" name="LEADCF28" value="31+">31+</label>
      </div></div>
    <label class="full">Anything we should know (optional)<textarea data-desc="Notes" maxlength="1500" placeholder="Chains you cover, how you report today, when you'd like to start"></textarea></label>
  </div>
  <button class="btn btn-primary" type="submit">Request a demo</button>
  <p class="form-note">Prefer to talk? Call 0709 100 140 or WhatsApp 0202 040 040.</p>
</form>"""

FOOTER = f"""
</main>
<footer class="foot"><div class="wrap">
  <div>
    <span class="logo-chip"><img src="/assets/rema-logo.png" alt="ReMA" width="64" height="22"></span>
    <p>The field app for sales and merchandising teams: store visits, availability, price, share of shelf, orders and a weekly review deck every Sunday at 8pm.</p>
  </div>
  <div><h3>Product</h3><ul>{''.join(f'<li><a href="/{s}">{t}</a></li>' for s, t in NAV)}<li><a href="{APP}">Sign in</a></li></ul></div>
  <div><h3>Talk to us</h3><ul>
    <li><a href="tel:+254709100140">0709 100 140</a></li>
    <li><a href="https://wa.me/254202040040">WhatsApp 0202 040 040</a></li>
    <li><a href="mailto:office@blue-flame.co.ke">office@blue-flame.co.ke</a></li>
    <li>Ngong Road, Nairobi</li></ul></div>
  <p class="legal">ReMA is a product of <a href="https://www.blue-flame.co.ke">Blueflame Technologies Ltd</a>, Nairobi. © 2026</p>
</div></footer>
<a class="wa" href="https://wa.me/254202040040?text=Hi%2C%20I%27d%20like%20to%20know%20more%20about%20ReMA">WhatsApp us</a>
<script src="/assets/site.js" defer></script>
<script>window.$zoho=window.$zoho || {{}};$zoho.salesiq=$zoho.salesiq||{{ready:function(){{}}}}</script><script id="zsiqscript" src="https://salesiq.zohopublic.com/widget?wc=siqc124da246565cf55ff7fab47605d84ef" defer></script>
</body>
</html>
"""

def build():
    if DIST.exists(): shutil.rmtree(DIST)
    shutil.copytree(ROOT / "assets", DIST / "assets")
    for f in (ROOT / "static").iterdir(): shutil.copy(f, DIST / f.name)
    for p in sorted(PAGES.glob("*.html")):
        src = p.read_text()
        m = re.match(r"\s*<!--(.*?)-->", src, re.S)
        meta = dict(kv.split(":", 1) for kv in (x.strip() for x in m.group(1).split("|")) if ":" in kv)
        meta = {k.strip(): v.strip() for k, v in meta.items()}
        body = src[m.end():].replace("{{FORM}}", FORM).replace("{{APP}}", APP)
        out = head(meta["title"], meta["desc"], p.stem) + header(meta.get("nav", "")) + body + FOOTER
        (DIST / p.name).write_text(out)
    print("built", [p.name for p in DIST.glob("*.html")])

if __name__ == "__main__":
    build()
