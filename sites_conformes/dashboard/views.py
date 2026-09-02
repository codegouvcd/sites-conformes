from datetime import date

from django.contrib.admin.utils import quote
from django.urls import reverse
from wagtail.admin.admin_url_finder import AdminURLFinder
from wagtail.admin.ui.components import Component
from wagtail.admin.views.account import PasswordResetConfirmView as WagtailPasswordResetConfirmView
from wagtail.models import Site

from sites_conformes.dashboard.forms import DsfrSetPasswordForm
from sites_conformes.dashboard.notifications import get_all_notifications

finder = AdminURLFinder()


class ShortcutsPanel(Component):
    order = 50

    def get_context_data(self, parent_content=None):
        site = Site.objects.filter(is_default_site=True).first()
        home_page = site.root_page
        home_page_edit = reverse("wagtailadmin_pages:edit", args=(quote(home_page.pk),))
        pages_list = reverse("wagtailadmin_explore", args=(quote(home_page.pk),))
        create_page_url = reverse("wagtailadmin_pages:add_subpage", args=(home_page.pk,))
        settings_url = reverse("wagtailsettings:edit", args=["sites_conformes_core", "cmsdsfrconfig", site.pk])
        main_menus_url = reverse("wagtailsnippets_sites_conformes_menus_mainmenu:list")

        return {
            "site": site,
            "home_page_edit": home_page_edit,
            "pages_list": pages_list,
            "create_page": create_page_url,
            "settings_url": settings_url,
            "main_menus": main_menus_url,
        }

    template_name = "wagtailadmin/home/panels/_main_links.html"


shortcuts_panel = ShortcutsPanel()


class TutorialsPanel(Component):
    """Guides du tableau de bord.

    La version d'origine interrogeait sites.beta.gouv.fr pour afficher les
    tutoriels video de Sites Faciles : un appel reseau vers un site francais a
    chaque chargement (cache une semaine), et des vignettes a la marque d'un
    autre Etat sur le tableau de bord d'un site congolais. Les guides sont ceux
    du site vitrine, servis par l'instance publique : aucun appel sortant.
    """

    order = 300
    template_name = "wagtailadmin/home/panels/_tutorials.html"

    GUIDES = [
        ("Créer votre site", "creer-votre-site", "doc-full"),
        ("Le système de design", "systeme-de-design", "view"),
        ("Questions fréquentes", "questions-frequentes", "help"),
    ]

    def get_context_data(self, parent_content=None):
        from django.conf import settings

        base = f"{settings.HOST_PROTO}://{settings.HOST_URL}"
        if getattr(settings, "HOST_PORT", "") and settings.HOST_PORT not in ("80", "443"):
            base = f"{base}:{settings.HOST_PORT}"
        return {
            "tutorials": [
                {"title": titre, "url": f"{base}/{slug}/", "icon": icone}
                for titre, slug, icone in self.GUIDES
            ]
        }


tutorials_panel = TutorialsPanel()


class NotificationPanel(Component):
    order = 20
    template_name = "sites_conformes_admin/panels/_notifications.html"
    panel_id = "notifications"

    def get_context_data(self, parent_context=None):
        notifications = []
        for item in get_all_notifications():
            item = dict(item)
            raw_start_date = item.get("start_date")
            if raw_start_date:
                try:
                    item["start_date"] = date.fromisoformat(raw_start_date)
                except ValueError:
                    pass
            notifications.append(item)
        return {"notifications": notifications}


class PasswordResetConfirmView(WagtailPasswordResetConfirmView):
    # Wagtail hard-codes django.contrib.auth.forms.SetPasswordForm, which isn't DSFR-styled.
    # There's no settings hook for it (unlike WAGTAILADMIN_USER_PASSWORD_RESET_FORM), so the
    # URL below overrides the one from wagtailadmin_urls (matched first by Django).
    form_class = DsfrSetPasswordForm
