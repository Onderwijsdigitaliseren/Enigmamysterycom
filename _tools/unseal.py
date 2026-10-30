#!/usr/bin/env python3
"""Opent verzegelde Pro-bestanden met de pascode. Gebruik: unseal.py CODE uitmap bestand..."""
import sys, re, json, base64, gzip
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from pathlib import Path
code = re.sub(r"[^A-Z0-9]", "", sys.argv[1].upper()); out = Path(sys.argv[2]); out.mkdir(exist_ok=True)
for f in sys.argv[3:]:
    s = Path(f).read_text(encoding="utf-8")
    P = json.loads(re.search(r'id="gfpro">(.*?)</script>', s, re.S).group(1))
    kek = PBKDF2HMAC(hashes.SHA256(), 32, base64.b64decode(P["salt"]), P["it"]).derive(code.encode())
    ck = None
    for w in P["keys"]:
        w = base64.b64decode(w)
        try: ck = AESGCM(kek).decrypt(w[:12], w[12:], None); break
        except Exception: pass
    if not ck: print("FOUT code past niet:", f); continue
    d = base64.b64decode(P["data"]); plat = AESGCM(ck).decrypt(d[:12], d[12:], None)
    if P.get("z"): plat = gzip.decompress(plat)
    (out / Path(f).name).write_bytes(plat); print("ok", f, len(plat))
