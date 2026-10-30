"""Merknaam- en linkvervangingen voor spelbestanden (gedeeld door migrate_games.py en reseal.py)."""
import re

RENAME = {"graveyard-match.html": "enigma-match.html"}
ALL = {"de-lichttafel.html","de-zwarte-kolom.html","grondplan.html","halfmoon.html","halvemaan.html","hotel-winterlicht.html","hotel-winterlight.html","last-seen-2314.html","graveyard-match.html","meridian-house.html","nachtfrequentie.html","nachtportier.html","nachttrein212.html","night-frequency.html","night-train-212.html","ravenhorst.html","ravenscourt.html","schakelkamer.html","seaview.html","the-black-column.html","the-empty-barrel.html","the-floor-plan.html","the-homicide-desk.html","the-inheritance.html","the-last-candle.html","the-light-table.html","the-night-porter.html","the-pawnbrokers-ledger.html","the-silent-village.html","the-stopped-clock.html","the-switch-room.html","villa-meridiaan.html","zeezicht.html"}

SITE = "https://www.enigmamystery.com"

def url_map(m):
    path = m.group(1) or ""
    path = path.lstrip("/")
    if path.startswith("nl/"):
        rest = path[3:]
        if rest in ("", "index.html"):
            return SITE + "/nl/spellen/"
        return SITE + "/spel/" + RENAME.get(rest, rest)
    if path in ("", "index.html"):
        return SITE + "/en/games/"
    if path == "hotel-winterlicht":
        return SITE + "/nl/puzzels/#hotel-winterlicht"
    if path == "hotel-winterlight":
        return SITE + "/en/puzzles/#hotel-winterlight"
    base = path.split("#")[0].split("?")[0]
    if base in ALL:
        return SITE + "/spel/" + RENAME.get(path, path)
    return SITE + "/" + path

TEXT = [
    # links eerst
    (re.compile(r"https?://(?:www\.)?graveyardfiles\.com(/[A-Za-z0-9_./#-]*)?"), url_map),
    (re.compile(r"graveyardfiles\\\.com"), lambda m: r"enigmamystery\.com"),
    # merknaam
    (re.compile(r"Een Nachtdossier-prototype"), lambda m: "Een Enigma Mystery-prototype"),
    (re.compile(r"A Graveyard Files prototype"), lambda m: "A Enigma Mystery prototype"),
    (re.compile(r"Het Nachtdossier / The Graveyard Files"), lambda m: "Enigma Mystery"),
    (re.compile(r"The Graveyard Files"), lambda m: "Enigma Mystery"),
    (re.compile(r"Het Nachtdossier"), lambda m: "Enigma Mystery"),
    (re.compile(r"Graveyard Match"), lambda m: "Enigma Match"),
    (re.compile(r"Nachtdossier(?=[ -]\d)"), lambda m: "Dossier"),
    (re.compile(r"Night File(?= \d)"), lambda m: "File"),
    (re.compile(r"Nachtdossier(?= · Zaak)"), lambda m: "Enigma Mystery"),
    (re.compile(r"Graveyard Files(?= · Case)"), lambda m: "Enigma Mystery"),
    (re.compile(r"&middot; nachtdossier<"), lambda m: "&middot; Enigma Mystery<"),
    (re.compile(r"&middot; graveyard file<"), lambda m: "&middot; Enigma Mystery<"),
    (re.compile(r"A Graveyard Files deduction game"), lambda m: "A Enigma Mystery deduction game"),
    # losse domeinnaam in deeltekst en voetregels
    (re.compile(r"(?<=\\n)graveyardfiles\.com"), lambda m: "www.enigmamystery.com"),
    (re.compile(r"(?<![\w/.])graveyardfiles\.com(?![\w])"), lambda m: "www.enigmamystery.com"),
]

# Al eerder omgezette bestanden (MaxiMystery-periode)
TEXT += [
    (re.compile(r"https://maximystery\.nl/spel/maximystery-match\.html"), lambda m: SITE + "/spel/enigma-match.html"),
    (re.compile(r"https://maximystery\.nl/nl/boeken/"), lambda m: SITE + "/nl/puzzels/"),
    (re.compile(r"https://maximystery\.nl/en/books/"), lambda m: SITE + "/en/puzzles/"),
    (re.compile(r"https://maximystery\.nl"), lambda m: SITE),
    (re.compile(r"maximystery\\\.nl"), lambda m: r"enigmamystery\.com"),
    (re.compile(r"(?<![\w/.])maximystery\.nl(?![\w])"), lambda m: "www.enigmamystery.com"),
    (re.compile(r"MaxiMystery Match"), lambda m: "Enigma Match"),
    (re.compile(r"MaxiMystery"), lambda m: "Enigma Mystery"),
]

def convert_text(s):
    for rx, fn in TEXT:
        s = rx.sub(fn, s)
    return s

