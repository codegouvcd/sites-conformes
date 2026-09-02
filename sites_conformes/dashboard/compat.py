"""Cales de compatibilite pour des dependances en retard sur Wagtail.

wagtail-2fa 1.8.0 importe `wagtail.users.widgets.UserListingButton`, retire
dans Wagtail 8 (deprecie depuis 7.1) au profit de
`wagtail.admin.widgets.ListingButton`, de meme signature
(label, url, attrs=..., priority=...). Sans cette cale, le chargement des
crochets de wagtail_2fa echoue et toute l'application avec lui.

La cale enregistre le module manquant dans `sys.modules` avant que Django ne
charge les applications ; elle est importee en tete de `config/settings.py`.
A retirer des que wagtail-2fa corrige https://github.com/labd/wagtail-2fa/issues/283.
"""

import sys
import types


def installer():
    if "wagtail.users.widgets" in sys.modules:
        return
    try:
        import wagtail.users.widgets  # noqa: F401  (existe encore : rien a faire)
        return
    except ImportError:
        pass
    from wagtail.admin.widgets import ListingButton

    module = types.ModuleType("wagtail.users.widgets")
    module.UserListingButton = ListingButton
    module.__doc__ = "Cale : voir sites_conformes.dashboard.compat."
    sys.modules["wagtail.users.widgets"] = module


installer()
