"""Verifie qu'une instance ne sert que ce qu'on lui a demande de servir.

Deployer le back-office sur son propre domaine n'a d'interet que si le site
public n'y repond pas, et reciproquement. Ces tests figent les deux sens, et
surtout ce qui doit continuer de passer des deux cotes : une premiere version du
filtre bloquait `/jsi18n/`, le catalogue de traductions que le back-office
charge — defaut invisible tant qu'on ne regarde pas la console du navigateur.

On passe par le client de test plutot que par une requete fabriquee : c'est la
resolution d'URL reelle qui est en jeu.
"""

from django.test import TestCase, override_settings
from django.urls import reverse
from wagtail.models import Page


class RolesTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.accueil = Page.objects.get(slug="home")

    @property
    def admin(self):
        """L'URL reelle du back-office, resolue plutot que devinee.

        La composer a la main a partir de WAGTAILADMIN_PATH donnait des chemins
        inexistants : `/cms-admin/` nu n'est pas une route, et `/cms-admin/login/`
        disparait lorsque ProConnect remplace la connexion locale.
        """
        return reverse("wagtailadmin_home")

    # ------------------------------------------------------------- par defaut
    def test_par_defaut_tout_est_servi(self):
        """Une instance unique doit se comporter exactement comme avant."""
        self.assertEqual(self.client.get("/").status_code, 200)
        self.assertEqual(self.client.get(self.admin).status_code, 302)

    # --------------------------------------------------- instance d'administration
    @override_settings(SF_SERVE_PUBLIC=False)
    def test_l_administration_ne_sert_pas_les_pages_publiques(self):
        self.assertEqual(self.client.get("/").status_code, 404)

    @override_settings(SF_SERVE_PUBLIC=False)
    def test_l_administration_sert_son_back_office(self):
        # Non connecte, Wagtail redirige vers la connexion : un 302, et non le
        # 404 que poserait le filtre.
        self.assertEqual(self.client.get(self.admin).status_code, 302)

    @override_settings(SF_SERVE_PUBLIC=False)
    def test_le_catalogue_de_traductions_reste_servi(self):
        """Defaut de la premiere version : `/jsi18n/` ne vit sous aucun prefixe
        d'administration, et une liste de chemins ecrite a la main l'oubliait.
        Le back-office le charge, et sans lui la console se remplit d'erreurs."""
        self.assertEqual(self.client.get("/jsi18n/").status_code, 200)

    @override_settings(SF_SERVE_PUBLIC=False)
    def test_le_domaine_d_administration_demande_a_ne_pas_etre_indexe(self):
        reponse = self.client.get(self.admin)
        self.assertIn("noindex", reponse.headers.get("X-Robots-Tag", ""))

    # ---------------------------------------------------------- instance publique
    @override_settings(SF_SERVE_ADMIN=False)
    def test_l_instance_publique_ne_sert_pas_l_administration(self):
        self.assertEqual(self.client.get(self.admin).status_code, 404)

    @override_settings(SF_SERVE_ADMIN=False)
    def test_l_instance_publique_sert_ses_pages(self):
        self.assertEqual(self.client.get("/").status_code, 200)

    @override_settings(SF_SERVE_ADMIN=False)
    def test_l_instance_publique_reste_indexable(self):
        self.assertNotIn("noindex", self.client.get("/").headers.get("X-Robots-Tag", ""))

    # ------------------------------------------------------------------- forme
    @override_settings(SF_SERVE_ADMIN=False)
    def test_refus_en_404_et_non_en_403(self):
        """Une instance ne doit pas reveler ce qu'elle ne sert pas."""
        self.assertEqual(self.client.get(self.admin).status_code, 404)

    @override_settings(SF_SERVE_PUBLIC=False)
    def test_reverse_fonctionne_encore_sur_l_instance_d_administration(self):
        """Les routes restent declarees : plusieurs commandes en dependent."""
        self.assertTrue(reverse("wagtailadmin_home"))
