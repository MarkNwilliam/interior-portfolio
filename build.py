#!/usr/bin/env python3
"""Static site generator for the interior portfolio."""
import os
from html import escape

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://marknwilliam.github.io/interior-portfolio"
SITE = "Nkugwa Mark William"
EMAIL = "hello@nkugwamarkwilliam.com"
X_HANDLE = "MarkNkugwa"

PROJECTS = [
    {
        "slug": "oak-and-light",
        "title": "Oak &amp; Light",
        "plain": "Oak & Light",
        "category": "3D study · Living",
        "year": "2026",
        "typology": "Living room",
        "area": "21.8 m²",
        "scope": "3D visualisation, spatial planning, lighting",
        "palette": "Oak, linen, cream, sage",
        "img": "oak-and-light",
        "glb": "oak-and-light",
        "widths": [1280, 800],
        "w": 1280, "h": 720,
        "alt": "3D render of a warm living room with a linen sofa, oak coffee table, armchair and floor lamp",
        "intro": "A living room modelled around one clear metre of movement — a linen sofa, an oak table and a chair that can be pulled into the light.",
        "body": [
            "The room is 5.2 by 4.2 metres. The sofa is 2.1 metres long with a 450 mm seat height; the coffee table sits at 400 mm, 450 mm in front of it, so legs can pass without the room feeling like a corridor.",
            "Every clearance is drawn rather than guessed: a 900 mm route around the seating, artwork centred at 1.5 metres, and a window sized above one-eighth of the floor area. The render tests the proportions before materials are committed.",
        ],
        "captions": ["The seating group in warm afternoon light", "Linen, oak and a single brass note"],
        "card": "wide",
    },
    {
        "slug": "quiet-quarters",
        "title": "Quiet Quarters",
        "plain": "Quiet Quarters",
        "category": "3D study · Bedroom",
        "year": "2026",
        "typology": "Bedroom",
        "area": "18.5 m²",
        "scope": "3D visualisation, layout, joinery study",
        "palette": "Oat, linen, oak, brass",
        "img": "quiet-quarters",
        "glb": "quiet-quarters",
        "widths": [1280, 800],
        "w": 1280, "h": 720,
        "alt": "3D render of a calm bedroom with a low bed, slatted oak headboard, nightstands and sliding wardrobe",
        "intro": "A bedroom drawn to rest: a 1.6-metre bed with 600 mm either side, a slatted oak headboard and a wardrobe that disappears into the wall.",
        "body": [
            "At 4.4 by 4.2 metres the room can hold the bed, two 450 mm nightstands and a full-height wardrobe without crowding the route to the window. The mattress sits at 540 mm — low enough to read as calm, high enough to rise from easily.",
            "The headboard is a screen of oak slats; the wardrobe runs the left wall at 600 mm deep. Everything else is left quiet so the morning light has somewhere to land.",
        ],
        "captions": ["Washed linen and a low oak ledge", "Soft light at the edge of the room"],
        "card": "narrow",
    },
    {
        "slug": "warm-kitchen",
        "title": "The Warm Kitchen",
        "plain": "The Warm Kitchen",
        "category": "3D study · Kitchen",
        "year": "2026",
        "typology": "Kitchen",
        "area": "18.2 m²",
        "scope": "3D visualisation, joinery design, lighting",
        "palette": "Oak, cream, charcoal, brass",
        "img": "warm-kitchen",
        "glb": "warm-kitchen",
        "widths": [1280, 800],
        "w": 1280, "h": 720,
        "alt": "3D render of a warm oak kitchen with a stone worktop, island, stools and pendant lights",
        "intro": "A working kitchen modelled around the work triangle — fridge, range and sink within 1.5 to 2.7 metres of one another.",
        "body": [
            "The back run holds 900 mm worktops over 600 mm cabinets, with the fridge, range and sink spaced to keep the work triangle compact. A 2.2-metre island sits behind a 1.1-metre aisle, close enough to pass a plate across.",
            "Pendants hang 750 mm above the island, the height that lights the surface without blocking the view. Oak, cream and blackened steel keep the room warm rather than clinical.",
        ],
        "captions": ["Oak joinery and honed stone", "The working edge, in detail"],
        "card": "half",
    },
    {
        "slug": "reading-nook",
        "title": "Reading Nook",
        "plain": "Reading Nook",
        "category": "3D study · Study",
        "year": "2026",
        "typology": "Study corner",
        "area": "20 m²",
        "scope": "3D visualisation, spatial study",
        "palette": "Linen, sage, oak, brass",
        "img": "reading-nook",
        "glb": "reading-nook",
        "widths": [1280, 800],
        "w": 1280, "h": 720,
        "alt": "3D render of a reading nook with a linen armchair, brass side table and full bookshelf",
        "intro": "A quiet corner modelled at full scale: a 450 mm linen armchair, a brass side table at 545 mm and a wall of books.",
        "body": [
            "This study asks how little a room needs. A chair, a light, a surface for a cup, and enough books to make the walls feel inhabited. The answer is not much — but each object has to earn its place.",
            "The seat sits at 450 mm with a 545 mm table beside it, both within reach of the window light. The palette moves between linen, sage and oak, with brass only where the hand might rest.",
        ],
        "captions": ["The corner in warm evening light", "Books, brass and a place to sit"],
        "card": "half",
    },
    {
        "slug": "dining-corner",
        "title": "Dining Corner",
        "plain": "Dining Corner",
        "category": "3D study · Dining",
        "year": "2026",
        "typology": "Dining",
        "area": "21 m²",
        "scope": "3D visualisation, layout, lighting",
        "palette": "Oak, terracotta, sage, cream",
        "img": "dining-corner",
        "glb": "dining-corner",
        "widths": [1280, 800],
        "w": 1280, "h": 720,
        "alt": "3D render of a dining room with an oak table, four chairs, low pendant and sideboard",
        "intro": "A 1.8-metre oak table under a pendant hung 750 mm above the surface — a dining room drawn for slow evenings.",
        "body": [
            "Four chairs sit at 450 mm, leaving a 300 mm thigh clearance under the 750 mm tabletop and 900 mm behind each chair to pull out. The pendant pools light on the table rather than the room.",
            "A sideboard runs the back wall, holding bowls, a vase and the things a dining room gathers. Terracotta and sage keep the oak from feeling too polite.",
        ],
        "captions": ["Oak, terracotta and pooled light", "The sideboard, dressed simply"],
        "card": "full",
    },
]

ICON_ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M7 17L17 7M9 7h8v8"/></svg>'
ICON_DOWN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M12 4v16m0 0l-6-6m6 6l6-6"/></svg>'
ICON_LEFT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M19 12H5m0 0l6-6m-6 6l6 6"/></svg>'
ICON_UP = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M12 20V4m0 0l-6 6m6-6l6 6"/></svg>'


def head(title, desc, image, rel="", canonical=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{escape(desc)}">
<meta name="theme-color" content="#f7f2ea">
<link rel="canonical" href="{BASE}/{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:image" content="{BASE}/assets/img/{image}">
<meta property="og:url" content="{BASE}/{canonical}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:creator" content="@{X_HANDLE}">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{escape(desc)}">
<meta name="twitter:image" content="{BASE}/assets/img/{image}">
<link rel="icon" href="{rel}assets/favicon.svg" type="image/svg+xml">
<script>document.documentElement.classList.add("js");</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..600;1,9..144,300..600&family=Manrope:wght@300..700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{rel}assets/css/style.css">
<script type="importmap">{{"imports":{{"three":"{rel}assets/vendor/three.module.js","three/addons/":"{rel}assets/vendor/addons/"}}}}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def header(rel="", current=""):
    links = [
        ("#work", "Work", "work"),
        ("#studio", "Studio", "studio"),
        ("#process", "Process", "process"),
        ("#contact", "Contact", "contact"),
    ]
    parts = []
    for h, label, key in links:
        active = ' aria-current="page"' if current == key else ""
        parts.append(f'<a href="{rel}index.html{h}"{active}>{label}</a>')
    nav = "".join(parts)
    return f"""<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="{rel}index.html">
      <span class="mark" aria-hidden="true">N</span>
      <span class="name">{SITE}</span>
    </a>
    <button class="menu-toggle" aria-label="Toggle menu" aria-expanded="false" aria-controls="nav"><span></span></button>
    <nav class="nav" id="nav" aria-label="Main">
      {nav}
      <a class="cta" href="mailto:{EMAIL}">Start a project</a>
    </nav>
  </div>
</header>
"""


def footer(rel=""):
    return f"""<footer class="site-footer">
  <div class="wrap footer-inner">
    <span>© <span data-year>2026</span> {SITE} · Interior design &amp; spatial styling</span>
    <a class="to-top" href="#top">Back to top {ICON_UP}</a>
  </div>
</footer>
<script src="{rel}assets/js/main.js" defer></script>
</body>
</html>
"""


def card(p, index):
    cls = {
        "wide": "card--wide",
        "narrow": "card--narrow",
        "half": "card--half",
        "full": "card--full",
    }[p["card"]]
    sizes = "(max-width:760px) 100vw, 60vw" if p["card"] in ("wide", "full") else "(max-width:760px) 100vw, 45vw"
    if p["card"] == "full":
        sizes = "(max-width:760px) 100vw, 100vw"
    widths = p.get("widths", [1800, 1200, 800])
    main = max(widths)
    srcset = ", ".join(f"assets/img/{p['img']}-{w}.webp {w}w" for w in widths)
    badge = '<span class="card-3d">3D view</span>' if p.get("glb") else ""
    return f"""<a class="card {cls} reveal" href="work/{p['slug']}.html" data-delay="{index % 3}">
  <div class="card-media">
    <span class="card-index">{index + 1:02d}</span>{badge}
    <img src="assets/img/{p['img']}-{main}.webp"
         srcset="{srcset}"
         sizes="{sizes}" width="{p['w']}" height="{p['h']}"
         alt="{escape(p['alt'])}" loading="lazy" decoding="async">
  </div>
  <div class="card-meta">
    <h3>{p['title']}</h3>
    <span>{p['category']} · {p['year']}</span>
  </div>
</a>"""


def index():
    cards = "\n".join(card(p, i) for i, p in enumerate(PROJECTS))
    ticker_items = [
        "Residential interiors", "Material palettes", "Spatial planning",
        "Styling", "3D visualisation", "Warm minimalism",
    ]
    ticker = "".join(f"<span>{t}</span>" for t in ticker_items)
    html = head(
        f"{SITE} — Interior design & spatial styling",
        "Warm, quiet interiors shaped by natural materials, honest light and the way people live. Selected work by Nkugwa Mark William, Kampala.",
        "oak-and-light-og.webp",
    )
    html += header()
    html += f"""<main id="main">
<section class="hero" id="top">
  <div class="wrap hero-grid">
    <div>
      <span class="eyebrow reveal">Interior design &amp; spatial styling — Kampala</span>
      <h1 class="reveal" data-delay="1">Spaces that feel like a <em>deep breath.</em></h1>
      <p class="lede reveal" data-delay="2">Warm, quiet interiors shaped by natural materials, honest light and the way people actually live. Selected work and visual studies by {SITE}.</p>
      <div class="hero-actions reveal" data-delay="3">
        <a class="btn btn-dark" href="#work">View selected work {ICON_DOWN}</a>
        <a class="btn btn-ghost" href="#contact">Start a project {ICON_ARROW}</a>
      </div>
      <div class="hero-meta reveal" data-delay="3">
        <div><strong>05</strong>3D rooms</div>
        <div><strong>05</strong>Orbitable models</div>
        <div><strong>KLA</strong>Kampala, Uganda</div>
      </div>
    </div>
    <div class="hero-visual reveal" data-delay="2">
      <div class="arch">
        <img src="assets/img/oak-and-light-1280.webp"
             srcset="assets/img/oak-and-light-800.webp 800w, assets/img/oak-and-light-1280.webp 1280w"
             sizes="(max-width:1000px) 90vw, 44vw" width="1280" height="720"
             alt="3D render of a warm living room with a linen sofa, oak coffee table and soft daylight" fetchpriority="high" decoding="async">
      </div>
      <div class="hero-note"><strong>Oak &amp; Light</strong>Living room · 3D study, 2026</div>
    </div>
  </div>
</section>

<div class="ticker" aria-hidden="true">
  <div class="ticker-track">{ticker}{ticker}</div>
</div>

<section class="section" id="work">
  <div class="wrap">
    <div class="section-head">
      <div>
        <span class="eyebrow reveal">Selected work</span>
        <h2 class="reveal" data-delay="1">A quiet collection of rooms</h2>
      </div>
      <p class="reveal" data-delay="2">Five rooms, modelled and measured in Blender, then published as orbitable 3D models. Open any room to move around it.</p>
    </div>
    <div class="work-grid">
      {cards}
    </div>
  </div>
</section>

<section class="section about" id="studio">
  <div class="wrap about-grid">
    <div class="about-figure reveal">
      <img src="assets/img/reading-nook-1280.webp"
           srcset="assets/img/reading-nook-800.webp 800w, assets/img/reading-nook-1280.webp 1280w"
           sizes="(max-width:1000px) 80vw, 38vw" width="1280" height="720"
           alt="Reading nook with linen armchair, bookshelf and warm lamp light" loading="lazy" decoding="async">
      <span class="tag">Kampala · Uganda</span>
    </div>
    <div class="about-copy">
      <span class="eyebrow reveal">The studio</span>
      <h2 class="reveal" data-delay="1">Considered rooms, made to be lived in.</h2>
      <p class="reveal" data-delay="2">I am {SITE}, an interior designer and spatial storyteller working between Kampala and the wider East African region. My work begins with how a room is used — where the light lands, where people pause, what the space should feel like at seven in the morning and again at nine at night.</p>
      <p class="reveal" data-delay="2">Every room is modelled at full scale and tested against researched dimensions — 450 mm seat heights, 750 mm dining tables, 900 mm worktops, 600 mm bed clearances and a compact kitchen work triangle. From there, the palette stays disciplined: timber, stone, linen, clay and a little brass.</p>
      <blockquote class="big-quote reveal" data-delay="3">“Good interiors do not ask for attention. They give it back.”</blockquote>
      <div class="services reveal" data-delay="3">
        <div><span>Interior design</span><span>Concept to install</span></div>
        <div><span>Spatial planning</span><span>Layout &amp; flow</span></div>
        <div><span>Anthropometrics</span><span>Dimensions &amp; clearances</span></div>
        <div><span>Material palettes</span><span>Sourcing</span></div>
        <div><span>3D visualisation</span><span>Models &amp; renders</span></div>
        <div><span>Styling</span><span>Furniture &amp; objects</span></div>
      </div>
      <p class="reveal" data-delay="3" style="margin-top:26px"><a class="link-arrow" href="mailto:{EMAIL}">Work with me {ICON_ARROW}</a></p>
    </div>
  </div>
</section>

<section class="section" id="process">
  <div class="wrap">
    <div class="section-head">
      <div>
        <span class="eyebrow reveal">How it works</span>
        <h2 class="reveal" data-delay="1">Four unhurried steps</h2>
      </div>
      <p class="reveal" data-delay="2">A simple, transparent process from first conversation to the final cushion.</p>
    </div>
    <div class="process-grid">
      <article class="step reveal"><span class="num">01</span><h3>Listen</h3><p>We walk the space, talk about routines, light and the things you want to keep. No mood boards yet.</p></article>
      <article class="step reveal" data-delay="1"><span class="num">02</span><h3>Sketch</h3><p>Layouts, material directions and a first visual study — enough to test the feeling before committing.</p></article>
      <article class="step reveal" data-delay="2"><span class="num">03</span><h3>Refine</h3><p>Samples, joinery details, lighting and a costed schedule. We edit until only the necessary remains.</p></article>
      <article class="step reveal" data-delay="3"><span class="num">04</span><h3>Deliver</h3><p>Procurement, installation and styling, with the room finished down to the last object.</p></article>
    </div>
  </div>
</section>

<section class="contact" id="contact">
  <div class="wrap contact-grid">
    <div>
      <span class="eyebrow reveal">Contact</span>
      <h2 class="reveal" data-delay="1">Let’s make a room that feels like <em>you.</em></h2>
      <p class="reveal" data-delay="2">Available for residential interiors, styling and visual studies. Share a few lines about your space and timeline.</p>
      <a class="mail reveal" data-delay="3" href="mailto:{EMAIL}">{EMAIL}</a>
    </div>
    <div class="contact-side reveal" data-delay="3">
      <div><span class="label">Based in</span>Kampala, Uganda — working across East Africa</div>
      <div><span class="label">Elsewhere</span><div class="socials"><a href="https://x.com/{X_HANDLE}" target="_blank" rel="noopener">X / Twitter</a><a href="https://github.com/MarkNwilliam" target="_blank" rel="noopener">GitHub</a></div></div>
      <div><span class="label">Response</span>Within two working days</div>
    </div>
  </div>
</section>
</main>
"""
    html += footer()
    return html


def viewer_section(p):
    return f"""<section class="section viewer-section" id="3d">
  <div class="wrap">
    <div class="section-head">
      <div>
        <span class="eyebrow reveal">Interactive 3D</span>
        <h2 class="reveal" data-delay="1">Step inside {p['plain']}</h2>
      </div>
      <p class="reveal" data-delay="2">A real-time model built in Blender. Drag to orbit, scroll or pinch to zoom, and open it fullscreen to look closer. Use the arrow keys to move and press 0 to reset.</p>
    </div>
    <div class="viewer reveal" data-3d data-model="../assets/models/{p['glb']}.glb" data-poster="../assets/img/{p['img']}-1280.webp" data-name="{escape(p['plain'])}">
      <div class="viewer-stage" tabindex="0" role="application" aria-label="Interactive 3D model of {escape(p['plain'])}. Drag to orbit, scroll to zoom, or use the arrow keys. Press 0 to reset.">
        <img class="viewer-poster" src="../assets/img/{p['img']}-1280.webp" width="1280" height="720" alt="{escape(p['alt'])}" loading="lazy" decoding="async">
        <div class="viewer-loader" role="status" data-viewer-loader><span>Loading 3D model</span><span class="viewer-bar"><i></i></span></div>
        <div class="viewer-error" role="alert" data-viewer-error hidden><span>3D preview unavailable — the render above still shows the room.</span></div>
      </div>
      <div class="viewer-toolbar">
        <span class="viewer-hint">Drag to orbit · Scroll to zoom</span>
        <div class="viewer-actions">
          <button type="button" data-viewer-rotate aria-pressed="true" disabled>Auto-rotate: on</button>
          <button type="button" data-viewer-reset disabled>Reset view</button>
          <button type="button" data-viewer-fullscreen disabled>Fullscreen</button>
        </div>
      </div>
    </div>
  </div>
</section>
<script type="module" src="../assets/js/viewer3d.js"></script>"""


def project_page(p, nxt, prev, index):
    widths = p.get("widths", [1280, 800])
    main = max(widths)
    body = "".join(f"<p>{escape(par)}</p>" for par in p["body"])
    viewer = viewer_section(p) if p.get("glb") else ""
    chip = '<a class="project-chip" href="#3d">Explore in 3D</a>' if p.get("glb") else ""
    html = head(
        f"{p['plain']} — {SITE}",
        p["intro"],
        f"{p['img']}-og.webp",
        rel="../",
        canonical=f"work/{p['slug']}.html",
    )
    html += header(rel="../")
    html += f"""<main id="main">
<section class="project-hero">
  <div class="wrap">
    <a class="back" href="../index.html#work">{ICON_LEFT} All work</a>
    <div class="project-intro">
      <div>
        <span class="eyebrow" style="margin-top:26px;display:inline-flex">{p['category']} · {p['year']}</span>
        <h1 class="project-title">{p['title']}</h1>{chip}
      </div>
      <p>{p['intro']}</p>
    </div>
    <div class="project-main">
      <img src="../assets/img/{p['img']}-{main}.webp" width="{p['w']}" height="{p['h']}" alt="{escape(p['alt'])}" fetchpriority="high" decoding="async">
    </div>
    <div class="project-meta">
      <div><span class="label">Typology</span><span class="value">{p['typology']}</span></div>
      <div><span class="label">Year</span><span class="value">{p['year']}</span></div>
      <div><span class="label">Area</span><span class="value">{p['area']}</span></div>
      <div><span class="label">Palette</span><span class="value">{p['palette']}</span></div>
    </div>
  </div>
</section>

<section class="wrap project-body">
  <h2 class="reveal">Modelled at full scale, finished in light.</h2>
  <div class="prose reveal" data-delay="1">{body}</div>
</section>

{viewer}

<a class="next" href="{nxt['slug']}.html">
  <div class="wrap">
    <span class="eyebrow">Next project</span>
    <h2>{nxt['title']} {ICON_ARROW}</h2>
  </div>
</a>
</main>
"""
    html += footer(rel="../")
    return html


def main():
    os.makedirs(os.path.join(ROOT, "work"), exist_ok=True)
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(index())
    for i, p in enumerate(PROJECTS):
        nxt = PROJECTS[(i + 1) % len(PROJECTS)]
        prev = PROJECTS[(i - 1) % len(PROJECTS)]
        with open(os.path.join(ROOT, "work", p["slug"] + ".html"), "w", encoding="utf-8") as f:
            f.write(project_page(p, nxt, prev, i))
    urls = [""] + [f"work/{p['slug']}.html" for p in PROJECTS]
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        sitemap += f"  <url><loc>{BASE}/{u}</loc></url>\n"
    sitemap += "</urlset>\n"
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
    print("Built", len(urls), "pages")


if __name__ == "__main__":
    main()
