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


# Repertoires que `git ls-files` ecartait d'office et que le parcours de secours
# doit ecarter aussi : dependances, sorties de collecte, caches.
_IGNORES = {
    ".git", "node_modules", "staticfiles", "medias", "__pycache__",
    ".venv", "venv", ".tox", ".mypy_cache", ".ruff_cache", "dist", "build",
}


def fichiers_suivis(*suffixes):
    """Recense les fichiers du projet, en refusant une liste vide.

    Les controles 3, 4, 6, 7, 8 et 9 partaient de `git ls-files`. Hors d'une
    copie de travail — dans un conteneur ou l'arborescence est montee sans son
    .git, ou simplement sur une machine sans git — la commande ne renvoie rien :
    les controles annonçaient alors « 0 examine, 0 defaut » et le script sortait
    vert. Un controle qui n'examine rien doit echouer, pas rassurer.

    D'ou les deux niveaux : git quand il repond, parcours du disque sinon, et
    dans tous les cas un arret si le recensement est vide.
    """
    motifs = ["*" + s for s in suffixes]
    try:
        sortie = subprocess.run(
            ["git", "ls-files"] + motifs, capture_output=True, text=True, cwd=RACINE
        )
        fichiers = sortie.stdout.split()
    except OSError:
        fichiers = []

    if not fichiers:
        fichiers = []
        for dossier, sous, noms in os.walk(RACINE):
            sous[:] = [d for d in sous if d not in _IGNORES]
            for nom in noms:
                if nom.endswith(suffixes):
                    fichiers.append(
                        os.path.relpath(os.path.join(dossier, nom), RACINE).replace("\\", "/")
                    )

    if not fichiers:
        raise SystemExit(
            "  ARRET  aucun fichier %s recense, ni par git ni par parcours du "
            "disque. Les controles suivants n'auraient rien examine et le script "
            "serait sorti vert." % ", ".join(suffixes)
        )
    return sorted(fichiers)


GABARITS = fichiers_suivis(".html")


titre("3. Classes sdcd-* emises par les gabarits")
# Tous les gabarits suivis, pas seulement sdcd/templates/. L'en-tete vit dans
# dsfr/templates/ — le shim d'alias — et echappait donc entierement a ce controle :
# sept classes sdcd-header__* inventees y sont restees jusqu'a ce que l'en-tete
# s'affiche sans mise en page en production.
emises = set()
_ou = {}
for _f in GABARITS:
    s = io.open(_f, encoding="utf-8", errors="replace").read()
    for m in re.finditer(r'class="([^"]*)"', s):
        for c in m.group(1).split():
            if c.startswith("sdcd-") and "{" not in c:
                emises.add(c)
                _ou.setdefault(c, _f)
definies = set()
for f in ("components.css", "base.css", "utilitaires.css", "responsive.css"):
    chemin = os.path.join(RACINE, "sdcd", "static", "sdcd", f)
    definies.update(re.findall(r"\.(sdcd-[a-zA-Z0-9_-]+)", io.open(chemin, encoding="utf-8").read()))
manquantes = sorted(emises - definies)
print("  emises : %d   manquantes : %d" % (len(emises), len(manquantes)))
for c in manquantes:
    print("    MANQUANTE %s  (%s)" % (c, _ou.get(c, "?")))
echecs += len(manquantes)


titre("4. Compilation des gabarits du CMS")
fichiers = GABARITS
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
_fichiers2 = GABARITS
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
for _f3 in GABARITS:
    for _i3, _l3 in enumerate(
        io.open(_f3, encoding="utf-8", errors="replace").read().split("\n"), 1
    ):
        if "{#" in _l3 and "#}" not in _l3[_l3.index("{#"):]:
            _multi.append((_f3, _i3))
print("  %d commentaire(s) multiligne(s)" % len(_multi))
for _f3, _i3 in _multi:
    print("    RENDU LITTERAL %s:%d" % (_f3, _i3))
echecs += len(_multi)



titre("8. Aucune classe DSFR ne doit subsister")
# La couche de compatibilite a ete retiree : plus aucune classe `fr-*` ne
# trouverait de regle. Ce controle ne mesure donc plus une couverture, il
# interdit purement et simplement l'emission d'une classe DSFR.
#
# Il lit deux sources : l'attribut `class` litteral, et le filtre `add_class` de
# django-widget-tweaks. Ce second cas lui avait echappe une fois, et deux classes
# etaient restees sans regle jusqu'a ce que la page de connexion s'affiche de
# travers.
_emises = {}
for _f4 in GABARITS:
    if _f4.startswith("demo/"):
        continue
    _txt4 = io.open(_f4, encoding="utf-8", errors="replace").read()
    for _m4 in re.finditer(r'class="([^"]*)"|add_class:"([^"]+)"', _txt4):
        for _c4 in (_m4.group(1) or _m4.group(2) or "").split():
            # `cmsfr-*` est un prefixe propre au CMS, pas du DSFR.
            if _c4.startswith("fr-") and "{" not in _c4 and "}" not in _c4:
                _emises.setdefault(_c4, _f4)
print("  %d classe(s) DSFR emise(s)" % len(_emises))
for _c4, _f4 in sorted(_emises.items()):
    print("    DSFR RESIDUELLE %s  (%s)" % (_c4, _f4))
echecs += len(_emises)

titre("9. Aucun jeton fr-* hors des commentaires")
# Le controle 8 ne lit que les attributs `class` et `add_class`. C'est la ou vivent
# les classes, mais pas les selecteurs CSS, les identifiants, les attributs
# `data-fr-*` ni les chaines de selecteurs des tests. Le portage a donc laisse
# passer, sans que rien ne le signale :
#   - 233 lignes de feuille visant `.fr-usermenu`, que plus aucun gabarit
#     n'emettait : le menu de compte s'affichait sans habillage ;
#   - les identifiants `fr-sidemenu-wrapper-` et `fr-sidemenu-title` ;
#   - les crochets `data-fr-js-collapse-button` et `data-fr-current-step`, inertes
#     depuis le retrait du JavaScript du DSFR : le bouton « Fermer » d'un
#     mega-menu ne fermait rien, la jauge d'un indicateur d'etape restait vide ;
#   - les selecteurs `.fr-card__title` des tests du blog, qui ne trouvaient plus
#     aucune carte et faisaient echouer treize tests.
#
# Les commentaires sont retires avant l'examen : ce fichier et plusieurs gabarits
# expliquent legitimement ce qui a ete remplace, en le nommant.
# Les fixes JSON comptent : `sites_conformes/core/page_templates/pages_data.json`
# est reimporte a chaque deploiement par `just deploy`. Il a garde 47 jetons
# `fr-*` et sept couleurs du DSFR bien apres le portage — la migration nettoyait
# la base, l'import la repeuplait aussitot avec les anciennes valeurs.
_SUIVIS9 = [
    _f for _f in fichiers_suivis(".html", ".css", ".js", ".py", ".json")
    if not _f.startswith("demo/")
    # La table de correspondance du portage cite les deux vocabulaires : c'est son role.
    and not _f.startswith("sdcd/portage/")
    and "/migrations/" not in _f
    and "node_modules/" not in _f
    and not _f.endswith(("package-lock.json", "/package.json"))
    and _f != "verifier_sdcd.py"
]

# Noms de couleur du DSFR. Ils ne commencent pas par `fr-` et echappaient donc au
# motif ci-dessous, alors qu'ils sont interpoles dans `var(--sdcd-fond-<valeur>)`
# et `sdcd-badge--<valeur>` : une valeur restee en anglais ne designe aucun jeton
# ni aucune variante, et la couleur choisie par le redacteur ne s'affiche pas.
_COULEURS_DSFR = re.compile(
    r'"(blue-france|blue-ecume|blue-cumulus|red-marianne|purple-glycine|'
    r'pink-macaron|pink-tuile|yellow-tournesol|yellow-moutarde|orange-terre-battue|'
    r'brown-cafe-creme|brown-caramel|brown-opera|beige-gris-galet|'
    r'green-tilleul-verveine|green-bourgeon|green-emeraude|green-menthe|green-archipel)"'
)

_BLOC_COMMENTAIRE = re.compile(r"/\*.*?\*/", re.S)
_LIGNE_SLASH = re.compile(r"^\s*//.*$", re.M)
_COMMENT_DJANGO = re.compile(r"\{%\s*comment\s*%\}.*?\{%\s*endcomment\s*%\}", re.S)
_COMMENT_COURT = re.compile(r"\{#.*?#\}", re.S)
_COMMENT_HTML = re.compile(r"<!--.*?-->", re.S)
_DOCSTRING_D = re.compile(r'"""[\s\S]*?"""')
_DOCSTRING_S = re.compile(r"'''[\s\S]*?'''")
_DIESE = re.compile(r"^\s*#.*$", re.M)
_JETON_FR = re.compile(r"\bfr-[a-z0-9_-]+")


def _sans_commentaires(texte, suffixe):
    if suffixe in (".css", ".js"):
        return _LIGNE_SLASH.sub(" ", _BLOC_COMMENTAIRE.sub(" ", texte))
    if suffixe == ".html":
        texte = _COMMENT_DJANGO.sub(" ", texte)
        texte = _COMMENT_COURT.sub(" ", texte)
        return _COMMENT_HTML.sub(" ", texte)
    if suffixe == ".py":
        # Les docstrings d'abord : un `#` a l'interieur fausserait le decoupage.
        texte = _DOCSTRING_D.sub(" ", texte)
        texte = _DOCSTRING_S.sub(" ", texte)
        return _DIESE.sub(" ", texte)
    return texte


_restes9 = []
for _f9 in _SUIVIS9:
    _suf9 = os.path.splitext(_f9)[1]
    _txt9 = _sans_commentaires(
        io.open(_f9, encoding="utf-8", errors="replace").read(), _suf9)
    for _m9 in sorted(set(_JETON_FR.findall(_txt9))):
        _restes9.append((_f9, _m9))
    for _m9 in sorted(set(_COULEURS_DSFR.findall(_txt9))):
        _restes9.append((_f9, _m9))
print("  %d fichier(s) examines, %d residu(s) du vocabulaire DSFR"
      % (len(_SUIVIS9), len(_restes9)))
for _f9, _m9 in _restes9:
    print("    RESIDU %-32s %s" % (_m9, _f9))
echecs += len(_restes9)


titre("10. Variantes construites par interpolation")
# Le controle 3 ne voit que les classes ecrites en toutes lettres. Or plusieurs
# gabarits composent la leur : `class="sdcd-tag sdcd-tag--{{ value.color }}"`.
# La valeur vient d'un `ChoiceBlock`, donc l'ensemble des classes possibles est
# connu — mais aucun controle ne les rapprochait, et le champ « couleur de
# l'etiquette » a longtemps propose six teintes dont AUCUNE n'etait definie : le
# choix du redacteur restait sans effet. Meme cause pour le badge « Gris ».
#
# On resout ici les deux bouts : les choix declares par le bloc, et le gabarit
# que son Meta designe.
from wagtail import blocks as _wblocks  # noqa: E402

_DYNAMIQUE = re.compile(r"(sdcd-[a-z0-9-]+--)\{\{\s*([a-z_.]+)\s*\}\}")

_definies10 = set()
for _f10 in ("components.css", "base.css", "utilitaires.css", "responsive.css"):
    _definies10.update(
        re.findall(
            r"\.(sdcd-[a-zA-Z0-9_-]+)",
            io.open(os.path.join(RACINE, "sdcd", "static", "sdcd", _f10), encoding="utf-8").read(),
        )
    )


def _blocs_structures():
    """Tous les StructBlock du CMS, quel que soit le module qui les declare."""
    import importlib
    import pkgutil

    vus = {}
    for paquet in ("sites_conformes.core.blocks", "sites_conformes.menus.blocks"):
        try:
            mod = importlib.import_module(paquet)
        except ImportError:
            continue
        modules = [mod]
        if hasattr(mod, "__path__"):
            for info in pkgutil.iter_modules(mod.__path__):
                try:
                    modules.append(importlib.import_module("%s.%s" % (paquet, info.name)))
                except ImportError:
                    continue
        for m in modules:
            for nom in dir(m):
                objet = getattr(m, nom)
                if (
                    isinstance(objet, type)
                    and issubclass(objet, _wblocks.StructBlock)
                    and objet is not _wblocks.StructBlock
                ):
                    vus[objet] = nom
    return vus


_manquantes10 = []
_examinees10 = 0
for _bloc10, _nom10 in _blocs_structures().items():
    _gabarit10 = getattr(getattr(_bloc10, "_meta_class", None), "template", None)
    if not _gabarit10:
        continue
    try:
        _src10 = io.open(get_template(_gabarit10).origin.name, encoding="utf-8").read()
    except Exception:
        continue

    for _prefixe10, _var10 in _DYNAMIQUE.findall(_src10):
        _champ10 = _var10.rsplit(".", 1)[-1]
        _declare10 = _bloc10.declared_blocks.get(_champ10)
        if not isinstance(_declare10, _wblocks.ChoiceBlock):
            continue
        _valeurs10 = []
        for _cle10, _lib10 in _declare10.field.choices:
            # Les choix peuvent etre groupes : (« Couleurs systeme », [(...), ...]).
            if isinstance(_lib10, (list, tuple)):
                _valeurs10.extend(v for v, _ in _lib10)
            elif _cle10:
                _valeurs10.append(_cle10)
        for _v10 in _valeurs10:
            _examinees10 += 1
            if _prefixe10 + _v10 not in _definies10:
                _manquantes10.append((_prefixe10 + _v10, _nom10, _gabarit10))

print("  %d combinaison(s) examinees, %d sans regle" % (_examinees10, len(_manquantes10)))
for _c10, _n10, _g10 in _manquantes10:
    print("    SANS REGLE %-30s %s (%s)" % (_c10, _n10, _g10))
echecs += len(_manquantes10)


print("\n%s" % ("Aucun defaut." if echecs == 0 else "%d defaut(s)." % echecs))
raise SystemExit(1 if echecs else 0)
