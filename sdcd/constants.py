"""
Constantes du Système de design RDC.

Reprend la structure de `dsfr.constants` — mêmes noms, mêmes formes — pour que
les modèles Wagtail qui s'y réfèrent n'aient à changer que le module importé.
Les valeurs, elles, sont celles du SDCD.
"""

# Ces listes servent à choisir un FOND de section ou de bloc. Elles nommaient
# jusqu'ici des couleurs pleines — « Bleu d'action », « Filet » — dont aucune
# n'est lisible sous du texte ; et les gabarits construisaient de toute façon une
# variable `--background-alt-<valeur>` héritée du DSFR, que le système ne définit
# pas : le fond choisi par le rédacteur ne s'affichait donc pas du tout. Les
# valeurs correspondent désormais aux jetons `--sdcd-fond-<valeur>`, tous
# vérifiés à ≥ 4,5:1 sous --sdcd-texte, en clair comme en sombre.
COLOR_CHOICES_PRIMARY = [
    ("bleu", "Bleu"),
    ("bleu-soutenu", "Bleu soutenu"),
]

COLOR_CHOICES_NEUTRAL = [
    ("gris", "Gris"),
    ("gris-soutenu", "Gris soutenu"),
]

# Couleurs système : ces quatre-là ont un sens normé, ne pas les employer
# à des fins décoratives.
COLOR_CHOICES_SYSTEM = [
    ("succes", "Succès"),
    ("info", "Information"),
    ("alerte", "Avertissement"),
    ("erreur", "Erreur"),
]

# Couleurs d'illustration : décoratives, sans valeur sémantique.
COLOR_CHOICES_ILLUSTRATION = [
    ("chart-1", "Bleu d'État"),
    ("chart-2", "Bleu profond"),
    ("chart-3", "Ocre"),
    ("chart-4", "Vert"),
    ("chart-5", "Rouge"),
    ("chart-6", "Gris"),
]

COLOR_CHOICES = COLOR_CHOICES_PRIMARY + COLOR_CHOICES_NEUTRAL + COLOR_CHOICES_ILLUSTRATION

COLOR_CHOICES_WITH_SYSTEM = COLOR_CHOICES + COLOR_CHOICES_SYSTEM

NOTICE_TYPE_CHOICES = [
    ("info", "Information"),
    ("alerte", "Avertissement"),
    ("erreur", "Alerte"),
]

# Rapports d'image proposés dans l'éditeur.
IMAGE_RATIOS = [
    ("sdcd-ratio-32x9", "32x9"),
    ("sdcd-ratio-16x9", "16x9"),
    ("sdcd-ratio-3x2", "3x2"),
    ("sdcd-ratio-4x3", "4x3"),
    ("sdcd-ratio-1x1", "1x1"),
    ("sdcd-ratio-3x4", "3x4"),
    ("sdcd-ratio-2x3", "2x3"),
]

VIDEO_RATIOS = [
    ("sdcd-ratio-16x9", "16x9"),
    ("sdcd-ratio-4x3", "4x3"),
    ("sdcd-ratio-1x1", "1x1"),
]
