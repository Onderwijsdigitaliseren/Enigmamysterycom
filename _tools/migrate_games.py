#!/usr/bin/env python3
"""Zet de spelbestanden van graveyardfiles over naar Enigma Mystery.

Gebruik: python3 _tools/migrate_games.py <map-met-oude-graveyardfiles-repo>

- Kopieert elk spel naar /spel/ (Engelse namen uit de root, Nederlandse uit /nl/).
- Vervangt merknaam en links (The Graveyard Files / Het Nachtdossier -> Enigma Mystery,
  "Nachtdossier 44-C" -> "Dossier 44-C", graveyardfiles.com -> www.enigmamystery.com).
- Laat opslagsleutels (graveyardfiles_..., nachtdossier_...) ongemoeid.
- Verzegelde Pro-bestanden: alleen het omhulsel en de publieke instellingen
  (hub-link, titel) worden aangepast; de versleutelde inhoud blijft gelijk.
"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

SRC = Path(sys.argv[1])
DST = Path(__file__).resolve().parent.parent / "spel"
DST.mkdir(exist_ok=True)

from branding import RENAME, ALL, SITE, convert_text

# Samengevoegd tot één tweetalig bestand (#nl / #en): de NL-kopie wordt niet meer overgezet.
MERGED = {"de-zwarte-kolom.html": "the-black-column.html", "hotel-winterlicht.html": "hotel-winterlight.html"}
EN_FILES = [p.name for p in SRC.glob("*.html") if p.name not in ("index.html", "hotel-winterlicht.html")]
NL_FILES = [p.name for p in (SRC / "nl").glob("*.html") if p.name != "index.html" and p.name not in MERGED]
def convert_sealed(s, lang):
    m = re.search(r'(<script type="application/json" id="gfpro">)(.*?)(</script>)', s, re.S)
    head, body, tail = s[:m.start()], m.group(2), s[m.end():]
    P = json.loads(body)
    P["hub"] = "../nl/spellen/" if lang == "nl" else "../en/games/"
    P["title"] = convert_text(P["title"])
    if P.get("teaser"):
        P["teaser"] = convert_text(P["teaser"])
    new_json = json.dumps(P, ensure_ascii=False, separators=(",", ":"))
    return convert_text(head) + m.group(1) + new_json + m.group(3) + convert_text(tail)

# Geluid staat standaard uit; spelers zetten het zelf aan met de geluidsknop in het spel.
SOUND_OFF = {
    "de-zwarte-kolom.html": [("geluid:true, zaken:{}", "geluid:false, zaken:{}")],
    "the-black-column.html": [("geluid:true, zaken:{}", "geluid:false, zaken:{}")],
    "hotel-winterlicht.html": [('"scratch":{},"sound":true}', '"scratch":{},"sound":false}')],
    "hotel-winterlight.html": [('"scratch":{},"sound":true}', '"scratch":{},"sound":false}')],
    "graveyard-match.html": [("let P={lang:'nl',sound:true,", "let P={lang:'nl',sound:false,")],
    "nachtportier.html": [("concl:false,stil:false", "concl:false,stil:true")],
    "the-night-porter.html": [("concl:false,stil:false", "concl:false,stil:true")],
    "the-inheritance.html": [("let S={lang:'nl',mute:false,", "let S={lang:'nl',mute:true,")],
    "the-last-candle.html": [("tries:0,time:0,sound:true,", "tries:0,time:0,sound:false,")],
    "the-pawnbrokers-ledger.html": [("fin:false,snd:true}", "fin:false,snd:false}")],
    "the-silent-village.html": [('notes:"",snd:true}', 'notes:"",snd:false}')],
    "the-stopped-clock.html": [
        ("let snd=localStorage.getItem('lr_snd')!=='0';", "let snd=localStorage.getItem('lr_snd')==='1';"),
        ('<button id="bSnd" class="on">', '<button id="bSnd">'),
        ("$('bSnd').onclick=", "$('bSnd').classList.toggle('on',snd);$('bSnd').onclick="),
    ],
}

# Tweetalig maken: starttaal uit #nl / #en, anders de sitekeuze (mm_lang), anders Engels.
MERGE = {
    "the-black-column.html": [
        ('const STANDAARD = "en";',
         'const HASHTAAL = location.hash === "#nl" ? "nl" : location.hash === "#en" ? "en" : "";\n'
         'const STANDAARD = HASHTAAL || (function(){ try { const l = localStorage.getItem("mm_lang"); if (l === "nl" || l === "en") return l; } catch(e){} return "en"; })();'),
        ('const TAALSLEUTEL = "graveyardfiles_zwartekolom_taal_" + STANDAARD;', 'const TAALSLEUTEL = "graveyardfiles_zwartekolom_taal";'),
        ('    if(tl === "nl" || tl === "en") taal = tl;', '    if(!HASHTAAL && (tl === "nl" || tl === "en")) taal = tl;'),
        ('  try { Kluis.schrijf(TAALSLEUTEL, taal); } catch(e){}\n  if(huidig)', '  try { Kluis.schrijf(TAALSLEUTEL, taal); history.replaceState(null, "", "#" + taal); } catch(e){}\n  if(huidig)'),
        ('<link rel="alternate" hreflang="nl" href="https://www.enigmamystery.com/spel/de-zwarte-kolom.html">', '<link rel="alternate" hreflang="nl" href="https://www.enigmamystery.com/spel/the-black-column.html#nl">'),
        ('<link rel="alternate" hreflang="en" href="https://www.enigmamystery.com/spel/the-black-column.html">', '<link rel="alternate" hreflang="en" href="https://www.enigmamystery.com/spel/the-black-column.html#en">'),
        ('<title>The Black Column – three murder puzzles on a deduction grid | Enigma Mystery</title>', '<title>The Black Column · De Zwarte Kolom | Enigma Mystery</title>'),
    ],
    "hotel-winterlight.html": [
        ("let lang = (localStorage.getItem('hm_lang')) || 'en';",
         "let lang = location.hash === '#nl' ? 'nl' : location.hash === '#en' ? 'en' : (localStorage.getItem('hm_lang') || localStorage.getItem('mm_lang') || 'en'); if (lang !== 'nl') lang = 'en';"),
        ("document.getElementById('langbtn').onclick=()=>{ lang=lang==='nl'?'en':'nl'; save();", "document.getElementById('langbtn').onclick=()=>{ lang=lang==='nl'?'en':'nl'; save(); try{history.replaceState(null,'','#'+lang);}catch(e){}"),
        ('<link rel="alternate" hreflang="en" href="https://www.enigmamystery.com/spel/hotel-winterlight.html">', '<link rel="alternate" hreflang="en" href="https://www.enigmamystery.com/spel/hotel-winterlight.html#en">'),
        ('<link rel="alternate" hreflang="nl" href="https://www.enigmamystery.com/spel/hotel-winterlicht.html">', '<link rel="alternate" hreflang="nl" href="https://www.enigmamystery.com/spel/hotel-winterlight.html#nl">'),
        ('<title>Hotel Winterlight · Floor 7 – a free floor of murder puzzles | Enigma Mystery</title>', '<title>Hotel Winterlight · Hotel Winterlicht | Enigma Mystery</title>'),
    ],
}

def merge(name, s):
    for old, new in MERGE.get(name, []):
        assert s.count(old) == 1, f"samenvoeg-patroon niet (uniek) gevonden in {name}: {old[:60]}"
        s = s.replace(old, new)
    return s

def sound_off(name, s):
    for old, new in SOUND_OFF.get(name, []):
        assert s.count(old) == 1, f"geluid-patroon niet (uniek) gevonden in {name}: {old}"
        s = s.replace(old, new)
    return s

def run():
    done = []
    for folder, names in ((SRC, EN_FILES), (SRC / "nl", NL_FILES)):
        for name in names:
            s = (folder / name).read_text(encoding="utf-8")
            if 'id="gfpro"' in s:
                lang = json.loads(re.search(r'id="gfpro">(.*?)</script>', s, re.S).group(1)).get("lang", "en")
                out = convert_sealed(s, lang)
                kind = "verzegeld"
            else:
                out = convert_text(s)
                kind = "open"
            out = merge(name, sound_off(name, out))
            target = DST / RENAME.get(name, name)
            if kind == "verzegeld" and target.exists():
                done.append((target.name, "bestaat al (verzegeld, niet overschreven)")); continue
            target.write_text(out, encoding="utf-8")
            done.append((target.name, kind))
    for n, k in sorted(done):
        print(f"{k:10} {n}")
    print(len(done), "bestanden")

run()
