"""Verifie qu'une instance ne sert que ce qu'on lui a demande de servir.

Deployer le back-office sur son propre domaine n'a d'interet que si le site
public n'y repond pas, et reciproquement. Ces tests figent les deux sens.
"""

from django.conf import settings
from django.http import HttpResponse
from django.test import RequestFactory, TestCase

from sites_conformes.core.middleware import RoleMiddleware


def middleware(public=True, admin=True):
    with_settings = TestCase().settings(SF_SERVE_PUBLIC=public, SF_SERVE_ADMIN=admin)
    with_settings.enable()
    try:
        return RoleMiddleware(lambda r: HttpResponse("servi")), with_settings
    except Exception:
        with_settings.disable()
        raise


class RoleMiddlewareTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.admin = "/" + settings.WAGTAILADMIN_PATH.lstrip("/")

    def reponse(self, chemin, public=True, admin=True):
        mw, ctx = middleware(public, admin)
        try:
            return mw(self.factory.get(chemin))
        finally:
            ctx.disable()

    def test_par_defaut_tout_est_servi(self):
        """Une instance unique doit se comporter exactement comme avant."""
        self.assertEqual(self.reponse("/").status_code, 200)
        self.assertEqual(self.reponse(self.admin).status_code, 200)

    def test_instance_publique_ne_sert_pas_l_administration(self):
        self.assertEqual(self.reponse("/", admin=False).status_code, 200)
        self.assertEqual(self.reponse(self.admin, admin=False).status_code, 404)
        self.assertEqual(self.reponse(self.admin + "login/", admin=False).status_code, 404)
        self.assertEqual(self.reponse("/django-admin/", admin=False).status_code, 404)

    def test_instance_d_administration_ne_sert_pas_le_site_public(self):
        self.assertEqual(self.reponse(self.admin, public=False).status_code, 200)
        self.assertEqual(self.reponse(self.admin + "pages/", public=False).status_code, 200)
        self.assertEqual(self.reponse("/", public=False).status_code, 404)
        self.assertEqual(self.reponse("/contact/", public=False).status_code, 404)

    def test_les_ressources_restent_servies_des_deux_cotes(self):
        """Sans elles, le back-office s'afficherait sans style ni images."""
        for chemin in ("/static/sdcd/styles.css", "/medias/images/x.png", "/db-storage/serve/?name=x"):
            self.assertEqual(self.reponse(chemin, public=False).status_code, 200, chemin)
            self.assertEqual(self.reponse(chemin, admin=False).status_code, 200, chemin)

    def test_refus_en_404_et_non_en_403(self):
        """Une instance qui ne sert pas une partie ne doit pas en reveler l'existence."""
        self.assertEqual(self.reponse(self.admin, admin=False).status_code, 404)
