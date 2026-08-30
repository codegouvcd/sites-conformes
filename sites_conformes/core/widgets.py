from django.forms import Media, widgets


class DsfrIconPickerWidget(widgets.TextInput):
    template_name = "sites_conformes_core/widgets/dsfr-icon-picker-widget.html"

    def __init__(self, attrs=None):
        default_attrs = {}
        attrs = attrs or {}
        attrs = {**default_attrs, **attrs}
        super().__init__(attrs=attrs)

    @property
    def media(self):
        # La bibliotheque de selection d'icones venait de django-dsfr, desinstalle.
        # Sans elle le widget reste un champ texte fonctionnel : le rediger saisit la
        # classe d'icone a la main. Regression d'ergonomie assumee, preferable a un 500
        # sur toute page d'edition comportant un champ d'icone.
        return Media(
            css={"all": ["css/icon-picker.css", "sdcd/utilitaires.css"]},
        )
