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

    Le filtrage se fait sur le chemin, et non en retirant les routes : `reverse`
    continue de resoudre les URL d'administration meme sur une instance qui ne
    les sert pas. Plusieurs commandes de gestion en dependent, et les liens
    « voir en ligne » du back-office doivent pouvoir designer le site public.

    Ce qui reste toujours servi : les fichiers statiques, les medias, et la vue
    qui sert les fichiers stockes en base. Sans eux, le back-office s'afficherait
    sans style et sans images.
    """

    TOUJOURS_SERVIS = ("/static/", "/medias/", "/db-storage/", "/health", "/favicon.ico")

    def __init__(self, get_response):
        self.get_response = get_response
        self.sert_public = getattr(settings, "SF_SERVE_PUBLIC", True)
        self.sert_admin = getattr(settings, "SF_SERVE_ADMIN", True)
        self.prefixe_admin = "/" + settings.WAGTAILADMIN_PATH.lstrip("/")

    def __call__(self, request):
        if not (self.sert_public and self.sert_admin):
            chemin = request.path_info
            if not chemin.startswith(self.TOUJOURS_SERVIS):
                vise_admin = chemin.startswith(self.prefixe_admin) or chemin.startswith("/django-admin/")
                if vise_admin and not self.sert_admin:
                    return self.refuser(request, "administration")
                if not vise_admin and not self.sert_public:
                    return self.refuser(request, "site public")
        return self.get_response(request)

    @staticmethod
    def refuser(request, quoi):
        # 404 plutot que 403 : une instance qui ne sert pas cette partie ne doit
        # pas en reveler l'existence. Le journal, lui, dit pourquoi.
        logger.info("RoleMiddleware : %s non servi par cette instance (%s)", quoi, request.path_info)
        return HttpResponseNotFound()
