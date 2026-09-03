# National Guide Right Commission — Kappa League Portal

A multi-page static site. No build toolchain, no framework, no npm install. Open
`index.html` in a browser or drop the folder on any static host.

---

## 1. What is in here

```
index.html            Homepage (hero, trust stripe, 7 Phases, locator, audience blocks)
locator.html          Full-page Kappa League program locator
about.html            Commission mission, structure, leadership, youth protection
history.html          Guide Right history: timeline, primary sources, archives
kappa-league.html     Program overview, grade bands, program year, mentors
seven-phases.html     Full curriculum detail, phase by phase
kamp-kappa.html       Summer camp, STEM programming, travel grants
news.html             News layout and impact reporting (all entries are placeholders)
parents.html          Parent and student conversion page
donate.html           Donor and corporate sponsor page
chapters.html         Officer portal, certification, compliance, reporting

assets/css/site.css   Entire design system. One file, tokenized at the top.
assets/js/site.js     Mobile drawer, modal plumbing, footer year
assets/js/locator.js  Locator search, filtering, distance math, map, modals
assets/js/history.js  Sticky year rail on the history page
assets/data/chapters.json   SAMPLE chapter records — replace before launch
assets/img/                 Commission emblem and favicons (see section 4)

build.py              Regenerates the eleven HTML files from shared header/footer
shots/                Verification screenshots from the build
```

### Editing pages

Header, footer, navigation and the mobile drawer are defined once in `build.py`.
Change nav there and run `python3 build.py` to regenerate every page. If you would
rather hand-edit the HTML directly, delete `build.py` and edit the files; nothing
at runtime depends on it.

---

## 2. Before this goes live

Four things must be resolved. Each is marked in the code.

**Unverified figures.** The hero trust stripe carries `10,000+ mentees`,
`100% graduation rate`, `$1M+ scholarships` and `100+ years`. None of these were
verified, so each renders with a small crimson `verify` badge. Search for
`class="verify"` (nine instances across `index.html` and `news.html`) and either
replace the number with a documented figure and remove the badge, or delete the
tile. Do not ship the badge.

**Sample chapter data.** `assets/data/chapters.json` holds 21 placeholder records.
Chapter names are plausible, but program details, meeting schedules, application
windows and contact routing are invented for layout testing. The locator shows a
gold "Sample data" banner until you remove it from `build.py`. Keep the same JSON
shape and the locator needs no code changes; `meta.field_notes` documents every field.

**Build notes.** Twenty `<p class="notice">` blocks flag copy that needs
Commission sign-off: founding dates, risk management language, the reporting
calendar, fee and eligibility answers, 501(c)(3) entity details, allocation
percentages, and the unresolved year-round attribution on the history page. Grep for `Build note` and clear them one at a time.

**Photography.** The three hero-grid images are real. Every other image on the
site is still a labeled placeholder
(`<figure class="photo">`) with the intended subject and pixel size in the caption.
Replace each with a real photo using the `photo_real()` helper in `build.py`,
which handles the srcset, dimensions and lazy loading. The design was built for
authentic chapter photography, not stock.

---

## 3. The locator

### How it works

1. A ZIP code or city resolves to coordinates.
2. Haversine distance is computed from that point to every chapter.
3. Results are filtered by radius and by the active filter pills, then sorted
   nearest first.
4. Cards and map pins stay in sync. Clicking either highlights the other.

With no search entered, the list shows six programs alphabetically with a prompt
to search. This keeps the homepage from rendering the entire national directory.

### Geocoding

`assets/js/locator.js` checks a built-in table of ~70 metro centroids and every
sample chapter ZIP first, so common searches resolve instantly with no network
call. Anything else falls through to OpenStreetMap's Nominatim endpoint.

Nominatim is fine for development. It is not fine for production traffic: its
usage policy caps automated use and asks for attribution. Before launch, replace
the `fetch` in the `geocode()` function with your provider (Mapbox, Google,
Smarty, or a hosted ZIP centroid table). The function returns
`{ coords: [lat, lng], label: string }` and nothing else in the file needs to change.

### Map

Leaflet 1.9.4 from cdnjs, with OpenStreetMap tiles. Pins are CSS, not images, so
they inherit the crimson and gold palette directly and cost no requests.

To move to Mapbox or Google tiles, change `CONFIG.tileUrl` and
`CONFIG.tileAttribution` at the top of `locator.js`. To change the map library
entirely, `initMap`, `pinIcon` and `drawMarkers` are the only three functions that
touch Leaflet.

### Forms

All four forms (apply, contact director, request a League, contact province
director) are wired to intercept submit, show a success panel and transmit
nothing. Look for `wireForm()` near the bottom of `locator.js` and POST
`new FormData(form)` to your endpoint. The application form already carries
`chapter_id` and `chapter_name` as hidden fields, populated from the card the
user clicked.

---

## 4. Logo assets

The Commission emblem replaces the placeholder "GR" box in both the header and
the footer lockup. The supplied PNG was trimmed to its bounding box; its
background was already transparent, so it sits correctly on white and on the dark
footer without a visible plate.

| File | Size | Used by |
|---|---|---|
| `guide-right-emblem-320.png` | 298×320, 28 KB | Header (60px tall) and footer (74px tall) |
| `guide-right-emblem.png` | 953×1024, 160 KB | Master. Not loaded by any page. Use it for print, social or future assets |
| `favicon-32.png` | 32×32 | Browser tab |
| `favicon-180.png` | 180×180 | iOS home screen |

## Photographs

All three hero-grid slots now hold real photographs.

| File | Size | Used by |
|---|---|---|
| `kappa-league-temple-640.jpg` / `-960.jpg` | 640×423, 960×635 | Hero grid, large slot |
| `mentorship-monthly-session-640.jpg` / `-1170.jpg` | 640×464, 1170×848 | Hero grid, community service tile |
| `college-tour-800.jpg` / `-1600.jpg` | 800×600, 1600×1200 | Hero grid, college tour tile |
| `college-tour-wide-1600.jpg` | 1600×1200 | Not used. Wider establishing crop of the same frame |

**Crops.** The Temple frame and the Mansfield-Cedar Hill graphic are shown
uncropped, at their own aspect ratios, passed through `photo_real(ratio=...)`.
The monthly-session frame carries chapter branding in all four corners, and any
crop toward 16:9 would have cut the seal, the Texas mark or the Guide Right logo
off the edge. The college tour frame is the exception: its source was 7129×4935 and the
tile renders about 176px wide, so a wide establishing crop reduced the Leaguers
to specks. That one is pulled tight on the front rank, where the cardigans and
faces still read at tile size, and the wider version is kept alongside it.

**Delivery.** Two exports per photo wired through `srcset` with a `sizes` hint,
so a phone downloads the small file and a retina desktop gets the large one. All
carry explicit `width` and `height`. The large hero image is `eager` with
`fetchpriority="high"` because it is above the fold; the two tiles are lazy.

**Resolution ceiling.** The Temple photo tops out at 960px and the monthly-session
graphic at 1170px. Both are large enough for their current slots at 2x, but neither has room
to grow. If either is ever moved to a full-width band, source a higher-resolution
original rather than upscaling.

Alt text describes what the photograph shows rather than naming it. If you
publish a photo of identifiable minors, confirm a signed media release is on file
for every young man in the frame before it goes live.

The 320px file is quantized to 128 colors, which cut it from 142 KB to 28 KB with
no visible loss at display size. It serves both the 60px header and the 74px
footer, so it stays crisp on 2x and 3x displays from a single request. Both
`<img>` tags carry explicit `width` and `height` so the header reserves its space
before the image arrives and nothing shifts on load.

Alt text is intentionally empty (`alt=""`) on both. The emblem sits inside a link
whose adjacent text already reads "National Guide Right Commission", so a screen
reader announcing the image as well would repeat the name twice.

If you replace the emblem with a different file, keep the transparent background
and re-run the size exports. A logo with a baked-in white background will show as
a white rectangle against the footer.

---

## 5. Guide Right history

`history.html` and the "Our Legacy" section on the homepage. The homepage
introduces the history in three paragraphs, a sourced pull quote and a six-node
timeline teaser, then hands off to the history page for the full record.

### What the sources actually support

Every historical claim on these pages traces to the material supplied in the
project brief, drawn from the 1928, 1936 and 1952 Kappa Alpha Psi Fraternity
handbooks. Nothing was researched independently, inferred, or filled in.
Specifically:

- **No transcriptions were written.** The three primary-source panels open with
  an explicit "transcription not yet supplied" notice. Paste the verbatim
  handbook text into each, preserving original spelling, punctuation and
  terminology. Do not let anyone paraphrase into these slots.
- **No scans were faked.** Each panel carries a placeholder frame naming the file
  path to drop the real scan into (`assets/img/handbook-1928.jpg` and so on).
- **The Stewart/Steward variance is surfaced, not resolved.** The 1922 entry
  states plainly that the documents differ and that quotations keep their own
  source's spelling.
- **One attribution is unresolved.** The brief attributes the shift to year-round
  operation to "the later historical account" without naming a year. That entry
  carries a build note asking which handbook it comes from. Resolve it before
  publishing.
- **The 1952 objectives are labeled historical.** They appear under the heading
  "Historical 1952 objectives" with a line stating they are a record rather than
  the Commission's current objectives.
- **The then-and-now comparison claims no lineage.** The two columns sit side by
  side as themes, with a note stating that no modern phase is presented as the
  successor of a specific historical objective, because the sources do not
  document that.

### Design

The historical material uses a scoped archival treatment: a cream ground
(`--cream`) with two very low-contrast gradients standing in for aged paper, warm
near-black text, oversized crimson years, and Playfair for quotations against
Inter for explanation. It is applied only to `.archival` sections and the history
page. The rest of the site is untouched. No vintage textures, sepia filters or
period pastiche were applied globally.

The timeline is a semantic `<ol>` with one `<li>` per entry. On desktop a sticky
rail tracks which entry is in view via IntersectionObserver and marks it with
`aria-current`; the page is complete and readable with that script disabled. On
mobile the rail is hidden and the timeline collapses to a single chronological
column.

### Navigation change

Adding History made seven items in the header. The horizontal nav now needs
1240px; below that the drawer carries the full menu, including History. That
breakpoint moved up from 1060px, which is the only change to existing chrome. The
masthead also widened to 1400px so the row fits, and nav type steps down slightly
between 1240 and 1400px.

---

## 6. Design system

Tokens live at the top of `assets/css/site.css`.

| Token | Value | Used for |
|---|---|---|
| `--crimson` | `#70110C` | Primary CTAs, active pins, header stripe, structural borders |
| `--gold` | `#D4AF37` | Trim, badges, card top rules, donate button, secondary outlines |
| `--white` | `#FFFFFF` | Primary surface |
| `--surface` | `#F8F9FA` | Alternating sections, locator bar |
| `--ink` | `#111827` | Body and headings, dark sections, footer |
| `--ink-muted` | `#4B5563` | Sub-headlines, meeting schedules, distance labels |

Headings are Playfair Display, body is Inter, both from Google Fonts with system
fallbacks. Line height is 1.6 on body copy.

Gold is used as trim and on dark grounds only. Gold text on white fails AA at
normal sizes, so `--gold-deep` (`#8A6F17`) is provided for the rare case where
gold-toned text sits on a light background.

---

## 7. Verification performed

- **Contrast:** 22 foreground/background pairs computed against WCAG 2.1. Lowest
  ratio is 4.83:1 (faint neutral on white). Everything else clears 5:1, most clear 7:1.
- **Responsive:** no horizontal overflow at 21 widths from 320 to 1920 px across
  all eleven pages.
- **Touch targets:** no interactive element under 40px tall at 375px width.
  Buttons, inputs and selects are 48px; pills and small buttons are 44px.
- **Locator logic:** ZIP search, radius change, filter combinations, card and pin
  sync, application modal prefill, and the zero-result fallback were each exercised
  in a headless browser.
- **Links and anchors:** every internal href resolves to a file that exists; every
  in-page anchor resolves to an element that exists.
- **Logo:** header and footer lockups checked at 390, 1120 and 1440 px. Header
  sits on a single row at every width above the mobile breakpoint.
- **History page:** 19 additional contrast pairs checked across the archival
  palette; the two that fell under 4.5:1 were fixed with a darker `--gold-ink`
  for small gold text. Overflow re-checked at 21 widths from 320 to 1920px.
  Source modals open, trap focus and close on Escape.
- **JSON:** schema validated, unique IDs, no missing fields.

Screenshots from these runs are in `shots/`. The map area renders empty in them
because the sandbox that built this site blocks CDN traffic. Leaflet and the
tiles load normally from a browser with internet access.

---

## 8. Deploying

Any static host works. For GitHub Pages, push the folder contents to the branch
you serve from; no Jekyll configuration is needed. Two notes:

- `chapters.json` is loaded with `fetch`, which browsers block on `file://`. Open
  the site through a web server, not by double-clicking the HTML. Locally:
  `python3 -m http.server 8000`.
- Google Fonts and cdnjs are the only external requests. The emblem and favicons
  are local files. If your hosting policy
  forbids third-party requests, self-host both. The font stack already degrades
  to Georgia and system sans if the fonts never arrive.

---

## 9. Notes on the design brief

The spec called for TailwindCSS. This build uses hand-authored CSS instead,
because a multi-page static site with no build step would otherwise need the
Tailwind play CDN, which ships a compiler to every visitor, blocks first paint and
works against the sub-2-second target in the brief. The token block at the top of
`site.css` gives you the same single point of control over the palette. If you
later move to React or Next.js, the tokens port to a Tailwind theme config
directly.

Everything else follows the brief: no glassmorphism, no gradient meshes, no
floating 3D ornament, no stock carousel. Structure comes from rules, borders and
white space.
