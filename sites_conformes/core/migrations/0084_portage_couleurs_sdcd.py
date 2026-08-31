"""Reecrit les couleurs stockees en base vers le vocabulaire du SDCD.

Le portage des classes (0081) ne pouvait pas voir celles-ci : ce ne sont pas des
classes CSS mais des noms de couleur — « blue-france », « green-emeraude »,
« new » — poses comme valeur de champ par le redacteur, puis interpoles par le
gabarit dans `var(--background-alt-<valeur>)` ou dans `sdcd-badge--<valeur>`.

Trois vocabulaires se succedent dans les donnees d'une instance ancienne :

  1. celui du DSFR, d'origine (« blue-france », « red-marianne », « grey ») ;
  2. celui de la premiere passe du portage, qui nommait des couleurs pleines
     (« bleu-action », « fond-alt », « ligne ») — jamais lisibles sous du texte,
     et sans jeton `--background-alt-*` correspondant ;
  3. celui d'aujourd'hui, aligne sur les jetons `--sdcd-fond-*`.

La correspondance couvre les deux premiers. Une valeur inconnue est laissee
telle quelle : mieux vaut une couleur non portee, visible a la relecture, qu'un
contenu abime par une traduction approximative.

La palette du SDCD est plus courte que celle du DSFR — elle ne propose pas dix-neuf
teintes decoratives. Plusieurs couleurs convergent donc vers la meme, et la marche
arriere ne peut pas les distinguer : elle n'est pas fournie.
"""

import json

from django.db import migrations

# Fonds de section et de bloc.
FONDS = {
    # --- vocabulaire du DSFR ------------------------------------------------
    "blue-france": "bleu",
    "blue-ecume": "bleu",
    "blue-cumulus": "bleu",
    "grey": "gris",
    "beige-gris-galet": "gris",
    "green-tilleul-verveine": "chart-4",
    "green-bourgeon": "chart-4",
    "green-emeraude": "chart-4",
    "green-menthe": "chart-4",
    "green-archipel": "chart-4",
    "red-marianne": "chart-5",
    "pink-macaron": "chart-5",
    "pink-tuile": "chart-5",
    "yellow-tournesol": "chart-3",
    "yellow-moutarde": "chart-3",
    "orange-terre-battue": "chart-3",
    "brown-cafe-creme": "chart-3",
    "brown-caramel": "chart-3",
    "brown-opera": "chart-3",
    # Le SDCD ne propose pas de violet : la teinte la plus proche est le bleu profond.
    "purple-glycine": "chart-2",
    "success": "succes",
    "warning": "alerte",
    "error": "erreur",
    # --- vocabulaire de la premiere passe du portage ------------------------
    "bleu-action": "bleu",
    "bleu-aplat": "bleu-soutenu",
    "fond-alt": "gris",
    "ligne": "gris-soutenu",
}

# Variantes de badge : le gabarit rend `sdcd-badge--<valeur>`.
BADGES = dict(FONDS)
BADGES.update({"new": "nouveau", "grey": "gris"})

# Champs a reecrire, par nom. Les cles des blocs de flux sont les memes que les
# noms de champ des modeles, ce qui permet un seul parcours.
CHAMPS_FOND = {"header_color_class", "bg_color_class", "background_color"}
CHAMPS_BADGE = {"color"}


def parcourir(noeud, compteur):
    """Reecrit en profondeur, en place, toute valeur de couleur rencontree."""
    if isinstance(noeud, dict):
        neuf = {}
        for cle, valeur in noeud.items():
            if isinstance(valeur, str):
                if cle in CHAMPS_FOND and valeur in FONDS:
                    neuf[cle] = FONDS[valeur]
                    compteur[0] += 1
                    continue
                if cle in CHAMPS_BADGE and valeur in BADGES:
                    neuf[cle] = BADGES[valeur]
                    compteur[0] += 1
                    continue
            neuf[cle] = parcourir(valeur, compteur)
        return neuf
    if isinstance(noeud, list):
        return [parcourir(v, compteur) for v in noeud]
    return noeud


MODELES = (
    ("sites_conformes_core", "ContentPage"),
    ("sites_conformes_core", "CatalogIndexPage"),
    ("sites_conformes_blog", "BlogEntryPage"),
    ("sites_conformes_blog", "BlogIndexPage"),
    ("sites_conformes_events", "EventEntryPage"),
    ("sites_conformes_events", "EventsIndexPage"),
)


def porter(apps, schema_editor):
    compteur = [0]
    pages = 0
    for etiquette, modele in MODELES:
        try:
            Modele = apps.get_model(etiquette, modele)
        except LookupError:
            continue
        for objet in Modele.objects.all().iterator():
            change = False
            for champ in objet._meta.get_fields():
                nom = getattr(champ, "attname", None)
                if not nom:
                    continue
                valeur = getattr(objet, nom, None)
                if not isinstance(valeur, str) or not valeur:
                    continue

                # Champ simple : `header_color_class` est une colonne texte, pas
                # du JSON. Il echappait donc au parcours de 0081.
                if nom in CHAMPS_FOND and valeur in FONDS:
                    setattr(objet, nom, FONDS[valeur])
                    compteur[0] += 1
                    change = True
                    continue

                try:
                    donnees = json.loads(valeur)
                except (ValueError, TypeError):
                    continue  # champ texte ordinaire, pas un StreamField
                neuf = json.dumps(parcourir(donnees, compteur), ensure_ascii=False)
                if neuf != valeur:
                    setattr(objet, nom, neuf)
                    change = True
            if change:
                objet.save()
                pages += 1
    if compteur[0]:
        print("  %d couleur(s) portee(s) sur %d page(s)" % (compteur[0], pages))


class Migration(migrations.Migration):
    dependencies = [
        ("sites_conformes_core", "0083_alter_catalogindexpage_body_and_more"),
        ("sites_conformes_blog", "0064_alter_blogentrypage_body_and_more"),
        ("sites_conformes_events", "0036_alter_evententrypage_body_and_more"),
    ]
    operations = [migrations.RunPython(porter, migrations.RunPython.noop)]
