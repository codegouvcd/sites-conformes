"""Cales de compatibilite pour des dependances en retard sur Wagtail.

wagtail-2fa 1.8.0 importe `wagtail.users.widgets.UserListingButton`, retire
dans Wagtail 8 (deprecie depuis 7.1) au profit de
`wagtail.admin.widgets.ListingButton`, de meme signature
(label, url, attrs=..., priority=...). Sans cette cale, le chargement des
crochets de wagtail_2fa echoue et toute l'application avec lui.

La cale enregistre un module de remplacement dans `sys.modules` des les
reglages, mais ne resout `ListingButton` qu'a la premiere lecture de
l'attribut : importer `wagtail.admin.widgets` pendant le chargement des
reglages declencherait « Apps aren't loaded yet » (le module definit des
modeles). Les crochets de wagtail_2fa, eux, sont importes une fois les
applications pretes.

A retirer des que wagtail-2fa corrige https://github.com/labd/wagtail-2fa/issues/283.
"""

import sys
import types


class _ModuleCale(types.ModuleType):
    def __getattr__(self, nom):
        if nom == "UserListingButton":
            from wagtail.admin.widgets import ListingButton

            return ListingButton
        raise AttributeError(nom)


def installer():
    from wagtail import VERSION

    if VERSION < (8, 0) or "wagtail.users.widgets" in sys.modules:
        return
    module = _ModuleCale("wagtail.users.widgets")
    module.__doc__ = "Cale : voir sites_conformes.dashboard.compat."
    sys.modules["wagtail.users.widgets"] = module


installer()
