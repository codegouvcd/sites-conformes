"""Reecrit les classes DSFR stockees en base vers leurs equivalents SDCD.

Le portage des gabarits et du code Python ne suffit pas : plusieurs blocs
stockent une classe CSS comme **valeur de champ** — taille d'un lien, icone,
type de bouton, proportion d'une image. Ces valeurs vivent dans le JSON des
StreamField et dans quelques champs simples. Un site deja alimente continuerait
donc a rendre des classes `fr-*` que plus aucune feuille ne definit.

La migration parcourt le JSON en profondeur et ne touche qu'aux chaines
entierement composees de classes connues : une chaine qui contiendrait autre
chose — du texte redactionnel, une URL — est laissee telle quelle. C'est
volontairement conservateur : mieux vaut laisser une classe non portee, que la
couche de compatibilite couvre encore, que d'abimer du contenu.

Reversible : la correspondance est bijective sur les valeurs concernees, sauf
`fr-tag--purple-glycine`, teinte decorative sans equivalent — le SDCD ne propose
que des couleurs porteuses de sens. La marche arriere la restitue donc pas.
"""

from django.db import migrations

# Correspondance figee dans la migration plutot qu'importee : une migration doit
# rester lisible et rejouable dans dix ans, meme si le module a bouge.
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
    "fr-hidden": "sdcd-masque",
    "fr-displayed-lg": "sdcd-affiche-lg",
}
VARIANTES_BOUTON = {
    "fr-btn--secondary", "fr-btn--tertiary", "fr-btn--tertiary-no-outline",
}
RETIREES = {"fr-tag--purple-glycine"}


def traduire(valeur):
    """Traduit une chaine de classes, ou la rend inchangee si elle n'en est pas une."""
    jetons = valeur.split()
    if not jetons:
        return valeur
    # Une chaine n'est traitee que si TOUS ses jetons sont des classes connues.
    # Un texte redactionnel contenant par hasard « fr-btn » n'est pas touche.
    for j in jetons:
        connu = (j in JETONS or j in RETIREES or j == "fr-btn"
                 or j.startswith(("fr-icon-", "fr-fi-", "sdcd-", "ri-")))
        if not connu:
            return valeur
    if not any(j.startswith(("fr-", "sdcd-", "ri-")) for j in jetons):
        return valeur

    base_seule = "fr-btn" in jetons and not (VARIANTES_BOUTON & set(jetons))
    sortie = []
    for j in jetons:
        if j in RETIREES:
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


def parcourir(noeud):
    """Reecrit en profondeur, en place, toute chaine de classes rencontree."""
    if isinstance(noeud, dict):
        return {k: parcourir(v) for k, v in noeud.items()}
    if isinstance(noeud, list):
        return [parcourir(v) for v in noeud]
    if isinstance(noeud, str) and "fr-" in noeud:
        return traduire(noeud)
    return noeud


def porter(apps, schema_editor):
    import json

    modifies = 0
    for etiquette, modele in (
        ("sites_conformes_core", "ContentPage"),
        ("sites_conformes_blog", "BlogEntryPage"),
        ("sites_conformes_blog", "BlogIndexPage"),
        ("sites_conformes_events", "EventEntryPage"),
        ("sites_conformes_events", "EventsIndexPage"),
    ):
        try:
            Modele = apps.get_model(etiquette, modele)
        except LookupError:
            continue
        for objet in Modele.objects.all().iterator():
            change = False
            for champ in objet._meta.get_fields():
                if not hasattr(champ, "attname"):
                    continue
                valeur = getattr(objet, champ.attname, None)
                if not isinstance(valeur, str) or "fr-" not in valeur:
                    continue
                try:
                    donnees = json.loads(valeur)
                except (ValueError, TypeError):
                    continue          # champ texte ordinaire, pas un StreamField
                neuf = json.dumps(parcourir(donnees), ensure_ascii=False)
                if neuf != valeur:
                    setattr(objet, champ.attname, neuf)
                    change = True
            if change:
                objet.save()
                modifies += 1
    if modifies:
        print(f"  {modifies} page(s) portee(s) vers les classes SDCD")


def revenir(apps, schema_editor):
    """Marche arriere impossible a l'identique : plusieurs classes DSFR se
    traduisent vers la meme classe SDCD (`fr-nav__btn` et `fr-nav__link` vont
    toutes deux vers `sdcd-header__lien`), et `fr-tag--purple-glycine` n'a pas
    d'equivalent. Restaurer demanderait une sauvegarde, pas une migration."""
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("sites_conformes_core", "0080_cmsdsfrconfig_iframe_allow_origins"),
    ]
    operations = [migrations.RunPython(porter, revenir)]
