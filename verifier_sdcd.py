#!/usr/bin/env python
"""
Vérifie que `sdcd` remplace `dsfr` sans reste.

Quatre contrôles :
  1. les tags `sdcd_*` rendent, et aucun ne laisse fuiter une classe `fr-*` ;
  2. les tags `dsfr_*` rendent via le shim, sous leur nom d'origine ;
  3. toute classe `sdcd-*` émise par un gabarit existe dans les feuilles ;
  4. tous les gabarits du CMS qui chargent `dsfr_tags` se compilent.

Usage : .venv/Scripts/python.exe verifier_sdcd.py
"""

import io
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  # noqa: E402

django.setup()

from django.core.paginator import Paginator  # noqa: E402
from django.template import Context, Template, TemplateSyntaxError, engines  # noqa: E402
from django.template.loader import get_template  # noqa: E402

RACINE = os.path.dirname(os.path.abspath(__file__))
echecs = 0


def titre(t):
    print("\n%s\n%s" % (t, "-" * len(t)))


def cas(p):
    """Les mêmes appels, sous le préfixe `sdcd_` ou `dsfr_`."""
    return [
        ("%s_css" % p, "{%% %s_css %%}" % p, {}),
        ("%s_js" % p, "{%% %s_js nonce='n' %%}" % p, {}),
        ("%s_favicon" % p, "{%% %s_favicon %%}" % p, {}),
        ("%s_theme_modale" % p, "{%% %s_theme_modale %%}" % p, {}),
        ("%s_accordion" % p, "{%% %s_accordion id='a' title='T' content='<p>C</p>' %%}" % p, {}),
        ("%s_alert" % p, "{%% %s_alert title='A' type='warning' content='X' %%}" % p, {}),
        ("%s_breadcrumb" % p, "{%% %s_breadcrumb f %%}" % p, {"f": {"links": [], "current": "P"}}),
        ("%s_notice" % p, "{%% %s_notice title='N' %%}" % p, {}),
        ("%s_quote" % p, "{%% %s_quote text='Q' author='A' %%}" % p, {}),
        ("%s_skiplinks" % p, "{%% %s_skiplinks s %%}" % p, {"s": [{"link": "#c", "label": "L"}]}),
        ("%s_transcription" % p, "{%% %s_transcription title='T' content='<p>C</p>' %%}" % p, {}),
        ("%s_pagination" % p, "{%% %s_pagination pg %%}" % p,
         {"pg": Paginator(list(range(50)), 10).page(3), "request": None}),
        ("%s_badge" % p, "{%% %s_badge label='B' %%}" % p, {}),
        ("%s_badge_group" % p, "{%% %s_badge_group i %%}" % p, {"i": [{"label": "B"}]}),
        ("%s_button" % p, "{%% %s_button label='OK' type='secondaire' %%}" % p, {}),
        ("%s_button_group" % p, "{%% %s_button_group items=i %%}" % p, {"i": [{"label": "B"}]}),
        ("%s_card" % p, "{%% %s_card title='C' description='D' link='/x' %%}" % p, {}),
        ("%s_callout" % p, "{%% %s_callout title='C' text='T' %%}" % p, {}),
        ("%s_consent" % p, "{%% %s_consent title='C' content='X' %%}" % p, {}),
        ("%s_content" % p, "{%% %s_content image_url='/i.png' caption='C' %%}" % p, {}),
        ("%s_highlight" % p, "{%% %s_highlight content='H' %%}" % p, {}),
        ("%s_input" % p, "{%% %s_input id='i' label='L' %%}" % p, {}),
        ("%s_link" % p, "{%% %s_link url='/u' label='L' is_external=1 %%}" % p, {}),
        ("%s_select" % p, "{%% %s_select id='s' label='L' options=o %%}" % p,
         {"o": [{"value": "a", "text": "A"}]}),
        ("%s_sidemenu" % p, "{%% %s_sidemenu title='M' items=i %%}" % p,
         {"i": [{"link": "/a", "label": "A"}], "request": None}),
        ("%s_stepper" % p, "{%% %s_stepper current_step_id=1 current_step_title='E' total_steps=3 %%}" % p, {}),
        ("%s_summary" % p, "{%% %s_summary i %%}" % p, {"i": [{"link": "#a", "label": "A"}]}),
        ("%s_table" % p, "{%% %s_table caption='T' header=h content=c %%}" % p,
         {"h": ["A", "B"], "c": [["1", "2"]]}),
        ("%s_tag" % p, "{%% %s_tag label='E' %%}" % p, {}),
        ("%s_tile" % p, "{%% %s_tile title='T' url='/t' description='D' %%}" % p, {}),
        ("%s_toggle" % p, "{%% %s_toggle label='I' id='i1' %%}" % p, {}),
        ("%s_tooltip" % p, "{%% %s_tooltip label='L' content='C' %%}" % p, {}),
        ("%s_accordion_group" % p, "{%% %s_accordion_group i %%}" % p,
         {"i": [{"title": "T", "content": "C"}]}),
        ("%s_django_messages" % p, "{%% %s_django_messages %%}" % p, {"messages": []}),
    ]


def rendre(bibliotheque, jeu):
    global echecs
    fuites = 0
    for nom, src, ctx in jeu:
        try:
            html = Template("{%% load %s %%}" % bibliotheque + src).render(Context(ctx))
            # Ne chercher `fr-` que dans un attribut class : le nom de fichier
            # `compat-dsfr.css` en contient un, sans que ce soit une classe.
            classes = " ".join(re.findall(r'class="([^"]*)"', html)).split()
            if any(c.startswith("fr-") for c in classes):
                fuites += 1
                echecs += 1
                print("  FUITE fr-*  %s" % nom)
        except Exception as e:
            echecs += 1
            print("  ECHEC  %-26s %s: %s" % (nom, type(e).__name__, str(e)[:80]))
    print("  %d/%d rendus, %d fuite(s) de classe fr-*" % (len(jeu) - fuites, len(jeu), fuites))


titre("1. Tags sdcd_*")
rendre("sdcd_tags", cas("sdcd"))

titre("2. Tags dsfr_* via le shim (django-dsfr desinstalle)")
rendre("dsfr_tags", cas("dsfr"))
try:
    Template("{% load dsfr_tags %}{% dsfr_france_connect %}").render(Context({}))
    from dsfr.constants import NOTICE_TYPE_CHOICES  # noqa: F401
    from dsfr.forms import DsfrBaseForm  # noqa: F401
    from dsfr.utils import dsfr_input_class_attr  # noqa: F401
    print("  alias france_connect + imports dsfr.constants/forms/utils : OK")
except Exception as e:
    echecs += 1
    print("  ECHEC alias/imports : %s" % e)


titre("3. Classes sdcd-* emises par les gabarits")
emises = set()
for racine, _, fichiers in os.walk(os.path.join(RACINE, "sdcd", "templates")):
    for f in fichiers:
        if not f.endswith(".html"):
            continue
        s = io.open(os.path.join(racine, f), encoding="utf-8").read()
        for m in re.finditer(r'class="([^"]*)"', s):
            for c in m.group(1).split():
                if c.startswith("sdcd-") and "{" not in c:
                    emises.add(c)
definies = set()
for f in ("components.css", "base.css", "utilitaires.css", "responsive.css"):
    chemin = os.path.join(RACINE, "sdcd", "static", "sdcd", f)
    definies.update(re.findall(r"\.(sdcd-[a-zA-Z0-9_-]+)", io.open(chemin, encoding="utf-8").read()))
manquantes = sorted(emises - definies)
print("  emises : %d   manquantes : %d" % (len(emises), len(manquantes)))
for c in manquantes:
    print("    MANQUANTE %s" % c)
echecs += len(manquantes)


titre("4. Compilation des gabarits du CMS")
fichiers = subprocess.run(["git", "ls-files", "*.html"], capture_output=True, text=True).stdout.split()
cibles = [f for f in fichiers
          if "dsfr_tags" in io.open(f, encoding="utf-8", errors="ignore").read()]
casses = []
for f in cibles:
    i = f.find("/templates/")
    nom = f[i + len("/templates/"):] if i >= 0 else f
    try:
        get_template(nom)
    except TemplateSyntaxError as e:
        casses.append((nom, str(e)[:90]))
    except Exception:
        try:
            engines["django"].from_string(io.open(f, encoding="utf-8").read())
        except Exception as e2:
            casses.append((nom, str(e2)[:90]))
print("  %d/%d gabarits compiles" % (len(cibles) - len(casses), len(cibles)))
for n, m in casses:
    print("    CASSE %s : %s" % (n, m))
echecs += len(casses)




titre("5. References url() des feuilles de style")
# WhiteNoise resout chaque url() au moment de collectstatic et leve MissingFileError
# sur une reference morte : le conteneur refuse alors de demarrer, en boucle. Un seul
# fichier DSFR oublie dans un url() a suffi a faire echouer le premier deploiement.
# Ce controle attrape la classe entiere du probleme, pas ce cas precis.
import re as _re
from pathlib import Path as _Path

_racine = _Path("sites_conformes/static")
_motif = _re.compile(r"""url\(\s*["']?(?!data:|https?:|//|\#)([^"')]+)["']?\s*\)""")
_morts = []
_vus = 0
for _css in sorted(_racine.rglob("*.css")):
    _txt = _css.read_text(encoding="utf-8", errors="replace")
    for _m in _motif.finditer(_txt):
        _ref = _m.group(1).split("?")[0].split("#")[0].strip()
        if not _ref:
            continue
        _vus += 1
        if not (_css.parent / _ref).resolve().exists():
            _morts.append((str(_css).replace("\\", "/"), _ref))
print("  %d reference(s) examinee(s), %d morte(s)" % (_vus, len(_morts)))
for _f, _r in _morts:
    print("    MORTE %s -> %s" % (_f, _r))
echecs += len(_morts)



titre("6. Appels {% static %} des gabarits")
# Meme mecanisme que le controle 5, mais au rendu : ManifestStaticFilesStorage leve
# ValueError quand static() vise un fichier absent. Une seule reference morte dans un
# gabarit de base suffit a renvoyer 500 sur tout le site — c'est exactement ce qui est
# arrive avec sdcd/favicon/favicon.svg. On interroge les finders de Django plutot que
# de parcourir les repertoires a la main : ce sont eux que static() consulte, donc le
# controle voit ce que voit la production, sans faux positif sur les statiques
# fournis par les applications installees.
from django.contrib.staticfiles import finders as _finders
import re as _re2

_motif2 = _re2.compile(r"""\{%\s*static\s+["']([^"']+)["']""")
_fichiers2 = subprocess.run(
    ["git", "ls-files", "*.html"], capture_output=True, text=True
).stdout.split()
_morts2 = []
_vus2 = 0
for _f2 in _fichiers2:
    _txt2 = io.open(_f2, encoding="utf-8", errors="replace").read()
    for _m2 in _motif2.finditer(_txt2):
        _ref2 = _m2.group(1)
        _vus2 += 1
        if not _finders.find(_ref2):
            _morts2.append((_f2, _ref2))
print("  %d appel(s) examines, %d introuvable(s)" % (_vus2, len(_morts2)))
for _f2, _r2 in _morts2:
    print("    INTROUVABLE %s -> %s" % (_f2, _r2))
echecs += len(_morts2)



titre("7. Commentaires Django multilignes")
# {# ... #} ne vaut que sur UNE ligne. Des qu'il en couvre plusieurs, Django cesse de
# le reconnaitre et le rend tel quel : le texte du commentaire s'affiche aux visiteurs.
# Cinq commentaires ecrits pendant le portage etaient dans ce cas, visibles en haut de
# chaque page du site en production. La forme multiligne valide est {% comment %}.
_multi = []
for _f3 in subprocess.run(
    ["git", "ls-files", "*.html"], capture_output=True, text=True
).stdout.split():
    for _i3, _l3 in enumerate(
        io.open(_f3, encoding="utf-8", errors="replace").read().split("\n"), 1
    ):
        if "{#" in _l3 and "#}" not in _l3[_l3.index("{#"):]:
            _multi.append((_f3, _i3))
print("  %d commentaire(s) multiligne(s)" % len(_multi))
for _f3, _i3 in _multi:
    print("    RENDU LITTERAL %s:%d" % (_f3, _i3))
echecs += len(_multi)

print("\n%s" % ("Aucun defaut." if echecs == 0 else "%d defaut(s)." % echecs))
raise SystemExit(1 if echecs else 0)
