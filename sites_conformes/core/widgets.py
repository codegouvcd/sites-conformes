import re
from functools import lru_cache
from pathlib import Path

from django.contrib.staticfiles import finders
from django.forms import Media, widgets

# Une classe d'icone par regle, sous la forme `.ri-nom-line:before { ... }`.
MOTIF_ICONE = re.compile(r"^\.(ri-[a-z0-9-]+):before", re.MULTILINE)


@lru_cache(maxsize=1)
def icones_disponibles() -> tuple[str, ...]:
    """Liste les classes d'icones que le systeme de design embarque.

    La liste est lue dans la feuille livree plutot qu'ecrite en dur : elle suit
    donc la version de Remix Icon fournie par le SDCD, sans risque de proposer au
    rediger une icone que la police ne contient pas.

    Mise en cache pour la duree du processus — le fichier fait 3 000 regles et
    ne change qu'a la mise a jour du systeme.
    """
    chemin = finders.find("sdcd/assets/icones.css")
    if not chemin:
        # Le widget doit rester utilisable meme si la feuille manque : le rediger
        # saisit alors la classe a la main, sans liste de suggestions.
        return ()
    contenu = Path(chemin).read_text(encoding="utf-8", errors="replace")
    return tuple(sorted(set(MOTIF_ICONE.findall(contenu))))


class DsfrIconPickerWidget(widgets.TextInput):
    template_name = "sites_conformes_core/widgets/dsfr-icon-picker-widget.html"

    def __init__(self, attrs=None):
        default_attrs = {}
        attrs = attrs or {}
        attrs = {**default_attrs, **attrs}
        super().__init__(attrs=attrs)

    def get_context(self, name, value, attrs):
        contexte = super().get_context(name, value, attrs)
        contexte["icones"] = icones_disponibles()
        return contexte

    @property
    def media(self):
        # La bibliotheque UniversalIconPicker venait de django-dsfr, desinstalle.
        # Le gabarit l'appelait encore : le bouton « Choisir une icone » ne faisait
        # rien et chaque page d'edition portant un champ d'icone levait une
        # ReferenceError. Le widget s'appuie desormais sur la seule iconographie
        # que le systeme embarque, Remix Icon, avec une liste de suggestions
        # native et un apercu en direct — sans dependance JavaScript externe.
        return Media(
            css={"all": ["css/icon-picker.css", "sdcd/assets/icones.css"]},
            js=["js/icon-picker.js"],
        )
