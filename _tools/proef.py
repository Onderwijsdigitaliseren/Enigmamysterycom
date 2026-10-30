#!/usr/bin/env python3
"""Maakt van een verzegelde kast-bundel (zoals Het Grondplan) een proefversie:
de eerste dossiers zijn gratis, de rest zit versleuteld in hetzelfde bestand en
gaat open met de bestaande Pro-pascode (zelfde salt en sleutellijst, dus alle
bestaande codes werken).

Gebruik: python3 _tools/proef.py PASCODE AANTAL_GRATIS bestand.html [bestand.html ...]

Werkt op bestanden die nog helemaal verzegeld zijn (gfpro-omhulsel) en een
`const DOSSIERS = {...};` hebben met de kastcode van Het Grondplan.
"""
import sys, re, json, base64, gzip, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ARCHIEF = {"nl": "Archief I", "en": "Archive I"}
PRO_PAGINA = {"nl": "../nl/pro/", "en": "../en/pro/"}

T = {
 "nl": dict(status="ARCHIEF I · PRO", rij="Dit dossier hoort bij Archief I. Open het met je Pro-pas.",
            knop="ontgrendel", titel="Archief I openen", uitleg="Dossier I is gratis. Met de Pro-pas van Archief I gaan dossier II tot en met V open, en alle andere Pro-spellen van Enigma Mystery.",
            label="Pascode", open="Open", koop="Haal de Pro-pas", sluit="Sluiten",
            fout="Die code opent Archief I niet. Controleer op typfouten.", bezig="Bezig…", geen="Deze browser kan verzegelde dossiers niet openen."),
 "en": dict(status="ARCHIVE I · PRO", rij="This file belongs to Archive I. Open it with your Pro pass.",
            knop="unlock", titel="Open Archive I", uitleg="File I is free. The Archive I Pro pass opens files II to V, and every other Enigma Mystery Pro game.",
            label="Pass code", open="Open", koop="Get the Pro pass", sluit="Close",
            fout="That code does not open Archive I. Check for typos.", bezig="Checking…", geen="This browser cannot open sealed files."),
}

def b64(b): return base64.b64encode(b).decode()

def unseal(s, code):
    m = re.search(r'id="gfpro">(.*?)</script>', s, re.S)
    P = json.loads(m.group(1))
    kek = PBKDF2HMAC(hashes.SHA256(), 32, base64.b64decode(P["salt"]), P["it"]).derive(code.encode())
    ck = None
    for w in P["keys"]:
        w = base64.b64decode(w)
        try: ck = AESGCM(kek).decrypt(w[:12], w[12:], None); break
        except Exception: pass
    if not ck: raise SystemExit("code past niet")
    d = base64.b64decode(P["data"]); plat = AESGCM(ck).decrypt(d[:12], d[12:], None)
    if P.get("z"): plat = gzip.decompress(plat)
    return P, ck, plat.decode("utf-8")

def rep(s, old, new, n=1):
    assert s.count(old) == n, f"patroon {n}x verwacht, {s.count(old)}x gevonden: {old[:70]}"
    return s.replace(old, new)

def maak(path, code, gratis):
    s = path.read_text(encoding="utf-8")
    P, ck, html = unseal(s, code)
    lang = "nl" if 'lang="nl"' in html[:300] else "en"
    t = T[lang]
    html = html.replace("Lade II", ARCHIEF["nl"]).replace("Drawer II", ARCHIEF["en"])

    m = re.search(r'const DOSSIERS = (\{.*?\});\n', html, re.S)
    alle = json.loads(m.group(1))
    vrij = {k: v for k, v in alle.items() if int(k) <= gratis}
    pro = {k: v for k, v in alle.items() if int(k) > gratis}
    data = gzip.compress(json.dumps(pro, ensure_ascii=False).encode(), 9)
    iv = os.urandom(12)
    blob = {"salt": P["salt"], "it": P["it"], "keys": P["keys"], "z": 1, "data": b64(iv + AESGCM(ck).encrypt(iv, data, None))}
    vrij_js = json.dumps(vrij, ensure_ascii=False).replace("</", "<\\/")
    html = html[:m.start()] + "const DOSSIERS = " + vrij_js + ";\nconst DOSSIERS_PRO = " + json.dumps(blob) + ";\n" + html[m.end():]

    # slot op de Pro-dossiers
    html = rep(html, "function toegankelijk(i, staten){\n  if (i === 0) return true;",
               "function isPro(n){ return !DOSSIERS[n]; }\nfunction toegankelijk(i, staten){\n  if (isPro(META[i].n)) return false;\n  if (i === 0) return true;")
    html = rep(html, "    const status = !open ? '<div class=\"status zegel\">",
               "    const pro = isPro(m.n);\n    const status = pro ? '<div class=\"status zegel\">" + t["status"] + "</div>' : !open ? '<div class=\"status zegel\">")
    html = rep(html, "    const zegelrij = !open\n",
               "    const zegelrij = pro\n      ? '<div class=\"zegelrij\"><span>" + t["rij"] + "</span><button data-pro=\"1\">" + t["knop"] + "</button></div>'\n      : !open\n")
    html = rep(html, '  cont.querySelectorAll("[data-zegel]").forEach(el => {',
               '  cont.querySelectorAll("[data-pro]").forEach(el => el.addEventListener("click", toonProSlot));\n  cont.querySelectorAll("[data-zegel]").forEach(el => {')
    html = rep(html, '<div id="slot" style="display:none"></div>',
               '<div id="proslot" style="display:none"></div>\n      <div id="slot" style="display:none"></div>')

    ui = {k: t[k] for k in ("titel", "uitleg", "label", "open", "koop", "sluit", "fout", "bezig", "geen")}
    js = """
/* ---- Archief I: Pro-dossiers openen met de bestaande pascode ---- */
const PRO_T = %s;
const PRO_KEY = "gf_pro_code";
function proNorm(c){ return String(c || "").toUpperCase().replace(/[^A-Z0-9]/g, ""); }
function proB64(s){ const b = atob(s), u = new Uint8Array(b.length); for (let i = 0; i < b.length; i++) u[i] = b.charCodeAt(i); return u; }
async function proOpen(code){
  const P = DOSSIERS_PRO, S = crypto.subtle;
  const basis = await S.importKey("raw", new TextEncoder().encode(proNorm(code)), "PBKDF2", false, ["deriveKey"]);
  const kek = await S.deriveKey({ name:"PBKDF2", salt:proB64(P.salt), iterations:P.it, hash:"SHA-256" }, basis, { name:"AES-GCM", length:256 }, false, ["decrypt"]);
  let ck = null;
  for (const k of P.keys){ const w = proB64(k); try { ck = await S.decrypt({ name:"AES-GCM", iv:w.subarray(0,12) }, kek, w.subarray(12)); break; } catch(e){} }
  if (!ck) return false;
  const key = await S.importKey("raw", ck, "AES-GCM", false, ["decrypt"]);
  const d = proB64(P.data);
  let plat = await S.decrypt({ name:"AES-GCM", iv:d.subarray(0,12) }, key, d.subarray(12));
  plat = await new Response(new Blob([plat]).stream().pipeThrough(new DecompressionStream("gzip"))).arrayBuffer();
  Object.assign(DOSSIERS, JSON.parse(new TextDecoder().decode(plat)));
  try { localStorage.setItem(PRO_KEY, proNorm(code)); } catch(e){}
  return true;
}
function toonProSlot(){
  const el = $("#proslot");
  el.style.display = "";
  el.innerHTML = '<div class="dossier"><div class="binnen" style="display:block">'
    + '<div class="titel">' + PRO_T.titel + '</div>'
    + '<div class="oms" style="margin:6px 0 10px">' + PRO_T.uitleg + '</div>'
    + '<form id="proform" style="display:flex;gap:8px;flex-wrap:wrap;align-items:center">'
    + '<label for="procode" class="meta" style="margin:0">' + PRO_T.label + '</label>'
    + '<input id="procode" autocomplete="off" autocapitalize="characters" spellcheck="false" style="flex:1;min-width:160px;font:16px monospace;letter-spacing:2px;text-transform:uppercase;padding:9px;border:1px solid #9d9072;background:#fff8">'
    + '<button class="knop rood" type="submit">' + PRO_T.open + '</button></form>'
    + '<p id="promelding" class="oms" role="status" style="min-height:1.4em;margin-top:6px;color:#8e2b20"></p>'
    + '<p class="oms"><a href="%s" target="_top" style="color:#8e2b20">' + PRO_T.koop + ' &rarr;</a>'
    + ' &nbsp;·&nbsp; <button type="button" id="prosluit" style="color:#5a4a33;border-bottom:1px dashed">' + PRO_T.sluit + '</button></p>'
    + '</div></div>';
  el.scrollIntoView({ behavior:"smooth", block:"center" });
  $("#prosluit").onclick = () => { el.style.display = "none"; };
  $("#proform").onsubmit = async (e) => {
    e.preventDefault();
    const meld = $("#promelding");
    if (!(window.crypto && crypto.subtle && typeof DecompressionStream !== "undefined")){ meld.textContent = PRO_T.geen; return; }
    meld.textContent = PRO_T.bezig;
    let ok = false; try { ok = await proOpen($("#procode").value); } catch(err){}
    if (ok){ el.style.display = "none"; renderKast(); } else meld.textContent = PRO_T.fout;
  };
}
""" % (json.dumps(ui, ensure_ascii=False), PRO_PAGINA[lang])
    html = rep(html, "\nfunction init(){", js + "\nfunction init(){")
    html = rep(html, "init();\n</script>",
               "(async function(){ let c = \"\"; try { c = localStorage.getItem(PRO_KEY) || \"\"; } catch(e){}\n"
               "  if (c && window.crypto && crypto.subtle && typeof DecompressionStream !== \"undefined\"){ try { await proOpen(c); } catch(e){} }\n"
               "  init(); })();\n</script>")
    path.write_text(html, encoding="utf-8")
    print(f"proef: {path.name} ({lang}) — gratis {sorted(vrij)}, Pro {sorted(pro)}")

code = re.sub(r"[^A-Z0-9]", "", sys.argv[1].upper())
gratis = int(sys.argv[2])
for f in sys.argv[3:]:
    maak(Path(f), code, gratis)
