import logging

from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.utils.cache import patch_vary_headers

from sites_conformes.core.models import CmsDsfrConfig

logger = logging.getLogger(__name__)

# Sec-Fetch-Dest values indicating the document is loaded inside a frame.
# The header is sent by Chrome 80+, Firefox 90+ and Safari 16.4+. Older
# browsers never send it and always get the standalone template, even when
# embedded (graceful degradation: the page still renders, with full chrome).
_FRAME_FETCH_DESTS = ("iframe", "frame")


class IframeMiddleware:
    """
    Iframe embedding support et politique de securite de contenu.

    - flags requests coming from an iframe (``request.iframe``) so templates
      can render a stripped-down layout,
    - emits the ``Content-Security-Policy`` header, whose ``frame-ancestors``
      directive is built from the per-site ``CmsDsfrConfig.iframe_allow_origins``
      setting.

    Ce middleware ecrit l'en-tete en entier. C'est pourquoi la politique complete
    est composee ici plutot que par ``django.middleware.csp`` : les deux
    ecriraient le meme en-tete, et la derniere ecriture gagnerait. Jusqu'ici seul
    ``frame-ancestors`` etait emis — une protection anti-cadrage, pas une
    politique de scripts.

    La politique ne s'applique qu'aux pages publiques. Le back-office de Wagtail
    repose sur des scripts en ligne : lui imposer ``script-src 'self'`` le
    casserait. Il conserve donc ``frame-ancestors`` seul, ce qui est une limite
    assumee et signalee, pas un oubli.

    ``X-Frame-Options`` is intentionally left to Django's
    ``XFrameOptionsMiddleware`` (see ``X_FRAME_OPTIONS`` in settings): it only
    acts as a legacy fallback, as browsers supporting ``frame-ancestors``
    ignore it.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        request.iframe = request.headers.get("Sec-Fetch-Dest") in _FRAME_FETCH_DESTS

        response = self.get_response(request)

        self._set_content_security_policy(request, response)
        patch_vary_headers(response, ("Sec-Fetch-Dest",))

        return response

    def _set_content_security_policy(self, request: HttpRequest, response: HttpResponse) -> None:
        ancetres = self._frame_ancestors(request)
        directives = [f"frame-ancestors {ancetres}"]

        # Le back-office garde la seule protection anti-cadrage : voir la
        # docstring de la classe.
        if not self._is_admin_request(request):
            for nom, valeurs in getattr(settings, "SF_CSP_DIRECTIVES", {}).items():
                if valeurs:
                    directives.append("%s %s" % (nom, " ".join(valeurs)))

        response.headers["Content-Security-Policy"] = "; ".join(directives)

    def _frame_ancestors(self, request: HttpRequest) -> str:
        value = "'self'"

        # Never relax framing for the back office: only front-office pages
        # may be embedded by the configured external origins.
        if not self._is_admin_request(request):
            try:
                config = CmsDsfrConfig.for_request(request)
                origins = [line.strip() for line in config.iframe_allow_origins.splitlines() if line.strip()]
                if origins:
                    value = " ".join(["'self'", *(f"https://{origin}" for origin in origins)])
            except Exception:
                # Fail closed, but never silently: a misconfiguration here
                # would otherwise disable embedding without any trace.
                logger.warning(
                    "IframeMiddleware: could not resolve allowed iframe origins, falling back to 'self'",
                    exc_info=True,
                )

        return value

    @staticmethod
    def _is_admin_request(request: HttpRequest) -> bool:
        admin_path = settings.WAGTAILADMIN_PATH.lstrip("/")
        return request.path_info.lstrip("/").startswith(admin_path)


class RoleMiddleware:
    """Restreint ce qu'une instance sert : le site public, le back-office, ou les deux.

    Deployer le back-office sur son propre domaine demande deux instances de la
    meme application. Sans garde-fou, chacune servirait tout : le site public
    serait joignable sur l'adresse d'administration, et l'administration sur
    l'adresse publique — l'interet de la separation disparait.

    Deux reglages, tous deux vrais par defaut : une instance unique se comporte
    donc exactement comme avant.

      SF_SERVE_PUBLIC=0   l'instance ne sert que le back-office
      SF_SERVE_ADMIN=0    l'instance ne sert que le site public

    Le filtrage porte sur la VUE resolue, et non sur le chemin. Une premiere
    version comparait des prefixes d'URL, avec une liste de chemins toujours
    servis. Elle a bloque `/jsi18n/` — le catalogue de traductions JavaScript,
    que le back-office charge et qui ne vit sous aucun de ces prefixes. Toute
    liste de chemins ecrite a la main aurait le meme defaut : elle oublie ce
    qu'on n'a pas pense a y mettre.

    On ne refuse donc que ce qu'on sait devoir refuser : le rendu des pages
    Wagtail d'un cote, les vues d'administration de l'autre. Tout le reste —
    fichiers statiques, medias, catalogues, sante — passe sans avoir a etre
    enumere.

    Les routes restent declarees des deux cotes : `reverse` doit continuer de
    resoudre les URL d'administration, plusieurs commandes de gestion en
    dependent, et les liens « voir en ligne » designent le site public.
    """

    # Vues qui rendent le site public.
    VUES_PUBLIQUES = ("wagtail.views", "wagtail.contrib.sitemaps")
    # Vues qui composent le back-office.
    VUES_ADMIN = ("wagtail.admin", "django.contrib.admin", "wagtail.snippets", "wagtail.users")

    def __init__(self, get_response):
        self.get_response = get_response

    # Les reglages sont relus a chaque requete, et non figes a la construction :
    # un middleware n'est instancie qu'une fois par processus, et une valeur
    # capturee la ne suivrait ni `override_settings` en test, ni un changement de
    # configuration a chaud. Le cout est celui de deux acces a un attribut.
    @property
    def sert_public(self):
        return getattr(settings, "SF_SERVE_PUBLIC", True)

    @property
    def sert_admin(self):
        return getattr(settings, "SF_SERVE_ADMIN", True)

    def __call__(self, request):
        response = self.get_response(request)
        if not self.sert_public:
            # Le domaine d'administration n'a rien a faire dans un index.
            response.headers.setdefault("X-Robots-Tag", "noindex, nofollow")
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if self.sert_public and self.sert_admin:
            return None

        module = getattr(view_func, "__module__", "") or ""
        # Une vue basee sur une classe porte le module de sa classe.
        module = getattr(getattr(view_func, "view_class", None), "__module__", module)

        if not self.sert_admin and module.startswith(self.VUES_ADMIN):
            return self.refuser(request, "administration")
        if not self.sert_public and module.startswith(self.VUES_PUBLIQUES):
            return self.refuser(request, "site public")
        return None

    @staticmethod
    def refuser(request, quoi):
        # 404 plutot que 403 : une instance qui ne sert pas cette partie ne doit
        # pas en reveler l'existence. Le journal, lui, dit pourquoi.
        logger.info("RoleMiddleware : %s non servi par cette instance (%s)", quoi, request.path_info)
        return HttpResponseNotFound()
