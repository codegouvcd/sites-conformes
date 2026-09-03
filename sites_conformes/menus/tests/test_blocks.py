from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from sites_conformes.core.models import ContentPage
from sites_conformes.menus.models import FooterBottomMenu, MainMenu, TopMenu


class TopMenuLinkBlockTestCase(WagtailPageTestCase):
    """Tests for MenuLinkWithIconBlock rendered via header_top_menu.html / link.html."""

    def setUp(self):
        home = Page.objects.get(slug="home")
        self.site = Site.objects.get(is_default_site=True)
        self.content_page = home.add_child(instance=ContentPage(title="Page de test", slug="test-page"))
        self.content_page.save()
        self.top_menu = TopMenu.objects.create(site=self.site)

    def test_external_link(self):
        self.top_menu.items = [
            ("link", {"text": "Info Gouv", "external_url": "https://info.gouv.fr", "link_type": "external_url"})
        ]
        self.top_menu.save()

        response = self.client.get(self.content_page.url)
        html = response.content.decode()

        # L'assertion d'origine visait un lien du pied de page vers
        # www.info.gouv.fr, present dans le contenu de demarrage amont. Ce lien a
        # ete retire : un site d'Etat congolais n'a pas a renvoyer vers
        # l'administration francaise. Le test verifie desormais ce qu'annonce son
        # nom — le rendu de l'entree de menu haut creee juste au-dessus.
        self.assertInHTML(
            """
            <a class="sdcd-button sdcd-button--tertiaire sdcd-button--sm"
               href="https://info.gouv.fr"
               target="_blank"
               rel="noopener noreferrer">Info Gouv
              <span class="sdcd-lecteur-seul">Ouvre une nouvelle fenêtre</span>
            </a>
            """,
            html,
        )

    def test_page_link(self):
        self.top_menu.items = [("link", {"text": "Page de test", "page": self.content_page, "link_type": "page"})]
        self.top_menu.save()

        response = self.client.get(self.content_page.url)
        html = response.content.decode()

        self.assertInHTML(
            f'<a class="sdcd-button sdcd-button--tertiaire sdcd-button--sm" href="{self.content_page.url}" aria-current="page">Page de test</a>', html
        )
        self.assertNotInHTML(
            f"""<a class="sdcd-button sdcd-button--tertiaire sdcd-button--sm" href="{self.content_page.url}"
            target="_blank" aria-current="page">Page de test</a>""",
            html,
        )


class FooterBottomMenuLinkBlockTestCase(WagtailPageTestCase):
    """Tests for FooterBottomLinkBlock rendered via footer_bottom_menu.html / footer_bottom_link.html."""

    def setUp(self):
        home = Page.objects.get(slug="home")
        self.site = Site.objects.get(is_default_site=True)
        self.content_page = home.add_child(instance=ContentPage(title="Page de test", slug="test-page"))
        self.content_page.save()
        self.footer_menu = FooterBottomMenu.objects.create(site=self.site)

    def test_external_link(self):
        self.footer_menu.items = [
            (
                "link",
                {"text": "Mentions légales", "external_url": "https://info.gouv.fr", "link_type": "external_url"},
            )
        ]
        self.footer_menu.save()

        response = self.client.get(self.content_page.url)
        html = response.content.decode()

        self.assertInHTML(
            '<a class="sdcd-footer__lien" href="https://info.gouv.fr" target="_blank" rel="noopener noreferrer">'
            "Mentions légales"
            '<span class="sdcd-lecteur-seul">Ouvre une nouvelle fenêtre</span>'
            "</a>",
            html,
        )

    def test_page_link(self):

        response = self.client.get(self.content_page.url)
        html = response.content.decode()

        self.assertInHTML(
            """<a class="sdcd-footer__lien" href="/plan-du-site/">Plan du site</a>""",
            html,
        )


class MainMenuLinkBlockTestCase(WagtailPageTestCase):
    """Tests for MainMenuLinkBlock rendered via header_main_menu.html / main_menu_link.html."""

    def setUp(self):
        home = Page.objects.get(slug="home")
        self.site = Site.objects.get(is_default_site=True)
        self.content_page = home.add_child(instance=ContentPage(title="Page de test", slug="test-page"))
        self.content_page.save()
        self.main_menu = MainMenu.objects.create(site=self.site)

    def test_external_link(self):
        self.main_menu.items = [
            ("link", {"text": "Info Gouv", "external_url": "https://info.gouv.fr", "link_type": "external_url"})
        ]
        self.main_menu.save()

        response = self.client.get(self.content_page.url)
        html = response.content.decode()

        self.assertInHTML(
            '<a class="sdcd-header__lien" href="https://info.gouv.fr" target="_blank" rel="noopener noreferrer">'
            "Info Gouv"
            '<span class="sdcd-lecteur-seul">Ouvre une nouvelle fenêtre</span>'
            "</a>",
            html,
        )

    def test_page_link(self):
        self.main_menu.items = [("link", {"text": "Page de test", "page": self.content_page, "link_type": "page"})]
        self.main_menu.save()

        response = self.client.get(self.content_page.url)
        html = response.content.decode()

        self.assertInHTML(
            f'<a class="sdcd-header__lien" href="{self.content_page.url}" aria-current="page">Page de test</a>',
            html,
        )

        self.assertNotInHTML(
            f"""<a class="sdcd-header__lien" href="{self.content_page.url}"
            target="_blank" aria-current="page">Page de test</a>""",
            html,
        )


class MainMenuSubmenuBlockTestCase(WagtailPageTestCase):
    """Tests for MainMenuSubmenuBlock rendered via main_menu_submenu.html."""

    def setUp(self):
        home = Page.objects.get(slug="home")
        self.site = Site.objects.get(is_default_site=True)
        self.linked_page = home.add_child(instance=ContentPage(title="Page liée", slug="linked-page"))
        self.linked_page.save()
        self.other_page = home.add_child(instance=ContentPage(title="Autre page", slug="other-page"))
        self.other_page.save()
        self.main_menu = MainMenu.objects.create(site=self.site)
        self.main_menu.items = [
            (
                "submenu",
                {
                    "label": "Mon sous-menu",
                    "links": [("link", {"text": "Page liée", "page": self.linked_page, "link_type": "page"})],
                },
            )
        ]
        self.main_menu.save()

    def test_submenu_button(self):
        response = self.client.get(self.other_page.url)
        html = response.content.decode()

        self.assertInHTML(
            '<button aria-expanded="false" aria-controls="collapse-menu-mon-sous-menu"'
            ' type="button" class="sdcd-header__lien">Mon sous-menu</button>',
            html,
        )

    def test_submenu_collapse_div_contains_link(self):
        response = self.client.get(self.other_page.url)
        html = response.content.decode()

        self.assertInHTML(
            '<div class="sdcd-repli sdcd-dropdown__menu" id="collapse-menu-mon-sous-menu" hidden>'
            '<ul class="sdcd-dropdown__liste">'
            '<li class="sdcd-nav__item">'
            f'<a class="sdcd-header__lien" href="{self.linked_page.url}">Page liée</a>'
            "</li>"
            "</ul>"
            "</div>",
            html,
        )

    def test_submenu_button_has_aria_current_when_on_linked_page(self):
        response = self.client.get(self.linked_page.url)
        html = response.content.decode()

        self.assertInHTML(
            '<button aria-current="true" aria-expanded="false" aria-controls="collapse-menu-mon-sous-menu"'
            ' type="button" class="sdcd-header__lien">Mon sous-menu</button>',
            html,
        )

    def test_submenu_button_has_no_aria_current_when_on_other_page(self):
        response = self.client.get(self.other_page.url)
        html = response.content.decode()

        self.assertNotInHTML(
            '<button aria-current="true" class="sdcd-header__lien">Mon sous-menu</button>',
            html,
        )


class MainMenuMegamenuBlockTestCase(WagtailPageTestCase):
    """Tests for MainMenuMegamenuBlock rendered via main_menu_megamenu.html."""

    def setUp(self):
        home = Page.objects.get(slug="home")
        self.site = Site.objects.get(is_default_site=True)
        self.column_page = home.add_child(instance=ContentPage(title="Page de colonne", slug="column-page"))
        self.column_page.save()
        self.other_page = home.add_child(instance=ContentPage(title="Autre page", slug="other-page"))
        self.other_page.save()
        self.section_page = home.add_child(instance=ContentPage(title="Voir la section", slug="section-page"))
        self.section_page.save()
        self.main_menu = MainMenu.objects.create(site=self.site)
        self.main_menu.items = [
            (
                "megamenu",
                {
                    "label": "Ma section",
                    "description": "Description de la section",
                    "main_link": {
                        "text": "Voir la section",
                        "page": self.section_page,
                        "link_type": "page",
                    },
                    "columns": [
                        (
                            "column",
                            {
                                "label": "Colonne 1",
                                "links": [
                                    (
                                        "link",
                                        {"text": "Page de colonne", "page": self.column_page, "link_type": "page"},
                                    )
                                ],
                            },
                        )
                    ],
                },
            )
        ]
        self.main_menu.save()

    def test_megamenu_button(self):
        response = self.client.get(self.other_page.url)
        html = response.content.decode()

        self.assertInHTML(
            '<button aria-expanded="false" aria-controls="collapse-menu-ma-section"'
            ' type="button" class="sdcd-header__lien">Ma section</button>',
            html,
        )

    def test_megamenu_leader_section(self):
        response = self.client.get(self.other_page.url)
        html = response.content.decode()

        # Le titre est un paragraphe (pas de h4 dans la navigation, avant le h1)
        # et la description n'est plus masquee par une classe : c'est le panneau
        # mobile qui la retire.
        self.assertInHTML(
            f"""
            <div class="sdcd-megamenu__intro">
            <p class="sdcd-megamenu__titre">Ma section</p>
            <p>Description de la section</p>
            <a class="sdcd-lien ri-arrow-right-line sdcd-lien--icone-droite sdcd-lien--aligne"
                          href="{self.section_page.url}">Voir la section</a>
            </div>""",
            html,
        )

    def test_megamenu_column_with_link(self):
        response = self.client.get(self.other_page.url)
        html = response.content.decode()

        # L'intitule de colonne n'est pas un lien (le bloc ne lui associe aucune
        # page ; « # » remontait en haut de page) et la liste est celle du
        # mega-menu, pas celle d'une liste deroulante.
        self.assertInHTML(
            '<div class="sdcd-col-12 sdcd-col-lg-3">'
            '<p class="sdcd-megamenu__categorie">Colonne 1</p>'
            '<ul class="sdcd-megamenu__liste">'
            "<li>"
            f'<a class="sdcd-header__lien" href="{self.column_page.url}">Page de colonne</a>'
            "</li>"
            "</ul>"
            "</div>",
            html,
        )

    def test_megamenu_button_has_aria_current_when_on_column_linked_page(self):
        response = self.client.get(self.column_page.url)
        html = response.content.decode()

        self.assertInHTML(
            '<button aria-current="true" aria-expanded="false" aria-controls="collapse-menu-ma-section"'
            ' type="button" class="sdcd-header__lien">Ma section</button>',
            html,
        )

    def test_megamenu_button_has_no_aria_current_when_on_other_page(self):
        response = self.client.get(self.other_page.url)
        html = response.content.decode()

        self.assertNotInHTML(
            '<button aria-current="true" class="sdcd-header__lien">Ma section</button>',
            html,
        )

    def test_megamenu_close_button(self):
        response = self.client.get(self.other_page.url)
        html = response.content.decode()

        # `data-fr-js-collapse-button` etait le crochet du JavaScript du DSFR,
        # parti avec lui : le bouton ne fermait plus rien. sdcd.js replie la region
        # nommee par `data-sdcd-replie`.
        self.assertInHTML(
            '<button type="button" class="sdcd-lien--fermer sdcd-lien"'
            ' data-sdcd-replie="collapse-menu-ma-section">Fermer</button>',
            html,
        )
