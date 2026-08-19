"""
Système de design RDC (SDCD) pour Django.

Remplace `django-dsfr`, dont l'usage est réservé aux administrations de l'État
français. L'API reproduit celle de `django-dsfr` afin que le remplacement dans
les gabarits se limite à un renommage.

Correspondance : `{% load dsfr_tags %}` → `{% load sdcd_tags %}`,
`{% dsfr_alert … %}` → `{% sdcd_alert … %}`.
"""

__version__ = "0.1.0"
