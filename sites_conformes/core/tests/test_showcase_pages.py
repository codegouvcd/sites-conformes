"""Le site vitrine : ce qu'il doit contenir, et ce qu'il doit continuer de faire.

Le premier defaut trouve au navigateur n'aurait pas ete vu par un test de rendu :
la page d'accueil se rendait, mais ne pouvait plus etre editee — des tuiles
pointaient sur des URL relatives, que le champ URL refuse, et les cartes
recevaient une valeur par defaut hors de leurs choix. Chaque page construite est
donc validee bloc par bloc, comme le ferait le formulaire d'edition.
"""

import re
from io import StringIO

from django.core.management import call_command
from django.test import TestCase, override_settings
from wagtail.blocks import StreamBlockValidationError
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from sites_conformes.blog.models import BlogEntryPage, BlogIndexPage
from sites_conformes.core.models import CatalogIndexPage, CmsDsfrConfig, ContentPage
from sites_conformes.events.models import EventEntryPage, EventsIndexPage
from sites_conformes.forms.models import FormPage
from sites_conformes.menus.models import MainMenu, TopMenu

PAGES_ATTENDUES = [
    "documentation", "creer-votre-site", "systeme-de-design", "questions-frequentes",
    "exemples", "page-atterrissage", "site-vitrine", "actualites", "agenda",
    "catalogue-de-services", "formulaire-de-demonstration", "composants",
]


def construire():
    sortie = StringIO()
    call_command("create_starter_pages", stdout=sortie)
    call_command("create_showcase_pages", stdout=sortie)
    return sortie.getvalue()


class SiteVitrineTestCase(WagtailPageTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.sortie = construire()
        cls.site = Site.objects.filter(is_default_site=True).first()
        cls.accueil = cls.site.root_page.specific

    # ---------------------------------------------------------------- structure
    def test_les_pages_sont_creees_et_publiees(self):
        for slug in PAGES_ATTENDUES:
            page = Page.objects.filter(slug=slug).first()
            self.assertIsNotNone(page, f"page {slug} absente")
            self.assertTrue(page.live, f"page {slug} non publiée")

    def test_les_types_de_pages_sont_ceux_des_cas_d_usage(self):
        self.assertIsInstance(Page.objects.get(slug="exemples").specific, CatalogIndexPage)
        self.assertIsInstance(Page.objects.get(slug="documentation").specific, CatalogIndexPage)
        self.assertEqual(Page.objects.get(slug="creer-votre-site").get_parent().slug, "documentation")
        self.assertIsInstance(Page.objects.get(slug="actualites").specific, BlogIndexPage)
        self.assertIsInstance(Page.objects.get(slug="agenda").specific, EventsIndexPage)
        self.assertIsInstance(Page.objects.get(slug="catalogue-de-services").specific, CatalogIndexPage)
        self.assertIsInstance(Page.objects.get(slug="formulaire-de-demonstration").specific, FormPage)

    def test_les_modeles_de_pages_ont_des_slugs_propres(self):
        index = Page.objects.filter(slug="page_templates_index").first()
        if index is None:
            self.skipTest("pas de modeles de pages")
        for page in index.get_children():
            self.assertNotIn("dsfr", page.slug, page.slug)
            self.assertTrue(page.slug.isascii(), page.slug)

    def test_les_rubriques_vivantes_ont_des_entrees(self):
        self.assertEqual(BlogEntryPage.objects.live().count(), 4)
        self.assertEqual(EventEntryPage.objects.live().count(), 4)
        catalogue = Page.objects.get(slug="catalogue-de-services")
        self.assertEqual(catalogue.get_children().live().count(), 4)
        formulaire = Page.objects.get(slug="formulaire-de-demonstration").specific
        types = set(formulaire.form_fields.values_list("field_type", flat=True))
        self.assertGreaterEqual(len(types), 10, f"types de champs : {sorted(types)}")

    def test_les_articles_et_evenements_ont_des_categories_des_etiquettes_et_une_image(self):
        for page in list(BlogEntryPage.objects.all()) + list(EventEntryPage.objects.all()):
            self.assertIsNotNone(page.header_image, f"{page.slug} : pas d'image d'en-tête")
            self.assertTrue(page.tags.exists(), f"{page.slug} : pas d'étiquette")
        for article in BlogEntryPage.objects.all():
            self.assertTrue(article.blog_categories.exists(), f"{article.slug} : pas de catégorie")
        for evenement in EventEntryPage.objects.all():
            self.assertTrue(evenement.event_categories.exists(), f"{evenement.slug} : pas de catégorie")

    # ------------------------------------------------------------------ validite
    def test_chaque_page_est_valide_bloc_par_bloc(self):
        """Ce que le formulaire d'edition verifie : une page qui se rend mais ne
        se laisse plus editer est un defaut, pas un succes."""
        for page in Page.objects.all().exclude(depth__lte=1):
            page = page.specific
            for champ in ("body", "hero"):
                valeur = getattr(page, champ, None)
                if valeur is None or not len(valeur):
                    continue
                try:
                    valeur.stream_block.clean(valeur)
                except StreamBlockValidationError as e:
                    self.fail(f"{page.slug}.{champ} invalide : {e.as_json_data()}")

    def test_chaque_page_se_rend(self):
        # Les modeles de pages a copier vivent hors du site, sans URL : ils ne
        # se rendent pas, leurs copies sous Exemples si.
        for page in Page.objects.live().exclude(depth__lte=1):
            if page.url is None:
                continue
            with self.subTest(page=page.slug):
                self.assertPageIsRenderable(page.specific)

    def test_les_liens_internes_de_l_accueil_sont_des_pages(self):
        for bloc in self.accueil.body:
            if bloc.block_type != "item_grid":
                continue
            for item in bloc.value["items"]:
                lien = item.value.get("link")
                if lien and lien.get("link_type"):
                    self.assertEqual(lien.get("link_type"), "page", f"{item.value.get('title')} : lien externe")

    # ---------------------------------------------------------------- l'en-tete
    def test_l_en_tete_montre_tout_ce_que_le_cms_sait_afficher(self):
        config = CmsDsfrConfig.for_site(self.site)
        self.assertTrue(config.search_bar)
        self.assertTrue(config.header_login_button)
        self.assertTrue(config.theme_modale_button)
        self.assertTrue(config.notice_is_collapsible)
        self.assertTrue(config.show_newsletter_block)
        self.assertTrue(config.show_social_block)
        self.assertEqual(config.social_media_items.count(), 4)
        self.assertTrue(TopMenu.objects.filter(site=self.site).exists())

        contenu = self.client.get("/").content.decode()
        # ri-lock-line : le bouton de connexion de l'en-tete, quel que soit son libelle traduit.
        for attendu in ("sdcd-searchbar", "ri-lock-line", "Site de démonstration", "Exemples",
                        "Exemples de pages", "Exemples de composants", "Documentation",
                        "Facebook", "sdcd-notice"):
            self.assertIn(attendu, contenu, f"« {attendu} » absent de l'accueil rendu")

    def test_les_composants_ont_une_page_publique(self):
        # Les modeles de pages a copier vivent hors du site, sans URL : le menu
        # les reliait par « None ». Leurs copies, sous Exemples, ont une adresse.
        index = CatalogIndexPage.objects.get(slug="composants")
        pages = index.get_children().live()
        self.assertEqual(pages.count(), 10)
        for page in pages:
            self.assertTrue(page.url and page.url.startswith("/exemples/composants/"), page.title)
            self.assertTrue(page.specific.header_image, f"{page.slug} : pas de vignette")
        # L'ordre de l'arbre est celui du catalogue, pas celui des creations.
        from sites_conformes.core.vitrine.composants import PAGES

        self.assertEqual([p.slug for p in pages], [slug for slug, *_ in PAGES])
        # Le contenu est redige, pas copie des modeles amont.
        contenu = self.client.get("/exemples/composants/tuiles/").content.decode()
        self.assertIn("Acte de naissance", contenu)
        self.assertNotIn("Argument #1", contenu)

    def test_aucun_lien_de_l_accueil_ne_pointe_sur_none(self):
        contenu = self.client.get("/").content.decode()
        self.assertNotIn('href="None"', contenu)
        self.assertNotIn('href="#"', contenu.split("<main")[0], "un lien vers « # » dans l'en-tete")

    def test_l_etapier_decrit_l_etat_de_chaque_etape(self):
        fiche = ContentPage.objects.get(slug="acte-de-naissance")
        contenu = self.client.get(fiche.url).content.decode()
        self.assertIn("sdcd-stepper__etape--courante", contenu)
        self.assertIn("sdcd-stepper__etape--avenir", contenu)
        self.assertIn("Étape suivante", contenu)

    def test_le_menu_principal_est_un_mega_menu(self):
        menu = MainMenu.objects.filter(site=self.site).first()
        types = [bloc.block_type for bloc in menu.items]
        self.assertIn("megamenu", types)
        self.assertIn("submenu", types)

    # ------------------------------------------------------------- reproductible
    def test_la_commande_est_idempotente(self):
        avant = (ContentPage.objects.count(), BlogEntryPage.objects.count(), EventEntryPage.objects.count())
        call_command("create_showcase_pages", stdout=StringIO())
        apres = (ContentPage.objects.count(), BlogEntryPage.objects.count(), EventEntryPage.objects.count())
        self.assertEqual(avant, apres)

    def test_l_identite_du_site_est_renseignee(self):
        config = CmsDsfrConfig.for_site(self.site)
        self.assertEqual(config.site_title, "Sites Conformes")
        self.assertIn("Congo", config.footer_brand)
        contenu = self.client.get("/").content.decode()
        self.assertNotIn("Sous-titre du site", contenu)
        self.assertIn("Mentions légales", contenu)


class RacineInattendueTestCase(TestCase):
    def test_la_commande_refuse_de_travailler_sur_une_racine_inattendue(self):
        erreurs = StringIO()
        call_command("create_showcase_pages", stdout=StringIO(), stderr=erreurs)
        self.assertIn("create_starter_pages", erreurs.getvalue())


@override_settings(SF_SERVE_PUBLIC=False)
class ConnexionSurLeDomaineDAdministrationTestCase(TestCase):
    """La page de connexion heritait de l'en-tete et du pied du site public :
    sur le domaine d'administration, chacun de leurs liens repondait 404."""

    @classmethod
    def setUpTestData(cls):
        construire()

    def test_la_page_de_connexion_ne_porte_aucun_lien_vers_une_page_non_servie(self):
        reponse = self.client.get("/cms-admin/login/")
        self.assertEqual(reponse.status_code, 200)
        contenu = reponse.content.decode()
        self.assertNotIn("sdcd-header__nav", contenu)
        for href in re.findall(r'href="(/[^"#]*)"', contenu):
            if href.startswith("/static/") or href.startswith("/cms-admin/"):
                continue
            self.assertNotEqual(self.client.get(href).status_code, 404, f"{href} répond 404 sur ce domaine")


class TableauDeBordTestCase(TestCase):
    def test_les_guides_ne_font_aucun_appel_sortant(self):
        from sites_conformes.dashboard.views import TutorialsPanel

        guides = TutorialsPanel().get_context_data()["tutorials"]
        self.assertEqual(len(guides), 3)
        for guide in guides:
            self.assertNotIn("beta.gouv.fr", guide["url"])
            self.assertIn("http", guide["url"])
