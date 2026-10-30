#!/usr/bin/env python3
"""Verzegelt een nieuw spel als Pro-dossier, met dezelfde salt en sleutellijst als
de bestaande Pro-dossiers (alle bestaande pascodes werken dus meteen).

Gebruik:
  python3 _tools/seal.py PASCODE open_spel.html spel/doelnaam.html --taal en \
      --titel "The Clippings Room" --teaser "..." --beschrijving "..."

Het open bronbestand komt nooit in de repo; alleen het verzegelde resultaat.
"""
import argparse, base64, gzip, json, os, re, sys
from pathlib import Path
from html import escape
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ROOT = Path(__file__).resolve().parent.parent
SJABLOON = ROOT / "spel" / "halfmoon.html"   # bestaand verzegeld omhulsel als basis
SITE = "https://www.enigmamystery.com"

a = argparse.ArgumentParser()
a.add_argument("code"); a.add_argument("bron"); a.add_argument("doel")
a.add_argument("--taal", default="en"); a.add_argument("--titel", required=True)
a.add_argument("--teaser", default=""); a.add_argument("--beschrijving", default="")
x = a.parse_args()

code = re.sub(r"[^A-Z0-9]", "", x.code.upper())
s = SJABLOON.read_text(encoding="utf-8")
m = re.search(r'(<script type="application/json" id="gfpro">)(.*?)(</script>)', s, re.S)
P = json.loads(m.group(2))
kek = PBKDF2HMAC(hashes.SHA256(), 32, base64.b64decode(P["salt"]), P["it"]).derive(code.encode())
ck = None
for w in P["keys"]:
    w = base64.b64decode(w)
    try: ck = AESGCM(kek).decrypt(w[:12], w[12:], None); break
    except Exception: pass
if not ck: sys.exit("code past niet")

plat = Path(x.bron).read_bytes()
iv = os.urandom(12)
data = base64.b64encode(iv + AESGCM(ck).encrypt(iv, gzip.compress(plat, 9), None)).decode()
naam = Path(x.doel).name
N = dict(P, lang=x.taal, title=x.titel, teaser=x.teaser, data=data, z=1,
         hub="../nl/spellen/#archief-2" if x.taal == "nl" else "../en/games/#archief-2")

head, tail = s[:m.start()], s[m.end():]
url = f"{SITE}/spel/{naam}"
beschr = escape(x.beschrijving or x.teaser)
head = re.sub(r"<title>.*?</title>", f"<title>{escape(x.titel)} | Enigma Mystery</title>", head, count=1, flags=re.S)
head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{beschr}">', head, count=1)
head = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', head, count=1)
head = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{escape(x.titel)} – Enigma Mystery">', head, count=1)
head = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{beschr}">', head, count=1)
head = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', head, count=1)
head = head.replace('<html lang="en">', f'<html lang="{x.taal}">', 1)
out = head + m.group(1) + json.dumps(N, ensure_ascii=False, separators=(",", ":")) + m.group(3) + tail
Path(x.doel).write_text(out, encoding="utf-8")

# controle: terug ontsleutelen geeft exact de bron
d = base64.b64decode(N["data"])
assert gzip.decompress(AESGCM(ck).decrypt(d[:12], d[12:], None)) == plat
print(f"verzegeld: {naam} ({len(plat)} -> {len(out)} bytes)")
