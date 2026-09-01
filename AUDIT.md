# arlamusic.com — SEO / AEO / GEO audit and rebuild

24 August 2026 · revised 1 September 2026

---

## 1. What was missing

The old page looked good and said almost nothing a machine could read.

### Search engines had nothing to index

| Item | Before | Why it matters |
|---|---|---|
| `<title>` | `ARLA` | Four characters, competing with a Danish dairy cooperative and a clothing brand. No role, no genre, no city. |
| Meta description | **absent** | Google wrote its own snippet from whatever text it found — which was navigation labels. |
| `<h1>` | **absent** | No top-level heading anywhere. Section titles were `h2`s with nothing above them. |
| Canonical URL | **absent** | `arlamusic.com`, `www.` and `http://` could all be indexed as separate competing pages. |
| `robots.txt` | **404** | Confirmed missing on the live site. |
| `sitemap.xml` | **absent** | Nothing telling Google what exists or when it changed. |

### Social sharing was broken

No Open Graph or Twitter Card tags at all. Pasting `arlamusic.com` into WhatsApp,
an Instagram DM, Discord or X produced a bare blue link — no image, no title, no
description. For an artist whose distribution is people sharing links, this was
probably the single most expensive gap on the site.

### There was no structured data

Zero JSON-LD. Nothing machine-readable said that ARLA is a musician, that those
four tiles are recordings, or that the site and the Spotify profile are the same
entity. That connection is what produces an artist knowledge panel.

### The AEO / GEO problem: there was no text

This is the important one, and it is not a tags problem.

Answer engines — Google AI Overviews, ChatGPT, Perplexity, Claude — quote
**prose**. The old page contained roughly 60 words, all of them navigation
labels and track titles. No sentence anywhere said who ARLA is, what he makes,
or where he is from.

So when someone asked an assistant "who is ARLA, the Barcelona DJ?", there was
nothing on your own domain to retrieve. The only real bio text about you on the
open web was the two lines on your SoundCloud profile — which is where every
fact in the new About section came from, because your own site never stated
them.

### Accessibility, which is also a ranking input

- No `alt` text on any image, including all four covers and the logo.
- No skip link and no visible focus styles.
- Secondary text ran at **2.2:1 and 4.0:1** contrast, both under the WCAG AA
  minimum of 4.5:1.
- No `<main>`, no `<header>`, `div`s doing the job of headings.

### Performance

A single **390 KB** HTML file with the hero photo, logo and all four covers
inlined as base64. That means none of it could be cached — every visit
re-downloaded all 390 KB — base64 is ~33% larger than the bytes it encodes,
nothing could be lazy-loaded, and images had no `width`/`height` so the layout
jumped as they arrived.

---

## 2. What changed

### Design

Kept the black-and-red identity and the hero photograph. Those are the brand.

Rebuilt the structure around what actually makes the /zeroz reference feel
current: one large centred subject, deep whitespace, and small technical labels
pinned to the edges. The hero scrim was pulled back so the masked figure reads
*through* the wordmark instead of sitting behind a black wash.

The hero is the ARLA wordmark alone — no tagline, no framing parentheses, no
scroll cue. Your name is what people search, and stripping everything else out
of that first screen is what gives it the weight it has.

The site is now four screens: hero, Releases, Free Downloads, Contact.

### Typography

Bebas Neue and Space Mono are gone. Bebas is a condensed poster face that reads
as "event flyer" and was fighting the wide, geometric ARLA wordmark; the mono
was doing a second unrelated job alongside it.

Everything is now set in **Menda** — the typeface your logo is built from —
self-hosted as WOFF2. Using the logo's own face for the surrounding text is what
makes the page feel like one object rather than a logo dropped onto a template.

Two weights carry the whole site: Medium (500) for display and body, SemiBold
(600) for the small uppercase labels. Menda has nothing lighter than Medium, so
the airy 300-weight display setting used in the previous draft is not available;
at large sizes Medium reads close to it anyway, and it matches the wordmark
better.

The hero wordmark is deliberately **not** set in Menda — it is your actual logo,
traced from PNG to vector, because its letterforms are custom-edited. It went
from a 16 KB PNG that softened on retina screens to **1.8 KB** of SVG, sharp at
any size and inheriting text colour.

One licensing note, in section 4.

### SEO layer

- Descriptive `<title>` and meta description targeting *modern melodic techno*,
  *DJ / producer*, *Barcelona*.
- Full Open Graph and Twitter Card set, with a generated 1200×630 share image
  (`assets/og-image.jpg`) combining the hero photo and the wordmark.
- Canonical URL; robots directives with `max-image-preview:large`.
- One `h1`, then a clean `h2` hierarchy with no skipped levels.
- Descriptive `alt` text on all five images.
- `robots.txt` naming AI crawlers explicitly, `sitemap.xml` with image entries,
  `site.webmanifest`.

### Structured data

One JSON-LD `@graph`: `WebSite` · `WebPage` · `ImageObject` ·
`MusicGroup`+`Person` (ARLA), carrying four nested `MusicRecording` nodes.

The artist node carries genre, home location, a booking `contactPoint`, and
`sameAs` links to Spotify, SoundCloud and YouTube. That `sameAs` array is what
lets Google merge your website and your streaming profiles into a single entity
instead of three unrelated pages.

### AEO / GEO layer

This is where your last round of edits cost the most, and it is worth being
straight about it.

Removing the About and FAQ sections removed essentially all of the page's
crawlable prose. The site is back to roughly 90 words of visible text — track
titles, artist credits and navigation. That is the exact condition section 1
identified as the core AEO problem, and the fix has been undone by choice.

The `FAQPage` structured data went with it. That was not optional: Google
penalises FAQ markup whose answers are not visible on the page, so leaving the
schema behind after deleting the visible FAQ would have been worse than having
neither.

What still carries your identity to answer engines:

- **`llms.txt`** at the root — a clean structured summary of who you are, what
  you have released and where to listen. It now does most of the work that the
  About section used to, and it is the reason the situation is recoverable
  rather than back to zero. It also states plainly that you are not the dairy
  company, which is your single biggest disambiguation problem.
- **The `description` on the artist node** in the JSON-LD, which states in one
  sentence who you are, the stream count, who supports the music and where it
  has played. Schema descriptions do not require matching visible text, so this
  one is legitimate and stays.
- **The meta description**, which is a single sentence and is what shows up in a
  search result.

The honest summary: metadata now asserts your identity, but no human-readable
paragraph on the page corroborates it. Search engines weigh visible prose more
heavily than markup, precisely because markup is easy to game. If you later want
the AEO ground back without the site getting wordy, the cheapest version is
three or four sentences somewhere above the footer — it does not need a heading,
a stat block or an FAQ accordion.

### Performance

| | Before | After |
|---|---|---|
| Critical path to first paint | 390 KB, uncacheable | **123 KB** |
| Full page, all four covers | 390 KB | **253 KB**, cacheable |
| Cumulative Layout Shift | shifted as images arrived | **0.000** |
| First Contentful Paint | — | 336 ms (local server) |

Images extracted to real files and served as WebP with JPEG fallbacks through
`<picture>`; hero preloaded at `fetchpriority="high"` with an 800 px variant for
phones; all four covers `loading="lazy"`; explicit `width`/`height` on every
image, which is why CLS is zero; the Medium weight preloaded, and every heading
pinned to a weight that actually ships.

The headline number is not really the 253 KB — it is that assets are now
separate cacheable files instead of one blob that had to be re-downloaded in
full on every single visit.

### Accessibility

Skip link, visible focus rings, `<main>` / `<header>` / `<section>` semantics,
`aria-label`s on the icon-only controls, a keyboard-operable mobile menu with
`aria-expanded` that closes on `Escape` and restores body scroll, and
`prefers-reduced-motion` honoured throughout.

The muted greys were measured and moved to 6.5:1 and 4.8:1 against the
background, both clearing WCAG AA. There is a comment in the CSS saying so,
because darkening them for mood is the obvious temptation.

---

## 3. Verification performed

- Rendered at 1920, 1440, 1024, 768, 390 and 320 px. **No horizontal overflow at
  any width** (measured, not eyeballed).
- **Found and fixed a broken mobile hero:** the hero was a CSS grid whose side
  labels were absolutely positioned on desktop. On mobile they rejoined the flow
  and each took its own grid row, spreading the wordmark to the bottom of the
  screen. Rebuilt as a flex column with explicit ordering.
- **Found and fixed a missing mobile menu:** the nav links were simply hidden
  under 860 px with nothing replacing them, leaving phone visitors no navigation
  at all. There is now a real menu — burger button, full-screen overlay,
  staggered reveal, closes on link click and on `Escape`.
- **Found and fixed uneven release cards:** the first card's title wraps to two
  lines, which pushed its "Listen" link out of alignment with the other three.
  Cards are now flex columns with the link pinned to the bottom.
- Added a scroll-driven safety sweep behind the reveal animations, so a fast
  flick-scroll cannot outrun the IntersectionObserver and strand a section at
  opacity 0.
- JSON-LD parsed and all nodes validated; `sitemap.xml` and `site.webmanifest`
  parsed.
- All internal anchors resolved against real element IDs; all 17 asset
  references checked to exist on disk. No broken references.
- Contrast ratios computed programmatically rather than judged by eye.
- Console checked at both breakpoints: no errors, no page errors.
- **Found and fixed an invisible font cost:** browsers default `h1`/`h2` to bold,
  so the page was downloading Menda Bold (36 KB) for headings that are set in
  Medium and for one screen-reader-only line. Headings are now pinned to 500 and
  Bold no longer loads at all.
- Confirmed Menda actually applies rather than silently falling back — computed
  `font-family` and `font-weight` read back from the live DOM, not eyeballed.
- Re-checked the removals: no dead CSS left behind for the deleted sections, no
  orphaned `#about` or `#faq` anchors in the nav or mobile menu, section
  numbering renumbered to 01/02 and 02/02.

---

## 4. Things I need you to confirm

I built the copy and structured data from facts I could verify, and did not
invent anything. Three items are still your call.

1. **`contact@arlamusic.com`** — carried over from the old site. Confirm it is
   live and monitored, because it is now the booking contact point inside your
   structured data, not just a link.

2. **The stream count goes stale.** `900,000+` is hard-coded in four places
   (visible facts block, FAQ answer, JSON-LD description, `llms.txt`) plus the
   meta description. Search the folder for the number when you update it. I
   deliberately left out Spotify monthly listeners, which moves weekly and would
   have been wrong within a fortnight.

3. **The four Hypeddit download links** could not be verified — outbound requests
   to that host were blocked from my environment. Please click each one once
   after deploying.

4. **Menda's licence — check this before going live.** Menda is © 2023 Yukita
   Creative. Desktop font licences very often do *not* cover `@font-face` web
   embedding; that is normally sold separately as a webfont licence. I have
   self-hosted it because that is what you asked for and it is the right
   technical choice, but I cannot verify what you bought. If your licence does
   not cover web use, the options are to buy the webfont add-on, or to keep
   Menda for the logo only — which is already a traced SVG and not affected —
   and set the surrounding text in something licensed for the web.

One thing worth knowing: your SoundCloud handle is `arla_ofc`, and there is a
`soundcloud.com/arlaofc` in circulation too. I used `arla_ofc` throughout since
that is the one that resolves. Worth claiming the other if it is not already
yours.

---

## 5. What to do after deploying

The on-page work is finished. These are the off-site steps that actually move
rankings, in rough order of payoff.

**Immediately after upload**

1. **Google Search Console** — add and verify `arlamusic.com`, submit
   `sitemap.xml`, then request indexing on the homepage. Without this you are
   waiting weeks for a natural crawl.
2. **Bing Webmaster Tools** — same. Bing's index feeds ChatGPT's search, so this
   is a direct AEO lever rather than an afterthought.
3. **Test the share preview** — paste the URL into a real WhatsApp chat and
   check the card renders before promoting the link anywhere.
4. **Validate the structured data** with Google's Rich Results Test. It should
   report both a music entity and an FAQ.
5. **Force HTTPS and one hostname** — 301 everything to `https://arlamusic.com/`.

**Entity work — this is what builds a knowledge panel**

Google decides ARLA is a real musical entity by seeing the same identity
asserted consistently across independent sources. Right now your site says it
and almost nothing else does.

6. **Claim Spotify for Artists.** Fill in the bio, image and socials, and make
   sure `arlamusic.com` is listed there.
7. **Get a MusicBrainz entry.** Free, community-editable, and a primary source
   that Google and several LLMs ingest directly for music entities. Probably the
   highest-leverage single item on this list.
8. **Put your website URL on every profile** — SoundCloud, YouTube, Instagram,
   Beatport, Linktree. `sameAs` in your schema points outward; these are the
   links that point back and close the loop.
9. **Keep the bio wording consistent** across SoundCloud, Spotify, YouTube and
   Instagram, close to the sentence now on the site. Corroborated repetition
   across independent domains is exactly what an entity resolver looks for.

**Ongoing**

10. **Give each release its own page** eventually — `/releases/ko-arla-remix/`
    and so on. A single-page site can only ever rank for one cluster of terms.
    Per-release pages let you rank for "K.O. ARLA remix" specifically, each with
    its own `MusicRecording` schema. This is the biggest remaining structural
    limit on the site.
11. **Press and blog mentions** matter more than any tag on the page. One
    write-up on a real electronic music site does more for entity recognition
    than everything in section 2 combined.
12. **Re-run the Rich Results Test whenever you edit the FAQ.** If the visible
    `<details>` text and the JSON-LD drift apart, Google penalises the mismatch.

---

## 6. Honest limitations

- **It is still one page.** Everything above is the ceiling of what a single URL
  can achieve. Item 10 is the real next step.
- **No analytics is installed.** I did not add Google Analytics or Plausible
  because I do not know what you use, and installing a tracker unasked is not my
  call. You will want something, or you cannot tell whether any of this worked.
- **Performance numbers are from a local server**, not a real network. The byte
  counts are exact; the millisecond timings will be slower in the wild and
  depend on your host.
- **Nothing here is a ranking guarantee.** On-page SEO makes you *eligible* to
  rank. Streams, press and inbound links are what actually rank an artist.
- **The width axis needs a modern browser.** Anything without variable-font
  support renders headings at normal width. It degrades invisibly.
