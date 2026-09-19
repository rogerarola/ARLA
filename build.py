#!/usr/bin/env python3
"""arlamusic.com static build.

    python3 build.py

Reads data.json and writes index.html, releases/, free-downloads/, one folder
per track, 404.html,
sitemap.xml and llms.txt. Edit data.json, run this, commit the output.
No dependencies beyond the Python standard library.
"""
import json, html, os, datetime, re

ROOT = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(ROOT, "data.json"), encoding="utf-8"))
S = D["site"]
TRACKS = D["tracks"]
TODAY = datetime.date.today().isoformat()
BASE = S["url"]

def e(s):
    return html.escape(str(s), quote=True)

def join_names(names):
    names = list(names)
    if len(names) <= 1:
        return "".join(names)
    return ", ".join(names[:-1]) + " & " + names[-1]

def full_title(t):
    return f'{t["title"]} ({t["version"]})'

def hub_of(t):
    return "free-downloads" if t["free"] else "releases"

HUB_LABEL = {"releases": "Releases", "free-downloads": "Free Downloads"}

def path_of(t):
    return f'/{hub_of(t)}/{t["slug"]}/'

def kind_label(t):
    if t["kind"] == "mashup":
        return "Mashup"
    if t["kind"] == "edit":
        return "Edit"
    return "Official remix" if t["official"] else "Remix"

def kind_phrase(t):
    if t["kind"] == "mashup":
        return "mashup"
    if t["kind"] == "edit":
        return "edit"
    return "official remix" if t["official"] else "remix"

# ---------------------------------------------------------------- fragments
SPRITE = """<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">
  <symbol id="arla" viewBox="0 0 800 144"><g transform="translate(0,144) scale(0.1,-0.1)"><path d="M736 1418 c-20 -34 -716 -1404 -716 -1412 0 -3 96 -6 213 -6 l214 0 76 160 76 160 448 0 448 0 77 -160 76 -160 215 0 215 0 -153 313 c-84 171 -243 495 -353 720 l-200 407 -311 0 -311 0 -14 -22z m492 -536 c89 -187 162 -341 162 -343 0 -2 -156 -3 -346 -1 -202 1 -344 6 -342 12 2 5 75 157 163 339 130 268 164 330 180 330 17 1 48 -58 183 -337z M2270 721 l0 -721 205 0 205 0 0 266 0 266 283 -4 c308 -4 326 -7 378 -64 14 -16 79 -125 145 -243 65 -117 123 -215 129 -217 6 -3 105 -3 221 -2 l211 3 -127 235 c-140 257 -187 321 -264 355 l-50 22 67 13 c76 14 172 57 228 101 23 18 51 56 70 94 30 62 31 68 27 167 -3 88 -7 112 -32 161 -60 124 -199 217 -386 259 -90 20 -126 22 -702 25 l-608 4 0 -720z m1078 429 c108 -12 197 -44 225 -82 11 -15 22 -49 25 -78 12 -124 -75 -193 -278 -220 -41 -5 -202 -10 -357 -10 l-283 0 0 200 0 200 288 0 c158 0 329 -5 380 -10z M4240 720 l0 -720 745 0 745 0 0 145 0 145 -540 0 -540 0 -2 572 -3 573 -202 3 -203 2 0 -720z M6450 1038 c-113 -222 -278 -546 -367 -720 l-161 -318 216 0 217 0 77 160 76 160 447 0 446 0 77 -160 77 -159 213 -1 c116 0 212 3 212 8 0 4 -157 327 -349 717 l-348 710 -314 3 -314 2 -205 -402z m686 -158 l161 -335 -340 -3 c-187 -1 -342 0 -344 2 -3 2 69 155 159 340 139 287 166 336 183 334 15 -2 56 -79 181 -338z"/></g></symbol>
  <symbol id="i-up-right" viewBox="0 0 256 256"><path d="M204,64V168a12,12,0,0,1-24,0V93L72.49,200.49a12,12,0,0,1-17-17L163,76H88a12,12,0,0,1,0-24H192A12,12,0,0,1,204,64Z"/></symbol>
  <symbol id="i-download" viewBox="0 0 256 256"><path d="M228,144v64a12,12,0,0,1-12,12H40a12,12,0,0,1-12-12V144a12,12,0,0,1,24,0v52H204V144a12,12,0,0,1,24,0Zm-108.49,8.49a12,12,0,0,0,17,0l40-40a12,12,0,0,0-17-17L140,115V32a12,12,0,0,0-24,0v83L96.49,95.51a12,12,0,0,0-17,17Z"/></symbol>
  <symbol id="i-spotify" viewBox="0 0 24 24"><path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"/></symbol>
  <symbol id="i-soundcloud" viewBox="0 0 24 24"><path d="M23.999 14.165c-.052 1.796-1.612 3.169-3.4 3.169h-8.18a.68.68 0 0 1-.675-.683V7.862a.747.747 0 0 1 .452-.724s.75-.513 2.333-.513a5.364 5.364 0 0 1 2.763.755 5.433 5.433 0 0 1 2.57 3.54c.282-.08.574-.121.868-.12.884 0 1.73.358 2.347.992s.948 1.49.922 2.373ZM10.721 8.421c.247 2.98.427 5.697 0 8.672a.264.264 0 0 1-.53 0c-.395-2.946-.22-5.718 0-8.672a.264.264 0 0 1 .53 0ZM9.072 9.448c.285 2.659.37 4.986-.006 7.655a.277.277 0 0 1-.55 0c-.331-2.63-.256-5.02 0-7.655a.277.277 0 0 1 .556 0Zm-1.663-.257c.27 2.726.39 5.171 0 7.904a.266.266 0 0 1-.532 0c-.38-2.69-.257-5.21 0-7.904a.266.266 0 0 1 .532 0Zm-1.647.77a26.108 26.108 0 0 1-.008 7.147.272.272 0 0 1-.542 0 27.955 27.955 0 0 1 0-7.147.275.275 0 0 1 .55 0Zm-1.67 1.769c.421 1.865.228 3.5-.029 5.388a.257.257 0 0 1-.514 0c-.21-1.858-.398-3.549 0-5.389a.272.272 0 0 1 .543 0Zm-1.655-.273c.388 1.897.26 3.508-.01 5.412-.026.28-.514.283-.54 0-.244-1.878-.347-3.54-.01-5.412a.283.283 0 0 1 .56 0Zm-1.668.911c.4 1.268.257 2.292-.026 3.572a.257.257 0 0 1-.514 0c-.241-1.262-.354-2.312-.023-3.572a.283.283 0 0 1 .563 0Z"/></symbol>
  <symbol id="i-youtube" viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></symbol>
  <symbol id="i-instagram" viewBox="0 0 24 24"><path d="M7.0301.084c-1.2768.0602-2.1487.264-2.911.5634-.7888.3075-1.4575.72-2.1228 1.3877-.6652.6677-1.075 1.3368-1.3802 2.127-.2954.7638-.4956 1.6365-.552 2.914-.0564 1.2775-.0689 1.6882-.0626 4.947.0062 3.2586.0206 3.6671.0825 4.9473.061 1.2765.264 2.1482.5635 2.9107.308.7889.72 1.4573 1.388 2.1228.6679.6655 1.3365 1.0743 2.1285 1.38.7632.295 1.6361.4961 2.9134.552 1.2773.056 1.6884.069 4.9462.0627 3.2578-.0062 3.668-.0207 4.9478-.0814 1.28-.0607 2.147-.2652 2.9098-.5633.7889-.3086 1.4578-.72 2.1228-1.3881.665-.6682 1.0745-1.3378 1.3795-2.1284.2957-.7632.4966-1.636.552-2.9124.056-1.2809.0692-1.6898.063-4.948-.0063-3.2583-.021-3.6668-.0817-4.9465-.0607-1.2797-.264-2.1487-.5633-2.9117-.3084-.7889-.72-1.4568-1.3876-2.1228C21.2982 1.33 20.628.9208 19.8378.6165 19.074.321 18.2017.1197 16.9244.0645 15.6471.0093 15.236-.005 11.977.0014 8.718.0076 8.31.0215 7.0301.0839m.1402 21.6932c-1.17-.0509-1.8053-.2453-2.2287-.408-.5606-.216-.96-.4771-1.3819-.895-.422-.4178-.6811-.8186-.9-1.378-.1644-.4234-.3624-1.058-.4171-2.228-.0595-1.2645-.072-1.6442-.079-4.848-.007-3.2037.0053-3.583.0607-4.848.05-1.169.2456-1.805.408-2.2282.216-.5613.4762-.96.895-1.3816.4188-.4217.8184-.6814 1.3783-.9003.423-.1651 1.0575-.3614 2.227-.4171 1.2655-.06 1.6447-.072 4.848-.079 3.2033-.007 3.5835.005 4.8495.0608 1.169.0508 1.8053.2445 2.228.408.5608.216.96.4754 1.3816.895.4217.4194.6816.8176.9005 1.3787.1653.4217.3617 1.056.4169 2.2263.0602 1.2655.0739 1.645.0796 4.848.0058 3.203-.0055 3.5834-.061 4.848-.051 1.17-.245 1.8055-.408 2.2294-.216.5604-.4763.96-.8954 1.3814-.419.4215-.8181.6811-1.3783.9-.4224.1649-1.0577.3617-2.2262.4174-1.2656.0595-1.6448.072-4.8493.079-3.2045.007-3.5825-.006-4.848-.0608M16.953 5.5864A1.44 1.44 0 1 0 18.39 4.144a1.44 1.44 0 0 0-1.437 1.4424M5.8385 12.012c.0067 3.4032 2.7706 6.1557 6.173 6.1493 3.4026-.0065 6.157-2.7701 6.1506-6.1733-.0065-3.4032-2.771-6.1565-6.174-6.1498-3.403.0067-6.156 2.771-6.1496 6.1738M8 12.0077a4 4 0 1 1 4.008 3.9921A3.9996 3.9996 0 0 1 8 12.0077"/></symbol>
  <symbol id="i-beatport" viewBox="0 0 24 24"><path d="M21.429 17.055a7.114 7.114 0 0 1-.794 3.246 6.917 6.917 0 0 1-2.181 2.492 6.698 6.698 0 0 1-3.063 1.163 6.653 6.653 0 0 1-3.239-.434 6.796 6.796 0 0 1-2.668-1.932 7.03 7.03 0 0 1-1.481-2.983 7.124 7.124 0 0 1 .049-3.345 7.015 7.015 0 0 1 1.566-2.937l-4.626 4.73-2.421-2.479 5.201-5.265a3.791 3.791 0 0 0 1.066-2.675V0h3.41v6.613a7.172 7.172 0 0 1-.519 2.794 7.02 7.02 0 0 1-1.559 2.353l-.153.156a6.768 6.768 0 0 1 3.49-1.725 6.687 6.687 0 0 1 3.845.5 6.873 6.873 0 0 1 2.959 2.564 7.118 7.118 0 0 1 1.118 3.8Zm-3.089 0a3.89 3.89 0 0 0-.611-2.133 3.752 3.752 0 0 0-1.666-1.424 3.65 3.65 0 0 0-2.158-.233 3.704 3.704 0 0 0-1.92 1.037 3.852 3.852 0 0 0-1.031 1.955 3.908 3.908 0 0 0 .205 2.213c.282.7.76 1.299 1.374 1.721a3.672 3.672 0 0 0 2.076.647 3.637 3.637 0 0 0 2.635-1.096c.347-.351.622-.77.81-1.231.188-.461.285-.956.286-1.456Z"/></symbol>
</svg>"""

ICONS = """<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/assets/icon-96.png" type="image/png" sizes="96x96">
<link rel="icon" href="/assets/icon-192.png" type="image/png" sizes="192x192">
<link rel="icon" href="/assets/icon-512.png" type="image/png" sizes="512x512">
<link rel="icon" href="/assets/icon-96-light.png" type="image/png" sizes="96x96" media="(prefers-color-scheme: dark)">
<link rel="icon" href="/assets/icon-192-light.png" type="image/png" sizes="192x192" media="(prefers-color-scheme: dark)">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">"""

def socials(cls="soc caps"):
    return f"""<a class="{cls}" href="{S['spotify']}" target="_blank" rel="noopener"><svg class="ic" aria-hidden="true"><use href="#i-spotify"/></svg>Spotify</a>
      <a class="{cls}" href="{S['soundcloud']}" target="_blank" rel="noopener"><svg class="ic" aria-hidden="true"><use href="#i-soundcloud"/></svg>SoundCloud</a>
      <a class="{cls}" href="{S['youtube']}" target="_blank" rel="noopener"><svg class="ic" aria-hidden="true"><use href="#i-youtube"/></svg>YouTube</a>
      <a class="{cls}" href="{S['instagram']}" target="_blank" rel="noopener"><svg class="ic" aria-hidden="true"><use href="#i-instagram"/></svg>Instagram</a>"""

NAV_ITEMS = [("/releases/", "Releases"), ("/free-downloads/", "Free Downloads"), ("/#contact", "Contact")]

def nav(current):
    def li(href, label):
        cur = ' aria-current="page"' if href == current else ""
        return f'<li><a href="{href}"{cur}>{label}</a></li>'
    links = "\n      ".join(li(h, l) for h, l in NAV_ITEMS)
    return f"""<a class="skip" href="#main">Skip to content</a>

<header class="nav">
  <a class="nav-mark" href="/" aria-label="ARLA home">
    <svg viewBox="0 0 800 144" aria-hidden="true"><use href="#arla"/></svg>
  </a>
  <nav aria-label="Primary">
    <ul class="nav-links caps">
      {links}
    </ul>
  </nav>
  <div class="nav-end">
    <a class="nav-cta caps" href="{S['spotify']}" target="_blank" rel="noopener">
      Listen <svg class="ic" aria-hidden="true"><use href="#i-up-right"/></svg>
    </a>
    <button class="nav-toggle" id="menu-btn" aria-label="Open menu" aria-expanded="false" aria-controls="menu"><span></span></button>
  </div>
</header>

<nav class="menu" id="menu" aria-label="Mobile" hidden>
  <ul>
    {links}
  </ul>
  <div class="menu-foot">
      {socials()}
  </div>
</nav>"""

def footer():
    return f"""<footer class="foot">
  <div class="foot-row caps">
    <span>&copy; <span id="yr">{datetime.date.today().year}</span> ARLA</span>
    <ul>
      <li><a href="/releases/">Releases</a></li>
      <li><a href="/free-downloads/">Free Downloads</a></li>
      <li><a href="mailto:{S['email']}">Contact</a></li>
    </ul>
  </div>
</footer>
<script src="/assets/site.js" defer></script>"""

def cover_picture(t, lazy=True, sizes="(max-width:860px) 68vw, 32vw", vt=True):
    """Artwork tile for a track: the real cover, or a typographic one."""
    vt_style = f' style="view-transition-name:cover-{t["slug"]}"' if vt else ""
    if t["cover"]:
        lz = ' loading="lazy"' if lazy else ' fetchpriority="high"'
        return f"""<span class="art tilt"{vt_style}>
            <picture>
              <source type="image/webp" srcset="/assets/{t['cover']}.webp">
              <img src="/assets/{t['cover']}.jpg" width="500" height="500"{lz} decoding="async" alt="Cover art for {e(full_title(t))}">
            </picture>
          </span>"""
    return f"""<span class="tcover tilt"{vt_style} role="img" aria-label="{e(full_title(t))}">
            <svg viewBox="0 0 800 144" aria-hidden="true"><use href="#arla"/></svg>
            <span aria-hidden="true">{e(t['title'])}<small>{e(t['version'])}</small></span>
            <i class="glow"></i>
          </span>"""

def rel_card(t, heading="h3", extra_cls=""):
    return f"""<a class="rel {extra_cls}" href="{path_of(t)}">
          {cover_picture(t)}
          <{heading} class="rel-name">{e(t['title'])}</{heading}>
          <span class="rel-mix">{e(t['version'])}</span>
          <span class="rel-by">{e(join_names(t['original_by']))}</span>
        </a>"""

def head(title, desc, path, og_image, og_type="website", extra="", robots="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"):
    url = BASE + path
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{f'<link rel="canonical" href="{url}">' if robots.startswith("index") else ""}
<meta name="robots" content="{robots}">
<meta name="author" content="ARLA">
<meta name="theme-color" content="#05070c">
<meta name="color-scheme" content="dark">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="ARLA Music">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}{og_image[0]}">
<meta property="og:image:width" content="{og_image[1]}">
<meta property="og:image:height" content="{og_image[2]}">
<meta property="og:image:alt" content="{e(og_image[3])}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{BASE}{og_image[0]}">
<meta name="twitter:image:alt" content="{e(og_image[3])}">
{ICONS}
<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/mendamedium.woff2" crossorigin>
{extra}
<link rel="stylesheet" href="/assets/site.css">
<script>document.documentElement.classList.add('js')</script>
"""

def ld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=1) + "\n</script>"

ARTIST_ID = BASE + "/#arla"

def artist_node():
    return {
        "@type": ["MusicGroup", "Person"],
        "@id": ARTIST_ID,
        "name": "ARLA",
        "alternateName": ["ARLA Music", "Roger Arola"],
        "url": BASE + "/",
        "image": BASE + "/assets/og-image.jpg",
        "logo": BASE + "/assets/logo.png",
        "description": S["description"],
        "genre": ["Melodic Techno", "Electronic", "House"],
        "jobTitle": "DJ and Music Producer",
        "email": S["email"],
        "foundingLocation": {"@type": "Place", "name": "Barcelona, Spain"},
        "address": {"@type": "PostalAddress", "addressLocality": "Barcelona", "addressCountry": "ES"},
        "sameAs": [S["spotify"], S["soundcloud"], S["youtube"], S["instagram"]],
        "contactPoint": {"@type": "ContactPoint", "contactType": "booking", "email": S["email"], "availableLanguage": ["en", "es", "ca"]},
        "track": [{"@id": BASE + path_of(t) + "#recording"} for t in TRACKS],
    }

def recording_node(t, full=True):
    node = {
        "@type": "MusicRecording",
        "@id": BASE + path_of(t) + "#recording",
        "name": full_title(t),
        "url": BASE + path_of(t),
        "byArtist": [{"@type": "MusicGroup", "name": n} for n in t["original_by"]] + [{"@id": ARTIST_ID}] + [{"@type": "MusicGroup", "name": n} for n in t["with"]],
        "genre": "Melodic Techno",
        "inLanguage": "en",
    }
    if t["cover"]:
        node["image"] = BASE + f'/assets/{t["cover"]}.jpg'
    if t.get("album"):
        node["inAlbum"] = {"@type": "MusicAlbum", "name": t["album"], "byArtist": {"@id": ARTIST_ID}}
    if t.get("date"):
        node["datePublished"] = t["date"]
    same = [u for u in (t.get("spotify"), t.get("beatport")) if u]
    if same:
        node["sameAs"] = same
    if t["free"]:
        node["isAccessibleForFree"] = True
        node["offers"] = {"@type": "Offer", "price": "0", "priceCurrency": "EUR", "url": t["url"], "availability": "https://schema.org/InStock"}
    else:
        node["offers"] = {"@type": "Offer", "url": t.get("beatport") or t["url"]}
    return node

def breadcrumb(items):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + p} for i, (n, p) in enumerate(items)],
    }

# ---------------------------------------------------------------- home
def build_home():
    official = [t for t in TRACKS if t["official"]]
    free = [t for t in TRACKS if t["free"]]
    latest = official[0]
    title = "ARLA | Melodic Techno DJ and Producer from Barcelona"
    desc = S["description"]
    og = ("/assets/og-image.jpg", 1200, 630, "ARLA, photographed in deep blue light, with the ARLA wordmark")
    extra = """<link rel="preload" as="image" href="/assets/hero-wide-1600.webp" type="image/webp" fetchpriority="high" media="(min-width:861px)">
<link rel="preload" as="image" href="/assets/hero-tall.webp" type="image/webp" fetchpriority="high" media="(max-width:860px)">"""

    words = ["Supported", "by", "GORDO,", "SCRIPT", "and", "braev", "on", "the", "stages", "of", "Tomorrowland,", "Lollapalooza,", "Afterlife", "and", "UNVRS."]
    keys = {"GORDO,", "SCRIPT", "braev", "Tomorrowland,", "Lollapalooza,", "Afterlife", "UNVRS."}
    lede = " ".join(f'<span class="w{" k" if w in keys else ""}"><span style="--i:{i}">{w}</span></span>' for i, w in enumerate(words))

    pan_items = "\n        ".join(f'<li class="rv">{rel_card(t)}</li>' for t in official)
    dl_items = "\n        ".join(f'<li class="rv">{rel_card(t)}</li>' for t in free)

    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebSite", "@id": BASE + "/#website", "url": BASE + "/", "name": "ARLA Music", "alternateName": "ARLA",
             "description": "Official site of ARLA, melodic techno DJ and producer from Barcelona, Spain.", "inLanguage": "en", "publisher": {"@id": ARTIST_ID}},
            {"@type": "WebPage", "@id": BASE + "/#webpage", "url": BASE + "/", "name": title, "isPartOf": {"@id": BASE + "/#website"},
             "about": {"@id": ARTIST_ID}, "primaryImageOfPage": {"@id": BASE + "/#heroimage"}, "inLanguage": "en"},
            {"@type": "ImageObject", "@id": BASE + "/#heroimage", "url": BASE + "/assets/hero-wide-3200.jpg", "contentUrl": BASE + "/assets/hero-wide-3200.jpg",
             "width": 3200, "height": 1800, "caption": "ARLA photographed in deep blue light"},
            artist_node(),
        ] + [recording_node(t) for t in TRACKS],
    }

    return head(title, desc, "/", og, "profile", extra) + ld(graph) + f"""
</head>
<body>
{SPRITE}
{nav("/")}

<main id="main">

<section class="hero" aria-label="Introduction">
  <div class="hero-media">
    <picture>
      <source media="(max-width:860px)" type="image/webp" srcset="/assets/hero-tall.webp">
      <source media="(max-width:860px)" srcset="/assets/hero-tall.jpg">
      <source type="image/webp" srcset="/assets/hero-wide-1600.webp 1600w, /assets/hero-wide-3200.webp 3200w" sizes="100vw">
      <img src="/assets/hero-wide-1600.jpg" srcset="/assets/hero-wide-1600.jpg 1600w, /assets/hero-wide-3200.jpg 3200w" sizes="100vw"
           width="1600" height="900" fetchpriority="high" decoding="async"
           alt="ARLA, wearing a cap with his head lowered, photographed in deep blue light">
    </picture>
  </div>
  <div class="hero-inner">
    <h1 class="hero-title">
      <span class="sr-only">ARLA, melodic techno DJ and producer from Barcelona, Spain</span>
      <svg viewBox="0 0 800 144" aria-hidden="true"><use href="#arla"/></svg>
    </h1>
  </div>
  <div class="hero-foot">
    <p class="hero-sub"><b>Melodic techno</b> DJ and producer from Barcelona.</p>
    <div class="hero-cta">
      <a class="btn caps" href="{path_of(latest)}">Latest release <svg class="ic" aria-hidden="true"><use href="#i-up-right"/></svg></a>
    </div>
  </div>
</section>

<div class="over">

<section class="section about" id="about" aria-labelledby="about-h">
  <div class="wrap">
    <h2 class="sr-only" id="about-h">About ARLA</h2>
    <p class="about-lede" data-split>{lede}</p>
    <p class="about-stat rv"><span class="stat-num">{S['plays']}</span><span class="stat-label">plays worldwide</span></p>
  </div>
</section>

<section class="pan" id="releases" aria-labelledby="rel-h">
  <div class="pan-stick">
    <div class="pan-head">
      <div class="sec-head" style="margin:0">
        <h2 class="sec-title" id="rel-h">Official Releases</h2>
        <a class="sec-link caps" href="/releases/">All releases <svg class="ic" aria-hidden="true"><use href="#i-up-right"/></svg></a>
      </div>
    </div>
    <ul class="pan-track">
        {pan_items}
    </ul>
  </div>
</section>

<section class="pan" id="downloads" aria-labelledby="dl-h">
  <div class="pan-stick">
    <div class="pan-head">
      <div class="sec-head" style="margin:0">
        <h2 class="sec-title" id="dl-h">Free Downloads</h2>
        <a class="sec-link caps" href="/free-downloads/">All free downloads <svg class="ic" aria-hidden="true"><use href="#i-up-right"/></svg></a>
      </div>
    </div>
    <ul class="pan-track">
        {dl_items}
    </ul>
  </div>
</section>

<section class="section" id="contact" aria-labelledby="contact-h">
  <div class="wrap">
    <div class="contact-head rv">
      <h2 class="sec-title" id="contact-h">Get in touch</h2>
      <p class="contact-note">Bookings, collaborations, remix requests and demos.</p>
    </div>
    <a class="mail rv" href="mailto:{S['email']}"><span>{S['email']}</span> <svg class="ic" aria-hidden="true"><use href="#i-up-right"/></svg></a>
    <div class="socials rv">
      {socials()}
    </div>
  </div>
</section>

</div>
</main>

{footer()}
</body>
</html>
"""

# ---------------------------------------------------------------- track page
def track_copy(t):
    by = join_names(t["original_by"])
    if t["kind"] == "mashup":
        p1 = f"<b>{e(full_title(t))}</b> is a mashup by ARLA built from tracks by {e(by)}."
    else:
        p1 = f"<b>{e(full_title(t))}</b> is ARLA's {kind_phrase(t)} of {e(t['title'])} by {e(by)}"
        p1 += f", made together with {e(join_names(t['with']))}." if t["with"] else "."
    if t["free"]:
        p2 = "It is a free download on Hypeddit."
    else:
        p2 = f"Released on <b>{e(t['label'])}</b> in {t['date'][:4]}. " if t.get("label") and t.get("date") else ""
        p2 += "Out now on all streaming platforms" + (" and on Beatport." if t.get("beatport") else ".")
    return f"{p1} {p2}"

def build_track(t):
    hub = hub_of(t)
    hub_label = HUB_LABEL[hub]
    ft = full_title(t)
    by = join_names(t["original_by"])
    title = f"{ft} | {by}" if len(f"{ft} | {by}") <= 70 else ft
    if t["free"]:
        desc = f"{ft}: free download of ARLA's {kind_phrase(t)} of {t['title']} by {by}. Melodic techno by ARLA, DJ and producer from Barcelona." if t["kind"] != "mashup" else f"{ft}: free download of ARLA's mashup of {by}. Melodic techno by ARLA, DJ and producer from Barcelona."
    else:
        desc = f"{ft}: ARLA's official remix of {t['title']} by {by}" + (f", out on {t['label']}" if t.get("label") else "") + ". Listen on all platforms or buy on Beatport."
    og = (f'/assets/{t["cover"]}.jpg', t.get("cover_px", 500), t.get("cover_px", 500), f"Cover art for {ft}") if t["cover"] else ("/assets/og-image.jpg", 1200, 630, "ARLA, photographed in deep blue light, with the ARLA wordmark")
    extra = f'<link rel="preload" as="image" href="/assets/{t["cover"]}.webp" type="image/webp" fetchpriority="high">' if t["cover"] else ""

    others = [o for o in TRACKS if o is not t]
    same = [o for o in others if hub_of(o) == hub]
    more = (same + [o for o in others if o not in same])[:3]
    more_items = "\n      ".join(f'<li class="rv">{rel_card(o)}</li>' for o in more)

    if t["free"]:
        cta = f'<a class="btn btn-blue caps" href="{t["url"]}" target="_blank" rel="noopener">Free download <svg class="ic" aria-hidden="true"><use href="#i-download"/></svg></a>'
    else:
        cta = f'<a class="btn btn-solid caps" href="{t["url"]}" target="_blank" rel="noopener">Listen <svg class="ic" aria-hidden="true"><use href="#i-up-right"/></svg></a>'
        if t.get("beatport"):
            cta += f'\n        <a class="btn caps" href="{t["beatport"]}" target="_blank" rel="noopener"><svg class="ic" aria-hidden="true"><use href="#i-beatport"/></svg> Buy</a>'

    glow = f'<img class="track-glow" src="/assets/{t["cover"]}.webp" width="500" height="500" alt="" decoding="async">' if t["cover"] else ""

    graph = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": BASE + path_of(t) + "#webpage", "url": BASE + path_of(t), "name": title, "description": desc,
         "isPartOf": {"@id": BASE + "/#website"}, "about": {"@id": BASE + path_of(t) + "#recording"}, "inLanguage": "en",
         "breadcrumb": {"@id": BASE + path_of(t) + "#crumb"}},
        dict(breadcrumb([("ARLA", "/"), (hub_label, f"/{hub}/"), (ft, path_of(t))]), **{"@id": BASE + path_of(t) + "#crumb"}),
        recording_node(t),
        {"@type": ["MusicGroup", "Person"], "@id": ARTIST_ID, "name": "ARLA", "alternateName": ["ARLA Music", "Roger Arola"], "url": BASE + "/",
         "sameAs": [S["spotify"], S["soundcloud"], S["youtube"], S["instagram"]]},
    ]}

    return head(title, desc, path_of(t), og, "music.song", extra) + ld(graph) + f"""
</head>
<body>
{SPRITE}
{nav(f"/{hub}/")}

<main id="main">

<section class="track-hero" aria-labelledby="t-h">
  <div class="track-grid">
    <div class="track-art">
      {glow}
      {cover_picture(t, lazy=False, sizes="(max-width:1080px) 90vw, 40vw")}
    </div>
    <div class="track-copy">
      <ol class="crumb caps">
        <li><a href="/">ARLA</a></li>
        <li><a href="/{hub}/">{hub_label}</a></li>
      </ol>
      <h1 class="track-title" id="t-h">{e(t['title'])}<span class="track-version">{e(t['version'])}</span></h1>
      <p class="track-by">{'Built from tracks by' if t['kind']=='mashup' else 'Original by'} <b>{e(by)}</b>{'. With <b>' + e(join_names(t['with'])) + '</b>' if t['with'] else ''}</p>
      <div class="track-cta">
        {cta}
      </div>
      <p class="track-body">{track_copy(t)}</p>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="more-h">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="sec-title" id="more-h">More from ARLA</h2>
      <a class="sec-link caps" href="/{hub}/">All {hub_label.lower()} <svg class="ic" aria-hidden="true"><use href="#i-up-right"/></svg></a>
    </div>
    <ul class="more-grid">
      {more_items}
    </ul>
  </div>
</section>

<section class="section" id="contact" aria-labelledby="contact-h" style="padding-top:0">
  <div class="wrap">
    <div class="contact-head rv">
      <h2 class="sec-title" id="contact-h">Get in touch</h2>
      <p class="contact-note">Bookings, collaborations, remix requests and demos.</p>
    </div>
    <a class="mail rv" href="mailto:{S['email']}"><span>{S['email']}</span> <svg class="ic" aria-hidden="true"><use href="#i-up-right"/></svg></a>
  </div>
</section>

</main>

{footer()}
</body>
</html>
"""

# ---------------------------------------------------------------- hub pages
def build_hub(hub):
    if hub == "releases":
        items = [t for t in TRACKS if not t["free"]]
        title = "ARLA Releases | Official Singles and Remixes"
        h1 = "Releases"
        lede = "Official ARLA releases: singles and remixes, out on all streaming platforms and on Beatport."
        desc = "ARLA releases: official melodic techno remixes and singles by ARLA, with remixes of DALEXO, LAVINIA, Brian Cross and Marsal Ventura. Free ARLA remixes and mashups too."
        other = ("/free-downloads/", "free downloads")
    else:
        items = [t for t in TRACKS if t["free"]]
        title = "ARLA Free Downloads | Free Remixes, Edits and Mashups"
        h1 = "Free Downloads"
        lede = "Free ARLA remixes, edits and mashups. Download them on Hypeddit."
        desc = "Free ARLA downloads: melodic techno remixes of John Summit and Anyma, an edit of Gordo's Olvidarte and ARLA mashups. Free on Hypeddit. ARLA releases and remixes."
        other = ("/releases/", "official releases")
    path = f"/{hub}/"
    cards = "\n      ".join(f'<li class="rv">{rel_card(t)}</li>' for t in items)
    graph = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": BASE + path + "#webpage", "url": BASE + path, "name": title, "description": desc,
         "isPartOf": {"@id": BASE + "/#website"}, "inLanguage": "en", "breadcrumb": {"@id": BASE + path + "#crumb"},
         "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": BASE + path_of(t), "name": full_title(t)} for i, t in enumerate(items)]}},
        dict(breadcrumb([("ARLA", "/"), (h1, path)]), **{"@id": BASE + path + "#crumb"}),
        {"@type": ["MusicGroup", "Person"], "@id": ARTIST_ID, "name": "ARLA", "alternateName": ["ARLA Music", "Roger Arola"], "url": BASE + "/",
         "sameAs": [S["spotify"], S["soundcloud"], S["youtube"], S["instagram"]]},
    ]}
    og = ("/assets/og-image.jpg", 1200, 630, "ARLA, photographed in deep blue light, with the ARLA wordmark")
    return head(title, desc, path, og) + ld(graph) + f"""
</head>
<body>
{SPRITE}
{nav(path)}

<main id="main">

<section class="hub-hero" aria-labelledby="hub-h">
  <div class="wrap">
    <ol class="crumb caps" style="margin:0">
      <li><a href="/">ARLA</a></li>
      <li aria-current="page">{h1}</li>
    </ol>
    <h1 class="hub-title" id="hub-h">{h1}</h1>
    <p class="lede">{lede}</p>
  </div>
</section>

<section class="section" style="padding-top:clamp(24px,4vh,48px)" aria-label="{h1}">
  <div class="wrap">
    <ul class="hub-grid">
      {cards}
    </ul>
    <div class="hub-note">
      <p class="lede">Looking for something else? See the <a href="{other[0]}">{other[1]}</a>, or write for bookings, remix requests and demos.</p>
      <a class="btn btn-solid caps" href="mailto:{S['email']}">Contact <svg class="ic" aria-hidden="true"><use href="#i-up-right"/></svg></a>
    </div>
  </div>
</section>

</main>

{footer()}
</body>
</html>
"""

# ---------------------------------------------------------------- 404
def build_404():
    og = ("/assets/og-image.jpg", 1200, 630, "ARLA, photographed in deep blue light, with the ARLA wordmark")
    return head("Page not found | ARLA", "This page does not exist on arlamusic.com.", "/404.html", og, robots="noindex, follow") + f"""
</head>
<body>
{SPRITE}
{nav("")}

<main id="main">
<section class="nf" aria-labelledby="nf-h">
  <div class="wrap">
    <p class="nf-code" aria-hidden="true">404</p>
    <h1 class="nf-title" id="nf-h">This page does not exist.</h1>
    <p class="lede">The link may be old or mistyped. The music is still here.</p>
    <div class="track-cta">
      <a class="btn btn-solid caps" href="/releases/">Releases <svg class="ic" aria-hidden="true"><use href="#i-up-right"/></svg></a>
      <a class="btn caps" href="/free-downloads/">Free downloads <svg class="ic" aria-hidden="true"><use href="#i-download"/></svg></a>
    </div>
  </div>
</section>
</main>

{footer()}
</body>
</html>
"""

# ---------------------------------------------------------------- sitemap / llms
def build_sitemap():
    def url(loc, prio, images=()):
        imgs = "".join(f"\n    <image:image><image:loc>{BASE}{i[0]}</image:loc><image:title>{e(i[1])}</image:title></image:image>" for i in images)
        return f"  <url>\n    <loc>{BASE}{loc}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <priority>{prio}</priority>{imgs}\n  </url>"
    covers = [(f'/assets/{t["cover"]}.jpg', full_title(t)) for t in TRACKS if t["cover"]]
    out = [url("/", "1.0", [("/assets/hero-wide-3200.jpg", "ARLA")] + covers), url("/releases/", "0.9"), url("/free-downloads/", "0.9")]
    for t in TRACKS:
        out.append(url(path_of(t), "0.8" if t["official"] else "0.7", [(f'/assets/{t["cover"]}.jpg', full_title(t))] if t["cover"] else []))
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n' + "\n".join(out) + "\n</urlset>\n"

def build_llms():
    lines = ["# ARLA", "", f"> {S['description']}", "",
             "- **Artist name:** ARLA (also written ARLA Music; real name Roger Arola)", "- **Role:** DJ and music producer", "- **Based in:** Barcelona, Spain",
             "- **Genre:** Melodic techno", f"- **Total streams:** {S['plays']}", f"- **Supported by:** {', '.join(S['supporters'])}",
             f"- **Supported at:** {', '.join(S['stages'])}", f"- **Bookings, remixes and demos:** {S['email']}", f"- **Website:** {BASE}/",
             f"- **Official releases:** {BASE}/releases/", f"- **Free downloads (remixes, edits, mashups):** {BASE}/free-downloads/", "", "## Official releases", ""]
    for t in TRACKS:
        if t["official"]:
            rel = f", {t['label']}, {t['date'][:4]}" if t.get("label") else ""
            buy = f" Buy: {t['beatport']}" if t.get("beatport") else ""
            lines.append(f"- **{full_title(t)}**, original by {join_names(t['original_by'])}{rel}. Page: {BASE}{path_of(t)} Listen: {t['url']}{buy}")
    lines += ["", "## Free downloads", ""]
    for t in TRACKS:
        if t["free"]:
            lines.append(f"- **{full_title(t)}**, {join_names(t['original_by'])}. Page: {BASE}{path_of(t)} Download: {t['url']}")
    lines += ["", "## Listen", "", f"- Spotify: {S['spotify']}", f"- SoundCloud: {S['soundcloud']}", f"- YouTube: {S['youtube']}", f"- Instagram: {S['instagram']}", "", "## Notes", "",
              "ARLA is a music artist. Not to be confused with Arla Foods, the Danish-Swedish dairy cooperative, or with any similarly named clothing brand.", ""]
    return "\n".join(lines)

# ---------------------------------------------------------------- write
def write(rel, content):
    p = os.path.join(ROOT, rel.lstrip("/"))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", rel)

if __name__ == "__main__":
    write("index.html", build_home())
    import shutil
    for old in ("remixes", "mashups"):  # retired sections, not rebuilt
        shutil.rmtree(os.path.join(ROOT, old), ignore_errors=True)
    write("releases/index.html", build_hub("releases"))
    write("free-downloads/index.html", build_hub("free-downloads"))
    for t in TRACKS:
        write(path_of(t) + "index.html", build_track(t))
    write("404.html", build_404())
    write("sitemap.xml", build_sitemap())
    write("llms.txt", build_llms())
