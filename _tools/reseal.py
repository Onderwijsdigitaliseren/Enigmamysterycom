#!/usr/bin/env python3
"""Opent verzegelde Pro-bestanden, past merknaam en geluid aan, en verzegelt opnieuw.

Gebruik: python3 _tools/reseal.py PASCODE [bestand ...]   (zonder bestanden: alle verzegelde in /spel/)

Salt en sleutellijst blijven gelijk, dus alle bestaande pascodes blijven werken.
Alleen de versleutelde inhoud wordt vervangen. De open inhoud komt nooit op schijf.
"""
import sys, re, json, base64, gzip, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from branding import convert_text

ROOT = Path(__file__).resolve().parent.parent

# Geluid standaard uit; de speler zet het aan met de knop in het spel.
SOUND_OFF = {
    "grondplan.html": [("geluid:true", "geluid:false")],
    "the-floor-plan.html": [("geluid:true", "geluid:false")],
    "schakelkamer.html": [('fase:"omslag", geluid:true,', 'fase:"omslag", geluid:false,')],
    "the-switch-room.html": [('fase:"omslag", geluid:true,', 'fase:"omslag", geluid:false,')],
    "nachtfrequentie.html": [("talked:{}, muted:false,", "talked:{}, muted:true,")],
    "night-frequency.html": [("talked:{}, muted:false,", "talked:{}, muted:true,")],
    "the-homicide-desk.html": [("mute: 0", "mute: 1")],
    "the-empty-barrel.html": [
        ("let snd=localStorage.getItem('lr_snd')!=='0'", "let snd=localStorage.getItem('lr_snd')==='1'"),
        ('<button id="bSnd" class="on">', '<button id="bSnd">'),
        ("$('bSnd').onclick=", "$('bSnd').classList.toggle('on',snd);$('bSnd').onclick="),
    ],
    # Laatst gezien: één piep op het laadscherm, geen knop; de piep vervalt.
    "last-seen-2314.html": [("try{ beep(); }catch(e){}", "")],
}
# Ravenhorst / Ravenscourt hadden geluid zonder knop: knop erbij, standaard uit.
RAVEN = {
    "ravenhorst.html": ("Geluid", "Geluid aan", "Geluid uit"),
    "ravenscourt.html": ("Sound", "Sound on", "Sound off"),
}

def patch_raven(name, s):
    titel, aan, uit = RAVEN[name]
    if 'id="geluidKnop"' in s:
        return s  # al gedaan
    knop = f'<button class="kopknop" id="geluidKnop" type="button" aria-pressed="false" title="{titel}">&#9834;</button>'
    old = '<button class="kopknop" id="resetKnop">'
    assert s.count(old) == 1, name
    s = s.replace(old, knop + old)
    old = "let AC=null;\nfunction audioInit(){if(!AC){try{AC=new (window.AudioContext||window.webkitAudioContext)();}catch(e){}}}\nfunction toon(f,d,type,vol,tijd){if(!AC)return;try{"
    assert s.count(old) == 1, name
    new = ("let AC=null;let geluidAan=false;try{geluidAan=localStorage.getItem('rh_geluid')==='1';}catch(e){}\n"
           "function audioInit(){if(!geluidAan)return;if(!AC){try{AC=new (window.AudioContext||window.webkitAudioContext)();}catch(e){}}if(AC&&AC.state==='suspended')AC.resume();}\n"
           "function zetGeluidKnop(){const k=document.getElementById('geluidKnop');if(!k)return;k.setAttribute('aria-pressed',geluidAan?'true':'false');k.style.opacity=geluidAan?1:.45;k.title=geluidAan?" + json.dumps(uit) + ":" + json.dumps(aan) + ";}\n"
           "document.addEventListener('DOMContentLoaded',function(){zetGeluidKnop();const k=document.getElementById('geluidKnop');if(k)k.addEventListener('click',function(){geluidAan=!geluidAan;try{localStorage.setItem('rh_geluid',geluidAan?'1':'0');}catch(e){}audioInit();zetGeluidKnop();if(geluidAan)toon(660,.12,'sine',.06);});});\n"
           "function toon(f,d,type,vol,tijd){if(!AC||!geluidAan)return;try{")
    return s.replace(old, new)

def patch(name, s):
    s = convert_text(s)
    for old, new in SOUND_OFF.get(name, []):
        if old in s:
            s = s.replace(old, new)
    if name in RAVEN:
        s = patch_raven(name, s)
    return s

def main():
    code = re.sub(r"[^A-Z0-9]", "", sys.argv[1].upper())
    files = [Path(f) for f in sys.argv[2:]] or sorted(p for p in (ROOT / "spel").glob("*.html") if 'id="gfpro"' in p.read_text(encoding="utf-8"))
    for f in files:
        s = f.read_text(encoding="utf-8")
        m = re.search(r'(<script type="application/json" id="gfpro">)(.*?)(</script>)', s, re.S)
        P = json.loads(m.group(2))
        kek = PBKDF2HMAC(hashes.SHA256(), 32, base64.b64decode(P["salt"]), P["it"]).derive(code.encode())
        ck = None
        for w in P["keys"]:
            w = base64.b64decode(w)
            try: ck = AESGCM(kek).decrypt(w[:12], w[12:], None); break
            except Exception: pass
        if not ck:
            print("OVERGESLAGEN, code past niet:", f.name); continue
        d = base64.b64decode(P["data"])
        plat = AESGCM(ck).decrypt(d[:12], d[12:], None)
        if P.get("z"): plat = gzip.decompress(plat)
        html = plat.decode("utf-8")
        nieuw = patch(f.name, html)
        if nieuw == html and convert_text(s) == s:
            print("ongewijzigd:", f.name); continue
        data = gzip.compress(nieuw.encode("utf-8"), 9)
        iv = os.urandom(12)
        P["data"] = base64.b64encode(iv + AESGCM(ck).encrypt(iv, data, None)).decode()
        P["z"] = 1
        # controle: terug ontsleutelen moet exact de nieuwe inhoud geven
        d2 = base64.b64decode(P["data"])
        assert gzip.decompress(AESGCM(ck).decrypt(d2[:12], d2[12:], None)).decode("utf-8") == nieuw
        P["title"] = convert_text(P["title"])
        if P.get("teaser"): P["teaser"] = convert_text(P["teaser"])
        out = convert_text(s[:m.start()]) + m.group(1) + json.dumps(P, ensure_ascii=False, separators=(",", ":")) + m.group(3) + convert_text(s[m.end():])
        tmp = f.with_suffix(".tmp"); tmp.write_text(out, encoding="utf-8"); os.replace(tmp, f)
        rest = len(re.findall(r"raveyard|achtdossier", nieuw))
        print(f"herverzegeld: {f.name:28} {len(html):>8} -> {len(nieuw):>8} tekens, oude naam nog {rest}x")

main()
