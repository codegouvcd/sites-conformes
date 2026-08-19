"""
Alias de la bibliothèque de tags.

Chaque `dsfr_x` pointe sur la fonction déjà compilée de `sdcd_x` : le gabarit
rendu est donc celui du SDCD. Aucun gabarit `dsfr/*.html` n'est nécessaire.
"""

from django import template

from sdcd.templatetags import sdcd_tags as _sdcd

register = template.Library()

# Correspondances où le nom diffère : la RDC n'a pas de FranceConnect.
EQUIVALENCES = {
    "dsfr_france_connect": "sdcd_connect",
}


def _alias(nom_sdcd: str) -> str:
    """`sdcd_alert` → `dsfr_alert`. Les auxiliaires gardent leur nom."""
    return "dsfr_" + nom_sdcd[len("sdcd_"):] if nom_sdcd.startswith("sdcd_") else nom_sdcd


for _nom, _fn in _sdcd.register.tags.items():
    register.tags[_alias(_nom)] = _fn

for _nom, _fn in _sdcd.register.filters.items():
    register.filters[_alias(_nom)] = _fn

# Noms sans correspondance mécanique.
for _ancien, _nouveau in EQUIVALENCES.items():
    if _nouveau in _sdcd.register.tags:
        register.tags[_ancien] = _sdcd.register.tags[_nouveau]

# `dsfr_inline` est un filtre côté DSFR ; il l'est aussi côté SDCD.
__all__ = ["register"]
