"""Utilitaires du Système de design RDC. Miroir de `dsfr.utils`."""

import functools

from django.forms import widgets
from django.forms.boundfield import BoundField
from django.templatetags.static import static
from django.utils.functional import keep_lazy_text


def parse_tag_args(args, kwargs, allowed_keys: list) -> dict:
    """
    Autorise l'appel d'un tag soit avec un dictionnaire, soit avec des
    paramètres nommés. Reproduit le comportement de django-dsfr.
    """
    tag_data = {}

    if args:
        tag_data = args[0].copy()

    for k in kwargs:
        if k in allowed_keys:
            tag_data[k] = kwargs[k]

    return tag_data


def generate_pagination_list(page_obj, on_each_side: int = 2, on_ends: int = 1):
    """
    Construit la liste des numéros de page à afficher, en remplaçant les
    intervalles par « … ». Attaché à `page_obj.pages_list`.
    """
    paginator = page_obj.paginator
    total = paginator.num_pages
    courant = page_obj.number

    if total <= (on_each_side + on_ends) * 2 + 1:
        page_obj.pages_list = list(paginator.page_range)
        return page_obj

    pages = set()
    for i in range(1, on_ends + 1):
        pages.add(i)
        pages.add(total - i + 1)
    for i in range(courant - on_each_side, courant + on_each_side + 1):
        if 1 <= i <= total:
            pages.add(i)

    ordonnees = sorted(pages)
    avec_separateurs: list = [ordonnees[0]]
    for i in range(1, len(ordonnees)):
        ecart = ordonnees[i] - ordonnees[i - 1]
        # Si « … » ne remplacerait qu'une seule valeur, autant l'afficher.
        if ecart == 2:
            avec_separateurs.append(ordonnees[i - 1] + 1)
        elif ecart > 1:
            avec_separateurs.append("…")
        avec_separateurs.append(ordonnees[i])

    page_obj.pages_list = avec_separateurs
    return page_obj


def sdcd_input_class_attr(bf: BoundField | str):
    """
    Pose les classes du système sur un champ de formulaire, et relie le message
    d'erreur au champ par `aria-describedby`.
    """
    if bf == "":
        raise AttributeError("Nom de champ invalide passé à sdcd_input_class_attr.")

    if bf.is_hidden:
        return bf

    if "class" not in bf.field.widget.attrs:
        bf.field.label_suffix = ""
        if isinstance(bf.field.widget, (widgets.Select, widgets.SelectMultiple)):
            bf.field.widget.attrs["class"] = "sdcd-select__champ"
            bf.field.widget.group_class = "sdcd-champ"
        elif isinstance(bf.field.widget, widgets.RadioSelect):
            bf.field.widget.group_class = "sdcd-champ"
        elif isinstance(bf.field.widget, widgets.CheckboxSelectMultiple):
            pass
        elif not isinstance(
            bf.field.widget,
            (widgets.CheckboxInput, widgets.FileInput, widgets.ClearableFileInput),
        ):
            bf.field.widget.attrs["class"] = "sdcd-input__champ"

    # bf.errors déclenche la validation : on interroge form._errors pour l'éviter.
    if bf.form._errors and bf.errors:
        bf.field.widget.attrs.update(
            {"aria-invalid": "true", "aria-describedby": f"{bf.auto_id}-desc-error"}
        )

    return bf


def lazy_static(path):
    """Équivalent différé du tag `{% static %}`, utilisable hors gabarit."""
    return keep_lazy_text(functools.partial(static, path))
