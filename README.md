# arlamusic.com — rebuilt

## Deploying

Upload the **contents** of this folder to your web root, keeping the structure:

```
index.html
robots.txt
sitemap.xml
site.webmanifest
llms.txt
favicon.ico
assets/
  fonts/  mendamedium.woff2      (500 — display + body)
          mendasemibold.woff2    (600 — labels, nav, small caps)
          mendabold.woff2        (700 — declared but unused; see below)
  hero.webp / hero.jpg / hero-800.webp / hero-800.jpg / hero-lqip.jpg
  cover-*.webp / cover-*.jpg   (4 releases)
  og-image.jpg
  icon-16/32/180/192/512.png   favicon-32.png   favicon.ico
  logo.svg   logo.png
```

Paths are absolute (`/assets/...`), so the site must be served from the domain
root. Opening `index.html` straight from disk will not resolve the images — run
a local server to preview:

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

## Server notes

**Set long cache headers on `/assets/`.** This is the main reason the rebuild is
faster than the old single-file page — it only pays off if the browser is
allowed to keep the files. One year, immutable, is right for everything in
`assets/` since the filenames are stable and you would rename on change.

**Serve `.woff2` as `font/woff2`** and make sure it is not gzipped again (woff2
is already compressed).

**Force one hostname over HTTPS.** 301 `www.arlamusic.com`, `http://` and any
trailing-slash variants to `https://arlamusic.com/`. The canonical tag says that
is the real URL; the redirects are what make it true.

## Editing

Everything is in `index.html` — one file, no build step, no dependencies.

**If you change a fact, change it in three places.** Facts are deliberately
repeated so they are quotable by search engines and AI assistants:

1. the visible HTML (About section / FAQ),
2. the JSON-LD block in `<head>`,
3. `llms.txt`.

The stream count (`900,000+`) appears in all three, plus the meta description.
Search the folder for the number before you update it.

**If you edit an FAQ answer**, edit the matching `acceptedAnswer` in the JSON-LD
too. Google penalises a mismatch between visible FAQ text and its markup.

**Adding a release** means: cover image into `assets/` (500×500, save as both
`.webp` and `.jpg`), one `<a class="rel">` block in the Releases section, one
`MusicRecording` entry in the JSON-LD `track` array, one line in `llms.txt`, and
the image added to `sitemap.xml`.

## Colour and type

The muted greys (`--dim`, `--dimmer`) are tuned to pass WCAG AA contrast against
the background — 6.5:1 and 4.8:1. It is tempting to darken them for mood; that
drops body text below the 4.5:1 legibility minimum. There is a comment in the
CSS saying so.

Type is **Menda** throughout — the typeface from your logo — self-hosted as
WOFF2. Two weights are actually used:

- **Medium (500)** — all display type, headings and body. Menda has no weight
  below Medium, so 500 is the lightest setting available. Every heading is
  pinned to it, because browsers default `h1`/`h2` to bold and would otherwise
  download a font file for text that is never set in it.
- **SemiBold (600)** — the small uppercase labels, nav and buttons, where the
  extra weight keeps 10–11px type crisp on a dark ground.

**Bold (700)** ships and is declared, but nothing currently uses it. It costs
visitors nothing until something does — set `font-weight:700` on any element and
it loads on demand.

The hero wordmark is **not** set in Menda. It is your actual logo, traced to
vector, because the letterforms in it are custom-edited. Menda is used for
everything around it.

**Licensing:** Menda is © 2023 Yukita Creative. Desktop font licences frequently
do *not* cover `@font-face` web embedding — that is usually sold as a separate
webfont licence. Check what your licence covers before this goes live. If it
does not cover web use, the fix is small: buy the webfont licence, or keep Menda
for the logo only and set the surrounding text in a licensed lookalike.
