"""Generate individual case study pages for each project in the portfolio."""
import os, re, html

BASE = os.path.dirname(os.path.abspath(__file__))
WORK_DIR = os.path.join(BASE, "work")
os.makedirs(WORK_DIR, exist_ok=True)

# All 35 projects with metadata extracted from work.html index
# Format: (slug, name, categories, sector, location, area, hero_img, excerpt)
PROJECTS = [
    ("angel-square", "Angel Square", "workplace", "Co-working & office space", "Angel Square, London", "3800 sqm", "angel-square.jpg", "Redefining office space with a design-led approach."),
    ("barbour", "Barbour", "exhibition retail heritage", "Fashion Expo", "Global", "60 - 100 sqm", "barbour.jpg", "Bringing seasonal brand campaigns to life at Europe's largest fashion fairs."),
    ("b-fit", "B_Fit", "health-leisure", "Smart Gym", "Various, Saudi Arabia", "4500 sqm", "b-fit.jpg", "A smart gym concept redefining fitness in the Middle East."),
    ("birdies-crazy-golf", "Birdies Crazy Golf", "social-gaming hospitality", "Kaleidoscopic Crazy Golf", "Various, London", "480 - 570 sqm", "birdies-crazy-golf.jpg", "Kaleidoscopic. Luminous. Surreal. Crazy golf just got crazier!"),
    ("bite", "Bite", "workplace", "A modern workplace", "London, UK", "1125 sqm", "bite.jpg", "A modern workplace designed for collaboration and creativity."),
    ("bounce-battersea", "Bounce Battersea", "hospitality social-gaming", "Ping Pong Bar", "Battersea, London", "750 sqm", "bounce-battersea.jpg", "Staying ahead of the game by playing to sporting origins."),
    ("bunkers", "Bunkers", "social-gaming", "Dystopian Social Gaming", "Romford, UK", "2000 sqm", "bunkers.jpg", "A dystopian social gaming experience unlike anything else."),
    ("cha-cha-teng", "Cha Cha Teng", "hospitality", "Hong Kong Style Restaurant", "Holborn, London", "400 sqm", "cha-cha-teng.jpg", "Authentic Hong Kong dining brought to the heart of London."),
    ("commodity", "Commodity", "beauty retail", "Retail", "NYC, USA", "", "commodity.jpg", "Making the exceptional accessible."),
    ("counter-house", "The Counter House", "hospitality", "Local Bar & Eatery", "Ancoats, Manchester", "225 sqm", "counter-house.jpg", "A neighbourhood bar and eatery with character and warmth."),
    ("etat-libre", "Etat Libre D'Orange", "beauty retail", "Experimental Fragrance Lab", "Redchurch St, London", "40 sqm", "etat-libre.jpg", "An experimental fragrance lab pushing the boundaries of scent."),
    ("freuds", "Freuds", "workplace", "Office meets members club", "London, UK", "3500 sqm", "freuds.jpg", "Where the workplace meets the members club."),
    ("harrods-toy-kingdom", "Harrods Toy Kingdom", "retail", "Iconic Toy Department", "Harrods, London", "350 sqm", "harrods-toy-kingdom.jpg", "Breaking gender stereotypes with an immersive retail wonderland."),
    ("jollibee", "Jollibee", "hospitality", "Fast food served with a smile", "Various, Asia", "230 sqm", "jollibee.jpg", "Refreshing a brand to put a smile at the heart of everything they do."),
    ("kudos", "Kudos", "hospitality", "A home from home", "Islington, London", "680 sqm", "kudos.jpg", "Creating a home from home in the heart of Islington."),
    ("level-shoe-district", "Level Shoe District", "retail", "The world's biggest shoe store", "Dubai Mall", "9000 sqm", "level-shoe-district.jpg", "The world's biggest shoe store, in the world's mega mall."),
    ("lotte-dongtang", "Lotte Dongtang", "retail", "Three floors of fashion retail", "Dongtan, South Korea", "16000 sqm", "lotte-dongtang.jpg", "Creating a retailtainment destination with three floors of fashion retail."),
    ("luton-airport", "Luton Airport", "infrastructure brand-identity", "Infrastructure & Brand Identity", "London, UK", "", "luton-airport.jpg", "Helping a busy airport to embrace and express their difference."),
    ("margaret-dabbs", "Margaret Dabbs", "beauty", "Luxury Hand & Nail Spa", "Doha, Qatar", "232 sqm", "margaret-dabbs.jpg", "A luxury hand and nail spa experience in the heart of Doha."),
    ("meat-liquor", "Meat Liquor", "hospitality", "Dive Burger Bar", "Various, UK", "180 - 500 sqm", "meat-liquor.jpg", "Creators of the original bad boy behemoth."),
    ("optimo", "Optimo", "health-leisure", "Members club meets gym", "Various, Saudi Arabia", "4500 sqm", "optimo.jpg", "Where the members club meets the gym."),
    ("oree", "Or\u00e9e", "hospitality", "Boulangerie patisserie", "Various, UK", "80 - 180 sqm", "oree.jpg", "Artisan boulangerie patisserie with a French soul and a London heart."),
    ("pass-on-plastic", "Pass on Plastic", "exhibition", "Pop-up Exhibition", "Soho, London", "119 sqm", "pass-on-plastic.jpg", "A pop-up exhibition raising awareness about plastic pollution."),
    ("peter-reed", "Peter Reed", "retail", "Retail Concession & Brand Book", "Harrods, London", "20 sqm", "peter-reed.jpg", "A refined retail concession for a heritage linen brand."),
    ("queens-skate", "Queens Skate Dine Bowl", "hospitality social-gaming", "Bowling, Ice Rink & Bar", "London, UK", "460 sqm", "queens-skate.jpg", "Bowling, ice skating and dining under one roof."),
    ("russell-bromley", "Russell & Bromley", "retail", "British Shoe Store", "Various, UK", "150 - 200 sqm", "russell-bromley.jpg", "Shaping the next chapter of the great British shoe store."),
    ("shakti", "Shakti", "brand-identity health-leisure", "Acupressure and wellbeing", "Global", "", "shakti.jpg", "Reframing an ancient ritual for modern life."),
    ("spencer-hart", "Spencer Hart", "retail", "Modern British Tailoring", "Brook St, London", "25 sqm", "spencer-hart.jpg", "Translating Nick Hart's rich and varied world into the brand's first flagship store."),
    ("the-brewery", "The Brewery", "workplace", "Out of town workplace", "Oxfordshire, UK", "468 sqm", "brewery.jpg", "An out of town workplace with rural charm and modern thinking."),
    ("the-office-group", "The Office Group", "workplace", "A suite of projects", "London, UK", "885 - 1040 sqm", "office-group.jpg", "A suite of workspace projects across London."),
    ("thomas-goode", "Thomas Goode", "retail heritage", "Royal Warrant Tableware", "Mumbai, India", "110 sqm", "thomas-goode.jpg", "Bringing a Royal Warrant tableware brand to Mumbai."),
    ("turnbull-asser", "Turnbull & Asser", "retail heritage", "Royal Warrant Shirtmaker", "Davis St, London", "110 sqm", "turnbull-asser.jpg", "A Royal Warrant shirtmaker reimagined for a modern era."),
    ("ulu-cliffhouse", "Ulu Cliffhouse", "hospitality health-leisure", "World class beach club", "Bali, Indonesia", "4750 sqm", "ulu-cliffhouse.jpg", "Building a world class destination from the rock-face up."),
    ("vertu", "Vertu", "retail", "Luxury tech retail", "Global", "", "vertu.jpg", "Luxury tech retail rolled out across the globe."),
    ("william-son", "William & Son", "retail heritage", "Heritage Lifestyle Store", "Bruton Street, London", "950 sqm", "william-son.jpg", "A heritage lifestyle store brought into the 21st century."),
]

def get_category_labels(cats_str):
    """Convert category slugs to display labels."""
    mapping = {
        "workplace": "Workplace",
        "exhibition": "Exhibition",
        "retail": "Retail",
        "heritage": "Heritage",
        "hospitality": "Hospitality",
        "social-gaming": "Social Gaming",
        "health-leisure": "Health & Leisure",
        "brand-identity": "Brand Identity",
        "beauty": "Beauty",
        "infrastructure": "Infrastructure",
    }
    return [mapping.get(c, c.title()) for c in cats_str.split()]

def pill_html(label):
    return f'''<span class="title-pill title-pill--filled title-pill--fill-dark">
                      <svg class="title-pill__border" preserveAspectRatio="none"><rect x="0" y="0" width="100%" height="100%" rx="20"></rect></svg>
                      <span class="title-pill__label body-xs text-uppercase">{html.escape(label)}</span>
                    </span>'''

def get_next_project(idx):
    return PROJECTS[(idx + 1) % len(PROJECTS)]

def get_related_projects(idx):
    """Get 3 related projects (next 3 after current)."""
    total = len(PROJECTS)
    return [PROJECTS[(idx + i) % total] for i in range(1, 4)]

def generate_page(idx):
    slug, name, categories, sector, location, area, hero_img, excerpt = PROJECTS[idx]
    cat_labels = get_category_labels(categories)
    next_proj = get_next_project(idx)
    related = get_related_projects(idx)

    name_escaped = html.escape(name)
    sector_escaped = html.escape(sector)
    location_escaped = html.escape(location)
    area_escaped = html.escape(area)
    excerpt_escaped = html.escape(excerpt)

    # Category pills for metadata
    cats_display = ", ".join(cat_labels)

    # Related project cards HTML
    related_cards = ""
    for rslug, rname, rcats, rsector, rloc, rarea, rimg, rexcerpt in related:
        rcat_labels = get_category_labels(rcats)
        rpills = "\n                    ".join([pill_html(l) for l in rcat_labels[:2]])
        related_cards += f'''
          <div class="work-grid__item">
            <a href="{rslug}.html" class="list-item" data-cursor="View">
              <div class="list-item__fig clip-reveal" data-reveal>
                <img src="../img/{rimg}" alt="{html.escape(rname)}" class="base-image__img base-image__img--loaded">
              </div>
              <div class="list-item__wrapper anim-line" data-reveal>
                <h4 class="list-item__title">{html.escape(rname)}</h4>
                <div class="list-item-tags">
                    {rpills}
                </div>
              </div>
            </a>
          </div>'''

    page_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Shed | {name_escaped}</title>
  <meta name="description" content="{name_escaped} &mdash; {location_escaped}. {excerpt_escaped}">
  <meta property="og:title" content="Shed | {name_escaped}">
  <meta property="og:description" content="{name_escaped} &mdash; {sector_escaped}. {location_escaped}.">
  <meta property="og:type" content="website">

  <!-- CSS -->
  <link rel="stylesheet" href="../css/branding.css">
  <link rel="stylesheet" href="../css/base.css">
  <link rel="stylesheet" href="../css/components.css">
  <link rel="stylesheet" href="../css/pages.css">

  <!-- Preload fonts -->
  <link rel="preload" href="../fonts/Owners-Bold.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="../fonts/SequelSans-RomanHead.woff2" as="font" type="font/woff2" crossorigin>
</head>
<body>
  <!-- Page Transition Overlay -->
  <div class="page-transition-overlay"></div>

  <!-- Custom Cursor -->
  <div class="cursor">
    <div class="cursor__label"><p></p></div>
  </div>

  <!-- Custom Scrollbar -->
  <div class="scrollbar">
    <div class="scrollbar__wrapper">
      <div class="scrollbar__handle"></div>
    </div>
  </div>

  <!-- Header -->
  <header class="header header--dark">
    <a href="../index.html" class="header-logo" data-cursor="Home" data-cursor-small>
      <svg class="header-logo__svg" viewBox="0 0 96 32" fill="currentColor">
        <path d="m13.085 12.857-.953-.432c-3.07-1.386-4.214-2.54-4.214-4.27 0-1.894 1.437-3.327 3.347-3.327 3.198 0 4.614 2.998 5.49 5.61l.115.339 2.674-.423-.068-.415c-.489-3.01-.782-5.073-.948-6.692l-.03-.288-1.947-.528-.587-.152a15.7 15.7 0 0 0-4.091-.533c-3.321 0-6.09.934-8.012 2.702-1.782 1.636-2.76 3.961-2.76 6.544 0 4.621 3.76 6.989 7.825 8.862l.646.3c2.905 1.327 4.087 2.71 4.087 4.786 0 2.371-1.365 3.843-3.564 3.843-4.533 0-6.884-5.83-7.31-6.997l-.136-.372L0 22.192l.068.367c.272 1.522.566 2.905.82 4.127.23 1.095.447 2.13.609 3.06l.038.208.192.093c.54.27 1.45.617 2.78 1.057 1.102.363 2.943.752 4.81.752 6.723 0 11.422-3.944 11.422-9.588s-3.95-7.741-7.65-9.42zm28.806 13.38v-8.611c0-4.414-2.568-7.052-6.876-7.052-2.037 0-3.674.993-5.035 1.961V0l-.489.08-2.7.448c-2.675.449-4.989.833-6.766 1.057l-.37.047v2.313l.395.025c1.149.076 1.812.13 2.042.363.234.237.246.905.246 1.97v19.934c0 2.203-.02 2.229-2.432 2.465l-.379.038v2.478h11.87v-2.452l-.35-.06c-.71-.122-.859-.207-.935-.35-.12-.237-.128-.757-.128-1.603V15.808c.638-.495 1.22-.867 2.046-.867 1.833 0 2.22 1.67 2.22 3.07v8.446c0 .969 0 1.607-.154 1.86-.106.178-.386.267-1.203.385l-.361.051v2.46h11.74V28.74l-.37-.042c-1.972-.232-2.01-.237-2.01-2.465v.005Zm19.979-8.18c0-4.41-4.01-7.48-7.608-7.48-6.035 0-10.946 5.036-10.946 11.226 0 5.85 4.231 9.935 10.295 9.935 1.701 0 5.324-1.061 8.097-5.044l.153-.22-1.178-1.974-.366.22c-1.607.972-2.925 1.573-4.541 1.573-1.982 0-4.73-1.87-5.006-5.378 3.951-.178 8.977-.58 9.68-.719 1.194-.224 1.42-.562 1.42-2.135zm-7.174-.453s-.09.055-.46.076l-3.393.115c.14-3.112 1.322-4.14 1.9-4.14.736 0 2.004 1.751 2.004 3.54 0 .338-.043.401-.051.41ZM86.18 27.781l-1.74-.11c-.956-.072-1.033-.076-1.033-1.734V0l-.489.08-2.691.448c-2.569.427-4.997.833-6.775 1.057l-.37.047v2.313l.396.025c1.148.076 1.811.13 2.045.363.234.237.247.905.247 1.97V10.7c-.34-.067-.689-.126-1.008-.126-3.56 0-6.787 1.302-9.083 3.665-2.059 2.118-3.134 4.9-3.028 7.834.23 6.591 5.762 9.66 9.428 9.66.655 0 1.407-.11 2.5-.896 0 0 .66-.486 1.195-.883v2.037l.532-.143c3.023-.82 6.557-1.256 8.458-1.488l1.433-.186-.008-.368v-2.03zm-10.414-.888c-.409.321-.808.473-1.31.473-.761 0-3.606-1.234-3.606-7.284s2.734-6.426 3.044-6.426c.681 0 1.276.376 1.872 1.154v12.087zm15.815-3.924c-2.492 0-4.368 1.924-4.368 4.473s1.88 4.473 4.368 4.473c2.487 0 4.414-1.88 4.414-4.473 0-2.591-1.897-4.473-4.414-4.473"/>
      </svg>
    </a>
    <!-- Center Pill: Back to Work -->
    <a href="../work.html" class="header__center-pill title-pill title-pill--small" data-cursor="View" data-cursor-small>
      <svg class="title-pill__border" preserveAspectRatio="none"><rect x="0" y="0" width="100%" height="100%" rx="20"></rect></svg>
      <span class="title-pill__label body-xs text-uppercase">Back to Work</span>
    </a>
    <button class="nav-toggle nav-toggle--open" data-cursor="Menu" data-cursor-small>
      <svg class="nav-toggle__svg" viewBox="0 0 19 19" fill="none">
        <path stroke="currentColor" d="M19 9.5H0M9.5 19V0"></path>
      </svg>
      <span class="nav-toggle__label-wrapper" data-label="Menu">
        <span class="nav-toggle__label">Menu</span>
      </span>
    </button>
  </header>

  <!-- Full-Screen Navigation -->
  <nav class="nav" id="nav">
    <div class="nav__title">
      <span class="title-pill title-pill--medium title-pill--filled title-pill--fill-dark">
        <svg class="title-pill__border" preserveAspectRatio="none"><rect x="0" y="0" width="100%" height="100%" rx="20"></rect></svg>
        <span class="title-pill__label body-xs text-uppercase">Navigation</span>
      </span>
    </div>
    <ul class="nav__list">
      <li class="nav-item">
        <div class="nav-item__link-border nav-item__link-border--top"></div>
        <a href="../index.html" class="nav-item__link">
          <span class="nav-item__link-label"><span class="nav-item__link-inner">About</span></span>
        </a>
        <div class="nav-item__link-border nav-item__link-border--bot"></div>
      </li>
      <li class="nav-item">
        <div class="nav-item__link-border nav-item__link-border--top"></div>
        <a href="../services.html" class="nav-item__link">
          <span class="nav-item__link-label"><span class="nav-item__link-inner">Services</span></span>
        </a>
        <div class="nav-item__link-border nav-item__link-border--bot"></div>
      </li>
      <li class="nav-item">
        <div class="nav-item__link-border nav-item__link-border--top"></div>
        <a href="../work.html" class="nav-item__link active">
          <span class="nav-item__link-label"><span class="nav-item__link-inner">Work</span></span>
        </a>
        <div class="nav-item__link-border nav-item__link-border--bot"></div>
      </li>
      <li class="nav-item">
        <div class="nav-item__link-border nav-item__link-border--top"></div>
        <a href="../blog.html" class="nav-item__link">
          <span class="nav-item__link-label"><span class="nav-item__link-inner">News &amp; Views</span></span>
        </a>
        <div class="nav-item__link-border nav-item__link-border--bot"></div>
      </li>
      <li class="nav-item">
        <div class="nav-item__link-border nav-item__link-border--top"></div>
        <a href="../contact.html" class="nav-item__link">
          <span class="nav-item__link-label"><span class="nav-item__link-inner">Contact</span></span>
        </a>
        <div class="nav-item__link-border nav-item__link-border--bot"></div>
      </li>
    </ul>
    <button class="nav-toggle nav-toggle--close" style="position:absolute;right:0.8rem;top:1.4rem;display:none;color:#000;z-index:700">
      <svg class="nav-toggle__svg" viewBox="0 0 19 19" fill="none">
        <path stroke="currentColor" d="M19 9.5H0M9.5 19V0"></path>
      </svg>
      <span class="nav-toggle__label-wrapper" data-label="Close">
        <span class="nav-toggle__label">Close</span>
      </span>
    </button>
  </nav>

  <!-- Nav Backdrop -->
  <div class="transition-overlay"></div>

  <!-- Page Wrapper -->
  <div class="page-wrapper">
    <main class="page page--dark">

      <!-- ===== 1. PROJECT HERO ===== -->
      <section class="project-hero">
        <div class="project-hero__fig">
          <img src="../img/{hero_img}" alt="{name_escaped} &mdash; {location_escaped}">
        </div>
        <div class="project-hero__content">
          <h1 class="project-hero__title anim-word">{name_escaped}</h1>
          <p class="project-hero__subtitle anim-line">{location_escaped}</p>
        </div>
      </section>

      <!-- ===== 2. PROJECT INTRO ===== -->
      <section class="module">
        <div class="module__side-by-side">
          <div class="project-meta anim-line" data-reveal>
            <div class="project-meta__group" style="margin-bottom:2.4rem">
              <span class="body-xs text-uppercase" style="display:block;margin-bottom:0.6rem;opacity:0.5">Client</span>
              <span class="body-md">{name_escaped}</span>
            </div>
            <div class="project-meta__group" style="margin-bottom:2.4rem">
              <span class="body-xs text-uppercase" style="display:block;margin-bottom:0.6rem;opacity:0.5">Location</span>
              <span class="body-md">{location_escaped}</span>
            </div>
            <div class="project-meta__group" style="margin-bottom:2.4rem">
              <span class="body-xs text-uppercase" style="display:block;margin-bottom:0.6rem;opacity:0.5">Sectors</span>
              <span class="body-md">{cats_display}</span>
            </div>{f"""
            <div class="project-meta__group">
              <span class="body-xs text-uppercase" style="display:block;margin-bottom:0.6rem;opacity:0.5">Size</span>
              <span class="body-md">{area_escaped}</span>
            </div>""" if area else ""}
          </div>
          <div class="project-intro anim-line" data-reveal>
            <p class="body-lg" style="margin-bottom:2rem">
              {excerpt_escaped}
            </p>
            <p class="body-md">
              This is a placeholder case study page. Replace this content with the actual project description, detailing the design brief, creative approach, and outcomes delivered.
            </p>
          </div>
        </div>
      </section>

      <!-- ===== 3. FULL-WIDTH IMAGE ===== -->
      <section class="module module--fullwidth">
        <div class="clip-reveal" data-reveal>
          <img src="../img/{hero_img}" alt="{name_escaped} project image">
        </div>
      </section>

      <!-- ===== 4. NEXT PROJECT ===== -->
      <section class="next-up next-up--dark">
        <div class="next-up__header">
          <span class="next-up__label body-xs text-uppercase anim-fade" data-reveal>Next Up</span>
          <a href="{next_proj[0]}.html" class="next-up__name h2 anim-word" data-reveal><strong>{html.escape(next_proj[1])}</strong></a>
          <a href="{next_proj[0]}.html" class="next-up__arrow anim-fade" data-reveal data-cursor="View">
            <svg viewBox="0 0 155 157" fill="currentColor">
              <path stroke="currentColor" stroke-width="3" d="M1.5 87.688v1.5h109.691l-48.798 48.797-1.064 1.064 1.068 1.061 13.046 12.954 1.06 1.054 1.058-1.057 73.5-73.5 1.06-1.061-1.06-1.06-73.5-73.5L76.5 2.878l-1.06 1.06-12.955 12.955-1.06 1.06 1.059 1.06 48.711 48.799H1.5v19.874Z"/>
            </svg>
          </a>
        </div>
      </section>

      <!-- ===== 5. RELATED PROJECTS ===== -->
      <section class="module">
        <div class="grid" style="margin-bottom:2rem">
          <div class="col-5 col-md-9" style="display:flex;justify-content:space-between;align-items:center">
            <h3 class="body-lg anim-word" data-reveal>Related Projects</h3>
            <a href="../work.html" class="btn btn--theme-dark anim-fade" data-reveal data-cursor="View">
              <span class="btn__label">All work</span>
            </a>
          </div>
        </div>
        <div class="work-grid">{related_cards}
        </div>
      </section>

      <!-- ===== BACK TO WORK ===== -->
      <section class="back-to-work">
        <a href="../work.html" class="back-to-work__link" data-cursor="View">
          <span class="title-pill title-pill--medium">
            <svg class="title-pill__border" preserveAspectRatio="none"><rect x="0" y="0" width="100%" height="100%" rx="20"></rect></svg>
            <span class="title-pill__label body-sm text-uppercase">Back to Work</span>
          </span>
        </a>
      </section>

    </main>

    <!-- ===== FOOTER ===== -->
    <footer class="footer">
      <div class="footer__top">
        <div class="footer__social">
          <a href="https://www.instagram.com/shed_design/" class="footer-link body-xs text-uppercase" data-label="Instagram" data-cursor-small target="_blank" rel="noopener">
            <span class="footer-link__label">Instagram</span>
          </a>
          <a href="https://www.linkedin.com/company/shed-design/" class="footer-link body-xs text-uppercase" data-label="LinkedIn" data-cursor-small target="_blank" rel="noopener">
            <span class="footer-link__label">LinkedIn</span>
          </a>
        </div>
        <a href="../index.html" class="header-logo" style="color:currentColor">
          <svg class="header-logo__svg" viewBox="0 0 96 32" fill="currentColor">
            <path d="m13.085 12.857-.953-.432c-3.07-1.386-4.214-2.54-4.214-4.27 0-1.894 1.437-3.327 3.347-3.327 3.198 0 4.614 2.998 5.49 5.61l.115.339 2.674-.423-.068-.415c-.489-3.01-.782-5.073-.948-6.692l-.03-.288-1.947-.528-.587-.152a15.7 15.7 0 0 0-4.091-.533c-3.321 0-6.09.934-8.012 2.702-1.782 1.636-2.76 3.961-2.76 6.544 0 4.621 3.76 6.989 7.825 8.862l.646.3c2.905 1.327 4.087 2.71 4.087 4.786 0 2.371-1.365 3.843-3.564 3.843-4.533 0-6.884-5.83-7.31-6.997l-.136-.372L0 22.192l.068.367c.272 1.522.566 2.905.82 4.127.23 1.095.447 2.13.609 3.06l.038.208.192.093c.54.27 1.45.617 2.78 1.057 1.102.363 2.943.752 4.81.752 6.723 0 11.422-3.944 11.422-9.588s-3.95-7.741-7.65-9.42zm28.806 13.38v-8.611c0-4.414-2.568-7.052-6.876-7.052-2.037 0-3.674.993-5.035 1.961V0l-.489.08-2.7.448c-2.675.449-4.989.833-6.766 1.057l-.37.047v2.313l.395.025c1.149.076 1.812.13 2.042.363.234.237.246.905.246 1.97v19.934c0 2.203-.02 2.229-2.432 2.465l-.379.038v2.478h11.87v-2.452l-.35-.06c-.71-.122-.859-.207-.935-.35-.12-.237-.128-.757-.128-1.603V15.808c.638-.495 1.22-.867 2.046-.867 1.833 0 2.22 1.67 2.22 3.07v8.446c0 .969 0 1.607-.154 1.86-.106.178-.386.267-1.203.385l-.361.051v2.46h11.74V28.74l-.37-.042c-1.972-.232-2.01-.237-2.01-2.465v.005Zm19.979-8.18c0-4.41-4.01-7.48-7.608-7.48-6.035 0-10.946 5.036-10.946 11.226 0 5.85 4.231 9.935 10.295 9.935 1.701 0 5.324-1.061 8.097-5.044l.153-.22-1.178-1.974-.366.22c-1.607.972-2.925 1.573-4.541 1.573-1.982 0-4.73-1.87-5.006-5.378 3.951-.178 8.977-.58 9.68-.719 1.194-.224 1.42-.562 1.42-2.135zm-7.174-.453s-.09.055-.46.076l-3.393.115c.14-3.112 1.322-4.14 1.9-4.14.736 0 2.004 1.751 2.004 3.54 0 .338-.043.401-.051.41ZM86.18 27.781l-1.74-.11c-.956-.072-1.033-.076-1.033-1.734V0l-.489.08-2.691.448c-2.569.427-4.997.833-6.775 1.057l-.37.047v2.313l.396.025c1.148.076 1.811.13 2.045.363.234.237.247.905.247 1.97V10.7c-.34-.067-.689-.126-1.008-.126-3.56 0-6.787 1.302-9.083 3.665-2.059 2.118-3.134 4.9-3.028 7.834.23 6.591 5.762 9.66 9.428 9.66.655 0 1.407-.11 2.5-.896 0 0 .66-.486 1.195-.883v2.037l.532-.143c3.023-.82 6.557-1.256 8.458-1.488l1.433-.186-.008-.368v-2.03zm-10.414-.888c-.409.321-.808.473-1.31.473-.761 0-3.606-1.234-3.606-7.284s2.734-6.426 3.044-6.426c.681 0 1.276.376 1.872 1.154v12.087zm15.815-3.924c-2.492 0-4.368 1.924-4.368 4.473s1.88 4.473 4.368 4.473c2.487 0 4.414-1.88 4.414-4.473 0-2.591-1.897-4.473-4.414-4.473"/>
          </svg>
        </a>
      </div>
      <nav class="footer__nav">
        <a href="../index.html" class="footer-nav__link h4" data-cursor-small>About</a>
        <a href="../services.html" class="footer-nav__link h4" data-cursor-small>Services</a>
        <a href="../work.html" class="footer-nav__link h4" data-cursor-small>Work</a>
        <a href="../blog.html" class="footer-nav__link h4" data-cursor-small>News &amp; Views</a>
        <a href="../contact.html" class="footer-nav__link h4" data-cursor-small>Contact</a>
      </nav>
      <div class="footer__bottom">
        <div class="footer__legal">
          <a href="#" class="footer-link body-xs text-uppercase" data-label="Terms &amp; Conditions">
            <span class="footer-link__label">Terms &amp; Conditions</span>
          </a>
          <a href="#" class="footer-link body-xs text-uppercase" data-label="Privacy Policy">
            <span class="footer-link__label">Privacy Policy</span>
          </a>
        </div>
        <span class="footer__credit body-xs">Site by IJP + TA</span>
      </div>
    </footer>

    <!-- SEE WORK CTA -->
    <section class="see-work-cta" data-cursor="View">
      <a href="../work.html" class="see-work-cta__link">
        <span class="see-work-cta__text h2">See</span>
        <span class="see-work-cta__img-wrapper">
          <img src="../img/{hero_img}" alt="" class="see-work-cta__img">
        </span>
        <span class="see-work-cta__text h2">Work</span>
        <span class="see-work-cta__arrow">
          <svg viewBox="0 0 155 157" fill="currentColor">
            <path stroke="currentColor" stroke-width="3" d="M1.5 87.688v1.5h109.691l-48.798 48.797-1.064 1.064 1.068 1.061 13.046 12.954 1.06 1.054 1.058-1.057 73.5-73.5 1.06-1.061-1.06-1.06-73.5-73.5L76.5 2.878l-1.06 1.06-12.955 12.955-1.06 1.06 1.059 1.06 48.711 48.799H1.5v19.874Z"/>
          </svg>
        </span>
      </a>
    </section>
  </div>

  <!-- Scripts (CDN) -->
  <script src="https://cdn.jsdelivr.net/npm/lenis@1.1.18/dist/lenis.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.12.7/dist/gsap.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.12.7/dist/ScrollTrigger.min.js"></script>

  <!-- App Scripts -->
  <script src="../js/app.js"></script>
  <script src="../js/animations.js"></script>
  <script src="../js/nav.js"></script>
  <script src="../js/transitions.js"></script>
  <script src="../js/components.js"></script>
</body>
</html>'''

    return page_html


# ---- Generate all pages ----
print("Generating 35 project pages...")
for i in range(len(PROJECTS)):
    slug = PROJECTS[i][0]
    page_html = generate_page(i)
    filepath = os.path.join(WORK_DIR, f"{slug}.html")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(page_html)
    print(f"  Created work/{slug}.html")

# ---- Build slug lookup for updating work.html links ----
# Map project names to slugs for link updating
NAME_TO_SLUG = {}
for slug, name, *_ in PROJECTS:
    NAME_TO_SLUG[name.lower()] = slug
    # Also map without "the " prefix
    if name.lower().startswith("the "):
        NAME_TO_SLUG[name[4:].lower()] = slug

print(f"\nGenerated {len(PROJECTS)} pages in work/ directory.")
print("\nSlug mapping for work.html link updates:")
for name, slug in sorted(NAME_TO_SLUG.items()):
    print(f"  {name} -> work/{slug}.html")
