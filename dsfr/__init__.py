"""
Couche de compatibilité : `dsfr` → `sdcd`.

Ce paquet **remplace** `django-dsfr`. Il en reprend le nom et l'API afin que le
code existant — `{% load dsfr_tags %}`, `from dsfr.constants import …`,
`DsfrBaseForm` — continue de fonctionner sans modification, tout en rendant le
balisage du Système de design RDC.

Pourquoi conserver le nom `dsfr` plutôt que renommer partout : le DSFR nous est
juridiquement interdit, mais le CMS amont y fait référence dans 61 gabarits et
10 modules. Garder l'alias permet de suivre les évolutions de l'amont sans
résoudre un conflit à chaque fusion. Le code nouveau doit employer `sdcd`
directement ; l'alias n'existe que pour l'existant.

Aucune ligne du DSFR n'est reprise ici : seuls les noms le sont.
"""

__version__ = "0.1.0"
__all__ = ["constants", "forms", "utils"]
