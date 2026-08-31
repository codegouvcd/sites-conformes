"""
Couche formulaires du Système de design RDC. Miroir de `dsfr.forms`.

`SdcdBaseForm` pose les classes du système sur chaque champ visible et choisit
le gabarit de rendu adapté au type de widget.
"""

from pathlib import Path

from django import forms
from django.forms.renderers import DjangoTemplates, get_default_renderer
from django.utils.functional import cached_property

from sdcd.utils import sdcd_input_class_attr


class SdcdDjangoTemplates(DjangoTemplates):
    @cached_property
    def engine(self):  # type: ignore[override]
        return self.backend(
            {
                "APP_DIRS": True,
                "DIRS": [
                    Path(__file__).resolve().parent / self.backend.app_dirname,
                    Path(forms.__path__[0]).resolve() / "templates",  # type: ignore[attr-defined]
                ],
                "NAME": "djangoforms",
                "OPTIONS": {},
            }  # type: ignore[arg-type]
        )


class SdcdBoundField(forms.BoundField):
    @property
    def template_name(self):
        template_name = self.field.template_name or getattr(
            self.field.__class__, "template_name", None
        )
        if template_name:
            return template_name

        match self.widget_type:
            case "checkbox":
                return "sdcd/form_field_snippets/checkbox_snippet.html"
            case "checkboxselectmultiple" | "inlinecheckboxselectmultiple":
                return "sdcd/form_field_snippets/checkboxselectmultiple_snippet.html"
            case "radioselect" | "inlineradioselect":
                return "sdcd/form_field_snippets/radioselect_snippet.html"
            case _:
                # Les widgets exotiques du DSFR (curseur numérique, contrôle
                # segmenté, radio enrichie) n'ont pas d'équivalent SDCD à ce
                # stade : ils retombent sur le champ de saisie standard.
                return "sdcd/form_field_snippets/input_snippet.html"

    def label_tag(self, contents=None, attrs=None, label_suffix=None, tag=None):
        if hasattr(self.field.widget, "sdcd_label_attrs"):
            attrs = {**self.field.widget.sdcd_label_attrs, **(attrs or {})}
        return super().label_tag(contents, attrs, label_suffix, tag)


class SdcdBaseForm(forms.Form):
    """Formulaire de base : applique les classes du système à chaque champ."""

    template_name = "sdcd/form_snippet.html"  # type: ignore[assignment]
    bound_field_class = SdcdBoundField

    @property
    def default_renderer(self):  # type: ignore[override]
        from django.conf import global_settings, settings

        return (
            SdcdDjangoTemplates
            if settings.FORM_RENDERER == global_settings.FORM_RENDERER
            else get_default_renderer()
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            sdcd_input_class_attr(visible)

    def set_autofocus_on_first_error(self):
        """Pose `autofocus` sur le premier champ en erreur.

        Reprend le comportement de `DsfrBaseForm`, que la reecriture de cette
        couche avait perdu : sans lui, apres un envoi refuse, le curseur reste
        en haut de page et l'utilisateur — a la souris comme au clavier — doit
        retrouver seul le champ fautif. `SitesFacilesBaseForm` l'appelle depuis
        son `__init__`.
        """
        if not self.is_bound:
            return
        for nom in self.fields:
            if self.errors.get(nom):
                self.fields[nom].widget.attrs["autofocus"] = ""
                return
