"""Porte reellement les classes et les couleurs stockees en base.

Les migrations 0081 et 0084 devaient faire ce travail. Elles n'ont rien fait, et
se sont appliquees sans erreur, ce qui est pire qu'un echec : elles ont laisse
croire que les donnees etaient portees.

La cause est la meme dans les deux : elles lisaient le champ ainsi

    valeur = getattr(objet, champ.attname)
    if not isinstance(valeur, str) or "fr-" not in valeur:
        continue

Or `page.body` n'est pas une chaine — c'est un `StreamValue`. La condition etait
donc toujours fausse, et la boucle passait au champ suivant sans jamais entrer
dans la traduction. Mesure faite apres coup sur l'instance en service : sept
pages portaient encore des classes `fr-*` et six la couleur `blue-france`.

Ici, le contenu brut est lu par `valeur.raw_data`, traduit, puis reecrit sous la
forme d'une chaine JSON — que le descripteur du champ sait reinterpreter. Le
mecanisme a ete verifie sur la base en service, dans une transaction annulee :
six pages reecrites pendant, base identique apres.

Les tables de correspondance sont recopiees plutot qu'importees : une migration
doit rester lisible et rejouable dans dix ans, meme si le module a bouge.
"""

import json

from django.db import migrations

# --- classes CSS ------------------------------------------------------------
JETONS = {
    "fr-btn--secondary": "sdcd-button--secondaire",
    "fr-btn--tertiary": "sdcd-button--tertiaire-bordure",
    "fr-btn--tertiary-no-outline": "sdcd-button--tertiaire",
    "fr-btn--icon-left": "sdcd-button--icone-gauche",
    "fr-btn--icon-right": "sdcd-button--icone-droite",
    "fr-btns-group": "sdcd-boutons",
    "fr-btns-group--inline-lg": "sdcd-boutons--enligne-lg",
    "fr-btns-group--center": "sdcd-boutons--centre",
    "fr-btns-group--right": "sdcd-boutons--droite",
    "fr-btns-group--inline-reverse": "sdcd-boutons--enligne-inverse",
    "fr-card": "sdcd-card",
    "fr-card--horizontal": "sdcd-card--horizontal",
    "fr-card--horizontal-half": "sdcd-card--horizontal-moitie",
    "fr-card--horizontal-tier": "sdcd-card--horizontal-tiers",
    "fr-card__desc": "sdcd-card__description",
    "fr-card__title": "sdcd-card__titre",
    "fr-enlarge-link": "sdcd-cliquable",
    "fr-col": "sdcd-col",
    "fr-col-12": "sdcd-col-12",
    "fr-col-lg-3": "sdcd-col-lg-3",
    "fr-col-offset-md-2": "sdcd-col-decale-md-2",
    "fr-col-offset-md-3": "sdcd-col-decale-md-3",
    "fr-col-offset-md-4": "sdcd-col-decale-md-4",
    "fr-col-offset-md-6": "sdcd-col-decale-md-6",
    "fr-content-media--sm": "sdcd-media--sm",
    "fr-content-media--lg": "sdcd-media--lg",
    "fr-ratio-16x9": "sdcd-ratio-16x9",
    "fr-ratio-32x9": "sdcd-ratio-32x9",
    "fr-ratio-3x2": "sdcd-ratio-3x2",
    "fr-ratio-4x3": "sdcd-ratio-4x3",
    "fr-ratio-1x1": "sdcd-ratio-1x1",
    "fr-ratio-3x4": "sdcd-ratio-3x4",
    "fr-ratio-2x3": "sdcd-ratio-2x3",
    "fr-responsive-img": "sdcd-image-fluide",
    "fr-collapse": "sdcd-repli",
    "fr-menu": "sdcd-dropdown__menu",
    "fr-menu__list": "sdcd-dropdown__liste",
    "fr-nav__btn": "sdcd-header__lien",
    "fr-nav__item": "sdcd-nav__item",
    "fr-nav__link": "sdcd-header__lien",
    "fr-mega-menu__category": "sdcd-megamenu__categorie",
    "fr-mega-menu__leader": "sdcd-megamenu__intro",
    "fr-translate": "sdcd-langmenu",
    "fr-translate__language": "sdcd-dropdown__item",
    "fr-header__service": "sdcd-header__entite-bloc",
    "fr-header__service-title": "sdcd-header__service",
    "fr-header__service-tagline": "sdcd-header__service-accroche",
    "fr-footer__bottom-link": "sdcd-footer__lien",
    "fr-footer__content-link": "sdcd-footer__lien",
    "fr-footer__brand": "sdcd-footer__marque",
    "fr-logo": "sdcd-logo",
    "fr-link": "sdcd-lien",
    "fr-link--sm": "sdcd-lien--sm",
    "fr-link--lg": "sdcd-lien--lg",
    "fr-link--icon-left": "sdcd-lien--icone-gauche",
    "fr-link--icon-right": "sdcd-lien--icone-droite",
    "fr-link--close": "sdcd-lien--fermer",
    "fr-link--align-on-content": "sdcd-lien--aligne",
    "fr-links-group": "sdcd-liens",
    "fr-tag": "sdcd-tag",
    "fr-tag--sm": "sdcd-tag--sm",
    "fr-tag--icon-left": "sdcd-tag--icone-gauche",
    "fr-tags-group": "sdcd-tags",
    "fr-badge": "sdcd-badge",
    "fr-badge--sm": "sdcd-badge--sm",
    "fr-badge--green-emeraude": "sdcd-badge--succes",
    "fr-tile__header": "sdcd-tile__media",
    "fr-tile__pictogram": "sdcd-tile__media",
    "fr-notice__body": "sdcd-notice__corps",
    "fr-error-text": "sdcd-champ__erreur",
    "fr-sr-only": "sdcd-lecteur-seul",
    "fr-h4": "sdcd-h4",
    "fr-mb-2v": "sdcd-mb-2",
    "fr-p-2w": "sdcd-p-4",
    "fr-background-alt--grey": "sdcd-fond-alt",
    "fr-text--sm": "sdcd-texte-sm",
    "fr-text--lg": "sdcd-texte-lg",
    "fr-text--lead": "sdcd-texte-lead",
    "fr-hidden": "sdcd-masque",
    "fr-hidden-lg": "sdcd-masque-lg",
    "fr-displayed-lg": "sdcd-affiche-lg",
}
VARIANTES_BOUTON = {
    "fr-btn--secondary",
    "fr-btn--tertiary",
    "fr-btn--tertiary-no-outline",
}
# Teinte decorative du DSFR sans equivalent : le SDCD ne propose pas de palette
# purement decorative, ses couleurs portent un sens.
CLASSES_RETIREES = {"fr-tag--purple-glycine"}

# --- couleurs ---------------------------------------------------------------
# Trois vocabulaires se succedent dans les donnees : celui du DSFR, celui de la
# premiere passe du portage, et celui d'aujourd'hui, aligne sur les jetons
# `--sdcd-fond-*`. Les deux premiers sont traduits vers le troisieme.
FONDS = {
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
    # Le SDCD ne propose pas de violet : le plus proche est le bleu profond.
    "purple-glycine": "chart-2",
    "success": "succes",
    "warning": "alerte",
    "error": "erreur",
    "bleu-action": "bleu",
    "bleu-aplat": "bleu-soutenu",
    "fond-alt": "gris",
    "ligne": "gris-soutenu",
}
BADGES = dict(FONDS)
BADGES.update({"new": "nouveau", "grey": "gris"})

CHAMPS_FOND = {"header_color_class", "bg_color_class", "background_color"}
CHAMPS_BADGE = {"color"}


def traduire_classes(valeur):
    """Traduit une chaine de classes, ou la rend inchangee si elle n'en est pas une.

    Conservateur a dessein : une chaine n'est traitee que si TOUS ses jetons sont
    des classes connues. Un texte redactionnel contenant par hasard « fr-btn »
    n'est pas touche.
    """
    jetons = valeur.split()
    if not jetons:
        return valeur
    for j in jetons:
        connu = (
            j in JETONS
            or j in CLASSES_RETIREES
            or j == "fr-btn"
            or j.startswith(("fr-icon-", "fr-fi-", "sdcd-", "ri-"))
        )
        if not connu:
            return valeur
    if not any(j.startswith(("fr-", "sdcd-", "ri-")) for j in jetons):
        return valeur

    base_seule = "fr-btn" in jetons and not (VARIANTES_BOUTON & set(jetons))
    sortie = []
    for j in jetons:
        if j in CLASSES_RETIREES:
            continue
        if j == "fr-btn":
            sortie.append("sdcd-button")
            if base_seule:
                sortie.append("sdcd-button--primaire")
        elif j in JETONS:
            sortie.extend(JETONS[j].split())
        elif j.startswith("fr-icon-"):
            sortie.append("ri-" + j[len("fr-icon-"):])
        elif j.startswith("fr-fi-"):
            sortie.append("ri-" + j[len("fr-fi-"):])
        else:
            sortie.append(j)
    final = []
    for j in sortie:
        if j not in final:
            final.append(j)
    return " ".join(final)


def parcourir(noeud, compteur, cle_parente=None):
    """Reecrit en profondeur classes et couleurs."""
    if isinstance(noeud, dict):
        return {k: parcourir(v, compteur, k) for k, v in noeud.items()}
    if isinstance(noeud, list):
        return [parcourir(v, compteur, cle_parente) for v in noeud]
    if not isinstance(noeud, str) or not noeud:
        return noeud

    if cle_parente in CHAMPS_FOND and noeud in FONDS:
        compteur["couleurs"] += 1
        return FONDS[noeud]
    if cle_parente in CHAMPS_BADGE and noeud in BADGES:
        compteur["couleurs"] += 1
        return BADGES[noeud]
    if "fr-" in noeud:
        neuf = traduire_classes(noeud)
        if neuf != noeud:
            compteur["classes"] += 1
        return neuf
    return noeud


def porter(apps, schema_editor):
    compteur = {"classes": 0, "couleurs": 0}
    objets = 0

    for modele in apps.get_models():
        flux = [
            f.attname
            for f in modele._meta.get_fields()
            if getattr(f, "attname", None) and f.__class__.__name__ == "StreamField"
        ]
        simples = [
            f.attname
            for f in modele._meta.get_fields()
            if getattr(f, "attname", None) and f.attname in CHAMPS_FOND
        ]
        if not flux and not simples:
            continue

        for objet in modele.objects.all().iterator():
            change = False

            for nom in simples:
                valeur = getattr(objet, nom, None)
                if isinstance(valeur, str) and valeur in FONDS:
                    setattr(objet, nom, FONDS[valeur])
                    compteur["couleurs"] += 1
                    change = True

            for nom in flux:
                valeur = getattr(objet, nom, None)
                brut = getattr(valeur, "raw_data", None)
                if brut is None:
                    continue
                # `raw_data` est une vue, pas une liste : on la materialise.
                brut = list(brut)
                neuf = parcourir(brut, compteur)
                if neuf != brut:
                    # Le descripteur du champ sait relire une chaine JSON ; lui
                    # passer la liste brute ne donnerait pas un StreamValue valide.
                    setattr(objet, nom, json.dumps(neuf, ensure_ascii=False))
                    change = True

            if change:
                objet.save()
                objets += 1

    if objets:
        print(
            "  %d classe(s) et %d couleur(s) portees sur %d objet(s)"
            % (compteur["classes"], compteur["couleurs"], objets)
        )


class Migration(migrations.Migration):
    dependencies = [
        ("sites_conformes_core", "0084_portage_couleurs_sdcd"),
    ]
    # Plusieurs couleurs du DSFR convergent vers la meme du SDCD, et deux classes
    # DSFR distinctes vers une seule : la marche arriere ne peut pas les
    # distinguer. Restaurer demanderait une sauvegarde, pas une migration.
    operations = [migrations.RunPython(porter, migrations.RunPython.noop)]
