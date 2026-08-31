"""Construit le site vitrine : un site de demonstration qui explique comment en faire un.

`create_starter_pages` pose un site vide avec un texte d'attente.
`create_demo_pages` remplit des pages de lorem ipsum pour montrer les blocs.
Ni l'un ni l'autre ne montre a un service ce qu'il peut faire, ni comment.

Cette commande ecrit un vrai site : une page d'accueil qui presente le CMS, un
guide en six etapes pour creer son site, une presentation du systeme de design,
et une foire aux questions. Le contenu est redige, pas genere : c'est ce qu'un
agent d'un ministere lira.

Elle est idempotente : relancee, elle met a jour les pages qu'elle a creees
plutot que d'en ajouter. Le contenu redactionnel est donc reproductible, ce que
des pages construites a la main dans l'administration ne seraient pas.

    python manage.py create_showcase_pages
    python manage.py create_showcase_pages --reinitialiser   # reecrit meme si modifiee
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from wagtail.models import Page
from wagtail.rich_text import RichText

from sites_conformes.core.models import CmsDsfrConfig, ContentPage
from sites_conformes.core.utils import get_default_site
from sites_conformes.menus.models import FooterBottomMenu, MainMenu


def rt(html):
    return RichText(html)


# --------------------------------------------------------------------- accueil
def corps_accueil():
    return [
        (
            "paragraph",
            rt(
                "<p class=\"sdcd-texte-lead\">Le gestionnaire de contenus de "
                "l’administration congolaise. Votre service écrit le contenu ; les "
                "pages, les composants et l’identité de l’État sont déjà là.</p>"
            ),
        ),
        (
            "fullwidthbackground",
            {
                "bg_color_class": "bleu",
                "top_margin": 0,
                "bottom_margin": 0,
                "content": [
                    (
                        # `text`, et non `paragraph` : dans ce bloc de mise en page,
                        # le texte riche porte un autre nom. Un nom inconnu n'est pas
                        # une erreur pour Wagtail, il est ignore — le fond se rendait
                        # vide, sans rien signaler.
                        "text",
                        rt(
                            "<h2>Un site d’État, sans partir de zéro</h2>"
                            "<p>Sites Conformes est le gestionnaire de contenus de "
                            "l’administration congolaise. Il fournit les pages, les "
                            "composants et l’identité visuelle de l’État : votre service "
                            "écrit le contenu, le reste est déjà fait.</p>"
                        ),
                    ),
                ],
            },
        ),
        (
            "item_grid",
            {
                "column_width": "4",
                "horizontal_align": "left",
                "items": [
                    (
                        "tile",
                        {
                            "title": "Créer votre site",
                            "heading_tag": "h3",
                            "description": rt(
                                "<p>Six étapes, de la demande d’ouverture à la mise en "
                                "ligne. Comptez une demi-journée pour la première page.</p>"
                            ),
                            "link": {"link_type": "external_url", "external_url": "/creer-votre-site/"},
                        },
                    ),
                    (
                        "tile",
                        {
                            "title": "Le système de design",
                            "heading_tag": "h3",
                            "description": rt(
                                "<p>Couleurs, typographie, composants. Ce que vous "
                                "assemblez respecte l’identité de l’État sans effort.</p>"
                            ),
                            "link": {"link_type": "external_url", "external_url": "/systeme-de-design/"},
                        },
                    ),
                    (
                        "tile",
                        {
                            "title": "Questions fréquentes",
                            "heading_tag": "h3",
                            "description": rt(
                                "<p>Hébergement, nom de domaine, accessibilité, "
                                "responsabilités de chacun.</p>"
                            ),
                            "link": {"link_type": "external_url", "external_url": "/questions-frequentes/"},
                        },
                    ),
                ],
            },
        ),
        (
            "paragraph",
            rt(
                "<h2>Ce que le CMS apporte</h2>"
                "<p>Un service qui ouvre un site part rarement d’une page blanche : il "
                "part d’un besoin — publier des actualités, un annuaire, des formulaires, "
                "des textes réglementaires — et d’une contrainte : que le résultat soit "
                "reconnaissable comme un site de l’État, lisible sur un téléphone, et "
                "utilisable par tous.</p>"
            ),
        ),
        (
            "item_grid",
            {
                "column_width": "6",
                "items": [
                    (
                        "card",
                        {
                            "title": "L’identité de l’État, par défaut",
                            "heading_tag": "h3",
                            "description": rt(
                                "<p>Armoiries, filet tricolore, devise, typographie et "
                                "couleurs sont posés par le système. Un rédacteur ne peut "
                                "pas produire une page hors charte par inadvertance.</p>"
                            ),
                        },
                    ),
                    (
                        "card",
                        {
                            "title": "Accessible et lisible sur téléphone",
                            "heading_tag": "h3",
                            "description": rt(
                                "<p>Contrastes vérifiés, navigation au clavier, mesure de "
                                "lecture bornée. La majorité des visites se fait sur un "
                                "téléphone : la mise en page en tient compte d’abord.</p>"
                            ),
                        },
                    ),
                    (
                        "card",
                        {
                            "title": "Vous restez propriétaire",
                            "heading_tag": "h3",
                            "description": rt(
                                "<p>Le code est libre, sous licence AGPL-3.0, et publié. "
                                "Aucun engagement envers un prestataire : le service peut "
                                "héberger lui-même ou déléguer.</p>"
                            ),
                        },
                    ),
                    (
                        "card",
                        {
                            "title": "Pensé pour des rédacteurs",
                            "heading_tag": "h3",
                            "description": rt(
                                "<p>On assemble des blocs — texte, image, carte, "
                                "accordéon, tableau — sans écrire une ligne de code. La "
                                "prise en main tient en une matinée.</p>"
                            ),
                        },
                    ),
                ],
            },
        ),
        (
            "callout",
            {
                "title": "Ce site est lui-même une démonstration",
                "heading_tag": "h2",
                "icon_class": "ri-information-line",
                "text": rt(
                    "<p>Toutes les pages que vous parcourez ici ont été construites avec "
                    "le CMS, avec les mêmes blocs que ceux mis à votre disposition. Rien "
                    "n’a été développé sur mesure.</p>"
                ),
                "color": "chart-1",
            },
        ),
    ]


# ------------------------------------------------------------- créer son site
def corps_creer():
    return [
        (
            "paragraph",
            rt(
                "<p class=\"sdcd-texte-lead\">De la demande d’ouverture à la mise en "
                "ligne, la création d’un site suit six étapes. Les trois premières "
                "relèvent de votre administration, les trois suivantes de votre "
                "équipe éditoriale.</p>"
            ),
        ),
        (
            "stepper",
            {
                "title": "Ouvrir le site",
                "heading_tag": "h2",
                "total": 6,
                "current": 1,
                "steps": [
                    (
                        "step",
                        {
                            "title": "Désigner un responsable de publication",
                            "detail": "C’est la personne qui engage l’entité sur ce qui est "
                            "publié. Elle figure dans les mentions légales et arbitre en "
                            "cas de doute. Sans elle, le site ne peut pas ouvrir.",
                        },
                    ),
                    (
                        "step",
                        {
                            "title": "Obtenir un nom de domaine en .gouv.cd",
                            "detail": "Le domaine est délivré par l’autorité compétente. "
                            "Un site d’État se reconnaît à son adresse : c’est la première "
                            "protection du citoyen contre les sites frauduleux.",
                        },
                    ),
                    (
                        "step",
                        {
                            "title": "Choisir l’hébergement",
                            "detail": "Hébergement par votre direction informatique, ou "
                            "délégué. Le CMS s’installe avec Docker et une base "
                            "PostgreSQL ; l’installation type tient sur un serveur modeste.",
                        },
                    ),
                    (
                        "step",
                        {
                            "title": "Renseigner la configuration du site",
                            "detail": "Intitulé officiel, sous-titre, logo de l’opérateur, "
                            "coordonnées. Tout se règle dans Configuration › Configuration "
                            "du site, sans toucher au code.",
                        },
                    ),
                    (
                        "step",
                        {
                            "title": "Écrire les pages obligatoires",
                            "detail": "Mentions légales, déclaration d’accessibilité, page "
                            "de contact. Elles existent déjà, vides : votre service "
                            "juridique en fournit le contenu applicable.",
                        },
                    ),
                    (
                        "step",
                        {
                            "title": "Construire l’arborescence et publier",
                            "detail": "Créez vos rubriques, assemblez vos pages à partir "
                            "des blocs, prévisualisez, publiez. Une page peut être "
                            "préparée puis publiée à une date choisie.",
                        },
                    ),
                ],
            },
        ),
        (
            "paragraph",
            rt(
                "<h2>Assembler une page</h2>"
                "<p>Une page se compose de blocs empilés. Vous choisissez un bloc, vous "
                "le remplissez, vous le déplacez si besoin. Il n’y a pas de gabarit figé "
                "à respecter : c’est la succession des blocs qui fait la page.</p>"
            ),
        ),
        (
            "accordions",
            [
                ("title", "Les blocs les plus utilisés"),
                (
                    "accordion",
                    {
                        "title": "Texte enrichi",
                        "content": rt(
                            "<p>Le bloc de base : titres, paragraphes, listes, liens, "
                            "gras et italique. Sa largeur de ligne est bornée "
                            "automatiquement, pour que le texte reste lisible sur un "
                            "grand écran.</p>"
                            "<p>Évitez de coller du texte depuis un traitement de texte "
                            "sans le nettoyer : la mise en forme importée entre en "
                            "conflit avec celle du système.</p>"
                        ),
                    },
                ),
                (
                    "accordion",
                    {
                        "title": "Cartes et tuiles",
                        "content": rt(
                            "<p>Une <strong>tuile</strong> oriente : elle porte un titre "
                            "court et mène ailleurs. Une <strong>carte</strong> informe : "
                            "elle porte un titre, une description, parfois une image, une "
                            "étiquette et un lien.</p>"
                            "<p>Posées dans une grille d’éléments, elles se réorganisent "
                            "d’elles-mêmes selon la largeur de l’écran.</p>"
                        ),
                    },
                ),
                (
                    "accordion",
                    {
                        "title": "Accordéons",
                        "content": rt(
                            "<p>Pour une suite de questions-réponses ou une procédure "
                            "détaillée. Le visiteur ouvre ce qui l’intéresse. À réserver "
                            "aux contenus secondaires : ce qui est replié est moins lu, "
                            "et n’est pas trouvé par la recherche du navigateur.</p>"
                        ),
                    },
                ),
                (
                    "accordion",
                    {
                        "title": "Fond pleine largeur",
                        "content": rt(
                            "<p>Pour marquer une rupture entre deux sections. Les "
                            "couleurs proposées sont des teintes claires, vérifiées pour "
                            "porter du texte sans perte de contraste.</p>"
                            "<p>Deux fonds colorés consécutifs annulent l’effet : "
                            "alternez avec du blanc.</p>"
                        ),
                    },
                ),
                (
                    "accordion",
                    {
                        "title": "Indicateur d’étapes",
                        "content": rt(
                            "<p>Pour une démarche en plusieurs temps, comme celle que "
                            "vous lisez plus haut. Indiquez le nombre total d’étapes et "
                            "l’étape en cours ; la jauge se dessine seule.</p>"
                        ),
                    },
                ),
            ],
        ),
        (
            "paragraph",
            rt(
                "<h2>Avant de publier</h2>"
                "<p>Quatre vérifications valent d’être faites sur chaque page, avant le "
                "premier clic sur « Publier ».</p>"
            ),
        ),
        (
            "item_grid",
            {
                "column_width": "6",
                "items": [
                    (
                        "card",
                        {
                            "title": "Un seul titre de niveau 1",
                            "heading_tag": "h3",
                            "description": rt(
                                "<p>C’est le titre de la page, posé automatiquement. Dans "
                                "vos blocs de texte, commencez donc au niveau 2, et ne "
                                "sautez pas de niveau.</p>"
                            ),
                        },
                    ),
                    (
                        "card",
                        {
                            "title": "Une alternative sur chaque image",
                            "heading_tag": "h3",
                            "description": rt(
                                "<p>Décrivez ce que l’image apporte. Si elle est purement "
                                "décorative, cochez la case prévue : elle sera ignorée "
                                "par les lecteurs d’écran.</p>"
                            ),
                        },
                    ),
                    (
                        "card",
                        {
                            "title": "Des liens qui se comprennent seuls",
                            "heading_tag": "h3",
                            "description": rt(
                                "<p>« Consulter le décret » plutôt que « cliquez ici ». "
                                "Un utilisateur de lecteur d’écran parcourt souvent la "
                                "liste des liens, hors de leur phrase.</p>"
                            ),
                        },
                    ),
                    (
                        "card",
                        {
                            "title": "Un aperçu sur téléphone",
                            "heading_tag": "h3",
                            "description": rt(
                                "<p>Le bouton « Aperçu » de l’éditeur propose les "
                                "largeurs mobile et bureau. La majorité de vos visiteurs "
                                "verra la première.</p>"
                            ),
                        },
                    ),
                ],
            },
        ),
    ]


# --------------------------------------------------------- système de design
def corps_design():
    return [
        (
            "paragraph",
            rt(
                "<p class=\"sdcd-texte-lead\">Le Système de design RDC fournit les "
                "couleurs, la typographie et les composants communs aux sites de l’État "
                "congolais. Le CMS s’appuie dessus : vous n’avez rien à en connaître pour "
                "l’utiliser, mais en comprendre les règles aide à faire de bons choix.</p>"
            ),
        ),
        (
            "paragraph",
            rt(
                "<h2>Trois principes</h2>"
                "<p>Ils expliquent la plupart des contraintes que vous rencontrerez dans "
                "l’éditeur.</p>"
            ),
        ),
        (
            "item_grid",
            {
                "column_width": "4",
                "items": [
                    (
                        "card",
                        {
                            "title": "La couleur porte un sens",
                            "heading_tag": "h3",
                            "description": rt(
                                "<p>Le vert dit la réussite, l’orange l’avertissement, le "
                                "rouge l’erreur. C’est pourquoi la palette est courte : "
                                "une couleur choisie pour décorer brouille un message que "
                                "d’autres pages utilisent pour alerter.</p>"
                            ),
                        },
                    ),
                    (
                        "card",
                        {
                            "title": "Le contraste n’est pas négociable",
                            "heading_tag": "h3",
                            "description": rt(
                                "<p>Chaque couple texte/fond est vérifié à 4,5:1 au "
                                "minimum, en thème clair comme en thème sombre. Les fonds "
                                "proposés dans l’éditeur sont ceux qui passent ce seuil.</p>"
                            ),
                        },
                    ),
                    (
                        "card",
                        {
                            "title": "Le téléphone d’abord",
                            "heading_tag": "h3",
                            "description": rt(
                                "<p>Les composants sont dessinés pour un écran étroit, "
                                "puis étendus. Une grille de trois colonnes devient une "
                                "colonne unique sans que vous ayez à le prévoir.</p>"
                            ),
                        },
                    ),
                ],
            },
        ),
        (
            "paragraph",
            rt(
                "<h2>Quelques composants</h2>"
                "<p>Voici, rendus par le système lui-même, des éléments que vous "
                "retrouverez dans l’éditeur.</p>"
            ),
        ),
        (
            "badges_list",
            [
                ("badge", {"text": "Nouveau", "color": "nouveau"}),
                ("badge", {"text": "En vigueur", "color": "succes"}),
                ("badge", {"text": "En consultation", "color": "info"}),
                ("badge", {"text": "Abrogé", "color": "erreur"}),
            ],
        ),
        (
            "tags_list",
            [
                ("tag", {"label": "Santé", "color": "chart-4"}),
                ("tag", {"label": "Éducation", "color": "chart-1"}),
                ("tag", {"label": "Infrastructures", "color": "chart-3"}),
                ("tag", {"label": "Numérique", "color": "chart-2"}),
            ],
        ),
        (
            "highlight",
            {
                "text": rt(
                    "<p>Une mise en exergue attire l’œil sur une phrase, sans lui donner "
                    "le poids d’un titre. À employer une fois par page au plus.</p>"
                ),
                "color": "chart-2",
                "size": "sdcd-texte-lg",
            },
        ),
        (
            "quote",
            {
                "quote": "Un service public en ligne doit être aussi accessible que son "
                "guichet : à tous, sans condition.",
                "author_name": "Principe directeur",
                "author_title": "Système de design RDC",
            },
        ),
        (
            "callout",
            {
                "title": "Le système est public",
                "heading_tag": "h2",
                "icon_class": "ri-git-repository-line",
                "text": rt(
                    "<p>Code, jetons de couleur et composants sont publiés sous licence "
                    "MIT. Les armoiries, la devise et le filet tricolore restent, eux, "
                    "réservés aux entités de l’État.</p>"
                ),
                "color": "chart-1",
            },
        ),
    ]


# ------------------------------------------------------------------- la FAQ
def corps_faq():
    return [
        (
            "paragraph",
            rt(
                "<p class=\"sdcd-texte-lead\">Les questions que se posent les services "
                "avant d’ouvrir un site. Si la vôtre n’y figure pas, la page de contact "
                "est faite pour ça.</p>"
            ),
        ),
        (
            "accordions",
            [
                ("title", "Ouvrir et héberger"),
                (
                    "accordion",
                    {
                        "title": "Combien coûte le CMS ?",
                        "content": rt(
                            "<p>Le logiciel est libre et gratuit. Les coûts sont ceux de "
                            "l’hébergement, du nom de domaine et du temps de vos agents. "
                            "Il n’y a ni licence, ni redevance, ni engagement.</p>"
                        ),
                    },
                ),
                (
                    "accordion",
                    {
                        "title": "Faut-il un développeur ?",
                        "content": rt(
                            "<p>Pour installer et maintenir l’hébergement, oui — une "
                            "personne à l’aise avec Docker et PostgreSQL. Pour créer et "
                            "publier des pages, non : l’éditeur ne demande aucune "
                            "compétence technique.</p>"
                        ),
                    },
                ),
                (
                    "accordion",
                    {
                        "title": "Peut-on reprendre un site existant ?",
                        "content": rt(
                            "<p>Les contenus doivent être ressaisis ou importés page par "
                            "page. C’est l’occasion de faire le tri : un site repris tel "
                            "quel reconduit ses pages mortes.</p>"
                        ),
                    },
                ),
            ],
        ),
        (
            "accordions",
            [
                ("title", "Contenu et responsabilités"),
                (
                    "accordion",
                    {
                        "title": "Qui est responsable de ce qui est publié ?",
                        "content": rt(
                            "<p>Le responsable de publication désigné par l’entité. Le "
                            "CMS fournit l’outil ; il ne se substitue pas à la "
                            "responsabilité éditoriale, qui reste entière.</p>"
                        ),
                    },
                ),
                (
                    "accordion",
                    {
                        "title": "Que doivent contenir les mentions légales ?",
                        "content": rt(
                            "<p>L’identité de l’éditeur, celle de l’hébergeur, le "
                            "responsable de publication, et le traitement des données "
                            "personnelles. Le texte applicable relève du droit congolais : "
                            "faites-le valider par votre service juridique. Le CMS "
                            "fournit la page, pas son contenu.</p>"
                        ),
                    },
                ),
                (
                    "accordion",
                    {
                        "title": "Le site est-il accessible aux personnes handicapées ?",
                        "content": rt(
                            "<p>Le système de design pose les bases : contrastes, "
                            "navigation au clavier, structure de titres, alternatives "
                            "d’images. Mais un site n’est accessible que si son contenu "
                            "l’est aussi. La déclaration d’accessibilité doit refléter un "
                            "audit réel, pas une intention.</p>"
                        ),
                    },
                ),
                (
                    "accordion",
                    {
                        "title": "Plusieurs personnes peuvent-elles rédiger ?",
                        "content": rt(
                            "<p>Oui. Chaque rédacteur a son compte, et une page peut être "
                            "soumise à relecture avant publication. L’historique conserve "
                            "qui a modifié quoi, et permet de revenir en arrière.</p>"
                        ),
                    },
                ),
            ],
        ),
    ]


PAGES = [
    ("creer-votre-site", "Créer votre site", corps_creer, 1),
    ("systeme-de-design", "Le système de design", corps_design, 2),
    ("questions-frequentes", "Questions fréquentes", corps_faq, 3),
]


class Command(BaseCommand):
    help = "Construit le site vitrine : accueil, guide de creation, systeme de design, FAQ."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reinitialiser",
            action="store_true",
            help="Reecrit les pages meme si elles ont ete modifiees depuis leur creation.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        site = get_default_site()
        accueil = site.root_page.specific if site else None

        if not isinstance(accueil, ContentPage):
            self.stderr.write(
                self.style.ERROR(
                    "La racine du site n'est pas une ContentPage. "
                    "Lancez d'abord `create_starter_pages`."
                )
            )
            return

        self.configurer(site)
        self.ecrire_accueil(accueil, options["reinitialiser"])

        creees = []
        for slug, titre, corps, ordre in PAGES:
            page = self.ecrire_page(accueil, slug, titre, corps(), options["reinitialiser"])
            if page:
                creees.append((page, ordre))

        self.ranger_menu(site, accueil, creees)
        self.stdout.write(self.style.SUCCESS("Site vitrine en place."))

    # ------------------------------------------------------------------ outils
    def configurer(self, site):
        """Renseigne l'identite du site.

        Sans cela, la demonstration affiche « Titre du site », « Sous-titre du
        site » et « Intitulé officiel » : les valeurs d'usine. Un service qui
        decouvre le CMS y verrait un site inacheve plutot qu'un exemple.
        """
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
        config.save()
        self.stdout.write(self.style.SUCCESS("  configuration du site : renseignee"))

        menu = FooterBottomMenu.objects.filter(site=site).first()
        if menu:
            liens = []
            for slug, libelle in (
                ("mentions-legales", "Mentions légales"),
                ("accessibilite", "Accessibilité"),
                ("contact", "Contact"),
            ):
                page = Page.objects.filter(slug=slug).first()
                if page:
                    liens.append(("link", {"text": libelle, "page": page, "link_type": "page"}))
            menu.items = liens
            menu.save()
            self.stdout.write(self.style.SUCCESS(f"  bas de page : {len(liens)} liens"))

    def ecrire_accueil(self, accueil, forcer):
        accueil.title = "Sites Conformes"
        accueil.seo_title = "Sites Conformes — le gestionnaire de contenus de l’État congolais"
        accueil.search_description = (
            "Le gestionnaire de contenus de l’administration congolaise : pages, "
            "composants et identité de l’État, prêts à l’emploi."
        )
        accueil.header_with_title = True
        accueil.body = corps_accueil()
        self.publier(accueil, "accueil")

    def ecrire_page(self, parent, slug, titre, corps, forcer):
        page = ContentPage.objects.filter(slug=slug).first()
        if page:
            if not forcer and page.latest_revision_id and page.live_revision_id != page.latest_revision_id:
                self.stdout.write(
                    f"  {slug} : modifiee depuis sa creation, laissee telle quelle "
                    f"(--reinitialiser pour l'ecraser)"
                )
                return page
            page.title = titre
            page.body = corps
            self.publier(page, slug)
            return page

        page = ContentPage(title=titre, slug=slug, body=corps, show_in_menus=True)
        parent.add_child(instance=page)
        self.publier(page, slug)
        return page

    def publier(self, page, etiquette):
        page.save()
        revision = page.save_revision()
        revision.publish()
        self.stdout.write(self.style.SUCCESS(f"  {etiquette} : publiee"))

    def ranger_menu(self, site, accueil, pages):
        """Le menu principal suit l'arborescence : accueil, puis les trois rubriques."""
        menu = MainMenu.objects.filter(site=site).first()
        if not menu:
            self.stdout.write("  menu principal absent, non modifie")
            return

        contact = Page.objects.filter(slug="contact").first()
        entrees = [("link", {"text": "Accueil", "page": accueil, "link_type": "page"})]
        for page, _ordre in sorted(pages, key=lambda c: c[1]):
            entrees.append(("link", {"text": page.title, "page": page, "link_type": "page"}))
        if contact:
            entrees.append(("link", {"text": "Contact", "page": contact, "link_type": "page"}))

        menu.items = entrees
        menu.save()
        self.stdout.write(self.style.SUCCESS(f"  menu principal : {len(entrees)} entrees"))
