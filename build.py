#!/usr/bin/env python3
"""
Static site generator for the National Guide Right Commission portal.

Every page shares one header, footer, drawer and mobile action bar defined here,
so a nav change is a one-file change. Run `python3 build.py` to regenerate the
HTML files at the project root. Assets are never touched.
"""

import os
import re

OUT = os.path.dirname(os.path.abspath(__file__))

SITE_NAME = "National Guide Right Commission"
SITE_SUB = "Kappa Alpha Psi Fraternity, Inc."

NAV = [
    ("about.html", "About Us"),
    ("history.html", "History"),
    ("kappa-league.html", "Kappa League"),
    ("seven-phases.html", "7 Phases"),
    ("kamp-kappa.html", "Kamp Kappa &amp; STEM"),
    ("news.html", "News &amp; Impact"),
]

DRAWER_EXTRA = [
    ("parents.html", "For Parents &amp; Students"),
    ("chapters.html", "Chapter Officer Resources"),
    ("locator.html", "Find a Kappa League"),
    ("donate.html", "Support the Commission"),
]


def verify(text):
    """Wrap an unconfirmed figure so it cannot ship unnoticed."""
    return f'{text}<span class="verify" title="Unverified figure. Confirm with the Commission or remove before launch.">verify</span>'


# --------------------------------------------------------------------------- shell


def head(title, description, page):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | {SITE_NAME}</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{title} | {SITE_NAME}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap">
<link rel="icon" type="image/png" sizes="32x32" href="assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="assets/img/favicon-180.png">
<link rel="stylesheet" href="assets/css/site.css">
</head>
<body data-page="{page}">
<a class="skip-link" href="#main">Skip to main content</a>
"""


CURRENT = ' aria-current="page"'


def header(page):
    nav_links = "".join(
        '<a href="%s"%s>%s</a>' % (href, CURRENT if href == page else "", label)
        for href, label in NAV
    )
    drawer_links = "".join(
        '<a href="%s"%s>%s</a>' % (href, CURRENT if href == page else "", label)
        for href, label in NAV + DRAWER_EXTRA
    )
    return f"""
<div class="utility">
  <div class="shell utility__inner">
    <span class="utility__tag">Youth leadership and development, grades 6 through 12</span>
    <nav class="utility__links" aria-label="Utility">
      <a href="chapters.html">Chapter Portal Login</a>
      <a href="about.html#contact">Contact Us</a>
      <a href="donate.html#transparency">Tax-Deductible 501(c)(3) Info</a>
    </nav>
  </div>
</div>

<header class="masthead">
  <div class="shell masthead__inner">
    <a class="brand" href="index.html">
      <img class="brand__mark" src="assets/img/guide-right-emblem-320.png" width="298" height="320" alt="" decoding="async">
      <span class="brand__text">
        <span class="brand__name">{SITE_NAME}</span>
        <span class="brand__sub">{SITE_SUB}</span>
      </span>
    </a>

    <nav class="nav" aria-label="Primary">{nav_links}</nav>

    <div class="masthead__actions">
      <a class="btn btn--primary" href="locator.html">Find Kappa League</a>
      <a class="btn btn--gold" href="donate.html">Donate</a>
    </div>

    <button class="hamburger" id="drawer-open" type="button" aria-expanded="false" aria-controls="drawer">
      <span class="hamburger__bars" aria-hidden="true"><span></span><span></span><span></span></span>
      Menu
    </button>
  </div>
</header>

<div class="drawer" id="drawer" data-open="false" role="dialog" aria-modal="true" aria-label="Site menu">
  <div class="drawer__scrim" data-drawer-close></div>
  <div class="drawer__panel">
    <div class="drawer__head">
      <span class="kicker">Menu</span>
      <button class="drawer__close" type="button" data-drawer-close aria-label="Close menu">&times;</button>
    </div>
    <nav class="drawer__nav" aria-label="Mobile">{drawer_links}</nav>
    <div class="drawer__actions">
      <a class="btn btn--primary btn--block" href="locator.html">Find Kappa League</a>
      <a class="btn btn--gold btn--block" href="donate.html">Donate</a>
    </div>
    <p class="drawer__meta">The National Guide Right Commission is the youth mentorship arm of Kappa Alpha Psi Fraternity, Inc.</p>
  </div>
</div>
"""


FOOTER = """
<footer class="footer">
  <div class="shell">
    <div class="footer__grid">
      <div>
        <a class="brand" href="index.html">
          <img class="brand__mark brand__mark--footer" src="assets/img/guide-right-emblem-320.png" width="298" height="320" alt="" loading="lazy" decoding="async">
          <span class="brand__text">
            <span class="brand__name">National Guide Right Commission</span>
            <span class="brand__sub">Kappa Alpha Psi Fraternity, Inc.</span>
          </span>
        </a>
        <p style="margin-top:1rem;max-width:34ch;color:#9CA3AF;font-size:.875rem;">
          Guide Right is the community service and youth mentorship program of Kappa Alpha Psi Fraternity, Inc.
          The Kappa Youth Leadership and Development League, known as Kappa League, is its flagship initiative for young men in grades 6 through 12.
        </p>
      </div>
      <div>
        <h3>Programs</h3>
        <ul>
          <li><a href="kappa-league.html">Kappa League</a></li>
          <li><a href="seven-phases.html">The 7 Phases</a></li>
          <li><a href="kamp-kappa.html">Kamp Kappa &amp; STEM</a></li>
          <li><a href="locator.html">Find a Program</a></li>
        </ul>
      </div>
      <div>
        <h3>Get Involved</h3>
        <ul>
          <li><a href="parents.html">Parents &amp; Students</a></li>
          <li><a href="donate.html">Donors &amp; Sponsors</a></li>
          <li><a href="chapters.html">Chapter Officers</a></li>
          <li><a href="news.html">News &amp; Impact</a></li>
        </ul>
      </div>
      <div>
        <h3>Commission</h3>
        <ul>
          <li><a href="about.html">About Guide Right</a></li>
          <li><a href="history.html">Guide Right History</a></li>
          <li><a href="about.html#leadership">Leadership</a></li>
          <li><a href="about.html#contact">Contact</a></li>
          <li><a href="donate.html#transparency">501(c)(3) Information</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__legal">
      <span>&copy; <span data-year>2026</span> Kappa Alpha Psi Fraternity, Inc. All rights reserved.</span>
      <span>Placeholder build. Replace legal entity details, privacy policy and youth-protection notices before launch.</span>
    </div>
  </div>
</footer>

<div class="mobile-bar">
  <a class="btn btn--primary btn--sm" href="locator.html">Find Kappa League</a>
  <a class="btn btn--gold btn--sm" href="donate.html">Donate</a>
</div>
"""


def page(filename, title, description, body, extra_head="", extra_scripts=""):
    html = (
        head(title, description, filename).replace("</head>", extra_head + "</head>")
        + header(filename)
        + '\n<main id="main">\n'
        + body
        + "\n</main>\n"
        + FOOTER
        + '\n<script src="assets/js/site.js"></script>\n'
        + extra_scripts
        + "</body>\n</html>\n"
    )
    with open(os.path.join(OUT, filename), "w", encoding="utf-8") as f:
        f.write(html)
    return filename


# --------------------------------------------------------------------------- blocks


def photo_real(base, alt, widths=(800, 1600), mod="",
               sizes="(min-width: 940px) 22vw, 45vw", ratio=None, eager=False):
    """A real photograph.

    base    filename stem in assets/img/, with one JPEG per entry in widths
    widths  exported widths, smallest first; the smallest is the src fallback
    ratio   (w, h) to override the tile aspect. Use it when the frame should not
            be cropped, for example a graphic with branding in its corners.
    eager   skip lazy loading. Set it on anything above the fold.
    """
    srcset = ", ".join(f"assets/img/{base}-{w}.jpg {w}w" for w in widths)
    small = widths[0]
    style = f' style="aspect-ratio: {ratio[0]} / {ratio[1]};"' if ratio else ""
    loading = "eager" if eager else "lazy"
    priority = ' fetchpriority="high"' if eager else ""
    big = widths[-1]
    return f"""<figure class="photo photo--filled {mod}"{style}>
      <img src="assets/img/{base}-{small}.jpg"
           srcset="{srcset}"
           sizes="{sizes}"
           width="{big}" height="{{}}" loading="{loading}" decoding="async"{priority}
           alt="{alt}">
    </figure>""".replace("{}", str(round(big * (ratio[1] / ratio[0]) if ratio else big * 0.75)))


def photo(label, note, mod=""):
    return f"""<figure class="photo {mod}">
      <figcaption class="photo__label">{label}<span>{note}</span></figcaption>
    </figure>"""


def pagehead(title, lede, crumb, anchors=None):
    a = ""
    if anchors:
        a = '<nav class="anchor-nav" aria-label="On this page">' + "".join(
            f'<a href="#{i}">{t}</a>' for i, t in anchors
        ) + "</nav>"
    return f"""
<section class="pagehead">
  <div class="shell">
    <p class="crumbs"><a href="index.html">Home</a> &rsaquo; {crumb}</p>
    <h1>{title}</h1>
    <p class="lede measure">{lede}</p>
    {a}
  </div>
</section>
"""


GUIDE_RIGHT_OBJECTIVES = [
    "Create the next generation of leaders through leadership development",
    "Prepare students for college",
    "Mentor students to college graduation",
    "Positively impact youth through mentoring and training",
    "Prepare youth for academic success in middle school, high school and college",
]

GUIDE_RIGHT_IMPACT = [
    ("98%", "of Guide Right students graduate high school"),
    ("77%", "graduate college within six years"),
    ("500K+", "young lives impacted"),
    ("266", "chapters"),
    ("11,100+", "students"),
]


def guide_right_section():
    objectives = "".join(f"<li>{o}</li>" for o in GUIDE_RIGHT_OBJECTIVES)
    impact = "".join(
        f'<div class="impact__item"><p class="impact__fig">{fig}</p><p class="impact__lbl">{lbl}</p></div>'
        for fig, lbl in GUIDE_RIGHT_IMPACT
    )
    return f"""
<section class="section" id="guide-right">
  <div class="shell">
    <p class="eyebrow--plain eyebrow">Our National Service Initiative</p>
    <h2>Guide Right</h2>

    <div class="split">
      <div>
        <p class="lede">Guide Right is our National Service Initiative and includes all our youth-oriented programs. The flagship initiative of the Guide Right Service Program is the Kappa Leadership Development League, known as Kappa League.</p>
        <p>Guide Right is a program of the educational and occupational guidance of youth, primarily inspirational and informative in character. The purpose of the Guide Right Service Program is to place the training, experience and interest of successful men at the disposal of youth.</p>
        <p>We focus on developing leadership, creating an achievement mindset, and mentoring. We have mentored over 500,000 young people.</p>
        <p class="statement">We are the oldest, most successful mentoring program for young people of color.</p>
      </div>

      <div>
        <h3>Guide Right objectives</h3>
        <ol class="objectives-grid" style="grid-template-columns:1fr;">{objectives}</ol>
        <div class="btn-row" style="margin-top:1.75rem;">
          <a class="btn btn--ghost btn--sm" href="history.html">Read the Guide Right history &rarr;</a>
        </div>
      </div>
    </div>

    <h3 style="margin-top:2.5rem;margin-bottom:0;">Our impact</h3>
    <div class="impact">{impact}</div>
    <p class="impact__note">Figures supplied by the National Guide Right Commission.</p>

    <p class="notice" style="margin-top:1.75rem;">
      <strong>Build note.</strong> These figures conflict with the hero stripe above, which still carries the placeholder values <em>10,000+ mentees</em> and a <em>100% graduation rate</em>. Two different numbers for the same measure cannot both ship. Align the stripe with the figures in this section, or remove the stripe.
    </p>
  </div>
</section>
"""


def video_section():
    return """
<section class="section section--surface" id="watch">
  <div class="shell">
    <p class="eyebrow--plain eyebrow">Watch</p>
    <h2>Ensure No Graduate is Left Behind</h2>
    <p class="lede measure">The Kappa League to Kappa Kollege handoff, and what it takes to carry a young man past the diploma.</p>

    <div class="video__wrap" style="margin-top:2rem;">
      <div class="video">
        <iframe
          src="https://www.youtube-nocookie.com/embed/_AXTGy5hg78"
          title="Ensure No Graduate is Left Behind: Kappa League to Kappa Kollege handoff"
          loading="lazy"
          referrerpolicy="strict-origin-when-cross-origin"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
          allowfullscreen></iframe>
      </div>

      <div class="video__meta">
        <span class="kicker">About this video</span>
        <p>Guide Right does not end at high school graduation. The handoff from Kappa League into Kappa Kollege is how the Commission keeps a mentor in a young man's life through the years when most programs let go.</p>
        <div class="btn-row">
          <a class="btn btn--outline btn--sm" href="https://www.youtube.com/watch?v=_AXTGy5hg78" target="_blank" rel="noopener">Watch on YouTube</a>
        </div>
        <p class="notice" style="margin-top:1.25rem;">
          <strong>Build note.</strong> The video title is taken from the link you supplied. Confirm the publishing channel and add a caption or transcript link so the content is available to visitors who cannot use the player.
        </p>
      </div>
    </div>
  </div>
</section>
"""


LEGACY_TEASER = [
    ("1922", "The Idea"),
    ("1923", "National Adoption"),
    ("1928", "Early Vision"),
    ("1936", "Year-Round Development"),
    ("1952", "Expanded Program"),
    ("Today", "The Legacy Continues"),
]


def legacy_section():
    nodes = "".join(
        f'''<li class="teaser__node">
            <p class="teaser__year">{yr}</p>
            <p class="teaser__label">{label}</p>
          </li>'''
        for yr, label in LEGACY_TEASER
    )
    return f"""
<section class="section archival" id="legacy">
  <div class="shell">
    <p class="eyebrow--plain eyebrow">Our Legacy</p>
    <h2>More Than a Century of Guide Right</h2>
    <p class="kicker" style="color:var(--sepia-muted);margin-bottom:1.25rem;">A National Movement Since 1922</p>

    <div class="legacy__grid">
      <div>
        <p>Guide Right began in St. Louis, Missouri, in 1922 from a vision to provide young men with guidance, mentorship, vocational direction, and opportunities to prepare for lives of usefulness and service.</p>
        <p>What began as an initiative of the St. Louis Alumni Chapter developed into a national movement of Kappa Alpha Psi Fraternity, Inc. Over the decades, Guide Right expanded from its early emphasis on vocational guidance into a year-round youth development program centered on mentorship, education, leadership, career preparation, service, and personal development.</p>
        <p>For more than a century, the methods have evolved while the commitment to guiding young men toward productive futures has endured.</p>
        <div class="btn-row" style="margin-top:1.75rem;">
          <a class="btn btn--primary" href="history.html">Explore our history &rarr;</a>
        </div>
      </div>

      <div class="legacy__quote">
        <blockquote>&ldquo;How shall I invest my life?&rdquo;</blockquote>
        <cite>Recorded in the 1952 historical account</cite>
        <p>The question early Guide Right leaders set out to help young men answer. More than a century later, it is still the work.</p>
      </div>
    </div>

    <div class="teaser">
      <h3 class="visually-hidden">Guide Right milestones</h3>
      <ol class="teaser__track">{nodes}</ol>
      <p class="teaser__hint">Scroll for more milestones.</p>
    </div>
  </div>
</section>
"""


PHASES = [
    ("I", "Self-Identity &amp; Purpose",
     "Discipline, character, self-assurance and personal presentation. Every Leaguer begins by learning who he is and what he is accountable for."),
    ("II", "Training &amp; Academic Preparation",
     "Tutoring, study habits and college entrance preparation. Grades are tracked term over term, and mentors intervene early."),
    ("III", "Competition &amp; Preparedness",
     "Public speaking, debate, academic bowls and sportsmanship. Leaguers compete at chapter, province and national levels."),
    ("IV", "Social &amp; Cultural Awareness",
     "Etiquette, fine arts and interpersonal communication. Young men learn to carry themselves in any room they enter."),
    ("V", "Health &amp; Wellness Education",
     "Physical fitness, mental health awareness and personal health literacy taught by qualified presenters."),
    ("VI", "Economic Empowerment",
     "Financial literacy, budgeting, investing and entrepreneurship, taught with real accounts and real decisions."),
    ("VII", "College &amp; Career Readiness",
     "Campus tours, FAFSA assistance, resume workshops and sustained mentorship through the college application cycle."),
]


def phase_cards(limit=None):
    items = PHASES if limit is None else PHASES[:limit]
    out = []
    for num, name, body in items:
        out.append(f"""<article class="card phase">
        <span class="phase__index" aria-hidden="true">{num}</span>
        <span class="card__num">Phase {num}</span>
        <h3>{name}</h3>
        <p>{body}</p>
      </article>""")
    return "\n".join(out)


LOCATOR_HEAD = """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css" crossorigin="anonymous" referrerpolicy="no-referrer">
"""

LOCATOR_SCRIPTS = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
<script src="assets/js/locator.js"></script>
"""


def locator_block(heading=True):
    head_markup = ""
    if heading:
        head_markup = """
    <p class="eyebrow">Program Locator</p>
    <h2>Find an active Kappa League near you</h2>
    <p class="lede measure">Search by ZIP code or city. Results show meeting schedules, grade bands and whether applications are open right now.</p>
"""
    return f"""
<section class="section locator-section" id="find">
  <div class="shell shell--wide">
    {head_markup}
    <div class="sample-banner">
      <strong>Sample data.</strong>
      <span>Chapter records below are structural placeholders for build and testing. Replace <code>assets/data/chapters.json</code> with records verified by the Commission before launch.</span>
    </div>

    <div class="locator" id="locator" data-view="list" data-source="assets/data/chapters.json">
      <div class="locator__bar">
        <form class="locator__row" id="loc-form" role="search">
          <div class="field">
            <label for="loc-query">ZIP code or city and state</label>
            <input type="search" id="loc-query" name="q" placeholder="76201 or Denton, TX" autocomplete="postal-code" inputmode="search">
          </div>
          <div class="field">
            <label for="loc-radius">Distance</label>
            <select id="loc-radius" name="radius">
              <option value="10">Within 10 miles</option>
              <option value="25" selected>Within 25 miles</option>
              <option value="50">Within 50 miles</option>
              <option value="100">Within 100 miles</option>
            </select>
          </div>
          <button class="btn btn--primary" type="submit">Search</button>
          <button class="btn btn--outline" type="button" id="loc-geo">Use my location</button>
        </form>

        <div class="filters" role="group" aria-label="Program filters">
          <button type="button" class="pill" data-filter="has_league" aria-pressed="true">
            <span class="pill__box" aria-hidden="true">&#10003;</span> Has active Kappa League
          </button>
          <button type="button" class="pill" data-filter="accepting" aria-pressed="false">
            <span class="pill__box" aria-hidden="true">&#10003;</span> Currently accepting applications
          </button>
          <button type="button" class="pill" data-filter="junior" aria-pressed="false">
            <span class="pill__box" aria-hidden="true">&#10003;</span> Junior League, grades 6&ndash;8
          </button>
          <button type="button" class="pill" data-filter="senior" aria-pressed="false">
            <span class="pill__box" aria-hidden="true">&#10003;</span> Senior League, grades 9&ndash;12
          </button>
        </div>

        <div class="view-toggle" role="group" aria-label="Result view">
          <button type="button" data-view-btn="list" aria-pressed="true">List view</button>
          <button type="button" data-view-btn="map" aria-pressed="false">Map view</button>
        </div>
      </div>

      <p id="loc-status" class="visually-hidden" role="status" aria-live="polite"></p>

      <div class="locator__split">
        <div class="locator__results" id="loc-results" aria-label="Search results">
          <p class="locator__count" id="loc-count">Loading</p>
          <div id="loc-list"></div>
        </div>
        <div class="locator__map" id="loc-map" role="application" aria-label="Map of Kappa League programs"></div>
      </div>
      <p class="small muted" style="margin-top:.85rem;">Sorted by distance from your search location. Programs marked <em>in formation</em> have no chartered League yet and route to an interest list.</p>
    </div>
  </div>
</section>

<!-- Application modal ------------------------------------------------------>
<div class="modal" id="modal-apply" data-open="false" role="dialog" aria-modal="true" aria-labelledby="apply-title">
  <div class="modal__scrim" data-modal-close></div>
  <div class="modal__panel">
    <div class="modal__head">
      <div>
        <h2 id="apply-title">Apply to this Kappa League</h2>
        <p class="small muted" style="margin:0;">Takes about four minutes. A chapter officer follows up with orientation details.</p>
      </div>
      <button class="modal__close" type="button" data-modal-close aria-label="Close">&times;</button>
    </div>
    <div class="modal__chapter" id="apply-chapter"></div>
    <p class="form-status" id="apply-status" hidden></p>
    <form class="form-grid" id="apply-form">
      <input type="hidden" id="apply-chapter-id" name="chapter_id">
      <input type="hidden" id="apply-chapter-name" name="chapter_name">
      <div class="form-grid form-grid--2">
        <div class="field"><label for="apply-student">Student name</label><input id="apply-student" name="student_name" required></div>
        <div class="field"><label for="apply-grade">Grade level</label>
          <select id="apply-grade" name="grade" required>
            <option value="">Select</option>
            <option>6th</option><option>7th</option><option>8th</option>
            <option>9th</option><option>10th</option><option>11th</option><option>12th</option>
          </select>
        </div>
      </div>
      <div class="form-grid form-grid--2">
        <div class="field"><label for="apply-parent">Parent or guardian name</label><input id="apply-parent" name="parent_name" required></div>
        <div class="field"><label for="apply-phone">Phone</label><input id="apply-phone" name="phone" type="tel" required></div>
      </div>
      <div class="field"><label for="apply-email">Email</label><input id="apply-email" name="email" type="email" required></div>
      <div class="field"><label for="apply-school">School</label><input id="apply-school" name="school"></div>
      <div class="field"><label for="apply-notes">Anything the chapter should know</label><textarea id="apply-notes" name="notes" rows="3"></textarea></div>
      <p class="form-note">Submitting shares this information with the chapter Guide Right Chairman only. Every adult volunteer completes fraternity background screening and youth-protection training.</p>
      <button class="btn btn--primary btn--block" type="submit">Submit application</button>
    </form>
  </div>
</div>

<!-- Contact director modal ------------------------------------------------->
<div class="modal" id="modal-contact" data-open="false" role="dialog" aria-modal="true" aria-labelledby="contact-title">
  <div class="modal__scrim" data-modal-close></div>
  <div class="modal__panel">
    <div class="modal__head">
      <div>
        <h2 id="contact-title">Contact the program director</h2>
        <p class="small muted" style="margin:0;">Routes to the chapter Guide Right Chairman.</p>
      </div>
      <button class="modal__close" type="button" data-modal-close aria-label="Close">&times;</button>
    </div>
    <div class="modal__chapter" id="contact-chapter"></div>
    <p class="form-status" id="contact-status" hidden></p>
    <form class="form-grid" id="contact-form">
      <input type="hidden" id="contact-chapter-id" name="chapter_id">
      <input type="hidden" id="contact-chapter-name" name="chapter_name">
      <div class="form-grid form-grid--2">
        <div class="field"><label for="contact-name">Your name</label><input id="contact-name" name="name" required></div>
        <div class="field"><label for="contact-grade">Student grade level</label>
          <select id="contact-grade" name="grade">
            <option value="">Select</option>
            <option>6th</option><option>7th</option><option>8th</option>
            <option>9th</option><option>10th</option><option>11th</option><option>12th</option>
          </select>
        </div>
      </div>
      <div class="form-grid form-grid--2">
        <div class="field"><label for="contact-phone">Phone</label><input id="contact-phone" name="phone" type="tel"></div>
        <div class="field"><label for="contact-email">Email</label><input id="contact-email" name="email" type="email" required></div>
      </div>
      <div class="field"><label for="contact-msg">Your question</label><textarea id="contact-msg" name="message" rows="4" required></textarea></div>
      <button class="btn btn--primary btn--block" type="submit">Send message</button>
    </form>
  </div>
</div>

<!-- Start a League modal --------------------------------------------------->
<div class="modal" id="modal-start" data-open="false" role="dialog" aria-modal="true" aria-labelledby="start-title">
  <div class="modal__scrim" data-modal-close></div>
  <div class="modal__panel">
    <div class="modal__head">
      <div>
        <h2 id="start-title">Bring Kappa League to your district</h2>
        <p class="small muted" style="margin:0;">The Commission reviews every request against nearby chapter capacity.</p>
      </div>
      <button class="modal__close" type="button" data-modal-close aria-label="Close">&times;</button>
    </div>
    <p class="form-status" id="start-status" hidden></p>
    <form class="form-grid" id="start-form">
      <div class="form-grid form-grid--2">
        <div class="field"><label for="start-name">Your name</label><input id="start-name" name="name" required></div>
        <div class="field"><label for="start-role">Your role</label>
          <select id="start-role" name="role">
            <option>Parent or guardian</option>
            <option>Student</option>
            <option>School or district staff</option>
            <option>Community organization</option>
            <option>Fraternity member</option>
          </select>
        </div>
      </div>
      <div class="form-grid form-grid--2">
        <div class="field"><label for="start-email">Email</label><input id="start-email" name="email" type="email" required></div>
        <div class="field"><label for="start-zip">ZIP code</label><input id="start-zip" name="zip" inputmode="numeric" required></div>
      </div>
      <div class="field"><label for="start-detail">Schools, districts or community sites to serve</label><textarea id="start-detail" name="detail" rows="3"></textarea></div>
      <button class="btn btn--primary btn--block" type="submit">Submit request</button>
    </form>
  </div>
</div>

<!-- Province director modal ------------------------------------------------>
<div class="modal" id="modal-province" data-open="false" role="dialog" aria-modal="true" aria-labelledby="province-title">
  <div class="modal__scrim" data-modal-close></div>
  <div class="modal__panel">
    <div class="modal__head">
      <div>
        <h2 id="province-title">Contact a Province Guide Right Director</h2>
        <p class="small muted" style="margin:0;">Province directors know which chapters near you are chartering next.</p>
      </div>
      <button class="modal__close" type="button" data-modal-close aria-label="Close">&times;</button>
    </div>
    <p class="form-status" id="province-status" hidden></p>
    <form class="form-grid" id="province-form">
      <div class="field"><label for="province-select">Province</label>
        <select id="province-select" name="province" required>
          <option value="">Select your province</option>
          <option>Eastern</option><option>Middle Eastern</option><option>Southern</option>
          <option>Southeastern</option><option>East Central</option><option>Great Lakes</option>
          <option>North Central</option><option>Northern</option><option>Southwestern</option>
          <option>Western</option>
        </select>
      </div>
      <div class="form-grid form-grid--2">
        <div class="field"><label for="province-name">Your name</label><input id="province-name" name="name" required></div>
        <div class="field"><label for="province-email">Email</label><input id="province-email" name="email" type="email" required></div>
      </div>
      <div class="field"><label for="province-msg">Your question</label><textarea id="province-msg" name="message" rows="4" required></textarea></div>
      <p class="form-note">Province list is the standard fraternity province structure. Confirm current province names and routing addresses before launch.</p>
      <button class="btn btn--primary btn--block" type="submit">Send message</button>
    </form>
  </div>
</div>
"""


# --------------------------------------------------------------------------- pages


def build_index():
    body = f"""
<section class="hero">
  <div class="shell hero__grid">
    <div>
      <p class="eyebrow">Youth Leadership &amp; Development</p>
      <h1>Training the leaders of tomorrow, starting today.</h1>
      <p class="lede">The official youth mentorship initiative of Kappa Alpha Psi Fraternity, Inc. Equipping young men in grades 6 through 12 with academic excellence, college preparation, financial literacy and character development.</p>
      <div class="btn-row hero__actions">
        <a class="btn btn--primary" href="locator.html">Find a Kappa League program &rarr;</a>
        <a class="btn btn--outline" href="donate.html">Support our youth</a>
      </div>
      <p class="small muted" style="margin-top:1.25rem;">Programs operate in chapters nationwide. Every adult volunteer completes background screening and youth-protection training.</p>
    </div>
    <div class="photo-grid">
      {photo_real("kappa-league-temple",
                  "A Kappa League cohort and their chapter advisors gathered outside the Temple University campus entrance during a college visit.",
                  widths=(640, 960), ratio=(960, 635), eager=True,
                  sizes="(min-width: 940px) 44vw, 92vw")}
      {photo_real("mentorship-monthly-session",
                  "Chapter mentors standing shoulder to shoulder with Kappa Leaguers, collection bags and grabbers in hand, at a monthly session service project.",
                  widths=(640, 1170), ratio=(1170, 848))}
      {photo_real("college-tour",
                  "Kappa Leaguers in crimson and cream cardigans walking together across a college campus during a group visit.")}
    </div>
  </div>
</section>

<section class="trust">
  <div class="shell trust__inner">
    <div class="trust__item"><p class="trust__figure">{verify("10,000+")}</p><p class="trust__label">Mentees mentored</p></div>
    <div class="trust__item"><p class="trust__figure">{verify("100%")}</p><p class="trust__label">Graduation rate</p></div>
    <div class="trust__item"><p class="trust__figure">{verify("$1M+")}</p><p class="trust__label">Scholarships awarded</p></div>
    <div class="trust__item"><p class="trust__figure">{verify("100+ Years")}</p><p class="trust__label">Of Guide Right legacy</p></div>
  </div>
</section>

<section class="section--tight" style="background:var(--surface-2);">
  <div class="shell">
    <p class="notice"><strong>Build note.</strong> Figures in the stripe above carry a <span class="verify">verify</span> marker because they are unconfirmed. Replace each with a documented number sourced from Commission reporting, or remove the tile. Search the codebase for <code>class="verify"</code> to find every instance.</p>
  </div>
</section>

{guide_right_section()}

{video_section()}

{legacy_section()}

<section class="section">
  <div class="shell">
    <div class="center" style="margin-bottom:2.5rem;">
      <p class="eyebrow--plain eyebrow">The Curriculum</p>
      <h2>The 7 Phases of youth development</h2>
      <p class="lede measure">A national curriculum built to develop every part of a young man's potential, delivered locally by trained chapter mentors.</p>
    </div>
    <div class="grid grid--3 grid--phases">
      {phase_cards()}
    </div>
    <div class="btn-row" style="margin-top:2rem;justify-content:center;">
      <a class="btn btn--ghost" href="seven-phases.html">See what each phase covers</a>
    </div>
  </div>
</section>

{locator_block()}

<section class="section section--surface">
  <div class="shell split">
    <div>
      <p class="eyebrow--plain eyebrow">For Parents &amp; Students</p>
      <h2>Empowering your son's path to higher achievement</h2>
      <p class="lede">Four steps from first search to a matched mentor. Chapters run on a school-year calendar, and most accept students at the start of each term.</p>
      <div class="btn-row" style="margin-top:1.5rem;">
        <a class="btn btn--primary" href="parents.html">Parent and student guide</a>
        <a class="btn btn--outline" href="parents.html#handbook">Download the parent handbook</a>
      </div>
    </div>
    <div class="steps" style="grid-template-columns:1fr;">
      <div class="step"><span class="step__n">1</span><h4>Search your local chapter</h4><p>Use the locator to confirm an active League, meeting schedule and grade band.</p></div>
      <div class="step"><span class="step__n">2</span><h4>Attend orientation</h4><p>Meet the Guide Right Chairman and mentors. Bring your son. Ask everything.</p></div>
      <div class="step"><span class="step__n">3</span><h4>Complete the application</h4><p>Enrollment forms, media release and emergency contacts, submitted to the chapter.</p></div>
      <div class="step"><span class="step__n">4</span><h4>Mentor matching</h4><p>Your son is paired with a screened mentor and begins Phase I with his cohort.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="grid grid--2">
      <article class="card card--crimson">
        <p class="card__num">For Donors &amp; Corporate Sponsors</p>
        <h3>Invest in community impact and future leaders</h3>
        <p>Contributions fund scholarships, Kamp Kappa travel grants and STEM kits. Every gift is reported by category so sponsors can see where support lands.</p>
        <ul class="list-check">
          <li>Community Supporter, Scholarship Sponsor and National Corporate Partner tiers</li>
          <li>Category-level reporting on scholarships, travel and program supplies</li>
          <li>Tax-deductible under the fraternity's 501(c)(3) foundation</li>
        </ul>
        <div class="btn-row" style="margin-top:1rem;">
          <a class="btn btn--gold" href="donate.html">Give today</a>
          <a class="btn btn--ghost" href="donate.html#tiers">See sponsorship tiers</a>
        </div>
      </article>

      <article class="card card--crimson">
        <p class="card__num">For Chapter Officers &amp; Mentors</p>
        <h3>Guide Right officer and chairman resources</h3>
        <p>Certification, compliance and reporting in one place, so chapter leaders spend their time with the young men and not the paperwork.</p>
        <ul class="list-check">
          <li>National certification system for Guide Right chairmen and mentors</li>
          <li>Risk management and background screening compliance</li>
          <li>Activity reporting and annual program submission</li>
        </ul>
        <div class="btn-row" style="margin-top:1rem;">
          <a class="btn btn--primary" href="chapters.html">Open officer resources</a>
        </div>
      </article>
    </div>
  </div>
</section>

<section class="section section--ink">
  <div class="shell split">
    <div>
      <p class="eyebrow--plain eyebrow">Kamp Kappa &amp; STEM</p>
      <h2>Summer programming that changes what a young man believes is possible</h2>
      <p class="lede">Kamp Kappa combines outdoor leadership with hands-on STEM instruction. Chapters send cohorts on travel grants funded by donors and sponsors.</p>
      <div class="btn-row" style="margin-top:1.5rem;">
        <a class="btn btn--gold" href="kamp-kappa.html">Explore Kamp Kappa</a>
      </div>
    </div>
    <div class="photo-grid">
      {photo("Kamp Kappa", "Leaguers at summer camp. 1600&times;900.", "photo--wide")}
    </div>
  </div>
</section>
"""
    return page("index.html",
                "Youth Leadership and Development",
                "The National Guide Right Commission is the youth mentorship initiative of Kappa Alpha Psi Fraternity, Inc., serving young men in grades 6 through 12 through Kappa League.",
                body, LOCATOR_HEAD, LOCATOR_SCRIPTS)


def build_locator():
    body = pagehead(
        "Find a Kappa League program",
        "Search active programs by ZIP code or city. Each result shows meeting schedule, grade bands, application status and a direct line to the chapter Guide Right Chairman.",
        "Find a Kappa League",
    ) + locator_block(heading=False) + f"""
<section class="section section--surface">
  <div class="shell">
    <div class="center" style="margin-bottom:2rem;">
      <h2>No program near you</h2>
      <p class="lede measure">Districts without a chartered League are where the Commission looks first when planning new programs. Both paths below are read by real people.</p>
    </div>
    <div class="grid grid--2">
      <article class="card">
        <h3>Request a Kappa League in your district</h3>
        <p>Tell the Commission which schools and community sites need a program. Requests are matched against nearby chapter capacity and province planning.</p>
        <button class="btn btn--primary" type="button" data-modal-open="modal-start">Submit a request</button>
      </article>
      <article class="card">
        <h3>Contact your Province Guide Right Director</h3>
        <p>Province directors coordinate chapters across a multi-state region and know which programs are chartering next.</p>
        <button class="btn btn--outline" type="button" data-modal-open="modal-province">Contact a director</button>
      </article>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell measure">
    <h2>What to expect after you apply</h2>
    <p>A chapter officer contacts you within the chapter's stated response window to confirm orientation, enrollment forms and the meeting calendar. Kappa League operates on a school-year cycle, so most chapters enroll new Leaguers at the start of a term and hold a rolling interest list in between.</p>
    <p class="notice"><strong>Build note.</strong> Response-time commitments, enrollment windows and any fee information must be confirmed by the Commission before this copy goes live.</p>
  </div>
</section>
"""
    return page("locator.html", "Find a Kappa League",
                "Locate active Kappa League programs by ZIP code or city, view meeting schedules and apply directly to a local chapter.",
                body, LOCATOR_HEAD, LOCATOR_SCRIPTS)


def build_about():
    body = pagehead(
        "About the National Guide Right Commission",
        "Guide Right is the community service and youth mentorship program of Kappa Alpha Psi Fraternity, Inc. The Commission sets national curriculum, certification and reporting standards that every chapter program follows.",
        "About Us",
        [("mission", "Mission"), ("structure", "How it works"), ("leadership", "Leadership"), ("safety", "Youth protection"), ("contact", "Contact")],
    ) + f"""
<section class="section" id="mission">
  <div class="shell split">
    <div>
      <h2>Mission</h2>
      <p>Guide Right exists to place capable, screened, committed men in the lives of young men who need them. The Commission carries that charge nationally: one curriculum, one standard of care, delivered by chapters that know their own communities.</p>
      <p>The Kappa Youth Leadership and Development League, known throughout the fraternity as Kappa League, is the flagship program. It serves young men in grades 6 through 12 across seven phases of development, from self-identity through college and career readiness.</p>
      <p class="notice"><strong>Build note.</strong> Founding dates and historical milestones are intentionally left out of this draft. Supply them from fraternity records and they will be added with citations.</p>
    </div>
    <div class="photo-grid">
      {photo("Program photograph", "Mentors and Leaguers in session. 1600&times;900.", "photo--wide")}
    </div>
  </div>
</section>

<section class="section section--surface" id="structure">
  <div class="shell">
    <h2>How the program works</h2>
    <p class="lede measure">National sets the standard. Provinces coordinate the region. Chapters run the program.</p>
    <div class="grid grid--3" style="margin-top:2rem;">
      <article class="card"><p class="card__num">National</p><h3>The Commission</h3><p>Owns the 7 Phases curriculum, mentor certification, risk management policy and the national reporting calendar. Publishes program materials every chapter works from.</p></article>
      <article class="card"><p class="card__num">Province</p><h3>Province Guide Right Directors</h3><p>Coordinate chapters across a multi-state province, run province-level competition and conference programming, and identify districts that need a new League.</p></article>
      <article class="card"><p class="card__num">Local</p><h3>Chapter Guide Right Chairmen</h3><p>Run the weekly program: recruit and screen mentors, enroll Leaguers, deliver phases, track academics and report activity to the province and the Commission.</p></article>
    </div>
  </div>
</section>

<section class="section" id="leadership">
  <div class="shell">
    <h2>Leadership</h2>
    <p class="lede measure">Commission leadership, province directors and staff contacts.</p>
    <div class="grid grid--3" style="margin-top:2rem;">
      <article class="card card--flat"><p class="card__num">Role</p><h3>National Guide Right Director</h3><p class="muted">Name, photograph and biography to be supplied by the Commission.</p></article>
      <article class="card card--flat"><p class="card__num">Role</p><h3>National Kappa League Chairman</h3><p class="muted">Name, photograph and biography to be supplied by the Commission.</p></article>
      <article class="card card--flat"><p class="card__num">Role</p><h3>Commission Members</h3><p class="muted">Roster to be supplied by the Commission.</p></article>
    </div>
  </div>
</section>

<section class="section section--surface" id="safety">
  <div class="shell split--sidebar split">
    <div>
      <h2>Youth protection and risk management</h2>
      <p>Parents deserve a direct answer about who is in the room with their son. Every adult who works with Kappa League participants completes fraternity background screening and youth-protection training before contact, and chapters follow national risk management policy for meetings, transportation and travel.</p>
      <ul class="list-check">
        <li>Background screening for every mentor and chaperone</li>
        <li>Required youth-protection training, renewed on the national cycle</li>
        <li>Two-adult rule for meetings and travel</li>
        <li>Written parental consent for activities, travel and media use</li>
        <li>Incident reporting through the chapter to the province and Commission</li>
      </ul>
      <p class="notice"><strong>Build note.</strong> Confirm exact screening vendor, training cadence and policy language with Risk Management before publication. Do not paraphrase policy on a public page.</p>
    </div>
    <aside class="card">
      <h3>Questions parents ask</h3>
      <p class="small muted">Who supervises meetings, how travel is handled, what a background check covers, and who to contact with a concern. Answers to be finalized with Risk Management.</p>
      <a class="link-arrow" href="parents.html">Parent and student guide</a>
    </aside>
  </div>
</section>

<section class="section" id="contact">
  <div class="shell">
    <h2>Contact the Commission</h2>
    <div class="grid grid--3" style="margin-top:1.5rem;">
      <article class="card card--flat"><h3>General inquiries</h3><p class="muted">Mailing address, phone and email to be supplied.</p></article>
      <article class="card card--flat"><h3>Media and partnerships</h3><p class="muted">Contact to be supplied.</p></article>
      <article class="card card--flat"><h3>Program and chapter support</h3><p class="muted">Contact to be supplied.</p></article>
    </div>
  </div>
</section>
"""
    return page("about.html", "About Us",
                "The National Guide Right Commission sets the curriculum, certification and safety standards behind every local Kappa League program.",
                body)


def build_kappa_league():
    body = pagehead(
        "Kappa League",
        "The Kappa Youth Leadership and Development League serves young men in grades 6 through 12 with a structured, mentor-led program that runs on the school year.",
        "Kappa League",
        [("who", "Who it serves"), ("year", "The program year"), ("phases", "The 7 Phases"), ("mentors", "Mentors")],
    ) + f"""
<section class="section" id="who">
  <div class="shell split">
    <div>
      <h2>Who Kappa League serves</h2>
      <p>Kappa League is open to young men in grades 6 through 12. Chapters organize participants into two bands so that curriculum meets students where they are.</p>
      <div class="grid grid--2" style="margin-top:1.5rem;">
        <article class="card"><p class="card__num">Junior League</p><h3>Grades 6 through 8</h3><p>Foundations: study habits, personal presentation, character and the first exposure to public speaking and service.</p></article>
        <article class="card"><p class="card__num">Senior League</p><h3>Grades 9 through 12</h3><p>College preparation, financial literacy, competition, campus visits and sustained one-to-one mentorship through application season.</p></article>
      </div>
      <p class="small muted" style="margin-top:1rem;">Not every chapter offers both bands. The locator shows which bands each program runs.</p>
    </div>
    <div class="photo-grid">
      {photo("Junior League", "Grades 6 to 8 in session. 800&times;600.")}
      {photo("Senior League", "Grades 9 to 12 in session. 800&times;600.")}
    </div>
  </div>
</section>

<section class="section section--surface" id="year">
  <div class="shell">
    <h2>The program year</h2>
    <p class="lede measure">Kappa League runs on the school calendar. A typical chapter year looks like this.</p>
    <div class="table-wrap" style="margin-top:1.5rem;">
      <table>
        <thead><tr><th>Term</th><th>Focus</th><th>Typical activity</th></tr></thead>
        <tbody>
          <tr><td>Late summer</td><td>Recruitment and orientation</td><td>Interest meetings, enrollment, mentor matching, parent orientation</td></tr>
          <tr><td>Fall</td><td>Phases I through III</td><td>Study skills, character sessions, public speaking, first service project</td></tr>
          <tr><td>Winter</td><td>Phases IV and V</td><td>Etiquette and cultural programming, health and wellness instruction</td></tr>
          <tr><td>Spring</td><td>Phases VI and VII</td><td>Financial literacy, campus tours, FAFSA and resume workshops, province competition</td></tr>
          <tr><td>Summer</td><td>Kamp Kappa and STEM</td><td>Camp cohorts, STEM instruction, leadership conference travel</td></tr>
        </tbody>
      </table>
    </div>
    <p class="notice" style="margin-top:1.25rem;"><strong>Build note.</strong> This calendar is a structural template. Confirm the national program cycle and any required national events before publishing.</p>
  </div>
</section>

<section class="section" id="phases">
  <div class="shell">
    <h2>The 7 Phases</h2>
    <p class="lede measure">Every chapter delivers the same seven phases. How they deliver them reflects the community they serve.</p>
    <div class="grid grid--3 grid--phases" style="margin-top:2rem;">{phase_cards()}</div>
    <div class="btn-row" style="margin-top:2rem;"><a class="btn btn--ghost" href="seven-phases.html">Full phase detail</a></div>
  </div>
</section>

<section class="section section--ink" id="mentors">
  <div class="shell split">
    <div>
      <h2>The mentors</h2>
      <p class="lede">Kappa League mentors are fraternity members who commit to a full program year. They are screened, trained and accountable to the chapter Guide Right Chairman.</p>
      <ul class="list-check">
        <li>Background screening completed before any contact with participants</li>
        <li>Youth-protection training on the national renewal cycle</li>
        <li>Certification through the national Guide Right system</li>
        <li>A named chairman responsible for every session and every roster</li>
      </ul>
    </div>
    <div class="photo-grid">{photo("Mentors", "Mentor and Leaguer, one to one. 1600&times;900.", "photo--wide")}</div>
  </div>
</section>

<section class="section">
  <div class="shell center">
    <h2>Find the program near you</h2>
    <p class="lede measure">Search active Leagues by ZIP code and see which are accepting applications right now.</p>
    <div class="btn-row" style="justify-content:center;margin-top:1.5rem;">
      <a class="btn btn--primary" href="locator.html">Open the program locator</a>
      <a class="btn btn--outline" href="parents.html">Parent and student guide</a>
    </div>
  </div>
</section>
"""
    return page("kappa-league.html", "Kappa League",
                "Kappa League serves young men in grades 6 through 12 through Junior and Senior bands, seven phases of curriculum and screened chapter mentors.",
                body)


def build_phases():
    detail = {
        "I": ["Personal presentation and grooming standards", "Character, discipline and accountability sessions", "Goal setting and self-assessment", "Chapter creed and program expectations"],
        "II": ["Structured tutoring and homework support", "Study skills and time management", "PSAT, SAT and ACT preparation", "Term-over-term grade tracking with mentor follow-up"],
        "III": ["Public speaking and oratorical competition", "Debate and academic bowl teams", "Province and national competition preparation", "Sportsmanship and team conduct"],
        "IV": ["Formal etiquette and dining instruction", "Fine arts exposure and cultural outings", "Interpersonal and written communication", "Community service with cultural institutions"],
        "V": ["Physical fitness programming", "Mental health awareness with qualified presenters", "Nutrition and personal health literacy", "Age-appropriate decision-making instruction"],
        "VI": ["Budgeting and banking fundamentals", "Credit, saving and investing basics", "Entrepreneurship projects and pitch practice", "Understanding pay, taxes and first employment"],
        "VII": ["College campus tours", "FAFSA and scholarship application assistance", "Resume, essay and interview workshops", "One-to-one mentorship through application season"],
    }
    cards = []
    for num, name, body_text in PHASES:
        items = "".join(f"<li>{i}</li>" for i in detail[num])
        cards.append(f"""
    <article class="card phase" id="phase-{num.lower()}">
      <span class="phase__index" aria-hidden="true">{num}</span>
      <span class="card__num">Phase {num}</span>
      <h3>{name}</h3>
      <p>{body_text}</p>
      <ul class="list-check">{items}</ul>
    </article>""")

    body = pagehead(
        "The 7 Phases of youth development",
        "One national curriculum, delivered locally. Each phase builds on the one before it, and a Leaguer moves through all seven across his years in the program.",
        "7 Phases",
        [(f"phase-{n.lower()}", f"Phase {n}") for n, _, _ in PHASES],
    ) + f"""
<section class="section">
  <div class="shell">
    <div class="grid grid--2 grid--phases">{"".join(cards)}</div>
    <p class="notice" style="margin-top:2rem;"><strong>Build note.</strong> Activity lists under each phase are drafted from the phase descriptions supplied in the project brief. Replace with the exact activity language from the current national curriculum guide before launch.</p>
  </div>
</section>

<section class="section section--surface">
  <div class="shell center">
    <h2>Delivered by trained mentors, close to home</h2>
    <p class="lede measure">The curriculum is national. The men delivering it are from your community.</p>
    <div class="btn-row" style="justify-content:center;margin-top:1.5rem;">
      <a class="btn btn--primary" href="locator.html">Find a Kappa League</a>
      <a class="btn btn--outline" href="chapters.html">Officer resources</a>
    </div>
  </div>
</section>
"""
    return page("seven-phases.html", "The 7 Phases",
                "The seven phases of the Kappa League curriculum, from self-identity and academic preparation through economic empowerment and college readiness.",
                body)


def build_kamp():
    body = pagehead(
        "Kamp Kappa and STEM programming",
        "Summer programming that pairs outdoor leadership with hands-on science, technology, engineering and mathematics instruction.",
        "Kamp Kappa &amp; STEM",
        [("kamp", "Kamp Kappa"), ("stem", "STEM"), ("grants", "Travel grants"), ("sponsor", "Sponsor a cohort")],
    ) + f"""
<section class="section" id="kamp">
  <div class="shell split">
    <div>
      <h2>Kamp Kappa</h2>
      <p>Kamp Kappa takes Leaguers out of familiar surroundings and puts them in a setting where leadership is practiced instead of discussed. Cohorts travel with screened chapter mentors and return to their local program with assignments that carry into the fall.</p>
      <ul class="list-check">
        <li>Multi-day residential format with chapter cohorts</li>
        <li>Outdoor leadership, teamwork and problem solving</li>
        <li>Evening character and brotherhood programming</li>
        <li>Chaperone ratios set by national risk management policy</li>
      </ul>
      <p class="notice"><strong>Build note.</strong> Dates, locations, cost, capacity and registration deadlines to be supplied by the Commission.</p>
    </div>
    <div class="photo-grid">{photo("Kamp Kappa", "Camp cohort photograph. 1600&times;900.", "photo--wide")}</div>
  </div>
</section>

<section class="section section--surface" id="stem">
  <div class="shell">
    <h2>STEM instruction</h2>
    <p class="lede measure">STEM programming runs inside the League year and at camp, using kits chapters can deploy without a lab.</p>
    <div class="grid grid--3" style="margin-top:2rem;">
      <article class="card"><h3>Engineering and build challenges</h3><p>Structured design problems with materials chapters can source locally.</p></article>
      <article class="card"><h3>Computing and robotics</h3><p>Introductory programming and robotics kits sized for a two-hour session.</p></article>
      <article class="card"><h3>Career exposure</h3><p>Site visits and speaker sessions with professionals in technical fields.</p></article>
    </div>
    <p class="notice" style="margin-top:1.5rem;"><strong>Build note.</strong> Confirm the current STEM kit vendors, curriculum partners and any grant restrictions before publishing.</p>
  </div>
</section>

<section class="section" id="grants">
  <div class="shell split--sidebar split">
    <div>
      <h2>Travel grants</h2>
      <p>Cost is the most common reason a young man misses camp. Travel grants funded by donors and corporate partners cover transportation and fees for Leaguers whose families cannot absorb them, so a chapter never has to choose which boys go.</p>
      <p>Grants are requested by the chapter Guide Right Chairman and awarded through the Commission.</p>
    </div>
    <aside class="card">
      <h3>Request a travel grant</h3>
      <p class="small muted">Chapter officers submit grant requests through the officer portal. Application window and award criteria to be supplied.</p>
      <a class="link-arrow" href="chapters.html">Officer resources</a>
    </aside>
  </div>
</section>

<section class="section section--ink" id="sponsor">
  <div class="shell center">
    <h2>Sponsor a cohort</h2>
    <p class="lede measure">Corporate partners fund camp cohorts, STEM kits and travel outright, and receive category-level reporting on how the support was used.</p>
    <div class="btn-row" style="justify-content:center;margin-top:1.5rem;">
      <a class="btn btn--gold" href="donate.html#tiers">See sponsorship tiers</a>
    </div>
  </div>
</section>
"""
    return page("kamp-kappa.html", "Kamp Kappa &amp; STEM",
                "Kamp Kappa pairs outdoor leadership with hands-on STEM instruction, supported by donor-funded travel grants for Kappa League participants.",
                body)


def build_news():
    def entry(kind, title, summary):
        return f"""<article class="card">
      <p class="card__num">{kind} &middot; Sample entry</p>
      <h3>{title}</h3>
      <p>{summary}</p>
      <p class="small muted">Placeholder record. Replace with a published item, date and author before launch.</p>
    </article>"""

    body = pagehead(
        "News and impact",
        "Program news, chapter recognition and the reporting behind the Commission's numbers.",
        "News &amp; Impact",
        [("news", "Latest"), ("impact", "Impact reporting"), ("stories", "Chapter stories")],
    ) + f"""
<section class="section" id="news">
  <div class="shell">
    <div class="sample-banner">
      <strong>Sample entries.</strong>
      <span>Every item on this page is a layout placeholder. No news item, date, quotation or figure here is real.</span>
    </div>
    <div class="grid grid--3">
      {entry("Program", "National Kappa League Conference recap", "Placeholder summary describing competition results, workshop tracks and participating provinces.")}
      {entry("Chapter", "Chapter recognized for Guide Right programming", "Placeholder summary describing a chapter award, the program behind it and the officers involved.")}
      {entry("Scholarship", "Scholarship recipients announced", "Placeholder summary describing award recipients, institutions and the selection process.")}
    </div>
  </div>
</section>

<section class="section section--surface" id="impact">
  <div class="shell">
    <h2>Impact reporting</h2>
    <p class="lede measure">Numbers on this site should trace to a document. This page is where that reporting lives.</p>
    <div class="stat-line" style="margin-top:2rem;">
      <div class="stat-line__item"><p class="stat-line__fig">{verify("&mdash;")}</p><p class="stat-line__lbl">Leaguers enrolled, current program year</p></div>
      <div class="stat-line__item"><p class="stat-line__fig">{verify("&mdash;")}</p><p class="stat-line__lbl">Chapters operating an active League</p></div>
      <div class="stat-line__item"><p class="stat-line__fig">{verify("&mdash;")}</p><p class="stat-line__lbl">Scholarship dollars awarded</p></div>
    </div>
    <p class="notice" style="margin-top:2rem;"><strong>Build note.</strong> Publish the annual report or program summary these figures come from and link it here. A number without a source does not belong on a donor-facing page.</p>
  </div>
</section>

<section class="section" id="stories">
  <div class="shell split">
    <div>
      <h2>Chapter stories</h2>
      <p>Long-form features on chapters, mentors and Leaguers. Photography and quotations require signed media releases from participants and guardians before publication.</p>
      <a class="link-arrow" href="chapters.html">Media release forms for officers</a>
    </div>
    <div class="photo-grid">
      {photo("Feature photograph", "Chapter story lead image. 1600&times;900.", "photo--wide")}
      {photo("Portrait", "Mentor portrait. 800&times;600.")}
      {photo("Program", "Session photograph. 800&times;600.")}
    </div>
  </div>
</section>
"""
    return page("news.html", "News &amp; Impact",
                "Program news, chapter recognition and the impact reporting behind National Guide Right Commission figures.",
                body)


def build_parents():
    body = pagehead(
        "For parents and students",
        "What Kappa League asks of your son, what it gives back, and exactly how to enroll him.",
        "Parents &amp; Students",
        [("steps", "How to enroll"), ("expect", "What to expect"), ("safety", "Safety"), ("faq", "Questions"), ("handbook", "Handbook")],
    ) + f"""
<section class="section" id="steps">
  <div class="shell">
    <h2>Empowering your son's path to higher achievement</h2>
    <p class="lede measure">Four steps, start to finish.</p>
    <div class="steps" style="margin-top:2rem;">
      <div class="step"><span class="step__n">1</span><h4>Search your local chapter</h4><p>Confirm an active League, meeting schedule and whether the chapter runs your son's grade band.</p></div>
      <div class="step"><span class="step__n">2</span><h4>Attend orientation</h4><p>Meet the Guide Right Chairman and the mentors. Bring your son and ask everything.</p></div>
      <div class="step"><span class="step__n">3</span><h4>Complete the application</h4><p>Enrollment forms, emergency contacts, medical information and media release.</p></div>
      <div class="step"><span class="step__n">4</span><h4>Mentor matching</h4><p>Your son is paired with a screened mentor and starts Phase I with his cohort.</p></div>
    </div>
    <div class="btn-row" style="margin-top:2rem;">
      <a class="btn btn--primary" href="locator.html">Find your chapter</a>
    </div>
  </div>
</section>

<section class="section section--surface" id="expect">
  <div class="shell split">
    <div>
      <h2>What the program asks</h2>
      <ul class="list-check">
        <li>Consistent attendance at chapter meetings, usually two Saturdays each month</li>
        <li>Participation in service projects and at least one competition or presentation</li>
        <li>Grade reporting each term so mentors can support academics early</li>
        <li>A parent or guardian reachable for every session and every trip</li>
      </ul>
    </div>
    <div>
      <h2>What your son gets</h2>
      <ul class="list-check">
        <li>A screened, trained mentor who knows his name and his goals</li>
        <li>Structured academic support and college entrance preparation</li>
        <li>Financial literacy instruction with real budgeting practice</li>
        <li>Campus visits, FAFSA help and resume and interview coaching</li>
        <li>A cohort of young men held to the same standard</li>
      </ul>
    </div>
  </div>
</section>

<section class="section" id="safety">
  <div class="shell split--sidebar split">
    <div>
      <h2>Safety and supervision</h2>
      <p>Every adult who works with Kappa League participants completes fraternity background screening and youth-protection training before any contact. Chapters follow national risk management policy for meeting supervision, transportation and travel, and a named chairman is accountable for every session.</p>
      <p>Concerns go to the chapter Guide Right Chairman first and escalate to the Province Guide Right Director and the Commission.</p>
      <p class="notice"><strong>Build note.</strong> Confirm screening, training and escalation language with Risk Management. This section is parent-facing and must match policy exactly.</p>
    </div>
    <aside class="card">
      <h3>Report a concern</h3>
      <p class="small muted">Escalation contacts and reporting procedure to be supplied by the Commission.</p>
    </aside>
  </div>
</section>

<section class="section section--surface" id="faq">
  <div class="shell">
    <h2>Questions parents ask</h2>
    <div class="grid grid--2" style="margin-top:1.5rem;">
      <article class="card card--flat"><h3>Does it cost anything?</h3><p class="muted">Fee structure varies by chapter. Answer to be supplied by the Commission, with the assistance policy stated plainly.</p></article>
      <article class="card card--flat"><h3>Does my son have to be connected to the fraternity?</h3><p class="muted">Kappa League is a community program. Eligibility language to be confirmed by the Commission.</p></article>
      <article class="card card--flat"><h3>How much time does it take?</h3><p class="muted">Most chapters meet two Saturdays a month during the school year, with occasional service projects and trips.</p></article>
      <article class="card card--flat"><h3>Can he join mid-year?</h3><p class="muted">Many chapters keep an interest list between enrollment windows. The locator shows which programs are open now.</p></article>
    </div>
  </div>
</section>

<section class="section" id="handbook">
  <div class="shell split--sidebar split">
    <div>
      <h2>Parent handbook</h2>
      <p>The handbook covers program expectations, the meeting calendar, safety policy, media release terms and chapter contacts in one document parents can keep.</p>
      <p class="notice"><strong>Build note.</strong> Place the approved PDF at <code>assets/docs/parent-handbook.pdf</code> and point the button below at it. The link is disabled until that file exists.</p>
    </div>
    <aside class="card">
      <h3>Download</h3>
      <p class="small muted">Parent Handbook, PDF. Pending Commission approval.</p>
      <a class="btn btn--outline" href="#handbook" aria-disabled="true">Handbook not yet published</a>
    </aside>
  </div>
</section>
"""
    return page("parents.html", "For Parents &amp; Students",
                "How to enroll a student in Kappa League, what the program asks, how supervision and safety work, and where to find your local chapter.",
                body)


def build_donate():
    body = pagehead(
        "Support the National Guide Right Commission",
        "Contributions fund scholarships, Kamp Kappa travel grants and STEM programming for young men in chapters nationwide.",
        "Donate",
        [("give", "Give"), ("tiers", "Sponsorship tiers"), ("allocation", "Where gifts go"), ("transparency", "501(c)(3) info")],
    ) + f"""
<section class="section" id="give">
  <div class="shell split">
    <div>
      <h2>Invest in community impact and future leaders</h2>
      <p class="lede">A gift to Guide Right pays for a specific thing: a scholarship, a seat at camp, a STEM kit in a chapter that could not otherwise buy one.</p>
      <p class="notice"><strong>Build note.</strong> The payment form below is a layout placeholder. Connect Stripe or PayPal through the fraternity's 501(c)(3) foundation account, and confirm receipting and acknowledgment language with the foundation before enabling it.</p>
    </div>
    <aside class="card card--crimson">
      <h3>Make a gift</h3>
      <div class="btn-row" style="margin-block:.5rem;">
        <button class="btn btn--outline btn--sm" type="button">$50</button>
        <button class="btn btn--outline btn--sm" type="button">$100</button>
        <button class="btn btn--outline btn--sm" type="button">$250</button>
        <button class="btn btn--outline btn--sm" type="button">$500</button>
      </div>
      <div class="field"><label for="gift-other">Other amount</label><input id="gift-other" inputmode="decimal" placeholder="$"></div>
      <div class="field"><label for="gift-design">Designate my gift</label>
        <select id="gift-design">
          <option>Where it is needed most</option>
          <option>Scholarships</option>
          <option>Kamp Kappa travel grants</option>
          <option>STEM kits and program supplies</option>
        </select>
      </div>
      <button class="btn btn--gold btn--block" type="button">Continue to secure checkout</button>
      <p class="form-note">Payment processing not yet connected in this build.</p>
    </aside>
  </div>
</section>

<section class="section section--surface" id="tiers">
  <div class="shell">
    <h2>Sponsorship tiers</h2>
    <p class="lede measure">Recognition benefits at each level to be confirmed by the Commission.</p>
    <div class="grid grid--3" style="margin-top:2rem;">
      <article class="tier">
        <p class="card__num">Tier One</p>
        <h3>Community Supporter</h3>
        <p class="tier__amt">Amount to be set</p>
        <ul><li>Supports program supplies and meeting costs</li><li>Recognition on the annual supporter listing</li><li>Annual impact summary</li></ul>
      </article>
      <article class="tier tier--feature">
        <p class="card__num">Tier Two</p>
        <h3>Scholarship Sponsor</h3>
        <p class="tier__amt">Amount to be set</p>
        <ul><li>Funds a named scholarship or camp cohort</li><li>Recognition at national program events</li><li>Category-level reporting on the gift</li></ul>
      </article>
      <article class="tier">
        <p class="card__num">Tier Three</p>
        <h3>National Corporate Partner</h3>
        <p class="tier__amt">Amount to be set</p>
        <ul><li>Multi-year commitment across provinces</li><li>Employee volunteer and speaker pathways</li><li>Partnership reporting and named recognition</li></ul>
      </article>
    </div>
  </div>
</section>

<section class="section" id="allocation">
  <div class="shell">
    <h2>Where gifts go</h2>
    <div class="grid grid--3" style="margin-top:1.5rem;">
      <article class="card"><h3>Scholarships</h3><p>Direct awards to graduating Leaguers, paid to the institution.</p></article>
      <article class="card"><h3>Kamp Kappa travel grants</h3><p>Transportation and fees so cost does not decide who attends.</p></article>
      <article class="card"><h3>STEM kits and supplies</h3><p>Materials chapters use to run technical sessions without a lab.</p></article>
    </div>
    <p class="notice" style="margin-top:2rem;"><strong>Build note.</strong> Publish actual allocation percentages only when they come from audited or board-approved figures. Until then this page shows categories and no percentages.</p>
  </div>
</section>

<section class="section section--surface" id="transparency">
  <div class="shell measure">
    <h2>Tax-deductible giving</h2>
    <p>Gifts are processed through the fraternity's 501(c)(3) foundation. Donors receive a written acknowledgment for tax purposes.</p>
    <p class="notice"><strong>Build note.</strong> Insert the exact legal entity name, EIN, mailing address, and links to the current Form 990 and financial statements. Do not publish deductibility language that has not been reviewed.</p>
  </div>
</section>
"""
    return page("donate.html", "Donate",
                "Support Kappa League with a gift that funds scholarships, Kamp Kappa travel grants and STEM programming through the fraternity's 501(c)(3) foundation.",
                body)


def build_chapters():
    body = pagehead(
        "Guide Right officer and chairman resources",
        "Certification, compliance and reporting for chapter Guide Right Chairmen, Kappa League advisors and province directors.",
        "Chapter Officers",
        [("portal", "Portal"), ("certification", "Certification"), ("compliance", "Compliance"), ("reporting", "Reporting"), ("materials", "Materials")],
    ) + """
<section class="section" id="portal">
  <div class="shell split--sidebar split">
    <div>
      <h2>Chapter portal</h2>
      <p>Officer tools sit behind fraternity credentials. The portal is where chairmen manage rosters, submit activity reports, request travel grants and confirm mentor compliance status.</p>
      <p class="notice"><strong>Build note.</strong> Point the login button at the fraternity's existing single sign-on. Do not build a separate credential store for this site.</p>
    </div>
    <aside class="card card--crimson">
      <h3>Officer login</h3>
      <p class="small muted">Fraternity credentials required.</p>
      <a class="btn btn--primary btn--block" href="#portal">Sign in to the chapter portal</a>
      <p class="form-note">Single sign-on not yet connected in this build.</p>
    </aside>
  </div>
</section>

<section class="section section--surface" id="certification">
  <div class="shell">
    <h2>National certification</h2>
    <div class="grid grid--3" style="margin-top:1.5rem;">
      <article class="card"><p class="card__num">Step 1</p><h3>Chairman certification</h3><p>Required for every chapter Guide Right Chairman before the program year opens.</p></article>
      <article class="card"><p class="card__num">Step 2</p><h3>Mentor certification</h3><p>Required for every adult who works directly with Leaguers.</p></article>
      <article class="card"><p class="card__num">Step 3</p><h3>Annual renewal</h3><p>Recertification on the national cycle, tracked at province level.</p></article>
    </div>
    <p class="notice" style="margin-top:1.5rem;"><strong>Build note.</strong> Link each step to the live certification system and state the current renewal cadence.</p>
  </div>
</section>

<section class="section" id="compliance">
  <div class="shell split">
    <div>
      <h2>Risk management and background compliance</h2>
      <ul class="list-check">
        <li>Background screening submitted and cleared before mentor contact</li>
        <li>Youth-protection training current for every adult on the roster</li>
        <li>Two-adult rule enforced for meetings, transportation and travel</li>
        <li>Signed parental consent and media release on file for each participant</li>
        <li>Incident reporting routed to province and Commission</li>
      </ul>
      <p class="notice"><strong>Build note.</strong> Confirm every line against current national risk management policy. Officer-facing compliance language must not paraphrase.</p>
    </div>
    <div>
      <h2>Activity reporting</h2>
      <ul class="list-check">
        <li>Session logs with attendance by Leaguer</li>
        <li>Phase completion tracking across the program year</li>
        <li>Service hours and competition participation</li>
        <li>Annual program report to province and Commission</li>
      </ul>
    </div>
  </div>
</section>

<section class="section section--surface" id="reporting">
  <div class="shell">
    <h2>Reporting calendar</h2>
    <div class="table-wrap" style="margin-top:1.25rem;">
      <table>
        <thead><tr><th>When</th><th>What is due</th><th>Submitted to</th></tr></thead>
        <tbody>
          <tr><td>Before program year opens</td><td>Chairman and mentor certification, screening clearances</td><td>Province</td></tr>
          <tr><td>Each term</td><td>Roster updates and attendance logs</td><td>Province</td></tr>
          <tr><td>Spring</td><td>Travel grant requests for summer programming</td><td>Commission</td></tr>
          <tr><td>End of program year</td><td>Annual Guide Right activity report</td><td>Province and Commission</td></tr>
        </tbody>
      </table>
    </div>
    <p class="notice" style="margin-top:1.25rem;"><strong>Build note.</strong> Replace with the published national reporting calendar and exact due dates.</p>
  </div>
</section>

<section class="section" id="materials">
  <div class="shell">
    <h2>Program materials</h2>
    <div class="grid grid--3" style="margin-top:1.5rem;">
      <article class="card card--flat"><h3>Curriculum guide</h3><p class="muted">7 Phases delivery guide. File to be supplied.</p></article>
      <article class="card card--flat"><h3>Enrollment and consent forms</h3><p class="muted">Application, medical, consent and media release. Files to be supplied.</p></article>
      <article class="card card--flat"><h3>Operations and mentorship guide</h3><p class="muted">Chapter operations manual. File to be supplied.</p></article>
    </div>
  </div>
</section>
"""
    return page("chapters.html", "Chapter Officer Resources",
                "Certification, risk management compliance, activity reporting and program materials for Guide Right chairmen and Kappa League mentors.",
                body)


# --------------------------------------------------------------- history page

TIMELINE = [
    ("tl-1922", "1922", "The Idea Is Born"),
    ("tl-1923", "1923", "From Local Idea to National Movement"),
    ("tl-1928", "1928", "The Early Vision"),
    ("tl-1936a", "1936", "An Organized Model of Guidance"),
    ("tl-1936b", "1936", "From a Week to a Year-Round Mission"),
    ("tl-1940", "1940&ndash;1944", "Continued Development"),
    ("tl-1945", "1945&ndash;1952", "Expanding the National Structure"),
    ("tl-1952", "1952", "The Program Defined"),
]


def source_modal(year, title, subtitle):
    """Primary-source panel. The transcription slot stays empty until the real
    handbook text is supplied. Never fill it with reconstructed language."""
    return f"""
<div class="modal" id="modal-{year}" data-open="false" role="dialog" aria-modal="true" aria-labelledby="src-{year}-title">
  <div class="modal__scrim" data-modal-close></div>
  <div class="modal__panel modal__panel--wide">
    <div class="modal__head">
      <div>
        <p class="panel__label">Primary source &mdash; {year}</p>
        <h2 id="src-{year}-title">{title}</h2>
        <p class="small muted" style="margin:0;">{subtitle}</p>
      </div>
      <button class="modal__close" type="button" data-modal-close aria-label="Close">&times;</button>
    </div>

    <div class="modal__grid">
      <figure class="scan" aria-label="Placeholder for a scan of the {year} Kappa Alpha Psi Fraternity handbook page">
        <figcaption><strong>{year} handbook page</strong>
        <p>Drop the scan at <code>assets/img/handbook-{year}.jpg</code> and replace this figure. Alt text should describe the document, not repeat the transcription.</p></figcaption>
      </figure>

      <div>
        <div class="transcript">
          <h3>Full transcription</h3>
          <div class="transcript__pending">
            <strong>Transcription not yet supplied.</strong>
            The verbatim text of the {year} handbook account has not been provided to this build. Paste it here exactly as printed, preserving original spelling, punctuation and terminology. Nothing has been reconstructed or paraphrased in its place.
          </div>
        </div>
        <p class="small muted" style="margin-top:1rem;">Quotations shown on this page are reproduced as supplied by the Commission. The transcription panel is the place for the complete passage, so visitors never have to read text embedded in an image.</p>
      </div>
    </div>
  </div>
</div>
"""


def build_history():
    rail = "".join(
        f'<li><a href="#{i}">{yr} &middot; {t}</a></li>' for i, yr, t in TIMELINE
    )

    body = f"""
<section class="archival archive-hero">
  <div class="shell">
    <p class="crumbs"><a href="index.html">Home</a> &rsaquo; Guide Right History</p>
    <p class="eyebrow">Established 1922</p>
    <h1>More Than a Century of Guiding Young Men</h1>
    <div class="measure">
      <p class="lede">Guide Right represents more than a program. It is a continuing commitment to the development of young men that began in St. Louis, Missouri, in 1922.</p>
      <p>Historical accounts preserved in Kappa Alpha Psi Fraternity handbooks from 1928, 1936, and 1952 provide a unique record of how the movement began, how its methods developed, and how its mission expanded over time.</p>
    </div>
    <nav class="anchor-nav" aria-label="On this page">
      <a href="#question">The founding question</a>
      <a href="#timeline">Timeline</a>
      <a href="#then-now">Then and today</a>
      <a href="#archives">From the archives</a>
      <a href="#sources">About these sources</a>
    </nav>
  </div>
</section>

<!-- The question ---------------------------------------------------------->
<section class="section question" id="question">
  <div class="shell">
    <p class="eyebrow--plain eyebrow" style="color:var(--gold);">The Question That Started a Movement</p>
    <blockquote class="question__quote">&ldquo;How shall I invest my life?&rdquo;</blockquote>
    <p class="question__cite">Recorded in the 1952 historical account</p>
    <div class="measure" style="margin-top:2rem;">
      <p>Early Guide Right leaders recognized that many young men were completing high school without clear vocational direction, and that they often lacked access to experienced men who could provide guidance.</p>
      <p>That question is the reason the movement exists. Everything that follows on this page is an account of how Kappa Alpha Psi organized itself to help young men answer it.</p>
    </div>
  </div>
</section>

<!-- Timeline -------------------------------------------------------------->
<section class="section archival" id="timeline">
  <div class="shell">
    <p class="eyebrow--plain eyebrow">The Record</p>
    <h2>A Timeline of the Guide Right Movement</h2>
    <p class="lede measure">Drawn from the 1928, 1936, and 1952 Kappa Alpha Psi Fraternity handbooks. Where the accounts differ, the source is named.</p>

    <div class="tl-wrap" style="margin-top:2.5rem;">
      <nav class="tl-rail" id="tl-rail" aria-label="Timeline entries">
        <ol>{rail}</ol>
      </nav>

      <ol class="tl">

        <li class="tl__item" id="tl-1922">
          <h3 class="tl__year">1922</h3>
          <p class="tl__title">The Idea Is Born</p>
          <div class="tl__body">
            <p>Guide Right originated in St. Louis, Missouri, through the St. Louis Alumni Chapter of Kappa Alpha Psi Fraternity, Inc.</p>
            <p>The historical sources identify Leon W. Stewart/Steward, Ben H. Mosby, and Dr. J. Jerome Peters as important figures in the early development and national advancement of Guide Right.</p>
            <p class="notice" style="background:rgba(255,255,255,.7);border-color:var(--cream-line);border-left-color:var(--gold-deep);color:var(--sepia-muted);">
              <strong>A note on spelling.</strong> The historical documents vary between &ldquo;Stewart&rdquo; and &ldquo;Steward.&rdquo; Both forms appear in the record. Direct quotations preserve the spelling used by their original source rather than settling on one form.
            </p>
          </div>
        </li>

        <li class="tl__item" id="tl-1923">
          <h3 class="tl__year">1923</h3>
          <p class="tl__title">From Local Idea to National Movement</p>
          <div class="tl__body">
            <p>Dr. J. Jerome Peters presented the Guide Right concept and its supporting information at the Grand Chapter meeting in Louisville, Kentucky.</p>
            <p>According to the 1936 historical account, the Grand Chapter adopted Guide Right as a national movement and established a commission to carry it forward.</p>
            <div class="stack-note">
              <p class="stack-note__tier">Local vision</p>
              <p class="stack-note__name">St. Louis Alumni Chapter</p>
              <p class="stack-note__arrow" aria-hidden="true">&darr;</p>
              <p class="stack-note__tier">National movement</p>
              <p class="stack-note__name">Kappa Alpha Psi</p>
            </div>
          </div>
        </li>

        <li class="tl__item" id="tl-1928">
          <h3 class="tl__year">1928</h3>
          <p class="tl__title">The Early Vision</p>
          <div class="tl__body">
            <p>This early account described Guide Right primarily as a vocational movement, designed to help high school boys identify their place in the occupational world and become useful members of their communities and of the nation.</p>
            <div class="panel">
              <p class="panel__label">Primary source &mdash; 1928</p>
              <p class="panel__source">Kappa Alpha Psi Fraternity Handbook</p>
              <blockquote>
                &ldquo;The purpose of the movement is a vocational one.&rdquo;
                <cite>1928 handbook</cite>
              </blockquote>
              <ul class="keywords">
                <li>Vocational guidance</li>
                <li>Self-analysis</li>
                <li>Mentorship</li>
                <li>Education</li>
                <li>Citizenship</li>
                <li>Community usefulness</li>
              </ul>
              <div class="btn-row" style="margin-top:1.25rem;">
                <button class="btn btn--ghost btn--sm" type="button" data-modal-open="modal-1928">View 1928 primary source</button>
              </div>
            </div>
          </div>
        </li>

        <li class="tl__item" id="tl-1936a">
          <h3 class="tl__year">1936</h3>
          <p class="tl__title">An Organized Model of Guidance</p>
          <div class="tl__body">
            <p>The 1936 account shows an increasingly structured approach. It describes local committees identifying students, recruiting community professionals, conducting vocational conferences, providing individual interviews, maintaining self-discovery information, and continuing assistance when needed.</p>
            <div class="panel">
              <p class="panel__label">Primary source &mdash; 1936</p>
              <p class="panel__source">Kappa Alpha Psi Fraternity Handbook</p>
              <blockquote>
                &ldquo;Help him choose his course, his college or placement&hellip;&rdquo;
                <cite>1936 handbook</cite>
              </blockquote>
              <ol class="flow">
                <li>Identify young men</li>
                <li>Discover interests</li>
                <li>Connect with community mentors</li>
                <li>Explore vocations</li>
                <li>Provide individual counsel</li>
                <li>Assist with education and employment</li>
                <li>Follow up</li>
              </ol>
              <div class="btn-row" style="margin-top:1.25rem;">
                <button class="btn btn--ghost btn--sm" type="button" data-modal-open="modal-1936">View 1936 primary source</button>
              </div>
            </div>
          </div>
        </li>

        <li class="tl__item" id="tl-1936b">
          <h3 class="tl__year">1936</h3>
          <p class="tl__title">From a Week to a Year-Round Mission</p>
          <div class="tl__body">
            <p>The later handbook account describes Guide Right moving beyond a single annual observance. The movement was placed on a year-round basis, while Guide Right Week remained a concentrated observance of the larger program.</p>
            <ol class="flow flow--pair">
              <li>Guide Right Week</li>
              <li>365 days of guidance</li>
              <li>Year-round youth development</li>
            </ol>
            <p class="notice" style="margin-top:1.25rem;background:rgba(255,255,255,.7);border-color:var(--cream-line);border-left-color:var(--gold-deep);color:var(--sepia-muted);">
              <strong>Build note.</strong> The project brief attributes the year-round shift to &ldquo;the later historical account&rdquo; without naming the year. Confirm whether this comes from the 1936 or the 1952 handbook and label the entry accordingly before publication.
            </p>
          </div>
        </li>

        <li class="tl__item" id="tl-1940">
          <h3 class="tl__year">1940&ndash;1944</h3>
          <p class="tl__title">Continued Development</p>
          <div class="tl__body">
            <p>The 1952 account records a succession of leaders and the emphases each brought to the program.</p>
            <ul class="roster">
              <li>
                <span class="roster__yr">1940&ndash;1941</span>
                <p>R. J. Reynolds led further program development, including inspirational materials, vocational survey efforts, Guide Right breakfasts, and student employment efforts.</p>
              </li>
              <li>
                <span class="roster__yr">1942</span>
                <p>C. Rodger Wilson emphasized community needs, conferences, symposia, and speakers.</p>
              </li>
              <li>
                <span class="roster__yr">1943</span>
                <p>G. Smith Hawkins emphasized early contacts and guidance in the home.</p>
              </li>
              <li>
                <span class="roster__yr">1944</span>
                <p>James E. Anderson emphasized the importance and objectives of Guide Right through a published bulletin.</p>
              </li>
            </ul>
          </div>
        </li>

        <li class="tl__item" id="tl-1945">
          <h3 class="tl__year">1945&ndash;1952</h3>
          <p class="tl__title">Expanding the National Structure</p>
          <div class="tl__body">
            <p>Under Elbert W. Strothers, the movement expanded its objectives and developed full-time guidance programs, clinics, supervised year-round projects, Guide Right workbooks, self-analysis materials, counselee history outlines, and Provincial Area Guide Right Directors.</p>
            <div class="stack-note">
              <p class="stack-note__tier">National program</p>
              <p class="stack-note__arrow" aria-hidden="true">&updownarrow;</p>
              <p class="stack-note__tier">Provincial leadership</p>
              <p class="stack-note__arrow" aria-hidden="true">&updownarrow;</p>
              <p class="stack-note__tier">Local chapters</p>
            </div>
          </div>
        </li>

        <li class="tl__item" id="tl-1952">
          <h3 class="tl__year">1952</h3>
          <p class="tl__title">The Program Defined</p>
          <div class="tl__body">
            <p>The 1952 handbook offers the most extensive historical snapshot of the program, setting out its purpose and objectives in full.</p>
            <div class="panel">
              <p class="panel__label">Primary source &mdash; 1952</p>
              <p class="panel__source">Kappa Alpha Psi Fraternity Handbook</p>
              <h4 style="margin-bottom:.35rem;">Historical 1952 objectives</h4>
              <p class="small" style="color:var(--sepia-muted);margin-bottom:.5rem;">These are the objectives as documented in 1952. They are presented as a historical record, not as the current objectives of the Commission.</p>
              <ol class="objectives">
                <li>Help youth select educational courses leading toward appropriate vocations.</li>
                <li>Encourage cooperative attitudes in the home and community.</li>
                <li>Assist students during training, employment entry, and advancement.</li>
                <li>Help boys facing serious emotional and social difficulties.</li>
                <li>Assist parents in helping their children.</li>
                <li>Provide constructive experiences and activities for less fortunate youth.</li>
                <li>Provide fellowship and wholesome recreation through organized groups and clubs.</li>
              </ol>
              <div class="btn-row" style="margin-top:1.25rem;">
                <button class="btn btn--ghost btn--sm" type="button" data-modal-open="modal-1952">View 1952 primary source</button>
              </div>
            </div>
          </div>
        </li>

      </ol>
    </div>
  </div>
</section>

<!-- Then and today -------------------------------------------------------->
<section class="section" id="then-now">
  <div class="shell">
    <p class="eyebrow--plain eyebrow">From Then to Today</p>
    <h2>The Mission Endures</h2>
    <p class="lede measure">The methods have evolved. The commitment remains.</p>
    <p class="measure" style="margin-top:1.25rem;">Across generations, many of the themes found in Guide Right&rsquo;s earliest documents remain visible in its continuing commitment to youth development.</p>

    <div class="compare">
      <div class="compare__col">
        <p class="compare__head">Historical Guide Right</p>
        <ul>
          <li>Vocational guidance</li>
          <li>Self-analysis</li>
          <li>Educational planning</li>
          <li>Community mentorship</li>
          <li>Employment assistance</li>
          <li>Scholarship support</li>
          <li>Constructive recreation</li>
          <li>Citizenship</li>
        </ul>
      </div>
      <div class="compare__col compare__col--now">
        <p class="compare__head">Modern Guide Right</p>
        <ul>
          <li>Phase I &middot; Self-Identity &amp; Purpose</li>
          <li>Phase II &middot; Training &amp; Academic Preparation</li>
          <li>Phase III &middot; Competition &amp; Preparedness</li>
          <li>Phase IV &middot; Social &amp; Cultural Awareness</li>
          <li>Phase V &middot; Health &amp; Wellness Education</li>
          <li>Phase VI &middot; Economic Empowerment</li>
          <li>Phase VII &middot; College &amp; Career Readiness</li>
        </ul>
      </div>
    </div>
    <p class="small muted" style="margin-top:1.25rem;max-width:70ch;">The two columns are placed side by side as themes, not as a mapping. No modern phase is presented here as the direct successor of a specific historical objective, because the sources do not document such a correspondence.</p>
  </div>
</section>

<!-- Enduring question ----------------------------------------------------->
<section class="section enduring">
  <div class="shell">
    <div class="enduring__grid">
      <div>
        <p class="enduring__mark">1922</p>
        <blockquote class="enduring__quote">&ldquo;How shall I invest my life?&rdquo;</blockquote>
      </div>
      <div>
        <p class="enduring__mark">Today</p>
        <p class="lede" style="color:#F5E6E5;">More than a century later, Guide Right continues helping young men explore that question through mentorship, education, leadership, service, career preparation, and personal development.</p>
      </div>
    </div>
    <p class="enduring__close">The methods have evolved.<br>The responsibility endures.</p>
    <div class="btn-row">
      <a class="btn btn--gold" href="seven-phases.html">Discover Guide Right today &rarr;</a>
    </div>
  </div>
</section>

<!-- Archives -------------------------------------------------------------->
<section class="section archival" id="archives">
  <div class="shell">
    <p class="eyebrow--plain eyebrow">From the Archives</p>
    <h2>The Handbooks</h2>
    <p class="lede measure">Three Kappa Alpha Psi Fraternity handbooks carry the documentary record of Guide Right&rsquo;s first three decades.</p>

    <div class="archive-grid">
      <article class="archive-card">
        <p class="archive-card__year">1928</p>
        <h3 class="archive-card__title">The Guide Right Movement</h3>
        <p class="archive-card__sub">Kappa Alpha Psi Fraternity Handbook</p>
        <span class="archive-card__flag">Primary source</span>
        <div class="archive-card__actions">
          <button class="btn btn--primary btn--sm" type="button" data-modal-open="modal-1928">View original</button>
          <button class="btn btn--outline btn--sm" type="button" data-modal-open="modal-1928">Read transcription</button>
        </div>
      </article>

      <article class="archive-card">
        <p class="archive-card__year">1936</p>
        <h3 class="archive-card__title">The Guide Right Movement</h3>
        <p class="archive-card__sub">Kappa Alpha Psi Fraternity Handbook</p>
        <span class="archive-card__flag">Primary source</span>
        <div class="archive-card__actions">
          <button class="btn btn--primary btn--sm" type="button" data-modal-open="modal-1936">View original</button>
          <button class="btn btn--outline btn--sm" type="button" data-modal-open="modal-1936">Read transcription</button>
        </div>
      </article>

      <article class="archive-card">
        <p class="archive-card__year">1952</p>
        <h3 class="archive-card__title">The Program Defined</h3>
        <p class="archive-card__sub">Its evolution and development &middot; Purpose and objectives<br>Kappa Alpha Psi Fraternity Handbook</p>
        <span class="archive-card__flag">Primary source</span>
        <div class="archive-card__actions">
          <button class="btn btn--primary btn--sm" type="button" data-modal-open="modal-1952">View original</button>
          <button class="btn btn--outline btn--sm" type="button" data-modal-open="modal-1952">Read transcription</button>
        </div>
      </article>
    </div>

    <p class="notice" style="margin-top:2rem;background:rgba(255,255,255,.7);border-color:var(--cream-line);border-left-color:var(--gold-deep);color:var(--sepia-muted);">
      <strong>Build note.</strong> The three panels open with empty transcription slots and placeholder scan frames on purpose. Supply the handbook scans and the verbatim transcriptions; nothing has been reconstructed to fill the gap.
    </p>
  </div>
</section>

<!-- Source note ----------------------------------------------------------->
<section class="section--tight archival" id="sources" style="border-top:0;">
  <div class="shell">
    <div class="source-note measure">
      <h2>About These Sources</h2>
      <p>The history presented here draws upon Kappa Alpha Psi Fraternity handbooks published in 1928, 1936, and 1952. These primary historical documents were produced at different points in Guide Right&rsquo;s development and occasionally vary in detail, terminology, spelling, and emphasis. Historical quotations and source material are presented within their original context.</p>
      <p>Where the accounts differ, this page names the source rather than reconciling them into a single version.</p>
    </div>
  </div>
</section>

{source_modal("1928", "The Guide Right Movement", "Kappa Alpha Psi Fraternity Handbook")}
{source_modal("1936", "The Guide Right Movement", "Kappa Alpha Psi Fraternity Handbook")}
{source_modal("1952", "The Program Defined", "Kappa Alpha Psi Fraternity Handbook")}
"""

    return page(
        "history.html",
        "History of Guide Right",
        "Explore the history of the Guide Right movement from its beginnings in St. Louis in 1922 through more than a century of mentorship, vocational guidance, leadership, education, and youth development.",
        body,
        extra_scripts='<script src="assets/js/history.js"></script>\n',
    )


# --------------------------------------------------------------------------- run

def main():
    built = [
        build_index(),
        build_locator(),
        build_about(),
        build_history(),
        build_kappa_league(),
        build_phases(),
        build_kamp(),
        build_news(),
        build_parents(),
        build_donate(),
        build_chapters(),
    ]
    print("Built %d pages:" % len(built))
    for b in built:
        print("  " + b)


if __name__ == "__main__":
    main()
