"""Construit le site vitrine : un site de demonstration qui montre ce que le CMS sait faire.

`create_starter_pages` pose un site vide avec un texte d'attente.
`create_demo_pages` remplit des pages de lorem ipsum pour montrer les blocs.
Ni l'un ni l'autre ne montre a un service ce qu'il peut faire, ni comment.

Cette commande ecrit un vrai site, a la maniere de sites.beta.gouv.fr pour la
version francaise : un accueil qui presente le CMS, une rubrique « Exemples »
(page d'atterrissage, site vitrine, actualites, agenda, catalogue, formulaire),
la documentation (creer son site, systeme de design, FAQ), et tout ce que
l'en-tete et le pied savent afficher : recherche, connexion, bandeau, lettre
d'information, reseaux sociaux, mega-menu. Le contenu est redige, en contexte
congolais ; il vit dans `sites_conformes.core.vitrine`.

Elle est idempotente : relancee, elle met a jour les pages qu'elle a creees
plutot que d'en ajouter.

    python manage.py create_showcase_pages
    python manage.py create_showcase_pages --reinitialiser   # reecrit meme si modifiee
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from wagtail.models import Page

from sites_conformes.blog.models import BlogEntryPage, BlogIndexPage, Category
from sites_conformes.core.models import CatalogIndexPage, ContentPage
from sites_conformes.core.utils import get_default_site
from sites_conformes.core.vitrine import accueil, configuration, documentation, exemples
from sites_conformes.core.vitrine.images import importer_images
from sites_conformes.events.models import EventEntryPage, EventsIndexPage
from sites_conformes.forms.models import FormField, FormPage

class Command(BaseCommand):
    help = "Construit le site vitrine : accueil, exemples, documentation, reglages."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reinitialiser",
            action="store_true",
            help="Reecrit les pages meme si elles ont ete modifiees depuis leur creation.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        site = get_default_site()
        racine = site.root_page.specific if site else None

        if not isinstance(racine, ContentPage):
            self.stderr.write(
                self.style.ERROR(
                    "La racine du site n'est pas une ContentPage. "
                    "Lancez d'abord `create_starter_pages`."
                )
            )
            return

        self.forcer = options["reinitialiser"]
        ecrire = self.stdout.write
        images = importer_images(ecrire)

        pages = {"accueil": racine}
        contact = Page.objects.filter(slug="contact").first()
        if contact is None:
            self.stderr.write(self.style.ERROR("La page de contact est absente : lancez `create_starter_pages`."))
            return
        pages["contact"] = contact

        # ---------------------------------------------------------- documentation
        for slug, titre, corps, _ordre in documentation.PAGES:
            pages[slug] = self.page_contenu(racine, slug, titre, corps())

        # ---------------------------------------------------------------- exemples
        index = self.index(CatalogIndexPage, racine, "exemples", "Exemples", exemples.INTRO_EXEMPLES)
        pages["exemples"] = index
        # Le catalogue « Exemples » liste ses sous-pages ; les pages d'exemple
        # sont creees avant l'accueil, qui les relie.
        pages["formulaire-de-demonstration"] = self.formulaire(index)
        blog = self.index(BlogIndexPage, index, "actualites", "Actualités", exemples.intro_blog())
        pages["actualites"] = blog
        agenda = self.index(EventsIndexPage, index, "agenda", "Agenda", exemples.intro_agenda())
        pages["agenda"] = agenda
        catalogue = self.index(CatalogIndexPage, index, "catalogue-de-services", "Catalogue de services",
                               exemples.intro_catalogue())
        pages["catalogue-de-services"] = catalogue

        pages["page-atterrissage"] = self.page_contenu(index, "page-atterrissage", "Page d’atterrissage d’un service numérique", [])
        pages["site-vitrine"] = self.page_contenu(index, "site-vitrine", "Site vitrine d’une administration", [])
        hero, corps = exemples.atterrissage(images, pages)
        self.page_contenu(index, "page-atterrissage", "Page d’atterrissage d’un service numérique", corps, hero=hero,
                          image=images["hero-atterrissage"])
        hero, corps = exemples.vitrine(images, pages, blog, agenda)
        self.page_contenu(index, "site-vitrine", "Site vitrine d’une administration", corps, hero=hero,
                          image=images["hero-vitrine"])

        self.articles(blog, images)
        self.evenements(agenda, images)
        self.fiches(catalogue, images)

        # Exemples de composants : les modeles de pages a copier, quand ils
        # existent. On lit les enfants de leur index plutot qu'une liste de
        # slugs ecrite a la main — celle-ci ne correspondait pas aux slugs
        # reels, et le menu se retrouvait sans aucun exemple de composant.
        # L'index des modeles porte le slug `page_templates_index` (pose par
        # create_starter_pages), pas celui que son titre laisse deviner.
        modeles = (
            Page.objects.filter(slug="page_templates_index").first()
            or Page.objects.filter(slug="modeles-de-pages-a-copier").first()
        )
        composants = list(modeles.get_children().live().specific()) if modeles else []
        pages["composant-blocs"] = next((p for p in composants if "bloc" in p.slug), None) or pages["systeme-de-design"]
        pages["modeles"] = modeles or index

        # ----------------------------------------------------------------- accueil
        racine.title = "Sites Conformes"
        racine.seo_title = "Sites Conformes — le gestionnaire de contenus de l’État congolais"
        racine.search_description = (
            "Le gestionnaire de contenus de l’administration congolaise : pages, "
            "composants et identité de l’État, prêts à l’emploi."
        )
        racine.header_with_title = False
        racine.hero = accueil.hero(images, pages)
        racine.body = accueil.corps(images, pages, blog, agenda)
        self.publier(racine, "accueil")

        # ---------------------------------------------------------------- reglages
        configuration.configurer(site, pages, ecrire)
        configuration.ranger_menu(site, pages, composants, ecrire)
        self.stdout.write(self.style.SUCCESS("Site vitrine en place."))

    # ------------------------------------------------------------------ outils
    def modifiee(self, page):
        return bool(page.latest_revision_id and page.live_revision_id != page.latest_revision_id)

    def laisser(self, page, slug):
        if self.forcer or not self.modifiee(page):
            return False
        self.stdout.write(f"  {slug} : modifiée depuis sa création, laissée telle quelle (--reinitialiser pour l'écraser)")
        return True

    def page_contenu(self, parent, slug, titre, corps, hero=None, image=None):
        page = ContentPage.objects.filter(slug=slug).first()
        if page and self.laisser(page, slug):
            return page
        if page is None:
            page = ContentPage(title=titre, slug=slug, show_in_menus=True)
            parent.add_child(instance=page)
        page.title = titre
        page.body = corps
        if hero is not None:
            page.hero = hero
        if image is not None:
            page.header_image = image
        self.publier(page, slug)
        return page

    def index(self, modele, parent, slug, titre, corps):
        page = modele.objects.filter(slug=slug).first()
        if page and self.laisser(page, slug):
            return page
        if page is None:
            page = modele(title=titre, slug=slug, show_in_menus=True)
            parent.add_child(instance=page)
        page.title = titre
        page.body = corps
        self.publier(page, slug)
        return page

    def formulaire(self, parent):
        slug = "formulaire-de-demonstration"
        page = FormPage.objects.filter(slug=slug).first()
        if page and self.laisser(page, slug):
            return page
        if page is None:
            page = FormPage(title="Formulaire de démonstration", slug=slug, show_in_menus=True)
            parent.add_child(instance=page)
        page.title = "Formulaire de démonstration"
        page.intro = exemples.INTRO_FORMULAIRE
        page.thank_you_text = exemples.MERCI_FORMULAIRE
        page.save()
        page.form_fields.all().delete()
        for ordre, (type_, libelle, aide, requis, choix) in enumerate(exemples.champs_formulaire()):
            FormField.objects.create(
                page=page, sort_order=ordre, label=libelle, field_type=type_, required=requis,
                help_text=aide, choices=choix, default_value="",
            )
        self.publier(page, slug)
        return page

    def categorie(self, nom):
        from django.utils.text import slugify

        categorie = Category.objects.filter(name=nom).first()
        if categorie is None:
            categorie = Category.objects.create(name=nom, slug=slugify(nom))
        return categorie

    def articles(self, blog, images):
        for slug, titre, date, categorie, etiquettes, image, corps in exemples.articles(images):
            page = BlogEntryPage.objects.filter(slug=slug).first()
            if page and self.laisser(page, slug):
                continue
            if page is None:
                page = BlogEntryPage(title=titre, slug=slug)
                blog.add_child(instance=page)
            page.title = titre
            page.date = date
            page.body = corps
            page.header_image = image
            page.save()
            page.blog_categories.set([self.categorie(categorie)])
            page.tags.set(etiquettes, clear=True)
            self.publier(page, slug)

    def evenements(self, agenda, images):
        for slug, titre, debut, fin, lieu, categorie, etiquettes, image, corps in exemples.evenements(images):
            page = EventEntryPage.objects.filter(slug=slug).first()
            if page and self.laisser(page, slug):
                continue
            if page is None:
                page = EventEntryPage(title=titre, slug=slug)
                agenda.add_child(instance=page)
            page.title = titre
            page.date = debut
            page.event_date_start = debut
            page.event_date_end = fin
            page.location = lieu
            page.body = corps
            page.header_image = image
            page.save()
            page.event_categories.set([self.categorie(categorie)])
            page.tags.set(etiquettes, clear=True)
            self.publier(page, slug)

    def fiches(self, catalogue, images):
        for slug, titre, etiquettes, image, corps in exemples.fiches(images):
            page = self.page_contenu(catalogue, slug, titre, corps, image=image)
            page.tags.set(etiquettes, clear=True)
            page.save()

    def publier(self, page, etiquette):
        # Le resume sert aux tuiles des catalogues et aux balises de partage ;
        # sans lui, l'extrait est calcule sur le corps et remonte des noms de
        # classes ou des libelles de blocs.
        # Toujours, pas seulement quand il est vide : la page de base remplit
        # search_description a partir du corps a la premiere sauvegarde, et
        # l'extrait remontait alors des libelles de blocs (« width 4 content »).
        if page.slug in exemples.RESUMES:
            page.search_description = exemples.RESUMES[page.slug]
        page.save()
        revision = page.save_revision()
        revision.publish()
        self.stdout.write(self.style.SUCCESS(f"  {etiquette} : publiée"))
