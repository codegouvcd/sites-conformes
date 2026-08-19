"""Alias des constantes. Les valeurs sont celles du Système de design RDC."""

from sdcd.constants import (  # noqa: F401
    COLOR_CHOICES,
    COLOR_CHOICES_ILLUSTRATION,
    COLOR_CHOICES_NEUTRAL,
    COLOR_CHOICES_PRIMARY,
    COLOR_CHOICES_SYSTEM,
    COLOR_CHOICES_WITH_SYSTEM,
    IMAGE_RATIOS,
    NOTICE_TYPE_CHOICES,
    VIDEO_RATIOS,
)

# Le DSFR expose cette liste ; le SDCD porte les six langues de la République.
DJANGO_DSFR_LANGUAGES = [
    ("fr", "Français"),
    ("en", "English"),
    ("ln", "Lingála"),
    ("sw", "Kiswahili"),
    ("kg", "Kikongo"),
    ("lua", "Tshiluba"),
]
