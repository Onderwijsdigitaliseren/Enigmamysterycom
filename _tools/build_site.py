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
PRO_ARCHIEF = {"nl": "Archief II", "en": "Archive II"}
PRO_PRIJS = "€3,99"
KOFI_PRO = "https://ko-fi.com/s/67649bac70"
WANDEL = {"nl": "wandel/nl/", "en": "wandel/"}  # één site met keuze NL/EN; murderwalk.com verdwijnt
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
 dict(plank="verhaal", art="knipsel", pro=True, added="2026-10-30",
      nl=("Het Knipselarchief", "Een koude zaak uit 1974. Alleen het archief weet het nog.", "the-clippings-room.html#nl"),
      en=("The Clippings Room", "A 1974 cold case. Only the archive still remembers.", "the-clippings-room.html#en")),
 dict(plank="verhaal", art="texel", pro=True, added="2026-10-30",
      nl=("Huisje Texel", "Zes vrienden, één huurhuis, een telefoon vol berichten. Wie vertrouw jij?", "texel-house.html#nl"),
      en=("Texel House", "Six friends, one holiday house, a phone full of messages. Who do you trust?", "texel-house.html#en")),
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

for _s in SPELLEN:
    _s["status"] = "proef" if _s.get("proef") else ("pro" if _s["pro"] else "gratis")
    _s["archief"] = 1 if _s["status"] == "gratis" else 2   # I = open dossiers, II = verzegeld (pas)
PROEF_TEKST = {"dossier I": {"nl": "Dossier I gratis", "en": "File I free"}}

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
 "maat":   ("nl/op-maat/", "en/made-to-measure/"),
 "l_online":   ("nl/detectivespel-online/", "en/detective-game-online/"),
 "l_thuis":    ("nl/moordmysterie-thuis/", "en/murder-mystery-game-at-home/"),
 "l_vrijgezel":("nl/vrijgezellenfeest-moordmysterie/", "en/murder-mystery-hen-party/"),
 "l_uitje":    ("nl/uitje-moordwandeling/", "en/murder-mystery-group-outing/"),
}
MENU = [("spellen", "Spellen", "Games"), ("wandel", "Wandelingen", "Walks"), ("boeken", "Puzzels", "Puzzles"), ("mini", "Mini", "Mini"), ("pro", "Pro", "Pro"), ("maat", "Op maat", "Custom"), ("contact", "Contact", "Contact")]

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
   gratis="Gratis", pro="Pro", proef="Proef", nieuwstempel="Nieuw",
   alles="Alles", alleengratis="Gratis te spelen", alleenpro="Met de pas",
   footzin="Fictieve zaken. Echte puzzels. Elke zaak heeft precies één oplossing.",
   privacy="Privacy", notitie="Laat een notitie achter", overlink="Over Enigma Mystery",
 ),
 "en": dict(
   zin="Murder mysteries to play, to walk and to read.",
   naarspellen="Browse the games", naarwandel="Go on a murder walk",
   nieuw="New", nieuwzin="Just in on the desk.",
   deuren="The evidence board", deurenzin="Four leads, one name.",
   deurenuitleg="Online on your screen, outdoors on foot, on paper with a pencil, or together with the little ones. Pull a thread.",
   gratis="Free", pro="Pro", proef="Trial", nieuwstempel="New",
   alles="All", alleengratis="Free to play", alleenpro="With the pass",
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
        cls = ' class="pro"' if k == "pro" else (' class="maat"' if k == "maat" else "")
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
             (pad("maat", lang), "Op maat" if lang == "nl" else "Made to measure"),
             (pad("over", lang), t["overlink"]),
             (pad("contact", lang), "Contact"),
             (pad("over", lang) + "#privacy", t["privacy"])]
    nav = "".join(f'<a href="{p if p.startswith("http") else r(p)}"{" rel=\"noopener\"" if p.startswith("http") else ""}>{escape(n)}</a>' for p, n in links)
    return f"""</main>
<footer class="voet"><div class="binnen">
<span class="woordmerk"><b>Enigma</b> Mystery</span>
<nav aria-label="{'Onderaan' if lang == 'nl' else 'Footer'}">{nav}</nav>
<nav class="klein" aria-label="{'Ideeën' if lang == 'nl' else 'Ideas'}">{''.join(f'<a href="{r(pad(k, lang))}">{escape(LANDING[k][lang]["h1"])}</a>' for k in LANDING)}</nav>
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
    st = s["status"]
    stempels = f'<span class="stempel {st}">{t[st]}</span>'
    if nieuw_stempel and i in NIEUW:
        stempels += f'<span class="stempel nieuw">{t["nieuwstempel"]}</span>'
    regel = ""
    if st == "proef":
        regel = f'<p class="proefregel">{escape(PROEF_TEKST[s["proef"]][lang])} · {"de rest met de pas" if lang == "nl" else "the rest with the pass"}</p>'
    return (f'<a class="dossier" href="{spel_url(s, lang, here)}" data-status="{st}">'
            f'<div class="foto"><img src="{rel(here, "assets/dossiers/" + s["art"] + ".jpg")}" alt="" loading="lazy" decoding="async"></div>'
            f'<div class="tekst"><span class="soort">{escape(plaknaam)}</span><h3>{escape(titel)}</h3><p>{escape(haak)}</p>{regel}</div>{stempels}</a>')

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
        [("Waar", "Op telefoon of computer"), ("Duur", "20 minuten tot een paar avonden"), ("Prijs", "Van elke soort één zaak gratis, de rest met Pro (eenmalig €3,99)")], "Naar de spellen"),
       ("Online", "Mystery Games", "Play in your browser", f"{len(SPELLEN)} cases: stories, 3D escape rooms, logic puzzles and calm building games.",
        [("Where", "On your phone or computer"), ("Time", "20 minutes to a few evenings"), ("Price", "One case of every kind free, the rest with Pro (€3.99 once)")], "To the games")),
      ("wandel", pad("wandel", lang), "buiten", "voet", "assets/deur-wandelingen.jpg", 1.6,
       ("Buiten", "Mystery Wandelingen", "Loop de zaak zelf", "Een moordzaak die je buiten oplost. De stad om je heen wordt de plaats delict.",
        [("Waar", "Overal, met je telefoon in de hand"), ("Duur", "Ongeveer anderhalf uur"), ("Prijs", "Proefronde gratis; daarna € 9,95 per team")], "Naar de wandelingen"),
       ("Outdoors", "Mystery Walks", "Walk the case yourself", "A murder case you solve outside. The town around you becomes the crime scene.",
        [("Where", "Anywhere, phone in hand"), ("Time", "About ninety minutes"), ("Price", "Free trial round; then € 9.95 per team")], "To the walks")),
      ("boeken", pad("boeken", lang), "papier", "boek", "assets/deur-puzzels.jpg", -1.4,
       ("Op papier", "Mystery Puzzels", "Puzzelen met potlood", "Gedrukte puzzelboeken vol moordzaken, van makkelijk naar moeilijk.",
        [("Waar", "Aan tafel, in de trein, op vakantie"), ("Duur", "100 puzzels per boek"), ("Nu", "Gratis proefverdieping online; boeken volgen")], "Naar de puzzels"),
       ("On paper", "Mystery Puzzles", "Puzzle with a pencil", "Printed puzzle books full of murder cases, from easy to hard.",
        [("Where", "At the table, on the train, on holiday"), ("Time", "100 puzzles per book"), ("Now", "Free trial floor online; books to follow")], "To the puzzles")),
      ("mini", MINI, "mini", "ster", "assets/deur-mini.jpg", 2.4,
       ("Voor de kleintjes", "Mini Mystery", "Speuren zonder moord", "Raadsels en speurtochten voor jonge detectives.",
        [("Waar", "Online en op pad"), ("Voor wie", "Kinderen, samen met een grote")], "Naar Mini Mystery"),
       ("For the little ones", "Mini Mystery", "Sleuthing without murder", "Riddles and treasure hunts for young detectives.",
        [("Where", "Online and out and about"), ("For whom", "Children, together with a grown-up")], "To Mini Mystery")),
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
""" + nieuwband(lang, here)
    body += f"""<section class="sectie"><div class="binnen">
<div class="sectiekop"><span class="label">{t['deuren']}</span><h2>{t['deurenzin']}</h2><p class="zacht">{t['deurenuitleg']}</p></div>
<div class="bord"><div class="deuren">{deur_html}</div>{draad}</div></div></section>
{maatband(lang, here)}<section class="sectie"><div class="binnen">
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
    nl = lang == "nl"
    prijs = PRO_PRIJS if nl else PRO_PRIJS.replace(",", ".")
    volg = {"gratis": 0, "proef": 1, "pro": 2}
    def soorten(archief):
        out = ""
        for key, namen in PLANKEN:
            idx = [i for i, x in enumerate(SPELLEN) if x["plank"] == key and x["archief"] == archief]
            if not idx: continue
            idx.sort(key=lambda i: (volg[SPELLEN[i]["status"]], -int(SPELLEN[i]["added"].replace("-", ""))))
            naam, zin = namen[lang]
            out += (f'<section class="plank" id="a{archief}-{key}"><div class="sectiekop"><span class="label">{len(idx)} {("zaak" if len(idx) == 1 else "zaken") if nl else ("case" if len(idx) == 1 else "cases")}</span><h3 class="plankkop">{escape(naam)}</h3><p class="zacht">{escape(zin)}</p></div>'
                    f'<div class="rij">{"".join(kaart(i, lang, here) for i in idx)}</div></section>')
        return out
    n1 = sum(1 for x in SPELLEN if x["archief"] == 1); n2 = sum(1 for x in SPELLEN if x["archief"] == 2)
    npf = sum(1 for x in SPELLEN if x["status"] == "proef")
    def la(nr, rom, kop, sub, status_html, inhoud, open_=False, dicht=False):
        return (f'<section class="la{" open" if open_ else ""}{" dicht" if dicht else ""}" id="archief-{nr}">'
                f'<button class="lafront" type="button" aria-expanded="{"true" if open_ else "false"}" aria-controls="la{nr}-inhoud"{" disabled" if dicht else ""}>'
                f'<span class="greep" aria-hidden="true"></span><span class="lalabel"><span class="nummer">{rom}</span><span class="latekst"><b>{kop}</b><small>{sub}</small></span></span>{status_html}</button>'
                f'<div class="lainhoud" id="la{nr}-inhoud"{"" if open_ else " hidden"}><div class="labinnen">{inhoud}</div></div></section>')
    la1 = la(1, "I", f'{"Archief" if nl else "Archive"} I · {"Open dossiers" if nl else "Open files"}',
             (f"{n1} zaken, helemaal gratis te spelen" if nl else f"{n1} cases, free to play in full"),
             f'<span class="lastatus gratis">{t["gratis"]}</span>',
             f'<p class="lauitleg">{"Deze lade staat voor iedereen open. Kies een soort en begin." if nl else "This drawer is open to everyone. Pick a kind and begin."}</p>' + soorten(1), open_=True)
    uitleg2 = (f'<div class="lauitleg twee"><div><p>{(f"Verzegelde dossiers. Eén pas opent alle {n2} zaken in deze lade, eenmalig {prijs}, geen abonnement.") if nl else (f"Sealed files. One pass opens all {n2} cases in this drawer, {prijs} once, no subscription.")}</p>'
               + ((f'<p class="zacht">{(f"{npf} zaak heeft een proefhoofdstuk: het eerste dossier speel je gratis, de rest gaat open met de pas.") if nl else (f"{npf} case has a trial chapter: the first file is free, the rest opens with the pass.")}</p>') if npf else "") + '</div>'
               f'<div class="laknoppen"><a class="knop lak" href="{rel(here, pad("pro", lang))}">{(f"Pas {PRO_ARCHIEF[lang]} · {prijs}") if nl else (f"{PRO_ARCHIEF[lang]} pass · {prijs}")}</a><a class="knop lijn" href="{rel(here, pad("pro", lang))}#proCode">{"Ik heb al een code" if nl else "I already have a code"}</a></div></div>')
    la2 = la(2, "II", f'{"Archief" if nl else "Archive"} II · {"Verzegelde dossiers" if nl else "Sealed files"}',
             (f"{n2} zaken, met de pas · {prijs}" if nl else f"{n2} cases, with the pass · {prijs}"),
             f'<span class="zegel" aria-hidden="true"><span>PRO</span><small>{prijs}</small></span><span class="lastatus pro open-tekst">{"Ontgrendeld" if nl else "Unlocked"}</span>',
             uitleg2 + soorten(2))
    slots = "".join(f'<div class="leegvak"><span class="label">{escape(nm[lang][0])}</span><p>{"Nieuwe zaken" if nl else "New cases"}</p></div>' for _, nm in PLANKEN)
    la3 = la(3, "III", f'{"Archief" if nl else "Archive"} III · {"In voorbereiding" if nl else "In preparation"}',
             ("Dezelfde vier soorten, nieuwe zaken, een eigen pas" if nl else "The same four kinds, new cases, a pass of its own"),
             f'<span class="lastatus dicht">{"Op slot" if nl else "Locked"}</span>',
             f'<div class="leegvakken">{slots}</div>', dicht=True)
    body = kop + f'<section class="sectie"><div class="binnen"><div class="kastkop"><span class="label">{"De dossierkast" if nl else "The file cabinet"}</span><h2>{"Trek een lade open." if nl else "Pull open a drawer."}</h2><p class="zacht">{"Lade I is gratis. Lade II gaat open met één pas. Lade III komt eraan." if nl else "Drawer I is free. Drawer II opens with one pass. Drawer III is on its way."}</p></div><div class="kast">{la1}{la2}{la3}</div></div></section>\n'
    schrijf(here + "index.html", head(lang, "spellen", title, desc, here) + kopbalk(lang, "spellen", here) + body + voet(lang, here))

WANDELZAKEN = [  # (cover, nl-pagina, en-pagina, nl-titel, en-titel, nl-haak, en-haak, label)
 ("cover-sm", "de-erfenis-van-de-spellenmaker.html", "the-gamemakers-legacy.html", "De Erfenis van de Spellenmaker", "The Gamemaker's Legacy",
  "Tien kisten, tien spellen, vijf erfgenamen. Een speurtocht van twee uur.", "Ten chests, ten games, five heirs. A two-hour trail.", "Nieuw|New"),
 ("cover-mw", "moordwandeling.html", "murder-walk.html", "Moordwandeling", "Murder Walk",
  "Acht sporen, vijf getuigen, één leugenaar.", "Eight leads, five witnesses, one liar.", None),
 ("cover-vz", "de-verdwijning.html", "the-vanishing.html", "De Verdwijning", "The Vanishing",
  "Iemand is weg. Ontvoerd, gevlucht, of iets anders?", "Someone is gone. Abducted, fled, or something else?", None),
 ("cover-lb", "de-laatste-bus.html", "the-last-bus.html", "De Laatste Bus", "The Last Bus",
  "Telefoon zegt: aangekomen. Thuis zegt: nee.", "Phone says: arrived. Home says: no.", None),
 ("cover-cc", "onopgelost.html", "unsolved.html", "Onopgelost", "Unsolved",
  "Een vermissing van twintig jaar geleden, nooit opgelost.", "A disappearance twenty years ago, never solved.", None),
 ("cover-og", "ooggetuige.html", "eyewitness.html", "Ooggetuige", "Eyewitness",
  "Jij zag iets wat je niet had mogen zien. En iemand loopt achter je.", "You saw something you were never meant to see. Someone is walking behind you.", None),
 ("cover-td", "tot-de-dood-ons-scheidt.html", "till-death-do-us-part.html", "Tot de Dood Ons Scheidt", "Till Death Do Us Part",
  "Ze zou vandaag trouwen. De bruid kwam nooit aan.", "She was to be married today. The bride never arrived.", None),
 ("cover-ng", "de-nacht-van-de-geesten.html", "night-of-the-ghosts.html", "De Nacht van de Geesten", "Night of the Ghosts",
  "Geen moordenaar, wel een geest. Durf jij na het donker?", "No murderer, but a ghost. Do you dare after dark?", None),
]

def wandelpagina(lang):
    here = pad("wandel", lang); r = lambda p: rel(here, p); nl = lang == "nl"
    title = "Mystery Wandelingen · Enigma Mystery" if nl else "Mystery Walks · Enigma Mystery"
    desc = ("Detectivespellen die je loopt, in je eigen straten. De kaart legt acht sporen op echte plekken om je heen. Zeven zaken, proefronde gratis, één ticket per team."
            if nl else
            "Detective games you walk in your own streets. The map places eight leads at real places around you. Seven cases, free trial round, one ticket per team.")
    basis = r("wandel/nl/" if nl else "wandel/")
    W = lambda f: r("assets/wandel/" + f)
    kop = f"""<section class="held wandelheld">
<picture class="beeld"><source media="(max-width:640px)" srcset="{W('hero.webp')}"><img src="{W('hero-breed.webp')}" alt="" fetchpriority="high"></picture>
<div class="binnen"><span class="label">{"Buiten" if nl else "Outdoors"}</span><h1>{"Mystery Wandelingen" if nl else "Mystery Walks"}</h1>
<p class="zin">{"Een detectivespel dat je loopt, in je eigen straten. De buurt om je heen wordt de plaats delict." if nl else "A detective game you walk, in your own streets. The neighbourhood around you becomes the crime scene."}</p>
<div class="knoppen"><a class="knop" href="#zaken">{"Kies een zaak" if nl else "Pick a case"}</a><a class="knop lijn" href="#hoe">{"Zo werkt het" if nl else "How it works"}</a></div>
<ul class="wandelfeiten">
<li><b>{"Overal" if nl else "Anywhere"}</b><span>{"gps legt de route om je heen" if nl else "GPS lays the route around you"}</span></li>
<li><b>{"Gratis" if nl else "Free"}</b><span>{"proefronde bij elke zaak" if nl else "trial round for every case"}</span></li>
<li><b>€ 9,95</b><span>{"één ticket per team" if nl else "one ticket per team"}</span></li>
</ul></div></section>
"""
    zaken = ""
    for n, (cov, pnl, pen, tnl, ten, hnl, hen, lab) in enumerate(WANDELZAKEN):
        href = basis + (pnl if nl else pen)
        lab = lab and (lab.split("|")[0 if nl else -1])
        tag = f'<span class="zaaklabel">{lab}</span>' if lab else ""
        zaken += (f'<a class="wandelzaak" href="{href}" style="--d:{n * 70}ms">{tag}'
                  f'<span class="medaille"><img src="{W(cov + ".webp")}" alt="" loading="lazy" width="320" height="320"></span>'
                  f'<h3>{escape(tnl if nl else ten)}</h3><p>{escape(hnl if nl else hen)}</p>'
                  f'<span class="pijl">{"Bekijk de zaak" if nl else "View the case"} &rarr;</span></a>')
    stappen = ([("mw-lantern", "Kies een zaak", "Start waar je staat. De kaart legt acht sporen op echte plekken op loopafstand: de kerk, de bushalte, het café."),
                ("mw-evidence", "Loop en verzamel", "Binnen 35 meter gaat een spoor open: een schim die iets zag, een bewijsstuk, een camerabeeld, een bericht."),
                ("mw-suspect", "Wijs de dader aan", "Sluit samen verdachten uit in het notitieboek, ontmasker de leugenaar en wijs de dader aan.")]
               if nl else
               [("mw-lantern", "Pick a case", "Start where you stand. The map places eight leads at real places within walking distance: the church, the bus stop, the café."),
                ("mw-evidence", "Walk and collect", "Within 35 metres a lead opens: a shade who saw something, a piece of evidence, a camera still, a message."),
                ("mw-suspect", "Name the killer", "Rule out suspects together in the notebook, unmask the liar and name the killer.")])
    stap_html = "".join(f'<li class="stap"><span class="polaroid" style="--h:{h}deg"><img src="{W(img + ".webp")}" alt="" loading="lazy"><span class="nr">{n}</span></span><h3>{escape(a)}</h3><p>{escape(b)}</p></li>'
                        for (img, a, b), n, h in zip(stappen, ("I", "II", "III"), (-3, 2, -1.5)))
    galerij = ([("mw-shade", "Een schim in de mist"), ("mw-schoen", "Voetsporen in de regen"), ("mw-victim", "De omtrek op de stoep"),
                ("mw-vezel", "Een draad aan het hek"), ("mw-hand", "Een handschoen in de goot"), ("mw-witness", "De getuige in de deuropening"),
                ("mw-flee", "Iemand rent weg"), ("mw-bril", "Een bril op tafel")]
               if nl else
               [("mw-shade", "A shade in the fog"), ("mw-schoen", "Footprints in the rain"), ("mw-victim", "The outline on the pavement"),
                ("mw-vezel", "A thread on the railing"), ("mw-hand", "A glove in the gutter"), ("mw-witness", "The witness in the doorway"),
                ("mw-flee", "Someone runs"), ("mw-bril", "Glasses on the table")])
    gal_html = "".join(f'<figure><img src="{W(f + ".webp")}" alt="{escape(c)}" loading="lazy"><figcaption>{escape(c)}</figcaption></figure>' for f, c in galerij)
    blokken = ([("Samen op pad", ["Eén ticket per team, iedereen vult dezelfde code in", "Samen op één telefoon of ieder op een eigen", "De code blijft twee maanden geldig"]),
                ("Op maat", ["Personaliseren met jullie foto's, namen en thema: € 29,95 inclusief ticket", "Voor een verjaardag, vrijgezellenfeest, uitje of klas", "Iets helemaal nieuws, zoals een eigen route? Dien een aanvraag in"])]
               if nl else
               [("Out together", ["One ticket per team, everyone enters the same code", "Together on one phone or each on their own", "The code stays valid for two months"]),
                ("Made to measure", ["Personalise with your photos, names and theme: € 29.95 including the ticket", "For a birthday, hen or stag party, outing or class", "Something entirely new, like a route of your own? Send a request"])])
    blok_html = "".join(f'<div class="blok"><h3>{a}</h3><ul>{"".join(f"<li>{x}</li>" for x in b)}</ul>'
                        + (f'<a class="knop lijn" href="{r(pad("maat", lang))}">{"Alles over maatwerk" if nl else "All about made to measure"} &rarr;</a>' if i == 1 else "") + '</div>'
                        for i, (a, b) in enumerate(blokken))
    body = kop + nieuwband(lang, here) + f"""<section class="sectie" id="zaken"><div class="binnen">
<div class="sectiekop"><span class="label">{"Zeven zaken op straat" if nl else "Seven cases on the street"}</span><h2>{"Kies je zaak, trek je jas aan." if nl else "Pick your case, grab your coat."}</h2>
<p class="zacht">{"Elke zaak speel je in je eigen buurt, in het Nederlands of het Engels. Elke wandeling begint met een gratis proefronde." if nl else "Every case plays in your own neighbourhood, in English or Dutch. Every walk starts with a free trial round."}</p></div>
<div class="wandelzaken">{zaken}</div></div></section>
<section class="sectie" id="hoe"><div class="binnen">
<div class="sectiekop"><span class="label">{"Zo werkt het" if nl else "How it works"}</span><h2>{"Drie stappen, één dader" if nl else "Three steps, one killer"}</h2></div>
<div class="route"><svg class="routelijn" viewBox="0 0 1000 60" preserveAspectRatio="none" aria-hidden="true"><path d="M60 30 C 250 -10, 350 70, 500 30 S 760 -10, 940 30" fill="none" stroke="var(--lak)" stroke-width="2.4" stroke-dasharray="2 10" stroke-linecap="round"/></svg>
<ol class="stappen wandelstappen">{stap_html}</ol></div></div></section>
<section class="sectie onderweg"><div class="binnen">
<div class="sectiekop"><span class="label">{"Onderweg" if nl else "On the way"}</span><h2>{"Wat je onderweg tegenkomt" if nl else "What you will run into"}</h2></div>
<div class="galerij">{gal_html}</div></div></section>
{maatband(lang, here)}
<section class="sectie"><div class="binnen"><div class="twee">{blok_html}</div></div></section>
<section class="wandelcta"><img src="{W('mw-shadow.webp')}" alt="" loading="lazy"><div class="binnen">
<h2>{"Klaar om te gaan?" if nl else "Ready to go?"}</h2><p class="zin">{"De eerste ronde is gratis. Je hebt alleen je telefoon en je schoenen nodig." if nl else "The first round is free. All you need is your phone and your shoes."}</p>
<div class="knoppen"><a class="knop" href="{basis}">{"Naar de wandelingen" if nl else "To the walks"} &rarr;</a><a class="knop lijn" href="{r(pad('maat', lang))}">{"Wandeling op maat" if nl else "Made to measure"}</a></div></div></section>
"""
    schrijf(here + "index.html", head(lang, "wandel", title, desc, here) + kopbalk(lang, "wandel", here) + body + voet(lang, here))

BOEKEN = [
 dict(id={"nl": "moord-op-het-uur", "en": "murder-by-the-hour"}, status="binnenkort",
      nl=("Moord op het uur", "Gongoku · 100 moordpuzzels op de plattegrond",
          "Een landhuis, een gong die elk uur slaat, en een moord die op de plattegrond te reconstrueren is. Honderd puzzels in vijf huizen, oplopend van 4×4 tot 8×8. De beginletters van de daders vormen per hoofdstuk het gif.",
          None, None),
      en=("Murder by the Hour", "Gongoku · 100 murder puzzles on the floor plan",
          "A country house, a gong that strikes every hour, and a murder you can reconstruct on the floor plan. One hundred puzzles across five houses, from 4×4 up to 8×8. Each chapter's killers spell out the poison.",
          None, None)),
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
    pro_lijst = "".join(f'<li><a href="{spel_url(s, lang, here)}">{escape(s[lang][0])}</a>{(" · " + ("alles na " if lang == "nl" else "everything after ") + s["proef"]) if s["status"] == "proef" else ""}</li>' for s in SPELLEN if s["status"] in ("pro", "proef"))
    n_pro = sum(1 for s in SPELLEN if s["status"] in ("pro", "proef"))
    kop = held(here, lang, f'<span class="label" style="color:var(--lak-licht)">Pro · {PRO_ARCHIEF[lang]}</span><h1>{"De Pro-pas" if nl else "The Pro pass"}</h1><p class="zin">{(f"Eén pas opent alle {n_pro} verzegelde dossiers van {PRO_ARCHIEF['nl']}. Eenmalig {PRO_PRIJS}, geen abonnement." if nl else f"One pass opens all {n_pro} sealed files in {PRO_ARCHIEF['en']}. {PRO_PRIJS.replace(',', '.')} once, no subscription.")}</p><div class="knoppen"><a class="knop lak" href="{KOFI_PRO}" rel="noopener">{(f"Haal de Pro-pas · {PRO_PRIJS}") if nl else (f"Get the Pro pass · {PRO_PRIJS.replace(',', '.')}")}</a></div>', klein=True)
    stappen = ([("Koop de pas", "Via Ko-fi. Je krijgt direct een pascode."), ("Vul de code in", "Hieronder, of in een verzegeld dossier zelf."), ("Speel alles", "De code wordt op dit apparaat onthouden. Op een ander apparaat vul je hem één keer opnieuw in.")]
               if nl else [("Buy the pass", "Through Ko-fi. You get a pass code right away."), ("Enter the code", "Below, or inside any sealed file."), ("Play everything", "The code is remembered on this device. On another device you enter it once more.")])
    body = kop + f"""<section class="sectie"><div class="binnen twee">
<div class="blok"><h3>{(f"Wat {PRO_ARCHIEF['nl']} opent") if nl else (f"What {PRO_ARCHIEF['en']} opens")}</h3><ul>{pro_lijst}</ul></div>
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

MAAT_T = {
 "nl": dict(
   band_label="Op maat", band_h="Jullie eigen versie van een zaak",
   band_p="Elke wandeling of elk spel kan gepersonaliseerd worden met jullie eigen foto's, namen en een thema, voor € 29,95 inclusief ticket. Iets helemaal nieuws, zoals een eigen route of verhaal? Dien een aanvraag in.",
   band_knop="Bekijk de mogelijkheden", band_knop2="Direct aanvragen",
   title="Op maat · Personaliseren of een eigen zaak · Enigma Mystery",
   desc="Personaliseer een wandeling of spel met jullie eigen foto's, namen en thema voor € 29,95 inclusief ticket, voor een verjaardag, vrijgezellenfeest, bedrijfsuitje of familiedag. Iets helemaal nieuws? Dien een aanvraag in, prijs nader te bepalen.",
   label="Op maat", h1="Jullie eigen versie",
   zin="Maak een bestaande wandeling of een spel van jullie: met jullie eigen foto's, namen en een thema. Voor een vaste prijs van € 29,95 inclusief ticket. En wil je iets wat nog niet bestaat, dan kun je dat aanvragen.",
   k1="Aanvragen", k2="Wat kan er?",
   twee_label="Twee manieren", twee_h="Personaliseren of iets nieuws",
   twee=[("Personaliseren","€ 29,95","Een bestaande wandeling of een spel, aangekleed met jullie eigen foto's, namen en een thema. Het verhaal, de puzzels en de route blijven zoals ze zijn.",
          ["Inclusief het ticket voor jullie team","Jullie foto's bij de verdachten, getuigen en sporen","Jullie namen in het verhaal","Een thema: verjaardag, vrijgezellenfeest, bedrijfsuitje, kerst…","Eén keer iets laten aanpassen als je hem gezien hebt","Een eigen link om te spelen"],"Personaliseren aanvragen"),
         ("Iets helemaal nieuws","Prijs nader te bepalen","Een eigen route met een vast start- en eindpunt, een eigen verhaal, nieuwe puzzels of een zaak voor een grote groep of een evenement.",
          ["Een route langs jullie plekken, eindigen in jullie café","Een verhaal dat over jullie gaat","Teams tegen elkaar met een eindstand","Voor bedrijven, scholen, evenementen en toerisme"],"Aanvraag indienen")],
   gel_label="Voor welke gelegenheid?", gel_h="Waar een eigen versie leuk voor is",
   gel=[("Verjaardag of jubileum","De jarige als slachtoffer, verdachte of rechercheur, met foto's die alleen jullie herkennen."),
        ("Vrijgezellenfeest","De bruid of bruidegom in de hoofdrol, met foto's van de vriendengroep."),
        ("Bedrijfs- of teamuitje","Collega's als verdachten en de directeur in een verdachte rol (met een knipoog)."),
        ("Familie- of vriendendag","Opa, tante en de kleinkinderen in het verhaal. Voor alle leeftijden."),
        ("Cadeau","Een zaak met iemands eigen foto's en naam erin, om samen te spelen."),
        ("School of klas","De klas en de docent in een moordzaak, als afsluiting of introductie.")],
   hoe_label="Zo werkt personaliseren", hoe_h="In drie stappen",
   hoe=[("Kies een wandeling of spel","Vul het formulier in: welke zaak, de gelegenheid en welk thema. Stuur daarna de foto's en namen mee in de mail."),
        ("Ik maak jullie versie","Jullie foto's, namen en thema gaan erin. Het verhaal en de puzzels blijven hetzelfde."),
        ("Bekijken en spelen","Je krijgt een eigen link. Je mag één keer iets laten aanpassen; daarna ligt hij vast.")],
   mini_h="Voor kinderen", mini_p="Een speurtocht voor een kinderfeestje, schoolkamp of buurtfeest personaliseren, zonder moord en geschikt voor 6 tot 12 jaar, doe je via Mini Mystery.", mini_k="Op maat bij Mini Mystery",
   faq_label="Vragen", faq=[("Wat kost personaliseren?","€ 29,95 inclusief ticket per wandeling of spel. Daarvoor krijg je jullie eigen versie met foto's, namen en een thema."),
        ("Kan de route ook anders?","Nee, bij personaliseren blijft de zaak zoals hij is. Een eigen route, verhaal of nieuwe onderdelen is iets nieuws: dien daarvoor een aanvraag in, dan hoor je wat het kost."),
        ("Kan ik daarna nog dingen veranderen?","Je mag één keer iets laten aanpassen als je jullie versie gezien hebt. Daarna ligt hij vast."),
        ("Hoe ver van tevoren moet ik aanvragen?","Minimaal twee weken van tevoren. Voor iets helemaal nieuws liever langer.")],
   form_label="Aanvragen", form_h="Vertel wat je wilt",
   form_p="Het formulier opent je mailprogramma met alles al ingevuld. Foto's voeg je daarna als bijlage toe aan die mail.",
   f=dict(naam="Je naam",mail="Je e-mailadres",soort="Wat wil je?",soortopt=["Personaliseren (€ 29,95)","Iets helemaal nieuws (aanvraag)"],
          basis="Welke wandeling of welk spel?",basisopt=["Moordwandeling","De Verdwijning","De Laatste Bus","Tot de Dood Ons Scheidt","Ooggetuige","Onopgelost","De Nacht van de Geesten","Een online spel (zet in je wensen welk)","Weet ik nog niet"],
          gel="Gelegenheid",n="Aantal deelnemers",teams="Thema",waar="Waar spelen jullie (stad of buurt)",wanneer="Wanneer (datum, of ongeveer)",wens="Jullie wensen",
          wensp="Bijvoorbeeld: thema vrijgezellenfeest, de bruid heet Sanne, foto's van de vriendinnen als verdachten…",
          knop="Open de mail en verstuur",kopie="Lukt mailen niet? Kopieer de tekst",nodig="Vul in elk geval je naam en jullie wensen in.",gekopieerd="Gekopieerd. Plak het in een mail aan ",
          onderwerp="Op maat via Enigma Mystery",hoi="Hoi Kellie,",intro="Ik wil graag een zaak op maat.",groet="Groet,",
          opties=["Verjaardag of jubileum","Vrijgezellenfeest","Bedrijfs- of teamuitje","Familie- of vriendendag","Cadeau","School of klas","Iets anders"]),
   noot="Personaliseren: € 29,95 inclusief ticket, één keer aanpassen. Iets helemaal nieuws: prijs nader te bepalen."),
 "en": dict(
   band_label="Made to measure", band_h="Your own version of a case",
   band_p="Every walk or game can be personalised with your own photos, names and a theme, for € 29.95 including the ticket. Something entirely new, like a route or story of your own? Send a request.",
   band_knop="See what's possible", band_knop2="Ask straight away",
   title="Made to measure · Personalise or a case of your own · Enigma Mystery",
   desc="Personalise a walk or game with your own photos, names and theme for € 29.95 including the ticket, for a birthday, hen or stag party, company outing or family day. Something entirely new? Send a request, price to be agreed.",
   label="Made to measure", h1="Your own version",
   zin="Make an existing walk or game yours: with your own photos, names and a theme. For a fixed price of € 29.95 including the ticket. And if you want something that doesn't exist yet, you can ask for it.",
   k1="Ask", k2="What's possible?",
   twee_label="Two ways", twee_h="Personalise, or something new",
   twee=[("Personalise","€ 29.95","An existing walk or game, dressed up with your own photos, names and a theme. The story, the puzzles and the route stay as they are.",
          ["Including the ticket for your team","Your photos with the suspects, witnesses and leads","Your names in the story","A theme: birthday, hen or stag party, company outing, Christmas…","One round of changes once you've seen it","Your own link to play"],"Ask to personalise"),
         ("Something entirely new","Price to be agreed","A route of your own with a fixed start and finish, a story of your own, new puzzles, or a case for a big group or an event.",
          ["A route past your places, finishing at your pub","A story that's about you","Teams against each other with a leaderboard","For companies, schools, events and tourism"],"Send a request")],
   gel_label="For which occasion?", gel_h="When your own version is fun",
   gel=[("Birthday or anniversary","The birthday person as victim, suspect or detective, with photos only you will recognise."),
        ("Hen or stag party","The bride or groom in the lead role, with photos of the group."),
        ("Company or team outing","Colleagues as suspects and the boss in a suspicious role (tongue in cheek)."),
        ("Family or friends' day","Grandad, auntie and the grandchildren in the story. For all ages."),
        ("A gift","A case with someone's own photos and name in it, to play together."),
        ("School or class","The class and the teacher in a murder case, to round off or kick off.")],
   hoe_label="How personalising works", hoe_h="In three steps",
   hoe=[("Pick a walk or game","Fill in the form: which case, the occasion and which theme. Then attach the photos and names to the email."),
        ("I make your version","Your photos, names and theme go in. The story and puzzles stay the same."),
        ("Check and play","You get your own link. You can ask for one round of changes; then it's final.")],
   mini_h="For children", mini_p="Personalising a treasure hunt for a kids' party, school trip or street party, without murder and suited to ages 6 to 12, is done through Mini Mystery.", mini_k="Made to measure at Mini Mystery",
   faq_label="Questions", faq=[("What does personalising cost?","€ 29.95 including the ticket per walk or game. For that you get your own version with photos, names and a theme."),
        ("Can the route be different?","No, when personalising the case stays as it is. A route, story or new parts of your own count as something new: send a request and you'll hear what it costs."),
        ("Can I still change things afterwards?","You can ask for one round of changes once you've seen your version. Then it's final."),
        ("How far ahead should I ask?","At least two weeks ahead. For something entirely new, longer.")],
   form_label="Ask", form_h="Tell me what you want",
   form_p="The form opens your mail app with everything filled in. Attach the photos to that email afterwards.",
   f=dict(naam="Your name",mail="Your email address",soort="What would you like?",soortopt=["Personalise (€ 29.95)","Something entirely new (request)"],
          basis="Which walk or game?",basisopt=["Murder Walk","The Vanishing","The Last Bus","Till Death Do Us Part","Eyewitness","Unsolved","Night of the Ghosts","An online game (say which in your wishes)","Not sure yet"],
          gel="Occasion",n="Number of players",teams="Theme",waar="Where will you play (town or neighbourhood)",wanneer="When (date, or roughly)",wens="Your wishes",
          wensp="For example: hen party theme, the bride is called Sanne, photos of her friends as the suspects…",
          knop="Open the email and send",kopie="Email not working? Copy the text",nodig="At least fill in your name and your wishes.",gekopieerd="Copied. Paste it into an email to ",
          onderwerp="Made to measure via Enigma Mystery",hoi="Hi Kellie,",intro="I'd like a case made to measure.",groet="Kind regards,",
          opties=["Birthday or anniversary","Hen or stag party","Company or team outing","Family or friends' day","A gift","School or class","Something else"]),
   noot="Personalise: € 29.95 including the ticket, one round of changes. Something entirely new: price to be agreed."),
}

# UITGELICHT: nieuwkomer bovenaan de voorpagina en de wandelpagina. Tot `tot` (Nederlandse tijd) met de gratis-tekst,
# daarna schakelt een klein script vanzelf naar de gewone tekst. Op None zetten om de band weg te halen.
UITGELICHT = {"tot": "2026-11-16T23:59:59+01:00", "beeld": "wandel/assets/feature-sm.webp",
  "nl": {"href": "wandel/nl/de-erfenis-van-de-spellenmaker.html", "label": "Nieuw · gratis t/m maandag 16 november", "label2": "Nieuw",
         "h": "De Erfenis van de Spellenmaker",
         "p": "Een speurtocht van twee uur door je eigen buurt. Open tien kisten in 3D, win het spel dat erin ligt en vang met je camera de schimmen van de laatste avond van de spellenmaker. Buiten, binnen of op de bank.",
         "knop": "Speel gratis", "knop2": "Bekijk de speurtocht"},
  "en": {"href": "wandel/the-gamemakers-legacy.html", "label": "New · free until Monday 16 November", "label2": "New",
         "h": "The Gamemaker's Legacy",
         "p": "A two-hour trail around your own neighbourhood. Open ten puzzle chests in 3D, win the game inside each one and catch the shades of the gamemaker's last evening with your camera. Outdoors, indoors or on the sofa.",
         "knop": "Play for free", "knop2": "View the trail"}}

def nieuwband(lang, here):
    u = UITGELICHT
    if not u: return ""
    r = lambda p: rel(here, p); m = u[lang]
    return f"""<section class="sectie nieuwband"><div class="binnen"><a class="nieuwkaart" href="{r(m['href'])}" data-tot="{u['tot']}" style="--beeld:url('{r(u['beeld'])}')">
<div class="nieuwtekst"><span class="label" data-na="{escape(m['label2'])}">{escape(m['label'])}</span><h2>{escape(m['h'])}</h2><p>{escape(m['p'])}</p>
<span class="knop" data-na="{escape(m['knop2'])} &rarr;">{escape(m['knop'])} &rarr;</span></div></a>
<script>(function(){{var k=document.currentScript.previousElementSibling;if(Date.now()>Date.parse(k.dataset.tot))k.querySelectorAll("[data-na]").forEach(function(e){{e.innerHTML=e.dataset.na}})}})()</script>
</div></section>
"""

def maatband(lang, here):
    r = lambda p: rel(here, p); m = MAAT_T[lang]
    return f"""<section class="sectie maatband"><div class="binnen"><div class="maatkaart">
<div class="maattekst"><span class="label">{m['band_label']}</span><h2>{escape(m['band_h'])}</h2><p class="zacht">{escape(m['band_p'])}</p></div>
<div class="knoppen"><a class="knop" href="{r(pad('maat', lang))}">{escape(m['band_knop'])} &rarr;</a><a class="knop lijn" href="{r(pad('maat', lang))}#aanvragen">{escape(m['band_knop2'])}</a></div>
</div></div></section>
"""

def maatpagina(lang):
    here = pad("maat", lang); r = lambda p: rel(here, p); m = MAAT_T[lang]; f = m["f"]
    W = lambda x: r("assets/wandel/" + x)
    kop = f"""<section class="held wandelheld maatheld">
<picture class="beeld"><source media="(max-width:640px)" srcset="{W('hero.webp')}"><img src="{W('hero-breed.webp')}" alt="" fetchpriority="high"></picture>
<div class="binnen"><span class="label">{m['label']}</span><h1>{escape(m['h1'])}</h1><p class="zin">{escape(m['zin'])}</p>
<div class="knoppen"><a class="knop" href="#aanvragen">{escape(m['k1'])}</a><a class="knop lijn" href="#hoe">{escape(m['k2'])}</a></div></div></section>
"""
    kaartjes = lambda lst: "".join(f'<div class="maatvak"><h3>{escape(a)}</h3><p>{escape(b)}</p></div>' for a, b in lst)
    twee = "".join(f'<div class="maattier{" nieuw" if n else ""}"><span class="label">{escape(a)}</span><b class="prijs">{escape(pr)}</b><p class="zacht">{escape(z)}</p><ul>{"".join(f"<li>{escape(x)}</li>" for x in lst)}</ul><a class="knop{" lijn" if n else ""}" href="#aanvragen" data-soort="{n}">{escape(kn)} &rarr;</a></div>'
                   for n, (a, pr, z, lst, kn) in enumerate(m["twee"]))
    hoe = "".join(f'<li><span class="nr">{n}</span><h3>{escape(a)}</h3><p>{escape(b)}</p></li>' for n, (a, b) in zip(("I", "II", "III"), m["hoe"]))
    faq = "".join(f'<details class="maatvraag"><summary>{escape(q)}</summary><p>{escape(a)}</p></details>' for q, a in m["faq"])
    opt = "".join(f"<option>{escape(o)}</option>" for o in f["opties"])
    veld = lambda i, lab, typ="text", extra="": f'<label for="{i}">{escape(lab)}</label><input id="{i}" type="{typ}"{extra}>'
    body = kop + f"""<section class="sectie" id="wat"><div class="binnen">
<div class="sectiekop"><span class="label">{m['twee_label']}</span><h2>{escape(m['twee_h'])}</h2></div>
<div class="maattiers">{twee}</div></div></section>
<section class="sectie"><div class="binnen">
<div class="sectiekop"><span class="label">{m['gel_label']}</span><h2>{escape(m['gel_h'])}</h2></div>
<div class="maatraster">{kaartjes(m['gel'])}</div></div></section>
<section class="sectie" id="hoe"><div class="binnen">
<div class="sectiekop"><span class="label">{m['hoe_label']}</span><h2>{escape(m['hoe_h'])}</h2></div>
<ol class="maatstappen">{hoe}</ol></div></section>
<section class="sectie" id="aanvragen"><div class="binnen maataanvraag">
<div class="maatlinks"><span class="label">{m['form_label']}</span><h2>{escape(m['form_h'])}</h2><p class="zacht">{escape(m['form_p'])}</p>
<p class="zacht">{escape(m['noot'])}</p></div>
<form class="formulier maatform" id="maatForm" novalidate>
{veld("mNaam", f['naam'], "text", ' autocomplete="name"')}
{veld("mMail", f['mail'], "email", ' autocomplete="email"')}
<label for="mSoort">{escape(f['soort'])}</label><select id="mSoort">{"".join(f"<option>{escape(o)}</option>" for o in f['soortopt'])}</select>
<label for="mBasis">{escape(f['basis'])}</label><select id="mBasis">{"".join(f"<option>{escape(o)}</option>" for o in f['basisopt'])}</select>
<label for="mGel">{escape(f['gel'])}</label><select id="mGel">{opt}</select>
<div class="maat2"><div>{veld("mN", f['n'], "number", ' min="1"')}</div><div>{veld("mTeams", f['teams'])}</div></div>
{veld("mWaar", f['waar'])}
{veld("mWanneer", f['wanneer'])}
<label for="mWens">{escape(f['wens'])}</label><textarea id="mWens" placeholder="{escape(f['wensp'])}"></textarea>
<button class="knop" type="submit">&#9993; {escape(f['knop'])}</button>
<button class="knop lijn" type="button" id="mKopie">{escape(f['kopie'])}</button>
<p class="melding" id="mMelding" role="status" aria-live="polite"></p>
</form></div></section>
<section class="sectie"><div class="binnen maataanvraag">
<div class="maatvragen"><span class="label">{m['faq_label']}</span>{faq}</div>
<div class="blok maatmini"><h3>{escape(m['mini_h'])}</h3><p class="zacht">{escape(m['mini_p'])}</p><a class="knop lijn" href="{MINI}/{'' if lang == 'nl' else 'en/'}#custom" rel="noopener">{escape(m['mini_k'])} &rarr;</a></div>
</div></section>
<script>
(function(){{var F={json.dumps(f, ensure_ascii=False)},ADR="{NOTITIE_ADRES}",$=function(i){{return document.getElementById(i)}};
var ids=["mNaam","mMail","mSoort","mBasis","mGel","mN","mTeams","mWaar","mWanneer","mWens"];
try{{var s=JSON.parse(localStorage.getItem("em_maat")||"{{}}");ids.forEach(function(i){{if(s[i])$(i).value=s[i]}})}}catch(e){{}}
function lees(){{var o={{}};ids.forEach(function(i){{o[i]=($(i).value||"").trim()}});try{{localStorage.setItem("em_maat",JSON.stringify(o))}}catch(e){{}}return o}}
function tekst(o){{return F.hoi+"\\n\\n"+F.intro+"\\n\\n"+F.soort+": "+o.mSoort+"\\n"+F.basis+": "+o.mBasis+"\\n"+F.gel+": "+o.mGel+"\\n"+F.n+": "+o.mN+"\\n"+F.teams+": "+o.mTeams+"\\n"+F.waar+": "+o.mWaar+"\\n"+F.wanneer+": "+o.mWanneer+"\\n\\n"+F.wens+":\\n"+o.mWens+"\\n\\n"+F.groet+"\\n"+o.mNaam+(o.mMail?"\\n"+o.mMail:"")+"\\n"}}
function ok(o){{if(!o.mNaam||!o.mWens){{$("mMelding").textContent=F.nodig;$("mMelding").className="melding fout";return false}}$("mMelding").textContent="";return true}}
[].forEach.call(document.querySelectorAll("[data-soort]"),function(a){{a.addEventListener("click",function(){{$("mSoort").selectedIndex=+a.getAttribute("data-soort")}})}});
$("maatForm").onsubmit=function(e){{e.preventDefault();var o=lees();if(!ok(o))return;location.href="mailto:"+ADR+"?subject="+encodeURIComponent(F.onderwerp)+"&body="+encodeURIComponent(tekst(o))}};
$("mKopie").onclick=function(){{var o=lees();if(!ok(o))return;var t=F.onderwerp+"\\n\\n"+tekst(o);try{{navigator.clipboard.writeText(t).then(function(){{$("mMelding").textContent=F.gekopieerd+ADR+".";$("mMelding").className="melding ok"}},function(){{prompt(ADR,t)}})}}catch(e){{prompt(ADR,t)}}}};
}})();
</script>
"""
    schrijf(here + "index.html", head(lang, "maat", m["title"], m["desc"], here) + kopbalk(lang, "maat", here) + body + voet(lang, here))

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
<p class="zacht">{"Liever mailen? " if nl else "Prefer e-mail? "}<a href="mailto:{NOTITIE_ADRES}">{NOTITIE_ADRES}</a></p>
<p class="zacht">{"Een wandeling of speurtocht op maat aanvragen? " if nl else "Looking for a walk or treasure hunt made to measure? "}<a href="{r(pad('maat', lang))}">{"Daar is een eigen formulier voor" if nl else "There's a form for that"} &rarr;</a></p></div>
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

# --------------------------------------------------------------------------
# Zoekwoordpagina's: één pagina per zoekvraag, verwijzen naar spellen of wandelingen.
# Nieuwe toevoegen: een sleutel in PAD en LANDING, en opnieuw bouwen.
# --------------------------------------------------------------------------
LANDING = {
 "l_online": dict(soort="spel", planken=None, nl=dict(
   title="Detectivespel online spelen, gratis te beginnen · Enigma Mystery",
   desc="Speel een detectivespel online in je browser: verhoor verdachten, zoek bewijs en wijs de dader aan. Zonder app of account. Van elke soort is een zaak gratis.",
   label="Online", h1="Detectivespel online spelen", zin="Verhoor de verdachten, zoek het bewijs en wijs de dader aan. In je browser, op telefoon of computer.",
   tekst=["Bij Enigma Mystery speel je een detectivespel gewoon in je browser. Je downloadt niets en maakt geen account aan. Open een zaak en je zit meteen aan het bureau.",
          "Er zijn vier soorten zaken. In de verhaalzaken verhoor je verdachten en dien je een aanklacht in. In de escape rooms kijk je in 3D rond en kraak je sloten. De logicapuzzels zijn pen-en-papierpuzzels op het scherm, en de cozy spellen speel je rustig, zonder klok.",
          "Elke zaak is fictief en heeft precies één oplossing. Van elke soort is minstens één zaak gratis. Wil je alles spelen, dan koop je eenmalig de Pro-pas voor €3,99."],
   lijst_label="Gratis om mee te beginnen", lijst_h="Begin met deze zaken",
   faq=[("Is het echt gratis?", "Ja, van elke soort zaak is er minstens één gratis te spelen. De andere zaken speel je met de Pro-pas, eenmalig €3,99."),
        ("Heb ik een app nodig?", "Nee. Alles werkt in de browser van je telefoon, tablet of computer. Je hebt geen account nodig."),
        ("Hoe lang duurt een zaak?", "Van twintig minuten tot een paar avonden, afhankelijk van de zaak. Je voortgang blijft bewaard op je apparaat."),
        ("Kan ik het samen spelen?", "Ja. Veel mensen spelen samen op één scherm en overleggen wie het gedaan heeft.")]),
  en=dict(
   title="Play a detective game online, free to start · Enigma Mystery",
   desc="Play a detective game online in your browser: question suspects, find evidence and name the killer. No app, no account. One case of every kind is free.",
   label="Online", h1="Play a detective game online", zin="Question the suspects, find the evidence and name the killer. In your browser, on phone or computer.",
   tekst=["At Enigma Mystery you play a detective game right in your browser. Nothing to download, no account to make. Open a case and you are at the desk.",
          "There are four kinds of cases. In the story cases you question suspects and file a charge. In the escape rooms you look around in 3D and crack locks. The logic puzzles are pen-and-paper puzzles on screen, and the cozy games play at your own pace, with no clock.",
          "Every case is fictional and has exactly one solution. At least one case of every kind is free. To play everything, buy the Pro pass once for €3.99."],
   lijst_label="Free to start", lijst_h="Start with these cases",
   faq=[("Is it really free?", "Yes, at least one case of every kind is free to play. The other cases are unlocked with the Pro pass, €3.99 once."),
        ("Do I need an app?", "No. Everything runs in the browser of your phone, tablet or computer. No account needed."),
        ("How long does a case take?", "From twenty minutes to a few evenings, depending on the case. Your progress is saved on your device."),
        ("Can we play together?", "Yes. Many people play together on one screen and argue about who did it.")])),
 "l_thuis": dict(soort="spel", planken=("verhaal", "escape"), nl=dict(
   title="Moordmysterie spel voor thuis, voor een avond samen · Enigma Mystery",
   desc="Een moordmysterie spelen voor thuis, met z'n tweeën of met vrienden: verhaalzaken en escape rooms in 3D, gewoon in de browser. Begin gratis.",
   label="Thuis", h1="Moordmysterie spel voor thuis", zin="Een avond samen een moord oplossen, op de bank, op één scherm.",
   tekst=["Zin in een avond speuren, zonder iets te hoeven organiseren? Kies een zaak, zet hem op de laptop of de tv en los hem samen op. Je hebt geen spelleider, geen kaartjes en geen voorbereiding nodig.",
          "De verhaalzaken zijn het meest als een klassiek moordmysterie: verdachten met elk een eigen verhaal, bewijs dat niet klopt en één dader. In de escape rooms lopen jullie zelf rond in een 3D-ruimte en zoeken jullie samen naar de code.",
          "Van elke soort is minstens één zaak gratis, zodat je eerst kunt proberen of het bevalt. Met de Pro-pas (eenmalig €3,99) speel je daarna alle zaken."],
   lijst_label="Voor een avond samen", lijst_h="Verhaalzaken en escape rooms",
   faq=[("Met hoeveel mensen kun je spelen?", "Alleen, met z'n tweeën of met een groepje. Speel op één groot scherm, dan kan iedereen meekijken en meedenken."),
        ("Moet iemand de spelleider zijn?", "Nee. Het spel vertelt het verhaal en controleert je antwoord. Iedereen speelt mee."),
        ("Is het eng?", "Het zijn moordzaken, dus het is spannend. De nadruk ligt op puzzelen en redeneren."),
        ("Kunnen we stoppen en later verder?", "Ja. Je voortgang blijft bewaard op het apparaat waarop je speelt.")]),
  en=dict(
   title="Murder mystery game to play at home · Enigma Mystery",
   desc="A murder mystery to play at home, as a couple or with friends: story cases and 3D escape rooms, right in your browser. Start for free.",
   label="At home", h1="Murder mystery game for at home", zin="An evening of solving a murder together, on the sofa, on one screen.",
   tekst=["Fancy an evening of sleuthing without organising anything? Pick a case, put it on the laptop or TV and solve it together. No game master, no cards, no preparation.",
          "The story cases are closest to a classic murder mystery: suspects who each have their own story, evidence that doesn't add up, and one killer. In the escape rooms you walk around a 3D room yourselves and hunt for the code together.",
          "At least one case of every kind is free, so you can try it first. With the Pro pass (€3.99 once) you can then play every case."],
   lijst_label="For an evening together", lijst_h="Story cases and escape rooms",
   faq=[("How many people can play?", "Alone, as a couple or with a group. Play on one big screen so everyone can watch and think along."),
        ("Does someone have to be the host?", "No. The game tells the story and checks your answer. Everyone plays."),
        ("Is it scary?", "They are murder cases, so it is tense. The focus is on puzzling and reasoning."),
        ("Can we stop and continue later?", "Yes. Your progress is saved on the device you play on.")])),
 "l_vrijgezel": dict(soort="wandel", nl=dict(
   title="Moordmysterie voor een vrijgezellenfeest: moordwandeling · Enigma Mystery",
   desc="Een moordmysterie voor het vrijgezellenfeest: een moordwandeling door je eigen stad, met de bruid of bruidegom in het verhaal. € 9,95 per team of op maat met foto's.",
   label="Vrijgezellenfeest", h1="Moordmysterie voor een vrijgezellenfeest", zin="Los samen een moord op, buiten, in jullie eigen stad. Met de bruid of bruidegom als hoofdpersoon.",
   tekst=["Een moordwandeling is een detectivespel dat je buiten loopt. Jullie starten waar je wilt, en de kaart op de telefoon legt acht sporen op echte plekken in de buurt. Bij elk spoor gaat een stukje van de zaak open: een getuige, een bewijsstuk, een camerabeeld.",
          "Perfect voor een vrijgezellenfeest is Tot de Dood Ons Scheidt: een bruid die vandaag zou trouwen, maar nooit aankwam. Of laat een zaak op maat maken, met foto's van de groep, jullie namen in het verhaal en de vrijgezel als hoofdpersoon.",
          "Eén ticket van € 9,95 geldt voor het hele team. Iedereen vult dezelfde code in, op één telefoon of ieder op een eigen. Een zaak duurt ongeveer anderhalf uur, dus er blijft genoeg tijd over voor de rest van het feest."],
   lijst_label="Zeven zaken op straat", lijst_h="Kies jullie zaak",
   faq=[("Wat kost het?", "Eén ticket van € 9,95 per team. Een gepersonaliseerde versie met foto's, namen en thema kost € 29,95 inclusief ticket."),
        ("In welke stad kan het?", "Overal. De kaart legt de sporen rondom de plek waar jullie starten, in een stad of een dorp."),
        ("Hoe ver van tevoren moet ik een versie op maat aanvragen?", "Vraag een gepersonaliseerde zaak minimaal twee weken van tevoren aan, zodat er tijd is om hem klaar te maken."),
        ("Kunnen we met twee groepen tegen elkaar?", "Ja, bij de Moordwandeling. Kies in de groepszaak 'Teams tegen elkaar': elk team krijgt eigen sporen, en jullie moeten spoorcodes ruilen, eerlijk of niet.")]),
  en=dict(
   title="Murder mystery for a hen or stag party: murder walk · Enigma Mystery",
   desc="A murder mystery for a hen or stag party: a murder walk through your own town, with the bride or groom in the story. € 9.95 per team, or made to measure with photos.",
   label="Hen & stag", h1="Murder mystery for a hen or stag party", zin="Solve a murder together, outside, in your own town. With the bride or groom as the lead.",
   tekst=["A murder walk is a detective game you play on foot. You start wherever you like, and the map on your phone places eight leads at real places nearby. At every lead part of the case opens: a witness, a piece of evidence, a camera still.",
          "A perfect fit for a hen party is Till Death Do Us Part: a bride who was due to marry today but never arrived. Or have a case made to measure, with photos of the group, your names in the story and the bride or groom as the lead.",
          "One € 9.95 ticket covers the whole team. Everyone enters the same code, on one phone or each on their own. A case takes about ninety minutes, leaving plenty of time for the rest of the party."],
   lijst_label="Seven cases on the street", lijst_h="Pick your case",
   faq=[("What does it cost?", "One ticket of € 9.95 per team. A personalised version with photos, names and a theme costs € 29.95 including the ticket."),
        ("Which towns does it work in?", "Anywhere. The map places the leads around the spot where you start, in a city or a village."),
        ("How far ahead should I order a custom version?", "Request a personalised case at least two weeks ahead, so there is time to prepare it."),
        ("Can two groups compete?", "Yes, in the Murder Walk. Choose 'teams against each other' in the group case: every team gets its own leads, and you have to trade lead codes, honestly or not.")])),
 "l_uitje": dict(soort="wandel", nl=dict(
   title="Uitje met vrienden of collega's: een moordwandeling · Enigma Mystery",
   desc="Een origineel uitje met vrienden, familie of collega's: een moordwandeling door je eigen stad, wanneer jullie willen. Proefronde gratis, daarna € 9,95 per team.",
   label="Uitje", h1="Een uitje met een moord erin", zin="Met vrienden, familie of collega's de stad in, op zoek naar een dader. Wanneer jullie willen, zonder reserveren.",
   tekst=["Zoek je een uitje dat niet hetzelfde is als altijd? Met een moordwandeling wordt jullie eigen stad de plaats delict. Jullie lopen samen langs acht sporen, horen getuigen en sluiten verdachten uit tot er één dader overblijft.",
          "Je hoeft niets te reserveren en er komt geen gids mee. Jullie starten wanneer het uitkomt, waar het uitkomt. Elke zaak heeft een gratis proefronde, zodat iedereen eerst ziet hoe het werkt.",
          "Met een grote groep? Kies bij de Moordwandeling de stand teams tegen elkaar: elk team krijgt eigen sporen, en jullie moeten ruilen om de dader te vinden. Voor een bedrijfsuitje of feest kun je ook een zaak op maat laten maken, met jullie namen en foto's."],
   lijst_label="Zeven zaken op straat", lijst_h="Kies jullie zaak",
   faq=[("Wat kost het?", "De proefronde is gratis. Daarna kost een ticket € 9,95 per team, en de code blijft twee maanden geldig."),
        ("Hoe lang duurt het?", "Ongeveer anderhalf uur. Jullie bepalen zelf het tempo en kunnen onderweg pauzeren."),
        ("Kan het in het Engels?", "Ja. Elke zaak is in het Nederlands en het Engels te spelen, handig voor internationale collega's."),
        ("Kan het ook met een hele afdeling?", "Ja. Speel in teams van een paar personen, ieder met een telefoon. Voor een uitje op maat kun je een aanvraag doen.")]),
  en=dict(
   title="Group outing with friends or colleagues: a murder walk · Enigma Mystery",
   desc="An original outing with friends, family or colleagues: a murder walk through your own town, whenever you like. Free trial round, then € 9.95 per team.",
   label="Group outing", h1="An outing with a murder in it", zin="Out into town with friends, family or colleagues, hunting for a killer. Whenever you like, no booking.",
   tekst=["Looking for an outing that isn't the usual? With a murder walk your own town becomes the crime scene. Together you walk past eight leads, hear witnesses and rule out suspects until one killer is left.",
          "Nothing to book and no guide comes along. You start when it suits you, where it suits you. Every case has a free trial round, so everyone sees how it works first.",
          "A big group? In the Murder Walk, choose teams against each other: every team gets its own leads, and you have to trade to find the killer. For a company outing or party you can also have a case made to measure, with your names and photos."],
   lijst_label="Seven cases on the street", lijst_h="Pick your case",
   faq=[("What does it cost?", "The trial round is free. After that a ticket costs € 9.95 per team, and the code stays valid for two months."),
        ("How long does it take?", "About ninety minutes. You set the pace and can take breaks along the way."),
        ("Is it available in English?", "Yes. Every case can be played in English and Dutch, handy for international colleagues."),
        ("Can a whole department play?", "Yes. Split into teams of a few people, each with a phone. For a custom outing you can send a request.")])),
}

def landingpagina(key, lang):
    here = pad(key, lang); r = lambda p: rel(here, p); nl = lang == "nl"
    L = LANDING[key]; d = L[lang]
    if L["soort"] == "wandel":
        W = lambda f: r("assets/wandel/" + f)
        kop = f"""<section class="held wandelheld">
<picture class="beeld"><source media="(max-width:640px)" srcset="{W('hero.webp')}"><img src="{W('hero-breed.webp')}" alt="" fetchpriority="high"></picture>
<div class="binnen"><span class="label">{escape(d['label'])}</span><h1>{escape(d['h1'])}</h1><p class="zin">{escape(d['zin'])}</p>
<div class="knoppen"><a class="knop" href="#zaken">{"Kies een zaak" if nl else "Pick a case"}</a><a class="knop lijn" href="{r(pad('maat', lang))}">{"Op maat" if nl else "Made to measure"}</a></div></div></section>
"""
        basis = r("wandel/nl/" if nl else "wandel/")
        lijst = '<div class="wandelzaken">' + "".join(
            f'<a class="wandelzaak" href="{basis + (pnl if nl else pen)}">' + (f'<span class="zaaklabel">{lab.split("|")[0 if nl else -1]}</span>' if lab else "")
            + f'<span class="medaille"><img src="{W(cov + ".webp")}" alt="" loading="lazy" width="320" height="320"></span>'
            f'<h3>{escape(tnl if nl else ten)}</h3><p>{escape(hnl if nl else hen)}</p><span class="pijl">{"Bekijk de zaak" if nl else "View the case"} &rarr;</span></a>'
            for cov, pnl, pen, tnl, ten, hnl, hen, lab in WANDELZAKEN) + '</div>'
    else:
        kop = held(here, lang, f'<span class="label">{escape(d["label"])}</span><h1>{escape(d["h1"])}</h1><p class="zin">{escape(d["zin"])}</p>'
                   f'<div class="knoppen"><a class="knop" href="#zaken">{"Kies een zaak" if nl else "Pick a case"}</a><a class="knop lijn" href="{r(pad("spellen", lang))}">{"Alle spellen" if nl else "All games"}</a></div>', klein=True)
        idx = [i for i, s in enumerate(SPELLEN) if (L["planken"] is None or s["plank"] in L["planken"])]
        idx.sort(key=lambda i: (SPELLEN[i]["status"] != "gratis", SPELLEN[i]["added"]))
        lijst = '<div class="rij">' + "".join(kaart(i, lang, here) for i in idx[:8]) + '</div>'
    tekst = "".join(f'<p class="zacht">{escape(x)}</p>' for x in d["tekst"])
    faq = "".join(f'<details class="maatvraag"><summary>{escape(q)}</summary><p>{escape(a)}</p></details>' for q, a in d["faq"])
    ander = "".join(f'<a class="knop lijn" href="{r(pad(k, lang))}">{escape(LANDING[k][lang]["h1"])}</a>' for k in LANDING if k != key)
    ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d["faq"]]}, ensure_ascii=False)
    body = kop + f"""<section class="sectie"><div class="binnen">
<div class="sectiekop"><span class="label">{escape(d['label'])}</span><h2>{"Zo werkt het" if nl else "How it works"}</h2>{tekst}</div></div></section>
<section class="sectie" id="zaken"><div class="binnen">
<div class="sectiekop"><span class="label">{escape(d['lijst_label'])}</span><h2>{escape(d['lijst_h'])}</h2></div>
{lijst}</div></section>
<section class="sectie"><div class="binnen"><div class="maatvragen"><span class="label">{"Veelgestelde vragen" if nl else "Questions"}</span>{faq}</div></div></section>
{maatband(lang, here)}<section class="sectie"><div class="binnen"><div class="sectiekop"><span class="label">{"Meer ideeën" if nl else "More ideas"}</span></div><div class="knoppen">{ander}</div></div></section>
<script type="application/ld+json">{ld}</script>
"""
    schrijf(here + "index.html", head(lang, key, d["title"], d["desc"], here) + kopbalk(lang, key, here) + body + voet(lang, here))

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
<meta name="google-site-verification" content="r1TDU1p7uliOPfeb9qhqcrNB5rykBlty_8ieMLZes0M">
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
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /_tools/\nDisallow: /wandel/codes.html\nSitemap: {SITE}/sitemap.xml\n")
    urls = ["", *(pad(k, l) for k in PAD for l in ("nl", "en"))]
    spel = sorted({s[l][2].split("#")[0] for s in SPELLEN for l in ("nl", "en")})
    vandaag = date.today().isoformat()
    rows = "".join(f"<url><loc>{SITE}/{u}</loc><lastmod>{vandaag}</lastmod></url>\n" for u in urls)
    rows += "".join(f"<url><loc>{SITE}/spel/{u}</loc><lastmod>{vandaag}</lastmod></url>\n" for u in spel)
    wsm = ROOT / "wandel" / "sitemap-bron.xml"   # sitemap van de wandel-app, samengevoegd
    if wsm.exists():
        import re as _re
        rows += "".join(m + "\n" for m in _re.findall(r"<url>.*?</url>", wsm.read_text(encoding="utf-8"), _re.S))
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + rows + "</urlset>\n")

def main():
    for f in ["spel/" + s[l][2].split("#")[0] for s in SPELLEN for l in ("nl", "en")]:
        assert (ROOT / f).exists(), "ontbreekt: " + f
    for s in SPELLEN:
        assert (ROOT / "assets/dossiers" / (s["art"] + ".jpg")).exists(), s["art"]
    taalkeuze()
    for lang in ("nl", "en"):
        voorpagina(lang); spellenpagina(lang); wandelpagina(lang); boekenpagina(lang); propagina(lang); overpagina(lang); contactpagina(lang); maatpagina(lang)
        for k in LANDING: landingpagina(k, lang)
    extra()
    print("klaar:", len(SPELLEN), "spellen,", "nieuw:", [SPELLEN[i]["en"][0] for i in NIEUW])

main()
