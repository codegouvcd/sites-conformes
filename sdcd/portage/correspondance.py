"""Correspondance fr-* -> sdcd-*, partagee par le portage du code Python et par
la migration de donnees.

Ces classes ne vivent pas dans les gabarits mais dans les modeles : elles sont
proposees au rediger dans l'administration, puis **stockees en base** comme
valeur de champ. Les porter demande donc deux gestes, pas un : changer ce que le
code propose, et reecrire ce que la base contient deja.
"""

JETONS = {
    # boutons
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
    # cartes
    "fr-card": "sdcd-card",
    "fr-card--horizontal": "sdcd-card--horizontal",
    "fr-card--horizontal-half": "sdcd-card--horizontal-moitie",
    "fr-card--horizontal-tier": "sdcd-card--horizontal-tiers",
    "fr-card__desc": "sdcd-card__description",
    "fr-card__title": "sdcd-card__titre",
    "fr-enlarge-link": "sdcd-cliquable",
    # grille
    "fr-col-12": "sdcd-col-12",
    "fr-col-lg-3": "sdcd-col-lg-3",
    "fr-col-offset-md-2": "sdcd-col-decale-md-2",
    "fr-col-offset-md-3": "sdcd-col-decale-md-3",
    "fr-col-offset-md-4": "sdcd-col-decale-md-4",
    "fr-col-offset-md-6": "sdcd-col-decale-md-6",
    # media et proportions
    "fr-content-media--sm": "sdcd-media--sm",
    "fr-content-media--lg": "sdcd-media--lg",
    "fr-ratio-16x9": "sdcd-ratio-16x9",
    "fr-ratio-32x9": "sdcd-ratio-32x9",
    "fr-responsive-img": "sdcd-image-fluide",
    # navigation et menus
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
    # en-tete et pied de page
    "fr-header__service": "sdcd-header__entite-bloc",
    "fr-header__service-title": "sdcd-header__service",
    "fr-header__service-tagline": "sdcd-header__service-accroche",
    "fr-footer__bottom-link": "sdcd-footer__lien",
    "fr-footer__content-link": "sdcd-footer__lien",
    "fr-footer__brand": "sdcd-footer__marque",
    "fr-logo": "sdcd-logo",
    # liens
    "fr-link": "sdcd-lien",
    "fr-link--sm": "sdcd-lien--sm",
    "fr-link--lg": "sdcd-lien--lg",
    "fr-link--icon-left": "sdcd-lien--icone-gauche",
    "fr-link--icon-right": "sdcd-lien--icone-droite",
    "fr-link--close": "sdcd-lien--fermer",
    "fr-link--align-on-content": "sdcd-lien--aligne",
    "fr-links-group": "sdcd-liens",
    # etiquettes et badges
    "fr-tag": "sdcd-tag",
    "fr-tag--icon-left": "sdcd-tag--icone-gauche",
    "fr-tags-group": "sdcd-tags",
    "fr-badge": "sdcd-badge",
    "fr-badge--sm": "sdcd-badge--sm",
    "fr-badge--green-emeraude": "sdcd-badge--succes",
    # tuiles, bandeaux, divers
    "fr-tile__header": "sdcd-tile__media",
    "fr-tile__pictogram": "sdcd-tile__media",
    "fr-notice__body": "sdcd-notice__corps",
    "fr-error-text": "sdcd-champ__erreur",
    "fr-sr-only": "sdcd-lecteur-seul",
    # typographie et utilitaires
    "fr-h4": "sdcd-h4",
    "fr-mb-2v": "sdcd-mb-2",
    "fr-p-2w": "sdcd-p-4",
    "fr-background-alt--grey": "sdcd-fond-alt",
    "fr-text--sm": "sdcd-texte-sm",
    "fr-text--lg": "sdcd-texte-lg",
    "fr-hidden": "sdcd-masque",
    "fr-displayed-lg": "sdcd-affiche-lg",
}

# Teinte de marque du DSFR sans equivalent : le SDCD ne propose pas de palette
# decorative, ses couleurs portent un sens (succes, alerte, erreur, nouveau).
# On retire plutot que de traduire vers une couleur qui signifierait autre chose.
RETIREES = {"fr-tag--purple-glycine"}


def porter(valeur):
    """Traduit une valeur de champ, qui peut contenir plusieurs classes."""
    if not valeur:
        return valeur
    jetons = valeur.split()
    # `fr-btn` seul est primaire en DSFR ; `.sdcd-button` seul est neutre. On
    # n'ajoute donc `--primaire` que si aucune autre variante n'accompagne la
    # base — sinon le bouton porterait deux variantes contradictoires.
    variantes = {"fr-btn--secondary", "fr-btn--tertiary", "fr-btn--tertiary-no-outline"}
    base_seule = "fr-btn" in jetons and not (variantes & set(jetons))

    sortie = []
    for jeton in jetons:
        if jeton == "fr-btn":
            sortie.append("sdcd-button")
            if base_seule:
                sortie.append("sdcd-button--primaire")
            continue
        if jeton in RETIREES:
            continue
        if jeton in JETONS:
            sortie.extend(JETONS[jeton].split())
        elif jeton.startswith("fr-icon-"):
            sortie.append("ri-" + jeton[len("fr-icon-"):])
        elif jeton.startswith("fr-fi-"):
            sortie.append("ri-" + jeton[len("fr-fi-"):])
        else:
            sortie.append(jeton)
    vus, final = [], []
    for j in sortie:
        if j not in vus:
            vus.append(j)
            final.append(j)
    return " ".join(final)
