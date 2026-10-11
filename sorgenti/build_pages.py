# -*- coding: utf-8 -*-
import json, base64, secrets, string, os, sys
from quizzes import GROUPS

REPO = "/home/claude/gottardo-quiz"
OUT = "/home/claude/build/out"
BASE = "https://nuovipercorsi123-sys.github.io/gottardo-quiz/"
os.makedirs(OUT, exist_ok=True)
MAP = os.path.join(OUT, "mappa.json")

mapping = json.load(open(MAP)) if os.path.exists(MAP) else {}
alpha = string.ascii_lowercase + string.digits

def slug_for(key):
    if key not in mapping:
        while True:
            s = "q" + "".join(secrets.choice(alpha) for _ in range(7))
            if s not in mapping.values():
                mapping[key] = s; break
    return mapping[key]

def enc(obj, key):
    raw = json.dumps(obj, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    kb = key.encode()
    return base64.b64encode(bytes(b ^ kb[i % len(kb)] for i, b in enumerate(raw))).decode()

tpl = open("/home/claude/build/template.html", encoding="utf-8").read()
for f in os.listdir(REPO):
    if f.startswith("q") and f.endswith(".html") and len(f) == 13:
        os.remove(os.path.join(REPO, f))

rows = []
for g in GROUPS:
    for d in g["domande"]:
        key = f'{g["id"]}-{d["letter"]}'
        slug = slug_for(key)
        payload = {
            "group": g["name"], "pages": g["pages"], "letter": d["letter"], "short": d["short"],
            "sheet": d["sheet"], "pos": d["pos"], "word": g["phrase"][d["pos"] - 1],
            "qs": [{"q": q["q"], "o": q["o"], "p": q["p"], "k": q["k"]} for q in d["qs"]],
        }
        html = (tpl.replace("__ACCENT__", g["color"]).replace("__KEY__", slug)
                   .replace("__DATA__", enc(payload, slug)))
        open(os.path.join(REPO, slug + ".html"), "w", encoding="utf-8").write(html)
        rows.append((key, slug))

index = """<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow"><title>Attività Gottardo</title><style>body{font:18px/1.5 system-ui,sans-serif;max-width:560px;margin:6vh auto;padding:0 16px;color:#1d1b18}</style></head><body><img src="locandina2.jpg" alt="Locandina del film Gotthard" style="display:block;width:100%;max-width:300px;height:auto;border-radius:12px;margin:0 auto"><img src="libro3d.jpg" alt="Copertina del libro La Ferrovia del Gottardo" style="display:block;width:140px;max-width:45%;margin:14px auto"><h1>Attività Gottardo</h1><p>Per iniziare, scansiona il codice QR del tuo foglio.</p></body></html>"""
open(os.path.join(REPO, "index.html"), "w", encoding="utf-8").write(index)
open(os.path.join(REPO, "README.md"), "w", encoding="utf-8").write("# Gottardo-quiz\n\nPagine dell'attività «Dal film al libro: la Ferrovia del Gottardo».\n")
json.dump(mapping, open(MAP, "w"), indent=1)
print(len(rows), "pagine"); print(rows[:3])
