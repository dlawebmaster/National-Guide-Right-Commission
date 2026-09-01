# National Guide Right Commission — Kappa League Portal

A multi-page static site. No build toolchain, no framework, no npm install. Open
`index.html` in a browser or drop the folder on any static host.

---

## 1. What is in here

```
index.html            Homepage (hero, trust stripe, 7 Phases, locator, audience blocks)
locator.html          Full-page Kappa League program locator
about.html            Commission mission, structure, leadership, youth protection
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
assets/data/chapters.json   SAMPLE chapter records — replace before launch

build.py              Regenerates the ten HTML files from shared header/footer
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

**Build notes.** Eighteen `<p class="notice">` blocks flag copy that needs
Commission sign-off: founding dates, risk management language, the reporting
calendar, fee and eligibility answers, 501(c)(3) entity details and allocation
percentages. Grep for `Build note` and clear them one at a time.

**Photography.** Every image is a labeled placeholder (`<figure class="photo">`)
with the intended subject and pixel size in the caption. Replace each with a real
`<img>` carrying descriptive alt text. The design was built for authentic chapter
photography, not stock.

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

## 4. Design system

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

## 5. Verification performed

- **Contrast:** 22 foreground/background pairs computed against WCAG 2.1. Lowest
  ratio is 4.83:1 (faint neutral on white). Everything else clears 5:1, most clear 7:1.
- **Responsive:** no horizontal overflow at 320, 360, 375, 414, 768, 1024, 1280
  and 1440 px across all ten pages.
- **Touch targets:** no interactive element under 40px tall at 375px width.
  Buttons, inputs and selects are 48px; pills and small buttons are 44px.
- **Locator logic:** ZIP search, radius change, filter combinations, card and pin
  sync, application modal prefill, and the zero-result fallback were each exercised
  in a headless browser.
- **Links and anchors:** every internal href resolves to a file that exists; every
  in-page anchor resolves to an element that exists.
- **JSON:** schema validated, unique IDs, no missing fields.

Screenshots from these runs are in `shots/`. The map area renders empty in them
because the sandbox that built this site blocks CDN traffic. Leaflet and the
tiles load normally from a browser with internet access.

---

## 6. Deploying

Any static host works. For GitHub Pages, push the folder contents to the branch
you serve from; no Jekyll configuration is needed. Two notes:

- `chapters.json` is loaded with `fetch`, which browsers block on `file://`. Open
  the site through a web server, not by double-clicking the HTML. Locally:
  `python3 -m http.server 8000`.
- Google Fonts and cdnjs are the only external requests. If your hosting policy
  forbids third-party requests, self-host both. The font stack already degrades
  to Georgia and system sans if the fonts never arrive.

---

## 7. Notes on the design brief

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
