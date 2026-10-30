#!/usr/bin/env python3
"""Bouwt alle pagina's van Enigma Mystery (NL en EN) uit de gegevens hieronder.

Gebruik: python3 _tools/build_site.py
Nieuw spel toevoegen: één regel in SPELLEN, beeld in assets/dossiers/<art>.jpg, opnieuw bouwen.
"""
import json
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.enigmamystery.com"
MINI = "https://www.minimystery.nl"  # kinderserie, eigen site
KOFI_PRO = "https://ko-fi.com/s/67649bac70"
WANDEL = {"nl": "https://www.moordwandeling.nl", "en": "https://www.murderwalk.com"}
NOTITIE_ADRES = "kellievandekerkhof@gmail.com"

# --------------------------------------------------------------------------
# Spellen: plank, beeld, titels, haak, bestand NL/EN, pro, datum toegevoegd
# --------------------------------------------------------------------------
SPELLEN = [
 # Verhaalzaken
 dict(plank="verhaal", art="villa", pro=False, added="2026-09-01",
      nl=("Villa Meridiaan", "Een val van de keldertrap. Of toch niet?", "villa-meridiaan.html"),
      en=("Meridian House", "A fall down the cellar stairs. Or was it?", "meridian-house.html")),
 dict(plank="verhaal", art="telefoon", pro=True, added="2026-10-20",
      nl=("Laatst gezien 23:14", "Haar telefoon. Haar laatste avond. Eén bericht dat zij nooit schreef.", "last-seen-2314.html#nl"),
      en=("Last Seen 23:14", "Her phone. Her last evening. One message she never wrote.", "last-seen-2314.html#en")),
 dict(plank="verhaal", art="radio", pro=True, added="2026-09-02",
      nl=("Nachtfrequentie", "Iedereen verbergt iets. De radio speelt door.", "nachtfrequentie.html"),
      en=("Night Frequency", "Everyone is hiding something. The radio plays on.", "night-frequency.html")),
 dict(plank="verhaal", art="trein", pro=True, added="2026-09-03",
      nl=("Nachttrein 212", "Eén nachttrein. Geen stops. Eén dode vóór de ochtend.", "nachttrein212.html"),
      en=("Night Train 212", "One sleeper train. No stops. One dead by morning.", "night-train-212.html")),
 dict(plank="verhaal", art="maan", pro=True, added="2026-09-04",
      nl=("Halvemaan", "De dokter tekende hartfalen. De apotheek zegt iets anders.", "halvemaan.html"),
      en=("The Half Moon", "The doctor signed heart failure. The pharmacy disagrees.", "halfmoon.html")),
 dict(plank="verhaal", art="zee", pro=True, added="2026-09-05",
      nl=("Zeezicht", "Een gesloten badhotel, storm, een lichaam in het zwembad.", "zeezicht.html"),
      en=("Sea View", "A closed hotel, a storm, a body in the pool.", "seaview.html")),
 # Escape & 3D
 dict(plank="escape", art="klok", pro=False, added="2026-09-20",
      nl=("De Stilstaande Klok", "Opgesloten met het lichaam. In 3D.", "the-stopped-clock.html"),
      en=("The Stopped Clock", "Locked in with the body. In 3D.", "the-stopped-clock.html")),
 dict(plank="escape", art="kaars", pro=False, added="2026-10-20",
      nl=("De Laatste Kaars", "Dertien kaarsen. Vier geesten. Eén leugenaar.", "the-last-candle.html#nl"),
      en=("The Last Candle", "Thirteen candles. Four ghosts. One liar.", "the-last-candle.html#en")),
 dict(plank="escape", art="vat", pro=True, added="2026-09-22",
      nl=("Het Lege Vat", "Een wijnkelder, een lantaarn, een dode handelaar.", "the-empty-barrel.html"),
      en=("The Empty Barrel", "A wine cellar, a lantern, a dead merchant.", "the-empty-barrel.html")),
 dict(plank="escape", art="schakel", pro=True, added="2026-09-06",
      nl=("De Schakelkamer", "Codes en documenten uit een atelier, 1963.", "schakelkamer.html"),
      en=("The Switch Room", "Ciphers and documents from a studio, 1963.", "the-switch-room.html")),
 dict(plank="escape", art="raaf", pro=True, added="2026-09-07",
      nl=("Ravenhorst", "Elk vertrek van het landhuis verbergt een raadsel.", "ravenhorst.html"),
      en=("Ravenscourt", "Every room of the manor hides a riddle.", "ravenscourt.html")),
 dict(plank="escape", art="ster", pro=True, added="2026-09-08",
      nl=("De Lichttafel", "Het antwoord ligt tussen de fotoplaten.", "de-lichttafel.html"),
      en=("The Light Table", "The answer lies among the photographic plates.", "the-light-table.html")),
 # Logica & raster
 dict(plank="logica", art="portier", pro=False, added="2026-09-09",
      nl=("De Nachtportier", "Vijf plattegronden. Eén portier die te veel wist.", "nachtportier.html"),
      en=("The Night Porter", "Five floor plans. One porter who knew too much.", "the-night-porter.html")),
 dict(plank="logica", art="hotel", pro=False, added="2026-09-29",
      nl=("Hotel Winterlicht", "Elf kamers, elf moordpuzzels, één gang.", "hotel-winterlight.html#nl"),
      en=("Hotel Winterlight", "Eleven rooms, eleven murder puzzles, one corridor.", "hotel-winterlight.html#en")),
 dict(plank="logica", art="boek", pro=False, added="2026-10-06",
      nl=("Het Pandjesboek", "3.113 namen. Streep weg tot er één overblijft.", "the-pawnbrokers-ledger.html#nl"),
      en=("The Pawnbroker’s Ledger", "3,113 names. Strike until one is left.", "the-pawnbrokers-ledger.html#en")),
 dict(plank="logica", art="krant", pro=False, added="2026-10-07",
      nl=("De Zwarte Kolom", "Drie nachten, drie doden, één rooster.", "the-black-column.html#nl"),
      en=("The Black Column", "Three nights, three deaths, one grid.", "the-black-column.html#en")),
 dict(plank="logica", art="plan", pro=True, added="2026-09-10",
      nl=("Het Grondplan", "Wie waar stond bepaalt wie het deed.", "grondplan.html"),
      en=("The Floor Plan", "Where everyone stood decides who did it.", "the-floor-plan.html")),
 # Cozy & bouwen
 dict(plank="cozy", art="match", pro=False, added="2026-10-17",
      nl=("Enigma Match", "Drie kaartjes op een rij. Eén kamer licht op.", "enigma-match.html#nl"),
      en=("Enigma Match", "Three cards in a row. One room lights up.", "enigma-match.html#en")),
 dict(plank="cozy", art="erfenis", pro=False, added="2026-10-10",
      nl=("De Nalatenschap", "Een zwak hart, zei de dokter. Het briefje op zolder zegt iets anders.", "the-inheritance.html#nl"),
      en=("The Inheritance", "A weak heart, the doctor said. The note in the attic disagrees.", "the-inheritance.html#en")),
 dict(plank="cozy", art="dorp", pro=False, added="2026-10-11",
      nl=("Het Zwijgende Dorp", "Bouw het dorp op. Eén van wie terugkeert, liegt.", "the-silent-village.html#nl"),
      en=("The Silent Village", "Rebuild the village. One of those who return is lying.", "the-silent-village.html#en")),
 dict(plank="cozy", art="bureau", pro=True, added="2026-10-12",
      nl=("Afdeling Moord", "Eén kelderbureau. Twaalf moorden. Bouw je afdeling.", "the-homicide-desk.html#nl"),
      en=("The Homicide Desk", "One basement desk. Twelve murders. Build the squad.", "the-homicide-desk.html#en")),
]

PLANKEN = [
 ("verhaal", {"nl": ("Verhaalzaken", "Verhoor de verdachten, zoek het bewijs, dien je aanklacht in."),
              "en": ("Story cases", "Question the suspects, find the evidence, file your charge.")}),
 ("escape",  {"nl": ("Escape & 3D", "Kijk zelf rond, kraak de sloten, vind de uitweg."),
              "en": ("Escape & 3D", "Look around for yourself, crack the locks, find the way out.")}),
 ("logica",  {"nl": ("Logica & raster", "Pen-en-papierpuzzels op het scherm. Eén oplossing, precies genoeg aanwijzingen."),
              "en": ("Logic & grids", "Pen-and-paper puzzles on screen. One solution, exactly enough clues.")}),
 ("cozy",    {"nl": ("Cozy & bouwen", "Rustig spelen zonder klok. Er zit wel een echte zaak onder."),
              "en": ("Cozy & building", "Play at your own pace, no clock. There is a real case underneath.")}),
]

NIEUW = sorted(range(len(SPELLEN)), key=lambda i: SPELLEN[i]["added"], reverse=True)[:3]

# --------------------------------------------------------------------------
# Paden en taal
# --------------------------------------------------------------------------
PAD = {  # sleutel -> (nl-pad, en-pad), relatief aan de root
 "home":   ("nl/", "en/"),
 "spellen":("nl/spellen/", "en/games/"),
 "wandel": ("nl/wandelingen/", "en/walks/"),
 "boeken": ("nl/puzzels/", "en/puzzles/"),
 "pro":    ("nl/pro/", "en/pro/"),
 "over":   ("nl/over/", "en/about/"),
 "contact":("nl/contact/", "en/contact/"),
}
MENU = [("spellen", "Spellen", "Games"), ("wandel", "Wandelingen", "Walks"), ("boeken", "Puzzels", "Puzzles"), ("mini", "Mini", "Mini"), ("pro", "Pro", "Pro"), ("contact", "Contact", "Contact")]

def pad(key, lang):
    return PAD[key][0 if lang == "nl" else 1]

def rel(frm, to):
    """relatief pad van map 'frm' (bv. 'nl/spellen/') naar 'to' (vanaf root)."""
    diepte = frm.count("/")
    return "../" * diepte + to

T = {
 "nl": dict(
   zin="Moordmysteries om te spelen, te lopen en te lezen.",
   naarspellen="Bekijk de spellen", naarwandel="Ga op moordwandeling",
   nieuw="Nieuw", nieuwzin="Net binnengekomen op het bureau.",
   deuren="Het bewijsbord", deurenzin="Vier sporen, één naam.",
   deurenuitleg="Online op je scherm, buiten op de been, op papier met een potlood, of samen met de kleintjes. Trek aan een draad.",
   gratis="Gratis", pro="Pro", nieuwstempel="Nieuw",
   alles="Alles", alleengratis="Gratis", alleenpro="Pro",
   footzin="Fictieve zaken. Echte puzzels. Elke zaak heeft precies één oplossing.",
   privacy="Privacy", notitie="Laat een notitie achter", overlink="Over Enigma Mystery",
 ),
 "en": dict(
   zin="Murder mysteries to play, to walk and to read.",
   naarspellen="Browse the games", naarwandel="Go on a murder walk",
   nieuw="New", nieuwzin="Just in on the desk.",
   deuren="The evidence board", deurenzin="Four leads, one name.",
   deurenuitleg="Online on your screen, outdoors on foot, on paper with a pencil, or together with the little ones. Pull a thread.",
   gratis="Free", pro="Pro", nieuwstempel="New",
   alles="All", alleengratis="Free", alleenpro="Pro",
   footzin="Fictional cases. Real puzzles. Every case has exactly one solution.",
   privacy="Privacy", notitie="Leave a note", overlink="About Enigma Mystery",
 ),
}

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Cormorant+Garamond:wght@600;700&family=Spectral:ital,wght@0,400;0,500;1,400&display=swap">')

def head(lang, key, title, desc, here):
    other = "en" if lang == "nl" else "nl"
    r = lambda p: rel(here, p)
    canon = SITE + "/" + pad(key, lang)
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="{lang}" href="{canon}">
<link rel="alternate" hreflang="{other}" href="{SITE}/{pad(key, other)}">
<link rel="alternate" hreflang="x-default" href="{SITE}/">
<meta property="og:site_name" content="Enigma Mystery">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:type" content="website">
<meta property="og:image" content="{SITE}/assets/deelbeeld.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0d0a07">
<link rel="icon" href="{r('favicon.ico')}" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{r('assets/favicon-32.png')}">
<link rel="apple-touch-icon" href="{r('assets/apple-touch-icon.png')}">
<link rel="manifest" href="{r('site.webmanifest')}">
{FONTS}
<link rel="stylesheet" href="{r('assets/site.css')}">
</head>
<body data-lang="{lang}">
"""

def kopbalk(lang, key, here):
    r = lambda p: rel(here, p)
    items = []
    for k, nl, en in MENU:
        cur = ' aria-current="page"' if k == key else ""
        cls = ' class="pro"' if k == "pro" else ""
        href, ext = (MINI, ' rel="noopener"') if k == "mini" else (r(pad(k, lang)), "")
        items.append(f'<a href="{href}"{ext}{cls}{cur}>{nl if lang == "nl" else en}</a>')
    other = "en" if lang == "nl" else "nl"
    wissel = (f'<span>NL</span><a href="{r(pad(key, other))}" data-kies-taal="en" hreflang="en">EN</a>' if lang == "nl"
              else f'<a href="{r(pad(key, other))}" data-kies-taal="nl" hreflang="nl">NL</a><span>EN</span>')
    return f"""<header class="kopbalk"><div class="binnen">
<a class="merk" href="{r(pad('home', lang))}" aria-label="Enigma Mystery"><img src="{r('assets/icon-192.png')}" alt="" width="192" height="192"><span class="woordmerk"><b>Enigma</b> Mystery</span></a>
<nav class="menu" aria-label="{'Hoofdmenu' if lang == 'nl' else 'Main menu'}">{''.join(items)}<div class="taalwissel" role="group" aria-label="{'Taal' if lang == 'nl' else 'Language'}">{wissel}</div></nav>
</div></header>
<main>
"""

def voet(lang, here):
    r = lambda p: rel(here, p)
    t = T[lang]
    links = [(pad("spellen", lang), "Spellen" if lang == "nl" else "Games"),
             (pad("wandel", lang), "Wandelingen" if lang == "nl" else "Walks"),
             (pad("boeken", lang), "Mystery Puzzels" if lang == "nl" else "Mystery Puzzles"),
             (MINI, "Mini Mystery"),
             (pad("pro", lang), "Pro"),
             (pad("over", lang), t["overlink"]),
             (pad("contact", lang), "Contact"),
             (pad("over", lang) + "#privacy", t["privacy"])]
    nav = "".join(f'<a href="{p if p.startswith("http") else r(p)}"{" rel=\"noopener\"" if p.startswith("http") else ""}>{escape(n)}</a>' for p, n in links)
    return f"""</main>
<footer class="voet"><div class="binnen">
<span class="woordmerk"><b>Enigma</b> Mystery</span>
<nav aria-label="{'Onderaan' if lang == 'nl' else 'Footer'}">{nav}</nav>
<p class="klein">{t['footzin']} &middot; &copy; {date.today().year} Enigma Mystery</p>
</div></footer>
<script src="{r('assets/site.js')}" defer></script>
</body>
</html>
"""

def spel_url(s, lang, here):
    return rel(here, "spel/" + s[lang][2])

def kaart(i, lang, here, nieuw_stempel=True):
    s = SPELLEN[i]
    titel, haak, _ = s[lang]
    t = T[lang]
    plaknaam = dict(PLANKEN)[s["plank"]][lang][0]
    stempels = f'<span class="stempel {"pro" if s["pro"] else "gratis"}">{t["pro"] if s["pro"] else t["gratis"]}</span>'
    if nieuw_stempel and i in NIEUW:
        stempels += f'<span class="stempel nieuw">{t["nieuwstempel"]}</span>'
    return (f'<a class="dossier" href="{spel_url(s, lang, here)}" data-pro="{1 if s["pro"] else 0}">'
            f'<div class="foto"><img src="{rel(here, "assets/dossiers/" + s["art"] + ".jpg")}" alt="" loading="lazy" decoding="async"></div>'
            f'<div class="tekst"><span class="soort">{escape(plaknaam)}</span><h3>{escape(titel)}</h3><p>{escape(haak)}</p></div>{stempels}</a>')

def schrijf(path, html):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html, encoding="utf-8")

def held(here, lang, inhoud, klein=False, smal=None):
    r = lambda p: rel(here, p)
    smal = smal or "assets/achtergrond-smal.jpg"
    return f"""<section class="held{' klein' if klein else ''}">
<picture><source media="(max-width:640px)" srcset="{r(smal)}"><img src="{r('assets/achtergrond.jpg')}" alt="" fetchpriority="high"></picture>
<div class="binnen">{inhoud}</div></section>
"""

# --------------------------------------------------------------------------
# Pagina's
# --------------------------------------------------------------------------
def voorpagina(lang):
    here = pad("home", lang); r = lambda p: rel(here, p); t = T[lang]
    title = "Enigma Mystery" + (" · Moordmysteries om te spelen, te lopen en te lezen" if lang == "nl" else " · Murder mysteries to play, walk and read")
    desc = ("Online moordspellen, moordwandelingen door je eigen stad en puzzelboeken. Fictieve zaken met precies één oplossing; van elke soort is de eerste zaak gratis."
            if lang == "nl" else
            "Online murder mystery games, murder walks through your own town and puzzle books. Fictional cases with exactly one solution; the first case of every kind is free.")
    nl_ = lang == "nl"
    deuren = [
      ("spellen", pad("spellen", lang), "online", "scherm", "assets/deur-spellen.jpg", -2.2,
       ("Online", "Mystery Spellen", "Speel in je browser", f"{len(SPELLEN)} zaken: verhalen, escape rooms in 3D, logicapuzzels en rustige bouwspellen.",
        [("Waar", "Op telefoon of computer"), ("Duur", "20 minuten tot een paar avonden"), ("Prijs", "Van elke soort één zaak gratis, de rest met Pro")], "Naar de spellen"),
       ("Online", "Mystery Games", "Play in your browser", f"{len(SPELLEN)} cases: stories, 3D escape rooms, logic puzzles and calm building games.",
        [("Where", "On your phone or computer"), ("Time", "20 minutes to a few evenings"), ("Price", "One case of every kind free, the rest with Pro")], "To the games")),
      ("wandel", pad("wandel", lang), "buiten", "voet", "assets/deur-wandelingen.jpg", 1.6,
       ("Buiten", "Mystery Wandelingen", "Loop de zaak zelf", "Een moordzaak die je buiten oplost. De stad om je heen wordt de plaats delict.",
        [("Waar", "Overal, met je telefoon in de hand"), ("Duur", "Ongeveer anderhalf uur"), ("Prijs", "Proefwandeling gratis; verhalen en groepspas los te koop")], "Naar de wandelingen"),
       ("Outdoors", "Mystery Walks", "Walk the case yourself", "A murder case you solve outside. The town around you becomes the crime scene.",
        [("Where", "Anywhere, phone in hand"), ("Time", "About ninety minutes"), ("Price", "Trial walk free; stories and group pass sold separately")], "To the walks")),
      ("boeken", pad("boeken", lang), "papier", "boek", "assets/deur-puzzels.jpg", -1.4,
       ("Op papier", "Mystery Puzzels", "Puzzelen met potlood", "Gedrukte puzzelboeken vol moordzaken, van makkelijk naar moeilijk.",
        [("Waar", "Aan tafel, in de trein, op vakantie"), ("Duur", "100 puzzels per boek"), ("Prijs", "Paperback via Amazon; één verdieping gratis online")], "Naar de puzzels"),
       ("On paper", "Mystery Puzzles", "Puzzle with a pencil", "Printed puzzle books full of murder cases, from easy to hard.",
        [("Where", "At the table, on the train, on holiday"), ("Time", "100 puzzles per book"), ("Price", "Paperback on Amazon; one floor free online")], "To the puzzles")),
      ("mini", MINI, "mini", "ster", "assets/deur-mini.jpg", 2.4,
       ("Voor de kleintjes", "Mini Mystery", "Speuren zonder moord", "Raadsels en speurtochten voor jonge detectives, op een eigen site.",
        [("Waar", "minimystery.nl"), ("Voor wie", "Kinderen, samen met een grote"), ("Prijs", "Zie de Mini-site")], "Naar Mini Mystery"),
       ("For the little ones", "Mini Mystery", "Sleuthing without murder", "Riddles and treasure hunts for young detectives, on a site of its own.",
        [("Where", "minimystery.nl"), ("For whom", "Children, together with a grown-up"), ("Price", "See the Mini site")], "To Mini Mystery")),
    ]
    IC = {
      "scherm": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="4" width="18" height="12" rx="1.5"/><path d="M8 20h8M12 16v4"/></svg>',
      "voet": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 3c2 0 3 2 3 5s-1 4-2 5-3 0-3-3 0-7 2-7zM7 14c1.5 0 2 1 2 2.5S8.5 19 7.5 19 6 18 6 16.5 6 14 7 14zM17 7c-2 0-3 2-3 5s1 4 2 5 3 0 3-3 0-7-2-7zM17 18c-1.5 0-2 1-2 2.5"/></svg>',
      "boek": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 4h6a3 3 0 0 1 3 3v13a2 2 0 0 0-2-2H4zM20 4h-6a3 3 0 0 0-3 3v13a2 2 0 0 1 2-2h7z"/></svg>',
      "ster": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l2.6 5.6 6.1.7-4.5 4.2 1.2 6-5.4-3-5.4 3 1.2-6L3.3 9.3l6.1-.7z"/></svg>',
    }
    def deur(n, k, href, kleur, ic, img, hoek, d):
        wijze, naam, kop, zin, feiten, knop = d
        feit_html = "".join(f'<div><dt>{escape(a)}</dt><dd>{escape(b)}</dd></div>' for a, b in feiten)
        ext = ' rel="noopener"' if href.startswith("http") else ""
        return (f'<a class="deur {kleur}" style="--hoek:{hoek}deg" href="{href if href.startswith("http") else r(href)}"{ext}><span class="punaise" aria-hidden="true"></span>'
                f'<div class="deurbeeld"><img src="{r(img)}" alt="" loading="lazy"></div>'
                f'<div class="deurtekst"><span class="wijze">{IC[ic]}{escape(wijze)}</span><h3>{escape(naam)}</h3><p class="kop">{escape(kop)}</p><p>{escape(zin)}</p>'
                f'<dl class="feiten">{feit_html}</dl><span class="pijl">{escape(knop)} &rarr;</span></div></a>')
    deur_html = "".join(deur(n, *d[:6], d[6] if nl_ else d[7]) for n, d in enumerate(deuren))
    draad = ('<svg class="draad" viewBox="0 0 1000 100" preserveAspectRatio="none" aria-hidden="true">'
             '<path d="M125 40 C 290 92, 460 4, 625 58 S 790 96, 875 40" fill="none" stroke="var(--lak)" stroke-width="2.2" stroke-linecap="round"/>'
             '<path d="M125 40 L 375 62 L 625 58 L 875 40" fill="none" stroke="var(--lak)" stroke-width="1.4" stroke-dasharray="4 7" opacity=".7"/></svg>')
    nieuw = "".join(kaart(i, lang, here, nieuw_stempel=False) for i in NIEUW)
    gratis_zin = ("Op elke plank is minstens één zaak gratis. Met de Pro-pas gaan alle verzegelde dossiers open."
                  if lang == "nl" else "Every shelf has at least one free case. The Pro pass opens every sealed file.")
    body = f"""<section class="held hoofd">
<div class="vul" aria-hidden="true"></div>
<picture class="beeld"><source media="(max-width:640px)" srcset="{r('assets/hero-logo-vierkant.jpg')}"><img src="{r('assets/hero-logo.jpg')}" alt="Enigma Mystery · Unlock the mystery" fetchpriority="high" width="1536" height="1024"></picture>
<span class="lamp" aria-hidden="true"></span>
<div class="binnen">
<h1 class="verborgen">Enigma Mystery</h1>
<p class="zin typ" data-tekst="{escape(t['zin'])}">{t['zin']}</p>
<div class="knoppen"><a class="knop" href="{r(pad('spellen', lang))}">{t['naarspellen']}</a><a class="knop lijn" href="{r(pad('wandel', lang))}">{t['naarwandel']}</a></div>
</div></section>
"""
    body += f"""<section class="sectie"><div class="binnen">
<div class="sectiekop"><span class="label">{t['deuren']}</span><h2>{t['deurenzin']}</h2><p class="zacht">{t['deurenuitleg']}</p></div>
<div class="bord"><div class="deuren">{deur_html}</div>{draad}</div></div></section>
<section class="sectie"><div class="binnen">
<div class="sectiekop"><span class="label">{t['nieuw']}</span><h2>{t['nieuwzin']}</h2></div>
<div class="rij">{nieuw}</div></div></section>
"""
    schrijf(here + "index.html", head(lang, "home", title, desc, here) + kopbalk(lang, "home", here) + body + voet(lang, here))

def spellenpagina(lang):
    here = pad("spellen", lang); t = T[lang]
    title = ("Spellen · Enigma Mystery" if lang == "nl" else "Games · Enigma Mystery")
    desc = ("Alle online moordmysteries van Enigma Mystery: verhaalzaken, escape rooms in 3D, logicapuzzels en cozy bouwspellen. Speel in je browser, zonder account."
            if lang == "nl" else
            "Every online murder mystery on Enigma Mystery: story cases, 3D escape rooms, logic puzzles and cozy building games. Play in your browser, no account needed.")
    intro = ("Alle zaken spelen in je browser, op telefoon en computer. Geen account nodig; je voortgang blijft op je eigen apparaat."
             if lang == "nl" else
             "Every case plays in your browser, on phone and computer. No account needed; your progress stays on your own device.")
    kop = held(here, lang, f'<span class="label">{"Online" if lang == "nl" else "Online"}</span><h1>{"Mystery Spellen" if lang == "nl" else "Mystery Games"}</h1><p class="zin">{intro}</p>', klein=True,
               smal="assets/dossiers/telefoon.jpg")
    filt = (f'<div class="filters" role="group" aria-label="Filter"><button type="button" data-filter="alles" aria-pressed="true">{t["alles"]}</button>'
            f'<button type="button" data-filter="gratis" aria-pressed="false">{t["alleengratis"]}</button>'
            f'<button type="button" data-filter="pro" aria-pressed="false">{t["alleenpro"]}</button></div>')
    planken = ""
    for key, namen in PLANKEN:
        idx = [i for i, s in enumerate(SPELLEN) if s["plank"] == key]
        idx.sort(key=lambda i: (SPELLEN[i]["pro"], -int(SPELLEN[i]["added"].replace("-", ""))))
        naam, zin = namen[lang]
        planken += (f'<section class="plank" id="{key}"><div class="sectiekop"><span class="label">{len(idx)} {"zaken" if lang == "nl" else "cases"}</span><h2>{escape(naam)}</h2><p class="zacht">{escape(zin)}</p></div>'
                    f'<div class="rij">{"".join(kaart(i, lang, here) for i in idx)}</div></section>')
    body = kop + f'<section class="sectie"><div class="binnen">{filt}{planken}</div></section>\n'
    schrijf(here + "index.html", head(lang, "spellen", title, desc, here) + kopbalk(lang, "spellen", here) + body + voet(lang, here))

def wandelpagina(lang):
    here = pad("wandel", lang); r = lambda p: rel(here, p)
    nl = lang == "nl"
    title = "Moordwandelingen · Enigma Mystery" if nl else "Murder walks · Enigma Mystery"
    desc = ("Een moordmysterie dat je buiten oplost: loop door je eigen stad, verzamel bewijs, verhoor schaduwfiguren en wijs de dader aan. Ongeveer anderhalf uur, alleen of met een groep."
            if nl else
            "A murder mystery you solve outdoors: walk through your own town, collect evidence, question shadow figures and name the killer. About ninety minutes, alone or with a group.")
    app = WANDEL[lang]
    kop = held(here, lang, f"""<span class="label">{"Buiten" if nl else "Outdoors"}</span><h1>{"Mystery Wandelingen" if nl else "Mystery Walks"}</h1>
<p class="zin">{"Een moordzaak die je met je voeten oplost. De stad om je heen wordt de plaats delict." if nl else "A murder case you solve on foot. The town around you becomes the crime scene."}</p>
<div class="knoppen"><a class="knop" href="{app}" rel="noopener">{"Start de wandeling" if nl else "Start the walk"}</a></div>""", klein=True)
    stappen = ([("Kies een verhaal", "Begin met de gratis proefwandeling of kies een Pro-verhaal. De app gebruikt gewone plekken om je heen: een kerk, een bank, een hotel."),
                ("Loop en verzamel", "Op de kaart verschijnen schaduwfiguren met informatie. Loop ernaartoe, vind het bewijs, los de minipuzzels op en verhoor de verdachten."),
                ("Wijs de dader aan", "Na ongeveer anderhalf uur heb je genoeg. Eén verdachte liegt. Klopt je aanklacht?")]
               if nl else
               [("Pick a story", "Start with the free trial walk or choose a Pro story. The app uses ordinary places around you: a church, a bank, a hotel."),
                ("Walk and collect", "Shadow figures with information appear on the map. Walk up to them, find the evidence, solve the mini-puzzles and question the suspects."),
                ("Name the killer", "After about ninety minutes you have enough. One suspect is lying. Does your charge hold?")])
    stap_html = "".join(f"<li><h3>{a}</h3><p>{b}</p></li>" for a, b in stappen)
    blokken = ([("Gratis proefwandeling", ["Speel overal, ook bij jou om de hoek", "Proefroute door de binnenstad van Eindhoven", "Geen account nodig"]),
                ("Pro-verhalen", ["Meerdere complete zaken", "Verhoren en gebeurtenissen onderweg op tijd", "Eenmalig kopen, blijft open op je telefoon"]),
                ("Samen of tegen elkaar", ["Groepsspel: Samen of Teams tegen elkaar", "Misleid de andere groep", "Groepspas voor maximaal 10 spelers, 48 uur geldig"])]
               if nl else
               [("Free trial walk", ["Play anywhere, even around the corner", "Trial route through Eindhoven city centre", "No account needed"]),
                ("Pro stories", ["Several complete cases", "Interrogations and timed events along the route", "Buy once, stays open on your phone"]),
                ("Together or against each other", ["Group play: Together or Teams against each other", "Mislead the other group", "Group pass for up to 10 players, valid for 48 hours"])])
    blok_html = "".join(f'<div class="blok"><h3>{a}</h3><ul>{"".join(f"<li>{x}</li>" for x in b)}</ul></div>' for a, b in blokken)
    body = kop + f"""<section class="sectie"><div class="binnen">
<div class="sectiekop"><span class="label">{"Zo werkt het" if nl else "How it works"}</span><h2>{"Drie stappen, één dader" if nl else "Three steps, one killer"}</h2></div>
<ol class="stappen">{stap_html}</ol></div></section>
<section class="sectie"><div class="binnen"><div class="twee">{blok_html}</div>
<p style="margin-top:28px"><a class="knop" href="{app}" rel="noopener">{"Open de wandel-app" if nl else "Open the walk app"}</a></p></div></section>
"""
    schrijf(here + "index.html", head(lang, "wandel", title, desc, here) + kopbalk(lang, "wandel", here) + body + voet(lang, here))

BOEKEN = [
 dict(id={"nl": "moord-op-het-uur", "en": "murder-by-the-hour"}, status="uit",
      nl=("Moord op het uur", "Gongoku · 100 moordpuzzels op de plattegrond",
          "Een landhuis, een gong die elk uur slaat, en een moord die op de plattegrond te reconstrueren is. Honderd puzzels in vijf huizen, oplopend van 4×4 tot 8×8. De beginletters van de daders vormen per hoofdstuk het gif.",
          "Paperback bij Amazon", "https://www.amazon.nl/s?k=Moord+op+het+uur+Gongoku"),
      en=("Murder by the Hour", "Gongoku · 100 murder puzzles on the floor plan",
          "A country house, a gong that strikes every hour, and a murder you can reconstruct on the floor plan. One hundred puzzles across five houses, from 4×4 up to 8×8. Each chapter's killers spell out the poison.",
          "Paperback on Amazon", "https://www.amazon.com/s?k=Murder+by+the+Hour+Gongoku")),
 dict(id={"nl": "hotel-winterlicht", "en": "hotel-winterlight"}, status="binnenkort",
      nl=("Hotel Winterlicht", "Twaalf verdiepingen en een geheime dertiende",
          "Een hotel vol moordpuzzels van tien soorten. Elke kamer levert een sleutel die een andere kamer opent, en wie alle twaalf verdiepingen kraakt, vindt de lift naar de dertiende. 138 kamers, van makkelijk naar moeilijk.",
          "Speel verdieping 7 gratis", None),
      en=("Hotel Winterlight", "Twelve floors and a secret thirteenth",
          "A hotel full of murder puzzles of ten kinds. Every room yields a key that opens another room, and whoever cracks all twelve floors finds the lift to the thirteenth. 138 rooms, from easy to hard.",
          "Play floor 7 for free", None)),
 dict(id={"nl": "voetsporen", "en": "footprints"}, status="maak",
      nl=("Voetsporen", "Moordpuzzels in de sneeuw", "Verse sneeuw verraadt wie waar heeft gelopen. Volg de sporen en reconstrueer de nacht.", None, None),
      en=("Footprints", "Murder puzzles in the snow", "Fresh snow gives away who walked where. Follow the tracks and reconstruct the night.", None, None)),
 dict(id={"nl": "alibi-net", "en": "alibi-web"}, status="maak",
      nl=("Het Alibi-net", "Eén leugenaar per zaak", "Iedereen geeft een alibi. Alleen de dader liegt. Leg de verklaringen naast elkaar tot er één niet meer past.", None, None),
      en=("The Alibi Web", "One liar per case", "Everyone gives an alibi. Only the killer lies. Lay the statements side by side until one no longer fits.", None, None)),
]

def boekenpagina(lang):
    here = pad("boeken", lang); r = lambda p: rel(here, p); nl = lang == "nl"
    title = "Puzzelboeken · Enigma Mystery" if nl else "Puzzle books · Enigma Mystery"
    desc = ("Moordpuzzelboeken van Enigma Mystery: Moord op het uur, Hotel Winterlicht en meer. Van makkelijk naar moeilijk, met potlood en geduld."
            if nl else "Murder puzzle books from Enigma Mystery: Murder by the Hour, Hotel Winterlight and more. From easy to hard, with pencil and patience.")
    statusnaam = {"uit": "Verschenen" if nl else "Out now", "binnenkort": "Binnenkort" if nl else "Coming soon", "maak": "In de maak" if nl else "In the works"}
    items = ""
    for b in BOEKEN:
        titel, sub, tekst, knop, url = b[lang]
        if b["id"]["nl"] == "hotel-winterlicht":
            url = r("spel/hotel-winterlight.html#" + lang)
        knop_html = f'<p><a class="knop{" lijn" if b["status"] != "uit" else ""}" href="{url}" rel="noopener">{knop}</a></p>' if knop else ""
        items += (f'<article class="boek" id="{b["id"][lang]}"><div class="omslag"><div><span>{escape(titel)}</span><small>Enigma Mystery</small></div></div>'
                  f'<div class="info"><span class="status {b["status"]}">{statusnaam[b["status"]]}</span><h2>{escape(titel)}</h2>'
                  f'<p class="label" style="letter-spacing:.14em">{escape(sub)}</p><p class="zacht">{escape(tekst)}</p>{knop_html}</div></article>')
    kop = held(here, lang, f'<span class="label">{"Op papier" if nl else "On paper"}</span><h1>{"Mystery Puzzels" if nl else "Mystery Puzzles"}</h1><p class="zin">{"Moordpuzzels op papier. Elk boek begint makkelijk en eindigt moeilijk." if nl else "Murder puzzles on paper. Every book starts easy and ends hard."}</p>',
               klein=True, smal="assets/boeken.jpg")
    body = kop + f'<section class="sectie"><div class="binnen">{items}</div></section>\n'
    schrijf(here + "index.html", head(lang, "boeken", title, desc, here) + kopbalk(lang, "boeken", here) + body + voet(lang, here))

def propagina(lang):
    here = pad("pro", lang); r = lambda p: rel(here, p); nl = lang == "nl"
    title = "Pro-pas · Enigma Mystery" if nl else "Pro pass · Enigma Mystery"
    desc = ("Eén Pro-pas opent alle verzegelde dossiers van Enigma Mystery op je apparaat." if nl
            else "One Pro pass opens every sealed Enigma Mystery file on your device.")
    pro_lijst = "".join(f'<li><a href="{spel_url(s, lang, here)}">{escape(s[lang][0])}</a></li>' for s in SPELLEN if s["pro"])
    n_pro = sum(1 for s in SPELLEN if s["pro"])
    kop = held(here, lang, f'<span class="label" style="color:var(--lak-licht)">Pro</span><h1>{"De Pro-pas" if nl else "The Pro pass"}</h1><p class="zin">{(f"Eén pas opent alle {n_pro} verzegelde dossiers." if nl else f"One pass opens all {n_pro} sealed files.")}</p><div class="knoppen"><a class="knop lak" href="{KOFI_PRO}" rel="noopener">{"Haal de Pro-pas" if nl else "Get the Pro pass"}</a></div>', klein=True)
    stappen = ([("Koop de pas", "Via Ko-fi. Je krijgt direct een pascode."), ("Vul de code in", "Hieronder, of in een verzegeld dossier zelf."), ("Speel alles", "De code wordt op dit apparaat onthouden. Op een ander apparaat vul je hem één keer opnieuw in.")]
               if nl else [("Buy the pass", "Through Ko-fi. You get a pass code right away."), ("Enter the code", "Below, or inside any sealed file."), ("Play everything", "The code is remembered on this device. On another device you enter it once more.")])
    body = kop + f"""<section class="sectie"><div class="binnen twee">
<div class="blok"><h3>{"Wat Pro opent" if nl else "What Pro opens"}</h3><ul>{pro_lijst}</ul></div>
<form class="pas" id="proForm" autocomplete="off">
<span class="label" style="color:#8e2b20">{"Pascode" if nl else "Pass code"}</span>
<h2>{"Heb je al een code?" if nl else "Already have a code?"}</h2>
<p id="proStand">{"Vul hem hier in. Alle verzegelde dossiers gaan dan open op dit apparaat." if nl else "Enter it here. Every sealed file then opens on this device."}</p>
<label for="proCode">{"Pascode" if nl else "Pass code"}</label>
<input id="proCode" name="code" inputmode="text" autocapitalize="characters" autocorrect="off" spellcheck="false" maxlength="40">
<button class="knop lak" type="submit">{"Controleer en bewaar" if nl else "Check and save"}</button>
<p class="melding" id="proMelding" role="status" aria-live="polite"></p>
</form>
</div></section>
<script>window.MM_PRO={{probe:"{r('spel/night-frequency.html')}",t:{json.dumps({
    "kort": "Die code is te kort." if nl else "That code is too short.",
    "bezig": "Bezig met controleren…" if nl else "Checking…",
    "ok": "Gelukt. Alle verzegelde dossiers zijn open op dit apparaat." if nl else "Done. Every sealed file is open on this device.",
    "fout": "Die code opent de dossiers niet. Controleer op typfouten." if nl else "That code doesn’t open the files. Check for typos.",
    "actief": "Je Pro-pas is actief op dit apparaat." if nl else "Your Pro pass is active on this device.",
    "offline": "Controleren lukt nu niet. De code is bewaard; open een verzegeld dossier om hem te proberen." if nl else "Can’t check right now. The code is saved; open a sealed file to try it."
}, ensure_ascii=False)}}};</script>
"""
    schrijf(here + "index.html", head(lang, "pro", title, desc, here) + kopbalk(lang, "pro", here) + body + voet(lang, here))

def overpagina(lang):
    here = pad("over", lang); r = lambda p: rel(here, p); nl = lang == "nl"
    title = "Over Enigma Mystery" if nl else "About Enigma Mystery"
    desc = ("Wie er achter Enigma Mystery zit, hoe je een notitie achterlaat en hoe er met je gegevens wordt omgegaan." if nl
            else "Who is behind Enigma Mystery, how to leave a note and how your data is handled.")
    if nl:
        over = ("Enigma Mystery bundelt alle moordmysteries die eerder verschenen als Het Nachtdossier, The Graveyard Files, Moordwandeling en Murder Walk. "
                "Elke zaak is verzonnen, elke puzzel is nagerekend: er is precies één oplossing en de aanwijzingen geven je precies genoeg.")
        priv = [("De spellen", "Alles draait in je browser. Je voortgang, gebruikte tips, je taalkeuze en je Pro-code staan in de lokale opslag van je eigen browser. Ze verlaten je apparaat niet; als je je browsergegevens wist, zijn ze weg. Geen cookies, geen statistieken, geen tracking."),
                ("Het notitieformulier", "Alleen als je een notitie stuurt, ontvangen wij wat je typte: je bericht, en je naam en e-mailadres als je die invulde. Het komt binnen als e-mail via FormSubmit, dat je bericht daarna niet bewaart. We gebruiken het alleen om te lezen en te antwoorden, en delen het met niemand."),
                ("Hosting", "De site staat op GitHub Pages, dat zoals elke webhost IP-adressen logt voor beveiliging. Wij zien of gebruiken die logs niet."),
                ("De Pro-pas", "Aankopen lopen via Ko-fi, onder de privacyvoorwaarden van Ko-fi. Er komt niets over je aankoop terug naar deze site."),
                ("Wie is verantwoordelijk", f"Kellie van de Kerkhof, bereikbaar via {NOTITIE_ADRES}. Je mag vragen wat we van je hebben, het laten verbeteren of verwijderen, of een klacht indienen bij de Autoriteit Persoonsgegevens.")]
    else:
        over = ("Enigma Mystery brings together every murder mystery that appeared earlier as The Graveyard Files, Het Nachtdossier, Murder Walk and Moordwandeling. "
                "Every case is fiction, every puzzle is checked: there is exactly one solution and the clues give you exactly enough.")
        priv = [("The games", "Everything runs in your browser. Your progress, hints used, your language and your Pro code are kept in your own browser's local storage. They never leave your device; clearing your browser data removes them. No cookies, no analytics, no tracking."),
                ("The note form", "Only if you send a note do we receive what you typed: your message, and your name and e-mail address if you gave them. It arrives as an e-mail through FormSubmit, which does not keep your message afterwards. We use it only to read and reply, and share it with nobody."),
                ("Hosting", "The site is served by GitHub Pages, which, like any web host, logs IP addresses for security. We do not see or use those logs."),
                ("The Pro pass", "Purchases go through Ko-fi, under Ko-fi's own privacy terms. Nothing about a purchase comes back to this site."),
                ("Who is responsible", f"Kellie van de Kerkhof, reachable at {NOTITIE_ADRES}. Under the GDPR you may ask what we hold about you, have it corrected or deleted, or complain to the Dutch Data Protection Authority.")]
    priv_html = "".join(f"<p><b>{a}.</b> {escape(b)}</p>" for a, b in priv)
    form_t = {
        "naam": "Je naam (optioneel)" if nl else "Your name (optional)",
        "mail": "Antwoordadres (optioneel)" if nl else "Reply address (optional)",
        "bericht": "Je notitie" if nl else "Your note",
        "knop": "Verstuur" if nl else "Send",
    }
    body = f"""<section class="sectie"><div class="binnen twee">
<div style="display:grid;gap:16px;align-content:start;max-width:62ch"><span class="label">{"Over" if nl else "About"}</span><h1>Enigma Mystery</h1><p class="zacht">{escape(over)}</p></div>

</div></section>
<section class="sectie" id="privacy"><div class="binnen" style="display:grid;gap:14px;max-width:72ch"><span class="label">Privacy</span><h2>{"Hoe er met je gegevens wordt omgegaan" if nl else "How your data is handled"}</h2>{priv_html}</div></section>
"""
    schrijf(here + "index.html", head(lang, "over", title, desc, here) + kopbalk(lang, "over", here) + body + voet(lang, here))

def contactpagina(lang):
    here = pad("contact", lang); r = lambda p: rel(here, p); nl = lang == "nl"
    title = "Contact · Enigma Mystery"
    desc = ("Laat een notitie achter voor Enigma Mystery: een vraag, een foutje in een zaak, een idee." if nl
            else "Leave a note for Enigma Mystery: a question, a mistake in a case, an idea.")
    form_t = {
        "naam": "Je naam (optioneel)" if nl else "Your name (optional)",
        "mail": "Antwoordadres (optioneel)" if nl else "Reply address (optional)",
        "bericht": "Je bericht" if nl else "Your message",
        "knop": "Verstuur" if nl else "Send",
    }
    body = f"""<section class="sectie"><div class="binnen twee">
<div style="display:grid;gap:16px;align-content:start;max-width:52ch"><span class="label">Contact</span><h1>{"Laat een notitie achter" if nl else "Leave a note"}</h1>
<p class="zacht">{"Een vraag, een aanwijzing die niet klopte, een typfout, een zaak die je graag zou zien: alles is welkom en wordt gelezen." if nl else "A question, a clue that didn't hold, a typo, a case you would like to see: anything is welcome and gets read."}</p>
<p class="zacht">{"Liever mailen? " if nl else "Prefer e-mail? "}<a href="mailto:{NOTITIE_ADRES}">{NOTITIE_ADRES}</a></p></div>
<div><form class="formulier" id="notitieForm">
<label for="nNaam">{form_t['naam']}</label><input id="nNaam" name="name" autocomplete="name">
<label for="nMail">{form_t['mail']}</label><input id="nMail" name="email" type="email" autocomplete="email">
<label for="nBericht">{form_t['bericht']}</label><textarea id="nBericht" name="message" required></textarea>
<input class="verborgen" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">
<button class="knop" type="submit">{form_t['knop']}</button>
<p class="melding" id="notitieMelding" role="status" aria-live="polite"></p>
</form></div>
</div></section>
<script>window.MM_NOTITIE={{adres:"{NOTITIE_ADRES}",t:{json.dumps({
    "leeg": "De notitie is nog leeg." if nl else "The note is still blank.",
    "bezig": "Versturen…" if nl else "Sending…",
    "ok": "Verstuurd. Dank je wel." if nl else "Sent. Thank you.",
    "fout": "Versturen lukte niet." if nl else "Sending failed.",
    "mail": "Stuur hem per e-mail" if nl else "Send it by e-mail",
}, ensure_ascii=False)}}};</script>
"""
    schrijf(here + "index.html", head(lang, "contact", title, desc, here) + kopbalk(lang, "contact", here) + body + voet(lang, here))

def taalkeuze():
    html = f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Enigma Mystery · Kies je taal / Choose your language</title>
<meta name="description" content="Enigma Mystery: moordmysteries om te spelen, te lopen en te lezen. Murder mysteries to play, walk and read.">
<link rel="canonical" href="{SITE}/">
<link rel="alternate" hreflang="nl" href="{SITE}/nl/">
<link rel="alternate" hreflang="en" href="{SITE}/en/">
<link rel="alternate" hreflang="x-default" href="{SITE}/">
<meta property="og:site_name" content="Enigma Mystery">
<meta property="og:title" content="Enigma Mystery">
<meta property="og:description" content="Moordmysteries om te spelen, te lopen en te lezen. Murder mysteries to play, walk and read.">
<meta property="og:url" content="{SITE}/">
<meta property="og:image" content="{SITE}/assets/deelbeeld.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0d0a07">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<script>
(function(){{try{{var q=location.search.indexOf("kies")>-1;var l=localStorage.getItem("mm_lang");if(!q&&(l==="nl"||l==="en")){{location.replace(l+"/");}}}}catch(e){{}}}})();
</script>
{FONTS}
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<main class="kies">
<div class="vul" aria-hidden="true"></div>
<picture><source media="(max-aspect-ratio: 5/4)" srcset="assets/hero-logo-vierkant.jpg"><img src="assets/hero-logo.jpg" alt="Enigma Mystery · Unlock the mystery" fetchpriority="high"></picture>
<div class="kaart">
<h1 class="verborgen">Enigma Mystery</h1>
<p>Kies je taal &middot; Choose your language</p>
<div class="knoppen">
<a class="knop" href="nl/" data-kies-taal="nl" hreflang="nl">Nederlands</a>
<a class="knop" href="en/" data-kies-taal="en" hreflang="en">English</a>
</div>
</div>
</main>
<script src="assets/site.js" defer></script>
</body>
</html>
"""
    schrijf("index.html", html)

def doorstuur(path, doel_js, uitleg):
    schrijf(path, f"""<!DOCTYPE html>
<html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Enigma Mystery</title><meta name="robots" content="noindex">
<script>{doel_js}</script>
<style>body{{background:#0d0a07;color:#ecdfc4;font:17px Georgia,serif;display:grid;place-items:center;min-height:100vh;margin:0;padding:16px;text-align:center}}a{{color:#ecc77d}}</style>
</head><body><p>{uitleg}</p></body></html>
""")

def extra():
    # oude NL-bestandsnamen van samengevoegde spellen
    for oud, nieuw in (("de-zwarte-kolom", "the-black-column"), ("hotel-winterlicht", "hotel-winterlight")):
        doorstuur(f"spel/{oud}.html", f'location.replace("{nieuw}.html#nl");', f'<a href="{nieuw}.html#nl">Naar het spel</a>')
    doorstuur("spel/maximystery-match.html", 'location.replace("enigma-match.html" + location.hash);', '<a href="enigma-match.html">Enigma Match</a>')
    doorstuur("nl/boeken/index.html", 'location.replace("../puzzels/" + location.hash);', '<a href="../puzzels/">Mystery Puzzels</a>')
    doorstuur("en/books/index.html", 'location.replace("../puzzles/" + location.hash);', '<a href="../puzzles/">Mystery Puzzles</a>')
    # /spel/ zonder bestand -> spellenoverzicht in de gekozen taal
    doorstuur("spel/index.html",
              'var l="nl";try{l=localStorage.getItem("mm_lang")||(navigator.language||"").slice(0,2)}catch(e){}location.replace(l==="en"?"../en/games/":"../nl/spellen/");',
              '<a href="../nl/spellen/">Naar de spellen</a> &middot; <a href="../en/games/">To the games</a>')
    doorstuur("404.html",
              '',
              '<span style="display:block;font-size:1.6rem;margin-bottom:12px">Dit dossier bestaat niet &middot; This file does not exist</span><a href="/nl/">Enigma Mystery (NL)</a> &middot; <a href="/en/">Enigma Mystery (EN)</a>')
    (ROOT / "site.webmanifest").write_text(json.dumps({
        "name": "Enigma Mystery", "short_name": "Enigma Mystery", "start_url": "/", "display": "standalone",
        "background_color": "#0d0a07", "theme_color": "#0d0a07",
        "icons": [{"src": "/assets/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/assets/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=1), encoding="utf-8")
    if not (ROOT / "CNAME").exists():
        (ROOT / "CNAME").write_text("www.enigmamystery.com\n")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /_tools/\nSitemap: {SITE}/sitemap.xml\n")
    urls = ["", *(pad(k, l) for k in PAD for l in ("nl", "en"))]
    spel = sorted({s[l][2].split("#")[0] for s in SPELLEN for l in ("nl", "en")})
    vandaag = date.today().isoformat()
    rows = "".join(f"<url><loc>{SITE}/{u}</loc><lastmod>{vandaag}</lastmod></url>\n" for u in urls)
    rows += "".join(f"<url><loc>{SITE}/spel/{u}</loc><lastmod>{vandaag}</lastmod></url>\n" for u in spel)
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + rows + "</urlset>\n")

def main():
    for f in ["spel/" + s[l][2].split("#")[0] for s in SPELLEN for l in ("nl", "en")]:
        assert (ROOT / f).exists(), "ontbreekt: " + f
    for s in SPELLEN:
        assert (ROOT / "assets/dossiers" / (s["art"] + ".jpg")).exists(), s["art"]
    taalkeuze()
    for lang in ("nl", "en"):
        voorpagina(lang); spellenpagina(lang); wandelpagina(lang); boekenpagina(lang); propagina(lang); overpagina(lang); contactpagina(lang)
    extra()
    print("klaar:", len(SPELLEN), "spellen,", "nieuw:", [SPELLEN[i]["en"][0] for i in NIEUW])

main()
