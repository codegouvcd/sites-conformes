from django.utils.translation import gettext_lazy as _

HEADER_FIELDS = [
    "header_image",
    "header_with_title",
    "header_color_class",
    "header_large",
    "header_darken",
    "header_cta_text",
    "header_cta_buttons",
]

BUTTON_TYPE_CHOICES = (
    ("sdcd-button sdcd-button--primaire", _("Primary")),
    ("sdcd-button sdcd-button--secondaire", _("Secundary")),
    ("sdcd-button sdcd-button--tertiaire-bordure", _("Tertiary")),
    ("sdcd-button sdcd-button--tertiaire", _("Tertiary without border")),
)

BUTTON_ICON_SIDE = (
    ("sdcd-button--icone-gauche", _("Left")),
    ("sdcd-button--icone-droite", _("Right")),
)

BUTTONS_ALIGN_CHOICES = (
    ("", _("Left")),
    ("sdcd-boutons--centre", _("Center")),
    ("sdcd-boutons--droite", _("Right")),
    ("sdcd-boutons--droite sdcd-boutons--enligne-inverse", _("Right (reverse order on desktop)")),
)

GRID_3_4_6_CHOICES = [
    ("3", "3/12"),
    ("4", "4/12"),
    ("6", "6/12"),
]

GRID_6_8_12_CHOICES = [
    ("6", _("small")),
    ("8", _("medium")),
    ("12", _("large")),
]

GRID_HORIZONTAL_ALIGN_CHOICES = [
    ("left", _("Left")),
    ("center", _("Center")),
    ("right", _("Right")),
]

GRID_VERTICAL_ALIGN_CHOICES = [
    ("top", _("Top")),
    ("middle", _("Middle")),
    ("bottom", _("Bottom")),
]

HEADING_CHOICES = [
    ("h2", _("Heading 2")),
    ("h3", _("Heading 3")),
    ("h4", _("Heading 4")),
    ("h5", _("Heading 5")),
    ("h6", _("Heading 6")),
    ("p", _("Paragraph")),
]

HEADING_CHOICES_2_5 = [
    ("h2", _("Heading 2")),
    ("h3", _("Heading 3")),
    ("h4", _("Heading 4")),
    ("h5", _("Heading 5")),
]

HORIZONTAL_CARD_IMAGE_RATIOS = [
    ("sdcd-card--horizontal-tiers", "1/3"),
    ("sdcd-card--horizontal-moitie", "50/50"),
]

LEVEL_CHOICES = [
    ("error", _("Error")),
    ("success", _("Success")),
    ("info", _("Information")),
    ("warning", _("Warning")),
]

EXTRA_LIMITED_RICHTEXTFIELD_FEATURES = [
    "bold",
    "italic",
    "link",
    "document-link",
]

LIMITED_RICHTEXTFIELD_FEATURES = [
    "bold",
    "italic",
    "link",
    "document-link",
    "superscript",
    "subscript",
    "strikethrough",
    "text-left",
    "text-center",
    "text-right",
]

LIMITED_RICHTEXTFIELD_FEATURES_WITHOUT_LINKS = [
    "bold",
    "italic",
    "superscript",
    "subscript",
    "strikethrough",
]

LIMITED_RICHTEXTFIELD_FEATURES_WITH_HEADINGS = [
    "bold",
    "italic",
    "link",
    "document-link",
    "strikethrough",
    "h2",
    "h3",
    "h4",
]

LINK_SIZE_CHOICES = [
    ("sdcd-lien--sm", _("Small")),
    ("", _("Medium")),
    ("sdcd-lien--lg", _("Large")),
]

LINK_ICON_CHOICES = [
    ("", _("No icon")),
    ("ri-arrow-right-line sdcd-lien--icone-droite", _("Icon on the right side")),
    ("ri-arrow-right-line sdcd-lien--icone-gauche", _("Icon on the left side")),
]

MEDIA_WIDTH_CHOICES = [
    ("sdcd-media--sm", _("Small")),
    ("", _("Medium")),
    ("sdcd-media--lg", _("Large")),
]

TEXT_SIZE_CHOICES = [
    ("sdcd-texte-sm", _("Small")),
    ("", _("Medium")),
    ("sdcd-texte-lg", _("Large")),
]

ALIGN_HORIZONTAL_CHOICES = [
    ("left", _("Left")),
    ("right", _("Right")),
]

ALIGN_HORIZONTAL_CHOICES_EXTENDED = [
    ("left", _("Left")),
    ("", _("Center")),
    ("right", _("Right")),
]

ALIGN_VERTICAL_CHOICES = [
    ("top", _("Top")),
    ("bottom", _("Bottom")),
]


ALIGN_VERTICAL_CHOICES_EXTENDED = [
    ("top", _("Top")),
    ("middle", _("Middle")),
    ("bottom", _("Bottom")),
]

TEMPLATE_EXAMPLE_BUTTON_LIST = [
    {
        "link_type": "external_url",
        "text": "Nous contacter",
        "external_url": "https://github.com/codegouvcd/sites-conformes/issues",
        "button_type": "sdcd-button sdcd-button--primaire",
        "icon_side": "--",
        "anchor": "",
    },
    {
        "link_type": "external_url",
        "text": "Voir la vidéo",
        "external_url": "https://tube.numerique.gouv.fr/",
        "button_type": "sdcd-button sdcd-button--secondaire",
        "icon_side": "--",
        "anchor": "",
    },
]

TEMPLATE_EXAMPLE_TAG_BADGE_LIST = [
    (
        "tags",
        [
            (
                "tag",
                {
                    "label": "Site vitrine",
                    "is_small": False,
                    "color": "",
                    "icon_class": {},
                    "link": {
                        "link_type": "--",
                        "page": None,
                        "external_url": "",
                        "document": None,
                        "anchor": "",
                    },
                },
            ),
            (
                "tag",
                {
                    "label": "Blog",
                    "is_small": False,
                    "color": "",
                    "icon_class": {},
                    "link": {
                        "link_type": "--",
                        "page": None,
                        "external_url": "",
                        "document": None,
                        "anchor": "",
                    },
                },
            ),
        ],
    ),
]
IMAGE_GRID_SIZE = [("80", _("Small (80px)")), ("140", _("Medium (140px)")), ("200", _("Large (200px)"))]
