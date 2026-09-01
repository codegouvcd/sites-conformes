"""Reglages du site vitrine : identite, en-tete, bandeau, lettre d'information,
reseaux sociaux, menus. Tout ce que le CMS sait afficher est active, pour que
la demonstration le montre."""

from django.conf import settings
from wagtail.models import Page

from sites_conformes.core.models import CmsDsfrConfig, SocialMediaItem
from sites_conformes.menus.models import FooterBottomMenu, MainMenu, TopMenu

from .outils import rt

RESEAUX = [
    ("Facebook", "https://www.facebook.com/", "ri-facebook-circle-line"),
    ("X (Twitter)", "https://x.com/", "ri-twitter-x-line"),
    ("LinkedIn", "https://www.linkedin.com/", "ri-linkedin-box-line"),
    ("YouTube", "https://www.youtube.com/", "ri-youtube-line"),
]


def adresse_publique():
    base = f"{settings.HOST_PROTO}://{settings.HOST_URL}"
    port = getattr(settings, "HOST_PORT", "")
    if port and port not in ("80", "443"):
        base = f"{base}:{port}"
    return base


def configurer(site, pages, ecrire=print):
    config = CmsDsfrConfig.for_site(site)
    config.site_title = "Sites Conformes"
    config.site_tagline = "Le gestionnaire de contenus de l’État"
    config.header_brand = "République Démocratique du Congo"
    config.header_brand_html = "République<br />Démocratique<br />du Congo"
    config.footer_brand = "République Démocratique du Congo"
    config.footer_brand_html = "République<br />Démocratique<br />du Congo"
    config.footer_description = rt(
        "<p>Sites Conformes est mis à disposition des services de l’État "
        "congolais. Le code est libre ; chaque entité reste responsable de "
        "ce qu’elle publie.</p>"
    )

    # En-tete : recherche, connexion, parametres d'affichage.
    config.search_bar = True
    config.header_login_button = True
    config.theme_modale_button = True
    config.beta_tag = False

    # Bandeau d'information : ce site est une demonstration.
    config.notice_title = rt("<p>Site de démonstration</p>")
    config.notice_description = rt(
        "<p>Ce site montre ce que Sites Conformes sait faire. Ses contenus, ses "
        "actualités et ses événements sont fictifs.</p>"
    )
    config.notice_type = "info"
    config.notice_icon_class = "ri-flask-line"
    config.notice_is_collapsible = True

    # Lettre d'information : le bloc s'affiche des que description et adresse sont renseignees.
    config.newsletter_description = (
        "Une lettre par mois sur les nouveautés du CMS, les formations et les "
        "sites qui ouvrent."
    )
    config.newsletter_url = f"{adresse_publique()}/contact/"

    # Liens de partage sur les pages, articles et evenements.
    config.share_links_content_pages = True
    config.share_links_blog_posts = True
    config.share_links_events = True
    config.share_links_facebook = True
    config.share_links_twitter = True
    config.share_links_linkedin = True
    config.share_links_email = True
    config.share_links_clipboard = True
    config.save()

    # Reseaux sociaux (idempotent : on remplace la liste).
    config.social_media_items.all().delete()
    for ordre, (titre, url, icone) in enumerate(RESEAUX):
        SocialMediaItem.objects.create(site_config=config, title=titre, url=url, icon_class=icone, sort_order=ordre)
    ecrire("  configuration du site : identité, recherche, connexion, bandeau, lettre, réseaux")

    # Menu haut : trois acces rapides.
    haut = TopMenu.objects.filter(site=site).first()
    if haut is None:
        haut = TopMenu(site=site)
    haut.items = [
        ("link", {"text": "Documentation", "link_type": "page", "page": pages["creer-votre-site"],
                  "icon_class": "ri-book-2-line"}),
        ("link", {"text": "Code source", "link_type": "external_url",
                  "external_url": "https://github.com/codegouvcd/sites-conformes", "icon_class": "ri-github-line"}),
        ("link", {"text": "Nous contacter", "link_type": "page", "page": pages["contact"],
                  "icon_class": "ri-mail-line"}),
    ]
    haut.save()
    ecrire("  menu haut : 3 accès rapides")

    # Bas de page.
    bas = FooterBottomMenu.objects.filter(site=site).first()
    if bas is None:
        bas = FooterBottomMenu(site=site)
    liens = []
    for slug, libelle in (("mentions-legales", "Mentions légales"), ("accessibilite", "Accessibilité"),
                          ("contact", "Contact")):
        page = Page.objects.filter(slug=slug).first()
        if page:
            liens.append(("link", {"text": libelle, "page": page, "link_type": "page"}))
    bas.items = liens
    bas.save()
    ecrire(f"  bas de page : {len(liens)} liens")


def lien(page, texte=None):
    return ("link", {"text": texte or page.title, "link_type": "page", "page": page})


def ranger_menu(site, pages, composants, ecrire=print):
    """Menu principal a la maniere de sites.beta.gouv.fr : accueil, un mega-menu
    d'exemples en deux colonnes, la documentation en sous-menu, puis les
    rubriques vivantes."""
    menu = MainMenu.objects.filter(site=site).first()
    if menu is None:
        menu = MainMenu(site=site)

    exemples_pages = [
        lien(pages["page-atterrissage"], "Page d’atterrissage"),
        lien(pages["site-vitrine"], "Site vitrine d’une administration"),
        lien(pages["actualites"], "Blog"),
        lien(pages["agenda"], "Agenda"),
        lien(pages["catalogue-de-services"], "Catalogue"),
        lien(pages["formulaire-de-demonstration"], "Formulaire"),
    ]
    entrees = [
        lien(pages["accueil"], "Accueil"),
        ("megamenu", {
            "label": "Exemples",
            "description": "Des pages construites avec les blocs du CMS, à ouvrir puis à retrouver dans le back-office.",
            "main_link": {"text": "Voir toute la rubrique", "link_type": "page", "page": pages["exemples"]},
            "columns": [
                ("column", {"label": "Exemples de pages", "links": exemples_pages}),
                ("column", {"label": "Exemples de composants", "links": [lien(p) for p in composants]}),
            ],
        }),
        ("submenu", {
            "label": "Documentation",
            "links": [
                lien(pages["creer-votre-site"], "Créer votre site"),
                lien(pages["systeme-de-design"], "Le système de design"),
                lien(pages["questions-frequentes"], "Questions fréquentes"),
            ],
        }),
        lien(pages["actualites"], "Actualités"),
        lien(pages["agenda"], "Agenda"),
        lien(pages["contact"], "Contact"),
    ]
    menu.items = entrees
    menu.save()
    ecrire(f"  menu principal : {len(entrees)} entrées, {len(exemples_pages)} exemples de pages, "
           f"{len(composants)} exemples de composants")
