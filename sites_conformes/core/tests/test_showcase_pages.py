"""Verifie que la commande du site vitrine construit un site qui rend.

Une commande qui pose du contenu en base ne se verifie pas en la lisant : une
structure de bloc fausse ne se voit qu'a l'execution, et parfois seulement au
rendu. Ces tests l'executent, puis demandent les pages.
"""

from django.core.management import call_command
from django.test import TestCase
from wagtail.models import Page
from wagtail.test.utils import WagtailPageTestCase

from sites_conformes.core.models import ContentPage


class ShowcasePagesTestCase(WagtailPageTestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("create_starter_pages", verbosity=0)
        call_command("create_showcase_pages", verbosity=0)

    def test_les_pages_sont_creees_et_publiees(self):
        for slug in ("creer-votre-site", "systeme-de-design", "questions-frequentes"):
            page = ContentPage.objects.filter(slug=slug).first()
            self.assertIsNotNone(page, f"page {slug} absente")
            self.assertTrue(page.live, f"page {slug} non publiee")

    def test_chaque_page_se_rend(self):
        """Le rendu est la seule preuve qu'une structure de bloc est valide."""
        for slug in ("creer-votre-site", "systeme-de-design", "questions-frequentes"):
            page = ContentPage.objects.get(slug=slug)
            self.assertPageIsRenderable(page)

    def test_l_accueil_se_rend_et_porte_le_contenu_vitrine(self):
        accueil = ContentPage.objects.get(slug="home")
        self.assertPageIsRenderable(accueil)
        reponse = self.client.get(accueil.url)
        contenu = reponse.content.decode()
        self.assertIn("Un site d’État, sans partir de zéro", contenu)
        # Le texte d'attente de create_starter_pages ne doit plus etre la.
        self.assertNotIn("Vous venez de créer un site", contenu)

    def test_les_blocs_rendent_leurs_composants(self):
        """Les composants poses par la commande doivent produire leurs classes.

        Sans cela, une valeur de couleur invalide ou un nom de champ errone
        passerait inapercu : le bloc se rendrait vide, sans erreur.
        """
        reponse = self.client.get(ContentPage.objects.get(slug="systeme-de-design").url)
        contenu = reponse.content.decode()
        for classe in ("sdcd-badge--nouveau", "sdcd-badge--succes", "sdcd-tag--chart-4", "sdcd-highlight"):
            self.assertIn(classe, contenu, f"{classe} absente du rendu")

        reponse = self.client.get(ContentPage.objects.get(slug="creer-votre-site").url)
        contenu = reponse.content.decode()
        self.assertIn("sdcd-stepper__segment--fait", contenu)
        self.assertIn("sdcd-accordion", contenu)

    def test_la_commande_est_idempotente(self):
        """Relancee, la commande ne duplique pas les pages."""
        avant = ContentPage.objects.count()
        call_command("create_showcase_pages", verbosity=0)
        self.assertEqual(ContentPage.objects.count(), avant)

    def test_le_menu_principal_pointe_vers_les_rubriques(self):
        reponse = self.client.get(ContentPage.objects.get(slug="home").url)
        contenu = reponse.content.decode()
        for libelle in ("Créer votre site", "Le système de design", "Questions fréquentes"):
            self.assertIn(libelle, contenu, f"« {libelle} » absent du menu")


class ShowcaseSansSiteDeDepartTestCase(TestCase):
    def test_la_commande_refuse_de_travailler_sur_une_racine_inattendue(self):
        """Sans site de depart, la commande doit le dire plutot que d'echouer plus loin."""
        from io import StringIO

        Page.objects.filter(depth__gt=1).delete()
        erreurs = StringIO()
        call_command("create_showcase_pages", stderr=erreurs, verbosity=0)
        self.assertIn("create_starter_pages", erreurs.getvalue())
